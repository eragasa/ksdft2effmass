r"""Artifact-owned route evidence for the row-062 blind-alignment family move.

Evidence profile: claim_bearing

The tests establish canonical class identity, curated facades, mirrored implementation
and test ownership, and removal of the former source package without forwarding aliases.
They do not authenticate transitive campaign sources, reconstruct numerical results,
validate physical adequacy, quantify uncertainty, or establish acceptance.
"""

import importlib.util
from pathlib import Path

import pytest

from ksdft2effmass.periodic1d.campaign import alignment as alignment_facade
from ksdft2effmass.periodic1d.campaign.alignment import blind as blind_facade
from ksdft2effmass.periodic1d.campaign.alignment.blind.campaign import (
    BlindAlignmentCampaign,
)
from ksdft2effmass.periodic1d.campaign.alignment.blind.encoded_documents import (
    BlindAlignmentEncodedDocuments,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestCanonicalBlindAlignmentFamily:
    """Own canonical-route and retired-route evidence for row 062."""

    repository_root = Path(__file__).resolve().parents[8]

    def test_facades__export_defining_class_objects_only(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-062-001.

        Requirement: Canonical campaign, alignment, and blind facades must expose the
        same defining campaign and encoded-document class objects.

        Method: Compare facade attributes by identity and inspect both child-facade
        export inventories.

        Oracle: The reviewed row-062 facade contract.

        Acceptance: Every supported route resolves to the defining class object and
        child facades export exactly the two reviewed names.

        Interpretation: A pass establishes deliberate canonical imports without class
        duplication or a dynamic registry.

        Limitations: Import identity does not establish campaign numerical behavior.
        """
        for facade in (alignment_facade, blind_facade):
            assert facade.BlindAlignmentCampaign is BlindAlignmentCampaign
            assert (
                facade.BlindAlignmentEncodedDocuments is BlindAlignmentEncodedDocuments
            )
        expected = ["BlindAlignmentCampaign", "BlindAlignmentEncodedDocuments"]
        assert alignment_facade.__all__ == expected
        assert blind_facade.__all__ == expected

    def test_former_route__is_absent_without_forwarding_alias(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-062-002.

        Requirement: The former underscored defect-package route must be removed rather
        than retained as a compatibility alias.

        Method: Check module discovery and the former tracked source location.

        Oracle: The no-compatibility-alias migration policy.

        Acceptance: Discovery returns no module specification and no former Python
        source directory exists.

        Interpretation: A pass establishes route removal in this worktree.

        Limitations: It does not inspect separately installed historical distributions.
        """
        former = "ksdft2effmass.campaigns.periodic_1d.defects.blind_alignment"
        assert importlib.util.find_spec(former) is None
        assert not (
            self.repository_root
            / "python/src/ksdft2effmass/campaigns/periodic_1d/defects/blind_alignment"
        ).exists()

    def test_layout__mirrors_canonical_implementation_namespace(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-062-003.

        Requirement: Maintained software tests must mirror canonical implementation
        ownership rather than the retired underscored namespace.

        Method: Compare the package suffixes of this test and the defining source files.

        Oracle: The repository test-layout policy.

        Acceptance: Source and test family directories have the same
        ``periodic1d/campaign/alignment/blind`` suffix.

        Interpretation: A pass establishes discoverable ownership for future evidence.

        Limitations: Layout agreement does not qualify the scientific claims of tests.
        """
        source_suffix = Path("periodic1d/campaign/alignment/blind")
        source_root = self.repository_root / "python/src/ksdft2effmass" / source_suffix
        test_root = (
            self.repository_root
            / "python/tests/software_verification/ksdft2effmass"
            / source_suffix
        )
        assert source_root.is_dir()
        assert test_root == Path(__file__).parent
