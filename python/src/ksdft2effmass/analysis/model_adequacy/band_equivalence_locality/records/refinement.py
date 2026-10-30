"""Retained wire projections for mesh-refinement assessments."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from ..definitions import BandEquivalenceLocalityFamilyEnum
from ..refinement_records import (
    BandEquivalenceLocalityRefinementAssessment,
    BandEquivalenceLocalityRefinementPair,
)

_PAIR_FIELDS = {
    "coarse_construction_size",
    "fine_construction_size",
    "maximum_parent_diagnostic_change",
    "maximum_final_parent_invariant_change",
    "maximum_correlation_change",
    "maximum_threshold_change",
    "maximum_hopping_weight_change",
    "maximum_hopping_block_power_change",
    "maximum_angle_change",
    "maximum_band_defect",
    "maximum_reconstruction_defect",
    "maximum_parseval_defect",
    "maximum_final_outcome_change",
    "first_passing_dispositions_stable",
    "transport_closure_and_plaquette_applicability_stable",
    "shared_mesh_quantities_applicable",
    "shared_mesh_inapplicable_reason",
    "maximum_shared_parent_eigenvalue_defect",
    "maximum_shared_projector_defect",
    "within_draft_tolerances",
    "tolerance_disposition_reason",
}
_ASSESSMENT_FIELDS = {
    "family",
    "refinements",
    "required_stable_refinements",
    "momentum_disposition",
    "momentum_disposition_reason",
    "passes_draft_tolerance",
    "passes_unit_scale_draft_tolerance",
    "tolerance_inapplicable_reason",
    "paper1_literal_range_endpoints_applicable",
    "paper1_literal_range_endpoints_inapplicable_reason",
}


def _integer(values: Mapping[str, SerializableValue], name: str) -> int:
    value = values[name]
    if type(value) is not int:
        raise TypeError(f"{name} must decode to a built-in integer")
    return value


def _optional_integer(values: Mapping[str, SerializableValue], name: str) -> int | None:
    value = values[name]
    if value is not None and type(value) is not int:
        raise TypeError(f"{name} must decode to a built-in integer or None")
    return value


def _floating(values: Mapping[str, SerializableValue], name: str) -> float:
    value = values[name]
    if type(value) is not float:
        raise TypeError(f"{name} must decode to a built-in float")
    return value


def _optional_floating(
    values: Mapping[str, SerializableValue], name: str
) -> float | None:
    value = values[name]
    if value is not None and type(value) is not float:
        raise TypeError(f"{name} must decode to a built-in float or None")
    return value


def _boolean(values: Mapping[str, SerializableValue], name: str) -> bool:
    value = values[name]
    if type(value) is not bool:
        raise TypeError(f"{name} must decode to a built-in bool")
    return value


def _optional_boolean(
    values: Mapping[str, SerializableValue], name: str
) -> bool | None:
    value = values[name]
    if value is not None and type(value) is not bool:
        raise TypeError(f"{name} must decode to a built-in bool or None")
    return value


def _string(values: Mapping[str, SerializableValue], name: str) -> str:
    value = values[name]
    if type(value) is not str:
        raise TypeError(f"{name} must decode to a built-in string")
    return value


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityRefinementPairRecord(BaseTypedRecord):
    """Retain one adjacent-pair refinement comparison."""

    coarse_construction_size: int
    fine_construction_size: int
    maximum_parent_diagnostic_change: float
    maximum_final_parent_invariant_change: float
    maximum_correlation_change: float
    maximum_threshold_change: float
    maximum_hopping_weight_change: float
    maximum_hopping_block_power_change: float
    maximum_angle_change: float
    maximum_band_defect: float
    maximum_reconstruction_defect: float
    maximum_parseval_defect: float
    maximum_final_outcome_change: int | None
    first_passing_dispositions_stable: bool
    transport_closure_and_plaquette_applicability_stable: bool
    shared_mesh_quantities_applicable: bool
    shared_mesh_inapplicable_reason: str
    maximum_shared_parent_eigenvalue_defect: float | None
    maximum_shared_projector_defect: float | None
    within_draft_tolerances: bool | None
    tolerance_disposition_reason: str

    def __post_init__(self) -> None:
        if type(self.coarse_construction_size) is not int:
            raise TypeError("coarse_construction_size must be a built-in integer")
        if self.coarse_construction_size < 4:
            raise ValueError("coarse_construction_size must be at least four")
        if type(self.fine_construction_size) is not int:
            raise TypeError("fine_construction_size must be a built-in integer")
        if self.fine_construction_size != 2 * self.coarse_construction_size:
            raise ValueError("fine_construction_size must double the coarse size")
        floating_values = (
            self.maximum_parent_diagnostic_change,
            self.maximum_final_parent_invariant_change,
            self.maximum_correlation_change,
            self.maximum_threshold_change,
            self.maximum_hopping_weight_change,
            self.maximum_hopping_block_power_change,
            self.maximum_angle_change,
            self.maximum_band_defect,
            self.maximum_reconstruction_defect,
            self.maximum_parseval_defect,
        )
        if any(type(value) is not float for value in floating_values):
            raise TypeError("refinement defects must be built-in floats")
        if any(not math.isfinite(value) or value < 0.0 for value in floating_values):
            raise ValueError("refinement defects must be finite and nonnegative")
        if self.maximum_final_outcome_change is not None:
            if type(self.maximum_final_outcome_change) is not int:
                raise TypeError(
                    "maximum_final_outcome_change must be a built-in integer or None"
                )
            if self.maximum_final_outcome_change < 0:
                raise ValueError(
                    "maximum_final_outcome_change must be nonnegative or None"
                )
        boolean_values = (
            self.first_passing_dispositions_stable,
            self.transport_closure_and_plaquette_applicability_stable,
            self.shared_mesh_quantities_applicable,
        )
        if any(type(value) is not bool for value in boolean_values):
            raise TypeError("refinement applicability fields must be built-in bools")
        if (
            type(self.shared_mesh_inapplicable_reason) is not str
            or type(self.tolerance_disposition_reason) is not str
        ):
            raise TypeError("refinement disposition reasons must be built-in strings")
        optional_defects = (
            self.maximum_shared_parent_eigenvalue_defect,
            self.maximum_shared_projector_defect,
        )
        if any(
            value is not None and type(value) is not float for value in optional_defects
        ):
            raise TypeError("shared-mesh defects must be built-in floats or None")
        if any(
            value is not None and (not math.isfinite(value) or value < 0.0)
            for value in optional_defects
        ):
            raise ValueError("shared-mesh defects must be finite and nonnegative")
        if (
            self.within_draft_tolerances is not None
            and type(self.within_draft_tolerances) is not bool
        ):
            raise TypeError("within_draft_tolerances must be a built-in bool or None")
        if self.shared_mesh_quantities_applicable:
            if self.shared_mesh_inapplicable_reason:
                raise ValueError(
                    "applicable shared-mesh quantities cannot have an "
                    "inapplicable reason"
                )
            if (
                self.maximum_shared_parent_eigenvalue_defect is None
                or self.maximum_shared_projector_defect is None
            ):
                raise ValueError("applicable shared-mesh defects cannot be None")
        elif (
            not self.shared_mesh_inapplicable_reason
            or self.maximum_shared_parent_eigenvalue_defect is not None
            or self.maximum_shared_projector_defect is not None
        ):
            raise ValueError(
                "inapplicable shared-mesh quantities require only a reason"
            )

    @classmethod
    def from_analysis(
        cls,
        analysis: BandEquivalenceLocalityRefinementPair,
    ) -> Self:
        """Project one plain scientific pair without recomputation."""
        if type(analysis) is not BandEquivalenceLocalityRefinementPair:
            raise TypeError("analysis must be BandEquivalenceLocalityRefinementPair")
        return cls(
            coarse_construction_size=analysis.coarse_construction_size,
            fine_construction_size=analysis.fine_construction_size,
            maximum_parent_diagnostic_change=(
                analysis.maximum_parent_diagnostic_change
            ),
            maximum_final_parent_invariant_change=(
                analysis.maximum_final_parent_invariant_change
            ),
            maximum_correlation_change=analysis.maximum_correlation_change,
            maximum_threshold_change=analysis.maximum_threshold_change,
            maximum_hopping_weight_change=analysis.maximum_hopping_weight_change,
            maximum_hopping_block_power_change=(
                analysis.maximum_hopping_block_power_change
            ),
            maximum_angle_change=analysis.maximum_angle_change,
            maximum_band_defect=analysis.maximum_band_defect,
            maximum_reconstruction_defect=analysis.maximum_reconstruction_defect,
            maximum_parseval_defect=analysis.maximum_parseval_defect,
            maximum_final_outcome_change=analysis.maximum_final_outcome_change,
            first_passing_dispositions_stable=(
                analysis.first_passing_dispositions_stable
            ),
            transport_closure_and_plaquette_applicability_stable=(
                analysis.transport_closure_and_plaquette_applicability_stable
            ),
            shared_mesh_quantities_applicable=(
                analysis.shared_mesh_quantities_applicable
            ),
            shared_mesh_inapplicable_reason=analysis.shared_mesh_inapplicable_reason,
            maximum_shared_parent_eigenvalue_defect=(
                analysis.maximum_shared_parent_eigenvalue_defect
            ),
            maximum_shared_projector_defect=(analysis.maximum_shared_projector_defect),
            within_draft_tolerances=analysis.within_draft_tolerances,
            tolerance_disposition_reason=analysis.tolerance_disposition_reason,
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "coarse_construction_size": self.coarse_construction_size,
            "fine_construction_size": self.fine_construction_size,
            "maximum_parent_diagnostic_change": (self.maximum_parent_diagnostic_change),
            "maximum_final_parent_invariant_change": (
                self.maximum_final_parent_invariant_change
            ),
            "maximum_correlation_change": self.maximum_correlation_change,
            "maximum_threshold_change": self.maximum_threshold_change,
            "maximum_hopping_weight_change": self.maximum_hopping_weight_change,
            "maximum_hopping_block_power_change": (
                self.maximum_hopping_block_power_change
            ),
            "maximum_angle_change": self.maximum_angle_change,
            "maximum_band_defect": self.maximum_band_defect,
            "maximum_reconstruction_defect": self.maximum_reconstruction_defect,
            "maximum_parseval_defect": self.maximum_parseval_defect,
            "maximum_final_outcome_change": self.maximum_final_outcome_change,
            "first_passing_dispositions_stable": (
                self.first_passing_dispositions_stable
            ),
            "transport_closure_and_plaquette_applicability_stable": (
                self.transport_closure_and_plaquette_applicability_stable
            ),
            "shared_mesh_quantities_applicable": (
                self.shared_mesh_quantities_applicable
            ),
            "shared_mesh_inapplicable_reason": self.shared_mesh_inapplicable_reason,
            "maximum_shared_parent_eigenvalue_defect": (
                self.maximum_shared_parent_eigenvalue_defect
            ),
            "maximum_shared_projector_defect": (self.maximum_shared_projector_defect),
            "within_draft_tolerances": self.within_draft_tolerances,
            "tolerance_disposition_reason": self.tolerance_disposition_reason,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != _PAIR_FIELDS:
            raise ValueError("refinement-pair fields do not match")
        return cls(
            coarse_construction_size=_integer(values, "coarse_construction_size"),
            fine_construction_size=_integer(values, "fine_construction_size"),
            maximum_parent_diagnostic_change=_floating(
                values, "maximum_parent_diagnostic_change"
            ),
            maximum_final_parent_invariant_change=_floating(
                values, "maximum_final_parent_invariant_change"
            ),
            maximum_correlation_change=_floating(values, "maximum_correlation_change"),
            maximum_threshold_change=_floating(values, "maximum_threshold_change"),
            maximum_hopping_weight_change=_floating(
                values, "maximum_hopping_weight_change"
            ),
            maximum_hopping_block_power_change=_floating(
                values, "maximum_hopping_block_power_change"
            ),
            maximum_angle_change=_floating(values, "maximum_angle_change"),
            maximum_band_defect=_floating(values, "maximum_band_defect"),
            maximum_reconstruction_defect=_floating(
                values, "maximum_reconstruction_defect"
            ),
            maximum_parseval_defect=_floating(values, "maximum_parseval_defect"),
            maximum_final_outcome_change=_optional_integer(
                values, "maximum_final_outcome_change"
            ),
            first_passing_dispositions_stable=_boolean(
                values, "first_passing_dispositions_stable"
            ),
            transport_closure_and_plaquette_applicability_stable=_boolean(
                values, "transport_closure_and_plaquette_applicability_stable"
            ),
            shared_mesh_quantities_applicable=_boolean(
                values, "shared_mesh_quantities_applicable"
            ),
            shared_mesh_inapplicable_reason=_string(
                values, "shared_mesh_inapplicable_reason"
            ),
            maximum_shared_parent_eigenvalue_defect=_optional_floating(
                values, "maximum_shared_parent_eigenvalue_defect"
            ),
            maximum_shared_projector_defect=_optional_floating(
                values, "maximum_shared_projector_defect"
            ),
            within_draft_tolerances=_optional_boolean(
                values, "within_draft_tolerances"
            ),
            tolerance_disposition_reason=_string(
                values, "tolerance_disposition_reason"
            ),
        )


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityRefinementAssessmentRecord(BaseTypedRecord):
    """Retain one complete family refinement assessment."""

    family: BandEquivalenceLocalityFamilyEnum
    refinements: tuple[BandEquivalenceLocalityRefinementPairRecord, ...]
    required_stable_refinements: int
    momentum_disposition: str
    momentum_disposition_reason: str
    passes_draft_tolerance: bool | None
    passes_unit_scale_draft_tolerance: bool | None
    tolerance_inapplicable_reason: str
    paper1_literal_range_endpoints_applicable: bool
    paper1_literal_range_endpoints_inapplicable_reason: str

    def __post_init__(self) -> None:
        if type(self.family) is not BandEquivalenceLocalityFamilyEnum:
            raise TypeError("family must be BandEquivalenceLocalityFamilyEnum")
        if type(self.refinements) is not tuple or any(
            type(item) is not BandEquivalenceLocalityRefinementPairRecord
            for item in self.refinements
        ):
            raise TypeError("refinements must be a tuple of pair records")
        if len(self.refinements) < 2:
            raise ValueError("refinements must contain at least two pair records")
        if type(self.required_stable_refinements) is not int:
            raise TypeError("required_stable_refinements must be a built-in integer")
        if not 1 <= self.required_stable_refinements <= len(self.refinements):
            raise ValueError("required_stable_refinements is outside the inventory")
        strings = (
            self.momentum_disposition,
            self.momentum_disposition_reason,
            self.tolerance_inapplicable_reason,
            self.paper1_literal_range_endpoints_inapplicable_reason,
        )
        if any(type(value) is not str for value in strings):
            raise TypeError("refinement dispositions must be built-in strings")
        optional_booleans = (
            self.passes_draft_tolerance,
            self.passes_unit_scale_draft_tolerance,
        )
        if any(
            value is not None and type(value) is not bool for value in optional_booleans
        ):
            raise TypeError("tolerance dispositions must be built-in bools or None")
        if type(self.paper1_literal_range_endpoints_applicable) is not bool:
            raise TypeError(
                "paper1_literal_range_endpoints_applicable must be a built-in bool"
            )
        if self.paper1_literal_range_endpoints_applicable:
            if self.paper1_literal_range_endpoints_inapplicable_reason:
                raise ValueError(
                    "applicable Paper 1 endpoints cannot have an inapplicable reason"
                )
        elif not self.paper1_literal_range_endpoints_inapplicable_reason:
            raise ValueError("inapplicable Paper 1 endpoints require a reason")

    @classmethod
    def from_analysis(
        cls,
        analysis: BandEquivalenceLocalityRefinementAssessment,
    ) -> Self:
        """Project one plain scientific assessment without recomputation."""
        if type(analysis) is not BandEquivalenceLocalityRefinementAssessment:
            raise TypeError(
                "analysis must be BandEquivalenceLocalityRefinementAssessment"
            )
        return cls(
            family=analysis.family,
            refinements=tuple(
                BandEquivalenceLocalityRefinementPairRecord.from_analysis(item)
                for item in analysis.refinements
            ),
            required_stable_refinements=analysis.required_stable_refinements,
            momentum_disposition=analysis.momentum_disposition,
            momentum_disposition_reason=analysis.momentum_disposition_reason,
            passes_draft_tolerance=analysis.passes_draft_tolerance,
            passes_unit_scale_draft_tolerance=(
                analysis.passes_unit_scale_draft_tolerance
            ),
            tolerance_inapplicable_reason=analysis.tolerance_inapplicable_reason,
            paper1_literal_range_endpoints_applicable=(
                analysis.paper1_literal_range_endpoints_applicable
            ),
            paper1_literal_range_endpoints_inapplicable_reason=(
                analysis.paper1_literal_range_endpoints_inapplicable_reason
            ),
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "family": self.family.to_wire(),
            "refinements": self.refinements,
            "required_stable_refinements": self.required_stable_refinements,
            "momentum_disposition": self.momentum_disposition,
            "momentum_disposition_reason": self.momentum_disposition_reason,
            "passes_draft_tolerance": self.passes_draft_tolerance,
            "passes_unit_scale_draft_tolerance": (
                self.passes_unit_scale_draft_tolerance
            ),
            "tolerance_inapplicable_reason": self.tolerance_inapplicable_reason,
            "paper1_literal_range_endpoints_applicable": (
                self.paper1_literal_range_endpoints_applicable
            ),
            "paper1_literal_range_endpoints_inapplicable_reason": (
                self.paper1_literal_range_endpoints_inapplicable_reason
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != _ASSESSMENT_FIELDS:
            raise ValueError("refinement-assessment fields do not match")
        family = _string(values, "family")
        refinements = values["refinements"]
        if not isinstance(refinements, tuple) or any(
            not isinstance(item, Mapping) for item in refinements
        ):
            raise TypeError("refinements must decode to a tuple of mappings")
        return cls(
            family=BandEquivalenceLocalityFamilyEnum.from_wire(family),
            refinements=tuple(
                BandEquivalenceLocalityRefinementPairRecord.from_dict(item)
                for item in refinements
            ),
            required_stable_refinements=_integer(values, "required_stable_refinements"),
            momentum_disposition=_string(values, "momentum_disposition"),
            momentum_disposition_reason=_string(values, "momentum_disposition_reason"),
            passes_draft_tolerance=_optional_boolean(values, "passes_draft_tolerance"),
            passes_unit_scale_draft_tolerance=_optional_boolean(
                values, "passes_unit_scale_draft_tolerance"
            ),
            tolerance_inapplicable_reason=_string(
                values, "tolerance_inapplicable_reason"
            ),
            paper1_literal_range_endpoints_applicable=_boolean(
                values, "paper1_literal_range_endpoints_applicable"
            ),
            paper1_literal_range_endpoints_inapplicable_reason=_string(
                values,
                "paper1_literal_range_endpoints_inapplicable_reason",
            ),
        )


__all__ = [
    "BandEquivalenceLocalityRefinementAssessmentRecord",
    "BandEquivalenceLocalityRefinementPairRecord",
]
