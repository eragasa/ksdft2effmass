"""Independent reconstruction for the smooth non-flat four-state realization."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from projectkoios.optimization.selection.harmonic import (
    PeriodicHarmonic,
    PeriodicHarmonicMaximum,
    PeriodicHarmonicMaximumStatus,
)

from ._validation import _finite_float
from .nonflat_definition import SmoothFourStateDefinition
from .nonflat_results import (
    SmoothFourStateHoppingBlockResult,
    SmoothFourStateParentFamilyResult,
    SmoothFourStatePointResult,
    SmoothFourStateResult,
)


@dataclass(frozen=True, slots=True)
class SmoothFourStateVerificationResult:
    """Retain the bounded outcome of independent non-flat reconstruction."""

    passes: bool
    absolute_tolerance: float
    maximum_absolute_defect: float

    def __post_init__(self) -> None:
        """Validate the verification decision against its maximum defect."""
        if type(self.passes) is not bool:
            raise TypeError("passes must be a built-in bool")
        _finite_float("absolute_tolerance", self.absolute_tolerance)
        _finite_float("maximum_absolute_defect", self.maximum_absolute_defect)
        if self.absolute_tolerance <= 0.0:
            raise ValueError("absolute_tolerance must be positive")
        if self.maximum_absolute_defect < 0.0:
            raise ValueError("maximum_absolute_defect must be nonnegative")
        if self.passes is not (self.maximum_absolute_defect <= self.absolute_tolerance):
            raise ValueError("passes must match the maximum defect")


class SmoothFourStateVerifier:
    """Rebuild the non-flat result without calling its producing action."""

    __slots__ = ()

    def execute(
        self, retained: SmoothFourStateResult
    ) -> SmoothFourStateVerificationResult:
        """Return the maximum independently reconstructed absolute defect."""
        if type(retained) is not SmoothFourStateResult:
            raise TypeError("retained must be SmoothFourStateResult")
        expected = self._reconstruct(retained.definition)
        defects = [
            abs(expected.minimum_external_gap - retained.minimum_external_gap),
            abs(
                expected.minimum_transport_singular_value
                - retained.minimum_transport_singular_value
            ),
            abs(
                expected.maximum_frame_orthonormality_defect
                - retained.maximum_frame_orthonormality_defect
            ),
            abs(expected.periodic_closure_defect - retained.periodic_closure_defect),
            abs(
                expected.maximum_reference_hermiticity_defect
                - retained.maximum_reference_hermiticity_defect
            ),
        ]
        if len(expected.points) != len(retained.points):
            defects.append(math.inf)
        else:
            for expected_point, retained_point in zip(
                expected.points, retained.points, strict=True
            ):
                defects.extend(self._point_defects(expected_point, retained_point))
        maximum = float(max(defects, default=0.0))
        tolerance = retained.definition.verification_absolute_tolerance
        return SmoothFourStateVerificationResult(
            passes=maximum <= tolerance,
            absolute_tolerance=tolerance,
            maximum_absolute_defect=maximum,
        )

    @staticmethod
    def _point_defects(
        expected: SmoothFourStatePointResult,
        retained: SmoothFourStatePointResult,
    ) -> list[float]:
        defects = [
            abs(expected.amplitude - retained.amplitude),
            abs(expected.maximum_band_defect - retained.maximum_band_defect),
            abs(expected.splitting_scale - retained.splitting_scale),
            abs(
                expected.discrete_maximum_correlation
                - retained.discrete_maximum_correlation
            ),
            abs(
                expected.minimum_operator_threshold
                - retained.minimum_operator_threshold
            ),
            abs(
                expected.exact_spectrum_joint_operator_threshold
                - retained.exact_spectrum_joint_operator_threshold
            ),
            abs(
                expected.minimum_loss_reconstruction_defect
                - retained.minimum_loss_reconstruction_defect
            ),
            abs(
                expected.reference_nonzero_hopping_weight
                - retained.reference_nonzero_hopping_weight
            ),
            abs(
                expected.comparison_nonzero_hopping_weight
                - retained.comparison_nonzero_hopping_weight
            ),
            abs(
                expected.reference_parseval_defect - retained.reference_parseval_defect
            ),
            abs(
                expected.comparison_parseval_defect
                - retained.comparison_parseval_defect
            ),
            abs(
                expected.harmonic_maximum.harmonic.offset
                - retained.harmonic_maximum.harmonic.offset
            ),
            abs(
                expected.harmonic_maximum.harmonic.cosine_coefficient
                - retained.harmonic_maximum.harmonic.cosine_coefficient
            ),
            abs(
                expected.harmonic_maximum.harmonic.sine_coefficient
                - retained.harmonic_maximum.harmonic.sine_coefficient
            ),
            abs(
                expected.harmonic_maximum.maximum_value
                - retained.harmonic_maximum.maximum_value
            ),
            abs(
                expected.harmonic_maximum.amplitude
                - retained.harmonic_maximum.amplitude
            ),
            abs(
                expected.harmonic_maximum.fundamental_period
                - retained.harmonic_maximum.fundamental_period
            ),
            abs(
                expected.harmonic_maximum.applied_degeneracy_cutoff
                - retained.harmonic_maximum.applied_degeneracy_cutoff
            ),
        ]
        expected_harmonic = expected.harmonic_maximum.harmonic
        retained_harmonic = retained.harmonic_maximum.harmonic
        if (
            expected_harmonic.harmonic_order != retained_harmonic.harmonic_order
            or expected_harmonic.fundamental_interval_start
            != retained_harmonic.fundamental_interval_start
        ):
            defects.append(math.inf)
        expected_angle = expected.harmonic_maximum.canonical_maximizing_argument
        retained_angle = retained.harmonic_maximum.canonical_maximizing_argument
        if expected_angle is None and retained_angle is None:
            defects.append(0.0)
        elif expected_angle is None or retained_angle is None:
            defects.append(math.inf)
        else:
            defects.append(abs(expected_angle - retained_angle))
        if expected.harmonic_maximum.status is not retained.harmonic_maximum.status:
            defects.append(math.inf)
        if len(expected.hopping_blocks) != len(retained.hopping_blocks):
            defects.append(math.inf)
        else:
            for expected_block, retained_block in zip(
                expected.hopping_blocks, retained.hopping_blocks, strict=True
            ):
                if expected_block.displacement != retained_block.displacement:
                    defects.append(math.inf)
                    continue
                expected_reference = (
                    expected_block.reference_normalized_squared_frobenius_norm
                )
                retained_reference = (
                    retained_block.reference_normalized_squared_frobenius_norm
                )
                expected_comparison = (
                    expected_block.comparison_normalized_squared_frobenius_norm
                )
                retained_comparison = (
                    retained_block.comparison_normalized_squared_frobenius_norm
                )
                defects.extend(
                    (
                        abs(expected_reference - retained_reference),
                        abs(expected_comparison - retained_comparison),
                    )
                )
        return defects

    @classmethod
    def _reconstruct(
        cls, definition: SmoothFourStateDefinition
    ) -> SmoothFourStateResult:
        sample_count = definition.reciprocal_mesh_size
        coordinates = -0.5 + np.arange(sample_count, dtype=np.float64) / float(
            sample_count
        )
        parent = cls._parent(coordinates, definition.parent_hopping_scale)
        eigenvalues, eigenvectors = np.linalg.eigh(parent)
        external_gap = float(np.min(eigenvalues[:, 2] - eigenvalues[:, 1]))
        frames, minimum_singular, closure_defect = cls._frame(
            eigenvectors[:, :, :2], definition
        )
        identity = np.eye(2, dtype=np.complex128)
        orthonormality_defect = float(
            max(np.linalg.norm(frame.conj().T @ frame - identity) for frame in frames)
        )
        retained_matrices = np.asarray(
            [
                frame.conj().T @ matrix @ frame
                for frame, matrix in zip(frames, parent, strict=True)
            ],
            dtype=np.complex128,
        )
        hermiticity_defect = float(
            np.max(
                np.abs(retained_matrices - retained_matrices.conj().transpose(0, 2, 1))
            )
        )
        means = np.trace(retained_matrices, axis1=1, axis2=2).real / 2.0
        traceless = retained_matrices - means[:, None, None] * identity
        splitting_scale = float(
            np.mean([np.vdot(matrix, matrix).real / 2.0 for matrix in traceless])
        )
        displacements = tuple(range(-(sample_count // 2), sample_count // 2))
        reference_blocks = cls._blocks(coordinates, retained_matrices, displacements)
        reference_powers = cls._powers(reference_blocks)
        reference_nonzero = math.fsum(
            power
            for displacement, power in zip(displacements, reference_powers, strict=True)
            if displacement != 0
        )
        reference_reciprocal = float(
            np.mean(
                [np.vdot(matrix, matrix).real / 2.0 for matrix in retained_matrices]
            )
        )
        reference_parseval = abs(reference_reciprocal - math.fsum(reference_powers))
        points = tuple(
            cls._point(
                definition,
                coordinates,
                retained_matrices,
                traceless,
                means,
                splitting_scale,
                displacements,
                reference_powers,
                reference_nonzero,
                reference_parseval,
                amplitude,
            )
            for amplitude in definition.amplitudes
        )
        return SmoothFourStateResult(
            definition=definition,
            minimum_external_gap=external_gap,
            minimum_transport_singular_value=minimum_singular,
            maximum_frame_orthonormality_defect=orthonormality_defect,
            periodic_closure_defect=closure_defect,
            maximum_reference_hermiticity_defect=hermiticity_defect,
            points=points,
        )

    @staticmethod
    def _parent(coordinates: np.ndarray, parent_hopping_scale: float) -> np.ndarray:
        onsite_lower = np.asarray([[-1.20, 0.06], [0.06, -0.35]], dtype=np.complex128)
        onsite_upper = np.asarray([[1.00, 0.04], [0.04, 1.75]], dtype=np.complex128)
        hop_lower = np.diag([0.15, -0.10]).astype(np.complex128)
        hop_upper = np.diag([0.05, -0.04]).astype(np.complex128)
        coupling = np.diag([0.12, 0.10]).astype(np.complex128)
        matrices = []
        for coordinate in coordinates:
            phase = np.exp(2.0j * np.pi * coordinate)
            scaled_phase = parent_hopping_scale * phase
            matrices.append(
                np.block(
                    [
                        [
                            onsite_lower
                            + scaled_phase * hop_lower
                            + scaled_phase.conjugate() * hop_lower.conj().T,
                            scaled_phase * coupling,
                        ],
                        [
                            scaled_phase.conjugate() * coupling.conj().T,
                            onsite_upper
                            + scaled_phase * hop_upper
                            + scaled_phase.conjugate() * hop_upper.conj().T,
                        ],
                    ]
                )
            )
        return np.asarray(matrices, dtype=np.complex128)

    @classmethod
    def _frame(
        cls, raw: np.ndarray, definition: SmoothFourStateDefinition
    ) -> tuple[np.ndarray, float, float]:
        transported = [raw[0]]
        minimum_singular = 1.0
        for next_frame in raw[1:]:
            overlap = transported[-1].conj().T @ next_frame
            left, singular_values, right_h = np.linalg.svd(overlap)
            smallest = float(singular_values[-1])
            if smallest <= definition.minimum_transport_singular_value:
                raise ValueError(
                    "independent transport overlap fails before unitary completion"
                )
            transported.append(next_frame @ right_h.conj().T @ left.conj().T)
            minimum_singular = min(minimum_singular, smallest)
        overlap = transported[-1].conj().T @ raw[0]
        left, singular_values, right_h = np.linalg.svd(overlap)
        smallest = float(singular_values[-1])
        if smallest <= definition.minimum_transport_singular_value:
            raise ValueError(
                "independent closure overlap fails before unitary completion"
            )
        duplicate = raw[0] @ right_h.conj().T @ left.conj().T
        minimum_singular = min(minimum_singular, smallest)
        mismatch = transported[0].conj().T @ duplicate
        left, _, right_h = np.linalg.svd(mismatch)
        unitary = left @ right_h
        eigenvalues, eigenvectors = np.linalg.eig(unitary)
        inverse = np.linalg.inv(eigenvectors)
        phases = np.angle(eigenvalues)
        sample_count = raw.shape[0]
        corrected = []
        for index, frame in enumerate(transported):
            correction = (
                eigenvectors
                @ np.diag(np.exp(-1.0j * float(index) / float(sample_count) * phases))
                @ inverse
            )
            left, _, right_h = np.linalg.svd(correction)
            corrected.append(frame @ left @ right_h)
        endpoint = eigenvectors @ np.diag(np.exp(-1.0j * phases)) @ inverse
        left, _, right_h = np.linalg.svd(endpoint)
        closure = float(np.linalg.norm(duplicate @ left @ right_h - corrected[0]))
        return np.asarray(corrected, dtype=np.complex128), minimum_singular, closure

    @classmethod
    def _point(
        cls,
        definition: SmoothFourStateDefinition,
        coordinates: np.ndarray,
        reference: np.ndarray,
        traceless: np.ndarray,
        means: np.ndarray,
        splitting_scale: float,
        displacements: tuple[int, ...],
        reference_powers: tuple[float, ...],
        reference_nonzero: float,
        reference_parseval: float,
        amplitude: float,
    ) -> SmoothFourStatePointResult:
        theta = amplitude * np.sin(2.0 * np.pi * coordinates)
        rotations = np.asarray(
            [
                [
                    [math.cos(value), -math.sin(value)],
                    [math.sin(value), math.cos(value)],
                ]
                for value in theta
            ],
            dtype=np.complex128,
        )
        comparison = np.asarray(
            [
                rotation.conj().T @ matrix @ rotation
                for rotation, matrix in zip(rotations, reference, strict=True)
            ]
        )
        comparison_traceless = comparison - means[:, None, None] * np.eye(2)
        coefficients = cls._coefficients(traceless, comparison_traceless)
        harmonic = PeriodicHarmonic(*coefficients, 2, -math.pi / 2.0)
        maximum = cls._harmonic_maximum(definition, harmonic)
        raw_correlation = maximum.maximum_value / splitting_scale
        tolerance = definition.verification_absolute_tolerance
        if abs(raw_correlation - 1.0) <= tolerance:
            correlation = 1.0
        elif abs(raw_correlation + 1.0) <= tolerance:
            correlation = -1.0
        elif not -1.0 < raw_correlation < 1.0:
            raise FloatingPointError("independent correlation lies outside [-1, 1]")
        else:
            correlation = raw_correlation
        optimal_scale = max(0.0, correlation)
        minimum_squared = splitting_scale * (1.0 - optimal_scale**2)
        selected_angle = maximum.canonical_maximizing_argument
        angle = 0.0 if selected_angle is None else selected_angle
        rotation = np.asarray(
            [[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]],
            dtype=np.complex128,
        )
        candidate = np.asarray(
            [
                mean * np.eye(2) + optimal_scale * rotation.conj().T @ matrix @ rotation
                for mean, matrix in zip(means, traceless, strict=True)
            ]
        )
        reconstructed = float(
            np.mean(
                [
                    np.vdot(left - right, left - right).real / 2.0
                    for left, right in zip(candidate, comparison, strict=True)
                ]
            )
        )
        blocks = cls._blocks(coordinates, comparison, displacements)
        powers = cls._powers(blocks)
        nonzero = math.fsum(
            power
            for displacement, power in zip(displacements, powers, strict=True)
            if displacement != 0
        )
        reciprocal = float(
            np.mean([np.vdot(matrix, matrix).real / 2.0 for matrix in comparison])
        )
        parseval = abs(reciprocal - math.fsum(powers))
        band_defect = float(
            np.max(
                np.abs(np.linalg.eigvalsh(comparison) - np.linalg.eigvalsh(reference))
            )
        )
        hopping = tuple(
            SmoothFourStateHoppingBlockResult(displacement, ref_power, comp_power)
            for displacement, ref_power, comp_power in zip(
                displacements, reference_powers, powers, strict=True
            )
        )
        return SmoothFourStatePointResult(
            amplitude=amplitude,
            maximum_band_defect=band_defect,
            splitting_scale=splitting_scale,
            harmonic_maximum=maximum,
            discrete_maximum_correlation=correlation,
            minimum_operator_threshold=math.sqrt(max(0.0, minimum_squared)),
            exact_spectrum_joint_operator_threshold=math.sqrt(
                max(0.0, 2.0 * splitting_scale * (1.0 - correlation))
            ),
            minimum_loss_reconstruction_defect=abs(reconstructed - minimum_squared),
            reference_nonzero_hopping_weight=reference_nonzero,
            comparison_nonzero_hopping_weight=nonzero,
            reference_parseval_defect=reference_parseval,
            comparison_parseval_defect=parseval,
            hopping_blocks=hopping,
        )

    @staticmethod
    def _coefficients(
        reference: np.ndarray, comparison: np.ndarray
    ) -> tuple[float, float, float]:
        x_value = reference[:, 0, 1].real
        y_value = -reference[:, 0, 1].imag
        z_value = 0.5 * (reference[:, 0, 0].real - reference[:, 1, 1].real)
        target_x = comparison[:, 0, 1].real
        target_y = -comparison[:, 0, 1].imag
        target_z = 0.5 * (comparison[:, 0, 0].real - comparison[:, 1, 1].real)
        return (
            float(np.mean(y_value * target_y)),
            float(np.mean(x_value * target_x + z_value * target_z)),
            float(np.mean(x_value * target_z - z_value * target_x)),
        )

    @staticmethod
    def _harmonic_maximum(
        definition: SmoothFourStateDefinition,
        harmonic: PeriodicHarmonic,
    ) -> PeriodicHarmonicMaximum:
        amplitude = math.hypot(harmonic.cosine_coefficient, harmonic.sine_coefficient)
        maximum_value = harmonic.offset + amplitude
        scale = max(1.0, abs(harmonic.offset), amplitude)
        cutoff = definition.harmonic_absolute_degeneracy_tolerance + (
            definition.harmonic_relative_degeneracy_tolerance * scale
        )
        if amplitude <= cutoff:
            argument = None
            status = PeriodicHarmonicMaximumStatus.NUMERICALLY_CONSTANT
        else:
            phase = math.atan2(harmonic.sine_coefficient, harmonic.cosine_coefficient)
            raw = phase / float(harmonic.harmonic_order)
            period = harmonic.fundamental_period
            start = harmonic.fundamental_interval_start
            argument = start + ((raw - start) % period)
            if argument >= harmonic.fundamental_interval_stop:
                argument = start
            status = PeriodicHarmonicMaximumStatus.UNIQUE
        return PeriodicHarmonicMaximum(
            harmonic=harmonic,
            maximum_value=maximum_value,
            amplitude=amplitude,
            canonical_maximizing_argument=argument,
            fundamental_period=harmonic.fundamental_period,
            applied_degeneracy_cutoff=cutoff,
            status=status,
        )

    @staticmethod
    def _blocks(
        coordinates: np.ndarray,
        matrices: np.ndarray,
        displacements: tuple[int, ...],
    ) -> np.ndarray:
        output: list[np.ndarray] = []
        for displacement in displacements:
            block = np.zeros((2, 2), dtype=np.complex128)
            for coordinate, matrix in zip(coordinates, matrices, strict=True):
                block += np.exp(-2.0j * np.pi * coordinate * displacement) * matrix
            output.append(block / float(coordinates.size))
        return np.asarray(output, dtype=np.complex128)

    @staticmethod
    def _powers(blocks: np.ndarray) -> tuple[float, ...]:
        return tuple(float(np.vdot(block, block).real / 2.0) for block in blocks)


class SmoothFourStateParentFamilyVerifier:
    """Verify every member of a bounded parent-hopping homotopy."""

    __slots__ = ()

    def execute(
        self, retained: SmoothFourStateParentFamilyResult
    ) -> SmoothFourStateVerificationResult:
        """Return the largest independently reconstructed member defect."""
        if type(retained) is not SmoothFourStateParentFamilyResult:
            raise TypeError("retained must be SmoothFourStateParentFamilyResult")
        member_verifications = tuple(
            SmoothFourStateVerifier().execute(member) for member in retained.members
        )
        maximum = max(item.maximum_absolute_defect for item in member_verifications)
        tolerance = (
            retained.definition.template_definition.verification_absolute_tolerance
        )
        return SmoothFourStateVerificationResult(
            passes=all(item.passes for item in member_verifications),
            absolute_tolerance=tolerance,
            maximum_absolute_defect=maximum,
        )


__all__ = [
    "SmoothFourStateParentFamilyVerifier",
    "SmoothFourStateVerificationResult",
    "SmoothFourStateVerifier",
]
