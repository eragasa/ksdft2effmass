"""Pytest-owned classification for retained PIAB1D studies."""

from pathlib import Path

import pytest

STUDY_ROOT = Path(__file__).resolve().parent


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Mark retained PIAB1D reconstruction studies as expensive."""
    for item in items:
        if item.path.is_relative_to(STUDY_ROOT):
            item.add_marker(pytest.mark.expensive)
