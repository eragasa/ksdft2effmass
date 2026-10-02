"""Immutable version-one input records for the blind-alignment campaign."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np

from .records import BlindAlignmentInferencePolicy

type BlindAlignmentStopKind = Literal[
    "anchor-condition",
    "principal-angle",
    "rank-mismatch",
    "spin-mismatch",
    "energy-anchor",
]


@dataclass(frozen=True, slots=True)
class BlindAlignmentSourceIdentity:
    """Identify one immutable baseline artifact.

    Parameters
    ----------
    path
        Nonempty repository-relative POSIX path.
    sha256
        Lowercase hexadecimal SHA-256 digest.
    """

    path: str
    sha256: str

    def __post_init__(self) -> None:
        """Require a safe repository-relative path and lowercase SHA-256 digest."""
        if type(self.path) is not str or type(self.sha256) is not str:
            raise TypeError("source path and SHA-256 must be strings")
        if not self.path:
            raise ValueError("source path must be nonempty")
        if self.path.startswith("/") or ".." in self.path.split("/"):
            raise ValueError("source path must be repository-relative")
        if len(self.sha256) != 64 or any(
            value not in "0123456789abcdef" for value in self.sha256
        ):
            raise ValueError("source SHA-256 must be lowercase hexadecimal")


@dataclass(frozen=True, slots=True)
class BlindAlignmentObservationInformationContract:
    """Declare the exact information exposed to inference.

    Parameters
    ----------
    anchor_cross_covariance
        Availability declaration for the authored covariance matrix.
    site_anchor_labels
        Availability declaration for site labels.
    orbital_labels
        Availability declaration for orbital labels.
    spin_frame
        Availability declaration for reference and candidate spin frames.
    energy_reference
        Availability declaration for the exterior anchor and scalar shift.
    """

    anchor_cross_covariance: str
    site_anchor_labels: str
    orbital_labels: str
    spin_frame: str
    energy_reference: str

    def __post_init__(self) -> None:
        """Require the exact version-one observation-information declarations."""
        values = (
            self.anchor_cross_covariance,
            self.site_anchor_labels,
            self.orbital_labels,
            self.spin_frame,
            self.energy_reference,
        )
        if any(type(value) is not str for value in values):
            raise TypeError("observation information declarations must be strings")
        expected = (
            "available_as_authored_matrix",
            "available_on_reference_rows_only",
            "available_on_reference_rows_only",
            "reference_frame_labels_available_candidate_rotation_hidden",
            "exterior_projector_available_scalar_shift_hidden",
        )
        if values != expected:
            raise ValueError("observation information contract is unsupported")


@dataclass(frozen=True, slots=True)
class BlindAlignmentExactCase:
    """Represent one exact full-rank campaign case.

    Parameters
    ----------
    identifier
        Nonempty case identifier.
    defect_id
        Nonempty planted-defect identifier used only by campaign construction.
    spin_count
        Represented spin factor, either one or two.
    minimum_anchor_singular_value
        Positive finite smallest authored anchor singular value.
    """

    identifier: str
    defect_id: str
    spin_count: int
    minimum_anchor_singular_value: float

    def __post_init__(self) -> None:
        """Validate exact-case identifiers, spin factor, and anchor bound."""
        if not self.identifier or not self.defect_id:
            raise ValueError("exact-case identifiers must be nonempty")
        if type(self.spin_count) is not int:
            raise TypeError("spin_count must be an integer")
        if self.spin_count not in (1, 2):
            raise ValueError("spin_count must be one or two")
        if isinstance(self.minimum_anchor_singular_value, bool) or not isinstance(
            self.minimum_anchor_singular_value, int | float
        ):
            raise TypeError("minimum anchor singular value must be real")
        if (
            not np.isfinite(self.minimum_anchor_singular_value)
            or not 0.0 < self.minimum_anchor_singular_value <= 1.0
        ):
            raise ValueError("minimum anchor singular value must lie in (0, 1]")


@dataclass(frozen=True, slots=True)
class BlindAlignmentNoiseSweep:
    """Represent the well-conditioned anchor-noise sequence.

    Parameters
    ----------
    identifier
        Nonempty sequence identifier.
    defect_id
        Nonempty planted-defect identifier.
    spin_count
        Represented spin factor.
    minimum_anchor_singular_value
        Positive smallest unperturbed anchor singular value.
    unitary_noise_radians
        Increasing nonnegative unitary-noise amplitudes in radians.
    generator_seed
        Python integer seed for deterministic construction.
    """

    identifier: str
    defect_id: str
    spin_count: int
    minimum_anchor_singular_value: float
    unitary_noise_radians: tuple[float, ...]
    generator_seed: int

    def __post_init__(self) -> None:
        """Validate the base case, ordered amplitudes, and deterministic seed."""
        BlindAlignmentExactCase(
            self.identifier,
            self.defect_id,
            self.spin_count,
            self.minimum_anchor_singular_value,
        )
        if not self.unitary_noise_radians:
            raise ValueError("unitary noise sequence must be nonempty")
        if tuple(sorted(set(self.unitary_noise_radians))) != self.unitary_noise_radians:
            raise ValueError("unitary noise sequence must be increasing and unique")
        if any(
            not np.isfinite(value) or value < 0.0
            for value in self.unitary_noise_radians
        ):
            raise ValueError("unitary noise amplitudes must be nonnegative and finite")
        if type(self.generator_seed) is not int:
            raise TypeError("generator_seed must be an integer")


@dataclass(frozen=True, slots=True)
class BlindAlignmentGaugeCase:
    """Represent the undercomplete identified-sector control.

    Parameters
    ----------
    identifier
        Nonempty case identifier.
    defect_id
        Nonempty planted-defect identifier.
    spin_count
        Represented spin factor.
    identified_site_count
        Positive number of anchored sites.
    minimum_nonzero_anchor_singular_value
        Positive smallest active anchor singular value.
    complement_rotation_radians
        Finite nonzero rotation amplitude on the unidentified complement.
    generator_seed
        Python integer seed for deterministic construction.
    """

    identifier: str
    defect_id: str
    spin_count: int
    identified_site_count: int
    minimum_nonzero_anchor_singular_value: float
    complement_rotation_radians: float
    generator_seed: int

    def __post_init__(self) -> None:
        """Validate identified-sector dimensions, anchor bound, rotation, and seed."""
        BlindAlignmentExactCase(
            self.identifier,
            self.defect_id,
            self.spin_count,
            self.minimum_nonzero_anchor_singular_value,
        )
        if type(self.identified_site_count) is not int:
            raise TypeError("identified_site_count must be an integer")
        if self.identified_site_count < 1:
            raise ValueError("identified_site_count must be positive")
        if isinstance(self.complement_rotation_radians, bool) or not isinstance(
            self.complement_rotation_radians, int | float
        ):
            raise TypeError("complement rotation must be real")
        if (
            not np.isfinite(self.complement_rotation_radians)
            or self.complement_rotation_radians == 0.0
        ):
            raise ValueError("complement rotation must be finite and nonzero")
        if type(self.generator_seed) is not int:
            raise TypeError("generator_seed must be an integer")


@dataclass(frozen=True, slots=True)
class BlindAlignmentStoppingCase:
    """Represent one authored structured-stop observation.

    Parameters
    ----------
    identifier
        Nonempty case identifier.
    kind
        Closed stopping-case kind.
    numeric_value
        Optional finite authored threshold probe or integer dimension/spin change.
    """

    identifier: str
    kind: BlindAlignmentStopKind
    numeric_value: float | int | None

    def __post_init__(self) -> None:
        """Validate the closed stop kind and its kind-specific optional value."""
        if type(self.identifier) is not str or not self.identifier:
            raise ValueError("stopping-case identifier must be nonempty")
        kinds = (
            "anchor-condition",
            "principal-angle",
            "rank-mismatch",
            "spin-mismatch",
            "energy-anchor",
        )
        if self.kind not in kinds:
            raise ValueError("unsupported stopping-case kind")
        if self.kind == "energy-anchor":
            if self.numeric_value is not None:
                raise ValueError("energy-anchor stop has no numeric value")
            return
        if self.numeric_value is None or isinstance(self.numeric_value, bool):
            raise TypeError("stopping-case numeric value is required")
        if self.kind in ("rank-mismatch", "spin-mismatch"):
            if type(self.numeric_value) is not int:
                raise TypeError("rank and spin stopping values must be integers")
        elif not isinstance(self.numeric_value, int | float):
            raise TypeError("stopping threshold must be real")
        if not np.isfinite(self.numeric_value):
            raise ValueError("stopping-case numeric value must be finite")


@dataclass(frozen=True, slots=True)
class BlindAlignmentDiagnosticControls:
    """Represent neighboring probes for structured stopping boundaries.

    Parameters
    ----------
    conditioning_minimum_singular_values
        Positive finite singular values used around the conditioning boundary.
    conditioning_additive_anchor_noise
        Positive finite spectral-norm amplitude of additive anchor noise.
    conditioning_noise_seed
        Python integer deterministic seed.
    principal_angle_radians
        Increasing finite retained-subspace angles in ``[0, pi/2]``.
    rank_drop
        Positive integer dimension drop for explicit reconciliation.
    energy_anchor_ranks
        Increasing nonnegative integer exterior ranks.
    """

    conditioning_minimum_singular_values: tuple[float, ...]
    conditioning_additive_anchor_noise: float
    conditioning_noise_seed: int
    principal_angle_radians: tuple[float, ...]
    rank_drop: int
    energy_anchor_ranks: tuple[int, ...]

    def __post_init__(self) -> None:
        """Validate all ordered finite boundary-probe controls."""
        if not self.conditioning_minimum_singular_values:
            raise ValueError("conditioning diagnostic sequence must be nonempty")
        if any(
            not np.isfinite(value) or value <= 0.0
            for value in self.conditioning_minimum_singular_values
        ):
            raise ValueError("conditioning singular values must be positive and finite")
        if (
            not np.isfinite(self.conditioning_additive_anchor_noise)
            or self.conditioning_additive_anchor_noise <= 0.0
        ):
            raise ValueError("conditioning anchor noise must be positive and finite")
        if type(self.conditioning_noise_seed) is not int:
            raise TypeError("conditioning_noise_seed must be an integer")
        if not self.principal_angle_radians or any(
            not np.isfinite(value) or not 0.0 <= value <= np.pi / 2.0
            for value in self.principal_angle_radians
        ):
            raise ValueError("principal angles must be finite and lie in [0, pi/2]")
        if type(self.rank_drop) is not int or self.rank_drop < 1:
            raise ValueError("rank_drop must be a positive integer")
        if not self.energy_anchor_ranks or any(
            type(value) is not int or value < 0 for value in self.energy_anchor_ranks
        ):
            raise ValueError("energy-anchor ranks must be nonnegative integers")


@dataclass(frozen=True, slots=True)
class BlindAlignmentCampaignInput:
    """Represent the complete immutable version-one campaign input.

    Parameters
    ----------
    experiment_id
        Nonempty retained experiment identifier.
    baseline_input
        Identity of the matched-extraction input.
    baseline_result
        Identity of the matched-extraction retained result.
    observation_information
        Exact declaration of information visible to inference.
    policy
        Frozen numerical inference policy.
    core_radius_cells
        Nonnegative exterior-energy-anchor core radius in primitive cells.
    exact_cases
        Nonempty exact full-rank cases.
    noise_sweep
        Controlled anchor-noise sensitivity sequence.
    gauge_case
        Undercomplete identified-sector control.
    stopping_cases
        Authored negative controls.
    diagnostics
        Neighboring stopping-boundary probes.
    algebraic_tolerance
        Positive finite dimensionless verification tolerance.
    """

    experiment_id: str
    baseline_input: BlindAlignmentSourceIdentity
    baseline_result: BlindAlignmentSourceIdentity
    observation_information: BlindAlignmentObservationInformationContract
    policy: BlindAlignmentInferencePolicy
    core_radius_cells: int
    exact_cases: tuple[BlindAlignmentExactCase, ...]
    noise_sweep: BlindAlignmentNoiseSweep
    gauge_case: BlindAlignmentGaugeCase
    stopping_cases: tuple[BlindAlignmentStoppingCase, ...]
    diagnostics: BlindAlignmentDiagnosticControls
    algebraic_tolerance: float

    def __post_init__(self) -> None:
        """Enforce complete case inventories, unique IDs, and finite tolerance."""
        if type(self.experiment_id) is not str or not self.experiment_id:
            raise ValueError("experiment_id must be nonempty")
        if type(self.core_radius_cells) is not int:
            raise TypeError("core_radius_cells must be an integer")
        if self.core_radius_cells < 0:
            raise ValueError("core_radius_cells must be nonnegative")
        if not self.exact_cases or not self.stopping_cases:
            raise ValueError("campaign cases must be nonempty")
        identifiers = (
            *(item.identifier for item in self.exact_cases),
            self.noise_sweep.identifier,
            self.gauge_case.identifier,
            *(item.identifier for item in self.stopping_cases),
        )
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("campaign case identifiers must be unique")
        if isinstance(self.algebraic_tolerance, bool) or not isinstance(
            self.algebraic_tolerance, int | float
        ):
            raise TypeError("algebraic_tolerance must be real")
        if not np.isfinite(self.algebraic_tolerance) or self.algebraic_tolerance <= 0.0:
            raise ValueError("algebraic_tolerance must be positive and finite")
