#!/usr/bin/env -S python/.venv/bin/python
"""Validate the repository-local skill capability inventory.

This control-plane validator checks filesystem inventory, skill frontmatter
identity, exact content hashes, one primary CPN classification per skill,
required invocation-contract fields, requested review/tool-block ownership, and
accepted evidence-authority boundaries. It does not execute skills or judge
scientific correctness.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
INVENTORY_PATH = ROOT / ".pi" / "skills" / "skill-capability-inventory.json"
SKILL_ROOTS = (ROOT / ".pi" / "skills", ROOT / ".agents" / "skills")
CLASSIFICATIONS = {
    "DIRECTLY_COMPOSABLE",
    "COMPOSABLE_AFTER_HARDENING",
    "ADVISORY_REVIEW_ONLY",
    "HUMAN_DECISION_SUPPORT",
    "NOT_CPN_SUITABLE",
    "DEFERRED",
}
REQUIRED_SKILL_FIELDS = {
    "skill_name",
    "path",
    "content_sha256",
    "trigger_description",
    "current_consumers",
    "authoritative_references",
    "inputs",
    "outputs",
    "side_effects",
    "external_tools_used",
    "deterministic_scripts_used",
    "authorization_requirements",
    "failure_behavior",
    "retry_behavior",
    "idempotency",
    "evidence_classification",
    "current_validation_status",
    "primary_classification",
    "hardening_applied",
    "stop_condition",
}
REQUIRED_REVIEW_BLOCKS = {
    "ArchitectureContractReviewBlock",
    "SourceDocumentationReviewBlock",
    "TestDocumentationReviewBlock",
    "VVUQClassificationReviewBlock",
    "PublicApiInventoryReviewBlock",
    "StaticDependencyDirectionReviewBlock",
    "SchemaFixtureReviewBlock",
    "NumericalEvidenceReviewBlock",
    "IntegrationReviewBlock",
    "StalePathReviewBlock",
    "CheckpointReviewBlock",
    "TaskSelectionReviewBlock",
    "DocumentationSynchronizationReviewBlock",
}
REQUIRED_TOOL_BLOCKS = {
    "PytestBlock",
    "RuffFormatBlock",
    "RuffLintBlock",
    "MypyBlock",
    "SphinxWarningsAsErrorsBlock",
    "JsonSchemaValidationBlock",
    "ChecksumValidationBlock",
    "GitDiffCheckBlock",
    "HarnessValidationRouteBlock",
    "EvidenceIdentifierAuditBlock",
    "CheckpointSchemaValidationBlock",
    "StaticDependencyDirectionToolBlock",
    "SkillCapabilityInventoryValidationBlock",
}
REQUIRED_TOKEN_FIELDS = {
    "SkillIdentityToken": {"stable_skill_name", "source_path", "content_sha256"},
    "SkillCapabilityToken": {
        "supported_capability",
        "invocation_contract_version",
        "required_references",
        "permitted_side_effect_class",
        "required_authorization",
        "validation_status",
    },
    "SkillInvocationRequestToken": {
        "request_identity",
        "requested_capability",
        "task_id",
        "immutable_artifact_references",
        "expected_output_schema",
        "evidence_classification",
        "permitted_mutation_scope",
        "termination_policy",
        "parent_workflow_id",
        "attempt_id",
        "retry_authorization_identity_or_policy",
    },
    "SkillInvocationResultToken": {
        "request_identity",
        "task_id",
        "parent_workflow_id",
        "attempt_id",
        "skill_identity",
        "skill_content_sha256",
        "input_artifact_identities",
        "produced_artifacts",
        "structured_findings",
        "deterministic_commands",
        "command_results",
        "mutation_summary",
        "warnings",
        "failure_classification",
        "completion_status",
    },
    "SkillInvocationFailureToken": {
        "request_identity",
        "task_id",
        "parent_workflow_id",
        "attempt_id",
        "retry_authorization_identity_or_policy",
        "failure_classification",
        "partial_effects",
        "retained_findings",
        "retry_eligibility",
    },
    "SkillReviewFindingSetToken": {
        "review_scope",
        "finding_ids",
        "severity",
        "file_line_evidence",
        "recommendations",
        "unresolved_human_decisions",
    },
    "DeterministicToolResultToken": {
        "tool_identity",
        "tool_version",
        "command",
        "environment_identity",
        "input_artifact_identities",
        "exit_status",
        "stdout_stderr_artifacts",
        "completion_status",
    },
    "ParentVerificationToken": {
        "required_evidence_inventory",
        "verified_result_identities",
        "missing_or_rejected_evidence",
        "scope",
        "completion_status",
    },
    "HumanAcceptanceResultToken": {
        "request_identity",
        "task_id",
        "human_response_artifact",
        "normalized_decision",
        "authorized_scope",
        "record_paths",
        "completion_status",
    },
}
REQUIRED_REVIEW_FIELDS = {"block", "kind", "evidence_owner", "result", "authority"}
REQUIRED_TOOL_FIELDS = {
    "block",
    "command",
    "evidence_owner",
    "classification",
    "current_status",
}
EXPECTED_SKILL_NAMES = {
    "graphify",
    "inspect-task-state",
    "resolve-human-checkpoint",
    "recommend-next-task",
    "design-data-action-objects",
    "develop-architecture-decision",
    "develop-harness-resources",
    "develop-operator-records",
    "develop-python-test-evidence",
    "document-python-research-software",
}


def load_json(path: Path) -> Any:
    """Load one UTF-8 JSON artifact."""

    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    """Return the exact SHA-256 identity of one skill file."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


def frontmatter_name(path: Path) -> str | None:
    """Read the exact top-level name from simple skill YAML frontmatter."""

    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if match is None:
        return None
    for line in match.group(1).splitlines():
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip("\"'")
    return None


def actual_skill_paths() -> set[str]:
    """Return every repository-local SKILL.md path relative to repository root."""

    paths: set[str] = set()
    for root in SKILL_ROOTS:
        for path in root.rglob("SKILL.md"):
            paths.add(str(path.relative_to(ROOT)))
    return paths


def require_nonempty_list(
    record: dict[str, Any], field: str, errors: list[str]
) -> None:
    """Require a nonempty list field on an inventory record."""

    value = record.get(field)
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(item, str) or not item for item in value)
    ):
        errors.append(
            f"{record.get('skill_name', '<unknown>')}: {field} must be a nonempty string list"
        )


def main() -> int:
    """Validate all deterministic skill-capability inventory invariants."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inventory",
        type=Path,
        default=INVENTORY_PATH,
        help="inventory JSON to validate; defaults to the repository artifact",
    )
    args = parser.parse_args()
    inventory = load_json(args.inventory)
    errors: list[str] = []

    if inventory.get("schema_version") != 1:
        errors.append("schema_version must equal 1")

    boundary = inventory.get("cpn_boundary", {})
    if "never invoked or loaded by guards" not in boundary.get("guard_policy", ""):
        errors.append(
            "CPN boundary must prohibit skill invocation and loading in guards"
        )
    if "outside guard evaluation" not in boundary.get("invocation_policy", ""):
        errors.append("CPN boundary must require external invocation outside guards")
    retry_policy = boundary.get("retry_policy", "")
    if "new attempt identity" not in retry_policy:
        errors.append(
            "CPN retry policy must retain history through new attempt identities"
        )
    if "authorization" not in retry_policy:
        errors.append("CPN retry policy must require immutable retry authorization")

    tokens = inventory.get("token_responsibilities", {})
    missing_tokens = set(REQUIRED_TOKEN_FIELDS) - set(tokens)
    unexpected_tokens = set(tokens) - set(REQUIRED_TOKEN_FIELDS)
    if missing_tokens:
        errors.append(f"missing token responsibilities: {sorted(missing_tokens)}")
    if unexpected_tokens:
        errors.append(f"unexpected token responsibilities: {sorted(unexpected_tokens)}")
    for token_name, required_fields in REQUIRED_TOKEN_FIELDS.items():
        actual_fields = tokens.get(token_name)
        if not isinstance(actual_fields, list) or not actual_fields:
            errors.append(f"{token_name}: responsibility list must be nonempty")
            continue
        if any(not isinstance(field, str) or not field for field in actual_fields):
            errors.append(
                f"{token_name}: every responsibility must be a nonempty string"
            )
            continue
        actual_field_set = set(actual_fields)
        if len(actual_fields) != len(actual_field_set):
            errors.append(f"{token_name}: duplicate responsibility fields")
        if actual_field_set != required_fields:
            errors.append(
                f"{token_name}: responsibility mismatch: "
                f"missing={sorted(required_fields - actual_field_set)} "
                f"unexpected={sorted(actual_field_set - required_fields)}"
            )

    skill_records = inventory.get("skills")
    if not isinstance(skill_records, list):
        errors.append("skills must be a list")
        skill_records = []

    inventory_paths: set[str] = set()
    inventory_names: set[str] = set()
    for record in skill_records:
        if not isinstance(record, dict):
            errors.append("each skill record must be an object")
            continue
        missing_fields = REQUIRED_SKILL_FIELDS - set(record)
        if missing_fields:
            errors.append(
                f"{record.get('skill_name', '<unknown>')}: missing fields {sorted(missing_fields)}"
            )
        name = record.get("skill_name")
        relative = record.get("path")
        classification = record.get("primary_classification")
        if not isinstance(name, str) or not name:
            errors.append("skill_name must be a nonempty string")
            continue
        if name in inventory_names:
            errors.append(f"duplicate skill name: {name}")
        inventory_names.add(name)
        if classification not in CLASSIFICATIONS:
            errors.append(f"{name}: invalid primary classification {classification!r}")
        if classification == "COMPOSABLE_AFTER_HARDENING":
            require_nonempty_list(record, "remaining_hardening", errors)
        if not isinstance(relative, str):
            errors.append(f"{name}: path must be a string")
            continue
        if relative in inventory_paths:
            errors.append(f"duplicate skill path: {relative}")
        inventory_paths.add(relative)
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"{name}: missing skill file {relative}")
            continue
        if frontmatter_name(path) != name:
            errors.append(f"{name}: frontmatter name does not match {relative}")
        expected_hash = record.get("content_sha256")
        if (
            not isinstance(expected_hash, str)
            or re.fullmatch(r"[0-9a-f]{64}", expected_hash) is None
        ):
            errors.append(
                f"{name}: content_sha256 must be 64 lowercase hexadecimal digits"
            )
        actual_hash = sha256(path)
        if expected_hash != actual_hash:
            errors.append(
                f"{name}: content hash mismatch: inventory={expected_hash} actual={actual_hash}"
            )
        for field in (
            "current_consumers",
            "authoritative_references",
            "inputs",
            "outputs",
            "side_effects",
            "external_tools_used",
            "deterministic_scripts_used",
            "hardening_applied",
        ):
            require_nonempty_list(record, field, errors)
        for consumer in record.get("current_consumers", []):
            consumer_path = ROOT / consumer
            if not isinstance(consumer, str) or not consumer_path.exists():
                errors.append(f"{name}: missing concrete consumer path {consumer!r}")
                continue
            if consumer_path.is_file() and name not in consumer_path.read_text(
                encoding="utf-8"
            ):
                errors.append(
                    f"{name}: consumer path does not reference skill: {consumer}"
                )
        for reference in record.get("authoritative_references", []):
            if not isinstance(reference, str) or not (ROOT / reference).exists():
                errors.append(f"{name}: missing authoritative reference {reference!r}")
        for field in (
            "trigger_description",
            "authorization_requirements",
            "failure_behavior",
            "retry_behavior",
            "idempotency",
            "evidence_classification",
            "current_validation_status",
            "stop_condition",
        ):
            if not isinstance(record.get(field), str) or not record[field].strip():
                errors.append(f"{name}: {field} must be a nonempty string")

    if inventory_names != EXPECTED_SKILL_NAMES:
        errors.append(
            "skill name inventory mismatch: "
            f"missing={sorted(EXPECTED_SKILL_NAMES - inventory_names)} "
            f"unexpected={sorted(inventory_names - EXPECTED_SKILL_NAMES)}"
        )
    actual_paths = actual_skill_paths()
    if inventory_paths != actual_paths:
        errors.append(
            "skill path inventory mismatch: "
            f"missing={sorted(actual_paths - inventory_paths)} "
            f"unexpected={sorted(inventory_paths - actual_paths)}"
        )

    review_blocks = inventory.get("cpn_review_blocks", [])
    review_name_list = [
        item.get("block") for item in review_blocks if isinstance(item, dict)
    ]
    review_names = set(review_name_list)
    if len(review_name_list) != len(review_names):
        errors.append("duplicate CPN review block names")
    if review_names != REQUIRED_REVIEW_BLOCKS:
        errors.append(
            "CPN review block mismatch: "
            f"missing={sorted(REQUIRED_REVIEW_BLOCKS - review_names)} "
            f"unexpected={sorted(review_names - REQUIRED_REVIEW_BLOCKS)}"
        )
    for item in review_blocks:
        if not isinstance(item, dict):
            errors.append(f"invalid CPN review block record: {item!r}")
            continue
        missing_fields = REQUIRED_REVIEW_FIELDS - set(item)
        unexpected_fields = set(item) - REQUIRED_REVIEW_FIELDS
        wrong_types = [
            field
            for field in REQUIRED_REVIEW_FIELDS & set(item)
            if not isinstance(item[field], str) or not item[field]
        ]
        if missing_fields or unexpected_fields or wrong_types:
            errors.append(
                f"{item.get('block', '<unknown>')}: invalid review block: "
                f"missing={sorted(missing_fields)} "
                f"unexpected={sorted(unexpected_fields)} "
                f"non_string_or_empty={sorted(wrong_types)}"
            )
        if item.get("kind") not in {
            "agent_review",
            "mixed",
            "human_decision_support",
        }:
            errors.append(f"{item.get('block', '<unknown>')}: invalid review kind")

    tool_blocks = inventory.get("deterministic_tool_blocks", [])
    tool_name_list = [
        item.get("block") for item in tool_blocks if isinstance(item, dict)
    ]
    tool_names = set(tool_name_list)
    if len(tool_name_list) != len(tool_names):
        errors.append("duplicate deterministic tool block names")
    if tool_names != REQUIRED_TOOL_BLOCKS:
        errors.append(
            "deterministic tool block mismatch: "
            f"missing={sorted(REQUIRED_TOOL_BLOCKS - tool_names)} "
            f"unexpected={sorted(tool_names - REQUIRED_TOOL_BLOCKS)}"
        )
    for item in tool_blocks:
        if not isinstance(item, dict):
            errors.append(f"invalid deterministic tool block record: {item!r}")
            continue
        missing_fields = REQUIRED_TOOL_FIELDS - set(item)
        unexpected_fields = set(item) - REQUIRED_TOOL_FIELDS
        wrong_types = [
            field
            for field in REQUIRED_TOOL_FIELDS & set(item)
            if not isinstance(item[field], str) or not item[field]
        ]
        if missing_fields or unexpected_fields or wrong_types:
            errors.append(
                f"{item.get('block', '<unknown>')}: invalid tool block: "
                f"missing={sorted(missing_fields)} "
                f"unexpected={sorted(unexpected_fields)} "
                f"non_string_or_empty={sorted(wrong_types)}"
            )

    evidence_authority = inventory.get("evidence_authority", {})
    if "human" not in evidence_authority.get("human_acceptance_result", "").lower():
        errors.append("human acceptance authority must remain explicit")
    if "not an oracle" not in evidence_authority.get("prohibited_inference", ""):
        errors.append("inventory must prohibit agreement-based AI oracle claims")

    print(f"skill_records={len(skill_records)}")
    print(f"filesystem_skills={len(actual_paths)}")
    print(f"cpn_review_blocks={len(review_names)}")
    print(f"deterministic_tool_blocks={len(tool_names)}")
    print(f"validation_errors={len(errors)}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
