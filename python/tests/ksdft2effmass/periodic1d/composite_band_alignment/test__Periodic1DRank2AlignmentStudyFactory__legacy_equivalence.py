"""Factory-route equivalence for the maintained rank-two alignment calculation."""

import pytest
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesSolver,
)
from projectkoios.physkit.periodic.lattice import DirectLattice1D
from projectkoios.physkit.units import PhysicalUnit

from ksdft2effmass.periodic1d.composite_band_alignment import (
    Periodic1DCompositeBandAlignmentCalculationResult,
    Periodic1DCompositeBandAlignmentConfiguration,
)
from ksdft2effmass.periodic1d.gauge_alignment.factory import (
    Periodic1DAlignmentStudyFactory,
    Periodic1DRank2AlignmentStudySpecification,
)
from ksdft2effmass.periodic1d.geometry import Periodic1DLatticeGeometry

pytestmark = [
    pytest.mark.integration,
    pytest.mark.software_verification,
    pytest.mark.legacy_equivalence,
]


class TestPeriodic1DAlignmentStudyFactoryRank2LegacyEquivalence:
    """Establish that factory dispatch does not change retained result bytes."""

    def test__execute__preserves_direct_analyzer_bytes(
        self,
        composite_configuration: Periodic1DCompositeBandAlignmentConfiguration,
        composite_result: Periodic1DCompositeBandAlignmentCalculationResult,
    ) -> None:
        action = Periodic1DAlignmentStudyFactory.create(
            Periodic1DRank2AlignmentStudySpecification(
                lattice_geometry=Periodic1DLatticeGeometry.from_direct_lattice(
                    DirectLattice1D(1.0),
                    PhysicalUnit("bohr"),
                ),
                configuration=composite_configuration,
                procrustes_solver=NumpyBatchedComplexUnitaryProcrustesSolver(),
            )
        )

        assert action.execute().to_json() == composite_result.to_json()
