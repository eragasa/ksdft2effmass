# `periodic1d.campaign.alignment.blind.encoded_documents`

## Purpose and status

This implemented canonical module owns
`ksdft2effmass.periodic1d.campaign.alignment.blind.encoded_documents`.
`BlindAlignmentEncodedDocuments` stores exact campaign input and retained-result bytes.
It does not own repository location, decoded scientific records, inference-visible
observations, hidden truth, verification policy, or acceptance. Row 062 moved the
complete family without an alias or wire-identity change.

## Public contract

The frozen slotted DataObject owns two ordered nonempty exact built-in `bytes` fields:
`input_document` and `retained_result_document`. Wrong representations, including
`bytes` subclasses, raise `TypeError`; empty exact bytes raise `ValueError`. Construction
performs no decoding, normalization, copying, filesystem access, or scientific
interpretation.

The reviewed leaf facade is
`ksdft2effmass.periodic1d.campaign.alignment.blind`. It exports the defining
encoded-document class and `BlindAlignmentCampaign` only. No retired
`BlindAlignmentCampaignModel` route or forwarding module is supported.

## Repository-location split

The following defining request types own explicit absolute `repository_root` fields:

- `BlindAlignmentCampaignCalculationRequest`;
- `BlindAlignmentCampaignRetainedCorrelationRequest`; and
- `BlindAlignmentCampaignVerificationRequest`.

Request construction checks type and absolute-path syntax without resolving paths or
accessing files. Downstream Actions own source authentication. A repository root does
not establish historical execution provenance merely because retained payloads contain
source identities.

## Class navigation

| Crosswalk row | Canonical class page |
|---|---|
| `PERIODIC-XWALK-041` | [`BlindAlignmentEncodedDocuments`](BlindAlignmentEncodedDocuments/index.md) |

## Code mapping

| Code path | Symbol kind | Qualified name | Architecture responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/periodic1d/campaign/alignment/blind/encoded_documents.py` | Class | `ksdft2effmass.periodic1d.campaign.alignment.blind.encoded_documents.BlindAlignmentEncodedDocuments` | Owns exact input and retained-result bytes only |
| `python/src/ksdft2effmass/periodic1d/campaign/alignment/blind/campaign.py` | Class | `ksdft2effmass.periodic1d.campaign.alignment.blind.campaign.BlindAlignmentCampaignCalculationRequest` | Owns calculation documents, explicit repository root, and caller execution provenance |
| `python/src/ksdft2effmass/periodic1d/campaign/alignment/blind/campaign.py` | Class | `ksdft2effmass.periodic1d.campaign.alignment.blind.campaign.BlindAlignmentCampaignRetainedCorrelationRequest` | Owns correlation documents and explicit repository root |
| `python/src/ksdft2effmass/periodic1d/campaign/alignment/blind/verification.py` | Class | `ksdft2effmass.periodic1d.campaign.alignment.blind.verification.BlindAlignmentCampaignVerificationRequest` | Owns verification documents and explicit repository root |
| `python/src/ksdft2effmass/periodic1d/campaign/alignment/blind/__init__.py` | Package | `ksdft2effmass.periodic1d.campaign.alignment.blind` | Curated supported current facade |

## Test mapping

| Test path | Pytest node | Evidence class | Established behavior |
|---|---|---|---|
| `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/alignment/blind/test__BlindAlignmentEncodedDocuments.py` | `TestBlindAlignmentEncodedDocuments::test_contract__owns_exact_fields_without_repository_location` | Software verification, class-owned | Exact fields, defining module, no-copy synthetic bytes, and absence of repository state |
| `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/alignment/blind/test__BlindAlignmentEncodedDocuments.py` | `TestBlindAlignmentEncodedDocuments::test_construction__rejects_wrong_and_empty_payload_representations` | Software verification, class-owned | Fail-closed exact-byte and nonempty contracts |
| `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/alignment/blind/test__BlindAlignmentEncodedDocuments.py` | `TestBlindAlignmentEncodedDocuments::test_construction__is_frozen_and_slotted` | Software verification, class-owned | Operational immutability and no undeclared repository location |
| `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/alignment/blind/test__integration__blind_alignment_encoded_document_artifacts.py` | `TestBlindAlignmentEncodedDocumentArtifacts::test_retained_artifacts__preserve_exact_bytes_and_catalog_identities` | Software verification, artifact-owned integration | Exact retained bytes and checksum-catalog identities |
| `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/alignment/blind/test__integration__blind_alignment_encoded_document_artifacts.py` | `TestBlindAlignmentEncodedDocumentArtifacts::test_routes_and_request_fields__preserve_repository_location_split` | Software verification, artifact-owned integration | Curated facade, request-owned roots, and retired aggregate-route removal |

The ownership manifest is
`python/tests/software_verification/ksdft2effmass/periodic1d/campaign/alignment/blind/resources/implementation-verification-ownership.json`.

## Sphinx mapping

| Sphinx path | Documented route | Role |
|---|---|---|
| `doc/sphinx/api/ksdft2effmass/periodic1d/campaign/alignment-blind.rst` | `ksdft2effmass.periodic1d.campaign.alignment.blind` | Complete defining-module API and scientific boundaries |
| `doc/sphinx/api/research-monograph-campaigns.rst` | `ksdft2effmass.periodic1d.campaign.alignment.blind` | Campaign-family narrative and reviewed facade |

## Provenance, evidence, and limitations

Routine class-owned evidence covers intrinsic representation. Claim-bearing
artifact-owned integration evidence covers maintained bytes, checksum-catalog content
identities, facade behavior, retired routes, and structural location ownership. Passing
these checks does not establish decoded correctness, hidden-truth separation, source or
execution provenance, numerical reconstruction, scientific validation, uncertainty
quantification, transferability, or acceptance.

Original local work under the repository license. No calculator execution is required
or authorized by this dossier.
