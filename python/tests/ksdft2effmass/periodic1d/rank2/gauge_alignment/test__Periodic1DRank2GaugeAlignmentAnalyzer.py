"""Tests for the extracted rank-two gauge-alignment capability."""

import numpy as np
import pytest
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesSolver,
)
from projectkoios.physkit.units import ComplexMatrixQuantity, ScalarQuantity, Unitless

from ksdft2effmass.gauge_alignment import (
    GaugeAlignmentActionConvention,
    GaugeAlignmentInnerProductConvention,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.composite import (
    Periodic1DCompositeBandAlignmentCalculationResult,
    Periodic1DCompositeBandAlignmentConfiguration,
)
from ksdft2effmass.periodic1d.rank2.gauge_alignment import analysis as analysis_module
from ksdft2effmass.periodic1d.rank2.gauge_alignment import result as result_module
from ksdft2effmass.periodic1d.rank2.gauge_alignment.analysis import (
    Periodic1DRank2GaugeAlignmentAnalysisRequest,
    Periodic1DRank2GaugeAlignmentAnalyzer,
)
from ksdft2effmass.periodic1d.rank2.gauge_alignment.result import (
    Periodic1DRank2GaugeAlignmentAnalysis,
)
from ksdft2effmass.solidstate import (
    CenteredUniformReciprocalMesh1D,
    ReciprocalBandFramePath1D,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DRank2GaugeAlignmentAnalyzer:
    """Preserve the maintained composite producer's alignment values exactly."""

    def test__public_class_names__use_the_analysis_capability_triad(self) -> None:
        assert analysis_module.__all__ == [
            "Periodic1DRank2GaugeAlignmentAnalyzer",
            "Periodic1DRank2GaugeAlignmentAnalysisRequest",
        ]
        assert result_module.__all__ == ["Periodic1DRank2GaugeAlignmentAnalysis"]
        assert not hasattr(analysis_module, "Periodic1DRank2GaugeAlignmentRequest")
        assert not hasattr(result_module, "Periodic1DRank2GaugeAlignmentResult")

    def test__request__requires_rank_two_paths(self) -> None:
        with pytest.raises(ValueError, match="both have rank two"):
            self._request(
                reference=self._path(point_count=2, ambient_dimension=3, rank=1),
                attacked=self._path(point_count=2, ambient_dimension=3, rank=2),
            )

    def test__request__requires_one_reciprocal_mesh(self) -> None:
        with pytest.raises(ValueError, match="meshes must agree"):
            self._request(
                reference=self._path(point_count=2, ambient_dimension=3, rank=2),
                attacked=self._path(point_count=4, ambient_dimension=3, rank=2),
            )

    def test__request__requires_one_ambient_state_space_dimension(self) -> None:
        with pytest.raises(ValueError, match="ambient dimensions must agree"):
            self._request(
                reference=self._path(point_count=2, ambient_dimension=3, rank=2),
                attacked=self._path(point_count=2, ambient_dimension=4, rank=2),
            )

    def test__request__requires_one_endpoint_sewing_convention(self) -> None:
        with pytest.raises(ValueError, match="sewing maps must agree"):
            self._request(
                reference=self._path(point_count=2, ambient_dimension=3, rank=2),
                attacked=self._path(
                    point_count=2,
                    ambient_dimension=3,
                    rank=2,
                    sewing_sign=-1.0,
                ),
            )

    def test__analysis__requires_rank_two_paths(self) -> None:
        rank_one_path = self._path(point_count=2, ambient_dimension=3, rank=1)
        with pytest.raises(ValueError, match="both have rank two"):
            self._analysis(
                rank_one_path,
                rank_one_path,
                pointwise_rotation_count=2,
            )

    def test__analysis__requires_one_rotation_per_sample(self) -> None:
        path = self._path(point_count=2, ambient_dimension=3, rank=2)
        with pytest.raises(ValueError, match="rotation count"):
            self._analysis(path, path, pointwise_rotation_count=1)

    def test__analysis__requires_correlated_aligned_paths(self) -> None:
        pointwise = self._path(point_count=2, ambient_dimension=3, rank=2)
        with pytest.raises(ValueError, match="aligned path meshes must agree"):
            self._analysis(
                pointwise,
                self._path(point_count=4, ambient_dimension=3, rank=2),
                pointwise_rotation_count=2,
            )
        with pytest.raises(ValueError, match="ambient dimensions must agree"):
            self._analysis(
                pointwise,
                self._path(point_count=2, ambient_dimension=4, rank=2),
                pointwise_rotation_count=2,
            )
        with pytest.raises(ValueError, match="aligned path sewing maps must agree"):
            self._analysis(
                pointwise,
                self._path(
                    point_count=2,
                    ambient_dimension=3,
                    rank=2,
                    sewing_sign=-1.0,
                ),
                pointwise_rotation_count=2,
            )

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

        request = Periodic1DRank2GaugeAlignmentAnalysisRequest(
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
        )
        analyzer = Periodic1DRank2GaugeAlignmentAnalyzer(
            request,
            NumpyBatchedComplexUnitaryProcrustesSolver(),
        )
        result = analyzer.execute()

        assert request.retained_rank == 2
        assert request.gauge_group == "U(2)"
        assert request.alignment_sample_count == mesh.point_count
        assert request.action_convention is GaugeAlignmentActionConvention.RIGHT
        assert (
            request.inner_product_convention
            is GaugeAlignmentInnerProductConvention.EUCLIDEAN_ORTHONORMAL
        )
        assert type(result) is Periodic1DRank2GaugeAlignmentAnalysis
        assert analyzer.analysis_identity == request.analysis_identity
        assert result.analysis_identity == request.analysis_identity
        assert result.retained_rank == request.retained_rank
        assert result.gauge_group == request.gauge_group
        assert result.alignment_sample_count == request.alignment_sample_count
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

    @staticmethod
    def _path(
        *,
        point_count: int,
        ambient_dimension: int,
        rank: int,
        sewing_sign: float = 1.0,
    ) -> ReciprocalBandFramePath1D:
        unit = Unitless()
        frame = np.eye(ambient_dimension, rank, dtype=np.complex128)
        return ReciprocalBandFramePath1D(
            mesh=CenteredUniformReciprocalMesh1D(
                reciprocal_period=ScalarQuantity(1.0, unit),
                point_count=point_count,
            ),
            frames=tuple(
                ComplexMatrixQuantity(frame, unit) for _ in range(point_count)
            ),
            sewing_map=ComplexMatrixQuantity(
                sewing_sign * np.eye(ambient_dimension, dtype=np.complex128),
                unit,
            ),
            orthonormality_absolute_tolerance=0.0,
        )

    @staticmethod
    def _request(
        *,
        reference: ReciprocalBandFramePath1D,
        attacked: ReciprocalBandFramePath1D,
    ) -> Periodic1DRank2GaugeAlignmentAnalysisRequest:
        return Periodic1DRank2GaugeAlignmentAnalysisRequest(
            reference=reference,
            attacked=attacked,
            rank_absolute_tolerance=0.0,
            rank_relative_tolerance=0.0,
            validation_absolute_tolerance=0.0,
        )

    @staticmethod
    def _analysis(
        pointwise_aligned: ReciprocalBandFramePath1D,
        globally_aligned: ReciprocalBandFramePath1D,
        *,
        pointwise_rotation_count: int,
    ) -> Periodic1DRank2GaugeAlignmentAnalysis:
        unit = Unitless()
        rotation = ComplexMatrixQuantity(np.eye(2, dtype=np.complex128), unit)
        return Periodic1DRank2GaugeAlignmentAnalysis(
            pointwise_aligned=pointwise_aligned,
            globally_aligned=globally_aligned,
            pointwise_rotations=tuple(
                rotation for _ in range(pointwise_rotation_count)
            ),
            global_rotation=rotation,
            pointwise_minimum_cross_singular_value=1.0,
            global_minimum_cross_singular_value=1.0,
            pointwise_maximum_rank_cutoff=0.0,
            global_rank_cutoff=0.0,
        )
