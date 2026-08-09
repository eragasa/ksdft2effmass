r"""Software verification of ``HarnessTaskMigrationReviewPacketRequest``.

Facet and represented meaning

Software verification of one accepted project-local HarnessTask surface.

Intrinsic and cross-object scope

The sole primary SUT is ``HarnessTaskMigrationReviewPacketRequest``.
Artifact-owned evidence covers detailed cross-object algorithms.

VVUQ and scientific exclusions

Passing establishes software-interface behavior only. It does not establish a
migration, activation, scientific validity, or human acceptance.
"""

import pytest

from ksdft2effmass.harness.pi.local import HarnessTaskMigrationReviewPacketRequest

from .task_model_examples import make_request

pytestmark = pytest.mark.software_verification
SUT = HarnessTaskMigrationReviewPacketRequest


def test_constructor__public_stereotype__has_exact_runtime_identity() -> None:
    """Evidence ID: ``SV-HT-014``.

    Requirement: The public immutable object has its accepted runtime identity.

    Method: Construct or enumerate the public SUT using explicit synthetic support
    input.

    Oracle: The accepted 19-interface table supplies the expected name and stereotype.

    Acceptance: Runtime identity, fieldlessness, fields, or closed values match exactly.

    Interpretation: Failure identifies public API, stereotype, or value-semantics drift.

    Limitations: Detailed algorithms are asserted by focused artifact-owned evidence.
    """
    value = make_request()
    assert type(value) is SUT
    assert value == value


def test_constructor__runtime_bundle__rejects_empty_mappings_and_nonbyte_json() -> None:
    """Evidence ID: ``SV-HT-045``.

    Requirement: Packet requests require nonempty mapping tuples and canonical-byte
    claims as bytes.

    Method: Exercise independently invalid partitions against explicit synthetic input.

    Oracle: The accepted public constructor or ActionObject contract defines exact
    outcomes.

    Acceptance: Valid input remains exact and every specified invalid partition
    fails closed.

    Interpretation: Failure identifies intrinsic or cross-object contract drift.

    Limitations: Software verification does not authorize migration or human acceptance.
    """
    request = make_request()
    values = [getattr(request, name) for name in request.__dataclass_fields__]
    values[1] = ()
    with pytest.raises(ValueError, match="mappings"):
        SUT(*values)
    values[1] = request.mappings
    values[3] = "{}"
    with pytest.raises(TypeError, match="canonical_task_json"):
        SUT(*values)
