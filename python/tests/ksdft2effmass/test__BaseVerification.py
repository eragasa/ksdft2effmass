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

    def test_observation__different_units__rejects_comparison(self) -> None:
        with pytest.raises(ValueError, match="units must agree"):
            VerificationObservation(
                value=ScalarQuantity(1.0, Unitless()),
                tolerance=ScalarQuantity(1.0, PhysicalUnit("electron_volt")),
            )
