"""Software verification for the higher-rank D1 numerical exception boundary."""

from __future__ import annotations

from typing import cast

import pytest

from ksdft2effmass.campaigns.periodic_reduction.higher_rank_d1 import (
    HigherRankD1A1NumericallyUnresolvedSelection,
    HigherRankD1AlignmentBackendError,
    HigherRankD1BackendExceptionCode,
    HigherRankD1NumericalExceptionHandler,
    HigherRankD1TransportBackendError,
)

pytestmark = pytest.mark.software_verification


class TestHigherRankD1NumericalExceptionHandler:
    """Establish thrown exceptions and closed retained dispositions."""

    def test_exception_code__maps_documented_causes_to_strenum(self) -> None:
        """One handler maps backend exception classes to stable enum members."""
        assert (
            HigherRankD1NumericalExceptionHandler.exception_code(
                HigherRankD1AlignmentBackendError(FloatingPointError())
            )
            is HigherRankD1BackendExceptionCode.ARITHMETIC_NONFINITE
        )
        assert (
            HigherRankD1NumericalExceptionHandler.exception_code(
                HigherRankD1AlignmentBackendError(RuntimeError())
            )
            is HigherRankD1BackendExceptionCode.NONCONVERGENCE
        )
        assert (
            HigherRankD1NumericalExceptionHandler.exception_code(
                HigherRankD1AlignmentBackendError(ValueError())
            )
            is HigherRankD1BackendExceptionCode.VALIDATION_FAILED
        )
        assert str(HigherRankD1BackendExceptionCode.NONCONVERGENCE) == (
            "backend-nonconvergence"
        )

    def test_transport_error__retains_stage_context_until_handled(self) -> None:
        """Thrown transport errors preserve only context needed by the case handler."""
        backend = FloatingPointError()
        error = HigherRankD1TransportBackendError("closure", 513, backend)

        assert error.stage == "closure"
        assert error.attempted_link_count == 513
        assert error.backend_exception is backend
        assert (
            HigherRankD1NumericalExceptionHandler.exception_code(error)
            is HigherRankD1BackendExceptionCode.ARITHMETIC_NONFINITE
        )

    def test_unresolved_record__rejects_raw_string_code(self) -> None:
        """Raw strings cannot bypass the retained exception-code enum boundary."""
        raw = cast(HigherRankD1BackendExceptionCode, "backend-nonconvergence")

        with pytest.raises(
            TypeError, match="exception_code must be HigherRankD1BackendExceptionCode"
        ):
            HigherRankD1A1NumericallyUnresolvedSelection(2049, raw)
