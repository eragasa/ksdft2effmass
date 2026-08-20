# Kohn--Sham contract verification

## Status and identity

This page records the bounded implementation result for
`migration.v2.ksdft.contract-verification`. The neutral target owner is
`ksdft2effmass.ksdft`; the existing plane-wave aggregate remains owned by
`ksdft2effmass.ksdft.pw` pending later field-by-field migration.

This result authorizes no scientific execution and establishes no numerical
verification, scientific validation, uncertainty quantification, or production
acceptance.

## Retained neutral contract

`ksdft2effmass.ksdft` retains immutable representation-neutral spectral and
total-energy observations. Eigenvalues remain ordered Kohn--Sham observations,
not a complete many-body spectrum or a uniquely identified basis-independent
operator. Energy values use hartree, and unavailable energy-reference and
spin-resolved states remain explicit.

Public numeric inputs accept built-in Python scalar and tuple types only.
Booleans, numeric strings, NumPy scalars, and nonfinite values are rejected
rather than converted. Wrong semantic types raise `TypeError`; correctly typed
values that violate finiteness, positivity, shape, unit, or availability
invariants raise `ValueError`.

## Aggregate compatibility ownership

`KohnShamPlaneWaveCalculationRecord` retains intrinsic aggregate field and value
invariants. `KohnShamPlaneWaveCalculationRecordValidator` now owns compatibility
between independently valid components:

- reciprocal-lattice and sampled-$k$-point `alat` scales must agree exactly; and
- spectral row count must equal sampled-$k$-point count.

The QEXSD construction ActionObject and schema-version-1 serializer invoke the
validator explicitly. The serializer also invokes
`ReciprocalLatticeCompatibilityValidator`, preserving the existing aggregate
wire fields and canonical bytes. No schema version, retained fixture, dependency,
or native-format contract changes.

## Verification

Direct software verification covers the exact neutral public export inventory,
representative finite numeric rejection boundaries, immutable total-energy state,
compatible aggregate validation without mutation, and independent scale and count
disagreement. Existing
QEXSD construction, rejection, retained-artifact, schema, and canonical
serialization tests provide consumer regression evidence.

These checks establish documented software behavior only. They do not establish
physical band identity, energy alignment, sampling convergence, numerical
verification, scientific validation, or uncertainty quantification.

## Residual limitations

The prospective v2 split of calculator, integration, provenance, plane-wave, and
neutral Kohn--Sham fields remains deferred to its owning migration Tasks. This
bounded result introduces no standalone Kohn--Sham wire and does not retire the
schema-version-1 aggregate record.

Schema version 1 permits any positive duality tolerance. A serializer configured
with that represented tolerance preserves it exactly; the default serializer
intentionally rejects a wire carrying a different tolerance rather than silently
changing operation policy. Legacy callers consuming nondefault-tolerance wires must
configure the serializer from their declared contract before deserialization.
