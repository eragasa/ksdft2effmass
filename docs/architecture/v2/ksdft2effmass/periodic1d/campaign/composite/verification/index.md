# `periodic1d.campaign.composite.verification`

`Periodic1DCompositeCampaignVerifier` correlates exact wires and then delegates to the
independent numerical implementation in `numerical_verification`. The result preserves
correlation diagnostics, reconstructable-channel outcomes, explicit unavailable-channel
accounting, and an aggregate pass over available checks only.

Independent verification may reuse strict wire decoding but does not call the campaign
calculation implementation. It reconstructs only channels supported by retained data;
unavailable historical frame/projector arrays cannot contribute positive evidence.
Dense operations scale with retained mesh and matrix sizes and may raise `MemoryError`;
nonrepresentable binary64/complex128 outcomes fail closed with `OverflowError`.

Evidence:
`python/tests/numerical_verification/ksdft2effmass/periodic1d/campaign/composite/test__Periodic1DCompositeResultVerifier.py::TestPeriodic1DCompositeResultVerifier`.
Passing is bounded numerical consistency, not parent convergence, physical adequacy,
scientific validation, UQ, or acceptance.
