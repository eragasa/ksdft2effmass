"""Verify removal of obsolete hopping-reduction Workflow surfaces."""

from importlib.util import find_spec

from ksdft2effmass.campaigns import periodic_1d
from ksdft2effmass.campaigns.periodic_1d import compare, workflows


class TestHoppingReductionWorkflowRetirement:
    """Keep retired Workflow modules and public names absent."""

    def test_modules__retired_hopping_workflows__are_absent(self) -> None:
        """The removed analysis and campaign facades have no importable modules."""
        assert find_spec("ksdft2effmass.analysis.single_band_reduction") is None
        assert find_spec("ksdft2effmass.campaigns.periodic_1d.compare.hopping") is None

    def test_public_surfaces__retired_hopping_workflows__are_absent(self) -> None:
        """No package or owner module re-exports the removed Workflow contracts."""
        retired = (
            "Periodic1DHoppingReductionRequest",
            "Periodic1DHoppingReductionResult",
            "Periodic1DHoppingReductionWorkflow",
        )
        for module in (periodic_1d, compare, workflows):
            for name in retired:
                assert not hasattr(module, name)
