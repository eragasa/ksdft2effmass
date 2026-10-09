"""Route and import-independence evidence for periodic crosswalk row 064.

Evidence profile: claim_bearing

This module checks canonical Python ownership and former-route removal only. It does not
reconstruct the oracle, broaden its qualified evidence class or validity domain,
validate a physical model, quantify uncertainty, or record acceptance.
"""

import subprocess
import sys
from pathlib import Path

import pytest

from ksdft2effmass.periodic1d.campaign import oracle
from ksdft2effmass.periodic1d.campaign.oracle import finite_rank

pytestmark = pytest.mark.software_verification


class TestCanonicalFiniteRankOracleFamily:
    """Own canonical-route and transitional-import-removal evidence."""

    def test_public_facades__expose_defining_class_objects(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-064-001."""
        assert oracle.FiniteRankOracleCampaign is finite_rank.FiniteRankOracleCampaign
        assert (
            oracle.FiniteRankOracleEncodedDocuments
            is finite_rank.FiniteRankOracleEncodedDocuments
        )
        assert finite_rank.FiniteRankOracleCampaign.__module__.startswith(
            "ksdft2effmass.periodic1d.campaign.oracle.finite_rank"
        )

    def test_canonical_import__avoids_transitional_campaign(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-064-002."""
        code = """
import sys
import ksdft2effmass.periodic1d.campaign.oracle.finite_rank
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
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-064-003."""
        repository_root = Path(__file__).resolve().parents[8]
        former = repository_root / (
            "python/src/ksdft2effmass/campaigns/periodic_1d/defects/finite_rank_oracle"
        )
        assert not former.exists()
