"""Independent reconstruction for controlled multiband alignment results."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.linalg import schur  # type: ignore[import-untyped]

from ksdft2effmass.operators import ScalarQuantity
from ksdft2effmass.solid_state import BlockHoppingModel1D

from .definition import Periodic1DMultibandAlignmentCalculationDefinition
from .results import Periodic1DMultibandAlignmentCalculationResult


@dataclass(frozen=True, slots=True)
class Periodic1DMultibandAlignmentVerificationResult:
    """Retain independently reconstructed M2 numerical-consistency evidence.

    ``dimensionless_maximum_absolute_defect`` aggregates frame, projector, rotation,
    identity, and Boolean-state channels.  ``energy_maximum_absolute_defect`` aggregates
    spectra, represented operators, hoppings, and locality in the parent energy unit.
    ``passes`` is derived from both defects and the common absolute tolerance.
    """

    calculation: Periodic1DMultibandAlignmentCalculationResult
    dimensionless_maximum_absolute_defect: float
    energy_maximum_absolute_defect: ScalarQuantity
    absolute_tolerance: float
    passes: bool

    def __post_init__(self) -> None:
        """Validate nonnegative defects, units, and derived disposition."""
        if type(self.calculation) is not Periodic1DMultibandAlignmentCalculationResult:
            raise TypeError(
                "calculation must be Periodic1DMultibandAlignmentCalculationResult"
            )
        if type(self.dimensionless_maximum_absolute_defect) is not float:
            raise TypeError(
                "dimensionless_maximum_absolute_defect must be a built-in float"
            )
        if (
            not np.isfinite(self.dimensionless_maximum_absolute_defect)
            or self.dimensionless_maximum_absolute_defect < 0.0
        ):
            raise ValueError(
                "dimensionless_maximum_absolute_defect must be finite and nonnegative"
            )
        if type(self.energy_maximum_absolute_defect) is not ScalarQuantity:
            raise TypeError("energy_maximum_absolute_defect must be ScalarQuantity")
        energy_unit = (
            self.calculation.definition.parent_model.hopping_model.hopping_blocks[
                0
            ].unit
        )
        if self.energy_maximum_absolute_defect.unit != energy_unit:
            raise ValueError("energy defect must use the parent energy unit")
        if self.energy_maximum_absolute_defect.magnitude < 0.0:
            raise ValueError("energy defect must be nonnegative")
        if type(self.absolute_tolerance) is not float:
            raise TypeError("absolute_tolerance must be a built-in float")
        if not np.isfinite(self.absolute_tolerance) or self.absolute_tolerance < 0.0:
            raise ValueError("absolute_tolerance must be finite and nonnegative")
        if type(self.passes) is not bool:
            raise TypeError("passes must be a built-in bool")
        expected = (
            self.dimensionless_maximum_absolute_defect <= self.absolute_tolerance
            and self.energy_maximum_absolute_defect.magnitude <= self.absolute_tolerance
        )
        if self.passes is not expected:
            raise ValueError("passes must match reconstructed defects and tolerance")


class Periodic1DMultibandAlignmentResultVerifier:
    """Reconstruct M2 without invoking its producer calculation Action.

    The verifier owns direct finite formulas for parent interpolation, eigensystems,
    polar transport, gauge attack, pointwise/global alignment, projection, Fourier
    blocks, Hermiticity, and range diagnostics.  Shared libraries and conventions mean
    this remains numerical verification rather than an independent physical oracle.
    """

    __slots__ = ()

    def execute(
        self, calculation: Periodic1DMultibandAlignmentCalculationResult
    ) -> Periodic1DMultibandAlignmentVerificationResult:
        """Rebuild every M2 finite channel and return maximum defects.

        Parameters
        ----------
        calculation
            Exact typed M2 aggregate result.

        Returns
        -------
        Periodic1DMultibandAlignmentVerificationResult
            Separate dimensionless and energy defects with the derived pass state.

        Raises
        ------
        TypeError
            If ``calculation`` is not the exact M2 result type.
        """
        if type(calculation) is not Periodic1DMultibandAlignmentCalculationResult:
            raise TypeError(
                "calculation must be Periodic1DMultibandAlignmentCalculationResult"
            )
        definition = calculation.definition
        parent = definition.parent_model.hopping_model
        training_reduced = (
            calculation.training_target.coordinates.magnitude
            / parent.reciprocal_period.magnitude
        )
        withheld_reduced = np.asarray(
            definition.withheld_reduced_momenta, dtype=np.float64
        )
        parent_training = self._interpolate_parent(parent, training_reduced)
        parent_withheld = self._interpolate_parent(parent, withheld_reduced)
        training_eigenvalues, raw_frames = self._eigensystem(
            parent_training, definition.retained_rank
        )
        withheld_eigenvalues = np.asarray(
            [
                np.linalg.eigvalsh(matrix)[: definition.retained_rank]
                for matrix in parent_withheld
            ],
            dtype=np.float64,
        )
        reference_frames, minimum_overlap, closure_phases = self._transport(raw_frames)
        attacks = self._attacks(definition, training_reduced)
        attacked_frames = np.asarray(
            [
                frame @ attack
                for frame, attack in zip(reference_frames, attacks, strict=True)
            ],
            dtype=np.complex128,
        )
        rotations, aligned_frames = self._pointwise_align(
            reference_frames, attacked_frames
        )
        constrained_rotation = self._global_rotation(reference_frames, attacked_frames)
        constrained_frames = np.asarray(
            [frame @ constrained_rotation for frame in attacked_frames],
            dtype=np.complex128,
        )
        reference_operators = self._project(parent_training, reference_frames)
        attacked_operators = self._project(parent_training, attacked_frames)
        aligned_operators = self._project(parent_training, aligned_frames)
        constrained_operators = self._project(parent_training, constrained_frames)
        representatives = np.arange(
            -definition.reciprocal_mesh_size // 2,
            definition.reciprocal_mesh_size // 2,
            dtype=np.int64,
        )
        reference_blocks = self._fourier(
            training_reduced, reference_operators, representatives
        )
        attacked_blocks = self._fourier(
            training_reduced, attacked_operators, representatives
        )
        aligned_blocks = self._fourier(
            training_reduced, aligned_operators, representatives
        )

        dimensionless_defects: list[float] = []
        energy_defects: list[float] = []
        energy_defects.extend(
            (
                self._maximum(
                    training_eigenvalues,
                    calculation.training_target.eigenvalues.magnitude,
                ),
                self._maximum(
                    withheld_eigenvalues,
                    calculation.withheld_target.eigenvalues.magnitude,
                ),
            )
        )
        retained = calculation.diagnostics
        expected_gap = min(
            float(
                np.linalg.eigvalsh(matrix)[definition.retained_rank]
                - np.linalg.eigvalsh(matrix)[definition.retained_rank - 1]
            )
            for matrix in np.concatenate((parent_training, parent_withheld), axis=0)
        )
        energy_defects.append(
            abs(retained.external_gap_minimum.magnitude - expected_gap)
        )
        dimensionless_defects.extend(
            (
                abs(
                    retained.transport.minimum_overlap_singular_value - minimum_overlap
                ),
                self._maximum(
                    np.asarray(retained.transport.closure_eigenphases), closure_phases
                ),
                abs(
                    retained.pointwise_alignment.projector_maximum_frobenius_defect
                    - self._projector_defect(reference_frames, attacked_frames)
                ),
                abs(
                    retained.attack_frame_maximum_frobenius_defect
                    - self._frame_defect(reference_frames, attacked_frames)
                ),
                abs(
                    retained.pointwise_alignment.frame_maximum_frobenius_defect
                    - self._frame_defect(reference_frames, aligned_frames)
                ),
                abs(
                    retained.pointwise_rotation_recovery_maximum_frobenius_defect
                    - float(
                        max(
                            np.linalg.norm(rotation - attack.conj().T)
                            for rotation, attack in zip(rotations, attacks, strict=True)
                        )
                    )
                ),
                self._maximum(
                    retained.constrained_rotation.magnitude, constrained_rotation
                ),
                abs(
                    retained.constrained_frame_maximum_frobenius_defect
                    - self._frame_defect(reference_frames, constrained_frames)
                ),
            )
        )
        energy_defects.extend(
            (
                abs(
                    retained.attacked_operator_maximum_frobenius_defect.magnitude
                    - self._frame_defect(reference_operators, attacked_operators)
                ),
                abs(
                    retained.pointwise_operator_maximum_frobenius_defect.magnitude
                    - self._frame_defect(reference_operators, aligned_operators)
                ),
                abs(
                    retained.constrained_operator_maximum_frobenius_defect.magnitude
                    - self._frame_defect(reference_operators, constrained_operators)
                ),
            )
        )
        for transform, hermiticity, expected_blocks, expected_samples in (
            (
                calculation.reference_transform,
                calculation.reference_hermiticity,
                reference_blocks,
                reference_operators,
            ),
            (
                calculation.attacked_transform,
                calculation.attacked_hermiticity,
                attacked_blocks,
                attacked_operators,
            ),
            (
                calculation.aligned_transform,
                calculation.aligned_hermiticity,
                aligned_blocks,
                aligned_operators,
            ),
        ):
            retained_blocks = np.asarray(
                [block.magnitude for block in transform.hopping_model.hopping_blocks],
                dtype=np.complex128,
            )
            energy_defects.append(self._maximum(retained_blocks, expected_blocks))
            reconstructed = self._interpolate(
                training_reduced, representatives, expected_blocks
            )
            expected_reconstruction = self._frame_defect(
                reconstructed, expected_samples
            )
            energy_defects.append(
                abs(
                    transform.reconstruction_maximum_frobenius_error
                    - expected_reconstruction
                )
            )
            expected_paired, expected_missing, expected_hermiticity = self._hermiticity(
                representatives,
                expected_blocks,
                definition.reciprocal_mesh_size,
            )
            dimensionless_defects.extend(
                (
                    0.0
                    if hermiticity.representative_modulus
                    == definition.reciprocal_mesh_size
                    else 1.0,
                    0.0
                    if hermiticity.paired_representatives == expected_paired
                    else 1.0,
                    0.0
                    if hermiticity.missing_opposite_representatives == expected_missing
                    else 1.0,
                    0.0
                    if hermiticity.passes
                    is (
                        not expected_missing
                        and expected_hermiticity
                        <= definition.hermiticity_absolute_tolerance.magnitude
                    )
                    else 1.0,
                )
            )
            energy_defects.extend(
                (
                    abs(
                        hermiticity.maximum_frobenius_defect.magnitude
                        - expected_hermiticity
                    ),
                    abs(
                        hermiticity.absolute_tolerance.magnitude
                        - definition.hermiticity_absolute_tolerance.magnitude
                    ),
                )
            )
        self._range_defects(
            calculation,
            representatives,
            training_reduced,
            withheld_reduced,
            training_eigenvalues,
            withheld_eigenvalues,
            reference_blocks,
            attacked_blocks,
            aligned_blocks,
            energy_defects,
        )
        tolerance = definition.verification_absolute_tolerance
        dimensionless = max(dimensionless_defects, default=0.0)
        energy = max(energy_defects, default=0.0)
        result = Periodic1DMultibandAlignmentVerificationResult(
            calculation,
            float(dimensionless),
            ScalarQuantity(energy, parent.hopping_blocks[0].unit),
            tolerance,
            dimensionless <= tolerance and energy <= tolerance,
        )
        return result

    def _range_defects(
        self,
        calculation: Periodic1DMultibandAlignmentCalculationResult,
        representatives: np.ndarray,
        training_reduced: np.ndarray,
        withheld_reduced: np.ndarray,
        training_target: np.ndarray,
        withheld_target: np.ndarray,
        reference_blocks: np.ndarray,
        attacked_blocks: np.ndarray,
        aligned_blocks: np.ndarray,
        defects: list[float],
    ) -> None:
        """Append reconstructed omitted-block and spectral range defects."""
        for result in calculation.range_study:
            keep = np.abs(representatives) <= result.maximum_range
            for truncation, training_error, withheld_error, blocks in (
                (
                    result.reference_truncation,
                    result.reference_training_error,
                    result.reference_withheld_error,
                    reference_blocks,
                ),
                (
                    result.attacked_truncation,
                    result.attacked_training_error,
                    result.attacked_withheld_error,
                    attacked_blocks,
                ),
                (
                    result.aligned_truncation,
                    result.aligned_training_error,
                    result.aligned_withheld_error,
                    aligned_blocks,
                ),
            ):
                omitted = float(np.linalg.norm(blocks[~keep]))
                training_matrices = self._interpolate(
                    training_reduced, representatives[keep], blocks[keep]
                )
                withheld_matrices = self._interpolate(
                    withheld_reduced, representatives[keep], blocks[keep]
                )
                expected_training = self._spectral_error(
                    training_matrices, training_target
                )
                expected_withheld = self._spectral_error(
                    withheld_matrices, withheld_target
                )
                defects.extend(
                    (
                        abs(truncation.omitted_block_l2_norm - omitted),
                        abs(
                            training_error.maximum_absolute_error.magnitude
                            - expected_training
                        ),
                        abs(
                            withheld_error.maximum_absolute_error.magnitude
                            - expected_withheld
                        ),
                    )
                )

    @staticmethod
    def _hermiticity(
        representatives: np.ndarray,
        blocks: np.ndarray,
        modulus: int,
    ) -> tuple[tuple[int, ...], tuple[int, ...], float]:
        """Reconstruct periodic opposite pairs and the maximum Hermiticity defect."""
        lookup = {
            int(representative): index
            for index, representative in enumerate(representatives)
        }
        paired: list[int] = []
        missing: list[int] = []
        defects: list[float] = []
        for index, raw_representative in enumerate(representatives):
            representative = int(raw_representative)
            opposite = -representative
            if opposite not in lookup:
                candidates = tuple(
                    int(value)
                    for value in representatives
                    if (int(value) + representative) % modulus == 0
                )
                if len(candidates) != 1:
                    missing.append(representative)
                    continue
                opposite = candidates[0]
            paired.append(representative)
            defects.append(
                float(np.linalg.norm(blocks[index] - blocks[lookup[opposite]].conj().T))
            )
        return tuple(sorted(paired)), tuple(sorted(missing)), max(defects, default=0.0)

    @staticmethod
    def _interpolate_parent(
        parent: BlockHoppingModel1D, reduced: np.ndarray
    ) -> np.ndarray:
        """Interpolate the finite parent hopping model at reduced coordinates."""
        if type(parent) is not BlockHoppingModel1D:
            raise TypeError("parent must be BlockHoppingModel1D")
        representatives = np.asarray(parent.representatives, dtype=np.int64)
        blocks = np.asarray(
            [block.magnitude for block in parent.hopping_blocks],
            dtype=np.complex128,
        )
        return Periodic1DMultibandAlignmentResultVerifier._interpolate(
            reduced, representatives, blocks
        )

    @staticmethod
    def _eigensystem(
        matrices: np.ndarray, retained_rank: int
    ) -> tuple[np.ndarray, np.ndarray]:
        """Return ascending retained eigenvalues and raw orthonormal frames."""
        eigenvalues: list[np.ndarray] = []
        frames: list[np.ndarray] = []
        for matrix in matrices:
            values, vectors = np.linalg.eigh(matrix)
            eigenvalues.append(values[:retained_rank])
            frames.append(vectors[:, :retained_rank])
        return (
            np.asarray(eigenvalues, dtype=np.float64),
            np.asarray(frames, dtype=np.complex128),
        )

    @staticmethod
    def _transport(raw: np.ndarray) -> tuple[np.ndarray, float, np.ndarray]:
        """Reconstruct neighbor polar transport and distributed closure holonomy."""
        transported = [raw[0].copy()]
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

    @staticmethod
    def _attacks(
        definition: Periodic1DMultibandAlignmentCalculationDefinition,
        reduced: np.ndarray,
    ) -> np.ndarray:
        """Evaluate the frozen rank-two sine-series rotation attack."""
        if type(definition) is not Periodic1DMultibandAlignmentCalculationDefinition:
            raise TypeError("definition has the wrong type")
        rotations: list[np.ndarray] = []
        for momentum in reduced:
            angle = definition.attack_constant_angle + sum(
                coefficient * np.sin(2.0 * np.pi * harmonic * float(momentum))
                for harmonic, coefficient in enumerate(
                    definition.attack_sine_coefficients, start=1
                )
            )
            rotations.append(
                np.asarray(
                    [
                        [np.cos(angle), -np.sin(angle)],
                        [np.sin(angle), np.cos(angle)],
                    ],
                    dtype=np.complex128,
                )
            )
        return np.asarray(rotations, dtype=np.complex128)

    @staticmethod
    def _pointwise_align(
        reference: np.ndarray, candidate: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray]:
        """Solve independent pointwise unitary Procrustes problems."""
        rotations: list[np.ndarray] = []
        aligned: list[np.ndarray] = []
        for left_frame, right_frame in zip(reference, candidate, strict=True):
            left, _, right_h = np.linalg.svd(right_frame.conj().T @ left_frame)
            rotation = left @ right_h
            rotations.append(rotation)
            aligned.append(right_frame @ rotation)
        return (
            np.asarray(rotations, dtype=np.complex128),
            np.asarray(aligned, dtype=np.complex128),
        )

    @staticmethod
    def _global_rotation(reference: np.ndarray, candidate: np.ndarray) -> np.ndarray:
        """Solve the aggregate one-global-unitary Procrustes problem."""
        aggregate = np.sum(
            np.einsum("kji,kjl->kil", candidate.conj(), reference), axis=0
        )
        left, _, right_h = np.linalg.svd(aggregate)
        return np.asarray(left @ right_h, dtype=np.complex128)

    @staticmethod
    def _project(parent: np.ndarray, frames: np.ndarray) -> np.ndarray:
        """Represent each parent matrix in its identified retained frame."""
        return np.asarray(
            [
                frame.conj().T @ matrix @ frame
                for matrix, frame in zip(parent, frames, strict=True)
            ],
            dtype=np.complex128,
        )

    @staticmethod
    def _fourier(
        reduced: np.ndarray, matrices: np.ndarray, representatives: np.ndarray
    ) -> np.ndarray:
        """Apply the normalized discrete Fourier transform to matrix samples."""
        return np.asarray(
            [
                np.mean(
                    matrices
                    * np.exp(-2j * np.pi * reduced * int(representative))[
                        :, None, None
                    ],
                    axis=0,
                )
                for representative in representatives
            ],
            dtype=np.complex128,
        )

    @staticmethod
    def _interpolate(
        reduced: np.ndarray, representatives: np.ndarray, blocks: np.ndarray
    ) -> np.ndarray:
        """Interpolate matrix hopping blocks at reduced coordinates."""
        phases = np.exp(2j * np.pi * np.outer(reduced, representatives))
        return np.asarray(
            np.einsum("kr,rij->kij", phases, blocks, optimize=True),
            dtype=np.complex128,
        )

    @staticmethod
    def _projector_defect(reference: np.ndarray, candidate: np.ndarray) -> float:
        """Return the maximum invariant retained-projector Frobenius defect."""
        return float(
            max(
                np.linalg.norm(left @ left.conj().T - right @ right.conj().T)
                for left, right in zip(reference, candidate, strict=True)
            )
        )

    @staticmethod
    def _frame_defect(reference: np.ndarray, candidate: np.ndarray) -> float:
        """Return the maximum frame or represented-matrix Frobenius defect."""
        return float(
            max(
                np.linalg.norm(left - right)
                for left, right in zip(reference, candidate, strict=True)
            )
        )

    @staticmethod
    def _spectral_error(matrices: np.ndarray, target: np.ndarray) -> float:
        """Return the maximum ordered-eigenvalue defect against a common target."""
        values = np.asarray(
            [np.linalg.eigvalsh(matrix) for matrix in matrices], dtype=np.float64
        )
        return float(np.max(np.abs(values - target)))

    @staticmethod
    def _maximum(left: np.ndarray, right: np.ndarray) -> float:
        """Return the elementwise maximum absolute array defect."""
        return float(np.max(np.abs(left - right)))


__all__ = [
    "Periodic1DMultibandAlignmentResultVerifier",
    "Periodic1DMultibandAlignmentVerificationResult",
]
