r"""Two-dimensional plane-wave Bloch operator construction.

This module represents a spinless scalar periodic operator in a finite reciprocal
basis. PhysKit owns the direct and reciprocal primitive lattices. This module owns the
finite Fourier inventory, ordered basis truncation, Bloch-fiber request, and represented
energy matrix until the reusable capability is migrated to PhysKit.

For direct and reciprocal primitive-basis matrices ``A`` and ``B``, the constructor
requires ``A.T @ B = 2*pi*I`` to a caller-owned absolute tolerance. In reduced
coordinates ``kappa`` and reciprocal integer index ``n``, the represented matrix is

``H[n_prime, n] = kinetic_scale * |B @ (kappa + n)|**2 * delta[n_prime, n]
                  + V[n_prime - n]``.

The finite matrix is numerical-verification infrastructure. It is not a Kohn--Sham
calculation, a material model, or scientific validation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
from projectkoios.physkit.periodic.lattice import (
    DirectLattice2D,
    ReciprocalLattice2D,
)

from ksdft2effmass.operators import ComplexMatrixQuantity, ScalarQuantity

type ReciprocalIndex2D = tuple[int, int]
type ReducedMomentum2D = tuple[float, float]


@dataclass(frozen=True, slots=True)
class PlaneWaveFourierCoefficient2D:
    r"""Represent one two-dimensional Fourier coefficient.

    Parameters
    ----------
    reciprocal_transfer
        Integer pair :math:`\mathbf m` identifying the reciprocal transfer
        :math:`B\mathbf m`.
    value
        Finite built-in complex coefficient in the energy unit declared by the owning
        :class:`PlaneWaveBlochHamiltonian2DModel`.
    """

    reciprocal_transfer: ReciprocalIndex2D
    value: complex

    def __post_init__(self) -> None:
        """Require an exact integer pair and a finite built-in complex value."""
        if (
            type(self.reciprocal_transfer) is not tuple
            or len(self.reciprocal_transfer) != 2
        ):
            raise TypeError("reciprocal_transfer must be a two-component tuple")
        if any(type(component) is not int for component in self.reciprocal_transfer):
            raise TypeError("reciprocal_transfer components must be built-in integers")
        if type(self.value) is not complex:
            raise TypeError("value must be a built-in complex")
        if not np.isfinite(self.value.real) or not np.isfinite(self.value.imag):
            raise ValueError("value must be finite")


@dataclass(frozen=True, slots=True, eq=False)
class PlaneWaveBlochHamiltonian2DModel:
    r"""Define one finite-basis spinless periodic Fourier representation.

    Parameters
    ----------
    direct_lattice
        PhysKit direct primitive lattice with column-basis matrix :math:`A`.
    reciprocal_lattice
        PhysKit reciprocal primitive lattice with column-basis matrix :math:`B`.
        Compatibility with ``direct_lattice`` is evaluated by the constructor.
    reciprocal_cutoff
        Nonnegative built-in integer :math:`M`. The ordered basis contains
        :math:`-M\leq p,q\leq M` in ``p``-outer, ``q``-inner order.
    fourier_coefficients
        Lexicographically sorted, unique Fourier inventory. Every coefficient must
        have its exact conjugate partner so the represented potential is real.
        Unlisted reciprocal transfers have coefficient zero.
    kinetic_scale
        Positive finite energy multiplying
        :math:`\lVert B(\boldsymbol\kappa+\mathbf n)\rVert^2`.
    state_space_identifier
        Nonempty identity for the represented spinless scalar state space.
    basis_identifier
        Nonempty identity for the plane-wave basis convention and ordering.
    energy_reference
        Nonempty identity for the represented operator's zero of energy.

    Notes
    -----
    ``Model`` in this established numerical type name denotes the complete input model
    for finite matrix construction. This record fixes a cutoff, finite basis, Fourier
    inventory, and represented-space metadata, so it is a representation definition
    rather than a scientific ``PeriodicModel`` parent. The constructor result owns the
    represented operator.
    """

    direct_lattice: DirectLattice2D
    reciprocal_lattice: ReciprocalLattice2D
    reciprocal_cutoff: int
    fourier_coefficients: tuple[PlaneWaveFourierCoefficient2D, ...]
    kinetic_scale: ScalarQuantity
    state_space_identifier: str
    basis_identifier: str
    energy_reference: str

    def __post_init__(self) -> None:
        """Validate the complete finite representation definition."""
        self._check_args_lattices()
        self._check_args_basis()
        self._check_args_fourier_coefficients()
        self._check_args_energy_scale()
        self._check_args_identifiers()

    def _check_args_lattices(self) -> None:
        """Require exact PhysKit direct and reciprocal lattice records."""
        if type(self.direct_lattice) is not DirectLattice2D:
            raise TypeError("direct_lattice must be DirectLattice2D")
        if type(self.reciprocal_lattice) is not ReciprocalLattice2D:
            raise TypeError("reciprocal_lattice must be ReciprocalLattice2D")

    def _check_args_basis(self) -> None:
        """Require a nonnegative built-in integer reciprocal cutoff."""
        if type(self.reciprocal_cutoff) is not int:
            raise TypeError("reciprocal_cutoff must be a built-in integer")
        if self.reciprocal_cutoff < 0:
            raise ValueError("reciprocal_cutoff must be nonnegative")

    def _check_args_fourier_coefficients(self) -> None:
        """Require a canonical Fourier inventory for a real scalar potential."""
        if type(self.fourier_coefficients) is not tuple or any(
            type(coefficient) is not PlaneWaveFourierCoefficient2D
            for coefficient in self.fourier_coefficients
        ):
            raise TypeError(
                "fourier_coefficients must be a tuple of PlaneWaveFourierCoefficient2D"
            )
        transfers = tuple(
            coefficient.reciprocal_transfer for coefficient in self.fourier_coefficients
        )
        # Canonical transfer order makes the immutable inventory deterministic and
        # rejects duplicate contributions whose summation policy would be ambiguous.
        if transfers != tuple(sorted(set(transfers))):
            raise ValueError(
                "fourier_coefficients must be sorted by unique reciprocal transfer"
            )
        coefficient_by_transfer = {
            coefficient.reciprocal_transfer: coefficient.value
            for coefficient in self.fourier_coefficients
        }
        # V[-m] = conjugate(V[m]) is the coefficient-space reality condition. Missing
        # partners are exact zero, not values to be repaired by implicit symmetrization.
        for transfer, value in coefficient_by_transfer.items():
            partner = (-transfer[0], -transfer[1])
            if coefficient_by_transfer.get(partner, 0.0 + 0.0j) != value.conjugate():
                raise ValueError(
                    "fourier_coefficients must satisfy V[-m] = conjugate(V[m])"
                )

    def _check_args_energy_scale(self) -> None:
        """Require a positive declared scale for reciprocal kinetic energy."""
        if type(self.kinetic_scale) is not ScalarQuantity:
            raise TypeError("kinetic_scale must be ScalarQuantity")
        if self.kinetic_scale.magnitude <= 0.0:
            raise ValueError("kinetic_scale must be positive")

    def _check_args_identifiers(self) -> None:
        """Require explicit represented-space and energy-zero identities."""
        for name, identifier in (
            ("state_space_identifier", self.state_space_identifier),
            ("basis_identifier", self.basis_identifier),
            ("energy_reference", self.energy_reference),
        ):
            if type(identifier) is not str:
                raise TypeError(f"{name} must be a string")
            if not identifier:
                raise ValueError(f"{name} must be nonempty")

    @property
    def reciprocal_indices(self) -> tuple[ReciprocalIndex2D, ...]:
        """Return basis indices in ``p``-outer, ``q``-inner order."""
        cutoff = self.reciprocal_cutoff
        return tuple(
            (p, q)
            for p in range(-cutoff, cutoff + 1)
            for q in range(-cutoff, cutoff + 1)
        )

    @property
    def represented_dimension(self) -> int:
        """Return the finite plane-wave basis dimension."""
        return (2 * self.reciprocal_cutoff + 1) ** 2

    @property
    def basis_ordering(self) -> Literal["p_outer_q_inner"]:
        """Return the fixed reciprocal-index ordering identifier."""
        return "p_outer_q_inner"

    @property
    def spin_convention(self) -> Literal["spinless_scalar"]:
        """Return the fixed spin convention."""
        return "spinless_scalar"

    def coefficient(self, reciprocal_transfer: ReciprocalIndex2D) -> complex:
        """Return one Fourier coefficient, or exact zero when it is unlisted."""
        if type(reciprocal_transfer) is not tuple or len(reciprocal_transfer) != 2:
            raise TypeError("reciprocal_transfer must be a two-component tuple")
        if any(type(component) is not int for component in reciprocal_transfer):
            raise TypeError("reciprocal_transfer components must be built-in integers")
        for coefficient in self.fourier_coefficients:
            if coefficient.reciprocal_transfer == reciprocal_transfer:
                return coefficient.value
        return 0.0 + 0.0j


@dataclass(frozen=True, slots=True)
class PlaneWaveBlochHamiltonian2DRequest:
    r"""Request one finite two-dimensional Bloch fiber.

    Parameters
    ----------
    model
        Complete finite Fourier model and represented-space metadata.
    reduced_momentum
        Finite built-in-float pair :math:`\boldsymbol\kappa`. Components are
        coefficients in the reciprocal primitive basis. They are not silently
        interpreted as Cartesian wave-vector components.
    duality_absolute_tolerance
        Nonnegative finite built-in float applied to the maximum component of
        :math:`A^{\mathsf T}B-2\pi I`.
    """

    model: PlaneWaveBlochHamiltonian2DModel
    reduced_momentum: ReducedMomentum2D
    duality_absolute_tolerance: float

    def __post_init__(self) -> None:
        """Validate exact model, reduced-momentum, and tolerance fields."""
        if type(self.model) is not PlaneWaveBlochHamiltonian2DModel:
            raise TypeError("model must be PlaneWaveBlochHamiltonian2DModel")
        if type(self.reduced_momentum) is not tuple or len(self.reduced_momentum) != 2:
            raise TypeError("reduced_momentum must be a two-component tuple")
        if any(type(component) is not float for component in self.reduced_momentum):
            raise TypeError("reduced_momentum components must be built-in floats")
        if any(not np.isfinite(component) for component in self.reduced_momentum):
            raise ValueError("reduced_momentum components must be finite")
        if type(self.duality_absolute_tolerance) is not float:
            raise TypeError("duality_absolute_tolerance must be a built-in float")
        if (
            not np.isfinite(self.duality_absolute_tolerance)
            or self.duality_absolute_tolerance < 0.0
        ):
            raise ValueError(
                "duality_absolute_tolerance must be finite and nonnegative"
            )


@dataclass(frozen=True, slots=True, eq=False)
class PlaneWaveBlochHamiltonian2DResult:
    """Retain one represented Bloch operator and its complete construction request.

    Parameters
    ----------
    request
        Exact request identifying geometry, basis, momentum fiber, units, energy
        reference, spin convention, Fourier model, and duality tolerance.
    maximum_duality_residual
        Maximum absolute component of ``A.T @ B - 2*pi*I``.
    represented_matrix
        Immutable complex energy matrix in the request basis order.

    Notes
    -----
    This is reusable represented-space output. It retains the complete request and
    does not inherit from a scientific model, select a retained subspace, or assign
    campaign acceptance. Model adequacy, discretization error, and later reduction
    error remain separate.
    """

    request: PlaneWaveBlochHamiltonian2DRequest
    maximum_duality_residual: float
    represented_matrix: ComplexMatrixQuantity

    def __post_init__(self) -> None:
        """Validate result correlation, residual, matrix shape, and energy unit."""
        if type(self.request) is not PlaneWaveBlochHamiltonian2DRequest:
            raise TypeError("request must be PlaneWaveBlochHamiltonian2DRequest")
        if type(self.maximum_duality_residual) is not float:
            raise TypeError("maximum_duality_residual must be a built-in float")
        if (
            not np.isfinite(self.maximum_duality_residual)
            or self.maximum_duality_residual < 0.0
        ):
            raise ValueError("maximum_duality_residual must be finite and nonnegative")
        if self.maximum_duality_residual > self.request.duality_absolute_tolerance:
            raise ValueError("maximum_duality_residual exceeds the request tolerance")
        if type(self.represented_matrix) is not ComplexMatrixQuantity:
            raise TypeError("represented_matrix must be ComplexMatrixQuantity")
        dimension = self.request.model.represented_dimension
        if self.represented_matrix.magnitude.shape != (dimension, dimension):
            raise ValueError("represented_matrix shape must match the model basis")
        if self.represented_matrix.unit != self.request.model.kinetic_scale.unit:
            raise ValueError("represented_matrix must use the model energy unit")


class PlaneWaveBlochHamiltonian2DConstructor:
    r"""Construct a finite two-dimensional plane-wave Bloch operator.

    The Action validates direct--reciprocal duality and then evaluates

    .. math::

       H_{\mathbf n'\mathbf n}(\boldsymbol\kappa)
       = E_{\mathrm K}
         \left\lVert B(\boldsymbol\kappa+\mathbf n)\right\rVert^2
         \delta_{\mathbf n'\mathbf n}
         + V_{\mathbf n'-\mathbf n}.

    No eigensolver, band selection, gauge alignment, truncation comparison, or
    scientific acceptance is performed.
    """

    __slots__ = ()

    def execute(
        self, request: PlaneWaveBlochHamiltonian2DRequest
    ) -> PlaneWaveBlochHamiltonian2DResult:
        """Construct the represented matrix in the model's declared basis order.

        Parameters
        ----------
        request
            Validated Bloch-fiber construction request.

        Returns
        -------
        PlaneWaveBlochHamiltonian2DResult
            Immutable represented matrix and direct--reciprocal residual.

        Raises
        ------
        TypeError
            If ``request`` has the wrong semantic type.
        ValueError
            If direct and reciprocal primitive bases exceed the declared duality
            tolerance.
        """
        if type(request) is not PlaneWaveBlochHamiltonian2DRequest:
            raise TypeError("request must be PlaneWaveBlochHamiltonian2DRequest")
        model = request.model
        direct_basis = model.direct_lattice.A
        reciprocal_basis = model.reciprocal_lattice.primitive_basis
        # Reduced reciprocal coordinates are meaningful only after the direct and
        # reciprocal primitive bases satisfy the declared two-pi dual convention.
        duality_residual = direct_basis.T @ reciprocal_basis - 2.0 * np.pi * np.eye(2)
        maximum_duality_residual = float(np.max(np.abs(duality_residual)))
        if maximum_duality_residual > request.duality_absolute_tolerance:
            raise ValueError(
                "direct and reciprocal lattices exceed the duality tolerance"
            )

        indices = model.reciprocal_indices
        dimension = model.represented_dimension
        matrix = np.empty((dimension, dimension), dtype=np.complex128)
        coefficient_by_transfer = {
            coefficient.reciprocal_transfer: coefficient.value
            for coefficient in model.fourier_coefficients
        }
        # In the plane-wave basis, a potential matrix element depends on the reciprocal
        # transfer n' - n. Unlisted transfers represent exact zero coefficients.
        for row, row_index in enumerate(indices):
            for column, column_index in enumerate(indices):
                transfer = (
                    row_index[0] - column_index[0],
                    row_index[1] - column_index[1],
                )
                matrix[row, column] = coefficient_by_transfer.get(transfer, 0.0 + 0.0j)

        reduced_momentum = np.asarray(request.reduced_momentum, dtype=np.float64)
        for diagonal, reciprocal_index in enumerate(indices):
            shifted_reduced = reduced_momentum + np.asarray(
                reciprocal_index, dtype=np.float64
            )
            # B stores primitive reciprocal vectors as columns, so multiplying
            # reduced coefficients by B produces the Cartesian reciprocal vector.
            shifted_cartesian = reciprocal_basis @ shifted_reduced
            kinetic_energy = model.kinetic_scale.magnitude * float(
                np.dot(shifted_cartesian, shifted_cartesian)
            )
            matrix[diagonal, diagonal] += kinetic_energy

        return PlaneWaveBlochHamiltonian2DResult(
            request=request,
            maximum_duality_residual=maximum_duality_residual,
            represented_matrix=ComplexMatrixQuantity(
                matrix,
                model.kinetic_scale.unit,
            ),
        )
