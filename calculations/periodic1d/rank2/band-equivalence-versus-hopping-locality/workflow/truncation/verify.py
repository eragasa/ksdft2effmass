"""Independent verification for finite-range non-flat consequences."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from .._validation import _finite_float
from ..nonflat.verify import SmoothFourStateVerifier
from .definition import SmoothFourStateTruncationDefinition
from .results import (
    SmoothFourStateTruncationPointResult,
    SmoothFourStateTruncationRangeResult,
    SmoothFourStateTruncationResult,
)

ComplexArray = npt.NDArray[np.complex128]
RealArray = npt.NDArray[np.float64]


def _optional_range(name: str, value: int | None) -> None:
    if value is None:
        return
    if type(value) is not int:
        raise TypeError(f"{name} must be a built-in int or None")
    if value < 0:
        raise ValueError(f"{name} must be nonnegative")


@dataclass(frozen=True, slots=True)
class SmoothFourStateTruncationRangeDecision:
    """Retain independently reconstructed first-passing declared cutoffs."""

    amplitude: float
    tolerance: float
    reference_band_first_passing_range: int | None
    comparison_band_first_passing_range: int | None
    reference_hamiltonian_first_passing_range: int | None
    comparison_hamiltonian_first_passing_range: int | None

    def __post_init__(self) -> None:
        """Require positive finite controls and optional nonnegative cutoffs."""
        _finite_float("amplitude", self.amplitude)
        _finite_float("tolerance", self.tolerance)
        if self.amplitude < 0.0:
            raise ValueError("amplitude must be nonnegative")
        if self.tolerance <= 0.0:
            raise ValueError("tolerance must be positive")
        for name, value in (
            (
                "reference_band_first_passing_range",
                self.reference_band_first_passing_range,
            ),
            (
                "comparison_band_first_passing_range",
                self.comparison_band_first_passing_range,
            ),
            (
                "reference_hamiltonian_first_passing_range",
                self.reference_hamiltonian_first_passing_range,
            ),
            (
                "comparison_hamiltonian_first_passing_range",
                self.comparison_hamiltonian_first_passing_range,
            ),
        ):
            _optional_range(name, value)

    @property
    def band_range_inflation(self) -> int | None:
        """Return comparison-minus-reference band range when both ranges resolve."""
        if (
            self.reference_band_first_passing_range is None
            or self.comparison_band_first_passing_range is None
        ):
            return None
        return (
            self.comparison_band_first_passing_range
            - self.reference_band_first_passing_range
        )

    @property
    def hamiltonian_range_inflation(self) -> int | None:
        """Return comparison-minus-reference matrix range when both ranges resolve."""
        if (
            self.reference_hamiltonian_first_passing_range is None
            or self.comparison_hamiltonian_first_passing_range is None
        ):
            return None
        return (
            self.comparison_hamiltonian_first_passing_range
            - self.reference_hamiltonian_first_passing_range
        )


@dataclass(frozen=True, slots=True)
class SmoothFourStateTruncationVerificationResult:
    """Report independent reconstruction and declared-range decisions."""

    experiment_result: SmoothFourStateTruncationResult
    passes: bool
    absolute_tolerance: float
    maximum_absolute_discrepancy: float
    inventory_is_dense: bool
    decisions: tuple[SmoothFourStateTruncationRangeDecision, ...]

    def __post_init__(self) -> None:
        """Validate the verification decision and immutable decision inventory."""
        if type(self.experiment_result) is not SmoothFourStateTruncationResult:
            raise TypeError("experiment_result must be SmoothFourStateTruncationResult")
        if type(self.passes) is not bool:
            raise TypeError("passes must be a built-in bool")
        if type(self.inventory_is_dense) is not bool:
            raise TypeError("inventory_is_dense must be a built-in bool")
        _finite_float("absolute_tolerance", self.absolute_tolerance)
        _finite_float("maximum_absolute_discrepancy", self.maximum_absolute_discrepancy)
        if self.absolute_tolerance <= 0.0:
            raise ValueError("absolute_tolerance must be positive")
        if self.maximum_absolute_discrepancy < 0.0:
            raise ValueError("maximum_absolute_discrepancy must be nonnegative")
        if self.passes is not (
            self.maximum_absolute_discrepancy <= self.absolute_tolerance
        ):
            raise ValueError("passes must match the maximum discrepancy")
        if type(self.decisions) is not tuple or any(
            type(item) is not SmoothFourStateTruncationRangeDecision
            for item in self.decisions
        ):
            raise TypeError("decisions must contain truncation range decisions")


class SmoothFourStateTruncationVerifier:
    """Reconstruct truncation channels without calling the producing action.

    The verifier directly rebuilds the parent frame, finite Fourier blocks, ordinary
    lattice conversion, range truncations, Bloch matrices, Hermitian spectra, error
    channels, and first-passing decisions.  It intentionally does not call
    :class:`SmoothFourStateTruncationExperiment` or PhysKit's range-family evaluator.
    """

    __slots__ = ()

    def execute(
        self,
        retained: SmoothFourStateTruncationResult,
        decision_tolerances: tuple[float, ...],
    ) -> SmoothFourStateTruncationVerificationResult:
        """Verify one result and independently select declared first-passing ranges."""
        if type(retained) is not SmoothFourStateTruncationResult:
            raise TypeError("retained must be SmoothFourStateTruncationResult")
        self._validate_tolerances(decision_tolerances)
        expected = self._reconstruct(retained.definition)
        maximum = max(self._result_discrepancies(expected, retained), default=0.0)
        tolerance = retained.definition.model.verification_absolute_tolerance
        decisions = self._decisions(expected, decision_tolerances)
        return SmoothFourStateTruncationVerificationResult(
            experiment_result=retained,
            passes=maximum <= tolerance,
            absolute_tolerance=tolerance,
            maximum_absolute_discrepancy=float(maximum),
            inventory_is_dense=retained.definition.has_dense_integer_inventory,
            decisions=decisions,
        )

    @staticmethod
    def _validate_tolerances(tolerances: tuple[float, ...]) -> None:
        if type(tolerances) is not tuple or not tolerances:
            raise TypeError("decision_tolerances must be a nonempty tuple")
        for value in tolerances:
            if type(value) is not float:
                raise TypeError("decision_tolerances must contain built-in floats")
            _finite_float("decision_tolerance", value)
            if value <= 0.0:
                raise ValueError("decision_tolerances must be positive")
        if tolerances != tuple(sorted(set(tolerances), reverse=True)):
            raise ValueError(
                "decision_tolerances must be unique and strictly decreasing"
            )

    @classmethod
    def _reconstruct(
        cls, definition: SmoothFourStateTruncationDefinition
    ) -> SmoothFourStateTruncationResult:
        model = definition.model
        sample_count = model.reciprocal_mesh_size
        construction_coordinates = -0.5 + np.arange(
            sample_count, dtype=np.float64
        ) / float(sample_count)
        parent_matrices = SmoothFourStateVerifier._parent(
            construction_coordinates, model.parent_hopping_scale
        )
        _, eigenvectors = np.linalg.eigh(parent_matrices)
        frames = SmoothFourStateVerifier._frame(eigenvectors[:, :, :2], model)[0]
        construction_reference = np.asarray(
            [
                frame.conj().T @ matrix @ frame
                for frame, matrix in zip(frames, parent_matrices, strict=True)
            ],
            dtype=np.complex128,
        )
        independent_parent = SmoothFourStateVerifier._reconstruct(model)
        cyclic_displacements = tuple(range(-(sample_count // 2), sample_count // 2))
        cyclic_reference_blocks = SmoothFourStateVerifier._blocks(
            construction_coordinates,
            construction_reference,
            cyclic_displacements,
        )
        nyquist = -(sample_count // 2)
        ordinary_displacements = tuple(
            displacement
            for displacement in cyclic_displacements
            if displacement != nyquist
        )
        ordinary_reference_blocks = np.asarray(
            [
                block
                for displacement, block in zip(
                    cyclic_displacements,
                    cyclic_reference_blocks,
                    strict=True,
                )
                if displacement != nyquist
            ],
            dtype=np.complex128,
        )
        reference_nyquist_power = cls._block_power(
            cyclic_reference_blocks[cyclic_displacements.index(nyquist)]
        )
        evaluation_coordinates, coordinate_offset = cls._evaluation_coordinates(
            definition
        )
        separation = cls._minimum_periodic_separation(
            construction_coordinates, evaluation_coordinates
        )
        reference_full = cls._evaluate_blocks(
            ordinary_displacements,
            ordinary_reference_blocks,
            evaluation_coordinates,
        )
        reference_eigenvalues = cls._eigenvalues(
            reference_full, model.frame_absolute_tolerance
        )
        reference_ordinary_hermiticity = cls._hopping_hermiticity_discrepancy(
            ordinary_displacements, ordinary_reference_blocks
        )

        points = tuple(
            cls._point(
                definition,
                construction_coordinates,
                construction_reference,
                cyclic_displacements,
                ordinary_displacements,
                reference_full,
                reference_eigenvalues,
                ordinary_reference_blocks,
                reference_nyquist_power,
                reference_ordinary_hermiticity,
                evaluation_coordinates,
                amplitude,
            )
            for amplitude in model.amplitudes
        )
        return SmoothFourStateTruncationResult(
            definition=definition,
            minimum_external_gap=independent_parent.minimum_external_gap,
            minimum_transport_singular_value=(
                independent_parent.minimum_transport_singular_value
            ),
            maximum_transport_procrustes_residual=(
                independent_parent.maximum_transport_procrustes_residual
            ),
            maximum_transport_unitarity_defect=(
                independent_parent.maximum_transport_unitarity_defect
            ),
            maximum_transport_rank_cutoff=(
                independent_parent.maximum_transport_rank_cutoff
            ),
            closure_holonomy_phases=independent_parent.closure_holonomy_phases,
            closure_holonomy_unitarity_defect=(
                independent_parent.closure_holonomy_unitarity_defect
            ),
            maximum_frame_orthonormality_defect=(
                independent_parent.maximum_frame_orthonormality_defect
            ),
            periodic_closure_defect=independent_parent.periodic_closure_defect,
            maximum_reference_hermiticity_defect=(
                independent_parent.maximum_reference_hermiticity_defect
            ),
            evaluation_coordinate_offset=coordinate_offset,
            minimum_construction_evaluation_separation=separation,
            points=points,
        )

    @classmethod
    def _point(
        cls,
        definition: SmoothFourStateTruncationDefinition,
        construction_coordinates: RealArray,
        construction_reference: ComplexArray,
        cyclic_displacements: tuple[int, ...],
        ordinary_displacements: tuple[int, ...],
        reference_full: ComplexArray,
        reference_eigenvalues: RealArray,
        ordinary_reference_blocks: ComplexArray,
        reference_nyquist_power: float,
        reference_ordinary_hermiticity: float,
        evaluation_coordinates: RealArray,
        amplitude: float,
    ) -> SmoothFourStateTruncationPointResult:
        construction_comparison = cls._rotate(
            construction_coordinates, construction_reference, amplitude
        )
        cyclic_comparison_blocks = SmoothFourStateVerifier._blocks(
            construction_coordinates,
            construction_comparison,
            cyclic_displacements,
        )
        nyquist = -(definition.model.reciprocal_mesh_size // 2)
        comparison_nyquist_power = cls._block_power(
            cyclic_comparison_blocks[cyclic_displacements.index(nyquist)]
        )
        ordinary_comparison_blocks = np.asarray(
            [
                block
                for displacement, block in zip(
                    cyclic_displacements,
                    cyclic_comparison_blocks,
                    strict=True,
                )
                if displacement != nyquist
            ],
            dtype=np.complex128,
        )
        comparison_full = cls._evaluate_blocks(
            ordinary_displacements,
            ordinary_comparison_blocks,
            evaluation_coordinates,
        )
        comparison_full_eigenvalues = cls._eigenvalues(
            comparison_full, definition.model.frame_absolute_tolerance
        )
        direct_comparison = cls._rotate(
            evaluation_coordinates, reference_full, amplitude
        )
        direct_eigenvalues = cls._eigenvalues(
            direct_comparison, definition.model.frame_absolute_tolerance
        )
        direct_difference = direct_eigenvalues - reference_eigenvalues
        interpolation_matrix_difference = comparison_full - direct_comparison
        interpolation_difference = comparison_full_eigenvalues - direct_eigenvalues
        interpolation_maximum, interpolation_rms = cls._hamiltonian_errors(
            interpolation_matrix_difference
        )

        ranges = tuple(
            cls._range(
                maximum_range,
                ordinary_displacements,
                ordinary_reference_blocks,
                ordinary_comparison_blocks,
                reference_full,
                reference_eigenvalues,
                comparison_full,
                comparison_full_eigenvalues,
                direct_comparison,
                direct_eigenvalues,
                reference_nyquist_power,
                comparison_nyquist_power,
                evaluation_coordinates,
                definition.model.frame_absolute_tolerance,
            )
            for maximum_range in definition.maximum_ranges
        )
        return SmoothFourStateTruncationPointResult(
            amplitude=amplitude,
            reference_nyquist_power=reference_nyquist_power,
            comparison_nyquist_power=comparison_nyquist_power,
            reference_maximum_ordinary_hermiticity_defect=(
                reference_ordinary_hermiticity
            ),
            comparison_maximum_ordinary_hermiticity_defect=(
                cls._hopping_hermiticity_discrepancy(
                    ordinary_displacements, ordinary_comparison_blocks
                )
            ),
            maximum_direct_band_defect=float(np.max(np.abs(direct_difference))),
            comparison_maximum_interpolation_hamiltonian_error=interpolation_maximum,
            comparison_rms_interpolation_hamiltonian_error=interpolation_rms,
            comparison_maximum_interpolation_band_error=float(
                np.max(np.abs(interpolation_difference))
            ),
            comparison_rms_interpolation_band_error=cls._rms(interpolation_difference),
            ranges=ranges,
        )

    @classmethod
    def _range(
        cls,
        maximum_range: int,
        displacements: tuple[int, ...],
        reference_blocks: ComplexArray,
        comparison_blocks: ComplexArray,
        reference_full: ComplexArray,
        reference_eigenvalues: RealArray,
        comparison_full: ComplexArray,
        comparison_full_eigenvalues: RealArray,
        direct_comparison: ComplexArray,
        direct_eigenvalues: RealArray,
        reference_nyquist_power: float,
        comparison_nyquist_power: float,
        evaluation_coordinates: RealArray,
        hermiticity_tolerance: float,
    ) -> SmoothFourStateTruncationRangeResult:
        mask = np.asarray(
            [abs(displacement) <= maximum_range for displacement in displacements],
            dtype=np.bool_,
        )
        selected_displacements = tuple(
            displacement
            for displacement, include in zip(displacements, mask, strict=True)
            if bool(include)
        )
        selected_reference_blocks = reference_blocks[mask]
        selected_comparison_blocks = comparison_blocks[mask]
        reference_truncated = cls._evaluate_blocks(
            selected_displacements,
            selected_reference_blocks,
            evaluation_coordinates,
        )
        comparison_truncated = cls._evaluate_blocks(
            selected_displacements,
            selected_comparison_blocks,
            evaluation_coordinates,
        )
        reference_truncated_eigenvalues = cls._eigenvalues(
            reference_truncated, hermiticity_tolerance
        )
        comparison_truncated_eigenvalues = cls._eigenvalues(
            comparison_truncated, hermiticity_tolerance
        )

        reference_matrix_difference = reference_truncated - reference_full
        reference_difference = reference_truncated_eigenvalues - reference_eigenvalues
        comparison_truncation_matrix_difference = comparison_truncated - comparison_full
        comparison_truncation_difference = (
            comparison_truncated_eigenvalues - comparison_full_eigenvalues
        )
        comparison_total_matrix_difference = comparison_truncated - direct_comparison
        comparison_total_difference = (
            comparison_truncated_eigenvalues - direct_eigenvalues
        )
        reference_maximum, reference_rms = cls._hamiltonian_errors(
            reference_matrix_difference
        )
        comparison_truncation_maximum, comparison_truncation_rms = (
            cls._hamiltonian_errors(comparison_truncation_matrix_difference)
        )
        comparison_total_maximum, comparison_total_rms = cls._hamiltonian_errors(
            comparison_total_matrix_difference
        )
        reference_ordinary_power = math.fsum(
            cls._block_power(block)
            for displacement, block in zip(displacements, reference_blocks, strict=True)
            if abs(displacement) > maximum_range
        )
        comparison_ordinary_power = math.fsum(
            cls._block_power(block)
            for displacement, block in zip(
                displacements, comparison_blocks, strict=True
            )
            if abs(displacement) > maximum_range
        )
        return SmoothFourStateTruncationRangeResult(
            maximum_range=maximum_range,
            reference_ordinary_omitted_power=reference_ordinary_power,
            comparison_ordinary_omitted_power=comparison_ordinary_power,
            reference_total_omitted_power=(
                reference_ordinary_power + reference_nyquist_power
            ),
            comparison_total_omitted_power=(
                comparison_ordinary_power + comparison_nyquist_power
            ),
            reference_maximum_truncation_hamiltonian_error=reference_maximum,
            reference_rms_truncation_hamiltonian_error=reference_rms,
            reference_maximum_band_error=float(np.max(np.abs(reference_difference))),
            reference_rms_band_error=cls._rms(reference_difference),
            comparison_maximum_truncation_hamiltonian_error=(
                comparison_truncation_maximum
            ),
            comparison_rms_truncation_hamiltonian_error=comparison_truncation_rms,
            comparison_maximum_truncation_band_error=float(
                np.max(np.abs(comparison_truncation_difference))
            ),
            comparison_rms_truncation_band_error=cls._rms(
                comparison_truncation_difference
            ),
            comparison_maximum_total_hamiltonian_error=comparison_total_maximum,
            comparison_rms_total_hamiltonian_error=comparison_total_rms,
            comparison_maximum_total_band_error=float(
                np.max(np.abs(comparison_total_difference))
            ),
            comparison_rms_total_band_error=cls._rms(comparison_total_difference),
        )

    @staticmethod
    def _evaluation_coordinates(
        definition: SmoothFourStateTruncationDefinition,
    ) -> tuple[RealArray, float]:
        offset = 1.0 / float(definition.model.reciprocal_mesh_size + 1)
        coordinates = -0.5 + (
            np.arange(definition.evaluation_mesh_size, dtype=np.float64) + offset
        ) / float(definition.evaluation_mesh_size)
        return coordinates, offset

    @staticmethod
    def _minimum_periodic_separation(
        construction: RealArray, evaluation: RealArray
    ) -> float:
        differences = np.abs(evaluation[:, None] - construction[None, :])
        return float(np.min(np.minimum(differences, 1.0 - differences)))

    @staticmethod
    def _rotate(
        coordinates: RealArray, matrices: ComplexArray, amplitude: float
    ) -> ComplexArray:
        angles = amplitude * np.sin(2.0 * np.pi * coordinates)
        rotations = np.asarray(
            [
                [
                    [math.cos(angle), -math.sin(angle)],
                    [math.sin(angle), math.cos(angle)],
                ]
                for angle in angles
            ],
            dtype=np.complex128,
        )
        return np.asarray(
            [
                rotation.conj().T @ matrix @ rotation
                for rotation, matrix in zip(rotations, matrices, strict=True)
            ],
            dtype=np.complex128,
        )

    @staticmethod
    def _evaluate_blocks(
        displacements: tuple[int, ...],
        blocks: ComplexArray,
        coordinates: RealArray,
    ) -> ComplexArray:
        if len(displacements) != blocks.shape[0]:
            raise ValueError("displacements and blocks must have the same length")
        phases = np.exp(
            2.0j
            * np.pi
            * coordinates[:, None]
            * np.asarray(displacements, dtype=np.float64)[None, :]
        )
        return np.einsum("qr,rij->qij", phases, blocks, optimize=True)

    @staticmethod
    def _eigenvalues(matrices: ComplexArray, tolerance: float) -> RealArray:
        discrepancy = float(
            np.max(np.abs(matrices - matrices.conj().transpose(0, 2, 1)))
        )
        if discrepancy > tolerance:
            raise FloatingPointError("independent Bloch matrices are not Hermitian")
        return np.asarray(np.linalg.eigvalsh(matrices), dtype=np.float64)

    @staticmethod
    def _hopping_hermiticity_discrepancy(
        displacements: tuple[int, ...], blocks: ComplexArray
    ) -> float:
        mapping = {
            displacement: block
            for displacement, block in zip(displacements, blocks, strict=True)
        }
        if set(mapping) != {-displacement for displacement in mapping}:
            raise ValueError("ordinary hopping inventory is not conjugate closed")
        return max(
            float(np.linalg.norm(block - mapping[-displacement].conj().T))
            for displacement, block in mapping.items()
        )

    @staticmethod
    def _block_power(block: npt.NDArray[np.complex128]) -> float:
        return float(np.vdot(block, block).real / 2.0)

    @staticmethod
    def _hamiltonian_errors(matrix_differences: ComplexArray) -> tuple[float, float]:
        powers = np.sum(np.abs(matrix_differences) ** 2, axis=(1, 2))
        norms = np.sqrt(powers)
        return (
            float(np.max(norms) / math.sqrt(2.0)),
            math.sqrt(float(np.mean(powers)) / 2.0),
        )

    @staticmethod
    def _rms(values: RealArray) -> float:
        return math.sqrt(float(np.mean(np.square(values))))

    @classmethod
    def _decisions(
        cls,
        expected: SmoothFourStateTruncationResult,
        tolerances: tuple[float, ...],
    ) -> tuple[SmoothFourStateTruncationRangeDecision, ...]:
        return tuple(
            SmoothFourStateTruncationRangeDecision(
                amplitude=point.amplitude,
                tolerance=tolerance,
                reference_band_first_passing_range=cls._first_passing(
                    point, tolerance, "reference_band"
                ),
                comparison_band_first_passing_range=cls._first_passing(
                    point, tolerance, "comparison_band"
                ),
                reference_hamiltonian_first_passing_range=cls._first_passing(
                    point, tolerance, "reference_hamiltonian"
                ),
                comparison_hamiltonian_first_passing_range=cls._first_passing(
                    point, tolerance, "comparison_hamiltonian"
                ),
            )
            for point in expected.points
            for tolerance in tolerances
        )

    @staticmethod
    def _first_passing(
        point: SmoothFourStateTruncationPointResult,
        tolerance: float,
        channel: str,
    ) -> int | None:
        for item in point.ranges:
            if channel == "reference_band":
                value = item.reference_maximum_band_error
            elif channel == "comparison_band":
                value = item.comparison_maximum_total_band_error
            elif channel == "reference_hamiltonian":
                value = item.reference_maximum_truncation_hamiltonian_error
            elif channel == "comparison_hamiltonian":
                value = item.comparison_maximum_total_hamiltonian_error
            else:
                raise ValueError("unknown range-decision channel")
            if value <= tolerance:
                return item.maximum_range
        return None

    @classmethod
    def _result_discrepancies(
        cls,
        expected: SmoothFourStateTruncationResult,
        retained: SmoothFourStateTruncationResult,
    ) -> list[float]:
        discrepancies = [
            abs(expected.minimum_external_gap - retained.minimum_external_gap),
            abs(
                expected.minimum_transport_singular_value
                - retained.minimum_transport_singular_value
            ),
            abs(
                expected.maximum_transport_procrustes_residual
                - retained.maximum_transport_procrustes_residual
            ),
            abs(
                expected.maximum_transport_unitarity_defect
                - retained.maximum_transport_unitarity_defect
            ),
            abs(
                expected.maximum_transport_rank_cutoff
                - retained.maximum_transport_rank_cutoff
            ),
            abs(
                expected.closure_holonomy_unitarity_defect
                - retained.closure_holonomy_unitarity_defect
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
            abs(
                expected.evaluation_coordinate_offset
                - retained.evaluation_coordinate_offset
            ),
            abs(
                expected.minimum_construction_evaluation_separation
                - retained.minimum_construction_evaluation_separation
            ),
        ]
        discrepancies.extend(
            cls._sequence_discrepancies(
                expected.closure_holonomy_phases,
                retained.closure_holonomy_phases,
            )
        )
        if len(expected.points) != len(retained.points):
            discrepancies.append(math.inf)
            return discrepancies
        for expected_point, retained_point in zip(
            expected.points, retained.points, strict=True
        ):
            discrepancies.extend(
                cls._point_discrepancies(expected_point, retained_point)
            )
        return discrepancies

    @classmethod
    def _point_discrepancies(
        cls,
        expected: SmoothFourStateTruncationPointResult,
        retained: SmoothFourStateTruncationPointResult,
    ) -> list[float]:
        discrepancies = [
            abs(expected.amplitude - retained.amplitude),
            abs(expected.reference_nyquist_power - retained.reference_nyquist_power),
            abs(expected.comparison_nyquist_power - retained.comparison_nyquist_power),
            abs(
                expected.reference_maximum_ordinary_hermiticity_defect
                - retained.reference_maximum_ordinary_hermiticity_defect
            ),
            abs(
                expected.comparison_maximum_ordinary_hermiticity_defect
                - retained.comparison_maximum_ordinary_hermiticity_defect
            ),
            abs(
                expected.maximum_direct_band_defect
                - retained.maximum_direct_band_defect
            ),
            abs(
                expected.comparison_maximum_interpolation_hamiltonian_error
                - retained.comparison_maximum_interpolation_hamiltonian_error
            ),
            abs(
                expected.comparison_rms_interpolation_hamiltonian_error
                - retained.comparison_rms_interpolation_hamiltonian_error
            ),
            abs(
                expected.comparison_maximum_interpolation_band_error
                - retained.comparison_maximum_interpolation_band_error
            ),
            abs(
                expected.comparison_rms_interpolation_band_error
                - retained.comparison_rms_interpolation_band_error
            ),
        ]
        if len(expected.ranges) != len(retained.ranges):
            discrepancies.append(math.inf)
            return discrepancies
        for expected_range, retained_range in zip(
            expected.ranges, retained.ranges, strict=True
        ):
            discrepancies.extend(
                cls._range_discrepancies(expected_range, retained_range)
            )
        return discrepancies

    @staticmethod
    def _range_discrepancies(
        expected: SmoothFourStateTruncationRangeResult,
        retained: SmoothFourStateTruncationRangeResult,
    ) -> list[float]:
        discrepancies = [
            0.0 if expected.maximum_range == retained.maximum_range else math.inf
        ]
        discrepancies.extend(
            (
                abs(
                    expected.reference_ordinary_omitted_power
                    - retained.reference_ordinary_omitted_power
                ),
                abs(
                    expected.comparison_ordinary_omitted_power
                    - retained.comparison_ordinary_omitted_power
                ),
                abs(
                    expected.reference_total_omitted_power
                    - retained.reference_total_omitted_power
                ),
                abs(
                    expected.comparison_total_omitted_power
                    - retained.comparison_total_omitted_power
                ),
                abs(
                    expected.reference_maximum_truncation_hamiltonian_error
                    - retained.reference_maximum_truncation_hamiltonian_error
                ),
                abs(
                    expected.reference_rms_truncation_hamiltonian_error
                    - retained.reference_rms_truncation_hamiltonian_error
                ),
                abs(
                    expected.reference_maximum_band_error
                    - retained.reference_maximum_band_error
                ),
                abs(
                    expected.reference_rms_band_error
                    - retained.reference_rms_band_error
                ),
                abs(
                    expected.comparison_maximum_truncation_hamiltonian_error
                    - retained.comparison_maximum_truncation_hamiltonian_error
                ),
                abs(
                    expected.comparison_rms_truncation_hamiltonian_error
                    - retained.comparison_rms_truncation_hamiltonian_error
                ),
                abs(
                    expected.comparison_maximum_truncation_band_error
                    - retained.comparison_maximum_truncation_band_error
                ),
                abs(
                    expected.comparison_rms_truncation_band_error
                    - retained.comparison_rms_truncation_band_error
                ),
                abs(
                    expected.comparison_maximum_total_hamiltonian_error
                    - retained.comparison_maximum_total_hamiltonian_error
                ),
                abs(
                    expected.comparison_rms_total_hamiltonian_error
                    - retained.comparison_rms_total_hamiltonian_error
                ),
                abs(
                    expected.comparison_maximum_total_band_error
                    - retained.comparison_maximum_total_band_error
                ),
                abs(
                    expected.comparison_rms_total_band_error
                    - retained.comparison_rms_total_band_error
                ),
            )
        )
        return discrepancies

    @staticmethod
    def _sequence_discrepancies(
        expected: tuple[float, ...], retained: tuple[float, ...]
    ) -> list[float]:
        if len(expected) != len(retained):
            return [math.inf]
        return [
            abs(expected_value - retained_value)
            for expected_value, retained_value in zip(expected, retained, strict=True)
        ]


__all__ = [
    "SmoothFourStateTruncationRangeDecision",
    "SmoothFourStateTruncationVerificationResult",
    "SmoothFourStateTruncationVerifier",
]
