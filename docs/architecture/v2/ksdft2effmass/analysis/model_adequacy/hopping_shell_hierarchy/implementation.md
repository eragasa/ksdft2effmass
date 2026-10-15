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
allowed dependency direction is from this analysis package toward those periodic model
owners; periodic packages do not import HSH-1. HSH-1-specific shell policy, thresholds,
source correlation, certificates, and dispositions remain local.

## Producer algorithm

`Periodic2DHoppingShellHierarchyCalculator.execute()` is planned to:

1. validate the exact composed scalar-parent definition and source identities;
2. reconstruct the centered finite hopping family from the self-contained input;
3. measure Hermiticity, imaginary, and $D_4$ defects and fail before projection when a
   frozen source tolerance is exceeded;
4. project accepted blocks onto a canonical exact real orbit target and fix the common
   energy zero;
5. build maximal-space orbit functions, multiplicities, shell masks, coefficient box,
   and fixed metric;
6. assemble full spectral and operator squared-loss forms and independently restrict
   them to each active shell slice;
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
- Private numerical kernels convert once to dense NumPy arrays.
- The HSH wrapper exposes maximal-energy-space `squared_loss`, owns the energy scale,
  active-to-maximal map, inactive-zero policy, channel/shell identity, and reconstruction
  defects, maps active coefficients to dimensionless ratios, and delegates completed-
  square evaluation to sibling
  `analysis.model_adequacy.losses.DimensionlessPositiveDefiniteQuadraticLoss`.
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
must not invoke the common constructor, `squared_loss`, or `rms_loss`; otherwise a shared
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
`ksdft2effmass.periodic2d.hopping-shell-hierarchy-result.v1`. Encoding preserves exact
source identities, controls, orbit order, weights, quadratics, feasible points,
certificates, class outcomes, withheld roles, limitations, and nonclaims. Canonical JSON
forbids nonfinite values and rejects unknown fields on decode.

## External boundary

HSH-1 is local synthetic work. Its implementation must not execute Quantum ESPRESSO,
Wannier90, schedulers, remote resources, or cloud services. It does not depend on the
Si-VC production campaign.

## Current implementation mapping

There is no current source mapping. The existing
`python/src/ksdft2effmass/periodic2d/studies.py` scaffolds M4 and M5 dependency
boundaries and must not be repurposed as an HSH-1 result implementation.
