# Initial publication checks

**Author-side check record · 2026-09-03**

These checks concern the sanitized public bundle, not acceptance of the proposed
shared harness. The private source material was not modified or published.

## Executed locally

Environment: Windows, Python 3.14.6, standard library only.

| Check | Recorded result | Boundary |
|---|---|---|
| `python -B -m unittest discover -s tests -v` | 17 tests: 13 passed, 4 expected failures | Sequential smoke and known-defect checks, not concurrency/crash acceptance |
| `python -B -m prototype.harness demo` | Missing hash refused; valid edit applied; replay and ambiguous anchor refused | Fresh disposable demonstration, not the private historical trace |
| Demo audit check | Five synthetic events had valid self-hashes, links, sequence, and a matching local checkpoint | Not an independent anchor, completeness proof, or immutable history |
| `python scripts/check_publication.py` | No configured privacy patterns or prohibited runtime artifacts found | Limited backstop, not a comprehensive secret scanner |
| Publication review | Private identifiers, local paths, raw logs, and operational material excluded; local document links checked | Manual review can still miss information |
| Hero review | Conceptual illustration and embedded provenance inspected; no private paths or personal metadata found | The image is AI-generated, not a system screenshot |

The first test attempt was blocked by the execution sandbox's temporary-directory
permissions before test setup completed. The successful run used permitted
disposable temporary directories. That environmental failure is not counted as a
prototype failure or a passing test.

The four expected failures cover duplicate intent IDs, recovery bypass, an
unlocked rejection append, and missing replay material. They are deliberate
evidence of unresolved defects. See [known limitations](../KNOWN_LIMITATIONS.md).

## Public artifact identities

SHA-256 of the released files, using their repository bytes:

| File | SHA-256 |
|---|---|
| `prototype/harness.py` | `7af8eb98f576b6c9712896645a94a96ed713c88d2e8eb5feccf8eb748c84bfd3` |
| `tests/test_harness.py` | `ea4af1e518a324912ccf37eb5fa0bcd4543ae86569cd82cb78ae841fe6040998` |
| `assets/hero.png` | `c17b76d0485a41eb4f81f74b6bb06f9207711bb5dbc0fc4c633b00c6da351ec2` |

Hashes identify bytes; they do not establish correctness. The Git commit supplies
the complete publication manifest. An [inactive CI template](../ci/README.md)
can repeat the scanner and test suite on Windows and Linux with Python 3.11.
It was not activated at initial publication; no hosted CI result is claimed.
