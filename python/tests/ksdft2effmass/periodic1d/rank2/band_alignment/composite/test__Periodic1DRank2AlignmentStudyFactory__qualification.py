"""Factory-route numerical qualification for rank-two alignment."""

import numpy as np
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
from ksdft2effmass.periodic1d.rank2.band_alignment.composite.result import (
    Periodic1DCompositeBandAlignmentCalculationResult,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.composite.verification import (
    Periodic1DCompositeBandAlignmentVerifier,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.configuration import (
    Periodic1DCompositeBandAlignmentConfiguration,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestPeriodic1DAlignmentStudyFactoryRank2Qualification:
    """Establish route equivalence through scientific numerical invariants."""

    def test__execute__is_independently_qualified_without_byte_identity(
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

        routed = action.execute()

        assert routed.result_schema == composite_result.result_schema
        assert routed.configuration == composite_result.configuration
        assert np.allclose(
            routed.construction_parent_spectrum.magnitude,
            composite_result.construction_parent_spectrum.magnitude,
            rtol=0.0,
            atol=composite_configuration.energy_absolute_tolerance,
        )
        assert np.allclose(
            routed.global_rotation.magnitude,
            composite_result.global_rotation.magnitude,
            rtol=0.0,
            atol=10.0 * composite_configuration.dimensionless_absolute_tolerance,
        )
        assert np.allclose(
            routed.diagnostics.pointwise_procrustes.cross_singular_values,
            composite_result.diagnostics.pointwise_procrustes.cross_singular_values,
            rtol=0.0,
            atol=10.0 * composite_configuration.dimensionless_absolute_tolerance,
        )
        for result in (composite_result, routed):
            verified = Periodic1DCompositeBandAlignmentVerifier(
                result_wire=result.to_json()
            ).result()
            assert verified.verification.passed
