# `ksdft2effmass.periodic1d.campaign.oracle.finite_rank.encoded_documents`

## Purpose and status

This canonical target module page maps the implemented source module
`ksdft2effmass.periodic1d.campaign.oracle.finite_rank.encoded_documents`.
`FiniteRankOracleEncodedDocuments` owns exact campaign input and retained-result bytes.
It does not own repository location, decoded parent records, finite represented
operators, resolvent roots, eigenspaces, numerical criteria, verification policy,
qualification, or acceptance.

Row 064 moved the complete finite-rank-oracle campaign family to
`periodic1d.campaign.oracle.finite_rank` without an alias or wire change.

## Public contract

The frozen slotted DataObject owns two ordered nonempty exact built-in `bytes` fields:
`input_document` and `retained_result_document`. Wrong representations, including
`bytes` subclasses, raise `TypeError`; empty exact bytes raise `ValueError`.
Construction performs no decoding, normalization, copying, filesystem access, source
authentication, numerical calculation, or scientific interpretation.

The reviewed leaf facade is
`ksdft2effmass.periodic1d.campaign.oracle.finite_rank`. It exports the
defining encoded-document class and `FiniteRankOracleCampaign` only. No retired
`FiniteRankOracleCampaignModel` route or forwarding module is supported.

## Repository-location split

`FiniteRankOracleCampaign.calculate` and `correlate_retained` receive an explicit
`repository_root` operation argument. They require an absolute `Path` before decoding
or source access. This is explicit operation-owned location, not an encoded field or an
inferred provenance claim.

`FiniteRankOracleVerificationRequest` separately owns exact documents and an absolute
root. Its construction checks type and lexical absoluteness without resolving paths or
accessing files. The verifier later binds both encapsulated input bytes and the repository input file
to the retained input identity, accepts only the frozen historical runner digest for the retained legacy result or verifies
explicit script and implementation identities for newer results, and authenticates the
source-result identities declared by the input. It does not recursively authenticate
those source results' provenance graphs.

## Class navigation

| Crosswalk row | Canonical class page |
|---|---|
| `PERIODIC-XWALK-043` | [`FiniteRankOracleEncodedDocuments`](FiniteRankOracleEncodedDocuments/index.md) |

## Code mapping

| Code path | Symbol kind | Qualified name | Architecture responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/periodic1d/campaign/oracle/finite_rank/encoded_documents.py` | Class | `ksdft2effmass.periodic1d.campaign.oracle.finite_rank.encoded_documents.FiniteRankOracleEncodedDocuments` | Owns exact input and retained-result bytes only |
| `python/src/ksdft2effmass/periodic1d/campaign/oracle/finite_rank/campaign.py` | Methods | `FiniteRankOracleCampaign.calculate` and `FiniteRankOracleCampaign.correlate_retained` | Receive explicit absolute roots for executing operations |
| `python/src/ksdft2effmass/periodic1d/campaign/oracle/finite_rank/verification.py` | Class | `FiniteRankOracleVerificationRequest` | Owns verification documents and explicit absolute root |
| `python/src/ksdft2effmass/periodic1d/campaign/oracle/finite_rank/__init__.py` | Package | `ksdft2effmass.periodic1d.campaign.oracle.finite_rank` | Curated supported current facade |

## Test mapping

| Test path | Pytest node | Evidence class | Established behavior |
|---|---|---|---|
| `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/oracle/finite_rank/test__FiniteRankOracleEncodedDocuments.py` | `TestFiniteRankOracleEncodedDocuments::test_contract__owns_exact_fields_without_repository_location` | Software verification, class-owned | Exact fields, defining module, no-copy synthetic bytes, and absence of repository state |
| `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/oracle/finite_rank/test__FiniteRankOracleEncodedDocuments.py` | `TestFiniteRankOracleEncodedDocuments::test_construction__rejects_wrong_and_empty_payload_representations` | Software verification, class-owned | Fail-closed exact-byte and nonempty contracts |
| `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/oracle/finite_rank/test__FiniteRankOracleEncodedDocuments.py` | `TestFiniteRankOracleEncodedDocuments::test_construction__is_frozen_and_slotted` | Software verification, class-owned | Operational immutability and no undeclared repository location |
| `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/oracle/finite_rank/test__integration__finite_rank_oracle_encoded_document_artifacts.py` | `TestFiniteRankOracleEncodedDocumentArtifacts::test_retained_artifacts__preserve_exact_bytes_and_catalog_identities` | Software verification, artifact-owned integration | Exact retained bytes and checksum-catalog identities |
| `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/oracle/finite_rank/test__integration__finite_rank_oracle_encoded_document_artifacts.py` | `TestFiniteRankOracleEncodedDocumentArtifacts::test_operations__reject_input_bytes_outside_declared_provenance` | Software verification, artifact-owned integration | Calculation and verification bind encapsulated input bytes before scientific adaptation or reconstruction |
| `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/oracle/finite_rank/test__integration__finite_rank_oracle_encoded_document_artifacts.py` | `TestFiniteRankOracleEncodedDocumentArtifacts::test_routes_and_operation_roots__preserve_repository_location_split` | Software verification, artifact-owned integration | Curated facade, instance-owned campaign/Workflow/verifier behavior, operation-root boundaries, fail-closed roots, and retired aggregate-route removal |

The ownership manifest is
`python/tests/software_verification/ksdft2effmass/periodic1d/campaign/oracle/finite_rank/resources/implementation-verification-ownership.json`.

## Sphinx mapping

| Sphinx path | Documented route | Role |
|---|---|---|
| `doc/sphinx/api/research-monograph-campaigns.rst` | `ksdft2effmass.periodic1d.campaign.oracle.finite_rank` | Public split narrative and autodoc |
| `doc/sphinx/concepts/periodic-1d-defect-extraction.rst` | Finite-rank-oracle campaign | Scientific and evidence context within the defect chain |

## Provenance, evidence, and limitations

Routine class-owned evidence covers intrinsic representation. Claim-bearing
artifact-owned integration evidence covers maintained bytes, checksum-catalog content
identities, facade behavior, retired routes, and structural location ownership.
Passing these checks does not establish decoded correctness, execution provenance,
numerical reconstruction, infinite-volume or continuum convergence, oracle
qualification for another evidence class, material validation, transferability,
uncertainty quantification, or acceptance.

Original local work under the repository license. No calculator execution is required
or authorized by this dossier.
