"""CLI adapter for explicit canonical development-decision migration phases."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path, PurePosixPath

from ..decision_migration import (
    DevelopmentDecisionMigrationManifestSerializer,
    DevelopmentDecisionMigrator,
)


def run(argv: Sequence[str] | None = None) -> int:
    """Parse one explicit migration phase and invoke its ActionObject owner."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "phase",
        choices=(
            "propose",
            "write",
            "verify",
            "delete-sources",
            "verify-cutover",
        ),
    )
    parser.add_argument("--repository-root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--source-root", default=".pi/checkpoints")
    parser.add_argument("--target-root", default="decisions")
    arguments = parser.parse_args(argv)
    repository_root = arguments.repository_root
    if not repository_root.is_absolute():
        parser.error("--repository-root must be absolute")
    manifest_path = arguments.manifest
    if not manifest_path.is_absolute():
        parser.error("--manifest must be absolute")
    migrator = DevelopmentDecisionMigrator()
    serializer = DevelopmentDecisionMigrationManifestSerializer()
    if arguments.phase == "propose":
        manifest, result = migrator.propose(
            repository_root,
            PurePosixPath(arguments.source_root),
            PurePosixPath(arguments.target_root),
        )
        payload = serializer.serialize(manifest)
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        if manifest_path.exists() and manifest_path.read_bytes() != payload:
            parser.error("existing manifest bytes differ from the proposal")
        manifest_path.write_bytes(payload)
    else:
        if manifest_path.is_symlink() or not manifest_path.is_file():
            parser.error("--manifest must name a nonsymlink regular file")
        manifest = serializer.deserialize(manifest_path.read_bytes())
        if arguments.phase == "write":
            result = migrator.write(repository_root, manifest)
        elif arguments.phase == "verify":
            result = migrator.verify(repository_root, manifest)
        elif arguments.phase == "delete-sources":
            result = migrator.delete_sources(repository_root, manifest)
        else:
            result = migrator.verify_cutover(repository_root, manifest)
    print(
        json.dumps(
            {
                "decision_count": result.decision_count,
                "phase": result.phase,
                "source_count": result.source_count,
                "target_count": result.target_count,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    return 0
