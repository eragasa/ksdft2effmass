r"""Software verification of ``HarnessTaskMigrationReviewPacketPreparer``.

Facet and represented meaning

Software verification of one accepted project-local HarnessTask surface.

Intrinsic and cross-object scope

The sole primary SUT is ``HarnessTaskMigrationReviewPacketPreparer``.
Artifact-owned evidence covers detailed cross-object algorithms.

VVUQ and scientific exclusions

Passing establishes software-interface behavior only. It does not establish a
migration, activation, scientific validity, or human acceptance.
"""

import pytest

from ksdft2effmass.harness.pi.local import HarnessTaskMigrationReviewPacketPreparer

from .task_model_examples import identity, make_request

pytestmark = pytest.mark.software_verification
SUT = HarnessTaskMigrationReviewPacketPreparer


def test_constructor__public_stereotype__has_exact_runtime_identity() -> None:
    """Evidence ID: ``SV-HT-015``.

    Requirement: The public ActionObject is fieldless, stateless, and can be
    constructed directly.

    Method: Construct or enumerate the public SUT using explicit synthetic support
    input.

    Oracle: The accepted 19-interface table supplies the expected name and stereotype.

    Acceptance: Runtime identity, fieldlessness, fields, or closed values match exactly.

    Interpretation: Failure identifies public API, stereotype, or value-semantics drift.

    Limitations: Detailed algorithms are asserted by focused artifact-owned evidence.
    """
    assert SUT.__slots__ == ()
    assert type(SUT()) is SUT


def test_method__agreement__rejects_identity_and_json_drift() -> None:
    """Evidence ID: ``SV-HT-046``.

    Requirement: Packet preparation recomputes span identities and canonical Task JSON.

    Method: Exercise independently invalid partitions against explicit synthetic input.

    Oracle: The accepted public constructor or ActionObject contract defines exact
    outcomes.

    Acceptance: Valid input remains exact and every specified invalid partition
    fails closed.

    Interpretation: Failure identifies intrinsic or cross-object contract drift.

    Limitations: Software verification does not authorize migration or human acceptance.
    """
    request = make_request()
    mapping = request.mappings[0]
    bad = type(mapping)(
        mapping.mapping_id,
        mapping.source_identity,
        mapping.start_byte,
        mapping.end_byte,
        identity(b"other"),
        mapping.disposition,
        mapping.target_references,
        mapping.transformation,
        mapping.rationale,
    )
    values = [getattr(request, name) for name in request.__dataclass_fields__]
    values[1] = (bad,)
    with pytest.raises(ValueError, match="span identity"):
        SUT().execute(type(request)(*values))
    values[1] = request.mappings
    values[3] = b"{}\n"
    with pytest.raises(ValueError, match="canonical_task_json"):
        SUT().execute(type(request)(*values))
