# `RouteReconciliationCampaignResultDocument`

## Purpose and row-057 disposition

This frozen, slotted DataObject remains the named encoded result-document owner for the
route-reconciliation campaign. Row 057 keeps it in the campaign's existing
`result_documents.py` module, adds the deliberate leaf-package facade, and audits its
intrinsic, artifact, Sphinx, and architecture contracts. Row 066 retains ownership of
the later canonical package move.

## Public contract

```python
RouteReconciliationCampaignResultDocument(payload: bytes)
```

| Field or property | Representation | Contract |
|---|---|---|
| `payload` | Exact nonempty built-in `bytes` | Encoded result wire retained without decoding or copying |
| `sha256` | 64-character lowercase hexadecimal `str` | SHA-256 derived directly from `payload` |

Strings, mutable byte arrays, byte subclasses, and empty bytes fail closed. The object
is frozen and slotted. `__post_init__` delegates exact-byte validation to the cohesive
`_check_args_payload` method. Digest derivation never parses or canonically re-encodes
the wire.

## Retained content identity

| Artifact | SHA-256 |
|---|---|
| `calculations/research-monograph/impurity-defect-1d-independent-route/result.json` | `861097a6156999b615edd27cf68dcf36fd110248b9d24dc1b862eff5eeec3bdc` |

Artifact-owned evidence requires the same identity in the maintained `SHA256SUMS`
catalog and confirms that
`RouteReconciliationEncodedDocuments.retained_result_document` can be passed without
copying. Content identity does not establish either route identity, state-space
alignment, basis/gauge compatibility, authorship, execution provenance, schema
correctness, scientific validation, uncertainty quantification, or acceptance.

## Supported imports

- defining route:
  `ksdft2effmass.periodic1d.campaign.reconciliation.route.result_documents.RouteReconciliationCampaignResultDocument`;
- reviewed leaf facade:
  `ksdft2effmass.periodic1d.campaign.reconciliation.route.RouteReconciliationCampaignResultDocument`.

No generic reconciliation facade, structural fallback, or broader periodic-1D export is
introduced before row 066.

## Code and evidence mapping

| Surface | Path or node | Responsibility |
|---|---|---|
| Definition | `python/src/ksdft2effmass/periodic1d/campaign/reconciliation/route/result_documents.py` | Exact bytes and digest |
| Facade | `python/src/ksdft2effmass/periodic1d/campaign/reconciliation/route/__init__.py` | Deliberate leaf import |
| Routine evidence | `test__RouteReconciliationCampaignResultDocument.py::TestRouteReconciliationCampaignResultDocument` | Fields, module, fixed synthetic digest, failures, immutability |
| Artifact evidence | `test__integration__route_reconciliation_result_document_artifact.py::TestRouteReconciliationResultDocumentArtifact::test_retained_result__preserves_bytes_catalog_identity_and_route` | Retained bytes, catalog identity, paired owner, facade |
| Sphinx | `doc/sphinx/api/research-monograph-campaigns.rst` | User-facing campaign API and limitations |

The test paths are rooted at
`python/tests/software_verification/ksdft2effmass/periodic1d/campaign/reconciliation/route/`
and are registered in the periodic-1D implementation-verification ownership metadata.

## Scientific boundary

This DataObject does not identify either physical parent, finite representation, common
state space, alignment map, energy reference, basis, gauge, represented operator,
comparison, compatibility relation, or scientific conclusion. Passing its tests
establishes bounded software behavior and content identity only. No calculator is
invoked and no retained artifact is modified.
