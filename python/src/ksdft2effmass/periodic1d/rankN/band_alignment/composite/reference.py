"""Producer-independent reference analysis for analytic model core invariants.

This bounded slice reconstructs the protocol's analytic parent, constant retained frame,
real Givens attack, and model-structure diagnostics with direct NumPy formulas. It does
not call the calculation producer, its model owner, diagnostic actions, transport,
Procrustes, Fourier, interpolation, locality, or refinement actions.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

import numpy as np
from projectkoios.physkit.units import ScalarQuantity, Unitless, VectorQuantity

from ksdft2effmass.verification import MaximumAbsoluteErrorComparison

from .calculation_result import Periodic1DRankNAlignmentCalculationResult


@dataclass(frozen=True, slots=True)
class Periodic1DRankNCoreInvariantReference:
    """Retain independently reconstructed core-invariant comparisons.

    This record is intentionally narrower than the complete direct-formula verifier
    selected by the protocol. It covers the analytic model and attack invariants only.
    """

    comparisons: Mapping[str, MaximumAbsoluteErrorComparison]

    def __post_init__(self) -> None:
        """Copy and freeze one nonempty collision-free comparison inventory."""
        if not isinstance(self.comparisons, Mapping) or not self.comparisons:
            raise TypeError("comparisons must be a nonempty mapping")
        if any(
            type(name) is not str
            or not name
            or not isinstance(value, MaximumAbsoluteErrorComparison)
            for name, value in self.comparisons.items()
        ):
            raise TypeError("comparisons must contain named comparison values")
        object.__setattr__(
            self,
            "comparisons",
            MappingProxyType(dict(self.comparisons)),
        )


@dataclass(frozen=True, slots=True)
class Periodic1DRankNCoreInvariantReferenceRequest:
    """Bind one exact producer result as the reference-analysis subject."""

    result: Periodic1DRankNAlignmentCalculationResult

    def __post_init__(self) -> None:
        """Admit only the exact higher-rank calculation-result type."""
        if type(self.result) is not Periodic1DRankNAlignmentCalculationResult:
            raise TypeError("result must be Periodic1DRankNAlignmentCalculationResult")


@dataclass(frozen=True, slots=True)
class _ModelCoreInvariantValues:
    exact_analytic_isolation_gap: float
    sampled_isolation_gaps: np.ndarray
    exact_analytic_attack_angle_maximum: float
    sampled_attack_angle_maxima: np.ndarray
    parent_hermiticity_defect: float
    reference_frame_isometry_defect: float
    gauge_unitarity_defect: float
    attacked_frame_isometry_defect: float
    attacked_projector_equality_defect: float
    reference_projector_hermiticity_defect: float
    reference_projector_idempotency_defect: float
    reference_operator_recovery_defect: float
    reference_spectrum_recovery_defect: float
    attacked_operator_recovery_defect: float
    attacked_spectrum_recovery_defect: float
    oracle_frame_recovery_defect: float
    oracle_operator_recovery_defect: float


class Periodic1DRankNCoreInvariantReferenceAnalyzer:
    """Independently reconstruct the analytic model's core invariant diagnostics."""

    __slots__ = ("_request",)

    NORMALIZED_SCALAR_TOLERANCE = 1.0e-11
    ARRAY_TOLERANCE = 1.0e-10

    def __init__(
        self,
        request: Periodic1DRankNCoreInvariantReferenceRequest,
    ) -> None:
        if type(request) is not Periodic1DRankNCoreInvariantReferenceRequest:
            raise TypeError(
                "request must be Periodic1DRankNCoreInvariantReferenceRequest"
            )
        self._request = request

    @property
    def request(self) -> Periodic1DRankNCoreInvariantReferenceRequest:
        """Return the complete immutable reference-analysis request."""
        return self._request

    def execute(self) -> Periodic1DRankNCoreInvariantReference:
        """Return direct-formula comparisons for every construction mesh."""
        result = self.request.result
        request = result.request
        common_sampled_gaps = self._sampled_isolation_gaps()
        common_sampled_angles = self._sampled_attack_angle_maxima()
        comparisons: dict[str, MaximumAbsoluteErrorComparison] = {}
        for mesh in result.meshes:
            expected = self._mesh_reference(
                mesh.construction_mesh_size,
                common_sampled_gaps,
                common_sampled_angles,
            )
            observed = mesh.model_diagnostics
            prefix = f"mesh_{mesh.construction_mesh_size}"
            self._add_scalar(
                comparisons,
                f"{prefix}_exact_analytic_isolation_gap",
                observed.exact_analytic_isolation_gap,
                expected.exact_analytic_isolation_gap,
            )
            self._add_vector(
                comparisons,
                f"{prefix}_sampled_isolation_gaps",
                observed.sampled_isolation_gaps,
                expected.sampled_isolation_gaps,
            )
            self._add_scalar(
                comparisons,
                f"{prefix}_exact_analytic_attack_angle_maximum",
                observed.exact_analytic_attack_angle_maximum,
                expected.exact_analytic_attack_angle_maximum,
            )
            self._add_vector(
                comparisons,
                f"{prefix}_sampled_attack_angle_maxima",
                observed.sampled_attack_angle_maxima,
                expected.sampled_attack_angle_maxima,
            )
            scalar_values = (
                (
                    "parent_hermiticity_defect",
                    observed.parent_hermiticity_defect,
                    expected.parent_hermiticity_defect,
                ),
                (
                    "reference_frame_isometry_defect",
                    observed.reference_frame_isometry_defect,
                    expected.reference_frame_isometry_defect,
                ),
                (
                    "gauge_unitarity_defect",
                    observed.gauge_unitarity_defect,
                    expected.gauge_unitarity_defect,
                ),
                (
                    "attacked_frame_isometry_defect",
                    observed.attacked_frame_isometry_defect,
                    expected.attacked_frame_isometry_defect,
                ),
                (
                    "attacked_projector_equality_defect",
                    observed.attacked_projector_equality_defect,
                    expected.attacked_projector_equality_defect,
                ),
                (
                    "reference_projector_hermiticity_defect",
                    observed.reference_projector_hermiticity_defect,
                    expected.reference_projector_hermiticity_defect,
                ),
                (
                    "reference_projector_idempotency_defect",
                    observed.reference_projector_idempotency_defect,
                    expected.reference_projector_idempotency_defect,
                ),
                (
                    "reference_operator_recovery_defect",
                    observed.reference_operator_recovery_defect,
                    expected.reference_operator_recovery_defect,
                ),
                (
                    "reference_spectrum_recovery_defect",
                    observed.reference_spectrum_recovery_defect,
                    expected.reference_spectrum_recovery_defect,
                ),
                (
                    "attacked_operator_recovery_defect",
                    observed.attacked_operator_recovery_defect,
                    expected.attacked_operator_recovery_defect,
                ),
                (
                    "attacked_spectrum_recovery_defect",
                    observed.attacked_spectrum_recovery_defect,
                    expected.attacked_spectrum_recovery_defect,
                ),
                (
                    "oracle_frame_recovery_defect",
                    observed.oracle_frame_recovery_defect,
                    expected.oracle_frame_recovery_defect,
                ),
                (
                    "oracle_operator_recovery_defect",
                    observed.oracle_operator_recovery_defect,
                    expected.oracle_operator_recovery_defect,
                ),
            )
            for name, observed_value, expected_value in scalar_values:
                self._add_scalar(
                    comparisons,
                    f"{prefix}_{name}",
                    observed_value,
                    expected_value,
                )
        if tuple(mesh.construction_mesh_size for mesh in result.meshes) != (
            request.configuration.construction_mesh_sizes
        ):
            raise ValueError("result mesh inventory changed after result admission")
        return Periodic1DRankNCoreInvariantReference(comparisons)

    def _sampled_isolation_gaps(self) -> np.ndarray:
        values = []
        mesh_sizes = self.request.result.request.configuration.construction_mesh_sizes
        for mesh_size in mesh_sizes:
            coordinates = self._coordinates(mesh_size)
            retained, exterior = self._energies(coordinates)
            values.append(
                float(np.min(np.min(exterior, axis=1) - np.max(retained, axis=1)))
            )
        return np.asarray(values, dtype=np.float64)

    def _sampled_attack_angle_maxima(self) -> np.ndarray:
        request = self.request.result.request
        values = []
        for mesh_size in request.configuration.construction_mesh_sizes:
            coordinates = self._coordinates(mesh_size)
            k = 2.0 * np.pi * coordinates
            maximum = 0.0
            for layer_index in range(1, request.circuit_depth + 1):
                harmonic = 0.75 * np.sin(k) + 0.25 * ((-1.0) ** layer_index) * np.sin(
                    2.0 * k
                )
                for pair_index in range(1, request.retained_rank):
                    normalized_pair = (2.0 * pair_index - request.retained_rank) / (
                        request.retained_rank - 1.0
                    )
                    angles = (
                        0.35
                        * (-1.0) ** (layer_index + pair_index)
                        * (1.0 + 0.15 * normalized_pair)
                        * harmonic
                    )
                    maximum = max(maximum, float(np.max(np.abs(angles))))
            values.append(maximum)
        return np.asarray(values, dtype=np.float64)

    def _mesh_reference(
        self,
        mesh_size: int,
        sampled_isolation_gaps: np.ndarray,
        sampled_attack_angle_maxima: np.ndarray,
    ) -> _ModelCoreInvariantValues:
        request = self.request.result.request
        rank = request.retained_rank
        ambient = 2 * rank
        energy_reference = request.controls.energy_reference
        coordinates = self._coordinates(mesh_size)
        retained, exterior = self._energies(coordinates)
        diagonal = np.concatenate((retained, exterior), axis=1)
        parent = np.asarray(
            diagonal[:, :, None] * np.eye(ambient, dtype=np.complex128)[None, :, :],
            dtype=np.complex128,
        )
        exact = np.asarray(
            retained[:, :, None] * np.eye(rank, dtype=np.complex128)[None, :, :],
            dtype=np.complex128,
        )
        reference_seed = np.zeros((ambient, rank), dtype=np.complex128)
        reference_seed[:rank] = np.eye(rank, dtype=np.complex128)
        reference_frames = np.broadcast_to(
            reference_seed,
            (mesh_size, ambient, rank),
        ).copy()
        gauge = self._gauge_unitaries(coordinates)
        attacked_frames = np.asarray(reference_frames @ gauge, dtype=np.complex128)
        attacked = np.asarray(
            self._adjoint(gauge) @ exact @ gauge,
            dtype=np.complex128,
        )
        reference_recovered = np.asarray(
            self._adjoint(reference_frames) @ parent @ reference_frames,
            dtype=np.complex128,
        )
        attacked_recovered = np.asarray(
            self._adjoint(attacked_frames) @ parent @ attacked_frames,
            dtype=np.complex128,
        )
        reference_projectors = np.asarray(
            reference_frames @ self._adjoint(reference_frames),
            dtype=np.complex128,
        )
        attacked_projectors = np.asarray(
            attacked_frames @ self._adjoint(attacked_frames),
            dtype=np.complex128,
        )
        inverse_gauge = self._adjoint(gauge)
        oracle_frames = np.asarray(
            attacked_frames @ inverse_gauge,
            dtype=np.complex128,
        )
        oracle_operator = np.asarray(
            gauge @ attacked @ inverse_gauge,
            dtype=np.complex128,
        )
        q = (math.sqrt(41.0) - 3.0) / 8.0
        harmonic_maximum = math.sqrt(1.0 - q**2) * (0.75 + 0.5 * q)
        exact_angle = (
            0.35 * (1.0 + 0.15 * (rank - 2.0) / (rank - 1.0)) * harmonic_maximum
        )
        return _ModelCoreInvariantValues(
            exact_analytic_isolation_gap=2.1,
            sampled_isolation_gaps=sampled_isolation_gaps,
            exact_analytic_attack_angle_maximum=float(exact_angle),
            sampled_attack_angle_maxima=sampled_attack_angle_maxima,
            parent_hermiticity_defect=self._normalized_hermiticity_defect(
                parent,
                ambient,
                energy_reference,
            ),
            reference_frame_isometry_defect=self._normalized_isometry_defect(
                reference_frames,
                rank,
            ),
            gauge_unitarity_defect=self._normalized_isometry_defect(gauge, rank),
            attacked_frame_isometry_defect=self._normalized_isometry_defect(
                attacked_frames,
                rank,
            ),
            attacked_projector_equality_defect=self._maximum_frobenius_defect(
                attacked_projectors,
                reference_projectors,
            ),
            reference_projector_hermiticity_defect=(
                self._normalized_hermiticity_defect(
                    reference_projectors,
                    ambient,
                    1.0,
                )
            ),
            reference_projector_idempotency_defect=(
                self._maximum_frobenius_defect(
                    reference_projectors @ reference_projectors,
                    reference_projectors,
                )
                / math.sqrt(ambient)
            ),
            reference_operator_recovery_defect=self._normalized_matrix_defect(
                reference_recovered,
                exact,
                rank,
                energy_reference,
            ),
            reference_spectrum_recovery_defect=self._normalized_spectrum_defect(
                reference_recovered,
                exact,
                energy_reference,
            ),
            attacked_operator_recovery_defect=self._normalized_matrix_defect(
                attacked_recovered,
                attacked,
                rank,
                energy_reference,
            ),
            attacked_spectrum_recovery_defect=self._normalized_spectrum_defect(
                attacked,
                exact,
                energy_reference,
            ),
            oracle_frame_recovery_defect=(
                self._maximum_frobenius_defect(oracle_frames, reference_frames)
                / math.sqrt(rank)
            ),
            oracle_operator_recovery_defect=self._normalized_matrix_defect(
                oracle_operator,
                exact,
                rank,
                energy_reference,
            ),
        )

    def _energies(self, coordinates: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        rank = self.request.result.request.retained_rank
        k = 2.0 * np.pi * coordinates
        harmonic = 0.75 * np.cos(k) + 0.25 * np.cos(2.0 * k)
        orbital = np.arange(rank, dtype=np.float64)
        normalized_orbital = (2.0 * orbital - rank + 1.0) / (rank - 1.0)
        retained = (
            0.4 * normalized_orbital[None, :]
            + 0.25 * (1.0 + 0.2 * normalized_orbital[None, :]) * harmonic[:, None]
        )
        exterior = 3.0 + 0.3 * normalized_orbital[None, :] + 0.1 * harmonic[:, None]
        return (
            np.asarray(retained, dtype=np.float64),
            np.asarray(exterior, dtype=np.float64),
        )

    def _gauge_unitaries(self, coordinates: np.ndarray) -> np.ndarray:
        request = self.request.result.request
        rank = request.retained_rank
        k = 2.0 * np.pi * coordinates
        gauges = np.broadcast_to(
            np.eye(rank, dtype=np.complex128),
            (coordinates.size, rank, rank),
        ).copy()
        for layer_index in range(1, request.circuit_depth + 1):
            harmonic = 0.75 * np.sin(k) + 0.25 * ((-1.0) ** layer_index) * np.sin(
                2.0 * k
            )
            layer = np.broadcast_to(
                np.eye(rank, dtype=np.complex128),
                (coordinates.size, rank, rank),
            ).copy()
            first_index = 0 if layer_index % 2 == 1 else 1
            for left in range(first_index, rank - 1, 2):
                pair_index = left + 1
                normalized_pair = (2.0 * pair_index - rank) / (rank - 1.0)
                angle = (
                    0.35
                    * (-1.0) ** (layer_index + pair_index)
                    * (1.0 + 0.15 * normalized_pair)
                    * harmonic
                )
                cosine = np.cos(angle)
                sine = np.sin(angle)
                layer[:, left, left] = cosine
                layer[:, left, left + 1] = -sine
                layer[:, left + 1, left] = sine
                layer[:, left + 1, left + 1] = cosine
            gauges = gauges @ layer
        return np.asarray(gauges, dtype=np.complex128)

    def _coordinates(self, mesh_size: int) -> np.ndarray:
        return np.asarray(
            -0.5 + np.arange(mesh_size, dtype=np.float64) / mesh_size,
            dtype=np.float64,
        )

    def _adjoint(self, values: np.ndarray) -> np.ndarray:
        return np.swapaxes(values.conjugate(), -1, -2)

    def _maximum_frobenius_defect(
        self,
        left: np.ndarray,
        right: np.ndarray,
    ) -> float:
        return float(np.max(np.linalg.norm(left - right, axis=(-2, -1))))

    def _normalized_hermiticity_defect(
        self,
        matrices: np.ndarray,
        matrix_size: int,
        energy_reference: float,
    ) -> float:
        return self._maximum_frobenius_defect(
            matrices,
            self._adjoint(matrices),
        ) / (math.sqrt(matrix_size) * energy_reference)

    def _normalized_isometry_defect(
        self,
        frames: np.ndarray,
        rank: int,
    ) -> float:
        gram = self._adjoint(frames) @ frames
        identity = np.eye(rank, dtype=np.complex128)
        return self._maximum_frobenius_defect(gram, identity) / math.sqrt(rank)

    def _normalized_matrix_defect(
        self,
        approximation: np.ndarray,
        reference: np.ndarray,
        rank: int,
        energy_reference: float,
    ) -> float:
        return self._maximum_frobenius_defect(
            approximation,
            reference,
        ) / (math.sqrt(rank) * energy_reference)

    def _normalized_spectrum_defect(
        self,
        approximation: np.ndarray,
        reference: np.ndarray,
        energy_reference: float,
    ) -> float:
        difference = np.abs(
            np.linalg.eigvalsh(approximation) - np.linalg.eigvalsh(reference)
        )
        return float(np.max(difference)) / energy_reference

    def _add_scalar(
        self,
        comparisons: dict[str, MaximumAbsoluteErrorComparison],
        name: str,
        observed: float,
        reference: float,
    ) -> None:
        unit = Unitless()
        comparisons[name] = MaximumAbsoluteErrorComparison(
            observed=ScalarQuantity(observed, unit),
            reference=ScalarQuantity(reference, unit),
            tolerance=ScalarQuantity(self.NORMALIZED_SCALAR_TOLERANCE, unit),
        )

    def _add_vector(
        self,
        comparisons: dict[str, MaximumAbsoluteErrorComparison],
        name: str,
        observed: np.ndarray,
        reference: np.ndarray,
    ) -> None:
        unit = Unitless()
        comparisons[name] = MaximumAbsoluteErrorComparison(
            observed=VectorQuantity(observed, unit),
            reference=VectorQuantity(reference, unit),
            tolerance=ScalarQuantity(self.ARRAY_TOLERANCE, unit),
        )


__all__ = [
    "Periodic1DRankNCoreInvariantReference",
    "Periodic1DRankNCoreInvariantReferenceAnalyzer",
    "Periodic1DRankNCoreInvariantReferenceRequest",
]
