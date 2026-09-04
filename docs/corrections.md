# Correction history

**Sanitized account of the design's development**

This is a public summary derived from private drafts and correction records. It omits identities, operational details, raw conversation identifiers, and exact private chronology. It is not the original ledger or a hash-preserving export. See the [evidence register](evidence-register.md) for source visibility and commitments.

## 1. Supervision was mistaken for integration

The first draft concentrated on verdicts, approval frequency, dissent, and trust ladders. The operator's correction broadened the object of design: the harness must also help the human perceive, remember, compare, act, and follow through.

**Current position:** assurance is necessary, but the thesis is a shared operational system with goals, reciprocal capabilities, allocation, and learning.

## 2. Two connected harnesses became one harness

An intermediate architecture described separate human and agent harnesses joined through shared state. That preserved the split the design was trying to remove.

**Current position:** one harness owns the evidence, state, goals, work graph, correction path, and outcome record. Human and agent interfaces are two ports, not separate factual systems. This is an architectural decision, not a finding that the complete system already exists.

## 3. Citations were mistaken for causal evidence

Earlier drafts described rules as products of specific corrections, artifacts as encoding the operator, and a proposed goal as jointly discovered. The sources established that documents and proposals existed; they did not establish all those causal or psychological conclusions.

**Current position:** artifact existence and order can be documented while the story connecting them remains inferred. A proposed goal is not an adopted goal. A working rule is not a verified fact about a person's psychology.

## 4. A schema was mistaken for enforcement

Removing an `is_true` relation was initially described as making citation laundering structurally impossible. A writer could still assign a misleading status or attach an unsuitable method record.

**Current position:** the proposed runtime must derive verification from accepted method results and evidence. Even enforced transitions remain fallible because methods, inputs, and implementations can be wrong. The validator is not implemented in this release.

Conflict handling was corrected at the same boundary: contradictory evidence does not automatically supersede an earlier claim. Scope analysis and recorded adjudication are required.

## 5. A file-state failure was misdiagnosed

One incident was initially attributed to a write channel. The subsequent private audit identified omitted write-back operations and a splice performed after an unguarded failed anchor search in that incident.

**Current position:** that incident does not establish channel corruption. A tool reporting successful execution does not establish that the intended effect occurred. The narrow lesson is to check actual state and postconditions, not to infer a platform fault from a surprising result.

## 6. A prototype was mistaken for installed infrastructure

The first executable slice recorded guarded edits and a hash chain. Later language described the history as immutable and a colocated tip file as an external anchor. A hardening revision also listed tests and canary behavior before those acceptance steps existed.

**Current position:** the artifact is an experimental history-layer snapshot with known defects. It is not the installed ontology-backed substrate. The log is hash-chained; the nearby tip is a local checkpoint. Digests without reconstructable patch material are not full replay evidence. A demo is not a concurrency or interruption test.

Known defects include colliding operation identifiers, recovery records that can incorrectly settle an unresolved intent, audit appends outside the operation lock, and incomplete change evidence. Those defects remain visible in the public status rather than being silently repaired in prose.

## 7. A stopping decision did not establish a root cause

A later author report attributed malformed generated code to a long session. A subsequent report described similar output in a fresh context and a small-versus-larger-output comparison.

**Current position:** the reports weaken a simple session-length explanation, but they do not establish output-size causality, a model defect, a router fault, or a storage fault. The root cause is unknown. Stopping risky code generation was a risk decision; it was not a completed diagnosis.

## What the history supports

The record supports a modest methodological point: claims about the system, including flattering claims made by its authors, need the same evidence discipline as the system's working state. It does not prove that the proposed architecture is effective simply because its development contains corrections.

The next step is to turn the known implementation gaps into executable tests and measured outcomes. The architecture should earn its stronger claims there.
