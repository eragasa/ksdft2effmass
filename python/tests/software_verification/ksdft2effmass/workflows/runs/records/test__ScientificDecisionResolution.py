r"""Software verification of ``ScientificDecisionResolution``.

Evidence profile: routine

Bounded artifact scope: the public ``ScientificDecisionResolution`` contract.

Facet and represented meaning

This module verifies intrinsic represented behavior owned by
``ScientificDecisionResolution``.

Intrinsic and cross-object scope

Constructor and field invariants belong to this class. Complete cross-record replay
and package-export agreement remain with their separate owners.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, persistence,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

from dataclasses import fields

import pytest

from ksdft2effmass.workflows.runs import (
    ScientificDecisionResolution,
)

pytestmark = pytest.mark.software_verification
SUT = ScientificDecisionResolution


class TestScientificDecisionResolution:
    """Own software evidence for ``ScientificDecisionResolution``."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose the exact documented immutable field inventory.

        Evidence ID: SV-WFR-SCIENTIFIC-DECISION-RESOLUTION-001

        Requirement: ``ScientificDecisionResolution`` declares exactly its
        documented public DataObject
        or ResultObject fields in constructor order.

        Acceptance: :func:`dataclasses.fields` returns the exact field-name tuple.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "identity",
            "content_identity",
            "request_identity",
            "verbatim_response",
            "normalized_option_identity",
            "response_source_identity",
            "authority_context_identity",
            "boundary_receipt_identity",
            "predecessor_resolution_identity",
            "supersedes_resolution_identity",
            "producer_provenance",
        )
