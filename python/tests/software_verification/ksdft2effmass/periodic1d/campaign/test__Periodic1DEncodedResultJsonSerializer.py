r"""Class-owned verification of periodic-1D encoded result documents.

Evidence profile: routine

Bounded scope
-------------
Synthetic intrinsic tests cover the explicit wire-kind enumeration, complete immutable
JSON adaptation, exact source-byte retention, digest correlation, canonical encoding,
and serializer-kind boundary.

Scientific exclusions
---------------------
The SUT owns supporting encoded-document structure. It does not authenticate execution
provenance, construct a represented operator, establish convergence, validate a
scientific model, quantify uncertainty, or record acceptance. Retained-file evidence is
owned by a separate integration module.
"""

import hashlib
from dataclasses import FrozenInstanceError, fields, replace
from typing import get_type_hints

import pytest

from ksdft2effmass.periodic1d.campaign import (
    Periodic1DEncodedResultDocument,
    Periodic1DEncodedResultJsonSerializer,
    Periodic1DEncodedResultKind,
)
from ksdft2effmass.serialization.json import ImmutableJsonObject

pytestmark = pytest.mark.software_verification
SUT = Periodic1DEncodedResultJsonSerializer


def synthetic_payload() -> bytes:
    """Return a noncanonical but valid synthetic isolated-result wire."""
    return (
        b'{\n  "schema_version": 1,\n'
        b'  "experiment_id": "synthetic.encoded-result.v1",\n'
        b'  "evidence_status": "synthetic test data",\n'
        b'  "calculation_status": null,\n'
        b'  "nested": {"value": 3}\n}\n'
    )


class TestPeriodic1DEncodedResultJsonSerializer:
    """Own routine intrinsic row-045 evidence."""

    def test_contract__defines_explicit_wire_kinds_and_document_fields(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-045-001.

        Requirement: Wire kinds and encoded-document fields remain explicit and ordered.

        Acceptance: Historical enum values are unchanged; the document owns the full
        decoded tree, exact source bytes, and correlated source digest; retired names
        and compatibility serializer aliases are absent.
        """
        kind_values = tuple(
            (kind.name, kind.value) for kind in Periodic1DEncodedResultKind
        )
        assert kind_values == (
            ("ISOLATED_BAND", "isolated_band"),
            ("STRESS", "stress"),
            ("COMPOSITE", "composite"),
            ("WANNIER90", "wannier90"),
            ("WANNIER90_PRECONDITIONED", "wannier90_preconditioned"),
            ("WANNIER90_CONVERGENCE_ATTEMPT", "wannier90_convergence_attempt"),
        )
        assert [field.name for field in fields(Periodic1DEncodedResultDocument)] == [
            "kind",
            "schema_version",
            "record_id",
            "evidence_status",
            "calculation_status",
            "root",
            "source_document",
            "source_sha256",
        ]
        type_hints = get_type_hints(Periodic1DEncodedResultDocument)
        assert type_hints["source_document"] is bytes
        assert Periodic1DEncodedResultDocument.__module__ == (
            "ksdft2effmass.periodic1d.campaign.result_documents"
        )
        assert Periodic1DEncodedResultJsonSerializer.__module__ == (
            "ksdft2effmass.periodic1d.campaign.result_documents"
        )
        assert not hasattr(SUT, "decode")
        assert not hasattr(SUT, "encode")

    def test_methods__preserve_source_bytes_and_emit_canonical_json(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-045-002.

        Requirement: Deserialization preserves exact source bytes and complete immutable
        JSON meaning, while serialization explicitly emits a separate canonical wire.

        Acceptance: Source object identity and digest agree; canonical bytes differ from
        the noncanonical source but deserialize to the same immutable root and identity.
        """
        payload = synthetic_payload()
        serializer = SUT(Periodic1DEncodedResultKind.ISOLATED_BAND)

        document = serializer.deserialize(payload)
        canonical = serializer.serialize(document)
        reconstructed = serializer.deserialize(canonical)

        assert document.source_document is payload
        assert document.source_sha256 == hashlib.sha256(payload).hexdigest()
        assert type(document.root) is ImmutableJsonObject
        assert document.root.field("nested") == ImmutableJsonObject((("value", 3),))
        assert canonical != payload
        assert reconstructed.root == document.root
        assert reconstructed.record_id == document.record_id
        assert reconstructed.source_document is canonical
        assert reconstructed.source_sha256 == hashlib.sha256(canonical).hexdigest()

    def test_construction__rejects_unbound_or_mutable_source_identity(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-045-003.

        Requirement: Public document construction must fail closed when exact source
        bytes and their declared identity disagree.

        Acceptance: Empty, nonexact, changed, or forged source identities are rejected;
        the valid document is frozen and slotted.
        """
        document = SUT(Periodic1DEncodedResultKind.ISOLATED_BAND).deserialize(
            synthetic_payload()
        )

        class BytesSubclass(bytes):
            """Provide a bytes subtype outside the exact wire contract."""

        with pytest.raises(TypeError, match="schema_version must be a built-in int"):
            replace(document, schema_version=True)
        with pytest.raises(TypeError, match="source_document must be exact bytes"):
            replace(document, source_document=BytesSubclass(b"{}"))
        with pytest.raises(ValueError, match="source_document must be nonempty"):
            replace(document, source_document=b"")
        with pytest.raises(ValueError, match="must identify source_document"):
            replace(document, source_document=b"changed")
        with pytest.raises(TypeError, match="source_sha256 must be a built-in str"):
            replace(document, source_sha256=b"not-a-string")  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="must identify source_document"):
            replace(document, source_sha256="0" * 64)
        changed_source = synthetic_payload().replace(b'"value": 3', b'"value": 4')
        with pytest.raises(ValueError, match="complete decoding of source_document"):
            replace(
                document,
                source_document=changed_source,
                source_sha256=hashlib.sha256(changed_source).hexdigest(),
            )
        with pytest.raises(FrozenInstanceError):
            document.record_id = "changed"  # type: ignore[misc]
        with pytest.raises((AttributeError, TypeError)):
            document.repository_root = "/tmp"  # type: ignore[attr-defined]

    def test_methods__reject_wrong_or_mismatched_wire_kinds(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-045-004.

        Requirement: The caller must supply an exact explicit wire kind, and serializers
        must not silently reinterpret documents of another kind.

        Acceptance: Wrong constructor types and cross-kind serialization fail closed.
        """
        with pytest.raises(TypeError, match="kind must be Periodic1DEncodedResultKind"):
            SUT("isolated_band")  # type: ignore[arg-type]
        serializer = SUT(Periodic1DEncodedResultKind.ISOLATED_BAND)
        assert serializer.kind is Periodic1DEncodedResultKind.ISOLATED_BAND
        assert not hasattr(serializer, "immutable_codec")
        with pytest.raises(AttributeError):
            serializer.kind = Periodic1DEncodedResultKind.COMPOSITE  # type: ignore[misc]
        isolated = serializer.deserialize(synthetic_payload())
        with pytest.raises(ValueError, match="value kind must match"):
            SUT(Periodic1DEncodedResultKind.COMPOSITE).serialize(isolated)
