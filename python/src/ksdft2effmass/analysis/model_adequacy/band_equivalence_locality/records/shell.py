"""Metric-shell and first-passing locality result values."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from ..results import (
    BandEquivalenceLocalityFirstPassingDecision,
    BandEquivalenceLocalityShellAnalysis,
)
from .channels import ErrorChannels


@dataclass(frozen=True, slots=True)
class ShellDiagnostic(BaseTypedRecord):
    """Retain all diagnostics at one complete metric-shell cutoff."""

    shell_index: int
    retained_blocks: int
    reference_truncation: ErrorChannels
    comparison_truncation: ErrorChannels
    reference_total: ErrorChannels
    comparison_total: ErrorChannels
    reference_shell_power: float
    comparison_shell_power: float
    reference_omitted_power: float
    comparison_omitted_power: float
    reference_total_omitted_power: float
    comparison_total_omitted_power: float
    reference_truncation_parseval_defect: float
    comparison_truncation_parseval_defect: float

    @classmethod
    def from_analysis(cls, analysis: BandEquivalenceLocalityShellAnalysis) -> Self:
        """Project one plain scientific shell into a retained record."""
        if type(analysis) is not BandEquivalenceLocalityShellAnalysis:
            raise TypeError("analysis must be BandEquivalenceLocalityShellAnalysis")
        return cls(
            shell_index=analysis.shell_index,
            retained_blocks=analysis.retained_blocks,
            reference_truncation=ErrorChannels.from_analysis(
                analysis.reference_truncation
            ),
            comparison_truncation=ErrorChannels.from_analysis(
                analysis.comparison_truncation
            ),
            reference_total=ErrorChannels.from_analysis(analysis.reference_total),
            comparison_total=ErrorChannels.from_analysis(analysis.comparison_total),
            reference_shell_power=analysis.reference_shell_power,
            comparison_shell_power=analysis.comparison_shell_power,
            reference_omitted_power=analysis.reference_omitted_power,
            comparison_omitted_power=analysis.comparison_omitted_power,
            reference_total_omitted_power=analysis.reference_total_omitted_power,
            comparison_total_omitted_power=analysis.comparison_total_omitted_power,
            reference_truncation_parseval_defect=analysis.reference_truncation_parseval_defect,
            comparison_truncation_parseval_defect=analysis.comparison_truncation_parseval_defect,
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "shell_index": self.shell_index,
            "retained_blocks": self.retained_blocks,
            "reference_truncation": self.reference_truncation,
            "comparison_truncation": self.comparison_truncation,
            "reference_total": self.reference_total,
            "comparison_total": self.comparison_total,
            "reference_shell_power": self.reference_shell_power,
            "comparison_shell_power": self.comparison_shell_power,
            "reference_omitted_power": self.reference_omitted_power,
            "comparison_omitted_power": self.comparison_omitted_power,
            "reference_total_omitted_power": self.reference_total_omitted_power,
            "comparison_total_omitted_power": self.comparison_total_omitted_power,
            "reference_truncation_parseval_defect": (
                self.reference_truncation_parseval_defect
            ),
            "comparison_truncation_parseval_defect": (
                self.comparison_truncation_parseval_defect
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "shell_index",
            "retained_blocks",
            "reference_truncation",
            "comparison_truncation",
            "reference_total",
            "comparison_total",
            "reference_shell_power",
            "comparison_shell_power",
            "reference_omitted_power",
            "comparison_omitted_power",
            "reference_total_omitted_power",
            "comparison_total_omitted_power",
            "reference_truncation_parseval_defect",
            "comparison_truncation_parseval_defect",
        }
        if set(values) != required:
            raise ValueError("ShellDiagnostic fields do not match")
        shell_index = values["shell_index"]
        retained_blocks = values["retained_blocks"]
        reference_truncation_value = values["reference_truncation"]
        comparison_truncation_value = values["comparison_truncation"]
        reference_total_value = values["reference_total"]
        comparison_total_value = values["comparison_total"]
        reference_shell_power = values["reference_shell_power"]
        comparison_shell_power = values["comparison_shell_power"]
        reference_omitted_power = values["reference_omitted_power"]
        comparison_omitted_power = values["comparison_omitted_power"]
        reference_total_omitted_power = values["reference_total_omitted_power"]
        comparison_total_omitted_power = values["comparison_total_omitted_power"]
        reference_truncation_parseval_defect = values[
            "reference_truncation_parseval_defect"
        ]
        comparison_truncation_parseval_defect = values[
            "comparison_truncation_parseval_defect"
        ]
        if (
            type(reference_shell_power) is not float
            or type(comparison_shell_power) is not float
            or type(reference_omitted_power) is not float
            or type(comparison_omitted_power) is not float
            or type(reference_total_omitted_power) is not float
            or type(comparison_total_omitted_power) is not float
            or type(reference_truncation_parseval_defect) is not float
            or type(comparison_truncation_parseval_defect) is not float
        ):
            raise TypeError("float fields must use exact built-in types")
        if type(shell_index) is not int or type(retained_blocks) is not int:
            raise TypeError("integer fields must use exact built-in types")
        if not isinstance(reference_truncation_value, Mapping):
            raise TypeError("reference_truncation must decode to a mapping")
        if not isinstance(comparison_truncation_value, Mapping):
            raise TypeError("comparison_truncation must decode to a mapping")
        if not isinstance(reference_total_value, Mapping):
            raise TypeError("reference_total must decode to a mapping")
        if not isinstance(comparison_total_value, Mapping):
            raise TypeError("comparison_total must decode to a mapping")
        return cls(
            shell_index=shell_index,
            retained_blocks=retained_blocks,
            reference_truncation=ErrorChannels.from_dict(reference_truncation_value),
            comparison_truncation=ErrorChannels.from_dict(comparison_truncation_value),
            reference_total=ErrorChannels.from_dict(reference_total_value),
            comparison_total=ErrorChannels.from_dict(comparison_total_value),
            reference_shell_power=reference_shell_power,
            comparison_shell_power=comparison_shell_power,
            reference_omitted_power=reference_omitted_power,
            comparison_omitted_power=comparison_omitted_power,
            reference_total_omitted_power=reference_total_omitted_power,
            comparison_total_omitted_power=comparison_total_omitted_power,
            reference_truncation_parseval_defect=reference_truncation_parseval_defect,
            comparison_truncation_parseval_defect=comparison_truncation_parseval_defect,
        )


@dataclass(frozen=True, slots=True)
class FirstPassingDecision(BaseTypedRecord):
    """Name one first-passing complete shell or an unresolved sampled decision."""

    tolerance: float
    reference_band_shell: int | None
    comparison_band_shell: int | None
    reference_hamiltonian_shell: int | None
    comparison_hamiltonian_shell: int | None
    reference_band_passing_error: float | None
    reference_band_preceding_error: float | None
    comparison_band_passing_error: float | None
    comparison_band_preceding_error: float | None
    reference_hamiltonian_passing_error: float | None
    reference_hamiltonian_preceding_error: float | None
    comparison_hamiltonian_passing_error: float | None
    comparison_hamiltonian_preceding_error: float | None

    @classmethod
    def from_analysis(
        cls, analysis: BandEquivalenceLocalityFirstPassingDecision
    ) -> Self:
        """Project one plain scientific decision into a retained record."""
        if type(analysis) is not BandEquivalenceLocalityFirstPassingDecision:
            raise TypeError(
                "analysis must be BandEquivalenceLocalityFirstPassingDecision"
            )
        return cls(
            tolerance=analysis.tolerance,
            reference_band_shell=analysis.reference_band_shell,
            comparison_band_shell=analysis.comparison_band_shell,
            reference_hamiltonian_shell=analysis.reference_hamiltonian_shell,
            comparison_hamiltonian_shell=analysis.comparison_hamiltonian_shell,
            reference_band_passing_error=analysis.reference_band_passing_error,
            reference_band_preceding_error=analysis.reference_band_preceding_error,
            comparison_band_passing_error=analysis.comparison_band_passing_error,
            comparison_band_preceding_error=analysis.comparison_band_preceding_error,
            reference_hamiltonian_passing_error=analysis.reference_hamiltonian_passing_error,
            reference_hamiltonian_preceding_error=analysis.reference_hamiltonian_preceding_error,
            comparison_hamiltonian_passing_error=analysis.comparison_hamiltonian_passing_error,
            comparison_hamiltonian_preceding_error=analysis.comparison_hamiltonian_preceding_error,
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "tolerance": self.tolerance,
            "reference_band_shell": self.reference_band_shell,
            "comparison_band_shell": self.comparison_band_shell,
            "reference_hamiltonian_shell": self.reference_hamiltonian_shell,
            "comparison_hamiltonian_shell": self.comparison_hamiltonian_shell,
            "reference_band_passing_error": self.reference_band_passing_error,
            "reference_band_preceding_error": self.reference_band_preceding_error,
            "comparison_band_passing_error": self.comparison_band_passing_error,
            "comparison_band_preceding_error": self.comparison_band_preceding_error,
            "reference_hamiltonian_passing_error": (
                self.reference_hamiltonian_passing_error
            ),
            "reference_hamiltonian_preceding_error": (
                self.reference_hamiltonian_preceding_error
            ),
            "comparison_hamiltonian_passing_error": (
                self.comparison_hamiltonian_passing_error
            ),
            "comparison_hamiltonian_preceding_error": (
                self.comparison_hamiltonian_preceding_error
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "tolerance",
            "reference_band_shell",
            "comparison_band_shell",
            "reference_hamiltonian_shell",
            "comparison_hamiltonian_shell",
            "reference_band_passing_error",
            "reference_band_preceding_error",
            "comparison_band_passing_error",
            "comparison_band_preceding_error",
            "reference_hamiltonian_passing_error",
            "reference_hamiltonian_preceding_error",
            "comparison_hamiltonian_passing_error",
            "comparison_hamiltonian_preceding_error",
        }
        if set(values) != required:
            raise ValueError("FirstPassingDecision fields do not match")
        tolerance = values["tolerance"]
        reference_band_shell = values["reference_band_shell"]
        comparison_band_shell = values["comparison_band_shell"]
        reference_hamiltonian_shell = values["reference_hamiltonian_shell"]
        comparison_hamiltonian_shell = values["comparison_hamiltonian_shell"]
        reference_band_passing_error = values["reference_band_passing_error"]
        reference_band_preceding_error = values["reference_band_preceding_error"]
        comparison_band_passing_error = values["comparison_band_passing_error"]
        comparison_band_preceding_error = values["comparison_band_preceding_error"]
        reference_hamiltonian_passing_error = values[
            "reference_hamiltonian_passing_error"
        ]
        reference_hamiltonian_preceding_error = values[
            "reference_hamiltonian_preceding_error"
        ]
        comparison_hamiltonian_passing_error = values[
            "comparison_hamiltonian_passing_error"
        ]
        comparison_hamiltonian_preceding_error = values[
            "comparison_hamiltonian_preceding_error"
        ]
        if type(tolerance) is not float:
            raise TypeError("float fields must use exact built-in types")
        if (
            (
                reference_band_passing_error is not None
                and type(reference_band_passing_error) is not float
            )
            or (
                reference_band_preceding_error is not None
                and type(reference_band_preceding_error) is not float
            )
            or (
                comparison_band_passing_error is not None
                and type(comparison_band_passing_error) is not float
            )
            or (
                comparison_band_preceding_error is not None
                and type(comparison_band_preceding_error) is not float
            )
            or (
                reference_hamiltonian_passing_error is not None
                and type(reference_hamiltonian_passing_error) is not float
            )
            or (
                reference_hamiltonian_preceding_error is not None
                and type(reference_hamiltonian_preceding_error) is not float
            )
            or (
                comparison_hamiltonian_passing_error is not None
                and type(comparison_hamiltonian_passing_error) is not float
            )
            or (
                comparison_hamiltonian_preceding_error is not None
                and type(comparison_hamiltonian_preceding_error) is not float
            )
        ):
            raise TypeError("optional float fields have invalid types")
        if (
            (reference_band_shell is not None and type(reference_band_shell) is not int)
            or (
                comparison_band_shell is not None
                and type(comparison_band_shell) is not int
            )
            or (
                reference_hamiltonian_shell is not None
                and type(reference_hamiltonian_shell) is not int
            )
            or (
                comparison_hamiltonian_shell is not None
                and type(comparison_hamiltonian_shell) is not int
            )
        ):
            raise TypeError("optional integer fields have invalid types")
        return cls(
            tolerance=tolerance,
            reference_band_shell=reference_band_shell,
            comparison_band_shell=comparison_band_shell,
            reference_hamiltonian_shell=reference_hamiltonian_shell,
            comparison_hamiltonian_shell=comparison_hamiltonian_shell,
            reference_band_passing_error=reference_band_passing_error,
            reference_band_preceding_error=reference_band_preceding_error,
            comparison_band_passing_error=comparison_band_passing_error,
            comparison_band_preceding_error=comparison_band_preceding_error,
            reference_hamiltonian_passing_error=reference_hamiltonian_passing_error,
            reference_hamiltonian_preceding_error=reference_hamiltonian_preceding_error,
            comparison_hamiltonian_passing_error=comparison_hamiltonian_passing_error,
            comparison_hamiltonian_preceding_error=comparison_hamiltonian_preceding_error,
        )
