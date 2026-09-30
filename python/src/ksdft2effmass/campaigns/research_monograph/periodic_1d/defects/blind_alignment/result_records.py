"""Immutable version-one result records for the blind-alignment campaign."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np

from .evaluation import BlindAlignmentEvaluationResult
from .input_records import (
    BlindAlignmentObservationInformationContract,
    BlindAlignmentSourceIdentity,
    BlindAlignmentStopKind,
)
from .records import BlindAlignmentInferencePolicy

type SuccessfulStatus = Literal["aligned_full", "aligned_partial"]


@dataclass(frozen=True, slots=True)
class BlindAlignmentSuccessfulCaseResult:
    """Represent one flattened successful version-one case.

    Parameters
    ----------
    identifier
        Nonempty case identifier, equal to the nested evaluation identifier.
    status
        Full or partial alignment disposition.
    dimension
        Positive represented reference dimension.
    anchor_rank
        Positive identified anchor rank.
    anchor_condition_number
        Finite condition number of active anchor singular values.
    minimum_anchor_singular_value
        Positive smallest active anchor singular value.
    maximum_principal_angle_radians
        Finite largest retained-subspace principal angle in radians.
    energy_anchor_rank
        Positive finite represented exterior-anchor rank. The historical wire format
        stores this logically integral value as a JSON real.
    inferred_energy_shift
        Finite inferred candidate-minus-reference scalar shift in ``E_G``.
    evaluation
        Post hoc map, shift, extraction, model-class, and spectral diagnostics.
    """

    identifier: str
    status: SuccessfulStatus
    dimension: int
    anchor_rank: int
    anchor_condition_number: float
    minimum_anchor_singular_value: float
    maximum_principal_angle_radians: float
    energy_anchor_rank: float
    inferred_energy_shift: float
    evaluation: BlindAlignmentEvaluationResult

    def __post_init__(self) -> None:
        """Validate identity, dimensions, status, and finite diagnostics."""
        if type(self.identifier) is not str or not self.identifier:
            raise ValueError("successful-case identifier must be nonempty")
        if self.status not in ("aligned_full", "aligned_partial"):
            raise ValueError("successful-case status must be full or partial")
        if type(self.dimension) is not int or self.dimension < 1:
            raise ValueError("dimension must be a positive integer")
        if (
            type(self.anchor_rank) is not int
            or not 1 <= self.anchor_rank <= self.dimension
        ):
            raise ValueError("anchor_rank must lie within the represented dimension")
        values = (
            self.anchor_condition_number,
            self.minimum_anchor_singular_value,
            self.maximum_principal_angle_radians,
            self.energy_anchor_rank,
            self.inferred_energy_shift,
        )
        if any(not np.isfinite(value) for value in values):
            raise ValueError("successful inference diagnostics must be finite")
        if self.anchor_condition_number < 1.0:
            raise ValueError("anchor condition number must be at least one")
        if self.minimum_anchor_singular_value <= 0.0:
            raise ValueError("minimum anchor singular value must be positive")
        if self.energy_anchor_rank <= 0.0 or not self.energy_anchor_rank.is_integer():
            raise ValueError("energy_anchor_rank must be positive and integral")
        if not isinstance(self.evaluation, BlindAlignmentEvaluationResult):
            raise TypeError("evaluation must be BlindAlignmentEvaluationResult")
        if self.evaluation.identifier != self.identifier:
            raise ValueError("case and evaluation identifiers must agree")


@dataclass(frozen=True, slots=True)
class BlindAlignmentStoppedCaseResult:
    """Represent one structured stop without aligned outputs.

    Parameters
    ----------
    identifier
        Nonempty case identifier.
    issue_codes
        Sorted unique nonempty structured stop codes.
    anchor_rank
        Nonnegative numerical anchor rank available at the stop boundary.
    anchor_condition_number
        Optional finite active anchor condition number.
    minimum_anchor_singular_value
        Optional finite smallest active anchor singular value.
    maximum_principal_angle_radians
        Optional finite largest principal angle.
    energy_anchor_rank
        Optional finite nonnegative logically integral exterior rank.
    """

    identifier: str
    issue_codes: tuple[str, ...]
    anchor_rank: int
    anchor_condition_number: float | None
    minimum_anchor_singular_value: float | None
    maximum_principal_angle_radians: float | None
    energy_anchor_rank: float | None

    def __post_init__(self) -> None:
        """Validate a nonempty structured stop and its available finite diagnostics."""
        if type(self.identifier) is not str or not self.identifier:
            raise ValueError("stopped-case identifier must be nonempty")
        if not self.issue_codes or self.issue_codes != tuple(
            sorted(set(self.issue_codes))
        ):
            raise ValueError("stopped-case issue codes must be sorted and unique")
        if any(type(value) is not str or not value for value in self.issue_codes):
            raise TypeError("stopped-case issue codes must be nonempty strings")
        if type(self.anchor_rank) is not int or self.anchor_rank < 0:
            raise ValueError("anchor_rank must be a nonnegative integer")
        optional = (
            self.anchor_condition_number,
            self.minimum_anchor_singular_value,
            self.maximum_principal_angle_radians,
            self.energy_anchor_rank,
        )
        if any(value is not None and not np.isfinite(value) for value in optional):
            raise ValueError("available stop diagnostics must be finite")
        if self.energy_anchor_rank is not None and (
            self.energy_anchor_rank < 0.0 or not self.energy_anchor_rank.is_integer()
        ):
            raise ValueError("energy_anchor_rank must be nonnegative and integral")


type DiagnosticOutcome = (
    BlindAlignmentSuccessfulCaseResult | BlindAlignmentStoppedCaseResult
)


@dataclass(frozen=True, slots=True)
class BlindAlignmentNoiseCaseResult:
    """Bind one successful case to its authored unitary anchor-noise amplitude.

    Parameters
    ----------
    case
        Successful flattened inference and evaluation record.
    unitary_noise_radians
        Nonnegative finite authored anchor perturbation in radians.
    """

    case: BlindAlignmentSuccessfulCaseResult
    unitary_noise_radians: float

    def __post_init__(self) -> None:
        """Validate the successful case and nonnegative finite noise amplitude."""
        if not isinstance(self.case, BlindAlignmentSuccessfulCaseResult):
            raise TypeError("case must be BlindAlignmentSuccessfulCaseResult")
        if (
            not np.isfinite(self.unitary_noise_radians)
            or self.unitary_noise_radians < 0
        ):
            raise ValueError("unitary_noise_radians must be nonnegative and finite")


@dataclass(frozen=True, slots=True)
class BlindAlignmentGaugeCaseResult:
    """Represent identified-sector recovery and completion nonuniqueness.

    Parameters
    ----------
    case
        Successful partial identified-sector result.
    identified_dimension
        Positive identified reference dimension.
    unidentified_complement_dimension
        Positive unidentified complement dimension.
    full_completion_extraction_disagreement
        Full-space Frobenius disagreement between two unitary completions in ``E_G``.
    compressed_completion_extraction_disagreement
        Identified-sector compressed disagreement in ``E_G``.
    partial_map_agreement_between_completions
        Frobenius disagreement between identified partial maps.
    """

    case: BlindAlignmentSuccessfulCaseResult
    identified_dimension: int
    unidentified_complement_dimension: int
    full_completion_extraction_disagreement: float
    compressed_completion_extraction_disagreement: float
    partial_map_agreement_between_completions: float

    def __post_init__(self) -> None:
        """Validate partial status, dimensions, and finite completion diagnostics."""
        if not isinstance(self.case, BlindAlignmentSuccessfulCaseResult):
            raise TypeError("case must be BlindAlignmentSuccessfulCaseResult")
        if self.case.status != "aligned_partial":
            raise ValueError("gauge case must retain partial alignment status")
        if (
            type(self.identified_dimension) is not int
            or self.identified_dimension < 1
            or type(self.unidentified_complement_dimension) is not int
            or self.unidentified_complement_dimension < 1
        ):
            raise ValueError("identified and complement dimensions must be positive")
        if (
            self.identified_dimension + self.unidentified_complement_dimension
            != self.case.dimension
        ):
            raise ValueError("gauge dimensions must sum to represented dimension")
        values = (
            self.full_completion_extraction_disagreement,
            self.compressed_completion_extraction_disagreement,
            self.partial_map_agreement_between_completions,
        )
        if any(not np.isfinite(value) or value < 0.0 for value in values):
            raise ValueError("completion diagnostics must be nonnegative and finite")


@dataclass(frozen=True, slots=True)
class BlindAlignmentStoppingControlResult:
    """Bind one structured stop to its authored negative-control kind.

    Parameters
    ----------
    kind
        Closed negative-control kind.
    outcome
        Structured stopped result.
    """

    kind: BlindAlignmentStopKind
    outcome: BlindAlignmentStoppedCaseResult

    def __post_init__(self) -> None:
        """Require a supported stop kind and exact stopped-outcome record."""
        if self.kind not in (
            "anchor-condition",
            "principal-angle",
            "rank-mismatch",
            "spin-mismatch",
            "energy-anchor",
        ):
            raise ValueError("unsupported stopping-control kind")
        if not isinstance(self.outcome, BlindAlignmentStoppedCaseResult):
            raise TypeError("outcome must be BlindAlignmentStoppedCaseResult")


@dataclass(frozen=True, slots=True)
class BlindAlignmentConditioningDiagnosticResult:
    """Bind an outcome to a conditioning-boundary probe.

    Parameters
    ----------
    outcome
        Successful or stopped result at the probe.
    requested_minimum_anchor_singular_value
        Positive finite authored singular-value request.
    additive_anchor_noise_spectral_norm
        Positive finite additive anchor-noise spectral norm.
    """

    outcome: DiagnosticOutcome
    requested_minimum_anchor_singular_value: float
    additive_anchor_noise_spectral_norm: float

    def __post_init__(self) -> None:
        """Validate outcome type and positive finite conditioning controls."""
        if not isinstance(
            self.outcome,
            BlindAlignmentSuccessfulCaseResult | BlindAlignmentStoppedCaseResult,
        ):
            raise TypeError("outcome must be a successful or stopped case")
        values = (
            self.requested_minimum_anchor_singular_value,
            self.additive_anchor_noise_spectral_norm,
        )
        if any(not np.isfinite(value) or value <= 0.0 for value in values):
            raise ValueError("conditioning controls must be positive and finite")


@dataclass(frozen=True, slots=True)
class BlindAlignmentPrincipalAngleDiagnosticResult:
    """Bind an outcome to a retained-subspace angle probe.

    Parameters
    ----------
    outcome
        Successful or stopped result at the probe.
    requested_principal_angle_radians
        Finite authored principal angle in radians.
    minimum_subspace_overlap_singular_value
        Finite cosine of the requested angle.
    diagnostic_reference_basis_indices
        Nonempty tuple of nonnegative perturbed reference-basis indices.
    """

    outcome: DiagnosticOutcome
    requested_principal_angle_radians: float
    minimum_subspace_overlap_singular_value: float
    diagnostic_reference_basis_indices: tuple[int, ...]

    def __post_init__(self) -> None:
        """Validate outcome, angle channels, and deterministic basis indices."""
        if not isinstance(
            self.outcome,
            BlindAlignmentSuccessfulCaseResult | BlindAlignmentStoppedCaseResult,
        ):
            raise TypeError("outcome must be a successful or stopped case")
        if (
            not np.isfinite(self.requested_principal_angle_radians)
            or not 0.0 <= self.requested_principal_angle_radians <= np.pi / 2.0
        ):
            raise ValueError("requested principal angle must lie in [0, pi/2]")
        if (
            not np.isfinite(self.minimum_subspace_overlap_singular_value)
            or not 0.0 <= self.minimum_subspace_overlap_singular_value <= 1.0
        ):
            raise ValueError("minimum subspace overlap must lie in [0, 1]")
        if not self.diagnostic_reference_basis_indices or any(
            type(value) is not int or value < 0
            for value in self.diagnostic_reference_basis_indices
        ):
            raise ValueError("diagnostic basis indices must be nonnegative integers")


@dataclass(frozen=True, slots=True)
class BlindAlignmentEnergyAnchorDiagnosticResult:
    """Bind an outcome to one requested exterior energy-anchor rank.

    Parameters
    ----------
    outcome
        Successful or stopped result at the probe.
    requested_energy_anchor_rank
        Nonnegative integer requested rank.
    """

    outcome: DiagnosticOutcome
    requested_energy_anchor_rank: int

    def __post_init__(self) -> None:
        """Validate outcome type and nonnegative integer rank."""
        if not isinstance(
            self.outcome,
            BlindAlignmentSuccessfulCaseResult | BlindAlignmentStoppedCaseResult,
        ):
            raise TypeError("outcome must be a successful or stopped case")
        if type(self.requested_energy_anchor_rank) is not int:
            raise TypeError("requested_energy_anchor_rank must be an integer")
        if self.requested_energy_anchor_rank < 0:
            raise ValueError("requested_energy_anchor_rank must be nonnegative")


@dataclass(frozen=True, slots=True)
class BlindAlignmentRankReconciliationResult:
    """Represent explicit rectangular partial-isometry reconciliation.

    Parameters
    ----------
    case
        Successful partial identified-sector result.
    direct_comparison_issue_code
        Structured code from the unreconciled direct comparison.
    reference_dimension
        Positive reference-space dimension.
    candidate_dimension
        Positive lower candidate-space dimension.
    dropped_dimension
        Positive difference between reference and candidate dimensions.
    resolution
        Exact declared reconciliation mechanism.
    """

    case: BlindAlignmentSuccessfulCaseResult
    direct_comparison_issue_code: str
    reference_dimension: int
    candidate_dimension: int
    dropped_dimension: int
    resolution: str

    def __post_init__(self) -> None:
        """Validate partial outcome, dimension arithmetic, code, and resolution."""
        if not isinstance(self.case, BlindAlignmentSuccessfulCaseResult):
            raise TypeError("case must be BlindAlignmentSuccessfulCaseResult")
        if self.case.status != "aligned_partial":
            raise ValueError("rank reconciliation must retain partial status")
        if self.direct_comparison_issue_code != "BLIND_ALIGNMENT.RANK_MISMATCH":
            raise ValueError("rank reconciliation direct issue code is invalid")
        dimensions = (
            self.reference_dimension,
            self.candidate_dimension,
            self.dropped_dimension,
        )
        if any(type(value) is not int or value < 1 for value in dimensions):
            raise ValueError("rank reconciliation dimensions must be positive integers")
        if (
            self.reference_dimension - self.candidate_dimension
            != self.dropped_dimension
        ):
            raise ValueError("rank reconciliation dimension arithmetic is inconsistent")
        if self.resolution != "explicit_rectangular_partial_isometry":
            raise ValueError("rank reconciliation resolution is unsupported")


@dataclass(frozen=True, slots=True)
class BlindAlignmentSpinReconciliationResult:
    """Represent direct spin mismatch and explicit spin-lift reconciliation.

    Parameters
    ----------
    direct_comparison_issue_code
        Structured issue code from direct comparison.
    resolution
        Exact explicit spin-lift declaration.
    spin_independent_restriction_residual
        Nonnegative finite residual in ``E_G``.
    lossless_spin_restriction_available
        Whether lossless restriction to the spinless space exists.
    lifted_alignment
        Successful spinor alignment and post hoc evaluation.
    """

    direct_comparison_issue_code: str
    resolution: str
    spin_independent_restriction_residual: float
    lossless_spin_restriction_available: bool
    lifted_alignment: BlindAlignmentSuccessfulCaseResult

    def __post_init__(self) -> None:
        """Validate mismatch code, explicit lift, residual, Boolean, and lifted case."""
        if self.direct_comparison_issue_code != "BLIND_ALIGNMENT.SPIN_MISMATCH":
            raise ValueError("spin reconciliation direct issue code is invalid")
        if self.resolution != "explicit_spin_lift_to_common_spinor_space":
            raise ValueError("spin reconciliation resolution is unsupported")
        if (
            not np.isfinite(self.spin_independent_restriction_residual)
            or self.spin_independent_restriction_residual < 0.0
        ):
            raise ValueError("spin restriction residual must be nonnegative and finite")
        if type(self.lossless_spin_restriction_available) is not bool:
            raise TypeError("lossless_spin_restriction_available must be Boolean")
        if self.lossless_spin_restriction_available:
            raise ValueError("retained spin-mixing case has no lossless restriction")
        if not isinstance(self.lifted_alignment, BlindAlignmentSuccessfulCaseResult):
            raise TypeError("lifted_alignment must be a successful case")


@dataclass(frozen=True, slots=True)
class BlindAlignmentDiagnosticSuiteResult:
    """Store all retained neighboring stopping-boundary diagnostics.

    Parameters
    ----------
    conditioning_boundary
        Ordered conditioning probes.
    principal_angle_boundary
        Ordered retained-subspace angle probes.
    rank_reconciliation
        Explicit unequal-rank common-sector result.
    spin_reconciliation
        Explicit spin-lift result.
    energy_anchor_boundary
        Ordered exterior-rank probes.
    interpretation
        Exact retained diagnostic interpretation statement.
    """

    conditioning_boundary: tuple[BlindAlignmentConditioningDiagnosticResult, ...]
    principal_angle_boundary: tuple[BlindAlignmentPrincipalAngleDiagnosticResult, ...]
    rank_reconciliation: BlindAlignmentRankReconciliationResult
    spin_reconciliation: BlindAlignmentSpinReconciliationResult
    energy_anchor_boundary: tuple[BlindAlignmentEnergyAnchorDiagnosticResult, ...]
    interpretation: str

    def __post_init__(self) -> None:
        """Require nonempty ordered diagnostic families and exact typed records."""
        if (
            not self.conditioning_boundary
            or not self.principal_angle_boundary
            or not self.energy_anchor_boundary
        ):
            raise ValueError("diagnostic boundary families must be nonempty")
        if not isinstance(
            self.rank_reconciliation, BlindAlignmentRankReconciliationResult
        ):
            raise TypeError("rank_reconciliation has the wrong type")
        if not isinstance(
            self.spin_reconciliation, BlindAlignmentSpinReconciliationResult
        ):
            raise TypeError("spin_reconciliation has the wrong type")
        if type(self.interpretation) is not str or not self.interpretation:
            raise ValueError("diagnostic interpretation must be nonempty")


@dataclass(frozen=True, slots=True)
class BlindAlignmentInformationBoundary:
    """Represent the declared inference information boundary.

    Parameters
    ----------
    observation_contract
        Exact version-one observation-information declaration.
    inference_inputs
        Ordered human-readable inference-input inventory.
    withheld_from_inference
        Ordered hidden-value inventory.
    oracle_use
        Human-readable post hoc use declaration.
    """

    observation_contract: BlindAlignmentObservationInformationContract
    inference_inputs: tuple[str, ...]
    withheld_from_inference: tuple[str, ...]
    oracle_use: str

    def __post_init__(self) -> None:
        """Require typed contract and nonempty ordered explanatory inventories."""
        if not isinstance(
            self.observation_contract, BlindAlignmentObservationInformationContract
        ):
            raise TypeError("observation_contract has the wrong type")
        text = (*self.inference_inputs, *self.withheld_from_inference, self.oracle_use)
        if (
            not self.inference_inputs
            or not self.withheld_from_inference
            or any(type(value) is not str or not value for value in text)
        ):
            raise ValueError("information-boundary text must be nonempty")


@dataclass(frozen=True, slots=True)
class BlindAlignmentProvenance:
    """Represent retained version-one execution provenance.

    Parameters
    ----------
    input_path
        Repository-relative input path.
    input_sha256
        Input SHA-256 digest.
    script_path
        Repository-relative runner-adapter path.
    script_sha256
        Runner-adapter SHA-256 digest.
    python_version
        Recorded Python version string.
    numpy_version
        Recorded NumPy version string.
    """

    input_path: str
    input_sha256: str
    script_path: str
    script_sha256: str
    python_version: str
    numpy_version: str

    def __post_init__(self) -> None:
        """Require nonempty paths, versions, and lowercase SHA-256 digests."""
        text = (
            self.input_path,
            self.script_path,
            self.python_version,
            self.numpy_version,
        )
        if any(type(value) is not str or not value for value in text):
            raise ValueError("provenance paths and versions must be nonempty")
        for digest in (self.input_sha256, self.script_sha256):
            if len(digest) != 64 or any(
                character not in "0123456789abcdef" for character in digest
            ):
                raise ValueError("provenance digests must be lowercase SHA-256 values")


@dataclass(frozen=True, slots=True)
class BlindAlignmentCampaignResult:
    """Represent the complete semantic version-one blind-alignment result.

    Parameters
    ----------
    experiment_id
        Exact nonempty campaign identity.
    information_boundary
        Declared observation and oracle-use boundary.
    policy
        Numerical inference policy.
    core_radius_cells
        Nonnegative exterior-anchor core radius in primitive cells.
    exact_full_rank_cases
        Ordered exact successful cases.
    noise_sweep
        Ordered controlled sensitivity sequence.
    gauge_equivalent_case
        Undercomplete identified-sector and completion control.
    stopping_cases
        Ordered structured negative controls.
    debugging_diagnostics
        Neighboring stopping-boundary diagnostics.
    source_identities
        Ordered authenticated baseline identities.
    error_accounting
        Ordered named explanatory error-channel statements.
    limitations
        Ordered scientific and evidentiary limitations.
    provenance
        Retained execution provenance.
    """

    experiment_id: str
    information_boundary: BlindAlignmentInformationBoundary
    policy: BlindAlignmentInferencePolicy
    core_radius_cells: int
    exact_full_rank_cases: tuple[BlindAlignmentSuccessfulCaseResult, ...]
    noise_sweep: tuple[BlindAlignmentNoiseCaseResult, ...]
    gauge_equivalent_case: BlindAlignmentGaugeCaseResult
    stopping_cases: tuple[BlindAlignmentStoppingControlResult, ...]
    debugging_diagnostics: BlindAlignmentDiagnosticSuiteResult
    source_identities: tuple[BlindAlignmentSourceIdentity, ...]
    error_accounting: tuple[tuple[str, str], ...]
    limitations: tuple[str, ...]
    provenance: BlindAlignmentProvenance

    def __post_init__(self) -> None:
        """Validate complete nonempty inventories and top-level typed records."""
        if type(self.experiment_id) is not str or not self.experiment_id:
            raise ValueError("experiment_id must be nonempty")
        if not isinstance(self.information_boundary, BlindAlignmentInformationBoundary):
            raise TypeError("information_boundary has the wrong type")
        if not isinstance(self.policy, BlindAlignmentInferencePolicy):
            raise TypeError("policy has the wrong type")
        if type(self.core_radius_cells) is not int or self.core_radius_cells < 0:
            raise ValueError("core_radius_cells must be a nonnegative integer")
        inventories = (
            self.exact_full_rank_cases,
            self.noise_sweep,
            self.stopping_cases,
            self.source_identities,
            self.error_accounting,
            self.limitations,
        )
        if any(not values for values in inventories):
            raise ValueError("campaign result inventories must be nonempty")
        if not isinstance(self.gauge_equivalent_case, BlindAlignmentGaugeCaseResult):
            raise TypeError("gauge_equivalent_case has the wrong type")
        if not isinstance(
            self.debugging_diagnostics, BlindAlignmentDiagnosticSuiteResult
        ):
            raise TypeError("debugging_diagnostics has the wrong type")
        if not isinstance(self.provenance, BlindAlignmentProvenance):
            raise TypeError("provenance has the wrong type")
        if any(
            type(key) is not str or not key or type(value) is not str or not value
            for key, value in self.error_accounting
        ):
            raise ValueError("error-accounting entries must contain nonempty text")
        if any(type(value) is not str or not value for value in self.limitations):
            raise ValueError("limitations must contain nonempty strings")


@dataclass(frozen=True, slots=True)
class BlindAlignmentResultCorrelationRequest:
    """Request semantic and canonical correlation with one retained result.

    Parameters
    ----------
    calculated_result
        Newly calculated typed result.
    retained_payload
        Retained version-one UTF-8 JSON bytes.
    """

    calculated_result: BlindAlignmentCampaignResult
    retained_payload: bytes

    def __post_init__(self) -> None:
        """Require the exact result and bytes boundary types."""
        if not isinstance(self.calculated_result, BlindAlignmentCampaignResult):
            raise TypeError("calculated_result must be BlindAlignmentCampaignResult")
        if type(self.retained_payload) is not bytes:
            raise TypeError("retained_payload must be exact bytes")


@dataclass(frozen=True, slots=True)
class BlindAlignmentResultCorrelation:
    """Report identity-only correlation without a verification claim.

    Parameters
    ----------
    semantic_equal
        Whether decoded typed results compare equal.
    canonical_bytes_equal
        Whether canonical calculated bytes equal retained bytes exactly.
    calculated_sha256
        Canonical calculated-result SHA-256 digest.
    retained_sha256
        Original retained-payload SHA-256 digest.
    """

    semantic_equal: bool
    canonical_bytes_equal: bool
    calculated_sha256: str
    retained_sha256: str

    def __post_init__(self) -> None:
        """Validate Boolean channels and lowercase SHA-256 digests."""
        if (
            type(self.semantic_equal) is not bool
            or type(self.canonical_bytes_equal) is not bool
        ):
            raise TypeError("correlation agreement channels must be Boolean")
        for digest in (self.calculated_sha256, self.retained_sha256):
            if len(digest) != 64 or any(
                character not in "0123456789abcdef" for character in digest
            ):
                raise ValueError("correlation digests must be lowercase SHA-256 values")
