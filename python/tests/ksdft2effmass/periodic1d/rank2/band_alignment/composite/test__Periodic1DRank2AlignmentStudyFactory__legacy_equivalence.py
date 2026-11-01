"""Factory-route equivalence for the maintained rank-two alignment calculation."""

import hashlib

import pytest
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesSolver,
)
from projectkoios.physkit.periodic.lattice import DirectLattice1D
from projectkoios.physkit.units import PhysicalUnit

from ksdft2effmass.periodic1d.gauge_alignment.factory import (
    Periodic1DAlignmentStudyFactory,
    Periodic1DRank2AlignmentStudySpecification,
)
from ksdft2effmass.periodic1d.geometry import Periodic1DLatticeGeometry
from ksdft2effmass.periodic1d.rank2.band_alignment.composite import (
    Periodic1DCompositeBandAlignmentCalculationResult,
    Periodic1DCompositeBandAlignmentConfiguration,
)

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
        action = Periodic1DAlignmentStudyFactory(
            Periodic1DRank2AlignmentStudySpecification(
                lattice_geometry=Periodic1DLatticeGeometry.from_direct_lattice(
                    DirectLattice1D(1.0),
                    PhysicalUnit("bohr"),
                ),
                configuration=composite_configuration,
                procrustes_solver=NumpyBatchedComplexUnitaryProcrustesSolver(),
            )
        ).create()

        direct_bytes = composite_result.to_json()

        assert action.execute().to_json() == direct_bytes
        assert hashlib.sha256(direct_bytes).hexdigest() == (
            "7c8a65f14f480c22e4eeeeae26f56ef7f0116accec0a16f80bb7c0cf7931f0f7"
        )
