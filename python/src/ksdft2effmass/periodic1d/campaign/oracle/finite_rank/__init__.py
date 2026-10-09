"""Encapsulated public route for the finite-rank analytical oracle."""

from .campaign import FiniteRankOracleCampaign
from .encoded_documents import FiniteRankOracleEncodedDocuments
from .result_documents import FiniteRankOracleCampaignResultDocument

__all__ = [
    "FiniteRankOracleCampaign",
    "FiniteRankOracleCampaignResultDocument",
    "FiniteRankOracleEncodedDocuments",
]
