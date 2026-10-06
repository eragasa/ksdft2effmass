# `periodic1d.campaign`

## Purpose and status

This is the canonical target architecture for one-dimensional campaigns. The currently
implemented source remains temporarily at `ksdft2effmass.campaigns.periodic_1d`; rows
`058–066` must move it without an alias or wire-identity change. The legacy package owns
campaign definitions, execution, encoded documents, retained-evidence adapters, and
operation specifications that have not yet moved to canonical scientific owners. It
must not be used as a scientific-model base merely because historical modules contain
`model` in their path.

## Child map for audited surfaces

| Child | Responsibility | Canonical page |
|---|---|---|
| `model.toy_defects` | Controlled perturbation and basis-map definitions used by defect campaigns | [Toy defect operation definitions](model/toy_defects/index.md) |
| `isolated_replay` | Authenticated isolated-band replay evidence and scientific adoption | [Isolated-band replay adoption](isolated_replay/index.md) |
| `composite_adoption` | Finite-parent composite retained-operator adoption | [Composite scientific adoption](composite_adoption/index.md) |
| `composite_results` | Separate historical composite diagnostic and artifact-identity channels | [Composite campaign results](composite_results/index.md) |

Other campaign families remain governed by phase 5 and rows `058–066` until their
canonical migration dossiers are complete.

## Ownership and dependency boundary

Campaigns may consume nominal scientific models, retention objects, represented
operators, integration artifacts, and reusable Actions. Scientific model packages must
not import campaign execution, repository paths, verification policy, or retained
encoded documents.

## Code, tests, and Sphinx

| Kind | Path | Responsibility |
|---|---|---|
| Transitional package | `python/src/ksdft2effmass/campaigns/periodic_1d/__init__.py` | Current public campaign API pending canonical move |
| Tests | `python/tests/software_verification/ksdft2effmass/campaigns/periodic_1d/` | Campaign and supporting-operation software evidence |
| Sphinx | `doc/sphinx/api/research-monograph-campaigns.rst` | Current public campaign API |

Original local work under the repository license. Campaign software tests do not imply
scientific validation, uncertainty quantification, or acceptance.
