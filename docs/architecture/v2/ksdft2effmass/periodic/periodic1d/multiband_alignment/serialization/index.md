# `ksdft2effmass.periodic1d.multiband_alignment.serialization`

## Purpose and status

Implemented deterministic serializer for the complete M2 result.

## Public contract

- [`Periodic1DMultibandAlignmentResultJsonSerializer`](Periodic1DMultibandAlignmentResultJsonSerializer/index.md)

It emits schema
`ksdft2effmass.periodic1d.multiband-alignment-calculation-result.v1` with canonical key
order, compact separators, strict finite JSON values, ordered complex pairs, and one
terminal newline.

## Ownership and dependencies

The serializer owns wire representation only and cannot recompute alignment or
locality evidence. It records pointwise and global channels separately.

## Mapping and evidence

Source: `python/src/ksdft2effmass/periodic1d/multiband_alignment/serialization.py`.
Direct evidence covers schema distinction, byte determinism, and standalone contract
tampering.

## Limitations

Canonical bytes aid correlation but do not establish chronology or semantic validity.
Strict wire verification belongs to the retained verifier.
