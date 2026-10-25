"""Packaged strict schemas for sampled shell--scale decision artifacts."""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import StrEnum
from importlib.resources import files
from pathlib import Path

from jsonschema import Draft202012Validator  # type: ignore[import-untyped]

from .decision_landscape_serialization import (
    DECISION_REQUEST_SCHEMA_ID,
    DECISION_RESULT_SCHEMA_ID,
    DECISION_VERIFICATION_SCHEMA_ID,
)


class DecisionLandscapeSchemaKind(StrEnum):
    """Identify one shell--scale artifact contract."""

    REQUEST = "request"
    RESULT = "result"
    VERIFICATION = "verification"


@dataclass(frozen=True, slots=True)
class DecisionLandscapeSchema:
    """One immutable packaged JSON Schema."""

    kind: DecisionLandscapeSchemaKind

    def __post_init__(self) -> None:
        if type(self.kind) is not DecisionLandscapeSchemaKind:
            raise TypeError("kind must be DecisionLandscapeSchemaKind")

    @property
    def identity(self) -> str:
        """Return the exact schema identity required by its artifact."""
        match self.kind:
            case DecisionLandscapeSchemaKind.REQUEST:
                return DECISION_REQUEST_SCHEMA_ID
            case DecisionLandscapeSchemaKind.RESULT:
                return DECISION_RESULT_SCHEMA_ID
            case DecisionLandscapeSchemaKind.VERIFICATION:
                return DECISION_VERIFICATION_SCHEMA_ID

    @property
    def artifact_filename(self) -> str:
        """Return the maintained schema filename."""
        return f"shell-scale-decision-landscape-{self.kind.value}.v1.schema.json"

    def canonical_bytes(self) -> bytes:
        """Return the packaged schema document."""
        resource = files(__package__).joinpath(
            "schema_documents",
            f"shell-scale-decision-landscape.{self.kind.value}.schema.json",
        )
        return resource.read_bytes()

    def validate(self, document: bytes) -> None:
        """Validate serialized JSON against this strict schema."""
        if type(document) is not bytes:
            raise TypeError("document must be built-in bytes")
        Draft202012Validator(json.loads(self.canonical_bytes())).validate(
            json.loads(document)
        )

    def write_to(self, directory: Path) -> Path:
        """Write the packaged schema to a destination directory."""
        if not isinstance(directory, Path):
            raise TypeError("directory must be pathlib.Path")
        directory.mkdir(parents=True, exist_ok=True)
        output = directory / self.artifact_filename
        output.write_bytes(self.canonical_bytes())
        return output


__all__ = ["DecisionLandscapeSchema", "DecisionLandscapeSchemaKind"]
