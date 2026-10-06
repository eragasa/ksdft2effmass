from __future__ import annotations

from dataclasses import replace

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
from ksdft2effmass.solid_state import (
    WannierKineticDegenerateQuadraticDirectionalContractionConstructor3D,
    WannierKineticDegenerateQuadraticDirectionalContractionRequest3D,
    WannierKineticDegenerateQuadraticModelEvaluationRequest3D,
    WannierKineticDegenerateQuadraticModelEvaluator3D,
    WannierKineticDegenerateQuadraticReductionConstructor3D,
    WannierKineticDegenerateQuadraticReductionRequest3D,
    WannierOperatorRole,
    WannierRepresentedOperatorCartesianDerivativeConstructor3D,
    WannierRepresentedOperatorCartesianDerivativeRequest3D,
    WannierRepresentedOperatorMesh3D,
    WignerSeitzInterpolationInventory3D,
)


@pytest.mark.software_verification
class TestWannierKineticDegenerateQuadraticReductionConstructor3D:
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
    def _request(cls) -> WannierKineticDegenerateQuadraticReductionRequest3D:
        kinetic_gradient = np.zeros((3, 3), dtype=np.complex128)
        kinetic_gradient[0, 1] = kinetic_gradient[1, 0] = 1.0
        remainder_gradient = np.zeros((3, 3), dtype=np.complex128)
        remainder_gradient[0, 2] = remainder_gradient[2, 0] = 2.0
        hamiltonian_gradient = kinetic_gradient + remainder_gradient
        kinetic_zero = np.eye(3, dtype=np.complex128)
        hamiltonian_zero = np.diag((0.0, 2.0, 2.0)).astype(np.complex128)
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
        return WannierKineticDegenerateQuadraticReductionRequest3D(
            hamiltonian_derivatives=derivatives["hamiltonian"],
            kinetic_derivatives=derivatives["kinetic"],
            nonkinetic_remainder_derivatives=derivatives["remainder"],
            selected_eigenvalue_indices=(1, 2),
            reference_energy=ScalarQuantity(2.0, PhysicalUnit("eV")),
            degeneracy_absolute_tolerance=ScalarQuantity(1.0e-12, PhysicalUnit("eV")),
            covariance_probe_gauge=ComplexMatrixQuantity(gauge, Unitless()),
            frame_absolute_tolerance=1.0e-12,
        )

    def test_constructs_remote_partition_and_covariant_quadratic_tensor(self) -> None:
        result = WannierKineticDegenerateQuadraticReductionConstructor3D().execute(
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

    def test_evaluates_offsets_and_directional_quadratic_contractions(self) -> None:
        reduction = WannierKineticDegenerateQuadraticReductionConstructor3D().execute(
            self._request()
        )

        evaluated = WannierKineticDegenerateQuadraticModelEvaluator3D().execute(
            WannierKineticDegenerateQuadraticModelEvaluationRequest3D(
                reduction,
                MatrixQuantity(
                    np.asarray(((0.1, 0.0, 0.0), (0.0, 0.2, 0.0))),
                    PhysicalUnit("1 / bohr"),
                ),
            )
        )
        contraction = (
            WannierKineticDegenerateQuadraticDirectionalContractionConstructor3D()
        )
        directional = contraction.execute(
            WannierKineticDegenerateQuadraticDirectionalContractionRequest3D(
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
            np.zeros((2, 2), dtype=np.complex128), evaluated.matrices[0].unit
        )
        with pytest.raises(ValueError, match="evaluated matrices do not match"):
            replace(evaluated, matrices=(corrupted, *evaluated.matrices[1:]))

    def test_rejects_nonunit_directional_contraction_vector(self) -> None:
        reduction = WannierKineticDegenerateQuadraticReductionConstructor3D().execute(
            self._request()
        )

        with pytest.raises(ValueError, match="unit Euclidean norm"):
            WannierKineticDegenerateQuadraticDirectionalContractionRequest3D(
                reduction,
                MatrixQuantity(np.asarray(((2.0, 0.0, 0.0),)), Unitless()),
                1.0e-14,
            )

    def test_rejects_selection_outside_explicit_degeneracy_tolerance(self) -> None:
        request = replace(
            self._request(), reference_energy=ScalarQuantity(3.0, PhysicalUnit("eV"))
        )

        with pytest.raises(ValueError, match="outside degeneracy tolerance"):
            WannierKineticDegenerateQuadraticReductionConstructor3D().execute(request)

    def test_result_rejects_corrupted_effective_tensor(self) -> None:
        result = WannierKineticDegenerateQuadraticReductionConstructor3D().execute(
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

        with pytest.raises(ValueError, match="tensor does not match"):
            replace(result, effective_quadratic=corrupted_tensor)
