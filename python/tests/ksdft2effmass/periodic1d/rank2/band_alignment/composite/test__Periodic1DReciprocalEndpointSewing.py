"""Tests for explicit rank-two reciprocal-endpoint sewing composition."""

import numpy as np
import pytest
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesSolver,
)
from projectkoios.physkit.units import ComplexMatrixQuantity, Unitless

from ksdft2effmass.periodic1d.rank2.band_alignment.composite.analysis import (
    Periodic1DCompositeBandAlignmentAnalyzer,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.configuration import (
    Periodic1DCompositeBandAlignmentConfiguration,
)
from ksdft2effmass.sewing import (
    IdentityReciprocalSewing,
    ReciprocalEndpointSewingMap,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DReciprocalEndpointSewing:
    """Establish explicit immutable sewing values and composition-time swapping."""

    def test__identity__constructs_the_declared_ambient_map(self) -> None:
        sewing = IdentityReciprocalSewing(ambient_dimension=4).endpoint_map

        assert sewing.identifier == "identity-periodic-endpoint-sewing.v1"
        assert sewing.ambient_dimension == 4
        assert type(sewing.coefficient_map.unit) is Unitless
        assert np.array_equal(
            sewing.coefficient_map.magnitude,
            np.eye(4, dtype=np.complex128),
        )
        assert not sewing.coefficient_map.magnitude.flags.writeable

    def test__analyzer__retains_a_caller_selected_sewing_map(
        self,
        composite_configuration: Periodic1DCompositeBandAlignmentConfiguration,
    ) -> None:
        phases = np.exp(1.0j * np.asarray((0.0, 0.2, -0.3, 0.4), dtype=np.float64))
        sewing = ReciprocalEndpointSewingMap(
            identifier="diagonal-phase-endpoint-sewing.test",
            coefficient_map=ComplexMatrixQuantity(
                np.diag(phases).astype(np.complex128),
                Unitless(),
            ),
        )

        analyzer = Periodic1DCompositeBandAlignmentAnalyzer(
            composite_configuration,
            NumpyBatchedComplexUnitaryProcrustesSolver(),
            sewing,
        )

        assert analyzer.endpoint_sewing is sewing

    def test__analyzer__rejects_a_sewing_map_for_another_ambient_space(
        self,
        composite_configuration: Periodic1DCompositeBandAlignmentConfiguration,
    ) -> None:
        sewing = IdentityReciprocalSewing(ambient_dimension=2).endpoint_map

        with pytest.raises(ValueError, match="ambient dimension"):
            Periodic1DCompositeBandAlignmentAnalyzer(
                composite_configuration,
                NumpyBatchedComplexUnitaryProcrustesSolver(),
                sewing,
            )
