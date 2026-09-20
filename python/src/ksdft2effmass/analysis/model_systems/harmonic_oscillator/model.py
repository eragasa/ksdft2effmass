"""Immutable contracts for finite harmonic-oscillator comparisons.

The modeled subject is the one-dimensional quantum harmonic oscillator. The
mathematical reference operator is the real-line oscillator Hamiltonian, while the
numerical representation is a centered second-order finite-difference matrix on the
interior of a finite Dirichlet interval. A comparison request declares one finite
representation and one retained analytic number-state space. A comparison result
stores the explicit injection, both operators in retained coordinates, their signed
difference, and numerical diagnostics.

All scalar inputs are built-in Python ``float`` or ``int`` values as documented.
Arrays are canonicalized to C-contiguous ``numpy.float64`` views backed by immutable
bytes. The records establish represented software contracts only; they do not assert
continuum convergence, model adequacy, semiconductor relevance, scientific
validation, or uncertainty quantification.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.operators import (
    FiniteDifferenceHamiltonian1D,
    LadderOperator1D,
    SampledPotential1D,
    SchrodingerKineticEnergy1D,
    SecondOrderCentralDifferenceLaplacian1D,
)
from ksdft2effmass.operators.quantities import (
    MODEL_SYSTEM_UNIT_CONVERTER,
    MatrixQuantity,
    PhysicalUnit,
    ScalarQuantity,
    SparseMatrixQuantity,
    Unitless,
    VectorQuantity,
)

from ..intervals import DirichletInterval


@dataclass(frozen=True, slots=True)
class HarmonicOscillatorParameters:
    r"""Define positive unit-aware harmonic-oscillator parameters.

    A parameter set is either fully physical or fully nondimensional. Physical values
    must have action, mass, and inverse-time dimensions. Nondimensional values must all
    use the first-class :class:`~ksdft2effmass.operators.Unitless` unit.

    Parameters
    ----------
    hbar
        Positive reduced Planck constant with action dimensions, or Unitless under an
        explicit nondimensionalization.
    mass
        Positive particle mass, or Unitless under that nondimensionalization.
    omega
        Positive angular frequency, or Unitless under that nondimensionalization.
    """

    hbar: ScalarQuantity
    mass: ScalarQuantity
    omega: ScalarQuantity

    def __post_init__(self) -> None:
        values = (("hbar", self.hbar), ("mass", self.mass), ("omega", self.omega))
        for name, value in values:
            if not isinstance(value, ScalarQuantity):
                raise TypeError(f"{name} must be ScalarQuantity")
            if value.magnitude <= 0.0:
                raise ValueError(f"{name} must be positive")
        unitless = tuple(isinstance(value.unit, Unitless) for _, value in values)
        if any(unitless) and not all(unitless):
            raise ValueError(
                "harmonic-oscillator parameters must not mix "
                "unitless and physical units"
            )
        if not all(unitless):
            converter = MODEL_SYSTEM_UNIT_CONVERTER
            expectations = (
                (self.hbar.unit, PhysicalUnit("joule * second"), "hbar"),
                (self.mass.unit, PhysicalUnit("kilogram"), "mass"),
                (self.omega.unit, PhysicalUnit("1 / second"), "omega"),
            )
            for actual, expected, name in expectations:
                if not converter.compatible(actual, expected):
                    raise ValueError(f"{name} has incompatible physical dimensions")

    @property
    def is_nondimensional(self) -> bool:
        """Return whether all parameters use the first-class Unitless unit."""
        return isinstance(self.hbar.unit, Unitless)

    @property
    def oscillator_length(self) -> ScalarQuantity:
        r"""Return :math:`\sqrt{\hbar/(m\omega)}` with an explicit unit."""
        if self.is_nondimensional:
            value = np.sqrt(
                self.hbar.magnitude / (self.mass.magnitude * self.omega.magnitude)
            )
            return ScalarQuantity(float(value), Unitless())
        converter = MODEL_SYSTEM_UNIT_CONVERTER
        hbar = converter.convert_scalar(
            self.hbar, PhysicalUnit("joule * second")
        ).magnitude
        mass = converter.convert_scalar(self.mass, PhysicalUnit("kilogram")).magnitude
        omega = converter.convert_scalar(
            self.omega, PhysicalUnit("1 / second")
        ).magnitude
        return ScalarQuantity(
            float(np.sqrt(hbar / (mass * omega))), PhysicalUnit("meter")
        )


class HarmonicOscillatorNondimensionalizer:
    """Adapt explicit normalized scalar inputs to first-class Unitless quantities."""

    __slots__ = ()

    def execute(
        self, hbar: float, mass: float, omega: float
    ) -> HarmonicOscillatorParameters:
        """Return a fully Unitless parameter set without implying physical units."""
        return HarmonicOscillatorParameters(
            hbar=ScalarQuantity(hbar, Unitless()),
            mass=ScalarQuantity(mass, Unitless()),
            omega=ScalarQuantity(omega, Unitless()),
        )


@dataclass(frozen=True, slots=True)
class HarmonicOscillatorAnalytical:
    """Represent the exact real-line harmonic-oscillator solution.

    Parameters
    ----------
    parameters
        Positive physical oscillator parameters shared by every representation.

    Attributes
    ----------
    parameters
        Exact physical parameter record.
    """

    parameters: HarmonicOscillatorParameters

    def __post_init__(self) -> None:
        if not isinstance(self.parameters, HarmonicOscillatorParameters):
            raise TypeError("parameters must be HarmonicOscillatorParameters")

    def number_state_energies(self, retained_dimension: int) -> VectorQuantity:
        """Return exact unit-aware energies for states ``|0>`` through ``|K-1>``."""
        if type(retained_dimension) is not int:
            raise TypeError("retained_dimension must be a built-in int")
        if retained_dimension <= 0:
            raise ValueError("retained_dimension must be positive")
        parameters = self.parameters
        if parameters.is_nondimensional:
            scale = parameters.hbar.magnitude * parameters.omega.magnitude
            unit: PhysicalUnit | Unitless = Unitless()
        else:
            converter = MODEL_SYSTEM_UNIT_CONVERTER
            hbar = converter.convert_scalar(
                parameters.hbar, PhysicalUnit("joule * second")
            ).magnitude
            omega = converter.convert_scalar(
                parameters.omega, PhysicalUnit("1 / second")
            ).magnitude
            scale = hbar * omega
            unit = PhysicalUnit("joule")
        values = scale * (np.arange(retained_dimension, dtype=np.float64) + 0.5)
        return VectorQuantity(values, unit)

    def number_state_wavefunctions(
        self,
        dimensionless_coordinates: VectorQuantity,
        retained_dimension: int,
    ) -> MatrixQuantity:
        """Evaluate normalized Hermite states at Unitless coordinates ``x / ell``."""
        if not isinstance(dimensionless_coordinates, VectorQuantity):
            raise TypeError("dimensionless_coordinates must be VectorQuantity")
        if not isinstance(dimensionless_coordinates.unit, Unitless):
            raise ValueError("dimensionless_coordinates must use Unitless")
        coordinates = dimensionless_coordinates.magnitude
        if type(retained_dimension) is not int:
            raise TypeError("retained_dimension must be a built-in int")
        if retained_dimension <= 0:
            raise ValueError("retained_dimension must be positive")
        states = np.empty((coordinates.size, retained_dimension), dtype=np.float64)
        oscillator_length = self.parameters.oscillator_length
        states[:, 0] = (
            np.pi ** (-0.25)
            * np.exp(-0.5 * np.square(coordinates))
            / np.sqrt(oscillator_length.magnitude)
        )
        if retained_dimension > 1:
            states[:, 1] = np.sqrt(2.0) * coordinates * states[:, 0]
        for degree in range(1, retained_dimension - 1):
            states[:, degree + 1] = (
                np.sqrt(2.0 / (degree + 1.0)) * coordinates * states[:, degree]
                - np.sqrt(degree / (degree + 1.0)) * states[:, degree - 1]
            )
        unit: PhysicalUnit | Unitless
        if self.parameters.is_nondimensional:
            unit = Unitless()
        else:
            unit = PhysicalUnit("meter ** -0.5")
        return MatrixQuantity(states, unit)


@dataclass(frozen=True, slots=True)
class HarmonicOscillatorFiniteDifference:
    """Represent a harmonic oscillator on a reusable Dirichlet interval.

    Parameters
    ----------
    analytical
        Exact oscillator model supplying physical parameters and wavefunction units.
    interval
        Symmetric interval with homogeneous Dirichlet boundary data.
    """

    analytical: HarmonicOscillatorAnalytical
    interval: DirichletInterval

    def __post_init__(self) -> None:
        if not isinstance(self.analytical, HarmonicOscillatorAnalytical):
            raise TypeError("analytical must be HarmonicOscillatorAnalytical")
        if not isinstance(self.interval, DirichletInterval):
            raise TypeError("interval must be DirichletInterval")
        if not self.interval.boundary_condition.is_homogeneous:
            raise ValueError(
                "finite-matrix realization requires homogeneous Dirichlet data"
            )
        expected_length = self.canonical_length_unit
        if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
            self.interval.grid.coordinate_unit, expected_length
        ):
            raise ValueError("grid has incompatible coordinate dimensions")
        expected_field: PhysicalUnit | Unitless
        if self.analytical.parameters.is_nondimensional:
            expected_field = Unitless()
        else:
            expected_field = PhysicalUnit("meter ** -0.5")
        if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
            self.interval.boundary_condition.value.unit, expected_field
        ):
            raise ValueError("boundary value has incompatible wavefunction dimensions")
        lower = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
            self.interval.grid.lower_bound, expected_length
        ).magnitude
        upper = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
            self.interval.grid.upper_bound, expected_length
        ).magnitude
        if not np.isclose(lower, -upper, rtol=0.0, atol=1.0e-12):
            raise ValueError(
                "harmonic-oscillator interval must be symmetric about zero"
            )

    @property
    def canonical_length_unit(self) -> PhysicalUnit | Unitless:
        """Return Unitless for normalized models and meters for physical models."""
        if self.analytical.parameters.is_nondimensional:
            return Unitless()
        return PhysicalUnit("meter")

    @property
    def box_half_width(self) -> ScalarQuantity:
        """Return the symmetric interval half-width in the canonical length unit."""
        upper = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
            self.interval.grid.upper_bound, self.canonical_length_unit
        )
        return ScalarQuantity(upper.magnitude, self.canonical_length_unit)

    @property
    def requested_grid_spacing(self) -> ScalarQuantity:
        """Return the requested grid spacing in the canonical length unit."""
        return MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
            self.interval.grid.requested_spacing, self.canonical_length_unit
        )

    @property
    def interior_points(self) -> int:
        """Return the number of ordered interior grid coordinates."""
        return self.interval.interior_points

    @property
    def grid_spacing(self) -> ScalarQuantity:
        """Return the realized uniform spacing in the canonical length unit."""
        return MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
            self.interval.grid.spacing, self.canonical_length_unit
        )

    def grid_coordinates(self) -> VectorQuantity:
        """Return interior grid coordinates in the canonical length unit."""
        return MODEL_SYSTEM_UNIT_CONVERTER.convert_vector(
            self.interval.grid.interior_coordinates(), self.canonical_length_unit
        )

    def hamiltonian(self) -> SparseMatrixQuantity:
        """Return the sparse kinetic-plus-harmonic-potential Hamiltonian."""
        parameters = self.analytical.parameters
        laplacian = SecondOrderCentralDifferenceLaplacian1D(self.interval)
        kinetic = SchrodingerKineticEnergy1D(
            laplacian=laplacian,
            hbar=parameters.hbar,
            mass=parameters.mass,
        )
        coordinates = self.grid_coordinates().magnitude
        if parameters.is_nondimensional:
            mass = parameters.mass.magnitude
            omega = parameters.omega.magnitude
            energy_unit: PhysicalUnit | Unitless = Unitless()
        else:
            mass = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
                parameters.mass, PhysicalUnit("kilogram")
            ).magnitude
            omega = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
                parameters.omega, PhysicalUnit("1 / second")
            ).magnitude
            energy_unit = PhysicalUnit("joule")
        potential = SampledPotential1D(
            grid=self.interval.grid,
            values=VectorQuantity(
                0.5 * mass * omega**2 * np.square(coordinates), energy_unit
            ),
        )
        return FiniteDifferenceHamiltonian1D(kinetic, potential).matrix()


@dataclass(frozen=True, slots=True)
class HarmonicOscillatorLadderOperators:
    """Apply harmonic-oscillator energy scaling to a generic ladder basis.

    Parameters
    ----------
    analytical
        Exact oscillator model supplying the energy scale.
    ladder_operator
        Generic retained one-dimensional occupation-number basis.
    """

    analytical: HarmonicOscillatorAnalytical
    ladder_operator: LadderOperator1D

    def __post_init__(self) -> None:
        if not isinstance(self.analytical, HarmonicOscillatorAnalytical):
            raise TypeError("analytical must be HarmonicOscillatorAnalytical")
        if not isinstance(self.ladder_operator, LadderOperator1D):
            raise TypeError("ladder_operator must be LadderOperator1D")

    @property
    def retained_dimension(self) -> int:
        """Return the generic ladder basis dimension."""
        return self.ladder_operator.retained_dimension

    def annihilation(self) -> SparseMatrixQuantity:
        """Return the composed sparse Unitless annihilation operator."""
        return self.ladder_operator.annihilation()

    def creation(self) -> SparseMatrixQuantity:
        """Return the composed sparse Unitless creation operator."""
        return self.ladder_operator.creation()

    def number(self) -> SparseMatrixQuantity:
        """Return the composed exact sparse Unitless number operator."""
        return self.ladder_operator.number()

    def hamiltonian(self) -> SparseMatrixQuantity:
        """Return the sparse retained ``hbar*omega*(N + I/2)`` matrix."""
        energies = self.analytical.number_state_energies(self.retained_dimension)
        matrix = sparse.diags(
            energies.magnitude,
            offsets=0,
            shape=(self.retained_dimension, self.retained_dimension),
            format="csr",
            dtype=np.float64,
        )
        return SparseMatrixQuantity.from_csr(matrix, energies.unit)

    def commutator(self) -> SparseMatrixQuantity:
        """Return the composed finite sparse Unitless ladder commutator."""
        return self.ladder_operator.commutator()


@dataclass(frozen=True, slots=True)
class HarmonicOscillatorComparisonRequest:
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

    analytical: HarmonicOscillatorAnalytical
    finite_difference: HarmonicOscillatorFiniteDifference
    ladder_operators: HarmonicOscillatorLadderOperators

    def __post_init__(self) -> None:
        if not isinstance(self.analytical, HarmonicOscillatorAnalytical):
            raise TypeError("analytical must be HarmonicOscillatorAnalytical")
        if not isinstance(self.finite_difference, HarmonicOscillatorFiniteDifference):
            raise TypeError(
                "finite_difference must be HarmonicOscillatorFiniteDifference"
            )
        if not isinstance(self.ladder_operators, HarmonicOscillatorLadderOperators):
            raise TypeError(
                "ladder_operators must be HarmonicOscillatorLadderOperators"
            )
        if self.finite_difference.analytical != self.analytical:
            raise ValueError("finite_difference must share the analytical model")
        if self.ladder_operators.analytical != self.analytical:
            raise ValueError("ladder_operators must share the analytical model")
        if self.retained_dimension > self.interior_points:
            raise ValueError("retained dimension exceeds the spatial dimension")

    @property
    def parameters(self) -> HarmonicOscillatorParameters:
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
class HarmonicOscillatorComparisonResult:
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
    grid_spacing
        Positive realized finite-difference spacing with its explicit length unit.
    interior_points
        Number of ordered interior Dirichlet-grid coordinates.
    grid_coordinates
        Immutable vector quantity with shape ``(interior_points,)`` and the request
        length unit.
    injection
        Immutable Unitless matrix quantity with shape
        ``(interior_points, retained_dimension)``.
    gram_matrix
        Immutable Unitless sampled-state Gram matrix with shape ``(K, K)``.
    gram_inverse_square_root
        Immutable symmetric inverse square root of ``gram_matrix``.
    pulled_back_hamiltonian
        Immutable finite-grid Hamiltonian represented in retained coordinates.
    reference_hamiltonian
        Immutable exact retained number-state Hamiltonian.
    difference
        Immutable ``pulled_back_hamiltonian - reference_hamiltonian`` matrix.
    gram_deviation
        Nonnegative Frobenius norm of ``gram_matrix - I``.
    gram_condition_number
        Positive spectral condition number of the Gram matrix.
    injection_isometry_error
        Nonnegative Frobenius norm of ``injection.T @ injection - I``.
    absolute_discrepancy
        Nonnegative Frobenius norm of ``difference`` in the implied energy unit.
    relative_discrepancy
        Nonnegative absolute discrepancy divided by the reference Frobenius norm.
    diagonal_discrepancy
        Nonnegative Frobenius norm of the diagonal part of ``difference``.
    off_diagonal_discrepancy
        Nonnegative Frobenius norm of the off-diagonal part of ``difference``.

    Notes
    -----
    Array quantities own immutable byte-backed binary64 magnitudes and explicit units.
    Equality is not defined for this array-bearing record; consumers compare declared
    fields under explicit exact or numerical policy.
    """

    request: HarmonicOscillatorComparisonRequest
    grid_spacing: ScalarQuantity
    interior_points: int
    grid_coordinates: VectorQuantity
    injection: MatrixQuantity
    gram_matrix: MatrixQuantity
    gram_inverse_square_root: MatrixQuantity
    pulled_back_hamiltonian: MatrixQuantity
    reference_hamiltonian: MatrixQuantity
    difference: MatrixQuantity
    gram_deviation: ScalarQuantity
    gram_condition_number: ScalarQuantity
    injection_isometry_error: ScalarQuantity
    absolute_discrepancy: ScalarQuantity
    relative_discrepancy: ScalarQuantity
    diagonal_discrepancy: ScalarQuantity
    off_diagonal_discrepancy: ScalarQuantity

    def __post_init__(self) -> None:
        if not isinstance(self.request, HarmonicOscillatorComparisonRequest):
            raise TypeError("request must be HarmonicOscillatorComparisonRequest")
        if not isinstance(self.grid_spacing, ScalarQuantity):
            raise TypeError("grid_spacing must be ScalarQuantity")
        if self.grid_spacing.magnitude <= 0.0:
            raise ValueError("grid_spacing must be positive")
        if type(self.interior_points) is not int:
            raise TypeError("interior_points must be a built-in int")
        if self.interior_points <= 0:
            raise ValueError("interior_points must be positive")

        retained = self.request.retained_dimension
        arrays = (
            ("grid_coordinates", self.grid_coordinates, (self.interior_points,)),
            ("injection", self.injection, (self.interior_points, retained)),
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
            if not isinstance(array_quantity, VectorQuantity | MatrixQuantity):
                raise TypeError(f"{name} must be a typed array quantity")
            if array_quantity.magnitude.shape != shape:
                raise ValueError(f"{name} must have shape {shape}")

        unitless_arrays = (
            self.injection,
            self.gram_matrix,
            self.gram_inverse_square_root,
        )
        if any(not isinstance(item.unit, Unitless) for item in unitless_arrays):
            raise ValueError("map and Gram arrays must use Unitless")
        length_unit = self.request.finite_difference.canonical_length_unit
        if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
            self.grid_spacing.unit, length_unit
        ) or not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
            self.grid_coordinates.unit, length_unit
        ):
            raise ValueError("grid quantities must use compatible length units")
        energy_unit = self.reference_hamiltonian.unit
        energy_arrays = (
            self.pulled_back_hamiltonian,
            self.reference_hamiltonian,
            self.difference,
        )
        if any(
            not MODEL_SYSTEM_UNIT_CONVERTER.compatible(item.unit, energy_unit)
            for item in energy_arrays
        ):
            raise ValueError("Hamiltonian arrays must use compatible energy units")

        metrics = (
            ("gram_deviation", self.gram_deviation, True),
            ("gram_condition_number", self.gram_condition_number, True),
            ("injection_isometry_error", self.injection_isometry_error, True),
            ("absolute_discrepancy", self.absolute_discrepancy, False),
            ("relative_discrepancy", self.relative_discrepancy, True),
            ("diagonal_discrepancy", self.diagonal_discrepancy, False),
            ("off_diagonal_discrepancy", self.off_diagonal_discrepancy, False),
        )
        for name, metric_quantity, must_be_unitless in metrics:
            if not isinstance(metric_quantity, ScalarQuantity):
                raise TypeError(f"{name} must be ScalarQuantity")
            if metric_quantity.magnitude < 0.0:
                raise ValueError(f"{name} must be nonnegative")
            if must_be_unitless and not isinstance(metric_quantity.unit, Unitless):
                raise ValueError(f"{name} must use Unitless")
            if not must_be_unitless and not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
                metric_quantity.unit, energy_unit
            ):
                raise ValueError(f"{name} must use an energy unit")
        if self.gram_condition_number.magnitude <= 0.0:
            raise ValueError("gram_condition_number must be positive")
