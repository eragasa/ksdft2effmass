"""Exact-byte independent verification for composite-band alignment."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import ClassVar, Self

import numpy as np
from projectkoios.physkit.units import MatrixQuantity, Unitless, VectorQuantity

from ksdft2effmass.model_systems.analysis import BaseModelAnalysisVerifier
from ksdft2effmass.model_systems.verification import (
    BaseModelAnalysisVerification,
    VisualizationProjectionVerification,
)
from ksdft2effmass.serialization import SerializableValue
from ksdft2effmass.verification import CompositeVerification

from .reference import (
    Periodic1DCompositeBandAlignmentIndependentReferenceAnalyzer,
    Periodic1DCompositeBandAlignmentIndependentReferenceRequest,
)
from .result import Periodic1DCompositeBandAlignmentCalculationResult
from .visualizations.data import (
    Periodic1DCompositeBandAlignmentVisualizationData,
)


class CompositeBandAlignmentVerification(CompositeVerification):
    """Group independently reconstructed composite-alignment observations."""


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DCompositeBandAlignmentVerification(BaseModelAnalysisVerification):
    """Authenticate result bytes, projection bytes, and comparison groups."""

    subject_sha256: str
    visualization_data_sha256: str
    components: tuple[CompositeVerification, ...]

    component_types: ClassVar[Mapping[str, type[CompositeVerification]]] = (
        MappingProxyType(
            {
                "composite_band_alignment": CompositeBandAlignmentVerification,
                "visualization_projection": VisualizationProjectionVerification,
            }
        )
    )

    def __post_init__(self) -> None:
        self._validate_common_fields()
        if tuple(type(component) for component in self.components) != tuple(
            self.component_types.values()
        ):
            raise ValueError("components must match the composite-alignment inventory")

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
        if set(values) != {
            "subject_sha256",
            "visualization_data_sha256",
            "components",
        }:
            raise ValueError("composite-alignment verification fields do not match")
        subject_sha256 = values["subject_sha256"]
        visualization_sha256 = values["visualization_data_sha256"]
        components_value = values["components"]
        if type(subject_sha256) is not str or type(visualization_sha256) is not str:
            raise TypeError("verification digests must decode to strings")
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
            visualization_data_sha256=visualization_sha256,
            components=tuple(components),
        )


class Periodic1DCompositeBandAlignmentVerifier(
    BaseModelAnalysisVerifier[
        Periodic1DCompositeBandAlignmentCalculationResult,
        Periodic1DCompositeBandAlignmentVerification,
        Periodic1DCompositeBandAlignmentVisualizationData,
    ]
):
    """Own exact result-byte admission and independent projection verification."""

    __slots__ = ()

    @classmethod
    def _result_type(cls) -> type[Periodic1DCompositeBandAlignmentCalculationResult]:
        return Periodic1DCompositeBandAlignmentCalculationResult

    def _visualization_data(
        self,
    ) -> Periodic1DCompositeBandAlignmentVisualizationData:
        result = self._result
        unit = Unitless()
        return Periodic1DCompositeBandAlignmentVisualizationData(
            evaluation_reduced_momenta=VectorQuantity(
                np.asarray(result.evaluation_reduced_momenta, dtype=np.float64),
                unit,
            ),
            evaluation_parent_spectrum=MatrixQuantity(
                result.evaluation_parent_spectrum.magnitude[:, :2],
                unit,
            ),
            maximum_ranges=tuple(item.maximum_range for item in result.ranges),
            channel_names=tuple(item.channel for item in result.ranges[0].channels),
            cyclic_conversion_powers=VectorQuantity(
                np.asarray(
                    [
                        transform.cyclic_conversion_power.magnitude
                        for transform in result.transforms
                    ],
                    dtype=np.float64,
                ),
                unit,
            ),
            ordinary_omitted_block_l2_norms=MatrixQuantity(
                np.asarray(
                    [
                        [
                            channel.ordinary_omitted_block_l2_norm.magnitude
                            for channel in item.channels
                        ]
                        for item in result.ranges
                    ],
                    dtype=np.float64,
                ),
                unit,
            ),
            construction_total_spectral_maximum_errors=MatrixQuantity(
                np.asarray(
                    [
                        [
                            channel.construction_total_spectral_maximum_error.magnitude
                            for channel in item.channels
                        ]
                        for item in result.ranges
                    ],
                    dtype=np.float64,
                ),
                unit,
            ),
            evaluation_interpolation_hamiltonian_maximum_errors=VectorQuantity(
                np.asarray(
                    [
                        transform.evaluation_interpolation_hamiltonian_maximum_error.magnitude
                        for transform in result.transforms
                    ],
                    dtype=np.float64,
                ),
                unit,
            ),
            evaluation_truncation_hamiltonian_maximum_errors=MatrixQuantity(
                np.asarray(
                    [
                        [
                            channel.evaluation_truncation_hamiltonian_maximum_error.magnitude
                            for channel in item.channels
                        ]
                        for item in result.ranges
                    ],
                    dtype=np.float64,
                ),
                unit,
            ),
            evaluation_total_hamiltonian_maximum_errors=MatrixQuantity(
                np.asarray(
                    [
                        [
                            channel.evaluation_total_hamiltonian_maximum_error.magnitude
                            for channel in item.channels
                        ]
                        for item in result.ranges
                    ],
                    dtype=np.float64,
                ),
                unit,
            ),
            evaluation_interpolation_spectral_maximum_errors=VectorQuantity(
                np.asarray(
                    [
                        transform.evaluation_interpolation_spectral_maximum_error.magnitude
                        for transform in result.transforms
                    ],
                    dtype=np.float64,
                ),
                unit,
            ),
            evaluation_truncation_spectral_maximum_errors=MatrixQuantity(
                np.asarray(
                    [
                        [
                            channel.evaluation_truncation_spectral_maximum_error.magnitude
                            for channel in item.channels
                        ]
                        for item in result.ranges
                    ],
                    dtype=np.float64,
                ),
                unit,
            ),
            evaluation_total_spectral_maximum_errors=MatrixQuantity(
                np.asarray(
                    [
                        [
                            channel.evaluation_total_spectral_maximum_error.magnitude
                            for channel in item.channels
                        ]
                        for item in result.ranges
                    ],
                    dtype=np.float64,
                ),
                unit,
            ),
            transform_representatives=result.transforms[0].representatives,
            hopping_block_frobenius_norms=MatrixQuantity(
                np.asarray(
                    [
                        [
                            float(np.linalg.norm(block.magnitude))
                            for block in transform.hopping_blocks
                        ]
                        for transform in result.transforms
                    ],
                    dtype=np.float64,
                ),
                unit,
            ),
            diagnostic_names=(
                "attack frame",
                "pointwise frame",
                "global frame",
                "attack operator",
                "pointwise operator",
                "global operator",
            ),
            diagnostic_values=VectorQuantity(
                np.asarray(
                    [
                        result.diagnostics.attack_frame_maximum_frobenius_defect,
                        result.diagnostics.pointwise_frame_maximum_frobenius_defect,
                        result.diagnostics.global_frame_maximum_frobenius_defect,
                        result.diagnostics.attacked_operator_maximum_frobenius_defect.magnitude,
                        result.diagnostics.pointwise_operator_maximum_frobenius_defect.magnitude,
                        result.diagnostics.global_operator_maximum_frobenius_defect.magnitude,
                    ],
                    dtype=np.float64,
                ),
                unit,
            ),
        )

    def _verification_types(self) -> tuple[type[CompositeVerification], ...]:
        return (
            CompositeBandAlignmentVerification,
            VisualizationProjectionVerification,
        )

    def _verification_components(
        self,
        visualization_data: Periodic1DCompositeBandAlignmentVisualizationData,
    ) -> tuple[CompositeVerification, ...]:
        independent = Periodic1DCompositeBandAlignmentIndependentReferenceAnalyzer(
            Periodic1DCompositeBandAlignmentIndependentReferenceRequest(
                self._result,
                visualization_data,
            )
        ).execute()
        scientific = {
            name: comparison
            for name, comparison in independent.comparisons.items()
            if not name.startswith("visualization_")
        }
        projection = {
            name: comparison
            for name, comparison in independent.comparisons.items()
            if name.startswith("visualization_")
        }
        return (
            CompositeBandAlignmentVerification.evaluate(scientific),
            VisualizationProjectionVerification.evaluate(projection),
        )

    def _verification(
        self,
        *,
        visualization_data_sha256: str,
        components: tuple[CompositeVerification, ...],
    ) -> Periodic1DCompositeBandAlignmentVerification:
        return Periodic1DCompositeBandAlignmentVerification(
            subject_sha256=self._subject_sha256,
            visualization_data_sha256=visualization_data_sha256,
            components=components,
        )


__all__ = [
    "CompositeBandAlignmentVerification",
    "Periodic1DCompositeBandAlignmentVerification",
    "Periodic1DCompositeBandAlignmentVerifier",
]
