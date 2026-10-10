# `ksdft2effmass.periodic1d.isolated_band.serialization`

## Purpose and status

Implemented deterministic wire serializer for the complete M1 result.

## Public contract

- [`Periodic1DIsolatedBandResultJsonSerializer`](Periodic1DIsolatedBandResultJsonSerializer/index.md)

The serializer emits schema
`ksdft2effmass.periodic1d.isolated-band-calculation-result.v1` as sorted compact UTF-8
JSON with one terminal newline and no nonfinite values.

## Ownership and dependencies

The module owns wire mechanics only. It may encode quantities, vectors, spectra, and
complex matrices, but must not recompute diagnostics or decide validity. Schema identity
is distinct from M2/M3.

## Mapping and evidence

Source: `python/src/ksdft2effmass/periodic1d/isolated_band/serialization.py`.
Direct evidence is `test_serializer__uses_distinct_deterministic_schema_v1` plus
fresh-calculation byte determinism.

## Limitations

Serialization is one-way in the maintained library surface; strict retained decoding is
implemented by the standalone verifier. Byte determinism does not establish semantic
validity.
