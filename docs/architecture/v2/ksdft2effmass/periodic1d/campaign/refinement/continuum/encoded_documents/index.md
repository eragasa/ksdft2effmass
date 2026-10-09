# `ksdft2effmass.periodic1d.campaign.refinement.continuum.encoded_documents`

## Purpose and status

This canonical target module page maps the implemented source module
`ksdft2effmass.periodic1d.campaign.refinement.continuum.encoded_documents`.
`ContinuumRefinementEncodedDocuments` owns exact campaign input and retained-result
bytes. It does not own repository location, decoded axis definitions, parent lattice
records, continuum or lattice represented operators, numerical criteria, verification
policy, or acceptance.

Row 063 moved the complete continuum-refinement campaign family to
`periodic1d.campaign.refinement.continuum` without an alias or wire change. The parent
campaign's operators, scaling construction, numerical diagnostics, frozen
criteria, and scientific reasoning are documented separately in the
[continuum-refinement methods narrative](../numerical-techniques-and-scientific-reasoning.md)
so those meanings are not assigned to this byte owner.

## Public contract

The frozen slotted DataObject owns two ordered nonempty exact built-in `bytes` fields:
`input_document` and `retained_result_document`. Wrong representations, including
`bytes` subclasses, raise `TypeError`; empty exact bytes raise `ValueError`. Construction
performs no decoding, normalization, copying, filesystem access, or scientific
interpretation.

The reviewed leaf facade is
`ksdft2effmass.periodic1d.campaign.refinement.continuum`. It exports the
defining encoded-document class and `ContinuumRefinementCampaign` only. No retired
`ContinuumRefinementCampaignModel` route or forwarding module is supported.

## Repository-location split

`ContinuumRefinementCampaign.correlate_retained` receives an explicit
`repository_root` operation argument, validates that it is an absolute `Path`, and then
uses it for authenticated source access and recalculation. Because this is an executing
facade method rather than a passive request constructor, source existence and identity
are checked during the operation.

`ContinuumRefinementVerificationRequest` separately owns exact documents and an
absolute `repository_root`. Its construction checks type and lexical absoluteness
without resolving paths or accessing files. The verifier later authenticates sources
and reconstructs retained channels. Neither path boundary establishes provenance or
scientific validity by itself.

## Class navigation

| Crosswalk row | Canonical class page |
|---|---|
| `PERIODIC-XWALK-042` | [`ContinuumRefinementEncodedDocuments`](ContinuumRefinementEncodedDocuments/index.md) |

## Code mapping

| Code path | Symbol kind | Qualified name | Architecture responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/periodic1d/campaign/refinement/continuum/encoded_documents.py` | Class | `ksdft2effmass.periodic1d.campaign.refinement.continuum.encoded_documents.ContinuumRefinementEncodedDocuments` | Owns exact input and retained-result bytes only |
| `python/src/ksdft2effmass/periodic1d/campaign/refinement/continuum/campaign.py` | Method | `ksdft2effmass.periodic1d.campaign.refinement.continuum.campaign.ContinuumRefinementCampaign.correlate_retained` | Receives an explicit absolute root and performs retained correlation |
| `python/src/ksdft2effmass/periodic1d/campaign/refinement/continuum/verification.py` | Class | `ksdft2effmass.periodic1d.campaign.refinement.continuum.verification.ContinuumRefinementVerificationRequest` | Owns verification documents and explicit absolute root |
| `python/src/ksdft2effmass/periodic1d/campaign/refinement/continuum/__init__.py` | Package | `ksdft2effmass.periodic1d.campaign.refinement.continuum` | Curated supported current facade |

## Test mapping

| Test path | Pytest node | Evidence class | Established behavior |
|---|---|---|---|
| `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/refinement/continuum/test__ContinuumRefinementEncodedDocuments.py` | `TestContinuumRefinementEncodedDocuments::test_contract__owns_exact_fields_without_repository_location` | Software verification, class-owned | Exact fields, defining module, no-copy synthetic bytes, and absence of repository state |
| `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/refinement/continuum/test__ContinuumRefinementEncodedDocuments.py` | `TestContinuumRefinementEncodedDocuments::test_construction__rejects_wrong_and_empty_payload_representations` | Software verification, class-owned | Fail-closed exact-byte and nonempty contracts |
| `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/refinement/continuum/test__ContinuumRefinementEncodedDocuments.py` | `TestContinuumRefinementEncodedDocuments::test_construction__is_frozen_and_slotted` | Software verification, class-owned | Operational immutability and no undeclared repository location |
| `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/refinement/continuum/test__integration__continuum_refinement_encoded_document_artifacts.py` | `TestContinuumRefinementEncodedDocumentArtifacts::test_retained_artifacts__preserve_exact_bytes_and_catalog_identities` | Software verification, artifact-owned integration | Exact retained bytes and checksum-catalog identities |
| `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/refinement/continuum/test__integration__continuum_refinement_encoded_document_artifacts.py` | `TestContinuumRefinementEncodedDocumentArtifacts::test_routes_and_operation_roots__preserve_repository_location_split` | Software verification, artifact-owned integration | Curated facade, operation-root boundaries, fail-closed roots, and retired aggregate-route removal |

The ownership manifest is
`python/tests/software_verification/ksdft2effmass/periodic1d/campaign/refinement/continuum/resources/implementation-verification-ownership.json`.

## Sphinx mapping

| Sphinx path | Documented route | Role |
|---|---|---|
| `doc/sphinx/api/research-monograph-campaigns.rst` | `ksdft2effmass.periodic1d.campaign.refinement.continuum` | Canonical user-facing split narrative and autodoc |
| `doc/sphinx/concepts/periodic1d-continuum-refinement.rst` | Concept documentation | Numerical methods, scientific reasoning, error accounting, and claim boundaries |

## Provenance, evidence, and limitations

Routine class-owned evidence covers intrinsic representation. Claim-bearing
artifact-owned integration evidence covers maintained bytes, checksum-catalog content
identities, facade behavior, retired routes, and structural location ownership. Passing
these checks does not establish decoded correctness, source or execution provenance,
independent numerical reconstruction, asymptotic convergence, continuum-limit validity,
material validation, transferability, uncertainty quantification, or acceptance.

Original local work under the repository license. No calculator execution is required
or authorized by this dossier.
