"""Pytest-owned classification for retained PIAB1D campaigns."""

from pathlib import Path

import pytest

CAMPAIGN_ROOT = Path(__file__).resolve().parent


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Mark retained PIAB1D reconstruction tests as expensive."""
    for item in items:
        if item.path.is_relative_to(CAMPAIGN_ROOT):
            item.add_marker(pytest.mark.expensive)
