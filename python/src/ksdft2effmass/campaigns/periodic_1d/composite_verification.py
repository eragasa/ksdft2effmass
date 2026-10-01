"""Independent numerical verification of retained Appendix G composite results.

The verifier in this module consumes a correlated read-only campaign result and
reconstructs only quantities determined by the retained matrices and exact input
controls.  It implements the finite Fourier sums, direct least-squares route,
training-mesh eigenspectra, represented Hermiticity residual, and array identities
directly with NumPy.  It does not import the production hopping-transform, fitting,
frame-transport, alignment, or Wilson-loop algorithms.

Several historical diagnostics cannot be reconstructed because their source arrays
were not retained.  The aggregate result names those unavailable channels explicitly
instead of treating source-document presence as independent verification.  Passing is
numerical verification of the represented retained channels only; it is not material
validation, topology or polarization evidence, uncertainty quantification, or human
acceptance.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import StrEnum

import numpy as np
import numpy.typing as npt

from ksdft2effmass.operators import ScalarQuantity, Unitless

from .composite import Periodic1DCompositeCampaignDefinition
from .composite_results import Periodic1DCompositeBandGroupResult
from .wilson_workflows import Periodic1DCompositeCampaignWorkflowResult

type ComplexArray3 = npt.NDArray[np.complex128]
type IntegerVector = npt.NDArray[np.int64]
type RealVector = npt.NDArray[np.float64]


class Periodic1DCompositeUnavailableVerificationChannel(StrEnum):
    """Identify retained channels lacking sufficient independent source values."""

    SAMPLED_GAPS = "sampled_gaps"
    NEIGHBOR_OVERLAP_AND_WILSON = "neighbor_overlap_and_wilson"
    CONTROLLED_GAUGE = "controlled_gauge"
    POINTWISE_ALIGNMENT = "pointwise_alignment"
    ROUGH_RECIPROCAL_RECONSTRUCTION = "rough_reciprocal_reconstruction"
    WITHHELD_RANGE_ERRORS = "withheld_range_errors"
    SMOOTH_FRAME_IDENTITY = "smooth_frame_identity"
    SMOOTH_PROJECTOR_IDENTITY = "smooth_projector_identity"


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeVerificationRequest:
    """Provide one correlated campaign and numerical comparison tolerance.

    Parameters
    ----------
    correlated_campaign
        Read-only Workflow result whose input definition, result document, group
        inventory, mesh controls, range controls, and source identities already agree.
    absolute_tolerance
        Inclusive absolute tolerance in the dimensionless recoil-energy convention
        :math:`E_G`.  It applies to represented matrix defects and to differences
        between independently recomputed and retained scalar diagnostics.
    """

    correlated_campaign: Periodic1DCompositeCampaignWorkflowResult
    absolute_tolerance: ScalarQuantity

    def __post_init__(self) -> None:
        """Require an exact correlated result and nonnegative unitless tolerance."""
        if (
            type(self.correlated_campaign)
            is not Periodic1DCompositeCampaignWorkflowResult
        ):
            raise TypeError(
                "correlated_campaign must be Periodic1DCompositeCampaignWorkflowResult"
            )
        if type(self.absolute_tolerance) is not ScalarQuantity:
            raise TypeError("absolute_tolerance must be ScalarQuantity")
        if not isinstance(self.absolute_tolerance.unit, Unitless):
            raise ValueError("absolute_tolerance must use Unitless")
        if self.absolute_tolerance.magnitude < 0.0:
            raise ValueError("absolute_tolerance must be nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeGroupVerificationResult:
    r"""Retain independently recomputed diagnostics for one composite group.

    All scalar quantities use the dimensionless recoil-energy convention :math:`E_G`.
    A ``reported_absolute_defect`` is the absolute difference between an independent
    recomputation and the corresponding scalar stored in the retained result.

    Parameters
    ----------
    group_id
        Stable retained group identifier.
    reciprocal_hamiltonian_identity_passes
        Whether the stored smooth reciprocal matrices reproduce their SHA-256.
    smooth_hopping_identity_passes, rough_hopping_identity_passes
        Whether the complete stored hopping arrays reproduce their SHA-256 values.
    smooth_transform_maximum_absolute_defect
        Largest entrywise defect between a direct Fourier sum and stored smooth
        hopping blocks.
    smooth_inverse_maximum_frobenius_error
        Largest matrix Frobenius error after direct inverse reconstruction.
    smooth_inverse_reported_absolute_defect
        Defect between that inverse error and the retained reconstruction diagnostic.
    smooth_hermiticity_maximum_frobenius_residual
        Largest :math:`\|T_R-T_{-R}^\dagger\|_F` over exact represented opposite
        pairs.  The unmatched even-mesh Nyquist representative is excluded to match
        the retained metric.
    smooth_hermiticity_reported_absolute_defect
        Defect between the independent and retained Hermiticity residuals.
    maximum_omitted_norm_reported_absolute_defect
        Largest retained-versus-recomputed smooth or rough omitted-block norm defect.
    maximum_training_error_reported_absolute_defect
        Largest retained-versus-recomputed smooth or rough training eigenvalue-error
        defect.  Withheld errors are intentionally excluded.
    rough_vs_smooth_hopping_l2_defect
        Independently recomputed complete unaligned coefficient-space defect.
    rough_vs_smooth_reported_absolute_defect
        Defect between that value and the retained gauge-attack diagnostic.
    direct_coefficient_frobenius_defect
        Independent direct-fit versus transformed-coefficient Frobenius defect.
    direct_coefficient_reported_absolute_defect
        Difference between independent and retained coefficient defects.
    direct_training_operator_maximum_frobenius_defect
        Independent maximum training-mesh operator defect between the two routes.
    direct_training_operator_reported_absolute_defect
        Difference between independent and retained operator-route defects.
    absolute_tolerance
        Inclusive tolerance applied by this verification operation.
    passes
        Aggregate disposition for the channels this verifier can reconstruct.
    """

    group_id: str
    reciprocal_hamiltonian_identity_passes: bool
    smooth_hopping_identity_passes: bool
    rough_hopping_identity_passes: bool
    smooth_transform_maximum_absolute_defect: ScalarQuantity
    smooth_inverse_maximum_frobenius_error: ScalarQuantity
    smooth_inverse_reported_absolute_defect: ScalarQuantity
    smooth_hermiticity_maximum_frobenius_residual: ScalarQuantity
    smooth_hermiticity_reported_absolute_defect: ScalarQuantity
    maximum_omitted_norm_reported_absolute_defect: ScalarQuantity
    maximum_training_error_reported_absolute_defect: ScalarQuantity
    rough_vs_smooth_hopping_l2_defect: ScalarQuantity
    rough_vs_smooth_reported_absolute_defect: ScalarQuantity
    direct_coefficient_frobenius_defect: ScalarQuantity
    direct_coefficient_reported_absolute_defect: ScalarQuantity
    direct_training_operator_maximum_frobenius_defect: ScalarQuantity
    direct_training_operator_reported_absolute_defect: ScalarQuantity
    absolute_tolerance: ScalarQuantity
    passes: bool

    def __post_init__(self) -> None:
        """Validate identities, unitless finite diagnostics, and disposition."""
        if type(self.group_id) is not str or not self.group_id:
            raise ValueError("group_id must be a nonempty built-in str")
        identity_results = (
            self.reciprocal_hamiltonian_identity_passes,
            self.smooth_hopping_identity_passes,
            self.rough_hopping_identity_passes,
        )
        if any(type(value) is not bool for value in identity_results):
            raise TypeError("identity dispositions must be built-in bools")
        diagnostics = (
            self.smooth_transform_maximum_absolute_defect,
            self.smooth_inverse_maximum_frobenius_error,
            self.smooth_inverse_reported_absolute_defect,
            self.smooth_hermiticity_maximum_frobenius_residual,
            self.smooth_hermiticity_reported_absolute_defect,
            self.maximum_omitted_norm_reported_absolute_defect,
            self.maximum_training_error_reported_absolute_defect,
            self.rough_vs_smooth_hopping_l2_defect,
            self.rough_vs_smooth_reported_absolute_defect,
            self.direct_coefficient_frobenius_defect,
            self.direct_coefficient_reported_absolute_defect,
            self.direct_training_operator_maximum_frobenius_defect,
            self.direct_training_operator_reported_absolute_defect,
            self.absolute_tolerance,
        )
        if any(type(value) is not ScalarQuantity for value in diagnostics):
            raise TypeError("verification diagnostics must be ScalarQuantity values")
        if any(not isinstance(value.unit, Unitless) for value in diagnostics):
            raise ValueError("verification diagnostics must use Unitless")
        if any(value.magnitude < 0.0 for value in diagnostics):
            raise ValueError("verification diagnostics must be nonnegative")
        if type(self.passes) is not bool:
            raise TypeError("passes must be a built-in bool")
        tolerance = self.absolute_tolerance.magnitude
        bounded = (
            self.smooth_transform_maximum_absolute_defect,
            self.smooth_inverse_maximum_frobenius_error,
            self.smooth_inverse_reported_absolute_defect,
            self.smooth_hermiticity_maximum_frobenius_residual,
            self.smooth_hermiticity_reported_absolute_defect,
            self.maximum_omitted_norm_reported_absolute_defect,
            self.maximum_training_error_reported_absolute_defect,
            self.rough_vs_smooth_reported_absolute_defect,
            self.direct_coefficient_frobenius_defect,
            self.direct_coefficient_reported_absolute_defect,
            self.direct_training_operator_maximum_frobenius_defect,
            self.direct_training_operator_reported_absolute_defect,
        )
        expected = all(identity_results) and all(
            value.magnitude <= tolerance for value in bounded
        )
        if self.passes is not expected:
            raise ValueError("passes must match identities, diagnostics, and tolerance")


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeVerificationResult:
    """Retain per-group numerical verification and explicit unavailable channels.

    Parameters
    ----------
    groups
        Ordered per-group independent verification outcomes.
    unavailable_channels
        Retained channels that cannot be reconstructed from the available source
        document and exact input controls.
    passes
        ``True`` exactly when every reconstructed group passes.
    """

    groups: tuple[Periodic1DCompositeGroupVerificationResult, ...]
    unavailable_channels: tuple[Periodic1DCompositeUnavailableVerificationChannel, ...]
    passes: bool

    def __post_init__(self) -> None:
        """Validate nonempty typed groups, channel inventory, and disposition."""
        if (
            not isinstance(self.groups, tuple)
            or not self.groups
            or any(
                type(group) is not Periodic1DCompositeGroupVerificationResult
                for group in self.groups
            )
        ):
            raise TypeError("groups must be a nonempty typed tuple")
        if (
            not isinstance(self.unavailable_channels, tuple)
            or not self.unavailable_channels
            or any(
                type(channel) is not Periodic1DCompositeUnavailableVerificationChannel
                for channel in self.unavailable_channels
            )
        ):
            raise TypeError("unavailable_channels must be a nonempty typed tuple")
        if len(set(self.unavailable_channels)) != len(self.unavailable_channels):
            raise ValueError("unavailable_channels must be unique")
        if type(self.passes) is not bool:
            raise TypeError("passes must be a built-in bool")
        if self.passes is not all(group.passes for group in self.groups):
            raise ValueError("passes must equal the conjunction of group results")


class Periodic1DCompositeResultVerifier:
    """Independently verify reconstructable retained composite result channels.

    The operation uses direct dense sums and NumPy least squares.  It deliberately
    does not call reusable production Fourier, hopping, fitting, frame, alignment, or
    Wilson implementations, which keeps the verification route algorithmically
    independent from those construction surfaces.
    """

    __slots__ = ()

    unavailable_channels = (
        Periodic1DCompositeUnavailableVerificationChannel.SAMPLED_GAPS,
        Periodic1DCompositeUnavailableVerificationChannel.NEIGHBOR_OVERLAP_AND_WILSON,
        Periodic1DCompositeUnavailableVerificationChannel.CONTROLLED_GAUGE,
        Periodic1DCompositeUnavailableVerificationChannel.POINTWISE_ALIGNMENT,
        Periodic1DCompositeUnavailableVerificationChannel.ROUGH_RECIPROCAL_RECONSTRUCTION,
        Periodic1DCompositeUnavailableVerificationChannel.WITHHELD_RANGE_ERRORS,
        Periodic1DCompositeUnavailableVerificationChannel.SMOOTH_FRAME_IDENTITY,
        Periodic1DCompositeUnavailableVerificationChannel.SMOOTH_PROJECTOR_IDENTITY,
    )

    def execute(
        self, request: Periodic1DCompositeVerificationRequest
    ) -> Periodic1DCompositeVerificationResult:
        """Verify every retained group in correlated campaign order.

        Parameters
        ----------
        request
            Correlated retained campaign and explicit numerical tolerance.

        Returns
        -------
        Periodic1DCompositeVerificationResult
            Per-group reconstructed diagnostics and unavailable-channel inventory.

        Raises
        ------
        TypeError
            If ``request`` has the wrong exact semantic type.
        ValueError
            If retained matrix inventories cannot support the declared finite sums.
        """
        if type(request) is not Periodic1DCompositeVerificationRequest:
            raise TypeError("request must be Periodic1DCompositeVerificationRequest")
        campaign = request.correlated_campaign
        groups = tuple(
            self.verify_group(group, campaign.definition, request.absolute_tolerance)
            for group in campaign.campaign_result.groups
        )
        return Periodic1DCompositeVerificationResult(
            groups,
            self.unavailable_channels,
            all(group.passes for group in groups),
        )

    def verify_group(
        self,
        group: Periodic1DCompositeBandGroupResult,
        definition: Periodic1DCompositeCampaignDefinition,
        absolute_tolerance: ScalarQuantity,
    ) -> Periodic1DCompositeGroupVerificationResult:
        """Recompute every available numerical channel for one group.

        Parameters
        ----------
        group
            Typed retained group containing matrices, hoppings, and diagnostics.
        definition
            Exact campaign controls supplying the period and mesh conventions.
        absolute_tolerance
            Inclusive unitless :math:`E_G` tolerance.

        Returns
        -------
        Periodic1DCompositeGroupVerificationResult
            Independent identities, finite-sum defects, and disposition.
        """
        representation = group.hopping_representation
        source = np.asarray(
            [
                matrix.magnitude
                for matrix in representation.smooth_reciprocal_hamiltonians.matrices
            ],
            dtype=np.complex128,
        )
        representatives = np.asarray(
            representation.smooth_hopping_model.representatives, dtype=np.int64
        )
        smooth = np.asarray(
            [
                block.magnitude
                for block in representation.smooth_hopping_model.hopping_blocks
            ],
            dtype=np.complex128,
        )
        rough = np.asarray(
            [
                block.magnitude
                for block in representation.rough_hopping_model.hopping_blocks
            ],
            dtype=np.complex128,
        )
        coordinates = np.asarray(
            representation.smooth_reciprocal_hamiltonians.coordinates.magnitude,
            dtype=np.float64,
        )
        period = definition.period.magnitude
        direct_hoppings = self.direct_hoppings(
            source, coordinates, representatives, period
        )
        transform_defect = float(np.max(np.abs(direct_hoppings - smooth)))
        reconstructed = self.reconstruct(smooth, coordinates, representatives, period)
        inverse_error = self.maximum_frobenius_defect(reconstructed, source)
        inverse_report_defect = abs(
            inverse_error
            - representation.smooth_full_reconstruction_maximum_frobenius_error
        )
        hermiticity = self.exact_pair_hermiticity_residual(smooth, representatives)
        hermiticity_report_defect = abs(
            hermiticity
            - representation.smooth_hopping_hermiticity_maximum_frobenius_residual
        )
        omitted_report_defect, training_report_defect = self.range_report_defects(
            group, source, smooth, rough, coordinates, representatives, period
        )
        rough_smooth = float(np.linalg.norm(rough - smooth))
        rough_smooth_report_defect = abs(
            rough_smooth
            - group.gauge_comparison.rough_vs_smooth_unaligned_hopping_l2_defect
        )
        direct_coefficient, direct_operator = self.direct_route_defects(
            group, source, smooth, coordinates, representatives, period
        )
        direct_coefficient_report = abs(
            direct_coefficient - group.direct_route.coefficient_frobenius_defect
        )
        direct_operator_report = abs(
            direct_operator
            - group.direct_route.training_operator_maximum_frobenius_defect
        )
        reciprocal_identity = self.array_sha256(source) == (
            group.identities.smooth_reciprocal_hamiltonian_sha256
        )
        smooth_identity = self.array_sha256(smooth) == (
            group.identities.smooth_hopping_sha256
        )
        rough_identity = self.array_sha256(rough) == (
            group.identities.rough_hopping_sha256
        )
        quantities = tuple(
            ScalarQuantity(value, Unitless())
            for value in (
                transform_defect,
                inverse_error,
                inverse_report_defect,
                hermiticity,
                hermiticity_report_defect,
                omitted_report_defect,
                training_report_defect,
                rough_smooth,
                rough_smooth_report_defect,
                direct_coefficient,
                direct_coefficient_report,
                direct_operator,
                direct_operator_report,
            )
        )
        tolerance = absolute_tolerance.magnitude
        bounded = (
            transform_defect,
            inverse_error,
            inverse_report_defect,
            hermiticity,
            hermiticity_report_defect,
            omitted_report_defect,
            training_report_defect,
            rough_smooth_report_defect,
            direct_coefficient,
            direct_coefficient_report,
            direct_operator,
            direct_operator_report,
        )
        passes = (
            reciprocal_identity
            and smooth_identity
            and rough_identity
            and all(value <= tolerance for value in bounded)
        )
        return Periodic1DCompositeGroupVerificationResult(
            group_id=group.group_id,
            reciprocal_hamiltonian_identity_passes=reciprocal_identity,
            smooth_hopping_identity_passes=smooth_identity,
            rough_hopping_identity_passes=rough_identity,
            smooth_transform_maximum_absolute_defect=quantities[0],
            smooth_inverse_maximum_frobenius_error=quantities[1],
            smooth_inverse_reported_absolute_defect=quantities[2],
            smooth_hermiticity_maximum_frobenius_residual=quantities[3],
            smooth_hermiticity_reported_absolute_defect=quantities[4],
            maximum_omitted_norm_reported_absolute_defect=quantities[5],
            maximum_training_error_reported_absolute_defect=quantities[6],
            rough_vs_smooth_hopping_l2_defect=quantities[7],
            rough_vs_smooth_reported_absolute_defect=quantities[8],
            direct_coefficient_frobenius_defect=quantities[9],
            direct_coefficient_reported_absolute_defect=quantities[10],
            direct_training_operator_maximum_frobenius_defect=quantities[11],
            direct_training_operator_reported_absolute_defect=quantities[12],
            absolute_tolerance=absolute_tolerance,
            passes=passes,
        )

    def direct_hoppings(
        self,
        source: ComplexArray3,
        coordinates: RealVector,
        representatives: IntegerVector,
        period: float,
    ) -> ComplexArray3:
        r"""Evaluate the direct finite reciprocal-to-cell transform.

        The convention is
        :math:`T_R=N_k^{-1}\sum_k\exp(-iRak)H(k)` with the explicit campaign
        period ``a`` and ordered reduced reciprocal coordinates.

        Parameters
        ----------
        source
            Ordered rank-three complex array of reciprocal Hamiltonians.
        coordinates
            Ordered reduced reciprocal coordinates.
        representatives
            Ordered integer cell representatives.
        period
            Positive direct-lattice period in the retained dimensionless convention.

        Returns
        -------
        numpy.ndarray
            Complex hopping-block array ordered by ``representatives``.

        Raises
        ------
        ValueError
            If the source and coordinate counts disagree.
        """
        if source.shape[0] != coordinates.size:
            raise ValueError("source and coordinate counts must agree")
        transform = (
            np.exp(-1j * np.outer(representatives * period, coordinates))
            / coordinates.size
        )
        transformed = np.einsum("rk,kij->rij", transform, source, optimize=True)
        return np.asarray(transformed, dtype=np.complex128)

    def reconstruct(
        self,
        hoppings: ComplexArray3,
        coordinates: RealVector,
        representatives: IntegerVector,
        period: float,
    ) -> ComplexArray3:
        """Evaluate the direct finite cell-to-reciprocal reconstruction sum.

        Parameters
        ----------
        hoppings
            Ordered rank-three complex hopping-block array.
        coordinates
            Reduced reciprocal coordinates at which to reconstruct matrices.
        representatives
            Integer cell representative corresponding to each hopping block.
        period
            Positive direct-lattice period in the retained dimensionless convention.

        Returns
        -------
        numpy.ndarray
            Reconstructed complex matrix path ordered by ``coordinates``.

        Raises
        ------
        ValueError
            If hopping and representative counts disagree.
        """
        if hoppings.shape[0] != representatives.size:
            raise ValueError("hopping and representative counts must agree")
        inverse = np.exp(1j * np.outer(coordinates, representatives * period))
        reconstructed = np.einsum("kr,rij->kij", inverse, hoppings, optimize=True)
        return np.asarray(reconstructed, dtype=np.complex128)

    def maximum_frobenius_defect(
        self, candidate: ComplexArray3, reference: ComplexArray3
    ) -> float:
        """Return the largest matrix Frobenius defect over equal paths.

        Parameters
        ----------
        candidate, reference
            Equal-shape rank-three complex matrix paths.

        Returns
        -------
        float
            Nonnegative maximum of the per-sample Frobenius defects.

        Raises
        ------
        ValueError
            If the paths do not have equal rank-three shape.
        """
        if candidate.shape != reference.shape or candidate.ndim != 3:
            raise ValueError("candidate and reference must have equal rank-three shape")
        return float(np.max(np.linalg.norm(candidate - reference, axis=(1, 2))))

    def exact_pair_hermiticity_residual(
        self, hoppings: ComplexArray3, representatives: IntegerVector
    ) -> float:
        r"""Return the largest defect over explicitly represented opposite pairs.

        This reproduces the retained exact-representative convention.  It does not
        apply a Born--von Karman modulus, so an unmatched even-mesh Nyquist
        representative is excluded rather than silently identified with itself.

        Parameters
        ----------
        hoppings
            Ordered rank-three hopping-block array.
        representatives
            Integer representative corresponding to each block.

        Returns
        -------
        float
            Maximum :math:`\|T_R-T_{-R}^\dagger\|_F` over available exact pairs.

        Raises
        ------
        ValueError
            If counts disagree or no exact opposite pair is represented.
        """
        if hoppings.shape[0] != representatives.size:
            raise ValueError("hopping and representative counts must agree")
        lookup = {
            int(representative): index
            for index, representative in enumerate(representatives)
        }
        residuals = tuple(
            float(
                np.linalg.norm(
                    hoppings[index] - hoppings[lookup[-int(representative)]].conj().T
                )
            )
            for index, representative in enumerate(representatives)
            if -int(representative) in lookup
        )
        if not residuals:
            raise ValueError("at least one represented opposite pair is required")
        return max(residuals)

    def range_report_defects(
        self,
        group: Periodic1DCompositeBandGroupResult,
        source: ComplexArray3,
        smooth: ComplexArray3,
        rough: ComplexArray3,
        coordinates: RealVector,
        representatives: IntegerVector,
        period: float,
    ) -> tuple[float, float]:
        """Compare independently recomputed omitted norms and training errors.

        Parameters
        ----------
        group
            Typed group containing the ordered historical range study.
        source
            Smooth reciprocal Hamiltonian path used as the training target.
        smooth, rough
            Complete smooth- and rough-gauge hopping arrays.
        coordinates
            Ordered training reciprocal coordinates.
        representatives
            Ordered integer cell representatives.
        period
            Direct-lattice period used by the finite Fourier pair.

        Returns
        -------
        tuple
            Maximum retained-versus-recomputed omitted-norm defect followed by the
            maximum training-eigenvalue-error defect, both in :math:`E_G`.

        Notes
        -----
        Withheld errors are not evaluated because the withheld reciprocal matrices
        were not retained.
        """
        targets = np.linalg.eigvalsh(source)
        omitted_defects: list[float] = []
        training_defects: list[float] = []
        for retained in group.range_study:
            mask = np.abs(representatives) <= retained.hopping_range_cells
            omitted_smooth = float(np.linalg.norm(smooth[~mask]))
            omitted_rough = float(np.linalg.norm(rough[~mask]))
            omitted_defects.extend(
                (
                    abs(omitted_smooth - retained.smooth_omitted_block_l2_norm),
                    abs(omitted_rough - retained.rough_omitted_block_l2_norm),
                )
            )
            smooth_path = self.reconstruct(
                smooth[mask], coordinates, representatives[mask], period
            )
            rough_path = self.reconstruct(
                rough[mask], coordinates, representatives[mask], period
            )
            smooth_error = float(
                np.max(np.abs(np.linalg.eigvalsh(smooth_path) - targets))
            )
            rough_error = float(
                np.max(np.abs(np.linalg.eigvalsh(rough_path) - targets))
            )
            training_defects.extend(
                (
                    abs(
                        smooth_error - retained.smooth_training_eigenvalue_maximum_error
                    ),
                    abs(rough_error - retained.rough_training_eigenvalue_maximum_error),
                )
            )
        return max(omitted_defects), max(training_defects)

    def direct_route_defects(
        self,
        group: Periodic1DCompositeBandGroupResult,
        source: ComplexArray3,
        smooth: ComplexArray3,
        coordinates: RealVector,
        representatives: IntegerVector,
        period: float,
    ) -> tuple[float, float]:
        """Recompute direct-fit versus transform-and-truncate route defects.

        Parameters
        ----------
        group
            Typed group supplying the direct-route hopping range.
        source
            Smooth reciprocal Hamiltonian path used as the fit target.
        smooth
            Complete transformed smooth-gauge hopping array.
        coordinates
            Ordered training reciprocal coordinates.
        representatives
            Ordered integer cell representatives.
        period
            Direct-lattice period used by both routes.

        Returns
        -------
        tuple
            Coefficient Frobenius defect and maximum training-operator Frobenius
            defect, both in :math:`E_G`.
        """
        mask = np.abs(representatives) <= group.direct_route.hopping_range_cells
        retained_representatives = representatives[mask]
        design = np.exp(1j * np.outer(coordinates, retained_representatives * period))
        dimension = source.shape[1]
        direct_flat = np.linalg.lstsq(
            design,
            source.reshape(coordinates.size, dimension * dimension),
            rcond=None,
        )[0]
        direct = direct_flat.reshape(
            retained_representatives.size, dimension, dimension
        )
        mediated = smooth[mask]
        direct_path = self.reconstruct(
            direct, coordinates, retained_representatives, period
        )
        mediated_path = self.reconstruct(
            mediated, coordinates, retained_representatives, period
        )
        return (
            float(np.linalg.norm(direct - mediated)),
            self.maximum_frobenius_defect(direct_path, mediated_path),
        )

    def array_sha256(self, values: ComplexArray3) -> str:
        """Return SHA-256 over canonical contiguous little-endian ``complex128``.

        Parameters
        ----------
        values
            Rank-three represented complex array.

        Returns
        -------
        str
            Lowercase hexadecimal SHA-256 identity over C-order bytes.
        """
        canonical = np.ascontiguousarray(values, dtype="<c16")
        return hashlib.sha256(canonical.tobytes(order="C")).hexdigest()
