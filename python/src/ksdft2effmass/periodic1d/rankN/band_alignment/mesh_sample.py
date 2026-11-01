"""Immutable analytic construction-mesh samples for rank-N band alignment."""

from __future__ import annotations

from typing import final

import numpy as np
from projectkoios.numerics.finite_periodic.meshes import CenteredUniformMesh
from projectkoios.numerics.numpy.validation import NumpyImmutableArrayConstructor
from projectkoios.physkit.numerics.typing.numpy.arrays import ComplexArray, RealArray

from .configuration import Periodic1DRankNAlignmentConfiguration
from .model import Periodic1DRankNAnalyticCase


@final
class Periodic1DRankNAnalyticMeshSample:
    """Bind one model to one immutable unshifted construction-mesh sample."""

    __slots__ = (
        "_model",
        "_construction_mesh_size",
        "_coordinates",
        "_reference_frames",
        "_attacked_frames",
    )

    def __init__(
        self,
        model: Periodic1DRankNAnalyticCase,
        configuration: Periodic1DRankNAlignmentConfiguration,
        construction_mesh_size: int,
    ) -> None:
        if type(model) is not Periodic1DRankNAnalyticCase:
            raise TypeError("model must be the exact analytic rank-N case")
        if type(configuration) is not Periodic1DRankNAlignmentConfiguration:
            raise TypeError("configuration must be the exact rank-N configuration")
        if type(construction_mesh_size) is not int:
            raise TypeError("construction_mesh_size must be a built-in integer")
        if construction_mesh_size not in configuration.construction_mesh_sizes:
            raise ValueError(
                "construction_mesh_size is not in the configuration inventory"
            )
        coordinates = configuration.construction_coordinates(construction_mesh_size)
        reference_frames = NumpyImmutableArrayConstructor(
            model.reference_frames(coordinates),
            "reference_frames",
            np.dtype(np.complex128),
        ).execute()
        attacked_frames = NumpyImmutableArrayConstructor(
            model.attacked_frames(coordinates),
            "attacked_frames",
            np.dtype(np.complex128),
        ).execute()
        expected_shape = (
            construction_mesh_size,
            model.ambient_dimension,
            model.retained_rank,
        )
        if (
            reference_frames.shape != expected_shape
            or attacked_frames.shape != expected_shape
        ):
            raise ValueError("analytic frames do not match the construction mesh")
        self._model = model
        self._construction_mesh_size = construction_mesh_size
        self._coordinates = coordinates
        self._reference_frames = reference_frames
        self._attacked_frames = attacked_frames

    @property
    def model(self) -> Periodic1DRankNAnalyticCase:
        """Return the exact analytic model sampled by this value."""
        return self._model

    @property
    def construction_mesh_size(self) -> int:
        """Return the number of unshifted construction-mesh points."""
        return self._construction_mesh_size

    @property
    def mesh(self) -> CenteredUniformMesh:
        """Return a fresh finite-periodic mesh descriptor for this sample."""
        return CenteredUniformMesh(
            dimension=1,
            size=self._construction_mesh_size,
            offsets=(0.0,),
        )

    @property
    def coordinates(self) -> RealArray:
        """Return the immutable centered reduced coordinates."""
        return self._coordinates

    @property
    def reference_frames(self) -> ComplexArray:
        """Return the immutable analytic reference frames."""
        return self._reference_frames

    @property
    def attacked_frames(self) -> ComplexArray:
        """Return the immutable attacked frames on the same mesh."""
        return self._attacked_frames


__all__ = ["Periodic1DRankNAnalyticMeshSample"]
