"""Reviewed facades for bounded periodic-1D oracle campaign families.

An oracle exposed here is qualified only for its exact synthetic evidence class and
validity domain; this package is not a generic oracle registry or plugin surface.
"""

from .finite_rank import FiniteRankOracleCampaign, FiniteRankOracleEncodedDocuments

__all__ = [
    "FiniteRankOracleCampaign",
    "FiniteRankOracleEncodedDocuments",
]
