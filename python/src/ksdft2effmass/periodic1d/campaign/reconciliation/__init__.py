"""Reviewed facades for periodic-1D route-reconciliation campaigns.

Reconciliation requires explicit common-parent, common-space, and route identities
before numerical comparison; route agreement is not scientific validation.
"""

from .route import RouteReconciliationCampaign, RouteReconciliationEncodedDocuments

__all__ = [
    "RouteReconciliationCampaign",
    "RouteReconciliationEncodedDocuments",
]
