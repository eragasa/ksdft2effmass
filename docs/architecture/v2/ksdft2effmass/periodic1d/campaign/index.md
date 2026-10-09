# `periodic1d.campaign`

## Purpose and status

This is the canonical architecture for one-dimensional campaigns. Rows 058--066
moved the isolated-band, composite, reduction-challenge, retained Wannier90,
blind-alignment, continuum-refinement, finite-rank-oracle, matched-extraction, and
route-reconciliation families beneath this package without aliases or retained-wire
identity changes. Campaign packages must not be used as scientific-model bases merely
because historical modules contain `model` in their paths.

## Child map for audited surfaces

| Child | Responsibility | Canonical page |
|---|---|---|
| `model.toy_defects` | Controlled perturbation and basis-map definitions used by defect campaigns | [Toy defect operation definitions](model/toy_defects/index.md) |
| `isolated` | Canonical isolated-band controls, bytes, results, operations, verification, and adoption | [Isolated-band campaign](isolated/index.md) |
| `composite` | Canonical composite controls, explicit retention, bytes, represented diagnostics, operations, verification, and scientific adoption | [Composite campaign](composite/index.md) |
| `reduction_challenge` | Canonical adversarial reduction controls, historical wires, typed observations, correlation, independent verification, and campaign orchestration | [Reduction-challenge campaign](reduction_challenge/index.md) |
| `wannier90` | Canonical exact wires, result-first authentication, native-artifact correlation, independent Wilson verification, and cohesive integration | [Retained Wannier90 campaign](wannier90/index.md) |
| `result_documents` | Complete immutable encoded-result JSON trees with exact source-byte identities and explicit wire kinds | [Encoded result documents](result_documents/index.md) |
| `serialization` | Strict shared periodic-1D wire adaptation without schema or scientific ownership | [Campaign serialization](serialization/index.md) |
| `alignment` | Canonical blind-alignment records, exact wires, visible-observation/hidden-truth boundary, inference, evaluation, orchestration, correlation, and independent verification | [Alignment campaigns](alignment/index.md) |
| `extraction` | Canonical matched known-map extraction controls, authenticated parent loading, general represented-operator adaptation, workflow, and verification | [Extraction campaigns](extraction/index.md) |
| `refinement` | Campaign-specific separated refinement axes and retained evidence | [Refinement campaigns](refinement/index.md) |
| `oracle` | Named bounded comparison campaigns, not a generic oracle engine | [Oracle campaigns](oracle/index.md) |
| `reconciliation` | Explicit finite common-parent/common-space route comparisons | [Route reconciliation campaigns](reconciliation/index.md) |

## Ownership and dependency boundary

Campaigns may consume nominal scientific models, retention objects, represented
operators, integration artifacts, and reusable Actions. Scientific model packages must
not import campaign execution, repository paths, verification policy, or retained
encoded documents.

## Code, tests, and Sphinx

| Kind | Path | Responsibility |
|---|---|---|
| Canonical family packages | `python/src/ksdft2effmass/periodic1d/campaign/` | Row-058 through row-066 campaign families and reviewed parent facades |
| Canonical shared wire modules | `python/src/ksdft2effmass/periodic1d/campaign/{result_documents.py,serialization/}` | Exact result documents and strict field adaptation consumed by canonical families |
| Canonical shared-wire tests | `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/` | Routine and artifact-owned row-045/058 evidence |
| Canonical family tests | `python/tests/{software_verification,numerical_verification}/ksdft2effmass/periodic1d/campaign/` | Row-058 through row-066 software, numerical, and artifact evidence |
| Sphinx | `doc/sphinx/api/research-monograph-campaigns.rst` | Canonical campaign APIs |

Original local work under the repository license. Campaign software tests do not imply
scientific validation, uncertainty quantification, or acceptance.
