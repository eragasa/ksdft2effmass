# Periodic-2D rank-defect calculation family

## Status

This flat directory is the maintained calculation-composition home for periodic-2D
rank-defect studies formerly designed under the research-monograph calculation tree.
The active Folding and Null-Alignment Controls and Finite-Domain Sensitivity planning
records are scalar rank-one studies; the directory name does not silently generalize
their represented rank. It composes the public
`ksdft2effmass.campaigns.research_monograph.impurity_defect_2d` planning Workflow and
the reusable `ksdft2effmass.solidstate` lattice records.

The retained finite-domain inventory is a **planning result only**. A separate authored
Folding and Null-Alignment Controls package performs bounded dimensionless synthetic
folding and known-map null extraction; neither of those packages reads accepted-parent
evidence. The retained parent-qualification package binds an authenticated projection
of accepted historical synthetic parent evidence to maintained construction and
independent-reconstruction routes. None of these packages establishes finite-domain
convergence, isolated-defect behavior, scientific or material validation, or an
uncertainty statement. They do not authorize Quantum ESPRESSO, Wannier90, remote
computation, or the 3,240-evaluation defect campaign.

The maintained [research protocol](research_protocol/research_protocol.tex) fixes the
scientific questions, represented spaces, complete operator and diagnostic mathematics,
named workstream controls, finite-domain inventory, thresholds, the smallest
isolated-defect-like cell objective, independent-verification boundary, parity gate,
retention policy, and explicit nonclaims for this calculation family. Its in-document
schematics cover quotient seams, defect supports and periodic images, compatibility and
alignment, gauge routes, symmetry, aliasing regimes, workstream gates, size selection,
and independent verification. The protocol also retains a recommendation-only graph
atlas with explicit retained, planning-derived, and blocked statuses. Build it without retaining auxiliary products
with:

```bash
mkdir -p /tmp/periodic2d_rank_defect_protocol
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=/tmp/periodic2d_rank_defect_protocol \
  research_protocol/research_protocol.tex
```

The generated PDF is a local rendering and is not the protocol source of record.

## Retained protocol figures

`figures/` preserves the two version-one plots derived only from retained JSON
records:

- `folding-null-residuals.pdf` and `.png` show the maximum folding and null-alignment
  metric for each authored case relative to the prospective `1e-11` criterion; and
- `finite-domain-inventory.pdf` and `.png` visualize the unexecuted case and proposed
  operator-evaluation counts.

`figures-v2/` preserves the pre-qualification recommendation subset. `figures-v3/`
retains the complete currently supportable atlas: those ten folding/null and planning
figures plus the parent-qualification metric atlas, inherited truncation losses,
uniform/seam bridge residuals, aggregate independent-reconstruction comparison, and
measured resource observations. These are retained numerical, execution-free
inventory, or frozen planning-geometry figures; none presents an unexecuted combined
defect operator as a result.

The figures do not run an operator-producing calculation. Their renderer authenticates
the retained result and inventory by SHA-256 and refuses to overwrite existing output.
From `python/`, a fresh development rendering may be generated with:

```bash
uv run python \
  ../calculations/periodic2d_rank_defect/render_research_protocol_figures.py \
  --output-root /tmp/periodic2d_rank_defect_figures
```

## Retained planning packages

`executions/finite-domain-defect-planning-v2/` is the current execution-free inventory.
It records:

- ten ordered square area geometries from `1x1` through `16x16`, including explicit
  `1x1` through `5x5` small-cell periodic-aliasing controls;
- five fixed-area shape geometries, with the shared `12x12` geometry evaluated once;
- two anisotropic orientation pairs;
- two frozen synthetic defect identifiers;
- the complete `9x9` boundary-twist mesh;
- 2,268 unique isotropic cases;
- 324 orientation comparison records; and
- 3,240 proposed operator evaluations after accounting for three evaluations per
  orientation record.

The `1x1` through `4x4` cells alias radius-two defect support with periodic images. The
`5x5` through `8x8` cells can still alias the retained radius-18 parent hopping support.
They are controls of quotient behavior, not isolated-defect or convergence evidence.
The inventory preserves separate area, shape, orientation, and boundary-phase channel
memberships. Its counts are execution proposals, not evidence that the evaluations
occurred.

`executions/finite-domain-defect-planning-v1/` retains the superseded 2,430-evaluation
inventory without rewriting its scripts, bytes, or verification record.

## Authored Folding and Null-Alignment Controls package

`executions/folding-null-controls-v1/` is a **CALCULATED SYNTHETIC RESULT — UNSEALED**.
It uses an explicitly authored dimensionless Hermitian nearest-neighbor parent, the
adopted shapes `6x6` and `8x8`, four boundary twists per shape, and the known
translation/site-phase/energy-reference attack. The producer uses the maintained
public quotient-seam constructor and explicit finite Bloch folding. Independent
verification reconstructs the seam matrices, Fourier transform, primitive energies,
and null attack through separate Kronecker arithmetic.

The package contains eight cases and passes its prospective `1e-11` algebraic and
folding-unitarity criteria. That pass establishes only the retained synthetic numerical
behavior.

## Accepted historical synthetic parent qualification

`executions/parent-qualification-v1/` is a **CALCULATED NUMERICAL CAPABILITY
QUALIFICATION**. It binds historical revision
`c5d34a93b4710a4a430738c404c775865d418d42` and the accepted periodic input, periodic
result, Stage B parent evidence, and Stage C accepted-parent result identities. It
qualifies three rank-one dimensionless scalar parents:

- `isotropic_lambda_0p5_0p5_0`;
- `anisotropic_lambda_0p3_0p7_0`; and
- the separately identified axis-swapped `anisotropic_lambda_0p7_0p3_0`.

The calculation evaluates all fourteen unique planned shapes and all 81 boundary
twists through separate centered-uniform-link and quotient-seam routes. This comprises
6,804 parent route constructions and 4,536 route constructions for the two frozen
Hermitian perturbation inventories. Exact historical compact-hopping identities,
coefficient Hermiticity and symmetry, represented Hermiticity, gauge bridges, and
plane-wave separability pass their prospective criteria. Independent verification uses
FFT reconstruction and direct sparse seam/uniform arithmetic; its maximum aggregate
metric difference is `2.79359868571305e-14`.

Inherited radius-18 parent truncation remains explicit rather than being treated as
zero: the maximum represented losses at the two historical twists are approximately
`3.95544e-06` for the isotropic parent and `5.73302e-05` for each anisotropic parent,
with Frobenius losses `6.41720e-05` and `6.76334e-04`, respectively. Qualification of
these exact synthetic parents does not establish material validity or select an
adequate finite cell. The additive `source-projection-audit.json` authenticates the
request against the exact historical Git objects without restoring the removed tree;
`manifest-amendment-v1.json` binds that audit, the implementation modules, all three
qualification scripts, and installed package versions without replacing the original
manifest.

## Entry points

- `run_01_plan.py` and `run_02_verify.py` preserve replay of the superseded version-1
  planning package.
- `run_05_plan_finite_domain_controls.py` constructs the current version-2 definition,
  including the small-cell aliasing controls, through public records.
- `run_06_verify_finite_domain_controls.py` authenticates and reconstructs the
  version-2 planning inventory.
- `run_03_folding_null_controls.py` calculates the bounded authored folding/null result
  through the maintained public campaign and solid-state APIs.
- `run_04_verify_folding_null_controls.py` independently reconstructs the Folding and
  Null-Alignment Controls result without importing the producer script or production
  constructor.
- `run_07_qualify_parents.py` qualifies the three exact accepted historical synthetic
  parents over the complete planned shape/twist inventory through the public
  calculation Workflow.
- `run_08_verify_parent_qualification.py` independently reconstructs the retained
  qualification without importing or invoking its production calculator.
- `run_09_audit_parent_qualification_source.py` read-only authenticates the request
  projection against exact historical Git objects and creates an additive manifest
  amendment; it performs no parent or defect calculation.

From `python/`, a new development copy may be produced and verified with:

```bash
uv run python \
  ../calculations/periodic2d_rank_defect/run_05_plan_finite_domain_controls.py \
  --output-root /tmp/finite-domain-defect-planning-v2
uv run python \
  ../calculations/periodic2d_rank_defect/run_06_verify_finite_domain_controls.py \
  --execution-root /tmp/finite-domain-defect-planning-v2
uv run python \
  ../calculations/periodic2d_rank_defect/run_03_folding_null_controls.py \
  --output-root /tmp/folding-null-controls-v1
uv run python \
  ../calculations/periodic2d_rank_defect/run_04_verify_folding_null_controls.py \
  --execution-root /tmp/folding-null-controls-v1
```

The first pair is execution-free software composition. The second pair performs only a
small local authored synthetic calculation and independent reconstruction; it performs
no external or protected computation. Both retained packages use no-overwrite behavior;
do not replace them in place.

## Architecture and blocked successor work

The maintained public package now owns finite-domain case planning plus typed folding
and null-alignment definitions, results, canonical serialization, calculation,
independent verification, and Workflow contracts. Historical consumed-authorization,
provenance, and structured-stop surfaces are not reactivated. Generic finite-lattice defect representation,
extraction, and locality mechanics remain solid-state/periodic owners. Historical onsite-extraction and defect-model contracts (legacy Stage B/C) and retained
scientific parents are not restored here as active implementation.

The retained version-one package now closes the parent identity, represented rank-one
state space, basis/order, gauge/twist, energy reference, unit, support, inherited
truncation, defect-term, production-construction, independent seam/gauge reconstruction,
criterion, resource, provenance, and retention portions of the calculation-local
parent-qualification gate for these three exact synthetic parents.

The broader periodic2d capability-parity program remains open, and qualification does
not activate an operator-producing successor. Onsite Extraction and Covariance
Controls, Defect-Model Discrimination, and Finite-Domain Sensitivity still require
maintained campaign Workflows and result contracts. The finite-domain campaign also
requires prospective absolute isolation thresholds before execution. The current
3,240-evaluation inventory remains unexecuted and separately unauthorized.

## Historical relation

The removed `calculations/research-monograph/impurity-defect-2d/` tree remains available
through Git history and test-owned digest-bound fixtures. It is a provenance donor, not
the maintained calculation owner. This directory preserves the adopted finite-domain
inventory without reintroducing deprecated runners, consumed authorizations, or old
accepted-parent execution routes.
