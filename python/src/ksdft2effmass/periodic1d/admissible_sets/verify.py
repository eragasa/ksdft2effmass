"""Independent reconstruction for constrained admissible-set results."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.operators import MODEL_SYSTEM_UNIT_CONVERTER, ScalarQuantity
from ksdft2effmass.periodic1d.multiband_alignment import (
    Periodic1DMultibandAlignmentResultVerifier,
)
from ksdft2effmass.solid_state import ReciprocalOperatorSamples1D

from .definition import Periodic1DConstrainedAdmissibleSetCalculationDefinition
from .results import (
    Periodic1DAdmissibleSetDisposition,
    Periodic1DAdmissibleSetParameterEvaluation,
    Periodic1DConstrainedAdmissibleSetCalculationResult,
    Periodic1DQuadraticLoss,
)


@dataclass(frozen=True, slots=True)
class Periodic1DConstrainedAdmissibleSetVerificationResult:
    """Retain independently reconstructed M3 numerical-consistency evidence.

    Dimensionless and parent-energy defects remain separate. ``passes`` is derived from
    both defects and the retained absolute tolerance; it is software/numerical evidence,
    not scientific acceptance or material validation.
    """

    calculation: Periodic1DConstrainedAdmissibleSetCalculationResult
    dimensionless_maximum_absolute_defect: float
    energy_maximum_absolute_defect: ScalarQuantity
    absolute_tolerance: float
    passes: bool

    def __post_init__(self) -> None:
        """Validate finite defects, units, and the derived disposition."""
        if type(self.calculation) is not (
            Periodic1DConstrainedAdmissibleSetCalculationResult
        ):
            raise TypeError(
                "calculation must be "
                "Periodic1DConstrainedAdmissibleSetCalculationResult"
            )
        for name, value in (
            (
                "dimensionless_maximum_absolute_defect",
                self.dimensionless_maximum_absolute_defect,
            ),
            ("absolute_tolerance", self.absolute_tolerance),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not np.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        if type(self.energy_maximum_absolute_defect) is not ScalarQuantity:
            raise TypeError("energy_maximum_absolute_defect must be ScalarQuantity")
        unit = self.calculation.definition.parent_model.hopping_model.hopping_blocks[
            0
        ].unit
        if self.energy_maximum_absolute_defect.unit != unit:
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
            raise ValueError("passes must match reconstructed defects and tolerance")


class Periodic1DConstrainedAdmissibleSetResultVerifier:
    """Reconstruct M3 without invoking its producer calculation Action.

    The verifier independently rebuilds the composed M2 evidence, analytic training
    quadratics, role-identified compatible witness, axis-separation certificate,
    staggered evaluation diagnostics, Fourier locality, and bounded disposition.
    """

    __slots__ = ()

    def execute(
        self, calculation: Periodic1DConstrainedAdmissibleSetCalculationResult
    ) -> Periodic1DConstrainedAdmissibleSetVerificationResult:
        """Rebuild M2 consistency, quadratics, witnesses, and certificates.

        Parameters
        ----------
        calculation
            Exact retained M3 aggregate to verify.

        Returns
        -------
        Periodic1DConstrainedAdmissibleSetVerificationResult
            Maximum dimensionless and parent-energy defects with a derived pass flag.

        Raises
        ------
        TypeError
            If ``calculation`` is not the exact M3 result type.
        """
        if type(calculation) is not (
            Periodic1DConstrainedAdmissibleSetCalculationResult
        ):
            raise TypeError(
                "calculation must be "
                "Periodic1DConstrainedAdmissibleSetCalculationResult"
            )
        definition = calculation.definition
        baseline = calculation.multiband_baseline
        baseline_verification = Periodic1DMultibandAlignmentResultVerifier().execute(
            baseline
        )
        dimensionless = [
            baseline_verification.dimensionless_maximum_absolute_defect,
            0.0 if baseline_verification.passes else 1.0,
        ]
        energy = [baseline_verification.energy_maximum_absolute_defect.magnitude]
        energy_unit = definition.parent_model.hopping_model.hopping_blocks[0].unit
        scale = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
            definition.loss_energy_scale, energy_unit
        ).magnitude
        reference = self._samples(baseline.reference_transform.source)
        attacked = self._samples(baseline.attacked_transform.source)
        spectral = self._spectral_quadratic(
            reference, baseline.training_target.eigenvalues.magnitude, scale
        )
        operators = tuple(
            self._operator_quadratic(reference, attacked, scale, angle)
            for angle in definition.alignment_angles
        )
        self._loss_defect(calculation.spectral_loss, spectral, dimensionless)
        if len(calculation.operator_losses) != len(operators):
            dimensionless.append(1.0)
        else:
            for retained, expected in zip(
                calculation.operator_losses, operators, strict=True
            ):
                self._loss_defect(retained, expected, dimensionless)
        if len(calculation.cases) != 2:
            dimensionless.append(1.0)
        else:
            self._compatible_case(
                calculation, spectral, operators, dimensionless, energy
            )
            self._separated_case(
                calculation, spectral, operators, dimensionless, energy
            )
        maximum_dimensionless = max(dimensionless, default=0.0)
        maximum_energy = max(energy, default=0.0)
        tolerance = definition.verification_absolute_tolerance
        return Periodic1DConstrainedAdmissibleSetVerificationResult(
            calculation,
            float(maximum_dimensionless),
            ScalarQuantity(
                float(maximum_energy),
                definition.parent_model.hopping_model.hopping_blocks[0].unit,
            ),
            tolerance,
            maximum_dimensionless <= tolerance and maximum_energy <= tolerance,
        )

    def _compatible_case(
        self,
        calculation: Periodic1DConstrainedAdmissibleSetCalculationResult,
        spectral: Periodic1DQuadraticLoss,
        operators: tuple[Periodic1DQuadraticLoss, ...],
        dimensionless: list[float],
        energy: list[float],
    ) -> None:
        """Reconstruct the prospective witness case and append all defects."""
        definition = calculation.definition
        retained = calculation.cases[0]
        witness = definition.compatible_witness
        selected = min(operators, key=lambda item: item.squared_loss(witness))
        expected_angles = self._feasible_angles(
            definition,
            operators,
            definition.compatible_thresholds.operator_rms_threshold,
        )
        dimensionless.extend(
            (
                0.0 if retained.thresholds is definition.compatible_thresholds else 1.0,
                0.0
                if retained.disposition
                is Periodic1DAdmissibleSetDisposition.COMPATIBLE_WITNESS
                else 1.0,
                0.0
                if retained.feasible_operator_component_angles == expected_angles
                else 1.0,
                abs(retained.separation_lower_bound),
                abs(retained.separation_upper_bound),
                abs(retained.separation_resolution - definition.separation_resolution),
                max(
                    0.0,
                    spectral.rms_loss(witness)
                    - definition.compatible_thresholds.spectral_rms_threshold,
                ),
                max(
                    0.0,
                    selected.rms_loss(witness)
                    - definition.compatible_thresholds.operator_rms_threshold,
                ),
            )
        )
        if retained.common_witness is None:
            dimensionless.append(1.0)
            return
        for evaluation in (
            retained.common_witness,
            retained.spectral_certificate_point,
            retained.operator_certificate_point,
        ):
            self._evaluation_defects(
                calculation,
                evaluation,
                witness,
                self._angle(selected),
                "compatible-common-witness",
                dimensionless,
                energy,
            )

    def _separated_case(
        self,
        calculation: Periodic1DConstrainedAdmissibleSetCalculationResult,
        spectral: Periodic1DQuadraticLoss,
        operators: tuple[Periodic1DQuadraticLoss, ...],
        dimensionless: list[float],
        energy: list[float],
    ) -> None:
        """Reconstruct the splitting-axis certificate and bounded disposition."""
        definition = calculation.definition
        retained = calculation.cases[1]
        threshold = definition.separated_thresholds
        spectral_point, spectral_lower = self._axis_extreme(
            spectral, threshold.spectral_rms_threshold, -1.0
        )
        feasible = tuple(
            item
            for item in operators
            if self._domain_minimum(definition, item)
            <= threshold.operator_rms_threshold**2
        )
        extrema = tuple(
            (
                item,
                *self._axis_extreme(item, threshold.operator_rms_threshold, 1.0),
            )
            for item in feasible
        )
        selected, operator_point, operator_upper = max(
            extrema, key=lambda item: item[2]
        )
        lower = max(0.0, spectral_lower - operator_upper)
        upper = float(
            np.linalg.norm(np.asarray(spectral_point) - np.asarray(operator_point))
        )
        disposition = (
            Periodic1DAdmissibleSetDisposition.CERTIFIED_SEPARATED
            if lower > definition.separation_resolution
            else Periodic1DAdmissibleSetDisposition.UNRESOLVED
        )
        dimensionless.extend(
            (
                0.0 if retained.thresholds is threshold else 1.0,
                0.0 if retained.disposition is disposition else 1.0,
                0.0 if retained.common_witness is None else 1.0,
                0.0
                if retained.feasible_operator_component_angles
                == tuple(self._angle(item) for item in feasible)
                else 1.0,
                abs(retained.separation_lower_bound - lower),
                abs(retained.separation_upper_bound - upper),
                abs(retained.separation_resolution - definition.separation_resolution),
            )
        )
        self._evaluation_defects(
            calculation,
            retained.spectral_certificate_point,
            spectral_point,
            self._best_angle(operators, spectral_point),
            "separated-spectral-boundary",
            dimensionless,
            energy,
        )
        self._evaluation_defects(
            calculation,
            retained.operator_certificate_point,
            operator_point,
            self._angle(selected),
            "separated-operator-boundary",
            dimensionless,
            energy,
        )

    def _evaluation_defects(
        self,
        calculation: Periodic1DConstrainedAdmissibleSetCalculationResult,
        retained: Periodic1DAdmissibleSetParameterEvaluation,
        parameter: tuple[float, float],
        angle: float,
        expected_role: str,
        dimensionless: list[float],
        energy: list[float],
    ) -> None:
        """Rebuild one role-identified proof point and its locality diagnostics."""
        definition = calculation.definition
        baseline = calculation.multiband_baseline
        energy_unit = definition.parent_model.hopping_model.hopping_blocks[0].unit
        scale = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
            definition.loss_energy_scale, energy_unit
        ).magnitude
        training_reference = self._samples(baseline.reference_transform.source)
        training_attacked = self._samples(baseline.attacked_transform.source)
        representatives = np.asarray(
            baseline.reference_transform.hopping_model.representatives,
            dtype=np.int64,
        )
        reference_blocks = np.asarray(
            [
                block.magnitude
                for block in baseline.reference_transform.hopping_model.hopping_blocks
            ]
        )
        attacked_blocks = np.asarray(
            [
                block.magnitude
                for block in baseline.attacked_transform.hopping_model.hopping_blocks
            ]
        )
        reduced = (
            baseline.withheld_target.coordinates.magnitude
            / baseline.withheld_target.reciprocal_period.magnitude
        )
        withheld_reference = self._interpolate(
            reduced, representatives, reference_blocks
        )
        withheld_attacked = self._interpolate(reduced, representatives, attacked_blocks)
        training_candidate = self._candidate(training_reference, parameter, scale)
        withheld_candidate = self._candidate(withheld_reference, parameter, scale)
        rotation = self._rotation(angle)
        training_rotated = self._conjugate(training_candidate, rotation)
        withheld_rotated = self._conjugate(withheld_candidate, rotation)
        rank = definition.multiband_baseline.retained_rank
        values = (
            self._spectral_rms(
                training_candidate,
                baseline.training_target.eigenvalues.magnitude,
                scale,
            ),
            self._operator_rms(training_rotated, training_attacked, scale, rank),
            self._spectral_rms(
                withheld_candidate,
                baseline.withheld_target.eigenvalues.magnitude,
                scale,
            ),
            self._operator_rms(withheld_rotated, withheld_attacked, scale, rank),
        )
        dimensionless.extend(
            (
                0.0 if retained.role == expected_role else 1.0,
                self._maximum(np.asarray(retained.parameter), np.asarray(parameter)),
                abs(retained.selected_alignment_angle - angle),
                abs(retained.training_spectral_rms_loss - values[0]),
                abs(retained.training_operator_rms_loss - values[1]),
                abs(retained.withheld_spectral_rms_loss - values[2]),
                abs(retained.withheld_operator_rms_loss - values[3]),
            )
        )
        training_reduced = (
            baseline.training_target.coordinates.magnitude
            / baseline.training_target.reciprocal_period.magnitude
        )
        candidate_blocks = self._fourier(
            training_reduced, training_rotated, representatives
        )
        if len(retained.locality) != len(definition.locality_ranges):
            dimensionless.append(1.0)
            return
        for item, maximum_range in zip(
            retained.locality, definition.locality_ranges, strict=True
        ):
            keep = np.abs(representatives) <= maximum_range
            dimensionless.append(0.0 if item.maximum_range == maximum_range else 1.0)
            energy.extend(
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
    def _loss_defect(
        retained: Periodic1DQuadraticLoss,
        expected: Periodic1DQuadraticLoss,
        defects: list[float],
    ) -> None:
        """Append identity, angle, center, curvature, and minimum defects."""
        defects.extend(
            (
                0.0 if retained.channel_id == expected.channel_id else 1.0,
                0.0 if retained.alignment_angle == expected.alignment_angle else 1.0,
                Periodic1DConstrainedAdmissibleSetResultVerifier._maximum(
                    np.asarray(retained.center), np.asarray(expected.center)
                ),
                Periodic1DConstrainedAdmissibleSetResultVerifier._maximum(
                    np.asarray(retained.quadratic_matrix),
                    np.asarray(expected.quadratic_matrix),
                ),
                abs(retained.minimum_squared_loss - expected.minimum_squared_loss),
            )
        )

    @staticmethod
    def _quadratic(
        channel_id: str,
        angle: float | None,
        features: np.ndarray,
        offset: np.ndarray,
        scale: float,
    ) -> Periodic1DQuadraticLoss:
        """Independently complete a two-feature normalized least-squares quadratic."""
        normalization = float(features.shape[0] * features.shape[1]) * scale**2
        matrix = np.asarray(
            [
                [
                    np.vdot(features[..., row], features[..., column]).real
                    / normalization
                    for column in range(2)
                ]
                for row in range(2)
            ],
            dtype=np.float64,
        )
        matrix = 0.5 * (matrix + matrix.T)
        linear = np.asarray(
            [
                np.vdot(features[..., row], offset).real / normalization
                for row in range(2)
            ]
        )
        center = -np.linalg.solve(matrix, linear)
        constant = float(np.vdot(offset, offset).real / normalization)
        minimum = constant - float(linear @ np.linalg.solve(matrix, linear))
        if minimum < 0.0 and abs(minimum) <= 1.0e-14:
            minimum = 0.0
        return Periodic1DQuadraticLoss(
            channel_id,
            angle,
            (float(center[0]), float(center[1])),
            (
                (float(matrix[0, 0]), float(matrix[0, 1])),
                (float(matrix[1, 0]), float(matrix[1, 1])),
            ),
            float(minimum),
        )

    @classmethod
    def _spectral_quadratic(
        cls, reference: np.ndarray, target: np.ndarray, scale: float
    ) -> Periodic1DQuadraticLoss:
        """Independently derive the invariant spectral training quadratic."""
        rank = reference.shape[1]
        mean = np.trace(reference, axis1=1, axis2=2).real / float(rank)
        values = np.linalg.eigvalsh(reference)
        base = np.repeat(mean[:, None], rank, axis=1)
        features = np.stack((np.full_like(values, scale), values - base), axis=-1)
        return cls._quadratic(
            "spectral-training-rms-v1", None, features, base - target, scale
        )

    @classmethod
    def _operator_quadratic(
        cls,
        reference: np.ndarray,
        target: np.ndarray,
        scale: float,
        angle: float,
    ) -> Periodic1DQuadraticLoss:
        """Independently derive one angle-resolved operator training quadratic."""
        rank = reference.shape[1]
        identity = np.eye(rank, dtype=np.complex128)
        mean = np.trace(reference, axis1=1, axis2=2) / float(rank)
        base = mean[:, None, None] * identity
        rotation = cls._rotation(angle)
        rotated = cls._conjugate(reference - base, rotation)
        features = np.stack(
            (
                np.broadcast_to(scale * identity, reference.shape),
                rotated,
            ),
            axis=-1,
        )
        return cls._quadratic(
            f"operator-training-rms-angle-{angle:.17g}",
            angle,
            features,
            base - target,
            scale,
        )

    @staticmethod
    def _axis_extreme(
        loss: Periodic1DQuadraticLoss,
        threshold: float,
        direction: float,
    ) -> tuple[tuple[float, float], float]:
        """Rebuild one splitting-axis extreme of an unclipped threshold ellipse."""
        budget = threshold**2 - loss.minimum_squared_loss
        matrix_inverse = np.linalg.inv(np.asarray(loss.quadratic_matrix))
        unit = np.asarray((0.0, direction))
        point = np.asarray(loss.center) + np.sqrt(
            budget / float(unit @ matrix_inverse @ unit)
        ) * (matrix_inverse @ unit)
        return (float(point[0]), float(point[1])), float(point[1])

    @staticmethod
    def _domain_minimum(
        definition: Periodic1DConstrainedAdmissibleSetCalculationDefinition,
        loss: Periodic1DQuadraticLoss,
    ) -> float:
        """Minimize a positive quadratic over the closed continuous rectangle."""
        center = np.asarray(loss.center)
        matrix = np.asarray(loss.quadratic_matrix)
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
                point[other] = center[other] - matrix[other, axis] / matrix[
                    other, other
                ] * (bound - center[axis])
                point[other] = np.clip(point[other], lower[other], upper[other])
                candidates.append(point)
        return min(
            loss.squared_loss((float(point[0]), float(point[1])))
            for point in candidates
        )

    @classmethod
    def _feasible_angles(
        cls,
        definition: Periodic1DConstrainedAdmissibleSetCalculationDefinition,
        losses: tuple[Periodic1DQuadraticLoss, ...],
        threshold: float,
    ) -> tuple[float, ...]:
        """Rebuild the feasible frozen angle inventory for one threshold."""
        return tuple(
            cls._angle(item)
            for item in losses
            if cls._domain_minimum(definition, item) <= threshold**2
        )

    @classmethod
    def _best_angle(
        cls,
        losses: tuple[Periodic1DQuadraticLoss, ...],
        parameter: tuple[float, float],
    ) -> float:
        """Return the frozen operator angle of minimum loss at one point."""
        return cls._angle(min(losses, key=lambda item: item.squared_loss(parameter)))

    @staticmethod
    def _angle(loss: Periodic1DQuadraticLoss) -> float:
        """Extract an operator quadratic's mandatory global angle."""
        if loss.alignment_angle is None:
            raise ValueError("operator loss must retain an alignment angle")
        return loss.alignment_angle

    @staticmethod
    def _candidate(
        reference: np.ndarray,
        parameter: tuple[float, float],
        scale: float,
    ) -> np.ndarray:
        """Rebuild the affine trace/shift/traceless-splitting candidate matrices."""
        rank = reference.shape[1]
        identity = np.eye(rank, dtype=np.complex128)
        mean = np.trace(reference, axis1=1, axis2=2) / float(rank)
        base = mean[:, None, None] * identity
        return np.asarray(
            base + parameter[0] * scale * identity + parameter[1] * (reference - base),
            dtype=np.complex128,
        )

    @staticmethod
    def _rotation(angle: float) -> np.ndarray:
        """Return the rank-two real unitary rotation for one frozen angle."""
        return np.asarray(
            [
                [np.cos(angle), -np.sin(angle)],
                [np.sin(angle), np.cos(angle)],
            ],
            dtype=np.complex128,
        )

    @staticmethod
    def _conjugate(matrices: np.ndarray, rotation: np.ndarray) -> np.ndarray:
        """Apply one global represented-space conjugation to all matrices."""
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
    def _spectral_rms(candidate: np.ndarray, target: np.ndarray, scale: float) -> float:
        """Rebuild normalized ordered-eigenvalue RMS loss."""
        return float(
            np.sqrt(np.mean(np.abs(np.linalg.eigvalsh(candidate) - target) ** 2))
            / scale
        )

    @staticmethod
    def _operator_rms(
        candidate: np.ndarray, target: np.ndarray, scale: float, rank: int
    ) -> float:
        """Rebuild normalized represented-operator Frobenius RMS loss."""
        squared = sum(
            float(np.linalg.norm(left - right) ** 2)
            for left, right in zip(candidate, target, strict=True)
        )
        return float(np.sqrt(squared / float(candidate.shape[0] * rank)) / scale)

    @staticmethod
    def _fourier(
        reduced: np.ndarray, matrices: np.ndarray, representatives: np.ndarray
    ) -> np.ndarray:
        """Reconstruct hopping blocks by the declared finite Fourier convention."""
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
            ]
        )

    @staticmethod
    def _interpolate(
        reduced: np.ndarray, representatives: np.ndarray, blocks: np.ndarray
    ) -> np.ndarray:
        """Interpolate hopping blocks at reduced reciprocal coordinates."""
        phases = np.exp(2j * np.pi * np.outer(reduced, representatives))
        return np.asarray(
            np.einsum("kr,rij->kij", phases, blocks, optimize=True),
            dtype=np.complex128,
        )

    @staticmethod
    def _samples(samples: ReciprocalOperatorSamples1D) -> np.ndarray:
        """Stack reciprocal matrices from a typed sample sequence."""
        return np.asarray([matrix.magnitude for matrix in samples.matrices])

    @staticmethod
    def _maximum(left: np.ndarray, right: np.ndarray) -> float:
        """Return the maximum elementwise absolute reconstruction defect."""
        return float(np.max(np.abs(left - right)))


__all__ = [
    "Periodic1DConstrainedAdmissibleSetResultVerifier",
    "Periodic1DConstrainedAdmissibleSetVerificationResult",
]
