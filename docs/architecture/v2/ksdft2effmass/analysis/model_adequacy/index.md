# `ksdft2effmass.analysis.model_adequacy`

## Purpose and status

This is the prospective scientific-analysis owner for KSD-specific model-adequacy
normalization, channels, admissibility, certificates, and hierarchy policy. No
`ksdft2effmass.analysis.model_adequacy` Python package or supported import exists in this
candidate. It has no common serializer, admissible-set API, certificate API, HSH
implementation, or calculated result.

The scientific loss channels are the dimensionless ordered spectral RMS loss $L_E$ and
the dimensionless represented-operator RMS loss $L_H$. A positive-definite quadratic is
not a third channel: it is a reusable completed-square representation of $L_E^2$ or
$L_H^2$ over a declared affine candidate family.

Generic immutable evaluation of that quadratic is supplied by exact-pinned
`projectkoios-optimization` commit `ec3d290…` through
`projectkoios.optimization.adapters.PositiveDefiniteQuadraticLoss`. The
[`exports/optimization`](../../../../../../exports/optimization/README.md) page records
the completed transfer; no duplicate source remains here. Current M3 public routes and
retained wire identities remain unchanged. Direct $L_E$ construction, $L_H$
normalization, general admissible sets, and general certificates remain unimplemented.
Reusable dimensionful hopping/path aggregation belongs to PhysKit.

The prospective HSH-1 child is a separate domain-specific adequacy analysis. It owns
one finite two-dimensional hopping-shell hierarchy, including source correlation,
classes, scientific weight and bound selection, thresholds, witnesses, support certificates, and
bounded class/hierarchy dispositions. It is planned to compose PhysKit lattice
primitives and `projectkoios.optimization.ParameterSpace`. Missing reusable PhysKit
behavior belongs under the
[`exports/physkit`](../../../../../../exports/physkit/README.md) boundary; remaining generic optimization behavior belongs to Optimization, with
prospective
transfer work recorded under `exports/optimization`. HSH-1 remains draft,
unfrozen, and unimplemented.

The ownership selection is explained in the
[model-adequacy ownership decision](../model-adequacy-ownership-decision.md).
Cross-cutting contracts are recorded in the
[scientific boundary](scientific.md), [numerical contract](numeric.md), and
[ownership and data-flow schematic](schematic.md).

## Public contract

The current and prospective child surface is:

| Child | Responsibility | Status |
|---|---|---|
| [`hopping_shell_hierarchy`](hopping_shell_hierarchy/index.md) | HSH-1 source projection, nested shell classes, proof objects, and bounded dispositions | Architecture selected; not implemented or frozen |
| [`exports/optimization`](../../../../../../exports/optimization/README.md) | Completed quadratic transfer record and remaining prospective owner map | No active quadratic source; accepted owner commit exact-pinned |
| [`exports/physkit`](../../../../../../exports/physkit/README.md) | Reuse map and future PhysKit-bound candidates | No new source candidate yet |

Future general `admissible_sets` or `certificates` children require separate accepted
contracts. HSH-local admissible sets and certificates do not create those general
packages.

## Ownership boundary

This subpackage owns KSD-specific scientific mathematics and may own further analysis
after physical or mathematical objects have been placed in declared comparison
coordinates. It may own:

- normalized loss definitions and immutable loss results;
- parameter-space sublevel-set geometry;
- witness semantics that require one candidate to satisfy every declared criterion;
- reconstructable separation-analysis primitives; and
- explicit numerical and claim boundaries.

It does not own:

- finite represented-operator records, compatibility, subtraction, primitive norms, or
  PhysKit-owned units and dimensionful path/sample aggregation;
- periodic parent models, Bloch geometry, Fourier transforms, hopping construction, or
  alignment mechanics;
- campaign-specific candidate families, shell inventories, mesh roles, thresholds,
  source correlation, retained schemas, or dispositions;
- a general optimizer or mutable objective registry; or
- human scientific acceptance, material validation, or uncertainty quantification.

A raw metric becomes a model-adequacy loss only through an explicit definition of
sampling, weights, normalization, units, and intended mathematical role. The package
must not infer those controls from array shape or caller context.

## Dependency rules

Permitted inward dependencies are:

- `ksdft2effmass.operators` for already identified represented-operator records and
  primitive comparison results;
- sibling `ksdft2effmass.analysis` contracts such as explicit periodic-band samples;
- `ksdft2effmass.periodic` and dimension-specific periodic model/result records when an
  outward analyzer requires them;
- PhysKit lattice, hopping, symmetry, and represented-operator primitives;
- exact-pinned `projectkoios.optimization` parameter-space and quadratic-adapter
  contracts;
- project quantity and serialization primitives where selected by a later contract; and
- NumPy/SciPy numerical kernels at explicit dense boundaries.

Forbidden dependencies are:

- calculator packages or protected execution;
- campaign Workflows as inward loss semantics;
- retained calculation files or filesystem discovery inside DataObjects and
  ActionObjects;
- imports from outward publications; and
- reverse imports from inward periodic model packages to adequacy Actions.

An outward HSH or M3 analyzer may depend on periodic parents. A periodic parent/model
package must not import that outward analyzer.

## Mathematics, science, and workflow boundary

Nontrivial formulas and scientific semantics belong in immutable DataObjects and pure,
typed ActionObjects under their domain owner. Workflow and retained-script layers may
correlate identities, order calls, select explicitly declared branches, persist bytes,
and route failures. They must not privately reimplement projection, loss construction,
quadratic geometry, feasibility, distance, certificate, or hierarchy semantics.

This rule does not imply an abstract inheritance framework. The Optimization owner
supplies one public backend-selecting quadratic facade; no local duplicate implementation
exists. Later HSH implementation must
first select cohesive public scientific Actions for its nontrivial stages; a workflow or
monolithic private helper cannot become the sole owner of verifiable mathematics.

## Child map

- [`hopping_shell_hierarchy`](hopping_shell_hierarchy/index.md)
- [`exports/optimization`](../../../../../../exports/optimization/README.md)
- [`exports/physkit`](../../../../../../exports/physkit/README.md)
- [Scientific boundary](scientific.md)
- [Numerical contract](numeric.md)
- [Ownership and data-flow schematic](schematic.md)
- [Migration and compatibility plan](migration.md)
- [Ownership decision](../model-adequacy-ownership-decision.md)

## Code and export mapping

| Path | Role | Status |
|---|---|---|
| `python/src/ksdft2effmass/analysis/model_adequacy/` | Future KSD-specific analysis owner | Absent; no supported import |
| `exports/optimization/` | Completed quadratic-transfer record and future candidate boundary | No active source; owner commit `ec3d290…` accepted and pinned |
| `exports/physkit/` | Existing-API reuse map and future target-relative candidates | Staged boundary; no new source yet |
| `python/src/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy/` | Future HSH-1 domain owner | Absent; prospective only |

## Test mapping

Optimization owns its adapter test suite. Consuming-project smoke tests cover the
exact-pinned `ParameterSpace` contract and quadratic facade at
`python/tests/software_verification/ksdft2effmass/analysis/test__ProjectKoiosOptimizationParameterSpaceDependency.py`
and
`python/tests/software_verification/ksdft2effmass/analysis/test__ProjectKoiosOptimizationQuadraticLossDependency.py`.
HSH-1 requires separate software and numerical verification. Its independent verifier
must reconstruct formulas and invariants without calling producer evaluators. M3's
independent verifier remains separate.

## Sphinx mapping

There is no model-adequacy Sphinx API page because no local public API exists. The
external-dependency catalog records the exact Optimization owner revision and consuming
surface.

## Provenance

Original local work under the repository license. The selected quadratic mathematics
is explained in
`docs/publications/research-monograph/chapters/admissible-sets-and-certificates.tex`.
The architecture does not transfer any retained M3 outcome or evidence status to a new
API.

## Evidence

| Evidence kind | Status | Evidence or reason | Validity domain |
|---|---|---|---|
| Software verification | Dependency evidence | Optimization reports 95 owner cases plus clean Ruff/mypy/build/wheel gates; 5 focused consuming-project parameter-space/quadratic cases pass locally | Exact-pinned owner API and dependency boundary only; no local model-adequacy API |
| Numerical verification | Bounded dependency smoke evidence | Dense and sparse facade values agree with one hand-derived completed square | Selected smoke case only; not a retained scientific campaign |
| Scientific validation | Not evaluated | Mathematical analysis contract only | None |
| Uncertainty quantification | Not applicable | Deterministic losses are not uncertainty models | None |
| Human acceptance | Not applicable | Namespace selection is not scientific acceptance | None |

## Limitations and deviations

No local slice implements direct $L_E$ construction, $L_H$ normalization, spectral
weights, operator-path sampling, threshold or bound selection, admissible-set
dispositions, support arithmetic, or serializers. The generic closed-box record is
reused from `projectkoios.optimization`; no local coordinate-box type is introduced.
HSH-1 remains blocked on unresolved controls, missing PhysKit-owned foundations, and
outward-rounding policy; generic quadratic availability is no longer a blocker. Current
M3 quadratics remain implemented and supported at their existing `periodic1d` route.
Any later delegation is a separately reviewed behavior-preserving implementation change.
