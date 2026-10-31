"""PhysKit-backed lattice geometry for locality development diagnostics.

PhysKit owns direct-lattice metrics, coordinate mapping, exact integral operations, and
lattice-displacement transformation. This module retains only campaign-owned shell
scaling, selected covariance probes, and basis-pair aggregation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray
from projectkoios.physkit.periodic.lattice import DirectLatticeMetric
from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeDimension,
    LatticeDisplacement,
    LatticeIntegerComponents,
)
from projectkoios.physkit.periodic.lattice.symmetry import (
    IntegerMatrix,
    IntegralLatticeOperation,
    LatticeDisplacementTransformer,
)

from ksdft2effmass.numerical_consistency import (
    NumericalConsistency,
    PeriodicTensorGridSeparationAnalyzer,
)
from ksdft2effmass.real_space_support_truncation import (
    BasisResolvedMetricGeometry,
    MetricGeometry,
    MetricShellClassification,
    MetricShellSupportClassifier,
    MetricShellValueAnalyzer,
)
from ksdft2effmass.serialization import StringWireEnum

type FloatArray = NDArray[np.float64]
type IntArray = NDArray[np.int64]


def _direct_metric(geometry: MetricGeometry) -> DirectLatticeMetric:
    if not isinstance(geometry, MetricGeometry):
        raise TypeError("geometry must inherit MetricGeometry")
    geometry.validate_metric_geometry()
    return geometry.direct_metric


def _typed_displacements(
    geometry: MetricGeometry,
    displacements: IntArray,
) -> tuple[LatticeDisplacement, ...]:
    _direct_metric(geometry)
    if type(displacements) is not np.ndarray:
        raise TypeError("displacements must be an exact numpy.ndarray")
    if displacements.dtype != np.dtype(np.int64):
        raise TypeError("displacements must have dtype int64")
    if displacements.ndim != 2 or displacements.shape[1] != geometry.dimension:
        raise ValueError("displacements must have shape (count, geometry.dimension)")
    if geometry.dimension == 2:
        dimension = LatticeDimension.TWO
        typed_displacements = tuple(
            LatticeDisplacement(
                dimension,
                (int(components[0]), int(components[1])),
            )
            for components in displacements
        )
    elif geometry.dimension == 3:
        dimension = LatticeDimension.THREE
        typed_displacements = tuple(
            LatticeDisplacement(
                dimension,
                (int(components[0]), int(components[1]), int(components[2])),
            )
            for components in displacements
        )
    else:
        raise ValueError("only two- and three-dimensional metrics are supported")
    return typed_displacements


def metric_indices(geometry: MetricGeometry, displacements: IntArray) -> IntArray:
    """Return scaled metric values through the typed geometry owner."""
    analysis = MetricShellValueAnalyzer().execute(
        geometry,
        _typed_displacements(geometry, displacements),
    )
    return np.asarray(analysis.metric_shell_values, dtype=np.int64)


def metric_shell_classification(
    geometry: MetricGeometry,
    displacements: IntArray,
) -> MetricShellClassification:
    """Classify one ordinary conjugate-closed support through the typed owner."""
    return MetricShellSupportClassifier().execute(
        geometry,
        _typed_displacements(geometry, displacements),
    )


def minimum_mesh_separation(construction: FloatArray, evaluation: FloatArray) -> float:
    """Return tensor-grid torus separation through its consistency owner."""
    return PeriodicTensorGridSeparationAnalyzer().execute(construction, evaluation)


class BandEquivalenceLocalityMetricCovarianceProbeEnum(StringWireEnum):
    """Identify one campaign-selected primitive-basis covariance probe."""

    PRIMITIVE_BASIS_SHEAR_2D_V1 = "primitive-basis-shear-2d-v1"
    PRIMITIVE_BASIS_SHEAR_3D_V1 = "primitive-basis-shear-3d-v1"


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityMetricCovarianceDefectResult(NumericalConsistency):
    """Retain the selected probe identity and its maximum absolute defect."""

    probe: BandEquivalenceLocalityMetricCovarianceProbeEnum
    maximum_absolute_defect: float

    def __post_init__(self) -> None:
        if type(self.probe) is not BandEquivalenceLocalityMetricCovarianceProbeEnum:
            raise TypeError(
                "probe must be BandEquivalenceLocalityMetricCovarianceProbeEnum"
            )
        if type(self.maximum_absolute_defect) is not float:
            raise TypeError("maximum_absolute_defect must be a built-in float")
        if (
            not math.isfinite(self.maximum_absolute_defect)
            or self.maximum_absolute_defect < 0.0
        ):
            raise ValueError("maximum_absolute_defect must be finite and nonnegative")


@dataclass(frozen=True, slots=True)
class _MetricCovarianceProbeDefinition:
    """Correlate one private campaign probe with all of its finite policy."""

    identity: BandEquivalenceLocalityMetricCovarianceProbeEnum
    transform: IntegralLatticeOperation
    inverse_transform: IntegralLatticeOperation
    samples: tuple[LatticeDisplacement, ...]

    def __post_init__(self) -> None:
        if type(self.identity) is not BandEquivalenceLocalityMetricCovarianceProbeEnum:
            raise TypeError("identity must be the exact covariance-probe enum")
        if type(self.transform) is not IntegralLatticeOperation:
            raise TypeError("transform must be IntegralLatticeOperation")
        if type(self.inverse_transform) is not IntegralLatticeOperation:
            raise TypeError("inverse_transform must be IntegralLatticeOperation")
        if self.transform.dimension is not self.inverse_transform.dimension:
            raise ValueError("transform and inverse_transform dimensions must agree")
        if self.transform.dimension not in (
            LatticeDimension.TWO,
            LatticeDimension.THREE,
        ):
            raise ValueError("covariance probes require dimension two or three")
        expected_identity = {
            LatticeDimension.TWO: (
                BandEquivalenceLocalityMetricCovarianceProbeEnum.PRIMITIVE_BASIS_SHEAR_2D_V1
            ),
            LatticeDimension.THREE: (
                BandEquivalenceLocalityMetricCovarianceProbeEnum.PRIMITIVE_BASIS_SHEAR_3D_V1
            ),
        }[self.transform.dimension]
        if self.identity is not expected_identity:
            raise ValueError("probe identity must match the transform dimension")
        transform = np.asarray(self.transform.matrix, dtype=np.int64)
        inverse = np.asarray(self.inverse_transform.matrix, dtype=np.int64)
        if not np.array_equal(
            transform @ inverse,
            np.eye(transform.shape[0], dtype=np.int64),
        ):
            raise ValueError("inverse_transform must invert transform exactly")
        if (
            type(self.samples) is not tuple
            or not self.samples
            or any(
                type(sample) is not LatticeDisplacement
                or sample.dimension is not self.transform.dimension
                for sample in self.samples
            )
        ):
            raise TypeError(
                "samples must be typed displacements in the probe dimension"
            )


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityMetricCovarianceDefectAnalyzer:
    """Execute the covariance probe selected for one dimensional family."""

    geometry: MetricGeometry
    _probe: _MetricCovarianceProbeDefinition = field(init=False, repr=False)

    def __post_init__(self) -> None:
        metric = _direct_metric(self.geometry)
        object.__setattr__(self, "_probe", self._probe_for(metric.dimension))

    @staticmethod
    def _probe_for(dimension: int) -> _MetricCovarianceProbeDefinition:
        probe_type = BandEquivalenceLocalityMetricCovarianceProbeEnum
        identity: BandEquivalenceLocalityMetricCovarianceProbeEnum
        transform_matrix: IntegerMatrix
        inverse_matrix: IntegerMatrix
        sample_components: tuple[LatticeIntegerComponents, ...]
        if dimension == 2:
            identity = probe_type.PRIMITIVE_BASIS_SHEAR_2D_V1
            lattice_dimension = LatticeDimension.TWO
            transform_matrix = ((1, 1), (0, 1))
            inverse_matrix = ((1, -1), (0, 1))
            sample_components = ((0, 0), (1, 0), (0, 1), (2, -1))
        elif dimension == 3:
            identity = probe_type.PRIMITIVE_BASIS_SHEAR_3D_V1
            lattice_dimension = LatticeDimension.THREE
            transform_matrix = ((1, 1, 0), (0, 1, 0), (0, 0, 1))
            inverse_matrix = ((1, -1, 0), (0, 1, 0), (0, 0, 1))
            sample_components = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (1, -1, 2))
        else:
            raise ValueError("only two- and three-dimensional metrics are supported")
        return _MetricCovarianceProbeDefinition(
            identity=identity,
            transform=IntegralLatticeOperation(
                identifier="development-primitive-basis-transform",
                dimension=lattice_dimension,
                matrix=transform_matrix,
            ),
            inverse_transform=IntegralLatticeOperation(
                identifier="development-primitive-basis-inverse",
                dimension=lattice_dimension,
                matrix=inverse_matrix,
            ),
            samples=tuple(
                LatticeDisplacement(lattice_dimension, components)
                for components in sample_components
            ),
        )

    def execute(self) -> BandEquivalenceLocalityMetricCovarianceDefectResult:
        """Return the maximum squared-length defect for the selected probe."""
        metric = self.geometry.direct_metric.metric_tensor
        transformer = LatticeDisplacementTransformer()
        transformed_samples = tuple(
            transformer.execute(self._probe.inverse_transform, sample).components
            for sample in self._probe.samples
        )
        transform_array = np.asarray(self._probe.transform.matrix, dtype=np.float64)
        transformed_metric = transform_array.T @ metric @ transform_array
        sample_array = np.asarray(
            tuple(sample.components for sample in self._probe.samples),
            dtype=np.float64,
        )
        transformed_array = np.asarray(transformed_samples, dtype=np.float64)
        original_values = np.einsum("ri,ij,rj->r", sample_array, metric, sample_array)
        transformed_values = np.einsum(
            "ri,ij,rj->r",
            transformed_array,
            transformed_metric,
            transformed_array,
        )
        return BandEquivalenceLocalityMetricCovarianceDefectResult(
            probe=self._probe.identity,
            maximum_absolute_defect=float(
                np.max(np.abs(original_values - transformed_values))
            ),
        )


def basis_distance_range(
    geometry: BasisResolvedMetricGeometry, retained_displacements: IntArray
) -> tuple[float | None, float | None]:
    """Return the min/max PhysKit-mapped basis-pair distances in one support."""
    if not isinstance(geometry, BasisResolvedMetricGeometry):
        raise TypeError("geometry must inherit BasisResolvedMetricGeometry")
    geometry.validate_basis_resolved_metric_geometry()
    metric = geometry.direct_metric
    if not geometry.basis_offsets:
        return None, None
    offsets = tuple(
        np.asarray(value, dtype=np.float64) for value in geometry.basis_offsets
    )
    distances: list[float] = []
    for displacement in retained_displacements:
        for source in offsets:
            for target in offsets:
                vector = displacement.astype(np.float64) + target - source
                distances.append(float(np.linalg.norm(metric.to_cartesian(vector))))
    return min(distances), max(distances)


__all__ = [
    "BandEquivalenceLocalityMetricCovarianceDefectAnalyzer",
    "BandEquivalenceLocalityMetricCovarianceDefectResult",
    "BandEquivalenceLocalityMetricCovarianceProbeEnum",
    "MetricGeometry",
    "basis_distance_range",
    "metric_indices",
    "metric_shell_classification",
    "minimum_mesh_separation",
]
