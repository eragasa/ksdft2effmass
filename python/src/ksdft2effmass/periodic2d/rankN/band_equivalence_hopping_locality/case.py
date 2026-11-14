"""Periodic-2D finite-rank parent/transformation case composition."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array

from ksdft2effmass.periodic.periodic2d.operators import Periodic2DBasisIdentity
from ksdft2effmass.periodic.periodic2d.rankN.models import (
    Periodic2DRankNParentModel,
)
from ksdft2effmass.periodic2d.rankN.gauge_alignment.transformation import (
    Periodic2DRankNGaugeNormalizationEnum,
    Periodic2DRankNGivensGaugeTransformation,
)

from .base import Periodic2DRankNBandEquivalenceHoppingLocalityCaseValue


@dataclass(frozen=True, slots=True, eq=False)
class Periodic2DRankNParentGaugeCase(
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseValue,
):
    """Correlate one explicit parent and one right gauge transformation.

    Parameters
    ----------
    case_identifier
        Nonempty study-case identity owned by the calculation composition.
    parent_model
        Reusable periodic-2D finite-rank parent scientific model.
    gauge_transformation
        Independent retained-coordinate gauge transformation of matching rank and bonds.
    """

    CASE_FAMILY_IDENTITY: ClassVar[str] = (
        "ksdft2effmass.periodic2d-rankN-parent-gauge-case.v1"
    )

    case_identifier: str
    parent_model: Periodic2DRankNParentModel
    gauge_transformation: Periodic2DRankNGivensGaugeTransformation

    def __post_init__(self) -> None:
        """Validate exact parent/transformation correlation without inference."""
        if type(self.case_identifier) is not str or not self.case_identifier:
            raise TypeError("case_identifier must be a nonempty built-in string")
        if not isinstance(self.parent_model, Periodic2DRankNParentModel):
            raise TypeError("parent_model must be Periodic2DRankNParentModel")
        if (
            type(self.gauge_transformation)
            is not Periodic2DRankNGivensGaugeTransformation
        ):
            raise TypeError(
                "gauge_transformation must be the exact periodic-2D "
                "Givens gauge transformation"
            )
        if (
            self.parent_model.band_subspace_rank
            != self.gauge_transformation.retained_rank
        ):
            raise ValueError(
                "parent and gauge-transformation retained ranks must match"
            )
        if self.parent_model.positive_bonds != self.gauge_transformation.harmonic_bonds:
            raise ValueError(
                "parent and gauge-transformation harmonic bonds must match"
            )

    @property
    def retained_rank(self) -> int:
        """Return the correlated retained rank."""
        return self.parent_model.band_subspace_rank

    @property
    def band_subspace_rank(self) -> int:
        """Return the represented finite-rank case size."""
        return self.parent_model.band_subspace_rank

    @property
    def basis_identity(self) -> Periodic2DBasisIdentity:
        """Return the parent-owned structured retained basis identity."""
        return self.parent_model.basis_identity

    @property
    def circuit_depth(self) -> int:
        """Return the independent gauge-circuit depth."""
        return self.gauge_transformation.circuit_depth

    @property
    def positive_bonds(self) -> tuple[tuple[int, int], ...]:
        """Return the exactly correlated parent and transformation harmonic bonds."""
        return self.parent_model.positive_bonds

    @property
    def gauge_normalization(self) -> Periodic2DRankNGaugeNormalizationEnum:
        """Return the gauge-transformation normalization convention."""
        return self.gauge_transformation.normalization

    @property
    def parent_scale(self) -> float:
        """Return the parent coupling scale."""
        return self.parent_model.parent_scale

    @property
    def transformation_coefficient(self) -> float:
        """Return the gauge-transformation coefficient."""
        return self.gauge_transformation.coefficient

    @property
    def ambient_dimension(self) -> int:
        """Return the ordered retained-plus-exterior parent dimension."""
        return self.parent_model.ambient_dimension

    @property
    def isolation_gap_lower_bound(self) -> float:
        """Return the parent family's declared isolation-gap lower bound."""
        return self.parent_model.isolation_gap_lower_bound

    @property
    def model_identity(self) -> str:
        """Return the case correlation identity used by existing analysis records."""
        return (
            f"{self.CASE_FAMILY_IDENTITY}:{self.case_identifier}:"
            f"parent-{self.parent_model.model_id}:"
            f"transformation-{self.gauge_transformation.transformation_identity}"
        )

    @property
    def transformation_angle_upper_bound(self) -> float:
        """Return the gauge transformation's conservative angle bound."""
        return self.gauge_transformation.angle_upper_bound

    def structure_factor(self, reduced_coordinates: Float64Array) -> Float64Array:
        """Return the parent structure factor."""
        return self.parent_model.structure_factor(reduced_coordinates)

    def retained_energies(self, reduced_coordinates: Float64Array) -> Float64Array:
        """Return the parent retained-sector energies."""
        return self.parent_model.retained_energies(reduced_coordinates)

    def exterior_energies(self, reduced_coordinates: Float64Array) -> Float64Array:
        """Return the parent exterior-sector energies."""
        return self.parent_model.exterior_energies(reduced_coordinates)

    def parent_hamiltonians(self, reduced_coordinates: Float64Array) -> Complex128Array:
        """Return the parent ambient operators."""
        return self.parent_model.parent_hamiltonians(reduced_coordinates)

    def reference_frames(self, reduced_coordinates: Float64Array) -> Complex128Array:
        """Return the parent retained embedding."""
        return self.parent_model.reference_frames(reduced_coordinates)

    def exact_reduced_hamiltonians(
        self,
        reduced_coordinates: Float64Array,
    ) -> Complex128Array:
        """Return exact retained operators in the parent reference frame."""
        return self.parent_model.exact_reduced_hamiltonians(reduced_coordinates)

    def gauge_unitaries(self, reduced_coordinates: Float64Array) -> Complex128Array:
        """Return the independently owned gauge-transformation unitaries."""
        return self.gauge_transformation.unitaries(reduced_coordinates)

    def gauge_transformed_frames(
        self, reduced_coordinates: Float64Array
    ) -> Complex128Array:
        """Return parent frames after the right-acting gauge transformation."""
        return self.gauge_transformation.transform_frames(
            reduced_coordinates,
            self.reference_frames(reduced_coordinates),
        )

    def gauge_transformed_reduced_hamiltonians(
        self,
        reduced_coordinates: Float64Array,
    ) -> Complex128Array:
        """Return retained operators represented in the gauge-transformed frame."""
        return self.gauge_transformation.transform_operators(
            reduced_coordinates,
            self.exact_reduced_hamiltonians(reduced_coordinates),
        )

    def known_inverse_right_actions(
        self,
        reduced_coordinates: Float64Array,
    ) -> Complex128Array:
        """Return the exact construction-oracle inverse right actions."""
        return self.gauge_transformation.inverse_right_actions(reduced_coordinates)


__all__ = ["Periodic2DRankNParentGaugeCase"]
