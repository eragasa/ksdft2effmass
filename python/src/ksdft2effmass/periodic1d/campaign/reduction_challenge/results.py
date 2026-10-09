"""Typed retained outcomes for the periodic-1D reduction challenge.

Canonical Python attributes describe the scientific or numerical channel directly.
The serializer maps them explicitly to the unchanged historical schema-one ``stress``
keys retained in the Appendix G result wire.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.serialization import JsonCodec
from ksdft2effmass.serialization.json import ImmutableJsonObject

from ..result_documents import (
    Periodic1DEncodedResultDocument,
    Periodic1DEncodedResultJsonSerializer,
    Periodic1DEncodedResultKind,
)


@dataclass(frozen=True, slots=True)
class Periodic1DReductionChallengeDiscretizationObservation:
    """Retain one finite-representation error observation.

    Parameters
    ----------
    resolution
        Positive plane-wave cutoff or finite-difference point count, as selected by the
        owning inventory.
    maximum_low_band_error
        Nonnegative finite maximum absolute low-band difference in normalized recoil
        energy units :math:`E_G`.

    Raises
    ------
    TypeError
        If either value has the wrong exact scalar representation.
    ValueError
        If ``resolution`` is not positive or the error is negative.
    OverflowError
        If the error is not finite binary64.

    Notes
    -----
    This observation compares finite representations. It is not a bound on error
    against the untruncated parent and does not establish convergence.
    """

    resolution: int
    maximum_low_band_error: float

    def __post_init__(self) -> None:
        """Validate resolution and the finite nonnegative error diagnostic."""
        if type(self.resolution) is not int:
            raise TypeError("resolution must be a built-in int")
        if self.resolution <= 0:
            raise ValueError("resolution must be positive")
        if type(self.maximum_low_band_error) is not float:
            raise TypeError("maximum_low_band_error must be a built-in float")
        if not np.isfinite(self.maximum_low_band_error):
            raise OverflowError("maximum_low_band_error must be finite binary64")
        if self.maximum_low_band_error < 0.0:
            raise ValueError("maximum_low_band_error must be nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DReductionChallengePotentialAmplitudeResult:
    """Retain one potential-amplitude challenge outcome.

    Parameters
    ----------
    potential_strength
        Nonnegative dimensionless cosine amplitude.
    zone_boundary_gap
        Nonnegative sampled gap in normalized recoil-energy units.
    isolated_band_status
        Producer disposition under the declared gap threshold. Correlation and
        verification independently check this value against campaign controls.
    potential_sign_invariance_maximum_error
        Nonnegative maximum finite-representation sign-covariance defect.
    plane_wave_cutoff_study, finite_difference_grid_study
        Ordered finite-representation observations. These routes remain separate.
    """

    potential_strength: float
    zone_boundary_gap: float
    isolated_band_status: str
    potential_sign_invariance_maximum_error: float
    plane_wave_cutoff_study: tuple[
        Periodic1DReductionChallengeDiscretizationObservation, ...
    ]
    finite_difference_grid_study: tuple[
        Periodic1DReductionChallengeDiscretizationObservation, ...
    ]

    def __post_init__(self) -> None:
        """Validate scalar diagnostics, status, and typed study inventories."""
        self._check_args_scalars()
        self._check_args_status()
        self._check_args_studies()

    def _check_args_scalars(self) -> None:
        """Require exact finite nonnegative binary64 diagnostic scalars."""
        for name, value in (
            ("potential_strength", self.potential_strength),
            ("zone_boundary_gap", self.zone_boundary_gap),
            (
                "potential_sign_invariance_maximum_error",
                self.potential_sign_invariance_maximum_error,
            ),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not np.isfinite(value):
                raise OverflowError(f"{name} must be finite binary64")
            if value < 0.0:
                raise ValueError(f"{name} must be nonnegative")

    def _check_args_status(self) -> None:
        """Require a nonempty exact status string without interpreting it by name."""
        if type(self.isolated_band_status) is not str:
            raise TypeError("isolated_band_status must be a built-in str")
        if not self.isolated_band_status:
            raise ValueError("isolated_band_status must be nonempty")

    def _check_args_studies(self) -> None:
        """Require two nonempty exact observation inventories."""
        for name, study in (
            ("plane_wave_cutoff_study", self.plane_wave_cutoff_study),
            ("finite_difference_grid_study", self.finite_difference_grid_study),
        ):
            if type(study) is not tuple or not study:
                raise TypeError(f"{name} must be a nonempty tuple")
            if any(
                type(item) is not Periodic1DReductionChallengeDiscretizationObservation
                for item in study
            ):
                raise TypeError(f"{name} must contain owned observations")


@dataclass(frozen=True, slots=True)
class Periodic1DReductionChallengeMeshBandIsolationResult:
    """Retain one mesh, band, amplitude, and isolation challenge outcome.

    The gap and overlap diagnose scalar isolated-band applicability on one finite
    representation. Reconstruction and withheld-range errors diagnose distinct
    sampling and truncation channels; they must not be pooled into one error source.
    """

    potential_strength: float
    mesh_size: int
    band_index: int
    isolation_applicable: bool
    minimum_adjacent_gap: float
    minimum_sewn_neighbor_overlap: float
    full_reconstruction_maximum_error: float
    fixed_range_withheld_maximum_error: float

    def __post_init__(self) -> None:
        """Validate exact controls, applicability, and finite diagnostics."""
        self._check_args_discrete_controls()
        self._check_args_diagnostics()

    def _check_args_discrete_controls(self) -> None:
        """Require positive mesh size, nonnegative band index, and exact bool."""
        if type(self.mesh_size) is not int:
            raise TypeError("mesh_size must be a built-in int")
        if self.mesh_size <= 0:
            raise ValueError("mesh_size must be positive")
        if type(self.band_index) is not int:
            raise TypeError("band_index must be a built-in int")
        if self.band_index < 0:
            raise ValueError("band_index must be nonnegative")
        if type(self.isolation_applicable) is not bool:
            raise TypeError("isolation_applicable must be a built-in bool")

    def _check_args_diagnostics(self) -> None:
        """Require all retained diagnostics to be finite nonnegative binary64."""
        for name, value in (
            ("potential_strength", self.potential_strength),
            ("minimum_adjacent_gap", self.minimum_adjacent_gap),
            ("minimum_sewn_neighbor_overlap", self.minimum_sewn_neighbor_overlap),
            (
                "full_reconstruction_maximum_error",
                self.full_reconstruction_maximum_error,
            ),
            (
                "fixed_range_withheld_maximum_error",
                self.fixed_range_withheld_maximum_error,
            ),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not np.isfinite(value):
                raise OverflowError(f"{name} must be finite binary64")
            if value < 0.0:
                raise ValueError(f"{name} must be nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DReductionChallengePotentialShapeCase:
    """Retain diagnostics for one named finite-Fourier potential challenge.

    Parameters use normalized recoil-energy units except the dimensionless
    time-reversal residual. The gap tuple preserves increasing band order.
    """

    identifier: str
    finest_grid_maximum_band_error: float
    minimum_adjacent_gaps: tuple[float, ...]
    time_reversal_energy_residual: float

    def __post_init__(self) -> None:
        """Validate identity, ordered gap inventory, and finite diagnostics."""
        if type(self.identifier) is not str:
            raise TypeError("identifier must be a built-in str")
        if not self.identifier:
            raise ValueError("identifier must be nonempty")
        if type(self.minimum_adjacent_gaps) is not tuple:
            raise TypeError("minimum_adjacent_gaps must be a tuple")
        if not self.minimum_adjacent_gaps:
            raise ValueError("minimum_adjacent_gaps must be nonempty")
        for name, value in (
            ("finest_grid_maximum_band_error", self.finest_grid_maximum_band_error),
            *(("minimum_adjacent_gap", gap) for gap in self.minimum_adjacent_gaps),
            ("time_reversal_energy_residual", self.time_reversal_energy_residual),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not np.isfinite(value):
                raise OverflowError(f"{name} must be finite binary64")
            if value < 0.0:
                raise ValueError(f"{name} must be nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DReductionChallengePotentialShapeResult:
    """Retain potential-shape cases and covariance defects separately."""

    cases: tuple[Periodic1DReductionChallengePotentialShapeCase, ...]
    constant_shift_covariance_maximum_error: float
    translation_isospectral_maximum_error: float

    def __post_init__(self) -> None:
        """Validate unique typed cases and finite covariance defects."""
        self._check_args_cases()
        self._check_args_covariance_defects()

    def _check_args_cases(self) -> None:
        """Require a nonempty unique ordered inventory of exact case records."""
        if type(self.cases) is not tuple or not self.cases:
            raise TypeError("cases must be a nonempty tuple")
        if any(
            type(case) is not Periodic1DReductionChallengePotentialShapeCase
            for case in self.cases
        ):
            raise TypeError("cases must contain owned potential-shape records")
        identifiers = tuple(case.identifier for case in self.cases)
        if len(set(identifiers)) != len(identifiers):
            raise ValueError("shape identifiers must be unique")

    def _check_args_covariance_defects(self) -> None:
        """Require finite nonnegative translation and energy-shift defects."""
        for name, value in (
            (
                "constant_shift_covariance_maximum_error",
                self.constant_shift_covariance_maximum_error,
            ),
            (
                "translation_isospectral_maximum_error",
                self.translation_isospectral_maximum_error,
            ),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not np.isfinite(value):
                raise OverflowError(f"{name} must be finite binary64")
            if value < 0.0:
                raise ValueError(f"{name} must be nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DReductionChallengeGaugeCovarianceResult:
    """Retain deterministic gauge-covariance challenge diagnostics.

    The projector, aligned-frame, and closure-holonomy channels describe distinct
    gauge-dependent or gauge-invariant comparisons. They do not define a retained
    mathematical space by themselves.
    """

    potential_strength: float
    mesh_size: int
    random_phase_projector_maximum_frobenius_defect: float
    parallel_transport_frame_maximum_aligned_defect: float
    closure_holonomy_difference_modulo_2pi: float

    def __post_init__(self) -> None:
        """Validate mesh control and finite nonnegative covariance defects."""
        if type(self.mesh_size) is not int:
            raise TypeError("mesh_size must be a built-in int")
        if self.mesh_size <= 0:
            raise ValueError("mesh_size must be positive")
        for name, value in (
            ("potential_strength", self.potential_strength),
            (
                "random_phase_projector_maximum_frobenius_defect",
                self.random_phase_projector_maximum_frobenius_defect,
            ),
            (
                "parallel_transport_frame_maximum_aligned_defect",
                self.parallel_transport_frame_maximum_aligned_defect,
            ),
            (
                "closure_holonomy_difference_modulo_2pi",
                self.closure_holonomy_difference_modulo_2pi,
            ),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not np.isfinite(value):
                raise OverflowError(f"{name} must be finite binary64")
            if value < 0.0:
                raise ValueError(f"{name} must be nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DReductionChallengeRouteAssumptionResult:
    """Retain defects from complete, incomplete, and reweighted fitting routes.

    The altered routes intentionally change the fitting mathematics. Their nonzero
    defects are observations that expose route assumptions, not failed acceptance
    criteria.
    """

    potential_strength: float
    mesh_size: int
    hopping_range_cells: int
    uniform_complete_coefficient_defect: float
    incomplete_training_coefficient_defect: float
    incomplete_training_comparison_l2_defect: float
    nonuniform_weight_coefficient_defect: float
    nonuniform_weight_comparison_l2_defect: float

    def __post_init__(self) -> None:
        """Validate route controls and finite nonnegative defects."""
        if type(self.mesh_size) is not int:
            raise TypeError("mesh_size must be a built-in int")
        if self.mesh_size <= 0:
            raise ValueError("mesh_size must be positive")
        if type(self.hopping_range_cells) is not int:
            raise TypeError("hopping_range_cells must be a built-in int")
        if self.hopping_range_cells < 0:
            raise ValueError("hopping_range_cells must be nonnegative")
        for name, value in (
            ("potential_strength", self.potential_strength),
            (
                "uniform_complete_coefficient_defect",
                self.uniform_complete_coefficient_defect,
            ),
            (
                "incomplete_training_coefficient_defect",
                self.incomplete_training_coefficient_defect,
            ),
            (
                "incomplete_training_comparison_l2_defect",
                self.incomplete_training_comparison_l2_defect,
            ),
            (
                "nonuniform_weight_coefficient_defect",
                self.nonuniform_weight_coefficient_defect,
            ),
            (
                "nonuniform_weight_comparison_l2_defect",
                self.nonuniform_weight_comparison_l2_defect,
            ),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not np.isfinite(value):
                raise OverflowError(f"{name} must be finite binary64")
            if value < 0.0:
                raise ValueError(f"{name} must be nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DReductionChallengeCampaignResult:
    """Retain all typed challenge channels and the complete source document.

    The source document owns the exact immutable wire. Typed channels are adaptations
    of that document; they are campaign evidence rather than physical models, retained
    spaces, represented operators, effective models, or scientific conclusions.
    """

    source_document: Periodic1DEncodedResultDocument
    potential_amplitude: tuple[
        Periodic1DReductionChallengePotentialAmplitudeResult, ...
    ]
    mesh_band_isolation: tuple[Periodic1DReductionChallengeMeshBandIsolationResult, ...]
    potential_shapes: Periodic1DReductionChallengePotentialShapeResult
    gauge_covariance: Periodic1DReductionChallengeGaugeCovarianceResult
    route_assumptions: Periodic1DReductionChallengeRouteAssumptionResult

    def __post_init__(self) -> None:
        """Validate the exact source kind and typed channel ownership."""
        self._check_args_source_document()
        self._check_args_repeated_channels()
        self._check_args_single_channels()

    def _check_args_source_document(self) -> None:
        """Require the historical reduction-challenge result wire kind."""
        if type(self.source_document) is not Periodic1DEncodedResultDocument:
            raise TypeError("source_document must be Periodic1DEncodedResultDocument")
        # STRESS is the immutable schema-one wire discriminator. It is not the
        # canonical scientific or software name of this campaign family.
        if self.source_document.kind is not Periodic1DEncodedResultKind.STRESS:
            raise ValueError("source_document must use the historical stress wire kind")
        if self.source_document.evidence_status != "illustrative numerical stress test":
            raise ValueError("source_document has an unexpected evidence status")

    def _check_args_repeated_channels(self) -> None:
        """Require nonempty exact amplitude and mesh/band channel inventories."""
        if type(self.potential_amplitude) is not tuple or not self.potential_amplitude:
            raise TypeError("potential_amplitude must be a nonempty tuple")
        if any(
            type(item) is not Periodic1DReductionChallengePotentialAmplitudeResult
            for item in self.potential_amplitude
        ):
            raise TypeError("potential_amplitude contains the wrong result type")
        if type(self.mesh_band_isolation) is not tuple or not self.mesh_band_isolation:
            raise TypeError("mesh_band_isolation must be a nonempty tuple")
        if any(
            type(item) is not Periodic1DReductionChallengeMeshBandIsolationResult
            for item in self.mesh_band_isolation
        ):
            raise TypeError("mesh_band_isolation contains the wrong result type")

    def _check_args_single_channels(self) -> None:
        """Require exact shape, gauge, and route result owners."""
        if (
            type(self.potential_shapes)
            is not Periodic1DReductionChallengePotentialShapeResult
        ):
            raise TypeError("potential_shapes uses the wrong result type")
        if (
            type(self.gauge_covariance)
            is not Periodic1DReductionChallengeGaugeCovarianceResult
        ):
            raise TypeError("gauge_covariance uses the wrong result type")
        if (
            type(self.route_assumptions)
            is not Periodic1DReductionChallengeRouteAssumptionResult
        ):
            raise TypeError("route_assumptions uses the wrong result type")


class Periodic1DReductionChallengeResultJsonSerializer(
    JsonCodec[Periodic1DReductionChallengeCampaignResult, bytes]
):
    """Adapt retained historical result bytes to typed challenge channels.

    Serialization returns the complete correlated source document. It does not derive a
    new result from typed diagnostics and therefore cannot silently change provenance,
    evidence status, or historical wire fields.
    """

    __slots__ = ()

    retained = Periodic1DEncodedResultJsonSerializer(Periodic1DEncodedResultKind.STRESS)

    @staticmethod
    def _check_fields(
        value: ImmutableJsonObject, expected: frozenset[str], context: str
    ) -> None:
        """Require one exact closed version-one object field set."""
        observed = frozenset(name for name, _ in value.fields)
        if observed != expected:
            raise ValueError(f"{context} fields must match schema version one")

    def _check_root_contract(self, root: ImmutableJsonObject) -> None:
        """Require the complete closed root, status, and provenance contract."""
        self._check_fields(
            root,
            frozenset(
                {
                    "schema_version",
                    "experiment_id",
                    "evidence_status",
                    "calculation_status",
                    "claim_boundary",
                    "provenance",
                    "potential_amplitude_stress",
                    "mesh_band_and_isolation_stress",
                    "potential_shape_stress",
                    "gauge_covariance_stress",
                    "route_assumption_stress",
                }
            ),
            "reduction-challenge result",
        )
        if (
            self.retained.string_field(root, "evidence_status")
            != "illustrative numerical stress test"
        ):
            raise ValueError("unexpected evidence_status")
        self.retained.string_field(root, "calculation_status")
        self.retained.string_field(root, "claim_boundary")
        provenance = self.retained.object_field(root, "provenance")
        self._check_fields(
            provenance,
            frozenset(
                {
                    "floating_point",
                    "input_path",
                    "input_sha256",
                    "numpy_version",
                    "python_version",
                    "script_path",
                    "script_sha256",
                }
            ),
            "reduction-challenge provenance",
        )
        for name in (
            "floating_point",
            "input_path",
            "numpy_version",
            "python_version",
            "script_path",
        ):
            self.retained.string_field(provenance, name)
        for name in ("input_sha256", "script_sha256"):
            digest = self.retained.string_field(provenance, name)
            if len(digest) != 64 or any(
                character not in "0123456789abcdef" for character in digest
            ):
                raise ValueError(f"{name} must be lowercase SHA-256 hexadecimal")

    def deserialize(self, payload: bytes) -> Periodic1DReductionChallengeCampaignResult:
        """Decode the complete wire and extract every typed challenge channel.

        Parameters
        ----------
        payload
            Exact historical schema-one result bytes.

        Returns
        -------
        Periodic1DReductionChallengeCampaignResult
            Immutable source document and typed channel adaptations.

        Raises
        ------
        TypeError
            If the payload or a decoded field has the wrong representation.
        ValueError
            If strict JSON, schema, required fields, or intrinsic values are invalid.
        OverflowError
            If a retained diagnostic is not finite binary64.
        """
        try:
            document = self.retained.deserialize(payload)
        except KeyError as error:
            raise ValueError(
                "reduction-challenge result is missing a required routing field"
            ) from error
        root = document.root
        self._check_root_contract(root)
        # Explicit historical-key mapping preserves the wire without exposing its
        # misleading terminology as canonical Python attribute names.
        return Periodic1DReductionChallengeCampaignResult(
            document,
            tuple(
                self._deserialize_amplitude(item)
                for item in self.retained.object_array_field(
                    root, "potential_amplitude_stress"
                )
            ),
            tuple(
                self._deserialize_mesh_band(item)
                for item in self.retained.object_array_field(
                    root, "mesh_band_and_isolation_stress"
                )
            ),
            self._deserialize_potential_shapes(
                self.retained.object_field(root, "potential_shape_stress")
            ),
            self._deserialize_gauge_covariance(
                self.retained.object_field(root, "gauge_covariance_stress")
            ),
            self._deserialize_route_assumptions(
                self.retained.object_field(root, "route_assumption_stress")
            ),
        )

    def serialize(self, value: Periodic1DReductionChallengeCampaignResult) -> bytes:
        """Encode the complete correlated source document canonically.

        Parameters
        ----------
        value
            Exact typed reduction-challenge campaign result.

        Returns
        -------
        bytes
            Canonical encoding of ``value.source_document``.

        Raises
        ------
        TypeError
            If ``value`` is not the exact campaign-result type.
        ValueError
            If the source document cannot be encoded under its closed wire contract.
        """
        if type(value) is not Periodic1DReductionChallengeCampaignResult:
            raise TypeError("value must be Periodic1DReductionChallengeCampaignResult")
        return self.retained.serialize(value.source_document)

    def _deserialize_amplitude(
        self, value: ImmutableJsonObject
    ) -> Periodic1DReductionChallengePotentialAmplitudeResult:
        """Decode one historical amplitude-channel record."""
        self._check_fields(
            value,
            frozenset(
                {
                    "potential_strength",
                    "zone_boundary_gap",
                    "isolated_band_status",
                    "potential_sign_invariance_maximum_error",
                    "plane_wave_cutoff_study",
                    "finite_difference_grid_study",
                }
            ),
            "potential-amplitude observation",
        )
        return Periodic1DReductionChallengePotentialAmplitudeResult(
            self.retained.real_field(value, "potential_strength"),
            self.retained.real_field(value, "zone_boundary_gap"),
            self.retained.string_field(value, "isolated_band_status"),
            self.retained.real_field(value, "potential_sign_invariance_maximum_error"),
            tuple(
                self._deserialize_discretization(item, "cutoff")
                for item in self.retained.object_array_field(
                    value, "plane_wave_cutoff_study"
                )
            ),
            tuple(
                self._deserialize_discretization(item, "points")
                for item in self.retained.object_array_field(
                    value, "finite_difference_grid_study"
                )
            ),
        )

    def _deserialize_discretization(
        self, value: ImmutableJsonObject, resolution_field: str
    ) -> Periodic1DReductionChallengeDiscretizationObservation:
        """Decode one finite-representation observation."""
        self._check_fields(
            value,
            frozenset({resolution_field, "maximum_low_band_error"}),
            f"{resolution_field} discretization observation",
        )
        return Periodic1DReductionChallengeDiscretizationObservation(
            self.retained.integer_field(value, resolution_field),
            self.retained.real_field(value, "maximum_low_band_error"),
        )

    def _deserialize_mesh_band(
        self, value: ImmutableJsonObject
    ) -> Periodic1DReductionChallengeMeshBandIsolationResult:
        """Decode one mesh, band, and isolation challenge record."""
        self._check_fields(
            value,
            frozenset(
                {
                    "potential_strength",
                    "mesh_size",
                    "band_index",
                    "isolation_applicable",
                    "minimum_adjacent_gap",
                    "minimum_sewn_neighbor_overlap",
                    "full_reconstruction_maximum_error",
                    "fixed_range_withheld_maximum_error",
                }
            ),
            "mesh-band-isolation observation",
        )
        return Periodic1DReductionChallengeMeshBandIsolationResult(
            self.retained.real_field(value, "potential_strength"),
            self.retained.integer_field(value, "mesh_size"),
            self.retained.integer_field(value, "band_index"),
            self.retained.boolean_field(value, "isolation_applicable"),
            self.retained.real_field(value, "minimum_adjacent_gap"),
            self.retained.real_field(value, "minimum_sewn_neighbor_overlap"),
            self.retained.real_field(value, "full_reconstruction_maximum_error"),
            self.retained.real_field(value, "fixed_range_withheld_maximum_error"),
        )

    def _deserialize_potential_shapes(
        self, value: ImmutableJsonObject
    ) -> Periodic1DReductionChallengePotentialShapeResult:
        """Decode all named potential-shape challenge records."""
        self._check_fields(
            value,
            frozenset(
                {
                    "cases",
                    "constant_shift_covariance_maximum_error",
                    "translation_isospectral_maximum_error",
                }
            ),
            "potential-shape result",
        )
        return Periodic1DReductionChallengePotentialShapeResult(
            tuple(
                self._deserialize_potential_shape_case(item)
                for item in self.retained.object_array_field(value, "cases")
            ),
            self.retained.real_field(value, "constant_shift_covariance_maximum_error"),
            self.retained.real_field(value, "translation_isospectral_maximum_error"),
        )

    def _deserialize_potential_shape_case(
        self, value: ImmutableJsonObject
    ) -> Periodic1DReductionChallengePotentialShapeCase:
        """Decode one named potential-shape challenge case."""
        self._check_fields(
            value,
            frozenset(
                {
                    "id",
                    "finest_grid_maximum_band_error",
                    "minimum_adjacent_gaps",
                    "time_reversal_energy_residual",
                }
            ),
            "potential-shape case",
        )
        gaps = self.retained.real_vector_field(value, "minimum_adjacent_gaps")
        return Periodic1DReductionChallengePotentialShapeCase(
            self.retained.string_field(value, "id"),
            self.retained.real_field(value, "finest_grid_maximum_band_error"),
            tuple(float(item) for item in gaps),
            self.retained.real_field(value, "time_reversal_energy_residual"),
        )

    def _deserialize_gauge_covariance(
        self, value: ImmutableJsonObject
    ) -> Periodic1DReductionChallengeGaugeCovarianceResult:
        """Decode projector, frame, and closure gauge-covariance diagnostics."""
        self._check_fields(
            value,
            frozenset(
                {
                    "potential_strength",
                    "mesh_size",
                    "random_phase_projector_maximum_frobenius_defect",
                    "parallel_transport_frame_maximum_aligned_defect",
                    "closure_holonomy_difference_modulo_2pi",
                }
            ),
            "gauge-covariance result",
        )
        return Periodic1DReductionChallengeGaugeCovarianceResult(
            self.retained.real_field(value, "potential_strength"),
            self.retained.integer_field(value, "mesh_size"),
            self.retained.real_field(
                value, "random_phase_projector_maximum_frobenius_defect"
            ),
            self.retained.real_field(
                value, "parallel_transport_frame_maximum_aligned_defect"
            ),
            self.retained.real_field(value, "closure_holonomy_difference_modulo_2pi"),
        )

    def _deserialize_route_assumptions(
        self, value: ImmutableJsonObject
    ) -> Periodic1DReductionChallengeRouteAssumptionResult:
        """Decode complete, incomplete, and reweighted fitting-route diagnostics."""
        self._check_fields(
            value,
            frozenset(
                {
                    "potential_strength",
                    "mesh_size",
                    "hopping_range_cells",
                    "uniform_complete_coefficient_defect",
                    "incomplete_training_coefficient_defect",
                    "incomplete_training_comparison_l2_defect",
                    "nonuniform_weight_coefficient_defect",
                    "nonuniform_weight_comparison_l2_defect",
                }
            ),
            "route-assumption result",
        )
        return Periodic1DReductionChallengeRouteAssumptionResult(
            self.retained.real_field(value, "potential_strength"),
            self.retained.integer_field(value, "mesh_size"),
            self.retained.integer_field(value, "hopping_range_cells"),
            self.retained.real_field(value, "uniform_complete_coefficient_defect"),
            self.retained.real_field(value, "incomplete_training_coefficient_defect"),
            self.retained.real_field(value, "incomplete_training_comparison_l2_defect"),
            self.retained.real_field(value, "nonuniform_weight_coefficient_defect"),
            self.retained.real_field(value, "nonuniform_weight_comparison_l2_defect"),
        )
