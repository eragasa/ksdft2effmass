"""Gauge-invariant bound-subspace projectors and localization diagnostics."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.solid_state import FiniteLatticeCoordinateResolver

from .finite_domain_locality import MinimumImageChebyshevPartition
from .finite_domain_spectra import HostEdgeBoundStateResult

type LocalizationRadii = tuple[float] | tuple[float, float] | tuple[float, float, float]
"""Closed one-, two-, or three-dimensional RMS-radius representation."""


@dataclass(frozen=True, slots=True)
class BoundStateProjectorResult:
    """Retain a complete bound-subspace projector or explicit no-bound-state outcome."""

    bound_states: HostEdgeBoundStateResult
    projector: ComplexMatrixQuantity | None

    def __post_init__(self) -> None:
        """Validate complete coverage and projector rank, shape, and algebra."""
        if type(self.bound_states) is not HostEdgeBoundStateResult:
            raise TypeError("bound_states must be HostEdgeBoundStateResult")
        if not self.bound_states.count_is_complete:
            raise ValueError("bound-state spectral coverage must be complete")
        rank = self.bound_states.below_edge_state_count
        if rank == 0:
            if self.projector is not None:
                raise ValueError("no-bound-state result must not retain a projector")
            return
        if type(self.projector) is not ComplexMatrixQuantity:
            raise TypeError("projector must be ComplexMatrixQuantity for nonzero rank")
        if type(self.projector.unit) is not Unitless:
            raise ValueError("bound-state projector must be unitless")
        dimension = self.bound_states.eigenpairs.full_dimension
        if self.projector.magnitude.shape != (dimension, dimension):
            raise ValueError("projector shape must match the represented dimension")
        represented = self.projector.magnitude
        tolerance = 256.0 * np.finfo(np.float64).eps * float(max(1, dimension))
        if not np.allclose(
            represented,
            represented.conjugate().T,
            rtol=0.0,
            atol=tolerance,
        ):
            raise ValueError("bound-state projector must be Hermitian")
        if not np.allclose(
            represented @ represented,
            represented,
            rtol=0.0,
            atol=tolerance,
        ):
            raise ValueError("bound-state projector must be idempotent")
        trace = np.trace(represented)
        if abs(trace.imag) > tolerance or abs(trace.real - float(rank)) > tolerance:
            raise ValueError("bound-state projector trace must equal bound-state rank")

    @property
    def rank(self) -> int:
        """Return the complete below-edge subspace rank."""
        return self.bound_states.below_edge_state_count

    @property
    def available(self) -> bool:
        """Return whether a nonempty bound subspace is available."""
        return self.projector is not None


class BoundStateProjectorConstructor:
    """Construct a gauge-invariant projector from a complete bound-state selection."""

    __slots__ = ()

    def execute(
        self, bound_states: HostEdgeBoundStateResult
    ) -> BoundStateProjectorResult:
        """Return the bound projector, or ``None`` for a complete empty selection."""
        if type(bound_states) is not HostEdgeBoundStateResult:
            raise TypeError("bound_states must be HostEdgeBoundStateResult")
        if not bound_states.count_is_complete:
            raise ValueError("bound-state spectral coverage must be complete")
        if not bound_states.selected_indices:
            return BoundStateProjectorResult(bound_states, None)
        indices = np.asarray(bound_states.selected_indices, dtype=np.int64)
        vectors = bound_states.eigenpairs.eigenvectors.magnitude[:, indices]
        projector = vectors @ vectors.conjugate().T
        return BoundStateProjectorResult(
            bound_states, ComplexMatrixQuantity(projector, Unitless())
        )


@dataclass(frozen=True, slots=True)
class BoundSubspaceLocalizationResult:
    """Retain gauge-invariant localization metrics for one complete bound subspace."""

    projector_result: BoundStateProjectorResult
    partition: MinimumImageChebyshevPartition
    site_probabilities: VectorQuantity | None
    core_probability: float | None
    inverse_participation_ratio: float | None
    rms_radii: LocalizationRadii | None

    def __post_init__(self) -> None:
        """Validate availability, dimensions, probabilities, and scalar domains."""
        if type(self.projector_result) is not BoundStateProjectorResult:
            raise TypeError("projector_result must be BoundStateProjectorResult")
        if type(self.partition) is not MinimumImageChebyshevPartition:
            raise TypeError("partition must be MinimumImageChebyshevPartition")
        dimension = self.projector_result.bound_states.eigenpairs.full_dimension
        if self.partition.shape.cell_count != dimension:
            raise ValueError("partition size must match the represented dimension")
        metrics = (
            self.site_probabilities,
            self.core_probability,
            self.inverse_participation_ratio,
            self.rms_radii,
        )
        if not self.projector_result.available:
            if any(value is not None for value in metrics):
                raise ValueError(
                    "no-bound-state localization metrics must be unavailable"
                )
            return
        if type(self.site_probabilities) is not VectorQuantity:
            raise TypeError("site_probabilities must be VectorQuantity")
        if type(self.site_probabilities.unit) is not Unitless:
            raise ValueError("site probabilities must be unitless")
        probabilities = self.site_probabilities.magnitude
        if probabilities.shape != (dimension,):
            raise ValueError("site probabilities must match represented dimension")
        if np.any(probabilities < 0.0):
            raise ValueError("site probabilities must be nonnegative")
        tolerance = 256.0 * np.finfo(np.float64).eps * float(max(1, dimension))
        if abs(float(np.sum(probabilities)) - 1.0) > tolerance:
            raise ValueError("site probabilities must sum to one")
        if type(self.core_probability) is not float:
            raise TypeError("core_probability must be a built-in float")
        if (
            not math.isfinite(self.core_probability)
            or not 0.0 <= self.core_probability <= 1.0
        ):
            raise ValueError("core_probability must be finite and lie in [0, 1]")
        expected_core = float(
            np.sum(
                probabilities[np.asarray(self.partition.core_indices, dtype=np.int64)]
            )
        )
        if abs(self.core_probability - expected_core) > tolerance:
            raise ValueError("core_probability must agree with the locality partition")
        if type(self.inverse_participation_ratio) is not float:
            raise TypeError("inverse_participation_ratio must be a built-in float")
        expected_ipr = float(np.sum(probabilities * probabilities))
        if abs(self.inverse_participation_ratio - expected_ipr) > tolerance:
            raise ValueError(
                "inverse_participation_ratio must agree with probabilities"
            )
        if (
            type(self.rms_radii) is not tuple
            or len(self.rms_radii) != self.partition.shape.dimension.value
        ):
            raise TypeError("rms_radii must be a tuple matching the spatial dimension")
        if any(type(value) is not float for value in self.rms_radii):
            raise TypeError("RMS radii must be built-in floats")
        if any(not math.isfinite(value) or value < 0.0 for value in self.rms_radii):
            raise ValueError("RMS radii must be finite and nonnegative")

    @property
    def available(self) -> bool:
        """Return whether localization metrics exist for a nonempty bound subspace."""
        return self.site_probabilities is not None


class BoundSubspaceLocalizationAnalyzer:
    """Evaluate density, core probability, IPR, and lattice-coordinate RMS radii."""

    __slots__ = ()

    def execute(
        self,
        projector_result: BoundStateProjectorResult,
        partition: MinimumImageChebyshevPartition,
    ) -> BoundSubspaceLocalizationResult:
        """Return metrics, or explicit unavailable values for no bound state."""
        if type(projector_result) is not BoundStateProjectorResult:
            raise TypeError("projector_result must be BoundStateProjectorResult")
        if type(partition) is not MinimumImageChebyshevPartition:
            raise TypeError("partition must be MinimumImageChebyshevPartition")
        dimension = projector_result.bound_states.eigenpairs.full_dimension
        if partition.shape.cell_count != dimension:
            raise ValueError("partition size must match the represented dimension")
        if not projector_result.available:
            return BoundSubspaceLocalizationResult(
                projector_result, partition, None, None, None, None
            )
        selected = np.asarray(
            projector_result.bound_states.selected_indices, dtype=np.int64
        )
        vectors = projector_result.bound_states.eigenpairs.eigenvectors.magnitude[
            :, selected
        ]
        probabilities = np.sum(np.abs(vectors) ** 2, axis=1) / float(
            projector_result.rank
        )
        core_probability = float(
            np.sum(probabilities[np.asarray(partition.core_indices, dtype=np.int64)])
        )
        inverse_participation_ratio = float(np.sum(probabilities * probabilities))
        resolver = FiniteLatticeCoordinateResolver()
        second_moments: list[float] = []
        for axis in range(partition.shape.dimension.value):
            squared_distances: list[float] = []
            for index in range(partition.shape.cell_count):
                coordinate = resolver.execute(partition.shape, index)
                forward = (
                    coordinate.components[axis] - partition.origin.components[axis]
                ) % partition.shape.extents[axis]
                backward = (
                    partition.origin.components[axis] - coordinate.components[axis]
                ) % partition.shape.extents[axis]
                distance = min(forward, backward)
                squared_distances.append(float(distance * distance))
            second_moments.append(
                float(
                    np.dot(
                        probabilities,
                        np.asarray(squared_distances, dtype=np.float64),
                    )
                )
            )
        radii_values = tuple(math.sqrt(value) for value in second_moments)
        if partition.shape.dimension.value == 1:
            rms_radii: LocalizationRadii = (radii_values[0],)
        elif partition.shape.dimension.value == 2:
            rms_radii = (radii_values[0], radii_values[1])
        else:
            rms_radii = (radii_values[0], radii_values[1], radii_values[2])
        return BoundSubspaceLocalizationResult(
            projector_result,
            partition,
            VectorQuantity(probabilities, Unitless()),
            core_probability,
            inverse_participation_ratio,
            rms_radii,
        )
