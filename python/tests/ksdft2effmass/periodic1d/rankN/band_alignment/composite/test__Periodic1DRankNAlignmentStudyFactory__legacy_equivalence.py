"""Factory-route equivalence for the maintained rank-N alignment calculation."""

import pytest
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesSolver,
)
from projectkoios.physkit.periodic.lattice import DirectLattice1D
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
)
from projectkoios.physkit.units import PhysicalUnit

from ksdft2effmass.analysis.matrix_field.diagnostics import ScalarRefinementAnalyzer
from ksdft2effmass.periodic1d.gauge_alignment.factory import (
    Periodic1DAlignmentStudyFactory,
    Periodic1DRankNAlignmentStudySpecification,
)
from ksdft2effmass.periodic1d.geometry import Periodic1DLatticeGeometry
from ksdft2effmass.periodic1d.rankN.band_alignment.calculation import (
    Periodic1DRankNAlignmentCalculationRequest,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.calculation_result import (
    Periodic1DRankNAlignmentCalculationResult,
)

pytestmark = [
    pytest.mark.integration,
    pytest.mark.software_verification,
    pytest.mark.legacy_equivalence,
    pytest.mark.expensive,
]


class TestPeriodic1DAlignmentStudyFactoryRankNLegacyEquivalence:
    """Establish that factory dispatch does not change retained result bytes."""

    def test__execute__preserves_direct_analyzer_bytes(
        self,
        higher_rank_calculation_request: Periodic1DRankNAlignmentCalculationRequest,
        higher_rank_calculation_result: Periodic1DRankNAlignmentCalculationResult,
    ) -> None:
        action = Periodic1DAlignmentStudyFactory(
            Periodic1DRankNAlignmentStudySpecification(
                lattice_geometry=Periodic1DLatticeGeometry.from_direct_lattice(
                    DirectLattice1D(1.0),
                    PhysicalUnit("bohr"),
                ),
                request=higher_rank_calculation_request,
                procrustes_solver=NumpyBatchedComplexUnitaryProcrustesSolver(),
                transporter=ClosedLoopPolarFrameTransporter(),
                scalar_refinement_analyzer=ScalarRefinementAnalyzer(),
            )
        ).create()

        assert action.execute().to_json() == higher_rank_calculation_result.to_json()
