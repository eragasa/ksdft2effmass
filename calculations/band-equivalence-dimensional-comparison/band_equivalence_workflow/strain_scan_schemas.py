"""Packaged strict schemas for finite synthetic-strain scan artifacts."""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import StrEnum
from importlib.resources import files
from pathlib import Path

from jsonschema import Draft202012Validator  # type: ignore[import-untyped]

from .strain_scan_serialization import (
    SCAN_REQUEST_SCHEMA_ID,
    SCAN_RESULT_SCHEMA_ID,
    SCAN_VERIFICATION_SCHEMA_ID,
)


class SyntheticStrainScanSchemaKind(StrEnum):
    """Identify one finite strain-scan artifact contract."""

    REQUEST = "request"
    RESULT = "result"
    VERIFICATION = "verification"


@dataclass(frozen=True, slots=True)
class SyntheticStrainScanSchema:
    """One immutable packaged JSON Schema for a finite strain scan."""

    kind: SyntheticStrainScanSchemaKind

    def __post_init__(self) -> None:
        if type(self.kind) is not SyntheticStrainScanSchemaKind:
            raise TypeError("kind must be SyntheticStrainScanSchemaKind")

    @property
    def identity(self) -> str:
        """Return the exact schema identity required by its artifact."""
        match self.kind:
            case SyntheticStrainScanSchemaKind.REQUEST:
                return SCAN_REQUEST_SCHEMA_ID
            case SyntheticStrainScanSchemaKind.RESULT:
                return SCAN_RESULT_SCHEMA_ID
            case SyntheticStrainScanSchemaKind.VERIFICATION:
                return SCAN_VERIFICATION_SCHEMA_ID

    @property
    def artifact_filename(self) -> str:
        """Return the maintained schema filename."""
        return f"synthetic-strain-scan-{self.kind.value}.v1.schema.json"

    def canonical_bytes(self) -> bytes:
        """Return the packaged canonical schema document."""
        resource = files(__package__).joinpath(
            "schema_documents",
            f"synthetic-strain-scan.{self.kind.value}.schema.json",
        )
        document = json.loads(resource.read_bytes())
        return (
            json.dumps(document, allow_nan=False, separators=(",", ":"), sort_keys=True)
            + "\n"
        ).encode("utf-8")

    def validate(self, document: bytes) -> None:
        """Validate serialized canonical JSON against this strict schema."""
        if type(document) is not bytes:
            raise TypeError("document must be built-in bytes")
        Draft202012Validator(json.loads(self.canonical_bytes())).validate(
            json.loads(document)
        )

    def write_to(self, directory: Path) -> Path:
        """Write the packaged schema without exposing a mutable mapping."""
        if not isinstance(directory, Path):
            raise TypeError("directory must be pathlib.Path")
        directory.mkdir(parents=True, exist_ok=True)
        output = directory / self.artifact_filename
        output.write_bytes(self.canonical_bytes())
        return output


__all__ = ["SyntheticStrainScanSchema", "SyntheticStrainScanSchemaKind"]
