"""Disposable smoke checks and expected-failure defect demonstrations.

These are NOT the missing concurrency/crash-window acceptance suite. The four
expected failures assert desired properties that the historical prototype does
not satisfy. A green unittest exit with expected failures is not acceptance.
Run from the repository root with:
    python -B -m unittest discover -s tests -v
"""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from prototype import harness


class HarnessTestCase(unittest.TestCase):
    def setUp(self):
        self.previous_configuration = harness.DEFAULTS.copy()
        self.temporary = tempfile.TemporaryDirectory(prefix="shared-harness-test-")
        self.root = Path(self.temporary.name)
        self.events = self.root / "events.jsonl"
        self.target = self.root / "target.txt"
        self.original = b"before anchor after\n"
        self.target.write_bytes(self.original)
        harness.configure(self.events)

    def tearDown(self):
        harness.DEFAULTS.clear()
        harness.DEFAULTS.update(self.previous_configuration)
        self.temporary.cleanup()

    def records(self):
        if not self.events.exists():
            return []
        return [json.loads(line) for line in self.events.read_text(encoding="utf-8").splitlines()]

    def edit(self, anchor="anchor", replacement="changed", expected=None, **kwargs):
        expected = harness.sha(self.original) if expected is None else expected
        return harness.edit_anchor(
            self.target, anchor, replacement, "test-agent", expected, **kwargs
        )


class HarnessSmokeTests(HarnessTestCase):
    def test_explicit_configuration_required(self):
        harness.DEFAULTS.update(events=None, lock=None, tip=None)
        with self.assertRaisesRegex(RuntimeError, "configure"):
            harness.verify_chain()
        self.assertEqual(self.target.read_bytes(), self.original)
        self.assertFalse(self.events.exists())

    def test_missing_hash_refuses_and_logs_without_changing_target(self):
        result = harness.edit_anchor(self.target, "anchor", "changed", "test-agent", None)
        self.assertEqual(result["status"], "NOT_APPLIED:PREIMAGE_HASH_REQUIRED")
        self.assertEqual(self.target.read_bytes(), self.original)
        self.assertEqual(self.records()[0]["payload"]["code"], "PREIMAGE_HASH_REQUIRED")

    def test_success_has_readback_and_intent_outcome_records(self):
        result = self.edit()
        self.assertEqual(result["status"], "APPLIED")
        self.assertEqual(self.target.read_bytes(), b"before changed after\n")
        self.assertEqual(result["agent_port"]["result_sha"], harness.sha(self.target.read_bytes()))
        self.assertTrue(all(result["agent_port"]["postconditions"].values()))
        self.assertEqual([event["kind"] for event in self.records()], ["edit_intent", "edit"])
        self.assertTrue(harness.verify_chain(anchor_tip=False)[0])
        harness.write_tip_anchor()
        self.assertTrue(harness.verify_chain()[0])

    def test_absent_anchor_preserves_target(self):
        result = self.edit(anchor="absent")
        self.assertEqual(result["status"], "NOT_APPLIED:ANCHOR_ABSENT")
        self.assertEqual(self.target.read_bytes(), self.original)

    def test_ambiguous_anchor_preserves_target(self):
        content = b"anchor and anchor\n"
        self.target.write_bytes(content)
        result = self.edit(expected=harness.sha(content))
        self.assertEqual(result["status"], "NOT_APPLIED:ANCHOR_NOT_UNIQUE")
        self.assertEqual(self.target.read_bytes(), content)

    def test_stale_hash_preserves_target(self):
        result = self.edit(expected="0" * 64)
        self.assertEqual(result["status"], "NOT_APPLIED:PREIMAGE_MISMATCH")
        self.assertEqual(self.target.read_bytes(), self.original)

    def test_missing_target_is_recorded(self):
        missing = self.root / "missing.txt"
        result = harness.edit_anchor(missing, "anchor", "changed", "test-agent", "0" * 64)
        self.assertEqual(result["status"], "NOT_APPLIED:TARGET_MISSING")
        self.assertFalse(missing.exists())

    def test_failed_postcondition_documents_landed_content_not_rollback(self):
        result = self.edit(postconditions={"deliberately_false": lambda _: False})
        self.assertEqual(result["status"], "APPLIED_FAILED_POSTCONDITION")
        self.assertEqual(self.target.read_bytes(), b"before changed after\n")
        self.assertFalse(self.records()[-1]["payload"]["postconditions"]["user:deliberately_false"])

    def test_postcondition_exception_is_recorded_as_failed(self):
        def broken_check(_):
            raise ValueError("disposable test failure")

        result = self.edit(postconditions={"raises": broken_check})
        self.assertEqual(result["status"], "APPLIED_FAILED_POSTCONDITION")
        self.assertIn("user_error", self.records()[-1]["payload"]["postconditions"])
        self.assertEqual(self.target.read_bytes(), b"before changed after\n")

    def test_chain_detects_payload_edit(self):
        self.edit()
        records = self.records()
        records[0]["payload"]["writer"] = "changed-test-label"
        self.events.write_text(
            "".join(json.dumps(event) + "\n" for event in records), encoding="utf-8"
        )
        self.assertFalse(harness.verify_chain(anchor_tip=False)[0])

    def test_demo_is_disposable_and_restores_configuration(self):
        before = harness.DEFAULTS.copy()
        files_before = sorted(path.name for path in self.root.iterdir())
        report = harness.demo()
        self.assertEqual(harness.DEFAULTS, before)
        self.assertEqual(sorted(path.name for path in self.root.iterdir()), files_before)
        self.assertEqual(
            [case["status"] for case in report["cases"]],
            ["NOT_APPLIED:PREIMAGE_HASH_REQUIRED", "APPLIED",
             "NOT_APPLIED:ANCHOR_ABSENT", "NOT_APPLIED:ANCHOR_NOT_UNIQUE"],
        )
        self.assertNotIn(str(self.root), json.dumps(report))

    def test_cli_default_and_unknown_command_do_not_mutate(self):
        script = str(Path(harness.__file__).resolve())
        files_before = {path.name: path.read_bytes() for path in self.root.iterdir()}
        for arguments, expected_code in (([], 0), (["not-a-command"], 2)):
            result = subprocess.run(
                [sys.executable, "-B", script, *arguments], cwd=self.root,
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, expected_code, result.stderr)
            self.assertIn("usage:", result.stdout + result.stderr)
        self.assertEqual(
            {path.name: path.read_bytes() for path in self.root.iterdir()}, files_before
        )

    def test_cli_verify_requires_explicit_events_and_is_read_only(self):
        self.edit()
        harness.write_tip_anchor()
        script = str(Path(harness.__file__).resolve())
        files_before = {path.name: path.read_bytes() for path in self.root.iterdir()}
        result = subprocess.run(
            [sys.executable, "-B", script, "verify", "--events", str(self.events)],
            cwd=self.root, capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["ok"])
        self.assertEqual(
            {path.name: path.read_bytes() for path in self.root.iterdir()}, files_before
        )


class KnownDefectRegressions(HarnessTestCase):
    """Desired properties, deliberately expected to fail on this reference.

    These sequential/mocked checks expose defects. They do not exercise real
    simultaneous processes or kill processes at crash windows.
    """

    @unittest.expectedFailure
    def test_identical_same_second_operations_have_distinct_intent_ids(self):
        with mock.patch.object(harness, "now_utc", return_value="2000-01-01T00:00:00Z"):
            self.edit()
            self.target.write_bytes(self.original)
            self.edit()
        intent_ids = [
            event["payload"]["intent_id"] for event in self.records()
            if event["kind"] == "edit_intent"
        ]
        self.assertEqual(len(intent_ids), len(set(intent_ids)), "intent IDs collided")

    @unittest.expectedFailure
    def test_recovery_detection_stays_blocking_until_explicit_adjudication(self):
        harness.log_event("edit_intent", {
            "op": "anchor_edit", "target": harness.normalize_target(self.target),
            "writer": "test-agent", "intent_id": "unresolved-test-intent",
        })
        first = self.edit()
        self.assertEqual(first["status"], "NOT_APPLIED:PRIOR_INTENT_UNRESOLVED")
        second = self.edit()
        self.assertEqual(second["status"], "NOT_APPLIED:PRIOR_INTENT_UNRESOLVED")

    @unittest.expectedFailure
    def test_missing_hash_refusal_appends_under_operation_lock(self):
        depth = {"value": 0}
        original_log_event = harness.log_event
        testcase = self

        class ObservedLock:
            def __enter__(self):
                depth["value"] += 1
                return self

            def __exit__(self, *exc):
                depth["value"] -= 1

        def checked_log_event(kind, payload, path=None):
            testcase.assertGreater(depth["value"], 0, "audit append bypassed the lock")
            return original_log_event(kind, payload, path)

        with mock.patch.object(harness, "OpLock", ObservedLock), mock.patch.object(
            harness, "log_event", side_effect=checked_log_event
        ):
            harness.edit_anchor(self.target, "anchor", "changed", "test-agent", None)

    @unittest.expectedFailure
    def test_intent_contains_replay_material_not_only_a_digest(self):
        self.edit()
        payload = self.records()[0]["payload"]
        self.assertTrue(
            "patch" in payload or "patch_blob_ref" in payload,
            "a patch digest cannot reconstruct the edit",
        )


if __name__ == "__main__":
    unittest.main()
