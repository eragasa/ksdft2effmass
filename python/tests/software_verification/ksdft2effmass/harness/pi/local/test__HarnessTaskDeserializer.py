r"""Software verification of ``HarnessTaskDeserializer``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

Software verification of one accepted project-local HarnessTask surface.

Intrinsic and cross-object scope

The sole primary SUT is ``HarnessTaskDeserializer``.
Artifact-owned evidence covers detailed cross-object algorithms.

VVUQ and scientific exclusions

Passing establishes software-interface behavior only. It does not establish a
migration, activation, scientific validity, or human acceptance.
"""

import pytest

from ksdft2effmass.harness import (
    HarnessTaskDeserializer,
    HarnessTaskSerializer,
)

from .task_model_examples import make_task

pytestmark = pytest.mark.software_verification
SUT = HarnessTaskDeserializer


def test_constructor__public_stereotype__has_exact_runtime_identity() -> None:
    """Evidence ID: ``SV-HT-003``.

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


def test_method__strict_wire__rejects_bom_utf8_and_key_closure() -> None:
    """Evidence ID: ``SV-HT-035``.

    Requirement: Strict decoding rejects BOM, invalid UTF-8, unknown keys, and
    missing keys.

    Method: Exercise independently invalid partitions against explicit synthetic input.

    Oracle: The accepted public constructor or ActionObject contract defines exact
    outcomes.

    Acceptance: Valid input remains exact and every specified invalid partition
    fails closed.

    Interpretation: Failure identifies intrinsic or cross-object contract drift.

    Limitations: Software verification does not authorize migration or human acceptance.
    """
    payload = HarnessTaskSerializer().execute(make_task())
    with pytest.raises(ValueError, match="BOM"):
        SUT().execute(b"\xef\xbb\xbf" + payload)
    with pytest.raises(ValueError, match="UTF-8"):
        SUT().execute(b"\xff")
    with pytest.raises(ValueError, match="unknown field"):
        SUT().execute(payload.replace(b"{", b'{"unknown": 1,', 1))
    with pytest.raises(ValueError, match="missing field"):
        SUT().execute(payload.replace(b'  "title": "Example Task",\n', b"", 1))


def test_method__execute__applies_version_three_fields_and_intake_validation() -> None:
    """Evidence ID: ``SV-HT-038``.

    Requirement: Deserialization requires version-3 replacement IDs, rejects
    unsupported versions, and validates every non-null intake path.

    Method: Deserialize a canonical value, remove the required field, replace the
    schema version with 2, and inject an invalid intake path.

    Oracle: The accepted version-3 contract defines field closure and path validity.

    Acceptance: Replacement IDs are preserved, omission and version 2 fail, and an
    invalid intake raises ``ValueError``.

    Interpretation: Failure identifies deserializer or intrinsic path-validation
    drift.

    Limitations: Filesystem existence and Task authority are outside deserialization.
    """
    payload = HarnessTaskSerializer().execute(
        make_task(intake_path=None, superseded_by_task_ids=("replacement",))
    )
    decoded = SUT().execute(payload)
    assert decoded.intake_path is None
    assert decoded.superseded_by_task_ids == ("replacement",)
    missing = payload.replace(
        b'  "superseded_by_task_ids": [\n    "replacement"\n  ],\n', b""
    )
    with pytest.raises(ValueError, match="missing field superseded_by_task_ids"):
        SUT().execute(missing)
    unsupported = payload.replace(b'"schema_version": 3', b'"schema_version": 2')
    with pytest.raises(ValueError, match="schema_version must equal integer 3"):
        SUT().execute(unsupported)
    invalid = payload.replace(b'"intake_path": null', b'"intake_path": "../bad"')
    with pytest.raises(ValueError, match="intake_path"):
        SUT().execute(invalid)
