# The Human Harness

![The Human Harness — one harness around the pair, two ports, one truth](assets/hero.png)

## The pair is the product

Human–AI integration needs **one shared harness with two ports**, not an agent control panel on one side and a psychological profile of the human on the other.

The human and agent contribute different observations, judgment, capabilities, and authority. They work from one provenance-preserving record of evidence, claims, goals, tasks, decisions, corrections, and outcomes. The ontology defines what those things mean; the runtime turns them into work and returns the results to shared state.

“One truth” in the hero is shorthand for **one canonical evidence record**, not an infallible answer or the elimination of disagreement. Reality determines what is true. The harness records what has been observed, asserted, tested, decided, disputed, or left unknown.

> **Research status:** this is a sanitized field-note collection and an unsafe, pre-alpha prototype. The prototype has known recovery and concurrency defects. It has only been exercised on disposable files. Do not use it on important data. The full shared harness is not implemented.

### Read

- [The paper: The Pair Is the Product](docs/paper.md)
- [Architecture and proposed build order](docs/architecture.md)
- [Epistemic contract](docs/epistemic-contract.md)
- [Evidence register](docs/evidence-register.md)
- [Correction history](docs/corrections.md)
- [Optional charter template](docs/charter-template.md)
- [Known limitations and acceptance blockers](KNOWN_LIMITATIONS.md)
- [Initial publication checks](docs/publication-checks.md)

### What exists

| Component | Status |
|---|---|
| Unified-harness thesis and ontology/runtime design | Specified; research proposal |
| Guarded edit plus hash-chained audit log | Experimental reference implementation |
| Compressed human verdict and structured agent receipt | Demonstrated for individual edit outcomes |
| Public smoke and known-defect regression tests | Included; not the formal acceptance suite |
| Reliable crash recovery and concurrent audit serialization | Not accepted; known defects |
| Operational canary | Not built |
| Derived claim-verification status and current-state projector | Not built |
| Work allocator and experience compiler | Proposed; not built here |
| Measured improvement in joint outcomes or calibration | Not established |

### Inspect the prototype

Python 3.11 or later; standard library only. Use disposable files and an isolated environment.

```sh
python -m unittest discover -s tests -v
python -m prototype.harness demo
```

The suite includes **expected failures that encode known defects**. A successful test command does not mean the prototype is production-safe. Read the test output and [limitations](KNOWN_LIMITATIONS.md), not only the exit code.

The public wrapper uses isolated temporary state for its demo. No-argument and unknown-command invocations do not run the demo. [Publication changes](docs/prototype-publication-changes.md) distinguish packaging changes from unfixed core behavior.

An [optional CI template](ci/README.md) is included but not activated. The recorded checks were run locally.

### Evidence, not origin stories

This repository distinguishes publicly reproducible checks from private observations, documented assertions, inferences, decisions, proposals, and unbuilt mechanisms. Private source hashes are commitments to particular artifacts—not public proof of their contents or claims.

The release was assembled from an explicit file allowlist in a new repository. It does not contain the original wiki, session database, operational audit log, personal charter, infrastructure configuration, or their Git history. See [privacy and provenance](PRIVACY.md).

### Contributing

Useful contributions include falsifiable counterexamples, independently authored tests, clearer state-machine invariants, and privacy-preserving reproductions. Do not post private logs, credentials, personal profiles, or operational file paths in issues.

No open-source or content license has been selected for this research release. See [NOTICE](NOTICE.md).
