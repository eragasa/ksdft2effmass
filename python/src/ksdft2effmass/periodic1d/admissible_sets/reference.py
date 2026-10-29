"""Independent reconstruction for constrained admissible-set analysis."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

import numpy as np
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue
from ksdft2effmass.verification import MaximumAbsoluteErrorComparison

from ..composite_band_alignment import (
    Periodic1DCompositeBandAlignmentTransformResult,
)
from .definition import (
    Periodic1DAdmissibleSetThresholds,
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
from .visualizations import (
    Periodic1DAdmissibleSetProofPointVisualizationData,
    Periodic1DConstrainedAdmissibleSetVisualizationData,
)


@dataclass(frozen=True, slots=True)
class Periodic1DConstrainedAdmissibleSetIndependentReference:
    """Retain complete independently reconstructed field comparisons."""

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
            self, "comparisons", MappingProxyType(dict(self.comparisons))
        )


@dataclass(frozen=True, slots=True)
class Periodic1DConstrainedAdmissibleSetIndependentReferenceRequest:
    """Bind the admitted result and verifier-derived visualization projection."""

    result: Periodic1DConstrainedAdmissibleSetCalculationResult
    visualization_data: Periodic1DConstrainedAdmissibleSetVisualizationData

    def __post_init__(self) -> None:
        if type(self.result) is not Periodic1DConstrainedAdmissibleSetCalculationResult:
            raise TypeError("result has the wrong exact type")
        if (
            type(self.visualization_data)
            is not Periodic1DConstrainedAdmissibleSetVisualizationData
        ):
            raise TypeError("visualization_data has the wrong exact type")


class Periodic1DConstrainedAdmissibleSetIndependentReferenceAnalyzer:
    """Reconstruct one bound M3 result without production scientific actions."""

    __slots__ = ("_request",)

    def __init__(
        self, request: Periodic1DConstrainedAdmissibleSetIndependentReferenceRequest
    ) -> None:
        if (
            type(request)
            is not Periodic1DConstrainedAdmissibleSetIndependentReferenceRequest
        ):
            raise TypeError("request has the wrong exact type")
        self._request = request

    @property
    def request(self) -> Periodic1DConstrainedAdmissibleSetIndependentReferenceRequest:
        """Return the complete immutable reference-analysis request."""
        return self._request

    def execute(self) -> Periodic1DConstrainedAdmissibleSetIndependentReference:
        """Return complete field comparisons against direct NumPy reconstruction."""
        expected = self._expected_result()
        unit = Unitless()
        compatible, separated = expected.cases
        proof_points: list[Periodic1DAdmissibleSetProofPointVisualizationData] = []
        for case, evaluation in (
            (compatible, compatible.spectral_certificate_point),
            (separated, separated.spectral_certificate_point),
            (separated, separated.operator_certificate_point),
        ):
            proof_points.append(
                Periodic1DAdmissibleSetProofPointVisualizationData(
                    thresholds=case.thresholds,
                    disposition=case.disposition,
                    separation_bounds=VectorQuantity(
                        np.asarray(
                            (
                                case.separation_lower_bound,
                                case.separation_upper_bound,
                            )
                        ),
                        unit,
                    ),
                    evaluation=evaluation,
                )
            )
        expected_projection = Periodic1DConstrainedAdmissibleSetVisualizationData(
            parameter_names=("energy_shift_ratio", "splitting_scale"),
            parameter_bounds=MatrixQuantity(
                np.asarray(
                    (
                        expected.configuration.energy_shift_ratio_bounds,
                        expected.configuration.splitting_scale_bounds,
                    )
                ),
                unit,
            ),
            loss_channel_names=("spectral", "operator"),
            locality_channel_names=("reference", "attacked", "candidate"),
            proof_points=(proof_points[0], proof_points[1], proof_points[2]),
        )
        comparisons: dict[str, MaximumAbsoluteErrorComparison] = {}
        self._compare_values("result", self.request.result, expected, comparisons)
        self._compare_values(
            "visualization",
            self.request.visualization_data,
            expected_projection,
            comparisons,
        )
        return Periodic1DConstrainedAdmissibleSetIndependentReference(comparisons)

    def _expected_result(self) -> Periodic1DConstrainedAdmissibleSetCalculationResult:
        retained = self.request.result
        configuration = retained.configuration
        baseline = retained.composite_baseline
        reference = self._matrices(baseline.reference_operators)
        attacked = self._matrices(baseline.attacked_operators)
        scale = configuration.loss_energy_scale.magnitude
        spectral = self._spectral_quadratic(
            reference, baseline.construction_parent_spectrum.magnitude[:, :2], scale
        )
        operators = tuple(
            self._operator_quadratic(reference, attacked, scale, angle)
            for angle in configuration.alignment_angles
        )
        cases = (
            self._compatible_case(configuration, spectral, operators),
            self._separated_case(configuration, spectral, operators),
        )
        return Periodic1DConstrainedAdmissibleSetCalculationResult(
            configuration, baseline, spectral, operators, cases
        )

    def _compatible_case(
        self,
        configuration: Periodic1DConstrainedAdmissibleSetConfiguration,
        spectral: Periodic1DQuadraticLoss,
        operators: tuple[Periodic1DQuadraticLoss, ...],
    ) -> Periodic1DAdmissibleSetCaseResult:
        thresholds = configuration.compatible_thresholds
        witness = configuration.compatible_witness
        selected = min(
            operators,
            key=lambda item: self._squared_loss(item, witness),
        )
        evaluation = self._evaluation(
            "compatible-common-witness", witness, self._angle(selected)
        )
        return Periodic1DAdmissibleSetCaseResult(
            thresholds,
            Periodic1DAdmissibleSetDisposition.COMPATIBLE_WITNESS,
            self._feasible_angles(configuration, operators, thresholds),
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
        spectral: Periodic1DQuadraticLoss,
        operators: tuple[Periodic1DQuadraticLoss, ...],
    ) -> Periodic1DAdmissibleSetCaseResult:
        thresholds = configuration.separated_thresholds
        spectral_point, spectral_lower = self._axis_extreme(
            spectral, thresholds.spectral_rms_threshold, -1.0
        )
        feasible = tuple(
            item
            for item in operators
            if self._domain_minimum(configuration, item)
            <= thresholds.operator_rms_threshold**2
        )
        extrema = tuple(
            (item, *self._axis_extreme(item, thresholds.operator_rms_threshold, 1.0))
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
            if lower > configuration.separation_resolution
            else Periodic1DAdmissibleSetDisposition.UNRESOLVED
        )
        return Periodic1DAdmissibleSetCaseResult(
            thresholds,
            disposition,
            tuple(self._angle(item) for item in feasible),
            None,
            self._evaluation(
                "separated-spectral-boundary",
                spectral_point,
                self._best_angle(operators, spectral_point),
            ),
            self._evaluation(
                "separated-operator-boundary", operator_point, self._angle(selected)
            ),
            lower,
            upper,
            configuration.separation_resolution,
        )

    def _evaluation(
        self, role: str, parameter: tuple[float, float], angle: float
    ) -> Periodic1DAdmissibleSetParameterEvaluation:
        result = self.request.result
        configuration = result.configuration
        baseline = result.composite_baseline
        scale = configuration.loss_energy_scale.magnitude
        reference = self._matrices(baseline.reference_operators)
        attacked = self._matrices(baseline.attacked_operators)
        transforms = {transform.channel: transform for transform in baseline.transforms}
        reference_representatives, reference_blocks, reference_power = (
            self._ordinary_transform(transforms["reference"])
        )
        attacked_representatives, attacked_blocks, attacked_power = (
            self._ordinary_transform(transforms["attacked"])
        )
        coordinates = np.asarray(baseline.evaluation_reduced_momenta, dtype=np.float64)
        evaluation_reference = self._interpolate(
            coordinates, reference_representatives, reference_blocks
        )
        evaluation_attacked = self._interpolate(
            coordinates, attacked_representatives, attacked_blocks
        )
        construction_candidate = self._candidate(reference, parameter, scale)
        evaluation_candidate = self._candidate(evaluation_reference, parameter, scale)
        rotation = self._rotation(angle)
        construction_rotated = self._conjugate(construction_candidate, rotation)
        evaluation_rotated = self._conjugate(evaluation_candidate, rotation)
        cyclic_representatives = np.asarray(
            transforms["reference"].representatives, dtype=np.int64
        )
        candidate_blocks = self._fourier(
            np.asarray(baseline.construction_reduced_momenta, dtype=np.float64),
            construction_rotated,
            cyclic_representatives,
        )
        conversion_representative = transforms[
            "reference"
        ].cyclic_conversion_representative
        conversion_index = tuple(int(value) for value in cyclic_representatives).index(
            conversion_representative
        )
        candidate_power = float(
            np.linalg.norm(candidate_blocks[conversion_index]) ** 2
            / construction_rotated.shape[1]
        )
        keep = cyclic_representatives != conversion_representative
        candidate_representatives = cyclic_representatives[keep]
        candidate_ordinary_blocks = candidate_blocks[keep]
        locality = tuple(
            Periodic1DAdmissibleSetLocalityResult(
                maximum_range,
                reference_power,
                attacked_power,
                candidate_power,
                self._omitted_norm(
                    reference_representatives, reference_blocks, maximum_range
                ),
                self._omitted_norm(
                    attacked_representatives, attacked_blocks, maximum_range
                ),
                self._omitted_norm(
                    candidate_representatives, candidate_ordinary_blocks, maximum_range
                ),
            )
            for maximum_range in configuration.locality_ranges
        )
        return Periodic1DAdmissibleSetParameterEvaluation(
            role,
            parameter,
            angle,
            self._spectral_rms(
                construction_candidate,
                baseline.construction_parent_spectrum.magnitude[:, :2],
                scale,
            ),
            self._operator_rms(
                self._conjugate(construction_candidate, rotation), attacked, scale
            ),
            self._spectral_rms(
                evaluation_candidate,
                baseline.evaluation_parent_spectrum.magnitude[:, :2],
                scale,
            ),
            self._operator_rms(evaluation_rotated, evaluation_attacked, scale),
            locality,
        )

    def _ordinary_transform(
        self, transform: Periodic1DCompositeBandAlignmentTransformResult
    ) -> tuple[np.ndarray, np.ndarray, float]:
        representatives = np.asarray(transform.representatives, dtype=np.int64)
        blocks = np.asarray(
            [block.magnitude for block in transform.hopping_blocks], dtype=np.complex128
        )
        index = tuple(int(value) for value in representatives).index(
            transform.cyclic_conversion_representative
        )
        power = float(np.linalg.norm(blocks[index]) ** 2 / blocks.shape[1])
        keep = representatives != transform.cyclic_conversion_representative
        return representatives[keep], blocks[keep], power

    def _spectral_quadratic(
        self, reference: np.ndarray, target: np.ndarray, scale: float
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
        self, reference: np.ndarray, target: np.ndarray, scale: float, angle: float
    ) -> Periodic1DQuadraticLoss:
        rank = reference.shape[1]
        identity = np.eye(rank, dtype=np.complex128)
        mean = np.trace(reference, axis1=1, axis2=2) / float(rank)
        base = mean[:, None, None] * identity
        rotated = self._conjugate(reference - base, self._rotation(angle))
        features = np.stack(
            (np.broadcast_to(scale * identity, reference.shape), rotated), axis=-1
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
        features: np.ndarray,
        offset: np.ndarray,
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
            ]
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
        self, loss: Periodic1DQuadraticLoss, threshold: float, direction: float
    ) -> tuple[tuple[float, float], float]:
        inverse = np.linalg.inv(np.asarray(loss.quadratic_matrix))
        unit = np.asarray((0.0, direction))
        point = np.asarray(loss.center) + np.sqrt(
            (threshold**2 - loss.minimum_squared_loss) / float(unit @ inverse @ unit)
        ) * (inverse @ unit)
        return (float(point[0]), float(point[1])), float(point[1])

    def _domain_minimum(
        self,
        configuration: Periodic1DConstrainedAdmissibleSetConfiguration,
        loss: Periodic1DQuadraticLoss,
    ) -> float:
        center = np.asarray(loss.center)
        matrix = np.asarray(loss.quadratic_matrix)
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
            self._squared_loss(loss, (float(point[0]), float(point[1])))
            for point in candidates
        )

    def _feasible_angles(
        self,
        configuration: Periodic1DConstrainedAdmissibleSetConfiguration,
        losses: tuple[Periodic1DQuadraticLoss, ...],
        thresholds: Periodic1DAdmissibleSetThresholds,
    ) -> tuple[float, ...]:
        return tuple(
            self._angle(item)
            for item in losses
            if self._domain_minimum(configuration, item)
            <= thresholds.operator_rms_threshold**2
        )

    def _best_angle(
        self,
        losses: tuple[Periodic1DQuadraticLoss, ...],
        parameter: tuple[float, float],
    ) -> float:
        return self._angle(
            min(losses, key=lambda item: self._squared_loss(item, parameter))
        )

    def _squared_loss(
        self,
        loss: Periodic1DQuadraticLoss,
        parameter: tuple[float, float],
    ) -> float:
        delta = np.asarray(parameter, dtype=np.float64) - np.asarray(
            loss.center,
            dtype=np.float64,
        )
        return float(
            loss.minimum_squared_loss
            + delta @ np.asarray(loss.quadratic_matrix, dtype=np.float64) @ delta
        )

    def _angle(self, loss: Periodic1DQuadraticLoss) -> float:
        if loss.alignment_angle is None:
            raise ValueError("operator loss must retain an alignment angle")
        return loss.alignment_angle

    def _candidate(
        self, reference: np.ndarray, parameter: tuple[float, float], scale: float
    ) -> np.ndarray:
        rank = reference.shape[1]
        identity = np.eye(rank, dtype=np.complex128)
        mean = np.trace(reference, axis1=1, axis2=2) / float(rank)
        base = mean[:, None, None] * identity
        return np.asarray(
            base + parameter[0] * scale * identity + parameter[1] * (reference - base),
            dtype=np.complex128,
        )

    def _rotation(self, angle: float) -> np.ndarray:
        return np.asarray(
            [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]],
            dtype=np.complex128,
        )

    def _conjugate(self, matrices: np.ndarray, rotation: np.ndarray) -> np.ndarray:
        return np.asarray(
            np.einsum(
                "ab,kbc,cd->kad", rotation.conj().T, matrices, rotation, optimize=True
            ),
            dtype=np.complex128,
        )

    def _spectral_rms(
        self, candidate: np.ndarray, target: np.ndarray, scale: float
    ) -> float:
        return float(
            np.sqrt(np.mean(np.abs(np.linalg.eigvalsh(candidate) - target) ** 2))
            / scale
        )

    def _operator_rms(
        self, candidate: np.ndarray, target: np.ndarray, scale: float
    ) -> float:
        squared = sum(
            float(np.linalg.norm(left - right) ** 2)
            for left, right in zip(candidate, target, strict=True)
        )
        return float(
            np.sqrt(squared / float(candidate.shape[0] * candidate.shape[1])) / scale
        )

    def _fourier(
        self, reduced: np.ndarray, matrices: np.ndarray, representatives: np.ndarray
    ) -> np.ndarray:
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

    def _interpolate(
        self, reduced: np.ndarray, representatives: np.ndarray, blocks: np.ndarray
    ) -> np.ndarray:
        return np.asarray(
            np.einsum(
                "kr,rij->kij",
                np.exp(2j * np.pi * np.outer(reduced, representatives)),
                blocks,
                optimize=True,
            ),
            dtype=np.complex128,
        )

    def _omitted_norm(
        self, representatives: np.ndarray, blocks: np.ndarray, maximum_range: int
    ) -> float:
        return float(np.linalg.norm(blocks[np.abs(representatives) > maximum_range]))

    def _matrices(self, matrices: tuple[ComplexMatrixQuantity, ...]) -> np.ndarray:
        return np.asarray(
            [matrix.magnitude for matrix in matrices], dtype=np.complex128
        )

    def _compare_values(
        self,
        name: str,
        observed: SerializableValue,
        expected: SerializableValue,
        output: dict[str, MaximumAbsoluteErrorComparison],
    ) -> None:
        if isinstance(observed, BaseTypedRecord) and isinstance(
            expected, BaseTypedRecord
        ):
            self._compare_values(name, observed.to_dict(), expected.to_dict(), output)
            return
        if isinstance(observed, Mapping) and isinstance(expected, Mapping):
            for key in sorted(set(observed) | set(expected)):
                child = f"{name}.{key}"
                if key not in observed or key not in expected:
                    output[child] = self._exact(False)
                else:
                    self._compare_values(child, observed[key], expected[key], output)
            return
        if isinstance(observed, tuple) and isinstance(expected, tuple):
            output[f"{name}.length"] = self._exact(len(observed) == len(expected))
            for index, (left, right) in enumerate(
                zip(observed, expected, strict=False)
            ):
                self._compare_values(f"{name}[{index}]", left, right, output)
            return
        quantities = (
            ScalarQuantity,
            VectorQuantity,
            MatrixQuantity,
            ComplexMatrixQuantity,
        )
        if isinstance(observed, quantities) and isinstance(expected, quantities):
            output[name] = MaximumAbsoluteErrorComparison(
                observed,
                expected,
                ScalarQuantity(
                    self.request.result.configuration.verification_absolute_tolerance,
                    observed.unit,
                ),
            )
            return
        if observed is None and expected is None:
            output[name] = self._exact(True)
            return
        if type(observed) is float and type(expected) is float:
            unit = Unitless()
            output[name] = MaximumAbsoluteErrorComparison(
                ScalarQuantity(observed, unit),
                ScalarQuantity(expected, unit),
                ScalarQuantity(
                    self.request.result.configuration.verification_absolute_tolerance,
                    unit,
                ),
            )
            return
        if type(observed) in (bool, int, str) and type(expected) is type(observed):
            output[name] = self._exact(observed == expected)
            return
        output[name] = self._exact(False)

    def _exact(self, passes: bool) -> MaximumAbsoluteErrorComparison:
        unit = Unitless()
        return MaximumAbsoluteErrorComparison(
            ScalarQuantity(0.0 if passes else 1.0, unit),
            ScalarQuantity(0.0, unit),
            ScalarQuantity(0.0, unit),
        )


__all__ = [
    "Periodic1DConstrainedAdmissibleSetIndependentReference",
    "Periodic1DConstrainedAdmissibleSetIndependentReferenceAnalyzer",
    "Periodic1DConstrainedAdmissibleSetIndependentReferenceRequest",
]
