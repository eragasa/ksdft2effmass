"""Exact-byte independent verification for constrained admissible sets."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import ClassVar, Self

import numpy as np
from projectkoios.physkit.units import (
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.model_systems.analysis import BaseModelAnalysisVerifier
from ksdft2effmass.model_systems.verification import (
    BaseModelAnalysisVerification,
    VisualizationProjectionVerification,
)
from ksdft2effmass.serialization import SerializableValue
from ksdft2effmass.verification import CompositeVerification, VerificationObservation

from ..composite_band_alignment import Periodic1DCompositeBandAlignmentVerifier
from .reference import (
    Periodic1DConstrainedAdmissibleSetIndependentReferenceAnalyzer,
    Periodic1DConstrainedAdmissibleSetIndependentReferenceRequest,
)
from .results import (
    Periodic1DConstrainedAdmissibleSetCalculationResult,
)
from .visualizations import (
    Periodic1DAdmissibleSetProofPointVisualizationData,
    Periodic1DConstrainedAdmissibleSetVisualizationData,
)


class ConstrainedAdmissibleSetVerification(CompositeVerification):
    """Group independently reconstructed M3 observations."""


class ConstrainedAdmissibleSetUpstreamVerification(CompositeVerification):
    """Group exact embedded composite-result authentication observations."""


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DConstrainedAdmissibleSetVerification(BaseModelAnalysisVerification):
    """Authenticate M3 result bytes, upstream bytes, and visualization bytes."""

    subject_sha256: str
    visualization_data_sha256: str
    components: tuple[CompositeVerification, ...]

    component_types: ClassVar[Mapping[str, type[CompositeVerification]]] = (
        MappingProxyType(
            {
                "upstream_authentication": ConstrainedAdmissibleSetUpstreamVerification,
                "independent_reconstruction": ConstrainedAdmissibleSetVerification,
                "visualization_projection": VisualizationProjectionVerification,
            }
        )
    )

    def __post_init__(self) -> None:
        self._validate_common_fields()
        if tuple(type(component) for component in self.components) != tuple(
            self.component_types.values()
        ):
            raise ValueError(
                "components must match the constrained-admissible-set inventory"
            )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "subject_sha256": self.subject_sha256,
            "visualization_data_sha256": self.visualization_data_sha256,
            "components": {
                identifier: component.to_dict()
                for identifier, component in zip(
                    self.component_types, self.components, strict=True
                )
            },
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {"subject_sha256", "visualization_data_sha256", "components"}:
            raise ValueError("verification fields do not match")
        subject = values["subject_sha256"]
        visualization = values["visualization_data_sha256"]
        components_value = values["components"]
        if (
            type(subject) is not str
            or type(visualization) is not str
            or not isinstance(components_value, Mapping)
        ):
            raise TypeError("verification fields decode to wrong types")
        if set(components_value) != set(cls.component_types):
            raise ValueError("verification component fields do not match")
        components: list[CompositeVerification] = []
        for identifier, component_type in cls.component_types.items():
            value = components_value[identifier]
            if not isinstance(value, Mapping):
                raise TypeError("verification components must decode to mappings")
            components.append(component_type.from_dict(value))
        return cls(subject, visualization, tuple(components))


class Periodic1DConstrainedAdmissibleSetVerifier(
    BaseModelAnalysisVerifier[
        Periodic1DConstrainedAdmissibleSetCalculationResult,
        Periodic1DConstrainedAdmissibleSetVerification,
        Periodic1DConstrainedAdmissibleSetVisualizationData,
    ]
):
    """Own exact M3 bytes and independently authenticate every upstream layer."""

    __slots__ = ()

    @classmethod
    def _result_type(cls) -> type[Periodic1DConstrainedAdmissibleSetCalculationResult]:
        return Periodic1DConstrainedAdmissibleSetCalculationResult

    def _visualization_data(
        self,
    ) -> Periodic1DConstrainedAdmissibleSetVisualizationData:
        result = self._result
        unit = Unitless()
        compatible, separated = result.cases
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
        return Periodic1DConstrainedAdmissibleSetVisualizationData(
            parameter_names=("energy_shift_ratio", "splitting_scale"),
            parameter_bounds=MatrixQuantity(
                np.asarray(
                    (
                        result.configuration.energy_shift_ratio_bounds,
                        result.configuration.splitting_scale_bounds,
                    )
                ),
                unit,
            ),
            loss_channel_names=("spectral", "operator"),
            locality_channel_names=("reference", "attacked", "candidate"),
            proof_points=(proof_points[0], proof_points[1], proof_points[2]),
        )

    def _verification_types(self) -> tuple[type[CompositeVerification], ...]:
        return (
            ConstrainedAdmissibleSetUpstreamVerification,
            ConstrainedAdmissibleSetVerification,
            VisualizationProjectionVerification,
        )

    def _verification_components(
        self, visualization_data: Periodic1DConstrainedAdmissibleSetVisualizationData
    ) -> tuple[CompositeVerification, ...]:
        unit = Unitless()
        upstream = Periodic1DCompositeBandAlignmentVerifier(
            result_wire=self._result.composite_baseline.to_json()
        ).result()
        expected_digest = self._result.configuration.upstream_result_sha256
        upstream_comparisons: dict[str, VerificationObservation] = {
            "upstream_subject_sha256": VerificationObservation(
                ScalarQuantity(
                    0.0
                    if upstream.verification.subject_sha256 == expected_digest
                    else 1.0,
                    unit,
                ),
                ScalarQuantity(0.0, unit),
            ),
            "upstream_verification_passed": VerificationObservation(
                ScalarQuantity(0.0 if upstream.verification.passed else 1.0, unit),
                ScalarQuantity(0.0, unit),
            ),
        }
        independent = Periodic1DConstrainedAdmissibleSetIndependentReferenceAnalyzer(
            Periodic1DConstrainedAdmissibleSetIndependentReferenceRequest(
                self._result, visualization_data
            )
        ).execute()
        reconstruction: dict[str, VerificationObservation] = {
            name: comparison.result()
            for name, comparison in independent.comparisons.items()
            if name.startswith("result.")
        }
        projection: dict[str, VerificationObservation] = {
            name: comparison.result()
            for name, comparison in independent.comparisons.items()
            if name.startswith("visualization.")
        }
        return (
            ConstrainedAdmissibleSetUpstreamVerification(upstream_comparisons),
            ConstrainedAdmissibleSetVerification(reconstruction),
            VisualizationProjectionVerification(projection),
        )

    def _verification(
        self,
        *,
        visualization_data_sha256: str,
        components: tuple[CompositeVerification, ...],
    ) -> Periodic1DConstrainedAdmissibleSetVerification:
        return Periodic1DConstrainedAdmissibleSetVerification(
            self._subject_sha256, visualization_data_sha256, components
        )


__all__ = [
    "ConstrainedAdmissibleSetUpstreamVerification",
    "ConstrainedAdmissibleSetVerification",
    "Periodic1DConstrainedAdmissibleSetVerification",
    "Periodic1DConstrainedAdmissibleSetVerifier",
]
