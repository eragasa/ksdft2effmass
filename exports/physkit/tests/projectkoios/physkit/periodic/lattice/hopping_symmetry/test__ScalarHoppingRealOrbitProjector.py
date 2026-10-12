"""Software verification for scalar hopping defect analysis and projection."""

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
from projectkoios.physkit.periodic.lattice.hopping_symmetry import (
    ScalarHoppingRealOrbitProjector,
    ScalarHoppingSymmetryDefectAnalyzer,
)
from projectkoios.physkit.periodic.lattice.symmetry_orbits import (
    LatticeDisplacementOrbitPartition,
    LatticeDisplacementOrbitPartitioner,
    SquareLatticeD4OperationSetConstructor,
)
from projectkoios.physkit.units import PhysicalUnit, ScalarQuantity


class TestScalarHoppingRealOrbitProjector:
    """Verify defect measurement, canonical projection, and support checks."""

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
    def source(cls) -> ScalarHoppingModel:
        values = {
            (-1, -1): (-0.5, 0.0),
            (-1, 0): (1.1, -0.1),
            (-1, 1): (-0.5, 0.0),
            (0, -1): (1.0, 0.0),
            (0, 0): (2.0, 0.1),
            (0, 1): (0.9, 0.0),
            (1, -1): (-0.5, 0.0),
            (1, 0): (1.0, 0.2),
            (1, 1): (-0.5, 0.0),
        }
        terms = tuple(
            ScalarHoppingTerm(
                LatticeDisplacement(LatticeDimension.TWO, components),
                real,
                imaginary,
            )
            for components, (real, imaginary) in sorted(values.items())
        )
        return ScalarHoppingModel(
            "source",
            LatticeDimension.TWO,
            terms,
            PhysicalUnit("electron_volt"),
            "source-zero",
            "scalar-cell-basis",
        )

    def test_defect_analyzer_reports_independent_nonzero_defects(self) -> None:
        source = self.source()
        defects = ScalarHoppingSymmetryDefectAnalyzer().execute(
            source, self.partition()
        )

        assert defects.maximum_hermiticity_defect.magnitude > 0.0
        assert defects.maximum_imaginary_part.magnitude == 0.2
        assert defects.maximum_orbit_defect.magnitude > 0.0
        assert defects.maximum_hermiticity_defect.unit == source.energy_unit

    def test_projector_returns_exact_real_orbit_constant_coefficients(self) -> None:
        source = self.source()
        projection = ScalarHoppingRealOrbitProjector().execute(
            "projected", source, self.partition()
        )
        projected = {
            term.displacement.components: term for term in projection.projected.terms
        }

        assert projected[(0, 0)].real == 2.0
        assert projected[(0, 0)].imaginary == 0.0
        assert {
            projected[components].real
            for components in ((-1, 0), (0, -1), (0, 1), (1, 0))
        } == {1.0}
        assert {
            projected[components].real
            for components in ((-1, -1), (-1, 1), (1, -1), (1, 1))
        } == {-0.5}
        assert projection.projected.energy_unit == source.energy_unit
        assert projection.projected.energy_reference == source.energy_reference
        assert projection.maximum_absolute_change.magnitude > 0.0

        with pytest.raises(ValueError, match="maximum_absolute_change"):
            replace(
                projection,
                maximum_absolute_change=ScalarQuantity(
                    magnitude=0.0,
                    unit=source.energy_unit,
                ),
            )

    def test_projection_of_large_constant_orbits_preserves_finite_coefficients(
        self,
    ) -> None:
        partition = self.partition()
        source = ScalarHoppingModel(
            "large-source",
            LatticeDimension.TWO,
            tuple(
                ScalarHoppingTerm(displacement, 1.0e308, 0.0)
                for displacement in partition.displacements
            ),
            PhysicalUnit("electron_volt"),
            "source-zero",
            "scalar-cell-basis",
        )

        projection = ScalarHoppingRealOrbitProjector().execute(
            "large-projected",
            source,
            partition,
        )

        assert all(term.real == 1.0e308 for term in projection.projected.terms)
        assert projection.maximum_absolute_change.magnitude == 0.0

    def test_projector_does_not_apply_a_tolerance_or_change_the_energy_zero(
        self,
    ) -> None:
        source = self.source()
        projection = ScalarHoppingRealOrbitProjector().execute(
            "projected", source, self.partition()
        )

        assert projection.defects.maximum_imaginary_part.magnitude == 0.2
        assert projection.projected.energy_reference == "source-zero"
        assert (
            next(
                term.real
                for term in projection.projected.terms
                if term.displacement.components == (0, 0)
            )
            == 2.0
        )

    def test_projector_rejects_support_that_does_not_match_the_partition(self) -> None:
        source = self.source()
        incomplete = ScalarHoppingModel(
            "incomplete",
            source.dimension,
            source.terms[:-1],
            source.energy_unit,
            source.energy_reference,
            source.basis_identifier,
        )

        with pytest.raises(ValueError, match="support"):
            ScalarHoppingRealOrbitProjector().execute(
                "projected", incomplete, self.partition()
            )
