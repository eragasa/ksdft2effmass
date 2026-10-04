r"""Transport periodic2d finite-difference operators into plane-wave common space.

The comparison is defined only after the two represented operators agree on the toy
model, Bloch momentum, geometry, dimensionless energy convention, energy zero, spin
convention, and basis/grid ordering. The Action samples the declared plane waves on
the finite-difference grid, transports the grid operator by ``T.conj().T @ H_fd @ T``,
and records the operator difference without applying an acceptance threshold.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.operators import ComplexMatrixQuantity, ScalarQuantity, Unitless

from ..model.toy_models import (
    Periodic2DFiniteDifferenceHamiltonianResult,
    Periodic2DPlaneWaveHamiltonianResult,
)


@dataclass(frozen=True, slots=True)
class Periodic2DCommonSpaceComparisonRequest:
    """Request a plane-wave/finite-difference operator comparison.

    Parameters
    ----------
    plane_wave
        Plane-wave matrix and exact represented-space request.
    finite_difference
        Finite-difference matrix and exact coordinate-grid request. Its grid must
        resolve every retained plane-wave index without discrete Fourier aliasing.
    comparison_identifier
        Nonempty identity for the common-space comparison convention.
    """

    plane_wave: Periodic2DPlaneWaveHamiltonianResult
    finite_difference: Periodic2DFiniteDifferenceHamiltonianResult
    comparison_identifier: str

    def __post_init__(self) -> None:
        """Validate exact represented results and all comparison prerequisites."""
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
        plane_request = self.plane_wave.request
        finite_request = self.finite_difference.request
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
        Unitless isometric sampling map from plane-wave coefficients to grid values.
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

    Notes
    -----
    This is a threshold-free comparison result. It references two represented
    operators and retains an explicit directional transport into one common space; it
    is neither another represented operator nor an acceptance decision. The reported
    disagreement is representation/discretization evidence, not parent-model error,
    scientific validation, or uncertainty quantification.
    """

    request: Periodic2DCommonSpaceComparisonRequest
    plane_wave_to_grid: ComplexMatrixQuantity
    transported_finite_difference: ComplexMatrixQuantity
    operator_difference: ComplexMatrixQuantity
    isometry_frobenius_defect: ScalarQuantity
    operator_frobenius_error: ScalarQuantity
    operator_maximum_absolute_error: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate result correlation, shapes, units, and nonnegative diagnostics."""
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
        scalar_fields = (
            ("isometry_frobenius_defect", self.isometry_frobenius_defect),
            ("operator_frobenius_error", self.operator_frobenius_error),
            (
                "operator_maximum_absolute_error",
                self.operator_maximum_absolute_error,
            ),
        )
        for name, scalar_quantity in scalar_fields:
            if type(scalar_quantity) is not ScalarQuantity:
                raise TypeError(f"{name} must be ScalarQuantity")
            if type(scalar_quantity.unit) is not Unitless:
                raise ValueError(f"{name} must be unitless")
            if scalar_quantity.magnitude < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        expected_difference = (
            self.transported_finite_difference.magnitude
            - self.request.plane_wave.matrix
        )
        if not np.array_equal(self.operator_difference.magnitude, expected_difference):
            raise ValueError(
                "operator_difference must equal transported finite difference "
                "minus plane wave"
            )
        expected_isometry_defect = float(
            np.linalg.norm(
                self.plane_wave_to_grid.magnitude.conj().T
                @ self.plane_wave_to_grid.magnitude
                - np.eye(common_dimension, dtype=np.complex128)
            )
        )
        expected_frobenius_error = float(
            np.linalg.norm(self.operator_difference.magnitude)
        )
        expected_maximum_error = float(
            np.max(np.abs(self.operator_difference.magnitude))
        )
        if self.isometry_frobenius_defect.magnitude != expected_isometry_defect:
            raise ValueError("isometry_frobenius_defect must match plane_wave_to_grid")
        if self.operator_frobenius_error.magnitude != expected_frobenius_error:
            raise ValueError("operator_frobenius_error must match operator_difference")
        if self.operator_maximum_absolute_error.magnitude != expected_maximum_error:
            raise ValueError(
                "operator_maximum_absolute_error must match operator_difference"
            )


class Periodic2DCommonSpaceOperatorComparator:
    """Compare plane-wave and finite-difference operators in plane-wave space.

    The Action applies no threshold and assigns no pass/fail status. The returned
    diagnostics measure representation disagreement for caller-owned interpretation.
    """

    __slots__ = ()

    def execute(
        self, request: Periodic2DCommonSpaceComparisonRequest
    ) -> Periodic2DCommonSpaceComparisonResult:
        """Sample, transport, subtract, and measure the represented operators.

        Parameters
        ----------
        request
            Compatibility-checked plane-wave and finite-difference results.

        Returns
        -------
        Periodic2DCommonSpaceComparisonResult
            Immutable sampling map, transported operator, difference, and norms.

        Raises
        ------
        TypeError
            If ``request`` has the wrong semantic type.
        """
        if type(request) is not Periodic2DCommonSpaceComparisonRequest:
            raise TypeError("request must be Periodic2DCommonSpaceComparisonRequest")
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
        # ordering. The Kronecker product therefore preserves their declared order.
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
        plane_wave_to_grid = np.kron(first_sampling, second_sampling)
        transported = (
            plane_wave_to_grid.conj().T
            @ request.finite_difference.matrix
            @ plane_wave_to_grid
        )
        difference = transported - request.plane_wave.matrix
        common_dimension = request.common_dimension
        isometry_defect = float(
            np.linalg.norm(
                plane_wave_to_grid.conj().T @ plane_wave_to_grid
                - np.eye(common_dimension, dtype=np.complex128)
            )
        )
        frobenius_error = float(np.linalg.norm(difference))
        maximum_error = float(np.max(np.abs(difference)))
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
