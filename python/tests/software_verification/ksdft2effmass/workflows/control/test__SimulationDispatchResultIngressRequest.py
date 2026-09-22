r"""Software verification of ``SimulationDispatchResultIngressRequest``.

Evidence profile: routine

Bounded artifact scope: the immutable terminal result-ingress request.

Facet and represented meaning

The request retains the exact reconciliation and complete terminal record group.

Intrinsic and cross-object scope

This module verifies the request field contract only; integrated replay is owned by the
result-ingress preparer evidence.

VVUQ and scientific exclusions

This is software verification only and establishes no persistence, external effect,
scientific validation, uncertainty quantification, or human acceptance.
"""

from dataclasses import fields

import pytest

from ksdft2effmass.workflows import SimulationDispatchResultIngressRequest

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchResultIngressRequest


class TestSimulationDispatchResultIngressRequest:
    """Own public-field evidence for terminal ingress requests."""

    def test_fields__contract__retains_complete_terminal_group(self) -> None:
        """Retain every exact input needed for replay-verified atomic admission.

        Evidence ID: SV-WCI-RESULT-INGRESS-REQUEST-001
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "predecessor_run",
            "runtime_bundle",
            "reconciliation_result",
            "next_revision_identity",
            "terminal_attempt",
            "invocation_outcome",
            "dispatch_outcome",
            "obligation_dispositions",
            "result_references",
            "result_productions",
            "native_output_admissions",
            "failures",
            "transition",
        )
