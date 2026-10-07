r"""Transport periodic2d finite-difference operators into plane-wave common space.

The comparison is defined only after the two represented operators agree on the toy
model, Bloch momentum, geometry, dimensionless energy convention, energy zero, spin
convention, and basis/grid ordering. The Action samples the declared plane waves on
the finite-difference grid, transports the grid operator by ``T.conj().T @ H_fd @ T``,
and records the signed operator difference without applying an acceptance threshold.

The shared parent is the dimensionless spinless scalar toy Hamiltonian

.. math::

   H=-\partial_x^2-\partial_y^2
     +\lambda_x\cos x+\lambda_y\cos y
     +\lambda_{xy}\cos x\cos y

on the period-:math:`2\pi` square cell. At one reduced Bloch momentum, the plane-wave
matrix acts on the cutoff space spanned by
:math:`\exp(i[(\kappa_x+p)x+(\kappa_y+q)y])`; the grid matrix acts on Euclidean
samples with matching twisted seams. In exact basis-column-distinct arithmetic,
``T.conj().T @ T = I``. When ``N > 2*M+1``, ``T`` is a proper rectangular semiunitary
embedding with ``T @ T.conj().T != I``, and
``T.conj().T @ H_fd @ T`` is a proper-subspace compression. At the allowed boundary
``N = 2*M+1``, ``T`` is square unitary and the same expression is a full-space unitary
similarity transform.

The immutable Result validates the transport identity, signed subtraction, and every
retained diagnostic from its own stored values. It does not reconstruct the sampling
map from the request, rerun the comparison Action, or prove that the Action produced a
manually constructed Result. These boundaries keep intrinsic result algebra distinct
from request-to-value derivation and from scientific acceptance. The comparison can
expose finite-difference dispersion, cutoff, sampling/aliasing, compression, and
roundoff effects but does not uniquely separate them or establish continuum or material
adequacy.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from ksdft2effmass.operators import ComplexMatrixQuantity, ScalarQuantity, Unitless

from ..model.toy_models import (
    Periodic2DFiniteDifferenceHamiltonianResult,
    Periodic2DPlaneWaveHamiltonianResult,
)

type ComplexMatrix = npt.NDArray[np.complex128]


@dataclass(frozen=True, slots=True)
class Periodic2DCommonSpaceComparisonRequest:
    """Request a plane-wave/finite-difference operator comparison.

    Parameters
    ----------
    plane_wave
        Plane-wave matrix and exact represented-space request.
    finite_difference
        Finite-difference matrix and exact coordinate-grid request. Its grid must
        distinguish every retained plane-wave index modulo the grid. This
        basis-column condition does not exclude every possible potential-transfer
        alias.
    comparison_identifier
        Nonempty identity for the common-space comparison convention.
    """

    plane_wave: Periodic2DPlaneWaveHamiltonianResult
    finite_difference: Periodic2DFiniteDifferenceHamiltonianResult
    comparison_identifier: str

    def __post_init__(self) -> None:
        """Validate represented-result types, identity, and compatibility.

        Raises
        ------
        TypeError
            If either represented result or the comparison identity has the wrong
            semantic type.
        ValueError
            If the identity is empty, the represented operators do not share the exact
            cosine parent and Bloch momentum, or the coordinate grid aliases retained
            reciprocal indices.
        """
        self._check_args_types_and_identity()
        self._check_args_represented_compatibility()

    def _check_args_types_and_identity(self) -> None:
        """Require exact represented-result classes and a nonempty string identity."""
        if type(self.plane_wave) is not Periodic2DPlaneWaveHamiltonianResult:
            raise TypeError("plane_wave must be Periodic2DPlaneWaveHamiltonianResult")
        if (
            type(self.finite_difference)
            is not Periodic2DFiniteDifferenceHamiltonianResult
        ):
            raise TypeError(
                "finite_difference must be Periodic2DFiniteDifferenceHamiltonianResult"
            )
        if type(self.comparison_identifier) is not str:
            raise TypeError("comparison_identifier must be a string")
        if not self.comparison_identifier:
            raise ValueError("comparison_identifier must be nonempty")

    def _check_args_represented_compatibility(self) -> None:
        """Require one parent, Bloch fiber, and basis-column-distinct sampling."""
        plane_request = self.plane_wave.request
        finite_request = self.finite_difference.request
        # Exact adapter classes fix the square 2*pi geometry, dimensionless energy
        # scale and zero, scalar spin convention, and both basis orderings. Equality of
        # the configured parent and momentum then closes the remaining compatibility
        # conditions without inferring identity from matrix sizes or spectra.
        if plane_request.model != finite_request.model:
            raise ValueError("represented operators must use the same toy model")
        if (
            plane_request.reduced_momentum_x != finite_request.reduced_momentum_x
            or plane_request.reduced_momentum_y != finite_request.reduced_momentum_y
        ):
            raise ValueError("represented operators must use the same Bloch momentum")
        plane_wave_side = 2 * plane_request.cutoff + 1
        if plane_wave_side > finite_request.points_per_direction:
            raise ValueError(
                "finite-difference grid must resolve every plane-wave basis index"
            )

    @property
    def common_dimension(self) -> int:
        """Return the plane-wave common-space dimension."""
        return self.plane_wave.request.represented_dimension


@dataclass(frozen=True, slots=True, eq=False)
class Periodic2DCommonSpaceComparisonResult:
    """Retain transported operators and threshold-free comparison diagnostics.

    Parameters
    ----------
    request
        Exact represented operators and comparison identity.
    plane_wave_to_grid
        Unitless normalized sampling map from plane-wave coefficients to grid values.
        Its finite binary64 isometry defect is retained separately.
    transported_finite_difference
        Finite-difference operator represented in the plane-wave common space.
    operator_difference
        ``transported_finite_difference - plane_wave`` in that common space.
    isometry_frobenius_defect
        Frobenius norm of ``T.conj().T @ T - I``.
    operator_frobenius_error
        Frobenius norm of ``operator_difference``.
    operator_maximum_absolute_error
        Maximum absolute entry of ``operator_difference``.

    Raises
    ------
    TypeError
        If the request, any matrix quantity, or any scalar diagnostic has the wrong
        semantic type.
    ValueError
        If a quantity has the wrong unit or shape, the transported operator does not
        equal ``T.conj().T @ H_fd @ T``, the signed difference is inconsistent, or a
        diagnostic does not equal the norm of its retained matrix.
    OverflowError
        If intrinsic transport, subtraction, or norm evaluation is not representable
        as finite binary64/complex128 data.
    MemoryError
        If dense intrinsic transport validation cannot allocate its matrix-product
        workspace.

    Notes
    -----
    This is a threshold-free comparison result. It references two represented
    operators and retains an explicit directional transport into one common space; it
    is neither another represented operator nor an acceptance decision. The reported
    disagreement is representation/discretization evidence, not parent-model error,
    scientific validation, or uncertainty quantification.

    Construction validates algebra derivable from the retained map, represented
    inputs, matrices, and diagnostics. It deliberately does not reconstruct the
    request-dependent sampling map or establish that the comparator Action ran. A
    manually constructed valid Result therefore proves only intrinsic structural and
    algebraic consistency. Enforcing the retained transport equation requires one
    additional dense congruence evaluation during Result construction; this explicit
    integrity cost does not regenerate the sampling map or replay the complete Action.
    """

    request: Periodic2DCommonSpaceComparisonRequest
    plane_wave_to_grid: ComplexMatrixQuantity
    transported_finite_difference: ComplexMatrixQuantity
    operator_difference: ComplexMatrixQuantity
    isometry_frobenius_defect: ScalarQuantity
    operator_frobenius_error: ScalarQuantity
    operator_maximum_absolute_error: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate types, units, shapes, retained algebra, and diagnostics."""
        self._check_args_types_units_and_shapes()
        # Result construction checks only algebra available from retained values. The
        # comparator Action remains the owner of request-to-sampling-map derivation.
        self._check_args_intrinsic_relations()

    def _check_args_types_units_and_shapes(self) -> None:
        """Require exact quantity classes, unitless values, and directional shapes."""
        if type(self.request) is not Periodic2DCommonSpaceComparisonRequest:
            raise TypeError("request must be Periodic2DCommonSpaceComparisonRequest")
        matrix_fields = (
            ("plane_wave_to_grid", self.plane_wave_to_grid),
            ("transported_finite_difference", self.transported_finite_difference),
            ("operator_difference", self.operator_difference),
        )
        for name, matrix_quantity in matrix_fields:
            if type(matrix_quantity) is not ComplexMatrixQuantity:
                raise TypeError(f"{name} must be ComplexMatrixQuantity")
            if type(matrix_quantity.unit) is not Unitless:
                raise ValueError(f"{name} must be unitless")
        common_dimension = self.request.common_dimension
        grid_dimension = self.request.finite_difference.request.represented_dimension
        if self.plane_wave_to_grid.magnitude.shape != (
            grid_dimension,
            common_dimension,
        ):
            raise ValueError(
                "plane_wave_to_grid shape must map common space into grid space"
            )
        for name, common_matrix in (
            (
                "transported_finite_difference",
                self.transported_finite_difference,
            ),
            ("operator_difference", self.operator_difference),
        ):
            if common_matrix.magnitude.shape != (common_dimension, common_dimension):
                raise ValueError(f"{name} shape must match the common space")
        for name, scalar_quantity in (
            ("isometry_frobenius_defect", self.isometry_frobenius_defect),
            ("operator_frobenius_error", self.operator_frobenius_error),
            (
                "operator_maximum_absolute_error",
                self.operator_maximum_absolute_error,
            ),
        ):
            if type(scalar_quantity) is not ScalarQuantity:
                raise TypeError(f"{name} must be ScalarQuantity")
            if type(scalar_quantity.unit) is not Unitless:
                raise ValueError(f"{name} must be unitless")
            if scalar_quantity.magnitude < 0.0:
                raise ValueError(f"{name} must be nonnegative")

    def _check_args_intrinsic_relations(self) -> None:
        """Correlate transport, signed subtraction, and threshold-free diagnostics."""
        sampling = self.plane_wave_to_grid.magnitude
        finite_difference = self.request.finite_difference.matrix
        with np.errstate(over="ignore", invalid="ignore"):
            expected_transport = sampling.conj().T @ finite_difference @ sampling
        if not self._matrix_is_finite(expected_transport):
            raise OverflowError("common-space transport is outside complex128 range")
        if not np.array_equal(
            self.transported_finite_difference.magnitude,
            expected_transport,
        ):
            raise ValueError(
                "transported_finite_difference must equal "
                "plane_wave_to_grid.conj().T @ finite_difference @ "
                "plane_wave_to_grid"
            )

        # Subtraction is meaningful only after the finite-difference matrix has been
        # transported into the ordered plane-wave common space.
        with np.errstate(over="ignore", invalid="ignore"):
            expected_difference = expected_transport - self.request.plane_wave.matrix
        if not self._matrix_is_finite(expected_difference):
            raise OverflowError("common-space operator difference is outside range")
        if not np.array_equal(self.operator_difference.magnitude, expected_difference):
            raise ValueError(
                "operator_difference must equal transported finite difference "
                "minus plane wave"
            )

        common_dimension = self.request.common_dimension
        expected_isometry_defect = float(
            np.linalg.norm(
                sampling.conj().T @ sampling
                - np.eye(common_dimension, dtype=np.complex128)
            )
        )
        expected_frobenius_error = float(np.linalg.norm(expected_difference))
        expected_maximum_error = float(np.max(np.abs(expected_difference)))
        if not all(
            np.isfinite(value)
            for value in (
                expected_isometry_defect,
                expected_frobenius_error,
                expected_maximum_error,
            )
        ):
            raise OverflowError("common-space diagnostic is outside binary64 range")
        if self.isometry_frobenius_defect.magnitude != expected_isometry_defect:
            raise ValueError("isometry_frobenius_defect must match plane_wave_to_grid")
        if self.operator_frobenius_error.magnitude != expected_frobenius_error:
            raise ValueError("operator_frobenius_error must match operator_difference")
        if self.operator_maximum_absolute_error.magnitude != expected_maximum_error:
            raise ValueError(
                "operator_maximum_absolute_error must match operator_difference"
            )

    @staticmethod
    def _matrix_is_finite(matrix: ComplexMatrix) -> bool:
        """Return whether every complex128 component is representable and finite.

        Parameters
        ----------
        matrix
            Two-dimensional complex array produced by intrinsic Result algebra.

        Returns
        -------
        bool
            ``True`` only when every real and imaginary component is finite.
        """
        return bool(
            np.all(np.isfinite(matrix.real)) and np.all(np.isfinite(matrix.imag))
        )


class Periodic2DCommonSpaceOperatorComparator:
    """Compare two finite representations in the plane-wave common space.

    The source coordinate-grid space has dimension ``N**2`` in
    ``x_outer_y_inner`` order. The target/common plane-wave space has dimension
    ``(2*M+1)**2`` in ``p_outer_q_inner`` order. The Action evaluates the Bloch
    plane waves on the grid, producing a map ``T`` from plane-wave coefficients to
    Euclidean grid samples, and compresses the grid operator as
    ``T.conj().T @ H_fd @ T`` before subtraction.

    Notes
    -----
    When ``N > 2*M+1``, the map is a proper rectangular semiunitary embedding and the
    operation is a proper-subspace compression. At ``N = 2*M+1``, the map is square
    unitary and the operation is a full-space unitary similarity. The Action applies no
    threshold and assigns no pass/fail status. Its diagnostics measure one finite
    representation disagreement for caller-owned interpretation; they do not establish
    continuum convergence, parent-model adequacy, scientific validation, uncertainty
    quantification, or acceptance.
    """

    __slots__ = ()

    def execute(
        self, request: Periodic2DCommonSpaceComparisonRequest
    ) -> Periodic2DCommonSpaceComparisonResult:
        """Sample, transport, subtract, and measure the represented operators.

        Parameters
        ----------
        request
            Compatibility-checked plane-wave and finite-difference results. Both
            matrices are dimensionless energy representations on the same cosine
            parent and Bloch fiber but in different ordered finite bases.

        Returns
        -------
        Periodic2DCommonSpaceComparisonResult
            Immutable grid-sampling map of shape ``(N**2, (2*M+1)**2)``, transported
            finite-difference operator, signed plane-wave-space difference, and
            threshold-free diagnostics.

        Raises
        ------
        TypeError
            If ``request`` has the wrong semantic type.
        OverflowError
            If transport, subtraction, or a diagnostic cannot be represented as
            finite complex128/binary64 values.
        MemoryError
            If dense sampling-map or matrix-product allocation fails. The map contains
            ``N**2 * (2*M+1)**2`` complex values and no hidden size cap is applied.
            Intrinsic Result validation repeats the congruence product to reject a
            forged transported matrix.

        Notes
        -----
        The Action derives the request-dependent sampling map and comparison values.
        The Result independently enforces intrinsic algebra among retained values; it
        does not apply a convergence or scientific-acceptance threshold.
        """
        if type(request) is not Periodic2DCommonSpaceComparisonRequest:
            raise TypeError("request must be Periodic2DCommonSpaceComparisonRequest")
        plane_wave_to_grid = self._plane_wave_to_grid_sampling_map(request)
        with np.errstate(over="ignore", invalid="ignore"):
            transported = (
                plane_wave_to_grid.conj().T
                @ request.finite_difference.matrix
                @ plane_wave_to_grid
            )
        if not (
            np.all(np.isfinite(transported.real))
            and np.all(np.isfinite(transported.imag))
        ):
            raise OverflowError("common-space transport is outside complex128 range")
        with np.errstate(over="ignore", invalid="ignore"):
            difference = transported - request.plane_wave.matrix
        if not (
            np.all(np.isfinite(difference.real))
            and np.all(np.isfinite(difference.imag))
        ):
            raise OverflowError("common-space operator difference is outside range")

        common_dimension = request.common_dimension
        isometry_defect = float(
            np.linalg.norm(
                plane_wave_to_grid.conj().T @ plane_wave_to_grid
                - np.eye(common_dimension, dtype=np.complex128)
            )
        )
        frobenius_error = float(np.linalg.norm(difference))
        maximum_error = float(np.max(np.abs(difference)))
        if not all(
            np.isfinite(value)
            for value in (isometry_defect, frobenius_error, maximum_error)
        ):
            raise OverflowError("common-space diagnostic is outside binary64 range")
        unit = Unitless()
        return Periodic2DCommonSpaceComparisonResult(
            request=request,
            plane_wave_to_grid=ComplexMatrixQuantity(plane_wave_to_grid, unit),
            transported_finite_difference=ComplexMatrixQuantity(transported, unit),
            operator_difference=ComplexMatrixQuantity(difference, unit),
            isometry_frobenius_defect=ScalarQuantity(isometry_defect, unit),
            operator_frobenius_error=ScalarQuantity(frobenius_error, unit),
            operator_maximum_absolute_error=ScalarQuantity(maximum_error, unit),
        )

    @staticmethod
    def _plane_wave_to_grid_sampling_map(
        request: Periodic2DCommonSpaceComparisonRequest,
    ) -> ComplexMatrix:
        """Construct the normalized plane-wave-to-grid sampling embedding.

        Parameters
        ----------
        request
            Validated common-space request fixing period, Bloch momentum, reciprocal
            cutoff, grid extent, and both flattened basis orderings.

        Returns
        -------
        ComplexMatrix
            Complex128 array of shape ``(N**2, (2*M+1)**2)``. Rows are grid sites in
            ``x_outer_y_inner`` order; columns are plane waves in
            ``p_outer_q_inner`` order.

        Notes
        -----
        Each one-dimensional factor carries ``1/sqrt(N)`` normalization. Their
        Kronecker product is therefore semiunitary in exact arithmetic when retained
        reciprocal indices are distinct modulo ``N``. This method constructs the
        request-dependent map; Result validation deliberately does not call it.
        """
        plane_request = request.plane_wave.request
        finite_request = request.finite_difference.request
        points = finite_request.points_per_direction
        period = finite_request.period
        coordinates = np.arange(points, dtype=np.float64) * period / float(points)
        reciprocal_indices = np.arange(
            -plane_request.cutoff,
            plane_request.cutoff + 1,
            dtype=np.float64,
        )
        # Grid and reciprocal bases both use first-index-outer, second-index-inner
        # order. Their Kronecker product therefore maps (p, q) columns to (x, y)
        # rows without an implicit transpose or permutation.
        first_sampling = np.exp(
            1j
            * np.outer(
                coordinates,
                plane_request.reduced_momentum_x + reciprocal_indices,
            )
        ) / np.sqrt(float(points))
        second_sampling = np.exp(
            1j
            * np.outer(
                coordinates,
                plane_request.reduced_momentum_y + reciprocal_indices,
            )
        ) / np.sqrt(float(points))
        return np.kron(first_sampling, second_sampling)
