r"""Routine intrinsic evidence for optimizer-basin verification results.

Evidence profile: routine

These synthetic tests establish immutable representation, exact scalar typing, bounded
count ranges, digest syntax, and aggregate pass logic. Direct construction does not
prove verifier execution, source authentication, optimizer convergence, scientific
validity, uncertainty quantification, or acceptance.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.verify import (
    Periodic2DOptimizerBasinCampaignVerificationResult,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic2DOptimizerBasinCampaignVerificationResult
DIGEST = "d3074c086f6d8071bb608cde25b5605b6898b55b749b27c32ae735256299ff85"


class TestPeriodic2DOptimizerBasinCampaignVerificationResult:
    """Own intrinsic result-contract evidence for crosswalk row 052."""

    @staticmethod
    def result(
        *,
        source_passed: bool = True,
        structural_passed: bool = True,
        configuration_count: int = 9,
        converged_count: int = 51,
        nonconverged_count: int = 21,
        digest: str = DIGEST,
    ) -> Periodic2DOptimizerBasinCampaignVerificationResult:
        """Construct one synthetic intrinsically valid result by default."""
        return SUT(
            source_passed,
            structural_passed,
            configuration_count,
            converged_count,
            nonconverged_count,
            digest,
        )

    def test_construction__retains_intrinsic_state_and_pass_logic(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-052-RESULT-001.

        Requirement: A result retains exact bounded diagnostics and reports the
        conjunction of its two pass indicators without implying Action execution.

        Acceptance: Valid state is preserved, both true indicators pass, and either
        false indicator produces a false aggregate disposition.
        """
        result = self.result()

        assert result.configuration_count == 9
        assert result.converged_count == 51
        assert result.nonconverged_count == 21
        assert result.retained_result_sha256 == DIGEST
        assert result.passes
        assert not self.result(source_passed=False).passes
        assert not self.result(structural_passed=False).passes

    def test_construction__rejects_nonexact_flags_and_counts(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-052-RESULT-002.

        Requirement: Public scalar diagnostics reject Boolean/numeric substitution and
        invalid count ranges.

        Acceptance: Integer flags, Boolean counts, floating counts, and negative counts
        fail with the documented exception categories.
        """
        with pytest.raises(
            TypeError, match="source_authentication_passed must be a built-in bool"
        ):
            SUT(1, True, 9, 51, 21, DIGEST)  # type: ignore[arg-type]
        with pytest.raises(TypeError, match="configuration_count must be an integer"):
            SUT(True, True, True, 51, 21, DIGEST)
        with pytest.raises(TypeError, match="converged_count must be an integer"):
            SUT(True, True, 9, 51.0, 21, DIGEST)  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="nonconverged_count must be nonnegative"):
            SUT(True, True, 9, 51, -1, DIGEST)

    def test_construction__rejects_invalid_digest_and_is_frozen(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-052-RESULT-003.

        Requirement: The retained wire identity is exact lowercase SHA-256 and result
        state is operationally immutable.

        Acceptance: Wrong digest types and syntax fail; a valid field cannot be
        reassigned.
        """
        with pytest.raises(TypeError, match="retained_result_sha256 must be a string"):
            SUT(True, True, 9, 51, 21, b"0" * 64)  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="lowercase SHA-256 digest"):
            SUT(True, True, 9, 51, 21, "G" * 64)

        result = self.result()
        with pytest.raises(FrozenInstanceError):
            result.configuration_count = 8  # type: ignore[misc]
