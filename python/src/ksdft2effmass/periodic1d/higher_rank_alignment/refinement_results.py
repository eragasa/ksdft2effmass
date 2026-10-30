"""Immutable refinement results for higher-rank alignment calculations."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

import numpy as np
from projectkoios.numerics.numpy.typing import Float64Array, Int64Array

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from ._record_admission import (
    _decoded_float,
    _finite_nonnegative,
    _float_array,
    _int_array,
    _nonempty,
)
from .calculation import Periodic1DHigherRankAlignmentCalculationControls
from .definition import Periodic1DHigherRankAlignmentChannel


@dataclass(frozen=True, slots=True)
class Periodic1DHigherRankBlockRefinementResult(BaseTypedRecord):
    """Retain all recorded block-norm changes for one channel and mesh pair."""

    channel: Periodic1DHigherRankAlignmentChannel
    coarse_mesh_size: int
    fine_mesh_size: int
    translations: Int64Array
    coarse_normalized_block_norms: Float64Array
    fine_normalized_block_norms: Float64Array
    absolute_changes: Float64Array
    relative_changes: Float64Array
    applied_tolerances: Float64Array
    signed_margins: Float64Array
    all_pass: bool

    def __post_init__(self) -> None:
        if type(self.channel) is not Periodic1DHigherRankAlignmentChannel:
            raise TypeError("channel must be the exact alignment enum")
        if (
            type(self.coarse_mesh_size) is not int
            or type(self.fine_mesh_size) is not int
            or not self.coarse_mesh_size < self.fine_mesh_size
        ):
            raise ValueError("mesh sizes must be increasing built-in integers")
        translations = _int_array(self.translations, "translations")
        arrays = [
            _float_array(
                self.coarse_normalized_block_norms,
                "coarse_normalized_block_norms",
            ),
            _float_array(
                self.fine_normalized_block_norms,
                "fine_normalized_block_norms",
            ),
            _float_array(self.absolute_changes, "absolute_changes"),
            _float_array(self.relative_changes, "relative_changes"),
            _float_array(self.applied_tolerances, "applied_tolerances"),
            _float_array(self.signed_margins, "signed_margins"),
        ]
        if any(array.shape != translations.shape for array in arrays):
            raise ValueError("refinement arrays must share the translation shape")
        coarse, fine, absolute, relative, applied, margins = arrays
        if bool((coarse < 0.0).any()) or bool((fine < 0.0).any()):
            raise ValueError("normalized block norms must be nonnegative")
        controls = Periodic1DHigherRankAlignmentCalculationControls
        expected = tuple(
            (
                abs(float(fine_value) - float(coarse_value)),
                abs(float(fine_value) - float(coarse_value))
                / max(
                    abs(float(coarse_value)),
                    abs(float(fine_value)),
                    controls.REFINEMENT_DENOMINATOR_FLOOR,
                ),
                controls.REFINEMENT_ABSOLUTE_TOLERANCE
                + controls.REFINEMENT_RELATIVE_TOLERANCE
                * max(abs(float(coarse_value)), abs(float(fine_value))),
            )
            for coarse_value, fine_value in zip(coarse, fine, strict=True)
        )
        expected_absolute = np.asarray(
            tuple(item[0] for item in expected), dtype=np.float64
        )
        expected_relative = np.asarray(
            tuple(item[1] for item in expected), dtype=np.float64
        )
        expected_applied = np.asarray(
            tuple(item[2] for item in expected), dtype=np.float64
        )
        expected_margins = expected_applied - expected_absolute
        if not (
            np.array_equal(absolute, expected_absolute)
            and np.array_equal(relative, expected_relative)
            and np.array_equal(applied, expected_applied)
            and np.array_equal(margins, expected_margins)
        ):
            raise ValueError("block refinement arithmetic is inconsistent")
        if type(self.all_pass) is not bool:
            raise TypeError("all_pass must be a built-in bool")
        if self.all_pass is not bool(np.all(expected_margins >= 0.0)):
            raise ValueError("all_pass must agree with derived signed margins")
        object.__setattr__(self, "translations", translations)
        object.__setattr__(self, "coarse_normalized_block_norms", arrays[0])
        object.__setattr__(self, "fine_normalized_block_norms", arrays[1])
        object.__setattr__(self, "absolute_changes", arrays[2])
        object.__setattr__(self, "relative_changes", arrays[3])
        object.__setattr__(self, "applied_tolerances", arrays[4])
        object.__setattr__(self, "signed_margins", arrays[5])

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "channel": self.channel.value,
            "coarse_mesh_size": self.coarse_mesh_size,
            "fine_mesh_size": self.fine_mesh_size,
            "translations": self.translations,
            "coarse_normalized_block_norms": self.coarse_normalized_block_norms,
            "fine_normalized_block_norms": self.fine_normalized_block_norms,
            "absolute_changes": self.absolute_changes,
            "relative_changes": self.relative_changes,
            "applied_tolerances": self.applied_tolerances,
            "signed_margins": self.signed_margins,
            "all_pass": self.all_pass,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "channel",
            "coarse_mesh_size",
            "fine_mesh_size",
            "translations",
            "coarse_normalized_block_norms",
            "fine_normalized_block_norms",
            "absolute_changes",
            "relative_changes",
            "applied_tolerances",
            "signed_margins",
            "all_pass",
        }
        if set(values) != required:
            raise ValueError("block refinement fields do not match")
        channel = values["channel"]
        coarse = values["coarse_mesh_size"]
        fine = values["fine_mesh_size"]
        all_pass = values["all_pass"]
        if (
            type(channel) is not str
            or type(coarse) is not int
            or type(fine) is not int
            or type(all_pass) is not bool
        ):
            raise TypeError(
                "refinement identities and disposition have wrong decoded types"
            )
        arrays: dict[str, np.ndarray] = {}
        for name in required - {
            "channel",
            "coarse_mesh_size",
            "fine_mesh_size",
            "all_pass",
        }:
            value = values[name]
            if not isinstance(value, np.ndarray):
                raise TypeError(f"{name} must decode to numpy.ndarray")
            arrays[name] = value
        return cls(
            channel=Periodic1DHigherRankAlignmentChannel(channel),
            coarse_mesh_size=coarse,
            fine_mesh_size=fine,
            all_pass=all_pass,
            translations=_int_array(arrays["translations"], "translations"),
            coarse_normalized_block_norms=arrays["coarse_normalized_block_norms"],
            fine_normalized_block_norms=arrays["fine_normalized_block_norms"],
            absolute_changes=arrays["absolute_changes"],
            relative_changes=arrays["relative_changes"],
            applied_tolerances=arrays["applied_tolerances"],
            signed_margins=arrays["signed_margins"],
        )


@dataclass(frozen=True, slots=True)
class Periodic1DHigherRankScalarRefinementResult(BaseTypedRecord):
    """Retain one final-mesh scalar refinement value and frozen gate."""

    channel: Periodic1DHigherRankAlignmentChannel
    diagnostic_path: str
    coarse_mesh_size: int
    fine_mesh_size: int
    coarse_value: float
    fine_value: float
    absolute_change: float
    relative_change: float
    applied_tolerance: float
    signed_margin: float
    passes: bool

    def __post_init__(self) -> None:
        if type(self.channel) is not Periodic1DHigherRankAlignmentChannel:
            raise TypeError("channel must be the exact alignment enum")
        _nonempty(self.diagnostic_path, "diagnostic_path")
        if (self.coarse_mesh_size, self.fine_mesh_size) != (1025, 2049):
            raise ValueError("scalar refinement must use the frozen final mesh pair")
        for value, name in (
            (self.coarse_value, "coarse_value"),
            (self.fine_value, "fine_value"),
            (self.absolute_change, "absolute_change"),
            (self.relative_change, "relative_change"),
            (self.applied_tolerance, "applied_tolerance"),
        ):
            _finite_nonnegative(value, name)
        if type(self.signed_margin) is not float or not math.isfinite(
            self.signed_margin
        ):
            raise ValueError("signed_margin must be a finite built-in float")
        expected_change = abs(self.fine_value - self.coarse_value)
        expected_relative = expected_change / max(
            abs(self.coarse_value),
            abs(self.fine_value),
            Periodic1DHigherRankAlignmentCalculationControls.REFINEMENT_DENOMINATOR_FLOOR,
        )
        controls = Periodic1DHigherRankAlignmentCalculationControls
        expected_tolerance = controls.REFINEMENT_ABSOLUTE_TOLERANCE + (
            controls.REFINEMENT_RELATIVE_TOLERANCE
            * max(abs(self.coarse_value), abs(self.fine_value))
        )
        if (
            self.absolute_change != expected_change
            or self.relative_change != expected_relative
            or self.applied_tolerance != expected_tolerance
            or self.signed_margin != expected_tolerance - expected_change
        ):
            raise ValueError("scalar refinement arithmetic is inconsistent")
        if type(self.passes) is not bool or self.passes is not (
            self.signed_margin >= 0.0
        ):
            raise ValueError("scalar refinement disposition is inconsistent")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "channel": self.channel.value,
            "diagnostic_path": self.diagnostic_path,
            "coarse_mesh_size": self.coarse_mesh_size,
            "fine_mesh_size": self.fine_mesh_size,
            "coarse_value": self.coarse_value,
            "fine_value": self.fine_value,
            "absolute_change": self.absolute_change,
            "relative_change": self.relative_change,
            "applied_tolerance": self.applied_tolerance,
            "signed_margin": self.signed_margin,
            "passes": self.passes,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "channel",
            "diagnostic_path",
            "coarse_mesh_size",
            "fine_mesh_size",
            "coarse_value",
            "fine_value",
            "absolute_change",
            "relative_change",
            "applied_tolerance",
            "signed_margin",
            "passes",
        }
        if set(values) != required:
            raise ValueError("scalar refinement fields do not match")
        channel = values["channel"]
        path = values["diagnostic_path"]
        coarse = values["coarse_mesh_size"]
        fine = values["fine_mesh_size"]
        passes = values["passes"]
        if type(channel) is not str or type(path) is not str:
            raise TypeError("scalar refinement identities must decode to strings")
        if type(coarse) is not int or type(fine) is not int:
            raise TypeError("scalar refinement mesh sizes must decode to integers")
        if type(passes) is not bool:
            raise TypeError("scalar refinement passes must decode to bool")
        floats: dict[str, float] = {}
        for name in required - {
            "channel",
            "diagnostic_path",
            "coarse_mesh_size",
            "fine_mesh_size",
            "passes",
        }:
            floats[name] = _decoded_float(values[name], name)
        return cls(
            channel=Periodic1DHigherRankAlignmentChannel(channel),
            diagnostic_path=path,
            coarse_mesh_size=coarse,
            fine_mesh_size=fine,
            passes=passes,
            **floats,
        )
