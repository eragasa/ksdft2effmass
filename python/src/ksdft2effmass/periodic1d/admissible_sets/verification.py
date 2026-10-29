"""Typed verification values for constrained admissible sets."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import ClassVar, Self

from ksdft2effmass.model_systems.verification import (
    BaseModelAnalysisVerification,
    VisualizationProjectionVerification,
)
from ksdft2effmass.serialization import SerializableValue
from ksdft2effmass.verification import CompositeVerification


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


__all__ = [
    "ConstrainedAdmissibleSetUpstreamVerification",
    "ConstrainedAdmissibleSetVerification",
    "Periodic1DConstrainedAdmissibleSetVerification",
]
