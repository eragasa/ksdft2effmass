"""Code-driven disposition planning for retained bulk-silicon convergence evidence.

This private, revisable campaign slice validates the retained finite-setting analysis,
selects the smallest two-sided-guarded cutoff, requires the reciprocal-mesh scan to
have been performed at that cutoff, then selects its smallest guarded mesh and emits
a canonical human-decision packet. It performs no calculator execution, setting
selection, warning classification, authority decision, or scientific acceptance.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum
from hashlib import sha256
from typing import cast

from ksdft2effmass.analysis._finite_setting_guards import (
    FiniteSettingComparison,
    FiniteSettingCriteria,
    FiniteSettingGuardAnalyzer,
    FiniteSettingPasses,
    FiniteSettingSeries,
)
from ksdft2effmass.units import (
    MetalQuantityConverter,
    MetalUnitConversionRequest,
    MetalUnitConversionSuccess,
    UnitIdentity,
    UnitScalar,
)
from ksdft2effmass.workflows import ArtifactContentIdentity

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type JsonObject = dict[str, JsonValue]


@dataclass(frozen=True, slots=True)
class BulkSiliconFiniteSettingCriteria:
    """Frozen finite-setting thresholds in the retained analysis units."""

    energy_ry_atom: float
    pressure_and_max_stress_component_kbar: float
    fixed_point_band_and_gap_mev: float

    def __post_init__(self) -> None:
        for value, name in (
            (self.energy_ry_atom, "energy_ry_atom"),
            (
                self.pressure_and_max_stress_component_kbar,
                "pressure_and_max_stress_component_kbar",
            ),
            (self.fixed_point_band_and_gap_mev, "fixed_point_band_and_gap_mev"),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be finite and positive")


@dataclass(frozen=True, slots=True)
class BulkSiliconFiniteSettingPasses:
    """Retained pass/fail findings for all five consequential comparisons."""

    energy: bool
    pressure: bool
    stress: bool
    fixed_point_band_at_printed_precision: bool
    fixed_point_gap_at_printed_precision: bool

    def __post_init__(self) -> None:
        if any(
            type(value) is not bool
            for value in (
                self.energy,
                self.pressure,
                self.stress,
                self.fixed_point_band_at_printed_precision,
                self.fixed_point_gap_at_printed_precision,
            )
        ):
            raise TypeError("finite-setting pass values must be built-in bool values")

    @property
    def all_pass(self) -> bool:
        """Return whether every frozen finite-setting rule passes."""
        return all(
            (
                self.energy,
                self.pressure,
                self.stress,
                self.fixed_point_band_at_printed_precision,
                self.fixed_point_gap_at_printed_precision,
            )
        )


@dataclass(frozen=True, slots=True)
class BulkSiliconFiniteSettingComparison:
    """One adjacent-setting comparison from the retained direct audit."""

    from_label: str
    to_label: str
    energy_change_ry_atom: float
    pressure_change_kbar: float
    maximum_stress_component_change_kbar: float
    maximum_aligned_band_4_5_change_mev: float
    maximum_gap_probe_change_mev: float
    passes: BulkSiliconFiniteSettingPasses

    def __post_init__(self) -> None:
        if type(self.from_label) is not str or type(self.to_label) is not str:
            raise TypeError("comparison labels must be built-in str values")
        if not self.from_label or not self.to_label:
            raise ValueError("comparison labels must not be empty")
        if self.from_label == self.to_label:
            raise ValueError("comparison endpoints must be distinct")
        for value, name in (
            (self.energy_change_ry_atom, "energy_change_ry_atom"),
            (self.pressure_change_kbar, "pressure_change_kbar"),
            (
                self.maximum_stress_component_change_kbar,
                "maximum_stress_component_change_kbar",
            ),
            (
                self.maximum_aligned_band_4_5_change_mev,
                "maximum_aligned_band_4_5_change_mev",
            ),
            (self.maximum_gap_probe_change_mev, "maximum_gap_probe_change_mev"),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        if type(self.passes) is not BulkSiliconFiniteSettingPasses:
            raise TypeError("passes must be BulkSiliconFiniteSettingPasses")


@dataclass(frozen=True, slots=True)
class BulkSiliconFiniteSettingSeries:
    """One contiguous ordered cutoff or reciprocal-mesh comparison series."""

    name: str
    comparisons: tuple[BulkSiliconFiniteSettingComparison, ...]

    def __post_init__(self) -> None:
        if type(self.name) is not str:
            raise TypeError("series name must be a built-in str")
        if self.name not in {"cutoff", "mesh"}:
            raise ValueError("series name must be cutoff or mesh")
        if type(self.comparisons) is not tuple or any(
            type(value) is not BulkSiliconFiniteSettingComparison
            for value in self.comparisons
        ):
            raise TypeError(
                "comparisons must be a tuple of BulkSiliconFiniteSettingComparison"
            )
        if len(self.comparisons) < 2:
            raise ValueError("a guarded series requires at least two comparisons")
        if any(
            left.to_label != right.from_label
            for left, right in zip(
                self.comparisons[:-1], self.comparisons[1:], strict=True
            )
        ):
            raise ValueError("comparison series must form one contiguous chain")

    @property
    def candidate_labels(self) -> tuple[str, ...]:
        """Return the ordered labels implied by the contiguous comparison chain."""
        return (self.comparisons[0].from_label,) + tuple(
            value.to_label for value in self.comparisons
        )


@dataclass(frozen=True, slots=True)
class BulkSiliconFiniteSettingAnalysis:
    """Validated retained direct finite-setting analysis and warning evidence."""

    source_reference: str
    source_content_identity: ArtifactContentIdentity
    record_version: int
    status: str
    provenance_source: str
    criteria: BulkSiliconFiniteSettingCriteria
    cutoff: BulkSiliconFiniteSettingSeries
    mesh: BulkSiliconFiniteSettingSeries
    ieee_warning: str
    excluded_conclusions: tuple[str, ...]

    def __post_init__(self) -> None:
        if type(self.source_reference) is not str or not self.source_reference:
            raise ValueError("source_reference must be a nonempty built-in str")
        if type(self.source_content_identity) is not ArtifactContentIdentity:
            raise TypeError("source_content_identity must be ArtifactContentIdentity")
        if type(self.record_version) is not int:
            raise TypeError("record_version must be a built-in int excluding bool")
        if self.record_version != 1:
            raise ValueError(
                "only retained finite-setting analysis version 1 is supported"
            )
        for value, name in (
            (self.status, "status"),
            (self.provenance_source, "provenance_source"),
            (self.ieee_warning, "ieee_warning"),
        ):
            if type(value) is not str or not value:
                raise ValueError(f"{name} must be a nonempty built-in str")
        if type(self.criteria) is not BulkSiliconFiniteSettingCriteria:
            raise TypeError("criteria must be BulkSiliconFiniteSettingCriteria")
        if type(self.cutoff) is not BulkSiliconFiniteSettingSeries:
            raise TypeError("cutoff must be BulkSiliconFiniteSettingSeries")
        if type(self.mesh) is not BulkSiliconFiniteSettingSeries:
            raise TypeError("mesh must be BulkSiliconFiniteSettingSeries")
        if self.cutoff.name != "cutoff" or self.mesh.name != "mesh":
            raise ValueError("analysis series must retain their declared axes")
        if type(self.excluded_conclusions) is not tuple or any(
            type(value) is not str or not value for value in self.excluded_conclusions
        ):
            raise TypeError("excluded_conclusions must be nonempty strings")
        if not self.excluded_conclusions:
            raise ValueError("excluded_conclusions must not be empty")


class BulkSiliconFiniteSettingAnalysisJsonDecoder:
    """Decode the exact retained version-one finite-setting analysis wire format."""

    __slots__ = ()

    def execute(
        self, source_reference: str, payload: bytes
    ) -> BulkSiliconFiniteSettingAnalysis:
        """Return typed validated evidence from supplied retained bytes."""
        if type(source_reference) is not str or not source_reference:
            raise ValueError("source_reference must be a nonempty built-in str")
        if type(payload) is not bytes:
            raise TypeError("payload must be bytes")
        root = self._mapping(
            cast(JsonValue, json.loads(payload.decode("utf-8"))), "root"
        )
        self._keys(
            root,
            (
                "record_version",
                "status",
                "source",
                "criteria",
                "comparisons",
                "observations",
                "excluded_conclusions",
            ),
            "root",
        )
        criteria_value = self._mapping(root["criteria"], "criteria")
        self._keys(
            criteria_value,
            (
                "energy_ry_atom",
                "pressure_and_max_stress_component_kbar",
                "fixed_point_band_and_gap_mev",
            ),
            "criteria",
        )
        comparisons = self._mapping(root["comparisons"], "comparisons")
        self._keys(comparisons, ("cutoff", "mesh"), "comparisons")
        observations = self._mapping(root["observations"], "observations")
        self._keys(
            observations,
            ("cutoff", "mesh", "selection", "ieee_warning"),
            "observations",
        )
        excluded = self._sequence(root["excluded_conclusions"], "excluded_conclusions")
        digest = sha256(payload).hexdigest()
        return BulkSiliconFiniteSettingAnalysis(
            source_reference=source_reference,
            source_content_identity=ArtifactContentIdentity(
                "sha256", digest, len(payload)
            ),
            record_version=self._integer(root["record_version"], "record_version"),
            status=self._string(root["status"], "status"),
            provenance_source=self._string(root["source"], "source"),
            criteria=BulkSiliconFiniteSettingCriteria(
                self._real(criteria_value["energy_ry_atom"], "energy_ry_atom"),
                self._real(
                    criteria_value["pressure_and_max_stress_component_kbar"],
                    "pressure_and_max_stress_component_kbar",
                ),
                self._real(
                    criteria_value["fixed_point_band_and_gap_mev"],
                    "fixed_point_band_and_gap_mev",
                ),
            ),
            cutoff=BulkSiliconFiniteSettingSeries(
                "cutoff", self._comparisons(comparisons["cutoff"], "cutoff")
            ),
            mesh=BulkSiliconFiniteSettingSeries(
                "mesh", self._comparisons(comparisons["mesh"], "mesh")
            ),
            ieee_warning=self._string(observations["ieee_warning"], "ieee_warning"),
            excluded_conclusions=tuple(
                self._string(value, "excluded_conclusion") for value in excluded
            ),
        )

    def _comparisons(
        self, value: JsonValue, series_name: str
    ) -> tuple[BulkSiliconFiniteSettingComparison, ...]:
        sequence = self._sequence(value, series_name)
        return tuple(
            self._comparison(self._mapping(item, f"{series_name} comparison"))
            for item in sequence
        )

    def _comparison(self, value: JsonObject) -> BulkSiliconFiniteSettingComparison:
        self._keys(
            value,
            (
                "from",
                "to",
                "energy_change_ry_atom",
                "pressure_change_kbar",
                "maximum_stress_component_change_kbar",
                "maximum_aligned_band_4_5_change_mev",
                "maximum_gap_probe_change_mev",
                "criteria",
            ),
            "comparison",
        )
        passes = self._mapping(value["criteria"], "comparison criteria")
        self._keys(
            passes,
            (
                "energy_pass",
                "pressure_pass",
                "stress_pass",
                "fixed_point_band_pass_at_printed_precision",
                "fixed_point_gap_pass_at_printed_precision",
            ),
            "comparison criteria",
        )
        return BulkSiliconFiniteSettingComparison(
            self._string(value["from"], "from"),
            self._string(value["to"], "to"),
            self._real(value["energy_change_ry_atom"], "energy_change_ry_atom"),
            self._real(value["pressure_change_kbar"], "pressure_change_kbar"),
            self._real(
                value["maximum_stress_component_change_kbar"],
                "maximum_stress_component_change_kbar",
            ),
            self._real(
                value["maximum_aligned_band_4_5_change_mev"],
                "maximum_aligned_band_4_5_change_mev",
            ),
            self._real(
                value["maximum_gap_probe_change_mev"],
                "maximum_gap_probe_change_mev",
            ),
            BulkSiliconFiniteSettingPasses(
                self._boolean(passes["energy_pass"], "energy_pass"),
                self._boolean(passes["pressure_pass"], "pressure_pass"),
                self._boolean(passes["stress_pass"], "stress_pass"),
                self._boolean(
                    passes["fixed_point_band_pass_at_printed_precision"],
                    "fixed_point_band_pass_at_printed_precision",
                ),
                self._boolean(
                    passes["fixed_point_gap_pass_at_printed_precision"],
                    "fixed_point_gap_pass_at_printed_precision",
                ),
            ),
        )

    @staticmethod
    def _mapping(value: JsonValue, name: str) -> JsonObject:
        if not isinstance(value, dict) or any(type(key) is not str for key in value):
            raise TypeError(f"{name} must be a JSON object")
        return value

    @staticmethod
    def _sequence(value: JsonValue, name: str) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return value

    @staticmethod
    def _keys(value: JsonObject, expected: tuple[str, ...], name: str) -> None:
        if set(value) != set(expected):
            raise ValueError(f"{name} must contain exactly {expected}")

    @staticmethod
    def _string(value: JsonValue, name: str) -> str:
        if type(value) is not str:
            raise TypeError(f"{name} must be a JSON string")
        if not value:
            raise ValueError(f"{name} must not be empty")
        return value

    @staticmethod
    def _integer(value: JsonValue, name: str) -> int:
        if type(value) is not int:
            raise TypeError(f"{name} must be a JSON integer excluding bool")
        return value

    @staticmethod
    def _real(value: JsonValue, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be a JSON real excluding bool")
        result = float(value)
        if not math.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    @staticmethod
    def _boolean(value: JsonValue, name: str) -> bool:
        if type(value) is not bool:
            raise TypeError(f"{name} must be a JSON boolean")
        return value


class BulkSiliconWarningDisposition(StrEnum):
    """Human-owned warning dispositions offered by the generated packet."""

    BLOCK_PENDING_DIAGNOSIS = "block_pending_diagnosis"
    RETAIN_UNRESOLVED_WITH_DOWNSTREAM_EXECUTION_GATED = (
        "retain_unresolved_with_downstream_execution_gated"
    )


@dataclass(frozen=True, slots=True)
class BulkSiliconConvergenceSetting:
    """One canonical metal-unit cutoff and shifted reciprocal-mesh setting."""

    wavefunction_cutoff: UnitScalar
    mesh_axis_count: int

    def __post_init__(self) -> None:
        if type(self.wavefunction_cutoff) is not UnitScalar:
            raise TypeError("wavefunction_cutoff must be UnitScalar")
        if self.wavefunction_cutoff.unit is not UnitIdentity.ELECTRON_VOLT:
            raise ValueError("wavefunction_cutoff must use canonical electron volts")
        if self.wavefunction_cutoff.value <= 0.0:
            raise ValueError("wavefunction_cutoff must be positive")
        if type(self.mesh_axis_count) is not int:
            raise TypeError("mesh_axis_count must be a built-in int excluding bool")
        if self.mesh_axis_count <= 0:
            raise ValueError("mesh_axis_count must be positive")

    @property
    def charge_density_cutoff(self) -> UnitScalar:
        """Return the frozen four-times cutoff in canonical metal units."""
        return UnitScalar(
            4.0 * self.wavefunction_cutoff.value, UnitIdentity.ELECTRON_VOLT
        )


@dataclass(frozen=True, slots=True)
class BulkSiliconSequentialScanConfiguration:
    """Inclusive integer ranges for the ordered cutoff and k-point scans."""

    encut_min: UnitScalar
    encut_max: UnitScalar
    d_encut: UnitScalar
    kpoints_min: int
    kpoints_max: int
    d_kpoints: int

    def __post_init__(self) -> None:
        for cutoff_value, name in (
            (self.encut_min, "encut_min"),
            (self.encut_max, "encut_max"),
            (self.d_encut, "d_encut"),
        ):
            if type(cutoff_value) is not UnitScalar:
                raise TypeError(f"{name} must be UnitScalar")
            if cutoff_value.unit is not UnitIdentity.ELECTRON_VOLT:
                raise ValueError(f"{name} must use canonical electron volts")
            if cutoff_value.value <= 0.0:
                raise ValueError(f"{name} must be positive")
        for kpoint_value, name in (
            (self.kpoints_min, "kpoints_min"),
            (self.kpoints_max, "kpoints_max"),
            (self.d_kpoints, "d_kpoints"),
        ):
            if type(kpoint_value) is not int:
                raise TypeError(f"{name} must be a built-in int excluding bool")
            if kpoint_value <= 0:
                raise ValueError(f"{name} must be positive")
        if self.encut_min.value >= self.encut_max.value:
            raise ValueError("encut_min must be less than encut_max")
        if self.kpoints_min >= self.kpoints_max:
            raise ValueError("kpoints_min must be less than kpoints_max")
        encut_steps = (self.encut_max.value - self.encut_min.value) / self.d_encut.value
        if not math.isclose(
            encut_steps, round(encut_steps), rel_tol=0.0, abs_tol=1e-12
        ):
            raise ValueError("ENCUT range must end exactly at encut_max")
        if (self.kpoints_max - self.kpoints_min) % self.d_kpoints != 0:
            raise ValueError("k-point range must end exactly at kpoints_max")

    @property
    def encut_candidates(self) -> tuple[UnitScalar, ...]:
        """Return the inclusive canonical-metal-unit ENCUT sequence."""
        count = round(
            (self.encut_max.value - self.encut_min.value) / self.d_encut.value
        )
        minimum = Decimal(str(self.encut_min.value))
        step = Decimal(str(self.d_encut.value))
        return tuple(
            self.encut_max
            if index == count
            else UnitScalar(
                float(minimum + Decimal(index) * step),
                UnitIdentity.ELECTRON_VOLT,
            )
            for index in range(count + 1)
        )

    @property
    def kpoint_candidates(self) -> tuple[int, ...]:
        """Return the inclusive per-axis k-point candidate sequence."""
        return tuple(range(self.kpoints_min, self.kpoints_max + 1, self.d_kpoints))


BULK_SILICON_SEQUENTIAL_SCAN_CONFIGURATION = BulkSiliconSequentialScanConfiguration(
    encut_min=UnitScalar(408.170793689715, UnitIdentity.ELECTRON_VOLT),
    encut_max=UnitScalar(816.34158737943, UnitIdentity.ELECTRON_VOLT),
    d_encut=UnitScalar(81.634158737943, UnitIdentity.ELECTRON_VOLT),
    kpoints_min=6,
    kpoints_max=12,
    d_kpoints=2,
)


@dataclass(frozen=True, slots=True)
class BulkSiliconSequentialConvergencePlan:
    """Cutoff-first then conditional reciprocal-mesh scan recommendation."""

    cutoff_candidates: tuple[UnitScalar, ...]
    cutoff_eligible: tuple[UnitScalar, ...]
    recommended_cutoff: UnitScalar
    cutoff_lower_guard: UnitScalar
    cutoff_upper_guard: UnitScalar
    mesh_scan_cutoff: UnitScalar
    mesh_candidates: tuple[int, ...]
    mesh_eligible: tuple[int, ...]
    recommended_mesh: int
    mesh_lower_guard: int
    mesh_upper_guard: int

    def __post_init__(self) -> None:
        for cutoff_values, name in (
            (self.cutoff_candidates, "cutoff_candidates"),
            (self.cutoff_eligible, "cutoff_eligible"),
        ):
            if type(cutoff_values) is not tuple or any(
                type(value) is not UnitScalar for value in cutoff_values
            ):
                raise TypeError(f"{name} must be a tuple of UnitScalar values")
            if not cutoff_values or any(
                value.unit is not UnitIdentity.ELECTRON_VOLT for value in cutoff_values
            ):
                raise ValueError(f"{name} must use canonical electron volts")
            magnitudes = tuple(value.value for value in cutoff_values)
            if tuple(sorted(set(magnitudes))) != magnitudes:
                raise ValueError(f"{name} must be nonempty, unique, and increasing")
        for mesh_values, name in (
            (self.mesh_candidates, "mesh_candidates"),
            (self.mesh_eligible, "mesh_eligible"),
        ):
            if type(mesh_values) is not tuple or any(
                type(value) is not int for value in mesh_values
            ):
                raise TypeError(f"{name} must be a tuple of built-in int values")
            if not mesh_values or tuple(sorted(set(mesh_values))) != mesh_values:
                raise ValueError(f"{name} must be nonempty, unique, and increasing")
        for cutoff_value, name in (
            (self.recommended_cutoff, "recommended_cutoff"),
            (self.cutoff_lower_guard, "cutoff_lower_guard"),
            (self.cutoff_upper_guard, "cutoff_upper_guard"),
            (self.mesh_scan_cutoff, "mesh_scan_cutoff"),
        ):
            if type(cutoff_value) is not UnitScalar:
                raise TypeError(f"{name} must be UnitScalar")
            if cutoff_value.unit is not UnitIdentity.ELECTRON_VOLT:
                raise ValueError(f"{name} must use canonical electron volts")
        for mesh_value, name in (
            (self.recommended_mesh, "recommended_mesh"),
            (self.mesh_lower_guard, "mesh_lower_guard"),
            (self.mesh_upper_guard, "mesh_upper_guard"),
        ):
            if type(mesh_value) is not int:
                raise TypeError(f"{name} must be a built-in int")
        if self.recommended_cutoff != self.cutoff_eligible[0]:
            raise ValueError("recommended cutoff must be the smallest guarded cutoff")
        if self.mesh_scan_cutoff != self.recommended_cutoff:
            raise ValueError("mesh scan must be evaluated at the recommended cutoff")
        if self.recommended_mesh != self.mesh_eligible[0]:
            raise ValueError("recommended mesh must be the smallest guarded mesh")
        if not (
            self.cutoff_lower_guard.value
            < self.recommended_cutoff.value
            < self.cutoff_upper_guard.value
        ):
            raise ValueError("cutoff guards must bracket the recommendation")
        if not self.mesh_lower_guard < self.recommended_mesh < self.mesh_upper_guard:
            raise ValueError("mesh guards must bracket the recommendation")

    @property
    def recommended_setting(self) -> BulkSiliconConvergenceSetting:
        """Return the final sequential recommendation."""
        return BulkSiliconConvergenceSetting(
            self.recommended_cutoff, self.recommended_mesh
        )


@dataclass(frozen=True, slots=True)
class BulkSiliconConvergenceDispositionPacket:
    """Deterministic recommendation and unresolved human decision dimensions."""

    analysis: BulkSiliconFiniteSettingAnalysis
    plan: BulkSiliconSequentialConvergencePlan
    warning_dispositions: tuple[BulkSiliconWarningDisposition, ...]

    def __post_init__(self) -> None:
        if type(self.analysis) is not BulkSiliconFiniteSettingAnalysis:
            raise TypeError("analysis must be BulkSiliconFiniteSettingAnalysis")
        if type(self.plan) is not BulkSiliconSequentialConvergencePlan:
            raise TypeError("plan must be BulkSiliconSequentialConvergencePlan")
        if type(self.warning_dispositions) is not tuple or any(
            type(value) is not BulkSiliconWarningDisposition
            for value in self.warning_dispositions
        ):
            raise TypeError("warning_dispositions must contain closed enum values")
        if set(self.warning_dispositions) != set(BulkSiliconWarningDisposition):
            raise ValueError("warning dispositions must expose the complete closed set")


@dataclass(frozen=True, slots=True)
class BulkSiliconFiniteSettingCanonicalizer:
    """Convert retained Quantum ESPRESSO quantities to canonical metal units."""

    def energy_rydberg_to_electron_volt(self, value: float) -> float:
        """Convert one Quantum ESPRESSO energy at the retained-input boundary."""
        result = MetalQuantityConverter().convert(
            MetalUnitConversionRequest(
                UnitScalar(value, UnitIdentity.RYDBERG),
                UnitIdentity.ELECTRON_VOLT,
            )
        )
        if type(result) is not MetalUnitConversionSuccess:
            raise ValueError("retained Rydberg value must convert to electron volts")
        return result.output.value

    def pressure_kilobar_to_bar(self, value: float) -> float:
        """Convert one Quantum ESPRESSO pressure at the retained-input boundary."""
        return value * 1000.0

    def energy_millielectron_volt_to_electron_volt(self, value: float) -> float:
        """Convert one diagnostic energy at the retained-input boundary."""
        return value * 0.001


@dataclass(frozen=True, slots=True)
class BulkSiliconConvergenceDispositionPlanner:
    """Compose the configured cutoff-first, conditional-mesh recommendation."""

    configuration: BulkSiliconSequentialScanConfiguration

    def __post_init__(self) -> None:
        if type(self.configuration) is not BulkSiliconSequentialScanConfiguration:
            raise TypeError(
                "configuration must be BulkSiliconSequentialScanConfiguration"
            )

    def execute(
        self, analysis: BulkSiliconFiniteSettingAnalysis
    ) -> BulkSiliconConvergenceDispositionPacket:
        """Return the deterministic decision packet for validated retained evidence."""
        if type(analysis) is not BulkSiliconFiniteSettingAnalysis:
            raise TypeError("analysis must be BulkSiliconFiniteSettingAnalysis")
        cutoff_labels = analysis.cutoff.candidate_labels
        mesh_labels = analysis.mesh.candidate_labels
        cutoff_order = self.configuration.encut_candidates
        mesh_order = self.configuration.kpoint_candidates
        expected_cutoff_labels = ("C30", "C36", "C42", "C48", "C54", "C60")
        if cutoff_labels != expected_cutoff_labels or len(cutoff_labels) != len(
            cutoff_order
        ):
            raise ValueError(
                "retained cutoff chain does not match configured ENCUT range"
            )
        if len(mesh_labels) != len(mesh_order):
            raise ValueError(
                "retained mesh chain does not match configured k-point range"
            )
        canonicalizer = BulkSiliconFiniteSettingCanonicalizer()
        criteria = FiniteSettingCriteria(
            canonicalizer.energy_rydberg_to_electron_volt(
                analysis.criteria.energy_ry_atom
            ),
            canonicalizer.pressure_kilobar_to_bar(
                analysis.criteria.pressure_and_max_stress_component_kbar
            ),
            canonicalizer.energy_millielectron_volt_to_electron_volt(
                analysis.criteria.fixed_point_band_and_gap_mev
            ),
        )
        analyzer = FiniteSettingGuardAnalyzer(arithmetic_allowance=1e-9)
        cutoff_guard_analysis = analyzer.execute(
            criteria, self._analysis_series(analysis.cutoff)
        )
        mesh_guard_analysis = analyzer.execute(
            criteria, self._analysis_series(analysis.mesh)
        )
        cutoff_values = dict(zip(cutoff_labels, cutoff_order, strict=True))
        mesh_values = dict(zip(mesh_labels, mesh_order, strict=True))
        eligible_cutoffs = tuple(
            cutoff_values[label] for label in cutoff_guard_analysis.guarded_labels
        )
        eligible_meshes = tuple(
            mesh_values[label] for label in mesh_guard_analysis.guarded_labels
        )
        recommended_cutoff = eligible_cutoffs[0]
        recommended_mesh = eligible_meshes[0]
        expected_mesh_labels = ("K6", "C48", "K10", "K12")
        if mesh_labels != expected_mesh_labels:
            raise ValueError(
                "retained mesh chain is not the configured scan at recommended ENCUT"
            )
        cutoff_index = cutoff_order.index(recommended_cutoff)
        mesh_index = mesh_order.index(recommended_mesh)
        mesh_scan_cutoff = recommended_cutoff
        plan = BulkSiliconSequentialConvergencePlan(
            cutoff_candidates=cutoff_order,
            cutoff_eligible=eligible_cutoffs,
            recommended_cutoff=recommended_cutoff,
            cutoff_lower_guard=cutoff_order[cutoff_index - 1],
            cutoff_upper_guard=cutoff_order[cutoff_index + 1],
            mesh_scan_cutoff=mesh_scan_cutoff,
            mesh_candidates=mesh_order,
            mesh_eligible=eligible_meshes,
            recommended_mesh=recommended_mesh,
            mesh_lower_guard=mesh_order[mesh_index - 1],
            mesh_upper_guard=mesh_order[mesh_index + 1],
        )
        return BulkSiliconConvergenceDispositionPacket(
            analysis=analysis,
            plan=plan,
            warning_dispositions=tuple(BulkSiliconWarningDisposition),
        )

    @staticmethod
    def _analysis_series(value: BulkSiliconFiniteSettingSeries) -> FiniteSettingSeries:
        """Adapt material-specific retained fields to generic analysis records."""
        canonicalizer = BulkSiliconFiniteSettingCanonicalizer()
        return FiniteSettingSeries(
            value.name,
            tuple(
                FiniteSettingComparison(
                    comparison.from_label,
                    comparison.to_label,
                    canonicalizer.energy_rydberg_to_electron_volt(
                        comparison.energy_change_ry_atom
                    ),
                    canonicalizer.pressure_kilobar_to_bar(
                        comparison.pressure_change_kbar
                    ),
                    canonicalizer.pressure_kilobar_to_bar(
                        comparison.maximum_stress_component_change_kbar
                    ),
                    canonicalizer.energy_millielectron_volt_to_electron_volt(
                        comparison.maximum_aligned_band_4_5_change_mev
                    ),
                    canonicalizer.energy_millielectron_volt_to_electron_volt(
                        comparison.maximum_gap_probe_change_mev
                    ),
                    FiniteSettingPasses(
                        comparison.passes.energy,
                        comparison.passes.pressure,
                        comparison.passes.stress,
                        comparison.passes.fixed_point_band_at_printed_precision,
                        comparison.passes.fixed_point_gap_at_printed_precision,
                    ),
                )
                for comparison in value.comparisons
            ),
        )


@dataclass(frozen=True, slots=True)
class BulkSiliconConvergenceDispositionJsonSerializer:
    """Serialize one decision packet to canonical UTF-8 JSON bytes."""

    def execute(self, packet: BulkSiliconConvergenceDispositionPacket) -> bytes:
        """Return stable JSON without implying a human selection or authority."""
        if type(packet) is not BulkSiliconConvergenceDispositionPacket:
            raise TypeError("packet must be BulkSiliconConvergenceDispositionPacket")
        analysis = packet.analysis
        canonicalizer = BulkSiliconFiniteSettingCanonicalizer()
        claim_limits: list[JsonValue] = [
            *analysis.excluded_conclusions,
            ("two-sided finite-setting guards do not bound an infinite-setting limit"),
            "sequential one-variable scans do not bound cutoff-mesh interaction",
            "a warning disposition does not classify the IEEE report as harmless",
            "this packet grants no calculator execution authority",
        ]
        payload: JsonObject = {
            "record_version": 3,
            "status": "awaiting_human_disposition",
            "generated_by": ("BulkSiliconConvergenceDispositionPlanner.v3"),
            "unit_system": "lammps_metal",
            "source": {
                "path": analysis.source_reference,
                "unit_system": "quantum_espresso_native",
                "sha256": analysis.source_content_identity.digest,
                "byte_count": analysis.source_content_identity.byte_count,
            },
            "scan_configuration": {
                "encut_min": self._unit_scalar(packet.plan.cutoff_candidates[0]),
                "encut_max": self._unit_scalar(packet.plan.cutoff_candidates[-1]),
                "d_encut": self._unit_scalar(
                    UnitScalar(
                        packet.plan.cutoff_candidates[1].value
                        - packet.plan.cutoff_candidates[0].value,
                        UnitIdentity.ELECTRON_VOLT,
                    )
                ),
                "kpoints_min": packet.plan.mesh_candidates[0],
                "kpoints_max": packet.plan.mesh_candidates[-1],
                "d_kpoints": (
                    packet.plan.mesh_candidates[1] - packet.plan.mesh_candidates[0]
                ),
            },
            "criteria": {
                "energy_electron_volt_per_atom": (
                    canonicalizer.energy_rydberg_to_electron_volt(
                        analysis.criteria.energy_ry_atom
                    )
                ),
                "pressure_and_max_stress_component_bar": (
                    canonicalizer.pressure_kilobar_to_bar(
                        analysis.criteria.pressure_and_max_stress_component_kbar
                    )
                ),
                "fixed_point_band_and_gap_electron_volt": (
                    canonicalizer.energy_millielectron_volt_to_electron_volt(
                        analysis.criteria.fixed_point_band_and_gap_mev
                    )
                ),
            },
            "comparisons": {
                "cutoff": [
                    self._comparison(value) for value in analysis.cutoff.comparisons
                ],
                "mesh": [
                    self._comparison(value) for value in analysis.mesh.comparisons
                ],
            },
            "process": {
                "order": ["encut_scan", "kpoints_scan_at_selected_encut"],
                "encut_scan": {
                    "fixed_shifted_mesh": [8, 8, 8],
                    "candidate_wavefunction_cutoffs": [
                        self._unit_scalar(value)
                        for value in packet.plan.cutoff_candidates
                    ],
                    "eligible_wavefunction_cutoffs": [
                        self._unit_scalar(value)
                        for value in packet.plan.cutoff_eligible
                    ],
                    "recommended_wavefunction_cutoff": self._unit_scalar(
                        packet.plan.recommended_cutoff
                    ),
                    "recommended_charge_density_cutoff": self._unit_scalar(
                        UnitScalar(
                            4.0 * packet.plan.recommended_cutoff.value,
                            UnitIdentity.ELECTRON_VOLT,
                        )
                    ),
                    "lower_guard_wavefunction_cutoff": self._unit_scalar(
                        packet.plan.cutoff_lower_guard
                    ),
                    "upper_guard_wavefunction_cutoff": self._unit_scalar(
                        packet.plan.cutoff_upper_guard
                    ),
                },
                "kpoints_scan_at_selected_encut": {
                    "fixed_wavefunction_cutoff": self._unit_scalar(
                        packet.plan.mesh_scan_cutoff
                    ),
                    "fixed_charge_density_cutoff": self._unit_scalar(
                        UnitScalar(
                            4.0 * packet.plan.mesh_scan_cutoff.value,
                            UnitIdentity.ELECTRON_VOLT,
                        )
                    ),
                    "encut_dependency_satisfied": True,
                    "candidate_shifted_mesh_axis_counts": list(
                        packet.plan.mesh_candidates
                    ),
                    "eligible_shifted_mesh_axis_counts": list(
                        packet.plan.mesh_eligible
                    ),
                    "recommended_shifted_mesh_axis_count": (
                        packet.plan.recommended_mesh
                    ),
                    "lower_guard_shifted_mesh_axis_count": (
                        packet.plan.mesh_lower_guard
                    ),
                    "upper_guard_shifted_mesh_axis_count": (
                        packet.plan.mesh_upper_guard
                    ),
                },
            },
            "recommendation": {
                "status": "proposed_not_selected",
                "setting": self._setting(packet.plan.recommended_setting),
                "basis": (
                    "first select the smallest two-sided-guarded wavefunction "
                    "cutoff, then select the smallest two-sided-guarded shifted "
                    "mesh from the scan performed at that cutoff"
                ),
            },
            "setting_disposition_options": [
                "accept_sequential_recommendation",
                "reject_and_require_revised_scan",
            ],
            "backend_translation": {
                "owner": "ksdft2effmass.integration.quantum_espresso",
                "source_units": "canonical_metal_units",
                "target_units": "quantum_espresso_native_units",
                "status": "required_at_backend_compilation_not_performed_here",
            },
            "warning": {
                "observed_status": analysis.ieee_warning,
                "human_disposition_options": [
                    value.value for value in packet.warning_dispositions
                ],
                "selected": None,
            },
            "setting_selected": None,
            "downstream_eligibility": (
                "blocked_pending_human_setting_and_warning_disposition"
            ),
            "protected_execution_authorized": False,
            "claim_limits": claim_limits,
        }
        return (
            json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n"
        ).encode("utf-8")

    @staticmethod
    def _comparison(value: BulkSiliconFiniteSettingComparison) -> JsonValue:
        canonicalizer = BulkSiliconFiniteSettingCanonicalizer()
        return {
            "from": value.from_label,
            "to": value.to_label,
            "energy_change_electron_volt_per_atom": (
                canonicalizer.energy_rydberg_to_electron_volt(
                    value.energy_change_ry_atom
                )
            ),
            "pressure_change_bar": canonicalizer.pressure_kilobar_to_bar(
                value.pressure_change_kbar
            ),
            "maximum_stress_component_change_bar": (
                canonicalizer.pressure_kilobar_to_bar(
                    value.maximum_stress_component_change_kbar
                )
            ),
            "maximum_aligned_band_4_5_change_electron_volt": (
                canonicalizer.energy_millielectron_volt_to_electron_volt(
                    value.maximum_aligned_band_4_5_change_mev
                )
            ),
            "maximum_gap_probe_change_electron_volt": (
                canonicalizer.energy_millielectron_volt_to_electron_volt(
                    value.maximum_gap_probe_change_mev
                )
            ),
            "all_criteria_pass": value.passes.all_pass,
        }

    @classmethod
    def _setting(cls, value: BulkSiliconConvergenceSetting) -> JsonValue:
        return {
            "wavefunction_cutoff": cls._unit_scalar(value.wavefunction_cutoff),
            "charge_density_cutoff": cls._unit_scalar(value.charge_density_cutoff),
            "shifted_mesh": [
                value.mesh_axis_count,
                value.mesh_axis_count,
                value.mesh_axis_count,
            ],
        }

    @staticmethod
    def _unit_scalar(value: UnitScalar) -> JsonValue:
        return {"value": value.value, "unit": value.unit.value}
