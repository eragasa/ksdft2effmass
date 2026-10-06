"""Finite Wigner--Seitz interpolation of represented Wannier operators.

The records and actions in this module consume already identified finite-mesh
represented operators and an explicit Wigner--Seitz representative inventory. Native
Wannier90 decoding, artifact authority, retained-space selection, convergence, and
scientific validation remain with their established owners.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

import numpy as np
import numpy.typing as npt

from ksdft2effmass.operators import (
    MODEL_SYSTEM_UNIT_CONVERTER,
    ComplexMatrixQuantity,
    MatrixQuantity,
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from .wannier_kinetic import (
    WannierKineticDecompositionResult,
    WannierOperatorRole,
    WannierRepresentedOperatorMesh3D,
)

type CellRepresentative3D = tuple[int, int, int]
type ComplexArray = npt.NDArray[np.complex128]


@dataclass(frozen=True, slots=True, eq=False)
class WignerSeitzInterpolationInventory3D:
    """Retain an identified finite Wigner--Seitz representative inventory.

    Parameters
    ----------
    identifier
        Explicit identity of this interpolation inventory.
    source_binding_identifier
        Identity correlating the inventory with represented source operators.
    mesh_shape
        Source Born--von Karman reciprocal-mesh shape.
    direct_lattice
        Direct-lattice basis vectors as rows in a physical length unit.
    representatives
        Distinct ordered integer cell representatives.
    degeneracies
        Positive native degeneracies. Every representative in one modulo-mesh
        residue class has degeneracy equal to that class's supplied multiplicity.

    Notes
    -----
    This record does not parse or authenticate a native Wannier90 file. The caller
    must establish the scientific and provenance authority of the supplied inventory.
    """

    identifier: str
    source_binding_identifier: str
    mesh_shape: tuple[int, int, int]
    direct_lattice: MatrixQuantity
    representatives: tuple[CellRepresentative3D, ...]
    degeneracies: tuple[int, ...]

    def __post_init__(self) -> None:
        """Validate identity, lattice, mesh, representatives, and degeneracies."""
        self._check_args_identity()
        self._check_args_mesh_and_lattice()
        self._check_args_representatives()
        self._check_args_residue_degeneracies()

    def _check_args_identity(self) -> None:
        """Validate explicit nonempty inventory and source-binding identities."""
        for name, value in (
            ("identifier", self.identifier),
            ("source_binding_identifier", self.source_binding_identifier),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a string")
            if not value:
                raise ValueError(f"{name} must be nonempty")

    def _check_args_mesh_and_lattice(self) -> None:
        """Validate positive mesh dimensions and a nonsingular physical lattice."""
        if (
            type(self.mesh_shape) is not tuple
            or len(self.mesh_shape) != 3
            or any(type(value) is not int for value in self.mesh_shape)
        ):
            raise TypeError("mesh_shape must contain three built-in integers")
        if any(value <= 0 for value in self.mesh_shape):
            raise ValueError("mesh_shape entries must be positive")
        if type(self.direct_lattice) is not MatrixQuantity:
            raise TypeError("direct_lattice must be MatrixQuantity")
        if not isinstance(self.direct_lattice.unit, PhysicalUnit):
            raise ValueError("direct_lattice must use a physical length unit")
        try:
            MODEL_SYSTEM_UNIT_CONVERTER.conversion_factor(
                self.direct_lattice.unit, PhysicalUnit("meter")
            )
        except ValueError as error:
            raise ValueError(
                "direct_lattice must use a physical length unit"
            ) from error
        if self.direct_lattice.magnitude.shape != (3, 3):
            raise ValueError("direct_lattice must contain three three-vector rows")
        if float(np.linalg.det(self.direct_lattice.magnitude)) == 0.0:
            raise ValueError("direct_lattice must be nonsingular")

    def _check_args_representatives(self) -> None:
        """Validate a nonempty unique tuple of integer three-vectors."""
        if type(self.representatives) is not tuple or not self.representatives:
            raise TypeError("representatives must be a nonempty tuple")
        for representative in self.representatives:
            if (
                type(representative) is not tuple
                or len(representative) != 3
                or any(type(value) is not int for value in representative)
            ):
                raise TypeError(
                    "representatives must contain built-in integer three-tuples"
                )
        if len(set(self.representatives)) != len(self.representatives):
            raise ValueError("representatives must be unique")
        if type(self.degeneracies) is not tuple:
            raise TypeError("degeneracies must be a tuple")
        if len(self.degeneracies) != len(self.representatives):
            raise ValueError("one degeneracy is required per representative")
        if any(type(value) is not int for value in self.degeneracies):
            raise TypeError("degeneracies must contain built-in integers")
        if any(value <= 0 for value in self.degeneracies):
            raise ValueError("degeneracies must be positive")

    def _check_args_residue_degeneracies(self) -> None:
        """Require complete modulo-mesh residues and class-size degeneracies."""
        residue_groups: dict[CellRepresentative3D, list[int]] = {}
        for index, representative in enumerate(self.representatives):
            residue = self._residue(representative)
            residue_groups.setdefault(residue, []).append(index)
        expected = set(
            product(
                range(self.mesh_shape[0]),
                range(self.mesh_shape[1]),
                range(self.mesh_shape[2]),
            )
        )
        if set(residue_groups) != expected:
            raise ValueError(
                "representatives must cover every modulo-mesh residue class"
            )
        for indices in residue_groups.values():
            multiplicity = len(indices)
            if any(self.degeneracies[index] != multiplicity for index in indices):
                raise ValueError(
                    "each degeneracy must equal its residue-class multiplicity"
                )

    def _residue(self, representative: CellRepresentative3D) -> CellRepresentative3D:
        """Return one representative's componentwise modulo-mesh residue."""
        return (
            representative[0] % self.mesh_shape[0],
            representative[1] % self.mesh_shape[1],
            representative[2] % self.mesh_shape[2],
        )

    @property
    def representative_count(self) -> int:
        """Return the ordered Wigner--Seitz representative count."""
        return len(self.representatives)


@dataclass(frozen=True, slots=True, eq=False)
class WignerSeitzRepresentedOperator3D:
    """Retain one identified operator on a Wigner--Seitz block inventory."""

    identifier: str
    role: WannierOperatorRole
    source_binding_identifier: str
    frame_identifier: str
    energy_reference: str
    inventory: WignerSeitzInterpolationInventory3D
    blocks: tuple[ComplexMatrixQuantity, ...]

    def __post_init__(self) -> None:
        """Validate operator identity, inventory correlation, blocks, and units."""
        self._check_args_identity()
        self._check_args_blocks()

    def _check_args_identity(self) -> None:
        """Validate explicit identities, role, and source correlation."""
        for name, value in (
            ("identifier", self.identifier),
            ("source_binding_identifier", self.source_binding_identifier),
            ("frame_identifier", self.frame_identifier),
            ("energy_reference", self.energy_reference),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a string")
            if not value:
                raise ValueError(f"{name} must be nonempty")
        if type(self.role) is not WannierOperatorRole:
            raise TypeError("role must be WannierOperatorRole")
        if type(self.inventory) is not WignerSeitzInterpolationInventory3D:
            raise TypeError("inventory must be WignerSeitzInterpolationInventory3D")
        if self.source_binding_identifier != self.inventory.source_binding_identifier:
            raise ValueError("operator and inventory source bindings must agree")

    def _check_args_blocks(self) -> None:
        """Validate one homogeneous square physical-energy block per representative."""
        if type(self.blocks) is not tuple:
            raise TypeError("blocks must be a tuple")
        if len(self.blocks) != self.inventory.representative_count:
            raise ValueError("one block is required per Wigner--Seitz representative")
        if any(type(block) is not ComplexMatrixQuantity for block in self.blocks):
            raise TypeError("blocks must contain ComplexMatrixQuantity values")
        first = self.blocks[0]
        dimension = first.magnitude.shape[0]
        if dimension == 0 or first.magnitude.shape != (dimension, dimension):
            raise ValueError("blocks must be nonempty square matrices")
        if not isinstance(first.unit, PhysicalUnit):
            raise ValueError("blocks must use a physical energy unit")
        try:
            MODEL_SYSTEM_UNIT_CONVERTER.conversion_factor(
                first.unit, PhysicalUnit("joule")
            )
        except ValueError as error:
            raise ValueError("blocks must use a physical energy unit") from error
        for block in self.blocks:
            if block.magnitude.shape != (dimension, dimension):
                raise ValueError("all blocks must have one square shape")
            if block.unit != first.unit:
                raise ValueError("all blocks must use the same energy unit")

    @property
    def matrix_dimension(self) -> int:
        """Return the represented matrix dimension."""
        return int(self.blocks[0].magnitude.shape[0])


class WannierRepresentedOperatorWignerSeitzConstructor3D:
    """Lift canonical finite-mesh blocks onto one Wigner--Seitz inventory."""

    __slots__ = ()

    def execute(
        self,
        operator: WannierRepresentedOperatorMesh3D,
        inventory: WignerSeitzInterpolationInventory3D,
    ) -> WignerSeitzRepresentedOperator3D:
        """Return an identified Wigner--Seitz operator without native parsing."""
        if type(operator) is not WannierRepresentedOperatorMesh3D:
            raise TypeError("operator must be WannierRepresentedOperatorMesh3D")
        if type(inventory) is not WignerSeitzInterpolationInventory3D:
            raise TypeError("inventory must be WignerSeitzInterpolationInventory3D")
        if operator.source_binding_identifier != inventory.source_binding_identifier:
            raise ValueError("operator and inventory source bindings must agree")
        if operator.mesh_shape != inventory.mesh_shape:
            raise ValueError("operator and inventory mesh shapes must agree")
        blocks = WannierKineticWignerSeitzInterpolator3D._lifted_blocks(
            operator, inventory
        )
        unit = operator.lattice_blocks[0].unit
        return WignerSeitzRepresentedOperator3D(
            identifier=operator.identifier,
            role=operator.role,
            source_binding_identifier=operator.source_binding_identifier,
            frame_identifier=operator.frame_identifier,
            energy_reference=operator.energy_reference,
            inventory=inventory,
            blocks=tuple(ComplexMatrixQuantity(block, unit) for block in blocks),
        )


@dataclass(frozen=True, slots=True, eq=False)
class WignerSeitzOperatorInterpolationRequest3D:
    """Declare reduced reciprocal coordinates for one Wigner--Seitz operator."""

    operator: WignerSeitzRepresentedOperator3D
    fractional_kpoints: MatrixQuantity
    hermiticity_absolute_tolerance: float

    def __post_init__(self) -> None:
        """Validate the operator, coordinates, and output-energy-unit tolerance."""
        if type(self.operator) is not WignerSeitzRepresentedOperator3D:
            raise TypeError("operator must be WignerSeitzRepresentedOperator3D")
        if type(self.fractional_kpoints) is not MatrixQuantity:
            raise TypeError("fractional_kpoints must be MatrixQuantity")
        if not isinstance(self.fractional_kpoints.unit, Unitless):
            raise ValueError("fractional_kpoints must be unitless")
        if self.fractional_kpoints.magnitude.shape[
            0
        ] == 0 or self.fractional_kpoints.magnitude.shape[1:] != (3,):
            raise ValueError(
                "fractional_kpoints must contain one or more reduced three-vectors"
            )
        if type(self.hermiticity_absolute_tolerance) is not float:
            raise TypeError("hermiticity_absolute_tolerance must be a built-in float")
        if (
            not np.isfinite(self.hermiticity_absolute_tolerance)
            or self.hermiticity_absolute_tolerance < 0.0
        ):
            raise ValueError(
                "hermiticity_absolute_tolerance must be finite and nonnegative"
            )

    @property
    def sample_count(self) -> int:
        """Return the requested reciprocal-coordinate count."""
        return int(self.fractional_kpoints.magnitude.shape[0])


@dataclass(frozen=True, slots=True, eq=False)
class WignerSeitzOperatorInterpolationResult3D:
    """Retain one interpolated operator family and Hermiticity diagnostic."""

    request: WignerSeitzOperatorInterpolationRequest3D
    matrices: tuple[ComplexMatrixQuantity, ...]
    hermiticity_maximum_frobenius: float

    def __post_init__(self) -> None:
        """Validate result structure, values, and Hermiticity diagnostic."""
        if type(self.request) is not WignerSeitzOperatorInterpolationRequest3D:
            raise TypeError("request must be WignerSeitzOperatorInterpolationRequest3D")
        if type(self.matrices) is not tuple:
            raise TypeError("matrices must be a tuple")
        if len(self.matrices) != self.request.sample_count:
            raise ValueError("matrix count must equal requested point count")
        unit = self.request.operator.blocks[0].unit
        dimension = self.request.operator.matrix_dimension
        for matrix in self.matrices:
            if type(matrix) is not ComplexMatrixQuantity:
                raise TypeError("matrices must contain ComplexMatrixQuantity values")
            if matrix.magnitude.shape != (dimension, dimension):
                raise ValueError("interpolated matrices have the wrong shape")
            if matrix.unit != unit:
                raise ValueError("interpolated matrices have the wrong unit")
        if type(self.hermiticity_maximum_frobenius) is not float:
            raise TypeError("hermiticity_maximum_frobenius must be a built-in float")
        if (
            not np.isfinite(self.hermiticity_maximum_frobenius)
            or self.hermiticity_maximum_frobenius < 0.0
        ):
            raise ValueError(
                "hermiticity_maximum_frobenius must be finite and nonnegative"
            )
        expected, defect = WignerSeitzOperatorInterpolator3D._evaluate(self.request)
        if any(
            not np.array_equal(matrix.magnitude, value)
            for matrix, value in zip(self.matrices, expected, strict=True)
        ):
            raise ValueError("interpolated matrices do not match the request")
        if self.hermiticity_maximum_frobenius != defect:
            raise ValueError("Hermiticity diagnostic does not match the matrices")

    @property
    def passes(self) -> bool:
        """Return whether the maximum Hermiticity defect passes."""
        return (
            self.hermiticity_maximum_frobenius
            <= self.request.hermiticity_absolute_tolerance
        )


class WignerSeitzOperatorInterpolator3D:
    """Evaluate one identified Wigner--Seitz represented operator."""

    __slots__ = ()

    def execute(
        self, request: WignerSeitzOperatorInterpolationRequest3D
    ) -> WignerSeitzOperatorInterpolationResult3D:
        """Return positive-phase, degeneracy-divided interpolation values."""
        if type(request) is not WignerSeitzOperatorInterpolationRequest3D:
            raise TypeError("request must be WignerSeitzOperatorInterpolationRequest3D")
        values, defect = self._evaluate(request)
        unit = request.operator.blocks[0].unit
        return WignerSeitzOperatorInterpolationResult3D(
            request=request,
            matrices=tuple(ComplexMatrixQuantity(value, unit) for value in values),
            hermiticity_maximum_frobenius=defect,
        )

    @staticmethod
    def _evaluate(
        request: WignerSeitzOperatorInterpolationRequest3D,
    ) -> tuple[tuple[ComplexArray, ...], float]:
        """Evaluate matrices and Hermiticity without constructing the result."""
        representatives = np.asarray(
            request.operator.inventory.representatives, dtype=np.float64
        )
        degeneracies = np.asarray(
            request.operator.inventory.degeneracies, dtype=np.float64
        )
        blocks = np.asarray(
            [block.magnitude for block in request.operator.blocks],
            dtype=np.complex128,
        )
        phases = np.exp(
            2j * np.pi * request.fractional_kpoints.magnitude @ representatives.T
        )
        values_array = np.einsum(
            "kr,rij->kij",
            phases,
            blocks / degeneracies[:, np.newaxis, np.newaxis],
            optimize=True,
        )
        values = tuple(values_array)
        defect = float(max(np.linalg.norm(value - value.conj().T) for value in values))
        return values, defect


@dataclass(frozen=True, slots=True, eq=False)
class WannierKineticWignerSeitzInterpolationRequest3D:
    """Declare same-frame interpolation points for one kinetic decomposition."""

    decomposition: WannierKineticDecompositionResult
    inventory: WignerSeitzInterpolationInventory3D
    fractional_kpoints: MatrixQuantity
    diagnostic_absolute_tolerance: float

    def __post_init__(self) -> None:
        """Validate source correlation, coordinates, and diagnostic tolerance."""
        self._check_args_sources()
        self._check_args_coordinates()
        self._check_args_tolerance()

    def _check_args_sources(self) -> None:
        """Require exact decomposition and inventory types with matching identities."""
        if type(self.decomposition) is not WannierKineticDecompositionResult:
            raise TypeError("decomposition must be WannierKineticDecompositionResult")
        if type(self.inventory) is not WignerSeitzInterpolationInventory3D:
            raise TypeError("inventory must be WignerSeitzInterpolationInventory3D")
        request = self.decomposition.request
        if self.inventory.source_binding_identifier != (
            request.source_binding_identifier
        ):
            raise ValueError("inventory and decomposition source bindings must agree")
        if self.inventory.mesh_shape != request.mesh_shape:
            raise ValueError("inventory and decomposition mesh shapes must agree")

    def _check_args_coordinates(self) -> None:
        """Validate one or more dimensionless reduced reciprocal coordinates."""
        if type(self.fractional_kpoints) is not MatrixQuantity:
            raise TypeError("fractional_kpoints must be MatrixQuantity")
        if not isinstance(self.fractional_kpoints.unit, Unitless):
            raise ValueError("fractional_kpoints must be unitless")
        if (
            self.fractional_kpoints.magnitude.ndim != 2
            or self.fractional_kpoints.magnitude.shape[1] != 3
            or self.fractional_kpoints.magnitude.shape[0] == 0
        ):
            raise ValueError(
                "fractional_kpoints must contain one or more reduced three-vectors"
            )

    def _check_args_tolerance(self) -> None:
        """Validate the output-energy-unit diagnostic tolerance."""
        if type(self.diagnostic_absolute_tolerance) is not float:
            raise TypeError("diagnostic_absolute_tolerance must be a built-in float")
        if (
            not np.isfinite(self.diagnostic_absolute_tolerance)
            or self.diagnostic_absolute_tolerance < 0.0
        ):
            raise ValueError(
                "diagnostic_absolute_tolerance must be finite and nonnegative"
            )

    @property
    def sample_count(self) -> int:
        """Return the requested interpolation-point count."""
        return int(self.fractional_kpoints.magnitude.shape[0])


@dataclass(frozen=True, slots=True)
class WannierKineticWignerSeitzInterpolationDiagnostics:
    """Retain same-frame interpolation defects in the output energy unit."""

    hamiltonian_hermiticity_maximum_frobenius: float
    kinetic_hermiticity_maximum_frobenius: float
    nonkinetic_remainder_hermiticity_maximum_frobenius: float
    decomposition_maximum_frobenius: float
    absolute_tolerance: float

    def __post_init__(self) -> None:
        """Validate finite nonnegative defects and tolerance."""
        for name, value in (
            (
                "hamiltonian_hermiticity_maximum_frobenius",
                self.hamiltonian_hermiticity_maximum_frobenius,
            ),
            (
                "kinetic_hermiticity_maximum_frobenius",
                self.kinetic_hermiticity_maximum_frobenius,
            ),
            (
                "nonkinetic_remainder_hermiticity_maximum_frobenius",
                self.nonkinetic_remainder_hermiticity_maximum_frobenius,
            ),
            (
                "decomposition_maximum_frobenius",
                self.decomposition_maximum_frobenius,
            ),
            ("absolute_tolerance", self.absolute_tolerance),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not np.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")

    @property
    def passes(self) -> bool:
        """Return whether Hermiticity and decomposition defects pass."""
        return (
            max(
                self.hamiltonian_hermiticity_maximum_frobenius,
                self.kinetic_hermiticity_maximum_frobenius,
                self.nonkinetic_remainder_hermiticity_maximum_frobenius,
                self.decomposition_maximum_frobenius,
            )
            <= self.absolute_tolerance
        )


@dataclass(frozen=True, slots=True, eq=False)
class WannierKineticWignerSeitzInterpolationResult3D:
    """Retain three same-frame interpolated operator families and diagnostics."""

    request: WannierKineticWignerSeitzInterpolationRequest3D
    hamiltonian_matrices: tuple[ComplexMatrixQuantity, ...]
    kinetic_matrices: tuple[ComplexMatrixQuantity, ...]
    nonkinetic_remainder_matrices: tuple[ComplexMatrixQuantity, ...]
    diagnostics: WannierKineticWignerSeitzInterpolationDiagnostics

    def __post_init__(self) -> None:
        """Validate result shapes, units, construction, and diagnostics."""
        self._check_args_types_and_matrices()
        self._check_args_construction_and_diagnostics()

    def _check_args_types_and_matrices(self) -> None:
        """Validate exact component types and homogeneous matrix families."""
        if type(self.request) is not WannierKineticWignerSeitzInterpolationRequest3D:
            raise TypeError(
                "request must be WannierKineticWignerSeitzInterpolationRequest3D"
            )
        if type(self.diagnostics) is not (
            WannierKineticWignerSeitzInterpolationDiagnostics
        ):
            raise TypeError(
                "diagnostics must be WannierKineticWignerSeitzInterpolationDiagnostics"
            )
        dimension = self.request.decomposition.request.wannier_count
        unit = self.request.decomposition.request.output_energy_unit
        for name, matrices in (
            ("hamiltonian_matrices", self.hamiltonian_matrices),
            ("kinetic_matrices", self.kinetic_matrices),
            (
                "nonkinetic_remainder_matrices",
                self.nonkinetic_remainder_matrices,
            ),
        ):
            if type(matrices) is not tuple:
                raise TypeError(f"{name} must be a tuple")
            if len(matrices) != self.request.sample_count:
                raise ValueError(f"{name} count must equal requested point count")
            for matrix in matrices:
                if type(matrix) is not ComplexMatrixQuantity:
                    raise TypeError(f"{name} must contain ComplexMatrixQuantity values")
                if matrix.magnitude.shape != (dimension, dimension):
                    raise ValueError(f"{name} matrices have the wrong shape")
                if matrix.unit != unit:
                    raise ValueError(f"{name} matrices have the wrong energy unit")

    def _check_args_construction_and_diagnostics(self) -> None:
        """Require matrices and diagnostics to reproduce the declared request."""
        hamiltonian, kinetic, remainder, diagnostics = (
            WannierKineticWignerSeitzInterpolator3D._evaluate(self.request)
        )
        for name, actual, expected in (
            ("hamiltonian", self.hamiltonian_matrices, hamiltonian),
            ("kinetic", self.kinetic_matrices, kinetic),
            (
                "nonkinetic remainder",
                self.nonkinetic_remainder_matrices,
                remainder,
            ),
        ):
            if any(
                not np.array_equal(matrix.magnitude, value)
                for matrix, value in zip(actual, expected, strict=True)
            ):
                raise ValueError(f"{name} matrices do not match the request")
        if self.diagnostics != diagnostics:
            raise ValueError("interpolation diagnostics do not match the matrices")


class WannierKineticWignerSeitzInterpolator3D:
    r"""Interpolate one same-frame ``H^W = T^W + R^W`` decomposition.

    Canonical finite-mesh blocks are lifted by modulo-mesh residue to the explicit
    Wigner--Seitz inventory and evaluated with
    :math:`\exp(2\pi i\mathbf q\cdot\mathbf R)/d_{\mathbf R}`.
    """

    __slots__ = ()

    def execute(
        self, request: WannierKineticWignerSeitzInterpolationRequest3D
    ) -> WannierKineticWignerSeitzInterpolationResult3D:
        """Return three interpolated matrix families and numerical diagnostics."""
        if type(request) is not WannierKineticWignerSeitzInterpolationRequest3D:
            raise TypeError(
                "request must be WannierKineticWignerSeitzInterpolationRequest3D"
            )
        hamiltonian, kinetic, remainder, diagnostics = self._evaluate(request)
        unit = request.decomposition.request.output_energy_unit
        return WannierKineticWignerSeitzInterpolationResult3D(
            request=request,
            hamiltonian_matrices=tuple(
                ComplexMatrixQuantity(matrix, unit) for matrix in hamiltonian
            ),
            kinetic_matrices=tuple(
                ComplexMatrixQuantity(matrix, unit) for matrix in kinetic
            ),
            nonkinetic_remainder_matrices=tuple(
                ComplexMatrixQuantity(matrix, unit) for matrix in remainder
            ),
            diagnostics=diagnostics,
        )

    @classmethod
    def _evaluate(
        cls, request: WannierKineticWignerSeitzInterpolationRequest3D
    ) -> tuple[
        tuple[ComplexArray, ...],
        tuple[ComplexArray, ...],
        tuple[ComplexArray, ...],
        WannierKineticWignerSeitzInterpolationDiagnostics,
    ]:
        """Evaluate all three matrix families without constructing the result."""
        decomposition = request.decomposition
        hamiltonian = cls._interpolate_operator(
            decomposition.hamiltonian,
            request.inventory,
            request.fractional_kpoints.magnitude,
        )
        kinetic = cls._interpolate_operator(
            decomposition.kinetic,
            request.inventory,
            request.fractional_kpoints.magnitude,
        )
        remainder = cls._interpolate_operator(
            decomposition.nonkinetic_remainder,
            request.inventory,
            request.fractional_kpoints.magnitude,
        )
        diagnostics = WannierKineticWignerSeitzInterpolationDiagnostics(
            hamiltonian_hermiticity_maximum_frobenius=cls._hermiticity_defect(
                hamiltonian
            ),
            kinetic_hermiticity_maximum_frobenius=cls._hermiticity_defect(kinetic),
            nonkinetic_remainder_hermiticity_maximum_frobenius=(
                cls._hermiticity_defect(remainder)
            ),
            decomposition_maximum_frobenius=float(
                max(
                    np.linalg.norm(h_value - t_value - r_value)
                    for h_value, t_value, r_value in zip(
                        hamiltonian, kinetic, remainder, strict=True
                    )
                )
            ),
            absolute_tolerance=request.diagnostic_absolute_tolerance,
        )
        return hamiltonian, kinetic, remainder, diagnostics

    @classmethod
    def _interpolate_operator(
        cls,
        operator: WannierRepresentedOperatorMesh3D,
        inventory: WignerSeitzInterpolationInventory3D,
        fractional_kpoints: npt.NDArray[np.float64],
    ) -> tuple[ComplexArray, ...]:
        """Lift canonical blocks by residue and apply positive-phase interpolation."""
        blocks = cls._lifted_blocks(operator, inventory)
        representatives = np.asarray(inventory.representatives, dtype=np.float64)
        degeneracies = np.asarray(inventory.degeneracies, dtype=np.float64)
        phases = np.exp(2j * np.pi * fractional_kpoints @ representatives.T)
        weighted = blocks / degeneracies[:, np.newaxis, np.newaxis]
        values = np.einsum("kr,rij->kij", phases, weighted, optimize=True)
        return tuple(values)

    @staticmethod
    def _lifted_blocks(
        operator: WannierRepresentedOperatorMesh3D,
        inventory: WignerSeitzInterpolationInventory3D,
    ) -> npt.NDArray[np.complex128]:
        """Return canonical blocks repeated on matching modulo-mesh residues."""
        canonical = {
            inventory._residue(representative): block.magnitude
            for representative, block in zip(
                operator.representatives, operator.lattice_blocks, strict=True
            )
        }
        if len(canonical) != int(np.prod(inventory.mesh_shape)):
            raise ValueError(
                "canonical operator representatives do not cover the source mesh"
            )
        return np.asarray(
            [
                canonical[inventory._residue(value)]
                for value in inventory.representatives
            ],
            dtype=np.complex128,
        )

    @staticmethod
    def _hermiticity_defect(matrices: tuple[ComplexArray, ...]) -> float:
        """Return the largest matrix anti-Hermitian Frobenius norm."""
        return float(
            max(np.linalg.norm(matrix - matrix.conj().T) for matrix in matrices)
        )


@dataclass(frozen=True, slots=True, eq=False)
class WannierRepresentedOperatorCartesianDerivativeRequest3D:
    """Declare one Cartesian derivative evaluation of a represented operator."""

    operator: WannierRepresentedOperatorMesh3D
    inventory: WignerSeitzInterpolationInventory3D
    fractional_kpoint: VectorQuantity

    def __post_init__(self) -> None:
        """Validate operator correlation and one reduced reciprocal coordinate."""
        self._check_args_sources()
        self._check_args_coordinate()

    def _check_args_sources(self) -> None:
        """Require matching exact operator and inventory identities and mesh shapes."""
        if type(self.operator) is not WannierRepresentedOperatorMesh3D:
            raise TypeError("operator must be WannierRepresentedOperatorMesh3D")
        if type(self.inventory) is not WignerSeitzInterpolationInventory3D:
            raise TypeError("inventory must be WignerSeitzInterpolationInventory3D")
        if self.operator.source_binding_identifier != (
            self.inventory.source_binding_identifier
        ):
            raise ValueError("inventory and operator source bindings must agree")
        if self.operator.mesh_shape != self.inventory.mesh_shape:
            raise ValueError("inventory and operator mesh shapes must agree")

    def _check_args_coordinate(self) -> None:
        """Validate one dimensionless reduced reciprocal three-vector."""
        if type(self.fractional_kpoint) is not VectorQuantity:
            raise TypeError("fractional_kpoint must be VectorQuantity")
        if not isinstance(self.fractional_kpoint.unit, Unitless):
            raise ValueError("fractional_kpoint must be unitless")
        if self.fractional_kpoint.magnitude.shape != (3,):
            raise ValueError("fractional_kpoint must be a reduced three-vector")


@dataclass(frozen=True, slots=True)
class WannierRepresentedOperatorCartesianDerivativeDiagnostics3D:
    """Retain derivative Hermiticity and Hessian-symmetry defects with units."""

    value_hermiticity_frobenius: ScalarQuantity
    gradient_hermiticity_maximum_frobenius: ScalarQuantity
    hessian_hermiticity_maximum_frobenius: ScalarQuantity
    hessian_cartesian_symmetry_maximum_frobenius: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate exact scalar-quantity types and nonnegative defects."""
        for name, value in (
            ("value_hermiticity_frobenius", self.value_hermiticity_frobenius),
            (
                "gradient_hermiticity_maximum_frobenius",
                self.gradient_hermiticity_maximum_frobenius,
            ),
            (
                "hessian_hermiticity_maximum_frobenius",
                self.hessian_hermiticity_maximum_frobenius,
            ),
            (
                "hessian_cartesian_symmetry_maximum_frobenius",
                self.hessian_cartesian_symmetry_maximum_frobenius,
            ),
        ):
            if type(value) is not ScalarQuantity:
                raise TypeError(f"{name} must be ScalarQuantity")
            if value.magnitude < 0.0:
                raise ValueError(f"{name} must be nonnegative")


@dataclass(frozen=True, slots=True, eq=False)
class WannierRepresentedOperatorCartesianDerivativeResult3D:
    """Retain an operator value, Cartesian gradient, Hessian, and diagnostics."""

    request: WannierRepresentedOperatorCartesianDerivativeRequest3D
    value: ComplexMatrixQuantity
    gradient: tuple[ComplexMatrixQuantity, ...]
    hessian: tuple[tuple[ComplexMatrixQuantity, ...], ...]
    diagnostics: WannierRepresentedOperatorCartesianDerivativeDiagnostics3D

    def __post_init__(self) -> None:
        """Validate derivative tensor structure, units, values, and diagnostics."""
        self._check_args_types_and_tensors()
        self._check_args_construction_and_diagnostics()

    def _check_args_types_and_tensors(self) -> None:
        """Validate exact result types, tensor dimensions, matrix shapes, and units."""
        if type(self.request) is not (
            WannierRepresentedOperatorCartesianDerivativeRequest3D
        ):
            raise TypeError(
                "request must be WannierRepresentedOperatorCartesianDerivativeRequest3D"
            )
        if type(self.value) is not ComplexMatrixQuantity:
            raise TypeError("value must be ComplexMatrixQuantity")
        if type(self.gradient) is not tuple or len(self.gradient) != 3:
            raise TypeError("gradient must contain three matrices")
        if (
            type(self.hessian) is not tuple
            or len(self.hessian) != 3
            or any(type(row) is not tuple or len(row) != 3 for row in self.hessian)
        ):
            raise TypeError("hessian must contain three rows of three matrices")
        if type(self.diagnostics) is not (
            WannierRepresentedOperatorCartesianDerivativeDiagnostics3D
        ):
            raise TypeError(
                "diagnostics must be "
                "WannierRepresentedOperatorCartesianDerivativeDiagnostics3D"
            )
        dimension = self.request.operator.wannier_count
        expected_units = (
            self.request.operator.lattice_blocks[0].unit,
            WannierRepresentedOperatorCartesianDerivativeConstructor3D._gradient_unit(
                self.request
            ),
            WannierRepresentedOperatorCartesianDerivativeConstructor3D._hessian_unit(
                self.request
            ),
        )
        matrix_groups = (
            ("value", (self.value,), expected_units[0]),
            ("gradient", self.gradient, expected_units[1]),
            (
                "hessian",
                tuple(matrix for row in self.hessian for matrix in row),
                expected_units[2],
            ),
        )
        for name, matrices, unit in matrix_groups:
            for matrix in matrices:
                if type(matrix) is not ComplexMatrixQuantity:
                    raise TypeError(f"{name} must contain ComplexMatrixQuantity values")
                if matrix.magnitude.shape != (dimension, dimension):
                    raise ValueError(f"{name} matrices have the wrong shape")
                if matrix.unit != unit:
                    raise ValueError(f"{name} matrices have the wrong unit")
        diagnostic_units = (
            self.diagnostics.value_hermiticity_frobenius.unit,
            self.diagnostics.gradient_hermiticity_maximum_frobenius.unit,
            self.diagnostics.hessian_hermiticity_maximum_frobenius.unit,
            self.diagnostics.hessian_cartesian_symmetry_maximum_frobenius.unit,
        )
        if diagnostic_units != (
            expected_units[0],
            expected_units[1],
            expected_units[2],
            expected_units[2],
        ):
            raise ValueError("derivative diagnostic units do not match tensor units")

    def _check_args_construction_and_diagnostics(self) -> None:
        """Require every tensor value and diagnostic to reproduce the request."""
        value, gradient, hessian, diagnostics = (
            WannierRepresentedOperatorCartesianDerivativeConstructor3D._evaluate(
                self.request
            )
        )
        if not np.array_equal(self.value.magnitude, value):
            raise ValueError("value does not match the derivative request")
        if any(
            not np.array_equal(matrix.magnitude, expected)
            for matrix, expected in zip(self.gradient, gradient, strict=True)
        ):
            raise ValueError("gradient does not match the derivative request")
        if any(
            not np.array_equal(matrix.magnitude, expected)
            for matrix_row, expected_row in zip(self.hessian, hessian, strict=True)
            for matrix, expected in zip(matrix_row, expected_row, strict=True)
        ):
            raise ValueError("hessian does not match the derivative request")
        if self.diagnostics != diagnostics:
            raise ValueError("derivative diagnostics do not match the tensors")


class WannierRepresentedOperatorCartesianDerivativeConstructor3D:
    r"""Construct analytic Cartesian derivatives of one represented operator.

    For Cartesian representatives :math:`\mathbf r_s=\mathbf R_s A`, the gradient
    and Hessian apply factors :math:`i r_{s,a}` and
    :math:`-r_{s,a}r_{s,b}` to the positive-phase Wigner--Seitz sum.
    """

    __slots__ = ()

    def execute(
        self, request: WannierRepresentedOperatorCartesianDerivativeRequest3D
    ) -> WannierRepresentedOperatorCartesianDerivativeResult3D:
        """Return the value, Cartesian derivative tensors, and diagnostics."""
        if type(request) is not (
            WannierRepresentedOperatorCartesianDerivativeRequest3D
        ):
            raise TypeError(
                "request must be WannierRepresentedOperatorCartesianDerivativeRequest3D"
            )
        value, gradient, hessian, diagnostics = self._evaluate(request)
        energy_unit = request.operator.lattice_blocks[0].unit
        gradient_unit = self._gradient_unit(request)
        hessian_unit = self._hessian_unit(request)
        return WannierRepresentedOperatorCartesianDerivativeResult3D(
            request=request,
            value=ComplexMatrixQuantity(value, energy_unit),
            gradient=tuple(
                ComplexMatrixQuantity(matrix, gradient_unit) for matrix in gradient
            ),
            hessian=tuple(
                tuple(ComplexMatrixQuantity(matrix, hessian_unit) for matrix in row)
                for row in hessian
            ),
            diagnostics=diagnostics,
        )

    @classmethod
    def _evaluate(
        cls, request: WannierRepresentedOperatorCartesianDerivativeRequest3D
    ) -> tuple[
        ComplexArray,
        tuple[ComplexArray, ...],
        tuple[tuple[ComplexArray, ...], ...],
        WannierRepresentedOperatorCartesianDerivativeDiagnostics3D,
    ]:
        """Evaluate derivative arrays without constructing the result record."""
        inventory = request.inventory
        blocks = WannierKineticWignerSeitzInterpolator3D._lifted_blocks(
            request.operator, inventory
        )
        representatives = np.asarray(inventory.representatives, dtype=np.float64)
        cartesian = representatives @ inventory.direct_lattice.magnitude
        degeneracies = np.asarray(inventory.degeneracies, dtype=np.float64)
        phases = np.exp(
            2j * np.pi * representatives @ request.fractional_kpoint.magnitude
        )
        weighted = (
            phases[:, np.newaxis, np.newaxis]
            * blocks
            / degeneracies[:, np.newaxis, np.newaxis]
        )
        value = np.sum(weighted, axis=0)
        gradient_array = np.einsum(
            "ra,rij->aij", 1j * cartesian, weighted, optimize=True
        )
        hessian_array = np.einsum(
            "ra,rb,rij->abij", -cartesian, cartesian, weighted, optimize=True
        )
        gradient = tuple(gradient_array)
        hessian = tuple(tuple(row) for row in hessian_array)
        energy_unit = request.operator.lattice_blocks[0].unit
        gradient_unit = cls._gradient_unit(request)
        hessian_unit = cls._hessian_unit(request)
        diagnostics = WannierRepresentedOperatorCartesianDerivativeDiagnostics3D(
            value_hermiticity_frobenius=ScalarQuantity(
                float(np.linalg.norm(value - value.conj().T)), energy_unit
            ),
            gradient_hermiticity_maximum_frobenius=ScalarQuantity(
                cls._hermiticity_defect(gradient), gradient_unit
            ),
            hessian_hermiticity_maximum_frobenius=ScalarQuantity(
                cls._hermiticity_defect(
                    tuple(matrix for row in hessian for matrix in row)
                ),
                hessian_unit,
            ),
            hessian_cartesian_symmetry_maximum_frobenius=ScalarQuantity(
                float(
                    max(
                        np.linalg.norm(hessian[first][second] - hessian[second][first])
                        for first in range(3)
                        for second in range(3)
                    )
                ),
                hessian_unit,
            ),
        )
        return value, gradient, hessian, diagnostics

    @staticmethod
    def _gradient_unit(
        request: WannierRepresentedOperatorCartesianDerivativeRequest3D,
    ) -> PhysicalUnit:
        """Return the explicit energy-times-length gradient unit."""
        energy = request.operator.lattice_blocks[0].unit
        length = request.inventory.direct_lattice.unit
        if not isinstance(energy, PhysicalUnit):
            raise ValueError("represented operator must use a physical energy unit")
        if not isinstance(length, PhysicalUnit):
            raise ValueError("direct lattice must use a physical length unit")
        return PhysicalUnit(f"({energy.expression}) * ({length.expression})")

    @staticmethod
    def _hessian_unit(
        request: WannierRepresentedOperatorCartesianDerivativeRequest3D,
    ) -> PhysicalUnit:
        """Return the explicit energy-times-length-squared Hessian unit."""
        energy = request.operator.lattice_blocks[0].unit
        length = request.inventory.direct_lattice.unit
        if not isinstance(energy, PhysicalUnit):
            raise ValueError("represented operator must use a physical energy unit")
        if not isinstance(length, PhysicalUnit):
            raise ValueError("direct lattice must use a physical length unit")
        return PhysicalUnit(f"({energy.expression}) * ({length.expression}) ** 2")

    @staticmethod
    def _hermiticity_defect(matrices: tuple[ComplexArray, ...]) -> float:
        """Return the largest matrix anti-Hermitian Frobenius norm."""
        return float(
            max(np.linalg.norm(matrix - matrix.conj().T) for matrix in matrices)
        )


__all__ = [
    "WannierKineticWignerSeitzInterpolationDiagnostics",
    "WannierKineticWignerSeitzInterpolationRequest3D",
    "WannierKineticWignerSeitzInterpolationResult3D",
    "WannierKineticWignerSeitzInterpolator3D",
    "WannierRepresentedOperatorCartesianDerivativeConstructor3D",
    "WannierRepresentedOperatorCartesianDerivativeDiagnostics3D",
    "WannierRepresentedOperatorCartesianDerivativeRequest3D",
    "WannierRepresentedOperatorCartesianDerivativeResult3D",
    "WannierRepresentedOperatorWignerSeitzConstructor3D",
    "WignerSeitzInterpolationInventory3D",
    "WignerSeitzOperatorInterpolationRequest3D",
    "WignerSeitzOperatorInterpolationResult3D",
    "WignerSeitzOperatorInterpolator3D",
    "WignerSeitzRepresentedOperator3D",
]
