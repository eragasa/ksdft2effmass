"""Request-bound analysis for constrained rank-two admissible sets."""

from __future__ import annotations

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array as ComplexArray
from projectkoios.numerics.numpy.typing import Float64Array as RealArray
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.solidstate import (
    BlockHoppingInterpolationRequest1D,
    BlockHoppingInterpolator1D,
    BlockHoppingModel1D,
    BlockHoppingTruncationRequest1D,
    BlockHoppingTruncator1D,
    CenteredEvenMeshCyclicToOrdinaryConverter1D,
    CenteredEvenMeshCyclicToOrdinaryRequest1D,
    CenteredEvenMeshCyclicToOrdinaryResult1D,
    CenteredUniformReciprocalMesh1D,
    ReciprocalOperatorFourierTransformer1D,
    ReciprocalOperatorFourierTransformRequest1D,
    ReciprocalOperatorSamples1D,
)

from ..composite_band_alignment import (
    Periodic1DCompositeBandAlignmentCalculationResult,
    Periodic1DCompositeBandAlignmentTransformResult,
    Periodic1DCompositeBandAlignmentVerifier,
)
from .definition import (
    Periodic1DAdmissibleSetThresholds,
    Periodic1DConstrainedAdmissibleSetAnalysisRequest,
    Periodic1DConstrainedAdmissibleSetConfiguration,
)
from .results import (
    Periodic1DAdmissibleSetCaseResult,
    Periodic1DAdmissibleSetDisposition,
    Periodic1DAdmissibleSetLocalityResult,
    Periodic1DAdmissibleSetParameterEvaluation,
    Periodic1DConstrainedAdmissibleSetCalculationResult,
    Periodic1DQuadraticLoss,
)


class Periodic1DConstrainedAdmissibleSetAnalyzer:
    """Analyze one authenticated composite result under frozen M3 controls."""

    __slots__ = ("_request", "_upstream_verifier")

    def __init__(
        self,
        request: Periodic1DConstrainedAdmissibleSetAnalysisRequest,
        upstream_verifier: Periodic1DCompositeBandAlignmentVerifier,
    ) -> None:
        if type(request) is not Periodic1DConstrainedAdmissibleSetAnalysisRequest:
            raise TypeError("request has the wrong exact type")
        if type(upstream_verifier) is not Periodic1DCompositeBandAlignmentVerifier:
            raise TypeError("upstream_verifier has the wrong exact type")
        self._request = request
        self._upstream_verifier = upstream_verifier

    @property
    def request(self) -> Periodic1DConstrainedAdmissibleSetAnalysisRequest:
        """Return the complete immutable analysis request."""
        return self._request

    @property
    def upstream_verifier(self) -> Periodic1DCompositeBandAlignmentVerifier:
        """Return the explicitly supplied upstream authentication action."""
        return self._upstream_verifier

    def execute(self) -> Periodic1DConstrainedAdmissibleSetCalculationResult:
        """Return quadratics, witnesses, certificates, and locality diagnostics."""
        authenticated = self.upstream_verifier.result()
        configuration = self.request.configuration
        if (
            authenticated.verification.subject_sha256
            != configuration.upstream_result_sha256
        ):
            raise ValueError("upstream verifier is bound to different result bytes")
        if not authenticated.verification.passed:
            raise ValueError("upstream composite-band result failed verification")
        baseline = self.request.upstream_result
        reference = self._matrices(baseline.reference_operators)
        attacked = self._matrices(baseline.attacked_operators)
        scale = configuration.loss_energy_scale.magnitude
        spectral = self._spectral_quadratic(
            reference, baseline.construction_parent_spectrum.magnitude[:, :2], scale
        )
        operator = tuple(
            self._operator_quadratic(reference, attacked, scale, angle)
            for angle in configuration.alignment_angles
        )
        return Periodic1DConstrainedAdmissibleSetCalculationResult(
            configuration,
            baseline,
            spectral,
            operator,
            (
                self._compatible_case(configuration, baseline, spectral, operator),
                self._separated_case(configuration, baseline, spectral, operator),
            ),
        )

    def _compatible_case(
        self,
        configuration: Periodic1DConstrainedAdmissibleSetConfiguration,
        baseline: Periodic1DCompositeBandAlignmentCalculationResult,
        spectral: Periodic1DQuadraticLoss,
        operator: tuple[Periodic1DQuadraticLoss, ...],
    ) -> Periodic1DAdmissibleSetCaseResult:
        thresholds = configuration.compatible_thresholds
        witness = configuration.compatible_witness
        selected = min(operator, key=lambda item: item.squared_loss(witness))
        if (
            spectral.rms_loss(witness) > thresholds.spectral_rms_threshold
            or selected.rms_loss(witness) > thresholds.operator_rms_threshold
        ):
            raise ValueError("the configured compatible witness is not feasible")
        evaluation = self._evaluate(
            configuration,
            baseline,
            "compatible-common-witness",
            witness,
            self._angle(selected),
        )
        return Periodic1DAdmissibleSetCaseResult(
            thresholds,
            Periodic1DAdmissibleSetDisposition.COMPATIBLE_WITNESS,
            self._feasible_angles(configuration, operator, thresholds),
            evaluation,
            evaluation,
            evaluation,
            0.0,
            0.0,
            configuration.separation_resolution,
        )

    def _separated_case(
        self,
        configuration: Periodic1DConstrainedAdmissibleSetConfiguration,
        baseline: Periodic1DCompositeBandAlignmentCalculationResult,
        spectral: Periodic1DQuadraticLoss,
        operator: tuple[Periodic1DQuadraticLoss, ...],
    ) -> Periodic1DAdmissibleSetCaseResult:
        thresholds = configuration.separated_thresholds
        spectral_point, spectral_lower = self._axis_extreme(
            configuration, spectral, thresholds.spectral_rms_threshold, 1, -1.0
        )
        feasible = tuple(
            item
            for item in operator
            if self._domain_minimum(configuration, item)
            <= thresholds.operator_rms_threshold**2
        )
        if not feasible:
            raise ValueError("the configured operator admissible set is empty")
        extrema = tuple(
            (
                item,
                *self._axis_extreme(
                    configuration, item, thresholds.operator_rms_threshold, 1, 1.0
                ),
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
        if lower > upper + configuration.quadratic_absolute_tolerance:
            raise ValueError("derived separation bounds are inconsistent")
        disposition = (
            Periodic1DAdmissibleSetDisposition.CERTIFIED_SEPARATED
            if lower > configuration.separation_resolution
            else Periodic1DAdmissibleSetDisposition.UNRESOLVED
        )
        return Periodic1DAdmissibleSetCaseResult(
            thresholds,
            disposition,
            tuple(self._angle(item) for item in feasible),
            None,
            self._evaluate(
                configuration,
                baseline,
                "separated-spectral-boundary",
                spectral_point,
                self._best_angle(operator, spectral_point),
            ),
            self._evaluate(
                configuration,
                baseline,
                "separated-operator-boundary",
                operator_point,
                self._angle(selected),
            ),
            lower,
            upper,
            configuration.separation_resolution,
        )

    def _evaluate(
        self,
        configuration: Periodic1DConstrainedAdmissibleSetConfiguration,
        baseline: Periodic1DCompositeBandAlignmentCalculationResult,
        role: str,
        parameter: tuple[float, float],
        selected_angle: float,
    ) -> Periodic1DAdmissibleSetParameterEvaluation:
        unit = Unitless()
        period = ScalarQuantity(1.0, unit)
        construction_coordinates = VectorQuantity(
            np.asarray(baseline.construction_reduced_momenta, dtype=np.float64), unit
        )
        evaluation_coordinates = VectorQuantity(
            np.asarray(baseline.evaluation_reduced_momenta, dtype=np.float64), unit
        )
        reference_samples = ReciprocalOperatorSamples1D(
            construction_coordinates, period, baseline.reference_operators
        )
        attacked_samples = ReciprocalOperatorSamples1D(
            construction_coordinates, period, baseline.attacked_operators
        )
        transforms = {transform.channel: transform for transform in baseline.transforms}
        reference_conversion = self._ordinary_conversion(
            transforms["reference"], period
        )
        attacked_conversion = self._ordinary_conversion(transforms["attacked"], period)
        evaluation_reference = BlockHoppingInterpolator1D(
            BlockHoppingInterpolationRequest1D(
                reference_conversion.ordinary, evaluation_coordinates
            )
        ).execute()
        evaluation_attacked = BlockHoppingInterpolator1D(
            BlockHoppingInterpolationRequest1D(
                attacked_conversion.ordinary, evaluation_coordinates
            )
        ).execute()
        scale = configuration.loss_energy_scale.magnitude
        construction_candidate = self._candidate(
            self._sample_matrices(reference_samples), parameter, scale
        )
        evaluation_candidate = self._candidate(
            self._sample_matrices(evaluation_reference), parameter, scale
        )
        rotation = self._rotation(selected_angle)
        construction_rotated = self._conjugate(construction_candidate, rotation)
        evaluation_rotated = self._conjugate(evaluation_candidate, rotation)
        candidate_samples = ReciprocalOperatorSamples1D(
            construction_coordinates,
            period,
            tuple(
                ComplexMatrixQuantity(matrix, unit) for matrix in construction_rotated
            ),
        )
        candidate_transform = ReciprocalOperatorFourierTransformer1D(
            ReciprocalOperatorFourierTransformRequest1D(
                candidate_samples,
                CenteredUniformReciprocalMesh1D(
                    period, baseline.configuration.construction_size
                ),
                baseline.configuration.dimensionless_absolute_tolerance,
                baseline.configuration.energy_absolute_tolerance,
            )
        ).execute()
        candidate_conversion = CenteredEvenMeshCyclicToOrdinaryConverter1D(
            CenteredEvenMeshCyclicToOrdinaryRequest1D(candidate_transform.hopping_model)
        ).execute()
        locality = tuple(
            Periodic1DAdmissibleSetLocalityResult(
                maximum_range,
                reference_conversion.conversion_power_per_matrix_dimension,
                attacked_conversion.conversion_power_per_matrix_dimension,
                candidate_conversion.conversion_power_per_matrix_dimension,
                self._omitted_norm(reference_conversion.ordinary, maximum_range),
                self._omitted_norm(attacked_conversion.ordinary, maximum_range),
                self._omitted_norm(candidate_conversion.ordinary, maximum_range),
            )
            for maximum_range in configuration.locality_ranges
        )
        return Periodic1DAdmissibleSetParameterEvaluation(
            role,
            parameter,
            selected_angle,
            self._spectral_rms(
                construction_candidate,
                baseline.construction_parent_spectrum.magnitude[:, :2],
                scale,
            ),
            self._operator_rms(
                construction_rotated, self._sample_matrices(attacked_samples), scale
            ),
            self._spectral_rms(
                evaluation_candidate,
                baseline.evaluation_parent_spectrum.magnitude[:, :2],
                scale,
            ),
            self._operator_rms(
                evaluation_rotated, self._sample_matrices(evaluation_attacked), scale
            ),
            locality,
        )

    def _ordinary_conversion(
        self,
        transform: Periodic1DCompositeBandAlignmentTransformResult,
        period: ScalarQuantity,
    ) -> CenteredEvenMeshCyclicToOrdinaryResult1D:
        conversion = CenteredEvenMeshCyclicToOrdinaryConverter1D(
            CenteredEvenMeshCyclicToOrdinaryRequest1D(
                BlockHoppingModel1D(
                    period, transform.representatives, transform.hopping_blocks
                )
            )
        ).execute()
        if (
            conversion.ordinary.representatives != transform.ordinary_representatives
            or conversion.conversion_representative
            != transform.cyclic_conversion_representative
        ):
            raise ValueError("upstream and reusable cyclic conversion supports differ")
        if (
            abs(
                conversion.conversion_power_per_matrix_dimension
                - transform.cyclic_conversion_power.magnitude
            )
            > self.request.configuration.quadratic_absolute_tolerance
        ):
            raise ValueError("upstream and reusable cyclic conversion powers differ")
        return conversion

    def _omitted_norm(self, model: BlockHoppingModel1D, maximum_range: int) -> float:
        return (
            BlockHoppingTruncator1D(
                BlockHoppingTruncationRequest1D(model, maximum_range)
            )
            .execute()
            .omitted_block_l2_norm
        )

    def _spectral_quadratic(
        self, reference: ComplexArray, target: RealArray, scale: float
    ) -> Periodic1DQuadraticLoss:
        rank = reference.shape[1]
        mean = np.trace(reference, axis1=1, axis2=2).real / float(rank)
        values = np.linalg.eigvalsh(reference)
        base = np.repeat(mean[:, None], rank, axis=1)
        features = np.stack((np.full_like(values, scale), values - base), axis=-1)
        return self._quadratic(
            "spectral-training-rms-v1", None, features, base - target, scale
        )

    def _operator_quadratic(
        self, reference: ComplexArray, target: ComplexArray, scale: float, angle: float
    ) -> Periodic1DQuadraticLoss:
        rank = reference.shape[1]
        identity = np.eye(rank, dtype=np.complex128)
        mean = np.trace(reference, axis1=1, axis2=2) / float(rank)
        base = mean[:, None, None] * identity
        features = np.stack(
            (
                np.broadcast_to(scale * identity, reference.shape),
                self._conjugate(reference - base, self._rotation(angle)),
            ),
            axis=-1,
        )
        return self._quadratic(
            f"operator-training-rms-angle-{angle:.17g}",
            angle,
            features,
            base - target,
            scale,
        )

    def _quadratic(
        self,
        channel_id: str,
        angle: float | None,
        features: ComplexArray | RealArray,
        offset: ComplexArray | RealArray,
        scale: float,
    ) -> Periodic1DQuadraticLoss:
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
            ],
            dtype=np.float64,
        )
        center = -np.linalg.solve(matrix, linear)
        minimum = float(np.vdot(offset, offset).real / normalization) - float(
            linear @ np.linalg.solve(matrix, linear)
        )
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

    def _axis_extreme(
        self,
        configuration: Periodic1DConstrainedAdmissibleSetConfiguration,
        loss: Periodic1DQuadraticLoss,
        threshold: float,
        axis: int,
        direction: float,
    ) -> tuple[tuple[float, float], float]:
        budget = threshold**2 - loss.minimum_squared_loss
        if budget < 0.0:
            raise ValueError("requested admissible ellipsoid is empty")
        inverse = np.linalg.inv(np.asarray(loss.quadratic_matrix))
        unit = np.zeros(2, dtype=np.float64)
        unit[axis] = direction
        point = np.asarray(loss.center) + np.sqrt(
            budget / float(unit @ inverse @ unit)
        ) * (inverse @ unit)
        parameter = (float(point[0]), float(point[1]))
        if not configuration.contains(parameter):
            raise ValueError("certificate requires an unclipped ellipsoid")
        return parameter, float(point[axis])

    def _feasible_angles(
        self,
        configuration: Periodic1DConstrainedAdmissibleSetConfiguration,
        losses: tuple[Periodic1DQuadraticLoss, ...],
        thresholds: Periodic1DAdmissibleSetThresholds,
    ) -> tuple[float, ...]:
        return tuple(
            self._angle(loss)
            for loss in losses
            if self._domain_minimum(configuration, loss)
            <= thresholds.operator_rms_threshold**2
        )

    def _domain_minimum(
        self,
        configuration: Periodic1DConstrainedAdmissibleSetConfiguration,
        loss: Periodic1DQuadraticLoss,
    ) -> float:
        center = np.asarray(loss.center, dtype=np.float64)
        matrix = np.asarray(loss.quadratic_matrix, dtype=np.float64)
        lower = np.asarray(
            (
                configuration.energy_shift_ratio_bounds[0],
                configuration.splitting_scale_bounds[0],
            )
        )
        upper = np.asarray(
            (
                configuration.energy_shift_ratio_bounds[1],
                configuration.splitting_scale_bounds[1],
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

    def _best_angle(
        self,
        losses: tuple[Periodic1DQuadraticLoss, ...],
        parameter: tuple[float, float],
    ) -> float:
        return self._angle(min(losses, key=lambda item: item.squared_loss(parameter)))

    def _angle(self, loss: Periodic1DQuadraticLoss) -> float:
        if loss.alignment_angle is None:
            raise ValueError("operator loss must retain an alignment angle")
        return loss.alignment_angle

    def _candidate(
        self, reference: ComplexArray, parameter: tuple[float, float], scale: float
    ) -> ComplexArray:
        rank = reference.shape[1]
        identity = np.eye(rank, dtype=np.complex128)
        mean = np.trace(reference, axis1=1, axis2=2) / float(rank)
        base = mean[:, None, None] * identity
        return np.asarray(
            base + parameter[0] * scale * identity + parameter[1] * (reference - base),
            dtype=np.complex128,
        )

    def _rotation(self, angle: float) -> ComplexArray:
        return np.asarray(
            [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]],
            dtype=np.complex128,
        )

    def _conjugate(
        self, matrices: ComplexArray, rotation: ComplexArray
    ) -> ComplexArray:
        return np.asarray(
            np.einsum(
                "ab,kbc,cd->kad", rotation.conj().T, matrices, rotation, optimize=True
            ),
            dtype=np.complex128,
        )

    def _spectral_rms(
        self, candidate: ComplexArray, target: RealArray, scale: float
    ) -> float:
        return float(
            np.sqrt(np.mean(np.abs(np.linalg.eigvalsh(candidate) - target) ** 2))
            / scale
        )

    def _operator_rms(
        self, candidate: ComplexArray, target: ComplexArray, scale: float
    ) -> float:
        squared = sum(
            float(np.linalg.norm(left - right) ** 2)
            for left, right in zip(candidate, target, strict=True)
        )
        return float(
            np.sqrt(squared / float(candidate.shape[0] * candidate.shape[1])) / scale
        )

    def _matrices(self, matrices: tuple[ComplexMatrixQuantity, ...]) -> ComplexArray:
        return np.asarray(
            [matrix.magnitude for matrix in matrices], dtype=np.complex128
        )

    def _sample_matrices(self, samples: ReciprocalOperatorSamples1D) -> ComplexArray:
        return np.asarray(
            [matrix.magnitude for matrix in samples.matrices], dtype=np.complex128
        )


__all__ = ["Periodic1DConstrainedAdmissibleSetAnalyzer"]
