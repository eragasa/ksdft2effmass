"""Calculation Action for constrained multiband admissible sets."""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

from ksdft2effmass.operators import (
    MODEL_SYSTEM_UNIT_CONVERTER,
    ComplexMatrixQuantity,
)
from ksdft2effmass.periodic1d.multiband_alignment import (
    Periodic1DMultibandAlignmentCalculationResult,
    Periodic1DMultibandAlignmentCalculator,
)
from ksdft2effmass.solid_state import (
    BlockHoppingInterpolator1D,
    BlockHoppingTruncator1D,
    ReciprocalOperatorFourierTransformer1D,
    ReciprocalOperatorSamples1D,
)

from .definition import (
    Periodic1DAdmissibleSetThresholds,
    Periodic1DConstrainedAdmissibleSetCalculationDefinition,
)
from .results import (
    Periodic1DAdmissibleSetCaseResult,
    Periodic1DAdmissibleSetDisposition,
    Periodic1DAdmissibleSetLocalityResult,
    Periodic1DAdmissibleSetParameterEvaluation,
    Periodic1DConstrainedAdmissibleSetCalculationResult,
    Periodic1DQuadraticLoss,
)


class Periodic1DConstrainedAdmissibleSetCalculator:
    """Compose M2 with continuous-parameter losses and finite-angle certificates.

    This deterministic in-process Action invokes no external calculator. The v1
    certificate compares unclipped positive-definite ellipses only along the splitting-
    scale axis inside the frozen rectangle. It is not an arbitrary-direction or general
    nonconvex alignment solver.
    """

    __slots__ = ()

    def execute(
        self, definition: Periodic1DConstrainedAdmissibleSetCalculationDefinition
    ) -> Periodic1DConstrainedAdmissibleSetCalculationResult:
        """Calculate the frozen M3 quadratics, witness, and separation case.

        Parameters
        ----------
        definition
            Exact M3 controls composing one rank-two M2 baseline, continuous parameter
            rectangle, finite angle family, thresholds, and tolerances.

        Returns
        -------
        Periodic1DConstrainedAdmissibleSetCalculationResult
            Correlated M2 baseline, analytic spectral/operator quadratics, compatible
            witness case, and bounded separation case.

        Raises
        ------
        TypeError
            If ``definition`` is not the exact M3 definition type.
        ValueError
            If the prospective witness, ellipse geometry, units, or certificate
            premises violate the frozen controls.
        """
        if type(definition) is not (
            Periodic1DConstrainedAdmissibleSetCalculationDefinition
        ):
            raise TypeError(
                "definition must be "
                "Periodic1DConstrainedAdmissibleSetCalculationDefinition"
            )
        baseline = Periodic1DMultibandAlignmentCalculator().execute(
            definition.multiband_baseline
        )
        reference = self._matrices(baseline.reference_transform.source)
        attacked = self._matrices(baseline.attacked_transform.source)
        energy_unit = baseline.reference_transform.hopping_model.hopping_blocks[0].unit
        energy_scale = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
            definition.loss_energy_scale, energy_unit
        ).magnitude
        spectral = self._spectral_quadratic(
            reference,
            baseline.training_target.eigenvalues.magnitude,
            energy_scale,
        )
        operator = tuple(
            self._operator_quadratic(reference, attacked, energy_scale, angle)
            for angle in definition.alignment_angles
        )
        cases = (
            self._compatible_case(definition, baseline, spectral, operator),
            self._separated_case(definition, baseline, spectral, operator),
        )
        return Periodic1DConstrainedAdmissibleSetCalculationResult(
            definition,
            baseline,
            spectral,
            operator,
            cases,
        )

    def _compatible_case(
        self,
        definition: Periodic1DConstrainedAdmissibleSetCalculationDefinition,
        baseline: Periodic1DMultibandAlignmentCalculationResult,
        spectral: Periodic1DQuadraticLoss,
        operator: tuple[Periodic1DQuadraticLoss, ...],
    ) -> Periodic1DAdmissibleSetCaseResult:
        """Verify and retain the prospectively declared common witness."""
        thresholds = definition.compatible_thresholds
        witness = definition.compatible_witness
        selected = min(operator, key=lambda item: item.squared_loss(witness))
        if spectral.rms_loss(witness) > thresholds.spectral_rms_threshold or (
            selected.rms_loss(witness) > thresholds.operator_rms_threshold
        ):
            raise ValueError("the frozen compatible witness is not threshold-feasible")
        evaluation = self._evaluate(
            definition,
            baseline,
            "compatible-common-witness",
            witness,
            self._angle(selected),
        )
        feasible = self._feasible_angles(definition, operator, thresholds)
        return Periodic1DAdmissibleSetCaseResult(
            thresholds,
            Periodic1DAdmissibleSetDisposition.COMPATIBLE_WITNESS,
            feasible,
            evaluation,
            evaluation,
            evaluation,
            0.0,
            0.0,
            definition.separation_resolution,
        )

    def _separated_case(
        self,
        definition: Periodic1DConstrainedAdmissibleSetCalculationDefinition,
        baseline: Periodic1DMultibandAlignmentCalculationResult,
        spectral: Periodic1DQuadraticLoss,
        operator: tuple[Periodic1DQuadraticLoss, ...],
    ) -> Periodic1DAdmissibleSetCaseResult:
        """Construct axis-extreme points and a bounded separation certificate."""
        thresholds = definition.separated_thresholds
        spectral_point, spectral_lower = self._axis_extreme(
            definition,
            spectral,
            thresholds.spectral_rms_threshold,
            axis=1,
            direction=-1.0,
        )
        feasible_losses = tuple(
            item
            for item in operator
            if self._domain_minimum_squared_loss(definition, item)
            <= thresholds.operator_rms_threshold**2
        )
        if not feasible_losses:
            raise ValueError("the frozen operator admissible set is empty")
        operator_extrema = tuple(
            (
                item,
                *self._axis_extreme(
                    definition,
                    item,
                    thresholds.operator_rms_threshold,
                    axis=1,
                    direction=1.0,
                ),
            )
            for item in feasible_losses
        )
        selected, operator_point, operator_upper = max(
            operator_extrema, key=lambda item: item[2]
        )
        lower_bound = max(0.0, spectral_lower - operator_upper)
        upper_bound = float(
            np.linalg.norm(np.asarray(spectral_point) - np.asarray(operator_point))
        )
        tolerance = definition.quadratic_absolute_tolerance
        if lower_bound > upper_bound + tolerance:
            raise ValueError("derived separation bounds are inconsistent")
        disposition = (
            Periodic1DAdmissibleSetDisposition.CERTIFIED_SEPARATED
            if lower_bound > definition.separation_resolution
            else Periodic1DAdmissibleSetDisposition.UNRESOLVED
        )
        spectral_evaluation = self._evaluate(
            definition,
            baseline,
            "separated-spectral-boundary",
            spectral_point,
            self._best_angle(operator, spectral_point),
        )
        operator_evaluation = self._evaluate(
            definition,
            baseline,
            "separated-operator-boundary",
            operator_point,
            self._angle(selected),
        )
        return Periodic1DAdmissibleSetCaseResult(
            thresholds,
            disposition,
            tuple(self._angle(item) for item in feasible_losses),
            None,
            spectral_evaluation,
            operator_evaluation,
            lower_bound,
            upper_bound,
            definition.separation_resolution,
        )

    def _evaluate(
        self,
        definition: Periodic1DConstrainedAdmissibleSetCalculationDefinition,
        baseline: Periodic1DMultibandAlignmentCalculationResult,
        role: str,
        parameter: tuple[float, float],
        selected_angle: float,
    ) -> Periodic1DAdmissibleSetParameterEvaluation:
        """Evaluate one identified proof point on training and staggered meshes.

        The selected angle and parameter are already frozen by training geometry.
        Evaluation values cannot alter either or change a disposition.
        """
        energy_unit = baseline.reference_transform.hopping_model.hopping_blocks[0].unit
        energy_scale = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
            definition.loss_energy_scale, energy_unit
        ).magnitude
        training_reference = self._matrices(baseline.reference_transform.source)
        training_attacked = self._matrices(baseline.attacked_transform.source)
        withheld_coordinates = baseline.withheld_target.coordinates
        interpolator = BlockHoppingInterpolator1D()
        withheld_reference = self._matrices(
            interpolator.execute(
                baseline.reference_transform.hopping_model, withheld_coordinates
            )
        )
        withheld_attacked = self._matrices(
            interpolator.execute(
                baseline.attacked_transform.hopping_model, withheld_coordinates
            )
        )
        training_candidate = self._candidate(
            training_reference, parameter, energy_scale
        )
        withheld_candidate = self._candidate(
            withheld_reference, parameter, energy_scale
        )
        rotation = self._rotation(selected_angle)
        training_rotated = self._conjugate(training_candidate, rotation)
        withheld_rotated = self._conjugate(withheld_candidate, rotation)
        rank = definition.multiband_baseline.retained_rank
        training_spectral = self._spectral_rms(
            training_candidate,
            baseline.training_target.eigenvalues.magnitude,
            energy_scale,
        )
        withheld_spectral = self._spectral_rms(
            withheld_candidate,
            baseline.withheld_target.eigenvalues.magnitude,
            energy_scale,
        )
        training_operator = self._operator_rms(
            training_rotated, training_attacked, energy_scale, rank
        )
        withheld_operator = self._operator_rms(
            withheld_rotated, withheld_attacked, energy_scale, rank
        )
        candidate_samples = ReciprocalOperatorSamples1D(
            baseline.reference_transform.source.coordinates,
            baseline.reference_transform.source.reciprocal_period,
            tuple(
                ComplexMatrixQuantity(matrix, energy_unit)
                for matrix in training_rotated
            ),
        )
        candidate_transform = ReciprocalOperatorFourierTransformer1D().execute(
            candidate_samples,
            baseline.reference_transform.mesh,
            definition.multiband_baseline.coordinate_absolute_tolerance,
            definition.multiband_baseline.reconstruction_absolute_tolerance,
        )
        truncator = BlockHoppingTruncator1D()
        locality = tuple(
            Periodic1DAdmissibleSetLocalityResult(
                maximum_range,
                truncator.execute(
                    baseline.reference_transform.hopping_model, maximum_range
                ).omitted_block_l2_norm,
                truncator.execute(
                    baseline.attacked_transform.hopping_model, maximum_range
                ).omitted_block_l2_norm,
                truncator.execute(
                    candidate_transform.hopping_model, maximum_range
                ).omitted_block_l2_norm,
            )
            for maximum_range in definition.locality_ranges
        )
        return Periodic1DAdmissibleSetParameterEvaluation(
            role,
            parameter,
            selected_angle,
            training_spectral,
            training_operator,
            withheld_spectral,
            withheld_operator,
            locality,
        )

    @staticmethod
    def _spectral_quadratic(
        reference: npt.NDArray[np.complex128],
        target: npt.NDArray[np.float64],
        energy_scale: float,
    ) -> Periodic1DQuadraticLoss:
        """Derive the exact squared spectral-RMS quadratic over shift/splitting."""
        rank = reference.shape[1]
        mean = np.trace(reference, axis1=1, axis2=2).real / float(rank)
        values = np.linalg.eigvalsh(reference)
        base = np.repeat(mean[:, None], rank, axis=1)
        features = np.stack(
            (
                np.full_like(values, energy_scale),
                values - base,
            ),
            axis=-1,
        )
        return Periodic1DConstrainedAdmissibleSetCalculator._quadratic(
            "spectral-training-rms-v1",
            None,
            features,
            base - target,
            energy_scale,
        )

    @staticmethod
    def _operator_quadratic(
        reference: npt.NDArray[np.complex128],
        target: npt.NDArray[np.complex128],
        energy_scale: float,
        angle: float,
    ) -> Periodic1DQuadraticLoss:
        """Derive one angle-resolved represented-operator squared-loss quadratic."""
        rank = reference.shape[1]
        identity = np.eye(rank, dtype=np.complex128)
        mean = np.trace(reference, axis1=1, axis2=2) / float(rank)
        base = mean[:, None, None] * identity
        traceless = reference - base
        rotation = Periodic1DConstrainedAdmissibleSetCalculator._rotation(angle)
        rotated = Periodic1DConstrainedAdmissibleSetCalculator._conjugate(
            traceless, rotation
        )
        features = np.stack(
            (
                np.broadcast_to(energy_scale * identity, reference.shape),
                rotated,
            ),
            axis=-1,
        )
        return Periodic1DConstrainedAdmissibleSetCalculator._quadratic(
            f"operator-training-rms-angle-{angle:.17g}",
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
    ) -> Periodic1DQuadraticLoss:
        r"""Complete a two-feature least-squares loss to centered quadratic form.

        The normalization is ``N * rank * energy_scale**2``.  For feature Gram matrix
        ``Q`` and linear coefficient ``b``, the center is ``-Q^{-1} b`` and the retained
        minimum is the completed-square constant.
        """
        sample_count = features.shape[0]
        rank = features.shape[1]
        normalization = float(sample_count * rank) * energy_scale**2
        matrix = np.empty((2, 2), dtype=np.float64)
        linear = np.empty(2, dtype=np.float64)
        for row in range(2):
            linear[row] = float(
                np.vdot(features[..., row], offset).real / normalization
            )
            for column in range(2):
                matrix[row, column] = float(
                    np.vdot(features[..., row], features[..., column]).real
                    / normalization
                )
        matrix = 0.5 * (matrix + matrix.T)
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

    @staticmethod
    def _axis_extreme(
        definition: Periodic1DConstrainedAdmissibleSetCalculationDefinition,
        loss: Periodic1DQuadraticLoss,
        threshold: float,
        axis: int,
        direction: float,
    ) -> tuple[tuple[float, float], float]:
        """Return one support point of an unclipped quadratic threshold ellipse."""
        budget = threshold**2 - loss.minimum_squared_loss
        if budget < 0.0:
            raise ValueError("requested admissible ellipsoid is empty")
        matrix = np.asarray(loss.quadratic_matrix)
        inverse = np.linalg.inv(matrix)
        unit = np.zeros(2, dtype=np.float64)
        unit[axis] = direction
        denominator = float(unit @ inverse @ unit)
        point = np.asarray(loss.center) + np.sqrt(budget / denominator) * (
            inverse @ unit
        )
        parameter = (float(point[0]), float(point[1]))
        if not definition.contains(parameter):
            raise ValueError("v1 certificate requires an unclipped ellipsoid")
        return parameter, float(point[axis])

    @staticmethod
    def _feasible_angles(
        definition: Periodic1DConstrainedAdmissibleSetCalculationDefinition,
        losses: tuple[Periodic1DQuadraticLoss, ...],
        thresholds: Periodic1DAdmissibleSetThresholds,
    ) -> tuple[float, ...]:
        """Return angles whose operator sublevel sets intersect the rectangle."""
        feasible: list[float] = []
        domain_minimum = (
            Periodic1DConstrainedAdmissibleSetCalculator._domain_minimum_squared_loss
        )
        for loss in losses:
            minimum = domain_minimum(definition, loss)
            if minimum <= thresholds.operator_rms_threshold**2:
                feasible.append(
                    Periodic1DConstrainedAdmissibleSetCalculator._angle(loss)
                )
        return tuple(feasible)

    @staticmethod
    def _domain_minimum_squared_loss(
        definition: Periodic1DConstrainedAdmissibleSetCalculationDefinition,
        loss: Periodic1DQuadraticLoss,
    ) -> float:
        """Minimize a positive quadratic exactly over the closed parameter box."""
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
            loss.squared_loss((float(point[0]), float(point[1])))
            for point in candidates
        )

    @staticmethod
    def _best_angle(
        losses: tuple[Periodic1DQuadraticLoss, ...],
        parameter: tuple[float, float],
    ) -> float:
        """Return the frozen angle with least operator loss at one parameter."""
        return Periodic1DConstrainedAdmissibleSetCalculator._angle(
            min(losses, key=lambda item: item.squared_loss(parameter))
        )

    @staticmethod
    def _angle(loss: Periodic1DQuadraticLoss) -> float:
        """Return an operator quadratic's required alignment angle."""
        if loss.alignment_angle is None:
            raise ValueError("operator loss must retain an alignment angle")
        return loss.alignment_angle

    @staticmethod
    def _candidate(
        reference: np.ndarray,
        parameter: tuple[float, float],
        energy_scale: float,
    ) -> np.ndarray:
        """Build the affine trace/shift/traceless-splitting candidate matrices."""
        rank = reference.shape[1]
        identity = np.eye(rank, dtype=np.complex128)
        mean = np.trace(reference, axis1=1, axis2=2) / float(rank)
        base = mean[:, None, None] * identity
        shift, splitting = parameter
        return np.asarray(
            base + shift * energy_scale * identity + splitting * (reference - base),
            dtype=np.complex128,
        )

    @staticmethod
    def _rotation(angle: float) -> npt.NDArray[np.complex128]:
        """Return the rank-two real unitary rotation at one radian angle."""
        return np.asarray(
            [
                [np.cos(angle), -np.sin(angle)],
                [np.sin(angle), np.cos(angle)],
            ],
            dtype=np.complex128,
        )

    @staticmethod
    def _conjugate(matrices: np.ndarray, rotation: np.ndarray) -> np.ndarray:
        """Conjugate each represented matrix by one global rotation."""
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
    def _spectral_rms(
        candidate: np.ndarray,
        target: np.ndarray,
        energy_scale: float,
    ) -> float:
        """Return normalized RMS ordered-eigenvalue loss."""
        values = np.linalg.eigvalsh(candidate)
        return float(np.sqrt(np.mean(np.abs(values - target) ** 2)) / energy_scale)

    @staticmethod
    def _operator_rms(
        candidate: np.ndarray,
        target: np.ndarray,
        energy_scale: float,
        rank: int,
    ) -> float:
        """Return normalized RMS represented-operator Frobenius loss."""
        squared = sum(
            float(np.linalg.norm(left - right) ** 2)
            for left, right in zip(candidate, target, strict=True)
        )
        return float(np.sqrt(squared / float(candidate.shape[0] * rank)) / energy_scale)

    @staticmethod
    def _matrices(samples: ReciprocalOperatorSamples1D) -> np.ndarray:
        """Stack identified reciprocal operator matrices without changing units."""
        return np.asarray(
            [matrix.magnitude for matrix in samples.matrices], dtype=np.complex128
        )


__all__ = ["Periodic1DConstrainedAdmissibleSetCalculator"]
