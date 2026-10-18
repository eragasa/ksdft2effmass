# Model-adequacy migration and compatibility plan

## Migration objective

Introduce `ksdft2effmass.analysis.model_adequacy` without breaking maintained M3 public
imports, changing retained M3 schema-v1 bytes, weakening verifier independence, or
forcing an unimplemented HSH protocol to adopt premature common policy.

The migration is staged. Architecture documentation authorizes no source move by
itself.

## Current-to-target ownership

| Current or prospective object | Current owner | Target disposition |
|---|---|---|
| Finite represented-operator compatibility, difference, and primitive residuals | `ksdft2effmass.operators` | Remains inward; unit-bearing hopping/path aggregation $R_H$ is assigned to PhysKit |
| Periodic parent/model/Fourier primitives | `periodic`, `periodic1d`, `periodic2d`, `solid_state`, and PhysKit periodic lattice primitives | Compose exact-pinned PhysKit owners; do not duplicate lattice displacement, symmetry-operation, hopping, or represented-operator types |
| Ordered finite closed parameter box | `projectkoios.optimization.spaces.parameters.ParameterBound` and `ParameterSpace` | Reuse exact-pinned dependency directly; HSH owns names, bound selection, and scientific invariants, not the generic container |
| M3 `Periodic1DQuadraticLoss` | `periodic1d.admissible_sets` | Maintained compatibility wrapper; may delegate behavior later |
| M3 calculation/result/serializer/verifier | `periodic1d.admissible_sets` | Current route preserved; complete outward migration requires separate review |
| Generic unit-free SPD quadratic | `projectkoios-optimization` | Initially implemented at commit `ec3d290…`, consumed from accepted migration commit `2c6dd7f…` through `projectkoios.optimization.quadratic.quadratic.PositiveDefiniteQuadraticLoss`, and exact-pinned here |
| Generic unit-free affine-quadratic construction and positive diagonal metric | Active donor candidates under `exports/optimization/` | Requires Optimization owner review, immutable owner commit, and separately authorized dependency repin before runtime use |
| Generic hopping orbits, shells, real symmetry projection, and dimensionful Frobenius geometry | Active donor candidates under `exports/physkit/` | Requires PhysKit owner review, immutable owner commit, and separately authorized dependency repin before runtime use |
| Prospective HSH shell/channel wrapper and certificates | Not implemented | Outward HSH owner under `analysis.model_adequacy`; HSH policy remains local to that child |
| Generic spectral RMS loss $L_E$ | Private duplicated calculations only | Deferred pending stable sample contract |
| Generic dimensionful hopping/operator RMS residual $R_H$ | Absent | Deferred to PhysKit, composing already compatible primitive residuals |
| Generic normalized represented-operator loss $L_H$ | Private duplicated calculations only | Deferred here; must consume PhysKit-owned $R_H$ |

## Phase 0 — architecture only

Deliverables:

- accepted ownership decision;
- package, scientific, numerical, schematic, and migration pages;
- exact prospective class and import names; and
- explicit M3/HSH compatibility boundaries.

No Python, tests, Sphinx API, calculation outputs, or sealed retained evidence change.
A draft HSH planning protocol may be added, but no generated HSH input, result, or
verification record exists in this phase.

## Phase 1 — Optimization quadratic owner surface

**Complete.** Optimization supplied its initial owner implementation at immutable
commit `ec3d2907097a659aef4be2b3384bd1922a9cb4dc`; the accepted KSD migration checkpoint
is `2c6dd7f717722f6b0495feb8cfe1287a104268a6`. Its public facade is
`projectkoios.optimization.quadratic.quadratic.PositiveDefiniteQuadraticLoss`, selecting
NumPy dense storage by default or SciPy CSR with `sparse=True`. The initial owner
checkpoint reported 95 passing tests plus Ruff, strict mypy, build, dependency-free
facade, and installed-wheel backend
smoke gates.

KSD initially exact-pinned that migration revision; the live lock now selects reviewed
Optimization descendant `d38e00ceef7f0fb1c137d5c3450d210c1ae4c99f` while retaining
focused consuming-project provenance, dense, sparse, and `ParameterSpace` smoke tests.
Superseded donor bytes were preserved in an external
recovery bundle and removed from active export staging, so there is no supported local
quadratic import or duplicate implementation. No M3 source, retained package, schema, or
verifier changed in this phase.

## Phase 1A — owner-foundation export candidates

Active flattened donor candidates under `exports/optimization/` and
`exports/physkit/periodic/lattice/` implement the smallest reusable foundation tranche:
unit-free affine-residual quadratic construction, unit-free positive diagonal metric
geometry, signed-axis displacement orbits, exact integer shells, scalar-hopping defect
analysis and real-orbit projection, and dimensionful full-block Frobenius distance.

These files are non-runtime transfer candidates. They do not create supported KSD
imports, alter the current exact dependency pins, or imply target-owner acceptance.
Target integration requires separate owner review and immutable owner commits; KSD may
consume those commits only after a separately authorized repin.

Feasibility, reconstructable box-constrained minima, common-witness search, support
optimization, set-distance bounds, and directed rounding remain unstaged.

## Phase 2 — M3 agreement without public migration

With upstream integration and dependency repinning complete, add bounded
software-verification fixtures showing agreement between the accepted Optimization
quadratic and current M3 `Periodic1DQuadraticLoss` for:

- hand-derived diagonal and cross-term cases;
- M3 spectral and operator quadratic values at multiple parameters; and
- adversarial malformed input behavior where the contracts intentionally agree.

The external object must not be used by the independent M3 verifier as its reconstruction
oracle. Passing agreement tests does not change retained M3 evidence or source
manifests.

A behavior-preserving internal delegation may be proposed only after agreement is
established. It must preserve:

- `Periodic1DQuadraticLoss` constructor fields;
- its supported import path;
- exact serializer field names and schema version;
- channel and alignment semantics; and
- existing error behavior unless a versioned change is separately accepted.

## Phase 3 — HSH reconciliation

The prospective HSH-1 architecture now selects the outward package route and documents
the following ownership fields. This closes documentation reconciliation only; it does
not freeze the calculation protocol, implement an API, select rounding software, or
satisfy any execution gate.

Before HSH implementation or protocol freeze, its outward architecture must continue to
state and preserve:

- source parent dependency on periodic2d;
- the active coefficient ordering and energy unit;
- the positive normalization scale mapping coefficients to dimensionless ratios;
- the HSH wrapper's shell, channel, active-index, exact inactive-zero rule, and
  correlation fields;
- whether its wire nests or inlines accepted external quadratic coefficients; and
- independent reconstruction that does not import producer loss construction.

HSH weights, coefficient-bound selection, normalization, certificate meaning,
arithmetic controls, thresholds, dispositions, and hierarchy policy remain HSH-owned.
Reusable source projection, orbit/shell construction, multiplicities, and dimensionful
hopping/Frobenius metrics belong to PhysKit.
The generic inclusive box is represented by `projectkoios.optimization.ParameterSpace`;
fixed inactive coordinates use equal lower and upper bounds rather than a tolerance.
The staged donor candidates must first be accepted and published by their owners; files
under `exports/` are not HSH runtime dependencies.

## Phase 4 — outward Action migration

Moving a complete M3 or HSH adequacy Action out of a periodic namespace is a separate
public-API migration. Before such a move:

1. enumerate every supported and internal import;
2. select the new defining module;
3. retain deliberate compatibility re-exports for maintained routes;
4. decide whether class `__module__` and serialized type identity change;
5. update architecture and Sphinx mappings;
6. rerun complete affected tests and retained standalone verifiers;
7. amend source-correlation records without rewriting historical manifests; and
8. obtain explicit authorization for commit and push.

No compatibility facade may silently create two independently maintained class types.
One defining type may have deliberate re-export routes.

## Phase 5 — later loss channels

Unit-free affine-residual and quadratic mechanics belong to optimization. The active
export candidate implements only affine construction over the existing quadratic
facade; it does not implement bounded feasibility or certificates. A KSD-specific
$L_E$ analyzer remains responsible for sampled-spectrum identity, physical-unit
compatibility, ordering, weights, rank normalization, energy scale, and overflow
behavior before crossing that unit-free boundary.

A common dimensionful aggregate $R_H$ requires a PhysKit contract for path/sample
identity, weights, rank normalization, common energy units, and physical
hopping/Frobenius geometry. Compatibility, subtraction, and primitive residuals remain
with represented-operator owners. A later model-adequacy $L_H$ object consumes that
energy-valued PhysKit result and the declared positive energy scale; it does not repeat
the aggregation.

Neither later channel is implied by the accepted quadratic facade.

## Rollback

The superseded export bundle was removed without changing M3. Rollback of the accepted
external dependency follows both repositories' explicit compatibility policies and
requires a separately reviewed repin. Retained calculation schemas and historical
source manifests are never rewritten merely to simplify rollback.

## Definition of done for architecture phase

Phase 0 is complete when:

- every documentation link resolves;
- package ownership and dependency direction are unambiguous;
- represented-operator, M3, and HSH boundaries are stated;
- the accepted external route and absence of a local public route are explicit;
- scientific and numerical nonclaims are explicit;
- Markdown hygiene and repository diff checks pass; and
- no local model-adequacy source capability is claimed as implemented.
