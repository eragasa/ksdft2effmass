"""Numerical-verification contracts for the independent analytic oracle."""

import numpy as np

from periodic1d_rankn_analytic_oracle import (
    Periodic1DRankNAnalyticApproximationOracle,
)


class TestPeriodic1DRankNAnalyticApproximationOracle:
    """Establish exact identities used to check discrete approximations."""

    def test__sample__preserves_projectors_and_operator_spectra(self) -> None:
        coordinates = np.asarray(
            -0.5 + np.arange(17, dtype=np.float64) / 17.0,
            dtype=np.float64,
        )
        sample = Periodic1DRankNAnalyticApproximationOracle().sample(
            retained_rank=4,
            circuit_depth=3,
            reduced_coordinates=coordinates,
        )

        reference_projectors = sample.reference_frames @ np.swapaxes(
            sample.reference_frames.conjugate(), -1, -2
        )
        transformed_projectors = sample.gauge_transformed_frames @ np.swapaxes(
            sample.gauge_transformed_frames.conjugate(), -1, -2
        )
        assert np.allclose(
            transformed_projectors,
            reference_projectors,
            atol=1.0e-14,
        )
        assert np.allclose(
            np.linalg.eigvalsh(sample.gauge_transformed_operators),
            sample.retained_energies,
            atol=1.0e-14,
        )

    def test__sample__recovers_reference_fields_with_the_inverse_right_action(
        self,
    ) -> None:
        coordinates = np.asarray((-0.5, -0.125, 0.25), dtype=np.float64)
        sample = Periodic1DRankNAnalyticApproximationOracle().sample(
            retained_rank=3,
            circuit_depth=2,
            reduced_coordinates=coordinates,
        )
        inverse = sample.transformation.inverse_right_actions

        assert np.allclose(
            sample.gauge_transformed_frames @ inverse,
            sample.reference_frames,
            atol=1.0e-14,
        )
        assert np.allclose(
            sample.transformation.unitaries
            @ sample.gauge_transformed_operators
            @ inverse,
            sample.reference_operators,
            atol=1.0e-14,
        )
