"""Private fail-closed comparison of normalized band observations.

Comparison policy belongs to this analysis ActionObject rather than to the
independently valid periodic observations.  Results establish software behavior
only, not physical equivalence or scientific validation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum

from ._band_observations import BandEnergyUnit, BandStructureObservation


@dataclass(frozen=True, slots=True)
class BandComparisonSpecification:
    """Explicit alignment and tolerance policy for two band observations."""

    required_system_identity: str
    required_path_topology: tuple[str, ...]
    required_band_count: int
    required_energy_unit: BandEnergyUnit
    required_comparison_grid_identity: str
    required_pseudopotential_alignment_identity: str
    required_energy_alignment_identity: str
    lattice_parameter_absolute_tolerance_bohr: float
    wavefunction_cutoff_absolute_tolerance_hartree: float
    eigenvalue_absolute_tolerance_hartree: float

    def __post_init__(self) -> None:
        """Validate explicit comparison policy without applying it."""
        self._require_string(self.required_system_identity, "required_system_identity")
        if type(self.required_path_topology) is not tuple or any(
            type(item) is not str for item in self.required_path_topology
        ):
            raise TypeError("required_path_topology must be a tuple of strings")
        if not self.required_path_topology or any(
            not item for item in self.required_path_topology
        ):
            raise ValueError("required_path_topology must contain nonempty strings")
        if type(self.required_band_count) is not int:
            raise TypeError("required_band_count must be an integer")
        if self.required_band_count <= 0:
            raise ValueError("required_band_count must be positive")
        if not isinstance(self.required_energy_unit, BandEnergyUnit):
            raise TypeError("required_energy_unit must be BandEnergyUnit")
        if self.required_energy_unit is not BandEnergyUnit.HARTREE:
            raise ValueError("the internal comparison slice requires hartree")
        self._require_string(
            self.required_comparison_grid_identity,
            "required_comparison_grid_identity",
        )
        self._require_string(
            self.required_pseudopotential_alignment_identity,
            "required_pseudopotential_alignment_identity",
        )
        self._require_string(
            self.required_energy_alignment_identity,
            "required_energy_alignment_identity",
        )
        self._require_tolerance(
            self.lattice_parameter_absolute_tolerance_bohr,
            "lattice_parameter_absolute_tolerance_bohr",
        )
        self._require_tolerance(
            self.wavefunction_cutoff_absolute_tolerance_hartree,
            "wavefunction_cutoff_absolute_tolerance_hartree",
        )
        self._require_tolerance(
            self.eigenvalue_absolute_tolerance_hartree,
            "eigenvalue_absolute_tolerance_hartree",
        )

    @staticmethod
    def _require_string(value: str, name: str) -> None:
        """Validate one intrinsic nonempty policy identity."""
        if type(value) is not str:
            raise TypeError(f"{name} must be a string")
        if not value:
            raise ValueError(f"{name} must not be empty")

    @staticmethod
    def _require_tolerance(value: float, name: str) -> None:
        """Validate one intrinsic nonnegative finite tolerance."""
        if type(value) is not float:
            raise TypeError(f"{name} must be a float")
        if not math.isfinite(value):
            raise ValueError(f"{name} must be finite")
        if value < 0.0:
            raise ValueError(f"{name} must be nonnegative")


class BandStructureComparisonOutcome(StrEnum):
    """Closed fail-closed numerical comparison outcome."""

    COMPARED = "compared"
    REJECTED = "rejected"


class BandStructureComparisonIssueCode(StrEnum):
    """Closed incompatibility reasons for the initial comparison slice."""

    SYSTEM_MISMATCH = "system_mismatch"
    WORKFLOW_TOPOLOGY_MISMATCH = "workflow_topology_mismatch"
    PATH_TOPOLOGY_MISMATCH = "path_topology_mismatch"
    BAND_COUNT_MISMATCH = "band_count_mismatch"
    POINT_COUNT_MISMATCH = "point_count_mismatch"
    COORDINATE_CONVENTION_MISMATCH = "coordinate_convention_mismatch"
    COMPARISON_GRID_MISMATCH = "comparison_grid_mismatch"
    LATTICE_PARAMETER_MISMATCH = "lattice_parameter_mismatch"
    WAVEFUNCTION_CUTOFF_MISMATCH = "wavefunction_cutoff_mismatch"
    PSEUDOPOTENTIAL_ALIGNMENT_MISSING = "pseudopotential_alignment_missing"
    ENERGY_UNIT_MISMATCH = "energy_unit_mismatch"
    ENERGY_ALIGNMENT_MISSING = "energy_alignment_missing"
    COMPLETE_SPECTRUM_UNAVAILABLE = "complete_spectrum_unavailable"


@dataclass(frozen=True, slots=True)
class BandStructureComparisonIssue:
    """One structured reason that numerical comparison was rejected."""

    code: BandStructureComparisonIssueCode
    diagnostic: str

    def __post_init__(self) -> None:
        """Validate exact issue state."""
        if not isinstance(self.code, BandStructureComparisonIssueCode):
            raise TypeError("code must be BandStructureComparisonIssueCode")
        if type(self.diagnostic) is not str:
            raise TypeError("diagnostic must be a string")
        if not self.diagnostic:
            raise ValueError("diagnostic must not be empty")


@dataclass(frozen=True, slots=True)
class BandStructureComparisonResult:
    """Structured comparison or fail-closed incompatibility report."""

    outcome: BandStructureComparisonOutcome
    workflow_structure_compatible: bool
    issues: tuple[BandStructureComparisonIssue, ...]
    maximum_absolute_difference_hartree: float | None
    within_eigenvalue_tolerance: bool | None

    def __post_init__(self) -> None:
        """Enforce exact compared or rejected result variants."""
        if not isinstance(self.outcome, BandStructureComparisonOutcome):
            raise TypeError("outcome must be BandStructureComparisonOutcome")
        if type(self.workflow_structure_compatible) is not bool:
            raise TypeError("workflow_structure_compatible must be a bool")
        if type(self.issues) is not tuple or any(
            type(item) is not BandStructureComparisonIssue for item in self.issues
        ):
            raise TypeError("issues must be a tuple of BandStructureComparisonIssue")
        if self.maximum_absolute_difference_hartree is not None:
            maximum = self.maximum_absolute_difference_hartree
            if type(maximum) is not float:
                raise TypeError("maximum_absolute_difference_hartree must be a float")
            if not math.isfinite(maximum):
                raise ValueError("maximum_absolute_difference_hartree must be finite")
            if maximum < 0.0:
                raise ValueError(
                    "maximum_absolute_difference_hartree must be nonnegative"
                )
        if self.within_eigenvalue_tolerance is not None and (
            type(self.within_eigenvalue_tolerance) is not bool
        ):
            raise TypeError("within_eigenvalue_tolerance must be a bool or None")
        compared = (
            self.outcome is BandStructureComparisonOutcome.COMPARED
            and self.workflow_structure_compatible
            and not self.issues
            and self.maximum_absolute_difference_hartree is not None
            and self.within_eigenvalue_tolerance is not None
        )
        rejected = (
            self.outcome is BandStructureComparisonOutcome.REJECTED
            and bool(self.issues)
            and self.maximum_absolute_difference_hartree is None
            and self.within_eigenvalue_tolerance is None
        )
        if not (compared or rejected):
            raise ValueError("comparison fields do not match the outcome")


class BandStructureComparator:
    """ActionObject applying one explicit fail-closed comparison specification."""

    def execute(
        self,
        left: BandStructureObservation,
        right: BandStructureObservation,
        specification: BandComparisonSpecification,
    ) -> BandStructureComparisonResult:
        """Compare aligned complete spectra or return structured rejection."""
        if type(left) is not BandStructureObservation:
            raise TypeError("left must be BandStructureObservation")
        if type(right) is not BandStructureObservation:
            raise TypeError("right must be BandStructureObservation")
        if type(specification) is not BandComparisonSpecification:
            raise TypeError("specification must be BandComparisonSpecification")

        structure_compatible = self._workflow_structure_compatible(
            left, right, specification
        )
        issues = self._issues(left, right, specification)
        if issues:
            return BandStructureComparisonResult(
                BandStructureComparisonOutcome.REJECTED,
                structure_compatible,
                issues,
                None,
                None,
            )
        assert left.eigenvalues is not None
        assert right.eigenvalues is not None
        maximum = max(
            abs(left_value - right_value)
            for left_row, right_row in zip(
                left.eigenvalues, right.eigenvalues, strict=True
            )
            for left_value, right_value in zip(left_row, right_row, strict=True)
        )
        return BandStructureComparisonResult(
            BandStructureComparisonOutcome.COMPARED,
            structure_compatible,
            (),
            maximum,
            maximum <= specification.eigenvalue_absolute_tolerance_hartree,
        )

    @staticmethod
    def _workflow_structure_compatible(
        left: BandStructureObservation,
        right: BandStructureObservation,
        specification: BandComparisonSpecification,
    ) -> bool:
        """Return compatibility of shared system and logical workflow shape only."""
        return (
            left.system_identity
            == right.system_identity
            == specification.required_system_identity
            and left.scf_to_fixed_density_bands
            and right.scf_to_fixed_density_bands
            and left.path_topology
            == right.path_topology
            == specification.required_path_topology
            and left.band_count == right.band_count == specification.required_band_count
        )

    @staticmethod
    def _issues(
        left: BandStructureObservation,
        right: BandStructureObservation,
        specification: BandComparisonSpecification,
    ) -> tuple[BandStructureComparisonIssue, ...]:
        """Return deterministic alignment and completeness findings."""
        findings: list[BandStructureComparisonIssue] = []

        def add(code: BandStructureComparisonIssueCode, diagnostic: str) -> None:
            findings.append(BandStructureComparisonIssue(code, diagnostic))

        if not (
            left.system_identity
            == right.system_identity
            == specification.required_system_identity
        ):
            add(
                BandStructureComparisonIssueCode.SYSTEM_MISMATCH,
                "observations do not share the specification's system identity",
            )
        if not (left.scf_to_fixed_density_bands and right.scf_to_fixed_density_bands):
            add(
                BandStructureComparisonIssueCode.WORKFLOW_TOPOLOGY_MISMATCH,
                "both observations must represent SCF to fixed-density bands",
            )
        if not (
            left.path_topology
            == right.path_topology
            == specification.required_path_topology
        ):
            add(
                BandStructureComparisonIssueCode.PATH_TOPOLOGY_MISMATCH,
                "observations do not share the required path topology",
            )
        if not (
            left.band_count == right.band_count == specification.required_band_count
        ):
            add(
                BandStructureComparisonIssueCode.BAND_COUNT_MISMATCH,
                "observations do not share the required band count",
            )
        if left.point_count != right.point_count:
            add(
                BandStructureComparisonIssueCode.POINT_COUNT_MISMATCH,
                "normalized spectra contain different point counts",
            )
        if left.coordinate_convention != right.coordinate_convention:
            add(
                BandStructureComparisonIssueCode.COORDINATE_CONVENTION_MISMATCH,
                "source coordinate conventions differ before common-grid normalization",
            )
        if not (
            left.comparison_grid_identity
            == right.comparison_grid_identity
            == specification.required_comparison_grid_identity
        ):
            add(
                BandStructureComparisonIssueCode.COMPARISON_GRID_MISMATCH,
                "no common specification-identified comparison grid is present",
            )
        if (
            abs(left.lattice_parameter_bohr - right.lattice_parameter_bohr)
            > specification.lattice_parameter_absolute_tolerance_bohr
        ):
            add(
                BandStructureComparisonIssueCode.LATTICE_PARAMETER_MISMATCH,
                "lattice parameters exceed the specification tolerance",
            )
        if (
            abs(left.wavefunction_cutoff_hartree - right.wavefunction_cutoff_hartree)
            > specification.wavefunction_cutoff_absolute_tolerance_hartree
        ):
            add(
                BandStructureComparisonIssueCode.WAVEFUNCTION_CUTOFF_MISMATCH,
                "wavefunction cutoffs exceed the specification tolerance",
            )
        if not (
            left.pseudopotential_alignment_identity
            == right.pseudopotential_alignment_identity
            == specification.required_pseudopotential_alignment_identity
        ):
            add(
                BandStructureComparisonIssueCode.PSEUDOPOTENTIAL_ALIGNMENT_MISSING,
                "required pseudopotential alignment evidence is absent or mismatched",
            )
        if not (
            left.energy_unit is right.energy_unit is specification.required_energy_unit
        ):
            add(
                BandStructureComparisonIssueCode.ENERGY_UNIT_MISMATCH,
                "observations do not share the required energy unit",
            )
        if not (
            left.energy_alignment_identity
            == right.energy_alignment_identity
            == specification.required_energy_alignment_identity
        ):
            add(
                BandStructureComparisonIssueCode.ENERGY_ALIGNMENT_MISSING,
                "required energy-reference alignment is absent or mismatched",
            )
        if left.eigenvalues is None or right.eigenvalues is None:
            add(
                BandStructureComparisonIssueCode.COMPLETE_SPECTRUM_UNAVAILABLE,
                "both normalized complete spectra are required for comparison",
            )
        return tuple(findings)
