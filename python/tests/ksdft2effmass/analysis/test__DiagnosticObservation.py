"""Software verification of typed diagnostic observations."""

from __future__ import annotations

import pytest
from projectkoios.physkit.linalg.matrix.norm import MatrixNormEnum
from projectkoios.physkit.units import PhysicalUnit, ScalarQuantity, Unitless

from ksdft2effmass.analysis import (
    DiagnosticObservation,
    MatrixNormDiagnosticOptions,
)
from ksdft2effmass.serialization import TypedJsonValueCodec

pytestmark = pytest.mark.software_verification
SUT = DiagnosticObservation


class TestDiagnosticObservation:
    """Own validation and typed serialization of one diagnostic observation."""

    def test_round_trip__matrix_norm_observation__preserves_policy(self) -> None:
        observation = SUT(
            value=ScalarQuantity(2.5e-14, Unitless()),
            atol=ScalarQuantity(1.0e-12, Unitless()),
            rtol=0.0,
            options=MatrixNormDiagnosticOptions(matrix_norm=MatrixNormEnum.frobenius),
        )
        codec = TypedJsonValueCodec()

        decoded = codec.deserialize(codec.serialize(observation))

        assert isinstance(decoded, dict)
        reconstructed = SUT.from_dict(decoded)
        assert reconstructed.value.magnitude == observation.value.magnitude
        assert reconstructed.value.unit == observation.value.unit
        assert reconstructed.atol.magnitude == observation.atol.magnitude
        assert reconstructed.atol.unit == observation.atol.unit
        assert reconstructed.rtol == 0.0
        assert reconstructed.options is not None
        assert reconstructed.options.matrix_norm is MatrixNormEnum.frobenius

    def test_init__incompatible_atol_unit__rejects(self) -> None:
        with pytest.raises(ValueError, match="same unit"):
            SUT(
                value=ScalarQuantity(1.0, Unitless()),
                atol=ScalarQuantity(1.0e-12, PhysicalUnit("electron_volt")),
                rtol=0.0,
            )

    @pytest.mark.parametrize("rtol", [True, 0, "0.0"])
    def test_init__non_float_rtol__rejects(self, rtol: float) -> None:
        with pytest.raises(TypeError, match="built-in float"):
            SUT(
                value=ScalarQuantity(1.0, Unitless()),
                atol=ScalarQuantity(1.0e-12, Unitless()),
                rtol=rtol,
            )
