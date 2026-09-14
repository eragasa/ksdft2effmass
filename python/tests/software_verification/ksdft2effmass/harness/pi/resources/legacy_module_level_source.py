r"""Software verification of a synthetic legacy artifact.

Evidence profile: claim_bearing

Bounded artifact scope: one synthetic legacy evidence module.

Facet and represented meaning

The artifact represents exact synthetic legacy values.

Intrinsic and cross-object scope

Only explicit literal behavior is covered.

VVUQ and scientific exclusions

This is synthetic software verification only.
"""

import pytest

pytestmark = pytest.mark.software_verification


def test_artifact__legacy_literal__equals_itself() -> None:
    """Evidence ID: software-verification.synthetic.legacy.literal.equals-itself

    Requirement: The legacy literal equals itself.

    Method: Compare one literal integer with itself.

    Oracle: Python integer equality.

    Acceptance: Equality is true.

    Interpretation: Failure indicates synthetic legacy fixture drift.

    Limitations: No production behavior is represented.
    """
    assert 1 == 1
