"""Pytest-owned classification for expensive periodic-2D retained workflows."""

from pathlib import Path

import pytest

EXPENSIVE_ROOT = Path(__file__).resolve().parent


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Mark calculation-heavy retained Stage B and Stage C evidence as expensive."""
    for item in items:
        if item.path.is_relative_to(EXPENSIVE_ROOT):
            item.add_marker(pytest.mark.expensive)
