"""Dimensionless two-dimensional cosine-potential models and representations."""

from dataclasses import dataclass, field
from typing import ClassVar, Literal

import numpy as np
import numpy.typing as npt
from projectkoios.physkit.periodic.lattice import (
    DirectLattice2D,
    ReciprocalLattice2D,
)
from projectkoios.physkit.units import (
    ScalarQuantity,
    Unitless,
)

from ksdft2effmass.periodic.models import PeriodicModelRole
from ksdft2effmass.periodic.operators.basis import PlaneWaveBasisCoordinate
from ksdft2effmass.periodic.periodic2d.operators.basis import Periodic2DBasisIdentity

from .base import Periodic2DModel
from .plane_waves import (
    Periodic2DPlaneWaveBlochHamiltonianConstructor,
    Periodic2DPlaneWaveBlochHamiltonianModel,
    Periodic2DPlaneWaveBlochHamiltonianRequest,
    Periodic2DPlaneWaveFourierCoefficient,
)

type ComplexMatrix = npt.NDArray[np.complex128]


@dataclass(frozen=True, slots=True)
class Periodic2DCosinePotentialModel(Periodic2DModel):
    """Represent a spinless dimensionless periodic cosine potential.

    The represented potential is
    ``lambda_x*cos(x) + lambda_y*cos(y) + lambda_xy*cos(x)*cos(y)`` on a
    square cell of period ``2*pi``. Energies use the reciprocal kinetic scale.
    ``role`` explicitly records the model's evidentiary use; the cosine family does not
    infer control, material-reference, or reduced-model status.
    """

    MODEL_FAMILY_IDENTITY: ClassVar[str] = (
        "ksdft2effmass.periodic2d-cosine-potential-model.v1"
    )

    lambda_x: float
    lambda_y: float
    lambda_xy: float
    role: PeriodicModelRole = field(kw_only=True)

    @property
    def model_id(self) -> str:
        """Return the exact parameterized cosine-potential model identity."""
        return (
            f"{self.MODEL_FAMILY_IDENTITY}:"
            f"role-{self.model_role.to_wire()}:"
            f"lambda-x-{self.lambda_x.hex()}:"
            f"lambda-y-{self.lambda_y.hex()}:"
            f"lambda-xy-{self.lambda_xy.hex()}"
        )

    @property
    def model_role(self) -> PeriodicModelRole:
        """Return the explicitly supplied evidentiary role."""
        return self.role

    def __post_init__(self) -> None:
        """Require an explicit role and exact finite coupling coefficients."""
        if type(self.role) is not PeriodicModelRole:
            raise TypeError("role must be PeriodicModelRole")
        for name, value in (
            ("lambda_x", self.lambda_x),
            ("lambda_y", self.lambda_y),
            ("lambda_xy", self.lambda_xy),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a float")
            if not np.isfinite(value):
                raise ValueError(f"{name} must be finite")

    @property
    def direct_lattice(self) -> DirectLattice2D:
        """Return the dimensionless square direct lattice ``A = 2*pi*I``."""
        period = 2.0 * np.pi
        return DirectLattice2D(
            a1=np.array((period, 0.0), dtype=np.float64),
            a2=np.array((0.0, period), dtype=np.float64),
        )

    @property
    def reciprocal_lattice(self) -> ReciprocalLattice2D:
        """Return the two-pi-dual reciprocal lattice ``B = I``."""
        return ReciprocalLattice2D.from_direct_lattice(self.direct_lattice)


@dataclass(frozen=True, slots=True)
class Periodic2DPlaneWaveBasis:
    """Define one square finite reciprocal basis in deterministic pair order."""

    cutoff: int

    def __post_init__(self) -> None:
        """Require a nonnegative built-in integer cutoff."""
        if type(self.cutoff) is not int:
            raise TypeError("cutoff must be a built-in integer")
        if self.cutoff < 0:
            raise ValueError("cutoff must be nonnegative")

    @property
    def reciprocal_indices(self) -> tuple[tuple[int, int], ...]:
        """Return reciprocal pairs in ``p``-outer, ``q``-inner order."""
        return tuple(
            (p, q)
            for p in range(-self.cutoff, self.cutoff + 1)
            for q in range(-self.cutoff, self.cutoff + 1)
        )

    @property
    def represented_dimension(self) -> int:
        """Return the number of reciprocal basis vectors."""
        return (2 * self.cutoff + 1) ** 2

    @property
    def basis_identity(self) -> Periodic2DBasisIdentity:
        """Return the exact ordered scalar plane-wave coordinate identity.

        Returns
        -------
        Periodic2DBasisIdentity
            Reciprocal-index coordinates in the same ``p``-outer, ``q``-inner order
            used by the control Hamiltonian representation.
        """
        return Periodic2DBasisIdentity(
            display_identifier="periodic2d-spinless-scalar-plane-wave-basis",
            coordinates=tuple(
                PlaneWaveBasisCoordinate(reciprocal_index=index)
                for index in self.reciprocal_indices
            ),
        )

    @property
    def ordering(self) -> Literal["p_outer_q_inner"]:
        """Return the reciprocal-index ordering identifier."""
        return "p_outer_q_inner"


@dataclass(frozen=True, slots=True)
class Periodic2DUniformCellGrid:
    """Define one odd uniform grid on a dimensionless period-``2*pi`` cell."""

    points_per_direction: int

    def __post_init__(self) -> None:
        """Require an odd built-in integer grid size of at least five."""
        if type(self.points_per_direction) is not int:
            raise TypeError("points_per_direction must be a built-in integer")
        if self.points_per_direction < 5 or self.points_per_direction % 2 == 0:
            raise ValueError("points_per_direction must be odd and at least five")

    @property
    def period(self) -> float:
        """Return the dimensionless square-cell period."""
        return 2.0 * np.pi

    @property
    def spacing(self) -> float:
        """Return the uniform coordinate spacing."""
        return self.period / self.points_per_direction

    @property
    def represented_dimension(self) -> int:
        """Return the number of coordinate-basis sites."""
        return self.points_per_direction**2

    @property
    def site_indices(self) -> tuple[tuple[int, int], ...]:
        """Return grid indices in ``x``-outer, ``y``-inner order."""
        return tuple(
            (x_index, y_index)
            for x_index in range(self.points_per_direction)
            for y_index in range(self.points_per_direction)
        )

    @property
    def ordering(self) -> Literal["x_outer_y_inner"]:
        """Return the flattened coordinate ordering identifier."""
        return "x_outer_y_inner"


@dataclass(frozen=True, slots=True)
class Periodic2DPlaneWaveHamiltonianRequest:
    r"""Request a finite plane-wave representation of the control Hamiltonian.

    Reduced momentum components are built-in floats giving the coefficients
    :math:`\boldsymbol\kappa` in the PhysKit reciprocal primitive basis ``B`` of the
    period-``2*pi`` cell. ``cutoff`` is a built-in integer. Each kinetic diagonal is
    :math:`\lVert B(\boldsymbol\kappa+\mathbf n)\rVert^2` in the reciprocal
    kinetic-energy scale, with the model's fixed zero of energy.
    ``duality_absolute_tolerance`` is the nonnegative maximum-component tolerance for
    :math:`A^{\mathsf T}B-2\pi I`; its default covers binary64 reconstruction of the
    fixed square lattice and is not a scientific acceptance threshold.
    """

    model: Periodic2DCosinePotentialModel
    reduced_momentum_x: float
    reduced_momentum_y: float
    cutoff: int
    duality_absolute_tolerance: float = 4.0e-15

    def __post_init__(self) -> None:
        """Validate the model, momentum coordinates, and symmetric cutoff."""
        if type(self.model) is not Periodic2DCosinePotentialModel:
            raise TypeError("model must be Periodic2DCosinePotentialModel")
        for name, value in (
            ("reduced_momentum_x", self.reduced_momentum_x),
            ("reduced_momentum_y", self.reduced_momentum_y),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not np.isfinite(value):
                raise ValueError(f"{name} must be finite")
        Periodic2DPlaneWaveBasis(self.cutoff)
        if type(self.duality_absolute_tolerance) is not float:
            raise TypeError("duality_absolute_tolerance must be a built-in float")
        if (
            not np.isfinite(self.duality_absolute_tolerance)
            or self.duality_absolute_tolerance < 0.0
        ):
            raise ValueError(
                "duality_absolute_tolerance must be finite and nonnegative"
            )

    @property
    def basis(self) -> Periodic2DPlaneWaveBasis:
        """Return the immutable reciprocal-basis identity."""
        return Periodic2DPlaneWaveBasis(self.cutoff)

    @property
    def reciprocal_indices(self) -> tuple[tuple[int, int], ...]:
        """Return reciprocal pairs in the represented basis order."""
        return self.basis.reciprocal_indices

    @property
    def basis_identity(self) -> Periodic2DBasisIdentity:
        """Return the exact ordered basis identity of the represented matrix."""
        return self.basis.basis_identity

    @property
    def represented_dimension(self) -> int:
        """Return the finite plane-wave basis dimension."""
        return self.basis.represented_dimension

    @property
    def basis_ordering(self) -> Literal["p_outer_q_inner"]:
        """Return the declared reciprocal-index ordering identifier."""
        return self.basis.ordering


@dataclass(frozen=True, slots=True)
class Periodic2DFiniteDifferenceHamiltonianRequest:
    """Request a centered finite-difference representation on the square cell.

    Reduced momentum components are built-in floats in the dimensionless reciprocal
    coordinates of the period-``2*pi`` cell. ``points_per_direction`` is a built-in
    integer. The represented matrix uses the model's reciprocal kinetic-energy scale
    and fixed zero of energy.
    """

    model: Periodic2DCosinePotentialModel
    reduced_momentum_x: float
    reduced_momentum_y: float
    points_per_direction: int

    def __post_init__(self) -> None:
        """Validate the model, momentum coordinates, and odd grid size."""
        if type(self.model) is not Periodic2DCosinePotentialModel:
            raise TypeError("model must be Periodic2DCosinePotentialModel")
        for name, value in (
            ("reduced_momentum_x", self.reduced_momentum_x),
            ("reduced_momentum_y", self.reduced_momentum_y),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not np.isfinite(value):
                raise ValueError(f"{name} must be finite")
        Periodic2DUniformCellGrid(self.points_per_direction)

    @property
    def grid(self) -> Periodic2DUniformCellGrid:
        """Return the immutable coordinate-grid identity."""
        return Periodic2DUniformCellGrid(self.points_per_direction)

    @property
    def period(self) -> float:
        """Return the dimensionless square-cell period."""
        return self.grid.period

    @property
    def spacing(self) -> float:
        """Return the uniform real-space grid spacing."""
        return self.grid.spacing

    @property
    def represented_dimension(self) -> int:
        """Return the finite coordinate-basis dimension."""
        return self.grid.represented_dimension

    @property
    def site_ordering(self) -> Literal["x_outer_y_inner"]:
        """Return the declared flattened coordinate ordering identifier."""
        return self.grid.ordering

    @property
    def boundary_phase_x(self) -> complex:
        """Return the phase multiplying the last-to-first positive-x seam."""
        return complex(np.exp(1j * self.reduced_momentum_x * self.period))

    @property
    def boundary_phase_y(self) -> complex:
        """Return the phase multiplying the last-to-first positive-y seam."""
        return complex(np.exp(1j * self.reduced_momentum_y * self.period))


@dataclass(frozen=True, slots=True)
class Periodic2DHamiltonianResult:
    """Retain one operationally immutable finite represented Hamiltonian."""

    matrix: ComplexMatrix

    def __post_init__(self) -> None:
        """Copy one finite square Hermitian matrix into immutable storage."""
        matrix = np.asarray(self.matrix, dtype=np.complex128)
        if (
            matrix.ndim != 2
            or matrix.shape[0] == 0
            or matrix.shape[0] != matrix.shape[1]
        ):
            raise ValueError("matrix must be nonempty and square")
        if not np.all(np.isfinite(matrix)):
            raise ValueError("matrix must contain only finite values")
        if not np.array_equal(matrix, matrix.conj().T):
            raise ValueError("matrix must be exactly Hermitian")
        immutable = np.frombuffer(
            matrix.tobytes(order="C"), dtype=np.complex128
        ).reshape(matrix.shape)
        object.__setattr__(self, "matrix", immutable)


@dataclass(frozen=True, slots=True)
class Periodic2DPlaneWaveHamiltonianResult(Periodic2DHamiltonianResult):
    """Retain a plane-wave matrix with its represented-space and duality evidence."""

    request: Periodic2DPlaneWaveHamiltonianRequest
    maximum_duality_residual: float

    def __post_init__(self) -> None:
        """Validate the matrix and its plane-wave request identity."""
        Periodic2DHamiltonianResult.__post_init__(self)
        if type(self.request) is not Periodic2DPlaneWaveHamiltonianRequest:
            raise TypeError("request must be Periodic2DPlaneWaveHamiltonianRequest")
        if self.matrix.shape != (
            self.request.represented_dimension,
            self.request.represented_dimension,
        ):
            raise ValueError("matrix shape must match the plane-wave basis")
        if type(self.maximum_duality_residual) is not float:
            raise TypeError("maximum_duality_residual must be a built-in float")
        if (
            not np.isfinite(self.maximum_duality_residual)
            or self.maximum_duality_residual < 0.0
        ):
            raise ValueError("maximum_duality_residual must be finite and nonnegative")
        if self.maximum_duality_residual > self.request.duality_absolute_tolerance:
            raise ValueError("maximum_duality_residual exceeds the request tolerance")

    @property
    def basis_identity(self) -> Periodic2DBasisIdentity:
        """Return the request-owned basis identity of the represented matrix."""
        return self.request.basis_identity


@dataclass(frozen=True, slots=True)
class Periodic2DFiniteDifferenceHamiltonianResult(Periodic2DHamiltonianResult):
    """Retain a coordinate matrix with its declared grid and fiber identity."""

    request: Periodic2DFiniteDifferenceHamiltonianRequest

    def __post_init__(self) -> None:
        """Validate the matrix and its finite-difference request identity."""
        Periodic2DHamiltonianResult.__post_init__(self)
        if type(self.request) is not Periodic2DFiniteDifferenceHamiltonianRequest:
            raise TypeError(
                "request must be Periodic2DFiniteDifferenceHamiltonianRequest"
            )
        if self.matrix.shape != (
            self.request.represented_dimension,
            self.request.represented_dimension,
        ):
            raise ValueError("matrix shape must match the coordinate grid")


@dataclass(frozen=True, slots=True)
class Periodic2DPlaneWaveHamiltonian:
    r"""Construct one finite plane-wave representation from an exact request.

    The operation represents the spinless dimensionless control Hamiltonian

    .. math::

       H(\boldsymbol\kappa)
       = \lVert \boldsymbol\kappa - i\nabla \rVert^2
       + \lambda_x\cos(x)
       + \lambda_y\cos(y)
       + \lambda_{xy}\cos(x)\cos(y)

    in the request's square reciprocal basis. The basis uses ``p``-outer,
    ``q``-inner ordering and includes every integer pair in the closed square
    ``[-cutoff, cutoff]``. Construction introduces no additional basis truncation,
    energy shift, unit conversion, or scientific acceptance decision.

    Parameters
    ----------
    request : Periodic2DPlaneWaveHamiltonianRequest
        Exact control model, reduced reciprocal momentum, symmetric basis cutoff,
        and direct--reciprocal duality tolerance defining the representation.

    Attributes
    ----------
    request : Periodic2DPlaneWaveHamiltonianRequest
        The exact immutable request retained by identity and copied into the result.

    Notes
    -----
    This operation constructs a finite matrix representation of a scientific model.
    It is not itself a
    :class:`~ksdft2effmass.periodic.periodic2d.models.Periodic2DModel` and does not
    assign scientific-model identity. Reusable plane-wave assembly remains
    delegated to the Project Koios representation owner.
    """

    request: Periodic2DPlaneWaveHamiltonianRequest

    def __post_init__(self) -> None:
        """Validate the exact request boundary.

        Raises
        ------
        TypeError
            If ``request`` is not exactly a
            :class:`Periodic2DPlaneWaveHamiltonianRequest`. Subclasses and coercible
            request-like values are not admitted.
        """
        # Exact type admission prevents an unreviewed request subtype from changing
        # basis, momentum, tolerance, or energy-reference semantics implicitly.
        if type(self.request) is not Periodic2DPlaneWaveHamiltonianRequest:
            raise TypeError("request must be Periodic2DPlaneWaveHamiltonianRequest")

    def result(self) -> Periodic2DPlaneWaveHamiltonianResult:
        """Construct and return the immutable represented Hamiltonian.

        Returns
        -------
        Periodic2DPlaneWaveHamiltonianResult
            The Hermitian matrix in the declared reciprocal-basis order, correlated
            with the exact request and the provider-computed maximum lattice-duality
            residual.

        Notes
        -----
        The cosine potential has support only at the eight explicitly listed
        reciprocal displacements. The provider constructs the kinetic diagonal,
        applies those Fourier couplings, and verifies the direct--reciprocal lattice
        relation against the request tolerance.
        """
        # Keep the exact object identity so the result can correlate every represented
        # matrix with the admitted model, momentum, basis, and numerical tolerance.
        request = self.request
        model = request.model

        # cos(x) contributes lambda_x / 2 at the two x-directed unit shifts;
        # cos(y) contributes lambda_y / 2 at the two y-directed unit shifts.
        # The product cos(x)cos(y) contributes lambda_xy / 4 at all four corners.
        coefficients = (
            Periodic2DPlaneWaveFourierCoefficient(
                (-1, -1), complex(model.lambda_xy / 4.0)
            ),
            Periodic2DPlaneWaveFourierCoefficient(
                (-1, 0), complex(model.lambda_x / 2.0)
            ),
            Periodic2DPlaneWaveFourierCoefficient(
                (-1, 1), complex(model.lambda_xy / 4.0)
            ),
            Periodic2DPlaneWaveFourierCoefficient(
                (0, -1), complex(model.lambda_y / 2.0)
            ),
            Periodic2DPlaneWaveFourierCoefficient(
                (0, 1), complex(model.lambda_y / 2.0)
            ),
            Periodic2DPlaneWaveFourierCoefficient(
                (1, -1), complex(model.lambda_xy / 4.0)
            ),
            Periodic2DPlaneWaveFourierCoefficient(
                (1, 0), complex(model.lambda_x / 2.0)
            ),
            Periodic2DPlaneWaveFourierCoefficient(
                (1, 1), complex(model.lambda_xy / 4.0)
            ),
        )

        # Adapt the KSD control model into the reusable provider representation. This
        # provider object is composition data, not a superclass of the KSD model.
        operator_model = Periodic2DPlaneWaveBlochHamiltonianModel(
            direct_lattice=model.direct_lattice,
            reciprocal_lattice=model.reciprocal_lattice,
            reciprocal_cutoff=request.cutoff,
            fourier_coefficients=coefficients,
            # The control problem is dimensionless and uses |k + G|^2 directly.
            kinetic_scale=ScalarQuantity(1.0, Unitless()),
            # Stable identifiers state the represented space, basis order, and zero.
            state_space_identifier="periodic2d.cosine.spinless_scalar",
            basis_identifier="periodic2d.cosine.p_outer_q_inner",
            energy_reference="periodic2d.cosine.model_zero",
        )

        # Let the representation owner construct the finite operator and retain its
        # independently computed direct--reciprocal duality evidence.
        represented = Periodic2DPlaneWaveBlochHamiltonianConstructor().execute(
            Periodic2DPlaneWaveBlochHamiltonianRequest(
                model=operator_model,
                reduced_momentum=(
                    request.reduced_momentum_x,
                    request.reduced_momentum_y,
                ),
                duality_absolute_tolerance=request.duality_absolute_tolerance,
            )
        )

        # Project only the represented matrix magnitude and duality evidence into the
        # KSD-owned correlated result; provider model identity is not reinterpreted.
        return Periodic2DPlaneWaveHamiltonianResult(
            matrix=represented.represented_matrix.magnitude,
            request=request,
            maximum_duality_residual=represented.maximum_duality_residual,
        )


@dataclass(frozen=True, slots=True)
class Periodic2DFiniteDifferenceHamiltonian:
    r"""Construct one centered finite-difference representation from a request.

    The operation discretizes the same dimensionless periodic control Hamiltonian as
    :class:`Periodic2DPlaneWaveHamiltonian` on the request's odd uniform square grid.
    The kinetic term uses the second-order centered stencil for ``-d^2/dx^2`` and
    ``-d^2/dy^2``. Reduced reciprocal momentum enters only through the conjugate Bloch
    phases on each periodic seam.

    Parameters
    ----------
    request : Periodic2DFiniteDifferenceHamiltonianRequest
        Exact control model, reduced reciprocal momentum, odd grid size, and resulting
        periodic seam phases defining the coordinate representation.

    Attributes
    ----------
    request : Periodic2DFiniteDifferenceHamiltonianRequest
        The exact immutable request retained by identity and copied into the result.

    Notes
    -----
    Flattened coordinates use ``x``-outer, ``y``-inner order. The operation constructs
    a finite matrix representation and therefore does not inherit the nominal
    scientific-model hierarchy or make a continuum-convergence claim.
    """

    request: Periodic2DFiniteDifferenceHamiltonianRequest

    def __post_init__(self) -> None:
        """Validate the exact request boundary.

        Raises
        ------
        TypeError
            If ``request`` is not exactly a
            :class:`Periodic2DFiniteDifferenceHamiltonianRequest`. Subclasses and
            coercible request-like values are not admitted.
        """
        # Exact admission protects coordinate ordering, grid parity, seam-phase, and
        # energy-reference semantics from implicit request-subtype changes.
        if type(self.request) is not Periodic2DFiniteDifferenceHamiltonianRequest:
            raise TypeError(
                "request must be Periodic2DFiniteDifferenceHamiltonianRequest"
            )

    def result(self) -> Periodic2DFiniteDifferenceHamiltonianResult:
        """Construct and return the immutable coordinate-space Hamiltonian.

        Returns
        -------
        Periodic2DFiniteDifferenceHamiltonianResult
            The exactly Hermitian centered-difference matrix correlated with the exact
            finite-difference request.

        Notes
        -----
        The kinetic operator is assembled as the Kronecker sum ``K_x (x) I_y +
        I_x (x) K_y``. The potential is sampled pointwise on the half-open periodic
        grid and inserted as a diagonal matrix in the declared flattened order.
        """
        # Preserve exact request identity across construction and result correlation.
        request = self.request
        points = request.points_per_direction
        period = request.period

        # Each one-dimensional block owns its momentum-dependent periodic seam. Their
        # Kronecker sum preserves x-outer, y-inner flattened coordinate ordering.
        kinetic_x = self._one_dimensional(request.reduced_momentum_x)
        kinetic_y = self._one_dimensional(request.reduced_momentum_y)
        identity = np.eye(points, dtype=np.complex128)
        matrix = np.kron(kinetic_x, identity) + np.kron(identity, kinetic_y)

        # Sample the half-open cell [0, 2*pi) without duplicating its periodic endpoint.
        coordinate = np.arange(points, dtype=np.float64) * period / points
        cosine = np.cos(coordinate)
        model = request.model

        # Broadcast the two separable cosine terms and their mixed product onto the
        # square grid. C-order raveling matches x-outer, y-inner site enumeration.
        potential = (
            model.lambda_x * cosine[:, None]
            + model.lambda_y * cosine[None, :]
            + model.lambda_xy * cosine[:, None] * cosine[None, :]
        )
        matrix += np.diag(potential.ravel(order="C"))

        # The result owner copies the matrix into immutable storage and rechecks exact
        # Hermiticity and compatibility with the request's represented dimension.
        return Periodic2DFiniteDifferenceHamiltonianResult(
            matrix=matrix,
            request=request,
        )

    def _one_dimensional(self, momentum: float) -> ComplexMatrix:
        r"""Construct one momentum-twisted centered kinetic block.

        Parameters
        ----------
        momentum : float
            Built-in reduced reciprocal momentum for one periodic coordinate. The
            enclosing request has already established finiteness.

        Returns
        -------
        ComplexMatrix
            The ``points_per_direction`` square matrix representing ``-d^2/dx^2``
            with the request's spacing and conjugate Bloch seam phases.

        Notes
        -----
        The interior stencil has diagonal ``2/h^2`` and nearest-neighbor entries
        ``-1/h^2``. The two corner entries close the periodic quotient with phases
        ``exp(-i*k*period)`` and ``exp(+i*k*period)``.
        """
        points = self.request.points_per_direction
        period = self.request.period
        spacing = period / points

        # Populate the diagonal and the two interior nearest-neighbor bands for the
        # centered representation of the negative second derivative.
        matrix = np.diag(np.full(points, 2.0 / spacing**2)).astype(np.complex128)
        off_diagonal = -1.0 / spacing**2
        matrix += np.diag(np.full(points - 1, off_diagonal), 1)
        matrix += np.diag(np.full(points - 1, off_diagonal), -1)

        # Close the first/last-site seam with conjugate phases so the represented
        # kinetic operator remains exactly Hermitian for real reduced momentum.
        matrix[0, -1] = off_diagonal * np.exp(-1j * momentum * period)
        matrix[-1, 0] = off_diagonal * np.exp(1j * momentum * period)
        return matrix
