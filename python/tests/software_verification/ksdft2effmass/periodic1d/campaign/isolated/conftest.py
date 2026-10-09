"""Pytest-owned classification for the canonical isolated-band campaign."""

from pathlib import Path

import pytest

CAMPAIGN_ROOT = Path(__file__).resolve().parent
ROUTINE_MODULES = frozenset(
    {
        "test__Periodic1DIsolatedBandEncodedDocuments.py",
        "test__integration__isolated_band_encoded_document_artifacts.py",
    }
)


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Mark numerical reconstruction tests, but not structural evidence, expensive."""
    for item in items:
        if item.path.is_relative_to(CAMPAIGN_ROOT):
            if item.path.name not in ROUTINE_MODULES:
                item.add_marker(pytest.mark.expensive)
