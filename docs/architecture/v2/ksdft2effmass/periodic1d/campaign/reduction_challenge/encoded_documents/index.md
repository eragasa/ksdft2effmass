# `periodic1d.campaign.reduction_challenge.encoded_documents`

## Responsibility

`Periodic1DReductionChallengeEncodedDocuments` owns exactly two nonempty built-in
`bytes` objects: the historical input wire and result wire. It does not decode,
normalize, copy, correlate, authenticate, or interpret either payload.

## Wire compatibility

The canonical move deliberately preserves:

- `stress-input.json` and `stress-result.json` filenames;
- exact bytes and SHA-256 identities;
- the version-one experiment and schema identities;
- historical JSON key spellings;
- historical evidence-status text; and
- the `Periodic1DEncodedResultKind.STRESS` wire discriminator.

These historical tokens do not reintroduce `Periodic1DStress*` software aliases and do
not imply mechanical-stress semantics.

## Key class

- [Periodic1DReductionChallengeEncodedDocuments](Periodic1DReductionChallengeEncodedDocuments/index.md)
