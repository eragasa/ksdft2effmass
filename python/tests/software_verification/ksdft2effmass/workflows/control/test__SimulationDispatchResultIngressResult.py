r"""Software verification of ``SimulationDispatchResultIngressResult``.

Evidence profile: routine

Bounded artifact scope: the immutable terminal result-ingress result.

Facet and represented meaning

The result retains exact predecessor and candidate replay evidence.

Intrinsic and cross-object scope

This module verifies the result field contract only; integrated replay is owned by the
result-ingress preparer evidence.

VVUQ and scientific exclusions

This is software verification only and establishes no persistence, external effect,
scientific validation, uncertainty quantification, or human acceptance.
"""

from dataclasses import fields

import pytest

from ksdft2effmass.workflows import SimulationDispatchResultIngressResult

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchResultIngressResult


class TestSimulationDispatchResultIngressResult:
    """Own public-field evidence for ingress results."""

    def test_fields__contract__retains_request_replays_and_candidate(self) -> None:
        """Retain exact request, predecessor evidence, and optional candidate evidence.

        Evidence ID: SV-WCI-RESULT-INGRESS-RESULT-001
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "kind",
            "request",
            "predecessor_replay_result",
            "candidate_run",
            "candidate_replay_result",
            "diagnostics",
        )
