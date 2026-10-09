"""Closed immutable records for standalone optimizer-study verification."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OptimizerStandaloneProposal:
    """Represent verifier-owned proposal fields and frozen basin thresholds."""

    schema_version: int
    spread_tolerance: float
    center_tolerance: float
    density_tolerance: float
    best_basin_minimum_occupancy: int


@dataclass(frozen=True, slots=True)
class OptimizerStandaloneGaugeDesign:
    """Represent proposal identity and ordered deterministic-start identities."""

    schema_version: int
    proposal_sha256: str
    declared_start_count: int
    start_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class OptimizerStandaloneNativeCenter:
    """Represent one native center in active fractional coordinates."""

    active_fractional: tuple[float, float]
    active_fractional_modulo_cell: tuple[float, float]
    orbital: int


@dataclass(frozen=True, slots=True)
class OptimizerStandaloneNativeEndpoint:
    """Represent the complete retained native endpoint object field by field.

    Spread quantities have squared-cell units. Terminal slope and residual fields retain
    the historical extractor's binary64 values and conventions.
    """

    centers: tuple[OptimizerStandaloneNativeCenter, ...]
    classification_status: str
    diagnostic_classification: str
    iterations: int
    omega_d_cell_squared: float
    omega_i_cell_squared: float
    omega_od_cell_squared: float
    omega_tilde_cell_squared: float
    omega_total_cell_squared: float
    orbital_spreads_cell_squared: tuple[float, ...]
    terminal_detrended_spread_rms: float
    terminal_maximum_spread_cell_squared: float
    terminal_median_absolute_delta_spread: float
    terminal_median_rms_gradient: float
    terminal_minimum_spread_cell_squared: float
    terminal_spread_slope_per_iteration: float
    terminal_window_point_count: int
    trace_point_count: int


@dataclass(frozen=True, slots=True)
class OptimizerStandaloneEndpoint:
    """Represent fields needed to reconstruct one initial/continuation transition."""

    configuration_id: str
    arm: str
    start_id: str
    start_index: int
    initial_process_completed: bool
    initial_native_converged: bool
    continuation_applied: bool
    continuation_native_converged: bool | None
    initial_native_endpoint: OptimizerStandaloneNativeEndpoint
    continuation_native_endpoint: OptimizerStandaloneNativeEndpoint | None
    effective_native_converged: bool
    effective_native_endpoint: OptimizerStandaloneNativeEndpoint
    effective_total_iterations: int


@dataclass(frozen=True, slots=True)
class OptimizerStandaloneProvenance:
    """Represent direct compact-source declarations used for authentication."""

    proposal_sha256: str
    extractor_path: str
    extractor_sha256: str


@dataclass(frozen=True, slots=True)
class OptimizerStandaloneExecutionSummary:
    """Represent retained aggregate endpoint and continuation counts."""

    initial_localization_count: int
    initial_process_completion_count: int
    initial_native_converged_count: int
    continuation_count: int
    continuation_native_converged_count: int
    effective_native_converged_count: int
    effective_native_nonconverged_count: int
    diagnostic_counts: tuple[tuple[str, int], ...]


@dataclass(frozen=True, slots=True)
class OptimizerStandaloneRejectedEquivalence:
    """Represent one rejected direct basin-equivalence candidate.

    ``float('inf')`` is permitted only for the two historical extended-real mismatch
    fields. It denotes that the retained comparison found no finite admissible match.
    """

    center_set_periodic_distance: float
    maximum_density_l2_mismatch: float
    representative_start_id: str


@dataclass(frozen=True, slots=True)
class OptimizerStandaloneMemberEquivalence:
    """Represent one retained threshold-passing member-to-representative match."""

    start_id: str
    center_set_periodic_distance: float
    maximum_density_l2_mismatch: float


@dataclass(frozen=True, slots=True)
class OptimizerStandaloneBasin:
    """Represent one observed basin and its retained comparison diagnostics."""

    basin_id: str
    representative_start_id: str
    representative_omega_tilde_cell_squared: float
    start_ids: tuple[str, ...]
    occupancy: int
    start_blocks_present: tuple[int, ...]
    appears_in_both_start_blocks: bool
    member_equivalence_diagnostics: tuple[OptimizerStandaloneMemberEquivalence, ...]
    rejected_equivalence_candidates: tuple[OptimizerStandaloneRejectedEquivalence, ...]


@dataclass(frozen=True, slots=True)
class OptimizerStandaloneSensitivity:
    """Represent one retained density-tolerance sensitivity observation."""

    density_l2_tolerance: float
    direct_matching_pair_count: int
    best_endpoint_direct_match_start_ids: tuple[str, ...]
    best_endpoint_direct_occupancy: int


@dataclass(frozen=True, slots=True)
class OptimizerStandaloneControlObservation:
    """Represent one post-hoc exact-equivalence numerical control."""

    center_set_periodic_distance: float
    maximum_density_l2_mismatch: float


@dataclass(frozen=True, slots=True)
class OptimizerStandaloneControls:
    """Represent retained post-hoc control records and threshold flags."""

    declared_count: int
    maximum_center_distance: float
    maximum_density_mismatch: float
    passes_center_tolerance: bool
    passes_density_tolerance: bool
    observations: tuple[OptimizerStandaloneControlObservation, ...]


@dataclass(frozen=True, slots=True)
class OptimizerStandaloneGroup:
    """Represent verifier-owned aggregate and basin fields for one study group."""

    configuration_id: str
    arm: str
    initial_native_converged_count: int
    effective_native_converged_count: int
    effective_native_converged_fraction: float
    effective_nonconverged_start_ids: tuple[str, ...]
    best_observed_start_id: str
    declared_basin_count: int
    basins: tuple[OptimizerStandaloneBasin, ...]
    best_basin_criterion_pass: bool
    sensitivity: tuple[OptimizerStandaloneSensitivity, ...]
    controls: OptimizerStandaloneControls


@dataclass(frozen=True, slots=True)
class OptimizerStandaloneResult:
    """Represent all row-055 fields owned by portable verification."""

    schema_version: int
    provenance: OptimizerStandaloneProvenance
    endpoints: tuple[OptimizerStandaloneEndpoint, ...]
    summary: OptimizerStandaloneExecutionSummary
    groups: tuple[OptimizerStandaloneGroup, ...]
    basin_tolerance_control_status: str
    supports_declared_convergence: bool
    not_global_optimizer_convergence: bool
    not_general_wannier_convergence: bool
    convergence_disposition: str


@dataclass(frozen=True, slots=True)
class OptimizerStandaloneDecodedDocuments:
    """Pair typed proposal, gauge-design, and result records."""

    proposal: OptimizerStandaloneProposal
    gauge_design: OptimizerStandaloneGaugeDesign
    result: OptimizerStandaloneResult


@dataclass(frozen=True, slots=True)
class OptimizerStandaloneReconstruction:
    """Represent bounded reconstructed endpoint and continuation counts."""

    endpoint_count: int
    continuation_count: int
    effective_converged_count: int
    final_nonconverged_count: int
