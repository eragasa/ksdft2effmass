"""Requests and results for aligned QHO1D finite-model comparisons."""

from __future__ import annotations

from dataclasses import dataclass

from projectkoios.physkit.units import (
    MatrixQuantity,
    ModelSystemUnitConverter,
    ScalarQuantity,
    VectorQuantity,
)

from .analytical import Qho1dAnalytical
from .case_sections import (
    Qho1dHamiltonianComparisonResult,
    Qho1dSampledStateAlignmentResult,
    Qho1dSpatialRepresentationResult,
)
from .finite_difference import Qho1dFiniteDifference
from .ladder_operators import Qho1dLadderOperators
from .parameters import Qho1dParameters


@dataclass(frozen=True, slots=True)
class Qho1dComparisonRequest:
    """Bind analytical, finite-difference, and ladder-operator oscillator models.

    Parameters
    ----------
    analytical
        Exact real-line analytical model.
    finite_difference
        Harmonic finite-difference model using the same analytical model and a
        reusable Dirichlet interval.
    ladder_operators
        Retained ladder-operator model using the same analytical model.

    Raises
    ------
    TypeError
        If a field has the wrong model type.
    ValueError
        If the three models do not share one analytical model or the retained
        dimension exceeds the interval-grid dimension.
    """

    analytical: Qho1dAnalytical
    finite_difference: Qho1dFiniteDifference
    ladder_operators: Qho1dLadderOperators

    def __post_init__(self) -> None:
        if not isinstance(self.analytical, Qho1dAnalytical):
            raise TypeError("analytical must be Qho1dAnalytical")
        if not isinstance(self.finite_difference, Qho1dFiniteDifference):
            raise TypeError("finite_difference must be Qho1dFiniteDifference")
        if not isinstance(self.ladder_operators, Qho1dLadderOperators):
            raise TypeError("ladder_operators must be Qho1dLadderOperators")
        if self.finite_difference.analytical != self.analytical:
            raise ValueError("finite_difference must share the analytical model")
        if self.ladder_operators.analytical != self.analytical:
            raise ValueError("ladder_operators must share the analytical model")
        if self.retained_dimension > self.interior_points:
            raise ValueError("retained dimension exceeds the spatial dimension")

    @property
    def parameters(self) -> Qho1dParameters:
        """Return the shared physical parameter record."""
        return self.analytical.parameters

    @property
    def box_half_width(self) -> ScalarQuantity:
        """Return the unit-aware Dirichlet interval half-width."""
        return self.finite_difference.box_half_width

    @property
    def requested_grid_spacing(self) -> ScalarQuantity:
        """Return the unit-aware requested Dirichlet grid spacing."""
        return self.finite_difference.requested_grid_spacing

    @property
    def retained_dimension(self) -> int:
        """Return the ladder-operator retained dimension."""
        return self.ladder_operators.retained_dimension

    @property
    def interior_points(self) -> int:
        """Return the Dirichlet model's interior-grid dimension."""
        return self.finite_difference.interior_points


@dataclass(frozen=True, slots=True, eq=False)
class Qho1dComparisonResult:
    """Represent one aligned finite-grid and number-state comparison.

    The injection :math:`J` maps retained number-state coordinates into ordered
    finite-grid coordinates. ``pulled_back_hamiltonian`` is :math:`J^T H_h J`,
    ``reference_hamiltonian`` is the exact diagonal retained oscillator matrix, and
    ``difference`` is their signed finite-matrix difference. Every matrix is real
    ``numpy.float64`` and uses row-major ordering.

    Parameters
    ----------
    request
        Exact comparison request that produced this result.
    representation
        Finite spatial representation and its authored controls.
    alignment
        Sampled-state coordinate alignment and map diagnostics.
    hamiltonian_comparison
        Hamiltonians and discrepancy values in common retained coordinates.

    Notes
    -----
    Array quantities own immutable byte-backed binary64 magnitudes and explicit units.
    Equality is not defined for this array-bearing record; consumers compare declared
    fields under explicit exact or numerical policy.
    """

    request: Qho1dComparisonRequest
    representation: Qho1dSpatialRepresentationResult
    alignment: Qho1dSampledStateAlignmentResult
    hamiltonian_comparison: Qho1dHamiltonianComparisonResult

    def __post_init__(self) -> None:
        if not isinstance(self.request, Qho1dComparisonRequest):
            raise TypeError("request must be Qho1dComparisonRequest")
        section_types = (
            ("representation", Qho1dSpatialRepresentationResult),
            ("alignment", Qho1dSampledStateAlignmentResult),
            ("hamiltonian_comparison", Qho1dHamiltonianComparisonResult),
        )
        for name, expected_type in section_types:
            if not isinstance(getattr(self, name), expected_type):
                raise TypeError(f"{name} must be {expected_type.__name__}")
        represented_box = ModelSystemUnitConverter.convert_scalar(
            self.representation.box_half_width, self.request.box_half_width.unit
        )
        if represented_box.magnitude != self.request.box_half_width.magnitude:
            raise ValueError("representation box half-width differs from request")
        represented_spacing = ModelSystemUnitConverter.convert_scalar(
            self.representation.requested_grid_spacing,
            self.request.requested_grid_spacing.unit,
        )
        if (
            represented_spacing.magnitude
            != self.request.requested_grid_spacing.magnitude
        ):
            raise ValueError("representation requested spacing differs from request")
        if self.representation.retained_dimension != self.request.retained_dimension:
            raise ValueError("representation retained dimension differs from request")
        if self.representation.interior_points != self.request.interior_points:
            raise ValueError("representation interior dimension differs from request")

        retained = self.representation.retained_dimension
        points = self.representation.interior_points
        arrays = (
            ("injection", self.injection, (points, retained)),
            ("gram_matrix", self.gram_matrix, (retained, retained)),
            (
                "gram_inverse_square_root",
                self.gram_inverse_square_root,
                (retained, retained),
            ),
            (
                "pulled_back_hamiltonian",
                self.pulled_back_hamiltonian,
                (retained, retained),
            ),
            (
                "reference_hamiltonian",
                self.reference_hamiltonian,
                (retained, retained),
            ),
            ("difference", self.difference, (retained, retained)),
        )
        for name, array_quantity, shape in arrays:
            if array_quantity.magnitude.shape != shape:
                raise ValueError(f"{name} must have shape {shape}")

    @property
    def grid_spacing(self) -> ScalarQuantity:
        """Return the realized finite-difference spacing."""
        return self.representation.grid_spacing

    @property
    def interior_points(self) -> int:
        """Return the represented finite-grid dimension."""
        return self.representation.interior_points

    @property
    def grid_coordinates(self) -> VectorQuantity:
        """Return the ordered interior grid coordinates."""
        return self.representation.grid_coordinates

    @property
    def injection(self) -> MatrixQuantity:
        """Return the retained-to-spatial coordinate injection."""
        return self.alignment.injection

    @property
    def gram_matrix(self) -> MatrixQuantity:
        """Return the sampled-state Gram matrix."""
        return self.alignment.gram_matrix

    @property
    def gram_inverse_square_root(self) -> MatrixQuantity:
        """Return the symmetric Gram inverse square root."""
        return self.alignment.gram_inverse_square_root

    @property
    def gram_deviation(self) -> ScalarQuantity:
        """Return the sampled-state Gram deviation."""
        return self.alignment.gram_deviation

    @property
    def gram_condition_number(self) -> ScalarQuantity:
        """Return the sampled-state Gram condition number."""
        return self.alignment.gram_condition_number

    @property
    def injection_isometry_error(self) -> ScalarQuantity:
        """Return the injection-isometry discrepancy."""
        return self.alignment.injection_isometry_error

    @property
    def pulled_back_hamiltonian(self) -> MatrixQuantity:
        """Return the finite Hamiltonian in retained coordinates."""
        return self.hamiltonian_comparison.pulled_back_hamiltonian

    @property
    def reference_hamiltonian(self) -> MatrixQuantity:
        """Return the exact retained number-state Hamiltonian."""
        return self.hamiltonian_comparison.reference_hamiltonian

    @property
    def difference(self) -> MatrixQuantity:
        """Return pullback minus reference in common coordinates."""
        return self.hamiltonian_comparison.difference

    @property
    def absolute_discrepancy(self) -> ScalarQuantity:
        """Return the absolute Hamiltonian discrepancy."""
        return self.hamiltonian_comparison.absolute_discrepancy

    @property
    def relative_discrepancy(self) -> ScalarQuantity:
        """Return the reference-normalized Hamiltonian discrepancy."""
        return self.hamiltonian_comparison.relative_discrepancy

    @property
    def diagonal_discrepancy(self) -> ScalarQuantity:
        """Return the diagonal discrepancy component."""
        return self.hamiltonian_comparison.diagonal_discrepancy

    @property
    def off_diagonal_discrepancy(self) -> ScalarQuantity:
        """Return the off-diagonal discrepancy component."""
        return self.hamiltonian_comparison.off_diagonal_discrepancy
