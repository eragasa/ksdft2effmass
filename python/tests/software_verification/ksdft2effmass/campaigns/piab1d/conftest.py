"""Pytest-owned classification for retained PIAB1D campaigns."""

from pathlib import Path

import pytest

CAMPAIGN_ROOT = Path(__file__).resolve().parent
COMPATIBILITY_TEST = "test__piab1d_legacy_import.py"


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Mark retained reconstruction tests, but not the import contract, expensive."""
    for item in items:
        if not item.path.is_relative_to(CAMPAIGN_ROOT):
            continue
        if item.path.name != COMPATIBILITY_TEST:
            item.add_marker(pytest.mark.expensive)
