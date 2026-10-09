"""Pytest-owned classification for isolated-band numerical reconstruction."""

from pathlib import Path

import pytest

EXPENSIVE_ROOT = Path(__file__).resolve().parent


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Mark canonical isolated-band numerical reconstruction as expensive."""
    for item in items:
        if item.path.is_relative_to(EXPENSIVE_ROOT):
            item.add_marker(pytest.mark.expensive)
