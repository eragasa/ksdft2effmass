# `ksdft2effmass.periodic1d.admissible_sets.serialization`

## Purpose and status

Implemented deterministic serializer for the complete M3 result.

## Public contract

- [`Periodic1DConstrainedAdmissibleSetResultJsonSerializer`](Periodic1DConstrainedAdmissibleSetResultJsonSerializer/index.md)

It emits schema
`ksdft2effmass.periodic1d.constrained-admissible-set-result.v1`, including
units, parameter meaning, all sampled losses, proof quadratics, evaluation roles,
witnesses, separation certificates, locality evidence, and bounded non-claims.

## Ownership and dependencies

The serializer owns wire mechanics only and must not derive dispositions or recompute
proof objects. It encodes only finite JSON values with canonical ordering and one
terminal newline.

## Mapping and evidence

Source: `python/src/ksdft2effmass/periodic1d/admissible_sets/serialization.py`.
Direct evidence covers deterministic schema bytes and retained tamper detection.

## Limitations

Wire units are explicit expressions, not a replacement for typed in-memory unit
objects. Canonical encoding does not prove scientific validity.
