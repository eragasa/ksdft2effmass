"""Explicit migration of legacy checkpoints to canonical development decisions.

The migration is manifest-driven and split into proposal, write, verification, and
source-deletion phases. Canonical successor bytes are produced only by
``DevelopmentDecisionSerializer`` under its declared legacy normalization policy.
Source deletion is permitted only after every selected source still matches its
successor provenance and every successor round-trips canonically.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import cast

from ._contract import canonical_bytes, require_identifier, require_path, strict_json
from .decisions import DevelopmentDecision, DevelopmentDecisionSerializer


@dataclass(frozen=True, slots=True, kw_only=True)
class DevelopmentDecisionMigrationEntry:
    """Map one exact legacy source to one canonical successor identity and path."""

    source_path: PurePosixPath
    target_path: PurePosixPath
    decision_id: str
    predecessor_decision_id: str | None

    def __post_init__(self) -> None:
        for name in ("source_path", "target_path"):
            value = getattr(self, name)
            if type(value) is not PurePosixPath:
                raise TypeError(f"{name} must be PurePosixPath")
            require_path(value.as_posix(), name)
        require_identifier(self.decision_id, "decision_id")
        if self.predecessor_decision_id is not None:
            require_identifier(self.predecessor_decision_id, "predecessor_decision_id")
        if self.source_path == self.target_path:
            raise ValueError("source and target paths must differ")


@dataclass(frozen=True, slots=True, kw_only=True)
class DevelopmentDecisionMigrationManifest:
    """Represent one complete explicit migration and obsolete-source selection."""

    schema_version: int
    adapter_version: str
    entries: tuple[DevelopmentDecisionMigrationEntry, ...]
    obsolete_paths: tuple[PurePosixPath, ...]

    def __post_init__(self) -> None:
        if type(self.schema_version) is not int or self.schema_version != 1:
            raise ValueError("schema_version must equal 1")
        require_identifier(self.adapter_version, "adapter_version")
        if type(self.entries) is not tuple or any(
            type(value) is not DevelopmentDecisionMigrationEntry
            for value in self.entries
        ):
            raise TypeError("entries must contain DevelopmentDecisionMigrationEntry")
        if not self.entries:
            raise ValueError("entries must not be empty")
        source_keys = tuple(value.source_path.as_posix() for value in self.entries)
        target_keys = tuple(value.target_path.as_posix() for value in self.entries)
        identity_keys = tuple(value.decision_id for value in self.entries)
        if source_keys != tuple(sorted(set(source_keys))):
            raise ValueError("entry source paths must be sorted and unique")
        if len(target_keys) != len(set(target_keys)):
            raise ValueError("entry target paths must be unique")
        if len(identity_keys) != len(set(identity_keys)):
            raise ValueError("entry decision identities must be unique")
        if type(self.obsolete_paths) is not tuple:
            raise TypeError("obsolete_paths must be a tuple")
        for value in self.obsolete_paths:
            if type(value) is not PurePosixPath:
                raise TypeError("obsolete_paths must contain PurePosixPath values")
            require_path(value.as_posix(), "obsolete_paths item")
        obsolete_keys = tuple(value.as_posix() for value in self.obsolete_paths)
        if obsolete_keys != tuple(sorted(set(obsolete_keys))):
            raise ValueError("obsolete_paths must be sorted and unique")
        if set(obsolete_keys) & set(source_keys):
            raise ValueError("obsolete paths must be separate from migrated sources")
        known = set(identity_keys)
        if any(
            entry.predecessor_decision_id is not None
            and entry.predecessor_decision_id not in known
            for entry in self.entries
        ):
            raise ValueError("every predecessor must name a migrated decision")


@dataclass(frozen=True, slots=True)
class DevelopmentDecisionMigrationManifestSerializer:
    """Own canonical JSON mechanics for the explicit migration manifest."""

    def serialize(self, manifest: DevelopmentDecisionMigrationManifest) -> bytes:
        """Return canonical JSON bytes for one migration manifest."""
        if type(manifest) is not DevelopmentDecisionMigrationManifest:
            raise TypeError("manifest must be DevelopmentDecisionMigrationManifest")
        wire = {
            "adapter_version": manifest.adapter_version,
            "entries": [
                {
                    "decision_id": entry.decision_id,
                    "predecessor_decision_id": entry.predecessor_decision_id,
                    "source_path": entry.source_path.as_posix(),
                    "target_path": entry.target_path.as_posix(),
                }
                for entry in manifest.entries
            ],
            "obsolete_paths": [value.as_posix() for value in manifest.obsolete_paths],
            "schema_version": manifest.schema_version,
        }
        return canonical_bytes(wire)

    execute = serialize

    def deserialize(self, payload: bytes) -> DevelopmentDecisionMigrationManifest:
        """Decode canonical migration-manifest bytes with closed fields."""
        value = strict_json(payload)
        if type(value) is not dict:
            raise TypeError("migration manifest must contain one JSON object")
        source = cast(dict[str, object], value)
        expected = {
            "adapter_version",
            "entries",
            "obsolete_paths",
            "schema_version",
        }
        if set(source) != expected:
            raise ValueError("migration manifest fields are not closed")
        entries_value = source["entries"]
        obsolete_value = source["obsolete_paths"]
        if type(entries_value) is not list or type(obsolete_value) is not list:
            raise TypeError("migration manifest collections must be arrays")
        entries = []
        for item in cast(list[object], entries_value):
            if type(item) is not dict:
                raise TypeError("migration entry must be an object")
            record = cast(dict[str, object], item)
            if set(record) != {
                "decision_id",
                "predecessor_decision_id",
                "source_path",
                "target_path",
            }:
                raise ValueError("migration entry fields are not closed")
            entries.append(
                DevelopmentDecisionMigrationEntry(
                    source_path=PurePosixPath(self._string(record, "source_path")),
                    target_path=PurePosixPath(self._string(record, "target_path")),
                    decision_id=self._string(record, "decision_id"),
                    predecessor_decision_id=self._optional_string(
                        record, "predecessor_decision_id"
                    ),
                )
            )
        obsolete = tuple(
            PurePosixPath(self._array_string(value, "obsolete_paths"))
            for value in cast(list[object], obsolete_value)
        )
        schema_version = source["schema_version"]
        if type(schema_version) is not int:
            raise TypeError("schema_version must be a built-in int")
        manifest = DevelopmentDecisionMigrationManifest(
            schema_version=schema_version,
            adapter_version=self._string(source, "adapter_version"),
            entries=tuple(entries),
            obsolete_paths=obsolete,
        )
        if self.serialize(manifest) != payload:
            raise ValueError("migration manifest must use canonical JSON bytes")
        return manifest

    @staticmethod
    def _string(record: dict[str, object], name: str) -> str:
        value = record[name]
        if type(value) is not str:
            raise TypeError(f"{name} must be a built-in str")
        return value

    @staticmethod
    def _optional_string(record: dict[str, object], name: str) -> str | None:
        value = record[name]
        if value is not None and type(value) is not str:
            raise TypeError(f"{name} must be a built-in str or null")
        return value

    @staticmethod
    def _array_string(value: object, name: str) -> str:
        if type(value) is not str:
            raise TypeError(f"{name} must contain built-in strings")
        return value


@dataclass(frozen=True, slots=True, kw_only=True)
class DevelopmentDecisionMigrationResult:
    """Record one deterministic migration phase outcome."""

    phase: str
    decision_count: int
    source_count: int
    target_count: int

    def __post_init__(self) -> None:
        if self.phase not in {
            "proposed",
            "written",
            "verified",
            "sources_deleted",
            "cutover_verified",
        }:
            raise ValueError("phase is not supported")
        for name in ("decision_count", "source_count", "target_count"):
            value = getattr(self, name)
            if type(value) is not int or value < 0:
                raise ValueError(f"{name} must be a nonnegative built-in int")


@dataclass(frozen=True, slots=True)
class DevelopmentDecisionMigrator:
    """Propose, write, verify, and delete one explicit checkpoint migration."""

    decision_serializer: DevelopmentDecisionSerializer = DevelopmentDecisionSerializer()
    manifest_serializer: DevelopmentDecisionMigrationManifestSerializer = (
        DevelopmentDecisionMigrationManifestSerializer()
    )

    def propose(
        self,
        repository_root: Path,
        source_root: PurePosixPath,
        target_root: PurePosixPath,
    ) -> tuple[
        DevelopmentDecisionMigrationManifest,
        DevelopmentDecisionMigrationResult,
    ]:
        """Create an explicit proposal from top-level legacy decision records."""
        self._repository(repository_root)
        source_directory = repository_root / source_root
        target_directory = repository_root / target_root
        if not source_directory.is_dir() or source_directory.is_symlink():
            raise ValueError("source_root must be a nonsymlink directory")
        if target_directory.exists() and not target_directory.is_dir():
            raise ValueError("target_root must be absent or a directory")
        entries = []
        for source in sorted(source_directory.glob("*.json")):
            if source.name == "checkpoint.schema.json":
                continue
            payload = source.read_bytes()
            raw = strict_json(payload)
            if type(raw) is not dict:
                raise TypeError("legacy checkpoint must contain one JSON object")
            record = cast(dict[str, object], raw)
            checkpoint_id = record.get("checkpoint_id")
            if type(checkpoint_id) is not str:
                raise TypeError("legacy checkpoint requires checkpoint_id")
            predecessor = "P2-HC03" if checkpoint_id == "P2-HC04" else None
            entries.append(
                DevelopmentDecisionMigrationEntry(
                    source_path=PurePosixPath(
                        source.relative_to(repository_root).as_posix()
                    ),
                    target_path=target_root / source.name,
                    decision_id=checkpoint_id,
                    predecessor_decision_id=predecessor,
                )
            )
        manifest = DevelopmentDecisionMigrationManifest(
            schema_version=1,
            adapter_version="legacy-checkpoint-v2-lossy",
            entries=tuple(entries),
            obsolete_paths=(source_root / "checkpoint.schema.json",),
        )
        return manifest, DevelopmentDecisionMigrationResult(
            phase="proposed",
            decision_count=len(entries),
            source_count=len(entries) + len(manifest.obsolete_paths),
            target_count=0,
        )

    def write(
        self,
        repository_root: Path,
        manifest: DevelopmentDecisionMigrationManifest,
    ) -> DevelopmentDecisionMigrationResult:
        """Write every canonical successor without replacing differing bytes."""
        self._repository(repository_root)
        products = self._products(repository_root, manifest)
        for target, _decision, payload in products:
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists() or target.is_symlink():
                if target.is_symlink() or not target.is_file():
                    raise ValueError("existing migration target has unsupported type")
                if target.read_bytes() != payload:
                    raise ValueError("existing migration target bytes differ")
                continue
            descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(payload)
        self.verify(repository_root, manifest)
        return DevelopmentDecisionMigrationResult(
            phase="written",
            decision_count=len(products),
            source_count=len(manifest.entries) + len(manifest.obsolete_paths),
            target_count=len(products),
        )

    def verify(
        self,
        repository_root: Path,
        manifest: DevelopmentDecisionMigrationManifest,
    ) -> DevelopmentDecisionMigrationResult:
        """Verify source-to-successor equality and canonical target bytes."""
        self._repository(repository_root)
        products = self._products(repository_root, manifest)
        for target, decision, payload in products:
            if target.is_symlink() or not target.is_file():
                raise ValueError("migration target is missing or unsupported")
            observed = target.read_bytes()
            if observed != payload:
                raise ValueError("migration target differs from adapted source")
            if self.decision_serializer.deserialize(observed) != decision:
                raise ValueError("migration target does not round-trip")
        return DevelopmentDecisionMigrationResult(
            phase="verified",
            decision_count=len(products),
            source_count=len(manifest.entries) + len(manifest.obsolete_paths),
            target_count=len(products),
        )

    def delete_sources(
        self,
        repository_root: Path,
        manifest: DevelopmentDecisionMigrationManifest,
    ) -> DevelopmentDecisionMigrationResult:
        """Delete selected originals only after complete migration verification."""
        verified = self.verify(repository_root, manifest)
        sources = [repository_root / entry.source_path for entry in manifest.entries]
        obsolete = [repository_root / value for value in manifest.obsolete_paths]
        for path in (*sources, *obsolete):
            if path.is_symlink() or not path.is_file():
                raise ValueError("selected source is missing or unsupported")
        for path in (*sources, *obsolete):
            path.unlink()
        return DevelopmentDecisionMigrationResult(
            phase="sources_deleted",
            decision_count=verified.decision_count,
            source_count=len(sources) + len(obsolete),
            target_count=verified.target_count,
        )

    def verify_cutover(
        self,
        repository_root: Path,
        manifest: DevelopmentDecisionMigrationManifest,
    ) -> DevelopmentDecisionMigrationResult:
        """Verify canonical targets and absence of every selected legacy source."""
        self._repository(repository_root)
        for entry in manifest.entries:
            source = repository_root / entry.source_path
            target = repository_root / entry.target_path
            if source.exists() or source.is_symlink():
                raise ValueError("selected legacy source remains after cutover")
            if target.is_symlink() or not target.is_file():
                raise ValueError("canonical migration target is missing or unsupported")
            decision = self.decision_serializer.deserialize(target.read_bytes())
            if (
                decision.decision_id != entry.decision_id
                or decision.predecessor_decision_id != entry.predecessor_decision_id
                or decision.source_provenance.source_path
                != entry.source_path.as_posix()
                or decision.source_provenance.adapter_version
                != manifest.adapter_version
            ):
                raise ValueError("canonical migration target disagrees with manifest")
        for relative in manifest.obsolete_paths:
            path = repository_root / relative
            if path.exists() or path.is_symlink():
                raise ValueError("selected obsolete source remains after cutover")
        return DevelopmentDecisionMigrationResult(
            phase="cutover_verified",
            decision_count=len(manifest.entries),
            source_count=0,
            target_count=len(manifest.entries),
        )

    def _products(
        self,
        repository_root: Path,
        manifest: DevelopmentDecisionMigrationManifest,
    ) -> tuple[tuple[Path, DevelopmentDecision, bytes], ...]:
        products = []
        for entry in manifest.entries:
            source = repository_root / entry.source_path
            target = repository_root / entry.target_path
            if source.is_symlink() or not source.is_file():
                raise ValueError("migration source is missing or unsupported")
            try:
                decision = self.decision_serializer.adapt_legacy(
                    source.read_bytes(),
                    decision_id=entry.decision_id,
                    source_path=entry.source_path.as_posix(),
                    predecessor_decision_id=entry.predecessor_decision_id,
                    adapter_version=manifest.adapter_version,
                )
            except (TypeError, ValueError) as error:
                raise ValueError(
                    f"cannot adapt legacy source {entry.source_path.as_posix()}: "
                    f"{error}"
                ) from error
            products.append(
                (target, decision, self.decision_serializer.serialize(decision))
            )
        return tuple(products)

    @staticmethod
    def _repository(repository_root: Path) -> None:
        if not isinstance(repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        if not repository_root.is_absolute() or repository_root.is_symlink():
            raise ValueError("repository_root must be an absolute nonsymlink path")
        if not repository_root.is_dir():
            raise ValueError("repository_root must be a directory")
