"""Pytest-owned classification for periodic-1D numerical reconstruction."""

from pathlib import Path

import pytest

EXPENSIVE_ROOT = Path(__file__).resolve().parent


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Mark retained periodic-1D numerical reconstruction as expensive."""
    for item in items:
        if item.path.is_relative_to(EXPENSIVE_ROOT):
            item.add_marker(pytest.mark.expensive)
