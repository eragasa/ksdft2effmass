"""Nearest-neighbor orthogonal silicon :math:`sp^3s^*` model.

This module owns one explicitly frozen effective-model class for spinless diamond
silicon. It does not fit parameters, identify a Wannier-to-atomic-orbital alignment,
or establish physical adequacy. The real-space operator uses the cell-periodic Bloch
basis and the positive Fourier phase declared by the project research specification.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

import numpy as np

from ksdft2effmass.operators import (
    MODEL_SYSTEM_UNIT_CONVERTER,
    ComplexMatrixQuantity,
    MatrixQuantity,
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
)

type CellDisplacement3D = tuple[int, int, int]


class SiliconSp3sStarParameter(StrEnum):
    """Identify the eight independent coefficients of the initial model class."""

    S_ONSITE = "s-onsite"
    P_ONSITE = "p-onsite"
    S_STAR_ONSITE = "s-star-onsite"
    SS_SIGMA = "ss-sigma"
    SP_SIGMA = "sp-sigma"
    S_STAR_P_SIGMA = "s-star-p-sigma"
    PP_SIGMA = "pp-sigma"
    PP_PI = "pp-pi"


@dataclass(frozen=True, slots=True)
class SiliconSp3sStarNearestNeighborParameters:
    r"""Store parameter magnitudes for the initial silicon model class.

    Every value is a finite built-in ``float`` expressed in the model's declared
    energy unit. The parameterization contains three onsite coefficients and five
    nearest-neighbor two-center integrals. In particular, ``s-s*``, ``s*-s*``, and
    same-sublattice hopping channels are exact zeros of this model class rather than
    missing data.

    Parameters
    ----------
    s_onsite
        Common onsite energy of each valence-like ``s`` orbital.
    p_onsite
        Common onsite energy of each ``p_x``, ``p_y``, and ``p_z`` orbital.
    s_star_onsite
        Common onsite energy of each excited ``s*`` orbital.
    ss_sigma
        Nearest-neighbor :math:`ss\sigma` integral.
    sp_sigma
        Nearest-neighbor :math:`sp\sigma` integral.
    s_star_p_sigma
        Nearest-neighbor :math:`s^*p\sigma` integral.
    pp_sigma
        Nearest-neighbor :math:`pp\sigma` integral.
    pp_pi
        Nearest-neighbor :math:`pp\pi` integral.
    """

    s_onsite: float
    p_onsite: float
    s_star_onsite: float
    ss_sigma: float
    sp_sigma: float
    s_star_p_sigma: float
    pp_sigma: float
    pp_pi: float

    def __post_init__(self) -> None:
        """Validate exact scalar types and finiteness."""
        for name, value in self._named_coefficients():
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not np.isfinite(value):
                raise ValueError(f"{name} must be finite")

    def coefficient(self, parameter: SiliconSp3sStarParameter) -> float:
        """Return the magnitude associated with one exact parameter identity."""
        if type(parameter) is not SiliconSp3sStarParameter:
            raise TypeError("parameter must be SiliconSp3sStarParameter")
        return dict(self._parameter_coefficients())[parameter]

    def _named_coefficients(self) -> tuple[tuple[str, float], ...]:
        """Return field names and values in the frozen parameter order."""
        return (
            ("s_onsite", self.s_onsite),
            ("p_onsite", self.p_onsite),
            ("s_star_onsite", self.s_star_onsite),
            ("ss_sigma", self.ss_sigma),
            ("sp_sigma", self.sp_sigma),
            ("s_star_p_sigma", self.s_star_p_sigma),
            ("pp_sigma", self.pp_sigma),
            ("pp_pi", self.pp_pi),
        )

    def _parameter_coefficients(
        self,
    ) -> tuple[tuple[SiliconSp3sStarParameter, float], ...]:
        """Return parameter identities and values in model-component order."""
        return tuple(zip(SiliconSp3sStarParameter, self.values, strict=True))

    @property
    def values(self) -> tuple[float, ...]:
        """Return coefficient magnitudes in :class:`SiliconSp3sStarParameter` order."""
        return tuple(value for _, value in self._named_coefficients())


@dataclass(frozen=True, slots=True)
class SiliconDiamondSp3sStarNearestNeighborModel:
    r"""Define one spinless orthogonal nearest-neighbor silicon model.

    The primitive vectors, expressed in conventional cubic Cartesian axes, are

    .. math::

       \frac{a}{2}(0,1,1),\quad
       \frac{a}{2}(1,0,1),\quad
       \frac{a}{2}(1,1,0),

    with sublattice sites ``A=(0,0,0)`` and ``B=(1,1,1)/4``. The ordered cell basis
    is ``(A:s, A:px, A:py, A:pz, A:s*, B:s, B:px, B:py, B:pz, B:s*)``.
    Spin is implicit, the overlap matrix is the identity, and all parameter
    magnitudes use ``energy_unit`` relative to ``energy_reference``.

    Parameters
    ----------
    identifier
        Nonempty identity of this effective-model instance.
    basis_identifier
        Nonempty identity of the exact ordered orbital coordinate system.
    parameters
        Eight coefficients of the frozen nearest-neighbor model class.
    lattice_constant
        Positive physical length of the conventional cubic lattice edge.
    energy_unit
        Physical energy unit shared by every parameter and represented block.
    energy_reference
        Nonempty identity of the scalar energy zero.
    """

    identifier: str
    basis_identifier: str
    parameters: SiliconSp3sStarNearestNeighborParameters
    lattice_constant: ScalarQuantity
    energy_unit: PhysicalUnit
    energy_reference: str

    def __post_init__(self) -> None:
        """Validate identities, parameter class, and physical dimensions."""
        self._check_args_identities()
        self._check_args_parameters()
        self._check_args_units()

    def _check_args_identities(self) -> None:
        """Validate explicit nonempty model, basis, and energy-zero identities."""
        for name, value in (
            ("identifier", self.identifier),
            ("basis_identifier", self.basis_identifier),
            ("energy_reference", self.energy_reference),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a string")
            if not value:
                raise ValueError(f"{name} must be nonempty")

    def _check_args_parameters(self) -> None:
        """Require the exact frozen nearest-neighbor parameter record."""
        if type(self.parameters) is not SiliconSp3sStarNearestNeighborParameters:
            raise TypeError(
                "parameters must be SiliconSp3sStarNearestNeighborParameters"
            )

    def _check_args_units(self) -> None:
        """Validate a positive physical lattice length and physical energy unit."""
        if type(self.lattice_constant) is not ScalarQuantity:
            raise TypeError("lattice_constant must be ScalarQuantity")
        if not isinstance(self.lattice_constant.unit, PhysicalUnit):
            raise ValueError("lattice_constant must have a physical length unit")
        MODEL_SYSTEM_UNIT_CONVERTER.conversion_factor(
            self.lattice_constant.unit, PhysicalUnit("meter")
        )
        if self.lattice_constant.magnitude <= 0.0:
            raise ValueError("lattice_constant must be positive")
        if type(self.energy_unit) is not PhysicalUnit:
            raise TypeError("energy_unit must be PhysicalUnit")
        MODEL_SYSTEM_UNIT_CONVERTER.conversion_factor(
            self.energy_unit, PhysicalUnit("joule")
        )

    @property
    def basis_labels(self) -> tuple[str, ...]:
        """Return the exact ten-coordinate cell-basis order."""
        return tuple(
            f"{site}:{orbital}"
            for site in ("A", "B")
            for orbital in ("s", "px", "py", "pz", "s*")
        )

    @property
    def primitive_vectors_in_cubic_axes(self) -> MatrixQuantity:
        """Return primitive vectors divided by the conventional lattice constant."""
        return MatrixQuantity(
            np.asarray(
                (
                    (0.0, 0.5, 0.5),
                    (0.5, 0.0, 0.5),
                    (0.5, 0.5, 0.0),
                )
            ),
            Unitless(),
        )

    @property
    def basis_positions_in_cubic_axes(self) -> MatrixQuantity:
        """Return ``A`` and ``B`` positions divided by the lattice constant."""
        return MatrixQuantity(
            np.asarray(((0.0, 0.0, 0.0), (0.25, 0.25, 0.25))), Unitless()
        )


@dataclass(frozen=True, slots=True, eq=False)
class SiliconSp3sStarOperatorComponent:
    r"""Retain one dimensionless basis operator :math:`B_a(R)`.

    Multiplying every block by the corresponding parameter magnitude in the model's
    energy unit gives that parameter's contribution to the finite real-space
    representation.
    """

    parameter: SiliconSp3sStarParameter
    cell_displacements: tuple[CellDisplacement3D, ...]
    blocks: tuple[ComplexMatrixQuantity, ...]

    def __post_init__(self) -> None:
        """Validate parameter identity, canonical cells, and dimensionless blocks."""
        if type(self.parameter) is not SiliconSp3sStarParameter:
            raise TypeError("parameter must be SiliconSp3sStarParameter")
        _check_cell_displacements(self.cell_displacements)
        _check_block_family(
            self.blocks,
            self.cell_displacements,
            Unitless,
            "component blocks",
        )
        indexed = dict(zip(self.cell_displacements, self.blocks, strict=True))
        for displacement, block in indexed.items():
            reverse = (-displacement[0], -displacement[1], -displacement[2])
            if not np.array_equal(indexed[reverse].magnitude, block.magnitude.conj().T):
                raise ValueError("component blocks must obey H(-R) = H(R)^dagger")
        expected = _canonical_component_blocks(self.parameter, self.cell_displacements)
        if any(
            not np.array_equal(block.magnitude, expected_block)
            for block, expected_block in zip(self.blocks, expected, strict=True)
        ):
            raise ValueError(
                "component blocks must equal the canonical parameter basis operator"
            )


@dataclass(frozen=True, slots=True, eq=False)
class SiliconDiamondSp3sStarNearestNeighborOperator:
    r"""Retain the finite real-space representation of one model instance.

    The displacement convention is

    .. math::

       [H(R)]_{\mu\nu}
       = \langle\chi_{\mu 0}|\hat H|\chi_{\nu R}\rangle.

    ``components`` expose the exact eight-dimensional linear model span. ``blocks``
    contain their parameter-weighted sum and obey ``H(-R)=H(R)^dagger``. This record
    establishes a tight-binding representation only; it does not establish alignment
    with any Wannier coordinate system.
    """

    model: SiliconDiamondSp3sStarNearestNeighborModel
    components: tuple[SiliconSp3sStarOperatorComponent, ...]
    cell_displacements: tuple[CellDisplacement3D, ...]
    blocks: tuple[ComplexMatrixQuantity, ...]

    def __post_init__(self) -> None:
        """Validate model correlation, component order, and represented operator."""
        self._check_args_model_and_components()
        self._check_args_blocks()
        self._check_args_linear_combination()
        self._check_args_hermiticity()

    def _check_args_model_and_components(self) -> None:
        """Validate exact types, canonical cells, and complete component ordering."""
        if type(self.model) is not SiliconDiamondSp3sStarNearestNeighborModel:
            raise TypeError("model must be SiliconDiamondSp3sStarNearestNeighborModel")
        if type(self.components) is not tuple:
            raise TypeError("components must be a tuple")
        if any(
            type(component) is not SiliconSp3sStarOperatorComponent
            for component in self.components
        ):
            raise TypeError(
                "components must contain SiliconSp3sStarOperatorComponent values"
            )
        if tuple(component.parameter for component in self.components) != tuple(
            SiliconSp3sStarParameter
        ):
            raise ValueError("components must follow the complete parameter order")
        _check_cell_displacements(self.cell_displacements)
        if any(
            component.cell_displacements != self.cell_displacements
            for component in self.components
        ):
            raise ValueError("component cell displacements must match the operator")

    def _check_args_blocks(self) -> None:
        """Validate one homogeneous energy block for every canonical displacement."""
        _check_block_family(
            self.blocks,
            self.cell_displacements,
            PhysicalUnit,
            "operator blocks",
        )
        if any(block.unit != self.model.energy_unit for block in self.blocks):
            raise ValueError("operator blocks must use the model energy unit")

    def _check_args_linear_combination(self) -> None:
        """Require represented blocks to equal the declared parameter combination."""
        expected = np.zeros((len(self.cell_displacements), 10, 10), dtype=np.complex128)
        for component in self.components:
            coefficient = self.model.parameters.coefficient(component.parameter)
            expected += coefficient * np.asarray(
                [block.magnitude for block in component.blocks]
            )
        actual = np.asarray([block.magnitude for block in self.blocks])
        if not np.array_equal(actual, expected):
            raise ValueError("operator blocks must equal the parameter combination")

    def _check_args_hermiticity(self) -> None:
        """Require exact real-space Hermitian displacement reversal."""
        indexed = dict(zip(self.cell_displacements, self.blocks, strict=True))
        for displacement, block in indexed.items():
            reverse: CellDisplacement3D = (
                -displacement[0],
                -displacement[1],
                -displacement[2],
            )
            if reverse not in indexed:
                raise ValueError(
                    "operator displacement inventory must be reversal closed"
                )
            if not np.array_equal(indexed[reverse].magnitude, block.magnitude.conj().T):
                raise ValueError("operator blocks must obey H(-R) = H(R)^dagger")

    @property
    def matrix_dimension(self) -> int:
        """Return the fixed ten-orbital primitive-cell dimension."""
        return 10

    @property
    def overlap_matrix(self) -> ComplexMatrixQuantity:
        """Return the explicit identity overlap of the orthogonal model."""
        return ComplexMatrixQuantity(np.eye(10, dtype=np.complex128), Unitless())


@dataclass(frozen=True, slots=True, eq=False)
class SiliconSp3sStarBlochHamiltonianSamples:
    """Retain Bloch matrices at explicitly ordered reduced wavevectors.

    Reduced coordinates ``q`` are defined by ``k·a_i = 2π q_i`` for the primitive
    vectors ``a_i``. Matrices use the cell-periodic orbital gauge and the positive
    Fourier phase ``exp(+2π i q·R)``.
    """

    operator: SiliconDiamondSp3sStarNearestNeighborOperator
    reduced_wavevectors: MatrixQuantity
    matrices: tuple[ComplexMatrixQuantity, ...]

    def __post_init__(self) -> None:
        """Validate operator identity, reduced coordinates, and matrix family."""
        if type(self.operator) is not SiliconDiamondSp3sStarNearestNeighborOperator:
            raise TypeError(
                "operator must be SiliconDiamondSp3sStarNearestNeighborOperator"
            )
        if type(self.reduced_wavevectors) is not MatrixQuantity:
            raise TypeError("reduced_wavevectors must be MatrixQuantity")
        if not isinstance(self.reduced_wavevectors.unit, Unitless):
            raise ValueError("reduced_wavevectors must be unitless")
        if self.reduced_wavevectors.magnitude.ndim != 2 or (
            self.reduced_wavevectors.magnitude.shape[1] != 3
        ):
            raise ValueError("reduced_wavevectors must have shape (sample, 3)")
        if type(self.matrices) is not tuple or len(self.matrices) != len(
            self.reduced_wavevectors.magnitude
        ):
            raise ValueError("matrices must contain one value per wavevector")
        if any(type(matrix) is not ComplexMatrixQuantity for matrix in self.matrices):
            raise TypeError("matrices must contain ComplexMatrixQuantity values")
        for matrix in self.matrices:
            if matrix.magnitude.shape != (10, 10):
                raise ValueError("Bloch matrices must have shape (10, 10)")
            if matrix.unit != self.operator.model.energy_unit:
                raise ValueError("Bloch matrices must use the model energy unit")
        expected = _bloch_matrices(self.operator, self.reduced_wavevectors)
        if any(
            not np.array_equal(matrix.magnitude, expected_value)
            for matrix, expected_value in zip(self.matrices, expected, strict=True)
        ):
            raise ValueError(
                "Bloch matrices must equal the declared positive-phase Fourier sum"
            )


class SiliconDiamondSp3sStarNearestNeighborConstructor:
    r"""Construct the eight-component real-space operator.

    For a directed bond from the row-site ``A`` orbital to the column-site ``B``
    orbital with cubic direction cosines ``d=(l,m,n)``, the implemented convention is

    .. math::

       \langle s_A|H|p_{jB}\rangle=d_j V_{sp\sigma},\qquad
       \langle p_{iA}|H|s_B\rangle=-d_i V_{sp\sigma},

    with the same parity convention for ``s*`` and

    .. math::

       \langle p_{iA}|H|p_{jB}\rangle
       =d_i d_j V_{pp\sigma}+(\delta_{ij}-d_i d_j)V_{pp\pi}.

    The four ``A(0) -> B(R)`` nearest-neighbor cell displacements are ``(0,0,0)``,
    ``(-1,0,0)``, ``(0,-1,0)``, and ``(0,0,-1)``. Reverse blocks are constructed
    explicitly; no matrix shape or spectrum is used to infer Hermiticity.
    """

    __slots__ = ()

    def execute(
        self, model: SiliconDiamondSp3sStarNearestNeighborModel
    ) -> SiliconDiamondSp3sStarNearestNeighborOperator:
        """Return the component span and parameter-weighted real-space blocks."""
        if type(model) is not SiliconDiamondSp3sStarNearestNeighborModel:
            raise TypeError("model must be SiliconDiamondSp3sStarNearestNeighborModel")
        displacements = _canonical_displacements()
        components = tuple(
            SiliconSp3sStarOperatorComponent(
                parameter,
                displacements,
                tuple(
                    ComplexMatrixQuantity(block, Unitless())
                    for block in _canonical_component_blocks(parameter, displacements)
                ),
            )
            for parameter in SiliconSp3sStarParameter
        )
        assembled = np.zeros((len(displacements), 10, 10), dtype=np.complex128)
        for component in components:
            coefficient = model.parameters.coefficient(component.parameter)
            assembled += coefficient * np.asarray(
                [block.magnitude for block in component.blocks]
            )
        return SiliconDiamondSp3sStarNearestNeighborOperator(
            model,
            components,
            displacements,
            tuple(
                ComplexMatrixQuantity(block, model.energy_unit) for block in assembled
            ),
        )


class SiliconSp3sStarBlochHamiltonianConstructor:
    """Evaluate a represented model without diagonalization or basis alignment."""

    __slots__ = ()

    def execute(
        self,
        operator: SiliconDiamondSp3sStarNearestNeighborOperator,
        reduced_wavevectors: MatrixQuantity,
    ) -> SiliconSp3sStarBlochHamiltonianSamples:
        """Evaluate ``sum_R exp(+2π i q·R) H(R)`` at every reduced wavevector."""
        if type(operator) is not SiliconDiamondSp3sStarNearestNeighborOperator:
            raise TypeError(
                "operator must be SiliconDiamondSp3sStarNearestNeighborOperator"
            )
        if type(reduced_wavevectors) is not MatrixQuantity:
            raise TypeError("reduced_wavevectors must be MatrixQuantity")
        if not isinstance(reduced_wavevectors.unit, Unitless):
            raise ValueError("reduced_wavevectors must be unitless")
        if reduced_wavevectors.magnitude.ndim != 2 or (
            reduced_wavevectors.magnitude.shape[1] != 3
        ):
            raise ValueError("reduced_wavevectors must have shape (sample, 3)")
        matrices = _bloch_matrices(operator, reduced_wavevectors)
        return SiliconSp3sStarBlochHamiltonianSamples(
            operator,
            reduced_wavevectors,
            tuple(
                ComplexMatrixQuantity(matrix, operator.model.energy_unit)
                for matrix in matrices
            ),
        )


def _canonical_component_blocks(
    parameter: SiliconSp3sStarParameter,
    displacements: tuple[CellDisplacement3D, ...],
) -> tuple[np.ndarray, ...]:
    """Construct one canonical dimensionless real-space basis operator."""
    indexed = {
        displacement: np.zeros((10, 10), dtype=np.complex128)
        for displacement in displacements
    }
    if parameter in (
        SiliconSp3sStarParameter.S_ONSITE,
        SiliconSp3sStarParameter.P_ONSITE,
        SiliconSp3sStarParameter.S_STAR_ONSITE,
    ):
        _add_onsite_component(indexed[(0, 0, 0)], parameter)
    else:
        for displacement, signed_direction in _directed_nearest_neighbors():
            direction = np.asarray(signed_direction, dtype=np.float64) / np.sqrt(3.0)
            hopping = _directed_bond_component(parameter, direction)
            indexed[displacement][0:5, 5:10] += hopping
            reverse: CellDisplacement3D = (
                -displacement[0],
                -displacement[1],
                -displacement[2],
            )
            indexed[reverse][5:10, 0:5] += hopping.T
    return tuple(indexed[displacement] for displacement in displacements)


def _add_onsite_component(
    block: np.ndarray, parameter: SiliconSp3sStarParameter
) -> None:
    """Add the selected sublattice-equal onsite diagonal."""
    local_indices: tuple[int, ...]
    if parameter is SiliconSp3sStarParameter.S_ONSITE:
        local_indices = (0,)
    elif parameter is SiliconSp3sStarParameter.P_ONSITE:
        local_indices = (1, 2, 3)
    else:
        local_indices = (4,)
    for site_offset in (0, 5):
        for local_index in local_indices:
            block[site_offset + local_index, site_offset + local_index] = 1.0


def _directed_bond_component(
    parameter: SiliconSp3sStarParameter,
    direction: np.ndarray,
) -> np.ndarray:
    """Return one canonical five-orbital directed bond component."""
    block = np.zeros((5, 5), dtype=np.complex128)
    if parameter is SiliconSp3sStarParameter.SS_SIGMA:
        block[0, 0] = 1.0
    elif parameter is SiliconSp3sStarParameter.SP_SIGMA:
        block[0, 1:4] = direction
        block[1:4, 0] = -direction
    elif parameter is SiliconSp3sStarParameter.S_STAR_P_SIGMA:
        block[4, 1:4] = direction
        block[1:4, 4] = -direction
    elif parameter is SiliconSp3sStarParameter.PP_SIGMA:
        block[1:4, 1:4] = np.outer(direction, direction)
    elif parameter is SiliconSp3sStarParameter.PP_PI:
        block[1:4, 1:4] = np.eye(3) - np.outer(direction, direction)
    else:
        raise ValueError("onsite parameters do not define directed bond blocks")
    return block


def _bloch_matrices(
    operator: SiliconDiamondSp3sStarNearestNeighborOperator,
    reduced_wavevectors: MatrixQuantity,
) -> np.ndarray:
    """Return the declared positive-phase cell-periodic Fourier sum."""
    displacements = np.asarray(operator.cell_displacements, dtype=np.float64)
    phases = np.exp(2j * np.pi * reduced_wavevectors.magnitude @ displacements.T)
    blocks = np.asarray([block.magnitude for block in operator.blocks])
    return np.einsum("kr,rij->kij", phases, blocks, optimize=True)


def _canonical_displacements() -> tuple[CellDisplacement3D, ...]:
    """Return the minimal reversal-closed model support in canonical order."""
    return (
        (-1, 0, 0),
        (0, -1, 0),
        (0, 0, -1),
        (0, 0, 0),
        (0, 0, 1),
        (0, 1, 0),
        (1, 0, 0),
    )


def _directed_nearest_neighbors() -> tuple[
    tuple[CellDisplacement3D, tuple[int, int, int]], ...
]:
    """Return ``A(0) -> B(R)`` cells and cubic direction signs."""
    return (
        ((0, 0, 0), (1, 1, 1)),
        ((-1, 0, 0), (1, -1, -1)),
        ((0, -1, 0), (-1, 1, -1)),
        ((0, 0, -1), (-1, -1, 1)),
    )


def _check_cell_displacements(
    displacements: tuple[CellDisplacement3D, ...],
) -> None:
    """Validate the exact canonical nearest-neighbor support."""
    if type(displacements) is not tuple:
        raise TypeError("cell_displacements must be a tuple")
    if any(
        type(displacement) is not tuple
        or len(displacement) != 3
        or any(type(value) is not int for value in displacement)
        for displacement in displacements
    ):
        raise TypeError("cell_displacements must contain integer triples")
    if displacements != _canonical_displacements():
        raise ValueError("cell_displacements must use the canonical model support")


def _check_block_family(
    blocks: tuple[ComplexMatrixQuantity, ...],
    displacements: tuple[CellDisplacement3D, ...],
    unit_type: type[PhysicalUnit] | type[Unitless],
    name: str,
) -> None:
    """Validate one homogeneous ten-orbital block per cell displacement."""
    if type(blocks) is not tuple or len(blocks) != len(displacements):
        raise ValueError(f"{name} must contain one block per displacement")
    if any(type(block) is not ComplexMatrixQuantity for block in blocks):
        raise TypeError(f"{name} must contain ComplexMatrixQuantity values")
    for block in blocks:
        if block.magnitude.shape != (10, 10):
            raise ValueError(f"{name} must have shape (10, 10)")
        if not isinstance(block.unit, unit_type):
            raise ValueError(f"{name} have an invalid unit category")
