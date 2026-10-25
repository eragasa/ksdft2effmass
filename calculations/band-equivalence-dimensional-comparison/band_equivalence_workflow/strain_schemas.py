"""Packaged strict schemas for bounded synthetic-strain result artifacts."""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import StrEnum
from importlib.resources import files
from pathlib import Path

from jsonschema import Draft202012Validator  # type: ignore[import-untyped]

from .strain_serialization import (
    M0_RESULT_SCHEMA_ID,
    M1_RESULT_SCHEMA_ID,
    M2_RESULT_SCHEMA_ID,
    WITNESS_RESULT_SCHEMA_ID,
)


class SyntheticStrainSchemaKind(StrEnum):
    """Identify one bounded synthetic-strain result contract."""

    M0_RESULT = "m0-result"
    M1_RESULT = "m1-result"
    M2_RESULT = "m2-result"
    WITNESS_RESULT = "witness-result"


@dataclass(frozen=True, slots=True)
class SyntheticStrainSchema:
    """One immutable packaged JSON Schema for a synthetic-strain result."""

    kind: SyntheticStrainSchemaKind

    def __post_init__(self) -> None:
        if type(self.kind) is not SyntheticStrainSchemaKind:
            raise TypeError("kind must be SyntheticStrainSchemaKind")

    @property
    def identity(self) -> str:
        """Return the exact schema identity required by its artifact."""

        match self.kind:
            case SyntheticStrainSchemaKind.M0_RESULT:
                return M0_RESULT_SCHEMA_ID
            case SyntheticStrainSchemaKind.M1_RESULT:
                return M1_RESULT_SCHEMA_ID
            case SyntheticStrainSchemaKind.M2_RESULT:
                return M2_RESULT_SCHEMA_ID
            case SyntheticStrainSchemaKind.WITNESS_RESULT:
                return WITNESS_RESULT_SCHEMA_ID

    @property
    def artifact_filename(self) -> str:
        """Return the maintained schema filename."""

        return f"synthetic-strain-{self.kind.value}.v1.schema.json"

    def canonical_bytes(self) -> bytes:
        """Return the packaged canonical schema document."""

        resource = files(__package__).joinpath(
            "schema_documents", f"synthetic-strain.{self.kind.value}.schema.json"
        )
        return resource.read_bytes()

    def validate(self, document: bytes) -> None:
        """Validate serialized canonical JSON against this strict schema."""

        if type(document) is not bytes:
            raise TypeError("document must be built-in bytes")
        validator = Draft202012Validator(json.loads(self.canonical_bytes()))
        validator.validate(json.loads(document))

    def write_to(self, directory: Path) -> Path:
        """Write the packaged schema without exposing a mutable schema mapping."""

        if not isinstance(directory, Path):
            raise TypeError("directory must be pathlib.Path")
        directory.mkdir(parents=True, exist_ok=True)
        output = directory / self.artifact_filename
        output.write_bytes(self.canonical_bytes())
        return output


__all__ = ["SyntheticStrainSchema", "SyntheticStrainSchemaKind"]
