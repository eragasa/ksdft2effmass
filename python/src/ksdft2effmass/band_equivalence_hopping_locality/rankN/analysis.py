"""Dimension-neutral production arithmetic for periodic rank-N aggregates."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

import numpy as np
from projectkoios.numerics.finite_periodic.meshes import CenteredUniformMesh
from projectkoios.numerics.finite_periodic.numpy.matrix_series import (
    NumpyFiniteFourierMatrixSeries,
)
from projectkoios.numerics.finite_periodic.numpy.tensor_product_evaluation import (
    NumpyTensorProductFourierMatrixEvaluationDefinition,
    NumpyTensorProductFourierMatrixSeriesEvaluator,
)
from projectkoios.numerics.finite_periodic.numpy.transforms import (
    NumpyCenteredUniformMeshMatrixFourierTransformDefinition,
    NumpyCenteredUniformMeshMatrixFourierTransformer,
)
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array, Int64Array

from ksdft2effmass.band_equivalence_hopping_locality.shell_power import (
    MetricShellHoppingPowerResult,
)
from ksdft2effmass.gauge_alignment import (
    GaugeAlignmentActionConvention,
    GaugeAlignmentAnalysisIdentity,
    GaugeAlignmentGroupIdentity,
    GaugeAlignmentInnerProductConvention,
)
from ksdft2effmass.real_space_support_truncation import (
    MetricShellClassification,
)


@dataclass(frozen=True, slots=True)
class _ReferenceFourierData:
    source_mesh: CenteredUniformMesh
    construction_axes: tuple[Float64Array, ...]
    evaluation_axes: tuple[Float64Array, ...]
    ordinary_series: NumpyFiniteFourierMatrixSeries
    full_construction: Complex128Array
    full_evaluation: Complex128Array
    shell_classification: MetricShellClassification
    metric_indices: Int64Array
    metric_shell_values: tuple[int, ...]
    locality: MetricShellHoppingPowerResult
    shell_evaluation_fields: tuple[Complex128Array, ...]


class _PeriodicRankNBandEquivalenceHoppingLocalityProductionArithmetic:
    """Own production arithmetic that binds no dimensional scientific policy."""

    __slots__ = ()

    _SPATIAL_DIMENSION: ClassVar[int]

    @staticmethod
    def _coordinate_axis(size: int, offset: float) -> Float64Array:
        return np.asarray(
            -0.5 + (np.arange(size, dtype=np.float64) + offset) / float(size),
            dtype=np.float64,
        )

    @classmethod
    def _coordinates(cls, size: int, offset: float) -> Float64Array:
        axis = cls._coordinate_axis(size, offset)
        axes = tuple(axis for _ in range(cls._SPATIAL_DIMENSION))
        return np.asarray(
            np.stack(np.meshgrid(*axes, indexing="ij"), axis=-1),
            dtype=np.float64,
        )

    @classmethod
    def _centered_mesh(cls, size: int, offset: float) -> CenteredUniformMesh:
        return CenteredUniformMesh(
            cls._SPATIAL_DIMENSION,
            size,
            tuple(offset for _ in range(cls._SPATIAL_DIMENSION)),
        )

    @classmethod
    def _tensor_axes(cls, axis: Float64Array) -> tuple[Float64Array, ...]:
        return tuple(axis for _ in range(cls._SPATIAL_DIMENSION))

    @staticmethod
    def _transform(
        mesh: CenteredUniformMesh,
        values: Complex128Array,
    ) -> NumpyFiniteFourierMatrixSeries:
        return (
            NumpyCenteredUniformMeshMatrixFourierTransformer(
                definition=NumpyCenteredUniformMeshMatrixFourierTransformDefinition.from_array(
                    mesh,
                    values,
                )
            )
            .result()
            .series
        )

    @staticmethod
    def _evaluate(
        mesh: CenteredUniformMesh,
        series: NumpyFiniteFourierMatrixSeries,
        axes: tuple[Float64Array, ...],
    ) -> Complex128Array:
        return (
            NumpyTensorProductFourierMatrixSeriesEvaluator(
                definition=NumpyTensorProductFourierMatrixEvaluationDefinition.from_arrays(
                    mesh,
                    series,
                    axes,
                )
            )
            .result()
            .matrix_values
        )

    @classmethod
    def _ordinary_series(
        cls,
        construction_size: int,
        series: NumpyFiniteFourierMatrixSeries,
    ) -> NumpyFiniteFourierMatrixSeries:
        ordinary = ~np.any(
            series.integer_modes == -construction_size // 2,
            axis=1,
        )
        return NumpyFiniteFourierMatrixSeries.from_arrays(
            cls._SPATIAL_DIMENSION,
            series.integer_modes[ordinary],
            series.matrix_coefficients[ordinary],
        )

    @classmethod
    def _common_alignment_identity(
        cls,
        retained_rank: int,
        construction_size: int,
    ) -> GaugeAlignmentAnalysisIdentity:
        return GaugeAlignmentAnalysisIdentity(
            gauge_group_identity=GaugeAlignmentGroupIdentity.unitary(
                represented_dimension=retained_rank
            ),
            alignment_sample_count=construction_size**cls._SPATIAL_DIMENSION,
            action_convention=GaugeAlignmentActionConvention.RIGHT,
            inner_product_convention=GaugeAlignmentInnerProductConvention.EUCLIDEAN,
        )

    @staticmethod
    def _apply_right_action(
        operators: Complex128Array,
        right_action: Complex128Array,
    ) -> Complex128Array:
        return np.asarray(
            np.swapaxes(right_action.conjugate(), -1, -2) @ operators @ right_action,
            dtype=np.complex128,
        )
