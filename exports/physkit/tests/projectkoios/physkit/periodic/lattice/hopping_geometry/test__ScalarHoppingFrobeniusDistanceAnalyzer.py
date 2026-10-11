"""Software verification for dimensionful scalar hopping geometry."""

from __future__ import annotations

from dataclasses import replace

import pytest

from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeDimension,
    LatticeDisplacement,
)
from projectkoios.physkit.periodic.lattice.hopping import (
    ScalarHoppingModel,
    ScalarHoppingTerm,
)
from projectkoios.physkit.periodic.lattice.hopping_geometry import (
    ScalarHoppingFrobeniusDistanceAnalyzer,
)
from projectkoios.physkit.periodic.lattice.symmetry_orbits import (
    LatticeDisplacementOrbitPartition,
    LatticeDisplacementOrbitPartitioner,
    SquareLatticeD4OperationSetConstructor,
)
from projectkoios.physkit.units import PhysicalUnit, ScalarQuantity, Unitless


class TestScalarHoppingFrobeniusDistanceAnalyzer:
    """Verify full-block multiplicities, units, compatibility, and overflow."""

    @staticmethod
    def partition() -> LatticeDisplacementOrbitPartition:
        inventory = tuple(
            LatticeDisplacement(LatticeDimension.TWO, (first, second))
            for first in range(-1, 2)
            for second in range(-1, 2)
        )
        return LatticeDisplacementOrbitPartitioner().execute(
            inventory,
            SquareLatticeD4OperationSetConstructor().execute(),
        )

    @classmethod
    def model(
        cls,
        identifier: str,
        coefficients: tuple[float, float, float],
        *,
        unit: PhysicalUnit | Unitless | None = None,
        energy_reference: str = "common-zero",
    ) -> ScalarHoppingModel:
        center, axial, corner = coefficients
        terms = []
        for displacement in cls.partition().displacements:
            first, second = displacement.components
            if first == 0 and second == 0:
                value = center
            elif first == 0 or second == 0:
                value = axial
            else:
                value = corner
            terms.append(ScalarHoppingTerm(displacement, value, 0.0))
        return ScalarHoppingModel(
            identifier,
            LatticeDimension.TWO,
            tuple(terms),
            PhysicalUnit("electron_volt") if unit is None else unit,
            energy_reference,
            "scalar-cell-basis",
        )

    def test_distance_counts_every_represented_block_and_preserves_units(self) -> None:
        left = self.model("left", (0.0, 0.0, 0.0))
        right = self.model("right", (2.0, 1.0, -0.5))

        result = ScalarHoppingFrobeniusDistanceAnalyzer().execute(
            left, right, self.partition()
        )

        assert result.squared_distance.magnitude == 9.0
        assert result.squared_distance.unit == PhysicalUnit("(electron_volt) ** 2")
        assert result.distance.magnitude == 3.0
        assert result.distance.unit == PhysicalUnit("electron_volt")
        assert result.maximum_absolute_difference.magnitude == 2.0

        with pytest.raises(ValueError, match="reconstruct"):
            replace(
                result,
                maximum_absolute_difference=ScalarQuantity(
                    magnitude=0.0,
                    unit=PhysicalUnit("electron_volt"),
                ),
            )

    def test_distance_preserves_a_representable_root_when_its_square_underflows(
        self,
    ) -> None:
        left = self.model("left", (0.0, 0.0, 0.0))
        right = self.model("right", (1.0e-200, 0.0, 0.0))

        result = ScalarHoppingFrobeniusDistanceAnalyzer().execute(
            left,
            right,
            self.partition(),
        )

        assert result.squared_distance.magnitude == 0.0
        assert result.distance.magnitude == 1.0e-200
        assert result.maximum_absolute_difference.magnitude == 1.0e-200

    def test_distance_supports_a_genuinely_unitless_hopping_family(self) -> None:
        left = self.model("left", (0.0, 0.0, 0.0), unit=Unitless())
        right = self.model("right", (2.0, 1.0, -0.5), unit=Unitless())

        result = ScalarHoppingFrobeniusDistanceAnalyzer().execute(
            left, right, self.partition()
        )

        assert result.squared_distance.unit == Unitless()
        assert result.distance.unit == Unitless()

    def test_distance_rejects_different_energy_references(self) -> None:
        left = self.model("left", (0.0, 0.0, 0.0))
        right = self.model("right", (2.0, 1.0, -0.5), energy_reference="different-zero")

        with pytest.raises(ValueError, match="references"):
            ScalarHoppingFrobeniusDistanceAnalyzer().execute(
                left, right, self.partition()
            )

    def test_distance_rejects_overflow_instead_of_returning_infinity(self) -> None:
        left = self.model("left", (0.0, 0.0, 0.0))
        right = self.model("right", (1.0e308, 0.0, 0.0))

        with pytest.raises(ValueError, match="nonfinite"):
            ScalarHoppingFrobeniusDistanceAnalyzer().execute(
                left, right, self.partition()
            )
