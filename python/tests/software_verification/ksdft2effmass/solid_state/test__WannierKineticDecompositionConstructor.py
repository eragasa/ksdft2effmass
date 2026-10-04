from __future__ import annotations

from dataclasses import replace
from typing import cast

import numpy as np
import pytest

from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    MatrixQuantity,
    PhysicalUnit,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.solid_state import (
    PlaneWaveBandSample,
    WannierFrameSample,
    WannierKineticDecompositionConstructor,
    WannierKineticDecompositionRequest,
    WannierOperatorRole,
)


@pytest.mark.software_verification
class TestWannierKineticDecompositionConstructor:
    """Establish same-frame projection, subtraction, and Fourier behavior."""

    @staticmethod
    def _request(
        *,
        fractional_kpoints: np.ndarray,
        mesh_shape: tuple[int, int, int],
        kinetic_values: tuple[np.ndarray, ...],
        eigenvalues: tuple[np.ndarray, ...],
        disentanglements: tuple[np.ndarray, ...],
        gauges: tuple[np.ndarray, ...],
        coefficients: tuple[np.ndarray, ...] | None = None,
        frame_absolute_tolerance: float = 1.0e-12,
    ) -> WannierKineticDecompositionRequest:
        unit = PhysicalUnit("eV")
        if coefficients is None:
            coefficients = tuple(
                np.eye(values.size, dtype=np.complex128) for values in eigenvalues
            )
        return WannierKineticDecompositionRequest(
            source_binding_identifier="synthetic-parent",
            frame_identifier="synthetic-wannier-frame",
            energy_reference="synthetic-zero",
            hamiltonian_identifier="synthetic-HW",
            kinetic_identifier="synthetic-TW",
            nonkinetic_remainder_identifier="synthetic-nonkinetic-remainder",
            fractional_kpoints=MatrixQuantity(fractional_kpoints, Unitless()),
            mesh_shape=mesh_shape,
            plane_wave_samples=tuple(
                PlaneWaveBandSample(
                    ComplexMatrixQuantity(coefficient, Unitless()),
                    VectorQuantity(kinetic, unit),
                )
                for coefficient, kinetic in zip(
                    coefficients, kinetic_values, strict=True
                )
            ),
            frame_samples=tuple(
                WannierFrameSample(
                    VectorQuantity(spectrum, unit),
                    ComplexMatrixQuantity(disentanglement, Unitless()),
                    ComplexMatrixQuantity(gauge, Unitless()),
                )
                for spectrum, disentanglement, gauge in zip(
                    eigenvalues, disentanglements, gauges, strict=True
                )
            ),
            output_energy_unit=unit,
            coordinate_absolute_tolerance=1.0e-14,
            frame_absolute_tolerance=frame_absolute_tolerance,
            diagnostic_absolute_tolerance=1.0e-12,
        )

    def test_constructs_one_point_same_frame_decomposition(self) -> None:
        phase = np.exp(0.37j)
        request = self._request(
            fractional_kpoints=np.asarray([[0.0, 0.0, 0.0]]),
            mesh_shape=(1, 1, 1),
            kinetic_values=(np.asarray([1.0, 2.0]),),
            eigenvalues=(np.asarray([4.0, 5.0]),),
            disentanglements=(
                np.asarray([[2.0**-0.5], [2.0**-0.5]], dtype=np.complex128),
            ),
            gauges=(np.asarray([[phase]], dtype=np.complex128),),
        )

        result = WannierKineticDecompositionConstructor().execute(request)

        assert result.hamiltonian.role is WannierOperatorRole.HAMILTONIAN
        assert result.kinetic.role is WannierOperatorRole.KINETIC
        assert (
            result.nonkinetic_remainder.role is WannierOperatorRole.NONKINETIC_REMAINDER
        )
        np.testing.assert_allclose(
            result.hamiltonian.reciprocal_matrices[0].magnitude,
            np.asarray([[4.5]]),
            rtol=0.0,
            atol=1.0e-14,
        )
        np.testing.assert_allclose(
            result.kinetic.reciprocal_matrices[0].magnitude,
            np.asarray([[1.5]]),
            rtol=0.0,
            atol=1.0e-14,
        )
        np.testing.assert_allclose(
            result.nonkinetic_remainder.reciprocal_matrices[0].magnitude,
            np.asarray([[3.0]]),
            rtol=0.0,
            atol=1.0e-14,
        )
        assert result.hamiltonian.representatives == ((0, 0, 0),)
        assert result.diagnostics.passes

    def test_composes_nontrivial_multistate_frame_and_parent_kinetic(self) -> None:
        inverse_sqrt_two = 2.0**-0.5
        coefficients = np.asarray(
            (
                (inverse_sqrt_two, 0.0, 1j * inverse_sqrt_two),
                (1j * inverse_sqrt_two, 0.0, inverse_sqrt_two),
                (0.0, 1.0, 0.0),
            ),
            dtype=np.complex128,
        )
        disentanglement = np.asarray(
            ((1.0, 0.0), (0.0, 0.0), (0.0, 1.0)), dtype=np.complex128
        )
        gauge = np.asarray(
            (
                (inverse_sqrt_two, 1j * inverse_sqrt_two),
                (1j * inverse_sqrt_two, inverse_sqrt_two),
            ),
            dtype=np.complex128,
        )
        request = self._request(
            fractional_kpoints=np.asarray([[0.0, 0.0, 0.0]]),
            mesh_shape=(1, 1, 1),
            kinetic_values=(np.asarray([1.0, 3.0, 5.0]),),
            eigenvalues=(np.asarray([4.0, 100.0, 8.0]),),
            disentanglements=(disentanglement,),
            gauges=(gauge,),
            coefficients=(coefficients,),
        )

        result = WannierKineticDecompositionConstructor().execute(request)

        np.testing.assert_allclose(
            result.hamiltonian.reciprocal_matrices[0].magnitude,
            np.asarray(((6.0, -2.0j), (2.0j, 6.0))),
            rtol=0.0,
            atol=2.0e-15,
        )
        np.testing.assert_allclose(
            result.kinetic.reciprocal_matrices[0].magnitude,
            np.asarray(((3.0, 0.0), (0.0, 1.0))),
            rtol=0.0,
            atol=2.0e-15,
        )
        np.testing.assert_allclose(
            result.nonkinetic_remainder.reciprocal_matrices[0].magnitude,
            np.asarray(((3.0, -2.0j), (2.0j, 5.0))),
            rtol=0.0,
            atol=2.0e-15,
        )

    def test_uses_centered_canonical_lattice_representatives(self) -> None:
        request = self._request(
            fractional_kpoints=np.asarray([[0.0, 0.0, 0.0], [0.5, 0.0, 0.0]]),
            mesh_shape=(2, 1, 1),
            kinetic_values=(np.asarray([1.0]), np.asarray([3.0])),
            eigenvalues=(np.asarray([4.0]), np.asarray([8.0])),
            disentanglements=(
                np.asarray([[1.0 + 0.0j]]),
                np.asarray([[1.0 + 0.0j]]),
            ),
            gauges=(
                np.asarray([[1.0 + 0.0j]]),
                np.asarray([[1.0 + 0.0j]]),
            ),
        )

        result = WannierKineticDecompositionConstructor().execute(request)

        assert result.hamiltonian.representatives == ((-1, 0, 0), (0, 0, 0))
        np.testing.assert_allclose(
            [block.magnitude[0, 0] for block in result.hamiltonian.lattice_blocks],
            [-2.0, 6.0],
            rtol=0.0,
            atol=1.0e-14,
        )
        np.testing.assert_allclose(
            [block.magnitude[0, 0] for block in result.kinetic.lattice_blocks],
            [-1.0, 2.0],
            rtol=0.0,
            atol=1.0e-14,
        )
        np.testing.assert_allclose(
            [
                block.magnitude[0, 0]
                for block in result.nonkinetic_remainder.lattice_blocks
            ],
            [-1.0, 4.0],
            rtol=0.0,
            atol=1.0e-14,
        )
        assert result.diagnostics.passes

    def test_three_point_transform_uses_negative_forward_phase(self) -> None:
        request = self._request(
            fractional_kpoints=np.asarray(
                ((0.0, 0.0, 0.0), (1.0 / 3.0, 0.0, 0.0), (2.0 / 3.0, 0.0, 0.0))
            ),
            mesh_shape=(3, 1, 1),
            kinetic_values=(np.asarray([0.0]),) * 3,
            eigenvalues=(np.asarray([1.0]), np.asarray([2.0]), np.asarray([4.0])),
            disentanglements=(np.asarray([[1.0 + 0.0j]]),) * 3,
            gauges=(np.asarray([[1.0 + 0.0j]]),) * 3,
        )

        result = WannierKineticDecompositionConstructor().execute(request)

        assert result.hamiltonian.representatives == (
            (-1, 0, 0),
            (0, 0, 0),
            (1, 0, 0),
        )
        expected = np.asarray(
            (
                -2.0 / 3.0 - 1j / np.sqrt(3.0),
                7.0 / 3.0,
                -2.0 / 3.0 + 1j / np.sqrt(3.0),
            )
        )
        np.testing.assert_allclose(
            [block.magnitude[0, 0] for block in result.hamiltonian.lattice_blocks],
            expected,
            rtol=0.0,
            atol=5.0e-16,
        )

    def test_rejects_nonenergy_units(self) -> None:
        with pytest.raises(ValueError, match="physical energy unit"):
            PlaneWaveBandSample(
                ComplexMatrixQuantity(np.eye(1, dtype=np.complex128), Unitless()),
                VectorQuantity(np.ones(1), PhysicalUnit("meter")),
            )
        with pytest.raises(ValueError, match="physical energy unit"):
            WannierFrameSample(
                VectorQuantity(np.ones(1), PhysicalUnit("meter")),
                ComplexMatrixQuantity(np.eye(1, dtype=np.complex128), Unitless()),
                ComplexMatrixQuantity(np.eye(1, dtype=np.complex128), Unitless()),
            )
        request = self._request(
            fractional_kpoints=np.asarray([[0.0, 0.0, 0.0]]),
            mesh_shape=(1, 1, 1),
            kinetic_values=(np.asarray([1.0]),),
            eigenvalues=(np.asarray([4.0]),),
            disentanglements=(np.asarray([[1.0 + 0.0j]]),),
            gauges=(np.asarray([[1.0 + 0.0j]]),),
        )
        with pytest.raises(ValueError, match="physical energy unit"):
            replace(request, output_energy_unit=PhysicalUnit("meter"))

    def test_result_rejects_corrupted_values_or_diagnostics(self) -> None:
        request = self._request(
            fractional_kpoints=np.asarray([[0.0, 0.0, 0.0]]),
            mesh_shape=(1, 1, 1),
            kinetic_values=(np.asarray([1.0]),),
            eigenvalues=(np.asarray([4.0]),),
            disentanglements=(np.asarray([[1.0 + 0.0j]]),),
            gauges=(np.asarray([[1.0 + 0.0j]]),),
        )
        result = WannierKineticDecompositionConstructor().execute(request)
        corrupted_matrix = ComplexMatrixQuantity(
            np.asarray([[5.0 + 0.0j]]), request.output_energy_unit
        )
        with pytest.raises(ValueError, match="canonical Fourier transform"):
            replace(
                result.hamiltonian,
                reciprocal_matrices=(corrupted_matrix,),
            )
        corrupted_diagnostics = replace(
            result.diagnostics,
            hamiltonian_hermiticity_maximum_frobenius=1.0,
        )
        with pytest.raises(ValueError, match="diagnostic is inconsistent"):
            replace(result, diagnostics=corrupted_diagnostics)

    def test_rejects_nonisometric_disentanglement(self) -> None:
        with pytest.raises(ValueError, match="isometric frame"):
            self._request(
                fractional_kpoints=np.asarray([[0.0, 0.0, 0.0]]),
                mesh_shape=(1, 1, 1),
                kinetic_values=(np.asarray([1.0, 2.0]),),
                eigenvalues=(np.asarray([4.0, 5.0]),),
                disentanglements=(np.asarray([[1.0], [1.0]]),),
                gauges=(np.asarray([[1.0 + 0.0j]]),),
            )

    def test_rejects_kpoints_outside_declared_mesh_order(self) -> None:
        with pytest.raises(ValueError, match="half-open mesh order"):
            self._request(
                fractional_kpoints=np.asarray([[0.5, 0.0, 0.0], [0.0, 0.0, 0.0]]),
                mesh_shape=(2, 1, 1),
                kinetic_values=(np.asarray([1.0]), np.asarray([3.0])),
                eigenvalues=(np.asarray([4.0]), np.asarray([8.0])),
                disentanglements=(
                    np.asarray([[1.0 + 0.0j]]),
                    np.asarray([[1.0 + 0.0j]]),
                ),
                gauges=(
                    np.asarray([[1.0 + 0.0j]]),
                    np.asarray([[1.0 + 0.0j]]),
                ),
            )

    def test_rejects_boolean_or_integer_tolerance(self) -> None:
        request = self._request(
            fractional_kpoints=np.asarray([[0.0, 0.0, 0.0]]),
            mesh_shape=(1, 1, 1),
            kinetic_values=(np.asarray([1.0]),),
            eigenvalues=(np.asarray([4.0]),),
            disentanglements=(np.asarray([[1.0 + 0.0j]]),),
            gauges=(np.asarray([[1.0 + 0.0j]]),),
        )
        with pytest.raises(TypeError, match="built-in float"):
            replace(request, diagnostic_absolute_tolerance=cast(float, 1))
