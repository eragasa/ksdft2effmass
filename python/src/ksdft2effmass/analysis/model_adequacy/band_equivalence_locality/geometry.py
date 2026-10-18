"""PhysKit-backed lattice geometry for locality development diagnostics.

PhysKit owns direct-lattice metrics, coordinate mapping, exact integral operations, and
lattice-displacement transformation. This module retains only campaign-owned shell
scaling, selected covariance probes, and basis-pair aggregation.
"""

from __future__ import annotations

import math
from typing import Protocol

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

type FloatArray = NDArray[np.float64]
type IntArray = NDArray[np.int64]


class MetricGeometry(Protocol):
    """Expose the exact geometry fields required by this campaign."""

    @property
    def dimension(self) -> int: ...

    @property
    def direct_metric(self) -> DirectLatticeMetric: ...

    @property
    def shell_metric_scale(self) -> float: ...

    @property
    def basis_offsets(self) -> tuple[tuple[float, ...], ...]: ...


def _direct_metric(geometry: MetricGeometry) -> DirectLatticeMetric:
    if geometry.dimension != geometry.direct_metric.dimension:
        raise ValueError("geometry and direct-metric dimensions must agree")
    return geometry.direct_metric


def metric_indices(geometry: MetricGeometry, displacements: IntArray) -> IntArray:
    """Return campaign shell labels from the PhysKit-owned metric tensor."""
    metric = _direct_metric(geometry).metric_tensor
    values = geometry.shell_metric_scale * np.einsum(
        "ri,ij,rj->r", displacements, metric, displacements
    )
    rounded = np.rint(values)
    if float(np.max(np.abs(values - rounded))) > 1.0e-12:
        raise ValueError("scaled physical metric does not give integer shell labels")
    return np.asarray(rounded, dtype=np.int64)


def minimum_mesh_separation(construction: FloatArray, evaluation: FloatArray) -> float:
    """Return tensor-grid torus separation from sparse one-axis comparisons."""
    dimension = construction.shape[-1]
    squared = 0.0
    for axis in range(dimension):
        construction_index: list[int | slice] = [0] * dimension
        evaluation_index: list[int | slice] = [0] * dimension
        construction_index[axis] = slice(None)
        evaluation_index[axis] = slice(None)
        first = construction[tuple(construction_index)][..., axis]
        second = evaluation[tuple(evaluation_index)][..., axis]
        delta = second[:, None] - first[None, :]
        delta -= np.rint(delta)
        squared += float(np.min(np.abs(delta))) ** 2
    return math.sqrt(squared)


def metric_covariance_defect(geometry: MetricGeometry) -> float:
    """Check one campaign-selected primitive-basis covariance transformation."""
    transform_matrix: IntegerMatrix
    inverse_matrix: IntegerMatrix
    samples: tuple[LatticeIntegerComponents, ...]
    if geometry.dimension == 2:
        dimension = LatticeDimension.TWO
        transform_matrix = ((1, 1), (0, 1))
        inverse_matrix = ((1, -1), (0, 1))
        samples = ((0, 0), (1, 0), (0, 1), (2, -1))
    elif geometry.dimension == 3:
        dimension = LatticeDimension.THREE
        transform_matrix = ((1, 1, 0), (0, 1, 0), (0, 0, 1))
        inverse_matrix = ((1, -1, 0), (0, 1, 0), (0, 0, 1))
        samples = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (1, -1, 2))
    else:
        raise ValueError("only two- and three-dimensional metrics are supported")
    transform = IntegralLatticeOperation(
        identifier="development-primitive-basis-transform",
        dimension=dimension,
        matrix=transform_matrix,
    )
    inverse = IntegralLatticeOperation(
        identifier="development-primitive-basis-inverse",
        dimension=dimension,
        matrix=inverse_matrix,
    )
    transformer = LatticeDisplacementTransformer()
    transformed_samples = tuple(
        transformer.execute(
            inverse,
            LatticeDisplacement(dimension, sample),
        ).components
        for sample in samples
    )
    metric = _direct_metric(geometry).metric_tensor
    transform_array = np.asarray(transform.matrix, dtype=np.float64)
    transformed_metric = transform_array.T @ metric @ transform_array
    sample_array = np.asarray(samples, dtype=np.float64)
    transformed_array = np.asarray(transformed_samples, dtype=np.float64)
    original_values = np.einsum("ri,ij,rj->r", sample_array, metric, sample_array)
    transformed_values = np.einsum(
        "ri,ij,rj->r",
        transformed_array,
        transformed_metric,
        transformed_array,
    )
    return float(np.max(np.abs(original_values - transformed_values)))


def basis_distance_range(
    geometry: MetricGeometry, retained_displacements: IntArray
) -> tuple[float | None, float | None]:
    """Return the min/max PhysKit-mapped basis-pair distances in one support."""
    if not geometry.basis_offsets:
        return None, None
    metric = _direct_metric(geometry)
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
    "basis_distance_range",
    "metric_covariance_defect",
    "metric_indices",
    "minimum_mesh_separation",
]
