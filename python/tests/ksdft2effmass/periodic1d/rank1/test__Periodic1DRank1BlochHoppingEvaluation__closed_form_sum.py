"""Independent Bloch evaluation of the periodic-1D rank-one reduced model."""

from __future__ import annotations

import numpy as np
import pytest
from numpy.typing import NDArray
from projectkoios.physkit.solidstate.tb.bloch import (
    DenseBlockHoppingBlochEvaluator,
)
from projectkoios.physkit.units import (
    MatrixQuantity,
    PhysicalUnit,
    Unitless,
    UnitSystem,
)

from ksdft2effmass.periodic1d.geometry import Periodic1DLatticeGeometry
from ksdft2effmass.periodic1d.rank1.model.blochhopping import (
    Periodic1DRank1BlochHoppingModel,
)

pytestmark = [pytest.mark.unit, pytest.mark.numerical_verification]


class TestPeriodic1DRank1BlochHoppingEvaluation:
    """Compare PhysKit block evaluation with independent scalar arithmetic."""

    normalized_onsite = 1.25
    normalized_positive_hoppings = (
        (1, -0.30 + 0.20j),
        (2, 0.125 - 0.05j),
        (4, -0.015 + 0.025j),
    )
    fractional_coordinates = np.asarray(
        [[-0.5], [-0.375], [-0.125], [0.0], [0.2], [0.5]],
        dtype=np.float64,
    )

    @classmethod
    def _model(cls) -> Periodic1DRank1BlochHoppingModel:
        """Construct the finite-support rank-one numerical control."""
        return Periodic1DRank1BlochHoppingModel.from_lattice_kinetic_parameters(
            identifier="rank1-analytic-bloch-control-v1",
            geometry=Periodic1DLatticeGeometry(
                2.5,
                PhysicalUnit("angstrom"),
            ),
            unit_system=UnitSystem.METAL,
            energy_reference="rank1-analytic-zero-v1",
            basis_identifier="rank1-analytic-cell-basis-v1",
            normalized_onsite=cls.normalized_onsite,
            normalized_positive_hoppings=cls.normalized_positive_hoppings,
        )

    @classmethod
    def _closed_form_values(
        cls,
        model: Periodic1DRank1BlochHoppingModel,
    ) -> NDArray[np.complex128]:
        """Evaluate the scalar Bloch sum directly from constructor inputs."""
        coordinates = cls.fractional_coordinates[:, 0]
        expected_normalized = np.full(
            coordinates.shape,
            cls.normalized_onsite,
            dtype=np.float64,
        )
        for displacement, coefficient in cls.normalized_positive_hoppings:
            phase = np.exp(2.0j * np.pi * float(displacement) * coordinates)
            expected_normalized += 2.0 * np.real(complex(coefficient) * phase)
        return np.asarray(
            model.lattice_kinetic_energy_scale.magnitude * expected_normalized,
            dtype=np.complex128,
        )

    def test__Periodic1DRank1BlochHoppingEvaluation__matches_closed_form_sum(
        self,
    ) -> None:
        """Match the independent positive-exponent scalar Bloch sum."""
        model = self._model()
        evaluation = DenseBlockHoppingBlochEvaluator().evaluate(
            model.block_hopping_model,
            MatrixQuantity(self.fractional_coordinates, Unitless()),
        )

        # Extract the only retained-space entry from every evaluated block. Comparing
        # the full complex vector also verifies that conjugate support cancels the
        # imaginary component without a separate assertion.
        actual = np.asarray(
            [matrix.magnitude[0, 0] for matrix in evaluation.bloch_matrices],
            dtype=np.complex128,
        )
        expected = self._closed_form_values(model)
        tolerance = 5.0e-15 * model.lattice_kinetic_energy_scale.magnitude
        np.testing.assert_allclose(actual, expected, rtol=0.0, atol=tolerance)
