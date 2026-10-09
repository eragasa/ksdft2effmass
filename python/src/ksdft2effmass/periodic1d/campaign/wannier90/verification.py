r"""Independent retained-result verification for Appendix G Wilson loops.

The module reconstructs a discrete one-dimensional Wilson loop from authenticated
Wannier90 neighbor data.  For the selected positive-direction reciprocal loop, each
native overlap matrix :math:`M_j` is replaced by its unitary polar factor
:math:`Q_j`, and the represented loop is

.. math::

   W = Q_0 Q_1 \cdots Q_{N_k-1}.

A second route first applies the retained native gauge matrices
:math:`U_j`, giving :math:`M'_j=U_j^\dagger M_j U_{j+1}` with the periodic endpoint
identified by the native neighbor record.  The verifier compares both Wilson
phase multisets with the retained spectrum using circular assignment.

This is an independent verification surface: it does not import the production frame
transporter, Wilson-spectrum canonicalizer, Wilson comparator, historical extractor,
or historical verifier.  Authentication and native parsing are performed upstream by
``Periodic1DWannier90NativeArtifactWorkflow``.  Passing establishes only the declared
software and bounded numerical-verification requirements for the represented data; it
does not establish topology, polarization, material validity, or uncertainty
quantification.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
from scipy.optimize import linear_sum_assignment  # type: ignore[import-untyped]

from ksdft2effmass.integration.wannier90 import Wannier90ParsedNativeArtifactSet
from ksdft2effmass.solid_state import WilsonLoopSpectrum1D

from .native_artifacts import (
    Periodic1DWannier90NativeArtifactGroupResult,
    Periodic1DWannier90NativeArtifactWorkflowResult,
)
from .results import Periodic1DWannier90WilsonGroupResult

type ComplexMatrix = npt.NDArray[np.complex128]


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90WilsonVerificationRequest:
    r"""Declare authenticated native results and independent verifier controls.

    Parameters
    ----------
    native_result
        Output of ``Periodic1DWannier90NativeArtifactWorkflow``.  It contains the
        typed retained result, exact artifact correlation, and parsed native records.
    phase_absolute_tolerance
        Maximum accepted circular phase-set defect, in dimensionless radians.
    loop_unitarity_absolute_tolerance
        Maximum accepted Frobenius norm of :math:`W^\dagger W-I` for either loop.
    minimum_active_overlap_singular_value
        Minimum accepted singular value among all selected active overlap matrices.
        This is a conditioning threshold, not a phase tolerance.

    Notes
    -----
    All controls must be finite nonnegative built-in ``float`` values.  The request
    intentionally carries tolerances rather than selecting campaign policy internally.
    """

    native_result: Periodic1DWannier90NativeArtifactWorkflowResult
    phase_absolute_tolerance: float
    loop_unitarity_absolute_tolerance: float
    minimum_active_overlap_singular_value: float

    def __post_init__(self) -> None:
        """Validate exact AbstractResultObject ownership and numerical controls.

        Raises
        ------
        TypeError
            If ``native_result`` has the wrong exact semantic type or a control is not
            an exact built-in ``float``.
        ValueError
            If a control is nonfinite or negative.
        """
        self._check_args_native_result()
        self._check_args_controls()

    def _check_args_native_result(self) -> None:
        """Require the exact authenticated native-workflow result."""
        if (
            type(self.native_result)
            is not Periodic1DWannier90NativeArtifactWorkflowResult
        ):
            raise TypeError(
                "native_result uses the wrong Workflow AbstractResultObject"
            )

    def _check_args_controls(self) -> None:
        """Require finite nonnegative built-in-float acceptance controls."""
        for name, value in (
            ("phase_absolute_tolerance", self.phase_absolute_tolerance),
            (
                "loop_unitarity_absolute_tolerance",
                self.loop_unitarity_absolute_tolerance,
            ),
            (
                "minimum_active_overlap_singular_value",
                self.minimum_active_overlap_singular_value,
            ),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not np.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90WilsonGroupVerificationResult:
    r"""Retain independent Wilson verification for one retained band group.

    Parameters
    ----------
    group_id
        Stable retained group identifier.
    active_overlap_count
        Number of selected positive-direction reciprocal edges.  A closed complete
        loop has one edge for every reciprocal point.
    minimum_active_overlap_singular_value
        Minimum singular value over the selected raw overlap matrices.
    direct_spectrum
        Spectrum reconstructed from unitary polar factors of the raw overlaps.
    native_gauge_spectrum
        Spectrum reconstructed after applying retained ``_u.mat`` gauge matrices.
    direct_retained_maximum_phase_defect
        Circular phase-set defect between ``direct_spectrum`` and the retained result.
    native_gauge_retained_maximum_phase_defect
        Circular phase-set defect between ``native_gauge_spectrum`` and the retained
        result.
    gauge_covariance_maximum_phase_defect
        Circular phase-set defect between the two reconstructed routes.
    direct_loop_unitarity_frobenius_defect, native_gauge_loop_unitarity_frobenius_defect
        Frobenius defects :math:`\lVert W^\dagger W-I\rVert_F`.
    phase_absolute_tolerance, loop_unitarity_absolute_tolerance
        Explicit acceptance controls for phase and unitarity defects.
    minimum_overlap_singular_value_threshold
        Explicit lower acceptance threshold for active-overlap conditioning.
    passes
        ``True`` exactly when every phase and unitarity defect passes and the minimum
        overlap singular value is at least its threshold.
    """

    group_id: str
    active_overlap_count: int
    minimum_active_overlap_singular_value: float
    direct_spectrum: WilsonLoopSpectrum1D
    native_gauge_spectrum: WilsonLoopSpectrum1D
    direct_retained_maximum_phase_defect: float
    native_gauge_retained_maximum_phase_defect: float
    gauge_covariance_maximum_phase_defect: float
    direct_loop_unitarity_frobenius_defect: float
    native_gauge_loop_unitarity_frobenius_defect: float
    phase_absolute_tolerance: float
    loop_unitarity_absolute_tolerance: float
    minimum_overlap_singular_value_threshold: float
    passes: bool

    def __post_init__(self) -> None:
        """Validate dimensions, finite diagnostics, controls, and disposition.

        Raises
        ------
        TypeError
            If a spectrum, diagnostic, control, or ``passes`` value has the wrong exact
            semantic type.
        ValueError
            If identifiers, dimensions, finite ranges, spectrum ranks, or the derived
            disposition are inconsistent.
        """
        self._check_args_identity_and_count()
        self._check_args_spectra()
        self._check_args_diagnostics()
        self._check_args_disposition()

    def _check_args_identity_and_count(self) -> None:
        """Require a nonempty explicit group identity and positive edge count."""
        if type(self.group_id) is not str or not self.group_id:
            raise ValueError("group_id must be a nonempty built-in str")
        if type(self.active_overlap_count) is not int:
            raise TypeError("active_overlap_count must be a built-in int")
        if self.active_overlap_count <= 0:
            raise ValueError("active_overlap_count must be positive")

    def _check_args_spectra(self) -> None:
        """Require exact reconstructed spectra of equal retained rank."""
        if type(self.direct_spectrum) is not WilsonLoopSpectrum1D:
            raise TypeError("direct_spectrum must be WilsonLoopSpectrum1D")
        if type(self.native_gauge_spectrum) is not WilsonLoopSpectrum1D:
            raise TypeError("native_gauge_spectrum must be WilsonLoopSpectrum1D")
        if self.direct_spectrum.rank != self.native_gauge_spectrum.rank:
            raise ValueError("reconstructed Wilson spectra must have equal rank")

    def _check_args_diagnostics(self) -> None:
        """Require finite nonnegative diagnostics and acceptance controls."""
        values = (
            self.minimum_active_overlap_singular_value,
            self.direct_retained_maximum_phase_defect,
            self.native_gauge_retained_maximum_phase_defect,
            self.gauge_covariance_maximum_phase_defect,
            self.direct_loop_unitarity_frobenius_defect,
            self.native_gauge_loop_unitarity_frobenius_defect,
            self.phase_absolute_tolerance,
            self.loop_unitarity_absolute_tolerance,
            self.minimum_overlap_singular_value_threshold,
        )
        if any(type(value) is not float for value in values):
            raise TypeError("Wilson verification diagnostics must be built-in floats")
        if any(not np.isfinite(value) or value < 0.0 for value in values):
            raise ValueError(
                "Wilson verification diagnostics must be finite and nonnegative"
            )

    def _check_args_disposition(self) -> None:
        """Derive and validate the bounded aggregate disposition."""
        if type(self.passes) is not bool:
            raise TypeError("passes must be a built-in bool")
        expected_passes = (
            max(
                self.direct_retained_maximum_phase_defect,
                self.native_gauge_retained_maximum_phase_defect,
                self.gauge_covariance_maximum_phase_defect,
            )
            <= self.phase_absolute_tolerance
            and max(
                self.direct_loop_unitarity_frobenius_defect,
                self.native_gauge_loop_unitarity_frobenius_defect,
            )
            <= self.loop_unitarity_absolute_tolerance
            and self.minimum_active_overlap_singular_value
            >= self.minimum_overlap_singular_value_threshold
        )
        if self.passes is not expected_passes:
            raise ValueError(
                "passes must agree with all retained verification controls"
            )


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90WilsonVerificationResult:
    """Retain independent Wilson verification for every native band group.

    Parameters
    ----------
    groups
        Nonempty tuple of uniquely identified group verification results in retained
        campaign order.
    passes
        Aggregate disposition.  It is ``True`` exactly when every group passes.
    """

    groups: tuple[Periodic1DWannier90WilsonGroupVerificationResult, ...]
    passes: bool

    def __post_init__(self) -> None:
        """Validate group inventory and aggregate disposition.

        Raises
        ------
        TypeError
            If the group tuple or aggregate disposition has the wrong semantic type.
        ValueError
            If group identifiers repeat or ``passes`` disagrees with group results.
        """
        self._check_args_groups()
        self._check_args_disposition()

    def _check_args_groups(self) -> None:
        """Require nonempty exact group records with unique explicit identities."""
        if (
            type(self.groups) is not tuple
            or not self.groups
            or any(
                type(group) is not Periodic1DWannier90WilsonGroupVerificationResult
                for group in self.groups
            )
        ):
            raise TypeError("groups must be a nonempty typed tuple")
        group_ids = tuple(group.group_id for group in self.groups)
        if len(set(group_ids)) != len(group_ids):
            raise ValueError("verification group identifiers must be unique")

    def _check_args_disposition(self) -> None:
        """Require the aggregate Boolean to equal all group dispositions."""
        if type(self.passes) is not bool:
            raise TypeError("passes must be a built-in bool")
        if self.passes is not all(group.passes for group in self.groups):
            raise ValueError("aggregate disposition must agree with every group")


class Periodic1DWannier90WilsonVerifier:
    r"""Independently reconstruct Wilson spectra from native overlaps and gauges.

    The active loop contains the edge :math:`j\rightarrow j+1` for every reciprocal
    point.  The final edge wraps to point zero and must carry reciprocal shift
    :math:`(1,0,0)`; all preceding active edges carry zero shift.  This distinguishes
    the physical one-dimensional loop from the inactive transverse neighbors embedded
    in the native interface.

    For :math:`M_j=L_j\Sigma_jR_j^\dagger`, the verifier uses
    :math:`Q_j=L_jR_j^\dagger`.  The ordered product convention is
    :math:`W\leftarrow WQ_j`.  Under a periodic exact unitary gauge, the transformed
    loop is similar to the raw loop, so their unordered eigenphase multisets agree.
    Finite text precision and imperfect retained unitarity are measured rather than
    assumed away.

    Notes
    -----
    The phase-set assignment minimizes total absolute circular residual.  The reported
    defect is the largest residual within that assignment.  Principal phases use the
    half-open branch :math:`[-\pi,\pi)`. For :math:`N_k` active edges and retained rank
    :math:`r`, dense polar decompositions cost :math:`O(N_k r^3)` time, loop
    eigendecomposition and circular assignment each cost :math:`O(r^3)` time, and the
    verifier's dense working storage is :math:`O(r^2)` in addition to the parsed
    :math:`O(N_k r^2)` overlaps. No arbitrary size cap is imposed; allocation can raise
    :class:`MemoryError`. The geometric-phase and Wannier background is
    described in [WVKS1993]_ and [WVM2012]_; this verifier establishes only its stated
    represented numerical comparisons.

    References
    ----------
    .. [WVKS1993] R. D. King-Smith and D. Vanderbilt, "Theory of polarization of
       crystalline solids," *Physical Review B* **47**, 1651--1654 (1993).
       https://doi.org/10.1103/PhysRevB.47.1651
    .. [WVM2012] N. Marzari, A. A. Mostofi, J. R. Yates, I. Souza, and D. Vanderbilt,
       "Maximally localized Wannier functions: Theory and applications,"
       *Reviews of Modern Physics* **84**, 1419--1475 (2012).
       https://doi.org/10.1103/RevModPhys.84.1419

    See Also
    --------
    ksdft2effmass.solid_state.WilsonLoopSpectrum1D
        Immutable public representation used for retained phase multisets.
    Periodic1DWannier90NativeArtifactWorkflowResult
        Authenticated and parsed native input to this verifier.
    """

    __slots__ = ()

    def execute(
        self, request: Periodic1DWannier90WilsonVerificationRequest
    ) -> Periodic1DWannier90WilsonVerificationResult:
        """Verify every retained native group in campaign order.

        Parameters
        ----------
        request
            Authenticated native records and explicit acceptance controls.

        Returns
        -------
        Periodic1DWannier90WilsonVerificationResult
            Per-group reconstructed spectra and an aggregate disposition.

        Raises
        ------
        TypeError
            If ``request`` has the wrong exact semantic type.
        ValueError
            If native and retained group inventories disagree or a group's structural
            native contracts do not define one complete active loop.
        RuntimeError
            If the phase-assignment backend violates its row-coverage contract.
        numpy.linalg.LinAlgError
            If a dense singular-value or eigenvalue decomposition does not converge.
        MemoryError
            If dense loop, decomposition, or assignment storage cannot be allocated.
        """
        if type(request) is not Periodic1DWannier90WilsonVerificationRequest:
            raise TypeError(
                "request must be Periodic1DWannier90WilsonVerificationRequest"
            )
        expected_groups = request.native_result.campaign_result.groups
        native_groups = request.native_result.groups
        if tuple(group.group_id for group in native_groups) != tuple(
            group.group_id for group in expected_groups
        ):
            raise ValueError("native and retained Wilson group inventories disagree")
        groups = tuple(
            self._verify_group(expected, native, request)
            for expected, native in zip(expected_groups, native_groups, strict=True)
        )
        return Periodic1DWannier90WilsonVerificationResult(
            groups, all(group.passes for group in groups)
        )

    def _verify_group(
        self,
        expected: Periodic1DWannier90WilsonGroupResult,
        native: Periodic1DWannier90NativeArtifactGroupResult,
        request: Periodic1DWannier90WilsonVerificationRequest,
    ) -> Periodic1DWannier90WilsonGroupVerificationResult:
        """Reconstruct and compare one raw and native-gauge Wilson loop.

        Parameters
        ----------
        expected
            Typed retained Wilson spectrum and group metadata.
        native
            Authenticated and parsed native artifacts for the same group.
        request
            Verification controls shared by all groups.

        Returns
        -------
        Periodic1DWannier90WilsonGroupVerificationResult
            Reconstructed spectra, conditioning, defects, controls, and disposition.

        Raises
        ------
        ValueError
            If neighbor records fail to form one complete active loop.
        RuntimeError
            If circular assignment fails to cover every reference phase.
        """
        parsed = native.parsed_artifacts
        # Selection fixes reciprocal ordering and the final Bloch seam before any
        # matrix product is formed; transverse neighbor records remain excluded.
        active = self._active_overlap_matrices(parsed)
        direct_loop = np.eye(expected.direct_spectrum.rank, dtype=np.complex128)
        gauge_loop = np.eye(expected.direct_spectrum.rank, dtype=np.complex128)
        minimum_singular_value = np.inf
        for first, second, overlap in active:
            # Conditioning remains an evidence channel separate from the unitary
            # polar factor used to represent parallel transport.
            singular_values = np.linalg.svd(overlap, compute_uv=False)
            minimum_singular_value = min(
                minimum_singular_value, float(np.min(singular_values))
            )
            direct_loop = direct_loop @ self._polar_unitary(overlap)
            first_gauge = parsed.unitary_matrices.matrices[first].magnitude
            second_gauge = parsed.unitary_matrices.matrices[second].magnitude
            # This is the independent native-gauge route M'_j = U_j^† M_j U_{j+1};
            # agreement is measured after loop assembly rather than assumed.
            transformed = first_gauge.conj().T @ overlap @ second_gauge
            gauge_loop = gauge_loop @ self._polar_unitary(transformed)
        direct_spectrum = self._spectrum(direct_loop)
        gauge_spectrum = self._spectrum(gauge_loop)
        direct_retained = self._phase_set_defect(
            expected.direct_spectrum, direct_spectrum
        )
        gauge_retained = self._phase_set_defect(
            expected.direct_spectrum, gauge_spectrum
        )
        gauge_covariance = self._phase_set_defect(direct_spectrum, gauge_spectrum)
        direct_unitarity = self._unitarity_defect(direct_loop)
        gauge_unitarity = self._unitarity_defect(gauge_loop)
        passes = (
            max(direct_retained, gauge_retained, gauge_covariance)
            <= request.phase_absolute_tolerance
            and max(direct_unitarity, gauge_unitarity)
            <= request.loop_unitarity_absolute_tolerance
            and minimum_singular_value >= request.minimum_active_overlap_singular_value
        )
        return Periodic1DWannier90WilsonGroupVerificationResult(
            expected.group_id,
            len(active),
            float(minimum_singular_value),
            direct_spectrum,
            gauge_spectrum,
            direct_retained,
            gauge_retained,
            gauge_covariance,
            direct_unitarity,
            gauge_unitarity,
            request.phase_absolute_tolerance,
            request.loop_unitarity_absolute_tolerance,
            request.minimum_active_overlap_singular_value,
            passes,
        )

    def _active_overlap_matrices(
        self, parsed: Wannier90ParsedNativeArtifactSet
    ) -> tuple[tuple[int, int, ComplexMatrix], ...]:
        """Select one positive active-direction overlap per reciprocal point.

        Parameters
        ----------
        parsed
            Correlated parsed ``.nnkp`` and ``.mmn`` records plus the remaining native
            scientific artifacts.

        Returns
        -------
        tuple of tuple
            Ordered ``(first_index, second_index, overlap_matrix)`` records, beginning
            at reciprocal point zero and ending with the wrapped endpoint edge.

        Raises
        ------
        ValueError
            If ``.nnkp`` and ``.mmn`` inventories disagree, an active first point is
            duplicated, or the selected loop does not cover every reciprocal point.
        """
        neighbors = parsed.neighbor_list
        overlaps = parsed.neighbor_overlaps
        if len(neighbors.records) != len(overlaps.matrices):
            raise ValueError("nnkp and mmn record counts do not agree")
        active: dict[int, tuple[int, ComplexMatrix]] = {}
        for record, first, second, shift, matrix in zip(
            neighbors.records,
            overlaps.first_kpoint_indices,
            overlaps.second_kpoint_indices,
            overlaps.reciprocal_shifts,
            overlaps.matrices,
            strict=True,
        ):
            if record != (first + 1, second + 1, *shift):
                raise ValueError("nnkp and mmn neighbor records do not agree")
            expected_second = (first + 1) % overlaps.kpoint_count
            expected_shift = (
                (1, 0, 0) if first == overlaps.kpoint_count - 1 else (0, 0, 0)
            )
            if second == expected_second and shift == expected_shift:
                if first in active:
                    raise ValueError("active loop contains a duplicate first k point")
                active[first] = (second, matrix.magnitude)
        expected_first = tuple(range(overlaps.kpoint_count))
        if tuple(sorted(active)) != expected_first:
            raise ValueError("active loop does not cover every k point exactly once")
        return tuple(
            (first, active[first][0], active[first][1]) for first in expected_first
        )

    @staticmethod
    def _polar_unitary(matrix: ComplexMatrix) -> ComplexMatrix:
        r"""Return the unitary polar factor from an independent SVD assembly.

        Parameters
        ----------
        matrix
            Square complex overlap matrix :math:`M`.

        Returns
        -------
        numpy.ndarray
            :math:`LR^\dagger` for :math:`M=L\Sigma R^\dagger`, represented as
            ``complex128``.
        """
        left, _, right_h = np.linalg.svd(matrix)
        return np.asarray(left @ right_h, dtype=np.complex128)

    @staticmethod
    def _spectrum(matrix: ComplexMatrix) -> WilsonLoopSpectrum1D:
        r"""Return sorted principal eigenphases of one represented loop matrix.

        Parameters
        ----------
        matrix
            Square complex Wilson-loop representation.

        Returns
        -------
        WilsonLoopSpectrum1D
            Increasing deterministic storage of the unordered eigenphase multiset in
            :math:`[-\pi,\pi)`.
        """
        phases = np.angle(np.linalg.eigvals(matrix))
        normalized = tuple(
            float(-np.pi if phase >= np.pi else phase) for phase in phases
        )
        return WilsonLoopSpectrum1D(tuple(sorted(normalized)))

    @staticmethod
    def _phase_set_defect(
        reference: WilsonLoopSpectrum1D, candidate: WilsonLoopSpectrum1D
    ) -> float:
        r"""Return the maximum residual under optimal circular phase assignment.

        Parameters
        ----------
        reference, candidate
            Equal-rank canonical Wilson phase multisets.

        Returns
        -------
        float
            Largest absolute principal circular residual, in radians, after the
            minimum-total-absolute assignment.

        Raises
        ------
        ValueError
            If the spectra have different ranks.
        RuntimeError
            If the assignment backend does not cover all reference rows.
        """
        if reference.rank != candidate.rank:
            raise ValueError("Wilson spectra must have equal rank")
        reference_values = np.asarray(reference.eigenphases, dtype=np.float64)
        candidate_values = np.asarray(candidate.eigenphases, dtype=np.float64)
        # Pairwise residuals are wrapped to the half-open principal branch before
        # Hungarian assignment, so ordinary sorting cannot hide seam crossings.
        signed = (
            candidate_values[np.newaxis, :] - reference_values[:, np.newaxis] + np.pi
        ) % (2.0 * np.pi) - np.pi
        rows, columns = linear_sum_assignment(np.abs(signed))
        if not np.array_equal(rows, np.arange(reference.rank, dtype=np.int64)):
            raise RuntimeError("phase assignment did not cover reference rows")
        return max(
            abs(float(signed[row, column]))
            for row, column in zip(rows, columns, strict=True)
        )

    @staticmethod
    def _unitarity_defect(matrix: ComplexMatrix) -> float:
        r"""Return the represented loop's Frobenius unitarity defect.

        Parameters
        ----------
        matrix
            Square complex loop matrix :math:`W`.

        Returns
        -------
        float
            :math:`\lVert W^\dagger W-I\rVert_F` in represented binary64 precision.
        """
        identity = np.eye(matrix.shape[0], dtype=np.complex128)
        return float(np.linalg.norm(matrix.conj().T @ matrix - identity, ord="fro"))
