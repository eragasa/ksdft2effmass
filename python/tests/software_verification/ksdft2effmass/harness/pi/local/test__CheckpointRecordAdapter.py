r"""Software verification of ``CheckpointRecordAdapter``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module verifies adaptation of explicitly supplied checkpoint records.

Intrinsic and cross-object scope

``CheckpointRecordAdapter`` is the sole system under test.

VVUQ and scientific exclusions

Passing establishes software behavior only, not scientific validation or UQ.
"""

from typing import Any, cast

import pytest

from ksdft2effmass.harness.pi.local import CheckpointRecordAdapter

from .conftest import repository_root

pytestmark = pytest.mark.software_verification
SUT = CheckpointRecordAdapter


def test_method__execute__preserves_resolved_resumed_checkpoint_state() -> None:
    """Evidence ID: SV-HL-039

    Requirement: A selected resolved checkpoint retains its represented resumption
    state.

    Method: Adapt the exact accepted H2 final-acceptance checkpoint bytes.

    Oracle: The supplied checkpoint record declares resolved and resumed state.

    Acceptance: Adaptation passes and the sole result has ``resumption_status ==
    "resumed"``.

    Interpretation: Failure indicates checkpoint-adaptation or fixture drift.

    Limitations: The test does not resolve a checkpoint or establish scientific validity
    or UQ.
    """
    root = repository_root()
    path = ".pi/checkpoints/H2-HC02-final-acceptance.json"
    result = CheckpointRecordAdapter().execute(((path, (root / path).read_bytes()),))
    assert result.validation.status == "PASS"
    assert cast(Any, result.value)[0].resumption_status == "resumed"
