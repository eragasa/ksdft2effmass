"""Finite domains for identified operator representations.

The objects in this module identify finite numerical domains and their ordering.
They attach no physical interpretation, mathematical-property evidence, campaign
policy, or serialization contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import final

from projectkoios.numerics.finite_periodic.meshes import CenteredUniformMesh


class FiniteDomainABC(ABC):
    """Narrow interface for an identified finite ordered domain."""

    __slots__ = ()

    @property
    @abstractmethod
    def identity(self) -> str:
        """Return the stable domain identity."""

    @property
    @abstractmethod
    def cardinality(self) -> int:
        """Return the positive number of represented domain points."""


class MomentumSampleRole(Enum):
    """Enumerate declared numerical roles of a finite momentum mesh.

    Attributes
    ----------
    general
        No construction- or evaluation-specific role is declared.
    construction
        Samples are declared for representation construction.
    evaluation
        Samples are declared for evaluation.

    Notes
    -----
    The integer ``.value`` is an internal discriminant rather than a domain-facing
    string. A future serializer must map enum members to explicit, versioned wire
    tokens. Role identity alone does not establish withholding or evaluation
    non-influence.
    """

    general = 1
    construction = 2
    evaluation = 3


def _require_nonempty_exact_string(value: str, name: str, /) -> str:
    """Validate one exact nonempty built-in string without normalization."""
    if type(value) is not str:
        raise TypeError(f"{name} must be an exact built-in string")
    if value == "":
        raise ValueError(f"{name} must not be empty")
    return value


@final
@dataclass(frozen=True, slots=True)
class FiniteMomentumMeshDomain(FiniteDomainABC):
    """Identify one centered uniform finite momentum domain.

    Parameters
    ----------
    identifier
        Stable nonempty domain identity stored exactly.
    mesh
        Exact :class:`CenteredUniformMesh` owning dimension, axis size, and
        offsets. Coordinates are derived by the numerical owner rather than
        accepted as a second parallel input.
    coordinate_convention_id
        Stable nonempty identity for the reduced-coordinate convention.
    sample_role
        Semantic role of this sample domain. Construction and evaluation are
        roles, not mesh subclasses.
    """

    identifier: str
    mesh: CenteredUniformMesh
    coordinate_convention_id: str
    sample_role: MomentumSampleRole

    def __post_init__(self) -> None:
        """Validate exact identity, owner mesh, convention, and role types."""
        _require_nonempty_exact_string(self.identifier, "domain identifier")
        if type(self.mesh) is not CenteredUniformMesh:
            raise TypeError("mesh must be an exact CenteredUniformMesh")
        _require_nonempty_exact_string(
            self.coordinate_convention_id,
            "coordinate convention identity",
        )
        if type(self.sample_role) is not MomentumSampleRole:
            raise TypeError("sample_role must be a MomentumSampleRole")

    @property
    def identity(self) -> str:
        """Return the stable domain identity."""
        return self.identifier

    @property
    def cardinality(self) -> int:
        """Return the tensor-product point count owned by the mesh."""
        return self.mesh.point_count

    @property
    def dimension(self) -> int:
        """Return the reciprocal-coordinate dimension owned by the mesh."""
        return self.mesh.dimension


@final
@dataclass(frozen=True, slots=True)
class FiniteTranslationDomain(FiniteDomainABC):
    """Identify one ordered unique inventory of integer translations.

    Translation components are exact built-in integers with arbitrary Python
    magnitude. Boolean values and numeric strings are rejected. The object
    defines no metric, shell, support, unit, or physical hopping-range meaning.
    """

    identifier: str
    translations: tuple[tuple[int, ...], ...]
    coordinate_convention_id: str

    def __post_init__(self) -> None:
        """Validate exact immutable translation-domain state."""
        _require_nonempty_exact_string(self.identifier, "domain identifier")
        _require_nonempty_exact_string(
            self.coordinate_convention_id,
            "coordinate convention identity",
        )
        if type(self.translations) is not tuple:
            raise TypeError("translations must be an exact tuple")
        if not self.translations:
            raise ValueError("translations must not be empty")

        dimension: int | None = None
        for translation in self.translations:
            if type(translation) is not tuple:
                raise TypeError("each translation must be an exact tuple")
            if not translation:
                raise ValueError("translations must have positive dimension")
            if dimension is None:
                dimension = len(translation)
            elif len(translation) != dimension:
                raise ValueError("translations must have one common dimension")
            for component in translation:
                if type(component) is not int:
                    raise TypeError(
                        "translation components must be exact built-in integers"
                    )

        if len(set(self.translations)) != len(self.translations):
            raise ValueError("translations must be unique in retained order")

    @property
    def identity(self) -> str:
        """Return the stable domain identity."""
        return self.identifier

    @property
    def cardinality(self) -> int:
        """Return the number of retained translations."""
        return len(self.translations)

    @property
    def dimension(self) -> int:
        """Return the common positive translation-vector dimension."""
        return len(self.translations[0])


__all__ = [
    "FiniteDomainABC",
    "FiniteMomentumMeshDomain",
    "FiniteTranslationDomain",
    "MomentumSampleRole",
]
