r"""Software verification of ``SimulationDispatchPreparationOutcomeKind``.

Evidence profile: routine

Bounded artifact scope: the public dispatch-preparation outcome enum.

Facet and represented meaning

The enum closes effect-free dispatch preparation to prepared, denied, or error.

Intrinsic and cross-object scope

This module verifies only the exact closed public vocabulary.

VVUQ and scientific exclusions

This is software verification only and grants no persistence, external execution,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows.control import (
    SimulationDispatchPreparationOutcomeKind,
)

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchPreparationOutcomeKind


class TestSimulationDispatchPreparationOutcomeKind:
    """Own software evidence for preparation outcome discrimination."""

    def test_members__public_contract__is_closed(self) -> None:
        """Keep the exact closed outcome vocabulary.

        Evidence ID: SV-WFC-DISPATCH-PREPARATION-OUTCOME-KIND-001
        """
        assert tuple(member.value for member in SUT) == (
            "prepared",
            "denied",
            "error",
        )
