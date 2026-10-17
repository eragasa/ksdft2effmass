"""Bounded refinement of sampled synthetic-strain transition brackets."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .strain import (
    StrainPointDiagnostic,
    SyntheticStrainCalculator,
    SyntheticStrainResult,
)
from .strain_response import (
    StrainResponseModel,
    StrainWitnessControl,
    SyntheticStrainResponseResult,
    SyntheticStrainWitnessScanResult,
)


@dataclass(frozen=True, slots=True)
class StrainWitnessRequirementEnvelope:
    """Retain sampled maxima for one representation-witness control."""

    control: StrainWitnessControl
    optimized_maximum: float
    optimized_maximum_strain_fraction: float
    fixed_candidate_maximum: float
    fixed_candidate_maximum_strain_fraction: float


@dataclass(frozen=True, slots=True)
class StrainLocalityEnvelope:
    """Retain sampled physical-range and block-count maxima at one tolerance."""

    tail_tolerance: float
    maximum_physical_radius: float | None
    maximum_physical_radius_strain_fraction: float | None
    maximum_retained_blocks: int | None
    maximum_retained_blocks_strain_fraction: float | None


@dataclass(frozen=True, slots=True)
class StrainResponseEnvelope:
    """Retain one sampled aligned strain-response maximum."""

    control: StrainWitnessControl
    maximum_aligned_hamiltonian_defect: float
    maximum_strain_fraction: float


@dataclass(frozen=True, slots=True)
class SyntheticStrainScanSummary:
    """Combine independently interpreted sampled scan envelopes."""

    base_sample_count: int
    maximum_volume_defect: float
    maximum_direct_band_defect: float
    witness_requirements: tuple[StrainWitnessRequirementEnvelope, ...]
    locality: tuple[StrainLocalityEnvelope, ...]
    responses: tuple[StrainResponseEnvelope, ...]
    status: str = "sampled-development-summary-not-continuum-certificate"


class SyntheticStrainScanAssessor:
    """Summarize typed scan results without applying acceptance limits."""

    __slots__ = ()

    def execute(
        self,
        geometry_result: SyntheticStrainResult,
        witness_results: tuple[SyntheticStrainWitnessScanResult, ...],
        frozen_response: SyntheticStrainResponseResult,
        radial_response: SyntheticStrainResponseResult,
    ) -> SyntheticStrainScanSummary:
        """Calculate sampled envelopes for one common strain grid."""
        if type(geometry_result) is not SyntheticStrainResult:
            raise TypeError("geometry_result must be SyntheticStrainResult")
        if type(witness_results) is not tuple or any(
            type(result) is not SyntheticStrainWitnessScanResult
            for result in witness_results
        ):
            raise TypeError(
                "witness_results must be a tuple of SyntheticStrainWitnessScanResult"
            )
        if len(witness_results) != len(StrainWitnessControl) or {
            result.control for result in witness_results
        } != set(StrainWitnessControl):
            raise ValueError("witness_results must contain each control exactly once")
        if type(frozen_response) is not SyntheticStrainResponseResult:
            raise TypeError("frozen_response must be SyntheticStrainResponseResult")
        if type(radial_response) is not SyntheticStrainResponseResult:
            raise TypeError("radial_response must be SyntheticStrainResponseResult")
        if frozen_response.model is not StrainResponseModel.M1_FROZEN:
            raise ValueError("frozen_response must use the frozen-parent model")
        if radial_response.model is not StrainResponseModel.M2_RADIAL:
            raise ValueError("radial_response must use the radial-response model")

        path = geometry_result.path
        fractions = tuple(point.strain_fraction for point in geometry_result.points)
        if not fractions:
            raise ValueError("geometry_result must contain at least one strain point")
        if any(
            result.path is not path
            or tuple(point.strain_fraction for point in result.points) != fractions
            for result in witness_results
        ) or any(
            result.path is not path
            or tuple(point.strain_fraction for point in result.points) != fractions
            for result in (frozen_response, radial_response)
        ):
            raise ValueError("all scan results must use one path and strain grid")

        witness_envelopes: list[StrainWitnessRequirementEnvelope] = []
        for result in sorted(witness_results, key=lambda item: item.control.value):
            optimized = max(
                result.points,
                key=lambda point: point.pointwise_optimized_operator_threshold,
            )
            fixed = max(
                result.points,
                key=lambda point: point.fixed_candidate_operator_threshold,
            )
            witness_envelopes.append(
                StrainWitnessRequirementEnvelope(
                    control=result.control,
                    optimized_maximum=optimized.pointwise_optimized_operator_threshold,
                    optimized_maximum_strain_fraction=optimized.strain_fraction,
                    fixed_candidate_maximum=fixed.fixed_candidate_operator_threshold,
                    fixed_candidate_maximum_strain_fraction=fixed.strain_fraction,
                )
            )

        locality: list[StrainLocalityEnvelope] = []
        for tolerance_index, tolerance in enumerate(geometry_result.tail_tolerances):
            radius_points = tuple(
                point
                for point in geometry_result.points
                if point.first_passing_radius[tolerance_index] is not None
            )
            block_points = tuple(
                point
                for point in geometry_result.points
                if point.first_passing_blocks[tolerance_index] is not None
            )
            radius_point = (
                None
                if not radius_points
                else max(
                    radius_points,
                    key=lambda point: (
                        point.first_passing_radius[tolerance_index] or 0.0
                    ),
                )
            )
            block_point = (
                None
                if not block_points
                else max(
                    block_points,
                    key=lambda point: point.first_passing_blocks[tolerance_index] or 0,
                )
            )
            locality.append(
                StrainLocalityEnvelope(
                    tail_tolerance=tolerance,
                    maximum_physical_radius=(
                        None
                        if radius_point is None
                        else radius_point.first_passing_radius[tolerance_index]
                    ),
                    maximum_physical_radius_strain_fraction=(
                        None if radius_point is None else radius_point.strain_fraction
                    ),
                    maximum_retained_blocks=(
                        None
                        if block_point is None
                        else block_point.first_passing_blocks[tolerance_index]
                    ),
                    maximum_retained_blocks_strain_fraction=(
                        None if block_point is None else block_point.strain_fraction
                    ),
                )
            )

        responses: list[StrainResponseEnvelope] = []
        for control, response_result in (
            (StrainWitnessControl.FROZEN_PARENT, frozen_response),
            (StrainWitnessControl.RADIAL_RESPONSE, radial_response),
        ):
            maximum = max(
                response_result.points,
                key=lambda point: point.aligned_strain_perturbation.maximum_hamiltonian,
            )
            responses.append(
                StrainResponseEnvelope(
                    control=control,
                    maximum_aligned_hamiltonian_defect=(
                        maximum.aligned_strain_perturbation.maximum_hamiltonian
                    ),
                    maximum_strain_fraction=maximum.strain_fraction,
                )
            )

        return SyntheticStrainScanSummary(
            base_sample_count=len(fractions),
            maximum_volume_defect=max(
                abs(float(np.linalg.det(np.asarray(point.metric))) - 1.0)
                for point in geometry_result.points
            ),
            maximum_direct_band_defect=max(
                point.maximum_direct_band_defect
                for result in witness_results
                for point in result.points
            ),
            witness_requirements=tuple(witness_envelopes),
            locality=tuple(locality),
            responses=tuple(responses),
        )


@dataclass(frozen=True, slots=True)
class StrainShellTransitionBracket:
    """Bracket one detected change in a first-passing block count."""

    tail_tolerance: float
    left_strain_fraction: float
    right_strain_fraction: float
    left_retained_blocks: int | None
    right_retained_blocks: int | None

    @property
    def width(self) -> float:
        """Return the sampled strain width of the transition bracket."""
        return self.right_strain_fraction - self.left_strain_fraction


@dataclass(frozen=True, slots=True)
class StrainBondDegeneracyTransitionBracket:
    """Bracket one detected change in the number of bond-length orbits."""

    left_strain_fraction: float
    right_strain_fraction: float
    left_distinct_bond_lengths: int
    right_distinct_bond_lengths: int

    @property
    def width(self) -> float:
        """Return the sampled strain width of the transition bracket."""
        return self.right_strain_fraction - self.left_strain_fraction


@dataclass(frozen=True, slots=True)
class SyntheticStrainTransitionRefinementResult:
    """Retain bounded refinements of transitions detected on a base scan."""

    base_sample_count: int
    maximum_refinement_depth: int
    shell_transitions: tuple[StrainShellTransitionBracket, ...]
    bond_degeneracy_transitions: tuple[StrainBondDegeneracyTransitionBracket, ...]
    maximum_final_bracket_width: float
    status: str = "sampled-transition-brackets-not-continuum-certificates"


class SyntheticStrainTransitionRefiner:
    """Refine only transitions already detected between adjacent base samples."""

    __slots__ = ()

    def execute(
        self,
        base_result: SyntheticStrainResult,
        maximum_refinement_depth: int,
    ) -> SyntheticStrainTransitionRefinementResult:
        """Bisect detected shell and bond-degeneracy transition brackets."""
        if type(base_result) is not SyntheticStrainResult:
            raise TypeError("base_result must be SyntheticStrainResult")
        if (
            type(maximum_refinement_depth) is not int
            or not 1 <= maximum_refinement_depth <= 20
        ):
            raise ValueError(
                "maximum_refinement_depth must be a built-in integer in [1, 20]"
            )
        if len(base_result.points) < 2:
            raise ValueError("base_result must contain at least two strain points")
        fractions = tuple(point.strain_fraction for point in base_result.points)
        if fractions != tuple(sorted(set(fractions))):
            raise ValueError(
                "base_result points must have strictly increasing strain fractions"
            )

        cache = {point.strain_fraction: point for point in base_result.points}
        shell_transitions: list[StrainShellTransitionBracket] = []
        for tolerance_index, tolerance in enumerate(base_result.tail_tolerances):
            for left, right in zip(
                base_result.points[:-1], base_result.points[1:], strict=True
            ):
                if (
                    left.first_passing_blocks[tolerance_index]
                    == right.first_passing_blocks[tolerance_index]
                ):
                    continue
                shell_transitions.extend(
                    self._refine_shell_transition(
                        base_result,
                        tolerance_index,
                        tolerance,
                        left,
                        right,
                        maximum_refinement_depth,
                        cache,
                    )
                )

        bond_transitions: list[StrainBondDegeneracyTransitionBracket] = []
        for left, right in zip(
            base_result.points[:-1], base_result.points[1:], strict=True
        ):
            if left.distinct_bond_lengths == right.distinct_bond_lengths:
                continue
            bond_transitions.extend(
                self._refine_bond_transition(
                    base_result,
                    left,
                    right,
                    maximum_refinement_depth,
                    cache,
                )
            )

        ordered_shells = tuple(
            sorted(
                shell_transitions,
                key=lambda bracket: (
                    bracket.tail_tolerance,
                    bracket.left_strain_fraction,
                    bracket.right_strain_fraction,
                ),
            )
        )
        ordered_bonds = tuple(
            sorted(
                bond_transitions,
                key=lambda bracket: (
                    bracket.left_strain_fraction,
                    bracket.right_strain_fraction,
                ),
            )
        )
        widths = tuple(bracket.width for bracket in ordered_shells) + tuple(
            bracket.width for bracket in ordered_bonds
        )
        return SyntheticStrainTransitionRefinementResult(
            base_sample_count=len(base_result.points),
            maximum_refinement_depth=maximum_refinement_depth,
            shell_transitions=ordered_shells,
            bond_degeneracy_transitions=ordered_bonds,
            maximum_final_bracket_width=max(widths, default=0.0),
        )

    def _evaluate(
        self,
        base_result: SyntheticStrainResult,
        fraction: float,
        cache: dict[float, StrainPointDiagnostic],
    ) -> StrainPointDiagnostic:
        cached = cache.get(fraction)
        if cached is not None:
            return cached
        point = (
            SyntheticStrainCalculator()
            .execute(
                base_result.path,
                base_result.construction_size,
                (fraction,),
                base_result.maximum_rotation_amplitude,
                base_result.tail_tolerances,
            )
            .points[0]
        )
        cache[fraction] = point
        return point

    def _refine_shell_transition(
        self,
        base_result: SyntheticStrainResult,
        tolerance_index: int,
        tolerance: float,
        initial_left: StrainPointDiagnostic,
        initial_right: StrainPointDiagnostic,
        maximum_refinement_depth: int,
        cache: dict[float, StrainPointDiagnostic],
    ) -> list[StrainShellTransitionBracket]:
        stack = [(initial_left, initial_right, maximum_refinement_depth)]
        brackets: list[StrainShellTransitionBracket] = []
        while stack:
            left, right, remaining = stack.pop()
            left_count = left.first_passing_blocks[tolerance_index]
            right_count = right.first_passing_blocks[tolerance_index]
            if remaining == 0:
                brackets.append(
                    StrainShellTransitionBracket(
                        tail_tolerance=tolerance,
                        left_strain_fraction=left.strain_fraction,
                        right_strain_fraction=right.strain_fraction,
                        left_retained_blocks=left_count,
                        right_retained_blocks=right_count,
                    )
                )
                continue
            midpoint_fraction = (left.strain_fraction + right.strain_fraction) / 2.0
            midpoint = self._evaluate(base_result, midpoint_fraction, cache)
            midpoint_count = midpoint.first_passing_blocks[tolerance_index]
            if left_count != midpoint_count:
                stack.append((left, midpoint, remaining - 1))
            if midpoint_count != right_count:
                stack.append((midpoint, right, remaining - 1))
        return brackets

    def _refine_bond_transition(
        self,
        base_result: SyntheticStrainResult,
        initial_left: StrainPointDiagnostic,
        initial_right: StrainPointDiagnostic,
        maximum_refinement_depth: int,
        cache: dict[float, StrainPointDiagnostic],
    ) -> list[StrainBondDegeneracyTransitionBracket]:
        stack = [(initial_left, initial_right, maximum_refinement_depth)]
        brackets: list[StrainBondDegeneracyTransitionBracket] = []
        while stack:
            left, right, remaining = stack.pop()
            left_count = left.distinct_bond_lengths
            right_count = right.distinct_bond_lengths
            if remaining == 0:
                brackets.append(
                    StrainBondDegeneracyTransitionBracket(
                        left_strain_fraction=left.strain_fraction,
                        right_strain_fraction=right.strain_fraction,
                        left_distinct_bond_lengths=left_count,
                        right_distinct_bond_lengths=right_count,
                    )
                )
                continue
            midpoint_fraction = (left.strain_fraction + right.strain_fraction) / 2.0
            midpoint = self._evaluate(base_result, midpoint_fraction, cache)
            midpoint_count = midpoint.distinct_bond_lengths
            if left_count != midpoint_count:
                stack.append((left, midpoint, remaining - 1))
            if midpoint_count != right_count:
                stack.append((midpoint, right, remaining - 1))
        return brackets


__all__ = [
    "StrainBondDegeneracyTransitionBracket",
    "StrainLocalityEnvelope",
    "StrainResponseEnvelope",
    "StrainWitnessRequirementEnvelope",
    "StrainShellTransitionBracket",
    "SyntheticStrainScanAssessor",
    "SyntheticStrainScanSummary",
    "SyntheticStrainTransitionRefinementResult",
    "SyntheticStrainTransitionRefiner",
]
