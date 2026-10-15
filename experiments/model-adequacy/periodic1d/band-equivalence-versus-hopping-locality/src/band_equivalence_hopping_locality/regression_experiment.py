"""Historical finite-angle calculation retained only for regression."""

from __future__ import annotations

from typing import cast

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
from projectkoios.optimization.affine.complex_quadratic import (
    ComplexAffineResidualQuadraticTolerance,
)
from projectkoios.optimization.affine.factory import (
    ComplexAffineResidualQuadraticConstructorFactory,
    ComplexAffineResidualQuadraticMethod,
)
from projectkoios.optimization.quadratic.constrained import (
    ConstrainedQuadraticTolerance,
)
from projectkoios.optimization.quadratic.factory import (
    QuadraticSublevelSupportMethod,
    QuadraticSublevelSupportSolverFactory,
    RectangleQuadraticMinimizerFactory,
    RectangleQuadraticMinimizerMethod,
)
from projectkoios.optimization.quadratic.quadratic import (
    PositiveDefiniteQuadraticLoss,
)
from projectkoios.optimization.selection.finite import (
    first_minimum,
    indices_at_or_below,
)
from projectkoios.optimization.spaces.parameters import ParameterBound, ParameterSpace

from .regression_definition import (
    AdmissibleSetThresholds,
    ConstrainedAdmissibleSetsExperimentDefinition,
    QuadraticLoss2D,
)
from .regression_results import (
    AdmissibleSetCaseResult,
    AdmissibleSetDisposition,
    AdmissibleSetLocalityResult,
    AdmissibleSetPointEvaluation,
    ConstrainedAdmissibleSetsExperimentResult,
)


class ConstrainedAdmissibleSetsExperiment:
    """Derive KSD losses and compose certificates from owner capabilities.

    Notes
    -----
    KSD owns the parent calculation, represented-space feature construction,
    normalization, angle labels, thresholds, containment, certificate assembly,
    resolution, and disposition. Optimization owns complex affine-residual quadratic
    construction, completed-square evaluation, exact two-dimensional rectangle
    minimization, full-ellipsoid support, and ordered finite selection.
    """

    __slots__ = ()

    def execute(
        self, definition: ConstrainedAdmissibleSetsExperimentDefinition
    ) -> ConstrainedAdmissibleSetsExperimentResult:
        """Calculate the baseline, losses, diagnostics, and threshold cases.

        Parameters
        ----------
        definition
            Exact rank-two parent composition and experiment-owned controls.

        Returns
        -------
        ConstrainedAdmissibleSetsExperimentResult
            Correlated parent evidence, objective-construction quadratics,
            objective-evaluation diagnostics, locality, and bounded dispositions.

        Raises
        ------
        TypeError
            If ``definition`` is not the exact regression definition type.
        ValueError
            If a witness, owner result, containment premise, or certificate fails.
        """
        if type(definition) is not ConstrainedAdmissibleSetsExperimentDefinition:
            raise TypeError(
                "definition must be ConstrainedAdmissibleSetsExperimentDefinition"
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
            definition.owner_absolute_tolerance,
        )
        operators = tuple(
            self._operator_quadratic(
                reference,
                attacked,
                energy_scale,
                angle,
                definition.owner_absolute_tolerance,
            )
            for angle in definition.alignment_angles
        )
        compatible = self._compatible_case(definition, baseline, spectral, operators)
        separated = self._separated_case(definition, baseline, spectral, operators)
        return ConstrainedAdmissibleSetsExperimentResult(
            definition,
            baseline,
            spectral,
            operators,
            (compatible, separated),
        )

    def _compatible_case(
        self,
        definition: ConstrainedAdmissibleSetsExperimentDefinition,
        baseline: Periodic1DMultibandAlignmentCalculationResult,
        spectral: QuadraticLoss2D,
        operators: tuple[QuadraticLoss2D, ...],
    ) -> AdmissibleSetCaseResult:
        """Validate and retain the prospectively declared common witness."""
        thresholds = definition.compatible_thresholds
        witness = definition.compatible_witness
        evaluation = self._evaluation(
            definition,
            baseline,
            spectral,
            operators,
            "compatible-common-witness",
            witness,
        )
        if (
            evaluation.objective_construction_spectral_rms_loss
            > thresholds.spectral_rms_threshold
            or evaluation.objective_construction_operator_rms_loss
            > thresholds.operator_rms_threshold
        ):
            raise ValueError("compatible witness is not threshold-feasible")
        return AdmissibleSetCaseResult(
            thresholds,
            AdmissibleSetDisposition.COMPATIBLE_WITNESS,
            self._feasible_angles(definition, operators, thresholds),
            evaluation,
            evaluation,
            evaluation,
            0.0,
            0.0,
            definition.separation_resolution,
        )

    def _separated_case(
        self,
        definition: ConstrainedAdmissibleSetsExperimentDefinition,
        baseline: Periodic1DMultibandAlignmentCalculationResult,
        spectral: QuadraticLoss2D,
        operators: tuple[QuadraticLoss2D, ...],
    ) -> AdmissibleSetCaseResult:
        """Construct the KSD splitting-axis certificate from owner support points."""
        thresholds = definition.separated_thresholds
        spectral_point = self._support_point(
            definition,
            spectral,
            thresholds.spectral_rms_threshold,
            (0.0, -1.0),
        )
        feasible_indices = self._feasible_indices(definition, operators, thresholds)
        if not feasible_indices:
            raise ValueError("operator admissible set is empty")
        operator_supports = tuple(
            (
                index,
                self._support_point(
                    definition,
                    operators[index],
                    thresholds.operator_rms_threshold,
                    (0.0, 1.0),
                ),
            )
            for index in feasible_indices
        )
        selected_index = first_minimum(
            tuple(-point[1] for _, point in operator_supports)
        ).index
        operator_loss_index, operator_point = operator_supports[selected_index]
        lower_bound = max(0.0, spectral_point[1] - operator_point[1])
        upper_bound = float(
            np.linalg.norm(np.asarray(spectral_point) - np.asarray(operator_point))
        )
        if lower_bound > upper_bound + definition.owner_absolute_tolerance:
            raise ValueError("derived separation bounds are inconsistent")
        disposition = (
            AdmissibleSetDisposition.CERTIFIED_SEPARATED
            if lower_bound > definition.separation_resolution
            else AdmissibleSetDisposition.UNRESOLVED
        )
        spectral_evaluation = self._evaluation(
            definition,
            baseline,
            spectral,
            operators,
            "separated-spectral-boundary",
            spectral_point,
        )
        operator_evaluation = self._evaluation(
            definition,
            baseline,
            spectral,
            operators,
            "separated-operator-boundary",
            operator_point,
            forced_operator_index=operator_loss_index,
        )
        return AdmissibleSetCaseResult(
            thresholds,
            disposition,
            tuple(self._angle(operators[index]) for index in feasible_indices),
            None,
            spectral_evaluation,
            operator_evaluation,
            float(lower_bound),
            upper_bound,
            definition.separation_resolution,
        )

    @classmethod
    def _evaluation(
        cls,
        definition: ConstrainedAdmissibleSetsExperimentDefinition,
        baseline: Periodic1DMultibandAlignmentCalculationResult,
        spectral: QuadraticLoss2D,
        operators: tuple[QuadraticLoss2D, ...],
        role: str,
        parameter: tuple[float, float],
        *,
        forced_operator_index: int | None = None,
    ) -> AdmissibleSetPointEvaluation:
        """Evaluate a construction-selected point on both roles and locality."""
        if forced_operator_index is None:
            forced_operator_index = first_minimum(
                tuple(loss.squared_loss(parameter) for loss in operators)
            ).index
        selected = operators[forced_operator_index]
        angle = cls._angle(selected)
        energy_unit = baseline.reference_transform.hopping_model.hopping_blocks[0].unit
        energy_scale = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
            definition.loss_energy_scale, energy_unit
        ).magnitude
        construction_reference = cls._matrices(baseline.reference_transform.source)
        evaluation_coordinates = baseline.withheld_target.coordinates
        interpolator = BlockHoppingInterpolator1D()
        evaluation_reference = cls._matrices(
            interpolator.execute(
                baseline.reference_transform.hopping_model,
                evaluation_coordinates,
            )
        )
        evaluation_attacked = cls._matrices(
            interpolator.execute(
                baseline.attacked_transform.hopping_model,
                evaluation_coordinates,
            )
        )
        construction_candidate = cls._candidate(
            construction_reference, parameter, energy_scale
        )
        evaluation_candidate = cls._candidate(
            evaluation_reference, parameter, energy_scale
        )
        rotation = cls._rotation(angle)
        construction_rotated = cls._conjugate(construction_candidate, rotation)
        evaluation_rotated = cls._conjugate(evaluation_candidate, rotation)
        rank = definition.multiband_baseline.retained_rank
        candidate_samples = ReciprocalOperatorSamples1D(
            baseline.reference_transform.source.coordinates,
            baseline.reference_transform.source.reciprocal_period,
            tuple(
                ComplexMatrixQuantity(matrix, energy_unit)
                for matrix in construction_rotated
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
            AdmissibleSetLocalityResult(
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
        return AdmissibleSetPointEvaluation(
            role,
            parameter,
            angle,
            spectral.rms_loss(parameter),
            selected.rms_loss(parameter),
            cls._spectral_rms(
                evaluation_candidate,
                baseline.withheld_target.eigenvalues.magnitude,
                energy_scale,
            ),
            cls._operator_rms(
                evaluation_rotated,
                evaluation_attacked,
                energy_scale,
                rank,
            ),
            locality,
        )

    def _feasible_angles(
        self,
        definition: ConstrainedAdmissibleSetsExperimentDefinition,
        operators: tuple[QuadraticLoss2D, ...],
        thresholds: AdmissibleSetThresholds,
    ) -> tuple[float, ...]:
        """Return owner-filtered component angles in declaration order."""
        return tuple(
            self._angle(operators[index])
            for index in self._feasible_indices(definition, operators, thresholds)
        )

    def _feasible_indices(
        self,
        definition: ConstrainedAdmissibleSetsExperimentDefinition,
        operators: tuple[QuadraticLoss2D, ...],
        thresholds: AdmissibleSetThresholds,
    ) -> tuple[int, ...]:
        """Return components whose owner rectangle minima meet the threshold."""
        minimizer = RectangleQuadraticMinimizerFactory.create(
            RectangleQuadraticMinimizerMethod.NUMPY_DENSE,
            tolerance=self._owner_tolerance(definition),
        )
        bounds = self._parameter_space(definition)
        minima = tuple(
            minimizer.solve(self._owner_loss(loss), bounds).squared_loss
            for loss in operators
        )
        return indices_at_or_below(minima, thresholds.operator_rms_threshold**2)

    def _support_point(
        self,
        definition: ConstrainedAdmissibleSetsExperimentDefinition,
        loss: QuadraticLoss2D,
        rms_threshold: float,
        direction: tuple[float, float],
    ) -> tuple[float, float]:
        """Return owner full-ellipsoid support after KSD containment checking."""
        solver = QuadraticSublevelSupportSolverFactory.create(
            QuadraticSublevelSupportMethod.NUMPY_DENSE,
            tolerance=self._owner_tolerance(definition),
        )
        support = solver.solve(
            self._owner_loss(loss),
            rms_threshold**2,
            direction,
        )
        point = (support.point[0], support.point[1])
        if not definition.contains(point):
            raise ValueError("certificate requires an unclipped ellipsoid")
        return point

    @staticmethod
    def _spectral_quadratic(
        reference: npt.NDArray[np.complex128],
        target: npt.NDArray[np.float64],
        energy_scale: float,
        owner_absolute_tolerance: float,
    ) -> QuadraticLoss2D:
        """Derive the squared spectral-RMS quadratic over shift and splitting."""
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
        return ConstrainedAdmissibleSetsExperiment._quadratic(
            "spectral-objective-construction-rms-v1",
            None,
            features,
            base - target,
            energy_scale,
            owner_absolute_tolerance,
        )

    @staticmethod
    def _operator_quadratic(
        reference: npt.NDArray[np.complex128],
        target: npt.NDArray[np.complex128],
        energy_scale: float,
        angle: float,
        owner_absolute_tolerance: float,
    ) -> QuadraticLoss2D:
        """Derive one angle-resolved represented-operator squared-loss quadratic."""
        rank = reference.shape[1]
        identity = np.eye(rank, dtype=np.complex128)
        mean = np.trace(reference, axis1=1, axis2=2) / float(rank)
        base = mean[:, None, None] * identity
        rotation = ConstrainedAdmissibleSetsExperiment._rotation(angle)
        rotated = ConstrainedAdmissibleSetsExperiment._conjugate(
            reference - base, rotation
        )
        features = np.stack(
            (
                np.broadcast_to(energy_scale * identity, reference.shape),
                rotated,
            ),
            axis=-1,
        )
        return ConstrainedAdmissibleSetsExperiment._quadratic(
            f"operator-objective-construction-rms-angle-{angle:.17g}",
            angle,
            features,
            base - target,
            energy_scale,
            owner_absolute_tolerance,
        )

    @staticmethod
    def _quadratic(
        channel_id: str,
        angle: float | None,
        features: np.ndarray,
        offset: np.ndarray,
        energy_scale: float,
        owner_absolute_tolerance: float,
    ) -> QuadraticLoss2D:
        """Adapt KSD complex features to an owner-constructed labeled quadratic."""
        if features.ndim < 2 or features.shape[-1] != 2:
            raise ValueError("features must end in the two experiment coordinates")
        if offset.shape != features.shape[:-1]:
            raise ValueError("offset shape must match the feature observation shape")
        normalization = float(features.shape[0] * features.shape[1]) * energy_scale**2
        design = np.asarray(features, dtype=np.complex128).reshape((-1, 2), order="C")
        targets = -np.asarray(offset, dtype=np.complex128).reshape(-1, order="C")
        design_matrix = tuple(tuple(complex(value) for value in row) for row in design)
        target_vector = tuple(complex(value) for value in targets)
        weights = (1.0 / normalization,) * len(target_vector)
        constructor = ComplexAffineResidualQuadraticConstructorFactory.create(
            ComplexAffineResidualQuadraticMethod.NUMPY_DENSE,
            tolerance=ComplexAffineResidualQuadraticTolerance(
                absolute=owner_absolute_tolerance,
                relative=0.0,
            ),
        )
        owner_loss = constructor.construct(
            design_matrix,
            target_vector,
            weights=weights,
        )
        if owner_loss.dimension != 2:
            raise ValueError("owner quadratic must use both experiment coordinates")
        owner_matrix = owner_loss.matrix
        if type(owner_matrix) is not tuple:
            raise TypeError("owner quadratic matrix must use dense tuple storage")
        matrix = cast(tuple[tuple[float, ...], ...], owner_matrix)
        return QuadraticLoss2D(
            channel_id,
            angle,
            (owner_loss.center[0], owner_loss.center[1]),
            (
                (matrix[0][0], matrix[0][1]),
                (matrix[1][0], matrix[1][1]),
            ),
            owner_loss.minimum_squared_loss,
        )

    @staticmethod
    def _owner_tolerance(
        definition: ConstrainedAdmissibleSetsExperimentDefinition,
    ) -> ConstrainedQuadraticTolerance:
        """Map the experiment's adapter tolerance to the owner contract."""
        return ConstrainedQuadraticTolerance(
            absolute=definition.owner_absolute_tolerance,
            relative=0.0,
        )

    @staticmethod
    def _owner_loss(loss: QuadraticLoss2D) -> PositiveDefiniteQuadraticLoss:
        """Map one labeled KSD loss to unit-free owner state."""
        return PositiveDefiniteQuadraticLoss(
            loss.center,
            loss.quadratic_matrix,
            loss.minimum_squared_loss,
        )

    @staticmethod
    def _parameter_space(
        definition: ConstrainedAdmissibleSetsExperimentDefinition,
    ) -> ParameterSpace:
        """Map the named KSD rectangle to ordered owner bounds."""
        return ParameterSpace(
            (
                ParameterBound(
                    "energy_shift_ratio",
                    definition.energy_shift_ratio_bounds[0],
                    definition.energy_shift_ratio_bounds[1],
                ),
                ParameterBound(
                    "splitting_scale",
                    definition.splitting_scale_bounds[0],
                    definition.splitting_scale_bounds[1],
                ),
            )
        )

    @staticmethod
    def _angle(loss: QuadraticLoss2D) -> float:
        """Return an operator loss's mandatory KSD angle label."""
        if loss.alignment_angle is None:
            raise ValueError("operator loss must retain an alignment angle")
        return loss.alignment_angle

    @staticmethod
    def _candidate(
        reference: npt.NDArray[np.complex128],
        parameter: tuple[float, float],
        energy_scale: float,
    ) -> npt.NDArray[np.complex128]:
        """Construct the affine trace/shift/traceless-splitting family."""
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
    def _spectral_rms(
        candidate: npt.NDArray[np.complex128],
        target: npt.NDArray[np.float64],
        energy_scale: float,
    ) -> float:
        """Return normalized ordered-eigenvalue RMS loss."""
        return float(
            np.sqrt(np.mean(np.abs(np.linalg.eigvalsh(candidate) - target) ** 2))
            / energy_scale
        )

    @staticmethod
    def _operator_rms(
        candidate: npt.NDArray[np.complex128],
        target: npt.NDArray[np.complex128],
        energy_scale: float,
        rank: int,
    ) -> float:
        """Return normalized represented-operator Frobenius RMS loss."""
        squared = sum(
            float(np.linalg.norm(left - right) ** 2)
            for left, right in zip(candidate, target, strict=True)
        )
        return float(np.sqrt(squared / float(candidate.shape[0] * rank)) / energy_scale)

    @staticmethod
    def _rotation(angle: float) -> npt.NDArray[np.complex128]:
        """Return the rank-two real rotation for one frozen angle."""
        return np.asarray(
            [
                [np.cos(angle), -np.sin(angle)],
                [np.sin(angle), np.cos(angle)],
            ],
            dtype=np.complex128,
        )

    @staticmethod
    def _conjugate(
        matrices: npt.NDArray[np.complex128],
        rotation: npt.NDArray[np.complex128],
    ) -> npt.NDArray[np.complex128]:
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
    def _matrices(
        samples: ReciprocalOperatorSamples1D,
    ) -> npt.NDArray[np.complex128]:
        """Stack one typed reciprocal-operator sample sequence."""
        return np.asarray(
            [matrix.magnitude for matrix in samples.matrices],
            dtype=np.complex128,
        )


__all__ = ["ConstrainedAdmissibleSetsExperiment"]
