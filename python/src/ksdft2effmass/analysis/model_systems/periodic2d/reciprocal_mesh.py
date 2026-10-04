r"""Two-dimensional reciprocal-mesh neighbors and plane-wave sewing maps.

The lower-level centered uniform mesh uses the half-open primitive reciprocal cell
``[-1/2, 1/2) x [-1/2, 1/2)``. Positive neighbors wrap independently in the two
primitive directions. A wrapped neighbor retains the integer reciprocal translation
needed to recover its unwrapped reduced coordinate.

For a finite plane-wave basis, sewing from ``kappa`` to ``kappa + e_alpha`` shifts
coefficient indices by one in direction ``alpha``. The finite-cutoff map is explicitly
nonunitary because coefficients shifted beyond the retained square basis are discarded.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

import numpy as np

from ksdft2effmass.operators import ComplexMatrixQuantity, Unitless
from ksdft2effmass.solid_state import reciprocal_meshes as _reciprocal_meshes

from .plane_waves import PlaneWaveBlochHamiltonian2DModel

type MeshIndex2D = tuple[int, int]
type ReciprocalTranslation2D = tuple[int, int]


class PositiveReciprocalDirection2D(StrEnum):
    """Identify one positive primitive reciprocal direction."""

    FIRST = "plus_first_reciprocal_vector"
    SECOND = "plus_second_reciprocal_vector"


@dataclass(frozen=True, slots=True)
class ReciprocalMeshNeighbor2DRequest:
    """Request the positive neighbor of one reciprocal-mesh point.

    Parameters
    ----------
    mesh
        Centered uniform reciprocal mesh.
    point_index
        Exact in-range source index.
    direction
        Positive primitive reciprocal direction in which to advance one mesh step.
    """

    mesh: _reciprocal_meshes.CenteredUniformReciprocalMesh2D
    point_index: MeshIndex2D
    direction: PositiveReciprocalDirection2D

    def __post_init__(self) -> None:
        """Validate exact mesh, source index, and direction fields."""
        if type(self.mesh) is not _reciprocal_meshes.CenteredUniformReciprocalMesh2D:
            raise TypeError("mesh must be CenteredUniformReciprocalMesh2D")
        self.mesh.reduced_coordinate(self.point_index)
        if type(self.direction) is not PositiveReciprocalDirection2D:
            raise TypeError("direction must be PositiveReciprocalDirection2D")


@dataclass(frozen=True, slots=True)
class ReciprocalMeshNeighbor2DResult:
    r"""Retain one wrapped neighbor and its reciprocal sewing translation.

    ``reciprocal_translation`` satisfies

    ``unwrapped_neighbor = wrapped_neighbor + reciprocal_translation``

    in reduced reciprocal coordinates.
    """

    request: ReciprocalMeshNeighbor2DRequest
    neighbor_index: MeshIndex2D
    reciprocal_translation: ReciprocalTranslation2D

    def __post_init__(self) -> None:
        """Validate that the result exactly implements the requested mesh step."""
        if type(self.request) is not ReciprocalMeshNeighbor2DRequest:
            raise TypeError("request must be ReciprocalMeshNeighbor2DRequest")
        self.request.mesh.reduced_coordinate(self.neighbor_index)
        if (
            type(self.reciprocal_translation) is not tuple
            or len(self.reciprocal_translation) != 2
        ):
            raise TypeError("reciprocal_translation must be a two-component tuple")
        if any(type(component) is not int for component in self.reciprocal_translation):
            raise TypeError(
                "reciprocal_translation components must be built-in integers"
            )
        first, second = self.request.point_index
        first_count, second_count = self.request.mesh.point_counts
        if self.request.direction is PositiveReciprocalDirection2D.FIRST:
            expected_neighbor = ((first + 1) % first_count, second)
            expected_translation = (1, 0) if first + 1 == first_count else (0, 0)
        else:
            expected_neighbor = (first, (second + 1) % second_count)
            expected_translation = (0, 1) if second + 1 == second_count else (0, 0)
        if self.neighbor_index != expected_neighbor:
            raise ValueError("neighbor_index does not implement the requested step")
        if self.reciprocal_translation != expected_translation:
            raise ValueError(
                "reciprocal_translation does not implement the requested wrap"
            )

    @property
    def sewing_required(self) -> bool:
        """Return whether the positive step crosses the primitive-cell boundary."""
        return self.reciprocal_translation != (0, 0)


class ReciprocalMeshNeighbor2DConstructor:
    """Construct positive reciprocal-mesh neighbors with explicit boundary wraps."""

    __slots__ = ()

    def execute(
        self, request: ReciprocalMeshNeighbor2DRequest
    ) -> ReciprocalMeshNeighbor2DResult:
        """Return the wrapped neighbor and its integer reciprocal translation."""
        if type(request) is not ReciprocalMeshNeighbor2DRequest:
            raise TypeError("request must be ReciprocalMeshNeighbor2DRequest")
        first, second = request.point_index
        first_count, second_count = request.mesh.point_counts
        if request.direction is PositiveReciprocalDirection2D.FIRST:
            wraps = first + 1 == first_count
            neighbor_index = ((first + 1) % first_count, second)
            translation = (1, 0) if wraps else (0, 0)
        else:
            wraps = second + 1 == second_count
            neighbor_index = (first, (second + 1) % second_count)
            translation = (0, 1) if wraps else (0, 0)
        return ReciprocalMeshNeighbor2DResult(
            request=request,
            neighbor_index=neighbor_index,
            reciprocal_translation=translation,
        )


@dataclass(frozen=True, slots=True)
class PlaneWaveReciprocalSewing2DRequest:
    r"""Request a finite plane-wave coefficient map for ``kappa -> kappa + e``.

    Parameters
    ----------
    model
        Plane-wave model whose square reciprocal-index basis is sewn.
    direction
        Positive primitive reciprocal direction defining the unit reduced shift.
    """

    model: PlaneWaveBlochHamiltonian2DModel
    direction: PositiveReciprocalDirection2D

    def __post_init__(self) -> None:
        """Validate exact model and sewing direction fields."""
        if type(self.model) is not PlaneWaveBlochHamiltonian2DModel:
            raise TypeError("model must be PlaneWaveBlochHamiltonian2DModel")
        if type(self.direction) is not PositiveReciprocalDirection2D:
            raise TypeError("direction must be PositiveReciprocalDirection2D")


@dataclass(frozen=True, slots=True, eq=False)
class PlaneWaveReciprocalSewing2DResult:
    """Retain an explicit nonunitary finite-cutoff plane-wave sewing map.

    Parameters
    ----------
    request
        Exact model and positive reciprocal direction.
    coefficient_map
        Unitless immutable map in the model's declared plane-wave basis ordering.
    """

    request: PlaneWaveReciprocalSewing2DRequest
    coefficient_map: ComplexMatrixQuantity

    def __post_init__(self) -> None:
        """Validate exact request, unit, shape, and coefficient shift entries."""
        if type(self.request) is not PlaneWaveReciprocalSewing2DRequest:
            raise TypeError("request must be PlaneWaveReciprocalSewing2DRequest")
        if type(self.coefficient_map) is not ComplexMatrixQuantity:
            raise TypeError("coefficient_map must be ComplexMatrixQuantity")
        if type(self.coefficient_map.unit) is not Unitless:
            raise ValueError("coefficient_map must be unitless")
        dimension = self.request.model.represented_dimension
        if self.coefficient_map.magnitude.shape != (dimension, dimension):
            raise ValueError("coefficient_map shape must match the plane-wave basis")
        expected = np.zeros((dimension, dimension), dtype=np.complex128)
        lookup = {
            reciprocal_index: position
            for position, reciprocal_index in enumerate(
                self.request.model.reciprocal_indices
            )
        }
        first_shift = (
            1 if self.request.direction is PositiveReciprocalDirection2D.FIRST else 0
        )
        second_shift = (
            1 if self.request.direction is PositiveReciprocalDirection2D.SECOND else 0
        )
        for row, reciprocal_index in enumerate(self.request.model.reciprocal_indices):
            source_index = (
                reciprocal_index[0] + first_shift,
                reciprocal_index[1] + second_shift,
            )
            column = lookup.get(source_index)
            if column is not None:
                expected[row, column] = 1.0 + 0.0j
        if not np.array_equal(self.coefficient_map.magnitude, expected):
            raise ValueError(
                "coefficient_map must implement the declared reciprocal shift"
            )


class PlaneWaveReciprocalSewing2DConstructor:
    r"""Construct the finite coefficient map for ``kappa -> kappa + e_alpha``.

    The returned map has no periodic wrap inside the truncated coefficient basis.
    Rows whose source coefficient lies outside the retained cutoff remain zero, so the
    finite map is a partial shift rather than a unitary permutation.
    """

    __slots__ = ()

    def execute(
        self, request: PlaneWaveReciprocalSewing2DRequest
    ) -> PlaneWaveReciprocalSewing2DResult:
        """Return the explicit finite-cutoff shift in declared basis order."""
        if type(request) is not PlaneWaveReciprocalSewing2DRequest:
            raise TypeError("request must be PlaneWaveReciprocalSewing2DRequest")
        model = request.model
        coefficient_map = np.zeros(
            (model.represented_dimension, model.represented_dimension),
            dtype=np.complex128,
        )
        lookup = {
            reciprocal_index: position
            for position, reciprocal_index in enumerate(model.reciprocal_indices)
        }
        first_shift = (
            1 if request.direction is PositiveReciprocalDirection2D.FIRST else 0
        )
        second_shift = (
            1 if request.direction is PositiveReciprocalDirection2D.SECOND else 0
        )
        for row, reciprocal_index in enumerate(model.reciprocal_indices):
            source_index = (
                reciprocal_index[0] + first_shift,
                reciprocal_index[1] + second_shift,
            )
            column = lookup.get(source_index)
            if column is not None:
                coefficient_map[row, column] = 1.0 + 0.0j
        return PlaneWaveReciprocalSewing2DResult(
            request=request,
            coefficient_map=ComplexMatrixQuantity(coefficient_map, Unitless()),
        )
