"""Matrix-field error and comparison diagnostics."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from ksdft2effmass.analysis.matrix_field.diagnostics import (
    MatrixFieldComparisonDiagnostics,
    MatrixFieldErrorSummary,
)
from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from .._record_admission import (
    _decoded_bool,
    _decoded_float,
    _decoded_optional_float,
    _finite_nonnegative,
    _mapping_value,
)


@dataclass(frozen=True, slots=True)
class Periodic1DRankNMatrixErrorResult(BaseTypedRecord):
    """Retain one raw and rank/energy-normalized matrix and spectrum error summary."""

    rank: int
    energy_reference: float
    matrix_frobenius_maximum: float
    matrix_frobenius_rms: float
    normalized_matrix_frobenius_maximum: float
    normalized_matrix_frobenius_rms: float
    ordered_spectrum_maximum: float
    ordered_spectrum_l2_rms: float
    normalized_ordered_spectrum_maximum: float
    normalized_ordered_spectrum_l2_rms: float

    def __post_init__(self) -> None:
        MatrixFieldErrorSummary(
            rank=self.rank,
            norm_energy_scale=self.energy_reference,
            matrix_frobenius_maximum=self.matrix_frobenius_maximum,
            matrix_frobenius_rms=self.matrix_frobenius_rms,
            normalized_matrix_frobenius_maximum=(
                self.normalized_matrix_frobenius_maximum
            ),
            normalized_matrix_frobenius_rms=self.normalized_matrix_frobenius_rms,
            ordered_spectrum_maximum=self.ordered_spectrum_maximum,
            ordered_spectrum_l2_rms=self.ordered_spectrum_l2_rms,
            normalized_ordered_spectrum_maximum=(
                self.normalized_ordered_spectrum_maximum
            ),
            normalized_ordered_spectrum_l2_rms=(
                self.normalized_ordered_spectrum_l2_rms
            ),
        )

    @classmethod
    def from_diagnostics(cls, value: MatrixFieldErrorSummary) -> Self:
        """Copy one validated matrix-field diagnostic onto the calculation wire."""
        if type(value) is not MatrixFieldErrorSummary:
            raise TypeError("value must be MatrixFieldErrorSummary")
        return cls(
            rank=value.rank,
            energy_reference=value.norm_energy_scale,
            matrix_frobenius_maximum=value.matrix_frobenius_maximum,
            matrix_frobenius_rms=value.matrix_frobenius_rms,
            normalized_matrix_frobenius_maximum=(
                value.normalized_matrix_frobenius_maximum
            ),
            normalized_matrix_frobenius_rms=value.normalized_matrix_frobenius_rms,
            ordered_spectrum_maximum=value.ordered_spectrum_maximum,
            ordered_spectrum_l2_rms=value.ordered_spectrum_l2_rms,
            normalized_ordered_spectrum_maximum=(
                value.normalized_ordered_spectrum_maximum
            ),
            normalized_ordered_spectrum_l2_rms=(
                value.normalized_ordered_spectrum_l2_rms
            ),
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "rank": self.rank,
            "energy_reference": self.energy_reference,
            "matrix_frobenius_maximum": self.matrix_frobenius_maximum,
            "matrix_frobenius_rms": self.matrix_frobenius_rms,
            "normalized_matrix_frobenius_maximum": (
                self.normalized_matrix_frobenius_maximum
            ),
            "normalized_matrix_frobenius_rms": (self.normalized_matrix_frobenius_rms),
            "ordered_spectrum_maximum": self.ordered_spectrum_maximum,
            "ordered_spectrum_l2_rms": self.ordered_spectrum_l2_rms,
            "normalized_ordered_spectrum_maximum": (
                self.normalized_ordered_spectrum_maximum
            ),
            "normalized_ordered_spectrum_l2_rms": (
                self.normalized_ordered_spectrum_l2_rms
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "rank",
            "energy_reference",
            "matrix_frobenius_maximum",
            "matrix_frobenius_rms",
            "normalized_matrix_frobenius_maximum",
            "normalized_matrix_frobenius_rms",
            "ordered_spectrum_maximum",
            "ordered_spectrum_l2_rms",
            "normalized_ordered_spectrum_maximum",
            "normalized_ordered_spectrum_l2_rms",
        }:
            raise ValueError("matrix error fields do not match")
        rank = values["rank"]
        if type(rank) is not int:
            raise TypeError("rank must decode to a built-in integer")
        return cls(
            rank=rank,
            energy_reference=_decoded_float(
                values["energy_reference"], "energy_reference"
            ),
            matrix_frobenius_maximum=_decoded_float(
                values["matrix_frobenius_maximum"], "matrix_frobenius_maximum"
            ),
            matrix_frobenius_rms=_decoded_float(
                values["matrix_frobenius_rms"], "matrix_frobenius_rms"
            ),
            normalized_matrix_frobenius_maximum=_decoded_float(
                values["normalized_matrix_frobenius_maximum"],
                "normalized_matrix_frobenius_maximum",
            ),
            normalized_matrix_frobenius_rms=_decoded_float(
                values["normalized_matrix_frobenius_rms"],
                "normalized_matrix_frobenius_rms",
            ),
            ordered_spectrum_maximum=_decoded_float(
                values["ordered_spectrum_maximum"], "ordered_spectrum_maximum"
            ),
            ordered_spectrum_l2_rms=_decoded_float(
                values["ordered_spectrum_l2_rms"], "ordered_spectrum_l2_rms"
            ),
            normalized_ordered_spectrum_maximum=_decoded_float(
                values["normalized_ordered_spectrum_maximum"],
                "normalized_ordered_spectrum_maximum",
            ),
            normalized_ordered_spectrum_l2_rms=_decoded_float(
                values["normalized_ordered_spectrum_l2_rms"],
                "normalized_ordered_spectrum_l2_rms",
            ),
        )


@dataclass(frozen=True, slots=True)
class Periodic1DRankNMatrixComparisonResult(BaseTypedRecord):
    """Retain matrix/spectrum errors and pointwise perturbation-bound evidence."""

    errors: Periodic1DRankNMatrixErrorResult
    maximum_ordered_spectrum_minus_spectral_norm: float
    maximum_ordered_spectrum_minus_frobenius_norm: float
    maximum_spectral_norm_minus_frobenius_norm: float
    applied_perturbation_bound_tolerance: float
    all_perturbation_bounds_pass: bool
    maximum_band_over_spectral_ratio: float | None
    maximum_band_over_frobenius_ratio: float | None

    def __post_init__(self) -> None:
        if type(self.errors) is not Periodic1DRankNMatrixErrorResult:
            raise TypeError("errors must be the exact matrix error record")
        for value, name in (
            (
                self.maximum_ordered_spectrum_minus_spectral_norm,
                "maximum_ordered_spectrum_minus_spectral_norm",
            ),
            (
                self.maximum_ordered_spectrum_minus_frobenius_norm,
                "maximum_ordered_spectrum_minus_frobenius_norm",
            ),
            (
                self.maximum_spectral_norm_minus_frobenius_norm,
                "maximum_spectral_norm_minus_frobenius_norm",
            ),
            (
                self.applied_perturbation_bound_tolerance,
                "applied_perturbation_bound_tolerance",
            ),
        ):
            _finite_nonnegative(value, name)
        if type(self.all_perturbation_bounds_pass) is not bool:
            raise TypeError("all_perturbation_bounds_pass must be a built-in bool")
        observed = max(
            self.maximum_ordered_spectrum_minus_spectral_norm,
            self.maximum_ordered_spectrum_minus_frobenius_norm,
            self.maximum_spectral_norm_minus_frobenius_norm,
        )
        if self.all_perturbation_bounds_pass is not (
            observed <= self.applied_perturbation_bound_tolerance
        ):
            raise ValueError("perturbation-bound disposition is inconsistent")
        for optional_value, name in (
            (
                self.maximum_band_over_spectral_ratio,
                "maximum_band_over_spectral_ratio",
            ),
            (
                self.maximum_band_over_frobenius_ratio,
                "maximum_band_over_frobenius_ratio",
            ),
        ):
            if optional_value is not None:
                _finite_nonnegative(optional_value, name)

    @classmethod
    def from_diagnostics(
        cls,
        value: MatrixFieldComparisonDiagnostics,
        applied_tolerance: float,
    ) -> Self:
        """Copy one matrix comparison and its frozen gate onto the calculation wire."""
        if type(value) is not MatrixFieldComparisonDiagnostics:
            raise TypeError("value must be MatrixFieldComparisonDiagnostics")
        _finite_nonnegative(applied_tolerance, "applied_tolerance")
        bounds = value.perturbation_bounds
        observed = max(
            bounds.maximum_ordered_spectrum_minus_spectral_norm,
            bounds.maximum_ordered_spectrum_minus_frobenius_norm,
            bounds.maximum_spectral_norm_minus_frobenius_norm,
        )
        return cls(
            errors=Periodic1DRankNMatrixErrorResult.from_diagnostics(value.errors),
            maximum_ordered_spectrum_minus_spectral_norm=bounds.maximum_ordered_spectrum_minus_spectral_norm,
            maximum_ordered_spectrum_minus_frobenius_norm=bounds.maximum_ordered_spectrum_minus_frobenius_norm,
            maximum_spectral_norm_minus_frobenius_norm=bounds.maximum_spectral_norm_minus_frobenius_norm,
            applied_perturbation_bound_tolerance=applied_tolerance,
            all_perturbation_bounds_pass=observed <= applied_tolerance,
            maximum_band_over_spectral_ratio=bounds.maximum_band_over_spectral_ratio,
            maximum_band_over_frobenius_ratio=bounds.maximum_band_over_frobenius_ratio,
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "errors": self.errors,
            "maximum_ordered_spectrum_minus_spectral_norm": (
                self.maximum_ordered_spectrum_minus_spectral_norm
            ),
            "maximum_ordered_spectrum_minus_frobenius_norm": (
                self.maximum_ordered_spectrum_minus_frobenius_norm
            ),
            "maximum_spectral_norm_minus_frobenius_norm": (
                self.maximum_spectral_norm_minus_frobenius_norm
            ),
            "applied_perturbation_bound_tolerance": (
                self.applied_perturbation_bound_tolerance
            ),
            "all_perturbation_bounds_pass": self.all_perturbation_bounds_pass,
            "maximum_band_over_spectral_ratio": (self.maximum_band_over_spectral_ratio),
            "maximum_band_over_frobenius_ratio": (
                self.maximum_band_over_frobenius_ratio
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "errors",
            "maximum_ordered_spectrum_minus_spectral_norm",
            "maximum_ordered_spectrum_minus_frobenius_norm",
            "maximum_spectral_norm_minus_frobenius_norm",
            "applied_perturbation_bound_tolerance",
            "all_perturbation_bounds_pass",
            "maximum_band_over_spectral_ratio",
            "maximum_band_over_frobenius_ratio",
        }:
            raise ValueError("matrix comparison fields do not match")
        return cls(
            errors=Periodic1DRankNMatrixErrorResult.from_dict(
                _mapping_value(values["errors"], "errors")
            ),
            maximum_ordered_spectrum_minus_spectral_norm=_decoded_float(
                values["maximum_ordered_spectrum_minus_spectral_norm"],
                "maximum_ordered_spectrum_minus_spectral_norm",
            ),
            maximum_ordered_spectrum_minus_frobenius_norm=_decoded_float(
                values["maximum_ordered_spectrum_minus_frobenius_norm"],
                "maximum_ordered_spectrum_minus_frobenius_norm",
            ),
            maximum_spectral_norm_minus_frobenius_norm=_decoded_float(
                values["maximum_spectral_norm_minus_frobenius_norm"],
                "maximum_spectral_norm_minus_frobenius_norm",
            ),
            applied_perturbation_bound_tolerance=_decoded_float(
                values["applied_perturbation_bound_tolerance"],
                "applied_perturbation_bound_tolerance",
            ),
            all_perturbation_bounds_pass=_decoded_bool(
                values["all_perturbation_bounds_pass"],
                "all_perturbation_bounds_pass",
            ),
            maximum_band_over_spectral_ratio=_decoded_optional_float(
                values["maximum_band_over_spectral_ratio"],
                "maximum_band_over_spectral_ratio",
            ),
            maximum_band_over_frobenius_ratio=_decoded_optional_float(
                values["maximum_band_over_frobenius_ratio"],
                "maximum_band_over_frobenius_ratio",
            ),
        )
