"""Producer-independent numerical reconstruction for composite-band alignment."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    ComplexVectorQuantity,
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from scipy.linalg import schur  # type: ignore[import-untyped]

from ksdft2effmass.verification import MaximumAbsoluteErrorComparison

from .result import Periodic1DCompositeBandAlignmentCalculationResult
from .visualizations.data import (
    Periodic1DCompositeBandAlignmentVisualizationData,
)


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeBandAlignmentIndependentReference:
    """Retain collision-free independently reconstructed comparisons."""

    comparisons: Mapping[str, MaximumAbsoluteErrorComparison]

    def __post_init__(self) -> None:
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
class _CompositeReferenceValues:
    construction_spectrum: Float64Array
    evaluation_spectrum: Float64Array
    reference_frames: Complex128Array
    attacked_frames: Complex128Array
    pointwise_frames: Complex128Array
    global_frames: Complex128Array
    pointwise_rotations: Complex128Array
    global_rotation: Complex128Array
    reference_operators: Complex128Array
    attacked_operators: Complex128Array
    pointwise_operators: Complex128Array
    global_operators: Complex128Array
    representatives: tuple[int, ...]
    hopping_blocks: Complex128Array
    reconstruction_errors: Float64Array
    hermiticity_errors: Float64Array
    cyclic_conversion_powers: Float64Array
    interpolation_error_values: Float64Array
    range_values: Float64Array
    diagnostic_values: Float64Array
    closure_eigenphases: Float64Array


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeBandAlignmentIndependentReferenceRequest:
    """Bind the admitted rank-two result and verifier-derived projection."""

    result: Periodic1DCompositeBandAlignmentCalculationResult
    visualization_data: Periodic1DCompositeBandAlignmentVisualizationData

    def __post_init__(self) -> None:
        """Admit exact composite-alignment verification subject types."""
        if type(self.result) is not Periodic1DCompositeBandAlignmentCalculationResult:
            raise TypeError(
                "result must be Periodic1DCompositeBandAlignmentCalculationResult"
            )
        if type(self.visualization_data) is not (
            Periodic1DCompositeBandAlignmentVisualizationData
        ):
            raise TypeError("visualization_data has the wrong exact type")


class Periodic1DCompositeBandAlignmentIndependentReferenceAnalyzer:
    """Reconstruct one bound rank-two result with direct NumPy formulas."""

    __slots__ = ("_request",)

    DIAGNOSTIC_NAMES = (
        "minimum_sampled_gap",
        "minimum_overlap_singular_value",
        "attack_frame_maximum_frobenius_defect",
        "pointwise_frame_maximum_frobenius_defect",
        "pointwise_projector_maximum_frobenius_defect",
        "pointwise_rotation_recovery_maximum_frobenius_defect",
        "global_frame_maximum_frobenius_defect",
        "attacked_operator_maximum_frobenius_defect",
        "pointwise_operator_maximum_frobenius_defect",
        "global_operator_maximum_frobenius_defect",
        "pointwise_minimum_cross_singular_value",
        "global_minimum_cross_singular_value",
        "pointwise_maximum_rank_cutoff",
        "global_rank_cutoff",
    )

    def __init__(
        self, request: Periodic1DCompositeBandAlignmentIndependentReferenceRequest
    ) -> None:
        if (
            type(request)
            is not Periodic1DCompositeBandAlignmentIndependentReferenceRequest
        ):
            raise TypeError(
                "request must be "
                "Periodic1DCompositeBandAlignmentIndependentReferenceRequest"
            )
        self._request = request

    @property
    def request(self) -> Periodic1DCompositeBandAlignmentIndependentReferenceRequest:
        """Return the complete immutable independent-reference request."""
        return self._request

    def execute(self) -> Periodic1DCompositeBandAlignmentIndependentReference:
        """Return independent comparisons for the bound result and projection."""
        result = self.request.result
        configuration = result.configuration
        expected = self._reference()
        unit = Unitless()
        comparisons: dict[str, MaximumAbsoluteErrorComparison] = {}
        self._add(
            comparisons,
            "construction_reduced_momenta",
            VectorQuantity(
                np.asarray(result.construction_reduced_momenta, dtype=np.float64),
                unit,
            ),
            VectorQuantity(
                np.asarray(
                    configuration.construction_reduced_momenta(), dtype=np.float64
                ),
                unit,
            ),
            0.0,
        )
        self._add(
            comparisons,
            "evaluation_reduced_momenta",
            VectorQuantity(
                np.asarray(result.evaluation_reduced_momenta, dtype=np.float64),
                unit,
            ),
            VectorQuantity(
                np.asarray(
                    configuration.evaluation_reduced_momenta(), dtype=np.float64
                ),
                unit,
            ),
            0.0,
        )
        self._add(
            comparisons,
            "construction_parent_spectrum",
            result.construction_parent_spectrum,
            MatrixQuantity(expected.construction_spectrum, unit),
            configuration.energy_absolute_tolerance,
        )
        self._add(
            comparisons,
            "evaluation_parent_spectrum",
            result.evaluation_parent_spectrum,
            MatrixQuantity(expected.evaluation_spectrum, unit),
            configuration.energy_absolute_tolerance,
        )
        frame_fields = (
            ("reference_frames", result.reference_frames, expected.reference_frames),
            ("attacked_frames", result.attacked_frames, expected.attacked_frames),
            (
                "pointwise_aligned_frames",
                result.pointwise_aligned_frames,
                expected.pointwise_frames,
            ),
            (
                "globally_aligned_frames",
                result.globally_aligned_frames,
                expected.global_frames,
            ),
            (
                "pointwise_rotations",
                result.pointwise_rotations,
                expected.pointwise_rotations,
            ),
        )
        for name, observed, reference in frame_fields:
            self._add(
                comparisons,
                name,
                self._complex_inventory(observed),
                ComplexVectorQuantity(reference.reshape(-1), unit),
                configuration.dimensionless_absolute_tolerance * 10.0,
            )
        self._add(
            comparisons,
            "global_rotation",
            result.global_rotation,
            ComplexMatrixQuantity(expected.global_rotation, unit),
            configuration.dimensionless_absolute_tolerance * 10.0,
        )
        operator_fields = (
            (
                "reference_operators",
                result.reference_operators,
                expected.reference_operators,
            ),
            (
                "attacked_operators",
                result.attacked_operators,
                expected.attacked_operators,
            ),
            (
                "pointwise_aligned_operators",
                result.pointwise_aligned_operators,
                expected.pointwise_operators,
            ),
            (
                "globally_aligned_operators",
                result.globally_aligned_operators,
                expected.global_operators,
            ),
        )
        for name, observed, reference in operator_fields:
            self._add(
                comparisons,
                name,
                self._complex_inventory(observed),
                ComplexVectorQuantity(reference.reshape(-1), unit),
                configuration.energy_absolute_tolerance,
            )
        for index, transform in enumerate(result.transforms):
            prefix = f"transform_{transform.channel}"
            representatives_match = (
                transform.representatives == expected.representatives
            )
            self._add(
                comparisons,
                f"{prefix}_representatives",
                ScalarQuantity(0.0 if representatives_match else 1.0, unit),
                ScalarQuantity(0.0, unit),
                0.0,
            )
            self._add(
                comparisons,
                f"{prefix}_hopping_blocks",
                self._complex_inventory(transform.hopping_blocks),
                ComplexVectorQuantity(expected.hopping_blocks[index].reshape(-1), unit),
                configuration.energy_absolute_tolerance,
            )
            ordinary_match = transform.ordinary_representatives == tuple(
                representative
                for representative in expected.representatives
                if representative != expected.representatives[0]
            )
            self._add(
                comparisons,
                f"{prefix}_ordinary_representatives",
                ScalarQuantity(0.0 if ordinary_match else 1.0, unit),
                ScalarQuantity(0.0, unit),
                0.0,
            )
            conversion_representative_match = (
                transform.cyclic_conversion_representative
                == expected.representatives[0]
            )
            self._add(
                comparisons,
                f"{prefix}_cyclic_conversion_representative",
                ScalarQuantity(
                    0.0 if conversion_representative_match else 1.0,
                    unit,
                ),
                ScalarQuantity(0.0, unit),
                0.0,
            )
            self._add(
                comparisons,
                f"{prefix}_cyclic_conversion_power",
                transform.cyclic_conversion_power,
                ScalarQuantity(float(expected.cyclic_conversion_powers[index]), unit),
                configuration.energy_absolute_tolerance,
            )
            self._add(
                comparisons,
                f"{prefix}_reconstruction_error",
                transform.reconstruction_maximum_frobenius_error,
                ScalarQuantity(float(expected.reconstruction_errors[index]), unit),
                configuration.energy_absolute_tolerance,
            )
            self._add(
                comparisons,
                f"{prefix}_hermiticity_error",
                transform.hermiticity_maximum_frobenius_error,
                ScalarQuantity(float(expected.hermiticity_errors[index]), unit),
                configuration.energy_absolute_tolerance,
            )
            observed_interpolation = VectorQuantity(
                np.asarray(
                    (
                        transform.evaluation_interpolation_hamiltonian_maximum_error.magnitude,
                        transform.evaluation_interpolation_spectral_maximum_error.magnitude,
                    ),
                    dtype=np.float64,
                ),
                unit,
            )
            self._add(
                comparisons,
                f"{prefix}_evaluation_interpolation_errors",
                observed_interpolation,
                VectorQuantity(expected.interpolation_error_values[index], unit),
                configuration.energy_absolute_tolerance,
            )
        observed_ranges = np.asarray(
            [
                [
                    [
                        channel.ordinary_omitted_block_l2_norm.magnitude,
                        channel.construction_total_spectral_maximum_error.magnitude,
                        channel.evaluation_truncation_hamiltonian_maximum_error.magnitude,
                        channel.evaluation_total_hamiltonian_maximum_error.magnitude,
                        channel.evaluation_truncation_spectral_maximum_error.magnitude,
                        channel.evaluation_total_spectral_maximum_error.magnitude,
                    ]
                    for channel in item.channels
                ]
                for item in result.ranges
            ],
            dtype=np.float64,
        )
        ranges_match = tuple(item.maximum_range for item in result.ranges) == (
            configuration.hopping_ranges
        )
        self._add(
            comparisons,
            "range_inventory",
            ScalarQuantity(0.0 if ranges_match else 1.0, unit),
            ScalarQuantity(0.0, unit),
            0.0,
        )
        self._add(
            comparisons,
            "range_values",
            VectorQuantity(observed_ranges.reshape(-1), unit),
            VectorQuantity(expected.range_values.reshape(-1), unit),
            configuration.energy_absolute_tolerance,
        )
        observed_diagnostics = np.asarray(
            [
                result.diagnostics.minimum_sampled_gap.magnitude,
                result.diagnostics.minimum_overlap_singular_value,
                result.diagnostics.attack_frame_maximum_frobenius_defect,
                result.diagnostics.pointwise_frame_maximum_frobenius_defect,
                result.diagnostics.pointwise_projector_maximum_frobenius_defect,
                result.diagnostics.pointwise_rotation_recovery_maximum_frobenius_defect,
                result.diagnostics.global_frame_maximum_frobenius_defect,
                result.diagnostics.attacked_operator_maximum_frobenius_defect.magnitude,
                result.diagnostics.pointwise_operator_maximum_frobenius_defect.magnitude,
                result.diagnostics.global_operator_maximum_frobenius_defect.magnitude,
                result.diagnostics.pointwise_minimum_cross_singular_value,
                result.diagnostics.global_minimum_cross_singular_value,
                result.diagnostics.pointwise_maximum_rank_cutoff,
                result.diagnostics.global_rank_cutoff,
            ],
            dtype=np.float64,
        )
        self._add(
            comparisons,
            "diagnostic_values",
            VectorQuantity(observed_diagnostics, unit),
            VectorQuantity(expected.diagnostic_values, unit),
            configuration.energy_absolute_tolerance,
        )
        self._add(
            comparisons,
            "closure_eigenphases",
            VectorQuantity(
                np.asarray(result.diagnostics.closure_eigenphases, dtype=np.float64),
                unit,
            ),
            VectorQuantity(expected.closure_eigenphases, unit),
            configuration.dimensionless_absolute_tolerance * 10.0,
        )
        self._projection_comparisons(comparisons)
        return Periodic1DCompositeBandAlignmentIndependentReference(comparisons)

    def _reference(self) -> _CompositeReferenceValues:
        configuration = self.request.result.configuration
        construction_coordinates = np.asarray(
            configuration.construction_reduced_momenta(), dtype=np.float64
        )
        evaluation_coordinates = np.asarray(
            configuration.evaluation_reduced_momenta(), dtype=np.float64
        )
        construction_spectrum, raw_frames, construction_parent = self._parent_values(
            construction_coordinates
        )
        evaluation_spectrum, _, _ = self._parent_values(evaluation_coordinates)
        reference, minimum_overlap, closure_phases = self._transport(raw_frames)
        attacks = self._attack_rotations(construction_coordinates)
        attacked = np.einsum("kai,kij->kaj", reference, attacks, optimize=True)
        cross = np.einsum("kai,kaj->kij", attacked.conj(), reference, optimize=True)
        left, pointwise_singular_values, right_h = np.linalg.svd(cross)
        pointwise_rotations = np.einsum("kij,kjl->kil", left, right_h, optimize=True)
        pointwise = np.einsum(
            "kai,kij->kaj", attacked, pointwise_rotations, optimize=True
        )
        stacked_attacked = attacked.reshape(-1, configuration.retained_rank)
        stacked_reference = reference.reshape(-1, configuration.retained_rank)
        global_cross = stacked_attacked.conj().T @ stacked_reference
        global_left, global_singular_values, global_right_h = np.linalg.svd(
            global_cross
        )
        global_rotation = global_left @ global_right_h
        global_frames = np.einsum(
            "kai,ij->kaj", attacked, global_rotation, optimize=True
        )
        operators = np.asarray(
            [
                np.einsum(
                    "kai,kab,kbj->kij",
                    frames.conj(),
                    construction_parent,
                    frames,
                    optimize=True,
                )
                for frames in (reference, attacked, pointwise, global_frames)
            ],
            dtype=np.complex128,
        )
        representatives = tuple(range(-32, 32))
        representative_array = np.asarray(representatives, dtype=np.int64)
        block_sets: list[Complex128Array] = []
        reconstruction_errors: list[float] = []
        hermiticity_errors: list[float] = []
        for values in operators[:3]:
            blocks = np.fft.fftshift(np.fft.fft(values, axis=0, norm="forward"), axes=0)
            blocks *= np.where(np.remainder(representative_array, 2) == 0, 1.0, -1.0)[
                :, np.newaxis, np.newaxis
            ]
            block_sets.append(np.asarray(blocks, dtype=np.complex128))
            reconstructed = self._interpolate(
                representatives, blocks, construction_coordinates
            )
            reconstruction_errors.append(
                float(
                    max(
                        np.linalg.norm(candidate - source)
                        for candidate, source in zip(reconstructed, values, strict=True)
                    )
                )
            )
            lookup = dict(zip(representatives, blocks, strict=True))
            hermiticity_errors.append(
                float(
                    max(
                        np.linalg.norm(
                            block - lookup[((-representative + 32) % 64) - 32].conj().T
                        )
                        for representative, block in lookup.items()
                    )
                )
            )
        hopping_blocks = np.asarray(block_sets, dtype=np.complex128)
        cyclic_conversion_powers = np.asarray(
            [
                float(np.linalg.norm(blocks[0]) ** 2 / configuration.retained_rank)
                for blocks in hopping_blocks
            ],
            dtype=np.float64,
        )
        ordinary_representatives = representatives[1:]
        ordinary_blocks = hopping_blocks[:, 1:, :, :]
        complete_evaluation = np.asarray(
            [
                self._interpolate(
                    ordinary_representatives,
                    blocks,
                    evaluation_coordinates,
                )
                for blocks in ordinary_blocks
            ],
            dtype=np.complex128,
        )
        evaluation_attacks = self._attack_rotations(
            evaluation_coordinates,
        )
        direct_attacked = np.einsum(
            "kai,kab,kbj->kij",
            evaluation_attacks.conj(),
            complete_evaluation[0],
            evaluation_attacks,
            optimize=True,
        )
        direct_evaluation = np.asarray(
            (
                complete_evaluation[0],
                direct_attacked,
                complete_evaluation[0],
            ),
            dtype=np.complex128,
        )
        interpolation_error_values = np.asarray(
            [
                self._maximum_error_channels(complete, direct)
                for complete, direct in zip(
                    complete_evaluation,
                    direct_evaluation,
                    strict=True,
                )
            ],
            dtype=np.float64,
        )
        range_values = np.empty(
            (len(configuration.hopping_ranges), 3, 6), dtype=np.float64
        )
        for range_index, maximum_range in enumerate(configuration.hopping_ranges):
            retained_indices = np.asarray(
                [
                    index
                    for index, representative in enumerate(ordinary_representatives)
                    if abs(representative) <= maximum_range
                ],
                dtype=np.int64,
            )
            retained_representatives = tuple(
                ordinary_representatives[index] for index in retained_indices
            )
            omitted_indices = np.asarray(
                [
                    index
                    for index, representative in enumerate(ordinary_representatives)
                    if abs(representative) > maximum_range
                ],
                dtype=np.int64,
            )
            for channel_index, blocks in enumerate(ordinary_blocks):
                omitted = float(
                    np.sqrt(
                        sum(
                            float(np.linalg.norm(blocks[index]) ** 2)
                            for index in omitted_indices
                        )
                    )
                )
                construction_candidate = self._interpolate(
                    retained_representatives,
                    blocks[retained_indices],
                    construction_coordinates,
                )
                evaluation_candidate = self._interpolate(
                    retained_representatives,
                    blocks[retained_indices],
                    evaluation_coordinates,
                )
                construction_error = float(
                    np.max(
                        np.abs(
                            np.linalg.eigvalsh(construction_candidate)
                            - construction_spectrum[:, :2]
                        )
                    )
                )
                truncation_errors = self._maximum_error_channels(
                    evaluation_candidate,
                    complete_evaluation[channel_index],
                )
                total_errors = self._maximum_error_channels(
                    evaluation_candidate,
                    direct_evaluation[channel_index],
                )
                range_values[range_index, channel_index] = (
                    omitted,
                    construction_error,
                    truncation_errors[0],
                    total_errors[0],
                    truncation_errors[1],
                    total_errors[1],
                )
        attack_frame_defect = self._maximum_defect(reference, attacked)
        pointwise_frame_defect = self._maximum_defect(reference, pointwise)
        pointwise_projector_defect = self._maximum_defect(
            np.einsum("kai,kbi->kab", reference, reference.conj(), optimize=True),
            np.einsum("kai,kbi->kab", attacked, attacked.conj(), optimize=True),
        )
        recovery_defect = self._maximum_defect(
            pointwise_rotations,
            attacks.conj().transpose(0, 2, 1),
        )
        global_frame_defect = self._maximum_defect(reference, global_frames)
        gaps = np.concatenate(
            (
                construction_spectrum[:, 2] - construction_spectrum[:, 1],
                evaluation_spectrum[:, 2] - evaluation_spectrum[:, 1],
            )
        )
        pointwise_cutoffs = np.maximum(
            configuration.procrustes_rank_absolute_tolerance,
            configuration.procrustes_rank_relative_tolerance
            * pointwise_singular_values[:, 0],
        )
        global_cutoff = max(
            configuration.procrustes_rank_absolute_tolerance,
            configuration.procrustes_rank_relative_tolerance
            * float(global_singular_values[0]),
        )
        if np.any(pointwise_singular_values[:, -1] <= pointwise_cutoffs):
            raise ValueError(
                "independent pointwise covariance reconstruction is rank deficient"
            )
        if float(global_singular_values[-1]) <= global_cutoff:
            raise ValueError(
                "independent global covariance reconstruction is rank deficient"
            )
        diagnostics = np.asarray(
            [
                float(np.min(gaps)),
                minimum_overlap,
                attack_frame_defect,
                pointwise_frame_defect,
                pointwise_projector_defect,
                recovery_defect,
                global_frame_defect,
                self._maximum_defect(operators[0], operators[1]),
                self._maximum_defect(operators[0], operators[2]),
                self._maximum_defect(operators[0], operators[3]),
                float(np.min(pointwise_singular_values)),
                float(np.min(global_singular_values)),
                float(np.max(pointwise_cutoffs)),
                float(global_cutoff),
            ],
            dtype=np.float64,
        )
        return _CompositeReferenceValues(
            construction_spectrum=construction_spectrum,
            evaluation_spectrum=evaluation_spectrum,
            reference_frames=reference,
            attacked_frames=attacked,
            pointwise_frames=pointwise,
            global_frames=global_frames,
            pointwise_rotations=pointwise_rotations,
            global_rotation=global_rotation,
            reference_operators=operators[0],
            attacked_operators=operators[1],
            pointwise_operators=operators[2],
            global_operators=operators[3],
            representatives=representatives,
            hopping_blocks=hopping_blocks,
            reconstruction_errors=np.asarray(reconstruction_errors, dtype=np.float64),
            hermiticity_errors=np.asarray(hermiticity_errors, dtype=np.float64),
            cyclic_conversion_powers=cyclic_conversion_powers,
            interpolation_error_values=interpolation_error_values,
            range_values=range_values,
            diagnostic_values=diagnostics,
            closure_eigenphases=closure_phases,
        )

    def _parent_values(
        self,
        coordinates: Float64Array,
    ) -> tuple[Float64Array, Complex128Array, Complex128Array]:
        configuration = self.request.result.configuration
        denominator = float(configuration.coefficient_denominator)
        onsite = (
            np.asarray(configuration.onsite_numerators, dtype=np.complex128)
            / denominator
        )
        positive = (
            np.asarray(configuration.positive_hopping_numerators, dtype=np.complex128)
            / denominator
        )
        phase = np.exp(2j * np.pi * coordinates)
        parents = (
            onsite[np.newaxis, :, :]
            + phase[:, np.newaxis, np.newaxis] * positive[np.newaxis, :, :]
            + phase.conj()[:, np.newaxis, np.newaxis]
            * positive.conj().T[np.newaxis, :, :]
        )
        spectra: list[Float64Array] = []
        frames: list[Complex128Array] = []
        represented_parents: list[Complex128Array] = []
        for parent in parents:
            symmetric = 0.5 * (parent + parent.conj().T)
            represented = np.triu(symmetric) + np.triu(symmetric, 1).conj().T
            values, vectors = np.linalg.eigh(represented)
            canonical = np.asarray(vectors, dtype=np.complex128).copy()
            for column in range(canonical.shape[1]):
                pivot = int(np.argmax(np.abs(canonical[:, column])))
                pivot_value = canonical[pivot, column]
                pivot_magnitude = float(np.abs(pivot_value))
                canonical[:, column] /= pivot_value / pivot_magnitude
                canonical[pivot, column] = complex(pivot_magnitude, 0.0)
            spectra.append(np.asarray(values, dtype=np.float64))
            frames.append(np.asarray(canonical[:, :2], dtype=np.complex128))
            represented_parents.append(np.asarray(represented, dtype=np.complex128))
        return (
            np.asarray(spectra, dtype=np.float64),
            np.asarray(frames, dtype=np.complex128),
            np.asarray(represented_parents, dtype=np.complex128),
        )

    def _transport(
        self,
        raw: Complex128Array,
    ) -> tuple[Complex128Array, float, Float64Array]:
        transported: list[Complex128Array] = [raw[0].copy()]
        singular_values: list[float] = []
        for index in range(raw.shape[0] - 1):
            overlap = transported[index].conj().T @ raw[index + 1]
            left, values, right_h = np.linalg.svd(overlap)
            singular_values.extend(float(value) for value in values)
            transported.append(raw[index + 1] @ right_h.conj().T @ left.conj().T)
        closure = transported[-1].conj().T @ transported[0]
        left, values, right_h = np.linalg.svd(closure)
        singular_values.extend(float(value) for value in values)
        unitary_closure = left @ right_h
        triangular, eigenvectors = schur(unitary_closure, output="complex")
        phases = np.angle(np.diag(triangular)).astype(np.float64)
        order = np.argsort(phases)
        phases = phases[order]
        eigenvectors = eigenvectors[:, order]
        count = len(transported)
        for index in range(count):
            fraction = float(index) / float(count)
            root = (
                eigenvectors
                @ np.diag(np.exp(1j * phases * fraction))
                @ eigenvectors.conj().T
            )
            transported[index] = transported[index] @ root
        return (
            np.asarray(transported, dtype=np.complex128),
            min(singular_values),
            phases,
        )

    def _attack_rotations(
        self,
        coordinates: Float64Array,
    ) -> Complex128Array:
        configuration = self.request.result.configuration
        angle = np.full(
            coordinates.shape,
            configuration.attack_constant_angle,
            dtype=np.float64,
        )
        for harmonic, coefficient in enumerate(
            configuration.attack_sine_coefficients, start=1
        ):
            angle += coefficient * np.sin(2.0 * np.pi * harmonic * coordinates)
        rotations = np.empty((coordinates.size, 2, 2), dtype=np.complex128)
        rotations[:, 0, 0] = np.cos(angle)
        rotations[:, 0, 1] = -np.sin(angle)
        rotations[:, 1, 0] = np.sin(angle)
        rotations[:, 1, 1] = np.cos(angle)
        return rotations

    def _interpolate(
        self,
        representatives: tuple[int, ...],
        blocks: Complex128Array,
        coordinates: Float64Array,
    ) -> Complex128Array:
        phases = np.exp(
            2j
            * np.pi
            * np.outer(coordinates, np.asarray(representatives, dtype=np.float64))
        )
        return np.asarray(
            np.einsum("kr,rij->kij", phases, blocks, optimize=True),
            dtype=np.complex128,
        )

    def _maximum_error_channels(
        self,
        candidate: Complex128Array,
        reference: Complex128Array,
    ) -> tuple[float, float]:
        hamiltonian = float(
            max(
                np.linalg.norm(candidate_value - reference_value) / np.sqrt(2.0)
                for candidate_value, reference_value in zip(
                    candidate,
                    reference,
                    strict=True,
                )
            )
        )
        candidate_hermitian = 0.5 * (candidate + candidate.conj().transpose(0, 2, 1))
        reference_hermitian = 0.5 * (reference + reference.conj().transpose(0, 2, 1))
        spectral = float(
            np.max(
                np.abs(
                    np.linalg.eigvalsh(candidate_hermitian)
                    - np.linalg.eigvalsh(reference_hermitian)
                )
            )
        )
        return hamiltonian, spectral

    def _maximum_defect(self, left: Complex128Array, right: Complex128Array) -> float:
        return float(
            max(
                np.linalg.norm(left_value - right_value)
                for left_value, right_value in zip(left, right, strict=True)
            )
        )

    def _complex_inventory(
        self,
        values: tuple[ComplexMatrixQuantity, ...],
    ) -> ComplexVectorQuantity:
        return ComplexVectorQuantity(
            np.asarray(
                [entry for value in values for entry in value.magnitude.reshape(-1)],
                dtype=np.complex128,
            ),
            Unitless(),
        )

    def _add(
        self,
        comparisons: dict[str, MaximumAbsoluteErrorComparison],
        name: str,
        observed: ScalarQuantity
        | VectorQuantity
        | ComplexVectorQuantity
        | MatrixQuantity
        | ComplexMatrixQuantity,
        reference: ScalarQuantity
        | VectorQuantity
        | ComplexVectorQuantity
        | MatrixQuantity
        | ComplexMatrixQuantity,
        tolerance: float,
    ) -> None:
        comparisons[name] = MaximumAbsoluteErrorComparison(
            observed,
            reference,
            ScalarQuantity(tolerance, observed.unit),
        )

    def _projection_comparisons(
        self,
        comparisons: dict[str, MaximumAbsoluteErrorComparison],
    ) -> None:
        result = self.request.result
        data = self.request.visualization_data
        unit = Unitless()
        vector_fields = (
            (
                "evaluation_reduced_momenta",
                data.evaluation_reduced_momenta,
                VectorQuantity(
                    np.asarray(result.evaluation_reduced_momenta, dtype=np.float64),
                    unit,
                ),
            ),
            (
                "cyclic_conversion_powers",
                data.cyclic_conversion_powers,
                VectorQuantity(
                    np.asarray(
                        [
                            transform.cyclic_conversion_power.magnitude
                            for transform in result.transforms
                        ],
                        dtype=np.float64,
                    ),
                    unit,
                ),
            ),
            (
                "evaluation_interpolation_hamiltonian_maximum_errors",
                data.evaluation_interpolation_hamiltonian_maximum_errors,
                VectorQuantity(
                    np.asarray(
                        [
                            transform.evaluation_interpolation_hamiltonian_maximum_error.magnitude
                            for transform in result.transforms
                        ],
                        dtype=np.float64,
                    ),
                    unit,
                ),
            ),
            (
                "evaluation_interpolation_spectral_maximum_errors",
                data.evaluation_interpolation_spectral_maximum_errors,
                VectorQuantity(
                    np.asarray(
                        [
                            transform.evaluation_interpolation_spectral_maximum_error.magnitude
                            for transform in result.transforms
                        ],
                        dtype=np.float64,
                    ),
                    unit,
                ),
            ),
            (
                "diagnostic_values",
                data.diagnostic_values,
                VectorQuantity(
                    np.asarray(
                        [
                            result.diagnostics.attack_frame_maximum_frobenius_defect,
                            result.diagnostics.pointwise_frame_maximum_frobenius_defect,
                            result.diagnostics.global_frame_maximum_frobenius_defect,
                            result.diagnostics.attacked_operator_maximum_frobenius_defect.magnitude,
                            result.diagnostics.pointwise_operator_maximum_frobenius_defect.magnitude,
                            result.diagnostics.global_operator_maximum_frobenius_defect.magnitude,
                        ],
                        dtype=np.float64,
                    ),
                    unit,
                ),
            ),
        )
        for name, observed, reference in vector_fields:
            self._add(
                comparisons,
                f"visualization_{name}",
                observed,
                reference,
                0.0,
            )
        self._add(
            comparisons,
            "visualization_evaluation_parent_spectrum",
            data.evaluation_parent_spectrum,
            MatrixQuantity(result.evaluation_parent_spectrum.magnitude[:, :2], unit),
            0.0,
        )
        observed_range_matrices = (
            data.ordinary_omitted_block_l2_norms,
            data.construction_total_spectral_maximum_errors,
            data.evaluation_truncation_hamiltonian_maximum_errors,
            data.evaluation_total_hamiltonian_maximum_errors,
            data.evaluation_truncation_spectral_maximum_errors,
            data.evaluation_total_spectral_maximum_errors,
        )
        range_metric_names = (
            "ordinary_omitted_block_l2_norms",
            "construction_total_spectral_maximum_errors",
            "evaluation_truncation_hamiltonian_maximum_errors",
            "evaluation_total_hamiltonian_maximum_errors",
            "evaluation_truncation_spectral_maximum_errors",
            "evaluation_total_spectral_maximum_errors",
        )
        for metric_index, (name, range_observed) in enumerate(
            zip(range_metric_names, observed_range_matrices, strict=True)
        ):
            reference_values = np.asarray(
                [
                    [
                        (
                            channel.ordinary_omitted_block_l2_norm.magnitude,
                            channel.construction_total_spectral_maximum_error.magnitude,
                            channel.evaluation_truncation_hamiltonian_maximum_error.magnitude,
                            channel.evaluation_total_hamiltonian_maximum_error.magnitude,
                            channel.evaluation_truncation_spectral_maximum_error.magnitude,
                            channel.evaluation_total_spectral_maximum_error.magnitude,
                        )[metric_index]
                        for channel in item.channels
                    ]
                    for item in result.ranges
                ],
                dtype=np.float64,
            )
            self._add(
                comparisons,
                f"visualization_{name}",
                range_observed,
                MatrixQuantity(reference_values, unit),
                0.0,
            )
        norms = np.asarray(
            [
                [
                    float(np.linalg.norm(block.magnitude))
                    for block in transform.hopping_blocks
                ]
                for transform in result.transforms
            ],
            dtype=np.float64,
        )
        self._add(
            comparisons,
            "visualization_hopping_block_frobenius_norms",
            data.hopping_block_frobenius_norms,
            MatrixQuantity(norms, unit),
            0.0,
        )
        metadata_matches = (
            data.maximum_ranges == tuple(item.maximum_range for item in result.ranges)
            and data.channel_names
            == tuple(item.channel for item in result.ranges[0].channels)
            and data.transform_representatives == result.transforms[0].representatives
            and data.diagnostic_names
            == (
                "attack frame",
                "pointwise frame",
                "global frame",
                "attack operator",
                "pointwise operator",
                "global operator",
            )
        )
        self._add(
            comparisons,
            "visualization_metadata",
            ScalarQuantity(0.0 if metadata_matches else 1.0, unit),
            ScalarQuantity(0.0, unit),
            0.0,
        )


__all__ = [
    "Periodic1DCompositeBandAlignmentIndependentReference",
    "Periodic1DCompositeBandAlignmentIndependentReferenceAnalyzer",
    "Periodic1DCompositeBandAlignmentIndependentReferenceRequest",
]
