"""Immutable construction-mesh samples for rank-N band alignment."""

from __future__ import annotations

from typing import final

import numpy as np
from projectkoios.numerics.finite_periodic.meshes import CenteredUniformMesh
from projectkoios.numerics.numpy.validation import NumpyImmutableArrayConstructor
from projectkoios.physkit.numerics.typing.numpy.arrays import ComplexArray, RealArray

from ksdft2effmass.periodic.periodic1d.rankN.models import (
    Periodic1DRankNParentModel,
)
from ksdft2effmass.periodic1d.gauge_transformation import (
    Periodic1DFourierGivensGaugeTransformation,
)

from .configuration import Periodic1DRankNAlignmentConfiguration


@final
class Periodic1DRankNConstructionMeshSample:
    """Bind explicit parent and transformation fields to one construction mesh."""

    __slots__ = (
        "_parent_model",
        "_gauge_transformation",
        "_construction_mesh_size",
        "_coordinates",
        "_reference_frames",
        "_gauge_transformed_frames",
    )

    def __init__(
        self,
        parent_model: Periodic1DRankNParentModel,
        gauge_transformation: Periodic1DFourierGivensGaugeTransformation,
        configuration: Periodic1DRankNAlignmentConfiguration,
        construction_mesh_size: int,
    ) -> None:
        if not isinstance(parent_model, Periodic1DRankNParentModel):
            raise TypeError("parent_model must satisfy Periodic1DRankNParentModel")
        if type(gauge_transformation) is not Periodic1DFourierGivensGaugeTransformation:
            raise TypeError(
                "gauge_transformation must be the exact Fourier-Givens transformation"
            )
        if parent_model.band_subspace_rank != gauge_transformation.retained_rank:
            raise ValueError("parent and gauge-transformation ranks must match")
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
            parent_model.reference_frames(coordinates),
            "reference_frames",
            np.dtype(np.complex128),
        ).execute()
        gauge_transformed_frames = NumpyImmutableArrayConstructor(
            gauge_transformation.transform_frames(coordinates, reference_frames),
            "gauge_transformed_frames",
            np.dtype(np.complex128),
        ).execute()
        expected_shape = (
            construction_mesh_size,
            parent_model.ambient_dimension,
            parent_model.band_subspace_rank,
        )
        if (
            reference_frames.shape != expected_shape
            or gauge_transformed_frames.shape != expected_shape
        ):
            raise ValueError("parent frames do not match the construction mesh")
        self._parent_model = parent_model
        self._gauge_transformation = gauge_transformation
        self._construction_mesh_size = construction_mesh_size
        self._coordinates = coordinates
        self._reference_frames = reference_frames
        self._gauge_transformed_frames = gauge_transformed_frames

    @property
    def parent_model(self) -> Periodic1DRankNParentModel:
        """Return the explicit parent sampled by this value."""
        return self._parent_model

    @property
    def gauge_transformation(self) -> Periodic1DFourierGivensGaugeTransformation:
        """Return the explicit gauge transformation sampled by this value."""
        return self._gauge_transformation

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
        """Return the immutable reference frames."""
        return self._reference_frames

    @property
    def gauge_transformed_frames(self) -> ComplexArray:
        """Return the immutable gauge-transformed frames on the same mesh."""
        return self._gauge_transformed_frames


__all__ = ["Periodic1DRankNConstructionMeshSample"]
