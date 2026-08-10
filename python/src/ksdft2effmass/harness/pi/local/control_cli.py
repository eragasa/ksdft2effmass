"""Stable command-line surface for authoritative harness control state."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .dbcontrol import (
    HarnessControlMigrationRequest,
    HarnessControlMigrationResult,
    HarnessControlMigrator,
    HarnessControlVerificationResult,
    HarnessControlVerifier,
)


def main() -> int:
    """Migrate or verify one explicitly selected repository root."""
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("migrate", "verify"))
    parser.add_argument("--repository-root", type=Path, required=True)
    parser.add_argument(
        "--evidence-module-ownership",
        type=Path,
        help=(
            "repository-relative closed Python-conformance ownership input "
            "used only by migrate"
        ),
    )
    parser.add_argument(
        "--evidence-profile-matrix",
        type=Path,
        help="repository-relative generic evidence profile matrix used only by migrate",
    )
    parser.add_argument(
        "--evidence-module",
        type=Path,
        action="append",
        default=[],
        help="explicit repository-relative Python test source (repeatable)",
    )
    parser.add_argument(
        "--evidence-migration",
        type=Path,
        help="explicit repository-relative predecessor migration map",
    )
    parser.add_argument("--resource-profile", type=Path)
    parser.add_argument("--generic-resource-manifest", type=Path)
    parser.add_argument("--generic-resource-root", type=Path)
    parser.add_argument("--local-resource-manifest", type=Path)
    parser.add_argument("--local-resource-root", type=Path)
    args = parser.parse_args()
    root = args.repository_root.resolve()
    result: HarnessControlMigrationResult | HarnessControlVerificationResult
    if args.action == "migrate":
        result = HarnessControlMigrator().execute(
            HarnessControlMigrationRequest(
                root,
                evidence_module_ownership_path=args.evidence_module_ownership,
                evidence_profile_matrix_path=args.evidence_profile_matrix,
                evidence_module_paths=tuple(args.evidence_module),
                evidence_migration_path=args.evidence_migration,
                resource_profile_path=args.resource_profile,
                generic_resource_manifest_path=args.generic_resource_manifest,
                generic_resource_root_path=args.generic_resource_root,
                local_resource_manifest_path=args.local_resource_manifest,
                local_resource_root_path=args.local_resource_root,
            )
        )
    else:
        if (
            args.evidence_module_ownership is not None
            or args.evidence_profile_matrix is not None
            or args.evidence_module
            or args.evidence_migration is not None
            or args.resource_profile is not None
            or args.generic_resource_manifest is not None
            or args.generic_resource_root is not None
            or args.local_resource_manifest is not None
            or args.local_resource_root is not None
        ):
            parser.error("evidence and resource inputs are valid only with migrate")
        result = HarnessControlVerifier().execute(root)
    print(
        json.dumps(
            {name: getattr(result, name) for name in result.__dataclass_fields__},
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
