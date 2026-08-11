"""Codecs and structural helpers for common harness wire records."""

from __future__ import annotations

from typing import Any, cast

from ..identity import ArtifactIdentity


class _WireValueDecoder:
    """Own structural conversion and validation of decoded JSON values."""

    __slots__ = ()

    def freeze(self, value: Any) -> Any:
        """Recursively convert decoded JSON arrays to immutable tuples."""
        if type(value) is list:
            return tuple(self.freeze(item) for item in value)
        return value

    def record_object(self, value: Any) -> dict[str, Any]:
        """Return a decoded JSON object suitable for record construction."""
        if type(value) is not dict or any(type(key) is not str for key in value):
            raise TypeError("nested wire record must be an object")
        return value

    def require_fields(
        self, obj: dict[str, object], expected: tuple[str, ...]
    ) -> None:
        """Require exactly the accepted fields for one wire record."""
        unknown = set(obj) - set(expected)
        missing = set(expected) - set(obj)
        if unknown:
            raise KeyError("unknown:" + sorted(unknown)[0])
        if missing:
            raise KeyError("missing:" + sorted(missing)[0])

    def array(self, value: Any, field: str) -> list[Any]:
        """Return a decoded JSON array or reject its structural type."""
        if type(value) is not list:
            raise TypeError(f"{field} must be a JSON array")
        return value


class _CommonWireRecordSerializer:
    """Own explicit common harness-record wire mappings."""

    __slots__ = ("_values",)

    def __init__(self) -> None:
        self._values = _WireValueDecoder()

    def encode(self, record: object) -> dict[str, object]:
        from ..checksums import ChecksumEntry, ChecksumManifest
        from ..evidence import IdentifierOccurrence
        from ..validation import ValidationIssue, ValidationResult

        if type(record) is ArtifactIdentity:
            return self._encode_artifact_identity(record)
        if type(record) is ChecksumEntry:
            return {
                "schema_version": record.schema_version,
                "path": record.path,
                "content_identity": self._encode_artifact_identity(
                    record.content_identity
                ),
            }
        if type(record) is ChecksumManifest:
            return {
                "schema_version": record.schema_version,
                "entries": [self.encode(value) for value in record.entries],
            }
        if type(record) is IdentifierOccurrence:
            return {
                "schema_version": record.schema_version,
                "evidence_id": record.evidence_id,
                "path": record.path,
                "line": record.line,
            }
        if type(record) is ValidationIssue:
            return self._encode_validation_issue(record)
        if type(record) is ValidationResult:
            return {
                "schema_version": record.schema_version,
                "status": record.status,
                "issues": [
                    self._encode_validation_issue(value) for value in record.issues
                ],
            }
        raise TypeError("record is outside common wire records")

    def _encode_artifact_identity(self, value: ArtifactIdentity) -> dict[str, object]:
        return {
            "schema_version": value.schema_version,
            "algorithm": value.algorithm,
            "digest": value.digest,
        }

    def _decode_artifact_identity(self, obj: dict[str, Any]) -> ArtifactIdentity:
        self._values.require_fields(obj, ("schema_version", "algorithm", "digest"))
        return ArtifactIdentity(obj["schema_version"], obj["algorithm"], obj["digest"])

    def _encode_validation_issue(self, value: object) -> dict[str, object]:
        from ..validation import ValidationIssue

        if type(value) is not ValidationIssue:
            raise TypeError("value must be ValidationIssue")
        return {
            "schema_version": value.schema_version,
            "code": value.code,
            "severity": value.severity,
            "subject_id": value.subject_id,
            "path": value.path,
            "related_ids": list(value.related_ids),
            "message": value.message,
        }

    def decode(self, kind_name: str, obj: dict[str, Any]) -> object:
        from ..checksums import ChecksumEntry, ChecksumManifest
        from ..evidence import IdentifierOccurrence
        from ..validation import ValidationIssue, ValidationResult

        if kind_name == "ArtifactIdentity":
            return self._decode_artifact_identity(obj)
        if kind_name == "ChecksumEntry":
            self._values.require_fields(
                obj, ("schema_version", "path", "content_identity")
            )
            identity = self._decode_artifact_identity(
                self._values.record_object(obj["content_identity"])
            )
            return ChecksumEntry(obj["schema_version"], obj["path"], identity)
        if kind_name == "ChecksumManifest":
            self._values.require_fields(obj, ("schema_version", "entries"))
            entries = cast(
                tuple[ChecksumEntry, ...],
                tuple(
                    self.decode("ChecksumEntry", self._values.record_object(value))
                    for value in self._values.array(obj["entries"], "entries")
                ),
            )
            return ChecksumManifest(obj["schema_version"], entries)
        if kind_name == "IdentifierOccurrence":
            self._values.require_fields(
                obj, ("schema_version", "evidence_id", "path", "line")
            )
            return IdentifierOccurrence(
                obj["schema_version"], obj["evidence_id"], obj["path"], obj["line"]
            )
        if kind_name == "ValidationIssue":
            expected = (
                "schema_version",
                "code",
                "severity",
                "subject_id",
                "path",
                "related_ids",
                "message",
            )
            self._values.require_fields(obj, expected)
            return ValidationIssue(
                obj["schema_version"],
                obj["code"],
                obj["severity"],
                obj["subject_id"],
                obj["path"],
                self._values.freeze(obj["related_ids"]),
                obj["message"],
            )
        if kind_name == "ValidationResult":
            self._values.require_fields(obj, ("schema_version", "status", "issues"))
            issues = cast(
                tuple[ValidationIssue, ...],
                tuple(
                    self.decode("ValidationIssue", self._values.record_object(value))
                    for value in self._values.array(obj["issues"], "issues")
                ),
            )
            return ValidationResult(obj["schema_version"], obj["status"], issues)
        raise AssertionError("common wire kind is not exhaustively handled")
