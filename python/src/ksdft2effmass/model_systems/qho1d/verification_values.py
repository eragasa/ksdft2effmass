"""Composable verification values for direct QHO1D calculations."""

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


class Qho1dSweepVerification(CompositeVerification):
    """Decode the retained flat-sweep verification component."""


class Qho1dSpatialRepresentationVerification(CompositeVerification):
    """Compose checks of finite-grid geometry and represented dimensions."""


class Qho1dSampledStateAlignmentVerification(CompositeVerification):
    """Compose checks of Gram correction and the sampled-state injection."""


class Qho1dHamiltonianComparisonVerification(CompositeVerification):
    """Compose checks of aligned Hamiltonians and discrepancy channels."""


class Qho1dResidualVerification(CompositeVerification):
    """Compose checks of the full-space intertwining residual."""


class Qho1dStateComparisonVerification(CompositeVerification):
    """Compose independent checks of the selected state-resolved comparison."""


@dataclass(frozen=True, slots=True, eq=False)
class Qho1dVerification(BaseModelAnalysisVerification):
    """Authenticate and compose one direct QHO1D verification.

    Parameters
    ----------
    subject_sha256
        SHA-256 digest of the exact calculation-result bytes.
    visualization_data_sha256
        SHA-256 digest of the verifier-derived visualization projection.
    components
        Ordered operation-named semantic verification values. The retained flat-case
        three-component inventory is also accepted for exact artifact decoding.

    Raises
    ------
    TypeError
        A digest or component container has the wrong exact type.
    ValueError
        A digest is malformed, components differ from the declared inventory, or
        observation names collide.
    """

    subject_sha256: str
    visualization_data_sha256: str
    components: tuple[CompositeVerification, ...]

    component_types: ClassVar[Mapping[str, type[CompositeVerification]]] = (
        MappingProxyType(
            {
                "spatial_representation": Qho1dSpatialRepresentationVerification,
                "sampled_state_alignment": Qho1dSampledStateAlignmentVerification,
                "hamiltonian_comparison": Qho1dHamiltonianComparisonVerification,
                "residual": Qho1dResidualVerification,
                "state_comparison": Qho1dStateComparisonVerification,
                "visualization_projection": VisualizationProjectionVerification,
            }
        )
    )
    retained_component_types: ClassVar[Mapping[str, type[CompositeVerification]]] = (
        MappingProxyType(
            {
                "sweep": Qho1dSweepVerification,
                "state_comparison": Qho1dStateComparisonVerification,
                "visualization_projection": VisualizationProjectionVerification,
            }
        )
    )

    def __post_init__(self) -> None:
        self._validate_digest(self.subject_sha256, "subject_sha256")
        self._validate_digest(
            self.visualization_data_sha256, "visualization_data_sha256"
        )
        if not isinstance(self.components, tuple):
            raise TypeError("components must be a tuple")
        observed_types = tuple(type(component) for component in self.components)
        supported_types = (
            tuple(self.component_types.values()),
            tuple(self.retained_component_types.values()),
        )
        if observed_types not in supported_types:
            raise ValueError("components must match a QHO1D verification inventory")
        names: set[str] = set()
        for component in self.components:
            overlap = names.intersection(component.observations)
            if overlap:
                raise ValueError("verification observation names must be unique")
            names.update(component.observations)

    @property
    def passed(self) -> bool:
        """Return whether every verification observation passes.

        Returns
        -------
        bool
            ``True`` exactly when every component passes.
        """
        return all(component.passed for component in self.components)

    @property
    def checks(self) -> Mapping[str, float]:
        """Return a read-only mapping of discrepancy magnitudes.

        Returns
        -------
        Mapping[str, float]
            Flattened operation-qualified observations.
        """
        return MappingProxyType(
            {
                name: observation.value.magnitude
                for component in self.components
                for name, observation in component.observations.items()
            }
        )

    @property
    def check_tolerances(self) -> Mapping[str, float]:
        """Return a read-only mapping of observation tolerances.

        Returns
        -------
        Mapping[str, float]
            Tolerances aligned exactly with :attr:`checks`.
        """
        return MappingProxyType(
            {
                name: observation.tolerance.magnitude
                for component in self.components
                for name, observation in component.observations.items()
            }
        )

    def authenticated_visualization_data_sha256(self) -> str:
        """Return the authenticated visualization-projection digest.

        Returns
        -------
        str
            Lowercase SHA-256 digest calculated before verification composition.
        """
        return self.visualization_data_sha256

    def _mapping(self) -> Mapping[str, SerializableValue]:
        component_types = (
            self.component_types
            if tuple(type(component) for component in self.components)
            == tuple(self.component_types.values())
            else self.retained_component_types
        )
        return {
            "subject_sha256": self.subject_sha256,
            "visualization_data_sha256": self.visualization_data_sha256,
            "components": {
                identifier: component.to_dict()
                for identifier, component in zip(
                    component_types, self.components, strict=True
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
            raise ValueError("QHO1D verification fields do not match")
        subject_sha256 = values["subject_sha256"]
        visualization_sha256 = values["visualization_data_sha256"]
        components_value = values["components"]
        if type(subject_sha256) is not str or type(visualization_sha256) is not str:
            raise TypeError("QHO1D verification digests must decode to strings")
        if not isinstance(components_value, Mapping):
            raise TypeError("QHO1D verification components must decode to a mapping")
        if set(components_value) == set(cls.component_types):
            component_types = cls.component_types
        elif set(components_value) == set(cls.retained_component_types):
            component_types = cls.retained_component_types
        else:
            raise ValueError("QHO1D verification component fields do not match")
        components: list[CompositeVerification] = []
        for identifier, component_type in component_types.items():
            component_value = components_value[identifier]
            if not isinstance(component_value, Mapping):
                raise TypeError("verification components must decode to mappings")
            components.append(component_type.from_dict(component_value))
        return cls(
            subject_sha256=subject_sha256,
            visualization_data_sha256=visualization_sha256,
            components=tuple(components),
        )

    @staticmethod
    def _validate_digest(value: str, name: str) -> None:
        if (
            type(value) is not str
            or len(value) != 64
            or any(character not in "0123456789abcdef" for character in value)
        ):
            raise ValueError(f"{name} must be a lowercase SHA-256 digest")
