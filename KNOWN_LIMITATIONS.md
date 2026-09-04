# Known limitations: historical Slice 1.1 reference

**Not accepted for operational use. Do not use this prototype on important files.**

The public code preserves the unfinished Slice 1.1 mechanism as a research
reference. It was exercised on scratch files, not operational ledgers. Public
packaging improvements are not hardening acceptance. The tests included here are
sequential smoke checks and four expected-failure defect demonstrations, **not**
the missing concurrency/crash-window suite. A successful test-process exit with
expected failures does not mean the harness is safe.

## Four unresolved blockers

| Blocker | Current behavior | Required future property |
|---|---|---|
| Duplicate intent identity | The intent ID hashes patch digest, second-resolution time, and actor label. Identical same-second operations collide. | Unique operation identity independent of clock resolution, with duplicate detection. |
| Recovery bypass | An `edit_recovery` detection is counted as settlement. The next operation can proceed without adjudication. | Detection remains unresolved until a separate explicit resolution event. |
| Unlocked audit append | Missing-hash refusals and direct `log_event()` calls bypass `OpLock`; sequence and predecessor are read separately. | Every append serialized with a verified predecessor under one enforced mechanism. |
| Checkpoint and replay evidence | The tip is a colocated file and the event retains only a patch digest. | Call the tip a local checkpoint unless independently anchored; retain reconstructable patch material under an explicit privacy policy. |

These defects are retained intentionally and have expected-failure regression
checks. The checks demonstrate that desired properties are absent; they are not
implementations of those properties.

## Other correctness and safety limits

- **No crash-atomic transaction.** Target replacement, outcome append, and
  checkpoint update are separate operations. `finally` cannot run after process
  termination or power loss. Even ordinary logging failures can leave no terminal
  outcome, and some exceptions are swallowed. A dangling-intent detector exists
  but has the recovery defects above.
- **No rollback.** A false or exception-throwing postcondition produces
  `APPLIED_FAILED_POSTCONDITION` after the changed file has already landed.
- **Cooperative locking only.** Other programs can change a target between its
  checked read and replacement. Different configured lock paths do not coordinate.
  There is no operating-system compare-and-swap guarantee for the target.
- **Checkpoint weakness.** `write_tip_anchor()` retains its historical name but
  writes only a local checkpoint. It is unlocked, non-atomic, manually invoked,
  and does not verify the chain before overwriting the checkpoint. A party able
  to rewrite both files can reconstruct a consistent pair. An empty log does not
  validate an existing checkpoint.
- **Partial/malformed logs.** JSON parse errors and missing event fields may raise
  exceptions rather than return a structured verification failure. The edit path
  does not validate the complete chain/checkpoint before mutation.
- **Temporary-file cleanup.** Some failures before successful replacement leave
  temporary files. The public demo is contained by `TemporaryDirectory`, but the
  edit primitive itself has not been repaired.
- **Metadata loss.** Replacing a target with a new temporary file can change
  permissions, ownership, ACLs, or other metadata. Directory durability has not
  been established across filesystems/platforms.
- **No path boundary.** There is no root allowlist, symlink/junction escape policy,
  or protection against path races. Windows normalization lowercases paths, which
  can be wrong in case-sensitive directories.
- **Input/validation edge cases.** Empty anchors are not explicitly rejected;
  hashes are length-checked rather than validated as hexadecimal. The generic
  `replacement_present_once` and `anchor_gone` checks reject some valid edits,
  such as a replacement already present elsewhere or containing the anchor.
- **Unauthenticated labels.** `writer` is caller-provided text, not proof of
  identity or authority. The recorded source digest is also not attestation that
  a particular binary executed the operation.
- **Sensitive audit content.** Library events contain absolute target paths and
  may contain exception text. They are private runtime data by default. Do not
  commit generated logs, lock files, checkpoints, or target files. The public demo
  emits only a path-free summary and deletes its state.
- **Mutable global configuration.** `configure()` is process-global and has no
  thread-safety guarantee. The Windows lock-file initialization appends a null
  byte on each acquisition, so the lock file grows.
- **Not a truth engine.** VERIFIED derivation, projection recomputation, claim
  adjudication, work allocation, and operational canary routing remain unbuilt.

## Test interpretation

Run from the repository root:

```sh
python -B -m unittest discover -s tests -v
```

The four expected failures cover intent-ID collision, recovery bypass, the
unlocked missing-hash rejection, and absent replay material. They are ordinary
sequential or mocked tests. No real concurrency pressure, forced termination,
crash recovery, metadata-preservation, or operational-canary acceptance is claimed.

The next engineering gate is an assertion-based concurrency and crash-window
suite, followed by explicit fixes, a disposable canary, and only then consideration
of operational routing. Publishing this reference does not advance that gate.
