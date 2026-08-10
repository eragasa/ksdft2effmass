r"""Software verification of ``ChainRecordAdapter``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module verifies adaptation of one selected project chain into generic state.

Intrinsic and cross-object scope

``ChainRecordAdapter`` owns the chain result; ``TaskRecordAdapter`` supplies explicit
collaborating Task records.

VVUQ and scientific exclusions

Passing establishes software behavior only, not scientific validation or UQ.
"""

import json
from typing import Any, cast

import pytest

from ksdft2effmass.harness.pi.local import ChainRecordAdapter, TaskRecordAdapter

from .conftest import repository_root

pytestmark = pytest.mark.software_verification
SUT = ChainRecordAdapter


def test_method__execute__preserves_explicit_activation_without_active_task() -> None:
    """Evidence ID: SV-HL-003

    Requirement: The selected H4 chain preserves its explicit activation and inactive
    runtime state.

    Method: Adapt caller-supplied Task bytes and then the chain and activation bytes.

    Oracle: The accepted H4 records declare H4 explicitly activated and no active Task.

    Acceptance: Adaptation passes, ``active_task_id`` is absent, and the explicit
    activation tuple
    is exactly ``("H4",)``.

    Interpretation: Failure indicates chain-adaptation or selected-input drift.

    Limitations: The test does not authorize execution or establish scientific validity
    or UQ.
    """
    root = repository_root()
    chain_bytes = (root / ".pi/chains/pi-harness-incubation.chain.json").read_bytes()
    activation_bytes = (
        root / ".pi/evidence/pi-harness-incubation/H4/activation.json"
    ).read_bytes()
    chain = json.loads(chain_bytes)
    documents = tuple(
        (item["record"], (root / item["record"]).read_bytes())
        for item in chain["task_sequence"]
    )
    tasks = TaskRecordAdapter().execute(documents, chain_bytes, activation_bytes)
    assert tasks.validation.status == "PASS"
    result = ChainRecordAdapter().execute(
        chain_bytes, cast(Any, tasks.value), activation_bytes
    )
    assert result.validation.status == "PASS"
    value = cast(Any, result.value)
    assert value.active_task_id is None
    assert value.explicitly_activated_task_ids == ("H4",)
