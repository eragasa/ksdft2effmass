"""Immutable decoded records for optimizer-basin reanalysis verification.

These records expose only fields used by the frozen row-053 verification contract.
Complete endpoint objects are also retained as immutable JSON so exact-copy correlation
can include fields that the portable verifier deliberately does not interpret. Their
constructors are decoder-owned implementation boundaries and are not exported by a
reviewed package facade.
"""

from dataclasses import dataclass

from ksdft2effmass.serialization.json import ImmutableJsonObject

type PeriodicCenter2D = tuple[float, float]
type PeriodicCenterSet2D = tuple[PeriodicCenter2D, ...]


@dataclass(frozen=True, slots=True)
class OptimizerBasinSourceEndpoint:
    """Decoded source-result fields correlated with one reanalysis endpoint.

    Parameters
    ----------
    gauge_id
        Exact retained initial-gauge identity.
    convergence_criterion_satisfied
        Native convergence Boolean copied from the source result.
    native_total_spread_cell_squared
        Finite native total spread in retained cell-squared units.
    """

    gauge_id: str
    convergence_criterion_satisfied: bool
    native_total_spread_cell_squared: float


@dataclass(frozen=True, slots=True)
class OptimizerBasinSourceConfiguration:
    """Decoded source configuration used by row-053 correlation.

    Parameters
    ----------
    configuration_id
        Exact retained source-configuration identity.
    plane_wave_cutoff
        Exact retained plane-wave cutoff control.
    reciprocal_mesh_size
        Exact retained reciprocal-mesh control.
    transverse_lattice_length
        Finite retained auxiliary-embedding control.
    starts
        Immutable decoded source endpoint sequence in caller order.
    """

    configuration_id: str
    plane_wave_cutoff: int
    reciprocal_mesh_size: int
    transverse_lattice_length: float
    starts: tuple[OptimizerBasinSourceEndpoint, ...]


@dataclass(frozen=True, slots=True)
class OptimizerBasinSourceResult:
    """Decoded source result consumed by offline reanalysis verification.

    Parameters
    ----------
    schema_version
        Exact retained source schema version.
    configurations
        Immutable source configurations in retained order.
    """

    schema_version: int
    configurations: tuple[OptimizerBasinSourceConfiguration, ...]


@dataclass(frozen=True, slots=True)
class OptimizerReanalysisProvenance:
    """Decoded compact-source declarations owned by portable authentication.

    Parameters
    ----------
    source_result_sha256
        Declared identity of encapsulated source-result bytes.
    reanalyzer_path, base_extractor_path
        Direct repository-relative compact-source declarations.
    reanalyzer_sha256, base_extractor_sha256
        Declared identities of the corresponding compact source bytes.
    """

    source_result_sha256: str
    reanalyzer_path: str
    reanalyzer_sha256: str
    base_extractor_path: str
    base_extractor_sha256: str


@dataclass(frozen=True, slots=True)
class OptimizerReanalysisMethod:
    """Decoded method values used by bounded reconstruction.

    Parameters
    ----------
    common_estimator_fft_sizes
        Ordered retained FFT refinement sizes.
    basin_spread_absolute_tolerance
        Finite absolute gauge-dependent-spread tolerance in cell-squared units.
    basin_center_set_periodic_tolerance
        Finite periodic center-set tolerance in cell coordinates.
    """

    common_estimator_fft_sizes: tuple[int, ...]
    basin_spread_absolute_tolerance: float
    basin_center_set_periodic_tolerance: float


@dataclass(frozen=True, slots=True)
class OptimizerReanalysisSpreadComponents:
    """Decoded spread and terminal-trace fields for one endpoint.

    Parameters
    ----------
    omega_i_cell_squared, omega_d_cell_squared, omega_od_cell_squared
        Finite retained invariant, diagonal, and off-diagonal spread components.
    omega_tilde_cell_squared, omega_total_cell_squared
        Finite retained gauge-dependent and total spread values.
    terminal_spread_slope_per_iteration
        Finite retained terminal linear-spread slope.
    terminal_detrended_spread_rms
        Finite retained detrended terminal RMS spread diagnostic.
    terminal_median_absolute_delta_spread
        Finite retained median absolute terminal spread increment.
    terminal_median_rms_gradient
        Finite retained median terminal RMS-gradient diagnostic.
    diagnostic_classification
        Retained descriptive post-hoc class; not a native convergence decision.
    """

    omega_i_cell_squared: float
    omega_d_cell_squared: float
    omega_od_cell_squared: float
    omega_tilde_cell_squared: float
    omega_total_cell_squared: float
    terminal_spread_slope_per_iteration: float
    terminal_detrended_spread_rms: float
    terminal_median_absolute_delta_spread: float
    terminal_median_rms_gradient: float
    diagnostic_classification: str


@dataclass(frozen=True, slots=True)
class OptimizerReanalysisEndpoint:
    """Decoded verifier-owned fields plus the complete immutable endpoint object.

    Parameters
    ----------
    configuration_id, gauge_id
        Exact enclosing configuration and initial-gauge identities.
    convergence_criterion_satisfied
        Retained native convergence Boolean.
    native_centers_modulo_cell
        Nonempty center set in periodic cell coordinates.
    spread_components
        Typed spread decomposition and terminal diagnostics.
    complete_document
        Complete immutable endpoint object used only for exact-copy correlation.
    """

    configuration_id: str
    gauge_id: str
    convergence_criterion_satisfied: bool
    native_centers_modulo_cell: PeriodicCenterSet2D
    spread_components: OptimizerReanalysisSpreadComponents
    complete_document: ImmutableJsonObject


@dataclass(frozen=True, slots=True)
class OptimizerReanalysisBasin:
    """Decoded retained membership of one observed symmetry-aware basin.

    Parameters
    ----------
    gauge_ids
        Exact retained member gauge identities.
    """

    gauge_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class OptimizerReanalysisConfiguration:
    """Decoded configuration used by source and basin correlation.

    Parameters
    ----------
    configuration_id
        Exact retained configuration identity.
    plane_wave_cutoff, reciprocal_mesh_size, transverse_lattice_length
        Retained numerical controls correlated with the source result.
    starts
        Immutable decoded endpoint sequence.
    symmetry_aware_observed_basins
        Retained observed basin membership records.
    symmetry_aware_observed_basin_count
        Declared number of retained observed basins.
    best_observed_converged_by_omega_tilde
        Complete copied minimum reported converged endpoint.
    """

    configuration_id: str
    plane_wave_cutoff: int
    reciprocal_mesh_size: int
    transverse_lattice_length: float
    starts: tuple[OptimizerReanalysisEndpoint, ...]
    symmetry_aware_observed_basins: tuple[OptimizerReanalysisBasin, ...]
    symmetry_aware_observed_basin_count: int
    best_observed_converged_by_omega_tilde: OptimizerReanalysisEndpoint


@dataclass(frozen=True, slots=True)
class OptimizerReanalysisRefinementSize:
    """Decoded common-estimator observation at one FFT size.

    Parameters
    ----------
    fft_size
        Exact retained FFT-grid size.
    input_path, input_sha256
        External logical path and strict digest bound to a maintained fixture basename.
    common_total_spread_cell_squared
        Finite common-estimator total spread in cell-squared units.
    common_centers_modulo_cell
        Nonempty common-estimator center set in periodic cell coordinates.
    """

    fft_size: int
    input_path: str
    input_sha256: str
    common_total_spread_cell_squared: float
    common_centers_modulo_cell: PeriodicCenterSet2D


@dataclass(frozen=True, slots=True)
class OptimizerReanalysisRefinement:
    """Decoded common-estimator refinement case and retained comparison.

    Parameters
    ----------
    case_id, configuration_id, gauge_id
        Exact retained case, configuration, and initial-gauge identities.
    convergence_criterion_satisfied
        Retained native convergence Boolean correlated with the endpoint.
    sizes
        Ordered immutable common-estimator observations.
    relative_total_spread_difference
        Retained 512-to-1024 relative total-spread difference.
    center_set_periodic_distance
        Retained 512-to-1024 permutation-matched periodic center distance.
    """

    case_id: str
    configuration_id: str
    gauge_id: str
    convergence_criterion_satisfied: bool
    sizes: tuple[OptimizerReanalysisRefinementSize, ...]
    relative_total_spread_difference: float
    center_set_periodic_distance: float


@dataclass(frozen=True, slots=True)
class OptimizerReanalysisResult:
    """Decoded row-053 result fields owned by portable verification.

    Parameters
    ----------
    schema_version
        Exact retained reanalysis schema version.
    provenance
        Direct compact-source declarations.
    method
        Bounded reconstruction method values.
    configurations
        Immutable decoded reanalysis configurations.
    diagnostic_classification_counts
        Immutable class-to-count pairs in retained object order.
    common_estimator_refinement
        Immutable retained refinement cases.
    """

    schema_version: int
    provenance: OptimizerReanalysisProvenance
    method: OptimizerReanalysisMethod
    configurations: tuple[OptimizerReanalysisConfiguration, ...]
    diagnostic_classification_counts: tuple[tuple[str, int], ...]
    common_estimator_refinement: tuple[OptimizerReanalysisRefinement, ...]


@dataclass(frozen=True, slots=True)
class OptimizerReanalysisDecodedDocuments:
    """Pair typed source and reanalysis records from exact encoded wires.

    Parameters
    ----------
    source_result
        Typed verifier-owned source-result fields.
    reanalysis_result
        Typed verifier-owned offline-reanalysis fields.
    """

    source_result: OptimizerBasinSourceResult
    reanalysis_result: OptimizerReanalysisResult
