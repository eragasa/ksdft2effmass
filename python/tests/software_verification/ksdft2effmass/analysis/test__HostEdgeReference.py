r"""Software verification of ``HostEdgeReference``.

Evidence profile: routine

Bounded artifact scope: exact host spectral-edge identity and energy quantity.

Facet and represented meaning

The DataObject names one energy reference consumed by below-edge analysis without
inferring it from a defect spectrum.

Intrinsic and cross-object scope

A finite electron-volt edge and empty-identity rejection are included.

VVUQ and scientific exclusions

The value is synthetic test data, not a literature value, material validation, UQ,
campaign execution, or human acceptance.
"""

import pytest

from ksdft2effmass.analysis.finite_domain_spectra import HostEdgeReference
from ksdft2effmass.operators import PhysicalUnit, ScalarQuantity

pytestmark = pytest.mark.software_verification
SUT = HostEdgeReference


class TestHostEdgeReference:
    """Own software evidence for explicit host-edge identity."""

    def test_constructor__identity_and_energy__requires_explicit_values(self) -> None:
        """Evidence ID: SV-ANALYSIS-HOST-EDGE-001

        Requirement: Host edges have a nonempty identity and explicit finite energy.

        Acceptance: A zero-electron-volt edge is retained and an empty identity raises
        ``ValueError``.
        """
        edge = HostEdgeReference(
            "host_lower_edge", ScalarQuantity(0.0, PhysicalUnit("electron_volt"))
        )

        assert edge.energy.magnitude == 0.0
        with pytest.raises(ValueError, match="nonempty"):
            HostEdgeReference("", edge.energy)
