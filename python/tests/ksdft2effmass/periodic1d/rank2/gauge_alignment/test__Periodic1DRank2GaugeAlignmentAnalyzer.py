"""Tests for the extracted rank-two gauge-alignment capability."""

import numpy as np
import pytest
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesSolver,
)
from projectkoios.physkit.units import ComplexMatrixQuantity, ScalarQuantity, Unitless

from ksdft2effmass.periodic1d.rank2.band_alignment.composite import (
    Periodic1DCompositeBandAlignmentCalculationResult,
    Periodic1DCompositeBandAlignmentConfiguration,
)
from ksdft2effmass.periodic1d.rank2.gauge_alignment.analysis import (
    Periodic1DRank2GaugeAlignmentAnalyzer,
    Periodic1DRank2GaugeAlignmentRequest,
)
from ksdft2effmass.solidstate import (
    CenteredUniformReciprocalMesh1D,
    ReciprocalBandFramePath1D,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DRank2GaugeAlignmentAnalyzer:
    """Preserve the maintained composite producer's alignment values exactly."""

    def test__execute__matches_the_aggregate_result_values(
        self,
        composite_configuration: Periodic1DCompositeBandAlignmentConfiguration,
        composite_result: Periodic1DCompositeBandAlignmentCalculationResult,
    ) -> None:
        unit = Unitless()
        mesh = CenteredUniformReciprocalMesh1D(
            ScalarQuantity(1.0, unit),
            composite_configuration.construction_size,
        )
        sewing_map = ComplexMatrixQuantity(
            np.eye(4, dtype=np.complex128),
            unit,
        )
        reference = ReciprocalBandFramePath1D(
            mesh=mesh,
            frames=composite_result.reference_frames,
            sewing_map=sewing_map,
            orthonormality_absolute_tolerance=(
                composite_configuration.dimensionless_absolute_tolerance
            ),
        )
        attacked = ReciprocalBandFramePath1D(
            mesh=mesh,
            frames=composite_result.attacked_frames,
            sewing_map=sewing_map,
            orthonormality_absolute_tolerance=(
                composite_configuration.dimensionless_absolute_tolerance
            ),
        )

        result = Periodic1DRank2GaugeAlignmentAnalyzer(
            Periodic1DRank2GaugeAlignmentRequest(
                reference=reference,
                attacked=attacked,
                rank_absolute_tolerance=(
                    composite_configuration.procrustes_rank_absolute_tolerance
                ),
                rank_relative_tolerance=(
                    composite_configuration.procrustes_rank_relative_tolerance
                ),
                validation_absolute_tolerance=(
                    composite_configuration.dimensionless_absolute_tolerance
                ),
            ),
            NumpyBatchedComplexUnitaryProcrustesSolver(),
        ).execute()

        for observed, expected in (
            (
                result.pointwise_aligned.frames,
                composite_result.pointwise_aligned_frames,
            ),
            (result.globally_aligned.frames, composite_result.globally_aligned_frames),
            (result.pointwise_rotations, composite_result.pointwise_rotations),
        ):
            assert all(
                np.array_equal(left.magnitude, right.magnitude)
                for left, right in zip(observed, expected, strict=True)
            )
        assert np.array_equal(
            result.global_rotation.magnitude,
            composite_result.global_rotation.magnitude,
        )
        assert result.pointwise_minimum_cross_singular_value == (
            composite_result.diagnostics.pointwise_minimum_cross_singular_value
        )
        assert result.global_minimum_cross_singular_value == (
            composite_result.diagnostics.global_minimum_cross_singular_value
        )
        assert result.pointwise_maximum_rank_cutoff == (
            composite_result.diagnostics.pointwise_maximum_rank_cutoff
        )
        assert result.global_rank_cutoff == (
            composite_result.diagnostics.global_rank_cutoff
        )
