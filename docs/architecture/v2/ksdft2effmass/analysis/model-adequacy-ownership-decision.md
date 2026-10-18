# Model-adequacy loss and certificate ownership decision

## Status and scope

**Selected direction; first Optimization owner surface integrated and exact-pinned.**
KSD-specific model-adequacy analysis belongs under prospective
`ksdft2effmass.analysis.model_adequacy`. Generic unit-free parameter-space and quadratic
behavior is now consumed from `projectkoios-optimization`; remaining prospective
optimization ownership is recorded under `exports/optimization`. Missing reusable
physics and lattice mathematics is staged under `exports/physkit`. No local model-adequacy Python
package or supported import is implemented. This decision does not move a current public
symbol, rewrite a retained schema, implement HSH policy, or authorize a scientific
calculation.

The decision assigns one owner by semantics:

1. represented-operator mechanics remain with their represented-operator owner;
2. unit-free bounds, losses, metrics, feasibility, distance, dual norms, and support
   optimization belong to Project Koios Optimization;
3. dimensionful quantities, units, lattice symmetry, hopping shells and projection, and
   physically interpreted geometry belong to PhysKit;
4. KSD-specific normalization, channels, candidate hierarchy, controls, certificate
   meaning, and proof records belong to `ksdft2effmass`; and
5. human scientific acceptance remains outside the numerical objects.

The owner does not depend on how many consumers currently exist. Repository-level
`exports/` stages transfer bytes or records a completed transfer; it is never a runtime
import source.

## Problem

The maintained M3 calculation currently owns
`Periodic1DQuadraticLoss` inside
`ksdft2effmass.periodic1d.admissible_sets`. A prospective two-dimensional hopping-shell
hierarchy also needs completed-square spectral and operator loss geometry. Repeating the
same finite quadratic validation and evaluation in each calculation risks inconsistent
scalar validation, matrix conventions, and overflow behavior.

A generic `loss_functions` package would not solve the ownership problem. It would
invite raw metrics, fitting objectives, normalization policy, alignment searches,
thresholds, and scientific dispositions into one unbounded container. Likewise, moving
a parameter-space loss into `ksdft2effmass.operators` would confuse finite represented-
operator mechanics with higher-level model-adequacy analysis.

## Observed current ownership

- `projectkoios.physkit.periodic.lattice` owns reusable lattice coordinates,
  displacements, integral lattice operations, finite periodic domains, hopping records,
  and represented finite-lattice operators. HSH must compose those primitives rather
  than duplicate lattice geometry or represented-operator mechanics.
- `projectkoios.optimization` owns reusable bounded parameter contracts. Its
  `ParameterBound` and `ParameterSpace` already represent ordered, uniquely named,
  inclusive finite coordinate bounds, including exact fixed coordinates. A local
  model-adequacy coordinate-box type would duplicate that maintained contract.
- `ksdft2effmass.operators` owns finite represented-operator records, exact represented
  compatibility, guarded differences, primitive matrix norms, and fixed-representation
  residuals. It does not select alignment, fit model classes, or decide adequacy.
- `ksdft2effmass.analysis` owns higher-level deterministic scientific analysis,
  including alignment selection, model fitting, numerical policy, and explicit claim
  boundaries.
- `ksdft2effmass.periodic1d.admissible_sets` currently owns the complete M3 definition,
  calculation, quadratic result, witness/certificate results, serialization, and
  verification contract.
- Periodic parent/model namespaces own physical and mathematical periodic models. They
  are not the general owner of adequacy losses merely because one controlled analysis
  consumes a periodic parent.
- Scientific acceptance remains a human decision outside a numerical loss object or
  threshold comparison.

## Decision requirements

The selected architecture must:

- preserve `operators` as the inward owner of represented-operator compatibility,
  subtraction, and primitive residual mechanics while assigning reusable unit-bearing
  aggregation to PhysKit;
- keep scientific normalization, the meaning and selection of parameter bounds,
  admissible sets, and certificates in an outward analysis layer while composing
  generic bounded-coordinate records from `projectkoios.optimization`;
- reject Booleans, numeric strings, nonfinite values, malformed dimensions, and
  nonpositive curvature at public numeric boundaries;
- keep every maintained DataObject operationally immutable;
- distinguish a raw metric from a normalized loss, an optimization objective, a
  threshold, and a disposition;
- preserve current M3 public imports and retained schema-v1 bytes until a separately
  reviewed migration changes them;
- keep independent verifiers independent of producer construction and evaluation
  Actions; and
- separate reusable PhysKit shell/projection mechanics and optimization mathematics
  from HSH-selected radii, weights, bounds, normalization, rounding, and proof meaning.

## Considered options

### Option A — `ksdft2effmass.analysis.model_adequacy` (selected)

This option makes KSD-specific model adequacy an explicit scientific-analysis subdomain.
Its normalized channel wrappers and admissibility/certificate policy consume accepted
optimization and PhysKit primitives plus inward comparison results. It does not own
generic unit-free optimization objects or dimensionful physical primitives.

**Advantages**

- agrees with the accepted `analysis` responsibility for model fitting and scientific
  policy;
- prevents represented-operator mechanics from moving outward into a campaign owner;
- provides a coherent future home for KSD-specific normalized channels, admissible-set
  meaning, and certificates; and
- makes the dependency direction explicit rather than hiding it behind utility
  functions.

**Costs**

- higher-level M3 and future HSH adequacy Actions cannot remain inward periodic owners
  while importing outward analysis behavior;
- migration requires exact dependency pins, compatibility imports, and explicit
  retained-wire preservation; and
- HSH implementation remains blocked on owner review/publication of the staged
  PhysKit/Optimization foundations, missing feasibility/support certificates, and
  unresolved scientific controls, not on generic quadratic availability.

### Option B — top-level `ksdft2effmass.model_adequacy` (rejected)

A top-level package could be imported by both periodic and analysis namespaces only if
it remained an inward dependency-neutral mathematical kernel. It could not then
naturally own spectral sampling analysis or the policy that normalizes operator-owned
aggregates without reversing dependencies. The high-level name would overstate the responsibility of a
small mathematical utility package.

### Option C — `ksdft2effmass.operators.represented` (rejected for adequacy losses)

A future whole-package reorganization could place all represented-operator records and
mechanics below `operators.represented`, but moving only an operator-labelled adequacy
loss there would split one domain between flat and nested namespaces. Moreover, an HSH
coefficient-space loss is already downstream of representation and target projection;
it is not primitive `OperatorRecord` subtraction.

### Option D — keep every quadratic calculation-local (rejected)

This option duplicates unit-free completed-square evaluation that belongs to
optimization. Domain wrappers may remain local, but generic quadratic mechanics do not
acquire a KSD owner merely because target integration was once pending.

## Selected ownership boundary

### External reusable foundations

`projectkoios.physkit` supplies lattice and represented-operator primitives and owns
reusable square-lattice $D_4$ operation/orbit construction, deterministic orbit ordering,
hopping-shell construction, symmetry projection, multiplicities, and dimensionful
hopping/Frobenius geometry. HSH selects its shell-radius sequence and scientific use of
those objects. PhysKit behavior must build on maintained `LatticeDisplacement`,
`IntegralLatticeOperation`, and `LatticeDisplacementTransformer` contracts rather than
introducing competing integer-lattice types.

`projectkoios.optimization.ParameterSpace` is the reusable closed coordinate-box
representation. The HSH definition remains responsible for coordinate names, common
bounds, target/zero margin requirements, and exact derived active slices. A fixed bound
with equal endpoints represents an inactive coordinate exactly; solver tolerances do
not widen it. `ksdft2effmass` does not re-export or wrap `ParameterSpace` merely to
rename it.

The dependencies are pinned to exact accepted migration commits
`2c6dd7f717722f6b0495feb8cfe1287a104268a6` for Optimization and
`d81febb811fbc4feb014530fcae6cf6d9ad9ead5` for PhysKit. This reuse decision does not transfer HSH
scientific policy, feasibility proofs, certificates, or dispositions to the
optimization package.

### `ksdft2effmass.operators`

Retains ownership of:

- represented state-space and matrix identity;
- compatibility checks between declared represented spaces;
- signed represented differences;
- primitive maximum-entry, Frobenius, and spectral norms; and
- fixed-representation residual results.

PhysKit owns reusable unit behavior and dimensionful hopping/Frobenius aggregation. The
outward loss definition selects the scientific sample set and weights; neither
`operators` nor PhysKit infers or optimizes that policy.

It does not own thresholded model adequacy or parameter-space loss geometry.

### `exports/optimization`

Records the initial transfer of unit-free completed-square loss geometry to
`projectkoios-optimization` commit `ec3d290…` and its accepted migration through
`2c6dd7f…`; no duplicate quadratic source remains in this repository. The accepted
facade is
`projectkoios.optimization.quadratic.quadratic.PositiveDefiniteQuadraticLoss`, with NumPy dense
selection by default and SciPy CSR selection through `sparse=True`. Remaining affine,
metric, feasibility, distance, dual-norm, and support candidates are prospective and
have no staged source bytes.

### `exports/physkit`

Stages only genuinely missing reusable physical or lattice mathematics after existing
PhysKit capabilities have been exhausted. HSH must directly reuse existing lattice
displacement, integral-operation, finite-domain, hopping, and represented-operator
contracts. The export boundary may later hold reviewed orbit, shell, symmetry-projection,
or physically interpreted coefficient-geometry candidates; it currently contains no
new source.

### Prospective `ksdft2effmass.analysis.model_adequacy`

Owns KSD-specific normalization, spectral/operator channel semantics, admissible-set
meaning, witness/certificate policy, evidence roles, and domain-specific hierarchy
conclusions. It may consume accepted exact-pinned external primitives but must not host
generic export candidates merely to simplify local development.

### M3-local wrapper

`Periodic1DQuadraticLoss` continues to own M3 channel identity, optional alignment
angle, shift/splitting coordinate meaning, and retained schema-v1 representation. A
later behavior-preserving implementation may delegate validation and evaluation to the
exact-pinned upstream facade without changing public fields or wire bytes. Embedding
that external object as a new public field still requires a separately reviewed
versioned migration.

### HSH-local wrapper

A future HSH quadratic wrapper retains shell identity, channel identity, active maximal-
space indices, inactive-zero rules, coefficient normalization, source-correlation
defects, and reconstruction defects. It may contain or delegate to the exact-pinned
upstream facade only after converting its energy-valued coefficients to explicitly
declared unit-free canonical coordinates and selecting its dense or sparse backend
explicitly.

HSH retains spectral weights, scientific use of PhysKit-provided orbit multiplicities,
coefficient-box selection and scientific invariants, thresholds, normalization and
metric meaning, support direction, conservative
support endpoints, outward-rounding identity, certificates, class dispositions, and
hierarchy minimality. The coefficient-box container is
`projectkoios.optimization.ParameterSpace`; none of its HSH-specific meaning or any of
the other listed policy belongs to the generic quadratic facade.

## Represented-operator boundary

A represented-operator RMS channel has two layers:

1. `operators` establishes compatible represented differences and primitive residuals;
   PhysKit applies reusable unit-bearing hopping/Frobenius aggregation to produce the
   dimensional RMS residual $R_H$ under caller-declared samples and weights;
2. model-adequacy analysis applies the declared positive energy normalization $E_0$ to
   that result, producing the dimensionless loss $L_H=R_H/E_0$.

No general represented-operator model-adequacy loss module is selected in the first
extraction. HSH's orbit-multiplicity coefficient loss remains HSH-local because it
begins after exact projection into one common maximal coefficient space. A reusable
dimensionful hopping/path aggregation belongs to PhysKit and requires an explicit
sample contract; the adequacy layer must not duplicate its arithmetic.

## Certificate boundary

M3's axial Euclidean certificate and the proposed HSH weighted-metric, outward-rounded
support certificate do not yet share one software contract. Certificate generalization
is deferred. Each verifier reconstructs its own certificate premises and arithmetic
without importing the producer Action.

## Dependency direction

The target direction is:

```text
projectkoios.physkit periodic primitives ─┐
projectkoios.optimization spaces/quadratic ├─> analysis.model_adequacy
operators ────────────────────────────────┤             │
periodic model primitives ────────────────┤             └─> campaigns/publications
analysis band primitives ─────────────────┘
```

An inward periodic package must not import an outward adequacy Action. During migration,
current M3 compatibility routes may remain in `periodic1d` while new implementation is
introduced outward and old routes re-export deliberately. No source move occurs merely
because this decision exists.

## Consequences and migration order

1. **Complete:** document the prospective KSD-specific package and external ownership
   boundaries.
2. **Complete and superseded:** preserve then remove donor quadratic bytes after the
   Optimization owner supplied its own implementation.
3. **Complete:** pin accepted Optimization migration commit `2c6dd7f…` and verify the
   public facade from the consuming project.
4. Demonstrate exact agreement with the M3 quadratic over hand-derived and adversarial
   fixtures while the independent M3 verifier retains its own reconstruction.
5. Decide whether M3 delegates internally without changing public construction or wire
   identity; the dependency prerequisite is now satisfied.
6. Reconcile the HSH wrapper against accepted external primitives before HSH
   implementation or freeze.
7. Design any outward migration of complete M3/HSH adequacy Actions separately, with
   compatibility imports, Sphinx changes, architecture mappings, and retained-source
   amendments where applicable.
8. Place unit-free affine-residual construction and remaining generic optimization
   mathematics in Optimization after review; retain physical sampling, units, and
   normalization with their scientific owner. Generalize $L_H$ normalization only after
   PhysKit establishes a stable unit-bearing hopping/path aggregate contract.

## Evidence and authorization boundary

This is an architecture decision based on maintained package responsibilities and the
implemented M3 contract. The decision itself establishes no software behavior, numerical verification,
scientific validation, uncertainty quantification, or scientific acceptance. The
quadratic facade has owner software evidence and bounded consuming-project smoke
evidence, but neither establishes HSH scientific validity. Further source/API changes,
retained-package amendments, commits, and pushes require their applicable review and
authorization.
