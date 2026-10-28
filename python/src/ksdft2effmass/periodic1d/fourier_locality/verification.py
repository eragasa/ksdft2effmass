"""Exact-byte independent verification for rank-one Fourier locality."""

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
from ksdft2effmass.verification import CompositeVerification

from .result import Periodic1DFourierLocalityCalculationResult
from .verification_values import Periodic1DFourierLocalityIndependentVerifier
from .visualization import Periodic1DFourierLocalityVisualizationData


class FourierLocalityVerification(CompositeVerification):
    """Group independently reconstructed Fourier-locality observations."""


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DFourierLocalityVerification(BaseModelAnalysisVerification):
    """Authenticate result bytes, visualization bytes, and comparison groups."""

    subject_sha256: str
    visualization_data_sha256: str
    components: tuple[CompositeVerification, ...]

    component_types: ClassVar[Mapping[str, type[CompositeVerification]]] = (
        MappingProxyType(
            {
                "fourier_locality": FourierLocalityVerification,
                "visualization_projection": VisualizationProjectionVerification,
            }
        )
    )

    def __post_init__(self) -> None:
        self._validate_common_fields()
        if tuple(type(component) for component in self.components) != tuple(
            self.component_types.values()
        ):
            raise ValueError("components must match the Fourier-locality inventory")

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
            raise ValueError("Fourier-locality verification fields do not match")
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


class Periodic1DFourierLocalityVerifier(
    BaseModelAnalysisVerifier[
        Periodic1DFourierLocalityCalculationResult,
        Periodic1DFourierLocalityVerification,
        Periodic1DFourierLocalityVisualizationData,
    ]
):
    """Own result-byte admission, independent reconstruction, and projection auth."""

    __slots__ = ()

    @classmethod
    def _result_type(cls) -> type[Periodic1DFourierLocalityCalculationResult]:
        return Periodic1DFourierLocalityCalculationResult

    def _visualization_data(self) -> Periodic1DFourierLocalityVisualizationData:
        result = self._result
        production = result.meshes[-1]
        unit = Unitless()
        return Periodic1DFourierLocalityVisualizationData(
            evaluation_reduced_momenta=result.evaluation.reduced_momenta,
            evaluation_lowest_energies=result.evaluation.lowest_energies,
            evaluation_adjacent_energies=result.evaluation.adjacent_energies,
            evaluation_sampled_gaps=result.evaluation.sampled_gaps,
            production_reduced_momenta=production.construction_reduced_momenta,
            production_sampled_gaps=VectorQuantity(
                production.adjacent_energies.magnitude
                - production.lowest_energies.magnitude,
                unit,
            ),
            construction_sizes=tuple(mesh.construction_size for mesh in result.meshes),
            maximum_ranges=result.configuration.maximum_ranges,
            interpolation_maximum_errors=VectorQuantity(
                np.asarray(
                    [
                        mesh.interpolation_maximum_error.magnitude
                        for mesh in result.meshes
                    ],
                    dtype=np.float64,
                ),
                unit,
            ),
            refinement_maximum_changes=VectorQuantity(
                np.max(result.normalized_refinement_changes.magnitude, axis=1),
                unit,
            ),
            truncation_maximum_errors=MatrixQuantity(
                np.asarray(
                    [
                        [
                            item.truncation_maximum_error.magnitude
                            for item in mesh.ranges
                        ]
                        for mesh in result.meshes
                    ],
                    dtype=np.float64,
                ),
                unit,
            ),
            mediated_total_maximum_errors=MatrixQuantity(
                np.asarray(
                    [
                        [
                            item.mediated_total_maximum_error.magnitude
                            for item in mesh.ranges
                        ]
                        for mesh in result.meshes
                    ],
                    dtype=np.float64,
                ),
                unit,
            ),
            direct_total_maximum_errors=MatrixQuantity(
                np.asarray(
                    [
                        [
                            item.direct_total_maximum_error.magnitude
                            for item in mesh.ranges
                        ]
                        for mesh in result.meshes
                    ],
                    dtype=np.float64,
                ),
                unit,
            ),
            omitted_coefficient_l2_norms=MatrixQuantity(
                np.asarray(
                    [
                        [
                            item.omitted_coefficient_l2_norm.magnitude
                            for item in mesh.ranges
                        ]
                        for mesh in result.meshes
                    ],
                    dtype=np.float64,
                ),
                unit,
            ),
            coefficient_l2_defects=MatrixQuantity(
                np.asarray(
                    [
                        [item.coefficient_l2_defect.magnitude for item in mesh.ranges]
                        for mesh in result.meshes
                    ],
                    dtype=np.float64,
                ),
                unit,
            ),
            sampled_maximum_defects=MatrixQuantity(
                np.asarray(
                    [
                        [item.sampled_maximum_defect.magnitude for item in mesh.ranges]
                        for mesh in result.meshes
                    ],
                    dtype=np.float64,
                ),
                unit,
            ),
            production_complete_representatives=(production.complete_representatives),
            production_complete_coefficient_magnitudes=VectorQuantity(
                np.abs(production.complete_coefficients.magnitude),
                unit,
            ),
            nondominated_masks=tuple(mesh.nondominated_mask for mesh in result.meshes),
            near_tie_masks=tuple(mesh.near_tie_mask for mesh in result.meshes),
            first_joint_passes=tuple(mesh.first_joint_pass for mesh in result.meshes),
            sustained_after_first_passes=tuple(
                mesh.sustained_after_first_pass for mesh in result.meshes
            ),
            minimum_sampled_gap=result.minimum_sampled_gap,
            sampled_gap_threshold=ScalarQuantity(
                result.configuration.sampled_gap_threshold,
                unit,
            ),
            application_threshold=ScalarQuantity(
                result.configuration.application_threshold,
                unit,
            ),
        )

    def _verification_types(self) -> tuple[type[CompositeVerification], ...]:
        return (
            FourierLocalityVerification,
            VisualizationProjectionVerification,
        )

    def _verification_components(
        self,
        visualization_data: Periodic1DFourierLocalityVisualizationData,
    ) -> tuple[CompositeVerification, ...]:
        independent = Periodic1DFourierLocalityIndependentVerifier().execute(
            self._result,
            visualization_data,
        )
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
            FourierLocalityVerification.evaluate(scientific),
            VisualizationProjectionVerification.evaluate(projection),
        )

    def _verification(
        self,
        *,
        visualization_data_sha256: str,
        components: tuple[CompositeVerification, ...],
    ) -> Periodic1DFourierLocalityVerification:
        return Periodic1DFourierLocalityVerification(
            subject_sha256=self._subject_sha256,
            visualization_data_sha256=visualization_data_sha256,
            components=components,
        )
