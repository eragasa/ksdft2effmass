"""Test-owned analytic composition for periodic-1D finite-rank verification."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from projectkoios.physkit.numerics.typing.numpy.arrays import ComplexArray, RealArray

from ksdft2effmass.periodic.periodic1d.operators import Periodic1DBasisIdentity
from ksdft2effmass.periodic1d.gauge_transformation import (
    Periodic1DFourierGivensGaugeTransformation,
)
from periodic1d_rankn_control_basis_support import (
    SyntheticPeriodic1DRankNParentModel,
)


@dataclass(frozen=True, slots=True, eq=False)
class SyntheticPeriodic1DRankNAnalyticCase:
    """Correlate an analytic parent and transformation only for tests."""

    parent_model: SyntheticPeriodic1DRankNParentModel
    gauge_transformation: Periodic1DFourierGivensGaugeTransformation

    @property
    def retained_rank(self) -> int:
        return self.parent_model.retained_rank

    @property
    def band_subspace_rank(self) -> int:
        return self.parent_model.band_subspace_rank

    @property
    def circuit_depth(self) -> int:
        return self.gauge_transformation.circuit_depth

    @property
    def basis_identity(self) -> Periodic1DBasisIdentity:
        return self.parent_model.basis_identity

    @property
    def ambient_dimension(self) -> int:
        return self.parent_model.ambient_dimension

    @property
    def endpoint_sewing_map(self) -> ComplexArray:
        return self.parent_model.endpoint_sewing_map

    def retained_energies(self, coordinates: RealArray) -> RealArray:
        return self.parent_model.retained_energies(coordinates)

    def exterior_energies(self, coordinates: RealArray) -> RealArray:
        return self.parent_model.exterior_energies(coordinates)

    def parent_hamiltonians(self, coordinates: RealArray) -> ComplexArray:
        return self.parent_model.parent_hamiltonians(coordinates)

    def reference_frames(self, coordinates: RealArray) -> ComplexArray:
        return self.parent_model.reference_frames(coordinates)

    def exact_reduced_hamiltonians(self, coordinates: RealArray) -> ComplexArray:
        return self.parent_model.exact_reduced_hamiltonians(coordinates)

    @property
    def exact_transformation_angle_maximum(self) -> float:
        return self.gauge_transformation.exact_angle_maximum

    def sampled_transformation_angle_maximum(self, coordinates: RealArray) -> float:
        return self.gauge_transformation.sampled_angle_maximum(coordinates)

    def gauge_transformation_unitaries(self, coordinates: RealArray) -> ComplexArray:
        return self.gauge_transformation.unitaries(coordinates)

    def gauge_transformed_frames(self, coordinates: RealArray) -> ComplexArray:
        return self.gauge_transformation.transform_frames(
            coordinates,
            self.reference_frames(coordinates),
        )

    def gauge_transformed_reduced_hamiltonians(
        self,
        coordinates: RealArray,
    ) -> ComplexArray:
        return self.gauge_transformation.transform_operators(
            coordinates,
            self.exact_reduced_hamiltonians(coordinates),
        )

    def known_inverse_right_actions(self, coordinates: RealArray) -> ComplexArray:
        return self.gauge_transformation.inverse_right_actions(coordinates)


class SyntheticPeriodic1DRankNAnalyticCaseConstructor:
    """Construct a test-owned analytic parent/transformation composition."""

    def __init__(
        self,
        *,
        retained_rank: int,
        circuit_depth: int,
        basis_identity: Periodic1DBasisIdentity,
        gauge_transformation: Periodic1DFourierGivensGaugeTransformation,
    ) -> None:
        self._retained_rank = retained_rank
        self._circuit_depth = circuit_depth
        self._basis_identity = basis_identity
        self._gauge_transformation = gauge_transformation

    def execute(self) -> SyntheticPeriodic1DRankNAnalyticCase:
        rank = self._retained_rank
        if self._basis_identity.dimension != rank:
            raise ValueError("basis_identity dimension must equal retained_rank")
        transformation = self._gauge_transformation
        if transformation.retained_rank != rank:
            raise ValueError("gauge_transformation rank must equal retained_rank")
        if transformation.circuit_depth != self._circuit_depth:
            raise ValueError("gauge_transformation depth must equal circuit_depth")
        ambient = 2 * rank
        frame = np.zeros((ambient, rank), dtype=np.complex128)
        frame[:rank] = np.eye(rank, dtype=np.complex128)
        parent = SyntheticPeriodic1DRankNParentModel(
            retained_rank=rank,
            basis=self._basis_identity,
            reference_frame=frame,
            sewing_map=np.eye(ambient, dtype=np.complex128),
        )
        return SyntheticPeriodic1DRankNAnalyticCase(parent, transformation)


__all__ = [
    "SyntheticPeriodic1DRankNAnalyticCase",
    "SyntheticPeriodic1DRankNAnalyticCaseConstructor",
]
