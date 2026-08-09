r"""Software verification of ``AgentRecordAdapter``.

Facet and represented meaning

The module verifies deterministic adaptation of explicitly supplied agent records.

Intrinsic and cross-object scope

``AgentRecordAdapter`` is the sole system under test.

VVUQ and scientific exclusions

Passing establishes software behavior only, not scientific validation or UQ.
"""

from typing import Any, cast

import pytest

from ksdft2effmass.harness.pi.local import AgentRecordAdapter

from .conftest import repository_root

pytestmark = pytest.mark.software_verification
SUT = AgentRecordAdapter


def test_method__execute__sorts_explicit_agent_records_by_identity() -> None:
    """Evidence ID: SV-HL-040

    Requirement: Explicit agent records are returned in deterministic identity order.

    Method: Supply two current agent documents in reverse lexical path order.

    Oracle: The adapter contract requires lexical ordering by represented agent
    identity.

    Acceptance: Adaptation passes and result identities equal their sorted tuple.

    Interpretation: Failure indicates ordering, parsing, or selected-input drift.

    Limitations: The test does not launch agents or establish scientific validity or UQ.
    """
    root = repository_root()
    paths = (
        ".pi/agents/ksdft2effmass-harness-local-test-parity-writer.md",
        ".pi/agents/ksdft2effmass-harness-local-python-writer.md",
    )
    result = AgentRecordAdapter().execute(
        tuple((path, (root / path).read_bytes()) for path in reversed(paths))
    )
    assert result.validation.status == "PASS"
    values = cast(Any, result.value)
    assert tuple(item.agent_id for item in values) == tuple(
        sorted(item.agent_id for item in values)
    )
