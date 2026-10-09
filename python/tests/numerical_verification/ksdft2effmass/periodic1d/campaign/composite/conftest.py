"""Pytest-owned execution classification for composite numerical verification."""

from pathlib import Path

import pytest

COMPOSITE_NUMERICAL_ROOT = Path(__file__).resolve().parent


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Mark every retained composite reconstruction test as expensive."""
    for item in items:
        if item.path.is_relative_to(COMPOSITE_NUMERICAL_ROOT):
            item.add_marker(pytest.mark.expensive)
