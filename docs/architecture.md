# Architecture and build order

**Proposed architecture · Public research draft 0.1**

This document specifies a target, not an installed platform. The public code is an experimental history-layer snapshot. Claim-transition enforcement, current-state projection, adaptive allocation, and measured learning are not implemented here.

## One system, two ports

```text
Human port ----+
               +---- shared harness ---- observations and outcomes in the world
Agent port ----+

Shared records:
evidence | claims | goals | decisions | tasks | artifacts | outcomes | corrections
```

The ports differ in presentation and interaction cost. They do not own separate factual states. A human verdict and an agent receipt should identify the same underlying event or projection version.

The ontology supplies shared meanings. The runtime supplies the operations and enforcement that move between them.

## Six runtime layers

| Layer | Responsibility | Required output | Status |
|---|---|---|---|
| Evidence intake | Capture observations, documents, tool results, and their provenance | Addressable evidence record with source, time, scope, and content identity | Proposed |
| State estimator | Evaluate claim status using registered methods and conflict rules | Recomputable current-state projection with reasons and dependencies | Unbuilt |
| Goal model | Preserve desired outcomes, priorities, constraints, and definitions of done | Versioned goals and explicit unresolved choices | Proposed |
| Work allocator | Match work to capability, availability, uncertainty, cost, and authority | Assignment decision with rationale and required checks | Unbuilt |
| Projection layer | Render shared state appropriately for each participant | Human brief and machine context from one projection version | Proposed; the prototype only demonstrates two views of an edit result |
| Experience compiler | Propose durable changes from outcomes and corrections | Versioned candidate procedure, test, interface, or policy change | Unbuilt |

The edit-and-audit prototype sits below these layers. It attempts to protect one file operation and record its outcome. It is not the evidence bus, claim validator, or full event-sourced application.

## Minimum semantic model

Entities:

- Actor and capability
- Goal and definition of done
- Constraint and dependency
- Observation and source
- Claim, evidence, assumption, and hypothesis
- Proposal and decision
- Task and action
- Artifact and artifact version
- Outcome and correction
- Verification method and method result

Relations:

`asserted_by`, `observed_at`, `supported_by`, `contradicted_by`, `verified_by`,
`inferred_from`, `proposed_by`, `ratified_by`, `assigned_to`, `depends_on`,
`produced`, `supersedes`, and `valid_during`.

These names are a proposed vocabulary, not a released schema. Relation presence alone must not establish a claim's truth status. The [epistemic contract](epistemic-contract.md) defines the intended separation.

## A complete work cycle

1. **Capture:** preserve the request or observation without inventing missing intent.
2. **Frame:** propose an outcome, completion test, constraints, and unresolved decisions.
3. **Ground:** attach evidence and distinguish facts from assumptions.
4. **Allocate:** select a capable participant or tool within its authority.
5. **Act:** record intent, execution, artifact versions, and outcome.
6. **Check:** evaluate the result using a named method against actual output.
7. **Project:** update the shared state and render both views from the same version.
8. **Learn:** propose a durable change, test it, and measure its later effect.

An outcome may send the cycle back to framing rather than merely retrying execution. The goal itself may have been wrong or incomplete.

## Allocation is more than authorization

An assignment should record the task, eligible capabilities, selected executor, reason, evidence requirements, expected attention cost, and consequence boundary. Permission is a constraint, not the optimization objective.

The allocator may route observation to a human, analysis to an agent, arithmetic to a deterministic routine, and a consequential action back to an authorized person. It should be able to change an assignment when evidence or availability changes. Such changes must be explicit events, not inferred later from who happened to act.

No allocation policy is empirically validated in this release.

## Two projections of one result

Illustrative interface, not a historical receipt:

| Human view | Agent view |
|---|---|
| "Edit applied; readback matched the intended bytes. Application-level correctness is not checked." | Operation ID, target alias, preimage and result hashes, named checks, outcomes, unresolved limits, and event reference |

Compression must preserve decision-relevant uncertainty. A short verdict must not upgrade "bytes matched" into "the application is correct."

## Current prototype boundary

The historical snapshot includes mandatory expected hashes, cooperative locking, intent and outcome records, readback checks, a hash-chained audit log, and a local tip checkpoint. Its known defects prevent treating it as accepted enforcement infrastructure.

The principal open defects are operation-identity collisions, recovery records that can incorrectly settle an unresolved operation, audit appends outside the operation lock, and evidence insufficient to reconstruct a patch. A colocated tip is only a checkpoint. It does not prevent a party able to rewrite both files from reconstructing the log.

The prototype's readback checks concern file bytes. They neither derive epistemic `VERIFIED` status nor prove application behavior.

## Build order and exit conditions

### 1. Establish the history-layer boundary

Write regression tests for the known defects before fixing them. Require unique operation identity, serialized audit appends, explicit recovery adjudication, defined failed-postcondition behavior, reconstructable change evidence, and clear checkpoint semantics.

Exercise concurrency, interruption windows, malformed or partial logs, exceptions, and cleanup in isolated fixtures. A successful demo is not the acceptance test.

**Exit:** the relevant assertions pass, failures remain visible, and the documented guarantees match the implementation.

### 2. Route one constrained canary

Use a non-sensitive canary ledger with one authorized writer path and a defined rollback or recovery procedure. Demonstrate that bypasses are either prevented by the environment or explicitly outside the guarantee.

**Exit:** the canary's mutations and interruptions can be accounted for without relying on the author's recollection.

### 3. Enforce claim transitions

Implement the [epistemic contract](epistemic-contract.md). Make `VERIFIED` a derived status, require method and evidence records, retain conflicts, and invalidate dependent results when inputs or methods change.

**Exit:** direct status promotion is rejected, supported transitions are reproducible, and invalidation tests pass.

### 4. Compute shared state and render both ports

Build deterministic projections from the accepted history. Render a concise human view and structured agent view with matching identifiers, status, and provenance.

**Exit:** replay produces the same projection, and both views preserve the same decision-relevant uncertainty.

### 5. Add goals and allocation

Record goal adoption, completion tests, assignments, migrations, and outcomes. Begin with explicit policies before attempting adaptive routing.

**Exit:** the pair can explain why work was assigned, whether the outcome closed, and which decisions remain unresolved.

### 6. Test retained learning

Introduce the experience compiler as a proposal generator. Compare recurrence, detection, repair, and attention costs before and after accepted changes.

**Exit:** a measured outcome supports a bounded learning claim. Artifact creation alone does not.

## Cross-cutting limits

Privacy, authority, reversibility, and resource limits apply at every action boundary. Human approval does not replace empirical verification; empirical verification does not grant authority. No layer may silently promote an inference into a fact or a proposal into an adopted goal.
