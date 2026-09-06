r"""Software verification of ``SimulationDispatchPreparationResult``.

Evidence profile: routine

Bounded artifact scope: the public dispatch-preparation result DataObject.

Facet and represented meaning

The immutable result distinguishes replay-verified candidates from denied and
fail-closed preparation outcomes.

Intrinsic and cross-object scope

This module verifies the closed public field inventory. Variant behavior belongs to
the preparer owner.

VVUQ and scientific exclusions

This is software verification only; it provides no persistence, calculation,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

from dataclasses import fields

import pytest

from ksdft2effmass.workflows.control import SimulationDispatchPreparationResult

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchPreparationResult


class TestSimulationDispatchPreparationResult:
    """Own software evidence for the dispatch-preparation result DataObject."""

    def test_fields__public_contract__is_exact(self) -> None:
        """Keep the closed public result field inventory.

        Evidence ID: SV-WFC-DISPATCH-PREPARATION-RESULT-001
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "kind",
            "request",
            "authorization_result",
            "predecessor_replay_result",
            "candidate_run",
            "candidate_replay_result",
            "diagnostics",
        )
