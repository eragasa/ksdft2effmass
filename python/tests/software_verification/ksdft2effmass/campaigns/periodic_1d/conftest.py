"""Pytest-owned classification for retained periodic-1D campaigns."""

from pathlib import Path

import pytest

CAMPAIGN_ROOT = Path(__file__).resolve().parent
NON_RECONSTRUCTION_TESTS = frozenset(
    {
        "test__periodic_1d_legacy_import.py",
        "test__BlindAlignmentEncodedDocuments.py",
        "test__ContinuumRefinementEncodedDocuments.py",
        "test__FiniteRankOracleEncodedDocuments.py",
        "test__RouteReconciliationEncodedDocuments.py",
        "test__integration__blind_alignment_encoded_document_artifacts.py",
        "test__integration__continuum_refinement_encoded_document_artifacts.py",
        "test__integration__finite_rank_oracle_encoded_document_artifacts.py",
        "test__integration__route_reconciliation_encoded_document_artifacts.py",
    }
)


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Mark retained reconstruction tests, but not structural contracts, expensive."""
    for item in items:
        if not item.path.is_relative_to(CAMPAIGN_ROOT):
            continue
        if item.path.name not in NON_RECONSTRUCTION_TESTS:
            item.add_marker(pytest.mark.expensive)
