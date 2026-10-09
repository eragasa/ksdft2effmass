# `RouteReconciliationEncodedDocuments`

## Canonical identity and responsibility

`RouteReconciliationEncodedDocuments` is the row-044 byte owner. Its current defining
name is
`ksdft2effmass.periodic1d.campaign.reconciliation.route.encoded_documents.RouteReconciliationEncodedDocuments`.
The future canonical package is `periodic1d.campaign.reconciliation.route`; row 066 owns
that later family move.

The frozen slotted DataObject stores, in order, exact nonempty version-one input bytes
and exact nonempty retained-result bytes. It performs no copying, decoding,
normalization, authentication, filesystem access, route calculation, or scientific
interpretation.

## Non-responsibilities and location boundary

This class is not a parent model, finite representation, represented pristine or defect
operator, alignment map, folding map, reconciliation result, provenance record,
verification result, UQ statement, or acceptance decision. It does not own or infer a
repository root. Calculation, retained correlation, and verification each own their
explicit absolute root in a distinct typed request. Request construction checks lexical
absoluteness only; later operation owners access and authenticate sources.

No model identity, state space, basis, ordering, energy reference, route compatibility,
provenance, or scientific meaning is inferred from names, paths, payload appearance,
dimensions, spectra, or hashes.

## Retained artifact identities

| Artifact | SHA-256 content identity |
|---|---|
| `calculations/research-monograph/impurity-defect-1d-independent-route/input.json` | `aa7bd0750556bca3199678877f9ca2cd340f6c6b02885d6019c56173e912953f` |
| `calculations/research-monograph/impurity-defect-1d-independent-route/result.json` | `861097a6156999b615edd27cf68dcf36fd110248b9d24dc1b862eff5eeec3bdc` |

The maintained `SHA256SUMS` catalog repeats these identities. SHA-256 establishes
content identity only, not authorship, execution provenance, decoded correctness,
numerical validity, route compatibility, scientific validation, UQ, or acceptance.

## Historical-runner boundary

The retained legacy result records historical runner digest
`9ec2c391e4b49d859abef52249d17699173b6e7844387b3eda47e016d487839c`.
The verifier recognizes that exact frozen identity only for the legacy wire lacking
explicit implementation fields; it does not claim that the current adapter still has
those bytes. Newly encoded results bind and authenticate both current adapter and
implementation identities. This is bounded provenance compatibility, not proof of who
executed the historical calculation.

## Supported and retired routes

The supported current facade is
`ksdft2effmass.periodic1d.campaign.reconciliation.route`; its exported encoded
class is the defining class object. The former aggregate
`RouteReconciliationCampaignModel`, its `repository_root` field, and
`defects/route_reconciliation/model.py` are retired without a compatibility alias.

## Row-044 completion dossier

| Field | Reconciled content |
|---|---|
| Crosswalk identity | `PERIODIC-XWALK-044`; former owner `RouteReconciliationCampaignModel` |
| Scientific category | Supporting encoded campaign document; not a model, represented operator, route result, or acceptance record |
| Target ownership | Canonical defining module and reviewed leaf facade under `periodic1d.campaign.reconciliation.route` |
| Preserved meaning | Input bytes precede retained-result bytes; retained payloads, paths inside the wire, and digests remain unchanged |
| Changed meaning | Aggregate model/module removed; each operation owns repository location in an explicit typed request |
| Representation contract | Two ordered nonempty exact built-in `bytes`; basis, gauge, state space, units, geometry, dtype, and matrix ordering are not applicable at this boundary |
| Construction route | Frozen slotted assignment preserves supplied byte objects; no selection, projection, transformation, parsing, or source access occurs |
| Error boundaries | Wrong representations, including `bytes` subclasses, raise `TypeError`; empty exact bytes raise `ValueError`; request boundaries reject unsupported or relative roots before payload decoding; calculation and verification reject encapsulated or repository input bytes that disagree with provenance |
| Shared parser boundary | `serialization.json.StrictJsonDecoder`, through the campaign specialization, supplies strict JSON mechanics downstream; it assigns no scientific metadata or route meaning |
| Public documentation | This dossier, its [module page](../index.md), the [campaign dossier](../../index.md), `doc/sphinx/concepts/periodic-1d-defect-extraction.rst`, and `doc/sphinx/api/research-monograph-campaigns.rst` |
| Retained evidence | The two files and reviewed `SHA256SUMS` entries listed above |
| Unavailable/inapplicable | Byte storage does not supply authenticated provenance, decoded scientific identity, route reconstruction, convergence, material validation, UQ, or acceptance; none is inferred |
| Claim boundary | Software ownership and retained content identity only |

## Exact test mapping

| Test path | Exact pytest node | Evidence ownership | Established behavior |
|---|---|---|---|
| `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/reconciliation/route/test__RouteReconciliationEncodedDocuments.py` | `TestRouteReconciliationEncodedDocuments::test_contract__owns_exact_fields_without_repository_location` | Routine class-owned software verification | Exact ordered fields, defining owner, no-copy synthetic bytes, and absent repository state |
| same | `TestRouteReconciliationEncodedDocuments::test_construction__rejects_wrong_and_empty_payload_representations` | Routine class-owned software verification | Fail-closed exact-byte and nonempty contracts |
| same | `TestRouteReconciliationEncodedDocuments::test_construction__is_frozen_and_slotted` | Routine class-owned software verification | Operational immutability and no undeclared location |
| `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/reconciliation/route/test__integration__route_reconciliation_encoded_document_artifacts.py` | `TestRouteReconciliationEncodedDocumentArtifacts::test_retained_artifacts__preserve_exact_bytes_and_catalog_identities` | Artifact-owned integration software verification | Exact retained bytes and checksum-catalog identities |
| same | `TestRouteReconciliationEncodedDocumentArtifacts::test_operations__reject_input_bytes_outside_declared_provenance` | Artifact-owned integration software verification | Calculation and verification bind encapsulated input bytes before route-contract decoding or reconstruction |
| same | `TestRouteReconciliationEncodedDocumentArtifacts::test_routes_and_operation_requests__preserve_location_split` | Artifact-owned integration software verification | Facade identity, request-owned roots, fail-closed root validation, and retired-route removal |

The test ownership manifest is
`python/tests/software_verification/ksdft2effmass/periodic1d/campaign/reconciliation/route/resources/implementation-verification-ownership.json`.

## Sphinx and provenance mapping

| Sphinx path | Role |
|---|---|
| `doc/sphinx/api/research-monograph-campaigns.rst` | Public facade narrative and autodoc |
| `doc/sphinx/concepts/periodic-1d-defect-extraction.rst` | Scientific route-reconciliation context and claim boundary |

The artifact package's `README.md`, `protocol.md`, and `report.md` preserve the original
methods, retained observations, and limitations. This dossier neither reruns nor
reinterprets them.

## Limitations

Passing row-044 tests does not authenticate the whole transitive provenance graph,
reconstruct route numerics, prove a commutative diagram generally, establish continuum
or infinite-volume convergence, validate a material, establish transferability, quantify
uncertainty, or record acceptance. No calculator is invoked.

Original local work under the repository license.
