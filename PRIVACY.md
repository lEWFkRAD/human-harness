# Privacy and provenance

This is a sanitized public derivative, not an export of the private working environment.

## Included

- A public research draft of the unified-harness thesis.
- A proposed architecture, epistemic contract, and generic charter template.
- An anonymized correction history and evidence register.
- A sanitized experimental code snapshot, disposable-file tests, and explicit limitations.
- An AI-generated conceptual hero illustration. It is not a photograph or screenshot of an actual installation.

## Excluded

- Raw conversations, session databases, private memory, and continuity files.
- Personal names and biographies, household information, financial or legal circumstances, and client or employer information.
- Machine names, network topology, private endpoints, absolute home-directory paths, credentials, and automation identifiers.
- The signed personal charter, operational configurations, private audit events, checkpoint files, and old Git history.

The original materials remain private and unchanged. The public cut corrects stale wording and unsupported causal claims; it is not presented as a verbatim copy of the internal draft.

## Why the private event log is not redacted and republished

Its event hashes cover fields that contain private paths and actor labels. Redacting those fields changes the hashes and breaks the original chain. Rehashing a redacted log would create a different chain, not preserve the original receipt.

Instead, the evidence register can identify a private artifact by its digest and state exactly which checks were performed privately. Readers can reproduce the public tests independently. A digest does not prove that a private claim is true.

## Generated logs are sensitive

The reference implementation can record absolute target paths and caller-supplied actor labels. Keep any logs produced during local experimentation private unless they have been separately reviewed. Do not upload runtime logs, local checkpoints, or temporary files to this repository.

The publication scanner is a useful backstop, not a complete privacy or secret detector. Human review and explicit file selection remain necessary.
