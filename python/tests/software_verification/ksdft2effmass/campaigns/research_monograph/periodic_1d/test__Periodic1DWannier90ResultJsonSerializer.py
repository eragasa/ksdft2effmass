r"""Software verification of ``Periodic1DWannier90ResultJsonSerializer``.

Evidence profile: claim_bearing

Bounded artifact scope: retained Appendix G Wannier90 Wilson-center adaptation.

Facet and represented meaning

Direct Wilson phases, phase-derived centers, reported centers, and circular defects are
included for original and preconditioned retained results.

Intrinsic and cross-object scope

The public Wilson comparator reconstructs the reported center-set defect.

VVUQ and scientific exclusions

The adapter does not execute Wannier90 or interpret a phase set as topology.
"""

from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DRetainedResultKind,
    Periodic1DWannier90ResultJsonSerializer,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DWannier90ResultJsonSerializer


class TestPeriodic1DWannier90ResultJsonSerializer:
    """Own retained Wannier90 Wilson-center adaptation evidence."""

    @pytest.mark.parametrize(
        ("kind", "filename", "expected_defect"),
        (
            pytest.param(
                Periodic1DRetainedResultKind.WANNIER90,
                "wannier90-result.json",
                0.18118978430194888,
                id="native_localization_campaign",
            ),
            pytest.param(
                Periodic1DRetainedResultKind.WANNIER90_PRECONDITIONED,
                "wannier90-preconditioned-result.json",
                2.156980511980322e-07,
                id="preconditioned_native_campaign",
            ),
        ),
    )
    def test_method__deserialize__reconstructs_circular_center_comparison(
        self,
        kind: Periodic1DRetainedResultKind,
        filename: str,
        expected_defect: float,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-015

        Requirement: Both retained routes use one typed Wilson-center comparison.

        Method: Deserialize each retained format and inspect the low-pair comparison.

        Oracle: Reported defects and independently reconstructed circular matching.

        Acceptance: Spectrum rank is two and the reconstructed defect equals the wire.

        Interpretation: A pass establishes typed Wilson-center compatibility.

        Limitations: Convergence status is retained rather than inferred.

        Provenance: Original and preconditioned Appendix G result artifacts.
        """
        root = Path(__file__).resolve().parents[7]
        payload = (
            root / "calculations/research-monograph/periodic-1d" / filename
        ).read_bytes()

        result = SUT(kind).deserialize(payload)
        low_pair = result.groups[0]

        assert low_pair.direct_spectrum.rank == 2
        assert low_pair.recorded_center_set_circular_maximum_defect == expected_defect
        assert low_pair.center_phase_comparison.passes
