# Security

Do not use this prototype on important, sensitive, or operational files. It contains known defects in recovery, event serialization, and evidence completeness. Atomic replacement is not an end-to-end transaction or a security boundary.

Use a disposable workspace. Treat generated logs as sensitive. The actor label is not authenticated identity, the local checkpoint is not an independent trust anchor, and the operation lock does not constrain unrelated editors.

Report a problem with a minimal synthetic reproduction. Do not include credentials, private event logs, personal data, internal endpoints, or real operational paths in a public issue.

The project makes no security-support or production-readiness commitment at this stage.
