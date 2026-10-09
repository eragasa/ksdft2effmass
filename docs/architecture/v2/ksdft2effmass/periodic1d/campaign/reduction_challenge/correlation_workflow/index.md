# `periodic1d.campaign.reduction_challenge.correlation_workflow`

## Responsibility

`Periodic1DReductionChallengeCampaignWorkflow` is the read-only cross-document
correlation Action. Its request owns exact input/result bytes. Execution:

1. strictly decodes the result and derives its exact source-byte identity;
2. hashes the still-opaque supplied input bytes, validates the result-declared input
   digest, and requires equality before decoding the input;
3. strictly decodes the authenticated definition;
4. verifies experiment identity, potential-strength and discretization inventories,
   shape identities and gap cardinalities, reciprocal meshes, challenged bands, route
   controls, and the complete mesh/band/amplitude Cartesian product; and
5. returns the typed definition, typed result, and exact input/result content
   identities.

Caller order is preserved where the wire owns order. Correlation does not infer missing
identity from filenames, paths, dimensions, spectra, or hashes. It performs no
calculator execution and makes no numerical or scientific claim.
