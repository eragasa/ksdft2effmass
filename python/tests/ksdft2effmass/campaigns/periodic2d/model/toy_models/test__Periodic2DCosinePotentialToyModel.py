"""Software verification for the periodic-2D cosine-potential toy model."""

import numpy as np
import pytest

from ksdft2effmass.campaigns.periodic2d.model.toy_models import (
    Periodic2DCosinePotentialToyModel,
    Periodic2DFiniteDifferenceHamiltonianConstructor,
    Periodic2DFiniteDifferenceHamiltonianRequest,
    Periodic2DPlaneWaveHamiltonianConstructor,
    Periodic2DPlaneWaveHamiltonianRequest,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DCosinePotentialToyModel:
    """Own model invariants and represented-Hamiltonian evidence."""

    @staticmethod
    def require(condition: bool, message: str) -> None:
        """Raise an optimization-stable test failure when a condition is false."""
        if not condition:
            raise AssertionError(message)

    def test_method__constructors__preserve_separable_and_hermitian_contracts(
        self,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-TWO-D-006.

        Requirement: The reusable toy model must construct compatible Hermitian
        plane-wave and finite-difference representations, preserving exact separability
        when the mixed cosine coupling is zero.

        Method: Construct both representations and compare the two-dimensional
        plane-wave matrix with a Kronecker sum of one-dimensional factors.

        Oracle: Exact finite Kronecker identity and represented Hermiticity.

        Acceptance: Shapes agree with the declared bases, both matrices are Hermitian,
        and the separable plane-wave defect is at binary64 roundoff.

        Interpretation: A pass verifies reusable finite representation mechanics.

        Limitations: This is synthetic software verification, not material evidence.
        """
        model = Periodic2DCosinePotentialToyModel(0.4, 0.7, 0.0)
        momentum_x = 0.13
        momentum_y = -0.21
        cutoff = 2
        plane_wave = (
            Periodic2DPlaneWaveHamiltonianConstructor()
            .execute(
                Periodic2DPlaneWaveHamiltonianRequest(
                    model, momentum_x, momentum_y, cutoff
                )
            )
            .matrix
        )
        points = 7
        finite_difference = (
            Periodic2DFiniteDifferenceHamiltonianConstructor()
            .execute(
                Periodic2DFiniteDifferenceHamiltonianRequest(
                    model, momentum_x, momentum_y, points
                )
            )
            .matrix
        )
        indices = np.arange(-cutoff, cutoff + 1, dtype=np.float64)
        x_matrix = np.diag(np.square(momentum_x + indices))
        x_matrix += np.diag(np.full(2 * cutoff, model.lambda_x / 2.0), 1)
        x_matrix += np.diag(np.full(2 * cutoff, model.lambda_x / 2.0), -1)
        y_matrix = np.diag(np.square(momentum_y + indices))
        y_matrix += np.diag(np.full(2 * cutoff, model.lambda_y / 2.0), 1)
        y_matrix += np.diag(np.full(2 * cutoff, model.lambda_y / 2.0), -1)
        expected = np.kron(x_matrix, np.eye(2 * cutoff + 1)) + np.kron(
            np.eye(2 * cutoff + 1), y_matrix
        )

        self.require(plane_wave.shape == (25, 25), "plane-wave shape mismatch")
        self.require(
            finite_difference.shape == (49, 49),
            "finite-difference shape mismatch",
        )
        self.require(
            bool(np.array_equal(plane_wave, plane_wave.conj().T)),
            "plane-wave matrix is not Hermitian",
        )
        self.require(
            bool(np.array_equal(finite_difference, finite_difference.conj().T)),
            "finite-difference matrix is not Hermitian",
        )
        self.require(
            float(np.max(np.abs(plane_wave - expected))) < 2.0e-15,
            "separable Kronecker identity failed",
        )

    def test_contract__numeric_inputs__reject_booleans_and_nonfinite_values(
        self,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-TWO-D-007.

        Requirement: Public numerical contracts reject booleans and nonfinite values.

        Method: Construct invalid model and request records.

        Oracle: Exact documented runtime type and finite-value contracts.

        Acceptance: Every invalid value raises ``TypeError`` or ``ValueError``.

        Interpretation: A pass verifies the public numeric boundary.

        Limitations: The cases sample each semantic numeric category once.
        """
        with pytest.raises(TypeError):
            Periodic2DCosinePotentialToyModel(True, 0.7, 0.0)
        with pytest.raises(ValueError):
            Periodic2DCosinePotentialToyModel(float("nan"), 0.7, 0.0)
        model = Periodic2DCosinePotentialToyModel(0.4, 0.7, 0.0)
        with pytest.raises(TypeError):
            Periodic2DPlaneWaveHamiltonianRequest(
                model,
                True,
                0.0,
                2,
            )
        with pytest.raises(ValueError):
            Periodic2DFiniteDifferenceHamiltonianRequest(model, 0.0, 0.0, 6)
