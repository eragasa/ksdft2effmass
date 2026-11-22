"""Synthetic direction controls, not silicon orbital or symmetry evidence."""

from __future__ import annotations

from dataclasses import replace
from fractions import Fraction

import common_space.verification.tests.test__CommonSpaceNativeOverlapReconstruction as native_fixture
import pytest
from common_space.verification.controls import (
    CommonSpaceDeficientDirectionAnalysis,
    CommonSpaceDirectionOutcome,
    CommonSpaceUnitaryInvariance,
)
from common_space.verification.gram_rank import GramEigenvalueInterval
from common_space.verification.native_overlap import (
    CommonSpaceNativeOverlapReconstruction,
)
from common_space.verification.native_precision import (
    CommonSpaceMatrixUncertainty,
    CommonSpaceNativePrecisionAssessment,
    CommonSpaceNativeRankAssessment,
    CommonSpaceNativeRoundingModel,
)

pytestmark = [pytest.mark.integration, pytest.mark.numerical_verification]


class TestCommonSpaceDeficientDirectionAnalysis:
    """Check known mixed directions and explicit arithmetic/input stops."""

    @staticmethod
    def _assessment(
        *,
        component_error: Fraction = Fraction(0),
        threshold: Fraction = Fraction(1, 100),
    ) -> CommonSpaceNativeRankAssessment:
        loader, _ = native_fixture.TestCommonSpaceNativeOverlapReconstruction._fixture(
            mix_atomic_direction=True
        )
        overlap = CommonSpaceNativeOverlapReconstruction(
            parsed_inputs=loader.execute(), ordered_index=0
        ).execute()
        return CommonSpaceNativePrecisionAssessment(
            overlap=overlap,
            rounding_model=CommonSpaceNativeRoundingModel(
                amn_component_error=component_error,
                gauge_component_error=Fraction(0),
                disentanglement_component_error=Fraction(0),
            ),
            frozen_rank_threshold=threshold,
        ).execute()

    def test_mixed_atomic_direction__encloses_known_orbital_and_group_weights(
        self,
    ) -> None:
        assessment = self._assessment()
        direction = CommonSpaceDeficientDirectionAnalysis(
            assessment=assessment
        ).execute()
        assert assessment.resolved_rank == 9
        assert direction.outcome is CommonSpaceDirectionOutcome.enclosed
        expected = tuple(
            Fraction(1, 4) if i in (0, 4, 5, 9) else Fraction(0) for i in range(10)
        )
        for weight, interval in zip(expected, direction.orbital_intervals, strict=True):
            assert interval.lower <= weight <= interval.upper
        for weight, interval in zip(
            (Fraction(1, 2), Fraction(0), Fraction(1, 2)),
            direction.group_intervals,
            strict=True,
        ):
            assert interval.lower <= weight <= interval.upper
        assert CommonSpaceUnitaryInvariance(assessment=assessment).execute()

    def test_input_projector_bound__contains_analytic_rotated_null_direction(
        self,
    ) -> None:
        assessment = self._assessment(component_error=Fraction(1, 4096))
        direction = CommonSpaceDeficientDirectionAnalysis(
            assessment=assessment
        ).execute()
        assert direction.outcome is CommonSpaceDirectionOutcome.enclosed
        # A rational Givens change on atomic coordinates 0 and 1 has a known null
        # direction. Check that this changed matrix lies inside the declared B ball.
        t = Fraction(1, 4096)
        cosine = (1 - t * t) / (1 + t * t)
        sine = 2 * t / (1 + t * t)
        squared_norm = sum(
            (
                entry.real**2 + entry.imaginary**2
                for row in assessment.overlap._matrix.rows
                for entry in row
            ),
            start=Fraction(0),
        )
        perturbation_upper = CommonSpaceMatrixUncertainty._sqrt_upper(squared_norm) * (
            abs(1 - cosine) + abs(sine)
        )
        assert perturbation_upper <= assessment.uncertainty.combined_error_bound
        weights = (
            cosine**2 / 4,
            sine**2 / 4,
            Fraction(0),
            Fraction(0),
            Fraction(1, 4),
            Fraction(1, 4),
            Fraction(0),
            Fraction(0),
            Fraction(0),
            Fraction(1, 4),
        )
        assert sum(weights) == 1
        for weight, interval in zip(weights, direction.orbital_intervals, strict=True):
            assert interval.lower <= weight <= interval.upper

    def test_bad_minimum_candidate__cannot_supply_resolved_weights(self) -> None:
        assessment = self._assessment()
        wrong_candidate = tuple((Fraction(i == 3), Fraction(0)) for i in range(10))
        arithmetic = replace(assessment.arithmetic, minimum_eigenvector=wrong_candidate)
        direction = CommonSpaceDeficientDirectionAnalysis(
            assessment=replace(assessment, arithmetic=arithmetic)
        ).execute()
        assert (
            direction.outcome is CommonSpaceDirectionOutcome.arithmetic_gap_unresolved
        )
        assert direction.orbital_intervals == ()

    def test_insufficient_input_gap__stops_despite_resolved_raw_rank(self) -> None:
        assessment = self._assessment(
            component_error=Fraction(1, 40), threshold=Fraction(1, 2)
        )
        assert assessment.uncertainty_bound_covered
        assert assessment.resolved_rank == 9
        direction = CommonSpaceDeficientDirectionAnalysis(
            assessment=assessment
        ).execute()
        assert direction.outcome is CommonSpaceDirectionOutcome.input_gap_unresolved
        assert direction.orbital_intervals == ()

    def test_uncovered_input_bound__cannot_supply_direction_weights(self) -> None:
        assessment = self._assessment(component_error=Fraction(1))
        assert assessment.arithmetic.resolved_rank == 9
        assert assessment.resolved_rank is None
        direction = CommonSpaceDeficientDirectionAnalysis(
            assessment=assessment
        ).execute()
        assert direction.outcome is CommonSpaceDirectionOutcome.rank_unresolved
        assert direction.orbital_intervals == ()

    def test_threshold_straddling__is_not_repaired_by_direction_control(self) -> None:
        assessment = self._assessment()
        threshold_squared = assessment.frozen_rank_threshold**2
        intervals = (
            GramEigenvalueInterval(lower=Fraction(0), upper=2 * threshold_squared),
            *assessment.arithmetic.eigenvalue_intervals[1:],
        )
        arithmetic = replace(assessment.arithmetic, eigenvalue_intervals=intervals)
        assert arithmetic.rank_lower_bound == 9
        assert arithmetic.rank_upper_bound == 10
        ambiguous = replace(assessment, arithmetic=arithmetic)
        direction = CommonSpaceDeficientDirectionAnalysis(
            assessment=ambiguous
        ).execute()
        assert direction.outcome is CommonSpaceDirectionOutcome.rank_unresolved
        assert not CommonSpaceUnitaryInvariance(assessment=ambiguous).execute()

    @pytest.mark.parametrize(
        "value",
        (
            Fraction(0),
            Fraction(1, 4),
            Fraction(2),
            Fraction(2, 9),
            Fraction(1, 2**2001),
        ),
    )
    def test_square_root_bounds__use_exact_outward_endpoints(
        self, value: Fraction
    ) -> None:
        lower = CommonSpaceMatrixUncertainty._sqrt_lower(value)
        upper = CommonSpaceMatrixUncertainty._sqrt_upper(value)
        assert lower >= 0
        assert lower**2 <= value <= upper**2
