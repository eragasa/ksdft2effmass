"""Software verification of ``Periodic1DRetainedBandGroupDefinition``.

Evidence profile: routine

Facet and represented meaning
-----------------------------
The class names one parent-qualified selected-band retention definition.

Intrinsic and cross-object scope
--------------------------------
Exact identity, composition, ordered indices, and delegated rank are covered.

VVUQ and scientific exclusions
------------------------------
Synthetic records establish software behavior only, not band isolation, numerical
verification, scientific validation, or uncertainty quantification.
"""

import pytest

from ksdft2effmass.analysis.periodic_bands import ContiguousBandSelection
from ksdft2effmass.periodic import (
    PeriodicOperatorReference,
    PeriodicRetentionDefinition,
    PeriodicRetentionKind,
)
from ksdft2effmass.periodic1d import (
    Periodic1DRetainedBandGroupDefinition,
    Periodic1DSelectedBandRetentionDefinition,
)

pytestmark = pytest.mark.software_verification


class TestPeriodic1DRetainedBandGroupDefinition:
    """Own software evidence for named retained band groups."""

    @staticmethod
    def make_retained_bands() -> Periodic1DSelectedBandRetentionDefinition:
        """Return one synthetic parent-qualified two-band definition."""
        selection = ContiguousBandSelection(2, 3)
        retention = PeriodicRetentionDefinition(
            "test.retention.higher-pair",
            PeriodicOperatorReference("parent", "hamiltonian", "bloch-space", 1),
            "test.retained-space.higher-pair",
            PeriodicRetentionKind.SELECTED_BANDS,
            2,
            ("band-2", "band-3"),
            "primitive-zone",
            "test.selection.higher-pair",
            (),
            "test.provenance",
        )
        return Periodic1DSelectedBandRetentionDefinition(retention, selection)

    def test_construction__group__preserves_parent_qualified_order_and_rank(
        self,
    ) -> None:
        """Evidence ID: SV-PERIODIC1D-RETAINED-GROUP-001

        Requirement: A named group composes, without duplicating, one complete
        parent-qualified selected-band definition.

        Acceptance: Identity, composed object, ordered bounds, and rank equal the
        authored exact values.
        """
        retained_bands = self.make_retained_bands()
        group = Periodic1DRetainedBandGroupDefinition("higher_pair", retained_bands)

        assert group.identifier == "higher_pair"
        assert group.retained_bands is retained_bands
        assert group.lower_index == 2
        assert group.upper_index == 3
        assert group.band_count == 2

    def test_construction__identifier__rejects_empty_group_identity(self) -> None:
        """Evidence ID: SV-PERIODIC1D-RETAINED-GROUP-002

        Requirement: Every retained group has a nonempty stable identity.

        Acceptance: Empty identity raises ``ValueError``.
        """
        with pytest.raises(ValueError, match="identifier must be nonempty"):
            Periodic1DRetainedBandGroupDefinition("", self.make_retained_bands())
