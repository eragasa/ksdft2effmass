r"""Software verification of ``HarnessTaskDeserializer``.

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


def test_method__execute__accepts_null_and_rejects_invalid_non_null_intake() -> None:
    """Evidence ID: ``SV-HT-038``.

    Requirement: Deserialization accepts null intake and applies the existing
    ResourcePath contract to every non-null intake value.

    Method: Deserialize canonical null intake, then replace only that member with a
    parent-traversal path.

    Oracle: The corrected version-2 contract distinguishes absent intake from an
    invalid represented path.

    Acceptance: Null returns ``None`` and the invalid non-null value raises
    ``ValueError``.

    Interpretation: Failure identifies deserializer or intrinsic path-validation
    drift.

    Limitations: Filesystem existence and Task authority are outside deserialization.
    """
    payload = HarnessTaskSerializer().execute(make_task(intake_path=None))
    assert SUT().execute(payload).intake_path is None
    invalid = payload.replace(b'"intake_path": null', b'"intake_path": "../bad"')
    with pytest.raises(ValueError, match="intake_path"):
        SUT().execute(invalid)
