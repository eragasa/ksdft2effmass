r"""Dimension-specific uniform meshes for represented reciprocal domains.

The one-dimensional mesh carries an explicit reciprocal-coordinate unit and uses an
even half-open interval. The two-dimensional mesh uses reduced coordinates in the
half-open primitive cell. Both records own only coordinates, ordering, and intrinsic
mesh invariants; weighted electronic-structure sampling, neighbor Actions, reciprocal
sewing, and represented band frames remain separate.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np

from ksdft2effmass.operators import ScalarQuantity, VectorQuantity

type _MeshIndex2D = tuple[int, int]
type _ReducedCoordinate2D = tuple[float, float]


@dataclass(frozen=True, slots=True)
class CenteredUniformReciprocalMesh1D:
    """Represent an even uniform half-open mesh on ``[-G/2, G/2)``.

    ``reciprocal_period`` carries the reciprocal-coordinate unit. Mesh points are
    ordered increasingly, matching the Appendix G transform and sewing contracts.
    """

    reciprocal_period: ScalarQuantity
    point_count: int

    def __post_init__(self) -> None:
        """Validate a positive reciprocal period and even nontrivial point count."""
        if type(self.reciprocal_period) is not ScalarQuantity:
            raise TypeError("reciprocal_period must be ScalarQuantity")
        if self.reciprocal_period.magnitude <= 0.0:
            raise ValueError("reciprocal_period must be positive")
        if type(self.point_count) is not int:
            raise TypeError("point_count must be a built-in int")
        if self.point_count < 2 or self.point_count % 2 != 0:
            raise ValueError("point_count must be positive, nontrivial, and even")

    @property
    def spacing(self) -> ScalarQuantity:
        """Return the uniform reciprocal-coordinate spacing."""
        return ScalarQuantity(
            self.reciprocal_period.magnitude / float(self.point_count),
            self.reciprocal_period.unit,
        )

    @property
    def coordinates(self) -> VectorQuantity:
        """Return ordered half-open reciprocal coordinates."""
        values = self.reciprocal_period.magnitude * (
            -0.5
            + np.arange(self.point_count, dtype=np.float64) / float(self.point_count)
        )
        return VectorQuantity(values, self.reciprocal_period.unit)

    @property
    def centered_cell_representatives(self) -> tuple[int, ...]:
        """Return centered Born--von Karman representatives in transform order."""
        half = self.point_count // 2
        return tuple(range(-half, half))


@dataclass(frozen=True, slots=True)
class CenteredUniformReciprocalMesh2D:
    r"""Represent a uniform mesh on a half-open reciprocal primitive cell.

    Parameters
    ----------
    point_counts
        Two built-in integers, each at least two. The first component indexes the
        first reciprocal primitive direction and the second indexes the second.
    mesh_identifier
        Nonempty identity for the mesh convention. Points use first-index-outer,
        second-index-inner order.
    """

    point_counts: tuple[int, int]
    mesh_identifier: str

    def __post_init__(self) -> None:
        """Validate exact point counts and the mesh identity."""
        if type(self.point_counts) is not tuple or len(self.point_counts) != 2:
            raise TypeError("point_counts must be a two-component tuple")
        if any(type(count) is not int for count in self.point_counts):
            raise TypeError("point_counts components must be built-in integers")
        if any(count < 2 for count in self.point_counts):
            raise ValueError("point_counts components must be at least two")
        if type(self.mesh_identifier) is not str:
            raise TypeError("mesh_identifier must be a string")
        if not self.mesh_identifier:
            raise ValueError("mesh_identifier must be nonempty")

    @property
    def point_count(self) -> int:
        """Return the total number of reciprocal-mesh points."""
        return self.point_counts[0] * self.point_counts[1]

    @property
    def reduced_spacings(self) -> tuple[float, float]:
        """Return uniform spacings in the two reduced reciprocal coordinates."""
        return (1.0 / self.point_counts[0], 1.0 / self.point_counts[1])

    @property
    def point_indices(self) -> tuple[_MeshIndex2D, ...]:
        """Return mesh indices in first-outer, second-inner order."""
        return tuple(
            (first, second)
            for first in range(self.point_counts[0])
            for second in range(self.point_counts[1])
        )

    @property
    def reduced_coordinates(self) -> tuple[_ReducedCoordinate2D, ...]:
        """Return centered half-open reduced coordinates in mesh order."""
        first_count, second_count = self.point_counts
        return tuple(
            (
                -0.5 + first / first_count,
                -0.5 + second / second_count,
            )
            for first, second in self.point_indices
        )

    @property
    def point_ordering(self) -> Literal["first_outer_second_inner"]:
        """Return the fixed flattened mesh ordering identifier."""
        return "first_outer_second_inner"

    def reduced_coordinate(self, point_index: _MeshIndex2D) -> _ReducedCoordinate2D:
        """Return the reduced coordinate for one exact in-range mesh index."""
        if type(point_index) is not tuple or len(point_index) != 2:
            raise TypeError("point_index must be a two-component tuple")
        if any(type(component) is not int for component in point_index):
            raise TypeError("point_index components must be built-in integers")
        if not (
            0 <= point_index[0] < self.point_counts[0]
            and 0 <= point_index[1] < self.point_counts[1]
        ):
            raise ValueError("point_index must lie inside the reciprocal mesh")
        return (
            -0.5 + point_index[0] / self.point_counts[0],
            -0.5 + point_index[1] / self.point_counts[1],
        )
