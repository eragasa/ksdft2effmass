r"""Wilson-loop phase spectra and circular phase-set comparison in one dimension.

This module represents the eigenphases of a finite Wilson-loop matrix after that
matrix has been constructed by another owner.  If a loop matrix has eigenvalues
:math:`\lambda_j`, its represented phases satisfy

.. math::

   \lambda_j = \exp(i\theta_j), \qquad -\pi \leq \theta_j < \pi.

A spectrum is an unordered multiset.  ``WilsonLoopSpectrum1D`` therefore requires
increasing storage only to provide a deterministic representation; the order carries
no band-label correspondence.  ``WilsonLoopPhaseSetComparator1D`` compares two such
multisets by a minimum-total-absolute circular assignment rather than by their stored
positions.

All phases, residuals, and tolerances are dimensionless built-in ``float`` values in
radians.  Booleans, integer values, NumPy scalar values, strings, and nonfinite values
are rejected at public numeric boundaries.  This module does not construct overlap
matrices, choose a reciprocal-loop orientation, infer a gauge, unwrap phase branches,
or establish a topological invariant, polarization, scientific validation, or
uncertainty quantification.

References
----------
.. [1] R. D. King-Smith and D. Vanderbilt, "Theory of polarization of crystalline
   solids," *Physical Review B* **47**, 1651--1654 (1993).
   https://doi.org/10.1103/PhysRevB.47.1651
.. [2] N. Marzari, A. A. Mostofi, J. R. Yates, I. Souza, and D. Vanderbilt,
   "Maximally localized Wannier functions: Theory and applications,"
   *Reviews of Modern Physics* **84**, 1419--1475 (2012).
   https://doi.org/10.1103/RevModPhys.84.1419
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

import numpy as np
from scipy.optimize import linear_sum_assignment  # type: ignore[import-untyped]


class WilsonCenterConvention1D(StrEnum):
    r"""Identify an explicit Wilson-phase-to-center convention.

    Attributes
    ----------
    PHASE_OVER_TWO_PI
        Map a principal phase :math:`\theta` to the dimensionless center coordinate
        :math:`x/a=\theta/(2\pi)`, where :math:`a` is the lattice period.  The result
        lies in the half-open interval :math:`[-1/2,1/2)` and remains defined only
        modulo one lattice period.
    """

    PHASE_OVER_TWO_PI = "phase_over_two_pi"


@dataclass(frozen=True, slots=True)
class WilsonLoopSpectrum1D:
    r"""Retain an unordered Wilson eigenphase multiset in canonical storage.

    Parameters
    ----------
    eigenphases
        Nonempty tuple of finite built-in ``float`` values in radians.  Values must
        already lie in :math:`[-\pi,\pi)` and be sorted increasingly.  Repeated values
        are permitted and represent phase degeneracy.

    Notes
    -----
    Increasing order is a serialization convention, not a correspondence between
    individual bands in two spectra.  Use ``WilsonLoopSpectrumCanonicalizer1D`` for
    arbitrary finite phase representatives and ``WilsonLoopPhaseSetComparator1D`` for
    unordered comparison.  The geometric-phase and Wannier interpretations motivating
    phase/center relations are described in [WLSKS1993]_ and [WLSM2012]_; this record
    deliberately stores only the represented phase multiset.

    References
    ----------
    .. [WLSKS1993] R. D. King-Smith and D. Vanderbilt, "Theory of polarization of
       crystalline solids," *Physical Review B* **47**, 1651--1654 (1993).
       https://doi.org/10.1103/PhysRevB.47.1651
    .. [WLSM2012] N. Marzari, A. A. Mostofi, J. R. Yates, I. Souza, and D. Vanderbilt,
       "Maximally localized Wannier functions: Theory and applications,"
       *Reviews of Modern Physics* **84**, 1419--1475 (2012).
       https://doi.org/10.1103/RevModPhys.84.1419
    """

    eigenphases: tuple[float, ...]

    def __post_init__(self) -> None:
        r"""Validate the intrinsic principal-branch spectrum invariants.

        Raises
        ------
        TypeError
            If ``eigenphases`` is not a nonempty tuple.
        ValueError
            If a member is not a finite built-in ``float``, lies outside
            :math:`[-\pi,\pi)`, or the tuple is not increasingly sorted.
        """
        if not isinstance(self.eigenphases, tuple) or not self.eigenphases:
            raise TypeError("eigenphases must be a nonempty tuple")
        if any(
            type(phase) is not float or not np.isfinite(phase)
            for phase in self.eigenphases
        ):
            raise ValueError("eigenphases must contain finite built-in floats")
        if any(phase < -np.pi or phase >= np.pi for phase in self.eigenphases):
            raise ValueError("eigenphases must lie in the half-open branch [-pi, pi)")
        if self.eigenphases != tuple(sorted(self.eigenphases)):
            raise ValueError("eigenphases must use canonical increasing storage")

    @property
    def rank(self) -> int:
        """Return the number of represented Wilson eigenphases.

        Returns
        -------
        int
            Composite-subspace rank represented by the phase multiset.
        """
        return len(self.eigenphases)

    def centers_over_period(
        self, convention: WilsonCenterConvention1D
    ) -> tuple[float, ...]:
        r"""Return dimensionless centers modulo one lattice period.

        Parameters
        ----------
        convention
            Explicit phase-to-center mapping.  The supported mapping returns
            :math:`x_j/a=\theta_j/(2\pi)` in canonical phase-storage order.

        Returns
        -------
        tuple of float
            Center coordinates divided by the lattice period.  They inherit the
            half-open interval :math:`[-1/2,1/2)` and are not unwrapped positions.

        Raises
        ------
        TypeError
            If ``convention`` is not ``WilsonCenterConvention1D``.
        ValueError
            If a future enum member lacks an implemented mapping.
        """
        if type(convention) is not WilsonCenterConvention1D:
            raise TypeError("convention must be WilsonCenterConvention1D")
        if convention is WilsonCenterConvention1D.PHASE_OVER_TWO_PI:
            return tuple(phase / (2.0 * np.pi) for phase in self.eigenphases)
        raise ValueError("unsupported Wilson center convention")


class WilsonLoopSpectrumCanonicalizer1D:
    r"""Canonicalize arbitrary finite representatives of a Wilson phase multiset.

    Each input phase :math:`\phi` is mapped by

    .. math::

       \theta = ((\phi+\pi) \bmod 2\pi)-\pi,

    then the resulting values are sorted increasingly.  In particular, positive
    :math:`\pi` maps to the canonical negative Nyquist representative :math:`-\pi`.
    """

    __slots__ = ()

    def execute(self, eigenphases: tuple[float, ...]) -> WilsonLoopSpectrum1D:
        r"""Return canonical principal-branch storage for ``eigenphases``.

        Parameters
        ----------
        eigenphases
            Nonempty tuple of finite built-in ``float`` phase representatives in
            radians.  Values may use any integer multiple of :math:`2\pi` and need
            not be sorted.

        Returns
        -------
        WilsonLoopSpectrum1D
            Normalized and increasingly sorted phase multiset.

        Raises
        ------
        TypeError
            If ``eigenphases`` is not a nonempty tuple.
        ValueError
            If any phase is not a finite built-in ``float``.
        """
        if not isinstance(eigenphases, tuple) or not eigenphases:
            raise TypeError("eigenphases must be a nonempty tuple")
        if any(
            type(phase) is not float or not np.isfinite(phase) for phase in eigenphases
        ):
            raise ValueError("eigenphases must contain finite built-in floats")
        normalized = tuple(
            phase
            if -np.pi <= phase < np.pi
            else float((phase + np.pi) % (2.0 * np.pi) - np.pi)
            for phase in eigenphases
        )
        return WilsonLoopSpectrum1D(tuple(sorted(normalized)))


@dataclass(frozen=True, slots=True)
class WilsonLoopPhaseSetComparisonResult1D:
    r"""Retain an optimal circular matching of two Wilson phase multisets.

    Parameters
    ----------
    reference, candidate
        Equal-rank canonical spectra.  ``reference`` supplies residual row order;
        ``candidate`` is permuted by ``matched_candidate_indices``.
    matched_candidate_indices
        Complete permutation where entry :math:`j` identifies the candidate phase
        matched to reference phase :math:`j`.
    signed_phase_residuals
        Candidate-minus-reference circular residuals in :math:`[-\pi,\pi)`.
    maximum_absolute_phase_defect
        Maximum absolute circular residual, in radians.
    phase_l2_defect
        Euclidean norm of the signed residual vector, in radians.
    absolute_tolerance
        Finite nonnegative built-in ``float`` acceptance tolerance, in radians.
    passes
        ``True`` exactly when the maximum absolute defect does not exceed the
        tolerance.

    Notes
    -----
    The assignment minimizes the sum of absolute circular residuals.  If several
    assignments have the same minimum, ``matched_candidate_indices`` records the
    assignment returned by SciPy; no physical band labeling is inferred.
    """

    reference: WilsonLoopSpectrum1D
    candidate: WilsonLoopSpectrum1D
    matched_candidate_indices: tuple[int, ...]
    signed_phase_residuals: tuple[float, ...]
    maximum_absolute_phase_defect: float
    phase_l2_defect: float
    absolute_tolerance: float
    passes: bool

    def __post_init__(self) -> None:
        """Validate rank, permutation, residual, norm, and disposition correlations.

        Raises
        ------
        TypeError
            If spectra or ``passes`` have the wrong exact semantic types.
        ValueError
            If ranks differ; the matching is not a complete permutation; residuals
            are nonfinite, out of branch, or have the wrong count; defects or
            tolerance are invalid; or retained summaries disagree with residuals.
        """
        if type(self.reference) is not WilsonLoopSpectrum1D:
            raise TypeError("reference must be WilsonLoopSpectrum1D")
        if type(self.candidate) is not WilsonLoopSpectrum1D:
            raise TypeError("candidate must be WilsonLoopSpectrum1D")
        if self.reference.rank != self.candidate.rank:
            raise ValueError("Wilson spectra must have equal rank")
        expected_indices = tuple(range(self.reference.rank))
        if tuple(sorted(self.matched_candidate_indices)) != expected_indices:
            raise ValueError("matched_candidate_indices must be a complete permutation")
        if len(self.signed_phase_residuals) != self.reference.rank:
            raise ValueError("one phase residual is required per reference phase")
        if any(
            type(residual) is not float
            or not np.isfinite(residual)
            or residual < -np.pi
            or residual >= np.pi
            for residual in self.signed_phase_residuals
        ):
            raise ValueError("phase residuals must use the principal circular branch")
        for name, value in (
            ("maximum_absolute_phase_defect", self.maximum_absolute_phase_defect),
            ("phase_l2_defect", self.phase_l2_defect),
            ("absolute_tolerance", self.absolute_tolerance),
        ):
            if type(value) is not float or not np.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be a finite nonnegative built-in float")
        expected_maximum = max(abs(value) for value in self.signed_phase_residuals)
        expected_l2 = float(np.linalg.norm(self.signed_phase_residuals))
        if self.maximum_absolute_phase_defect != expected_maximum:
            raise ValueError("maximum phase defect must match residuals")
        if self.phase_l2_defect != expected_l2:
            raise ValueError("phase_l2_defect must match residuals")
        if type(self.passes) is not bool:
            raise TypeError("passes must be a built-in bool")
        if self.passes is not (expected_maximum <= self.absolute_tolerance):
            raise ValueError("passes must match the maximum defect and tolerance")


class WilsonLoopPhaseSetComparator1D:
    r"""Compare equal-rank Wilson phase multisets by circular assignment.

    For reference phase :math:`\theta_i` and candidate phase :math:`\phi_j`, the
    signed pair residual is

    .. math::

       \delta_{ij}=((\phi_j-\theta_i+\pi)\bmod 2\pi)-\pi.

    The ActionObject uses a linear-sum assignment with costs :math:`|\delta_{ij}|`.
    It reports both the maximum absolute residual used for acceptance and the
    Euclidean residual norm.  It does not align frames or compare Wilson matrices.
    """

    __slots__ = ()

    def execute(
        self,
        reference: WilsonLoopSpectrum1D,
        candidate: WilsonLoopSpectrum1D,
        absolute_tolerance: float,
    ) -> WilsonLoopPhaseSetComparisonResult1D:
        r"""Return minimum-total-absolute circular matching and defects.

        Parameters
        ----------
        reference, candidate
            Equal-rank canonical Wilson spectra.  Their stored order is not treated as
            an existing correspondence.
        absolute_tolerance
            Finite nonnegative built-in ``float`` tolerance in radians.  Acceptance
            uses the maximum absolute matched residual.

        Returns
        -------
        WilsonLoopPhaseSetComparisonResult1D
            Matching permutation, signed principal residuals, maximum and Euclidean
            defects, tolerance, and derived disposition.

        Raises
        ------
        TypeError
            If either spectrum or the tolerance has the wrong exact semantic type.
        ValueError
            If ranks differ or the tolerance is negative or nonfinite.
        RuntimeError
            If the assignment backend does not cover reference rows in order, which
            indicates an internal solver-contract failure.
        """
        if type(reference) is not WilsonLoopSpectrum1D:
            raise TypeError("reference must be WilsonLoopSpectrum1D")
        if type(candidate) is not WilsonLoopSpectrum1D:
            raise TypeError("candidate must be WilsonLoopSpectrum1D")
        if reference.rank != candidate.rank:
            raise ValueError("Wilson spectra must have equal rank")
        if (
            type(absolute_tolerance) is not float
            or not np.isfinite(absolute_tolerance)
            or absolute_tolerance < 0.0
        ):
            raise ValueError("absolute_tolerance must be finite and nonnegative")
        reference_values = np.asarray(reference.eigenphases, dtype=np.float64)
        candidate_values = np.asarray(candidate.eigenphases, dtype=np.float64)
        signed = (
            candidate_values[np.newaxis, :] - reference_values[:, np.newaxis] + np.pi
        ) % (2.0 * np.pi) - np.pi
        rows, columns = linear_sum_assignment(np.abs(signed))
        if not np.array_equal(rows, np.arange(reference.rank, dtype=np.int64)):
            raise RuntimeError("assignment did not cover reference phases in order")
        residuals = tuple(
            float(signed[row, column])
            for row, column in zip(rows, columns, strict=True)
        )
        maximum = max(abs(value) for value in residuals)
        l2 = float(np.linalg.norm(residuals))
        return WilsonLoopPhaseSetComparisonResult1D(
            reference,
            candidate,
            tuple(int(column) for column in columns),
            residuals,
            maximum,
            l2,
            absolute_tolerance,
            maximum <= absolute_tolerance,
        )
