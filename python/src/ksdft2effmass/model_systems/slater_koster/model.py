"""Concrete diamond ``sp3s*`` composition over reusable PhysKit mechanics."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from projectkoios.numerics.numpy.typing import Float64Array, Float64Matrix
from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeDimension,
    LatticeDisplacement,
)
from projectkoios.physkit.periodic.lattice.hopping import (
    DenseBlockHoppingModel,
    DenseBlockHoppingTerm,
)
from projectkoios.physkit.solidstate.tb.bloch import DenseBlockHoppingBlochEvaluator
from projectkoios.physkit.solidstate.tb.orbital_center_gauge import (
    CellToFullCenterGaugeTransformationConstructor,
    CellToFullCenterGaugeTransformationDefinition,
)
from projectkoios.physkit.solidstate.tb.slater_koster import (
    SP3S_STAR_ORBITAL_ORDER,
    HomopolarSp3sStarCellGaugeModelAssembler,
    HomopolarSp3sStarCellGaugeModelDefinition,
    HomopolarSp3sStarLinearBlochEvaluation,
    HomopolarSp3sStarLinearBlochEvaluator,
    HomopolarSp3sStarLinearParameterization,
    HomopolarSp3sStarLinearParameterizationAssembler,
    HomopolarSp3sStarParameterGroup,
    HomopolarSp3sStarParameterizedBond,
    HomopolarSp3sStarTwoCenterHoppingConstructor,
    HomopolarSp3sStarTwoCenterHoppingDefinition,
    SlaterKosterBondDirection,
)
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    MatrixQuantity,
    UnitSystem,
    VectorQuantity,
)

from ksdft2effmass.hamiltonian import HermitianHamiltonian
from ksdft2effmass.periodic.operators.basis import (
    SlaterKosterOrbital,
    SlaterKosterOrbitalBasisCoordinate,
)
from ksdft2effmass.periodic.periodic3d.operators.basis import Periodic3DBasisIdentity

from .geometry import (
    ORIGIN_CENTER_IDENTIFIER,
    QUARTER_CENTER_IDENTIFIER,
    DiamondSp3sStarGeometry,
)
from .parameters import ELECTRON_VOLT, DiamondSp3sStarParameters

_MODEL_IDENTIFIER = "homopolar-diamond-spinless-sp3s-star"
_ENERGY_REFERENCE = "onsite-parameter-defined"
_FIRST_NEIGHBOR_GROUP = "diamond-first-neighbor"
_SECOND_NEIGHBOR_GROUP = "diamond-second-neighbor"

_ORBITAL_BY_PHYSKIT_NAME = {
    "s": SlaterKosterOrbital.S,
    "p_x": SlaterKosterOrbital.P_X,
    "p_y": SlaterKosterOrbital.P_Y,
    "p_z": SlaterKosterOrbital.P_Z,
    "s_star": SlaterKosterOrbital.S_STAR,
}

_DIAMOND_SP3S_STAR_BASIS = Periodic3DBasisIdentity(
    display_identifier="diamond-spinless-sp3s-star",
    coordinates=tuple(
        SlaterKosterOrbitalBasisCoordinate(
            site_label=center_identifier,
            orbital=_ORBITAL_BY_PHYSKIT_NAME[orbital_name],
        )
        for center_identifier in (
            ORIGIN_CENTER_IDENTIFIER,
            QUARTER_CENTER_IDENTIFIER,
        )
        for orbital_name in SP3S_STAR_ORBITAL_ORDER
    ),
)


def _immutable_fractional_k(value: Float64Array) -> Float64Array:
    """Validate and copy one fractional reciprocal coordinate into immutable storage."""
    if not isinstance(value, np.ndarray):
        raise TypeError("fractional_k must be a numpy.ndarray")
    if value.dtype.kind not in "iuf":
        raise TypeError("fractional_k must contain real numbers excluding booleans")
    result = np.asarray(value, dtype=np.float64)
    if result.shape != (3,):
        raise ValueError("fractional_k must have shape (3,)")
    if not np.all(np.isfinite(result)):
        raise ValueError("fractional_k must be finite")
    immutable = np.frombuffer(result.astype("<f8").tobytes(), dtype="<f8")
    return immutable.reshape((3,))


@dataclass(frozen=True, slots=True, kw_only=True)
class DiamondSp3sStarBlochHamiltonianEvaluation:
    """Retain one full-center matrix with model, fiber, and ordered KSD basis."""

    model: DiamondSp3sStarModel
    fractional_k: Float64Array
    hamiltonian: HermitianHamiltonian

    def __post_init__(self) -> None:
        if type(self.model) is not DiamondSp3sStarModel:
            raise TypeError("model must be DiamondSp3sStarModel")
        object.__setattr__(
            self,
            "fractional_k",
            _immutable_fractional_k(self.fractional_k),
        )
        if type(self.hamiltonian) is not HermitianHamiltonian:
            raise TypeError("hamiltonian must be HermitianHamiltonian")
        if type(self.hamiltonian.matrix) is not ComplexMatrixQuantity:
            raise TypeError("hamiltonian matrix must be ComplexMatrixQuantity")
        if self.hamiltonian.matrix.magnitude.shape != (10, 10):
            raise ValueError("hamiltonian matrix must match the ten-orbital basis")
        if self.hamiltonian.matrix.unit != ELECTRON_VOLT:
            raise ValueError("hamiltonian matrix must use electron_volt")

    @property
    def basis_identity(self) -> Periodic3DBasisIdentity:
        """Return the exact KSD basis correlated with the represented matrix."""
        return self.model.basis_identity


@dataclass(frozen=True, slots=True, kw_only=True)
class DiamondSp3sStarModel:
    r"""KSD-owned diamond composition using PhysKit Slater--Koster mechanics.

    KSD selects the two diamond centers, first- and second-neighbor inventories,
    onsite policy, parameter sharing, energy reference, and represented KSD basis.
    PhysKit owns structured spatial basis admission, directed bond geometry, the
    seven-channel two-center matrix, generated Hermitian reverses, ordinary-cell
    assembly, linear channel parameterization, reciprocal-sample evaluation, finite
    Fourier evaluation, and orbital-center gauge construction.
    """

    geometry: DiamondSp3sStarGeometry
    parameters: DiamondSp3sStarParameters

    def __post_init__(self) -> None:
        if type(self.geometry) is not DiamondSp3sStarGeometry:
            raise TypeError("geometry must be DiamondSp3sStarGeometry")
        if type(self.parameters) is not DiamondSp3sStarParameters:
            raise TypeError("parameters must be DiamondSp3sStarParameters")

    @property
    def basis_identity(self) -> Periodic3DBasisIdentity:
        """Return the descriptive ordered ten-coordinate KSD basis identity."""
        return _DIAMOND_SP3S_STAR_BASIS

    @property
    def cell_gauge_hopping_definition(
        self,
    ) -> HomopolarSp3sStarCellGaugeModelDefinition:
        """Return the exact KSD-composed hopping definition without onsite terms."""
        basis = self.geometry.spatial_basis
        parameter_groups = (
            HomopolarSp3sStarParameterGroup(
                identifier=_FIRST_NEIGHBOR_GROUP,
                integrals=self.parameters.first_neighbor.two_center_integrals,
            ),
            HomopolarSp3sStarParameterGroup(
                identifier=_SECOND_NEIGHBOR_GROUP,
                integrals=self.parameters.second_neighbor.two_center_integrals,
            ),
        )
        bonds = tuple(
            HomopolarSp3sStarParameterizedBond(
                geometry=self.geometry.bond_geometry(bond=bond),
                parameter_group_identifier=_FIRST_NEIGHBOR_GROUP,
            )
            for bond in self.geometry.first_neighbor_bonds
        ) + tuple(
            HomopolarSp3sStarParameterizedBond(
                geometry=self.geometry.bond_geometry(bond=bond),
                parameter_group_identifier=_SECOND_NEIGHBOR_GROUP,
            )
            for bond in self.geometry.second_neighbor_positive_bonds_by_sublattice
        )
        return HomopolarSp3sStarCellGaugeModelDefinition(
            identifier=_MODEL_IDENTIFIER,
            basis=basis,
            parameter_groups=parameter_groups,
            bonds=bonds,
            energy_reference=_ENERGY_REFERENCE,
        )

    @property
    def linear_hopping_parameterization(
        self,
    ) -> HomopolarSp3sStarLinearParameterization:
        """Return all seven nondimensional channel models for both shell groups."""
        return HomopolarSp3sStarLinearParameterizationAssembler().execute(
            definition=self.cell_gauge_hopping_definition
        )

    def linear_hopping_bloch(
        self,
        *,
        fractional_wave_vectors: MatrixQuantity,
    ) -> HomopolarSp3sStarLinearBlochEvaluation:
        """Evaluate hopping-only channel models in ordinary-cell Bloch gauge."""
        return HomopolarSp3sStarLinearBlochEvaluator().execute(
            parameterization=self.linear_hopping_parameterization,
            fractional_wave_vectors=fractional_wave_vectors,
        )

    @property
    def cell_gauge_model(self) -> DenseBlockHoppingModel:
        """Return the complete PhysKit ordinary-cell model including onsite terms."""
        assembly = HomopolarSp3sStarCellGaugeModelAssembler().execute(
            definition=self.cell_gauge_hopping_definition
        )
        return self._with_onsite(assembly.model)

    def hamiltonian_at(
        self,
        *,
        fractional_k: Float64Array,
    ) -> DiamondSp3sStarBlochHamiltonianEvaluation:
        """Evaluate the full-center exact-Hermitian ten-by-ten matrix in eV."""
        k_point = _immutable_fractional_k(fractional_k)
        cell_model = self.cell_gauge_model
        self._validate_phase_arguments(model=cell_model, fractional_k=k_point)
        fractional_wave_vectors = MatrixQuantity(
            magnitude=k_point.reshape((1, 3)),
            unit=UnitSystem.NONDIMENSIONAL.length_unit,
        )
        try:
            cell_matrix = (
                DenseBlockHoppingBlochEvaluator()
                .evaluate(
                    cell_model,
                    fractional_wave_vectors,
                )
                .bloch_matrices[0]
                .magnitude
            )
        except FloatingPointError as error:
            raise OverflowError("Bloch evaluation arithmetic overflowed") from error

        gauge = (
            CellToFullCenterGaugeTransformationConstructor()
            .execute(
                definition=CellToFullCenterGaugeTransformationDefinition(
                    orbital_centers_fractional=(
                        self.geometry.spatial_basis.definition.orbital_centers_fractional
                    ),
                    fractional_wave_vector=VectorQuantity(
                        magnitude=k_point,
                        unit=UnitSystem.NONDIMENSIONAL.length_unit,
                    ),
                )
            )
            .matrix.magnitude
        )
        with np.errstate(over="ignore", invalid="ignore"):
            full_center = gauge.conjugate().T @ cell_matrix @ gauge
        if not np.all(np.isfinite(full_center)):
            raise OverflowError("Slater-Koster matrix arithmetic overflowed")

        # The KSD model class requires a Hermitian represented Hamiltonian. PhysKit
        # owns paired coefficients and Fourier evaluation; this final projection only
        # removes binary64 anti-Hermitian roundoff introduced by matrix products.
        antihermitian = full_center - full_center.conjugate().T
        scale = max(1.0, float(np.linalg.norm(full_center, ord=np.inf)))
        tolerance = 128.0 * np.finfo(np.float64).eps * scale
        if float(np.linalg.norm(antihermitian, ord=np.inf)) > tolerance:
            raise ArithmeticError("constructed Slater-Koster matrix is not Hermitian")
        full_center = 0.5 * (full_center + full_center.conjugate().T)

        return DiamondSp3sStarBlochHamiltonianEvaluation(
            model=self,
            fractional_k=k_point,
            hamiltonian=HermitianHamiltonian(
                matrix=ComplexMatrixQuantity(full_center, ELECTRON_VOLT)
            ),
        )

    def two_center_hopping(
        self,
        *,
        shell: int,
        direction_cosines: Float64Array,
    ) -> Float64Matrix:
        """Return the PhysKit-owned real five-by-five two-center matrix in eV."""
        if type(shell) is not int:
            raise TypeError("shell must be a built-in int")
        if shell not in (1, 2):
            raise ValueError("shell must be 1 or 2")
        direction = self._direction_cosines(direction_cosines)
        integrals = (
            self.parameters.first_neighbor.two_center_integrals
            if shell == 1
            else self.parameters.second_neighbor.two_center_integrals
        )
        return (
            HomopolarSp3sStarTwoCenterHoppingConstructor()
            .execute(
                definition=HomopolarSp3sStarTwoCenterHoppingDefinition(
                    bond_direction=SlaterKosterBondDirection(
                        components=VectorQuantity(
                            magnitude=direction,
                            unit=UnitSystem.NONDIMENSIONAL.length_unit,
                        )
                    ),
                    integrals=integrals,
                )
            )
            .matrix.magnitude
        )

    def _with_onsite(
        self,
        hopping_model: DenseBlockHoppingModel,
    ) -> DenseBlockHoppingModel:
        coefficients = {
            term.displacement.components: np.asarray(
                term.coefficient.magnitude,
                dtype=np.complex128,
            ).copy()
            for term in hopping_model.terms
        }
        zero = (0, 0, 0)
        coefficient = coefficients.setdefault(
            zero,
            np.zeros((10, 10), dtype=np.complex128),
        )
        onsite = self.parameters.onsite
        onsite_block = np.diag(
            np.asarray(
                (
                    onsite.s.magnitude,
                    onsite.p.magnitude,
                    onsite.p.magnitude,
                    onsite.p.magnitude,
                    onsite.s_star.magnitude,
                ),
                dtype=np.float64,
            )
        )
        with np.errstate(over="ignore", invalid="ignore"):
            coefficient[0:5, 0:5] += onsite_block
            coefficient[5:10, 5:10] += onsite_block
        if any(not np.all(np.isfinite(value)) for value in coefficients.values()):
            raise OverflowError("cell-gauge composition arithmetic overflowed")

        terms = tuple(
            DenseBlockHoppingTerm(
                displacement=LatticeDisplacement(
                    dimension=LatticeDimension.THREE,
                    components=displacement,
                ),
                coefficient=ComplexMatrixQuantity(matrix, ELECTRON_VOLT),
            )
            for displacement, matrix in sorted(coefficients.items())
        )
        return DenseBlockHoppingModel(
            identifier=hopping_model.identifier,
            dimension=LatticeDimension.THREE,
            terms=terms,
            energy_unit=ELECTRON_VOLT,
            energy_reference=hopping_model.energy_reference,
            basis_identifier=hopping_model.basis_identifier,
        )

    @staticmethod
    def _validate_phase_arguments(
        *,
        model: DenseBlockHoppingModel,
        fractional_k: Float64Array,
    ) -> None:
        displacements = np.asarray(
            tuple(term.displacement.components for term in model.terms),
            dtype=np.float64,
        )
        centers = np.asarray(
            (
                (0.0, 0.0, 0.0),
                (0.25, 0.25, 0.25),
            ),
            dtype=np.float64,
        )
        with np.errstate(over="ignore", invalid="ignore"):
            cell_arguments = 2.0 * math.pi * (displacements @ fractional_k)
            center_arguments = 2.0 * math.pi * (centers @ fractional_k)
        if not np.all(np.isfinite(cell_arguments)) or not np.all(
            np.isfinite(center_arguments)
        ):
            raise OverflowError("Bloch phase argument overflowed")

    @staticmethod
    def _direction_cosines(value: Float64Array) -> Float64Array:
        if not isinstance(value, np.ndarray):
            raise TypeError("direction_cosines must be a numpy.ndarray")
        if value.dtype.kind not in "iuf":
            raise TypeError(
                "direction_cosines must contain real numbers excluding booleans"
            )
        result = np.asarray(value, dtype=np.float64)
        if result.shape != (3,):
            raise ValueError("direction_cosines must have shape (3,)")
        if not np.all(np.isfinite(result)):
            raise ValueError("direction_cosines must be finite")
        if not math.isclose(
            float(np.linalg.norm(result)),
            1.0,
            rel_tol=0.0,
            abs_tol=128.0 * np.finfo(np.float64).eps,
        ):
            raise ValueError("direction_cosines must be a unit vector")
        immutable = np.frombuffer(result.astype("<f8").tobytes(), dtype="<f8")
        return immutable.reshape((3,))
