r"""Software verification of ``ScientificExecutionAuthorityVerificationKind``.

Evidence profile: routine

Bounded artifact scope: the public authority-verification discriminator.

Facet and represented meaning

This module verifies the closed represented outcomes of authority checks.

Intrinsic and cross-object scope

Enum membership belongs here; authorization policy belongs to its ActionObject.

VVUQ and scientific exclusions

This is software verification only. It establishes no authority, execution,
scientific validation, uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows import ScientificExecutionAuthorityVerificationKind

pytestmark = pytest.mark.software_verification
SUT = ScientificExecutionAuthorityVerificationKind


class TestScientificExecutionAuthorityVerificationKind:
    """Own software evidence for the authority-check discriminator."""

    def test_fields__members__form_exact_closed_set(self) -> None:
        """Retain the exact verified, failed, and indeterminate alternatives.

        Evidence ID: SV-WCI-AUTHORITY-VERIFICATION-KIND-001

        Requirement: Authority verification has exactly three documented outcomes.

        Acceptance: Iteration returns the exact values in declaration order.
        """
        assert tuple(SUT) == (
            SUT.VERIFIED,
            SUT.FAILED,
            SUT.INDETERMINATE,
        )
