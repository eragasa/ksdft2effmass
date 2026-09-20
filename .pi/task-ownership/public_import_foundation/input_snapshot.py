"""Explicit input selection, identity, and manifest boundaries."""

from __future__ import annotations

import hashlib
import unicodedata
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from python_public_import_foundation_model import (
    FoundationJsonCodec,
    InputCategory,
    JsonRecord,
    JsonValue,
)


class FoundationFormatError(ValueError):
    """Report one deterministic input, acquisition, or format defect."""


@dataclass(frozen=True, slots=True, kw_only=True)
class FoundationSelectionEntry:
    """Represent one explicitly selected repository-relative input path."""

    category: InputCategory
    path: PurePosixPath

    def __post_init__(self) -> None:
        if type(self.category) is not InputCategory:
            raise TypeError("selection category must be InputCategory")
        FoundationPathPolicy.require_relative(self.path)


@dataclass(frozen=True, slots=True, kw_only=True)
class FoundationInputEntry:
    """Represent one exact selected input and its byte identity."""

    category: InputCategory
    path: PurePosixPath
    sha256: str
    byte_count: int

    def __post_init__(self) -> None:
        if type(self.category) is not InputCategory:
            raise TypeError("input category must be InputCategory")
        FoundationPathPolicy.require_relative(self.path)
        if (
            type(self.sha256) is not str
            or len(self.sha256) != 64
            or any(character not in "0123456789abcdef" for character in self.sha256)
        ):
            raise ValueError("sha256 must be lowercase SHA-256 hexadecimal")
        if type(self.byte_count) is not int or self.byte_count < 0:
            raise ValueError("byte_count must be a nonnegative built-in int")

    @property
    def sort_key(self) -> tuple[str, str]:
        """Return canonical category/path ordering."""
        return self.category.value, self.path.as_posix()


@dataclass(frozen=True, slots=True, kw_only=True)
class FoundationInputManifest:
    """Represent the complete explicit input snapshot for one generation."""

    schema_version: int
    subject_identity: str
    subject_version: str
    entries: tuple[FoundationInputEntry, ...]

    def __post_init__(self) -> None:
        if self.schema_version != 1:
            raise ValueError("input-manifest schema_version must be 1")
        if (
            self.subject_identity
            != "ksdft2effmass.python.public-import-foundation-inputs"
        ):
            raise ValueError("input-manifest subject_identity is unsupported")
        if self.subject_version != "1":
            raise ValueError("input-manifest subject_version is unsupported")
        if type(self.entries) is not tuple or not self.entries:
            raise ValueError("input manifest must contain entries")
        if self.entries != tuple(
            sorted(self.entries, key=lambda entry: entry.sort_key)
        ):
            raise ValueError("input entries must be in canonical category/path order")
        paths = tuple(entry.path.as_posix() for entry in self.entries)
        if len(paths) != len(set(paths)):
            raise ValueError("input manifest paths must be unique")


class FoundationPathPolicy:
    """Own normalized repository-relative path checks."""

    __slots__ = ()

    @staticmethod
    def require_relative(path: PurePosixPath) -> None:
        """Require a normalized repository-relative POSIX path."""
        if type(path) is not PurePosixPath:
            raise TypeError("path must be PurePosixPath")
        rendered = path.as_posix()
        if (
            rendered in {"", "."}
            or path.is_absolute()
            or ".." in path.parts
            or "\\" in rendered
            or unicodedata.normalize("NFC", rendered) != rendered
        ):
            raise ValueError("path must be normalized repository-relative POSIX")

    @staticmethod
    def resolve(repository_root: Path, path: PurePosixPath) -> Path:
        """Resolve one checked path beneath the explicit repository root."""
        FoundationPathPolicy.require_relative(path)
        root = repository_root.resolve()
        resolved = (root / path.as_posix()).resolve()
        if not resolved.is_relative_to(root):
            raise FoundationFormatError(f"path escapes repository root: {path}")
        return resolved


class FoundationInputSelectionParser:
    """Parse an authored tab-separated category/path selection."""

    __slots__ = ()

    def execute(self, payload: bytes) -> tuple[FoundationSelectionEntry, ...]:
        """Return canonical unique selection entries."""
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise FoundationFormatError("selection is not UTF-8") from exc
        entries: list[FoundationSelectionEntry] = []
        for line_number, line in enumerate(text.splitlines(), start=1):
            if not line or line.startswith("#"):
                continue
            fields = line.split("\t")
            if len(fields) != 2:
                raise FoundationFormatError(
                    f"selection line {line_number} must contain category and path"
                )
            entries.append(
                FoundationSelectionEntry(
                    category=InputCategory(fields[0]),
                    path=PurePosixPath(fields[1]),
                )
            )
        ordered = tuple(
            sorted(
                entries,
                key=lambda entry: (
                    entry.category.value,
                    entry.path.as_posix(),
                ),
            )
        )
        paths = tuple(entry.path.as_posix() for entry in ordered)
        if not ordered or len(paths) != len(set(paths)):
            raise FoundationFormatError("selection must contain unique paths")
        return ordered


class FoundationInputManifestSerializer:
    """Serialize and deserialize the closed input-manifest contract."""

    __slots__ = ()

    def encode(self, manifest: FoundationInputManifest) -> bytes:
        """Return canonical manifest bytes."""
        if type(manifest) is not FoundationInputManifest:
            raise TypeError("manifest must be FoundationInputManifest")
        entries: list[JsonValue] = [
            {
                "byte_count": entry.byte_count,
                "category": entry.category.value,
                "path": entry.path.as_posix(),
                "sha256": entry.sha256,
            }
            for entry in manifest.entries
        ]
        return FoundationJsonCodec().encode(
            {
                "entries": entries,
                "schema_version": manifest.schema_version,
                "subject_identity": manifest.subject_identity,
                "subject_version": manifest.subject_version,
            }
        )

    def decode(self, payload: bytes) -> FoundationInputManifest:
        """Decode exact manifest bytes into immutable records."""
        root = self.record(FoundationJsonCodec().decode(payload), "manifest")
        self.require_exact_keys(
            root,
            {"entries", "schema_version", "subject_identity", "subject_version"},
            "manifest",
        )
        entries: list[FoundationInputEntry] = []
        for index, raw_entry in enumerate(self.array(root["entries"], "entries")):
            label = f"entries[{index}]"
            entry = self.record(raw_entry, label)
            self.require_exact_keys(
                entry, {"byte_count", "category", "path", "sha256"}, label
            )
            entries.append(
                FoundationInputEntry(
                    category=InputCategory(
                        self.text(entry["category"], f"{label}.category")
                    ),
                    path=PurePosixPath(self.text(entry["path"], f"{label}.path")),
                    sha256=self.text(entry["sha256"], f"{label}.sha256"),
                    byte_count=self.integer(entry["byte_count"], f"{label}.byte_count"),
                )
            )
        return FoundationInputManifest(
            schema_version=self.integer(root["schema_version"], "schema_version"),
            subject_identity=self.text(root["subject_identity"], "subject_identity"),
            subject_version=self.text(root["subject_version"], "subject_version"),
            entries=tuple(entries),
        )

    @staticmethod
    def record(value: JsonValue, label: str) -> JsonRecord:
        if type(value) is not dict:
            raise FoundationFormatError(f"{label} must be an object")
        return value

    @staticmethod
    def array(value: JsonValue, label: str) -> list[JsonValue]:
        if type(value) is not list:
            raise FoundationFormatError(f"{label} must be an array")
        return value

    @staticmethod
    def text(value: JsonValue | None, label: str) -> str:
        if type(value) is not str:
            raise FoundationFormatError(f"{label} must be a string")
        return value

    @staticmethod
    def integer(value: JsonValue, label: str) -> int:
        if type(value) is not int:
            raise FoundationFormatError(f"{label} must be an integer")
        return value

    @staticmethod
    def require_exact_keys(record: JsonRecord, keys: set[str], label: str) -> None:
        if set(record) != keys:
            raise FoundationFormatError(
                f"{label} fields do not match the closed contract"
            )


@dataclass(frozen=True, slots=True)
class FoundationInputManifestPreparer:
    """Hash one explicit authored selection without discovering paths."""

    repository_root: Path

    def execute(
        self, selections: tuple[FoundationSelectionEntry, ...]
    ) -> FoundationInputManifest:
        """Return a canonical content-identified manifest."""
        entries: list[FoundationInputEntry] = []
        for selection in selections:
            selected = FoundationPathPolicy.resolve(
                self.repository_root, selection.path
            )
            if not selected.is_file() or selected.is_symlink():
                raise FoundationFormatError(
                    f"selected input is not a nonsymlink regular file: {selection.path}"
                )
            payload = selected.read_bytes()
            entries.append(
                FoundationInputEntry(
                    category=selection.category,
                    path=selection.path,
                    sha256=hashlib.sha256(payload).hexdigest(),
                    byte_count=len(payload),
                )
            )
        return FoundationInputManifest(
            schema_version=1,
            subject_identity="ksdft2effmass.python.public-import-foundation-inputs",
            subject_version="1",
            entries=tuple(sorted(entries, key=lambda entry: entry.sort_key)),
        )
