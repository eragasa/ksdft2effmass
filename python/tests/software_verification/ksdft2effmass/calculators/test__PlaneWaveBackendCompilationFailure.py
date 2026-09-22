r"""Software verification of ``PlaneWaveBackendCompilationFailure``.

Evidence profile: routine

Bounded artifact scope: fail-closed portable-to-backend compilation outcomes.

Facet and represented meaning

The module verifies the closed one-to-one association between compilation failure
outcomes and their reason codes.

Intrinsic and cross-object scope

``PlaneWaveBackendCompilationFailure`` is the sole system under test. Binder behavior,
backend support policy, native rendering, and calculator execution are excluded.

VVUQ and scientific exclusions

This is software verification of represented failure consistency. It establishes no
numerical verification, scientific validation, uncertainty quantification, backend
equivalence, or human acceptance.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.calculators.dft.pw import (
    PlaneWaveBackendCompilationFailure,
    PlaneWaveBackendCompilationFailureCode,
    PlaneWaveBackendCompilationOutcome,
)

pytestmark = pytest.mark.software_verification
SUT = PlaneWaveBackendCompilationFailure

_VALID_PAIRS = (
    pytest.param(
        PlaneWaveBackendCompilationOutcome.UNSUPPORTED,
        PlaneWaveBackendCompilationFailureCode.UNSUPPORTED_REQUIREMENT,
        id="unsupported_requirement",
    ),
    pytest.param(
        PlaneWaveBackendCompilationOutcome.INCOMPATIBLE,
        PlaneWaveBackendCompilationFailureCode.INCOMPATIBLE_MODEL_AND_SUPPLEMENT,
        id="incompatible_model_and_supplement",
    ),
    pytest.param(
        PlaneWaveBackendCompilationOutcome.INVALID,
        PlaneWaveBackendCompilationFailureCode.INVALID_SPECIFICATION,
        id="invalid_specification",
    ),
    pytest.param(
        PlaneWaveBackendCompilationOutcome.ERROR,
        PlaneWaveBackendCompilationFailureCode.INTERNAL_ERROR,
        id="internal_error",
    ),
)

_CONTRADICTORY_PAIRS = (
    pytest.param(
        PlaneWaveBackendCompilationOutcome.INCOMPATIBLE,
        PlaneWaveBackendCompilationFailureCode.UNSUPPORTED_REQUIREMENT,
        id="unsupported_code_with_incompatible_outcome",
    ),
    pytest.param(
        PlaneWaveBackendCompilationOutcome.INVALID,
        PlaneWaveBackendCompilationFailureCode.UNSUPPORTED_REQUIREMENT,
        id="unsupported_code_with_invalid_outcome",
    ),
    pytest.param(
        PlaneWaveBackendCompilationOutcome.ERROR,
        PlaneWaveBackendCompilationFailureCode.UNSUPPORTED_REQUIREMENT,
        id="unsupported_code_with_error_outcome",
    ),
    pytest.param(
        PlaneWaveBackendCompilationOutcome.UNSUPPORTED,
        PlaneWaveBackendCompilationFailureCode.INCOMPATIBLE_MODEL_AND_SUPPLEMENT,
        id="incompatible_code_with_unsupported_outcome",
    ),
    pytest.param(
        PlaneWaveBackendCompilationOutcome.INVALID,
        PlaneWaveBackendCompilationFailureCode.INCOMPATIBLE_MODEL_AND_SUPPLEMENT,
        id="incompatible_code_with_invalid_outcome",
    ),
    pytest.param(
        PlaneWaveBackendCompilationOutcome.ERROR,
        PlaneWaveBackendCompilationFailureCode.INCOMPATIBLE_MODEL_AND_SUPPLEMENT,
        id="incompatible_code_with_error_outcome",
    ),
    pytest.param(
        PlaneWaveBackendCompilationOutcome.UNSUPPORTED,
        PlaneWaveBackendCompilationFailureCode.INVALID_SPECIFICATION,
        id="invalid_code_with_unsupported_outcome",
    ),
    pytest.param(
        PlaneWaveBackendCompilationOutcome.INCOMPATIBLE,
        PlaneWaveBackendCompilationFailureCode.INVALID_SPECIFICATION,
        id="invalid_code_with_incompatible_outcome",
    ),
    pytest.param(
        PlaneWaveBackendCompilationOutcome.ERROR,
        PlaneWaveBackendCompilationFailureCode.INVALID_SPECIFICATION,
        id="invalid_code_with_error_outcome",
    ),
    pytest.param(
        PlaneWaveBackendCompilationOutcome.UNSUPPORTED,
        PlaneWaveBackendCompilationFailureCode.INTERNAL_ERROR,
        id="internal_code_with_unsupported_outcome",
    ),
    pytest.param(
        PlaneWaveBackendCompilationOutcome.INCOMPATIBLE,
        PlaneWaveBackendCompilationFailureCode.INTERNAL_ERROR,
        id="internal_code_with_incompatible_outcome",
    ),
    pytest.param(
        PlaneWaveBackendCompilationOutcome.INVALID,
        PlaneWaveBackendCompilationFailureCode.INTERNAL_ERROR,
        id="internal_code_with_invalid_outcome",
    ),
)


class TestPlaneWaveBackendCompilationFailure:
    """Own software evidence for closed backend-compilation failures."""

    @pytest.mark.parametrize(("outcome", "code"), _VALID_PAIRS)
    def test_constructor__outcome_code_pair__admits_exact_association(
        self,
        outcome: PlaneWaveBackendCompilationOutcome,
        code: PlaneWaveBackendCompilationFailureCode,
    ) -> None:
        """Evidence ID: SV-CALCULATOR-VERIFY-003

        Requirement: Each failure code has exactly one associated non-success outcome.

        Acceptance: Every documented pair constructs, preserves both exact enum
        members, and rejects ordinary field reassignment.
        """
        result = SUT(outcome, code)

        assert result.outcome is outcome
        assert result.code is code
        with pytest.raises(FrozenInstanceError):
            result.code = code  # type: ignore[misc]

    @pytest.mark.parametrize(("outcome", "code"), _CONTRADICTORY_PAIRS)
    def test_constructor__outcome_code_pair__rejects_contradictory_association(
        self,
        outcome: PlaneWaveBackendCompilationOutcome,
        code: PlaneWaveBackendCompilationFailureCode,
    ) -> None:
        """Evidence ID: SV-CALCULATOR-VERIFY-004

        Requirement: A failure cannot combine a valid reason code with a different
        valid failure outcome.

        Acceptance: Each of the twelve contradictory failure-outcome/code pairs raises
        ``ValueError`` naming outcome/code agreement.
        """
        with pytest.raises(ValueError, match="agree with failure code"):
            SUT(outcome, code)

    def test_constructor__fields__reject_success_and_wrong_semantic_types(self) -> None:
        """Evidence ID: SV-CALCULATOR-VERIFY-005

        Requirement: A failure result accepts neither the ``COMPILED`` outcome nor raw
        string substitutes for either enum field.

        Acceptance: ``COMPILED`` raises ``ValueError``; each raw string raises
        ``TypeError`` identifying the required enum class.
        """
        code = PlaneWaveBackendCompilationFailureCode.INTERNAL_ERROR
        with pytest.raises(ValueError, match="failure outcome"):
            SUT(PlaneWaveBackendCompilationOutcome.COMPILED, code)
        with pytest.raises(TypeError, match="PlaneWaveBackendCompilationOutcome"):
            SUT("error", code)  # type: ignore[arg-type]
        with pytest.raises(TypeError, match="PlaneWaveBackendCompilationFailureCode"):
            SUT(
                PlaneWaveBackendCompilationOutcome.ERROR,
                "internal_error",  # type: ignore[arg-type]
            )
