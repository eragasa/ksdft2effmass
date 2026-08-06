#!/usr/bin/env python3
"""Validate structural completion of TEST-EVIDENCE-SKILL-1."""

from __future__ import annotations

import ast
import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REQUIRED = (
    "harness/pi/skills/develop-python-test-evidence/SKILL.md",
    "harness/pi/skills/develop-python-test-evidence/references/test-evidence-conventions.md",
    "harness/pi/skills/develop-python-test-evidence/descriptor.json",
    "harness/pi/validation/validate_python_test_evidence.py",
    ".pi/skills/develop-python-test-evidence/SKILL.md",
    ".pi/skills/develop-python-test-evidence/references/test-evidence-conventions.md",
    ".pi/skills/validate_skill_capabilities.py",
    "harness/pi/fixtures/python-test-evidence/valid/test__ExampleRecord.py",
    "harness/pi/fixtures/python-test-evidence/valid/ownership.json",
    "harness/pi/fixtures/python-test-evidence/invalid/test__bad-artifact.py",
    "harness/pi/fixtures/python-test-evidence/invalid/ownership.json",
    ".pi/evidence/develop-python-test-evidence-skill-correction/forward-validation.json",
    ".pi/evidence/develop-python-test-evidence-skill-correction/forward-findings.md",
    "harness/pi/resource-manifest.json",
    "harness/local/resource-manifest.json",
    "harness/local/profiles/ksdft2effmass-v2.json",
    "harness/local/validation-route.json",
    "harness/local/validation/replay_current_validators.py",
)
RETIRED = (
    "harness/pi/skills/document-python-research-software/references/test-evidence-documentation.md",
    ".pi/skills/document-python-research-software/references/test-evidence-documentation.md",
)
FORBIDDEN_CHANGED_PREFIXES = (
    "python/src/ksdft2effmass/provenance/",
    "python/tests/software_verification/ksdft2effmass/provenance/",
    "specification/provenance/v1/",
    ".pi/checkpoints/P2-",
)


def main() -> int:
    issues: list[str] = []
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            issues.append(f"missing required file: {relative}")
    for relative in RETIRED:
        if (ROOT / relative).exists():
            issues.append(f"superseded reference still exists: {relative}")

    skill_path = ROOT / "harness/pi/skills/develop-python-test-evidence/SKILL.md"
    if skill_path.is_file():
        text = skill_path.read_text(encoding="utf-8")
        expected_frontmatter = (
            "---\n"
            "name: develop-python-test-evidence\n"
            "description: Designs, writes, modifies, and reviews maintained Python software-verification, numerical-verification, and separately authorized validation or UQ tests. Use when creating class-owned or artifact-owned pytest evidence, test fixtures, parameterized cases, independent oracles, acceptance rules, test documentation, or test-evidence audits.\n"
            "---\n"
        )
        if not text.startswith(expected_frontmatter):
            issues.append(
                "canonical skill does not have the exact required two-field frontmatter"
            )
        if "behavior-version:" in text.split("---", 2)[1]:
            issues.append(
                "behavior-version must remain in descriptor, not skill frontmatter"
            )
        if "references/test-evidence-conventions.md" not in text:
            issues.append("canonical skill does not load its full reference")

    conventions_path = (
        ROOT
        / "harness/pi/skills/develop-python-test-evidence/references/test-evidence-conventions.md"
    )
    if conventions_path.is_file():
        conventions = conventions_path.read_text(encoding="utf-8")
        for heading in (
            "Facet and represented meaning",
            "Intrinsic and cross-object scope",
            "VVUQ and scientific exclusions",
        ):
            if heading not in conventions:
                issues.append(f"conventions lack maintained heading: {heading}")
        if (
            "Fifteen-step workflow" not in conventions
            or "AUTHORIZED_TEST_EVIDENCE_DOC_WRITE" not in conventions
        ):
            issues.append("conventions lack full workflow or invocation profiles")
        if (
            "test_method__eq__" not in conventions
            or "test_protocol__eq__" in conventions
        ):
            issues.append(
                "conventions do not apply the accepted method-owned eq classification"
            )

    generic_new_files = tuple(
        (ROOT / "harness/pi/skills/develop-python-test-evidence").rglob("*")
    ) + (
        ROOT / "harness/pi/validation/validate_python_test_evidence.py",
        *tuple((ROOT / "harness/pi/fixtures/python-test-evidence").rglob("*")),
    )
    for path in generic_new_files:
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            for leaked in ("SV-PROV", "ksdft2effmass", ".pi/"):
                if leaked in text:
                    issues.append(
                        f"generic project leakage {leaked!r}: {path.relative_to(ROOT)}"
                    )

    validator = ROOT / "harness/pi/validation/validate_python_test_evidence.py"
    if validator.is_file():
        try:
            ast.parse(validator.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, SyntaxError) as error:
            issues.append(f"convention validator is not parseable: {error}")

    manifest_path = ROOT / "harness/pi/resource-manifest.json"
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            resource_ids = {item["resource_id"] for item in manifest["resources"]}
        except (
            OSError,
            UnicodeError,
            json.JSONDecodeError,
            KeyError,
            TypeError,
        ) as error:
            issues.append(f"generic manifest is unreadable: {error}")
            resource_ids = set()
        for resource_id in (
            "pih.skill.develop-python-test-evidence.v1",
            "pih.reference.test-evidence-conventions.v1",
            "pih.manifest.skill-descriptor.develop-python-test-evidence.v1",
        ):
            if resource_id not in resource_ids:
                issues.append(f"generic manifest lacks {resource_id}")

    for relative in ("SKILL.md", "references/test-evidence-conventions.md"):
        canonical = ROOT / "harness/pi/skills/develop-python-test-evidence" / relative
        live = ROOT / ".pi/skills/develop-python-test-evidence" / relative
        if (
            canonical.is_file()
            and live.is_file()
            and canonical.read_bytes() != live.read_bytes()
        ):
            issues.append(f"canonical/live byte mismatch: {relative}")

    validator_command = [
        "python",
        "harness/pi/validation/validate_python_test_evidence.py",
    ]
    class_path = "harness/pi/fixtures/python-test-evidence/valid/test__ExampleRecord.py"
    class_ownership = "harness/pi/fixtures/python-test-evidence/valid/ownership.json"
    controlled_cases = [
        (
            "valid-class",
            [class_path, "--ownership", class_ownership],
            0,
            {},
            {
                "class_owned_modules": 1,
                "artifact_owned_modules": 0,
                "test_functions": 1,
                "helper_functions": 0,
                "static_collected_parameter_cases": 1,
                "unique_evidence_owners": 1,
            },
        ),
        (
            "valid-artifact",
            [
                "harness/pi/fixtures/python-test-evidence/valid-artifact/test__json_schema.py",
                "--ownership",
                "harness/pi/fixtures/python-test-evidence/valid-artifact/ownership.json",
            ],
            0,
            {},
            {
                "class_owned_modules": 0,
                "artifact_owned_modules": 1,
                "test_functions": 1,
                "helper_functions": 1,
                "static_collected_parameter_cases": 2,
                "unique_evidence_owners": 1,
            },
        ),
        (
            "invalid-grammar",
            [
                "harness/pi/fixtures/python-test-evidence/invalid/test__bad-artifact.py",
                "--ownership",
                "harness/pi/fixtures/python-test-evidence/invalid/ownership.json",
            ],
            1,
            {
                "TE.ARTIFACT_FILENAME": 1,
                "TE.FUNCTION_DOC": 2,
                "TE.HELPER_NAME": 1,
                "TE.HELPER_PRIVATE": 1,
                "TE.HIDDEN_LOOP": 1,
                "TE.MODULE_DOC": 1,
                "TE.MODULE_OPENING": 1,
                "TE.PARAMETER_ID": 3,
                "TE.SUPERSEDED_HEADING": 2,
                "TE.TEST_NAME": 1,
            },
            {"static_collected_parameter_cases": 3, "unique_evidence_owners": 0},
        ),
        (
            "duplicate-ids",
            [
                "harness/pi/fixtures/python-test-evidence/duplicate-ids/test__ExampleOne.py",
                "harness/pi/fixtures/python-test-evidence/duplicate-ids/test__ExampleTwo.py",
                "--ownership",
                "harness/pi/fixtures/python-test-evidence/duplicate-ids/ownership.json",
            ],
            1,
            {"TE.DUPLICATE_ID": 1},
            {"test_functions": 2, "unique_evidence_owners": 1},
        ),
        (
            "unknown-static",
            [
                "harness/pi/fixtures/python-test-evidence/unknown-static-count/test__ExampleDynamic.py",
                "--ownership",
                "harness/pi/fixtures/python-test-evidence/unknown-static-count/ownership.json",
            ],
            1,
            {"TE.PARAMETER_ID": 1},
            {"static_collected_parameter_cases": None, "unique_evidence_owners": 1},
        ),
    ]
    ownership_expectations = {
        "invalid-json.txt": {"TE.OWNERSHIP_INPUT": 1},
        "null.json": {"TE.OWNERSHIP_INPUT": 1},
        "top-unexpected.json": {"TE.OWNERSHIP_INPUT": 1},
        "nonstring-path.json": {"TE.OWNERSHIP_COVERAGE": 1, "TE.OWNERSHIP_PATH": 1},
        "numeric-path.json": {"TE.OWNERSHIP_COVERAGE": 1, "TE.OWNERSHIP_PATH": 1},
        "missing-path.json": {"TE.OWNERSHIP_COVERAGE": 1, "TE.OWNERSHIP_PATH": 1},
        "wrong-entry.json": {"TE.OWNERSHIP_COVERAGE": 1, "TE.OWNERSHIP_ENTRY": 1},
        "duplicate-path.json": {"TE.DUPLICATE_OWNERSHIP_PATH": 1},
        "wrong-mode.json": {"TE.OWNERSHIP_COVERAGE": 1, "TE.OWNERSHIP_MODE": 1},
        "wrong-class.json": {"TE.EVIDENCE_CLASS": 1, "TE.OWNERSHIP_COVERAGE": 1},
        "wrong-sut.json": {"TE.OWNERSHIP_COVERAGE": 1, "TE.OWNERSHIP_SUT": 1},
        "wrong-artifact.json": {"TE.OWNERSHIP_ARTIFACT": 1, "TE.OWNERSHIP_COVERAGE": 1},
        "unexpected-key.json": {
            "TE.OWNERSHIP_COVERAGE": 1,
            "TE.OWNERSHIP_KEYS": 1,
            "TE.OWNERSHIP_SUT": 1,
        },
    }
    for name, codes in ownership_expectations.items():
        controlled_cases.append(
            (
                f"ownership-{name}",
                [
                    class_path,
                    "--ownership",
                    f"harness/pi/fixtures/python-test-evidence/ownership-invalid/{name}",
                ],
                1,
                codes,
                {},
            )
        )
    migration_expectations = {
        "valid.json": (0, {}),
        "invalid-json.txt": (1, {"TE.MIGRATION_INPUT": 1}),
        "duplicate.json": (
            1,
            {"TE.MIGRATION_INCOMPLETE": 1, "TE.MIGRATION_ONE_TO_ONE": 1},
        ),
        "incomplete.json": (1, {"TE.MIGRATION_INCOMPLETE": 1}),
        "unexpected.json": (1, {"TE.MIGRATION_INPUT": 1}),
    }
    for name, (exit_status, codes) in migration_expectations.items():
        controlled_cases.append(
            (
                f"migration-{name}",
                [
                    class_path,
                    "--ownership",
                    class_ownership,
                    "--migration-map",
                    f"harness/pi/fixtures/python-test-evidence/migrations/{name}",
                ],
                exit_status,
                codes,
                {"test_functions": 1, "unique_evidence_owners": 1},
            )
        )

    for (
        case_id,
        arguments,
        expected_exit,
        expected_codes,
        expected_counts,
    ) in controlled_cases:
        result = subprocess.run(
            validator_command + arguments,
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError:
            issues.append(f"{case_id}: validator emitted invalid JSON")
            continue
        actual_codes = Counter(
            item.get("code")
            for item in payload.get("findings", [])
            if isinstance(item, dict)
        )
        if (
            result.returncode != expected_exit
            or dict(actual_codes) != expected_codes
            or payload.get("status") != ("PASS" if expected_exit == 0 else "FAIL")
        ):
            issues.append(
                f"{case_id}: exact result mismatch exit={result.returncode} codes={dict(actual_codes)}"
            )
        counts = payload.get("counts", {})
        required_count_fields = {
            "static_collected_parameter_cases",
            "unique_evidence_owners",
            "test_functions",
            "helper_functions",
            "class_owned_modules",
            "artifact_owned_modules",
            "evidence_class_modules",
        }
        if not required_count_fields <= set(counts):
            issues.append(f"{case_id}: missing structured count fields")
        for field, expected_value in expected_counts.items():
            if counts.get(field) != expected_value:
                issues.append(
                    f"{case_id}: count {field} expected {expected_value!r}, got {counts.get(field)!r}"
                )

    route_command = [
        "python",
        ".pi/skills/validate_harness.py",
        "--repository-root",
        str(ROOT),
        "--route-config",
        str(ROOT / "harness/local/validation-route.json"),
    ]
    route_result = subprocess.run(
        route_command, cwd=ROOT, text=True, capture_output=True, check=False
    )
    try:
        route_payload = json.loads(route_result.stdout)
    except json.JSONDecodeError:
        route_payload = {}
    if (
        route_result.returncode != 0
        or route_payload.get("status") != "PASS"
        or route_payload.get("selected_route") != "local"
    ):
        issues.append("maintained selected local validation route does not PASS")

    print(
        json.dumps(
            {
                "schema_version": 1,
                "task_id": "TEST-EVIDENCE-SKILL-1",
                "status": "PASS" if not issues else "FAIL",
                "issues": issues,
            },
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
