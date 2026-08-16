"""Command-line adapter for derived Harness projection synchronization."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from dataclasses import asdict
from pathlib import Path

from ksdft2effmass.harness.pi import PiHarnessConfigurationDeserializer
from ksdft2effmass.harness.pi.local import (
    HarnessControlMigrationRequest,
    HarnessControlMigrationResult,
    HarnessControlMigrator,
    HarnessControlVerificationResult,
    HarnessControlVerifier,
)


def _verification_passed(result: HarnessControlVerificationResult) -> bool:
    """Return whether every represented control verification check agrees."""
    return (
        result.integrity_check == "ok"
        and result.foreign_key_issue_count == 0
        and result.semantic_digest == result.reconstructed_semantic_digest
        and result.projections_identical
        and result.schema_version_agrees
        and result.sql_identical
        and result.manifest_identical
        and not result.findings
    )


def cli_main(argv: Sequence[str] | None = None) -> int:
    """Synchronize or compare derived projections for one repository root."""
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("sync", "check"))
    parser.add_argument("--repository-root", type=Path, required=True)
    parser.add_argument(
        "--pi-settings",
        type=Path,
        help=(
            "repository-relative Pi project settings used only by sync; "
            "defaults to .pi/settings.json"
        ),
    )
    parser.add_argument(
        "--evidence-profile-matrix",
        type=Path,
        help="repository-relative generic evidence profile matrix used only by sync",
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
    args = parser.parse_args(argv)
    root = args.repository_root.resolve()
    try:
        return _execute(args, parser, root)
    except (TypeError, ValueError) as exc:
        print(json.dumps({"error": str(exc), "status": "INVALID_INPUT"}))
        return 2
    except Exception as exc:  # noqa: BLE001 - exact command-boundary translation
        print(
            json.dumps(
                {"error": f"{type(exc).__name__}: {exc}", "status": "INTERNAL_ERROR"}
            )
        )
        return 3


def _execute(
    args: argparse.Namespace, parser: argparse.ArgumentParser, root: Path
) -> int:
    """Execute parsed control arguments and render the complete public result."""
    result: HarnessControlMigrationResult | HarnessControlVerificationResult
    if args.action == "sync":
        required = {
            "--evidence-profile-matrix": args.evidence_profile_matrix,
            "--evidence-migration": args.evidence_migration,
            "--resource-profile": args.resource_profile,
            "--generic-resource-manifest": args.generic_resource_manifest,
            "--generic-resource-root": args.generic_resource_root,
            "--local-resource-manifest": args.local_resource_manifest,
            "--local-resource-root": args.local_resource_root,
        }
        missing = [name for name, value in required.items() if value is None]
        if not args.evidence_module:
            missing.append("--evidence-module")
        if missing:
            parser.error("sync requires canonical inputs: " + ", ".join(missing))
        settings_relative = args.pi_settings or Path(".pi/settings.json")
        if (
            settings_relative.is_absolute()
            or settings_relative == Path(".")
            or ".." in settings_relative.parts
        ):
            raise ValueError(
                "pi-settings must be repository-relative and root-confined"
            )
        settings_candidate = root / settings_relative
        if settings_candidate.is_symlink() or not settings_candidate.is_file():
            raise ValueError("pi-settings must select a regular nonsymlink file")
        settings_path = settings_candidate.resolve(strict=True)
        settings_path.relative_to(root)
        configuration = PiHarnessConfigurationDeserializer().execute(
            settings_path.read_bytes()
        )
        result = HarnessControlMigrator().execute(
            HarnessControlMigrationRequest(
                root,
                evidence_profile_matrix_path=args.evidence_profile_matrix,
                evidence_module_paths=tuple(args.evidence_module),
                evidence_migration_path=args.evidence_migration,
                resource_profile_path=args.resource_profile,
                generic_resource_manifest_path=args.generic_resource_manifest,
                generic_resource_root_path=args.generic_resource_root,
                local_resource_manifest_path=args.local_resource_manifest,
                local_resource_root_path=args.local_resource_root,
                pi_harness_configuration=configuration,
            )
        )
    else:
        if (
            args.pi_settings is not None
            or args.evidence_profile_matrix is not None
            or args.evidence_module
            or args.evidence_migration is not None
            or args.resource_profile is not None
            or args.generic_resource_manifest is not None
            or args.generic_resource_root is not None
            or args.local_resource_manifest is not None
            or args.local_resource_root is not None
        ):
            parser.error(
                "configuration, evidence, and resource inputs are valid only with sync"
            )
        result = HarnessControlVerifier().execute(root)
    print(json.dumps(asdict(result), indent=2))
    if isinstance(result, HarnessControlVerificationResult):
        return 0 if _verification_passed(result) else 1
    return 0


main = cli_main


if __name__ == "__main__":
    raise SystemExit(cli_main())
