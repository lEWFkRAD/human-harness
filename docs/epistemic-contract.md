# Epistemic contract

**Proposed semantics · No transition validator is implemented by this document**

The shared harness begins with evidence and typed claims, not a synthesized narrative about either participant. Both ports must preserve the same distinctions between what was observed, what a source said, what was inferred, and what was chosen.

## The central rules

1. A document can establish that a statement was recorded. It does not automatically establish the statement itself.
2. A human decision can adopt policy or a goal. It cannot make an empirical assumption true.
3. An inference remains a hypothesis until a suitable method tests it.
4. Verification is scoped and method-dependent. It is not certainty or permanent truth.
5. Conflicting evidence requires explicit treatment. Conflict does not automatically supersede an earlier claim.
6. Corrections preserve the original assertion and the reason for its changed status.

## Working vocabulary

The private notes used the following labels. A production schema should separate evidence-acquisition type, epistemic status, and normative status rather than force all of them into one linear ladder.

| Label | Meaning | Does not mean |
|---|---|---|
| `OBSERVED` | A specified method directly recorded a result within a scope | Every interpretation of that result is established |
| `DOCUMENTED` | An identified source contains a statement | The source's statement is true |
| `INFERRED` | A reasoned interpretation is proposed from evidence | The interpretation may enter factual state |
| `PROPOSED` | A goal, action, or policy awaits an authorized decision | It is adopted or executable |
| `DECIDED` | An authorized choice is recorded | An empirical proposition was verified |
| `CONFLICTED` | Material evidence or claims disagree | The newest statement wins |
| `UNKNOWN` | Available evidence is insufficient for the required conclusion | The proposition is false |
| `VERIFIED` | A registered method accepted a claim in a defined scope using recorded inputs | The method is infallible, the result is timeless, or the action is authorized |

The [evidence register](evidence-register.md) additionally marks whether evidence is public or private. Visibility and epistemic status are separate properties.

## Minimum claim record

A proposed claim record should include:

- A stable identifier and an explicit proposition, including its subject and scope.
- The asserting actor, source record, source content identity, and observation time.
- Evidence references and the acquisition method for each observation.
- Inferences or assumptions needed to reach the proposition.
- Relevant validity interval and freshness requirements.
- Supporting and contradicting records.
- Verification method results, if any.
- Correction, adjudication, supersession, and dependency references.

Compound claims should be decomposed when their parts have different evidence. Two statements that sound contradictory may concern different predicates. The system must compare the actual propositions before declaring a conflict.

## Verification must be derived

In the intended runtime, callers cannot directly write `status = VERIFIED`.

A derivation requires a registered method identifier and version, evidence inputs with content identities, the proposition and scope checked, execution time, recorded result, and applicable validity limits. The method must actually have run on those inputs. A method name attached to a claim is not enough.

The transition validator should reject promotion when required inputs are missing, the method is not accepted for the scope, the result is unsuccessful, evidence has changed, or a relevant unresolved conflict prevents acceptance.

The current-state projector then computes the accepted status from those records. It must be possible to explain why a claim appears in the projection and to invalidate it when its evidence, method, or validity changes.

This design reduces an unguarded promotion path. It does not make false conclusions impossible. Incorrect methods, incomplete evidence, compromised sources, and implementation defects remain failure modes.

## Normative and factual lanes stay separate

| Input | Permitted result | Forbidden shortcut |
|---|---|---|
| An adopted proposal | Recorded goal or policy | Treating adoption as empirical proof |
| A document assertion | A documented claim with provenance | Importing its conclusion directly as fact |
| A successful method result | Scoped verification candidate | Treating unrelated claims as verified |
| Contradictory evidence | Conflict record and review | Automatically deleting the older claim |
| An upheld correction | Supersession or revised scope, with provenance | Rewriting history to hide the original assertion |
| Repeated behavior | A hypothesis or proposed working rule | A factual psychological profile |

Authority and verification are independent. A well-verified action may still be unauthorized. An authorized action may still rest on uncertain evidence.

## Corrections and projections

The proposed correction path is:

```text
original claim -> new evidence or correction -> conflict/scope analysis
               -> recorded adjudication -> revised projection
               -> affected outputs and tasks reconsidered
```

Supersession is one possible outcome, not the definition of correction. Other outcomes include retaining the original claim, narrowing its scope, decomposing it, or leaving it unresolved.

Append-oriented history is a design policy. A hash chain can detect some changes relative to a trusted prior checkpoint, but a colocated log and checkpoint do not establish immutable history. Storage integrity, source authenticity, semantic correctness, and authority need separate controls.

## Port consistency

Both ports should carry a projection identifier and access to its supporting records. The human view may compress detail but must retain uncertainty that could change a decision. The agent view must not receive a private factual upgrade hidden from the human.

For example, "the output bytes matched the intended edit" must not become "the application works" in the shorter view. They are different propositions requiring different methods.

## Acceptance criteria for an implementation

Before this contract can be called enforced, tests must demonstrate rejected direct promotion, reproducible method-based derivation, conflict handling, stale-input invalidation, correction provenance, deterministic replay, and consistent human/agent projections. None of those results should be inferred merely from the presence of this document.
