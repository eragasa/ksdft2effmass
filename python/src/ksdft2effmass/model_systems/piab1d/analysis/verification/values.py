"""Immutable composable PIAB1D model-analysis verification value."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import ClassVar, Self

from ksdft2effmass.analysis import (
    DiagnosticVerification,
    EigensystemVerification,
    KineticPotentialDecompositionVerification,
    RelativeErrorConvergenceVerification,
    TailProbabilitySelectionVerification,
)
from ksdft2effmass.hamiltonian import (
    HamiltonianVerification,
    SpectralReductionVerification,
)
from ksdft2effmass.model_systems.verification import (
    BaseModelAnalysisVerification,
    QuadratureVerification,
    VisualizationProjectionVerification,
)
from ksdft2effmass.serialization import SerializableValue
from ksdft2effmass.verification import CompositeVerification


@dataclass(frozen=True, slots=True, eq=False)
class Piab1dVerification(BaseModelAnalysisVerification):
    """Compose reusable verification values for one PIAB1D analysis.

    Parameters
    ----------
    subject_sha256
        Lowercase SHA-256 digest of the exact calculation-result bytes.
    visualization_data_sha256
        Lowercase SHA-256 digest of the verifier-derived projection JSON bytes.
    components
        Exact ordered tuple of nine operation-named verification aggregates.

    Raises
    ------
    TypeError
        Digests or the component container have the wrong exact type.
    ValueError
        A digest is malformed, component order differs, or observation names collide.

    Notes
    -----
    The aggregate contains 79 comparisons. Passing establishes declared software and
    numerical checks only; it does not establish scientific validation or acceptance.
    """

    subject_sha256: str
    visualization_data_sha256: str
    components: tuple[CompositeVerification, ...]

    component_types: ClassVar[Mapping[str, type[CompositeVerification]]] = (
        MappingProxyType(
            {
                "hamiltonian": HamiltonianVerification,
                "eigensystem": EigensystemVerification,
                "spectral_reduction": SpectralReductionVerification,
                "quadrature": QuadratureVerification,
                "relative_error_convergence": RelativeErrorConvergenceVerification,
                "tail_probability_selection": TailProbabilitySelectionVerification,
                "diagnostics": DiagnosticVerification,
                "kinetic_potential_decomposition": (
                    KineticPotentialDecompositionVerification
                ),
                "visualization_projection": VisualizationProjectionVerification,
            }
        )
    )

    def __post_init__(self) -> None:
        self._validate_digest(self.subject_sha256, "subject_sha256")
        self._validate_digest(
            self.visualization_data_sha256,
            "visualization_data_sha256",
        )
        if not isinstance(self.components, tuple):
            raise TypeError("components must be a tuple")
        expected_types = tuple(self.component_types.values())
        if len(self.components) != len(expected_types) or any(
            type(component) is not expected
            for component, expected in zip(
                self.components,
                expected_types,
                strict=True,
            )
        ):
            raise ValueError(
                "components must match the declared verification inventory"
            )
        names: set[str] = set()
        for component in self.components:
            overlap = names.intersection(component.observations)
            if overlap:
                raise ValueError(
                    "verification observation names must be globally unique"
                )
            names.update(component.observations)

    @property
    def checks(self) -> Mapping[str, float]:
        """Return flattened discrepancy magnitudes for reporting.

        Returns
        -------
        Mapping[str, float]
            Read-only mapping of all 79 operation-qualified observation values.
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
        """Return flattened tolerance magnitudes for reporting.

        Returns
        -------
        Mapping[str, float]
            Read-only mapping aligned exactly with :attr:`checks`.
        """
        return MappingProxyType(
            {
                name: observation.tolerance.magnitude
                for component in self.components
                for name, observation in component.observations.items()
            }
        )

    @property
    def passed(self) -> bool:
        """Return whether every reusable verification component passes.

        Returns
        -------
        bool
            ``True`` exactly when every component satisfies every observation.
        """
        return all(component.passed for component in self.components)

    def authenticated_visualization_data_sha256(self) -> str:
        """Return the authenticated visualization-projection digest.

        Returns
        -------
        str
            Lowercase SHA-256 digest computed before component composition.
        """
        return self.visualization_data_sha256

    def _mapping(self) -> Mapping[str, SerializableValue]:
        """Return each verification component through its final mapping boundary."""
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
    def _from_mapping(
        cls,
        values: Mapping[str, SerializableValue],
    ) -> Self:
        """Reconstruct every declared component through inherited ``from_dict``."""
        if set(values) != {
            "subject_sha256",
            "visualization_data_sha256",
            "components",
        }:
            raise ValueError("verification fields do not match the contract")
        subject_sha256 = values["subject_sha256"]
        visualization_data_sha256 = values["visualization_data_sha256"]
        components_value = values["components"]
        if type(subject_sha256) is not str:
            raise TypeError("subject_sha256 must decode to a built-in string")
        if type(visualization_data_sha256) is not str:
            raise TypeError(
                "visualization_data_sha256 must decode to a built-in string"
            )
        if not isinstance(components_value, Mapping):
            raise TypeError("components must decode to a mapping")
        if set(components_value) != set(cls.component_types):
            raise ValueError("verification component fields do not match the inventory")
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

    @staticmethod
    def _validate_digest(value: str, name: str) -> None:
        if (
            type(value) is not str
            or len(value) != 64
            or any(character not in "0123456789abcdef" for character in value)
        ):
            raise ValueError(f"{name} must be a lowercase SHA-256 digest")
