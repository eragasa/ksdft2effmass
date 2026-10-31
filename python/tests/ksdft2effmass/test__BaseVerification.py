"""Software verification of composable verification representation boundaries."""

from __future__ import annotations

import numpy as np
import pytest
from projectkoios.physkit.units import (
    MatrixQuantity,
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
)

from ksdft2effmass.hamiltonian import HamiltonianVerification
from ksdft2effmass.serialization import BaseTypedRecord
from ksdft2effmass.verification import (
    BaseVerification,
    MaximumAbsoluteErrorComparison,
    VerificationObservation,
)

pytestmark = pytest.mark.software_verification
SUT = BaseVerification


class TestBaseVerification:
    """Own final recursive dictionary and generic JSON composition."""

    def test_round_trip__composite_verification__uses_inherited_boundaries(
        self,
    ) -> None:
        verification = HamiltonianVerification.evaluate(
            {
                "matrix_error": MaximumAbsoluteErrorComparison(
                    observed=MatrixQuantity(
                        np.asarray([[1.0, 1.0e-14], [0.0, 1.0]]), Unitless()
                    ),
                    reference=MatrixQuantity(np.eye(2), Unitless()),
                    tolerance=ScalarQuantity(1.0e-12, Unitless()),
                )
            }
        )

        reconstructed = HamiltonianVerification.from_json(verification.to_json())

        assert issubclass(HamiltonianVerification, SUT)
        assert reconstructed.to_dict() == verification.to_dict()
        assert reconstructed.passed is True
        for name in ("to_dict", "from_dict", "to_json", "from_json"):
            assert name not in HamiltonianVerification.__dict__
            method = BaseTypedRecord.__dict__[name]
            if isinstance(method, classmethod):
                method = method.__func__
            assert getattr(method, "__final__", False) is True

    def test_observation__dimensionless__constructs_typed_unitless_values(self) -> None:
        observation = VerificationObservation.dimensionless(
            value=1.0e-12,
            tolerance=1.0e-10,
        )

        assert observation.value == ScalarQuantity(1.0e-12, Unitless())
        assert observation.tolerance == ScalarQuantity(1.0e-10, Unitless())
        assert observation.passed

    @pytest.mark.parametrize("value", (True, 1, "1.0"))
    def test_observation__dimensionless__rejects_non_float_scalars(
        self,
        value: bool | int | str,
    ) -> None:
        with pytest.raises(TypeError, match="value must be a built-in float"):
            VerificationObservation.dimensionless(
                value=value,  # type: ignore[arg-type]
                tolerance=1.0,
            )

    @pytest.mark.parametrize("value", (-1.0, float("inf"), float("nan")))
    def test_observation__dimensionless__rejects_invalid_value(
        self,
        value: float,
    ) -> None:
        with pytest.raises(
            ValueError,
            match="verification value must be finite and nonnegative",
        ):
            VerificationObservation.dimensionless(value=value, tolerance=1.0)

    @pytest.mark.parametrize("tolerance", (True, 1, "1.0"))
    def test_observation__dimensionless__rejects_non_float_tolerance(
        self,
        tolerance: bool | int | str,
    ) -> None:
        with pytest.raises(TypeError, match="tolerance must be a built-in float"):
            VerificationObservation.dimensionless(
                value=0.0,
                tolerance=tolerance,  # type: ignore[arg-type]
            )

    @pytest.mark.parametrize("tolerance", (-1.0, float("inf"), float("nan")))
    def test_observation__dimensionless__rejects_invalid_tolerance_value(
        self,
        tolerance: float,
    ) -> None:
        with pytest.raises(
            ValueError,
            match="verification tolerance must be finite and nonnegative",
        ):
            VerificationObservation.dimensionless(value=0.0, tolerance=tolerance)

    def test_observation__different_units__rejects_comparison(self) -> None:
        with pytest.raises(ValueError, match="units must agree"):
            VerificationObservation(
                value=ScalarQuantity(1.0, Unitless()),
                tolerance=ScalarQuantity(1.0, PhysicalUnit("electron_volt")),
            )
