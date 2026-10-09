# `periodic1d.campaign.reduction_challenge.verification`

## Responsibility

`Periodic1DReductionChallengeCampaignVerifier` accepts exact encoded documents and one
nonnegative finite unitless tolerance. It constructs a fresh correlation Action first,
then a fresh independent numerical verifier, and returns both outcomes without
conflating them.

Correlation failure prevents numerical use of unauthenticated input-owned controls.
The verification Result intrinsically validates exact child types only; it does not
prove Action execution. `passes` delegates only to the bounded numerical result.

The operation may propagate strict decoding/type/value failures, `MemoryError`,
`OverflowError`, and `numpy.linalg.LinAlgError`. It performs no file discovery,
calculator execution, material validation, UQ, or acceptance.
