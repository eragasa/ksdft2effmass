"""Independent reconstruction retained only for finite-angle regression."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from ksdft2effmass.operators import MODEL_SYSTEM_UNIT_CONVERTER, ScalarQuantity
from ksdft2effmass.periodic1d.multiband_alignment import (
    Periodic1DMultibandAlignmentResultVerifier,
)
from ksdft2effmass.solid_state import ReciprocalOperatorSamples1D

from .regression_definition import (
    AdmissibleSetThresholds,
    ConstrainedAdmissibleSetsExperimentDefinition,
    QuadraticLoss2D,
    _finite_float,
)
from .regression_results import (
    AdmissibleSetDisposition,
    AdmissibleSetPointEvaluation,
    ConstrainedAdmissibleSetsExperimentResult,
)


@dataclass(frozen=True, slots=True)
class ConstrainedAdmissibleSetsVerificationResult:
    """Retain independently reconstructed defects and pass disposition.

    Parameters
    ----------
    experiment_result
        Exact immutable result subjected to reconstruction.
    dimensionless_maximum_absolute_defect
        Maximum defect among geometry, loss, role, and disposition channels.
    energy_maximum_absolute_defect
        Maximum parent-energy defect among parent and locality channels.
    absolute_tolerance
        Common finite absolute acceptance tolerance.
    passes
        Derived conjunction of both defect channels meeting the tolerance.
    """

    experiment_result: ConstrainedAdmissibleSetsExperimentResult
    dimensionless_maximum_absolute_defect: float
    energy_maximum_absolute_defect: ScalarQuantity
    absolute_tolerance: float
    passes: bool

    def __post_init__(self) -> None:
        """Validate finite evidence and its derived pass flag."""
        if (
            type(self.experiment_result)
            is not ConstrainedAdmissibleSetsExperimentResult
        ):
            raise TypeError(
                "experiment_result must be ConstrainedAdmissibleSetsExperimentResult"
            )
        for name, value in (
            (
                "dimensionless_maximum_absolute_defect",
                self.dimensionless_maximum_absolute_defect,
            ),
            ("absolute_tolerance", self.absolute_tolerance),
        ):
            _finite_float(name, value)
            if value < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        if type(self.energy_maximum_absolute_defect) is not ScalarQuantity:
            raise TypeError("energy_maximum_absolute_defect must be ScalarQuantity")
        hopping_model = (
            self.experiment_result.multiband_baseline.reference_transform.hopping_model
        )
        parent_unit = hopping_model.hopping_blocks[0].unit
        if self.energy_maximum_absolute_defect.unit != parent_unit:
            raise ValueError("energy defect must use the parent energy unit")
        if self.energy_maximum_absolute_defect.magnitude < 0.0:
            raise ValueError("energy defect must be nonnegative")
        if type(self.passes) is not bool:
            raise TypeError("passes must be a built-in bool")
        expected = (
            self.dimensionless_maximum_absolute_defect <= self.absolute_tolerance
            and self.energy_maximum_absolute_defect.magnitude <= self.absolute_tolerance
        )
        if self.passes is not expected:
            raise ValueError("passes must match both defect channels and tolerance")


class ConstrainedAdmissibleSetsExperimentVerifier:
    """Reconstruct losses, evaluations, locality, and certificate geometry.

    Notes
    -----
    The verifier does not call the producer Action or Optimization solvers. It delegates
    only the composed M2 verification to M2's independent verifier, then rebuilds M3
    feature quadratics and geometry with separate direct formulas.
    """

    __slots__ = ()

    def execute(
        self, result: ConstrainedAdmissibleSetsExperimentResult
    ) -> ConstrainedAdmissibleSetsVerificationResult:
        """Reconstruct all decisive evidence and return maximum defects.

        Parameters
        ----------
        result
            Exact experiment result to verify without invoking its producer.

        Returns
        -------
        ConstrainedAdmissibleSetsVerificationResult
            Separate dimensionless and parent-energy defects with a derived pass flag.

        Raises
        ------
        TypeError
            If ``result`` is not the exact regression result type.
        """
        if type(result) is not ConstrainedAdmissibleSetsExperimentResult:
            raise TypeError("result must be ConstrainedAdmissibleSetsExperimentResult")
        baseline_verification = Periodic1DMultibandAlignmentResultVerifier().execute(
            result.multiband_baseline
        )
        defects = [
            baseline_verification.dimensionless_maximum_absolute_defect,
            0.0 if baseline_verification.passes else 1.0,
        ]
        energy_defects = [
            baseline_verification.energy_maximum_absolute_defect.magnitude
        ]
        definition = result.definition
        energy_unit = (
            result.multiband_baseline.reference_transform.hopping_model.hopping_blocks[
                0
            ].unit
        )
        energy_scale = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
            definition.loss_energy_scale, energy_unit
        ).magnitude
        reference = self._matrices(result.multiband_baseline.reference_transform.source)
        attacked = self._matrices(result.multiband_baseline.attacked_transform.source)
        spectral = self._spectral_quadratic(
            reference,
            result.multiband_baseline.training_target.eigenvalues.magnitude,
            energy_scale,
        )
        operators = tuple(
            self._operator_quadratic(reference, attacked, energy_scale, angle)
            for angle in definition.alignment_angles
        )
        self._loss_defects(result.spectral_loss, spectral, defects)
        if len(result.operator_losses) != len(operators):
            defects.append(1.0)
        else:
            for retained, expected in zip(
                result.operator_losses, operators, strict=True
            ):
                self._loss_defects(retained, expected, defects)
        self._compatible_defects(result, spectral, operators, defects, energy_defects)
        self._separated_defects(result, spectral, operators, defects, energy_defects)
        maximum = max(defects, default=0.0)
        maximum_energy = max(energy_defects, default=0.0)
        tolerance = definition.verification_absolute_tolerance
        return ConstrainedAdmissibleSetsVerificationResult(
            result,
            float(maximum),
            ScalarQuantity(float(maximum_energy), energy_unit),
            tolerance,
            maximum <= tolerance and maximum_energy <= tolerance,
        )

    def _compatible_defects(
        self,
        result: ConstrainedAdmissibleSetsExperimentResult,
        spectral: QuadraticLoss2D,
        operators: tuple[QuadraticLoss2D, ...],
        defects: list[float],
        energy_defects: list[float],
    ) -> None:
        """Reconstruct the prospective common-witness case."""
        definition = result.definition
        case = result.cases[0]
        threshold = definition.compatible_thresholds
        witness = definition.compatible_witness
        selected = self._first_minimum(
            tuple(self._squared_loss(loss, witness) for loss in operators)
        )
        expected_angles = self._feasible_angles(definition, operators, threshold)
        defects.extend(
            (
                0.0 if case.thresholds is threshold else 1.0,
                0.0
                if case.disposition is AdmissibleSetDisposition.COMPATIBLE_WITNESS
                else 1.0,
                0.0
                if case.feasible_operator_component_angles == expected_angles
                else 1.0,
                abs(case.separation_lower_bound),
                abs(case.separation_upper_bound),
                abs(case.separation_resolution - definition.separation_resolution),
            )
        )
        if case.common_witness is None:
            defects.append(1.0)
            return
        for point in (
            case.common_witness,
            case.spectral_certificate_point,
            case.operator_certificate_point,
        ):
            self._evaluation_defects(
                result,
                point,
                "compatible-common-witness",
                witness,
                self._angle(operators[selected]),
                defects,
                energy_defects,
            )
        defects.extend(
            (
                max(
                    0.0,
                    self._rms_loss(spectral, witness)
                    - threshold.spectral_rms_threshold,
                ),
                max(
                    0.0,
                    self._rms_loss(operators[selected], witness)
                    - threshold.operator_rms_threshold,
                ),
            )
        )

    def _separated_defects(
        self,
        result: ConstrainedAdmissibleSetsExperimentResult,
        spectral: QuadraticLoss2D,
        operators: tuple[QuadraticLoss2D, ...],
        defects: list[float],
        energy_defects: list[float],
    ) -> None:
        """Reconstruct finite feasibility, support points, and separation bounds."""
        definition = result.definition
        case = result.cases[1]
        threshold = definition.separated_thresholds
        spectral_point = self._support_point(
            spectral,
            threshold.spectral_rms_threshold**2,
            (0.0, -1.0),
        )
        feasible = self._feasible_indices(definition, operators, threshold)
        supports = tuple(
            self._support_point(
                operators[index],
                threshold.operator_rms_threshold**2,
                (0.0, 1.0),
            )
            for index in feasible
        )
        support_index = self._first_minimum(tuple(-point[1] for point in supports))
        operator_loss_index = feasible[support_index]
        operator_point = supports[support_index]
        lower = max(0.0, spectral_point[1] - operator_point[1])
        upper = float(
            np.linalg.norm(np.asarray(spectral_point) - np.asarray(operator_point))
        )
        disposition = (
            AdmissibleSetDisposition.CERTIFIED_SEPARATED
            if lower > definition.separation_resolution
            else AdmissibleSetDisposition.UNRESOLVED
        )
        spectral_selected = self._first_minimum(
            tuple(self._squared_loss(loss, spectral_point) for loss in operators)
        )
        defects.extend(
            (
                0.0 if case.thresholds is threshold else 1.0,
                0.0 if case.disposition is disposition else 1.0,
                0.0 if case.common_witness is None else 1.0,
                0.0
                if case.feasible_operator_component_angles
                == tuple(self._angle(operators[index]) for index in feasible)
                else 1.0,
                abs(case.separation_lower_bound - lower),
                abs(case.separation_upper_bound - upper),
                abs(case.separation_resolution - definition.separation_resolution),
                0.0 if definition.contains(spectral_point) else 1.0,
                0.0 if definition.contains(operator_point) else 1.0,
            )
        )
        self._evaluation_defects(
            result,
            case.spectral_certificate_point,
            "separated-spectral-boundary",
            spectral_point,
            self._angle(operators[spectral_selected]),
            defects,
            energy_defects,
        )
        self._evaluation_defects(
            result,
            case.operator_certificate_point,
            "separated-operator-boundary",
            operator_point,
            self._angle(operators[operator_loss_index]),
            defects,
            energy_defects,
        )

    def _evaluation_defects(
        self,
        result: ConstrainedAdmissibleSetsExperimentResult,
        retained: AdmissibleSetPointEvaluation,
        role: str,
        parameter: tuple[float, float],
        angle: float,
        defects: list[float],
        energy_defects: list[float],
    ) -> None:
        """Reconstruct both sample roles and every locality diagnostic."""
        definition = result.definition
        baseline = result.multiband_baseline
        energy_unit = baseline.reference_transform.hopping_model.hopping_blocks[0].unit
        energy_scale = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
            definition.loss_energy_scale, energy_unit
        ).magnitude
        construction_reference = self._matrices(baseline.reference_transform.source)
        construction_attacked = self._matrices(baseline.attacked_transform.source)
        representatives = np.asarray(
            baseline.reference_transform.hopping_model.representatives,
            dtype=np.int64,
        )
        reference_blocks = np.asarray(
            [
                block.magnitude
                for block in baseline.reference_transform.hopping_model.hopping_blocks
            ],
            dtype=np.complex128,
        )
        attacked_blocks = np.asarray(
            [
                block.magnitude
                for block in baseline.attacked_transform.hopping_model.hopping_blocks
            ],
            dtype=np.complex128,
        )
        reduced_evaluation = (
            baseline.withheld_target.coordinates.magnitude
            / baseline.withheld_target.reciprocal_period.magnitude
        )
        evaluation_reference = self._interpolate(
            reduced_evaluation, representatives, reference_blocks
        )
        evaluation_attacked = self._interpolate(
            reduced_evaluation, representatives, attacked_blocks
        )
        construction_candidate = self._candidate(
            construction_reference, parameter, energy_scale
        )
        evaluation_candidate = self._candidate(
            evaluation_reference, parameter, energy_scale
        )
        rotation = self._rotation(angle)
        construction_rotated = self._conjugate(construction_candidate, rotation)
        evaluation_rotated = self._conjugate(evaluation_candidate, rotation)
        rank = definition.multiband_baseline.retained_rank
        expected = (
            self._spectral_rms(
                construction_candidate,
                baseline.training_target.eigenvalues.magnitude,
                energy_scale,
            ),
            self._operator_rms(
                construction_rotated,
                construction_attacked,
                energy_scale,
                rank,
            ),
            self._spectral_rms(
                evaluation_candidate,
                baseline.withheld_target.eigenvalues.magnitude,
                energy_scale,
            ),
            self._operator_rms(
                evaluation_rotated,
                evaluation_attacked,
                energy_scale,
                rank,
            ),
        )
        defects.extend(
            (
                0.0 if retained.role == role else 1.0,
                self._maximum(retained.parameter, parameter),
                abs(retained.selected_alignment_angle - angle),
                abs(retained.objective_construction_spectral_rms_loss - expected[0]),
                abs(retained.objective_construction_operator_rms_loss - expected[1]),
                abs(retained.objective_evaluation_spectral_rms_loss - expected[2]),
                abs(retained.objective_evaluation_operator_rms_loss - expected[3]),
            )
        )
        reduced_construction = (
            baseline.training_target.coordinates.magnitude
            / baseline.training_target.reciprocal_period.magnitude
        )
        candidate_blocks = self._fourier(
            reduced_construction, construction_rotated, representatives
        )
        if len(retained.locality) != len(definition.locality_ranges):
            defects.append(1.0)
            return
        for item, maximum_range in zip(
            retained.locality, definition.locality_ranges, strict=True
        ):
            keep = np.abs(representatives) <= maximum_range
            defects.append(0.0 if item.maximum_range == maximum_range else 1.0)
            energy_defects.extend(
                (
                    abs(
                        item.reference_omitted_block_l2_norm
                        - float(np.linalg.norm(reference_blocks[~keep]))
                    ),
                    abs(
                        item.attacked_omitted_block_l2_norm
                        - float(np.linalg.norm(attacked_blocks[~keep]))
                    ),
                    abs(
                        item.candidate_omitted_block_l2_norm
                        - float(np.linalg.norm(candidate_blocks[~keep]))
                    ),
                )
            )

    @staticmethod
    def _loss_defects(
        retained: QuadraticLoss2D,
        expected: QuadraticLoss2D,
        defects: list[float],
    ) -> None:
        """Append label, angle, center, matrix, and minimum defects."""
        defects.extend(
            (
                0.0 if retained.channel_id == expected.channel_id else 1.0,
                0.0 if retained.alignment_angle == expected.alignment_angle else 1.0,
                ConstrainedAdmissibleSetsExperimentVerifier._maximum(
                    retained.center, expected.center
                ),
                float(
                    np.max(
                        np.abs(
                            np.asarray(retained.quadratic_matrix)
                            - np.asarray(expected.quadratic_matrix)
                        )
                    )
                ),
                abs(retained.minimum_squared_loss - expected.minimum_squared_loss),
            )
        )

    @classmethod
    def _feasible_angles(
        cls,
        definition: ConstrainedAdmissibleSetsExperimentDefinition,
        operators: tuple[QuadraticLoss2D, ...],
        thresholds: AdmissibleSetThresholds,
    ) -> tuple[float, ...]:
        """Return independently filtered angle labels."""
        return tuple(
            cls._angle(operators[index])
            for index in cls._feasible_indices(definition, operators, thresholds)
        )

    @classmethod
    def _feasible_indices(
        cls,
        definition: ConstrainedAdmissibleSetsExperimentDefinition,
        operators: tuple[QuadraticLoss2D, ...],
        thresholds: AdmissibleSetThresholds,
    ) -> tuple[int, ...]:
        """Filter independently reconstructed rectangle minima inclusively."""
        ceiling = thresholds.operator_rms_threshold**2
        return tuple(
            index
            for index, loss in enumerate(operators)
            if cls._rectangle_minimum(definition, loss) <= ceiling
        )

    @classmethod
    def _rectangle_minimum(
        cls,
        definition: ConstrainedAdmissibleSetsExperimentDefinition,
        loss: QuadraticLoss2D,
    ) -> float:
        """Enumerate the clipped center and four conditional edge minima."""
        center = np.asarray(loss.center, dtype=np.float64)
        matrix = np.asarray(loss.quadratic_matrix, dtype=np.float64)
        lower = np.asarray(
            (
                definition.energy_shift_ratio_bounds[0],
                definition.splitting_scale_bounds[0],
            )
        )
        upper = np.asarray(
            (
                definition.energy_shift_ratio_bounds[1],
                definition.splitting_scale_bounds[1],
            )
        )
        candidates = [np.clip(center, lower, upper)]
        for axis in (0, 1):
            other = 1 - axis
            for bound in (lower[axis], upper[axis]):
                point = center.copy()
                point[axis] = bound
                point[other] = center[other] - (
                    matrix[other, axis] / matrix[other, other] * (bound - center[axis])
                )
                point[other] = np.clip(point[other], lower[other], upper[other])
                candidates.append(point)
        return min(
            cls._squared_loss(loss, (float(point[0]), float(point[1])))
            for point in candidates
        )

    @staticmethod
    def _support_point(
        loss: QuadraticLoss2D,
        squared_loss_ceiling: float,
        direction: tuple[float, float],
    ) -> tuple[float, float]:
        """Reconstruct full-ellipsoid support with an independent linear solve."""
        matrix = np.asarray(loss.quadratic_matrix, dtype=np.float64)
        vector = np.asarray(direction, dtype=np.float64)
        solved = np.linalg.solve(matrix, vector)
        budget = squared_loss_ceiling - loss.minimum_squared_loss
        scale = np.sqrt(budget / float(vector @ solved))
        point = np.asarray(loss.center, dtype=np.float64) + scale * solved
        return float(point[0]), float(point[1])

    @staticmethod
    def _spectral_quadratic(
        reference: np.ndarray,
        target: np.ndarray,
        energy_scale: float,
    ) -> QuadraticLoss2D:
        """Independently derive the invariant objective-construction quadratic."""
        rank = reference.shape[1]
        mean = np.trace(reference, axis1=1, axis2=2).real / float(rank)
        values = np.linalg.eigvalsh(reference)
        base = np.repeat(mean[:, None], rank, axis=1)
        features = np.stack(
            (np.full_like(values, energy_scale), values - base), axis=-1
        )
        return ConstrainedAdmissibleSetsExperimentVerifier._quadratic(
            "spectral-objective-construction-rms-v1",
            None,
            features,
            base - target,
            energy_scale,
        )

    @staticmethod
    def _operator_quadratic(
        reference: np.ndarray,
        target: np.ndarray,
        energy_scale: float,
        angle: float,
    ) -> QuadraticLoss2D:
        """Independently derive one angle-resolved construction quadratic."""
        rank = reference.shape[1]
        identity = np.eye(rank, dtype=np.complex128)
        mean = np.trace(reference, axis1=1, axis2=2) / float(rank)
        base = mean[:, None, None] * identity
        rotation = ConstrainedAdmissibleSetsExperimentVerifier._rotation(angle)
        rotated = ConstrainedAdmissibleSetsExperimentVerifier._conjugate(
            reference - base, rotation
        )
        features = np.stack(
            (np.broadcast_to(energy_scale * identity, reference.shape), rotated),
            axis=-1,
        )
        return ConstrainedAdmissibleSetsExperimentVerifier._quadratic(
            f"operator-objective-construction-rms-angle-{angle:.17g}",
            angle,
            features,
            base - target,
            energy_scale,
        )

    @staticmethod
    def _quadratic(
        channel_id: str,
        angle: float | None,
        features: np.ndarray,
        offset: np.ndarray,
        energy_scale: float,
    ) -> QuadraticLoss2D:
        """Independently complete one normalized complex-feature quadratic."""
        normalization = float(features.shape[0] * features.shape[1]) * energy_scale**2
        matrix = np.asarray(
            [
                [
                    np.vdot(features[..., row], features[..., column]).real
                    / normalization
                    for column in range(2)
                ]
                for row in range(2)
            ]
        )
        matrix = 0.5 * (matrix + matrix.T)
        linear = np.asarray(
            [
                np.vdot(features[..., row], offset).real / normalization
                for row in range(2)
            ]
        )
        center = -np.linalg.solve(matrix, linear)
        minimum = float(np.vdot(offset, offset).real / normalization) - float(
            linear @ np.linalg.solve(matrix, linear)
        )
        if minimum < 0.0 and abs(minimum) <= 1.0e-14:
            minimum = 0.0
        return QuadraticLoss2D(
            channel_id,
            angle,
            (float(center[0]), float(center[1])),
            (
                (float(matrix[0, 0]), float(matrix[0, 1])),
                (float(matrix[1, 0]), float(matrix[1, 1])),
            ),
            float(minimum),
        )

    @staticmethod
    def _squared_loss(
        loss: QuadraticLoss2D,
        parameter: tuple[float, float],
    ) -> float:
        """Evaluate the completed square without using the owner facade."""
        delta = np.asarray(parameter, dtype=np.float64) - np.asarray(
            loss.center, dtype=np.float64
        )
        matrix = np.asarray(loss.quadratic_matrix, dtype=np.float64)
        return float(loss.minimum_squared_loss + delta @ matrix @ delta)

    @classmethod
    def _rms_loss(
        cls,
        loss: QuadraticLoss2D,
        parameter: tuple[float, float],
    ) -> float:
        """Return an independently reconstructed root loss."""
        return float(np.sqrt(max(0.0, cls._squared_loss(loss, parameter))))

    @staticmethod
    def _first_minimum(values: tuple[float, ...]) -> int:
        """Return the first exact minimum index without owner selection calls."""
        best_index = 0
        best_value = values[0]
        for index, value in enumerate(values[1:], start=1):
            if value < best_value:
                best_index = index
                best_value = value
        return best_index

    @staticmethod
    def _angle(loss: QuadraticLoss2D) -> float:
        """Return an operator loss's mandatory angle label."""
        if loss.alignment_angle is None:
            raise ValueError("operator loss must retain an angle")
        return loss.alignment_angle

    @staticmethod
    def _candidate(
        reference: np.ndarray,
        parameter: tuple[float, float],
        energy_scale: float,
    ) -> np.ndarray:
        """Independently rebuild one affine candidate family member."""
        rank = reference.shape[1]
        identity = np.eye(rank, dtype=np.complex128)
        mean = np.trace(reference, axis1=1, axis2=2) / float(rank)
        base = mean[:, None, None] * identity
        return np.asarray(
            base
            + parameter[0] * energy_scale * identity
            + parameter[1] * (reference - base),
            dtype=np.complex128,
        )

    @staticmethod
    def _spectral_rms(
        candidate: np.ndarray,
        target: np.ndarray,
        energy_scale: float,
    ) -> float:
        """Independently rebuild normalized ordered-eigenvalue RMS loss."""
        return float(
            np.sqrt(np.mean(np.abs(np.linalg.eigvalsh(candidate) - target) ** 2))
            / energy_scale
        )

    @staticmethod
    def _operator_rms(
        candidate: np.ndarray,
        target: np.ndarray,
        energy_scale: float,
        rank: int,
    ) -> float:
        """Independently rebuild normalized operator Frobenius RMS loss."""
        squared = sum(
            float(np.linalg.norm(left - right) ** 2)
            for left, right in zip(candidate, target, strict=True)
        )
        return float(np.sqrt(squared / float(candidate.shape[0] * rank)) / energy_scale)

    @staticmethod
    def _fourier(
        reduced: np.ndarray,
        matrices: np.ndarray,
        representatives: np.ndarray,
    ) -> np.ndarray:
        """Reconstruct finite hopping blocks by the declared forward transform."""
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
        reduced: np.ndarray,
        representatives: np.ndarray,
        blocks: np.ndarray,
    ) -> np.ndarray:
        """Evaluate finite hopping blocks at reduced reciprocal coordinates."""
        phases = np.exp(2j * np.pi * np.outer(reduced, representatives))
        return np.asarray(
            np.einsum("kr,rij->kij", phases, blocks, optimize=True),
            dtype=np.complex128,
        )

    @staticmethod
    def _rotation(angle: float) -> np.ndarray:
        """Return the rank-two real rotation for one frozen angle."""
        return np.asarray(
            [
                [np.cos(angle), -np.sin(angle)],
                [np.sin(angle), np.cos(angle)],
            ],
            dtype=np.complex128,
        )

    @staticmethod
    def _conjugate(matrices: np.ndarray, rotation: np.ndarray) -> np.ndarray:
        """Apply one global represented-space conjugation to every sample."""
        return np.asarray(
            np.einsum(
                "ab,kbc,cd->kad",
                rotation.conj().T,
                matrices,
                rotation,
                optimize=True,
            ),
            dtype=np.complex128,
        )

    @staticmethod
    def _matrices(samples: ReciprocalOperatorSamples1D) -> np.ndarray:
        """Stack one typed reciprocal-operator sample sequence."""
        return np.asarray(
            [matrix.magnitude for matrix in samples.matrices],
            dtype=np.complex128,
        )

    @staticmethod
    def _maximum(left: tuple[float, float], right: tuple[float, float]) -> float:
        """Return the maximum coordinate defect."""
        return float(
            np.max(np.abs(np.asarray(left, dtype=np.float64) - np.asarray(right)))
        )


__all__ = [
    "ConstrainedAdmissibleSetsExperimentVerifier",
    "ConstrainedAdmissibleSetsVerificationResult",
]
