"""Software verification of finite-difference model construction.

Synthetic arrays exercise metadata, shape, unit, and binary64 representability
invariants. They do not establish discretization convergence, continuum accuracy,
physical adequacy, scientific validation, uncertainty quantification, or acceptance.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.model_systems import (
    FiniteDifferenceBlochHamiltonian2DModel,
    UniformPeriodicCoordinateBasis2D,
)
from ksdft2effmass.operators import (
    MatrixQuantity,
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestFiniteDifferenceBlochHamiltonian2DModelConstruction:
    """Own complete-input and numeric-range invariant evidence for the model."""

    @staticmethod
    def model() -> FiniteDifferenceBlochHamiltonian2DModel:
        """Return one synthetic dimensionless five-by-five representation model."""
        unit = Unitless()
        return FiniteDifferenceBlochHamiltonian2DModel(
            basis=UniformPeriodicCoordinateBasis2D(
                2.0 * np.pi,
                5,
                "test.uniform.x_outer_y_inner.euclidean",
            ),
            potential_samples=MatrixQuantity(np.zeros((5, 5)), unit),
            kinetic_scale=ScalarQuantity(1.0, unit),
            source_identifier="test.source",
            operator_identifier="test.operator",
            state_space_identifier="test.state-space",
            energy_reference="test.zero",
            provenance_identifier="test.centered-second-order.v1",
        )

    def test_construction_retains_complete_finite_representation_metadata(self) -> None:
        """The model fixes grid, normalization, units, identities, and provenance."""
        model = self.model()

        assert model.represented_dimension == 25
        assert model.basis.ordering == "x_outer_y_inner"
        assert model.basis.normalization == "euclidean_site_basis"
        assert model.spin_convention == "spinless_scalar"
        assert model.stencil == "centered_second_order"
        assert model.kinetic_stencil_coefficient > 0.0
        assert model.potential_samples.unit == model.kinetic_scale.unit
        assert not model.potential_samples.magnitude.flags.writeable

    def test_construction_rejects_potential_shape_and_unit_contradictions(self) -> None:
        """Grid shape and energy unit cannot be supplied by dimensional inference."""
        basis = UniformPeriodicCoordinateBasis2D(2.0 * np.pi, 5, "test.basis")
        unit = Unitless()
        arguments = dict(
            basis=basis,
            kinetic_scale=ScalarQuantity(1.0, unit),
            source_identifier="test.source",
            operator_identifier="test.operator",
            state_space_identifier="test.state-space",
            energy_reference="test.zero",
            provenance_identifier="test.provenance",
        )

        with pytest.raises(ValueError, match="shape"):
            FiniteDifferenceBlochHamiltonian2DModel(
                potential_samples=MatrixQuantity(np.zeros((4, 4)), unit),
                **arguments,
            )
        with pytest.raises(ValueError, match="one unit"):
            FiniteDifferenceBlochHamiltonian2DModel(
                potential_samples=MatrixQuantity(
                    np.zeros((5, 5)), PhysicalUnit("joule")
                ),
                **arguments,
            )

    @pytest.mark.parametrize(
        ("period", "kinetic_scale"),
        (
            (1.0e-200, 1.0),
            (1.0e150, float(np.nextafter(0.0, 1.0))),
            (5.0, 1.0e308),
        ),
    )
    def test_construction_rejects_unrepresentable_kinetic_stencils(
        self,
        period: float,
        kinetic_scale: float,
    ) -> None:
        """Overflow, underflow, and nonrepresentable diagonals fail explicitly."""
        unit = Unitless()
        basis = UniformPeriodicCoordinateBasis2D(period, 5, "test.basis")

        with pytest.raises(
            OverflowError,
            match="binary64|finite-difference kinetic",
        ):
            FiniteDifferenceBlochHamiltonian2DModel(
                basis=basis,
                potential_samples=MatrixQuantity(np.zeros((5, 5)), unit),
                kinetic_scale=ScalarQuantity(kinetic_scale, unit),
                source_identifier="test.source",
                operator_identifier="test.operator",
                state_space_identifier="test.state-space",
                energy_reference="test.zero",
                provenance_identifier="test.provenance",
            )

    def test_construction_rejects_overflow_from_kinetic_and_potential_sum(self) -> None:
        """Finite inputs cannot compose a nonfinite represented diagonal."""
        unit = Unitless()

        with pytest.raises(OverflowError, match="represented diagonal"):
            FiniteDifferenceBlochHamiltonian2DModel(
                basis=UniformPeriodicCoordinateBasis2D(5.0, 5, "test.basis"),
                potential_samples=MatrixQuantity(np.full((5, 5), 5.0e307), unit),
                kinetic_scale=ScalarQuantity(4.0e307, unit),
                source_identifier="test.source",
                operator_identifier="test.operator",
                state_space_identifier="test.state-space",
                energy_reference="test.zero",
                provenance_identifier="test.provenance",
            )
