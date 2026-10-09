"""Pytest-owned execution classification for the reduction-challenge family."""

from pathlib import Path

import pytest

REDUCTION_CHALLENGE_TEST_ROOT = Path(__file__).resolve().parent
NUMERICAL_RECONSTRUCTION_TESTS = frozenset(
    {
        "test__Periodic1DReductionChallengeCampaign.py",
        "test__Periodic1DReductionChallengeVerifiedWorkflow.py",
    }
)


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Mark tests that execute independent dense reconstruction as expensive.

    Intrinsic DataObject, codec, correlation, and compact artifact-identity tests remain
    bounded. Campaign verification and the integrated verified Workflow reconstruct
    dense finite representations and therefore receive the explicit marker.
    """
    for item in items:
        if not item.path.is_relative_to(REDUCTION_CHALLENGE_TEST_ROOT):
            continue
        if item.path.name in NUMERICAL_RECONSTRUCTION_TESTS:
            item.add_marker(pytest.mark.expensive)
