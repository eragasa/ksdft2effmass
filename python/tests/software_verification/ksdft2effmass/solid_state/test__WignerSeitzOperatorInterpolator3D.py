from __future__ import annotations

from dataclasses import replace

import numpy as np
import pytest

from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    MatrixQuantity,
    PhysicalUnit,
    Unitless,
)
from ksdft2effmass.solid_state import (
    WannierOperatorRole,
    WannierRepresentedOperatorMesh3D,
    WannierRepresentedOperatorWignerSeitzConstructor3D,
    WignerSeitzInterpolationInventory3D,
    WignerSeitzOperatorInterpolationRequest3D,
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

    def test_result_rejects_corrupted_interpolation(self) -> None:
        operator = WannierRepresentedOperatorWignerSeitzConstructor3D().execute(
            self._source(), self._inventory()
        )
        request = WignerSeitzOperatorInterpolationRequest3D(
            operator,
            MatrixQuantity(np.asarray(((0.25, 0.0, 0.0),)), Unitless()),
            1.0e-12,
        )
        result = WignerSeitzOperatorInterpolator3D().execute(request)
        corrupted = ComplexMatrixQuantity(
            np.asarray(((7.0 + 0.0j,),)), PhysicalUnit("eV")
        )

        with pytest.raises(ValueError, match="do not match the request"):
            replace(result, matrices=(corrupted,))
