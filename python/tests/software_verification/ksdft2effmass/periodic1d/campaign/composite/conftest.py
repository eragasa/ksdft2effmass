"""Pytest-owned execution classification for the composite campaign family."""

from pathlib import Path

import pytest

COMPOSITE_TEST_ROOT = Path(__file__).resolve().parent
NON_RECONSTRUCTION_TESTS = frozenset(
    {
        "test__Periodic1DCompositeCampaignDefinition.py",
        "test__Periodic1DCompositeEncodedDocuments.py",
        "test__integration__composite_encoded_document_artifacts.py",
    }
)


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Mark retained numerical reconstruction tests as expensive.

    Structural DataObject checks and compact artifact-identity checks remain bounded;
    tests that reconstruct retained matrices or execute independent numerical routes
    receive the explicit ``expensive`` marker.
    """
    for item in items:
        if not item.path.is_relative_to(COMPOSITE_TEST_ROOT):
            continue
        if item.path.name not in NON_RECONSTRUCTION_TESTS:
            item.add_marker(pytest.mark.expensive)
