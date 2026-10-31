"""Independent direct-formula reference for embedded rank-two truncation."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array
from projectkoios.optimization.alignment.closed_loop_polar_transport import (
    ClosedLoopPolarFrameTransportStatus,
)

from ..parent_scale.independent_reference import (
    _closed_loop_transport,
    _direct_fourier_blocks,
    _independent_gauge_attack,
    _IndependentTransport,
    _IndependentTransportFailure,
    _parent_matrices,
    _representatives,
)
from ..parent_scale.results import (
    Periodic1DRank2BandTransportNumericallyUnresolved,
    Periodic1DRank2BandTransportThresholdFailure,
    Periodic1DRank2ExternalGapFailure,
    Periodic1DRank2QualifiedParent,
)
from .request import Periodic1DRank2TruncationRequest
from .results import (
    Periodic1DRank2TruncationAnalysis,
    Periodic1DRank2TruncationCompleted,
    Periodic1DRank2TruncationPoint,
    Periodic1DRank2TruncationQualificationStopped,
    Periodic1DRank2TruncationRange,
)


@dataclass(frozen=True, slots=True)
class _IndependentPreparation:
    coordinates: Float64Array
    retained_matrices: Complex128Array
    qualification: Periodic1DRank2QualifiedParent


@dataclass(frozen=True, slots=True)
class _IndependentOrdinaryField:
    representatives: tuple[int, ...]
    blocks: Complex128Array
    nyquist_power: float
    maximum_hermiticity_defect: float


@dataclass(frozen=True, slots=True)
class _IndependentErrors:
    hamiltonian_maximum: float
    hamiltonian_rms: float
    spectral_maximum: float
    spectral_rms: float


@dataclass(frozen=True, slots=True)
class _IndependentReferenceRange:
    maximum_range: int
    ordinary_omitted_power: float
    errors: _IndependentErrors


class Periodic1DRank2TruncationIndependentReferenceAnalyzer:
    """Rebuild qualification and truncation without production scientific owners."""

    __slots__ = ("_request",)

    def __init__(self, request: Periodic1DRank2TruncationRequest) -> None:
        if type(request) is not Periodic1DRank2TruncationRequest:
            raise TypeError("request must be a truncation request")
        self._request = request

    def execute(self) -> Periodic1DRank2TruncationAnalysis:
        """Return an independently reconstructed closed truncation outcome."""
        preparation = self._prepare()
        if (
            type(preparation) is (Periodic1DRank2ExternalGapFailure)
            or type(preparation) is (Periodic1DRank2BandTransportNumericallyUnresolved)
            or type(preparation) is (Periodic1DRank2BandTransportThresholdFailure)
        ):
            return Periodic1DRank2TruncationQualificationStopped(
                request=self._request,
                qualification=preparation,
            )
        if type(preparation) is not _IndependentPreparation:
            raise TypeError("independent preparation returned an unknown variant")
        evaluation, offset = self._evaluation_coordinates()
        separation = self._minimum_periodic_separation(
            preparation.coordinates, evaluation
        )
        reference = self._ordinary_field(
            preparation.coordinates, preparation.retained_matrices
        )
        reference_full = self._evaluate(reference, evaluation)
        reference_eigenvalues = self._eigenvalues(reference_full)
        reference_ranges = tuple(
            self._reference_range(
                reference,
                evaluation,
                reference_full,
                reference_eigenvalues,
                maximum_range,
            )
            for maximum_range in self._request.maximum_ranges
        )
        points = tuple(
            self._point(
                preparation.coordinates,
                preparation.retained_matrices,
                evaluation,
                reference,
                reference_full,
                reference_eigenvalues,
                reference_ranges,
                amplitude,
            )
            for amplitude in self._request.template_request.amplitudes
        )
        return Periodic1DRank2TruncationCompleted(
            request=self._request,
            qualification=preparation.qualification,
            evaluation_coordinate_offset=offset,
            minimum_construction_evaluation_separation=separation,
            points=points,
        )

    def _prepare(
        self,
    ) -> (
        _IndependentPreparation
        | Periodic1DRank2ExternalGapFailure
        | Periodic1DRank2BandTransportNumericallyUnresolved
        | Periodic1DRank2BandTransportThresholdFailure
    ):
        request = self._request.template_request
        size = request.reciprocal_mesh_size
        coordinates = np.asarray(
            tuple(-0.5 + float(index) / float(size) for index in range(size)),
            dtype=np.float64,
        )
        parent = _parent_matrices(coordinates, request.parent_hopping_scale)
        eigenvalues, eigenvectors = np.linalg.eigh(parent)
        minimum_gap = float(np.min(eigenvalues[:, 2] - eigenvalues[:, 1]))
        if minimum_gap < request.minimum_external_gap:
            return Periodic1DRank2ExternalGapFailure(minimum_gap)
        transport = _closed_loop_transport(eigenvectors[:, :, :2], request)
        if type(transport) is _IndependentTransportFailure:
            return Periodic1DRank2BandTransportNumericallyUnresolved(
                minimum_external_gap=minimum_gap,
                band_transport_status=(
                    ClosedLoopPolarFrameTransportStatus.RANK_DEFICIENT
                ),
                minimum_transport_singular_value=transport.minimum_singular_value,
            )
        if type(transport) is not _IndependentTransport:
            raise TypeError("independent transport returned an unknown variant")
        if transport.minimum_singular_value <= request.minimum_transport_singular_value:
            return Periodic1DRank2BandTransportThresholdFailure(
                minimum_external_gap=minimum_gap,
                minimum_transport_singular_value=transport.minimum_singular_value,
            )
        frames = transport.frames
        identity = np.eye(2, dtype=np.complex128)
        retained = np.asarray(
            np.swapaxes(frames.conjugate(), -1, -2) @ parent @ frames,
            dtype=np.complex128,
        )
        qualification = Periodic1DRank2QualifiedParent(
            minimum_external_gap=minimum_gap,
            minimum_transport_singular_value=transport.minimum_singular_value,
            maximum_transport_rank_cutoff=transport.maximum_rank_cutoff,
            maximum_transport_unitarity_defect=transport.maximum_unitarity_defect,
            maximum_primitive_link_frobenius_residual=(
                transport.maximum_primitive_link_frobenius_residual
            ),
            closure_holonomy_phases=transport.closure_phases,
            closure_alignment_residual=transport.closure_alignment_residual,
            closure_alignment_unitarity_defect=(
                transport.closure_alignment_unitarity_defect
            ),
            maximum_frame_orthonormality_defect=float(
                max(
                    np.linalg.norm(frame.conj().T @ frame - identity)
                    for frame in frames
                )
            ),
            maximum_reference_hermiticity_defect=float(
                np.max(np.abs(retained - np.swapaxes(retained.conjugate(), -1, -2)))
            ),
        )
        return _IndependentPreparation(
            coordinates=coordinates,
            retained_matrices=retained,
            qualification=qualification,
        )

    def _point(
        self,
        construction_coordinates: Float64Array,
        construction_reference: Complex128Array,
        evaluation_coordinates: Float64Array,
        reference: _IndependentOrdinaryField,
        reference_full: Complex128Array,
        reference_eigenvalues: Float64Array,
        reference_ranges: tuple[_IndependentReferenceRange, ...],
        amplitude: float,
    ) -> Periodic1DRank2TruncationPoint:
        construction_comparison = _independent_gauge_attack(
            construction_coordinates, construction_reference, amplitude
        )
        comparison = self._ordinary_field(
            construction_coordinates, construction_comparison
        )
        comparison_full = self._evaluate(comparison, evaluation_coordinates)
        comparison_eigenvalues = self._eigenvalues(comparison_full)
        direct = _independent_gauge_attack(
            evaluation_coordinates, reference_full, amplitude
        )
        direct_eigenvalues = self._eigenvalues(direct)
        interpolation = self._errors(
            comparison_full,
            direct,
            comparison_eigenvalues,
            direct_eigenvalues,
        )
        return Periodic1DRank2TruncationPoint(
            amplitude=amplitude,
            reference_nyquist_power=reference.nyquist_power,
            comparison_nyquist_power=comparison.nyquist_power,
            reference_ordinary_hermiticity_maximum_defect=(
                reference.maximum_hermiticity_defect
            ),
            comparison_ordinary_hermiticity_maximum_defect=(
                comparison.maximum_hermiticity_defect
            ),
            direct_spectral_maximum_defect=float(
                np.max(np.abs(direct_eigenvalues - reference_eigenvalues))
            ),
            comparison_interpolation_hamiltonian_maximum_error=(
                interpolation.hamiltonian_maximum
            ),
            comparison_interpolation_hamiltonian_rms_error=(
                interpolation.hamiltonian_rms
            ),
            comparison_interpolation_spectral_maximum_error=(
                interpolation.spectral_maximum
            ),
            comparison_interpolation_spectral_rms_error=(interpolation.spectral_rms),
            ranges=tuple(
                self._range(
                    comparison,
                    evaluation_coordinates,
                    comparison_full,
                    comparison_eigenvalues,
                    direct,
                    direct_eigenvalues,
                    reference_range,
                    reference.nyquist_power,
                    comparison.nyquist_power,
                )
                for reference_range in reference_ranges
            ),
        )

    def _reference_range(
        self,
        field: _IndependentOrdinaryField,
        coordinates: Float64Array,
        complete: Complex128Array,
        complete_eigenvalues: Float64Array,
        maximum_range: int,
    ) -> _IndependentReferenceRange:
        truncated, omitted_power = self._truncate(field, maximum_range)
        matrices = self._evaluate(truncated, coordinates)
        eigenvalues = self._eigenvalues(matrices)
        return _IndependentReferenceRange(
            maximum_range=maximum_range,
            ordinary_omitted_power=omitted_power,
            errors=self._errors(matrices, complete, eigenvalues, complete_eigenvalues),
        )

    def _range(
        self,
        field: _IndependentOrdinaryField,
        coordinates: Float64Array,
        complete: Complex128Array,
        complete_eigenvalues: Float64Array,
        direct: Complex128Array,
        direct_eigenvalues: Float64Array,
        reference: _IndependentReferenceRange,
        reference_nyquist_power: float,
        comparison_nyquist_power: float,
    ) -> Periodic1DRank2TruncationRange:
        truncated, omitted_power = self._truncate(field, reference.maximum_range)
        matrices = self._evaluate(truncated, coordinates)
        eigenvalues = self._eigenvalues(matrices)
        truncation = self._errors(matrices, complete, eigenvalues, complete_eigenvalues)
        total = self._errors(matrices, direct, eigenvalues, direct_eigenvalues)
        return Periodic1DRank2TruncationRange(
            maximum_range=reference.maximum_range,
            reference_ordinary_omitted_power=reference.ordinary_omitted_power,
            comparison_ordinary_omitted_power=omitted_power,
            reference_total_omitted_power=(
                reference.ordinary_omitted_power + reference_nyquist_power
            ),
            comparison_total_omitted_power=(omitted_power + comparison_nyquist_power),
            reference_truncation_hamiltonian_maximum_error=(
                reference.errors.hamiltonian_maximum
            ),
            reference_truncation_hamiltonian_rms_error=(
                reference.errors.hamiltonian_rms
            ),
            reference_truncation_spectral_maximum_error=(
                reference.errors.spectral_maximum
            ),
            reference_truncation_spectral_rms_error=(reference.errors.spectral_rms),
            comparison_truncation_hamiltonian_maximum_error=(
                truncation.hamiltonian_maximum
            ),
            comparison_truncation_hamiltonian_rms_error=truncation.hamiltonian_rms,
            comparison_truncation_spectral_maximum_error=truncation.spectral_maximum,
            comparison_truncation_spectral_rms_error=truncation.spectral_rms,
            comparison_total_hamiltonian_maximum_error=total.hamiltonian_maximum,
            comparison_total_hamiltonian_rms_error=total.hamiltonian_rms,
            comparison_total_spectral_maximum_error=total.spectral_maximum,
            comparison_total_spectral_rms_error=total.spectral_rms,
        )

    @staticmethod
    def _ordinary_field(
        coordinates: Float64Array, matrices: Complex128Array
    ) -> _IndependentOrdinaryField:
        representatives = tuple(
            int(value) for value in _representatives(coordinates.size)
        )
        cyclic_blocks = _direct_fourier_blocks(coordinates, matrices)
        nyquist = -(coordinates.size // 2)
        nyquist_index = representatives.index(nyquist)
        ordinary_representatives = tuple(
            value for value in representatives if value != nyquist
        )
        ordinary_blocks = np.asarray(
            [
                block
                for index, block in enumerate(cyclic_blocks)
                if index != nyquist_index
            ],
            dtype=np.complex128,
        )
        block_by_representative = dict(
            zip(ordinary_representatives, ordinary_blocks, strict=True)
        )
        hermiticity = float(
            max(
                np.linalg.norm(
                    block - block_by_representative[-representative].conj().T
                )
                for representative, block in block_by_representative.items()
            )
        )
        return _IndependentOrdinaryField(
            representatives=ordinary_representatives,
            blocks=ordinary_blocks,
            nyquist_power=float(
                np.sum(np.abs(cyclic_blocks[nyquist_index]) ** 2) / 2.0
            ),
            maximum_hermiticity_defect=hermiticity,
        )

    @staticmethod
    def _truncate(
        field: _IndependentOrdinaryField, maximum_range: int
    ) -> tuple[_IndependentOrdinaryField, float]:
        retained = tuple(
            index
            for index, representative in enumerate(field.representatives)
            if abs(representative) <= maximum_range
        )
        omitted = tuple(
            index
            for index, representative in enumerate(field.representatives)
            if abs(representative) > maximum_range
        )
        return (
            _IndependentOrdinaryField(
                representatives=tuple(
                    field.representatives[index] for index in retained
                ),
                blocks=np.asarray(
                    [field.blocks[index] for index in retained],
                    dtype=np.complex128,
                ),
                nyquist_power=field.nyquist_power,
                maximum_hermiticity_defect=field.maximum_hermiticity_defect,
            ),
            float(
                math.fsum(
                    float(np.sum(np.abs(field.blocks[index]) ** 2) / 2.0)
                    for index in omitted
                )
            ),
        )

    @staticmethod
    def _evaluate(
        field: _IndependentOrdinaryField, coordinates: Float64Array
    ) -> Complex128Array:
        phases = np.exp(
            2.0j
            * np.pi
            * np.outer(
                coordinates,
                np.asarray(field.representatives, dtype=np.float64),
            )
        )
        return np.asarray(
            np.einsum("kr,rij->kij", phases, field.blocks, optimize=True),
            dtype=np.complex128,
        )

    @staticmethod
    def _errors(
        candidate: Complex128Array,
        reference: Complex128Array,
        candidate_eigenvalues: Float64Array,
        reference_eigenvalues: Float64Array,
    ) -> _IndependentErrors:
        matrix_difference = candidate - reference
        spectral_difference = candidate_eigenvalues - reference_eigenvalues
        matrix_powers = np.sum(np.abs(matrix_difference) ** 2, axis=(1, 2))
        return _IndependentErrors(
            hamiltonian_maximum=(
                float(np.max(np.sqrt(matrix_powers))) / math.sqrt(2.0)
            ),
            hamiltonian_rms=math.sqrt(float(np.mean(matrix_powers)) / 2.0),
            spectral_maximum=float(np.max(np.abs(spectral_difference))),
            spectral_rms=math.sqrt(float(np.mean(np.square(spectral_difference)))),
        )

    @staticmethod
    def _eigenvalues(matrices: Complex128Array) -> Float64Array:
        return np.asarray(np.linalg.eigvalsh(matrices), dtype=np.float64)

    def _evaluation_coordinates(self) -> tuple[Float64Array, float]:
        construction_size = self._request.template_request.reciprocal_mesh_size
        evaluation_size = self._request.evaluation_mesh_size
        offset = 1.0 / float(construction_size + 1)
        return (
            np.asarray(
                -0.5
                + (np.arange(evaluation_size, dtype=np.float64) + offset)
                / float(evaluation_size),
                dtype=np.float64,
            ),
            offset,
        )

    @staticmethod
    def _minimum_periodic_separation(
        construction: Float64Array, evaluation: Float64Array
    ) -> float:
        differences = np.abs(evaluation[:, None] - construction[None, :])
        return float(np.min(np.minimum(differences, 1.0 - differences)))


__all__ = ["Periodic1DRank2TruncationIndependentReferenceAnalyzer"]
