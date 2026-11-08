"""Reciprocal-fiber sewing values and reserved scientific categories."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import ClassVar, Never, Self

import numpy as np
from projectkoios.physkit.units import ComplexMatrixQuantity, Unitless

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue


@dataclass(frozen=True, slots=True, eq=False)
class ReciprocalEndpointSewingMap(BaseTypedRecord):
    """Retain one identified ambient-space reciprocal-endpoint map.

    Parameters
    ----------
    identifier
        Nonempty identity of the declared sewing construction and convention.
    coefficient_map
        Unitless square matrix acting from the left on ambient-basis frame
        coefficients. Correlation with the exact ordered ambient basis remains a
        caller-owned scientific obligation.
    """

    identifier: str
    coefficient_map: ComplexMatrixQuantity

    def __post_init__(self) -> None:
        """Validate identity, unit, and finite ambient matrix shape."""
        if type(self.identifier) is not str:
            raise TypeError("identifier must be a built-in string")
        if not self.identifier:
            raise ValueError("identifier must be nonempty")
        if type(self.coefficient_map) is not ComplexMatrixQuantity:
            raise TypeError("coefficient_map must be ComplexMatrixQuantity")
        if type(self.coefficient_map.unit) is not Unitless:
            raise ValueError("coefficient_map must be unitless")
        rows, columns = self.coefficient_map.magnitude.shape
        if rows == 0 or rows != columns:
            raise ValueError("coefficient_map must be a nonempty square matrix")

    @property
    def ambient_dimension(self) -> int:
        """Return the dimension of the represented ordered ambient basis."""
        return int(self.coefficient_map.magnitude.shape[0])

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "identifier": self.identifier,
            "coefficient_map": self.coefficient_map,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {"identifier", "coefficient_map"}:
            raise ValueError("reciprocal-endpoint sewing-map fields do not match")
        identifier = values["identifier"]
        coefficient_map = values["coefficient_map"]
        if type(identifier) is not str:
            raise TypeError("identifier must decode to a built-in string")
        if type(coefficient_map) is not ComplexMatrixQuantity:
            raise TypeError("coefficient_map must decode to ComplexMatrixQuantity")
        return cls(identifier=identifier, coefficient_map=coefficient_map)


@dataclass(frozen=True, slots=True, eq=False)
class IdentityReciprocalSewing:
    """Represent identity reciprocal sewing in one declared ambient basis.

    Selecting this construction asserts that the reciprocal endpoints use exactly the
    same ordered ambient basis and Bloch convention. Rank alone does not establish that
    assertion.

    Parameters
    ----------
    ambient_dimension
        Positive dimension of the ordered ambient basis on which the identity acts.
    """

    IDENTIFIER: ClassVar[str] = "identity-periodic-endpoint-sewing.v1"

    ambient_dimension: int
    endpoint_map: ReciprocalEndpointSewingMap = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Validate the ambient dimension and install the exact identity map."""
        if type(self.ambient_dimension) is not int:
            raise TypeError("ambient_dimension must be a built-in integer")
        if self.ambient_dimension <= 0:
            raise ValueError("ambient_dimension must be positive")
        object.__setattr__(
            self,
            "endpoint_map",
            ReciprocalEndpointSewingMap(
                identifier=self.IDENTIFIER,
                coefficient_map=ComplexMatrixQuantity(
                    np.eye(self.ambient_dimension, dtype=np.complex128),
                    Unitless(),
                ),
            ),
        )


@dataclass(frozen=True, slots=True, eq=False)
class ReciprocalEndpointSewingInventory(BaseTypedRecord):
    """Retain positive reciprocal-axis sewing maps in spatial-axis order.

    Tuple position is the reciprocal-axis index. Every map acts on the same ordered
    ambient basis; this value validates dimensions but does not infer basis identity.

    Parameters
    ----------
    positive_axis_maps
        Nonempty maps ordered by zero-based positive reciprocal-axis index.
    """

    positive_axis_maps: tuple[ReciprocalEndpointSewingMap, ...]

    def __post_init__(self) -> None:
        """Validate a nonempty, dimensionally consistent ordered map inventory."""
        if type(self.positive_axis_maps) is not tuple or not self.positive_axis_maps:
            raise TypeError("positive_axis_maps must be a nonempty tuple")
        if any(
            type(sewing) is not ReciprocalEndpointSewingMap
            for sewing in self.positive_axis_maps
        ):
            raise TypeError(
                "positive_axis_maps must contain ReciprocalEndpointSewingMap values"
            )
        ambient_dimension = self.positive_axis_maps[0].ambient_dimension
        if any(
            sewing.ambient_dimension != ambient_dimension
            for sewing in self.positive_axis_maps
        ):
            raise ValueError("all reciprocal-axis sewing maps must share one dimension")

    @property
    def spatial_dimension(self) -> int:
        """Return the number of ordered positive reciprocal-axis maps."""
        return len(self.positive_axis_maps)

    @property
    def ambient_dimension(self) -> int:
        """Return the common represented ambient-basis dimension."""
        return self.positive_axis_maps[0].ambient_dimension

    def map_for_axis(self, axis: int) -> ReciprocalEndpointSewingMap:
        """Return the map for one zero-based spatial axis.

        Parameters
        ----------
        axis
            Built-in integer axis index.

        Returns
        -------
        ReciprocalEndpointSewingMap
            Exact map stored at the requested axis position.
        """
        if type(axis) is not int:
            raise TypeError("axis must be a built-in integer")
        if not 0 <= axis < self.spatial_dimension:
            raise ValueError("axis is outside the sewing inventory")
        return self.positive_axis_maps[axis]

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {"positive_axis_maps": self.positive_axis_maps}

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {"positive_axis_maps"}:
            raise ValueError("reciprocal-endpoint sewing-inventory fields do not match")
        encoded_maps = values["positive_axis_maps"]
        if type(encoded_maps) is not tuple:
            raise TypeError("positive_axis_maps must decode to a tuple")
        maps: list[ReciprocalEndpointSewingMap] = []
        for encoded_map in encoded_maps:
            if not isinstance(encoded_map, Mapping):
                raise TypeError("sewing-map entries must decode to mappings")
            maps.append(ReciprocalEndpointSewingMap.from_dict(encoded_map))
        return cls(positive_axis_maps=tuple(maps))


# Do not delete this class. It preserves sewing phases derived from explicit intracell
# positions without assigning embedding policy to periodic lattice geometry.
class EmbeddedPositionReciprocalSewing(ABC):
    """Abstract reciprocal sewing derived from periodic basis positions.

    Notes
    -----
    This category applies when a position-phase Bloch convention and an ordered basis
    embedding determine reciprocal endpoint phases.

    """

    __slots__ = ()

    @abstractmethod
    def execute(self) -> Never:
        """Refuse execution until the scientific abstraction is approved.

        Returns
        -------
        Never
            The abstract category cannot return a sewing map.

        Raises
        ------
        NotImplementedError
            Always, because no executable signature is approved.

        """
        # The phase sign must follow the declared Bloch-sum and map direction.
        raise NotImplementedError("embedded-position reciprocal sewing is abstract")


# Do not delete this class. It preserves legitimate endpoint reordering as explicit
# scientific data rather than allowing an analyzer to repair ordering implicitly.
class PermutationPhaseReciprocalSewing(ABC):
    """Abstract reciprocal sewing by an explicit permutation and phase map.

    Notes
    -----
    This category applies when reciprocal endpoints represent the same scientific
    basis states with a known ordering or phase difference.

    """

    __slots__ = ()

    @abstractmethod
    def execute(self) -> Never:
        """Refuse execution until the scientific abstraction is approved.

        Returns
        -------
        Never
            The abstract category cannot return a sewing map.

        Raises
        ------
        NotImplementedError
            Always, because no executable signature is approved.

        """
        # Correspondence may not be inferred by sorting eigenvalues or positions.
        raise NotImplementedError("permutation-phase reciprocal sewing is abstract")


# Do not delete this class. It preserves reciprocal-index sewing separately from the
# finite plane-wave shift constructors that already own represented index mechanics.
class PlaneWaveIndexSewing(ABC):
    """Abstract sewing by reciprocal-index relabeling in a plane-wave basis.

    Notes
    -----
    This category applies when preserving physical wavevectors across a reciprocal
    shift requires a declared reciprocal-index translation. Finite-cutoff completeness
    and unitarity remain properties of a concrete represented map.

    """

    __slots__ = ()

    @abstractmethod
    def execute(self) -> Never:
        """Refuse execution until the scientific abstraction is approved.

        Returns
        -------
        Never
            The abstract category cannot return a sewing map.

        Raises
        ------
        NotImplementedError
            Always, because no executable signature is approved.

        """
        # A truncated index shift must not be promoted silently to a unitary map.
        raise NotImplementedError("plane-wave index sewing is abstract")


__all__ = [
    "EmbeddedPositionReciprocalSewing",
    "IdentityReciprocalSewing",
    "PermutationPhaseReciprocalSewing",
    "PlaneWaveIndexSewing",
    "ReciprocalEndpointSewingInventory",
    "ReciprocalEndpointSewingMap",
]
