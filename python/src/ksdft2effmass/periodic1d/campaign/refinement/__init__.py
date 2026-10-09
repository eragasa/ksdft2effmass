"""Reviewed facades for periodic-1D refinement campaign families.

Refinement campaigns keep independently varied numerical axes explicit and do not turn
finite-sequence behavior into an asymptotic-convergence or acceptance claim.
"""

from .continuum import ContinuumRefinementCampaign, ContinuumRefinementEncodedDocuments

__all__ = [
    "ContinuumRefinementCampaign",
    "ContinuumRefinementEncodedDocuments",
]
