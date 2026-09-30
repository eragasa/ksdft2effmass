"""Pytest-owned classification for calculation-heavy monograph campaigns."""

from pathlib import Path

import pytest

CAMPAIGN_ROOT = Path(__file__).resolve().parent
EXPENSIVE_CAMPAIGNS = frozenset(("particle_in_box", "periodic_1d"))


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Mark retained numerical reconstruction campaigns as expensive."""
    for item in items:
        if not item.path.is_relative_to(CAMPAIGN_ROOT):
            continue
        relative = item.path.relative_to(CAMPAIGN_ROOT)
        if relative.parts and relative.parts[0] in EXPENSIVE_CAMPAIGNS:
            item.add_marker(pytest.mark.expensive)
