"""Degenerate finite-dimensional quadratic represented-operator reduction."""

from __future__ import annotations

from dataclasses import dataclass

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

from .wannier_kinetic import WannierOperatorRole
from .wigner_seitz_interpolation import (
    WannierRepresentedOperatorCartesianDerivativeResult3D,
)

type ComplexArray = npt.NDArray[np.complex128]
type RealArray = npt.NDArray[np.float64]


@dataclass(frozen=True, slots=True, eq=False)
class WannierKineticDegenerateQuadraticReductionRequest3D:
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
        ):
            if type(value) is not ScalarQuantity:
                raise TypeError(f"{name} must be ScalarQuantity")
            if value.unit != energy_unit:
                raise ValueError(f"{name} must use the Hamiltonian energy unit")
        if self.degeneracy_absolute_tolerance.magnitude < 0.0:
            raise ValueError("degeneracy_absolute_tolerance must be nonnegative")

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
class WannierKineticDegenerateQuadraticReductionDiagnostics3D:
    """Retain unit-carrying closure, Hermiticity, separation, and covariance defects."""

    selected_group_maximum_splitting: ScalarQuantity
    complement_minimum_separation: ScalarQuantity
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
class _DegenerateQuadraticArrays3D:
    """Hold one ephemeral quadratic reduction before quantity construction."""

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
    diagnostics: WannierKineticDegenerateQuadraticReductionDiagnostics3D


@dataclass(frozen=True, slots=True, eq=False)
class WannierKineticDegenerateQuadraticReductionResult3D:
    """Retain one explicit finite selected-space quadratic reduction."""

    request: WannierKineticDegenerateQuadraticReductionRequest3D
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
    diagnostics: WannierKineticDegenerateQuadraticReductionDiagnostics3D

    def __post_init__(self) -> None:
        """Validate types, tensor structures, units, construction, and diagnostics."""
        self._check_args_types_and_shapes()
        self._check_args_construction()

    def _check_args_types_and_shapes(self) -> None:
        """Validate result record classes and selected-space matrix dimensions."""
        if type(self.request) is not (
            WannierKineticDegenerateQuadraticReductionRequest3D
        ):
            raise TypeError(
                "request must be WannierKineticDegenerateQuadraticReductionRequest3D"
            )
        if type(self.hamiltonian_eigenvalues) is not VectorQuantity:
            raise TypeError("hamiltonian_eigenvalues must be VectorQuantity")
        if type(self.diagnostics) is not (
            WannierKineticDegenerateQuadraticReductionDiagnostics3D
        ):
            raise TypeError(
                "diagnostics must be "
                "WannierKineticDegenerateQuadraticReductionDiagnostics3D"
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
        ):
            self._check_matrix(name, matrix, (selected, selected), energy_unit)
        for name, tensor in (
            ("projected_hamiltonian_gradient", self.projected_hamiltonian_gradient),
            ("projected_kinetic_gradient", self.projected_kinetic_gradient),
            ("projected_remainder_gradient", self.projected_remainder_gradient),
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
        ):
            self._check_matrix_tensor(name, matrix_tensor, selected, hessian_unit)

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

    def _check_args_construction(self) -> None:
        """Require every retained array and diagnostic to reproduce the request."""
        arrays = WannierKineticDegenerateQuadraticReductionConstructor3D._evaluate(
            self.request
        )
        scalar_arrays = (
            (self.hamiltonian_eigenvalues.magnitude, arrays.eigenvalues),
            (self.selected_frame.magnitude, arrays.selected_frame),
            (self.complement_frame.magnitude, arrays.complement_frame),
            (self.complement_resolvent.magnitude, arrays.resolvent),
            (
                self.projected_hamiltonian_value.magnitude,
                arrays.projected_hamiltonian_value,
            ),
            (self.projected_kinetic_value.magnitude, arrays.projected_kinetic_value),
            (
                self.projected_remainder_value.magnitude,
                arrays.projected_remainder_value,
            ),
        )
        if any(
            not np.array_equal(actual, expected) for actual, expected in scalar_arrays
        ):
            raise ValueError("quadratic reduction values do not match the request")
        vector_tensors = (
            (
                self.projected_hamiltonian_gradient,
                arrays.projected_hamiltonian_gradient,
            ),
            (self.projected_kinetic_gradient, arrays.projected_kinetic_gradient),
            (self.projected_remainder_gradient, arrays.projected_remainder_gradient),
        )
        for actual, expected in vector_tensors:
            if any(
                not np.array_equal(matrix.magnitude, value)
                for matrix, value in zip(actual, expected, strict=True)
            ):
                raise ValueError("quadratic reduction gradient does not match request")
        matrix_tensors = (
            (
                self.projected_hamiltonian_direct_hessian,
                arrays.projected_hamiltonian_direct_hessian,
            ),
            (
                self.projected_kinetic_direct_hessian,
                arrays.projected_kinetic_direct_hessian,
            ),
            (
                self.projected_remainder_direct_hessian,
                arrays.projected_remainder_direct_hessian,
            ),
            (self.remote_total, arrays.remote_total),
            (self.remote_kinetic_kinetic, arrays.remote_kinetic_kinetic),
            (self.remote_remainder_remainder, arrays.remote_remainder_remainder),
            (self.remote_cross, arrays.remote_cross),
            (self.effective_quadratic, arrays.effective_quadratic),
        )
        for actual_matrix_tensor, expected_matrix_tensor in matrix_tensors:
            if any(
                not np.array_equal(matrix.magnitude, value)
                for row, expected_row in zip(
                    actual_matrix_tensor, expected_matrix_tensor, strict=True
                )
                for matrix, value in zip(row, expected_row, strict=True)
            ):
                raise ValueError("quadratic reduction tensor does not match request")
        if self.diagnostics != arrays.diagnostics:
            raise ValueError("quadratic reduction diagnostics do not match request")


class WannierKineticDegenerateQuadraticReductionConstructor3D:
    """Construct a caller-selected finite Löwdin quadratic reduction."""

    __slots__ = ()

    def execute(
        self, request: WannierKineticDegenerateQuadraticReductionRequest3D
    ) -> WannierKineticDegenerateQuadraticReductionResult3D:
        """Return selected frames, projected tensors, remote terms, and diagnostics."""
        if type(request) is not WannierKineticDegenerateQuadraticReductionRequest3D:
            raise TypeError(
                "request must be WannierKineticDegenerateQuadraticReductionRequest3D"
            )
        arrays = self._evaluate(request)
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
        return WannierKineticDegenerateQuadraticReductionResult3D(
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
            diagnostics=arrays.diagnostics,
        )

    @classmethod
    def _evaluate(
        cls, request: WannierKineticDegenerateQuadraticReductionRequest3D
    ) -> _DegenerateQuadraticArrays3D:
        """Evaluate one reduction without constructing the public result."""
        h = request.hamiltonian_derivatives
        t = request.kinetic_derivatives
        r = request.nonkinetic_remainder_derivatives
        h_value = cls._hermitian_part(h.value.magnitude)
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
        h_gradient = cls._vector_array(h.gradient)
        t_gradient = cls._vector_array(t.gradient)
        r_gradient = cls._vector_array(r.gradient)
        h_hessian = cls._matrix_array(h.hessian)
        t_hessian = cls._matrix_array(t.hessian)
        r_hessian = cls._matrix_array(r.hessian)
        h_projected = cls._project(frame, h.value.magnitude, h_gradient, h_hessian)
        t_projected = cls._project(frame, t.value.magnitude, t_gradient, t_hessian)
        r_projected = cls._project(frame, r.value.magnitude, r_gradient, r_hessian)
        h_base, h_projected_gradient, h_projected_hessian = h_projected
        t_base, t_projected_gradient, t_projected_hessian = t_projected
        r_base, r_projected_gradient, r_projected_hessian = r_projected
        remote_total = cls._remote(frame, h_gradient, resolvent, h_gradient)
        remote_tt = cls._remote(frame, t_gradient, resolvent, t_gradient)
        remote_rr = cls._remote(frame, r_gradient, resolvent, r_gradient)
        remote_cross = cls._remote(
            frame, t_gradient, resolvent, r_gradient
        ) + cls._remote(frame, r_gradient, resolvent, t_gradient)
        effective = h_projected_hessian + remote_total
        gauge = request.covariance_probe_gauge.magnitude
        changed_frame = frame @ gauge
        changed_h = cls._project(
            changed_frame, h.value.magnitude, h_gradient, h_hessian
        )
        changed_remote = cls._remote(changed_frame, h_gradient, resolvent, h_gradient)
        changed_effective = changed_h[2] + changed_remote
        energy_unit = h.value.unit
        gradient_unit = h.gradient[0].unit
        hessian_unit = h.hessian[0][0].unit
        diagnostics = WannierKineticDegenerateQuadraticReductionDiagnostics3D(
            selected_group_maximum_splitting=ScalarQuantity(
                float(np.max(selected_eigenvalues) - np.min(selected_eigenvalues)),
                energy_unit,
            ),
            complement_minimum_separation=ScalarQuantity(
                float(np.min(np.abs(complement_eigenvalues - reference))),
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
                cls._maximum_frobenius(h_gradient - t_gradient - r_gradient),
                gradient_unit,
            ),
            direct_hessian_decomposition_maximum_frobenius=ScalarQuantity(
                cls._maximum_frobenius(h_hessian - t_hessian - r_hessian),
                hessian_unit,
            ),
            remote_partition_decomposition_maximum_frobenius=ScalarQuantity(
                cls._maximum_frobenius(
                    remote_total - remote_tt - remote_rr - remote_cross
                ),
                hessian_unit,
            ),
            effective_quadratic_antihermitian_maximum_frobenius=ScalarQuantity(
                cls._antihermitian_defect(effective), hessian_unit
            ),
            basis_covariance_base_maximum_frobenius=ScalarQuantity(
                cls._covariance_defect(h_base, changed_h[0], gauge), energy_unit
            ),
            basis_covariance_gradient_maximum_frobenius=ScalarQuantity(
                cls._covariance_defect(h_projected_gradient, changed_h[1], gauge),
                gradient_unit,
            ),
            basis_covariance_quadratic_maximum_frobenius=ScalarQuantity(
                cls._covariance_defect(effective, changed_effective, gauge),
                hessian_unit,
            ),
        )
        return _DegenerateQuadraticArrays3D(
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
            diagnostics=diagnostics,
        )

    @staticmethod
    def _hermitian_part(matrix: ComplexArray) -> ComplexArray:
        """Return the roundoff-level Hermitian part of one matrix."""
        return 0.5 * (matrix + matrix.conj().T)

    @staticmethod
    def _vector_array(
        tensor: tuple[ComplexMatrixQuantity, ...],
    ) -> ComplexArray:
        """Return one three-component derivative array."""
        return np.asarray([matrix.magnitude for matrix in tensor])

    @staticmethod
    def _matrix_array(
        tensor: tuple[tuple[ComplexMatrixQuantity, ...], ...],
    ) -> ComplexArray:
        """Return one three-by-three derivative array."""
        return np.asarray([[matrix.magnitude for matrix in row] for row in tensor])

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
    def _maximum_frobenius(tensor: ComplexArray) -> float:
        """Return the largest matrix Frobenius norm in one tensor."""
        matrices = tensor.reshape((-1, tensor.shape[-2], tensor.shape[-1]))
        return float(max(np.linalg.norm(matrix) for matrix in matrices))

    @classmethod
    def _antihermitian_defect(cls, tensor: ComplexArray) -> float:
        """Return the largest matrix anti-Hermitian Frobenius defect."""
        matrices = tensor.reshape((-1, tensor.shape[-2], tensor.shape[-1]))
        return float(
            max(np.linalg.norm(matrix - matrix.conj().T) for matrix in matrices)
        )

    @staticmethod
    def _covariance_defect(
        original: ComplexArray, transformed: ComplexArray, gauge: ComplexArray
    ) -> float:
        """Return the largest selected-basis covariance defect."""
        matrices = original.reshape((-1, original.shape[-2], original.shape[-1]))
        changed = transformed.reshape(
            (-1, transformed.shape[-2], transformed.shape[-1])
        )
        return float(
            max(
                np.linalg.norm(after - gauge.conj().T @ before @ gauge)
                for before, after in zip(matrices, changed, strict=True)
            )
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


@dataclass(frozen=True, slots=True, eq=False)
class WannierKineticDegenerateQuadraticModelEvaluationRequest3D:
    """Declare Cartesian offsets for one retained quadratic model evaluation.

    Parameters
    ----------
    reduction
        Identified selected-space quadratic reduction to evaluate.
    cartesian_offsets
        Matrix of Cartesian reciprocal-space row vectors. Its unit must be
        dimensionally compatible with the inverse direct-lattice unit.
    """

    reduction: WannierKineticDegenerateQuadraticReductionResult3D
    cartesian_offsets: MatrixQuantity

    def __post_init__(self) -> None:
        """Validate the reduction and Cartesian reciprocal-coordinate contract."""
        self._check_args_reduction()
        self._check_args_offsets()

    def _check_args_reduction(self) -> None:
        """Require one exact finite quadratic-reduction result."""
        if type(self.reduction) is not (
            WannierKineticDegenerateQuadraticReductionResult3D
        ):
            raise TypeError(
                "reduction must be WannierKineticDegenerateQuadraticReductionResult3D"
            )

    def _check_args_offsets(self) -> None:
        """Require a nonempty matrix of compatible Cartesian reciprocal vectors."""
        if type(self.cartesian_offsets) is not MatrixQuantity:
            raise TypeError("cartesian_offsets must be MatrixQuantity")
        if self.cartesian_offsets.magnitude.ndim != 2 or (
            self.cartesian_offsets.magnitude.shape[1] != 3
        ):
            raise ValueError("cartesian_offsets must have shape (sample_count, 3)")
        if self.cartesian_offsets.magnitude.shape[0] == 0:
            raise ValueError("cartesian_offsets must contain at least one sample")
        if not isinstance(self.cartesian_offsets.unit, PhysicalUnit):
            raise ValueError("cartesian_offsets must have a physical reciprocal unit")
        target = self.target_offset_unit
        if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
            self.cartesian_offsets.unit, target
        ):
            raise ValueError(
                "cartesian_offsets unit must be inverse to the direct-lattice unit"
            )

    @property
    def target_offset_unit(self) -> PhysicalUnit:
        """Return the reciprocal unit paired with the derivative lattice unit."""
        inventory = self.reduction.request.hamiltonian_derivatives.request.inventory
        lattice_unit = inventory.direct_lattice.unit
        if not isinstance(lattice_unit, PhysicalUnit):
            raise ValueError("derivative inventory must use a physical lattice unit")
        return PhysicalUnit(f"1 / ({lattice_unit.expression})")


@dataclass(frozen=True, slots=True)
class WannierKineticDegenerateQuadraticModelEvaluationDiagnostics3D:
    """Retain the maximum evaluated-matrix anti-Hermitian defect."""

    antihermitian_maximum_frobenius: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate one nonnegative energy-valued defect."""
        if type(self.antihermitian_maximum_frobenius) is not ScalarQuantity:
            raise TypeError("antihermitian_maximum_frobenius must be ScalarQuantity")
        if self.antihermitian_maximum_frobenius.magnitude < 0.0:
            raise ValueError("antihermitian_maximum_frobenius must be nonnegative")


@dataclass(frozen=True, slots=True, eq=False)
class WannierKineticDegenerateQuadraticModelEvaluationResult3D:
    """Retain selected-space effective matrices at explicit Cartesian offsets."""

    request: WannierKineticDegenerateQuadraticModelEvaluationRequest3D
    matrices: tuple[ComplexMatrixQuantity, ...]
    diagnostics: WannierKineticDegenerateQuadraticModelEvaluationDiagnostics3D

    def __post_init__(self) -> None:
        """Validate matrix types, units, shapes, values, and diagnostics."""
        self._check_args_types_and_matrices()
        self._check_args_construction()

    def _check_args_types_and_matrices(self) -> None:
        """Require one homogeneous selected-space energy-matrix family."""
        if type(self.request) is not (
            WannierKineticDegenerateQuadraticModelEvaluationRequest3D
        ):
            raise TypeError(
                "request must be "
                "WannierKineticDegenerateQuadraticModelEvaluationRequest3D"
            )
        if type(self.diagnostics) is not (
            WannierKineticDegenerateQuadraticModelEvaluationDiagnostics3D
        ):
            raise TypeError(
                "diagnostics must be "
                "WannierKineticDegenerateQuadraticModelEvaluationDiagnostics3D"
            )
        sample_count = self.request.cartesian_offsets.magnitude.shape[0]
        rank = self.request.reduction.request.selected_rank
        energy_unit = self.request.reduction.projected_hamiltonian_value.unit
        if type(self.matrices) is not tuple or len(self.matrices) != sample_count:
            raise ValueError("matrices must contain one value per Cartesian offset")
        for matrix in self.matrices:
            if type(matrix) is not ComplexMatrixQuantity:
                raise TypeError("matrices must contain ComplexMatrixQuantity values")
            if matrix.magnitude.shape != (rank, rank):
                raise ValueError("evaluated matrix has the wrong selected rank")
            if matrix.unit != energy_unit:
                raise ValueError("evaluated matrix has the wrong energy unit")

    def _check_args_construction(self) -> None:
        """Require evaluated matrices and diagnostics to reproduce the request."""
        arrays, diagnostics = (
            WannierKineticDegenerateQuadraticModelEvaluator3D._evaluate(self.request)
        )
        if any(
            not np.array_equal(matrix.magnitude, expected)
            for matrix, expected in zip(self.matrices, arrays, strict=True)
        ):
            raise ValueError("evaluated matrices do not match the request")
        if self.diagnostics != diagnostics:
            raise ValueError("evaluation diagnostics do not match the request")


class WannierKineticDegenerateQuadraticModelEvaluator3D:
    """Evaluate a retained degenerate quadratic model at Cartesian offsets."""

    __slots__ = ()

    def execute(
        self, request: WannierKineticDegenerateQuadraticModelEvaluationRequest3D
    ) -> WannierKineticDegenerateQuadraticModelEvaluationResult3D:
        """Return one selected-space energy matrix for every requested offset."""
        if type(request) is not (
            WannierKineticDegenerateQuadraticModelEvaluationRequest3D
        ):
            raise TypeError(
                "request must be "
                "WannierKineticDegenerateQuadraticModelEvaluationRequest3D"
            )
        arrays, diagnostics = self._evaluate(request)
        energy_unit = request.reduction.projected_hamiltonian_value.unit
        if not isinstance(energy_unit, PhysicalUnit):
            raise ValueError("quadratic model must use a physical energy unit")
        return WannierKineticDegenerateQuadraticModelEvaluationResult3D(
            request=request,
            matrices=tuple(
                ComplexMatrixQuantity(matrix, energy_unit) for matrix in arrays
            ),
            diagnostics=diagnostics,
        )

    @staticmethod
    def _evaluate(
        request: WannierKineticDegenerateQuadraticModelEvaluationRequest3D,
    ) -> tuple[
        ComplexArray,
        WannierKineticDegenerateQuadraticModelEvaluationDiagnostics3D,
    ]:
        """Evaluate the finite Taylor polynomial in the derivative length unit."""
        offsets = MODEL_SYSTEM_UNIT_CONVERTER.convert_matrix(
            request.cartesian_offsets, request.target_offset_unit
        ).magnitude
        reduction = request.reduction
        base = reduction.projected_hamiltonian_value.magnitude
        gradient = np.asarray(
            [matrix.magnitude for matrix in reduction.projected_hamiltonian_gradient]
        )
        quadratic = np.asarray(
            [
                [matrix.magnitude for matrix in row]
                for row in reduction.effective_quadratic
            ]
        )
        matrices = np.asarray(
            [
                base
                + np.einsum("a,aij->ij", offset, gradient, optimize=True)
                + 0.5
                * np.einsum("a,b,abij->ij", offset, offset, quadratic, optimize=True)
                for offset in offsets
            ]
        )
        energy_unit = reduction.projected_hamiltonian_value.unit
        diagnostics = WannierKineticDegenerateQuadraticModelEvaluationDiagnostics3D(
            antihermitian_maximum_frobenius=ScalarQuantity(
                WannierKineticDegenerateQuadraticReductionConstructor3D._antihermitian_defect(
                    matrices
                ),
                energy_unit,
            )
        )
        return matrices, diagnostics


@dataclass(frozen=True, slots=True, eq=False)
class WannierKineticDegenerateQuadraticDirectionalContractionRequest3D:
    """Declare normalized Cartesian directions for quadratic-tensor contraction.

    Parameters
    ----------
    reduction
        Identified selected-space quadratic reduction to contract.
    cartesian_directions
        Nonempty matrix of unitless normalized Cartesian row vectors.
    direction_absolute_tolerance
        Absolute tolerance applied to each Euclidean direction norm.
    """

    reduction: WannierKineticDegenerateQuadraticReductionResult3D
    cartesian_directions: MatrixQuantity
    direction_absolute_tolerance: float

    def __post_init__(self) -> None:
        """Validate reduction type, Cartesian directions, and norm tolerance."""
        self._check_args_reduction()
        self._check_args_directions()

    def _check_args_reduction(self) -> None:
        """Require one exact finite quadratic-reduction result."""
        if type(self.reduction) is not (
            WannierKineticDegenerateQuadraticReductionResult3D
        ):
            raise TypeError(
                "reduction must be WannierKineticDegenerateQuadraticReductionResult3D"
            )

    def _check_args_directions(self) -> None:
        """Require nonempty normalized dimensionless Cartesian directions."""
        if type(self.cartesian_directions) is not MatrixQuantity:
            raise TypeError("cartesian_directions must be MatrixQuantity")
        if not isinstance(self.cartesian_directions.unit, Unitless):
            raise ValueError("cartesian_directions must be unitless")
        if self.cartesian_directions.magnitude.ndim != 2 or (
            self.cartesian_directions.magnitude.shape[1] != 3
        ):
            raise ValueError("cartesian_directions must have shape (count, 3)")
        if self.cartesian_directions.magnitude.shape[0] == 0:
            raise ValueError("cartesian_directions must contain at least one row")
        if type(self.direction_absolute_tolerance) is not float:
            raise TypeError("direction_absolute_tolerance must be a built-in float")
        if (
            not np.isfinite(self.direction_absolute_tolerance)
            or self.direction_absolute_tolerance < 0.0
        ):
            raise ValueError(
                "direction_absolute_tolerance must be finite and nonnegative"
            )
        norms = np.linalg.norm(self.cartesian_directions.magnitude, axis=1)
        if np.any(np.abs(norms - 1.0) > self.direction_absolute_tolerance):
            raise ValueError("every Cartesian direction must have unit Euclidean norm")


@dataclass(frozen=True, slots=True)
class WannierKineticDegenerateQuadraticDirectionalContractionDiagnostics3D:
    """Retain the maximum directional-matrix anti-Hermitian defect."""

    antihermitian_maximum_frobenius: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate one nonnegative quadratic-unit defect."""
        if type(self.antihermitian_maximum_frobenius) is not ScalarQuantity:
            raise TypeError("antihermitian_maximum_frobenius must be ScalarQuantity")
        if self.antihermitian_maximum_frobenius.magnitude < 0.0:
            raise ValueError("antihermitian_maximum_frobenius must be nonnegative")


@dataclass(frozen=True, slots=True, eq=False)
class WannierKineticDegenerateQuadraticDirectionalContractionResult3D:
    """Retain one selected-space quadratic matrix for each Cartesian direction."""

    request: WannierKineticDegenerateQuadraticDirectionalContractionRequest3D
    matrices: tuple[ComplexMatrixQuantity, ...]
    diagnostics: WannierKineticDegenerateQuadraticDirectionalContractionDiagnostics3D

    def __post_init__(self) -> None:
        """Validate matrix types, units, shapes, values, and diagnostics."""
        self._check_args_types_and_matrices()
        self._check_args_construction()

    def _check_args_types_and_matrices(self) -> None:
        """Require one homogeneous selected-space quadratic-matrix family."""
        if type(self.request) is not (
            WannierKineticDegenerateQuadraticDirectionalContractionRequest3D
        ):
            raise TypeError(
                "request must be "
                "WannierKineticDegenerateQuadraticDirectionalContractionRequest3D"
            )
        if type(self.diagnostics) is not (
            WannierKineticDegenerateQuadraticDirectionalContractionDiagnostics3D
        ):
            raise TypeError(
                "diagnostics must be "
                "WannierKineticDegenerateQuadraticDirectionalContractionDiagnostics3D"
            )
        direction_count = self.request.cartesian_directions.magnitude.shape[0]
        rank = self.request.reduction.request.selected_rank
        quadratic_unit = self.request.reduction.effective_quadratic[0][0].unit
        if type(self.matrices) is not tuple or len(self.matrices) != direction_count:
            raise ValueError("matrices must contain one value per Cartesian direction")
        for matrix in self.matrices:
            if type(matrix) is not ComplexMatrixQuantity:
                raise TypeError("matrices must contain ComplexMatrixQuantity values")
            if matrix.magnitude.shape != (rank, rank):
                raise ValueError("directional matrix has the wrong selected rank")
            if matrix.unit != quadratic_unit:
                raise ValueError("directional matrix has the wrong quadratic unit")

    def _check_args_construction(self) -> None:
        """Require contractions and diagnostics to reproduce the request."""
        arrays, diagnostics = (
            WannierKineticDegenerateQuadraticDirectionalContractionConstructor3D._evaluate(
                self.request
            )
        )
        if any(
            not np.array_equal(matrix.magnitude, expected)
            for matrix, expected in zip(self.matrices, arrays, strict=True)
        ):
            raise ValueError("directional matrices do not match the request")
        if self.diagnostics != diagnostics:
            raise ValueError("directional diagnostics do not match the request")


class WannierKineticDegenerateQuadraticDirectionalContractionConstructor3D:
    """Contract a selected-space quadratic tensor along Cartesian directions."""

    __slots__ = ()

    def execute(
        self,
        request: WannierKineticDegenerateQuadraticDirectionalContractionRequest3D,
    ) -> WannierKineticDegenerateQuadraticDirectionalContractionResult3D:
        """Return one quadratic-unit matrix for each normalized direction."""
        if type(request) is not (
            WannierKineticDegenerateQuadraticDirectionalContractionRequest3D
        ):
            raise TypeError(
                "request must be "
                "WannierKineticDegenerateQuadraticDirectionalContractionRequest3D"
            )
        arrays, diagnostics = self._evaluate(request)
        quadratic_unit = request.reduction.effective_quadratic[0][0].unit
        if not isinstance(quadratic_unit, PhysicalUnit):
            raise ValueError("quadratic tensor must use a physical unit")
        return WannierKineticDegenerateQuadraticDirectionalContractionResult3D(
            request=request,
            matrices=tuple(
                ComplexMatrixQuantity(matrix, quadratic_unit) for matrix in arrays
            ),
            diagnostics=diagnostics,
        )

    @staticmethod
    def _evaluate(
        request: WannierKineticDegenerateQuadraticDirectionalContractionRequest3D,
    ) -> tuple[
        ComplexArray,
        WannierKineticDegenerateQuadraticDirectionalContractionDiagnostics3D,
    ]:
        """Contract the effective quadratic tensor with normalized directions."""
        directions = request.cartesian_directions.magnitude
        quadratic = np.asarray(
            [
                [matrix.magnitude for matrix in row]
                for row in request.reduction.effective_quadratic
            ]
        )
        matrices = np.asarray(
            [
                np.einsum(
                    "a,b,abij->ij",
                    direction,
                    direction,
                    quadratic,
                    optimize=True,
                )
                for direction in directions
            ]
        )
        quadratic_unit = request.reduction.effective_quadratic[0][0].unit
        diagnostics_type = (
            WannierKineticDegenerateQuadraticDirectionalContractionDiagnostics3D
        )
        diagnostics = diagnostics_type(
            antihermitian_maximum_frobenius=ScalarQuantity(
                WannierKineticDegenerateQuadraticReductionConstructor3D._antihermitian_defect(
                    matrices
                ),
                quadratic_unit,
            )
        )
        return matrices, diagnostics


__all__ = [
    "WannierKineticDegenerateQuadraticDirectionalContractionConstructor3D",
    "WannierKineticDegenerateQuadraticDirectionalContractionDiagnostics3D",
    "WannierKineticDegenerateQuadraticDirectionalContractionRequest3D",
    "WannierKineticDegenerateQuadraticDirectionalContractionResult3D",
    "WannierKineticDegenerateQuadraticModelEvaluationDiagnostics3D",
    "WannierKineticDegenerateQuadraticModelEvaluationRequest3D",
    "WannierKineticDegenerateQuadraticModelEvaluationResult3D",
    "WannierKineticDegenerateQuadraticModelEvaluator3D",
    "WannierKineticDegenerateQuadraticReductionConstructor3D",
    "WannierKineticDegenerateQuadraticReductionDiagnostics3D",
    "WannierKineticDegenerateQuadraticReductionRequest3D",
    "WannierKineticDegenerateQuadraticReductionResult3D",
]
