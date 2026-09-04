# Public evidence register

**Release boundary · 2026-09-03**

This repository is a sanitized research release, not a dump of the private working environment. It distinguishes inspectable public artifacts from historical claims whose sources remain private.

## How to read the evidence

- **Public artifact:** a reader can inspect the released material. This proves what the artifact contains, not every claim made by it.
- **Publicly reproducible:** a reader can run the specified method on the released inputs. A successful result remains limited to that method and scope.
- **Documented privately:** a private source records the statement or event. The public reader cannot independently inspect that source here.
- **Observed privately:** an author-side check recorded a result against private material. This is an audit report, not public reproducibility.
- **Inferred:** an interpretation of evidence, not an established causal finding.
- **Decided or proposed:** an architectural or policy choice, not an empirical result.

These visibility labels supplement the claim types in the [epistemic contract](epistemic-contract.md).

## Claims and limits

| Claim | Basis | Status and limit |
|---|---|---|
| The design uses one harness with two ports | This paper and architecture specification | **Decided architecture.** Not a claim that the whole runtime is installed |
| Informal requests were followed by procedures, schemas, and other artifacts | Private dated notes and artifacts | **Documented privately.** The causal explanation remains inferred |
| A planning tool documented inferred-input warnings, validation rules, and a separately authorized release step | Private project documentation | **Documented privately.** No operational details or underlying project are released |
| A diagnosed repair was performed by a human after an agent's analysis | Private working record | **Documented privately.** Calling it adaptive work allocation is an interpretation |
| Paper corrections changed its terminology and claim classifications | Private drafts and correction records; sanitized summary in this release | **Documented privately.** Public readers can inspect the revised argument and summary, not the complete original conversation |
| A guarded-edit and audit-log prototype exists | Released experimental snapshot | **Public artifact.** Presence of code is not evidence that its guarantees hold |
| The private scratch log contained 31 events with a valid internal chain and matching local checkpoint at audit | Private source verifier and log reviewed for this release | **Observed privately.** Not proof of completeness, authenticity, production use, or immutable history |
| The historical prototype has known operation-identity, recovery, locking, and evidence gaps | Source review and recorded audit findings | **Known limitations.** The snapshot must not be treated as accepted production infrastructure |
| Human and agent views can be generated from one edit result | Prototype result structure | **Narrow implementation example.** Not a complete shared-state projection layer |
| Joint goal discovery, adaptive allocation, and retained learning improve outcomes | Proposed architecture and scorecard | **Unmeasured hypotheses** |
| A trust ladder or dissent process improves calibration | Proposed mechanisms | **Unmeasured.** No performance claim is made |
| VERIFIED derivation, a current-state projector, and an allocator are implemented | No such implementation in this release | **Unbuilt** |
| A constrained operational canary proves the enforcement boundary | No accepted canary result in this release | **Unbuilt** |
| Malformed generated code was caused by context length, output size, a model, or a router | Private author reports and limited comparisons | **Root cause unknown.** No controlled, publicly reproducible diagnosis is supplied |

The public tests establish only their stated assertions against the released snapshot. Regression tests that demonstrate defects are not acceptance tests for a safe writer. Any generated demonstration data must be labeled synthetic and must not be described as the private historical trace.

## Private source commitments

These SHA-256 commitments identify the private inputs used for this sanitized release. They let a holder of the originals check identity. They do not reveal the contents, prove the truth of the contents, or make the historical claims publicly verifiable.

| Opaque source identifier | SHA-256 |
|---|---|
| Private paper draft | `24fce06db97926f205bdc0524add9ffc6a7d1538fb26cb005cbfeee847e44d50` |
| Private history-layer source snapshot | `44c27712c2f0870bac27f8e9cdf0228424cbe8349001ed34cf298b7f1d32361f` |
| Private scratch audit log | `38ef73490358658b24dadd4161008b67f27860bfa9318cbcd8533197d5224e44` |

The public documents are revised derivatives. Their bytes intentionally differ from the private draft. Any sanitized code copy may also differ in comments, identifiers, or packaging. The private commitments must not be presented as hashes of the public files.

## What was withheld

The release excludes raw conversations, personal and household information, organization or client details, internal configuration, network and host information, absolute paths, session identifiers, live operational logs, and private behavioral profiles. The working charter is represented only by a generic [template](charter-template.md).

The private log was not edited, rehashed, and presented as an original chain. Redaction changes hashed content. A newly generated public chain is a new artifact, not a privacy-preserving proof of the old chain.

## What would strengthen the evidence

The next useful receipts are isolated regression tests, corrected implementation tests, interruption and concurrency tests, a constrained canary, and a reproducible claim-transition validator. Later claims about allocation or learning require defined outcomes, comparable work, and a baseline. More narrative confidence is not a substitute for those instruments.
