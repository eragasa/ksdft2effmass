# `Periodic1DIsolatedBandCampaignDefinition`

## Responsibility

This frozen, slotted DataObject retains the complete version-one isolated-band study
controls: experiment identity, explicit unitless lattice/reciprocal/energy convention,
potential strength, parent-discretization inventories, reciprocal and withheld meshes,
hopping ranges, and weak-potential controls. Its short `__post_init__` delegates
identity, quantity, vector, inventory, positive-integer, and cross-field checks.

The definition is not a physical Hamiltonian, finite matrix representation, selected
or retained state space, gauge frame, represented operator, hopping representation,
effective model, execution record, provenance record, or acceptance result.

## Invariants

- scalar and vector quantities use their exact public quantity types and `Unitless`;
- integer inventories are exact nonempty tuples of exact built-in integers, unique and
  increasing;
- sweep cutoffs are positive, every finite-difference grid has at least three points,
  and hopping ranges are nonnegative;
- the reference cutoff exceeds every sweep cutoff;
- the common low-mode dimension and compared-band count fit every declared finite
  parent representation;
- every weak-potential strength is positive; and
- lattice period and reciprocal vector satisfy the declared `2 pi` duality tolerance.

## Code and public route

| Surface | Mapping |
|---|---|
| Definition | `python/src/ksdft2effmass/periodic1d/campaign/isolated/definition.py` |
| Qualified class | `ksdft2effmass.periodic1d.campaign.isolated.definition.Periodic1DIsolatedBandCampaignDefinition` |
| Public facade | `ksdft2effmass.periodic1d.campaign.Periodic1DIsolatedBandCampaignDefinition` |
| Transitional aliases | None |

## Evidence and provenance

`TestPeriodic1DIsolatedBandCampaignJsonSerializer::test_method__deserialize_serialize__preserves_retained_definition`
in
`python/tests/software_verification/ksdft2effmass/periodic1d/campaign/isolated/test__Periodic1DIsolatedBandCampaignJsonSerializer.py`
binds the defining module and retained controls. Exact intrinsic validation nodes in
`test__Periodic1DIsolatedBandCampaignDefinition.py` are:

- `TestPeriodic1DIsolatedBandCampaignDefinition::test_construction__distinguishes_identity_type_and_value_errors`;
- `TestPeriodic1DIsolatedBandCampaignDefinition::test_construction__rejects_unusable_parent_dimensions`; and
- `TestPeriodic1DIsolatedBandCampaignDefinition::test_construction__rejects_nonpositive_weak_strengths`.

The source input is maintained as
`calculations/research-monograph/periodic-1d/input.json` with SHA-256
`ae17de790380dee76693e984b96fbb22773a40440e267d3e77b4543cafaad6fb`.

This evidence establishes bounded decoding, structure, and identity only. It does not
establish calculation provenance, parent convergence, physical adequacy, scientific
validation, uncertainty quantification, or acceptance. Original local work under the
repository license.
