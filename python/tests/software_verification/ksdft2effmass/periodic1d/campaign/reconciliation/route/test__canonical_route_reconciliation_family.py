"""Route and import-independence evidence for periodic crosswalk row 066.

Evidence profile: claim_bearing

This module checks canonical Python ownership and former-route removal only. It does not
establish common-space compatibility, route convergence, physical validation,
uncertainty quantification, or acceptance.
"""

import subprocess
import sys
from pathlib import Path

import pytest

from ksdft2effmass.periodic1d.campaign import reconciliation
from ksdft2effmass.periodic1d.campaign.reconciliation import route

pytestmark = pytest.mark.software_verification


class TestCanonicalRouteReconciliationFamily:
    """Own canonical-route and transitional-import-removal evidence."""

    def test_public_facades__expose_defining_class_objects(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-066-001."""
        assert (
            reconciliation.RouteReconciliationCampaign
            is route.RouteReconciliationCampaign
        )
        assert (
            reconciliation.RouteReconciliationEncodedDocuments
            is route.RouteReconciliationEncodedDocuments
        )
        assert route.RouteReconciliationCampaign.__module__.startswith(
            "ksdft2effmass.periodic1d.campaign.reconciliation.route"
        )

    def test_canonical_import__avoids_transitional_campaign(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-066-002."""
        code = """
import sys
import ksdft2effmass.periodic1d.campaign.reconciliation.route
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
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-066-003."""
        repository_root = Path(__file__).resolve().parents[8]
        former = repository_root / (
            "python/src/ksdft2effmass/campaigns/periodic_1d/defects/"
            "route_reconciliation"
        )
        assert not former.exists()
