#!/usr/bin/env python3
"""Dependency-free deterministic textual-resource completion validator.

The validator uses only the standard library for its own implementation.  When
``jsonschema`` is present in the repository's declared test environment it also
performs Draft 2020-12 meta-schema and fixture validation; absence is reported
as a failed gate rather than causing an import-time failure.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import tempfile
import unicodedata
import warnings
from pathlib import Path
from typing import Any, Iterable

PI = Path(__file__).resolve().parents[1]
LOCAL = PI.parent / "local"
HARNESS_ROOT = PI.parent
DRAFT = "https://json-schema.org/draft/2020-12/schema"
PUBLIC_RECORDS = (
    "agent-descriptor-view", "artifact-identity", "chain-view",
    "checkpoint-record", "checksum-entry", "checksum-manifest",
    "evidence-identifier-occurrence", "ownership-manifest-view",
    "ownership-scope", "project-profile", "resource-manifest",
    "resource-reference", "skill-descriptor", "task-reference",
    "validation-issue", "validation-result",
)
RESOURCE_KINDS = {"skill", "reference", "schema", "template", "profile",
                  "manifest", "script", "documentation"}
CANONICAL_SKILLS = {
    "develop-architecture-decision": "pih.skill.develop-architecture-decision.v1",
    "develop-python-test-evidence": "pih.skill.develop-python-test-evidence.v1",
    "document-python-research-software": "pih.skill.document-python-research-software.v1",
}
REQUIRED_RESOLUTION_CASES = {
    "dependency-cycle", "duplicate-resource-id", "duplicate-resource-path",
    "generic-to-local-dependency", "incompatible-format-version",
    "local-overlay-duplicate-id", "local-overlay-duplicate-path",
    "manifest-profile-incompatible", "missing-dependency", "self-dependency",
    "resolve-generic-leaf", "resolve-local-extension", "resource-file-missing",
    "resource-not-found", "resource-not-file", "resource-symlink",
    "resource-hash-mismatch", "resource-case-mismatch",
}


class Report:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.passes: list[str] = []

    def check(self, condition: bool, gate: str, detail: str) -> bool:
        if condition:
            self.passes.append(gate)
            return True
        self.failures.append(f"{gate}: {detail}")
        return False

    def fail(self, gate: str, detail: str) -> None:
        self.failures.append(f"{gate}: {detail}")


R = Report()


def rel(path: Path) -> str:
    try:
        return path.relative_to(HARNESS_ROOT).as_posix()
    except ValueError:
        return str(path)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def pairs_no_duplicates(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"),
                          object_pairs_hook=pairs_no_duplicates)
    except Exception as exc:
        R.fail("json.parse", f"{rel(path)}: {exc}")
        return None


def strictly_sorted(values: Iterable[Any]) -> bool:
    sequence = list(values)
    return all(sequence[i] < sequence[i + 1] for i in range(len(sequence) - 1))


def valid_lexical_path(value: Any) -> tuple[bool, str | None]:
    if not isinstance(value, str):
        return False, "PIH.WIRE.INVALID_TYPE"
    if not value:
        return False, "PIH.PATH.EMPTY"
    if unicodedata.normalize("NFC", value) != value:
        return False, "PIH.PATH.NONCANONICAL_UNICODE"
    if value.startswith("/"):
        return False, "PIH.PATH.ABSOLUTE"
    if re.match(r"^[A-Za-z]:", value) or value.startswith(("\\\\", "//")):
        return False, "PIH.PATH.WINDOWS_SYNTAX" if not value.startswith("//") else "PIH.PATH.ABSOLUTE"
    if "\\" in value:
        # Device and UNC spellings take precedence over the generic character error.
        if value.startswith(("\\\\?\\", "\\\\.\\", "\\\\")):
            return False, "PIH.PATH.WINDOWS_SYNTAX"
        return False, "PIH.PATH.INVALID_CHARACTER"
    if value.endswith("/") or "//" in value or any(x in ("", ".", "..") for x in value.split("/")):
        return False, "PIH.PATH.INVALID_SEGMENT"
    for char in value:
        code = ord(char)
        if code <= 0x1F or 0x7F <= code <= 0x9F or code in (0x2028, 0x2029) or 0xD800 <= code <= 0xDFFF:
            return False, "PIH.PATH.INVALID_CHARACTER"
    return True, None


def complete_file_gate() -> None:
    """Ensure every completed textual file is readable and every JSON file parses."""
    files = sorted(p for root in (PI, LOCAL) for p in root.rglob("*") if p.is_file())
    R.check(bool(files), "files.inventory-nonempty", "no textual resource files found")
    for path in files:
        R.check(not path.is_symlink(), "files.no-symlinks", f"{rel(path)} is a symlink")
        if path.suffix == ".json":
            load_json(path)
        elif path.suffix in {".md", ".py", ".txt"}:
            try:
                path.read_text(encoding="utf-8")
            except Exception as exc:
                R.fail("files.utf8", f"{rel(path)}: {exc}")


def schema_and_fixture_gate() -> tuple[dict[str, Any], dict[str, Any]]:
    schema_paths = sorted((PI / "schemas").rglob("*.schema.json"))
    schemas = {path: load_json(path) for path in schema_paths}
    ids = [schema.get("$id") for schema in schemas.values() if isinstance(schema, dict)]
    R.check(all(isinstance(s, dict) and s.get("$schema") == DRAFT and
                isinstance(s.get("$id"), str) for s in schemas.values()),
            "schema.draft-and-identity", "every schema must declare Draft 2020-12 and an absolute $id")
    R.check(len(ids) == len(set(ids)), "schema.identity-unique", "schema $id values are not unique")
    record_names = tuple(path.name.removesuffix(".schema.json") for path in
                         sorted((PI / "schemas/records").glob("*.schema.json"))
                         if path.name != "common.schema.json")
    R.check(record_names == PUBLIC_RECORDS, "schema.public-record-set",
            f"expected exactly 16 records {PUBLIC_RECORDS}, got {record_names}")
    expected_record_ids = {
        f"https://schemas.pi-harness.org/v1/records/{name}.schema.json"
        for name in PUBLIC_RECORDS
    }
    actual_record_ids = {
        schemas[PI / f"schemas/records/{name}.schema.json"].get("$id")
        for name in PUBLIC_RECORDS
        if isinstance(schemas.get(PI / f"schemas/records/{name}.schema.json"), dict)
    }
    R.check(actual_record_ids == expected_record_ids, "schema.public-record-identities",
            f"missing={sorted(expected_record_ids-actual_record_ids)}, extra={sorted(actual_record_ids-expected_record_ids)}")
    index = load_json(PI / "fixtures/fixture-index.json")
    R.check(isinstance(index, dict) and tuple(index.get("public_json_record_schemas", ())) == PUBLIC_RECORDS,
            "fixture.public-record-index", "fixture index must name the exact closed 16-record set in order")

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            import jsonschema  # type: ignore
            from jsonschema import Draft202012Validator, FormatChecker, RefResolver  # type: ignore
    except Exception as exc:
        R.fail("schema.jsonschema-environment", f"jsonschema Draft 2020-12 support unavailable: {exc}")
        return schemas, {}

    checker = FormatChecker()
    checker.checks("nfc")(lambda value: isinstance(value, str) and unicodedata.normalize("NFC", value) == value)
    store = {schema["$id"]: schema for schema in schemas.values() if isinstance(schema, dict) and "$id" in schema}
    for path, schema in schemas.items():
        if not isinstance(schema, dict):
            continue
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:
            R.fail("schema.meta-validation", f"{rel(path)}: {exc}")
    validators: dict[str, Any] = {}
    for name in PUBLIC_RECORDS:
        path = PI / f"schemas/records/{name}.schema.json"
        schema = schemas.get(path)
        if isinstance(schema, dict):
            validators[name] = Draft202012Validator(
                schema, resolver=RefResolver.from_schema(schema, store=store), format_checker=checker)
    manifest_validator = validators.get("resource-manifest")
    manifest_fixture = load_json(PI / "fixtures/valid/resource-manifest.json")
    if manifest_validator is not None and isinstance(manifest_fixture, dict):
        duplicate_candidate = dict(manifest_fixture)
        duplicate_candidate["resources"] = list(manifest_fixture["resources"]) * 2
        R.check(not list(manifest_validator.iter_errors(duplicate_candidate)),
                "schema.resource-manifest-preserves-exact-duplicates",
                "resource manifest schema must represent exact duplicate entries for relational validation")
    for name in PUBLIC_RECORDS:
        validator = validators.get(name)
        valid = load_json(PI / f"fixtures/valid/{name}.json")
        invalid = load_json(PI / f"fixtures/invalid/schema/{name}.json")
        if validator is None or valid is None or invalid is None:
            continue
        errors = list(validator.iter_errors(valid))
        R.check(not errors, "fixture.valid-schema", f"valid/{name}.json rejected: {errors[0].message if errors else ''}")
        errors = list(validator.iter_errors(invalid))
        R.check(bool(errors), "fixture.invalid-schema", f"invalid/schema/{name}.json was accepted")
    return schemas, validators


def semantic_invariant_gate(validators: dict[str, Any]) -> None:
    """Check the indexed structural-versus-cross-value invariant boundary."""
    index = load_json(PI / "fixtures/fixture-index.json") or {}
    oracle_text = index.get("semantic_invariant_oracle")
    ok, _ = valid_lexical_path(oracle_text)
    if not ok:
        R.fail("semantic-invariant.index", "fixture index has no valid semantic invariant oracle path")
        return
    oracle_path = PI / "fixtures" / oracle_text
    oracle = load_json(oracle_path) or {}
    cases = oracle.get("cases", [])
    R.check(len(cases) == 7 and len({x.get("case_id") for x in cases}) == 7,
            "semantic-invariant.case-set", "oracle must contain exactly seven unique cases")
    expected_boundary = {"reject": 4, "accept": 3}
    actual_boundary = {key: sum(x.get("schema_expectation") == key for x in cases)
                       for key in expected_boundary}
    R.check(actual_boundary == expected_boundary, "semantic-invariant.boundary-counts",
            f"expected {expected_boundary}, got {actual_boundary}")
    for case in cases:
        case_id = case.get("case_id")
        kind = case.get("record_kind")
        name = re.sub(r"(?<!^)(?=[A-Z])", "-", kind).lower() if isinstance(kind, str) else ""
        validator = validators.get(name)
        instance_text = case.get("instance_path")
        path_ok, _ = valid_lexical_path(instance_text)
        if validator is None or not path_ok:
            R.fail("semantic-invariant.case-input", f"{case_id}: invalid kind or path")
            continue
        instance = load_json(oracle_path.parent / instance_text)
        schema_accepts = instance is not None and not list(validator.iter_errors(instance))
        expected_schema_accepts = case.get("schema_expectation") == "accept"
        R.check(schema_accepts == expected_schema_accepts, "semantic-invariant.schema-boundary",
                f"{case_id}: expected schema {case.get('schema_expectation')}")
        semantic = case.get("semantic_validator_expectation", {})
        if not expected_schema_accepts:
            R.check(semantic == {"stage": "not_run"}, "semantic-invariant.schema-short-circuit",
                    f"{case_id}: rejected schema case must not run semantics")
            continue
        if kind == "ResourceReference":
            self_edge = instance.get("resource_id") in instance.get("dependency_ids", [])
            valid_boundary = (self_edge and semantic.get("stage") == "DeserializeJsonRecord" and
                              semantic.get("status") == "PASS" and semantic.get("issue_code") is None and
                              semantic.get("next_stage") == "ValidateResourceManifest" and
                              semantic.get("next_status") == "FAIL" and
                              semantic.get("next_issue_code") == "PIH.RESOURCE.DEPENDENCY_CYCLE")
        elif kind == "TaskReference":
            invalid = instance.get("task_id") in instance.get("task_prerequisite_ids", [])
            valid_boundary = (invalid and semantic.get("stage") == "DeserializeJsonRecord" and
                              semantic.get("status") == "FAIL" and
                              semantic.get("issue_code") == "PIH.WIRE.INVALID_VALUE")
        elif kind == "ChainView":
            task_ids = {task.get("task_id") for task in instance.get("tasks", [])}
            invalid = not set(instance.get("explicitly_activated_task_ids", [])) <= task_ids
            valid_boundary = (invalid and semantic.get("stage") == "DeserializeJsonRecord" and
                              semantic.get("status") == "FAIL" and
                              semantic.get("issue_code") == "PIH.WIRE.INVALID_VALUE")
        else:
            valid_boundary = False
        R.check(valid_boundary, "semantic-invariant.cross-value-boundary",
                f"{case_id}: semantic stage expectation or deterministic check differs")


def manifest_problems(manifest: dict[str, Any], generic: dict[str, Any] | None,
                      supported: set[tuple[str, int]] | None) -> list[str]:
    problems: list[str] = []
    resources = manifest.get("resources", [])
    ids = [x.get("resource_id") for x in resources]
    paths = [x.get("path") for x in resources]
    keys = [(x.get("resource_id"), x.get("path"), x.get("resource_kind"),
             x.get("format_version"), x.get("content_identity", {}).get("algorithm"),
             x.get("content_identity", {}).get("digest"), tuple(x.get("dependency_ids", [])))
            for x in resources]
    if keys != sorted(keys): problems.append("resources are not complete-key canonically ordered")
    if len(ids) != len(set(ids)): problems.append("duplicate resource ID")
    if len(paths) != len(set(paths)): problems.append("duplicate resource path")
    if manifest.get("layer") == "generic" and manifest.get("extends_manifest_id") is not None:
        problems.append("generic manifest extends another manifest")
    if manifest.get("layer") == "local" and (not generic or manifest.get("extends_manifest_id") != generic.get("manifest_id")):
        problems.append("local manifest does not extend the supplied generic manifest")
    generic_ids = {x.get("resource_id") for x in (generic or {}).get("resources", [])}
    generic_paths = {x.get("path") for x in (generic or {}).get("resources", [])}
    if manifest.get("layer") == "local" and (set(ids) & generic_ids or set(paths) & generic_paths):
        problems.append("local overlay replaces a generic ID or path")
    available = set(ids) | (generic_ids if manifest.get("layer") == "local" else set())
    graph: dict[str, list[str]] = {}
    for item in resources:
        rid = item.get("resource_id")
        deps = item.get("dependency_ids", [])
        if not strictly_sorted(deps): problems.append(f"{rid}: dependencies not strictly sorted")
        if rid in deps: problems.append(f"{rid}: self dependency")
        if any(dep not in available for dep in deps): problems.append(f"{rid}: missing dependency")
        if item.get("resource_kind") not in RESOURCE_KINDS: problems.append(f"{rid}: unsupported kind")
        if supported is not None and (item.get("resource_kind"), item.get("format_version")) not in supported:
            problems.append(f"{rid}: incompatible kind/version")
        graph[rid] = list(deps)
    visiting: set[str] = set(); visited: set[str] = set()
    def visit(node: str) -> None:
        if node in visiting:
            problems.append(f"dependency cycle at {node}"); return
        if node in visited: return
        visiting.add(node)
        for child in graph.get(node, []):
            if child in graph: visit(child)
        visiting.remove(node); visited.add(node)
    for rid in ids: visit(rid)
    return problems


def manifest_gate() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    generic = load_json(PI / "resource-manifest.json") or {}
    local = load_json(LOCAL / "resource-manifest.json") or {}
    profile_entries = [item for item in local.get("resources", [])
                       if str(item.get("path", "")).startswith("profiles/")]
    R.check(len(profile_entries) == 1, "manifest.local-profile-selection",
            "local manifest must declare exactly one project profile resource")
    profile = load_json(LOCAL / profile_entries[0]["path"]) if len(profile_entries) == 1 else {}
    profile = profile or {}
    supported = {tuple(x) for x in profile.get("supported_resource_formats", [])}
    for layer, root, manifest, base in (("generic", PI, generic, None), ("local", LOCAL, local, generic)):
        problems = manifest_problems(manifest, base, supported)
        R.check(not problems, f"manifest.{layer}-semantics", "; ".join(problems))
        declared_paths: set[str] = set()
        for item in manifest.get("resources", []):
            path_text = item.get("path")
            ok, _ = valid_lexical_path(path_text)
            if not ok:
                R.fail("manifest.resource-path", f"{item.get('resource_id')}: {path_text!r}")
                continue
            path = root / path_text
            declared_paths.add(path_text)
            if not path.is_file() or path.is_symlink():
                R.fail("manifest.resource-file", f"{rel(path)} is missing, non-file, or symlink")
                continue
            expected = item.get("content_identity", {}).get("digest")
            actual = sha256(path.read_bytes())
            R.check(expected == actual, "manifest.exact-byte-sha256",
                    f"{rel(path)} expected {expected}, actual {actual}")
        actual_owned = {p.relative_to(root).as_posix() for family in (root / "schemas", root / "skills")
                        if family.exists() for p in family.rglob("*") if p.is_file()}
        if layer == "local":
            actual_owned = {p.relative_to(root).as_posix() for family in
                            (root / "profiles", root / "extensions", root / "validation") if family.exists()
                            for p in family.rglob("*") if p.is_file() and "__pycache__" not in p.parts}
            if (root / "validation-route.json").is_file():
                actual_owned.add("validation-route.json")
        R.check(actual_owned == declared_paths, f"manifest.{layer}-declared-coverage",
                f"undeclared={sorted(actual_owned-declared_paths)}, stale={sorted(declared_paths-actual_owned)}")
    profile_id = profile.get("profile_id")
    R.check(generic.get("manifest_version") == 2 and
            local.get("manifest_version") == 2 and
            isinstance(profile_id, str) and profile_id.endswith(".profile.v2"),
            "manifest.naming-version-boundary",
            "naming correction requires generic/local manifest version 2 and profile instance v2")
    R.check(local.get("extends_manifest_id") == generic.get("manifest_id") and
            profile.get("generic_manifest_id") == generic.get("manifest_id") and
            profile.get("generic_manifest_version") == generic.get("manifest_version") and
            profile.get("local_manifest_id") == local.get("manifest_id") and
            profile.get("local_manifest_version") == local.get("manifest_version") and
            profile.get("overlay_policy") == "extend_only",
            "manifest.profile-binding", "profile does not exactly bind both manifests and extend_only policy")
    return generic, local, profile


def profile_gate(profile: dict[str, Any], generic: dict[str, Any], local: dict[str, Any]) -> None:
    sorted_fields = ("policy_reference_ids", "supported_resource_formats", "supported_skill_behaviors",
                     "evidence_namespace_rules", "protected_unowned_functions", "pytest_markers",
                     "checkpoint_unresolved_statuses", "checkpoint_resolved_statuses", "task_active_statuses",
                     "task_blocked_statuses", "task_satisfied_statuses", "local_extension_ids")
    for field in sorted_fields:
        values = profile.get(field, [])
        R.check(strictly_sorted(values), "profile.strict-order", f"{field} is not strictly sorted")
    namespaces = {x[0] for x in profile.get("evidence_namespace_rules", [])}
    markers = set(profile.get("pytest_markers", []))
    scopes: list[tuple[str, str, list[str]]] = []
    for rule in profile.get("evidence_scope_rules", []):
        scope, marker, allowed = rule
        scopes.append((scope.get("path"), marker, allowed))
        R.check(marker in markers and bool(allowed) and set(allowed) <= namespaces and strictly_sorted(allowed),
                "profile.evidence-policy", f"invalid scope policy for {scope.get('path')}")
    overlap = any(a == b or a.startswith(b + "/") or b.startswith(a + "/")
                  for i, (a, _, _) in enumerate(scopes) for b, _, _ in scopes[i + 1:])
    R.check(not overlap, "profile.scope-nonoverlap", "evidence scopes overlap")
    status_sets = [set(profile.get(x, [])) for x in ("checkpoint_unresolved_statuses",
                  "checkpoint_resolved_statuses")]
    task_sets = [set(profile.get(x, [])) for x in ("task_active_statuses", "task_blocked_statuses",
                 "task_satisfied_statuses")]
    R.check(not (status_sets[0] & status_sets[1]) and all(not (a & b) for i, a in enumerate(task_sets)
            for b in task_sets[i + 1:]), "profile.vocabulary-disjoint", "lifecycle vocabularies overlap")
    local_ids = {x["resource_id"] for x in local.get("resources", [])}
    all_ids = local_ids | {x["resource_id"] for x in generic.get("resources", [])}
    expected_extensions = set(profile.get("local_extension_ids", []))
    R.check(expected_extensions <= local_ids and set(profile.get("policy_reference_ids", [])) <=
            all_ids | {profile.get("filename_policy_id")}, "profile.explicit-local-policy",
            "local extension or policy reference is not explicitly declared")


def validation_route_gate(local: dict[str, Any]) -> None:
    """Require the repository-local live-consumer route to be explicit and safe."""
    route_path = LOCAL / "validation-route.json"
    route = load_json(route_path) or {}
    entries = [item for item in local.get("resources", [])
               if item.get("path") == "validation-route.json"]
    entry = entries[0] if len(entries) == 1 else {}
    project_profiles = [item for item in local.get("resources", [])
                        if str(item.get("path", "")).startswith("profiles/")]
    project_profile_id = (project_profiles[0].get("resource_id")
                          if len(project_profiles) == 1 else None)
    current_replay_ids = [item.get("resource_id") for item in local.get("resources", [])
                          if item.get("path") == "validation/replay_current_validators.py"]
    R.check(
        set(route) == {"rollback_route", "route", "schema_version"}
        and route.get("schema_version") == 1
        and route.get("route") in {"legacy", "local"}
        and route.get("rollback_route") == "legacy",
        "route.explicit-maintained-route",
        "validation route must be a closed schema-version-1 legacy/local route with legacy rollback",
    )
    R.check(
        len(entries) == 1
        and entry.get("resource_kind") == "profile"
        and entry.get("format_version") == 1
        and len(current_replay_ids) == 1
        and entry.get("dependency_ids") == sorted([project_profile_id, current_replay_ids[0]]),
        "route.manifest-identity",
        "validation route resource identity or dependency is invalid",
    )


def skill_gate(generic: dict[str, Any], profile: dict[str, Any]) -> None:
    resources = {x["resource_id"]: x for x in generic.get("resources", [])}
    supported = {tuple(x) for x in profile.get("supported_skill_behaviors", [])}
    for skill_id, resource_id in CANONICAL_SKILLS.items():
        descriptor = load_json(PI / f"skills/{skill_id}/descriptor.json") or {}
        R.check(descriptor.get("skill_id") == skill_id and
                descriptor.get("entry_resource_id") == resource_id and
                descriptor.get("behavior_version") == 1,
                "skill.canonical-identity", f"invalid canonical descriptor for {skill_id}")
        entry = resources.get(resource_id)
        required = descriptor.get("required_resource_ids", [])
        R.check(entry is not None and entry.get("resource_kind") == "skill", "skill.entry", f"{skill_id}: entry is missing or not skill")
        R.check(strictly_sorted(required) and resource_id in required,
                "skill.required-order", f"{skill_id}: required closure must be sorted and contain entry")
        closure: set[str] = set(); stack = [resource_id]
        while stack:
            rid = stack.pop()
            if rid in closure or rid not in resources: continue
            closure.add(rid); stack.extend(resources[rid].get("dependency_ids", []))
        R.check(set(required) == closure, "skill.closure", f"{skill_id}: declared={sorted(required)}, actual={sorted(closure)}")
        R.check((skill_id, descriptor.get("behavior_version")) in supported,
                "skill.behavior", f"profile does not support {skill_id} behavior")
        R.check(descriptor.get("authorization_policy_id") in set(profile.get("policy_reference_ids", [])) and
                descriptor.get("retry_policy") == "explicit_authorization_only" and
                descriptor.get("termination_policy") == "stop_after_result",
                "skill.policy", f"{skill_id}: authorization/retry/termination policy is incompatible")
    R.check(not (PI / "skills/document-research-python").exists(),
            "skill.no-stale-alias", "old generic skill directory still exists")
    R.check(not (PI / "skills/document-python-research-software/references/test-evidence-documentation.md").exists(),
            "skill.no-superseded-test-reference", "superseded test-evidence reference still exists")
    conventions = (PI / "skills/develop-python-test-evidence/references/test-evidence-conventions.md").read_text(encoding="utf-8")
    required_headings = ("Facet and represented meaning", "Intrinsic and cross-object scope", "VVUQ and scientific exclusions")
    R.check(all(heading in conventions for heading in required_headings),
            "skill.current-test-headings", "new test-evidence reference lacks maintained headings")
    R.check("superseded and prohibited" in conventions and
            "Evidence class and represented meaning" in conventions and
            "Owned contract, oracle, and scope" in conventions,
            "skill.superseded-heading-policy", "new reference does not expressly prohibit both superseded headings")


def classify_manifest_case(case: dict[str, Any],
                           fixture_base: Path | None = None) -> tuple[str, str | None]:
    generic = case.get("generic_manifest") or {}
    local = case.get("local_manifest")
    profile = case.get("profile") or {}
    gres = generic.get("resources", [])
    ids = [x.get("resource_id") for x in gres]; paths = [x.get("path") for x in gres]
    if len(ids) != len(set(ids)): return "FAIL", "PIH.RESOURCE.DUPLICATE_ID"
    if len(paths) != len(set(paths)): return "FAIL", "PIH.RESOURCE.DUPLICATE_PATH"
    if profile.get("generic_manifest_id") != generic.get("manifest_id") or profile.get("generic_manifest_version") != generic.get("manifest_version"):
        return "FAIL", "PIH.RESOURCE.MANIFEST_MISMATCH"
    local_ids: set[str] = set(); local_paths: set[str] = set()
    if local:
        if local.get("extends_manifest_id") != generic.get("manifest_id"): return "FAIL", "PIH.RESOURCE.MANIFEST_MISMATCH"
        lres = local.get("resources", [])
        local_id_list = [x.get("resource_id") for x in lres]
        local_path_list = [x.get("path") for x in lres]
        if len(local_id_list) != len(set(local_id_list)): return "FAIL", "PIH.RESOURCE.DUPLICATE_ID"
        if len(local_path_list) != len(set(local_path_list)): return "FAIL", "PIH.RESOURCE.DUPLICATE_PATH"
        local_ids = set(local_id_list); local_paths = set(local_path_list)
        if set(ids) & local_ids or set(paths) & local_paths: return "FAIL", "PIH.RESOURCE.OVERLAY_REPLACEMENT"
    supported = {tuple(x) for x in profile.get("supported_resource_formats", [])}
    all_ids = set(ids) | local_ids
    graph: dict[str, list[str]] = {}
    for item in gres + ((local or {}).get("resources", [])):
        rid = item.get("resource_id"); deps = item.get("dependency_ids", [])
        if (item.get("resource_kind"), item.get("format_version")) not in supported:
            return "FAIL", "PIH.RESOURCE.VERSION_INCOMPATIBLE"
        if any(dep not in all_ids for dep in deps): return "FAIL", "PIH.RESOURCE.MISSING_DEPENDENCY"
        graph[rid] = deps
    # A generic dependency naming a local identity is forbidden before generic missing-dependency reporting.
    if any(dep in local_ids for item in gres for dep in item.get("dependency_ids", [])):
        return "FAIL", "PIH.RESOURCE.GENERIC_TO_LOCAL_DEPENDENCY"
    def cyclic(node: str, active: set[str], done: set[str]) -> bool:
        if node in active: return True
        if node in done: return False
        active.add(node)
        if any(cyclic(x, active, done) for x in graph.get(node, [])): return True
        active.remove(node); done.add(node); return False
    done: set[str] = set()
    if any(cyclic(x, set(), done) for x in graph): return "FAIL", "PIH.RESOURCE.DEPENDENCY_CYCLE"
    rid = case.get("resource_id")
    if rid is None: return "PASS", None
    selected = next((x for x in gres + ((local or {}).get("resources", [])) if x.get("resource_id") == rid), None)
    if selected is None: return "FAIL", "PIH.RESOURCE.NOT_FOUND"
    layer = "generic" if selected in gres else "local"
    root_text = case.get(f"{layer}_root")
    base = fixture_base or PI / "fixtures/resource-resolution"
    root = base / root_text if isinstance(root_text, str) else None
    path_text = selected.get("path"); ok, code = valid_lexical_path(path_text)
    if not ok: return "FAIL", code
    if root is None or not root.is_dir(): return "FAIL", "PIH.PATH.ROOT_INVALID"
    candidate = root.joinpath(*path_text.split("/"))
    current = root
    for component in path_text.split("/"):
        if not current.is_dir(): break
        names = [p.name for p in current.iterdir()]
        if component not in names and component.casefold() in {n.casefold() for n in names}:
            return "FAIL", "PIH.PATH.CASE_MISMATCH"
        current /= component
        if current.is_symlink(): return "FAIL", "PIH.PATH.SYMLINK"
    try: candidate.resolve().relative_to(root.resolve())
    except ValueError: return "FAIL", "PIH.PATH.ESCAPE"
    if not candidate.exists(): return "FAIL", "PIH.PATH.MISSING"
    if not candidate.is_file(): return "FAIL", "PIH.PATH.NOT_FILE"
    if sha256(candidate.read_bytes()) != selected.get("content_identity", {}).get("digest"):
        return "FAIL", "PIH.ARTIFACT.HASH_MISMATCH"
    return "PASS", None


def evaluate_resolution_case(case: dict[str, Any], base: Path) -> tuple[str, str | None]:
    """Evaluate a case, realizing declarative setup only in a disposable tree."""
    setup = case.get("temporary_tree_setup")
    if setup is None:
        return classify_manifest_case(case, base)
    if not isinstance(setup, dict) or setup.get("base") != "roots":
        R.fail("resolution.temporary-setup", f"{case.get('case_id')}: unsupported base declaration")
        return "FAIL", None
    operations = setup.get("operations")
    if not isinstance(operations, list) or not operations:
        R.fail("resolution.temporary-setup", f"{case.get('case_id')}: operations must be nonempty")
        return "FAIL", None
    with tempfile.TemporaryDirectory(prefix="h3-resolution-") as temporary:
        disposable = Path(temporary)
        shutil.copytree(base / "roots", disposable / "roots")
        for operation in operations:
            if not isinstance(operation, dict) or operation.get("operation") != "create_symlink":
                R.fail("resolution.temporary-setup", f"{case.get('case_id')}: only create_symlink is permitted")
                return "FAIL", None
            link_text = operation.get("path")
            target = operation.get("target")
            ok, _ = valid_lexical_path(link_text)
            if not ok or not isinstance(target, str) or not target:
                R.fail("resolution.temporary-setup", f"{case.get('case_id')}: invalid symlink declaration")
                return "FAIL", None
            link = disposable / "roots" / link_text
            try:
                link.parent.mkdir(parents=True, exist_ok=True)
                os.symlink(target, link,
                           target_is_directory=bool(operation.get("target_is_directory", False)))
            except (OSError, NotImplementedError) as exc:
                R.fail("resolution.temporary-setup", f"{case.get('case_id')}: cannot create disposable symlink: {exc}")
                return "FAIL", None
        return classify_manifest_case(case, disposable)


def resolution_gate() -> None:
    base = PI / "fixtures/resource-resolution"
    oracle = load_json(base / "oracle-index.json") or {}
    oracle_cases = {x.get("case_id"): x for x in oracle.get("cases", [])}
    case_paths = sorted((base / "cases").glob("*.json"))
    file_ids = {p.stem for p in case_paths}
    R.check(file_ids == set(oracle_cases), "resolution.oracle-coverage",
            f"files-only={sorted(file_ids-set(oracle_cases))}, oracle-only={sorted(set(oracle_cases)-file_ids)}")
    R.check(REQUIRED_RESOLUTION_CASES <= file_ids, "resolution.required-fixtures",
            f"missing required explicit-root cases: {sorted(REQUIRED_RESOLUTION_CASES-file_ids)}")
    for path in case_paths:
        case = load_json(path)
        if not isinstance(case, dict): continue
        deserialization = case.get("deserialization_expectation")
        if path.stem in {"duplicate-resource-id", "duplicate-resource-path", "self-dependency"}:
            R.check(deserialization == {"status": "PASS", "issue_code": None},
                    "resolution.relational-candidate-deserializes",
                    f"{path.stem}: relationally invalid candidate must deserialize successfully")
            R.check(case.get("downstream_expectation") == "manifest_failure_propagated_no_selection",
                    "resolution.invalid-manifest-short-circuit",
                    f"{path.stem}: downstream action must propagate failure without selection")
        actual = evaluate_resolution_case(case, base)
        expected = case.get("expected", {})
        R.check(actual == (expected.get("status"), expected.get("issue_code")),
                "resolution.case-oracle", f"{path.stem}: expected {(expected.get('status'), expected.get('issue_code'))}, got {actual}")
        indexed_case = oracle_cases.get(path.stem, {})
        indexed = indexed_case.get("expected", {})
        R.check((indexed.get("status"), indexed.get("issue_code")) == actual,
                "resolution.index-oracle", f"{path.stem}: index disagrees with evaluated case")
        if deserialization is not None:
            R.check(indexed_case.get("deserialization_expectation") == deserialization,
                    "resolution.deserialization-index-oracle",
                    f"{path.stem}: deserialization boundary differs from index")


def diagnostic_and_canonical_gate() -> None:
    base = PI / "fixtures/diagnostic-path"
    oracle = load_json(base / "oracle-index.json") or {}
    for class_name in ("valid", "invalid"):
        indexed = {x["case"]: x for x in oracle.get(class_name, [])}
        files = {p.stem: p for p in sorted((base / class_name).glob("*.json"))}
        R.check(set(files) == set(indexed), "diagnostic.fixture-coverage",
                f"{class_name}: files/index differ: {sorted(set(files)^set(indexed))}")
        for case_id, path in files.items():
            record = load_json(path)
            if not isinstance(record, dict): continue
            value = record.get("path")
            ok, code = (True, None) if value is None else valid_lexical_path(value)
            expected = indexed[case_id].get("expected")
            R.check((ok and expected == "valid") or (not ok and code == expected),
                    "diagnostic.path-oracle", f"{case_id}: expected {expected}, got {code or 'valid'}")
            if "path" in indexed[case_id]:
                R.check(value == indexed[case_id]["path"], "diagnostic.exact-spelling", f"{case_id}: spelling differs")
    vectors = load_json(PI / "fixtures/canonical/canonical-json-vectors.json") or {}
    seen: set[str] = set()
    for vector in vectors.get("vectors", []):
        vid = vector.get("vector_id"); seen.add(vid)
        if "instance_path" in vector:
            instance = load_json((PI / "fixtures/canonical" / vector["instance_path"]).resolve())
        else: instance = vector.get("instance")
        canonical = (json.dumps(instance, ensure_ascii=False, sort_keys=True,
                                separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")
        declared = vector.get("canonical_json", "").encode("utf-8")
        R.check(canonical == declared and declared.endswith(b"\n") and not declared.endswith(b"\n\n"),
                "canonical.byte-identity", f"{vid}: declared canonical bytes differ")
        R.check(sha256(declared) == vector.get("canonical_sha256"),
                "canonical.sha256", f"{vid}: digest differs")
        if "spelling_oracle" in vector:
            R.check(instance.get("path") == vector["spelling_oracle"] and
                    vector["spelling_oracle"].encode("utf-8") in declared,
                    "canonical.diagnostic-spelling", f"{vid}: spelling not preserved")
    R.check(len(seen) == 17 and len(seen) == len(vectors.get("vectors", [])),
            "canonical.vector-set", "expected 17 unique canonical vector IDs")


def evidence_oracle_gate(profile: dict[str, Any]) -> None:
    data = load_json(LOCAL / "fixtures/evidence-classification/cases.json") or {}
    scopes = [(x[0]["path"], x[1], set(x[2])) for x in profile.get("evidence_scope_rules", [])]
    namespaces = {x[0]: (x[1], x[2], x[3]) for x in profile.get("evidence_namespace_rules", [])}
    protected = {tuple(x) for x in profile.get("protected_unowned_functions", [])}
    for case in data.get("cases", []):
        path = case.get("module_path"); marker = case.get("marker"); evidence = case.get("evidence_id")
        match = next((x for x in scopes if path == x[0] or path.startswith(x[0] + "/")), None)
        status = "PASS"; code = None; classification = marker
        if (path, case.get("function")) in protected and evidence is None:
            status, code = "WARN", "PIH.EVIDENCE.PROTECTED_GAP"
        elif not match or marker != match[1]: status, code = "FAIL", "PIH.EVIDENCE.MARKER_UNDECLARED"
        elif evidence:
            matched_ns = next((ns for ns in namespaces if evidence.startswith(ns + "-")), None)
            if matched_ns not in match[2]: status, code = "FAIL", "PIH.EVIDENCE.NAMESPACE_UNDECLARED"
        expected = case.get("expected", {})
        R.check(status == expected.get("status") and code == expected.get("issue_code"),
                "evidence.classification-oracle", f"{case.get('case_id')}: expected {expected}, got {status}/{code}")
        if status in {"PASS", "WARN"}:
            represented_claim = (classification if status == "PASS" else
                                 f"{classification}-only; no numerical/scientific claim")
            R.check(represented_claim == expected.get("classification"),
                    "evidence.classification-and-claim",
                    f"{case.get('case_id')}: expected {expected.get('classification')!r}, got {represented_claim!r}")


def leakage_gate(profile: dict[str, Any], local: dict[str, Any]) -> None:
    """Require the entire generic tree, including fixtures and this source, to be portable."""
    local_identity = str(profile.get("profile_id", "")).split(".", 1)[0]
    generic_evidence_classes = {
        "software_verification", "numerical_verification",
        "scientific_validation", "uncertainty_quantification",
    }
    # These spellings are now generic structured evidence-class values. Only
    # additional local marker vocabulary is project leakage.
    local_markers = {str(value) for value in profile.get("pytest_markers", [])} - generic_evidence_classes
    local_prefixes = {str(value[0]) for value in profile.get("evidence_namespace_rules", [])}
    local_roots = {str(value[0].get("path")) for value in profile.get("evidence_scope_rules", [])}
    local_ids = {str(item.get("resource_id")) for item in local.get("resources", [])}
    domain_literals = {
        "quantum " + "espresso", "wannier" + "90", "semi" + "conductor",
        "hamil" + "tonian", "kohn" + "-sham", "sna" + "kes", "operator " + "record",
    }
    literal_groups = {
        "project-identity": ({local_identity} | local_ids) - {""},
        "project-marker": local_markers,
        "project-evidence-prefix": local_prefixes,
        "project-root": local_roots,
        "domain-semantics": domain_literals,
    }
    task_pattern = re.compile(r"\b[HP][0-9]+\b")
    runtime_state_pattern = re.compile(r"\." + r"pi(?:/|`)")
    findings: list[str] = []
    maintained_text_paths = {
        str(item.get("path")) for item in (load_json(PI / "resource-manifest.json") or {}).get("resources", [])
        if isinstance(item.get("path"), str)
    }
    supported_text_suffixes = {".json", ".md", ".py", ".txt"}
    paths = sorted(
        path for path in PI.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.relative_to(PI).parts
        and path.suffix not in {".pyc", ".pyo"}
        and (path.suffix in supported_text_suffixes
             or path.relative_to(PI).as_posix() in maintained_text_paths)
    )
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            R.fail("leakage.generic-text-utf8", f"{rel(path)}: {exc}")
            continue
        for label, literals in literal_groups.items():
            for literal in sorted(literals):
                pattern = re.compile(re.escape(literal), re.I)
                for match in pattern.finditer(text):
                    line = text.count("\n", 0, match.start()) + 1
                    findings.append(f"{rel(path)}:{line}:{label}:{match.group(0)}")
        for label, pattern in (("project-task-id", task_pattern),
                               ("runtime-state-root", runtime_state_pattern)):
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                findings.append(f"{rel(path)}:{line}:{label}:{match.group(0)}")
    R.check(not findings, "leakage.generic-zero-local-dependencies", "; ".join(findings))


def docs_gate() -> None:
    requirements = {
        PI / "docs/resources.md": ("root explicitly", "extend", "symlink", "SHA-256", "DiagnosticPath", "human acceptance"),
        PI / "docs/evidence-grammar.md": ("class_owned", "artifact_owned", "software verification", "numerical verification", "scientific validation", "uncertainty quantification"),
        LOCAL / "docs/project-profile.md": ("explicit", "extend_only", "namespace", "marker", "compatibility", "local"),
    }
    for path, concepts in requirements.items():
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        missing = [x for x in concepts if x.casefold() not in text.casefold()]
        R.check(not missing, "docs.required-concepts", f"{rel(path)} missing {missing}")


def main() -> int:
    complete_file_gate()
    _, validators = schema_and_fixture_gate()
    semantic_invariant_gate(validators)
    generic, local, profile = manifest_gate()
    profile_gate(profile, generic, local)
    validation_route_gate(local)
    skill_gate(generic, profile)
    resolution_gate()
    diagnostic_and_canonical_gate()
    evidence_oracle_gate(profile)
    leakage_gate(profile, local)
    docs_gate()
    # Stable, sorted output permits byte-for-byte comparison across runs.
    unique_passes = sorted(set(R.passes))
    failures = sorted(set(R.failures))
    print(f"RESOURCE VALIDATION {'PASS' if not failures else 'FAIL'}")
    print(f"gates_passed={len(unique_passes)} defects={len(failures)}")
    for gate in unique_passes:
        print(f"PASS {gate}")
    for failure in failures:
        print(f"FAIL {failure}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
