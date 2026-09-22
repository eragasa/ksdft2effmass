r"""Software verification of ``WorkflowEncodedRun``.

Bounded artifact scope: exact aggregate byte binding, not aggregate traversal.

Evidence profile: claim_bearing

Facet and represented meaning

Independent fixed genesis bytes and digest exercise the immutable envelope.

Intrinsic and cross-object scope

Only intrinsic byte/schema binding is claimed; no decoding or domain validation.

VVUQ and scientific exclusions

Software verification only; synthetic genesis is not a calculation or stored run.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.workflows import WorkflowEncodedRun, WorkflowRunSnapshot

pytestmark = pytest.mark.software_verification
SUT = WorkflowEncodedRun


class TestWorkflowEncodedRun:
    """Exact immutable representation boundary."""

    def test_constructor__content_binding__retains_fixed_complete_bytes(
        self,
        genesis_snapshot: WorkflowRunSnapshot,
    ) -> None:
        """Evidence ID: SV-WFR-ENCODED-RUN-001

        Requirement: Content identity binds exact schema and bytes.

        Method: Construct from a hand-authored complete genesis envelope.

        Oracle: Fixed independent SHA-256 literal and resource bytes.

        Acceptance: Schema, content identity and exact immutable bytes are retained.

        Interpretation: Digest binding is not successful aggregate decoding.

        Limitations: The fixture is synthetic record input, not serializer output.
        """
        revision = genesis_snapshot.revision
        value = WorkflowEncodedRun(
            schema_identity=revision.schema_id,
            content_identity=revision.content_id,
            payload=revision.payload,
        )
        assert value.schema_identity == "ksdft2effmass.workflow-run:1"
        assert value.content_identity == (
            "ksdft2effmass.workflow-run:1:sha256:"
            "760cd93744b80ecdefd7fccb0bf0b3145dcc7cd794113154411c626fcd77f456"
        )
        assert value.payload == revision.payload
        assert type(value.payload) is bytes

    @pytest.mark.parametrize(
        "field",
        [
            pytest.param("payload", id="changed_bytes"),
            pytest.param("schema", id="changed_schema"),
            pytest.param("content", id="changed_digest"),
            pytest.param("empty", id="empty_schema"),
        ],
    )
    def test_constructor__content_binding__rejects_detachment(
        self,
        genesis_snapshot: WorkflowRunSnapshot,
        field: str,
    ) -> None:
        """Evidence ID: SV-WFR-ENCODED-RUN-002

        Requirement: Schema and exact bytes cannot detach from content identity.

        Method: Change one envelope field independently of the fixed identity.

        Oracle: Exact schema-plus-SHA-256 content contract.

        Acceptance: Each detached or empty-schema envelope raises ValueError.

        Interpretation: Even a trailing newline changes content binding.

        Limitations: No wire schema parser is exercised.
        """
        revision = genesis_snapshot.revision
        with pytest.raises(ValueError):
            WorkflowEncodedRun(
                schema_identity=""
                if field == "empty"
                else "other:1"
                if field == "schema"
                else revision.schema_id,
                content_identity="wrong" if field == "content" else revision.content_id,
                payload=revision.payload + b"\n"
                if field == "payload"
                else revision.payload,
            )

    @pytest.mark.parametrize(
        "invalid",
        [
            pytest.param("bytes", id="text_payload"),
            pytest.param(bytearray(b"bytes"), id="mutable_byte_buffer"),
            pytest.param(True, id="boolean_payload"),
        ],
    )
    def test_constructor__payload__rejects_wrong_type(
        self,
        invalid: str | bytearray | bool,
    ) -> None:
        """Evidence ID: SV-WFR-ENCODED-RUN-003

        Requirement: The payload boundary accepts only exact immutable bytes.

        Method: Supply closed invalid semantic types at the constructor call.

        Oracle: Exact bytes contract, excluding coercion and mutable buffers.

        Acceptance: Every wrong payload type raises TypeError.

        Interpretation: Invalid inputs are not copied or stringified.

        Limitations: These partitions do not enumerate all Python objects.
        """
        with pytest.raises(TypeError):
            WorkflowEncodedRun(
                schema_identity="schema",
                content_identity="content",
                payload=invalid,  # type: ignore[arg-type]
            )

    def test_field__payload__is_immutable(self) -> None:
        """Evidence ID: SV-WFR-ENCODED-RUN-004

        Requirement: Bound bytes cannot be reassigned after construction.

        Method: Construct a bound empty-byte envelope and attempt assignment.

        Oracle: Standard empty SHA-256 digest and frozen dataclass semantics.

        Acceptance: Assignment raises FrozenInstanceError; bytes remain empty.

        Interpretation: Intrinsic binding does not assert that empty wire is valid.

        Limitations: Wire validation and schema support belong to the serializer.
        """
        value = WorkflowEncodedRun(
            schema_identity="future:9",
            content_identity="future:9:sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            payload=b"",
        )
        with pytest.raises(FrozenInstanceError):
            value.payload = b"changed"  # type: ignore[misc]
        assert value.payload == b""
