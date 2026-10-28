# `ksdft2effmass.periodic1d.fourier_locality.verification`

## Status and responsibility

Byte-owning independent-verification module.

## Public classes

- [`FourierLocalityVerification`](FourierLocalityVerification/index.md)
- [`Periodic1DFourierLocalityVerification`](Periodic1DFourierLocalityVerification/index.md)
- [`Periodic1DFourierLocalityVerifier`](Periodic1DFourierLocalityVerifier/index.md)

## Admission boundary

The verifier accepts immutable built-in `bytes` only. Shared verification infrastructure
computes SHA-256 and decodes the typed result from those exact bytes. The family verifier
then constructs the authenticated projection from the admitted result and independently
recomputes the declared scientific channels for named fieldwise comparisons.

## Comparison policy

Exact identities, inventories, shapes, units, orderings, masks, and boolean dispositions
compare exactly. Binary64 scientific values use the configured mixed unit-aware rule.
Threshold-side disagreement fails closed even when values are otherwise within a
consistency tolerance.

## Exclusions

The module does not read a result path, invoke the production analyzer, render figures,
create a Formal certificate, seal evidence, or decide publication acceptance.

## Related pages

- [Schematics](schematics.md)
- [Numerics](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Parent package](../index.md)
