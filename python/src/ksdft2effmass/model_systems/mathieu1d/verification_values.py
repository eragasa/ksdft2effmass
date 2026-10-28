"""Composable verification values for direct Mathieu1D calculations."""

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


class Mathieu1dIndependentVerification(CompositeVerification):
    """Compose independent reconstruction checks for all result fields.

    Notes
    -----
    Observation names retain complete typed-field paths. The component therefore
    exposes missing, additional, reordered, or numerically different values instead of
    reducing verification to one aggregate norm.
    """


@dataclass(frozen=True, slots=True, eq=False)
class Mathieu1dVerification(BaseModelAnalysisVerification):
    """Authenticate and compose one direct Mathieu1D verification.

    Parameters
    ----------
    subject_sha256
        Lowercase SHA-256 of the exact immutable result bytes admitted by the verifier.
    visualization_data_sha256
        Lowercase SHA-256 of canonical typed visualization-projection bytes.
    components
        Ordered independent-reconstruction and visualization-projection components.

    Notes
    -----
    Digest identity binds bytes; it does not establish producer causality, scientific
    validity, evidence sealing, or a trusted timestamp.
    """

    subject_sha256: str
    visualization_data_sha256: str
    components: tuple[CompositeVerification, ...]

    component_types: ClassVar[Mapping[str, type[CompositeVerification]]] = (
        MappingProxyType(
            {
                "independent_reconstruction": Mathieu1dIndependentVerification,
                "visualization_projection": VisualizationProjectionVerification,
            }
        )
    )

    def __post_init__(self) -> None:
        # The base validates digest syntax, global observation-name uniqueness, and
        # aggregate pass reduction before this model fixes component order.
        self._validate_common_fields()
        if tuple(type(value) for value in self.components) != tuple(
            self.component_types.values()
        ):
            raise ValueError(
                "components must match the Mathieu1D verification inventory"
            )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "subject_sha256": self.subject_sha256,
            "visualization_data_sha256": self.visualization_data_sha256,
            "components": {
                name: component.to_dict()
                for name, component in zip(
                    self.component_types, self.components, strict=True
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
            raise ValueError("Mathieu1D verification fields do not match")
        subject_sha256 = values["subject_sha256"]
        visualization_data_sha256 = values["visualization_data_sha256"]
        components_value = values["components"]
        if (
            type(subject_sha256) is not str
            or type(visualization_data_sha256) is not str
        ):
            raise TypeError("Mathieu1D verification digests must decode to strings")
        if not isinstance(components_value, Mapping):
            raise TypeError(
                "Mathieu1D verification components must decode to a mapping"
            )
        if set(components_value) != set(cls.component_types):
            raise ValueError("Mathieu1D verification component fields do not match")
        # Reconstruct in the declared mapping order so wire order and semantic order
        # cannot drift independently.
        components: list[CompositeVerification] = []
        for name, component_type in cls.component_types.items():
            value = components_value[name]
            if not isinstance(value, Mapping):
                raise TypeError("verification components must decode to mappings")
            components.append(component_type.from_dict(value))
        return cls(
            subject_sha256=subject_sha256,
            visualization_data_sha256=visualization_data_sha256,
            components=tuple(components),
        )


__all__ = ["Mathieu1dIndependentVerification", "Mathieu1dVerification"]
