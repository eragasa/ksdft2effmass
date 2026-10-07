"""Software verification for same-frame Wigner--Seitz interpolation.

A synthetic scalar decomposition provides analytic Hamiltonian, kinetic, and remainder
oracles in eV. Comparisons use declared absolute tolerances; identity, rejection, and
fail-closed public construction checks are exact. The evidence does not establish
interpolation convergence, physical adequacy, scientific validation, uncertainty, or
acceptance.
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
    WannierKineticWignerSeitzInterpolationRequest3D,
    WannierKineticWignerSeitzInterpolationResult3D,
    WannierKineticWignerSeitzInterpolator3D,
    WignerSeitzInterpolationInventory3D,
)


@pytest.mark.software_verification
class TestWannierKineticWignerSeitzInterpolator3D:
    """Establish residue lifting and same-frame interpolation behavior."""

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
            direct_lattice=MatrixQuantity(np.eye(3), PhysicalUnit("bohr")),
            representatives=((-1, 0, 0), (0, 0, 0), (1, 0, 0)),
            degeneracies=(2, 1, 2),
        )

    def test_reconstructs_mesh_and_interpolates_same_frame_decomposition(self) -> None:
        decomposition = self._decomposition()
        request = WannierKineticWignerSeitzInterpolationRequest3D(
            decomposition=decomposition,
            inventory=self._inventory(),
            fractional_kpoints=MatrixQuantity(
                np.asarray(
                    (
                        (0.0, 0.0, 0.0),
                        (0.25, 0.0, 0.0),
                        (0.5, 0.0, 0.0),
                    )
                ),
                Unitless(),
            ),
            diagnostic_absolute_tolerance=1.0e-12,
        )

        result = WannierKineticWignerSeitzInterpolator3D().execute(request)

        np.testing.assert_allclose(
            [matrix.magnitude[0, 0] for matrix in result.hamiltonian_matrices],
            (4.0, 6.0, 8.0),
            rtol=0.0,
            atol=1.0e-14,
        )
        np.testing.assert_allclose(
            [matrix.magnitude[0, 0] for matrix in result.kinetic_matrices],
            (1.0, 2.0, 3.0),
            rtol=0.0,
            atol=1.0e-14,
        )
        np.testing.assert_allclose(
            [matrix.magnitude[0, 0] for matrix in result.nonkinetic_remainder_matrices],
            (3.0, 4.0, 5.0),
            rtol=0.0,
            atol=1.0e-14,
        )
        assert result.request.decomposition is decomposition
        assert result.diagnostics.passes
        assert result.diagnostics.decomposition_maximum_frobenius < 1.0e-14

    def test_execute_interpolates_each_operator_once_without_a_result_witness(
        self,
    ) -> None:
        """The Action owns three numerical passes and Result has no witness input."""
        request = WannierKineticWignerSeitzInterpolationRequest3D(
            decomposition=self._decomposition(),
            inventory=self._inventory(),
            fractional_kpoints=MatrixQuantity(
                np.asarray(((0.25, 0.0, 0.0),)), Unitless()
            ),
            diagnostic_absolute_tolerance=1.0e-12,
        )

        with patch(
            "ksdft2effmass.solid_state.wignerseitz.interpolation.np.einsum",
            wraps=np.einsum,
        ) as einsum:
            WannierKineticWignerSeitzInterpolator3D().execute(request)

        assert einsum.call_count == 3
        assert (
            "_evaluation"
            not in signature(WannierKineticWignerSeitzInterpolationResult3D).parameters
        )

    def test_inventory_rejects_incomplete_or_inconsistent_residue_classes(
        self,
    ) -> None:
        inventory = self._inventory()
        with pytest.raises(ValueError, match="cover every modulo-mesh residue"):
            replace(
                inventory,
                representatives=((-1, 0, 0), (1, 0, 0)),
                degeneracies=(2, 2),
            )
        with pytest.raises(ValueError, match="residue-class multiplicity"):
            replace(inventory, degeneracies=(1, 1, 1))

    def test_request_rejects_mismatched_source_binding(self) -> None:
        inventory = replace(
            self._inventory(), source_binding_identifier="different-source"
        )
        with pytest.raises(ValueError, match="source bindings must agree"):
            WannierKineticWignerSeitzInterpolationRequest3D(
                decomposition=self._decomposition(),
                inventory=inventory,
                fractional_kpoints=MatrixQuantity(
                    np.asarray(((0.0, 0.0, 0.0),)), Unitless()
                ),
                diagnostic_absolute_tolerance=1.0e-12,
            )

    def test_result_rejects_corrupted_interpolated_matrix(self) -> None:
        request = WannierKineticWignerSeitzInterpolationRequest3D(
            decomposition=self._decomposition(),
            inventory=self._inventory(),
            fractional_kpoints=MatrixQuantity(
                np.asarray(((0.25, 0.0, 0.0),)), Unitless()
            ),
            diagnostic_absolute_tolerance=1.0e-12,
        )
        result = WannierKineticWignerSeitzInterpolator3D().execute(request)
        corrupted = ComplexMatrixQuantity(
            np.asarray(((7.0 + 0.0j,),)), PhysicalUnit("eV")
        )

        with pytest.raises(ValueError, match="diagnostics do not match"):
            replace(result, hamiltonian_matrices=(corrupted,))
