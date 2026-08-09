r"""Software verification of ``HarnessTaskMigrationReviewPacket``.

Facet and represented meaning

Software verification of one accepted project-local HarnessTask surface.

Intrinsic and cross-object scope

The sole primary SUT is ``HarnessTaskMigrationReviewPacket``.
Artifact-owned evidence covers detailed cross-object algorithms.

VVUQ and scientific exclusions

Passing establishes software-interface behavior only. It does not establish a
migration, activation, scientific validity, or human acceptance.
"""

import pytest

from ksdft2effmass.harness.pi.local import (
    HarnessTaskMigrationReviewPacket,
    HarnessTaskMigrationReviewPacketPreparer,
)

from .task_model_examples import make_request

pytestmark = pytest.mark.software_verification
SUT = HarnessTaskMigrationReviewPacket


def test_constructor__public_stereotype__has_exact_runtime_identity() -> None:
    """Evidence ID: ``SV-HT-016``.

    Requirement: The public immutable object has its accepted runtime identity.

    Method: Construct or enumerate the public SUT using explicit synthetic support
    input.

    Oracle: The accepted 19-interface table supplies the expected name and stereotype.

    Acceptance: Runtime identity, fieldlessness, fields, or closed values match exactly.

    Interpretation: Failure identifies public API, stereotype, or value-semantics drift.

    Limitations: Detailed algorithms are asserted by focused artifact-owned evidence.
    """
    value = HarnessTaskMigrationReviewPacketPreparer().execute(make_request())
    assert type(value) is SUT
    assert value == value


def test_constructor__request_type__rejects_non_request_input() -> None:
    """Evidence ID: ``SV-HT-047``.

    Requirement: Migration review packet construction requires the exact request type.

    Method: Exercise independently invalid partitions against explicit synthetic input.

    Oracle: The accepted public constructor or ActionObject contract defines exact
    outcomes.

    Acceptance: Valid input remains exact and every specified invalid partition
    fails closed.

    Interpretation: Failure identifies intrinsic or cross-object contract drift.

    Limitations: Software verification does not authorize migration or human acceptance.
    """
    with pytest.raises(TypeError, match="Request"):
        SUT(object())  # type: ignore[arg-type]
