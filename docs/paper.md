# The Pair Is the Product

## One harness around a human-agent pair

**Public research draft 0.1 · 2026-09-03**

This is a sanitized, revised research draft derived from private working notes. It is not a verbatim release of the private draft, an account of a finished product, or evidence that the proposed architecture improves outcomes. The public project is called **The Human Harness**; its central correction is that there should not be a separate human harness and agent harness. There should be one system with two ports.

The evidence boundary is simple: an early, single-pair case study informed the design; a guarded-edit and audit-log prototype exists; the full ontology-backed runtime does not. Joint agenda formation, adaptive work allocation, calibration, and retained-learning benefits remain hypotheses to test. The [evidence register](evidence-register.md) separates private historical evidence, public artifacts, and proposals.

## 1. The unit of integration is the pair

Human-AI integration is usually pictured as a person operating a tool or supervising an increasingly autonomous worker. Both pictures capture useful interactions. Neither is a sufficient design model for persistent collaboration.

The proposed unit is a coupled system: a human and an agent jointly sensing, remembering, deciding, acting, and correcting. The human brings capabilities the agent may lack: embodied observation, relationships, tacit domain judgment, access, and accountability for consequences. The agent brings other capabilities: tool-mediated observation and action, broad working context, repeatable procedures, and work that does not require simultaneous human attention. These are contingent capabilities, not permanent assignments by species.

The engineering question is therefore not merely, "How can the person control the agent?" It is also, "What machinery lets the pair do work neither participant can reliably do alone?"

Our architectural answer is:

> **One harness. Two ports. One evidence base and one computed operational state.**

The human port may show a sentence, an option, or a question. The agent port may receive a structured graph and source references. They should expose different resolutions of the same entities, evidence, decisions, and outcomes, not maintain competing memories.

This is a design decision. The private record contains partial examples of shared records and differentiated views; it does not demonstrate a complete unified runtime.

## 2. Goals belong inside the system

"The human assigns; the agent executes" assumes that a well-formed goal arrives from outside the machinery. Real requests often arrive as incomplete intentions: make this easier, stop this recurring failure, help me decide what matters next.

A useful harness needs a goal model, not only a task queue. It should preserve the desired outcome, why it matters, competing priorities, constraints, a definition of done, and unresolved choices. Either participant may propose a goal or challenge its framing. Choosing a goal is a recorded decision; it is not an empirical fact about what the human supposedly wants.

The private notes document requests followed by artifacts such as procedures, interface contracts, and structured records. Those artifacts and their order support a modest observation: informal intent can be followed by more formal working state. They do not, by themselves, prove that a particular request caused a particular artifact, or that the pair jointly discovered its agenda. Those stronger readings remain inferences.

The proposed mechanism makes that distinction explicit:

1. Capture the intention and its source.
2. Propose an outcome and falsifiable completion condition.
3. Record the unresolved tradeoffs.
4. Obtain the decision required by the consequences.
5. Track whether the resulting work actually closes the outcome.

An agent can help form the agenda without being allowed to invent the human's preferences. The shared state must keep a proposal separate from an adopted goal.

## 3. Work should move with capability and circumstance

A static split such as "humans decide, agents execute" wastes capabilities on both sides. A human may be the only available actuator for one step and the strongest analyst for another. A deterministic script may be better than either participant for a third. An agent may identify an anomaly that the human can resolve only through observation outside the software environment.

The proposed allocator routes work using current capability, evidence quality, availability, attention cost, uncertainty, reversibility, and authority. It must not confuse the ability to perform an action with permission to perform it.

A private record describes an agent diagnosing an infrastructure fault and a human performing the consequential change. The sequence is documented privately. Calling it a migration of a work class is an interpretation, not a measured allocator result.

The larger hypothesis is more interesting than replacing human tasks. A coupled system may create useful new work for the human: comparing options that did not previously exist, checking a surprising observation, deciding when a recurring exception deserves a new procedure, or evaluating whether a proposed goal is worth pursuing. The harness should make that work legible and affordable, not merely move a growing approval queue onto the person.

No adaptive allocator is implemented in this release. The [architecture](architecture.md) specifies the records needed to test one.

## 4. Reciprocity is the core, not an accessory

The agent-facing port gives machine reasoning senses, memory, tools, and continuity. The human-facing port of the same harness should give human intent persistence, human judgment reach, and human attention leverage.

That includes more than a dashboard:

- **Perception:** surface anomalies, missing evidence, options, and consequences at a useful resolution.
- **Memory:** preserve commitments, reasons, decisions, and unresolved questions outside either participant's transient context.
- **Thinking:** support comparison, decomposition, counterfactuals, and explicit uncertainty.
- **Action:** connect decisions to executable work, follow-through, and measured outcomes.
- **Correction:** make it cheap for either participant to identify a wrong claim, failed procedure, or mismatched goal.

The reverse direction matters equally. A human can be an observation source, a domain critic, a physical actuator, an authorizer, or a consequence-bearing decision-maker. Both participants are sensors and actuators available to the pair, subject to different limits.

A planning-tool example illustrates the design without exposing private work. Its internal documentation records a boundary between observed and inferred inputs, explicit provenance warnings, validation rules, and a separately authorized release step. Those are documented artifacts. The attractive story that each rule precisely "encoded the operator" was not supported by a per-artifact causal trace and was withdrawn from factual status.

That correction matters. The human-facing view must not decay into an agent-generated psychological profile. The system may record a chosen working rule and its rationale. It should not silently transform recurring behavior into a fact about the person's character, needs, or motives.

## 5. Ontology is the substrate; the harness is the runtime

One harness requires common meanings, not merely a shared folder.

The proposed ontology describes actors, capabilities, goals, constraints, observations, sources, claims, evidence, decisions, tasks, artifacts, outcomes, and corrections. Relations say who asserted a claim, what supports or contradicts it, which method checked it, what an action produced, and when a record was valid.

The runtime operates on those meanings: ingest evidence, evaluate claims, compute state, render views, allocate work, execute actions, measure outcomes, and append corrections. A vocabulary is not a working engine. A graph is not a verification method. An event log is not the complete substrate.

The intended loop is:

```text
evidence -> typed claims -> current-state projection -> goals and allocation
   ^                                                        |
   |                                                        v
corrections and measured outcomes <------------------------ action

Human port and agent port read and update this same system.
```

The [epistemic contract](epistemic-contract.md) is the semantic boundary; the [architecture](architecture.md) is the proposed execution boundary.

## 6. Agreement is not a truth test

A pair can become excellent at predicting each other's approval while becoming jointly wrong about the world. Alignment to a partner is therefore insufficient. The loop must close against outcomes and independently checkable evidence.

The governing distinction is between a source saying something and that statement being established within a defined scope. A decision can choose policy; it cannot ratify an empirical assumption into fact. An inference can guide a test; it cannot enter factual state merely because it has a citation.

The design uses typed claims: observed, documented, inferred, proposed, decided, conflicted, unknown, and verified by a defined method. In the intended runtime, `VERIFIED` is not directly writable. It is derived from a method record, evidence inputs, scope, time, and result, subject to the method's limits and unresolved conflicts.

That does not make the projection infallible. A method can be wrong, evidence can be incomplete, and a once-valid result can expire. A verified projection means "accepted under these recorded checks," not metaphysical truth.

Corrections should append evidence and adjudication rather than erase the original claim. Conflict does not automatically mean supersession. The system must preserve what was asserted, why its status changed, and which dependent outputs need reconsideration.

The current prototype does not enforce these claim transitions. It records file-edit operations. Treating those two things as equivalent would repeat the very error the design is intended to prevent.

## 7. Experience should change the environment

Persistent collaboration becomes useful when a correction changes what happens next, not only what is remembered.

The proposed experience compiler turns a verified outcome or adopted correction into a candidate change: a procedure, test, interface, memory record, capability, or goal. That change needs its own acceptance condition and subsequent measurement. The loop is not "an episode happened, therefore promote a rule."

Private notes record corrections followed by changed documents and procedures. They also record corrections to overly confident stories about those changes. This supports retaining an explicit correction history; it does not establish a rate of learning or a reduction in recurring failures.

The test is practical: after a correction becomes a versioned artifact, does the relevant failure recur less often, cost less to detect, or become easier to repair? A durable artifact is an intermediate result. Retained learning is an outcome to measure.

## 8. Assurance is necessary, but not the whole harness

Receipts, permission boundaries, rollback, dissent, and review frequency are essential parts of the system. They should support the coupling rather than become its entire purpose.

The human-facing design should compress routine state into useful verdicts with a direct path to supporting evidence. It should reserve interruption for uncertainty, consequence, or a decision that genuinely needs the person. The agent-facing design should receive the same status and provenance, not a more flattering version.

A proposed trust ladder changes review frequency for a class of work after measured performance. Its promotions and revocations are policy decisions. This case study has no validated ladder-performance result, no calibration score, and no evidence that a particular number of clean cycles is sufficient. Those thresholds are design parameters, not findings.

Dissent is likewise a proposed information channel, not permission to cross a safety boundary. Recording disagreement cannot authorize an otherwise prohibited action. Authority, privacy, and reversibility remain constraints on allocation.

## 9. Score the pair

The evaluation unit should match the design unit. Five candidate measures are:

| Measure | Question |
|---|---|
| Joint outcomes closed | Did the pair achieve the defined result end to end? |
| Surprise rate | What important failures or changes did the pair fail to anticipate or detect? |
| Correction cost | How much intervention and repair did each completed outcome require? |
| Attention consumed | How much human steering time and agent context or execution budget did the work use? |
| Retained learning | Did a correction become a durable change that improved later outcomes? |

These are proposed measures, not reported results. They need consistent definitions, a baseline, and comparable work. A lower intervention count is not automatically better if failures become harder to notice. A higher completion count is not better if the system closes the wrong goals.

## 10. What this release establishes

This release makes the architecture and its limits inspectable. It preserves an experimental history-layer prototype and the known gaps around it. It does not establish that the full system is installed, that the pair is calibrated, or that the architecture outperforms ordinary tool use.

The private development record includes a useful failure: an agent attributed bad file state to a write channel before the underlying operations had been checked. The documented correction identified omitted writes and an unguarded anchor in that incident. Later malformed-generation reports do not establish an inference-path root cause; that diagnosis remains unresolved. The public [correction history](corrections.md) keeps these claims separate.

The next evidence should come from executable tests and a constrained canary, not a more confident essay. First establish the edit-and-audit boundary. Then enforce claim transitions, compute projections, expose both ports, and test allocation and learning against outcomes.

The thesis is not that a human needs a better control panel for an agent. It is that persistent human-agent integration needs **one shared operational system**: common evidence, explicit goals, reciprocal capabilities, a common correction path, and two usable views. Build that system, measure the pair, and let the results decide how much of the thesis survives.
