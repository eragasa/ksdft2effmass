r"""Software verification of ``HarnessTaskSerializer``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

Software verification of one accepted project-local HarnessTask surface.

Intrinsic and cross-object scope

The sole primary SUT is ``HarnessTaskSerializer``.
Artifact-owned evidence covers detailed cross-object algorithms.

VVUQ and scientific exclusions

Passing establishes software-interface behavior only. It does not establish a
migration, activation, scientific validity, or human acceptance.
"""

import pytest

from ksdft2effmass.harness.pi.local import HarnessTaskSerializer

from .task_model_examples import make_task

pytestmark = pytest.mark.software_verification
SUT = HarnessTaskSerializer


def test_constructor__public_stereotype__has_exact_runtime_identity() -> None:
    """Evidence ID: ``SV-HT-002``.

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


def test_method__execute__rejects_non_task_input() -> None:
    """Evidence ID: ``SV-HT-034``.

    Requirement: Serialization accepts exactly HarnessTask.

    Method: Exercise independently invalid partitions against explicit synthetic input.

    Oracle: The accepted public constructor or ActionObject contract defines exact
    outcomes.

    Acceptance: Valid input remains exact and every specified invalid partition
    fails closed.

    Interpretation: Failure identifies intrinsic or cross-object contract drift.

    Limitations: Software verification does not authorize migration or human acceptance.
    """
    with pytest.raises(TypeError, match="HarnessTask"):
        SUT().execute(object())  # type: ignore[arg-type]


def test_method__execute__serializes_version_specific_fields_canonically() -> None:
    """Evidence ID: ``SV-HT-037``.

    Requirement: Version 3 serializes replacement IDs and null intake, while retained
    version 2 omits the version-3 field.

    Method: Serialize valid synthetic version-3 and version-2 Tasks.

    Oracle: The accepted versioned wire contracts define exact field presence.

    Acceptance: Version 3 contains the replacement array and null intake; version 2
    omits the replacement field; both end in one LF.

    Interpretation: Failure identifies serializer or corrected wire-contract drift.

    Limitations: This does not establish repository artifact existence or migration
    acceptance.
    """
    payload = SUT().execute(
        make_task(intake_path=None, superseded_by_task_ids=("replacement",))
    )
    assert b'  "superseded_by_task_ids": [\n    "replacement"\n  ],\n' in payload
    assert b'  "intake_path": null,\n' in payload
    assert payload.endswith(b"\n") and not payload.endswith(b"\n\n")
    retained = SUT().execute(make_task(schema_version=2))
    assert b'"superseded_by_task_ids"' not in retained
