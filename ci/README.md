# Optional CI template

[`checks.yml.example`](checks.yml.example) is an inactive GitHub Actions template.
It repeats the privacy-pattern scan and the smoke/known-defect suite on Linux and
Windows with Python 3.11.

The initial publication credential could publish repository content but could not
install workflows, so no workflow was activated. No hosted CI result is claimed.

A maintainer with workflow permissions can review and copy the template to
`.github/workflows/checks.yml`. Its green status would still mean only that the
smoke tests passed and the four declared expected failures remained visible. It
would not mean the prototype passed concurrency, crash, or canary acceptance.
