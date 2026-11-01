"""Tests for rank-one capability ownership over the maintained calculation."""

import json

import pytest
from projectkoios.physkit.periodic.lattice import DirectLattice1D
from projectkoios.physkit.units import PhysicalUnit

from ksdft2effmass.gauge_alignment import (
    GaugeAlignment,
    GaugeAlignmentGroupFamily,
)
from ksdft2effmass.hopping_locality import HoppingLocality
from ksdft2effmass.periodic1d.fourier_locality import (
    Periodic1DFourierLocalityAnalyzer,
    Periodic1DFourierLocalityConfiguration,
)
from ksdft2effmass.periodic1d.gauge_alignment import Periodic1DGaugeAlignment
from ksdft2effmass.periodic1d.geometry import Periodic1DLatticeGeometry
from ksdft2effmass.periodic1d.hopping_locality import Periodic1DHoppingLocality
from ksdft2effmass.periodic1d.rank1.alignment import (
    Periodic1DRank1AlignmentApplicability,
    Periodic1DRank1AlignmentApplicabilityAnalyzer,
    Periodic1DRank1AlignmentApplicabilityResult,
)
from ksdft2effmass.periodic1d.rank1.hopping_locality import (
    Periodic1DRank1HoppingLocalityAnalysisRequest,
    Periodic1DRank1HoppingLocalityAnalyzer,
    Periodic1DRank1HoppingTailResult,
)
from ksdft2effmass.periodic1d.rank1.support_truncation import (
    Periodic1DRank1SupportResult,
    Periodic1DRank1SupportTruncationAnalysisRequest,
    Periodic1DRank1SupportTruncationAnalyzer,
)
from ksdft2effmass.periodic1d.support_truncation import (
    Periodic1DSupportTruncation,
)
from ksdft2effmass.serialization import StringWireEnum
from ksdft2effmass.support_truncation import SupportTruncation

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestPeriodic1DRank1Capabilities:
    """Establish base ownership and retained rank-one capability values."""

    @staticmethod
    def configuration() -> Periodic1DFourierLocalityConfiguration:
        return Periodic1DFourierLocalityConfiguration(
            parent_identity=(
                "ksdft2effmass.periodic1d.controlled-four-state-parent.v1"
            ),
            onsite_numerators=(
                (-120, 6, 0, 0),
                (6, -35, 0, 0),
                (0, 0, 100, 4),
                (0, 0, 4, 175),
            ),
            positive_hopping_numerators=(
                (15, 0, 12, 0),
                (0, -10, 0, 10),
                (0, 0, 5, 0),
                (0, 0, 0, -4),
            ),
            coefficient_denominator=100,
            construction_mesh_sizes=(4, 8),
            production_construction_size=8,
            evaluation_size=3,
            evaluation_shift_numerator=1,
            evaluation_shift_denominator=3,
            maximum_ranges=(0, 1),
            sampled_gap_threshold=0.25,
            energy_absolute_tolerance=1.0e-12,
            relative_tolerance=1.0e-12,
            squared_energy_absolute_tolerance=1.0e-12,
            dimensionless_absolute_tolerance=1.0e-12,
            refinement_tolerance=1.0e-10,
            application_threshold=1.0e-8,
        )

    def test__alignment__inherits_base_and_encodes_one_applicability(self) -> None:
        configuration = self.configuration()

        geometry = Periodic1DLatticeGeometry.from_direct_lattice(
            DirectLattice1D(2.0),
            PhysicalUnit("angstrom"),
        )
        result = Periodic1DRank1AlignmentApplicabilityAnalyzer(
            request=configuration,
            lattice_geometry=geometry,
        ).execute()
        reconstructed = Periodic1DRank1AlignmentApplicabilityResult.from_json(
            result.to_json()
        )

        assert isinstance(result, Periodic1DGaugeAlignment)
        assert isinstance(result, GaugeAlignment)
        assert result.direct_lattice.lattice_constant == 2.0
        assert result.lattice_geometry.lattice_unit == PhysicalUnit("angstrom")
        assert result.retained_rank == 1
        assert result.gauge_group == "U(1)"
        assert result.gauge_group_identity.family is GaugeAlignmentGroupFamily.UNITARY
        assert result.gauge_group_identity.represented_dimension == 1
        assert result.applicability is (
            Periodic1DRank1AlignmentApplicability.OPERATOR_TRIVIAL
        )
        assert result.inapplicable_alignment_controls == (
            "global-unitary",
            "pointwise-unitary",
            "known-inverse-oracle",
            "restricted-internal-rotation",
        )
        assert not hasattr(result, "channels")
        assert reconstructed.to_json() == result.to_json()

    def test__alignment_applicability__uses_strict_string_wire_enum(self) -> None:
        applicability = Periodic1DRank1AlignmentApplicability.OPERATOR_TRIVIAL

        assert isinstance(applicability, StringWireEnum)
        assert applicability.to_wire() == "operator-trivial"
        assert (
            Periodic1DRank1AlignmentApplicability.from_wire("operator-trivial")
            is applicability
        )
        with pytest.raises(TypeError, match="wire must be a built-in string"):
            Periodic1DRank1AlignmentApplicability.from_wire(True)  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="unsupported"):
            Periodic1DRank1AlignmentApplicability.from_wire("unknown")

    def test__alignment__rejects_tampered_retained_rank_wire(self) -> None:
        result = Periodic1DRank1AlignmentApplicabilityAnalyzer(
            request=self.configuration(),
            lattice_geometry=Periodic1DLatticeGeometry(
                1.0,
                PhysicalUnit("bohr"),
            ),
        ).execute()
        decoded = json.loads(result.to_json())
        decoded["retained_rank"] = 2

        with pytest.raises(ValueError, match="must equal one"):
            Periodic1DRank1AlignmentApplicabilityResult.from_json(
                json.dumps(decoded).encode("utf-8")
            )

    def test__alignment__rejects_tampered_gauge_group_wire(self) -> None:
        result = Periodic1DRank1AlignmentApplicabilityAnalyzer(
            request=self.configuration(),
            lattice_geometry=Periodic1DLatticeGeometry(
                1.0,
                PhysicalUnit("bohr"),
            ),
        ).execute()
        decoded = json.loads(result.to_json())
        decoded["gauge_group"] = "U(2)"

        with pytest.raises(ValueError, match="must use U\\(1\\)"):
            Periodic1DRank1AlignmentApplicabilityResult.from_json(
                json.dumps(decoded).encode("utf-8")
            )

    def test__locality_and_truncation__inherit_distinct_bases_without_rewriting_source(
        self,
    ) -> None:
        calculation = Periodic1DFourierLocalityAnalyzer(self.configuration()).execute()
        source_bytes = calculation.to_json()
        source_mesh = calculation.meshes[-1]
        geometry = Periodic1DLatticeGeometry.from_direct_lattice(
            DirectLattice1D(3.0),
            PhysicalUnit("bohr"),
        )

        locality = Periodic1DRank1HoppingLocalityAnalyzer(
            request=Periodic1DRank1HoppingLocalityAnalysisRequest(
                lattice_geometry=geometry,
                source_calculation=calculation,
                source_mesh=source_mesh,
            )
        ).execute()
        truncation = Periodic1DRank1SupportTruncationAnalyzer(
            request=Periodic1DRank1SupportTruncationAnalysisRequest(
                lattice_geometry=geometry,
                source_calculation=calculation,
                source_mesh=source_mesh,
            )
        ).execute()

        assert isinstance(locality, Periodic1DHoppingLocality)
        assert isinstance(locality, HoppingLocality)
        assert isinstance(truncation, Periodic1DSupportTruncation)
        assert isinstance(truncation, SupportTruncation)
        assert locality.tails[-1].direct_lattice.lattice_constant == 3.0
        assert locality.tails[-1].lattice_geometry.lattice_unit == PhysicalUnit("bohr")
        assert truncation.supports[-1].direct_lattice.lattice_constant == 3.0
        assert tuple(item.source_range for item in locality.tails) == source_mesh.ranges
        assert (
            tuple(item.source_range for item in truncation.supports)
            == source_mesh.ranges
        )
        assert locality.tails[-1].complete_coefficients is (
            source_mesh.complete_coefficients
        )
        assert locality.tails[-1].omitted_coefficient_l2_norm is (
            source_mesh.ranges[-1].omitted_coefficient_l2_norm
        )
        assert truncation.supports[-1].retained_coefficients is (
            source_mesh.ranges[-1].mediated_coefficients
        )
        assert truncation.supports[-1].evaluation_candidate is (
            source_mesh.ranges[-1].mediated_evaluation_candidate
        )
        assert calculation.to_json() == source_bytes

    def test__capability_values__reject_foreign_source_identities(self) -> None:
        calculation = Periodic1DFourierLocalityAnalyzer(self.configuration()).execute()
        foreign_calculation = Periodic1DFourierLocalityAnalyzer(
            self.configuration()
        ).execute()
        source_mesh = calculation.meshes[-1]
        foreign_mesh = foreign_calculation.meshes[-1]
        foreign_range = foreign_mesh.ranges[-1]
        geometry = Periodic1DLatticeGeometry(1.0, PhysicalUnit("bohr"))

        with pytest.raises(ValueError, match="source_calculation by identity"):
            Periodic1DRank1HoppingLocalityAnalysisRequest(
                lattice_geometry=geometry,
                source_calculation=calculation,
                source_mesh=foreign_mesh,
            )
        with pytest.raises(ValueError, match="source_calculation by identity"):
            Periodic1DRank1SupportTruncationAnalysisRequest(
                lattice_geometry=geometry,
                source_calculation=calculation,
                source_mesh=foreign_mesh,
            )
        with pytest.raises(ValueError, match="source_mesh by identity"):
            Periodic1DRank1HoppingTailResult(
                lattice_geometry=geometry,
                source_calculation=calculation,
                source_mesh=source_mesh,
                source_range=foreign_range,
            )
        with pytest.raises(ValueError, match="source_mesh by identity"):
            Periodic1DRank1SupportResult(
                lattice_geometry=geometry,
                source_calculation=calculation,
                source_mesh=source_mesh,
                source_range=foreign_range,
            )
