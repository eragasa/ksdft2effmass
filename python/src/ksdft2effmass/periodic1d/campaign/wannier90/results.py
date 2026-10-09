"""Typed observations adapted from retained Appendix G Wannier90 result wires.

The configured serializer preserves the complete exact source document, enforces the
closed version-one schema, and reconstructs only the documented circular Wilson-center
comparison. Retained localization and convergence statuses remain observations; they
are never derived from names, spectra, or artifact presence.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.integration.wannier90 import Wannier90NativeArtifactIdentity
from ksdft2effmass.periodic1d.campaign.result_documents import (
    Periodic1DEncodedResultDocument,
    Periodic1DEncodedResultJsonSerializer,
    Periodic1DEncodedResultKind,
)
from ksdft2effmass.periodic1d.campaign.serialization import (
    Periodic1DCampaignJsonDecoder,
)
from ksdft2effmass.serialization import JsonCodec
from ksdft2effmass.serialization.json import ImmutableJsonObject
from ksdft2effmass.solid_state import (
    WilsonCenterConvention1D,
    WilsonLoopPhaseSetComparator1D,
    WilsonLoopPhaseSetComparisonResult1D,
    WilsonLoopSpectrum1D,
    WilsonLoopSpectrumCanonicalizer1D,
)

_ROOT_FIELDS = frozenset(
    {
        "checkpoint_ids",
        "claim_boundary",
        "evidence_status",
        "executable",
        "experiment_id",
        "groups",
        "interface_conventions",
        "provenance",
        "schema_version",
    }
)
_GROUP_FIELDS = frozenset(
    {
        "aligned_direct_vs_wannier90_hopping_l2_defect",
        "artifact_identities",
        "band_indices",
        "center_set_circular_maximum_defect",
        "centers_cell_coordinates",
        "convergence_criterion_satisfied",
        "direct_wilson_centers_by_phase_convention",
        "direct_wilson_eigenphases",
        "hr_matrix_maximum_defect_from_u_matrix_transform",
        "hr_training_eigenvalue_maximum_error",
        "id",
        "iterations",
        "localization_status",
        "omega_components_cell_squared",
        "pointwise_alignment_frame_maximum_frobenius_defect",
        "pointwise_alignment_operator_maximum_frobenius_defect",
        "preprocessing_status",
        "range_study",
        "spreads_cell_squared",
        "u_matrices",
        "u_matrix_unitarity_maximum_frobenius_defect",
        "unaligned_direct_vs_wannier90_hopping_l2_defect",
        "wannier90_represented_eigenvalue_maximum_defect",
    }
)
_ARTIFACT_IDENTITY_FIELDS = frozenset({"bytes", "name", "sha256"})
_EXECUTABLE_FIELDS = frozenset({"documented_sha256", "name", "version"})
_INTERFACE_FIELDS = frozenset(
    {
        "active_lattice_mapping",
        "energy_mapping",
        "inactive_embedding",
        "num_iter",
        "preconditioned",
        "search_shells",
        "trial_projections",
    }
)
_PROVENANCE_FIELDS = frozenset(
    {
        "composite_input_path",
        "composite_input_sha256",
        "external_run_identity",
        "extractor_path",
        "extractor_sha256",
    }
)
_OMEGA_FIELDS = frozenset({"omega_d", "omega_i", "omega_od", "omega_total"})
_RANGE_STUDY_FIELDS = frozenset(
    {
        "hopping_range_cells",
        "wannier90_omitted_block_l2_norm",
        "wannier90_training_eigenvalue_maximum_error",
    }
)


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90WilsonGroupResult:
    """Retain direct Wilson phases and their comparison with Wannier90 centers.

    Parameters
    ----------
    group_id, band_indices
        Explicit group key and ordered selected zero-based parent-band inventory.
    direct_spectrum, direct_centers_over_period
        Canonical direct Wilson spectrum and centers under the explicit
        phase-over-``2*pi`` convention.
    wannier90_centers_cell_coordinates
        Retained three-coordinate centers; only the active first coordinate enters the
        periodic-1D phase comparison.
    center_phase_comparison
        Reconstructed circular assignment between direct phases and center phases.
    recorded_center_set_circular_maximum_defect
        Retained maximum circular center defect in unit-cell fractions.
    artifact_identities
        Nonempty unique logical native-artifact identity inventory.
    localization_status, convergence_criterion_satisfied
        Retained producer observations; neither is inferred by this Result.

    Raises
    ------
    TypeError
        If a semantic record, tuple member, status Boolean, or identity has the wrong
        exact representation.
    ValueError
        If identities, ranks, centers, conventions, circular defect algebra, or
        retained status text violate intrinsic invariants.

    Notes
    -----
    Inactive center coordinates remain explicit and are not silently pooled into the
    one-dimensional comparison. This Result validates retained algebra but does not
    prove a historical Action execution or scientific convergence.
    """

    group_id: str
    band_indices: tuple[int, ...]
    direct_spectrum: WilsonLoopSpectrum1D
    direct_centers_over_period: tuple[float, ...]
    wannier90_centers_cell_coordinates: tuple[tuple[float, float, float], ...]
    center_phase_comparison: WilsonLoopPhaseSetComparisonResult1D
    recorded_center_set_circular_maximum_defect: float
    artifact_identities: tuple[Wannier90NativeArtifactIdentity, ...]
    localization_status: str
    convergence_criterion_satisfied: bool

    def __post_init__(self) -> None:
        """Validate intrinsic rank, convention, comparison, and evidence invariants."""
        self._check_args_group_identity()
        self._check_args_direct_observations()
        self._check_args_wannier90_centers()
        self._check_args_center_comparison()
        self._check_args_artifact_identities()
        self._check_args_status()

    def _check_args_group_identity(self) -> None:
        """Require an explicit group ID and ordered nonnegative band inventory."""
        if type(self.group_id) is not str or not self.group_id:
            raise ValueError("group_id must be a nonempty built-in str")
        if (
            type(self.band_indices) is not tuple
            or not self.band_indices
            or any(type(index) is not int or index < 0 for index in self.band_indices)
        ):
            raise ValueError(
                "band_indices must be a nonempty tuple of nonnegative ints"
            )

    def _check_args_direct_observations(self) -> None:
        """Require rank-consistent direct phases and convention-derived centers."""
        if type(self.direct_spectrum) is not WilsonLoopSpectrum1D:
            raise TypeError("direct_spectrum must be WilsonLoopSpectrum1D")
        rank = len(self.band_indices)
        if self.direct_spectrum.rank != rank:
            raise ValueError(
                "direct Wilson spectrum rank must equal retained band count"
            )
        if (
            type(self.direct_centers_over_period) is not tuple
            or len(self.direct_centers_over_period) != rank
            or any(
                type(center) is not float or not np.isfinite(center)
                for center in self.direct_centers_over_period
            )
        ):
            raise ValueError("direct centers must be a finite built-in float tuple")
        expected_direct = self.direct_spectrum.centers_over_period(
            WilsonCenterConvention1D.PHASE_OVER_TWO_PI
        )
        if not np.allclose(
            self.direct_centers_over_period,
            expected_direct,
            rtol=0.0,
            atol=1.0e-15,
        ):
            raise ValueError("direct centers do not agree with the phase convention")

    def _check_args_wannier90_centers(self) -> None:
        """Require one finite retained three-coordinate center per selected band."""
        if (
            type(self.wannier90_centers_cell_coordinates) is not tuple
            or len(self.wannier90_centers_cell_coordinates) != len(self.band_indices)
            or any(
                type(center) is not tuple
                or len(center) != 3
                or any(
                    type(value) is not float or not np.isfinite(value)
                    for value in center
                )
                for center in self.wannier90_centers_cell_coordinates
            )
        ):
            raise ValueError("Wannier90 centers must be finite Cartesian triples")

    def _check_args_center_comparison(self) -> None:
        """Require exact spectrum correlation and retained circular-defect algebra."""
        if (
            type(self.center_phase_comparison)
            is not WilsonLoopPhaseSetComparisonResult1D
        ):
            raise TypeError(
                "center_phase_comparison uses the wrong AbstractResultObject"
            )
        if self.center_phase_comparison.reference != self.direct_spectrum:
            raise ValueError("center comparison reference must be the direct spectrum")
        defect = self.recorded_center_set_circular_maximum_defect
        if type(defect) is not float or not np.isfinite(defect) or defect < 0.0:
            raise ValueError("recorded center defect must be finite and nonnegative")
        reconstructed = self.center_phase_comparison.maximum_absolute_phase_defect / (
            2.0 * np.pi
        )
        if not np.isclose(reconstructed, defect, rtol=0.0, atol=1.0e-15):
            raise ValueError(
                "recorded center defect does not match circular comparison"
            )

    def _check_args_artifact_identities(self) -> None:
        """Require nonempty typed identities with unique explicit logical names."""
        if (
            type(self.artifact_identities) is not tuple
            or not self.artifact_identities
            or any(
                type(identity) is not Wannier90NativeArtifactIdentity
                for identity in self.artifact_identities
            )
        ):
            raise TypeError("artifact_identities must be a nonempty typed tuple")
        artifact_names = tuple(identity.name for identity in self.artifact_identities)
        if len(set(artifact_names)) != len(artifact_names):
            raise ValueError("native artifact names must be unique")

    def _check_args_status(self) -> None:
        """Require explicit retained localization text and convergence Boolean."""
        if type(self.localization_status) is not str or not self.localization_status:
            raise ValueError("localization_status must be a nonempty built-in str")
        if type(self.convergence_criterion_satisfied) is not bool:
            raise TypeError("convergence_criterion_satisfied must be a built-in bool")


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90CampaignResult:
    """Retain typed Wilson-center outcomes and one complete Wannier90 document.

    Parameters
    ----------
    source_document
        Complete immutable source tree, exact source bytes, explicit wire kind, and
        derived SHA-256 content identity.
    groups
        Nonempty unique ordered Wilson group Results.

    Raises
    ------
    TypeError
        If the source or group records have wrong exact semantic types.
    ValueError
        If the source kind is unsupported or group identities repeat.

    Notes
    -----
    Source retention and intrinsic validation do not establish execution provenance,
    native-file presence, convergence, scientific validation, UQ, or acceptance.
    """

    source_document: Periodic1DEncodedResultDocument
    groups: tuple[Periodic1DWannier90WilsonGroupResult, ...]

    def __post_init__(self) -> None:
        """Validate source-wire ownership and the ordered typed group inventory."""
        self._check_args_source_document()
        self._check_args_groups()

    def _check_args_source_document(self) -> None:
        """Require a retained document with an explicit supported result kind."""
        if type(self.source_document) is not Periodic1DEncodedResultDocument:
            raise TypeError("source_document must be Periodic1DEncodedResultDocument")
        if self.source_document.kind not in {
            Periodic1DEncodedResultKind.WANNIER90,
            Periodic1DEncodedResultKind.WANNIER90_PRECONDITIONED,
        }:
            raise ValueError("source_document must be a retained Wannier90 result")

    def _check_args_groups(self) -> None:
        """Require nonempty exact group records with unique explicit identifiers."""
        if (
            type(self.groups) is not tuple
            or not self.groups
            or any(
                type(group) is not Periodic1DWannier90WilsonGroupResult
                for group in self.groups
            )
        ):
            raise TypeError("groups must be a nonempty typed tuple")
        group_ids = tuple(group.group_id for group in self.groups)
        if len(set(group_ids)) != len(group_ids):
            raise ValueError("Wannier90 group identifiers must be unique")


class Periodic1DWannier90ResultJsonSerializer(
    JsonCodec[Periodic1DWannier90CampaignResult, bytes]
):
    """Adapt one explicit retained Wannier90 wire kind to typed observations.

    The configured result kind selects a schema before adaptation; it is never inferred
    from content, identifiers, paths, filenames, group ranks, spectra, or native-file
    presence. After schema selection, the source preconditioning declaration must agree
    with that explicit kind, so one valid variant cannot be relabeled as the other.
    Version-one schema-owned objects are closed. Deserialization preserves
    the complete source document and reconstructs circular center comparison with
    request-scoped stateless Actions. For :math:`N_k` retained complex matrices of
    rank :math:`r`, strict matrix adaptation uses :math:`O(N_k r^2)` time and temporary
    dense storage. No arbitrary size cap is imposed; decoding may raise
    :class:`MemoryError`.
    """

    __slots__ = ("retained",)

    def __init__(self, kind: Periodic1DEncodedResultKind) -> None:
        """Bind the adapter to original or preconditioned retained result bytes."""
        if type(kind) is not Periodic1DEncodedResultKind:
            raise TypeError("kind must be Periodic1DEncodedResultKind")
        if kind not in {
            Periodic1DEncodedResultKind.WANNIER90,
            Periodic1DEncodedResultKind.WANNIER90_PRECONDITIONED,
        }:
            raise ValueError("kind must identify a supported Wannier90 result")
        self.retained = Periodic1DEncodedResultJsonSerializer(kind)

    def deserialize(self, payload: bytes) -> Periodic1DWannier90CampaignResult:
        """Decode the closed source schema and reconstruct Wilson comparisons.

        Parameters
        ----------
        payload
            Exact built-in UTF-8 JSON bytes for the configured result kind.

        Returns
        -------
        Periodic1DWannier90CampaignResult
            Complete immutable source document plus typed group observations.

        Raises
        ------
        TypeError
            If the wire or a decoded primitive has the wrong exact representation.
        ValueError
            If strict JSON decoding, the closed schema, or retained algebra fails.
        UnicodeDecodeError
            If ``payload`` is not valid UTF-8.
        OverflowError
            If an integer component cannot be represented as finite binary64.
        MemoryError
            If the decoded tree or a dense intermediate cannot be allocated.
        RecursionError
            If the document exceeds parser recursion limits.
        """
        document = self.retained.deserialize(payload)
        self._check_exact_fields(document.root, _ROOT_FIELDS, "Wannier90 result")
        self._check_exact_fields(
            self.retained.object_field(document.root, "executable"),
            _EXECUTABLE_FIELDS,
            "Wannier90 executable",
        )
        self._check_exact_fields(
            self.retained.object_field(document.root, "interface_conventions"),
            _INTERFACE_FIELDS,
            "Wannier90 interface conventions",
        )
        self._check_exact_fields(
            self.retained.object_field(document.root, "provenance"),
            _PROVENANCE_FIELDS,
            "Wannier90 provenance",
        )
        self._validate_root_values(document.root)
        self._check_result_variant(document.root)
        return Periodic1DWannier90CampaignResult(
            document,
            tuple(
                self._decode_group(group)
                for group in self.retained.object_array_field(document.root, "groups")
            ),
        )

    def serialize(self, value: Periodic1DWannier90CampaignResult) -> bytes:
        """Encode the complete retained source tree as canonical JSON.

        Parameters
        ----------
        value
            Exact typed campaign result whose source document has the configured kind.

        Returns
        -------
        bytes
            Sorted, compact, newline-terminated UTF-8 JSON. It need not preserve the
            retained source's insignificant whitespace or original field order.

        Raises
        ------
        TypeError
            If ``value`` has the wrong exact semantic type.
        ValueError
            If its retained source kind or intrinsic source correlation is invalid.
        MemoryError
            If canonical encoding cannot allocate its output buffer.
        RecursionError
            If the immutable tree exceeds encoder recursion limits.
        """
        if type(value) is not Periodic1DWannier90CampaignResult:
            raise TypeError("value must be Periodic1DWannier90CampaignResult")
        return self.retained.serialize(value.source_document)

    def _decode_group(
        self, value: ImmutableJsonObject
    ) -> Periodic1DWannier90WilsonGroupResult:
        """Extract one closed group record and reconstruct its phase comparison."""
        self._check_exact_fields(value, _GROUP_FIELDS, "Wannier90 group")
        self._check_exact_fields(
            self.retained.object_field(value, "omega_components_cell_squared"),
            _OMEGA_FIELDS,
            "Wannier90 omega components",
        )
        for range_item in self.retained.object_array_field(value, "range_study"):
            self._check_exact_fields(
                range_item, _RANGE_STUDY_FIELDS, "Wannier90 range-study item"
            )
        self._validate_group_values(value)
        direct_phases = self.retained.real_vector_field(
            value, "direct_wilson_eigenphases"
        )
        direct_spectrum = WilsonLoopSpectrumCanonicalizer1D().execute(
            tuple(float(phase) for phase in direct_phases)
        )
        direct_centers = tuple(
            float(center)
            for center in self.retained.real_vector_field(
                value, "direct_wilson_centers_by_phase_convention"
            )
        )
        wannier90_centers = self._decode_center_coordinates(value)
        center_phase_spectrum = WilsonLoopSpectrumCanonicalizer1D().execute(
            tuple(center[0] * 2.0 * np.pi for center in wannier90_centers)
        )
        recorded_defect = self.retained.real_field(
            value, "center_set_circular_maximum_defect"
        )
        comparison = WilsonLoopPhaseSetComparator1D().execute(
            direct_spectrum,
            center_phase_spectrum,
            recorded_defect * 2.0 * np.pi + 1.0e-14,
        )
        return Periodic1DWannier90WilsonGroupResult(
            self.retained.string_field(value, "id"),
            self.retained.integer_tuple_field(value, "band_indices"),
            direct_spectrum,
            direct_centers,
            wannier90_centers,
            comparison,
            recorded_defect,
            tuple(
                self._decode_artifact_identity(identity)
                for identity in self.retained.object_array_field(
                    value, "artifact_identities"
                )
            ),
            self.retained.string_field(value, "localization_status"),
            self.retained.boolean_field(value, "convergence_criterion_satisfied"),
        )

    def _decode_artifact_identity(
        self, value: ImmutableJsonObject
    ) -> Wannier90NativeArtifactIdentity:
        """Decode one closed native-artifact identity record."""
        self._check_exact_fields(
            value, _ARTIFACT_IDENTITY_FIELDS, "Wannier90 artifact identity"
        )
        return Wannier90NativeArtifactIdentity(
            self.retained.string_field(value, "name"),
            self.retained.integer_field(value, "bytes"),
            self.retained.string_field(value, "sha256"),
        )

    def _validate_root_values(self, root: ImmutableJsonObject) -> None:
        """Validate every schema-owned root, interface, and provenance value."""
        for index, checkpoint in enumerate(
            self.retained.array(root.field("checkpoint_ids"), "checkpoint_ids").values
        ):
            self.retained.string(checkpoint, f"checkpoint_ids[{index}]")
        for name in ("claim_boundary", "evidence_status", "experiment_id"):
            self.retained.string_field(root, name)
        executable = self.retained.object_field(root, "executable")
        self.retained.string_field(executable, "name")
        self.retained.string_field(executable, "version")
        Periodic1DCampaignJsonDecoder().sha256(
            self.retained.string_field(executable, "documented_sha256"),
            "executable.documented_sha256",
        )
        interface = self.retained.object_field(root, "interface_conventions")
        for name in (
            "active_lattice_mapping",
            "energy_mapping",
            "inactive_embedding",
            "trial_projections",
        ):
            self.retained.string_field(interface, name)
        for name in ("num_iter", "search_shells"):
            if self.retained.integer_field(interface, name) < 0:
                raise ValueError(f"interface_conventions.{name} must be nonnegative")
        self.retained.boolean_field(interface, "preconditioned")
        provenance = self.retained.object_field(root, "provenance")
        for name in (
            "composite_input_path",
            "external_run_identity",
            "extractor_path",
        ):
            self.retained.string_field(provenance, name)
        decoder = Periodic1DCampaignJsonDecoder()
        for name in ("composite_input_sha256", "extractor_sha256"):
            decoder.sha256(
                self.retained.string_field(provenance, name), f"provenance.{name}"
            )

    def _check_result_variant(self, root: ImmutableJsonObject) -> None:
        """Correlate the explicit wire kind with the source variant declaration.

        The discriminator still selects the schema before adaptation. This subsequent
        check prevents a caller from relabeling one valid Wannier90 variant as the
        other while retaining otherwise schema-compatible content.

        Raises
        ------
        ValueError
            If ``interface_conventions.preconditioned`` contradicts the configured
            explicit result kind.
        """
        interface = self.retained.object_field(root, "interface_conventions")
        observed = self.retained.boolean_field(interface, "preconditioned")
        expected = (
            self.retained.kind is Periodic1DEncodedResultKind.WANNIER90_PRECONDITIONED
        )
        if observed is not expected:
            raise ValueError(
                "interface preconditioning does not agree with the result kind"
            )

    def _validate_group_values(self, group: ImmutableJsonObject) -> None:
        """Validate every schema-owned group diagnostic and nested record value."""
        for name in ("id", "localization_status", "preprocessing_status"):
            self.retained.string_field(group, name)
        if self.retained.integer_field(group, "iterations") < 0:
            raise ValueError("iterations must be nonnegative")
        self.retained.boolean_field(group, "convergence_criterion_satisfied")
        self.retained.integer_tuple_field(group, "band_indices")
        for name in (
            "direct_wilson_eigenphases",
            "direct_wilson_centers_by_phase_convention",
            "spreads_cell_squared",
        ):
            self.retained.real_vector_field(group, name)
        self._decode_center_coordinates(group)
        self.retained.complex_matrix_array_field(group, "u_matrices")
        nonnegative_fields = (
            "aligned_direct_vs_wannier90_hopping_l2_defect",
            "center_set_circular_maximum_defect",
            "hr_matrix_maximum_defect_from_u_matrix_transform",
            "hr_training_eigenvalue_maximum_error",
            "pointwise_alignment_frame_maximum_frobenius_defect",
            "pointwise_alignment_operator_maximum_frobenius_defect",
            "u_matrix_unitarity_maximum_frobenius_defect",
            "unaligned_direct_vs_wannier90_hopping_l2_defect",
            "wannier90_represented_eigenvalue_maximum_defect",
        )
        for name in nonnegative_fields:
            if self.retained.real_field(group, name) < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        omega = self.retained.object_field(group, "omega_components_cell_squared")
        for name in _OMEGA_FIELDS:
            if self.retained.real_field(omega, name) < 0.0:
                raise ValueError(f"omega_components_cell_squared.{name} is negative")
        for item in self.retained.object_array_field(group, "range_study"):
            if self.retained.integer_field(item, "hopping_range_cells") < 0:
                raise ValueError("hopping_range_cells must be nonnegative")
            for name in (
                "wannier90_omitted_block_l2_norm",
                "wannier90_training_eigenvalue_maximum_error",
            ):
                if self.retained.real_field(item, name) < 0.0:
                    raise ValueError(f"{name} must be nonnegative")
        decoder = Periodic1DCampaignJsonDecoder()
        for identity in self.retained.object_array_field(group, "artifact_identities"):
            self.retained.string_field(identity, "name")
            if self.retained.integer_field(identity, "bytes") < 0:
                raise ValueError("artifact bytes must be nonnegative")
            decoder.sha256(
                self.retained.string_field(identity, "sha256"), "artifact sha256"
            )

    @staticmethod
    def _check_exact_fields(
        value: ImmutableJsonObject, expected: frozenset[str], name: str
    ) -> None:
        """Reject every missing or unknown field in one schema-owned object.

        Parameters
        ----------
        value
            Immutable decoded JSON object.
        expected
            Complete field inventory for this schema location.
        name
            Human-readable object name used in diagnostics.

        Raises
        ------
        ValueError
            If the decoded field set differs from the closed schema.
        """
        observed = frozenset(key for key, _ in value.fields)
        if observed != expected:
            missing = sorted(expected - observed)
            unknown = sorted(observed - expected)
            raise ValueError(
                f"{name} fields must match the closed schema; "
                f"missing={missing}, unknown={unknown}"
            )

    def _decode_center_coordinates(
        self, value: ImmutableJsonObject
    ) -> tuple[tuple[float, float, float], ...]:
        """Decode retained Wannier90 center triples in cell coordinates."""
        array = self.retained.array(
            value.field("centers_cell_coordinates"), "centers_cell_coordinates"
        )
        centers: list[tuple[float, float, float]] = []
        for index, item in enumerate(array.values):
            triple = self.retained.array(item, f"centers_cell_coordinates[{index}]")
            if len(triple.values) != 3:
                raise ValueError("each Wannier90 center must contain three coordinates")
            centers.append(
                (
                    self.retained.real(triple.values[0], "center.x"),
                    self.retained.real(triple.values[1], "center.y"),
                    self.retained.real(triple.values[2], "center.z"),
                )
            )
        return tuple(centers)
