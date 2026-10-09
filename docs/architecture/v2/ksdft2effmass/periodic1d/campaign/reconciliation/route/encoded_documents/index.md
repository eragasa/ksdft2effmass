# `ksdft2effmass.periodic1d.campaign.reconciliation.route.encoded_documents`

## Purpose and status

This canonical module maps the implemented source
`ksdft2effmass.periodic1d.campaign.reconciliation.route.encoded_documents`.
`RouteReconciliationEncodedDocuments` owns exact input and retained-result bytes only.
It owns no repository path, decoded parent, represented operator, route map,
reconciliation, provenance claim, numerical result, or acceptance decision.

Row 066 moved the complete route-reconciliation family here without a compatibility
alias or wire change.

## Contract and routes

The frozen slotted DataObject owns two ordered nonempty exact built-in `bytes` fields:
`input_document` and `retained_result_document`. It preserves the supplied immutable
objects without copying or decoding. Wrong representations, including `bytes`
subclasses, raise `TypeError`; empty exact bytes raise `ValueError`.

The reviewed facade is
`ksdft2effmass.periodic1d.campaign.reconciliation.route`. It exports the
campaign facade and defining encoded-document class only. The former aggregate
`RouteReconciliationCampaignModel` and `model.py` route are retired without aliases.
Calculation, retained correlation, and verification own location in their distinct typed
request records.

## Mapping

| Crosswalk row | Canonical class page |
|---|---|
| `PERIODIC-XWALK-044` | [`RouteReconciliationEncodedDocuments`](RouteReconciliationEncodedDocuments/index.md) |

| Code path | Responsibility |
|---|---|
| `python/src/ksdft2effmass/periodic1d/campaign/reconciliation/route/encoded_documents.py` | Exact encoded bytes only |
| `python/src/ksdft2effmass/periodic1d/campaign/reconciliation/route/campaign.py` | Calculation/correlation request-owned location and campaign facade |
| `python/src/ksdft2effmass/periodic1d/campaign/reconciliation/route/verification.py` | Verification request-owned location and independent checking |

Exact tests, evidence identities, documentation routes, and limitations are enumerated
on the [class dossier](RouteReconciliationEncodedDocuments/index.md).

Original local work under the repository license.
