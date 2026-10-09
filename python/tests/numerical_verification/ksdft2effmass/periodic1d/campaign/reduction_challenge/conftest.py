"""Pytest-owned execution classification for challenge numerical verification."""

from pathlib import Path

import pytest

REDUCTION_CHALLENGE_NUMERICAL_ROOT = Path(__file__).resolve().parent


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Mark every retained dense reconstruction test as expensive."""
    for item in items:
        if item.path.is_relative_to(REDUCTION_CHALLENGE_NUMERICAL_ROOT):
            item.add_marker(pytest.mark.expensive)
