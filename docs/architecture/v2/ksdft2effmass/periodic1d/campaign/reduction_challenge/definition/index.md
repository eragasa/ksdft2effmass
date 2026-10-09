# `periodic1d.campaign.reduction_challenge.definition`

## Responsibility

This module owns the immutable version-one challenge controls and their strict JSON
adapter. `Periodic1DReductionChallengeCampaignDefinition` retains the explicit
experiment identity, unitless potential-strength axis, plane-wave cutoffs,
finite-difference grid sizes, compared and challenged bands, reciprocal-mesh sizes,
hopping ranges, isolation threshold, named finite-Fourier potential shapes, withheld
mesh, and route-challenge controls.

`Periodic1DReductionChallengePotentialShape` retains one named real finite-Fourier
potential. The potential owns a unitless period, constant coefficient, and paired
cosine/sine coefficient vectors whose positions identify positive integer harmonics;
no potential symmetry, physical identity, or adequacy is inferred from the name.

`Periodic1DReductionChallengeCampaignJsonSerializer` inherits the canonical strict
periodic-1D decoder. `deserialize(payload)` rejects invalid UTF-8, duplicate keys,
nonfinite JSON numbers, wrong schema/version/key sets, booleans in numeric fields,
nonintegral integer fields, nonfinite or binary64-unrepresentable values, and invalid
closed control inventories. `serialize(definition)` emits canonical JSON while
preserving historical version-one keys such as `stress_band_indices` and
`route_stress_mesh_size`. Deprecated `encode()` and `decode()` forwarding methods are
absent.

## Boundaries

The definition owns campaign controls only. It does not prove that a calculation ran,
define a retained subspace/operator, or turn the historical wire's informational
expectations into verification criteria. Dense allocation and numerical reconstruction
belong to the verifier.

## Key class

- [Periodic1DReductionChallengeCampaignDefinition](Periodic1DReductionChallengeCampaignDefinition/index.md)
