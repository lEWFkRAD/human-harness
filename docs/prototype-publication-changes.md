# Public prototype packaging changes

This repository contains a sanitized public adaptation of the unfinished Slice
1.1 history-layer prototype. It is not a byte-for-byte source archive and it is
not a hardening release. The private wiki and operational state were not edited
as part of public packaging.

The audited private source snapshot had SHA-256:

```text
44c27712c2f0870bac27f8e9cdf0228424cbe8349001ed34cf298b7f1d32361f
```

That digest identifies an unpublished source snapshot; it is not independent
proof of the public code's behavior. The public file has a different digest
because of the changes listed below.

## Changes made for publication

1. Removed personal names, internal actor aliases, private operational context,
   and misleading guarantee language from comments, docstrings, and demo labels.
   The generic demo actor is `demo-agent`; tests use `test-agent`.
2. Reworded the public status accurately: research reference, known defects,
   scratch-only demonstration, local checkpoint, unauthenticated actor label,
   and digest-only patch evidence. Tests, canary routing, VERIFIED derivation,
   projection recomputation, and allocation are not claimed as completed.
3. Removed automatic state configuration next to the source file. Library callers
   must call `configure(events_path, ...)` explicitly. Configuration selects paths
   but does not create files. Calls without configuration fail before mutation.
   `configure()` also accepts path-like objects through `os.fspath()`.
4. Added an argument-parser CLI. No arguments display help; unknown commands
   produce an argument error. Neither invokes a demo or mutates runtime state.
5. Moved the demonstration's target, log, lock, and checkpoint into one
   `TemporaryDirectory`. It restores prior process configuration and cleans up
   after success or an exception. Its returned/printed summary contains no
   absolute target path. The demo does not retain or publish its generated log.
6. Added read-only `verify --events PATH [--tip PATH]`, requiring an explicit
   audit-log path. There is no implicit source-directory log and no checkpoint-
   writing CLI command. The historical programmatic checkpoint function remains.
7. Made checkpoint file reading use a context manager and changed user-facing
   checkpoint/recovery wording so the interface does not claim an independent
   anchor or a recovery guarantee it does not enforce.
8. Applied neutral variable names and formatting without changing the guarded
   edit, intent identity, settlement, locking, or checkpoint algorithms.
9. Added disposable standard-library smoke checks and four `expectedFailure`
   regression demonstrations. These are expressly not the missing formal
   concurrency/crash-window acceptance suite.

## Deliberately not changed

- Same-second intent-ID collisions.
- Recovery detection counting as settlement.
- The unlocked missing-hash rejection and unlocked low-level audit/checkpoint
  helpers.
- Digest-only patch evidence and a colocated local checkpoint.
- Landed content remaining after failed postconditions.
- Best-effort, incomplete crash/exception handling and temporary-file cleanup in
  the edit primitive.
- Cooperative-only locking, path/metadata limitations, mutable global settings,
  and the other issues in [KNOWN_LIMITATIONS.md](../KNOWN_LIMITATIONS.md).

No expected-failure regression was made to pass by silently repairing the
historical algorithm. Future repairs should be separate, reviewed changes with
new tests and an explicit status update.

## Receipt and privacy boundary

The original development log, checkpoint, lock file, and bytecode cache are not
included. Original events contain private absolute paths and internal labels.
Changing those fields would invalidate their original chain IDs, so a redacted
copy must never be presented as the unchanged historical receipt.

The public CLI demo is a fresh disposable reproduction. It is not the original
development log and is not evidence of concurrency or crash safety. If a future
public sample chain is retained, it must be labeled as newly generated and must
not contain local machine/user paths or private target content.
