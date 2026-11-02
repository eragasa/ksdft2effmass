"""Bounded refinement of synthetic-strain transition brackets."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from ..strain import (
    StrainPointDiagnostic,
    SyntheticStrainCalculator,
    SyntheticStrainResult,
)


@dataclass(frozen=True, slots=True)
class StrainShellTransitionBracket(BaseTypedRecord):
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

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "tail_tolerance": self.tail_tolerance,
            "left_strain_fraction": self.left_strain_fraction,
            "right_strain_fraction": self.right_strain_fraction,
            "left_retained_blocks": self.left_retained_blocks,
            "right_retained_blocks": self.right_retained_blocks,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "tail_tolerance",
            "left_strain_fraction",
            "right_strain_fraction",
            "left_retained_blocks",
            "right_retained_blocks",
        }
        if set(values) != required:
            raise ValueError("StrainShellTransitionBracket fields do not match")
        tail_tolerance = values["tail_tolerance"]
        left_strain_fraction = values["left_strain_fraction"]
        right_strain_fraction = values["right_strain_fraction"]
        left_retained_blocks = values["left_retained_blocks"]
        right_retained_blocks = values["right_retained_blocks"]
        if (
            type(tail_tolerance) is not float
            or type(left_strain_fraction) is not float
            or type(right_strain_fraction) is not float
        ):
            raise TypeError("float fields must use exact built-in types")
        if (
            left_retained_blocks is not None and type(left_retained_blocks) is not int
        ) or (
            right_retained_blocks is not None and type(right_retained_blocks) is not int
        ):
            raise TypeError("optional integer fields have invalid types")
        return cls(
            tail_tolerance=tail_tolerance,
            left_strain_fraction=left_strain_fraction,
            right_strain_fraction=right_strain_fraction,
            left_retained_blocks=left_retained_blocks,
            right_retained_blocks=right_retained_blocks,
        )


@dataclass(frozen=True, slots=True)
class StrainBondDegeneracyTransitionBracket(BaseTypedRecord):
    """Bracket one detected change in the number of bond-length orbits."""

    left_strain_fraction: float
    right_strain_fraction: float
    left_distinct_bond_lengths: int
    right_distinct_bond_lengths: int

    @property
    def width(self) -> float:
        """Return the sampled strain width of the transition bracket."""
        return self.right_strain_fraction - self.left_strain_fraction

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "left_strain_fraction": self.left_strain_fraction,
            "right_strain_fraction": self.right_strain_fraction,
            "left_distinct_bond_lengths": self.left_distinct_bond_lengths,
            "right_distinct_bond_lengths": self.right_distinct_bond_lengths,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "left_strain_fraction",
            "right_strain_fraction",
            "left_distinct_bond_lengths",
            "right_distinct_bond_lengths",
        }
        if set(values) != required:
            raise ValueError(
                "StrainBondDegeneracyTransitionBracket fields do not match"
            )
        left_strain_fraction = values["left_strain_fraction"]
        right_strain_fraction = values["right_strain_fraction"]
        left_distinct_bond_lengths = values["left_distinct_bond_lengths"]
        right_distinct_bond_lengths = values["right_distinct_bond_lengths"]
        if (
            type(left_strain_fraction) is not float
            or type(right_strain_fraction) is not float
        ):
            raise TypeError("float fields must use exact built-in types")
        if (
            type(left_distinct_bond_lengths) is not int
            or type(right_distinct_bond_lengths) is not int
        ):
            raise TypeError("integer fields must use exact built-in types")
        return cls(
            left_strain_fraction=left_strain_fraction,
            right_strain_fraction=right_strain_fraction,
            left_distinct_bond_lengths=left_distinct_bond_lengths,
            right_distinct_bond_lengths=right_distinct_bond_lengths,
        )


@dataclass(frozen=True, slots=True)
class SyntheticStrainTransitionRefinementResult(BaseTypedRecord):
    """Retain bounded refinements of transitions detected on a base scan."""

    base_sample_count: int
    maximum_refinement_depth: int
    shell_transitions: tuple[StrainShellTransitionBracket, ...]
    bond_degeneracy_transitions: tuple[StrainBondDegeneracyTransitionBracket, ...]
    maximum_final_bracket_width: float
    status: str = "sampled-transition-brackets-not-continuum-certificates"

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "base_sample_count": self.base_sample_count,
            "maximum_refinement_depth": self.maximum_refinement_depth,
            "shell_transitions": self.shell_transitions,
            "bond_degeneracy_transitions": self.bond_degeneracy_transitions,
            "maximum_final_bracket_width": self.maximum_final_bracket_width,
            "status": self.status,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "base_sample_count",
            "maximum_refinement_depth",
            "shell_transitions",
            "bond_degeneracy_transitions",
            "maximum_final_bracket_width",
            "status",
        }
        if set(values) != required:
            raise ValueError(
                "SyntheticStrainTransitionRefinementResult fields do not match"
            )
        base_sample_count = values["base_sample_count"]
        maximum_refinement_depth = values["maximum_refinement_depth"]
        shell_transitions_values = values["shell_transitions"]
        bond_degeneracy_transitions_values = values["bond_degeneracy_transitions"]
        maximum_final_bracket_width = values["maximum_final_bracket_width"]
        status = values["status"]
        if type(maximum_final_bracket_width) is not float:
            raise TypeError("float fields must use exact built-in types")
        if (
            type(base_sample_count) is not int
            or type(maximum_refinement_depth) is not int
        ):
            raise TypeError("integer fields must use exact built-in types")
        if type(status) is not str:
            raise TypeError("string fields must use exact built-in types")
        if not isinstance(shell_transitions_values, tuple) or any(
            not isinstance(item, Mapping) for item in shell_transitions_values
        ):
            raise TypeError("shell_transitions must decode to a tuple of mappings")
        if not isinstance(bond_degeneracy_transitions_values, tuple) or any(
            not isinstance(item, Mapping) for item in bond_degeneracy_transitions_values
        ):
            raise TypeError(
                "bond_degeneracy_transitions must decode to a tuple of mappings"
            )
        return cls(
            base_sample_count=base_sample_count,
            maximum_refinement_depth=maximum_refinement_depth,
            shell_transitions=tuple(
                StrainShellTransitionBracket.from_dict(item)
                for item in shell_transitions_values
            ),
            bond_degeneracy_transitions=tuple(
                StrainBondDegeneracyTransitionBracket.from_dict(item)
                for item in bond_degeneracy_transitions_values
            ),
            maximum_final_bracket_width=maximum_final_bracket_width,
            status=status,
        )


class SyntheticStrainTransitionRefiner:
    """Own refinement of transitions detected between adjacent base samples."""

    __slots__ = ("_base_result", "_maximum_refinement_depth")

    def __init__(
        self,
        *,
        base_result: SyntheticStrainResult,
        maximum_refinement_depth: int,
    ) -> None:
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
        self._base_result = base_result
        self._maximum_refinement_depth = maximum_refinement_depth

    def execute(self) -> SyntheticStrainTransitionRefinementResult:
        """Bisect the constructor-bound shell and bond transition brackets."""
        base_result = self._base_result
        maximum_refinement_depth = self._maximum_refinement_depth
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
            SyntheticStrainCalculator(
                path=base_result.path,
                construction_size=base_result.construction_size,
                strain_fractions=(fraction,),
                maximum_rotation_amplitude=base_result.maximum_rotation_amplitude,
                tail_tolerances=base_result.tail_tolerances,
            )
            .execute()
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
