"""Software verification for the calculation-owned rank-one calculator."""

from pathlib import Path

import pytest
from calculator import Periodic1dRank1CalculationResult, Periodic1dRank1Calculator
from projectkoios.physkit.units import PhysicalUnit

from ksdft2effmass.periodic1d.fourier_locality import (
    Periodic1DFourierLocalityCalculationResult,
)
from ksdft2effmass.periodic1d.geometry import Periodic1DLatticeGeometry
from ksdft2effmass.periodic1d.rank1.alignment import (
    Periodic1DRank1AlignmentApplicability,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1dRank1Calculator:
    """Verify read-only composition of maintained rank-one capability owners."""

    @staticmethod
    def retained_result() -> Periodic1DFourierLocalityCalculationResult:
        """Decode the exact retained typed producer result without changing it."""
        calculation_root = Path(__file__).resolve().parents[1]
        result_path = (
            calculation_root
            / "executions/direct-controlled-four-state-n256/results/result.json"
        )
        return Periodic1DFourierLocalityCalculationResult.from_json(
            result_path.read_bytes()
        )

    def test__Periodic1dRank1Calculator__result__correlates_rank_owned_capabilities(
        self,
    ) -> None:
        """The retained producer result projects into each distinct rank-one view."""
        source = self.retained_result()

        # The retained predecessor did not store physical geometry. The caller makes
        # the current reduced-convention interpretation explicit instead of rewriting
        # or silently reinterpreting retained result bytes.
        geometry = Periodic1DLatticeGeometry(
            lattice_period=1.0,
            lattice_unit=PhysicalUnit("bohr"),
        )
        calculator = Periodic1dRank1Calculator(
            source_calculation=source,
            lattice_geometry=geometry,
        )

        result = calculator.result()

        assert type(result) is Periodic1dRank1CalculationResult
        assert result.source_calculation is source
        assert result.band_equivalence is source
        assert result.band_subspace_rank == 1
        assert result.production_mesh.construction_size == 256
        assert result.alignment.applicability is (
            Periodic1DRank1AlignmentApplicability.OPERATOR_TRIVIAL
        )
        assert result.alignment.retained_rank == 1
        assert result.hopping_locality.source_mesh is result.production_mesh
        assert result.support_truncation.source_mesh is result.production_mesh
        assert tuple(
            tail.maximum_range for tail in result.hopping_locality.tails
        ) == tuple(range(16))
        assert tuple(
            support.maximum_range for support in result.support_truncation.supports
        ) == tuple(range(16))

    def test__Periodic1dRank1Calculator__construction__rejects_untyped_sources(
        self,
    ) -> None:
        """The calculator does not coerce mappings into typed calculation results."""
        geometry = Periodic1DLatticeGeometry(1.0, PhysicalUnit("bohr"))

        with pytest.raises(TypeError, match="source_calculation"):
            Periodic1dRank1Calculator(
                source_calculation={},  # type: ignore[arg-type]
                lattice_geometry=geometry,
            )
