# HSH-1 implementation plan

## Target package layout

```text
python/src/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy/
    __init__.py
    definition.py
    calculate.py
    results.py
    serialization.py
    verify.py
```

The package is intentionally cohesive. General finite-periodic primitives already owned
by PhysKit or `ksdft2effmass.periodic2d` must be composed rather than duplicated. The
closed coefficient box composes exact-pinned
`projectkoios.optimization.ParameterSpace`; HSH does not introduce a competing box
record. The allowed dependency direction is from this analysis package toward those
reusable owners; periodic packages do not import HSH-1. PhysKit owns reusable symmetry
projection, orbit enumeration, hopping-shell construction, multiplicities, and
hopping/Frobenius physical geometry. HSH selects the shell-radius sequence and retains
bound selection, normalization, thresholds, source correlation, certificate meaning,
and dispositions.

## Mathematics, science, and workflow rule

HSH implementation must extract nontrivial mathematics and scientific semantics into
immutable DataObjects and pure, typed, independently testable ActionObjects before a
retained workflow is assembled. Workflow and retained scripts own correlation, call
ordering, explicit branching, persistence, and failure routing only. They must not own
private implementations of orbit projection, loss construction, bounded feasibility,
metric geometry, support bounds, or hierarchy resolution.

This requirement favors concrete composition over abstract base-class inheritance. The
generic quadratic facade is supplied by exact-pinned accepted Optimization migration
commit `2c6dd7f…`.
The exact public HSH stage-Action split must be accepted before HSH
source implementation; the aggregate
calculator may remain as a convenience composition Action, but it cannot be the sole
owner of mathematics hidden in private helpers.

## Producer algorithm

`Periodic2DHoppingShellHierarchyCalculator.execute()` is planned to compose public
semantic Actions that collectively:

1. validate the exact composed scalar-parent definition and source identities;
2. reconstruct the centered finite hopping family from the self-contained input;
3. compose PhysKit actions to measure Hermiticity, imaginary, and $D_4$ defects and
   fail before projection when a frozen source tolerance is exceeded;
4. compose PhysKit symmetry projection onto a canonical exact real orbit target, then
   apply the HSH-selected common energy-zero convention;
5. compose PhysKit orbit, multiplicity, hopping-shell, and physical metric objects;
   apply the HSH-selected shell-radius sequence; and build the HSH-selected
   `ParameterSpace` coefficient box and exact fixed-coordinate shell slices;
6. assemble full spectral and operator squared-loss forms, independently restrict them
   to each active shell slice, and construct the exact-pinned Optimization facade from
   explicitly normalized unit-free coefficients;
7. establish each channel's bounded-box minimum and nonemptiness;
8. retain a verified common witness or feasible pair and constructive upper bound;
9. construct one or more candidate separating directions, then retain only
   outward-rounded support certificates whose premises reconstruct;
10. assign per-class dispositions and resolve the hierarchy-level minimum-class claim;
11. evaluate only the retained fixed points on the withheld direct-parent mesh; and
12. return one immutable `Periodic2DHoppingShellHierarchyResult`.

No result object is partially mutable and no serializer performs a scientific
calculation.

## Representation choices

- Public vectors and matrices are immutable tuples of built-in numbers.
- Private numerical kernels use the explicitly selected NumPy dense or SciPy sparse
  representation; sparse inputs are not densified implicitly.
- The HSH wrapper exposes maximal-energy-space `squared_loss`, owns the energy scale,
  active-to-maximal map, exact inactive-zero rule, channel/shell identity, and reconstruction
  defects, maps active coefficients to unit-free ratios, and delegates completed-square
  evaluation to
  `projectkoios.optimization.quadratic.quadratic.PositiveDefiniteQuadraticLoss`.
  The definition retains `sparse` backend selection and relevant numerical provenance;
  backend choice is never inferred from matrix shape.
- The common coefficient box is an optimization `ParameterSpace`; derived class spaces
  copy active bounds and use `[0, 0]` bounds for inactive maximal coordinates.
- Feasible points and certificate directions are stored in the maximal space, making
  cross-class comparison and inactive-zero checking direct.
- Source and withheld samples retain exact roles and digest correlation outside the
  scientific value arrays.
- Dispositions are enums, not unconstrained strings inside library objects.

## Verification split

`Periodic2DHoppingShellHierarchyResultVerifier` consumes typed objects and reconstructs
all decisive numerical and semantic premises without calling the producer ActionObject.
The retained standalone verifier separately owns strict JSON schemas, unknown-field
rejection, manifest entry correlation, canonical-input regeneration, source-byte checks,
and the prohibition on producer imports.

Both routes must independently regenerate orbit inventories, shell masks, quadratics,
channel minima, feasible points, metric norms, support bounds, hierarchy logic, and
withheld values. The typed verifier may read common-quadratic fields for comparison but
must not invoke the common constructor, `squared_loss`, or `root_loss`; otherwise a shared
primitive defect could become its own oracle. Comparing only serialized hashes or
stored scalar summaries is insufficient.

## Failure behavior

Construction errors use `TypeError` for exact-type violations and `ValueError` for
invalid values or inconsistent immutable records. Top-level execution stops use stable
identities such as:

- `PERIODIC_2D.HSH.SOURCE_PROJECTION_DEFECT`;
- `PERIODIC_2D.HSH.ORBIT_INVENTORY_INVALID`; and
- `PERIODIC_2D.HSH.HIERARCHY_CORRELATION_INVALID`.

A class-local quadratic or certificate premise failure may be retained as the exact
`invalid-premise` disposition with a named reason, no distance interval, and no
hierarchy conclusion. The exact exception/result representation must be aligned with
the repository failure vocabulary before implementation. Invalid premises cannot be
downgraded silently to `unresolved-nonempty` or promoted to separation.

The outward-rounding backend must be selected from already authorized dependencies or
implemented with an accepted standard-library/numerical route. Adding or replacing an
interval-arithmetic dependency requires separate explicit human authorization and is
not authorized by this architecture draft.

## Serialization boundary

The planned schema identity is
`ksdft2effmass.analysis.model-adequacy.hopping-shell-hierarchy-result.v1`.
Encoding preserves exact source identities, controls, orbit order, weights,
quadratics, feasible points, certificates, class outcomes, withheld roles, limitations,
and nonclaims. Canonical JSON
forbids nonfinite values and rejects unknown fields on decode.

## External boundary

HSH-1 is local synthetic work. Its implementation must not execute Quantum ESPRESSO,
Wannier90, schedulers, remote resources, or cloud services. It does not depend on the
Si-VC production campaign.

## Current implementation mapping

There is no current source mapping. The existing
`python/src/ksdft2effmass/periodic2d/studies.py` scaffolds M4 and M5 dependency
boundaries and must not be repurposed as an HSH-1 result implementation.
