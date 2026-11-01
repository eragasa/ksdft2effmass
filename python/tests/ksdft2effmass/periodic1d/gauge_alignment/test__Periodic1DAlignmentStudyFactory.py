"""Tests for exact typed periodic-1D alignment-study dispatch."""

import pytest
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesSolver,
)
from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesRankCutoffRule,
)
from projectkoios.physkit.periodic.lattice import DirectLattice1D
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
    ClosedLoopPolarFrameTransportPrincipalPhaseBranch,
    EndpointSewingAction,
    FrameRotationAction,
)
from projectkoios.physkit.units import PhysicalUnit

from ksdft2effmass.analysis.matrix_field.diagnostics import ScalarRefinementAnalyzer
from ksdft2effmass.periodic1d.composite_band_alignment import (
    Periodic1DCompositeBandAlignmentConfiguration,
)
from ksdft2effmass.periodic1d.fourier_locality import (
    Periodic1DFourierLocalityConfiguration,
)
from ksdft2effmass.periodic1d.gauge_alignment import Periodic1DGaugeAlignment
from ksdft2effmass.periodic1d.gauge_alignment.factory import (
    Periodic1DAlignmentStudyFactory,
    Periodic1DRank1AlignmentStudySpecification,
    Periodic1DRank2AlignmentStudyAnalyzer,
    Periodic1DRank2AlignmentStudySpecification,
    Periodic1DRankNAlignmentStudyAnalyzer,
    Periodic1DRankNAlignmentStudySpecification,
)
from ksdft2effmass.periodic1d.geometry import Periodic1DLatticeGeometry
from ksdft2effmass.periodic1d.higher_rank_alignment import (
    Periodic1DRankNAlignmentCalculationControls,
    Periodic1DRankNAlignmentCalculationRequest,
    Periodic1DRankNAlignmentConfiguration,
)
from ksdft2effmass.periodic1d.rank1.alignment import (
    Periodic1DRank1AlignmentApplicabilityAnalyzer,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestPeriodic1DAlignmentStudyFactory:
    """Establish explicit lattice binding and closed exact-type dispatch."""

    @staticmethod
    def rank1_configuration() -> Periodic1DFourierLocalityConfiguration:
        configuration_type = Periodic1DFourierLocalityConfiguration
        return configuration_type(
            parent_identity=configuration_type.PARENT_IDENTITY,
            onsite_numerators=configuration_type.PARENT_ONSITE_NUMERATORS,
            positive_hopping_numerators=(
                configuration_type.PARENT_POSITIVE_HOPPING_NUMERATORS
            ),
            coefficient_denominator=(
                configuration_type.PARENT_COEFFICIENT_DENOMINATOR
            ),
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

    @staticmethod
    def rank2_configuration() -> Periodic1DCompositeBandAlignmentConfiguration:
        configuration_type = Periodic1DCompositeBandAlignmentConfiguration
        return configuration_type(
            parent_identity=configuration_type.PARENT_IDENTITY,
            onsite_numerators=configuration_type.PARENT_ONSITE_NUMERATORS,
            positive_hopping_numerators=(
                configuration_type.PARENT_POSITIVE_HOPPING_NUMERATORS
            ),
            coefficient_denominator=(
                configuration_type.PARENT_COEFFICIENT_DENOMINATOR
            ),
            retained_rank=2,
            construction_size=64,
            evaluation_size=257,
            evaluation_shift_numerator=1,
            evaluation_shift_denominator=65,
            hopping_ranges=configuration_type.HOPPING_RANGES,
            attack_constant_angle=0.30,
            attack_sine_coefficients=(0.65, 0.30),
            sampled_gap_threshold=0.5,
            overlap_singular_value_threshold=0.8,
            procrustes_rank_absolute_tolerance=1.0e-14,
            procrustes_rank_relative_tolerance=1.0e-12,
            energy_absolute_tolerance=1.0e-11,
            dimensionless_absolute_tolerance=1.0e-12,
        )

    @staticmethod
    def rankn_request() -> Periodic1DRankNAlignmentCalculationRequest:
        configuration_type = Periodic1DRankNAlignmentConfiguration
        configuration = configuration_type(
            family_identity=configuration_type.FAMILY_IDENTITY,
            version_identity=configuration_type.VERSION_IDENTITY,
            retained_ranks=configuration_type.RETAINED_RANKS,
            circuit_depths=configuration_type.CIRCUIT_DEPTHS,
            construction_mesh_sizes=configuration_type.CONSTRUCTION_MESH_SIZES,
            final_construction_mesh_size=(
                configuration_type.FINAL_CONSTRUCTION_MESH_SIZE
            ),
            global_unitary_selection_mesh_size=(
                configuration_type.GLOBAL_UNITARY_SELECTION_MESH_SIZE
            ),
            evaluation_mesh_size=configuration_type.EVALUATION_MESH_SIZE,
            evaluation_shift_numerator=(
                configuration_type.EVALUATION_SHIFT_NUMERATOR
            ),
            evaluation_shift_denominator=(
                configuration_type.EVALUATION_SHIFT_DENOMINATOR
            ),
            gauge_alignments=configuration_type.GAUGE_ALIGNMENTS,
            frame_rotation_action=FrameRotationAction.RIGHT,
            endpoint_sewing_action=EndpointSewingAction.LEFT_AMBIENT,
            principal_phase_branch=(
                ClosedLoopPolarFrameTransportPrincipalPhaseBranch.negative_pi_open
            ),
            rank_cutoff_rule=ComplexUnitaryProcrustesRankCutoffRule.MAXIMUM,
            rank_absolute_tolerance=configuration_type.RANK_ABSOLUTE_TOLERANCE,
            rank_relative_tolerance=configuration_type.RANK_RELATIVE_TOLERANCE,
            backend_validation_absolute_tolerance=(
                configuration_type.BACKEND_VALIDATION_ABSOLUTE_TOLERANCE
            ),
            backend_validation_relative_tolerance=(
                configuration_type.BACKEND_VALIDATION_RELATIVE_TOLERANCE
            ),
            endpoint_and_primitive_closure_tolerance=(
                configuration_type.ENDPOINT_AND_PRIMITIVE_CLOSURE_TOLERANCE
            ),
            maximum_closure_phase_tolerance=(
                configuration_type.MAXIMUM_CLOSURE_PHASE_TOLERANCE
            ),
        )
        return Periodic1DRankNAlignmentCalculationRequest(
            configuration=configuration,
            controls=Periodic1DRankNAlignmentCalculationControls.frozen(),
            retained_rank=3,
            circuit_depth=1,
            ambient_basis_identifier=(
                "analytic-parent-ordered-retained-exterior-basis"
            ),
            retained_frame_identifier="analytic-retained-coordinate-frame",
            endpoint_sewing_identifier="analytic-periodic-identity-sewing",
            represented_basis_identifier="aligned-retained-orbital-basis",
            energy_reference_identifier="analytic-selected-energy-reference",
        )

    def test__create__binds_explicit_lattices_without_executing_studies(self) -> None:
        rank1_geometry = Periodic1DLatticeGeometry.from_direct_lattice(
            DirectLattice1D(2.0),
            PhysicalUnit("angstrom"),
        )
        rank2_geometry = Periodic1DLatticeGeometry.from_direct_lattice(
            DirectLattice1D(3.0),
            PhysicalUnit("bohr"),
        )
        rankn_geometry = Periodic1DLatticeGeometry.from_direct_lattice(
            DirectLattice1D(4.0),
            PhysicalUnit("nanometer"),
        )
        rank1 = Periodic1DAlignmentStudyFactory.create(
            Periodic1DRank1AlignmentStudySpecification(
                lattice_geometry=rank1_geometry,
                configuration=self.rank1_configuration(),
            )
        )
        rank2 = Periodic1DAlignmentStudyFactory.create(
            Periodic1DRank2AlignmentStudySpecification(
                lattice_geometry=rank2_geometry,
                configuration=self.rank2_configuration(),
                procrustes_solver=NumpyBatchedComplexUnitaryProcrustesSolver(),
            )
        )
        rankn = Periodic1DAlignmentStudyFactory.create(
            Periodic1DRankNAlignmentStudySpecification(
                lattice_geometry=rankn_geometry,
                request=self.rankn_request(),
                procrustes_solver=NumpyBatchedComplexUnitaryProcrustesSolver(),
                transporter=ClosedLoopPolarFrameTransporter(),
                scalar_refinement_analyzer=ScalarRefinementAnalyzer(),
            )
        )

        assert type(rank1) is Periodic1DRank1AlignmentApplicabilityAnalyzer
        assert type(rank2) is Periodic1DRank2AlignmentStudyAnalyzer
        assert type(rankn) is Periodic1DRankNAlignmentStudyAnalyzer
        assert all(
            isinstance(action, Periodic1DGaugeAlignment)
            for action in (rank1, rank2, rankn)
        )
        assert rank1.direct_lattice.lattice_constant == 2.0
        assert rank1.lattice_geometry.lattice_unit == PhysicalUnit("angstrom")
        assert rank2.direct_lattice.lattice_constant == 3.0
        assert rank2.lattice_geometry.lattice_unit == PhysicalUnit("bohr")
        assert rankn.direct_lattice.lattice_constant == 4.0
        assert rankn.lattice_geometry.lattice_unit == PhysicalUnit("nanometer")

    def test__specifications__reject_untyped_lattice_geometry(self) -> None:
        with pytest.raises(TypeError, match="lattice_geometry"):
            Periodic1DRank1AlignmentStudySpecification(
                lattice_geometry=object(),  # type: ignore[arg-type]
                configuration=self.rank1_configuration(),
            )
        with pytest.raises(TypeError, match="lattice_geometry"):
            Periodic1DRank2AlignmentStudySpecification(
                lattice_geometry=object(),  # type: ignore[arg-type]
                configuration=self.rank2_configuration(),
                procrustes_solver=NumpyBatchedComplexUnitaryProcrustesSolver(),
            )
        with pytest.raises(TypeError, match="lattice_geometry"):
            Periodic1DRankNAlignmentStudySpecification(
                lattice_geometry=object(),  # type: ignore[arg-type]
                request=self.rankn_request(),
                procrustes_solver=NumpyBatchedComplexUnitaryProcrustesSolver(),
                transporter=ClosedLoopPolarFrameTransporter(),
                scalar_refinement_analyzer=ScalarRefinementAnalyzer(),
            )

    def test__create__rejects_untyped_rank_dispatch(self) -> None:
        with pytest.raises(TypeError, match="unsupported"):
            Periodic1DAlignmentStudyFactory.create(1)  # type: ignore[call-overload]
