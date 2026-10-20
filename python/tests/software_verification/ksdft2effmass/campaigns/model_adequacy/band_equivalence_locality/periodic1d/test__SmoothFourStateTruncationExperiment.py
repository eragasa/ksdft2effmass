"""Software verification for finite-range non-flat band consequences."""

from __future__ import annotations

import math
from dataclasses import replace

import numpy as np
import pytest

from ksdft2effmass.campaigns.model_adequacy.band_equivalence_locality.periodic1d import (  # noqa: E501
    SmoothFourStateDefinition,
    SmoothFourStateTruncationDefinition,
    SmoothFourStateTruncationExperiment,
)

pytestmark = pytest.mark.software_verification


class TestSmoothFourStateTruncationExperiment:
    """Establish disjoint evaluation and separated approximation channels."""

    @staticmethod
    def _model() -> SmoothFourStateDefinition:
        return SmoothFourStateDefinition(
            reciprocal_mesh_size=32,
            amplitudes=(0.0, math.pi / 8.0, math.pi / 4.0),
            minimum_external_gap=1.0,
            minimum_transport_singular_value=0.99,
            frame_absolute_tolerance=1.0e-11,
            harmonic_absolute_degeneracy_tolerance=1.0e-14,
            harmonic_relative_degeneracy_tolerance=1.0e-13,
            verification_absolute_tolerance=1.0e-10,
            parent_hopping_scale=1.0,
        )

    @classmethod
    def _definition(cls) -> SmoothFourStateTruncationDefinition:
        return SmoothFourStateTruncationDefinition(
            model=cls._model(),
            maximum_ranges=(0, 1, 2, 15),
            evaluation_mesh_size=129,
        )

    def test_definition__rejects_cyclic_nyquist_and_invalid_scalar_types(self) -> None:
        model = self._model()
        with pytest.raises(ValueError, match="exclude the cyclic Nyquist"):
            SmoothFourStateTruncationDefinition(
                model=model,
                maximum_ranges=(0, 16),
                evaluation_mesh_size=129,
            )
        with pytest.raises(TypeError, match="built-in ints"):
            SmoothFourStateTruncationDefinition(
                model=model,
                maximum_ranges=(0, True),
                evaluation_mesh_size=129,
            )
        with pytest.raises(ValueError, match=r"at least 2\*N\+1"):
            SmoothFourStateTruncationDefinition(
                model=model,
                maximum_ranges=(0, 1),
                evaluation_mesh_size=64,
            )

    def test_execute__separates_nyquist_interpolation_and_range_truncation(
        self,
    ) -> None:
        result = SmoothFourStateTruncationExperiment().execute(self._definition())

        assert result.minimum_construction_evaluation_separation > 0.0
        assert (
            tuple(point.amplitude for point in result.points)
            == self._model().amplitudes
        )
        assert result.points[
            0
        ].comparison_maximum_interpolation_band_error == pytest.approx(0.0, abs=2.0e-14)
        assert result.points[-1].maximum_direct_band_defect == pytest.approx(
            0.0, abs=2.0e-14
        )
        for point in result.points:
            assert point.reference_maximum_ordinary_hermiticity_defect <= 1.0e-11
            assert point.comparison_maximum_ordinary_hermiticity_defect <= 1.0e-11
            ordinary_reference = tuple(
                item.reference_ordinary_omitted_power for item in point.ranges
            )
            ordinary_comparison = tuple(
                item.comparison_ordinary_omitted_power for item in point.ranges
            )
            assert ordinary_reference == tuple(sorted(ordinary_reference, reverse=True))
            assert ordinary_comparison == tuple(
                sorted(ordinary_comparison, reverse=True)
            )
            full = point.ranges[-1]
            assert full.reference_ordinary_omitted_power == pytest.approx(0.0)
            assert full.comparison_ordinary_omitted_power == pytest.approx(0.0)
            assert full.reference_maximum_band_error == pytest.approx(0.0, abs=2.0e-14)
            assert full.comparison_maximum_truncation_band_error == pytest.approx(
                0.0, abs=2.0e-14
            )
            assert full.reference_total_omitted_power == pytest.approx(
                point.reference_nyquist_power
            )
            assert full.comparison_total_omitted_power == pytest.approx(
                point.comparison_nyquist_power
            )
            assert full.comparison_maximum_total_band_error == pytest.approx(
                point.comparison_maximum_interpolation_band_error,
                abs=2.0e-14,
            )

    def test_owner_eigenvalues__reject_nonhermitian_evaluated_matrices(self) -> None:
        matrices = np.asarray([[[0.0, 1.0], [0.0, 0.0]]], dtype=np.complex128)

        with pytest.raises(ValueError):
            SmoothFourStateTruncationExperiment._owner_eigenvalues(matrices, 1.0e-12)

    def test_result__rejects_total_power_that_excludes_ordinary_omissions(self) -> None:
        result = SmoothFourStateTruncationExperiment().execute(self._definition())
        first_range = result.points[-1].ranges[0]

        with pytest.raises(ValueError, match="must include Nyquist power"):
            replace(first_range, comparison_total_omitted_power=0.0)
