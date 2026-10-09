"""Software verification for a finite Löwdin quadratic effective Hamiltonian.

Synthetic three-state derivative tensors provide analytic projection, remote-term,
Hermiticity, covariance, evaluation, and directional-contraction oracles in declared
eV/bohr units. Comparisons use explicit absolute tolerances; rejection, corruption,
and fail-closed public construction checks are exact. The evidence does not identify
a physical band group, establish convergence, validate effective masses, quantify
uncertainty, or imply
scientific acceptance.
"""

from __future__ import annotations

from dataclasses import replace
from inspect import signature
from unittest.mock import patch

import numpy as np
import pytest

from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    MatrixQuantity,
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.solid_state.hamiltonians.effective.lowdin_quadratic.contraction import (  # noqa: E501
    WannierKineticLowdinQuadraticDirectionalContractionConstructor3D,
    WannierKineticLowdinQuadraticDirectionalContractionRequest3D,
    WannierKineticLowdinQuadraticDirectionalContractionResult3D,
)
from ksdft2effmass.solid_state.hamiltonians.effective.lowdin_quadratic.evaluation import (  # noqa: E501
    WannierKineticLowdinQuadraticModelEvaluationRequest3D,
    WannierKineticLowdinQuadraticModelEvaluationResult3D,
    WannierKineticLowdinQuadraticModelEvaluator3D,
)
from ksdft2effmass.solid_state.hamiltonians.effective.lowdin_quadratic.reduction import (  # noqa: E501
    WannierKineticLowdinQuadraticReductionConstructor3D,
    WannierKineticLowdinQuadraticReductionRequest3D,
    WannierKineticLowdinQuadraticReductionResult3D,
)
from ksdft2effmass.solid_state.wannier_kinetic import (
    WannierOperatorRole,
    WannierRepresentedOperatorMesh3D,
)
from ksdft2effmass.solid_state.wignerseitz.interpolation import (
    WannierRepresentedOperatorCartesianDerivativeConstructor3D,
    WannierRepresentedOperatorCartesianDerivativeRequest3D,
    WignerSeitzInterpolationInventory3D,
)


@pytest.mark.software_verification
class TestWannierKineticLowdinQuadraticReductionConstructor3D:
    """Establish explicit selected-space projection and remote-term partitioning."""

    @staticmethod
    def _source(
        identifier: str,
        role: WannierOperatorRole,
        centered_blocks: np.ndarray,
    ) -> WannierRepresentedOperatorMesh3D:
        unit = PhysicalUnit("eV")
        centered = centered_blocks.reshape((3, 1, 1, 3, 3))
        reciprocal = np.fft.ifftn(
            np.fft.ifftshift(centered, axes=(0, 1, 2)),
            axes=(0, 1, 2),
            norm="forward",
        )
        retained_blocks = np.fft.fftshift(
            np.fft.fftn(reciprocal, axes=(0, 1, 2), norm="forward"),
            axes=(0, 1, 2),
        )
        return WannierRepresentedOperatorMesh3D(
            identifier=identifier,
            role=role,
            source_binding_identifier="synthetic-source",
            frame_identifier="synthetic-frame",
            energy_reference="synthetic-zero",
            fractional_kpoints=MatrixQuantity(
                np.asarray(
                    ((0.0, 0.0, 0.0), (1.0 / 3.0, 0.0, 0.0), (2.0 / 3.0, 0.0, 0.0))
                ),
                Unitless(),
            ),
            mesh_shape=(3, 1, 1),
            coordinate_absolute_tolerance=1.0e-14,
            reciprocal_matrices=tuple(
                ComplexMatrixQuantity(matrix, unit)
                for matrix in reciprocal.reshape((-1, 3, 3))
            ),
            representatives=((-1, 0, 0), (0, 0, 0), (1, 0, 0)),
            lattice_blocks=tuple(
                ComplexMatrixQuantity(matrix, unit)
                for matrix in retained_blocks.reshape((-1, 3, 3))
            ),
        )

    @staticmethod
    def _inventory() -> WignerSeitzInterpolationInventory3D:
        return WignerSeitzInterpolationInventory3D(
            identifier="synthetic-inventory",
            source_binding_identifier="synthetic-source",
            mesh_shape=(3, 1, 1),
            direct_lattice=MatrixQuantity(np.eye(3), PhysicalUnit("bohr")),
            representatives=((-1, 0, 0), (0, 0, 0), (1, 0, 0)),
            degeneracies=(1, 1, 1),
        )

    @classmethod
    def _request(
        cls,
        *,
        hamiltonian_upper_offdiagonal: float = 0.0,
        hamiltonian_selected_upper_offdiagonal: float = 0.0,
        hamiltonian_hermiticity_tolerance: float = 1.0e-12,
    ) -> WannierKineticLowdinQuadraticReductionRequest3D:
        """Return a synthetic request with a controlled Hamiltonian defect."""
        kinetic_gradient = np.zeros((3, 3), dtype=np.complex128)
        kinetic_gradient[0, 1] = kinetic_gradient[1, 0] = 1.0
        remainder_gradient = np.zeros((3, 3), dtype=np.complex128)
        remainder_gradient[0, 2] = remainder_gradient[2, 0] = 2.0
        hamiltonian_gradient = kinetic_gradient + remainder_gradient
        kinetic_zero = np.eye(3, dtype=np.complex128)
        hamiltonian_zero = np.diag((0.0, 2.0, 2.0)).astype(np.complex128)
        hamiltonian_zero[0, 1] = hamiltonian_upper_offdiagonal
        hamiltonian_zero[1, 2] = hamiltonian_selected_upper_offdiagonal
        remainder_zero = hamiltonian_zero - kinetic_zero

        def blocks(value: np.ndarray, gradient: np.ndarray) -> np.ndarray:
            positive = -0.5j * gradient
            return np.asarray((positive.conj().T, value, positive))

        inventory = cls._inventory()
        constructor = WannierRepresentedOperatorCartesianDerivativeConstructor3D()
        coordinate = VectorQuantity(np.zeros(3), Unitless())
        derivatives = {}
        for name, role, value, gradient in (
            (
                "hamiltonian",
                WannierOperatorRole.HAMILTONIAN,
                hamiltonian_zero,
                hamiltonian_gradient,
            ),
            ("kinetic", WannierOperatorRole.KINETIC, kinetic_zero, kinetic_gradient),
            (
                "remainder",
                WannierOperatorRole.NONKINETIC_REMAINDER,
                remainder_zero,
                remainder_gradient,
            ),
        ):
            derivatives[name] = constructor.execute(
                WannierRepresentedOperatorCartesianDerivativeRequest3D(
                    cls._source(f"synthetic-{name}", role, blocks(value, gradient)),
                    inventory,
                    coordinate,
                )
            )
        gauge = np.asarray(((1.0, 1.0j), (1.0j, 1.0)), dtype=np.complex128) / np.sqrt(
            2.0
        )
        return WannierKineticLowdinQuadraticReductionRequest3D(
            hamiltonian_derivatives=derivatives["hamiltonian"],
            kinetic_derivatives=derivatives["kinetic"],
            nonkinetic_remainder_derivatives=derivatives["remainder"],
            selected_eigenvalue_indices=(1, 2),
            reference_energy=ScalarQuantity(2.0, PhysicalUnit("eV")),
            degeneracy_absolute_tolerance=ScalarQuantity(1.0e-12, PhysicalUnit("eV")),
            hamiltonian_hermiticity_absolute_tolerance=ScalarQuantity(
                hamiltonian_hermiticity_tolerance,
                PhysicalUnit("eV"),
            ),
            covariance_probe_gauge=ComplexMatrixQuantity(gauge, Unitless()),
            frame_absolute_tolerance=1.0e-12,
        )

    def test_constructs_remote_partition_and_covariant_quadratic_tensor(self) -> None:
        result = WannierKineticLowdinQuadraticReductionConstructor3D().execute(
            self._request()
        )

        effective_xx = result.effective_quadratic[0][0].magnitude
        remote_tt_xx = result.remote_kinetic_kinetic[0][0].magnitude
        remote_rr_xx = result.remote_remainder_remainder[0][0].magnitude
        remote_cross_xx = result.remote_cross[0][0].magnitude
        np.testing.assert_allclose(
            effective_xx, ((1.0, 2.0), (2.0, 4.0)), rtol=0.0, atol=1.0e-13
        )
        np.testing.assert_allclose(
            remote_tt_xx, ((1.0, 0.0), (0.0, 0.0)), rtol=0.0, atol=1.0e-13
        )
        np.testing.assert_allclose(
            remote_rr_xx, ((0.0, 0.0), (0.0, 4.0)), rtol=0.0, atol=1.0e-13
        )
        np.testing.assert_allclose(
            remote_cross_xx, ((0.0, 2.0), (2.0, 0.0)), rtol=0.0, atol=1.0e-13
        )
        assert (
            result.diagnostics.remote_partition_decomposition_maximum_frobenius.magnitude
            < 1.0e-13
        )
        assert (
            result.diagnostics.basis_covariance_quadratic_maximum_frobenius.magnitude
            < 1.0e-13
        )
        assert result.diagnostics.complement_minimum_separation.magnitude == 2.0
        assert (
            result.diagnostics.hamiltonian_hermitian_projection_correction_frobenius.magnitude
            == 0.0
        )

    def test_execute_rejects_hamiltonian_outside_hermiticity_tolerance(self) -> None:
        """A non-Hermitian input cannot define the declared Löwdin eigenspace."""
        request = self._request(
            hamiltonian_upper_offdiagonal=1.0e-3,
            hamiltonian_hermiticity_tolerance=1.0e-12,
        )

        with pytest.raises(
            ValueError,
            match="Hermitian eigenspace.*not mathematically defined",
        ):
            WannierKineticLowdinQuadraticReductionConstructor3D().execute(request)

    def test_execute_records_within_tolerance_hermitian_projection(self) -> None:
        """An accepted roundoff-scale projection retains its Frobenius correction."""
        defect_entry = 1.0e-13
        request = self._request(
            hamiltonian_upper_offdiagonal=defect_entry,
            hamiltonian_hermiticity_tolerance=2.0e-13,
        )

        result = WannierKineticLowdinQuadraticReductionConstructor3D().execute(request)

        assert (
            result.diagnostics.hamiltonian_hermitian_projection_correction_frobenius.magnitude
            == pytest.approx(defect_entry / np.sqrt(2.0), rel=0.0, abs=1.0e-28)
        )
        assert np.array_equal(
            result.projected_hamiltonian_value.magnitude,
            result.projected_hamiltonian_value.magnitude.conj().T,
        )

    def test_projected_selected_defect_is_not_reported_as_covariance_error(
        self,
    ) -> None:
        """Both covariance gauges use the same accepted Hermitian projection."""
        defect_entry = 1.0e-13
        result = WannierKineticLowdinQuadraticReductionConstructor3D().execute(
            self._request(
                hamiltonian_selected_upper_offdiagonal=defect_entry,
                hamiltonian_hermiticity_tolerance=2.0e-13,
            )
        )

        assert (
            result.diagnostics.hamiltonian_hermitian_projection_correction_frobenius.magnitude
            == pytest.approx(defect_entry / np.sqrt(2.0), rel=0.0, abs=1.0e-28)
        )
        assert (
            result.diagnostics.basis_covariance_base_maximum_frobenius.magnitude
            < 2.0e-15
        )

    def test_execute_solves_once_without_a_result_witness(self) -> None:
        """The Action owns one eigensolve and Result has no witness input."""
        with patch(
            "ksdft2effmass.solid_state.hamiltonians.effective.lowdin_quadratic.reduction.np.linalg.eigh",
            wraps=np.linalg.eigh,
        ) as eigh:
            WannierKineticLowdinQuadraticReductionConstructor3D().execute(
                self._request()
            )

        assert eigh.call_count == 1
        assert (
            "_evaluation"
            not in signature(WannierKineticLowdinQuadraticReductionResult3D).parameters
        )

    def test_result_rejects_forged_spectral_and_projection_diagnostics(self) -> None:
        """Spectral and accepted-Hamiltonian diagnostics remain value-correlated."""
        result = WannierKineticLowdinQuadraticReductionConstructor3D().execute(
            self._request()
        )
        names = (
            "selected_group_maximum_splitting",
            "complement_minimum_separation",
            "hamiltonian_hermitian_projection_correction_frobenius",
        )

        for name in names:
            diagnostic = getattr(result.diagnostics, name)
            forged = replace(
                result.diagnostics,
                **{name: ScalarQuantity(diagnostic.magnitude + 1.0, diagnostic.unit)},
            )
            with pytest.raises(ValueError, match=name):
                replace(result, diagnostics=forged)

    def test_result_rejects_forged_input_closure_diagnostics(self) -> None:
        """Input value and derivative closure diagnostics remain correlated."""
        result = WannierKineticLowdinQuadraticReductionConstructor3D().execute(
            self._request()
        )
        names = (
            "value_decomposition_frobenius",
            "gradient_decomposition_maximum_frobenius",
            "direct_hessian_decomposition_maximum_frobenius",
        )

        for name in names:
            diagnostic = getattr(result.diagnostics, name)
            forged = replace(
                result.diagnostics,
                **{name: ScalarQuantity(diagnostic.magnitude + 1.0, diagnostic.unit)},
            )
            with pytest.raises(ValueError, match=name):
                replace(result, diagnostics=forged)

    def test_result_rejects_forged_remote_and_hermiticity_diagnostics(self) -> None:
        """Remote partition and effective Hermiticity diagnostics remain correlated."""
        result = WannierKineticLowdinQuadraticReductionConstructor3D().execute(
            self._request()
        )
        names = (
            "remote_partition_decomposition_maximum_frobenius",
            "effective_quadratic_antihermitian_maximum_frobenius",
        )

        for name in names:
            diagnostic = getattr(result.diagnostics, name)
            forged = replace(
                result.diagnostics,
                **{name: ScalarQuantity(diagnostic.magnitude + 1.0, diagnostic.unit)},
            )
            with pytest.raises(ValueError, match=name):
                replace(result, diagnostics=forged)

    def test_result_rejects_forged_covariance_diagnostics(self) -> None:
        """Each covariance diagnostic remains correlated to retained probe tensors."""
        result = WannierKineticLowdinQuadraticReductionConstructor3D().execute(
            self._request()
        )
        names = (
            "basis_covariance_base_maximum_frobenius",
            "basis_covariance_gradient_maximum_frobenius",
            "basis_covariance_quadratic_maximum_frobenius",
        )

        for name in names:
            diagnostic = getattr(result.diagnostics, name)
            forged = replace(
                result.diagnostics,
                **{name: ScalarQuantity(diagnostic.magnitude + 1.0, diagnostic.unit)},
            )
            with pytest.raises(ValueError, match=name):
                replace(result, diagnostics=forged)

    def test_result_rejects_wrong_units_for_every_diagnostic(self) -> None:
        """Every retained diagnostic enforces its owned physical dimension."""
        result = WannierKineticLowdinQuadraticReductionConstructor3D().execute(
            self._request()
        )

        for name in result.diagnostics.__dataclass_fields__:
            diagnostic = getattr(result.diagnostics, name)
            forged = replace(
                result.diagnostics,
                **{name: ScalarQuantity(diagnostic.magnitude, Unitless())},
            )
            with pytest.raises(ValueError, match=name):
                replace(result, diagnostics=forged)

    def test_execute_evaluates_each_downstream_action_once(self) -> None:
        """Downstream Actions own one numerical pass without Result witnesses."""
        reduction = WannierKineticLowdinQuadraticReductionConstructor3D().execute(
            self._request()
        )
        evaluation_request = WannierKineticLowdinQuadraticModelEvaluationRequest3D(
            reduction,
            MatrixQuantity(np.asarray(((0.1, 0.0, 0.0),)), PhysicalUnit("1 / bohr")),
        )
        direction_request = (
            WannierKineticLowdinQuadraticDirectionalContractionRequest3D(
                reduction,
                MatrixQuantity(np.asarray(((1.0, 0.0, 0.0),)), Unitless()),
                1.0e-14,
            )
        )

        with patch(
            "ksdft2effmass.solid_state.hamiltonians.effective.lowdin_quadratic.evaluation.np.einsum",
            wraps=np.einsum,
        ) as model_einsum:
            WannierKineticLowdinQuadraticModelEvaluator3D().execute(evaluation_request)
        with patch(
            "ksdft2effmass.solid_state.hamiltonians.effective.lowdin_quadratic.contraction.np.einsum",
            wraps=np.einsum,
        ) as direction_einsum:
            WannierKineticLowdinQuadraticDirectionalContractionConstructor3D().execute(
                direction_request
            )

        assert model_einsum.call_count == 2
        assert direction_einsum.call_count == 1
        assert (
            "_evaluation"
            not in signature(
                WannierKineticLowdinQuadraticModelEvaluationResult3D
            ).parameters
        )
        assert (
            "_evaluation"
            not in signature(
                WannierKineticLowdinQuadraticDirectionalContractionResult3D
            ).parameters
        )

    def test_evaluates_offsets_and_directional_quadratic_contractions(self) -> None:
        reduction = WannierKineticLowdinQuadraticReductionConstructor3D().execute(
            self._request()
        )

        evaluated = WannierKineticLowdinQuadraticModelEvaluator3D().execute(
            WannierKineticLowdinQuadraticModelEvaluationRequest3D(
                reduction,
                MatrixQuantity(
                    np.asarray(((0.1, 0.0, 0.0), (0.0, 0.2, 0.0))),
                    PhysicalUnit("1 / bohr"),
                ),
            )
        )
        contraction = WannierKineticLowdinQuadraticDirectionalContractionConstructor3D()
        directional = contraction.execute(
            WannierKineticLowdinQuadraticDirectionalContractionRequest3D(
                reduction,
                MatrixQuantity(
                    np.asarray(((1.0, 0.0, 0.0), (0.0, 1.0, 0.0))),
                    Unitless(),
                ),
                1.0e-14,
            )
        )

        np.testing.assert_allclose(
            evaluated.matrices[0].magnitude,
            ((2.005, 0.01), (0.01, 2.02)),
            rtol=0.0,
            atol=1.0e-13,
        )
        np.testing.assert_allclose(
            evaluated.matrices[1].magnitude,
            2.0 * np.eye(2),
            rtol=0.0,
            atol=1.0e-13,
        )
        np.testing.assert_allclose(
            directional.matrices[0].magnitude,
            ((1.0, 2.0), (2.0, 4.0)),
            rtol=0.0,
            atol=1.0e-13,
        )
        np.testing.assert_allclose(
            directional.matrices[1].magnitude,
            np.zeros((2, 2)),
            rtol=0.0,
            atol=1.0e-13,
        )
        assert evaluated.diagnostics.antihermitian_maximum_frobenius.magnitude < 1e-13
        assert directional.diagnostics.antihermitian_maximum_frobenius.magnitude < 1e-13
        corrupted = ComplexMatrixQuantity(
            1.0j * np.eye(2, dtype=np.complex128), evaluated.matrices[0].unit
        )
        with pytest.raises(ValueError, match="diagnostics do not match"):
            replace(evaluated, matrices=(corrupted, *evaluated.matrices[1:]))

    def test_rejects_nonunit_directional_contraction_vector(self) -> None:
        reduction = WannierKineticLowdinQuadraticReductionConstructor3D().execute(
            self._request()
        )

        with pytest.raises(ValueError, match="unit Euclidean norm"):
            WannierKineticLowdinQuadraticDirectionalContractionRequest3D(
                reduction,
                MatrixQuantity(np.asarray(((2.0, 0.0, 0.0),)), Unitless()),
                1.0e-14,
            )

    def test_rejects_selection_outside_explicit_degeneracy_tolerance(self) -> None:
        request = replace(
            self._request(), reference_energy=ScalarQuantity(3.0, PhysicalUnit("eV"))
        )

        with pytest.raises(ValueError, match="outside degeneracy tolerance"):
            WannierKineticLowdinQuadraticReductionConstructor3D().execute(request)

    def test_result_rejects_corrupted_effective_tensor(self) -> None:
        result = WannierKineticLowdinQuadraticReductionConstructor3D().execute(
            self._request()
        )
        corrupted = ComplexMatrixQuantity(
            np.zeros((2, 2), dtype=np.complex128),
            result.effective_quadratic[0][0].unit,
        )
        corrupted_tensor = (
            (corrupted, *result.effective_quadratic[0][1:]),
            *result.effective_quadratic[1:],
        )

        with pytest.raises(ValueError, match="direct plus remote"):
            replace(result, effective_quadratic=corrupted_tensor)
