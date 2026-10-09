"""Software verification for concrete Wigner--Seitz operator interpolation.

Synthetic scalar blocks provide analytic residue-lift and interpolation oracles in eV.
Comparisons use explicit absolute tolerances, while corruption and evaluation-count
checks are exact. The evidence does not establish interpolation convergence, physical
adequacy, scientific validation, uncertainty quantification, or acceptance.
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
)
from ksdft2effmass.solid_state.wannier_kinetic import (
    WannierOperatorRole,
    WannierRepresentedOperatorMesh3D,
)
from ksdft2effmass.solid_state.wignerseitz.interpolation import (
    WannierRepresentedOperatorWignerSeitzConstructor3D,
    WignerSeitzInterpolationInventory3D,
    WignerSeitzOperatorInterpolationRequest3D,
    WignerSeitzOperatorInterpolationResult3D,
    WignerSeitzOperatorInterpolator3D,
)


@pytest.mark.software_verification
class TestWignerSeitzOperatorInterpolator3D:
    """Establish concrete per-operator residue lifting and interpolation."""

    @staticmethod
    def _source() -> WannierRepresentedOperatorMesh3D:
        unit = PhysicalUnit("eV")
        return WannierRepresentedOperatorMesh3D(
            identifier="synthetic-H",
            role=WannierOperatorRole.HAMILTONIAN,
            source_binding_identifier="synthetic-source",
            frame_identifier="synthetic-frame",
            energy_reference="synthetic-zero",
            fractional_kpoints=MatrixQuantity(
                np.asarray(((0.0, 0.0, 0.0), (0.5, 0.0, 0.0))), Unitless()
            ),
            mesh_shape=(2, 1, 1),
            coordinate_absolute_tolerance=1.0e-14,
            reciprocal_matrices=tuple(
                ComplexMatrixQuantity(np.asarray(((value + 0.0j,),)), unit)
                for value in (4.0, 8.0)
            ),
            representatives=((-1, 0, 0), (0, 0, 0)),
            lattice_blocks=tuple(
                ComplexMatrixQuantity(np.asarray(((value + 0.0j,),)), unit)
                for value in (-2.0, 6.0)
            ),
        )

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

    def test_lifts_and_interpolates_one_identified_operator(self) -> None:
        source = self._source()
        operator = WannierRepresentedOperatorWignerSeitzConstructor3D().execute(
            source, self._inventory()
        )

        result = WignerSeitzOperatorInterpolator3D().execute(
            WignerSeitzOperatorInterpolationRequest3D(
                operator,
                MatrixQuantity(
                    np.asarray(
                        (
                            (0.0, 0.0, 0.0),
                            (0.25, 0.0, 0.0),
                            (0.5, 0.0, 0.0),
                        )
                    ),
                    Unitless(),
                ),
                1.0e-12,
            )
        )

        np.testing.assert_allclose(
            [block.magnitude[0, 0] for block in operator.blocks],
            (-2.0, 6.0, -2.0),
            rtol=0.0,
            atol=1.0e-14,
        )
        np.testing.assert_allclose(
            [matrix.magnitude[0, 0] for matrix in result.matrices],
            (4.0, 6.0, 8.0),
            rtol=0.0,
            atol=1.0e-14,
        )
        assert operator.frame_identifier == source.frame_identifier
        assert result.passes

    def test_execute_interpolates_once_without_a_result_witness(self) -> None:
        """The Action owns one numerical pass and Result has no witness input."""
        operator = WannierRepresentedOperatorWignerSeitzConstructor3D().execute(
            self._source(), self._inventory()
        )
        request = WignerSeitzOperatorInterpolationRequest3D(
            operator,
            MatrixQuantity(np.asarray(((0.25, 0.0, 0.0),)), Unitless()),
            1.0e-12,
        )

        with patch(
            "ksdft2effmass.solid_state.wignerseitz.interpolation.np.einsum",
            wraps=np.einsum,
        ) as einsum:
            WignerSeitzOperatorInterpolator3D().execute(request)

        assert einsum.call_count == 1
        assert (
            "_evaluation"
            not in signature(WignerSeitzOperatorInterpolationResult3D).parameters
        )

    def test_result_rejects_corrupted_hermiticity_diagnostic(self) -> None:
        operator = WannierRepresentedOperatorWignerSeitzConstructor3D().execute(
            self._source(), self._inventory()
        )
        request = WignerSeitzOperatorInterpolationRequest3D(
            operator,
            MatrixQuantity(np.asarray(((0.25, 0.0, 0.0),)), Unitless()),
            1.0e-12,
        )
        result = WignerSeitzOperatorInterpolator3D().execute(request)
        with pytest.raises(ValueError, match="diagnostic does not match"):
            replace(result, hermiticity_maximum_frobenius=1.0)
