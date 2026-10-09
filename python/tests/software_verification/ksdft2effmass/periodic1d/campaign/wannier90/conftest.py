"""Pytest-owned cost classification for the periodic-1D Wannier90 campaign."""

from pathlib import Path

import pytest

CAMPAIGN_ROOT = Path(__file__).resolve().parent
ROUTINE_TESTS = frozenset(
    {
        "test__Periodic1DWannier90EncodedDocuments.py",
        "test__Periodic1DWannier90NativeArtifactGroup.py",
        "test__integration__wannier90_encoded_document_artifacts.py",
    }
)


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Mark local parsing and reconstruction tests as expensive.

    Structural DataObject and retained-byte identity tests remain routine. Tests that
    parse the complete native artifact inventory or reconstruct Wilson loops receive
    the project ``expensive`` marker without embedding cost policy in production code.
    """
    for item in items:
        if not item.path.is_relative_to(CAMPAIGN_ROOT):
            continue
        if item.path.name not in ROUTINE_TESTS:
            item.add_marker(pytest.mark.expensive)
