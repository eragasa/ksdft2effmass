"""Typed retained results for the Appendix G composite-band campaign.

The records in this module expose the demonstrated version-one composite result as
immutable campaign outcomes while preserving the complete source document.  Dense
rank-two reciprocal Hamiltonians and hopping blocks use the reusable represented-
operator contracts.  Gap, gauge, range, route, Wilson, and identity channels remain
separate because they answer different numerical questions.

Deserialization establishes retained-wire compatibility only.  It does not reproduce
the historical calculation, establish a material polarization or topology, validate a
physical model, or perform uncertainty quantification.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

import numpy as np

from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.serialization import JsonCodec
from ksdft2effmass.solid_state import (
    BlockHoppingModel1D,
    ReciprocalOperatorSamples1D,
    WilsonLoopSpectrum1D,
    WilsonLoopSpectrumCanonicalizer1D,
)

from .result_documents import (
    Periodic1DJsonObject,
    Periodic1DRetainedResultDocument,
    Periodic1DRetainedResultJsonSerializer,
    Periodic1DRetainedResultKind,
)


class Periodic1DCompositeExternalIsolationStatus(StrEnum):
    """Classify the retained external-gap threshold comparison.

    ``PASS`` means the sampled external minimum gap exceeded the historical campaign
    threshold.  ``FAILED`` means it did not.  This stored classification is not an
    independently recomputed scientific acceptance decision.
    """

    PASS = "pass"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeBandIsolationResult:
    """Retain internal and external sampled gaps for one composite group.

    Parameters
    ----------
    internal_minimum_gap
        Minimum sampled separation within the retained group, in recoil-energy
        units :math:`E_G`.
    external_minimum_gap
        Minimum sampled separation from bands outside the retained group, in
        :math:`E_G`.
    external_status
        Historical disposition of ``external_minimum_gap`` against the campaign's
        external-gap threshold.
    """

    internal_minimum_gap: float
    external_minimum_gap: float
    external_status: Periodic1DCompositeExternalIsolationStatus

    def __post_init__(self) -> None:
        """Require finite nonnegative gaps and an exact status enum."""
        for name, value in (
            ("internal_minimum_gap", self.internal_minimum_gap),
            ("external_minimum_gap", self.external_minimum_gap),
        ):
            if type(value) is not float or not np.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be a finite nonnegative float")
        if type(self.external_status) is not Periodic1DCompositeExternalIsolationStatus:
            raise TypeError(
                "external_status must be Periodic1DCompositeExternalIsolationStatus"
            )


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeWilsonGroupResult:
    """Retain Wilson-loop outcomes for one demonstrated composite band group.

    Parameters
    ----------
    group_id
        Stable retained group identifier.
    band_indices
        Ordered zero-based parent-band indices spanning the represented subspace.
    spectrum
        Canonical unordered principal-branch Wilson eigenphase multiset.
    controlled_gauge_phase_set_defect
        Historical optimal circular phase-set defect after a controlled gauge change,
        in radians.

    Notes
    -----
    The controlled-gauge phase spectrum was not retained, so its reported defect
    cannot be independently reconstructed from ``composite-result.json`` alone.
    """

    group_id: str
    band_indices: tuple[int, ...]
    spectrum: WilsonLoopSpectrum1D
    controlled_gauge_phase_set_defect: float

    def __post_init__(self) -> None:
        """Validate group identity, band inventory, spectrum rank, and defect."""
        if type(self.group_id) is not str or not self.group_id:
            raise ValueError("group_id must be a nonempty built-in str")
        if (
            not isinstance(self.band_indices, tuple)
            or not self.band_indices
            or any(type(index) is not int or index < 0 for index in self.band_indices)
        ):
            raise ValueError(
                "band_indices must be a nonempty tuple of nonnegative ints"
            )
        if len(set(self.band_indices)) != len(self.band_indices):
            raise ValueError("band_indices must be unique")
        if type(self.spectrum) is not WilsonLoopSpectrum1D:
            raise TypeError("spectrum must be WilsonLoopSpectrum1D")
        if self.spectrum.rank != len(self.band_indices):
            raise ValueError("Wilson spectrum rank must equal retained band count")
        if (
            type(self.controlled_gauge_phase_set_defect) is not float
            or not np.isfinite(self.controlled_gauge_phase_set_defect)
            or self.controlled_gauge_phase_set_defect < 0.0
        ):
            raise ValueError(
                "controlled-gauge phase defect must be finite and nonnegative"
            )


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeGaugeComparisonResult:
    r"""Retain conditioning and gauge-route comparison diagnostics.

    Parameters
    ----------
    neighbor_overlap_minimum_singular_value
        Minimum singular value over neighboring retained-frame overlaps.
    controlled_gauge_projector_maximum_frobenius_defect
        Maximum projector defect under the controlled gauge transformation.
    pointwise_alignment_frame_maximum_frobenius_defect
        Maximum frame defect after pointwise polar alignment.
    pointwise_alignment_operator_maximum_frobenius_defect
        Maximum represented-Hamiltonian defect after that alignment, in :math:`E_G`.
    controlled_gauge_eigenvalue_maximum_defect
        Maximum retained eigenvalue defect under the controlled gauge transformation,
        in :math:`E_G`.
    rough_vs_smooth_unaligned_hopping_l2_defect
        Unaligned coefficient-space :math:`\ell_2` defect between complete rough- and
        smooth-gauge hopping blocks, in :math:`E_G`.
    """

    neighbor_overlap_minimum_singular_value: float
    controlled_gauge_projector_maximum_frobenius_defect: float
    pointwise_alignment_frame_maximum_frobenius_defect: float
    pointwise_alignment_operator_maximum_frobenius_defect: float
    controlled_gauge_eigenvalue_maximum_defect: float
    rough_vs_smooth_unaligned_hopping_l2_defect: float

    def __post_init__(self) -> None:
        """Require finite nonnegative represented diagnostics."""
        for name, value in (
            (
                "neighbor_overlap_minimum_singular_value",
                self.neighbor_overlap_minimum_singular_value,
            ),
            (
                "controlled_gauge_projector_maximum_frobenius_defect",
                self.controlled_gauge_projector_maximum_frobenius_defect,
            ),
            (
                "pointwise_alignment_frame_maximum_frobenius_defect",
                self.pointwise_alignment_frame_maximum_frobenius_defect,
            ),
            (
                "pointwise_alignment_operator_maximum_frobenius_defect",
                self.pointwise_alignment_operator_maximum_frobenius_defect,
            ),
            (
                "controlled_gauge_eigenvalue_maximum_defect",
                self.controlled_gauge_eigenvalue_maximum_defect,
            ),
            (
                "rough_vs_smooth_unaligned_hopping_l2_defect",
                self.rough_vs_smooth_unaligned_hopping_l2_defect,
            ),
        ):
            if type(value) is not float or not np.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be a finite nonnegative float")


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeHoppingRangeResult:
    r"""Retain one smooth/rough finite-range approximation comparison.

    Parameters
    ----------
    hopping_range_cells
        Symmetric retained range :math:`|R|\leq R_{\max}` in lattice cells.
    smooth_omitted_block_l2_norm
        Smooth-gauge coefficient-space omitted-block :math:`\ell_2` norm in
        :math:`E_G`.
    rough_omitted_block_l2_norm
        Rough-gauge coefficient-space omitted-block :math:`\ell_2` norm in
        :math:`E_G`.
    smooth_training_eigenvalue_maximum_error
        Smooth-gauge maximum eigenvalue error on the transform mesh, in :math:`E_G`.
    rough_training_eigenvalue_maximum_error
        Rough-gauge maximum eigenvalue error on the transform mesh, in :math:`E_G`.
    smooth_withheld_eigenvalue_maximum_error
        Smooth-gauge maximum eigenvalue error on the independent withheld mesh, in
        :math:`E_G`.
    rough_withheld_eigenvalue_maximum_error
        Rough-gauge maximum eigenvalue error on the independent withheld mesh, in
        :math:`E_G`.
    """

    hopping_range_cells: int
    smooth_omitted_block_l2_norm: float
    rough_omitted_block_l2_norm: float
    smooth_training_eigenvalue_maximum_error: float
    rough_training_eigenvalue_maximum_error: float
    smooth_withheld_eigenvalue_maximum_error: float
    rough_withheld_eigenvalue_maximum_error: float

    def __post_init__(self) -> None:
        """Require a nonnegative range and finite nonnegative errors."""
        if type(self.hopping_range_cells) is not int or self.hopping_range_cells < 0:
            raise ValueError("hopping_range_cells must be a nonnegative built-in int")
        for name, value in (
            ("smooth_omitted_block_l2_norm", self.smooth_omitted_block_l2_norm),
            ("rough_omitted_block_l2_norm", self.rough_omitted_block_l2_norm),
            (
                "smooth_training_eigenvalue_maximum_error",
                self.smooth_training_eigenvalue_maximum_error,
            ),
            (
                "rough_training_eigenvalue_maximum_error",
                self.rough_training_eigenvalue_maximum_error,
            ),
            (
                "smooth_withheld_eigenvalue_maximum_error",
                self.smooth_withheld_eigenvalue_maximum_error,
            ),
            (
                "rough_withheld_eigenvalue_maximum_error",
                self.rough_withheld_eigenvalue_maximum_error,
            ),
        ):
            if type(value) is not float or not np.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be a finite nonnegative float")


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeDirectRouteComparisonResult:
    """Retain the direct-fit versus transform-and-truncate route comparison.

    Parameters
    ----------
    hopping_range_cells
        Common symmetric hopping range used by both routes.
    coefficient_frobenius_defect
        Frobenius defect between the fitted and transformed coefficient arrays, in
        :math:`E_G`.
    training_operator_maximum_frobenius_defect
        Maximum reciprocal-mesh operator defect between routes, in :math:`E_G`.
    """

    hopping_range_cells: int
    coefficient_frobenius_defect: float
    training_operator_maximum_frobenius_defect: float

    def __post_init__(self) -> None:
        """Require a nonnegative range and finite nonnegative route defects."""
        if type(self.hopping_range_cells) is not int or self.hopping_range_cells < 0:
            raise ValueError("hopping_range_cells must be a nonnegative built-in int")
        for name, value in (
            ("coefficient_frobenius_defect", self.coefficient_frobenius_defect),
            (
                "training_operator_maximum_frobenius_defect",
                self.training_operator_maximum_frobenius_defect,
            ),
        ):
            if type(value) is not float or not np.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be a finite nonnegative float")


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeArtifactIdentities:
    """Retain SHA-256 identities for non-serialized composite arrays.

    Parameters
    ----------
    smooth_frame_sha256
        Identity of the smooth retained frame array.
    smooth_projector_sha256
        Identity of projectors formed from the smooth frames.
    smooth_reciprocal_hamiltonian_sha256
        Identity of the smooth represented reciprocal Hamiltonians.
    smooth_hopping_sha256, rough_hopping_sha256
        Identities of the complete smooth- and rough-gauge hopping arrays.
    """

    smooth_frame_sha256: str
    smooth_projector_sha256: str
    smooth_reciprocal_hamiltonian_sha256: str
    smooth_hopping_sha256: str
    rough_hopping_sha256: str

    def __post_init__(self) -> None:
        """Require each identity to use lowercase SHA-256 hexadecimal syntax."""
        for name, value in (
            ("smooth_frame_sha256", self.smooth_frame_sha256),
            ("smooth_projector_sha256", self.smooth_projector_sha256),
            (
                "smooth_reciprocal_hamiltonian_sha256",
                self.smooth_reciprocal_hamiltonian_sha256,
            ),
            ("smooth_hopping_sha256", self.smooth_hopping_sha256),
            ("rough_hopping_sha256", self.rough_hopping_sha256),
        ):
            if (
                type(value) is not str
                or len(value) != 64
                or any(character not in "0123456789abcdef" for character in value)
            ):
                raise ValueError(f"{name} must be lowercase SHA-256 hexadecimal")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DCompositeHoppingRepresentationResult:
    r"""Retain dense reciprocal matrices and complete smooth/rough hoppings.

    Parameters
    ----------
    smooth_reciprocal_hamiltonians
        Smooth-gauge represented Hamiltonians on the ordered half-open uniform mesh.
        Matrices use the dimensionless recoil-energy convention :math:`E_G`.
    smooth_hopping_model
        Complete smooth-gauge Born--von Karman hopping blocks in centered cell
        representatives.
    rough_hopping_model
        Complete rough-gauge Born--von Karman hopping blocks in the same
        representatives.
    smooth_block_frobenius_norms
        Reported Frobenius norm of every smooth-gauge hopping block.
    rough_block_frobenius_norms
        Reported Frobenius norm of every rough-gauge hopping block.
    smooth_full_reconstruction_maximum_frobenius_error
        Maximum smooth-gauge complete-transform reconstruction defect, in
        :math:`E_G`.
    rough_full_reconstruction_maximum_frobenius_error
        Maximum rough-gauge complete-transform reconstruction defect, in
        :math:`E_G`.
    smooth_hopping_hermiticity_maximum_frobenius_residual
        Maximum smooth-gauge block residual for
        :math:`T_{-R}=T_R^\dagger`, in :math:`E_G`.
    """

    smooth_reciprocal_hamiltonians: ReciprocalOperatorSamples1D
    smooth_hopping_model: BlockHoppingModel1D
    rough_hopping_model: BlockHoppingModel1D
    smooth_block_frobenius_norms: tuple[float, ...]
    rough_block_frobenius_norms: tuple[float, ...]
    smooth_full_reconstruction_maximum_frobenius_error: float
    rough_full_reconstruction_maximum_frobenius_error: float
    smooth_hopping_hermiticity_maximum_frobenius_residual: float

    def __post_init__(self) -> None:
        """Validate complete-mesh dimensions, norms, and retained diagnostics."""
        if type(self.smooth_reciprocal_hamiltonians) is not ReciprocalOperatorSamples1D:
            raise TypeError(
                "smooth_reciprocal_hamiltonians must be ReciprocalOperatorSamples1D"
            )
        for name, model in (
            ("smooth_hopping_model", self.smooth_hopping_model),
            ("rough_hopping_model", self.rough_hopping_model),
        ):
            if type(model) is not BlockHoppingModel1D:
                raise TypeError(f"{name} must be BlockHoppingModel1D")
        smooth = self.smooth_hopping_model
        rough = self.rough_hopping_model
        samples = self.smooth_reciprocal_hamiltonians
        if smooth.representatives != rough.representatives:
            raise ValueError("smooth and rough representatives must agree")
        if smooth.matrix_dimension != rough.matrix_dimension:
            raise ValueError("smooth and rough block dimensions must agree")
        if samples.matrix_dimension != smooth.matrix_dimension:
            raise ValueError("reciprocal and hopping matrix dimensions must agree")
        if len(smooth.representatives) != len(samples.matrices):
            raise ValueError("complete hopping and reciprocal sample counts must agree")
        for name, reported, model in (
            (
                "smooth_block_frobenius_norms",
                self.smooth_block_frobenius_norms,
                smooth,
            ),
            (
                "rough_block_frobenius_norms",
                self.rough_block_frobenius_norms,
                rough,
            ),
        ):
            if not isinstance(reported, tuple) or len(reported) != len(
                model.hopping_blocks
            ):
                raise ValueError(f"{name} must contain one value per hopping block")
            measured = tuple(
                float(np.linalg.norm(block.magnitude)) for block in model.hopping_blocks
            )
            if any(
                type(value) is not float or not np.isfinite(value) or value < 0.0
                for value in reported
            ):
                raise ValueError(f"{name} must contain finite nonnegative floats")
            if reported != measured:
                raise ValueError(f"{name} must match the represented hopping blocks")
        for name, value in (
            (
                "smooth_full_reconstruction_maximum_frobenius_error",
                self.smooth_full_reconstruction_maximum_frobenius_error,
            ),
            (
                "rough_full_reconstruction_maximum_frobenius_error",
                self.rough_full_reconstruction_maximum_frobenius_error,
            ),
            (
                "smooth_hopping_hermiticity_maximum_frobenius_residual",
                self.smooth_hopping_hermiticity_maximum_frobenius_residual,
            ),
        ):
            if type(value) is not float or not np.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be a finite nonnegative float")


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeBandGroupResult:
    """Retain every typed result channel for one composite band group.

    Parameters
    ----------
    wilson
        Group identity, band inventory, and Wilson phase result.
    isolation
        Internal and external sampled gap diagnostics.
    gauge_comparison
        Neighbor conditioning, covariance, and alignment diagnostics.
    hopping_representation
        Dense smooth reciprocal matrices and complete smooth/rough hoppings.
    range_study
        Ordered finite-range approximation outcomes.
    direct_route
        Direct-fit versus transform-and-truncate route comparison.
    identities
        SHA-256 identities of the historical intermediate arrays.
    """

    wilson: Periodic1DCompositeWilsonGroupResult
    isolation: Periodic1DCompositeBandIsolationResult
    gauge_comparison: Periodic1DCompositeGaugeComparisonResult
    hopping_representation: Periodic1DCompositeHoppingRepresentationResult
    range_study: tuple[Periodic1DCompositeHoppingRangeResult, ...]
    direct_route: Periodic1DCompositeDirectRouteComparisonResult
    identities: Periodic1DCompositeArtifactIdentities

    def __post_init__(self) -> None:
        """Validate exact channel types, matrix rank, and ordered range inventory."""
        expected_types = (
            ("wilson", self.wilson, Periodic1DCompositeWilsonGroupResult),
            (
                "isolation",
                self.isolation,
                Periodic1DCompositeBandIsolationResult,
            ),
            (
                "gauge_comparison",
                self.gauge_comparison,
                Periodic1DCompositeGaugeComparisonResult,
            ),
            (
                "hopping_representation",
                self.hopping_representation,
                Periodic1DCompositeHoppingRepresentationResult,
            ),
            (
                "direct_route",
                self.direct_route,
                Periodic1DCompositeDirectRouteComparisonResult,
            ),
            (
                "identities",
                self.identities,
                Periodic1DCompositeArtifactIdentities,
            ),
        )
        for name, value, expected_type in expected_types:
            if type(value) is not expected_type:
                raise TypeError(f"{name} uses the wrong result type")
        if self.hopping_representation.smooth_hopping_model.matrix_dimension != len(
            self.wilson.band_indices
        ):
            raise ValueError("represented matrix rank must equal retained band count")
        if (
            not isinstance(self.range_study, tuple)
            or not self.range_study
            or any(
                type(item) is not Periodic1DCompositeHoppingRangeResult
                for item in self.range_study
            )
        ):
            raise TypeError("range_study must be a nonempty typed tuple")
        ranges = tuple(item.hopping_range_cells for item in self.range_study)
        if ranges != tuple(sorted(set(ranges))):
            raise ValueError("range_study must use unique increasing ranges")
        if self.direct_route.hopping_range_cells not in ranges:
            raise ValueError("direct-route range must occur in range_study")

    @property
    def group_id(self) -> str:
        """Return the stable retained group identifier."""
        return self.wilson.group_id

    @property
    def band_indices(self) -> tuple[int, ...]:
        """Return the ordered retained parent-band indices."""
        return self.wilson.band_indices

    @property
    def spectrum(self) -> WilsonLoopSpectrum1D:
        """Return the canonical unordered Wilson eigenphase spectrum."""
        return self.wilson.spectrum

    @property
    def controlled_gauge_phase_set_defect(self) -> float:
        """Return the historical controlled-gauge Wilson phase-set defect."""
        return self.wilson.controlled_gauge_phase_set_defect


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeCampaignResult:
    """Retain complete typed composite outcomes and their source document.

    Parameters
    ----------
    source_document
        Complete immutable version-one retained result and source-byte identity.
    groups
        Ordered typed composite-band group outcomes.
    """

    source_document: Periodic1DRetainedResultDocument
    groups: tuple[Periodic1DCompositeBandGroupResult, ...]

    def __post_init__(self) -> None:
        """Validate source kind and unique nonempty typed group inventory."""
        if type(self.source_document) is not Periodic1DRetainedResultDocument:
            raise TypeError("source_document must be Periodic1DRetainedResultDocument")
        if self.source_document.kind is not Periodic1DRetainedResultKind.COMPOSITE:
            raise ValueError("source_document must be a composite result")
        if (
            not isinstance(self.groups, tuple)
            or not self.groups
            or any(
                type(group) is not Periodic1DCompositeBandGroupResult
                for group in self.groups
            )
        ):
            raise TypeError("groups must be a nonempty typed tuple")
        group_ids = tuple(group.group_id for group in self.groups)
        if len(set(group_ids)) != len(group_ids):
            raise ValueError("composite group identifiers must be unique")


class Periodic1DCompositeResultJsonSerializer(
    JsonCodec[Periodic1DCompositeCampaignResult, bytes]
):
    """Adapt retained composite bytes to complete typed campaign outcomes.

    The decoder retains the entire immutable JSON document and additionally exposes
    every demonstrated group matrix, hopping, gap, gauge, range, direct-route, Wilson,
    and intermediate-array identity channel.  Complex matrices are represented with
    binary64 real and imaginary parts in the source convention.
    """

    __slots__ = ()

    retained = Periodic1DRetainedResultJsonSerializer(
        Periodic1DRetainedResultKind.COMPOSITE
    )
    canonicalizer = WilsonLoopSpectrumCanonicalizer1D()

    def deserialize(self, payload: bytes) -> Periodic1DCompositeCampaignResult:
        """Decode the complete source and extract every typed composite channel.

        Parameters
        ----------
        payload
            UTF-8 version-one ``composite-result.json`` bytes.

        Returns
        -------
        Periodic1DCompositeCampaignResult
            Complete immutable source document and ordered typed group outcomes.

        Raises
        ------
        TypeError
            If a required JSON value has the wrong semantic representation.
        ValueError
            If the version, status, dimensions, ordering, or intrinsic correlations
            violate the version-one contract.
        """
        document = self.retained.deserialize(payload)
        return Periodic1DCompositeCampaignResult(
            document,
            tuple(
                self.decode_group(group)
                for group in self.retained.object_array_field(document.root, "groups")
            ),
        )

    def serialize(self, value: Periodic1DCompositeCampaignResult) -> bytes:
        """Encode the complete correlated source document canonically.

        Parameters
        ----------
        value
            Typed composite result retaining its complete source document.

        Returns
        -------
        bytes
            Canonical newline-terminated JSON bytes.

        Raises
        ------
        TypeError
            If ``value`` is not an exact composite campaign result.
        """
        if type(value) is not Periodic1DCompositeCampaignResult:
            raise TypeError("value must be Periodic1DCompositeCampaignResult")
        return self.retained.serialize(value.source_document)

    def decode_group(
        self, value: Periodic1DJsonObject
    ) -> Periodic1DCompositeBandGroupResult:
        """Extract every retained channel for one composite band group.

        Parameters
        ----------
        value
            Immutable JSON object containing one version-one group record.

        Returns
        -------
        Periodic1DCompositeBandGroupResult
            Correlated typed channels for the group.
        """
        phases = self.retained.real_vector_field(value, "wilson_loop_eigenphases")
        wilson = Periodic1DCompositeWilsonGroupResult(
            self.retained.string_field(value, "id"),
            self.retained.integer_tuple_field(value, "band_indices"),
            self.canonicalizer.execute(tuple(float(phase) for phase in phases)),
            self.retained.real_field(value, "controlled_gauge_wilson_phase_set_defect"),
        )
        status_value = self.retained.string_field(value, "external_isolation_status")
        try:
            status = Periodic1DCompositeExternalIsolationStatus(status_value)
        except ValueError as error:
            raise ValueError(
                "unsupported composite external isolation status"
            ) from error
        return Periodic1DCompositeBandGroupResult(
            wilson,
            Periodic1DCompositeBandIsolationResult(
                self.retained.real_field(value, "internal_minimum_gap"),
                self.retained.real_field(value, "external_minimum_gap"),
                status,
            ),
            self.decode_gauge_comparison(value),
            self.decode_hopping_representation(value),
            tuple(
                self.decode_range_result(item)
                for item in self.retained.object_array_field(value, "range_study")
            ),
            self.decode_direct_route(self.retained.object_field(value, "direct_route")),
            self.decode_identities(self.retained.object_field(value, "identities")),
        )

    def decode_gauge_comparison(
        self, value: Periodic1DJsonObject
    ) -> Periodic1DCompositeGaugeComparisonResult:
        """Extract conditioning, alignment, and gauge-covariance diagnostics.

        Parameters
        ----------
        value
            Immutable JSON object containing one group record.

        Returns
        -------
        Periodic1DCompositeGaugeComparisonResult
            Separated overlap, projector, alignment, eigenvalue, and hopping defects.
        """
        return Periodic1DCompositeGaugeComparisonResult(
            self.retained.real_field(value, "neighbor_overlap_minimum_singular_value"),
            self.retained.real_field(
                value, "controlled_gauge_projector_maximum_frobenius_defect"
            ),
            self.retained.real_field(
                value, "pointwise_alignment_frame_maximum_frobenius_defect"
            ),
            self.retained.real_field(
                value, "pointwise_alignment_operator_maximum_frobenius_defect"
            ),
            self.retained.real_field(
                value, "controlled_gauge_eigenvalue_maximum_defect"
            ),
            self.retained.real_field(
                value, "rough_vs_smooth_unaligned_hopping_l2_defect"
            ),
        )

    def decode_hopping_representation(
        self, value: Periodic1DJsonObject
    ) -> Periodic1DCompositeHoppingRepresentationResult:
        """Extract smooth reciprocal matrices and complete smooth/rough hoppings.

        Parameters
        ----------
        value
            Immutable JSON object containing one group record.

        Returns
        -------
        Periodic1DCompositeHoppingRepresentationResult
            Complete dimensionless reciprocal and hopping representations with their
            retained diagnostics.
        """
        matrices = self.retained.complex_matrix_array_field(
            value, "represented_reciprocal_hamiltonians"
        )
        count = len(matrices)
        coordinates = -0.5 + np.arange(count, dtype=np.float64) / float(count)
        reciprocal_period = ScalarQuantity(1.0, Unitless())
        reciprocal_samples = ReciprocalOperatorSamples1D(
            VectorQuantity(coordinates, Unitless()),
            reciprocal_period,
            tuple(ComplexMatrixQuantity(matrix, Unitless()) for matrix in matrices),
        )
        smooth_model, smooth_norms = self.decode_hopping_model(
            value, "smooth_hopping_blocks", reciprocal_period
        )
        rough_model, rough_norms = self.decode_hopping_model(
            value, "rough_hopping_blocks", reciprocal_period
        )
        return Periodic1DCompositeHoppingRepresentationResult(
            reciprocal_samples,
            smooth_model,
            rough_model,
            smooth_norms,
            rough_norms,
            self.retained.real_field(
                value, "smooth_full_reconstruction_maximum_frobenius_error"
            ),
            self.retained.real_field(
                value, "rough_full_reconstruction_maximum_frobenius_error"
            ),
            self.retained.real_field(
                value, "smooth_hopping_hermiticity_maximum_frobenius_residual"
            ),
        )

    def decode_hopping_model(
        self,
        value: Periodic1DJsonObject,
        field_name: str,
        reciprocal_period: ScalarQuantity,
    ) -> tuple[BlockHoppingModel1D, tuple[float, ...]]:
        """Extract one complete hopping model and its reported block norms.

        Parameters
        ----------
        value
            Immutable group object containing the hopping-record array.
        field_name
            Name of either the smooth- or rough-gauge hopping field.
        reciprocal_period
            Explicit reduced reciprocal period shared by the represented model.

        Returns
        -------
        tuple
            Complete hopping model and the ordered reported block Frobenius norms.
        """
        records = self.retained.object_array_field(value, field_name)
        representatives = tuple(
            self.retained.integer_field(record, "representative_cells")
            for record in records
        )
        matrices = tuple(
            ComplexMatrixQuantity(
                self.retained.complex_matrix_field(record, "matrix"), Unitless()
            )
            for record in records
        )
        norms = tuple(
            self.retained.real_field(record, "frobenius_norm") for record in records
        )
        return (
            BlockHoppingModel1D(reciprocal_period, representatives, matrices),
            norms,
        )

    def decode_range_result(
        self, value: Periodic1DJsonObject
    ) -> Periodic1DCompositeHoppingRangeResult:
        """Extract one finite-range smooth/rough comparison.

        Parameters
        ----------
        value
            Immutable JSON object containing one range-study record.

        Returns
        -------
        Periodic1DCompositeHoppingRangeResult
            Separate smooth/rough, training/withheld approximation diagnostics.
        """
        return Periodic1DCompositeHoppingRangeResult(
            self.retained.integer_field(value, "hopping_range_cells"),
            self.retained.real_field(value, "smooth_omitted_block_l2_norm"),
            self.retained.real_field(value, "rough_omitted_block_l2_norm"),
            self.retained.real_field(value, "smooth_training_eigenvalue_maximum_error"),
            self.retained.real_field(value, "rough_training_eigenvalue_maximum_error"),
            self.retained.real_field(value, "smooth_withheld_eigenvalue_maximum_error"),
            self.retained.real_field(value, "rough_withheld_eigenvalue_maximum_error"),
        )

    def decode_direct_route(
        self, value: Periodic1DJsonObject
    ) -> Periodic1DCompositeDirectRouteComparisonResult:
        """Extract the direct-fit versus transformed-route comparison.

        Parameters
        ----------
        value
            Immutable JSON object containing the direct-route record.

        Returns
        -------
        Periodic1DCompositeDirectRouteComparisonResult
            Common-range coefficient and training-operator defects.
        """
        return Periodic1DCompositeDirectRouteComparisonResult(
            self.retained.integer_field(value, "hopping_range_cells"),
            self.retained.real_field(value, "coefficient_frobenius_defect"),
            self.retained.real_field(
                value, "training_operator_maximum_frobenius_defect"
            ),
        )

    def decode_identities(
        self, value: Periodic1DJsonObject
    ) -> Periodic1DCompositeArtifactIdentities:
        """Extract retained SHA-256 identities for intermediate arrays.

        Parameters
        ----------
        value
            Immutable JSON object containing the five historical identities.

        Returns
        -------
        Periodic1DCompositeArtifactIdentities
            Typed lowercase SHA-256 identity record.
        """
        return Periodic1DCompositeArtifactIdentities(
            self.retained.string_field(value, "smooth_frame_sha256"),
            self.retained.string_field(value, "smooth_projector_sha256"),
            self.retained.string_field(value, "smooth_reciprocal_hamiltonian_sha256"),
            self.retained.string_field(value, "smooth_hopping_sha256"),
            self.retained.string_field(value, "rough_hopping_sha256"),
        )
