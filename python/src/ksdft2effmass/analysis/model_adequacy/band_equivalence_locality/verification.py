"""Exact-byte independent verification for band-equivalence locality."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import ClassVar, Self

from projectkoios.physkit.units import ScalarQuantity, Unitless

from ksdft2effmass.analysis.diagnostics import (
    BaseDiagnosticAnalyzer,
    DiagnosticObservation,
)
from ksdft2effmass.model_systems.analysis import ModelAnalysisVerificationResult
from ksdft2effmass.model_systems.verification import (
    BaseModelAnalysisVerification,
    VisualizationProjectionVerification,
)
from ksdft2effmass.serialization import SerializableValue
from ksdft2effmass.verification import (
    CompositeVerification,
    VerificationObservation,
)

from .calculation import BandEquivalenceLocalityVerifier as DiagnosticVerifier
from .diagnostics import (
    BandEquivalenceLocalityDiagnosticMethodEnum,
    IndependentBandMaximumDefectAnalyzer,
    IndependentParentMaximumDefectAnalyzer,
    IndependentShellPowerMaximumDefectAnalyzer,
    StoredIdentityMaximumDefectAnalyzer,
)
from .reference import BandEquivalenceLocalityIndependentShellPowerAnalyzer
from .result import BandEquivalenceLocalityCalculationResult
from .visualizations.data import BandEquivalenceLocalityVisualizationData


class BandEquivalenceLocalityIndependentVerification(CompositeVerification):
    """Group independent scientific and stored-identity observations."""


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityVerificationThresholds:
    """Bind explicit unitless thresholds for every independent comparison."""

    stored_identity_maximum_defect: ScalarQuantity
    independent_parent_maximum_defect: ScalarQuantity
    independent_band_maximum_defect: ScalarQuantity
    independent_shell_power_maximum_defect: ScalarQuantity

    def __post_init__(self) -> None:
        for value, name in (
            (
                self.stored_identity_maximum_defect,
                "stored_identity_maximum_defect",
            ),
            (
                self.independent_parent_maximum_defect,
                "independent_parent_maximum_defect",
            ),
            (
                self.independent_band_maximum_defect,
                "independent_band_maximum_defect",
            ),
            (
                self.independent_shell_power_maximum_defect,
                "independent_shell_power_maximum_defect",
            ),
        ):
            if type(value) is not ScalarQuantity:
                raise TypeError(f"{name} must be ScalarQuantity")
            if type(value.unit) is not Unitless:
                raise ValueError(f"{name} must be explicitly unitless")
            if value.magnitude < 0.0:
                raise ValueError(f"{name} must be nonnegative")


@dataclass(frozen=True, slots=True, eq=False)
class BandEquivalenceLocalityVerification(BaseModelAnalysisVerification):
    """Authenticate exact result bytes and the plotting projection."""

    subject_sha256: str
    visualization_data_sha256: str
    components: tuple[CompositeVerification, ...]

    component_types: ClassVar[Mapping[str, type[CompositeVerification]]] = (
        MappingProxyType(
            {
                "band_equivalence_locality": (
                    BandEquivalenceLocalityIndependentVerification
                ),
                "visualization_projection": VisualizationProjectionVerification,
            }
        )
    )

    def __post_init__(self) -> None:
        self._validate_common_fields()
        if tuple(type(component) for component in self.components) != tuple(
            self.component_types.values()
        ):
            raise ValueError("components must match the band-equivalence inventory")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "subject_sha256": self.subject_sha256,
            "visualization_data_sha256": self.visualization_data_sha256,
            "components": {
                identifier: component.to_dict()
                for identifier, component in zip(
                    self.component_types,
                    self.components,
                    strict=True,
                )
            },
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "subject_sha256",
            "visualization_data_sha256",
            "components",
        }
        if set(values) != required:
            raise ValueError("band-equivalence verification fields do not match")
        subject_sha256 = values["subject_sha256"]
        visualization_data_sha256 = values["visualization_data_sha256"]
        components_value = values["components"]
        if (
            type(subject_sha256) is not str
            or type(visualization_data_sha256) is not str
        ):
            raise TypeError("verification digests must decode to built-in strings")
        if not isinstance(components_value, Mapping):
            raise TypeError("verification components must decode to a mapping")
        if set(components_value) != set(cls.component_types):
            raise ValueError("verification component fields do not match")
        components: list[CompositeVerification] = []
        for identifier, component_type in cls.component_types.items():
            component_value = components_value[identifier]
            if not isinstance(component_value, Mapping):
                raise TypeError("verification components must decode to mappings")
            components.append(component_type.from_dict(component_value))
        return cls(
            subject_sha256=subject_sha256,
            visualization_data_sha256=visualization_data_sha256,
            components=tuple(components),
        )


class BandEquivalenceLocalityResultVerifier:
    """Bind exact result bytes and an explicit independent diagnostic verifier."""

    __slots__ = (
        "_diagnostic_verifier",
        "_result",
        "_shell_power_analyzer",
        "_subject_sha256",
        "_thresholds",
    )

    def __init__(
        self,
        *,
        result_wire: bytes,
        diagnostic_verifier: DiagnosticVerifier,
        shell_power_analyzer: BandEquivalenceLocalityIndependentShellPowerAnalyzer,
        thresholds: BandEquivalenceLocalityVerificationThresholds,
    ) -> None:
        if type(result_wire) is not bytes:
            raise TypeError("result_wire must be built-in bytes")
        if type(diagnostic_verifier) is not DiagnosticVerifier:
            raise TypeError(
                "diagnostic_verifier must be BandEquivalenceLocalityVerifier"
            )
        if type(thresholds) is not BandEquivalenceLocalityVerificationThresholds:
            raise TypeError(
                "thresholds must be BandEquivalenceLocalityVerificationThresholds"
            )
        if (
            type(shell_power_analyzer)
            is not BandEquivalenceLocalityIndependentShellPowerAnalyzer
        ):
            raise TypeError(
                "shell_power_analyzer must be "
                "BandEquivalenceLocalityIndependentShellPowerAnalyzer"
            )
        self._subject_sha256 = hashlib.sha256(result_wire).hexdigest()
        self._result = BandEquivalenceLocalityCalculationResult.from_json(result_wire)
        if diagnostic_verifier.request.to_json() != self._result.request.to_json():
            raise ValueError("diagnostic verifier request does not match result bytes")
        if (
            diagnostic_verifier.retained_result.to_json()
            != self._result.diagnostics.to_json()
        ):
            raise ValueError("diagnostic verifier result does not match result bytes")
        if shell_power_analyzer.request.to_json() != self._result.request.to_json():
            raise ValueError("shell-power analyzer request does not match result bytes")
        self._diagnostic_verifier = diagnostic_verifier
        self._shell_power_analyzer = shell_power_analyzer
        self._thresholds = thresholds

    def _visualization_data(self) -> BandEquivalenceLocalityVisualizationData:
        names: list[str] = []
        parent_scales: list[float] = []
        amplitudes: list[float] = []
        minimum_thresholds: list[float] = []
        joint_thresholds: list[float] = []
        normalized_hopping: list[float | None] = []
        for case in self._result.diagnostics.cases:
            for point in case.points:
                names.append(case.name)
                parent_scales.append(point.parent_scale)
                amplitudes.append(point.amplitude)
                minimum_thresholds.append(point.minimum_operator_threshold)
                joint_thresholds.append(point.exact_spectrum_joint_operator_threshold)
                normalized_hopping.append(
                    point.normalized_excess_nonzero_hopping_weight
                )
        return BandEquivalenceLocalityVisualizationData(
            family=self._result.request.family,
            point_case_names=tuple(names),
            parent_scales=tuple(parent_scales),
            amplitudes=tuple(amplitudes),
            minimum_operator_thresholds=tuple(minimum_thresholds),
            joint_operator_thresholds=tuple(joint_thresholds),
            normalized_excess_nonzero_hopping_weights=tuple(normalized_hopping),
        )

    def _observation(
        self,
        value: float,
        tolerance: ScalarQuantity,
    ) -> VerificationObservation:
        return VerificationObservation(
            value=ScalarQuantity(value, Unitless()),
            tolerance=tolerance,
        )

    def _independent_shell_power_defect(self) -> float:
        """Compare every retained power value with the independent reference."""
        reference = self._shell_power_analyzer.execute()
        stored_points = tuple(
            (case.name, point)
            for case in self._result.diagnostics.cases
            for point in case.points
        )
        stored_identities = tuple(
            (name, point.parent_scale, point.amplitude) for name, point in stored_points
        )
        reference_identities = tuple(
            (point.case_name, point.parent_scale, point.amplitude)
            for point in reference.points
        )
        if stored_identities != reference_identities:
            raise ValueError(
                "stored point inventory does not match the shell-power reference"
            )
        defects: list[float] = []
        for (_, stored), expected in zip(
            stored_points,
            reference.points,
            strict=True,
        ):
            defects.extend(
                (
                    abs(
                        stored.reference_nyquist_power
                        - expected.reference_nyquist_power
                    ),
                    abs(
                        stored.comparison_nyquist_power
                        - expected.comparison_nyquist_power
                    ),
                )
            )
            stored_shell_indices = tuple(
                shell.shell_index for shell in stored.shell_diagnostics
            )
            expected_shell_indices = tuple(
                shell.shell_index for shell in expected.shells
            )
            if stored_shell_indices != expected_shell_indices:
                raise ValueError(
                    "stored shell inventory does not match the independent reference"
                )
            for stored_shell, expected_shell in zip(
                stored.shell_diagnostics,
                expected.shells,
                strict=True,
            ):
                defects.extend(
                    (
                        abs(
                            stored_shell.reference_shell_power
                            - expected_shell.reference_shell_power
                        ),
                        abs(
                            stored_shell.comparison_shell_power
                            - expected_shell.comparison_shell_power
                        ),
                        abs(
                            stored_shell.reference_omitted_power
                            - expected_shell.reference_omitted_power
                        ),
                        abs(
                            stored_shell.comparison_omitted_power
                            - expected_shell.comparison_omitted_power
                        ),
                        abs(
                            stored_shell.reference_total_omitted_power
                            - expected_shell.reference_total_omitted_power
                        ),
                        abs(
                            stored_shell.comparison_total_omitted_power
                            - expected_shell.comparison_total_omitted_power
                        ),
                    )
                )
        return max(defects, default=0.0)

    def result(
        self,
    ) -> ModelAnalysisVerificationResult[
        BandEquivalenceLocalityVerification,
        BandEquivalenceLocalityVisualizationData,
    ]:
        """Independently verify and authenticate the bound result bytes."""
        diagnostics = self._diagnostic_verifier.execute()
        independent_shell_power_defect = self._independent_shell_power_defect()
        diagnostic_analyzers: tuple[
            BaseDiagnosticAnalyzer[BandEquivalenceLocalityDiagnosticMethodEnum], ...
        ] = (
            StoredIdentityMaximumDefectAnalyzer(
                value=ScalarQuantity(
                    diagnostics.maximum_stored_identity_defect,
                    Unitless(),
                ),
                atol=self._thresholds.stored_identity_maximum_defect,
            ),
            IndependentParentMaximumDefectAnalyzer(
                value=ScalarQuantity(
                    diagnostics.maximum_independent_parent_defect,
                    Unitless(),
                ),
                atol=self._thresholds.independent_parent_maximum_defect,
            ),
            IndependentBandMaximumDefectAnalyzer(
                value=ScalarQuantity(
                    diagnostics.maximum_independent_band_defect,
                    Unitless(),
                ),
                atol=self._thresholds.independent_band_maximum_defect,
            ),
            IndependentShellPowerMaximumDefectAnalyzer(
                value=ScalarQuantity(independent_shell_power_defect, Unitless()),
                atol=self._thresholds.independent_shell_power_maximum_defect,
            ),
        )
        diagnostic_observations: dict[
            BandEquivalenceLocalityDiagnosticMethodEnum,
            DiagnosticObservation,
        ] = {}
        for diagnostic_analyzer in diagnostic_analyzers:
            if diagnostic_analyzer.method in diagnostic_observations:
                raise ValueError("diagnostic analyzer methods must be unique")
            diagnostic_observations[diagnostic_analyzer.method] = (
                diagnostic_analyzer.result()
            )
        verification_observations: dict[str, VerificationObservation] = {}
        for method, observation in diagnostic_observations.items():
            if type(observation.value) is not ScalarQuantity:
                raise TypeError("locality verification diagnostics must be scalar")
            verification_observations[method.to_wire()] = VerificationObservation(
                value=observation.value,
                tolerance=observation.atol,
            )
        independent = BandEquivalenceLocalityIndependentVerification(
            observations=verification_observations
        )
        visualization_data = self._visualization_data()
        projection = VisualizationProjectionVerification(
            observations={
                "projection_point_inventory_defect": self._observation(
                    0.0,
                    ScalarQuantity(0.0, Unitless()),
                )
            }
        )
        verification = BandEquivalenceLocalityVerification(
            subject_sha256=self._subject_sha256,
            visualization_data_sha256=hashlib.sha256(
                visualization_data.to_json()
            ).hexdigest(),
            components=(independent, projection),
        )
        return ModelAnalysisVerificationResult(
            verification=verification,
            visualization_data=visualization_data,
        )

    def admit_stored(
        self,
        *,
        verification: BandEquivalenceLocalityVerification,
        visualization_data: BandEquivalenceLocalityVisualizationData,
    ) -> ModelAnalysisVerificationResult[
        BandEquivalenceLocalityVerification,
        BandEquivalenceLocalityVisualizationData,
    ]:
        """Admit stored values only when exact canonical bytes are reproduced."""
        if type(verification) is not BandEquivalenceLocalityVerification:
            raise TypeError("verification has the wrong concrete type")
        if type(visualization_data) is not BandEquivalenceLocalityVisualizationData:
            raise TypeError("visualization_data has the wrong concrete type")
        expected = self.result()
        if verification.to_json() != expected.verification.to_json():
            raise ValueError(
                "stored verification differs from independent reconstruction"
            )
        if visualization_data.to_json() != expected.visualization_data.to_json():
            raise ValueError(
                "stored projection differs from independent reconstruction"
            )
        return expected


__all__ = [
    "BandEquivalenceLocalityIndependentVerification",
    "BandEquivalenceLocalityResultVerifier",
    "BandEquivalenceLocalityVerification",
    "BandEquivalenceLocalityVerificationThresholds",
]
