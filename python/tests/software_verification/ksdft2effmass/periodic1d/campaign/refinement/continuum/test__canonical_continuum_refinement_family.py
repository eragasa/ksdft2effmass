"""Route and import-independence evidence for periodic crosswalk row 063.

Evidence profile: claim_bearing

This module checks canonical Python ownership and former-route removal only. It does not
reconstruct retained numerics, establish a continuum limit or convergence, validate a
physical model, quantify uncertainty, or record acceptance.
"""

import subprocess
import sys
from pathlib import Path

import pytest

from ksdft2effmass.periodic1d.campaign import refinement
from ksdft2effmass.periodic1d.campaign.refinement import continuum

pytestmark = pytest.mark.software_verification


class TestCanonicalContinuumRefinementFamily:
    """Own canonical-route and transitional-import-removal evidence."""

    def test_public_facades__expose_defining_class_objects(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-063-001."""
        assert (
            refinement.ContinuumRefinementCampaign
            is continuum.ContinuumRefinementCampaign
        )
        assert (
            refinement.ContinuumRefinementEncodedDocuments
            is continuum.ContinuumRefinementEncodedDocuments
        )
        assert continuum.ContinuumRefinementCampaign.__module__.startswith(
            "ksdft2effmass.periodic1d.campaign.refinement.continuum"
        )

    def test_canonical_import__avoids_transitional_campaign(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-063-002."""
        code = """
import sys
import ksdft2effmass.periodic1d.campaign.refinement.continuum
prefix = 'ksdft2effmass.campaigns.periodic_1d'
bad = sorted(name for name in sys.modules if name.startswith(prefix))
if bad:
    raise SystemExit('transitional imports: ' + ', '.join(bad))
"""
        completed = subprocess.run(
            [sys.executable, "-c", code],
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode == 0, completed.stderr or completed.stdout

    def test_former_source_package__is_absent(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-063-003."""
        repository_root = Path(__file__).resolve().parents[8]
        former = repository_root / (
            "python/src/ksdft2effmass/campaigns/periodic_1d/defects/"
            "continuum_refinement"
        )
        assert not former.exists()
