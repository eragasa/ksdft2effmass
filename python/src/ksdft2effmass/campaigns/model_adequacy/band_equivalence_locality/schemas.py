"""Immutable JSON Schema documents for band-equivalence/locality artifacts."""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import StrEnum
from importlib.resources import files
from pathlib import Path

from jsonschema import Draft202012Validator  # type: ignore[import-untyped]

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.definitions import (  # noqa: E501
    BandEquivalenceLocalityFamily,
)


class BandEquivalenceLocalitySchemaKind(StrEnum):
    """Wire-document identities supported by the locality artifact contract."""

    ANALYSIS_REQUEST = "analysis-request"
    ANALYSIS_RESULT = "analysis-result"
    VERIFICATION_RESULT = "verification-result"
    REFINEMENT_RESULT = "refinement-result"


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalitySchema:
    """One immutable, packaged JSON Schema document.

    The schema's heterogeneous JSON representation is contained in the packaged
    resource.  Callers receive canonical bytes and validation behavior rather than a
    mutable, string-key mapping.
    """

    family: BandEquivalenceLocalityFamily
    kind: BandEquivalenceLocalitySchemaKind

    def __post_init__(self) -> None:
        if not isinstance(self.family, BandEquivalenceLocalityFamily):
            raise TypeError("family must be a BandEquivalenceLocalityFamily")
        if not isinstance(self.kind, BandEquivalenceLocalitySchemaKind):
            raise TypeError("kind must be a BandEquivalenceLocalitySchemaKind")

    @property
    def identity(self) -> str:
        """Return the stable ``$id`` carried by this schema."""

        match self.kind:
            case BandEquivalenceLocalitySchemaKind.ANALYSIS_REQUEST:
                suffix = "input"
            case BandEquivalenceLocalitySchemaKind.ANALYSIS_RESULT:
                suffix = "result"
            case BandEquivalenceLocalitySchemaKind.VERIFICATION_RESULT:
                suffix = "verification"
            case BandEquivalenceLocalitySchemaKind.REFINEMENT_RESULT:
                return f"{self.family.value}.calculation.refinement-assessment.v1"
        return f"{self.family.value}.calculation.{suffix}.v1"

    @property
    def artifact_filename(self) -> str:
        """Return the maintained artifact filename for this schema kind."""

        match self.kind:
            case BandEquivalenceLocalitySchemaKind.ANALYSIS_REQUEST:
                return "band-equivalence-locality-input.v1.schema.json"
            case BandEquivalenceLocalitySchemaKind.ANALYSIS_RESULT:
                return "band-equivalence-locality-result.v1.schema.json"
            case BandEquivalenceLocalitySchemaKind.VERIFICATION_RESULT:
                return "band-equivalence-locality-verification.v1.schema.json"
            case BandEquivalenceLocalitySchemaKind.REFINEMENT_RESULT:
                return "band-equivalence-locality-refinement.v1.schema.json"

    def canonical_bytes(self) -> bytes:
        """Return the packaged canonical JSON bytes without decoding to a mapping."""

        resource_name = f"{self.family.value}.{self.kind.value}.schema.json"
        resource = files(__package__).joinpath("schema_documents", resource_name)
        return resource.read_bytes()

    def validate(self, document: bytes) -> None:
        """Validate one serialized JSON document against this schema."""

        if type(document) is not bytes:
            raise TypeError("document must be built-in bytes")
        validator = Draft202012Validator(json.loads(self.canonical_bytes()))
        validator.validate(json.loads(document))

    def write_to(self, directory: Path) -> Path:
        """Write the canonical schema document and return its output path."""

        if not isinstance(directory, Path):
            raise TypeError("directory must be a pathlib.Path")
        directory.mkdir(parents=True, exist_ok=True)
        output = directory / self.artifact_filename
        output.write_bytes(self.canonical_bytes())
        return output


__all__ = [
    "BandEquivalenceLocalitySchema",
    "BandEquivalenceLocalitySchemaKind",
]
