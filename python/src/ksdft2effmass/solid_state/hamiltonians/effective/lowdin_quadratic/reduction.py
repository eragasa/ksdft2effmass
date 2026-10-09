"""Finite selected-space Löwdin quadratic effective Hamiltonians.

The name follows Per-Olov Löwdin, "A Note on the Quantum-Mechanical Perturbation
Theory," *The Journal of Chemical Physics* 19(11), 1396--1401 (1951),
https://doi.org/10.1063/1.1748067. The package and project specification record the
citation provenance and the narrower claims established by this implementation.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ....wannier_kinetic import WannierOperatorRole
from ....wignerseitz.interpolation import (
    WannierRepresentedOperatorCartesianDerivativeResult3D,
)
from .diagnostics import (
    antihermitian_maximum_frobenius,
    covariance_maximum_frobenius,
    maximum_frobenius,
)

type ComplexArray = npt.NDArray[np.complex128]
type RealArray = npt.NDArray[np.float64]


def _hermitian_part(matrix: ComplexArray) -> ComplexArray:
    """Return the Hermitian part of one finite matrix."""
    return 0.5 * (matrix + matrix.conj().T)


def _vector_array(tensor: tuple[ComplexMatrixQuantity, ...]) -> ComplexArray:
    """Return one three-component derivative array."""
    return np.asarray([matrix.magnitude for matrix in tensor])


def _matrix_array(
    tensor: tuple[tuple[ComplexMatrixQuantity, ...], ...],
) -> ComplexArray:
    """Return one three-by-three derivative array."""
    return np.asarray([[matrix.magnitude for matrix in row] for row in tensor])


@dataclass(frozen=True, slots=True, eq=False)
class WannierKineticLowdinQuadraticReductionRequest3D:
    """Declare one explicit degenerate-subspace quadratic reduction.

    Parameters
    ----------
    hamiltonian_derivatives, kinetic_derivatives, nonkinetic_remainder_derivatives
        Same-frame Cartesian derivative results at one reduced reciprocal point.
    selected_eigenvalue_indices
        Strictly increasing ordered Hamiltonian eigenvalue indices defining the
        selected eigenspace.
    reference_energy
        Explicit Löwdin reference energy.
    degeneracy_absolute_tolerance
        Energy tolerance that must contain exactly the selected eigenvalues.
    hamiltonian_hermiticity_absolute_tolerance
        Maximum accepted anti-Hermitian Frobenius defect of the Hamiltonian value.
        An accepted value is projected to its Hermitian part before eigenspace
        selection and direct value projection; the correction is retained as a
        diagnostic.
    covariance_probe_gauge
        Explicit unitary selected-space basis change used for covariance diagnostics.
    frame_absolute_tolerance
        Absolute Frobenius tolerance for covariance-probe unitarity.
    """

    hamiltonian_derivatives: WannierRepresentedOperatorCartesianDerivativeResult3D
    kinetic_derivatives: WannierRepresentedOperatorCartesianDerivativeResult3D
    nonkinetic_remainder_derivatives: (
        WannierRepresentedOperatorCartesianDerivativeResult3D
    )
    selected_eigenvalue_indices: tuple[int, ...]
    reference_energy: ScalarQuantity
    degeneracy_absolute_tolerance: ScalarQuantity
    hamiltonian_hermiticity_absolute_tolerance: ScalarQuantity
    covariance_probe_gauge: ComplexMatrixQuantity
    frame_absolute_tolerance: float

    def __post_init__(self) -> None:
        """Validate derivative correlation, selection, energy, and gauge contracts."""
        self._check_args_derivatives()
        self._check_args_selection()
        self._check_args_energy_quantities()
        self._check_args_covariance_gauge()

    def _check_args_derivatives(self) -> None:
        """Require exact derivative result types, roles, and shared representation."""
        derivatives = (
            (
                "hamiltonian_derivatives",
                self.hamiltonian_derivatives,
                WannierOperatorRole.HAMILTONIAN,
            ),
            (
                "kinetic_derivatives",
                self.kinetic_derivatives,
                WannierOperatorRole.KINETIC,
            ),
            (
                "nonkinetic_remainder_derivatives",
                self.nonkinetic_remainder_derivatives,
                WannierOperatorRole.NONKINETIC_REMAINDER,
            ),
        )
        for name, derivative, role in derivatives:
            if type(derivative) is not (
                WannierRepresentedOperatorCartesianDerivativeResult3D
            ):
                raise TypeError(
                    f"{name} must be "
                    "WannierRepresentedOperatorCartesianDerivativeResult3D"
                )
            if derivative.request.operator.role is not role:
                raise ValueError(f"{name} has the wrong represented operator role")
        reference = self.hamiltonian_derivatives.request
        for _, derivative, _ in derivatives[1:]:
            request = derivative.request
            if request.inventory is not reference.inventory:
                raise ValueError("derivatives must share one inventory record")
            if request.operator.source_binding_identifier != (
                reference.operator.source_binding_identifier
            ):
                raise ValueError("derivative source bindings must agree")
            if request.operator.frame_identifier != reference.operator.frame_identifier:
                raise ValueError("derivative retained frames must agree")
            if request.operator.energy_reference != (
                reference.operator.energy_reference
            ):
                raise ValueError("derivative energy references must agree")
            if request.operator.mesh_shape != reference.operator.mesh_shape:
                raise ValueError("derivative source meshes must agree")
            if not np.array_equal(
                request.fractional_kpoint.magnitude,
                reference.fractional_kpoint.magnitude,
            ):
                raise ValueError("derivatives must use one reciprocal coordinate")
            if request.operator.wannier_count != reference.operator.wannier_count:
                raise ValueError("derivative matrix dimensions must agree")
        expected_units = (
            self.hamiltonian_derivatives.value.unit,
            self.hamiltonian_derivatives.gradient[0].unit,
            self.hamiltonian_derivatives.hessian[0][0].unit,
        )
        for derivative in (
            self.kinetic_derivatives,
            self.nonkinetic_remainder_derivatives,
        ):
            if (
                derivative.value.unit,
                derivative.gradient[0].unit,
                derivative.hessian[0][0].unit,
            ) != expected_units:
                raise ValueError("derivative tensor units must agree")

    def _check_args_selection(self) -> None:
        """Validate a nonempty proper strictly increasing index selection."""
        if (
            type(self.selected_eigenvalue_indices) is not tuple
            or not self.selected_eigenvalue_indices
        ):
            raise TypeError("selected_eigenvalue_indices must be a nonempty tuple")
        if any(type(index) is not int for index in self.selected_eigenvalue_indices):
            raise TypeError(
                "selected_eigenvalue_indices must contain built-in integers"
            )
        if tuple(sorted(set(self.selected_eigenvalue_indices))) != (
            self.selected_eigenvalue_indices
        ):
            raise ValueError(
                "selected_eigenvalue_indices must be unique and strictly increasing"
            )
        dimension = self.hamiltonian_derivatives.request.operator.wannier_count
        if any(
            index < 0 or index >= dimension
            for index in self.selected_eigenvalue_indices
        ):
            raise ValueError("selected eigenvalue index lies outside the matrix")
        if len(self.selected_eigenvalue_indices) >= dimension:
            raise ValueError("quadratic reduction requires a nonempty complement")

    def _check_args_energy_quantities(self) -> None:
        """Validate explicit reference energy and nonnegative degeneracy tolerance."""
        energy_unit = self.hamiltonian_derivatives.value.unit
        for name, value in (
            ("reference_energy", self.reference_energy),
            ("degeneracy_absolute_tolerance", self.degeneracy_absolute_tolerance),
            (
                "hamiltonian_hermiticity_absolute_tolerance",
                self.hamiltonian_hermiticity_absolute_tolerance,
            ),
        ):
            if type(value) is not ScalarQuantity:
                raise TypeError(f"{name} must be ScalarQuantity")
            if value.unit != energy_unit:
                raise ValueError(f"{name} must use the Hamiltonian energy unit")
        if self.degeneracy_absolute_tolerance.magnitude < 0.0:
            raise ValueError("degeneracy_absolute_tolerance must be nonnegative")
        if self.hamiltonian_hermiticity_absolute_tolerance.magnitude < 0.0:
            raise ValueError(
                "hamiltonian_hermiticity_absolute_tolerance must be nonnegative"
            )

    def _check_args_covariance_gauge(self) -> None:
        """Validate an explicit unitary selected-space covariance probe."""
        if type(self.covariance_probe_gauge) is not ComplexMatrixQuantity:
            raise TypeError("covariance_probe_gauge must be ComplexMatrixQuantity")
        if not isinstance(self.covariance_probe_gauge.unit, Unitless):
            raise ValueError("covariance_probe_gauge must be unitless")
        rank = len(self.selected_eigenvalue_indices)
        if self.covariance_probe_gauge.magnitude.shape != (rank, rank):
            raise ValueError("covariance_probe_gauge has the wrong selected rank")
        if type(self.frame_absolute_tolerance) is not float:
            raise TypeError("frame_absolute_tolerance must be a built-in float")
        if (
            not np.isfinite(self.frame_absolute_tolerance)
            or self.frame_absolute_tolerance < 0.0
        ):
            raise ValueError("frame_absolute_tolerance must be finite and nonnegative")
        gauge = self.covariance_probe_gauge.magnitude
        defect = float(
            np.linalg.norm(gauge.conj().T @ gauge - np.eye(rank, dtype=np.complex128))
        )
        if defect > self.frame_absolute_tolerance:
            raise ValueError("covariance_probe_gauge must be unitary")

    @property
    def selected_rank(self) -> int:
        """Return the explicit selected eigenspace rank."""
        return len(self.selected_eigenvalue_indices)


@dataclass(frozen=True, slots=True)
class WannierKineticLowdinQuadraticReductionDiagnostics3D:
    """Retain unit-carrying closure, Hermiticity, separation, and covariance defects."""

    selected_group_maximum_splitting: ScalarQuantity
    complement_minimum_separation: ScalarQuantity
    hamiltonian_hermitian_projection_correction_frobenius: ScalarQuantity
    value_decomposition_frobenius: ScalarQuantity
    gradient_decomposition_maximum_frobenius: ScalarQuantity
    direct_hessian_decomposition_maximum_frobenius: ScalarQuantity
    remote_partition_decomposition_maximum_frobenius: ScalarQuantity
    effective_quadratic_antihermitian_maximum_frobenius: ScalarQuantity
    basis_covariance_base_maximum_frobenius: ScalarQuantity
    basis_covariance_gradient_maximum_frobenius: ScalarQuantity
    basis_covariance_quadratic_maximum_frobenius: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate exact scalar-quantity types and nonnegative magnitudes."""
        for name in self.__dataclass_fields__:
            value = getattr(self, name)
            if type(value) is not ScalarQuantity:
                raise TypeError(f"{name} must be ScalarQuantity")
            if value.magnitude < 0.0:
                raise ValueError(f"{name} must be nonnegative")


@dataclass(slots=True)
class _LowdinQuadraticArrays3D:
    """Hold one ephemeral Löwdin quadratic reduction before quantity construction."""

    eigenvalues: RealArray
    selected_frame: ComplexArray
    complement_frame: ComplexArray
    resolvent: ComplexArray
    projected_hamiltonian_value: ComplexArray
    projected_kinetic_value: ComplexArray
    projected_remainder_value: ComplexArray
    projected_hamiltonian_gradient: ComplexArray
    projected_kinetic_gradient: ComplexArray
    projected_remainder_gradient: ComplexArray
    projected_hamiltonian_direct_hessian: ComplexArray
    projected_kinetic_direct_hessian: ComplexArray
    projected_remainder_direct_hessian: ComplexArray
    remote_total: ComplexArray
    remote_kinetic_kinetic: ComplexArray
    remote_remainder_remainder: ComplexArray
    remote_cross: ComplexArray
    effective_quadratic: ComplexArray
    covariance_probe_projected_hamiltonian_value: ComplexArray
    covariance_probe_projected_hamiltonian_gradient: ComplexArray
    covariance_probe_effective_quadratic: ComplexArray
    diagnostics: WannierKineticLowdinQuadraticReductionDiagnostics3D


@dataclass(frozen=True, slots=True, eq=False)
class WannierKineticLowdinQuadraticReductionResult3D:
    """Retain one explicit finite selected-space quadratic reduction."""

    request: WannierKineticLowdinQuadraticReductionRequest3D
    hamiltonian_eigenvalues: VectorQuantity
    selected_frame: ComplexMatrixQuantity
    complement_frame: ComplexMatrixQuantity
    complement_resolvent: ComplexMatrixQuantity
    projected_hamiltonian_value: ComplexMatrixQuantity
    projected_kinetic_value: ComplexMatrixQuantity
    projected_remainder_value: ComplexMatrixQuantity
    projected_hamiltonian_gradient: tuple[ComplexMatrixQuantity, ...]
    projected_kinetic_gradient: tuple[ComplexMatrixQuantity, ...]
    projected_remainder_gradient: tuple[ComplexMatrixQuantity, ...]
    projected_hamiltonian_direct_hessian: tuple[tuple[ComplexMatrixQuantity, ...], ...]
    projected_kinetic_direct_hessian: tuple[tuple[ComplexMatrixQuantity, ...], ...]
    projected_remainder_direct_hessian: tuple[tuple[ComplexMatrixQuantity, ...], ...]
    remote_total: tuple[tuple[ComplexMatrixQuantity, ...], ...]
    remote_kinetic_kinetic: tuple[tuple[ComplexMatrixQuantity, ...], ...]
    remote_remainder_remainder: tuple[tuple[ComplexMatrixQuantity, ...], ...]
    remote_cross: tuple[tuple[ComplexMatrixQuantity, ...], ...]
    effective_quadratic: tuple[tuple[ComplexMatrixQuantity, ...], ...]
    covariance_probe_projected_hamiltonian_value: ComplexMatrixQuantity
    covariance_probe_projected_hamiltonian_gradient: tuple[ComplexMatrixQuantity, ...]
    covariance_probe_effective_quadratic: tuple[tuple[ComplexMatrixQuantity, ...], ...]
    diagnostics: WannierKineticLowdinQuadraticReductionDiagnostics3D

    def __post_init__(self) -> None:
        """Validate types, tensor structures, units, construction, and diagnostics."""
        self._check_args_types_and_shapes()
        # Result construction validates intrinsic tensor relations and retained
        # diagnostics only. The reduction Action owns request-to-value derivation.
        self._check_args_intrinsic_relations()

    def _check_args_types_and_shapes(self) -> None:
        """Validate result record classes and selected-space matrix dimensions."""
        if type(self.request) is not (WannierKineticLowdinQuadraticReductionRequest3D):
            raise TypeError(
                "request must be WannierKineticLowdinQuadraticReductionRequest3D"
            )
        if type(self.hamiltonian_eigenvalues) is not VectorQuantity:
            raise TypeError("hamiltonian_eigenvalues must be VectorQuantity")
        if type(self.diagnostics) is not (
            WannierKineticLowdinQuadraticReductionDiagnostics3D
        ):
            raise TypeError(
                "diagnostics must be "
                "WannierKineticLowdinQuadraticReductionDiagnostics3D"
            )
        ambient = self.request.hamiltonian_derivatives.request.operator.wannier_count
        selected = self.request.selected_rank
        complement = ambient - selected
        unitless_matrices = (
            ("selected_frame", self.selected_frame, (ambient, selected)),
            ("complement_frame", self.complement_frame, (ambient, complement)),
        )
        for name, matrix, shape in unitless_matrices:
            if type(matrix) is not ComplexMatrixQuantity:
                raise TypeError(f"{name} must be ComplexMatrixQuantity")
            if not isinstance(matrix.unit, Unitless):
                raise ValueError(f"{name} must be unitless")
            if matrix.magnitude.shape != shape:
                raise ValueError(f"{name} has the wrong shape")
        if type(self.complement_resolvent) is not ComplexMatrixQuantity:
            raise TypeError("complement_resolvent must be ComplexMatrixQuantity")
        if self.complement_resolvent.magnitude.shape != (ambient, ambient):
            raise ValueError("complement_resolvent has the wrong shape")
        energy_unit = self.request.hamiltonian_derivatives.value.unit
        gradient_unit = self.request.hamiltonian_derivatives.gradient[0].unit
        hessian_unit = self.request.hamiltonian_derivatives.hessian[0][0].unit
        if not isinstance(energy_unit, PhysicalUnit):
            raise ValueError("projected values must use a physical energy unit")
        if not isinstance(gradient_unit, PhysicalUnit):
            raise ValueError("projected gradients must use a physical unit")
        if not isinstance(hessian_unit, PhysicalUnit):
            raise ValueError("projected Hessians must use a physical unit")
        if self.hamiltonian_eigenvalues.magnitude.shape != (ambient,):
            raise ValueError("hamiltonian_eigenvalues has the wrong shape")
        if self.hamiltonian_eigenvalues.unit != energy_unit:
            raise ValueError("hamiltonian_eigenvalues has the wrong unit")
        expected_resolvent_unit = PhysicalUnit(f"1 / ({energy_unit.expression})")
        if self.complement_resolvent.unit != expected_resolvent_unit:
            raise ValueError("complement_resolvent has the wrong unit")
        for name, matrix in (
            ("projected_hamiltonian_value", self.projected_hamiltonian_value),
            ("projected_kinetic_value", self.projected_kinetic_value),
            ("projected_remainder_value", self.projected_remainder_value),
            (
                "covariance_probe_projected_hamiltonian_value",
                self.covariance_probe_projected_hamiltonian_value,
            ),
        ):
            self._check_matrix(name, matrix, (selected, selected), energy_unit)
        for name, tensor in (
            ("projected_hamiltonian_gradient", self.projected_hamiltonian_gradient),
            ("projected_kinetic_gradient", self.projected_kinetic_gradient),
            ("projected_remainder_gradient", self.projected_remainder_gradient),
            (
                "covariance_probe_projected_hamiltonian_gradient",
                self.covariance_probe_projected_hamiltonian_gradient,
            ),
        ):
            self._check_vector_tensor(name, tensor, selected, gradient_unit)
        for name, matrix_tensor in (
            (
                "projected_hamiltonian_direct_hessian",
                self.projected_hamiltonian_direct_hessian,
            ),
            (
                "projected_kinetic_direct_hessian",
                self.projected_kinetic_direct_hessian,
            ),
            (
                "projected_remainder_direct_hessian",
                self.projected_remainder_direct_hessian,
            ),
            ("remote_total", self.remote_total),
            ("remote_kinetic_kinetic", self.remote_kinetic_kinetic),
            ("remote_remainder_remainder", self.remote_remainder_remainder),
            ("remote_cross", self.remote_cross),
            ("effective_quadratic", self.effective_quadratic),
            (
                "covariance_probe_effective_quadratic",
                self.covariance_probe_effective_quadratic,
            ),
        ):
            self._check_matrix_tensor(name, matrix_tensor, selected, hessian_unit)
        self._check_args_diagnostic_units(energy_unit, gradient_unit, hessian_unit)

    def _check_args_diagnostic_units(
        self,
        energy_unit: PhysicalUnit,
        gradient_unit: PhysicalUnit,
        hessian_unit: PhysicalUnit,
    ) -> None:
        """Validate the physical unit owned by every retained diagnostic."""
        expected_units = {
            "selected_group_maximum_splitting": energy_unit,
            "complement_minimum_separation": energy_unit,
            "hamiltonian_hermitian_projection_correction_frobenius": energy_unit,
            "value_decomposition_frobenius": energy_unit,
            "gradient_decomposition_maximum_frobenius": gradient_unit,
            "direct_hessian_decomposition_maximum_frobenius": hessian_unit,
            "remote_partition_decomposition_maximum_frobenius": hessian_unit,
            "effective_quadratic_antihermitian_maximum_frobenius": hessian_unit,
            "basis_covariance_base_maximum_frobenius": energy_unit,
            "basis_covariance_gradient_maximum_frobenius": gradient_unit,
            "basis_covariance_quadratic_maximum_frobenius": hessian_unit,
        }
        for name, expected_unit in expected_units.items():
            diagnostic = getattr(self.diagnostics, name)
            if diagnostic.unit != expected_unit:
                raise ValueError(f"{name} has the wrong unit")

    @staticmethod
    def _check_matrix(
        name: str,
        matrix: ComplexMatrixQuantity,
        shape: tuple[int, int],
        unit: PhysicalUnit,
    ) -> None:
        """Validate one selected-space quantity matrix."""
        if type(matrix) is not ComplexMatrixQuantity:
            raise TypeError(f"{name} must be ComplexMatrixQuantity")
        if matrix.magnitude.shape != shape:
            raise ValueError(f"{name} has the wrong shape")
        if matrix.unit != unit:
            raise ValueError(f"{name} has the wrong unit")

    @classmethod
    def _check_vector_tensor(
        cls,
        name: str,
        tensor: tuple[ComplexMatrixQuantity, ...],
        rank: int,
        unit: PhysicalUnit,
    ) -> None:
        """Validate one three-component selected-space matrix tensor."""
        if type(tensor) is not tuple or len(tensor) != 3:
            raise TypeError(f"{name} must contain three matrices")
        for matrix in tensor:
            cls._check_matrix(name, matrix, (rank, rank), unit)

    @classmethod
    def _check_matrix_tensor(
        cls,
        name: str,
        tensor: tuple[tuple[ComplexMatrixQuantity, ...], ...],
        rank: int,
        unit: PhysicalUnit,
    ) -> None:
        """Validate one three-by-three selected-space matrix tensor."""
        if (
            type(tensor) is not tuple
            or len(tensor) != 3
            or any(type(row) is not tuple or len(row) != 3 for row in tensor)
        ):
            raise TypeError(f"{name} must contain three rows of three matrices")
        for row in tensor:
            for matrix in row:
                cls._check_matrix(name, matrix, (rank, rank), unit)

    def _check_args_intrinsic_relations(self) -> None:
        """Validate retained algebra and diagnostics without an eigensolve."""
        effective = _matrix_array(self.effective_quadratic)
        direct = _matrix_array(self.projected_hamiltonian_direct_hessian)
        remote_total = _matrix_array(self.remote_total)
        if not np.array_equal(effective, direct + remote_total):
            raise ValueError(
                "effective quadratic tensor must equal direct plus remote tensors"
            )
        remote_partition = (
            remote_total
            - _matrix_array(self.remote_kinetic_kinetic)
            - _matrix_array(self.remote_remainder_remainder)
            - _matrix_array(self.remote_cross)
        )
        h = self.request.hamiltonian_derivatives
        t = self.request.kinetic_derivatives
        r = self.request.nonkinetic_remainder_derivatives
        h_gradient = _vector_array(h.gradient)
        t_gradient = _vector_array(t.gradient)
        r_gradient = _vector_array(r.gradient)
        h_hessian = _matrix_array(h.hessian)
        t_hessian = _matrix_array(t.hessian)
        r_hessian = _matrix_array(r.hessian)
        eigenvalues = self.hamiltonian_eigenvalues.magnitude
        selected_indices = np.asarray(
            self.request.selected_eigenvalue_indices, dtype=np.int64
        )
        complement_indices = np.asarray(
            [
                index
                for index in range(eigenvalues.size)
                if index not in self.request.selected_eigenvalue_indices
            ],
            dtype=np.int64,
        )
        selected_eigenvalues = eigenvalues[selected_indices]
        complement_eigenvalues = eigenvalues[complement_indices]
        gauge = self.request.covariance_probe_gauge.magnitude
        quadratic_covariance = covariance_maximum_frobenius(
            effective,
            _matrix_array(self.covariance_probe_effective_quadratic),
            gauge,
        )
        expected_diagnostics = {
            "selected_group_maximum_splitting": float(
                np.max(selected_eigenvalues) - np.min(selected_eigenvalues)
            ),
            "complement_minimum_separation": float(
                np.min(
                    np.abs(
                        complement_eigenvalues - self.request.reference_energy.magnitude
                    )
                )
            ),
            "hamiltonian_hermitian_projection_correction_frobenius": float(
                np.linalg.norm(_hermitian_part(h.value.magnitude) - h.value.magnitude)
            ),
            "value_decomposition_frobenius": float(
                np.linalg.norm(
                    h.value.magnitude - t.value.magnitude - r.value.magnitude
                )
            ),
            "gradient_decomposition_maximum_frobenius": maximum_frobenius(
                h_gradient - t_gradient - r_gradient
            ),
            "direct_hessian_decomposition_maximum_frobenius": maximum_frobenius(
                h_hessian - t_hessian - r_hessian
            ),
            "remote_partition_decomposition_maximum_frobenius": (
                maximum_frobenius(remote_partition)
            ),
            "effective_quadratic_antihermitian_maximum_frobenius": (
                antihermitian_maximum_frobenius(effective)
            ),
            "basis_covariance_base_maximum_frobenius": covariance_maximum_frobenius(
                self.projected_hamiltonian_value.magnitude,
                self.covariance_probe_projected_hamiltonian_value.magnitude,
                gauge,
            ),
            "basis_covariance_gradient_maximum_frobenius": covariance_maximum_frobenius(
                _vector_array(self.projected_hamiltonian_gradient),
                _vector_array(self.covariance_probe_projected_hamiltonian_gradient),
                gauge,
            ),
            "basis_covariance_quadratic_maximum_frobenius": quadratic_covariance,
        }
        for name, expected in expected_diagnostics.items():
            observed = getattr(self.diagnostics, name).magnitude
            if observed != expected:
                raise ValueError(f"{name} does not match retained values")


class WannierKineticLowdinQuadraticReductionConstructor3D:
    """Construct a caller-selected finite Löwdin quadratic reduction."""

    __slots__ = ()

    def execute(
        self, request: WannierKineticLowdinQuadraticReductionRequest3D
    ) -> WannierKineticLowdinQuadraticReductionResult3D:
        """Return selected frames, projected tensors, remote terms, and diagnostics.

        The Action owns request-to-reduction derivation and evaluates it once. The
        immutable Result validates intrinsic retained relations without replaying this
        derivation or treating manual construction as evidence that the Action ran.

        Raises
        ------
        ValueError
            If the Hamiltonian anti-Hermitian Frobenius defect exceeds the caller's
            tolerance. Such an operator does not define the Hermitian eigenspace and
            Löwdin complement resolvent required by this reduction.
        """
        if type(request) is not WannierKineticLowdinQuadraticReductionRequest3D:
            raise TypeError(
                "request must be WannierKineticLowdinQuadraticReductionRequest3D"
            )
        h = request.hamiltonian_derivatives
        t = request.kinetic_derivatives
        r = request.nonkinetic_remainder_derivatives
        hermiticity_defect = h.diagnostics.value_hermiticity_frobenius
        hermiticity_tolerance = request.hamiltonian_hermiticity_absolute_tolerance
        if hermiticity_defect.magnitude > hermiticity_tolerance.magnitude:
            raise ValueError(
                "Hamiltonian value is not Hermitian within the caller-supplied "
                "hamiltonian_hermiticity_absolute_tolerance; the Hermitian "
                "eigenspace and Löwdin complement resolvent are not mathematically "
                "defined by this reduction request"
            )
        # The accepted finite defect is removed explicitly before the Hamiltonian
        # eigenspace and projected base value are constructed. The retained correction
        # quantifies this numerical projection rather than treating it as exact input.
        h_value = _hermitian_part(h.value.magnitude)
        hermitian_projection_correction = float(
            np.linalg.norm(h_value - h.value.magnitude)
        )
        eigenvalues, eigenvectors = np.linalg.eigh(h_value)
        selected_indices = np.asarray(
            request.selected_eigenvalue_indices, dtype=np.int64
        )
        complement_indices = np.asarray(
            [
                index
                for index in range(eigenvalues.size)
                if index not in request.selected_eigenvalue_indices
            ],
            dtype=np.int64,
        )
        reference = request.reference_energy.magnitude
        tolerance = request.degeneracy_absolute_tolerance.magnitude
        selected_eigenvalues = eigenvalues[selected_indices]
        complement_eigenvalues = eigenvalues[complement_indices]
        if np.any(np.abs(selected_eigenvalues - reference) > tolerance):
            raise ValueError("selected eigenvalues lie outside degeneracy tolerance")
        if np.any(np.abs(complement_eigenvalues - reference) <= tolerance):
            raise ValueError("degeneracy tolerance contains an unselected eigenvalue")
        denominators = reference - complement_eigenvalues
        if np.any(denominators == 0.0):
            raise ValueError("complement resolvent contains a zero denominator")
        frame = eigenvectors[:, selected_indices]
        complement = eigenvectors[:, complement_indices]
        resolvent = complement @ np.diag(1.0 / denominators) @ complement.conj().T
        h_gradient = _vector_array(h.gradient)
        t_gradient = _vector_array(t.gradient)
        r_gradient = _vector_array(r.gradient)
        h_hessian = _matrix_array(h.hessian)
        t_hessian = _matrix_array(t.hessian)
        r_hessian = _matrix_array(r.hessian)
        h_projected = self._project(frame, h_value, h_gradient, h_hessian)
        t_projected = self._project(frame, t.value.magnitude, t_gradient, t_hessian)
        r_projected = self._project(frame, r.value.magnitude, r_gradient, r_hessian)
        h_base, h_projected_gradient, h_projected_hessian = h_projected
        t_base, t_projected_gradient, t_projected_hessian = t_projected
        r_base, r_projected_gradient, r_projected_hessian = r_projected
        remote_total = self._remote(frame, h_gradient, resolvent, h_gradient)
        remote_tt = self._remote(frame, t_gradient, resolvent, t_gradient)
        remote_rr = self._remote(frame, r_gradient, resolvent, r_gradient)
        remote_cross = self._remote(
            frame, t_gradient, resolvent, r_gradient
        ) + self._remote(frame, r_gradient, resolvent, t_gradient)
        effective = h_projected_hessian + remote_total
        gauge = request.covariance_probe_gauge.magnitude
        changed_frame = frame @ gauge
        # Covariance must compare the same represented operator in both gauges. Use
        # the accepted Hermitian projection here as for ``h_base``; otherwise the
        # removed anti-Hermitian defect would be misreported as a covariance defect.
        changed_h = self._project(changed_frame, h_value, h_gradient, h_hessian)
        changed_remote = self._remote(changed_frame, h_gradient, resolvent, h_gradient)
        changed_effective = changed_h[2] + changed_remote
        energy_unit = h.value.unit
        gradient_unit = h.gradient[0].unit
        hessian_unit = h.hessian[0][0].unit
        diagnostics = WannierKineticLowdinQuadraticReductionDiagnostics3D(
            selected_group_maximum_splitting=ScalarQuantity(
                float(np.max(selected_eigenvalues) - np.min(selected_eigenvalues)),
                energy_unit,
            ),
            complement_minimum_separation=ScalarQuantity(
                float(np.min(np.abs(complement_eigenvalues - reference))),
                energy_unit,
            ),
            hamiltonian_hermitian_projection_correction_frobenius=ScalarQuantity(
                hermitian_projection_correction,
                energy_unit,
            ),
            value_decomposition_frobenius=ScalarQuantity(
                float(
                    np.linalg.norm(
                        h.value.magnitude - t.value.magnitude - r.value.magnitude
                    )
                ),
                energy_unit,
            ),
            gradient_decomposition_maximum_frobenius=ScalarQuantity(
                maximum_frobenius(h_gradient - t_gradient - r_gradient),
                gradient_unit,
            ),
            direct_hessian_decomposition_maximum_frobenius=ScalarQuantity(
                maximum_frobenius(h_hessian - t_hessian - r_hessian),
                hessian_unit,
            ),
            remote_partition_decomposition_maximum_frobenius=ScalarQuantity(
                maximum_frobenius(remote_total - remote_tt - remote_rr - remote_cross),
                hessian_unit,
            ),
            effective_quadratic_antihermitian_maximum_frobenius=ScalarQuantity(
                antihermitian_maximum_frobenius(effective), hessian_unit
            ),
            basis_covariance_base_maximum_frobenius=ScalarQuantity(
                covariance_maximum_frobenius(h_base, changed_h[0], gauge), energy_unit
            ),
            basis_covariance_gradient_maximum_frobenius=ScalarQuantity(
                covariance_maximum_frobenius(h_projected_gradient, changed_h[1], gauge),
                gradient_unit,
            ),
            basis_covariance_quadratic_maximum_frobenius=ScalarQuantity(
                covariance_maximum_frobenius(effective, changed_effective, gauge),
                hessian_unit,
            ),
        )
        arrays = _LowdinQuadraticArrays3D(
            eigenvalues=eigenvalues,
            selected_frame=frame,
            complement_frame=complement,
            resolvent=resolvent,
            projected_hamiltonian_value=h_base,
            projected_kinetic_value=t_base,
            projected_remainder_value=r_base,
            projected_hamiltonian_gradient=h_projected_gradient,
            projected_kinetic_gradient=t_projected_gradient,
            projected_remainder_gradient=r_projected_gradient,
            projected_hamiltonian_direct_hessian=h_projected_hessian,
            projected_kinetic_direct_hessian=t_projected_hessian,
            projected_remainder_direct_hessian=r_projected_hessian,
            remote_total=remote_total,
            remote_kinetic_kinetic=remote_tt,
            remote_remainder_remainder=remote_rr,
            remote_cross=remote_cross,
            effective_quadratic=effective,
            covariance_probe_projected_hamiltonian_value=changed_h[0],
            covariance_probe_projected_hamiltonian_gradient=changed_h[1],
            covariance_probe_effective_quadratic=changed_effective,
            diagnostics=diagnostics,
        )
        energy_unit = request.hamiltonian_derivatives.value.unit
        gradient_unit = request.hamiltonian_derivatives.gradient[0].unit
        hessian_unit = request.hamiltonian_derivatives.hessian[0][0].unit
        if not isinstance(energy_unit, PhysicalUnit):
            raise ValueError("Hamiltonian derivative must use a physical energy unit")
        if not isinstance(gradient_unit, PhysicalUnit):
            raise ValueError("Hamiltonian gradient must use a physical unit")
        if not isinstance(hessian_unit, PhysicalUnit):
            raise ValueError("Hamiltonian Hessian must use a physical unit")
        resolvent_unit = PhysicalUnit(f"1 / ({energy_unit.expression})")
        return WannierKineticLowdinQuadraticReductionResult3D(
            request=request,
            hamiltonian_eigenvalues=VectorQuantity(arrays.eigenvalues, energy_unit),
            selected_frame=ComplexMatrixQuantity(arrays.selected_frame, Unitless()),
            complement_frame=ComplexMatrixQuantity(arrays.complement_frame, Unitless()),
            complement_resolvent=ComplexMatrixQuantity(
                arrays.resolvent, resolvent_unit
            ),
            projected_hamiltonian_value=ComplexMatrixQuantity(
                arrays.projected_hamiltonian_value, energy_unit
            ),
            projected_kinetic_value=ComplexMatrixQuantity(
                arrays.projected_kinetic_value, energy_unit
            ),
            projected_remainder_value=ComplexMatrixQuantity(
                arrays.projected_remainder_value, energy_unit
            ),
            projected_hamiltonian_gradient=self._vector_quantities(
                arrays.projected_hamiltonian_gradient, gradient_unit
            ),
            projected_kinetic_gradient=self._vector_quantities(
                arrays.projected_kinetic_gradient, gradient_unit
            ),
            projected_remainder_gradient=self._vector_quantities(
                arrays.projected_remainder_gradient, gradient_unit
            ),
            projected_hamiltonian_direct_hessian=self._matrix_quantities(
                arrays.projected_hamiltonian_direct_hessian, hessian_unit
            ),
            projected_kinetic_direct_hessian=self._matrix_quantities(
                arrays.projected_kinetic_direct_hessian, hessian_unit
            ),
            projected_remainder_direct_hessian=self._matrix_quantities(
                arrays.projected_remainder_direct_hessian, hessian_unit
            ),
            remote_total=self._matrix_quantities(arrays.remote_total, hessian_unit),
            remote_kinetic_kinetic=self._matrix_quantities(
                arrays.remote_kinetic_kinetic, hessian_unit
            ),
            remote_remainder_remainder=self._matrix_quantities(
                arrays.remote_remainder_remainder, hessian_unit
            ),
            remote_cross=self._matrix_quantities(arrays.remote_cross, hessian_unit),
            effective_quadratic=self._matrix_quantities(
                arrays.effective_quadratic, hessian_unit
            ),
            covariance_probe_projected_hamiltonian_value=ComplexMatrixQuantity(
                arrays.covariance_probe_projected_hamiltonian_value, energy_unit
            ),
            covariance_probe_projected_hamiltonian_gradient=self._vector_quantities(
                arrays.covariance_probe_projected_hamiltonian_gradient, gradient_unit
            ),
            covariance_probe_effective_quadratic=self._matrix_quantities(
                arrays.covariance_probe_effective_quadratic, hessian_unit
            ),
            diagnostics=arrays.diagnostics,
        )

    @staticmethod
    def _project(
        frame: ComplexArray,
        value: ComplexArray,
        gradient: ComplexArray,
        hessian: ComplexArray,
    ) -> tuple[ComplexArray, ComplexArray, ComplexArray]:
        """Project value and derivative tensors into one selected frame."""
        projected_value = frame.conj().T @ value @ frame
        projected_gradient = np.asarray(
            [frame.conj().T @ matrix @ frame for matrix in gradient]
        )
        projected_hessian = np.asarray(
            [[frame.conj().T @ matrix @ frame for matrix in row] for row in hessian]
        )
        return projected_value, projected_gradient, projected_hessian

    @staticmethod
    def _remote(
        frame: ComplexArray,
        left: ComplexArray,
        resolvent: ComplexArray,
        right: ComplexArray,
    ) -> ComplexArray:
        """Return one symmetrized remote-subspace quadratic tensor."""
        return np.asarray(
            [
                [
                    frame.conj().T
                    @ (
                        left[first] @ resolvent @ right[second]
                        + right[second] @ resolvent @ left[first]
                    )
                    @ frame
                    for second in range(3)
                ]
                for first in range(3)
            ]
        )

    @staticmethod
    def _vector_quantities(
        tensor: ComplexArray, unit: PhysicalUnit
    ) -> tuple[ComplexMatrixQuantity, ...]:
        """Construct one immutable three-component matrix tensor."""
        return tuple(ComplexMatrixQuantity(matrix, unit) for matrix in tensor)

    @staticmethod
    def _matrix_quantities(
        tensor: ComplexArray, unit: PhysicalUnit
    ) -> tuple[tuple[ComplexMatrixQuantity, ...], ...]:
        """Construct one immutable three-by-three matrix tensor."""
        return tuple(
            tuple(ComplexMatrixQuantity(matrix, unit) for matrix in row)
            for row in tensor
        )


__all__ = [
    "WannierKineticLowdinQuadraticReductionConstructor3D",
    "WannierKineticLowdinQuadraticReductionDiagnostics3D",
    "WannierKineticLowdinQuadraticReductionRequest3D",
    "WannierKineticLowdinQuadraticReductionResult3D",
]
