"""Software verification for typed immutable endpoint sewing diagnostics."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import numpy as np
import pytest

from ksdft2effmass.campaigns.periodic_reduction.higher_rank_d1 import (
    HigherRankD1EndpointSewingDiagnostics,
)

pytestmark = pytest.mark.software_verification


class TestHigherRankD1EndpointSewingDiagnostics:
    """Establish exact scalar types, finiteness, and immutability."""

    def test_attributes__retain_finite_builtin_float_defects(self) -> None:
        """Endpoint sewing has named fields rather than positional tuple semantics."""
        diagnostics = HigherRankD1EndpointSewingDiagnostics(1.0e-14, 2.0e-14)

        assert diagnostics.frame_defect == 1.0e-14
        assert diagnostics.projector_defect == 2.0e-14
        with pytest.raises(FrozenInstanceError):
            diagnostics.frame_defect = 0.0  # type: ignore[misc]

    @pytest.mark.parametrize("value", [True, np.float64(0.0)])
    def test_attributes__reject_non_builtin_float_scalars(
        self, value: bool | np.float64
    ) -> None:
        """Boolean and NumPy scalar coercion cannot cross the record boundary."""
        with pytest.raises(TypeError, match="frame_defect"):
            HigherRankD1EndpointSewingDiagnostics(value, 0.0)

    @pytest.mark.parametrize("value", [float("nan"), float("inf"), -1.0])
    def test_attributes__reject_nonfinite_or_negative_defects(
        self, value: float
    ) -> None:
        """Unavailable or invalid numeric payloads cannot use sentinel values."""
        with pytest.raises(ValueError, match="projector_defect"):
            HigherRankD1EndpointSewingDiagnostics(0.0, value)
