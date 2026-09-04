# Periodic contract verification

## Status and identity

This page records the human-accepted, administratively closed implementation and
compatibility disposition for `migration.v2.periodic.contract-verification`. The
target owner is `ksdft2effmass.periodic`; its parent Task is
`migration.v2.periodic`.

This bounded acceptance establishes software-contract verification only. It does not
authorize scientific execution, select production geometry, or establish numerical
verification, scientific validation, uncertainty quantification, release, or
publication.

## V1 source responsibilities

The retained public surface is `python/src/ksdft2effmass/periodic/`. It owns:

- explicit unit, physical-dimension, coordinate, reciprocal-scale, and k-point
  normalization enums;
- immutable direct- and reciprocal-lattice records;
- ordered atomic-species, periodic-site, and periodic-structure records; and
- ordered k-point coordinates and weights with an explicit reciprocal scale.

Quantum ESPRESSO QEXSD construction consumes these records from the integration
owner. `ksdft2effmass.ksdft.pw` embeds them in the existing aggregate
Kohn--Sham plane-wave record and owns that aggregate wire format.

## Target concern and exclusions

The v2 owner remains `ksdft2effmass.periodic`. It has no dependency on
calculator, integration, QEXSD, Kohn--Sham, workflow, or analysis packages.
Calculator invocation, native-format parsing, workflow control, spectral state,
and scientific acceptance remain outside this package.

The v2 architecture defers exact future internal modules and standalone public
wire exports. This verification therefore introduces neither a periodic
serializer nor a periodic schema.

## Compatibility disposition

The existing thirteen geometry and enum exports are retained, and
`ReciprocalLatticeCompatibilityValidator` is added as the ActionObject owner of
direct--reciprocal compatibility and its explicit absolute tolerance. Represented
vectors continue to require finite built-in `float` components; booleans,
numeric strings, and nonfinite values are rejected. Direct and reciprocal
vectors retain their explicit bohr and inverse-bohr units, exact represented
`2*pi/alat` scale relation, and componentwise duality tolerance. Species and
sites retain source ordering, unique species names, one-based contiguous site
indices, and resolvable species references. K points retain exact represented
scale and weight-normalization states.

`ReciprocalLattice` now owns only its intrinsic fields and exact raw-to-physical
scale relation. It no longer stores a `DirectLattice` or a compatibility tolerance.
The validator receives both independently valid lattices and a positive finite
built-in-float tolerance explicitly, checks $A B^T = 2\pi I$ componentwise, and
leaves both inputs unchanged.

Wrong semantic types now fail at the public constructor boundary with
`TypeError`, including malformed vector containers, scalar types, and aggregate
members. Correctly typed values that violate finiteness, positivity, cardinality,
ordering, reference, scale, unit, or normalization invariants raise
`ValueError`. This is the repository-wide documented exception taxonomy, not a
new scientific convention. No numeric values are converted, so overflow in an
external parser remains the responsibility of that integration boundary.

Serialization remains with the current aggregate
`KohnShamPlaneWaveCalculationRecordJsonSerializer`. Its schema-version-1
`duality_absolute_tolerance` field is retained as serializer-owned validation
policy rather than `ReciprocalLattice` state. Deserialization applies the public
validator before returning a record, and serialization applies the same validator
before emitting canonical bytes. A standalone periodic wire would be a separate
public-contract decision because the v2 architecture does not currently determine
its fields or versioning.

## Verification

Direct software verification covers the exact public import inventory,
immutable value behavior, ActionObject-owned analytic cubic direct--reciprocal
consistency and incompatibility rejection, structure ordering and references,
k-point scaling and normalization, numeric
input rejection, aggregate type rejection, and forbidden dependency edges.
Existing QEXSD construction and Kohn--Sham aggregate serialization tests remain
regression evidence for consumer compatibility.

The analytic cubic case checks represented constructor behavior only. It does
not claim convergence, suitability of a physical geometry or sampling, or
agreement with an independent electronic-structure result.

## Cutover and rollback

No package move, schema-version change, fixture migration, or dependency change
is required. Existing constructors in the QEXSD translator and aggregate
serializer now invoke the validator explicitly; maintained schema-version-1 bytes
retain their field names and canonical representation. A regression can be rolled
back by reverting the lattice/validator boundary, its two consumers, and its direct
tests together; it must not be addressed by adding calculator-specific behavior
to `periodic`.

## Residual limitations

Architecture v2 still defers a standalone periodic wire, exact future internal
module decomposition, additional coordinate conventions, additional unit
systems, and additional k-point normalizations. Cross-object scale and count
checks still owned by `KohnShamPlaneWaveCalculationRecord` are outside this
periodic Task and remain for `migration.v2.ksdft.contract-verification` to
disposition. Those omissions do not block the periodic contract verified here.
