r"""Software verification of ``ResearchMonographCitationSnapshotResultJsonCodec``.

Evidence profile: routine

Bounded artifact scope: the complete unversioned citation Result JSON wire, exact
stored field families, deterministic bytes, bounded decoding, and integrity replay.

Facet and represented meaning

The codec represents one complete owner Result as canonical newline-terminated UTF-8
JSON without file I/O, source rescanning, or downstream state.

Intrinsic and cross-object scope

Evidence covers the public codec route, complete repository roundtrip, canonical byte
identity, exact JSON structure, fail-closed decoding, and request/snapshot/result
identity replay.

VVUQ and scientific exclusions

This is structural software verification. It establishes no bibliography metadata
truth, source support for claims, rights or use admission, scientific validation, UQ,
or human acceptance.
"""

from hashlib import sha256
from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph import (
    ResearchMonographCitationSnapshotCompiler,
    ResearchMonographCitationSnapshotRequest,
    ResearchMonographCitationSnapshotResult,
    ResearchMonographCitationSnapshotResultJsonCodec,
)

pytestmark = pytest.mark.software_verification
SUT = ResearchMonographCitationSnapshotResultJsonCodec


class TestResearchMonographCitationSnapshotResultJsonCodec:
    """Own software evidence for the complete canonical citation Result wire."""

    def test_method__roundtrip__preserves_complete_real_snapshot(self) -> None:
        """Evidence ID: SV-CITATION-RESULT-CODEC-001

        Requirement: The wire must preserve every stored owner family and identity in
        owner order for the complete repository snapshot.

        Acceptance: Decode equals the input Result with exact 34/122/221/277/45/2
        family counts, empty closure failures, and unchanged request, snapshot, and
        Result identities.
        """
        result = self.compile_repository()
        payload = SUT().serialize(result)

        decoded = SUT().deserialize(payload)
        replayed_payload = SUT().serialize(decoded)
        same_wire_digest = sha256(replayed_payload).digest() == sha256(payload).digest()

        assert same_wire_digest
        assert decoded.request_id == result.request_id
        assert decoded.result_id == result.result_id
        assert decoded.snapshot.snapshot_id == result.snapshot.snapshot_id
        assert len(decoded.snapshot.source_files) == 34
        assert len(decoded.snapshot.include_instances) == 34
        assert len(decoded.snapshot.groups) == 122
        assert len(decoded.snapshot.bibliography_entries) == 122
        assert len(decoded.snapshot.calls) == 221
        assert len(decoded.snapshot.occurrences) == 277
        assert len(decoded.snapshot.todos) == 45
        assert len(decoded.snapshot.source_gaps) == 2
        assert len(decoded.snapshot.missing_keys) == 0
        assert len(decoded.snapshot.duplicate_keys) == 0
        assert len(decoded.snapshot.uncited_keys) == 0

    def test_method__serialize__is_deterministic_canonical_utf8(self) -> None:
        """Evidence ID: SV-CITATION-RESULT-CODEC-002

        Requirement: Equal complete Results must produce one deterministic bounded
        newline-terminated UTF-8 representation.

        Acceptance: Independent serialization is byte-identical, has exactly one
        terminal newline, decodes as UTF-8, and matches the reviewed real-snapshot
        byte count and SHA-256 digest.
        """
        result = self.compile_repository()

        first = SUT().serialize(result)
        second = SUT().serialize(result)

        same_wire_digest = sha256(first).digest() == sha256(second).digest()

        assert same_wire_digest
        assert len(first) == len(second)
        assert first.endswith(b"\n")
        assert not first.endswith(b"\n\n")
        assert first.decode("utf-8").endswith("\n")
        assert len(first) == 724_108
        assert len(sha256(first).digest()) == 32

    def test_method__serialize__excludes_non_owner_runtime_fields(self) -> None:
        """Evidence ID: SV-CITATION-RESULT-CODEC-003

        Requirement: The wire must contain only the complete owner Result and must not
        add schema, version, time, root, excerpt, intake, or downstream-status fields.

        Acceptance: Canonical bytes begin with the three exact root members, contain
        no absolute repository root, and contain none of the prohibited member names.
        """
        repository_root = Path(__file__).resolve().parents[7]
        payload = SUT().serialize(self.compile_repository())
        prohibited = (
            "schema",
            "schema_version",
            "version",
            "timestamp",
            "repository_root",
            "excerpt",
            "raw_bibtex",
            "runtime_state",
            "availability",
            "rights",
            "processing_status",
            "projection_status",
        )

        has_exact_root_members = (
            payload.startswith(b'{\n  "request_id":')
            and b'\n  "result_id":' in payload
            and b'\n  "snapshot": {' in payload
        )
        contains_absolute_root = repository_root.as_posix().encode() in payload
        contains_prohibited_name = any(
            f'"{name}":'.encode() in payload for name in prohibited
        )

        assert has_exact_root_members
        assert not contains_absolute_root
        assert not contains_prohibited_name

    def test_method__deserialize__rejects_unknown_and_missing_fields(self) -> None:
        """Evidence ID: SV-CITATION-RESULT-CODEC-004

        Requirement: Exact wire objects must reject both unknown and missing fields.

        Acceptance: Adding an unknown root field or removing ``request_id`` raises
        ``ValueError`` without returning a partial Result.
        """
        payload = SUT().serialize(self.compile_repository())
        unknown = payload.replace(
            b'{\n  "request_id":', b'{\n  "extra": null,\n  "request_id":', 1
        )
        lines = payload.splitlines(keepends=True)
        missing = b"".join(line for line in lines if b'"request_id"' not in line)

        with pytest.raises(ValueError, match="fields differ"):
            SUT().deserialize(unknown)
        with pytest.raises(ValueError, match="fields differ"):
            SUT().deserialize(missing)

    def test_method__deserialize__rejects_duplicate_fields(self) -> None:
        """Evidence ID: SV-CITATION-RESULT-CODEC-005

        Requirement: Duplicate JSON object member names must never be collapsed.

        Acceptance: A duplicated root ``request_id`` raises ``ValueError`` before
        Result construction.
        """
        payload = SUT().serialize(self.compile_repository())
        duplicate = payload.replace(
            b'{\n  "request_id":',
            b'{\n  "request_id": "duplicate",\n  "request_id":',
            1,
        )

        with pytest.raises(ValueError, match="duplicate member 'request_id'"):
            SUT().deserialize(duplicate)

    def test_method__deserialize__rejects_malformed_non_utf8_and_trailing_input(
        self,
    ) -> None:
        """Evidence ID: SV-CITATION-RESULT-CODEC-006

        Requirement: Input must be one complete UTF-8 JSON value followed by exactly
        the canonical newline.

        Acceptance: Incomplete JSON, non-UTF-8 bytes, missing newline, and bytes after
        a complete value each raise ``ValueError``.
        """
        payload = SUT().serialize(self.compile_repository())

        with pytest.raises(ValueError):
            SUT().deserialize(b"{\n")
        with pytest.raises(ValueError, match="UTF-8"):
            SUT().deserialize(b'"\xff"\n')
        with pytest.raises(ValueError, match="canonical newline"):
            SUT().deserialize(payload[:-1])
        with pytest.raises(ValueError, match="trailing"):
            SUT().deserialize(payload + b" \n")

    def test_method__deserialize__rejects_overbound_input(self) -> None:
        """Evidence ID: SV-CITATION-RESULT-CODEC-007

        Requirement: Decoder work must be bounded before UTF-8 or JSON parsing and
        during recursive structure and integer parsing.

        Acceptance: A 20,000,001-byte payload, more than 64 nesting levels, and an
        integer token longer than 20 digits each raise ``ValueError``.
        """
        payload = b" " * 20_000_000 + b"\n"
        nested = b"[" * 66 + b"null" + b"]" * 66 + b"\n"

        with pytest.raises(ValueError, match="20,000,000"):
            SUT().deserialize(payload)
        with pytest.raises(ValueError, match="nesting"):
            SUT().deserialize(nested)
        with pytest.raises(ValueError, match="20 decimal digits"):
            SUT().deserialize(b"123456789012345678901\n")

    def test_method__deserialize__rejects_malformed_field_types(self) -> None:
        """Evidence ID: SV-CITATION-RESULT-CODEC-008

        Requirement: Stored fields must retain their exact semantic JSON types.

        Acceptance: Replacing the string ``request_id`` with null raises
        ``TypeError`` without coercion.
        """
        result = self.compile_repository()
        payload = SUT().serialize(result)
        malformed = payload.replace(
            f'"request_id": "{result.request_id}"'.encode(),
            b'"request_id": null',
            1,
        )

        with pytest.raises(TypeError, match="request_id"):
            SUT().deserialize(malformed)

    def test_method__deserialize__rejects_noncanonical_json_spelling(self) -> None:
        """Evidence ID: SV-CITATION-RESULT-CODEC-009

        Requirement: The unversioned wire has exactly one canonical JSON spelling.

        Acceptance: Semantically equivalent JSON with altered insignificant spacing
        raises ``ValueError``.
        """
        payload = SUT().serialize(self.compile_repository())
        noncanonical = payload.replace(b'"request_id": ', b'"request_id":', 1)

        with pytest.raises(ValueError, match="not the canonical"):
            SUT().deserialize(noncanonical)

    @pytest.mark.parametrize(
        "identity_name",
        ["request_id", "result_id", "snapshot_id"],
        ids=["request", "result", "snapshot"],
    )
    def test_method__deserialize__replays_every_result_identity(
        self, identity_name: str
    ) -> None:
        """Evidence ID: SV-CITATION-RESULT-CODEC-010

        Requirement: Decode must publicly replay request, Result, and snapshot
        identities rather than trusting stored identity strings.

        Acceptance: A one-character substitution in each identity family raises
        ``ValueError``.
        """
        result = self.compile_repository()
        payload = SUT().serialize(result)
        identities = {
            "request_id": result.request_id,
            "result_id": result.result_id,
            "snapshot_id": result.snapshot.snapshot_id,
        }
        identity = identities[identity_name]
        replacement = f"{identity[:-1]}{'0' if identity[-1] != '0' else '1'}"
        forged = payload.replace(identity.encode(), replacement.encode(), 1)

        with pytest.raises(ValueError):
            SUT().deserialize(forged)

    def test_method__serialize__rejects_non_result_input(self) -> None:
        """Evidence ID: SV-CITATION-RESULT-CODEC-011

        Requirement: Serialization accepts only the exact owner Result type.

        Acceptance: A bytes value is rejected without coercion.
        """
        invalid: bytes | ResearchMonographCitationSnapshotResult = b"not a result"

        with pytest.raises(TypeError, match="must be"):
            SUT().serialize(invalid)  # type: ignore[arg-type]

    @staticmethod
    def compile_repository() -> ResearchMonographCitationSnapshotResult:
        """Compile the current isolated worktree through the supported API."""
        repository_root = Path(__file__).resolve().parents[7]
        return ResearchMonographCitationSnapshotCompiler().execute(
            ResearchMonographCitationSnapshotRequest(repository_root.as_posix())
        )
