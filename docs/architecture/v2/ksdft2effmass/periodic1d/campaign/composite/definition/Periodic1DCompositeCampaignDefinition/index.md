# `Periodic1DCompositeCampaignDefinition`

## Purpose

This frozen, slotted DataObject owns the complete version-one composite campaign
controls. `retained_band_groups` contains explicit
`Periodic1DRetainedBandGroupDefinition` records whose selected-band retention objects
identify the declared untruncated parent model, reciprocal domain, operator, state
space, construction, assumptions, and provenance. Scientific adoption constructs a
separate retention record qualified to the finite plane-wave representation; it does
not reinterpret the input record as finite-parent-qualified.

## Invariants

Construction fails closed unless identities are nonempty exact strings; the physical
period and finite thresholds/amplitudes are representable finite binary64 values in
their documented domains; the reciprocal mesh count is an exact even integer of at
least two; other cutoffs, meshes, and ranges satisfy their exact integer domains;
retained groups and ranges are nonempty and uniquely identified; every retained group
references the declared untruncated parent operator and reciprocal domain; the
direct-fit range is included; and every selected parent-band index fits the finite
plane-wave parent dimension `2 * plane_wave_cutoff + 1`.

## Scientific boundary

The definition controls a finite represented campaign while distinguishing the
untruncated parent identity from its later finite plane-wave representation. It is not
a physical Hamiltonian, projector, retained frame, represented matrix, hopping model,
or evidence of convergence or validation. Group names and indices cannot supply
unavailable frame/projector coordinates.

## Implementation and evidence

- source: `python/src/ksdft2effmass/periodic1d/campaign/composite/definition.py`;
- reviewed routes: `ksdft2effmass.periodic1d.campaign` and
  `ksdft2effmass.periodic1d.campaign.composite`;
- routine evidence:
  `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/composite/test__Periodic1DCompositeCampaignDefinition.py::TestPeriodic1DCompositeCampaignDefinition`;
- serializer evidence:
  `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/composite/test__Periodic1DCompositeCampaignJsonSerializer.py::TestPeriodic1DCompositeCampaignJsonSerializer`.

Passing establishes the stated software invariants only.
