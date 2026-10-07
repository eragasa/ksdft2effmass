"""Software verification for represented-operator Cartesian derivatives.

Synthetic scalar Wigner--Seitz blocks provide analytic value, gradient, Hessian, unit,
and decomposition oracles. Comparisons use explicit absolute tolerances; fail-closed
public construction and failure checks are exact. The evidence does not establish
derivative convergence, physical adequacy, scientific validation, uncertainty
quantification, or acceptance.
"""

from __future__ import annotations

from dataclasses import replace
from inspect import signature
from unittest.mock import patch

import numpy as np
import pytest

from ksdft2effmass.operators import (
    MODEL_SYSTEM_UNIT_CONVERTER,
    ComplexMatrixQuantity,
    MatrixQuantity,
    PhysicalUnit,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.solid_state.wannier_kinetic import (
    PlaneWaveBandSample,
    WannierFrameSample,
    WannierKineticDecompositionConstructor,
    WannierKineticDecompositionRequest,
    WannierKineticDecompositionResult,
)
from ksdft2effmass.solid_state.wignerseitz.interpolation import (
    WannierRepresentedOperatorCartesianDerivativeConstructor3D,
    WannierRepresentedOperatorCartesianDerivativeRequest3D,
    WannierRepresentedOperatorCartesianDerivativeResult3D,
    WignerSeitzInterpolationInventory3D,
)


@pytest.mark.software_verification
class TestWannierRepresentedOperatorCartesianDerivativeConstructor3D:
    """Establish analytic Cartesian value, gradient, and Hessian behavior."""

    @staticmethod
    def _decomposition() -> WannierKineticDecompositionResult:
        energy = PhysicalUnit("eV")
        request = WannierKineticDecompositionRequest(
            source_binding_identifier="synthetic-source",
            frame_identifier="synthetic-frame",
            energy_reference="synthetic-zero",
            hamiltonian_identifier="synthetic-H",
            kinetic_identifier="synthetic-T",
            nonkinetic_remainder_identifier="synthetic-R",
            fractional_kpoints=MatrixQuantity(
                np.asarray(((0.0, 0.0, 0.0), (0.5, 0.0, 0.0))), Unitless()
            ),
            mesh_shape=(2, 1, 1),
            plane_wave_samples=tuple(
                PlaneWaveBandSample(
                    ComplexMatrixQuantity(np.asarray(((1.0 + 0.0j,),)), Unitless()),
                    VectorQuantity(np.asarray((kinetic,)), energy),
                )
                for kinetic in (1.0, 3.0)
            ),
            frame_samples=tuple(
                WannierFrameSample(
                    VectorQuantity(np.asarray((eigenvalue,)), energy),
                    ComplexMatrixQuantity(np.asarray(((1.0 + 0.0j,),)), Unitless()),
                    ComplexMatrixQuantity(np.asarray(((1.0 + 0.0j,),)), Unitless()),
                )
                for eigenvalue in (4.0, 8.0)
            ),
            output_energy_unit=energy,
            coordinate_absolute_tolerance=1.0e-14,
            frame_absolute_tolerance=1.0e-14,
            diagnostic_absolute_tolerance=1.0e-12,
        )
        return WannierKineticDecompositionConstructor().execute(request)

    @staticmethod
    def _inventory() -> WignerSeitzInterpolationInventory3D:
        return WignerSeitzInterpolationInventory3D(
            identifier="synthetic-wigner-seitz-inventory",
            source_binding_identifier="synthetic-source",
            mesh_shape=(2, 1, 1),
            direct_lattice=MatrixQuantity(
                np.asarray(((1.0, 2.0, 3.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))),
                PhysicalUnit("bohr"),
            ),
            representatives=((-1, 0, 0), (0, 0, 0), (1, 0, 0)),
            degeneracies=(2, 1, 2),
        )

    def test_constructs_cartesian_derivatives_with_explicit_units(self) -> None:
        decomposition = self._decomposition()
        request = WannierRepresentedOperatorCartesianDerivativeRequest3D(
            operator=decomposition.hamiltonian,
            inventory=self._inventory(),
            fractional_kpoint=VectorQuantity(np.asarray((0.25, 0.0, 0.0)), Unitless()),
        )

        result = WannierRepresentedOperatorCartesianDerivativeConstructor3D().execute(
            request
        )

        np.testing.assert_allclose(
            result.value.magnitude, ((6.0,),), rtol=0.0, atol=1.0e-14
        )
        np.testing.assert_allclose(
            result.gradient[0].magnitude, ((2.0,),), rtol=0.0, atol=1.0e-14
        )
        np.testing.assert_allclose(
            result.gradient[1].magnitude, ((4.0,),), rtol=0.0, atol=1.0e-14
        )
        np.testing.assert_allclose(
            result.gradient[2].magnitude, ((6.0,),), rtol=0.0, atol=1.0e-14
        )
        np.testing.assert_allclose(
            result.hessian[0][0].magnitude, ((0.0,),), rtol=0.0, atol=1.0e-14
        )
        assert MODEL_SYSTEM_UNIT_CONVERTER.compatible(
            result.gradient[0].unit, PhysicalUnit("eV * bohr")
        )
        assert MODEL_SYSTEM_UNIT_CONVERTER.compatible(
            result.hessian[0][0].unit, PhysicalUnit("eV * bohr**2")
        )
        assert result.diagnostics.value_hermiticity_frobenius.magnitude < 1.0e-14
        assert (
            result.diagnostics.gradient_hermiticity_maximum_frobenius.magnitude
            < 1.0e-14
        )
        assert (
            result.diagnostics.hessian_cartesian_symmetry_maximum_frobenius.magnitude
            == 0.0
        )

    def test_execute_differentiates_once_without_a_result_witness(self) -> None:
        """The Action owns one derivative pass and Result has no witness input."""
        decomposition = self._decomposition()
        request = WannierRepresentedOperatorCartesianDerivativeRequest3D(
            operator=decomposition.hamiltonian,
            inventory=self._inventory(),
            fractional_kpoint=VectorQuantity(np.zeros(3), Unitless()),
        )
        with patch(
            "ksdft2effmass.solid_state.wignerseitz.interpolation.np.einsum",
            wraps=np.einsum,
        ) as einsum:
            WannierRepresentedOperatorCartesianDerivativeConstructor3D().execute(
                request
            )

        assert einsum.call_count == 2
        assert (
            "_evaluation"
            not in signature(
                WannierRepresentedOperatorCartesianDerivativeResult3D
            ).parameters
        )

    def test_gamma_hessian_matches_analytic_scalar_curvature(self) -> None:
        decomposition = self._decomposition()
        request = WannierRepresentedOperatorCartesianDerivativeRequest3D(
            operator=decomposition.hamiltonian,
            inventory=self._inventory(),
            fractional_kpoint=VectorQuantity(np.zeros(3), Unitless()),
        )

        result = WannierRepresentedOperatorCartesianDerivativeConstructor3D().execute(
            request
        )

        np.testing.assert_allclose(
            result.value.magnitude, ((4.0,),), rtol=0.0, atol=1.0e-14
        )
        np.testing.assert_allclose(
            result.gradient[0].magnitude, ((0.0,),), rtol=0.0, atol=1.0e-14
        )
        np.testing.assert_allclose(
            result.hessian[0][0].magnitude, ((2.0,),), rtol=0.0, atol=1.0e-14
        )
        np.testing.assert_allclose(
            result.hessian[0][1].magnitude, ((4.0,),), rtol=0.0, atol=1.0e-14
        )
        np.testing.assert_allclose(
            result.hessian[1][2].magnitude, ((12.0,),), rtol=0.0, atol=1.0e-14
        )

    def test_derivative_tensors_preserve_same_frame_decomposition(self) -> None:
        decomposition = self._decomposition()
        inventory = self._inventory()
        coordinate = VectorQuantity(np.asarray((0.19, -0.07, 0.11)), Unitless())
        constructor = WannierRepresentedOperatorCartesianDerivativeConstructor3D()
        hamiltonian = constructor.execute(
            WannierRepresentedOperatorCartesianDerivativeRequest3D(
                decomposition.hamiltonian, inventory, coordinate
            )
        )
        kinetic = constructor.execute(
            WannierRepresentedOperatorCartesianDerivativeRequest3D(
                decomposition.kinetic, inventory, coordinate
            )
        )
        remainder = constructor.execute(
            WannierRepresentedOperatorCartesianDerivativeRequest3D(
                decomposition.nonkinetic_remainder, inventory, coordinate
            )
        )

        np.testing.assert_allclose(
            hamiltonian.value.magnitude,
            kinetic.value.magnitude + remainder.value.magnitude,
            rtol=0.0,
            atol=1.0e-14,
        )
        for axis in range(3):
            np.testing.assert_allclose(
                hamiltonian.gradient[axis].magnitude,
                kinetic.gradient[axis].magnitude + remainder.gradient[axis].magnitude,
                rtol=0.0,
                atol=1.0e-14,
            )
            for second_axis in range(3):
                np.testing.assert_allclose(
                    hamiltonian.hessian[axis][second_axis].magnitude,
                    kinetic.hessian[axis][second_axis].magnitude
                    + remainder.hessian[axis][second_axis].magnitude,
                    rtol=0.0,
                    atol=1.0e-14,
                )

    def test_request_rejects_mismatched_source_binding(self) -> None:
        decomposition = self._decomposition()
        inventory = replace(
            self._inventory(), source_binding_identifier="different-source"
        )

        with pytest.raises(ValueError, match="source bindings must agree"):
            WannierRepresentedOperatorCartesianDerivativeRequest3D(
                operator=decomposition.hamiltonian,
                inventory=inventory,
                fractional_kpoint=VectorQuantity(np.zeros(3), Unitless()),
            )

    def test_result_rejects_corrupted_gradient(self) -> None:
        decomposition = self._decomposition()
        request = WannierRepresentedOperatorCartesianDerivativeRequest3D(
            operator=decomposition.hamiltonian,
            inventory=self._inventory(),
            fractional_kpoint=VectorQuantity(np.zeros(3), Unitless()),
        )
        result = WannierRepresentedOperatorCartesianDerivativeConstructor3D().execute(
            request
        )
        corrupted = ComplexMatrixQuantity(
            np.asarray(((0.0 + 1.0j,),)), result.gradient[0].unit
        )

        with pytest.raises(ValueError, match="diagnostics do not match"):
            replace(
                result, gradient=(corrupted, result.gradient[1], result.gradient[2])
            )
