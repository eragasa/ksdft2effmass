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

from ksdft2effmass.harness.pi.local import (
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


def test_method__execute__applies_versioned_fields_and_intake_validation() -> None:
    """Evidence ID: ``SV-HT-038``.

    Requirement: Deserialization requires replacement IDs in version 3, supplies an
    empty tuple for retained version 2, and validates every non-null intake path.

    Method: Deserialize canonical values, remove the version-3 field, deserialize a
    retained version-2 value, and inject an invalid intake path.

    Oracle: The accepted versioned contracts define field closure and path validity.

    Acceptance: Version 3 preserves replacement IDs, omission fails, version 2 returns
    an empty replacement tuple, and invalid intake raises ``ValueError``.

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
    retained = SUT().execute(
        HarnessTaskSerializer().execute(make_task(schema_version=2))
    )
    assert retained.superseded_by_task_ids == ()
    invalid = payload.replace(b'"intake_path": null', b'"intake_path": "../bad"')
    with pytest.raises(ValueError, match="intake_path"):
        SUT().execute(invalid)
