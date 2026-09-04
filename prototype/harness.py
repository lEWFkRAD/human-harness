"""Executable research reference for the shared history layer, Slice 1.1.

This public copy preserves known defects in the historical prototype. It is not
safe for important files and has not passed concurrency, crash-recovery, or
operational-canary acceptance. Read KNOWN_LIMITATIONS.md before running it.

Implemented paths include a supplied preimage hash check, a single-anchor
check, cooperative locking, intent/outcome records, atomic file replacement,
and post-write readback. Their presence is not a claim of complete enforcement.
In particular, some audit writes are unlocked, intent IDs can collide, recovery
can be bypassed, and failed postconditions leave changed content in place.

The audit log is hash-chained, not immutable. Its colocated tip file is a local
checkpoint, not an independent trust anchor. A patch digest is recorded, but no
patch body is retained for replay. Actor labels are not authenticated identity.
VERIFIED derivation, projection recomputation, and allocation are not built.

Public packaging changes isolate demonstration state and require configure()
before library operations. No arguments display help without writing files.
CLI: python -m prototype.harness demo
     python -m prototype.harness verify --events PATH [--tip PATH]
"""

import argparse
import hashlib
import inspect
import json
import os
import sys
import tempfile
import time

if os.name == "nt":
    import msvcrt as _lockmod
else:
    import fcntl as _lockmod


DEFAULTS = {"events": None, "lock": None, "tip": None}
VALIDATOR_VERSION = "slice1.1-public-reference"


def configure(events_path, lock_path=None, tip_path=None):
    """Explicitly select audit state paths; configuration does not create files.

    Paths must belong to a disposable experiment. This prototype does not
    enforce a workspace boundary or protect against non-cooperating writers.
    """
    events_path = os.fspath(events_path)
    DEFAULTS["events"] = os.path.abspath(events_path)
    DEFAULTS["lock"] = os.path.abspath(lock_path or events_path + ".lock")
    DEFAULTS["tip"] = os.path.abspath(tip_path or events_path + ".tip")
    return DEFAULTS


def _require_configuration():
    if not all(DEFAULTS.values()):
        raise RuntimeError("Call configure(events_path) with disposable state paths first")
    return DEFAULTS


def sha(value):
    return hashlib.sha256(
        value if isinstance(value, bytes) else value.encode("utf-8")
    ).hexdigest()


def validator_code_sha():
    """Return a source digest, not proof that this code produced an event."""
    try:
        return sha(inspect.getsource(sys.modules[__name__]))
    except Exception:
        return "unavailable"


def now_utc():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def normalize_target(path):
    # Historical behavior retained: see the case-sensitive Windows limitation.
    path = os.path.realpath(path)
    return path.lower() if os.name == "nt" else path


# ---------------------------------------------------------------- audit log
def _events_path():
    return _require_configuration()["events"]


def _events_iter(path=None):
    path = path or _events_path()
    try:
        stream = open(path, "r", encoding="utf-8")
    except FileNotFoundError:
        return
    with stream:
        for line in stream:
            line = line.strip()
            if line:
                yield json.loads(line)


def _event_body(event):
    return json.dumps(
        {key: value for key, value in event.items() if key != "event_id"},
        sort_keys=True,
    )


def _chain_tip(path=None):
    tip = None
    for event in _events_iter(path):
        tip = event["event_id"]
    return tip


def log_event(kind, payload, path=None):
    """Append an event; this historical helper does NOT acquire a lock.

    Two independent scans choose sequence and predecessor. Concurrent callers
    can fork the chain. Keeping this defect visible is intentional.
    """
    path = path or _events_path()
    event = {
        "seq": sum(1 for _ in _events_iter(path)) + 1,
        "prev_event": _chain_tip(path),
        "ts_utc": now_utc(),
        "kind": kind,
        "validator": {
            "version": VALIDATOR_VERSION,
            "code_sha256": validator_code_sha(),
        },
        "payload": payload,
    }
    event["event_id"] = sha(_event_body(event))
    with open(path, "a", encoding="utf-8") as stream:
        stream.write(json.dumps(event) + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    return event


# ----------------------------------------------------------------- locking
class OpLock:
    """Cooperative process lock used by most, but not all, operation paths.

    The missing-hash refusal bypasses this lock. Direct log/checkpoint calls
    also bypass it. This does not exclude unrelated writers of the target.
    """

    def __init__(self):
        self._file = None

    def __enter__(self):
        self._file = open(_require_configuration()["lock"], "a+b")
        if os.name == "nt":
            self._file.seek(0)
            self._file.write(b"\x00")
            self._file.flush()
            self._file.seek(0)
            _lockmod.locking(self._file.fileno(), _lockmod.LK_LOCK, 1)
        else:
            _lockmod.flock(self._file, _lockmod.LOCK_EX)
        return self

    def __exit__(self, *exc):
        try:
            if os.name == "nt":
                _lockmod.locking(self._file.fileno(), _lockmod.LK_UNLCK, 1)
            else:
                _lockmod.flock(self._file, _lockmod.LOCK_UN)
        finally:
            self._file.close()
            self._file = None


def _read_bytes(path):
    with open(path, "rb") as stream:
        return stream.read()


# ---------------------------------------------------------- dangling intent
def detect_dangling_intent():
    """Find an intent not considered settled by the historical algorithm.

    Known defects: duplicate IDs overwrite prior intents, and a recovery
    detection itself counts as settlement without explicit adjudication.
    """
    intents = {}
    settled = set()
    for event in _events_iter():
        payload = event["payload"]
        if event["kind"] == "edit_intent":
            intents[payload["intent_id"]] = event
        elif event["kind"] in ("edit", "edit_rejected", "edit_recovery"):
            intent_id = payload.get("intent_id") or payload.get("settles_intent")
            if intent_id:
                settled.add(intent_id)
        if event["kind"] == "edit_recovery" and payload.get("settles_intent"):
            settled.add(payload["settles_intent"])
    open_intents = [value for key, value in intents.items() if key not in settled]
    return open_intents[-1] if open_intents else None


# ---------------------------------------------------------------- the edit
def edit_anchor(path, anchor, replacement, writer, expected_sha, postconditions=None):
    """Attempt one anchor edit and return human/agent views of its outcome.

    ``writer`` is an unauthenticated actor label. A missing preimage hash is
    refused and logged without the operation lock (a retained defect).
    Failed postconditions do not roll back landed content. Hard termination or
    logging failure can leave an intent without an outcome; recovery is flawed.
    """
    _require_configuration()
    target = normalize_target(path)
    operation = {"op": "anchor_edit", "target": target, "writer": writer}
    anchor_bytes = anchor.encode("utf-8")
    replacement_bytes = replacement.encode("utf-8")

    if not expected_sha or len(expected_sha) != 64:
        event = log_event(
            "edit_rejected",
            dict(
                operation,
                code="PREIMAGE_HASH_REQUIRED",
                detail="expected_sha is mandatory; target not read or written",
                result="NOT_APPLIED",
            ),
        )
        return _result(
            operation, "NOT_APPLIED:PREIMAGE_HASH_REQUIRED", event,
            None, None, None, None,
            "refusal: supply the preimage hash before editing",
        )

    with OpLock():
        dangling = detect_dangling_intent()
        if dangling is not None:
            event = log_event(
                "edit_recovery",
                dict(
                    operation,
                    settles_intent=dangling["payload"]["intent_id"],
                    code="PRIOR_INTENT_UNRESOLVED",
                    detail="a previous operation recorded intent without outcome; "
                           "its target state is unknown",
                    result="BLOCKED_PENDING_RECOVERY",
                ),
            )
            return _result(
                operation, "NOT_APPLIED:PRIOR_INTENT_UNRESOLVED", event,
                None, None, None, None,
                "a previous edit was interrupted; this attempt is blocked. "
                "Known defect: the next attempt may bypass recovery.",
            )

        try:
            preimage = _read_bytes(target)
        except FileNotFoundError:
            event = log_event(
                "edit_rejected",
                dict(operation, code="TARGET_MISSING", match_count=0, result="NOT_APPLIED"),
            )
            return _result(
                operation, "NOT_APPLIED:TARGET_MISSING", event,
                None, None, 0, None, "file does not exist; nothing written",
            )
        preimage_hash = sha(preimage)
        if expected_sha != preimage_hash:
            event = log_event(
                "edit_rejected",
                dict(
                    operation,
                    code="PREIMAGE_MISMATCH",
                    detail={"expected": expected_sha, "actual": preimage_hash},
                    preimage_sha=preimage_hash,
                    result="NOT_APPLIED",
                ),
            )
            return _result(
                operation, "NOT_APPLIED:PREIMAGE_MISMATCH", event,
                preimage_hash, None, 0, None,
                "file changed since you last read it (or wrong file); nothing written",
            )

        matches = preimage.count(anchor_bytes)
        if matches != 1:
            code = "ANCHOR_NOT_UNIQUE" if matches else "ANCHOR_ABSENT"
            event = log_event(
                "edit_rejected",
                dict(
                    operation, code=code,
                    detail="anchor matched %d time(s); exactly 1 required" % matches,
                    match_count=matches, preimage_sha=preimage_hash, result="NOT_APPLIED",
                ),
            )
            return _result(
                operation, "NOT_APPLIED:" + code, event,
                preimage_hash, None, matches, None,
                "anchor matched %d time(s); exactly 1 required; nothing written" % matches,
            )

        intended = preimage.replace(anchor_bytes, replacement_bytes, 1)
        patch_digest = sha(
            b"%d|" % len(anchor_bytes) + anchor_bytes + b"|" + replacement_bytes
            + b"|" + preimage_hash.encode()
        )
        intent = log_event(
            "edit_intent",
            dict(
                operation, preimage_sha=preimage_hash, match_count=matches,
                patch_digest=patch_digest,
                intent_id=sha(patch_digest + now_utc() + writer),
            ),
        )
        intent_id = intent["payload"]["intent_id"]

        landed = None
        try:
            descriptor, temporary_path = tempfile.mkstemp(
                dir=os.path.dirname(target) or ".", prefix=".harness_", suffix=".tmp"
            )
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(intended)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary_path, target)
            landed = True
            postimage = _read_bytes(target)
            postimage_hash = sha(postimage)
            checks = {
                "length_delta_matches": len(postimage) - len(preimage)
                                        == len(replacement_bytes) - len(anchor_bytes),
                "replacement_present_once": postimage.count(replacement_bytes) == 1,
                "anchor_gone": postimage.count(anchor_bytes) == 0,
                "content_matches_intent": postimage == intended,
            }
            try:
                for name, check in (postconditions or {}).items():
                    checks["user:" + name] = bool(check(postimage))
            except Exception as error:
                checks["user_error"] = repr(error)
            passed = all(value is True for value in checks.values())
            status = "APPLIED" if passed else "APPLIED_FAILED_POSTCONDITION"
            outcome = log_event(
                "edit",
                dict(
                    operation, settles_intent=intent_id,
                    preimage_sha=preimage_hash, result_sha=postimage_hash,
                    match_count=matches, patch_digest=patch_digest,
                    postconditions=checks, result=status,
                ),
            )
            return _result(
                operation, status, outcome, preimage_hash, postimage_hash, matches, checks
            )
        finally:
            # Best-effort exception handling, not a crash-atomic transaction.
            # A killed interpreter cannot run this block. Logging may also fail.
            if landed is True:
                try:
                    settled = any(
                        event["kind"] == "edit"
                        and event["payload"].get("settles_intent") == intent_id
                        for event in _events_iter()
                    )
                except Exception:
                    settled = False
                if not settled:
                    try:
                        postimage = _read_bytes(target)
                        log_event(
                            "edit",
                            dict(
                                operation, settles_intent=intent_id,
                                preimage_sha=preimage_hash, result_sha=sha(postimage),
                                result="APPLIED_UNVERIFIED_RECOVERED",
                            ),
                        )
                    except Exception:
                        pass


def _result(operation, status, event, pre_hash, post_hash, matches, checks, human_msg=None):
    ok = status == "APPLIED"
    human = human_msg or (
        "EDIT APPLIED - verified by readback." if ok else
        "EDIT NOT APPLIED - file unchanged; see agent port."
        if status.startswith("NOT_APPLIED") else
        "EDIT LANDED BUT FAILED A POSTCONDITION - treat as broken; see agent port."
    )
    return {
        "status": status,
        "human_port": human,
        "agent_port": {
            "op": operation,
            "event_id": event["event_id"],
            "prev_event": event["prev_event"],
            "validator": event["validator"],
            "preimage_sha": pre_hash,
            "result_sha": post_hash,
            "anchor_matches": matches,
            "postconditions": checks,
        },
    }


# ------------------------------------------------------------- verification
def verify_chain(anchor_tip=True):
    """Check self-hashes, links, sequence, and optionally a local checkpoint.

    The parameter name is retained for compatibility with the historical code.
    The checkpoint is not external or authenticated. A party able to replace
    both files can reconstruct them. Malformed JSON is not handled gracefully.
    """
    previous = None
    count = 0
    for event in _events_iter():
        if sha(_event_body(event)) != event["event_id"]:
            return False, "event %s self-hash broken at seq %s" % (
                event["event_id"][:12], event["seq"]
            )
        if event["prev_event"] != previous:
            return False, "chain link broken at seq %s" % event["seq"]
        if event["seq"] != count + 1:
            return False, "seq not monotonic at %s" % event["seq"]
        previous = event["event_id"]
        count += 1
    if anchor_tip and count:
        checkpoint = _require_configuration()["tip"]
        if os.path.exists(checkpoint):
            with open(checkpoint, "r", encoding="utf-8") as stream:
                wanted = stream.read().strip()
            if wanted != previous:
                return False, "chain tail %s != local checkpoint %s" % (
                    previous[:12], wanted[:12]
                )
        else:
            return False, "audit log exists but no local checkpoint was found"
    return True, "%d events, chain intact, tip %s" % (
        count, (previous or "none")[:12]
    )


def write_tip_anchor():
    """Write a local checkpoint, retaining the historical function name.

    This write is unlocked and non-atomic, and it does not validate the chain.
    It does not create an independent or authenticated trust anchor.
    """
    tip = _chain_tip()
    with open(_require_configuration()["tip"], "w", encoding="utf-8") as stream:
        stream.write((tip or "") + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    return tip


# ----------------------------------------------------------- isolated demo
def demo():
    """Run four sequential scratch cases, return a path-free summary, and clean up.

    This is a demonstration, not an assertion-based acceptance test. No audit
    log is retained and the caller's prior configuration is restored afterward.
    """
    previous_configuration = DEFAULTS.copy()
    try:
        with tempfile.TemporaryDirectory(prefix="shared-harness-demo-") as directory:
            configure(os.path.join(directory, "events.jsonl"))
            target = os.path.join(directory, "target.txt")
            original = b"alpha\nbeta anchor gamma\ndelta\n"
            with open(target, "wb") as stream:
                stream.write(original)
            results = [
                ("no preimage hash supplied",
                 edit_anchor(target, "beta anchor gamma", "X", "demo-agent", None)),
                ("good edit, mandatory preimage",
                 edit_anchor(target, "beta anchor gamma", "beta MOVED gamma",
                             "demo-agent", sha(original))),
                ("replay (anchor absent)",
                 edit_anchor(target, "beta anchor gamma", "X", "demo-agent",
                             sha(_read_bytes(target)))),
            ]
            with open(target, "wb") as stream:
                stream.write(b"x\ny\ny\nz\n")
            results.append((
                "ambiguous anchor",
                edit_anchor(target, "y", "Y", "demo-agent", sha(_read_bytes(target))),
            ))
            chain_ok, chain_message = verify_chain(anchor_tip=False)
            write_tip_anchor()
            checkpoint_ok, checkpoint_message = verify_chain(anchor_tip=True)
            return {
                "notice": "Disposable public demonstration, not historical receipts or acceptance.",
                "cases": [
                    {"name": name, "status": result["status"], "human": result["human_port"]}
                    for name, result in results
                ],
                "chain": {"ok": chain_ok, "message": chain_message},
                "local_checkpoint": {"ok": checkpoint_ok, "message": checkpoint_message},
            }
    finally:
        DEFAULTS.clear()
        DEFAULTS.update(previous_configuration)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command")
    commands.add_parser("demo", help="run a disposable demonstration and delete its state")
    verifier = commands.add_parser("verify", help="read-only verification of an explicit audit log")
    verifier.add_argument("--events", required=True, help="audit log to read")
    verifier.add_argument("--tip", help="local checkpoint to read (default: EVENTS.tip)")
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0
    if args.command == "demo":
        print(json.dumps(demo(), indent=2))
        return 0
    configure(args.events, tip_path=args.tip)
    ok, message = verify_chain()
    print(json.dumps({"ok": ok, "message": message}))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
