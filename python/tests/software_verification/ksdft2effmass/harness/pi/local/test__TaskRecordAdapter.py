r"""Software verification of ``TaskRecordAdapter``.

Facet and represented meaning

The module verifies explicit adaptation of selected project Task records.

Intrinsic and cross-object scope

``TaskRecordAdapter`` is the sole owner; chain and activation bytes are explicit inputs.

VVUQ and scientific exclusions

Passing establishes software behavior only, not scientific validation or UQ.
"""

import json
from typing import Any, cast

import pytest

from ksdft2effmass.harness.pi.local import TaskRecordAdapter

from .conftest import repository_root

pytestmark = pytest.mark.software_verification
SUT = TaskRecordAdapter


def selected_inputs() -> tuple[tuple[tuple[str, bytes], ...], bytes, bytes]:
    """Evidence ID: Owns no identifier; supports SV-HL-038.

    Requirement: The enclosing test requires explicit current H4 input bytes.

    Method: Read only the paths named by the fixed chain and activation records.

    Oracle: The selected repository files define the controlled setup bytes.

    Acceptance: Return Task documents, chain bytes, and activation bytes without
    adaptation.

    Interpretation: Failure indicates controlled setup drift.

    Limitations: This helper owns no independent evidence claim.
    """
    root = repository_root()
    chain_bytes = (root / ".pi/chains/pi-harness-incubation.chain.json").read_bytes()
    activation_bytes = (
        root / ".pi/evidence/pi-harness-incubation/H4/activation.json"
    ).read_bytes()
    chain = json.loads(chain_bytes)
    documents = tuple(
        (item["record"], (root / item["record"]).read_bytes())
        for item in reversed(chain["task_sequence"])
    )
    return documents, chain_bytes, activation_bytes


def test_method__execute__sorts_selected_tasks_and_fails_closed_when_missing() -> None:
    """Evidence ID: SV-HL-038

    Requirement: Explicitly selected Task records are complete and ordered
    deterministically.

    Method: Adapt the current reversed H4 selection, then omit H3 and adapt again.

    Oracle: The supplied chain selects H0 through H5 and requires every selected record.

    Acceptance: The complete result passes in lexical Task order; the incomplete result
    fails with
    no value and reports missing selected Task bytes.

    Interpretation: Failure indicates ordering drift or permissive fallback discovery.

    Limitations: The test does not establish chain semantics, scientific validity, or
    UQ.
    """
    documents, chain_bytes, activation_bytes = selected_inputs()
    result = TaskRecordAdapter().execute(documents, chain_bytes, activation_bytes)
    assert result.validation.status == "PASS"
    assert [item.task_id for item in cast(Any, result.value)] == [
        "H0",
        "H1",
        "H2",
        "H3",
        "H4",
        "H5",
    ]
    selected_chain = json.loads(chain_bytes)
    h3_path = next(
        item["record"] for item in selected_chain["task_sequence"] if item["id"] == "H3"
    )
    incomplete = TaskRecordAdapter().execute(
        tuple(item for item in documents if item[0] != h3_path),
        chain_bytes,
        activation_bytes,
    )
    assert incomplete.validation.status == "FAIL"
    assert incomplete.value is None
    assert "missing selected task bytes" in incomplete.validation.issues[0].detail
