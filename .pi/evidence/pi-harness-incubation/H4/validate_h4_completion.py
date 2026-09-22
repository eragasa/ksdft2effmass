#!/usr/bin/env python3
"""Fail-closed deterministic H4 completion and retained-evidence gate."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EVIDENCE = ROOT / ".pi/evidence/pi-harness-incubation/H4"
PAIR_IDS = (
    "task-chain-explicit-selection",
    "checkpoint-validator",
    "ownership-validator-h4",
    "ownership-validator-legacy-p1-boundary-owned",
    "evidence-id-audit-h4-selection",
    "accepted-checksum-catalogs",
    "skill-capability-and-explicit-descriptor-selection",
    "h3-resource-validator",
)
PAIR_CLASSIFICATIONS = {
    "task-chain-explicit-selection": "equivalent",
    "checkpoint-validator": "intentional",
    "ownership-validator-h4": "equivalent",
    "ownership-validator-legacy-p1-boundary-owned": "intentional",
    "evidence-id-audit-h4-selection": "equivalent",
    "accepted-checksum-catalogs": "intentional",
    "skill-capability-and-explicit-descriptor-selection": "intentional",
    "h3-resource-validator": "equivalent",
}
OBSERVATION_KEYS = {
    "command",
    "status",
    "exit_status",
    "issue_facts",
    "paths",
    "related_identities",
    "state",
    "inventory",
    "report_identity",
}
CHECKSUM_EXCLUSIONS = [
    {
        "path": ".pi/evidence/pi-harness-incubation/H4/checksums.sha256",
        "reason": "The stable catalog cannot include its own content identity without self-reference.",
    },
    {
        "path": ".pi/evidence/pi-harness-incubation/H4/shadow-parity-results.json",
        "reason": "Generated clean-replay output is validated structurally and against revision_identity by the semantic completion gate.",
    },
    {
        "path": ".pi/evidence/pi-harness-incubation/H4/acceptance-artifacts.json",
        "reason": "The acceptance index owns the catalog count and exact exclusion policy and is validated structurally by the semantic completion gate.",
    },
    {
        "path": ".pi/evidence/pi-harness-incubation/H4/validation-results.json",
        "reason": "Finalized command evidence is validated structurally by the semantic completion gate after stable-boundary checks complete.",
    },
    {
        "path": ".pi/evidence/pi-harness-incubation/H4/evidence-artifact-hashes.json",
        "reason": "The deterministic E hash index hashes exactly the three generated reports and cannot hash itself.",
    },
]
GENERATED_E_PATHS = (
    ".pi/evidence/pi-harness-incubation/H4/shadow-parity-results.json",
    ".pi/evidence/pi-harness-incubation/H4/acceptance-artifacts.json",
    ".pi/evidence/pi-harness-incubation/H4/validation-results.json",
)
FOCUSED_PYTEST_COMMAND = (
    "python -m pytest -q "
    "python/tests/software_verification/ksdft2effmass/harness/pi/local"
)
FULL_PYTEST_COMMAND = "pytest -q python"
LOCAL_TEST_ROOT = "python/tests/software_verification/ksdft2effmass/harness/pi/local"
EVIDENCE_ID_PATTERN = re.compile(r"SV-HL-[0-9]{3}")
REQUIRED = (
    "acceptance-artifacts.json",
    "checksums.sha256",
    "evidence-artifact-hashes.json",
    "cutover-and-rollback-plan.md",
    "old-new-traceability.json",
    "replay_selected_validators.py",
    "shadow-parity-results.json",
    "unrelated-worktree-baseline.json",
    "validation-results.json",
)


def fail(message: str) -> int:
    print(f"H4 completion: FAIL: {message}")
    return 1


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sorted_unique_strings(value: object, *, nonempty: bool = True) -> bool:
    return (
        isinstance(value, list)
        and all(
            isinstance(item, str) and (bool(item) or not nonempty) for item in value
        )
        and value == sorted(set(value))
    )


def valid_observation(value: object, expected_paths: list[str]) -> bool:
    if not isinstance(value, dict) or set(value) != OBSERVATION_KEYS:
        return False
    report = value.get("report_identity")
    issue_facts = value.get("issue_facts")
    state = value.get("state")
    valid_issues = isinstance(issue_facts, list)
    issue_keys: list[tuple[str, str, str, str, tuple[str, ...]]] = []
    if isinstance(issue_facts, list):
        for fact in issue_facts:
            if not isinstance(fact, list) or len(fact) != 5:
                valid_issues = False
                break
            code, severity, subject, path, related = fact
            if (
                not isinstance(code, str)
                or not code
                or not isinstance(severity, str)
                or not severity
                or (subject is not None and not isinstance(subject, str))
                or (path is not None and not isinstance(path, str))
                or not _sorted_unique_strings(related)
            ):
                valid_issues = False
                break
            issue_keys.append(
                (code, severity, subject or "", path or "", tuple(related))
            )
        valid_issues = valid_issues and issue_keys == sorted(set(issue_keys))
    valid_state = isinstance(state, list)
    state_keys: list[tuple[str, tuple[str, ...]]] = []
    if isinstance(state, list):
        for fact in state:
            if (
                not isinstance(fact, list)
                or len(fact) != 2
                or not isinstance(fact[0], str)
                or not fact[0]
                or not _sorted_unique_strings(fact[1])
            ):
                valid_state = False
                break
            state_keys.append((fact[0], tuple(fact[1])))
        valid_state = valid_state and state_keys == sorted(set(state_keys))
    return (
        isinstance(value.get("command"), list)
        and bool(value["command"])
        and all(isinstance(x, str) and x for x in value["command"])
        and value.get("status") in {"PASS", "WARN", "FAIL"}
        and isinstance(value.get("exit_status"), int)
        and not isinstance(value.get("exit_status"), bool)
        and valid_issues
        and value.get("paths") == expected_paths
        and _sorted_unique_strings(value.get("paths"))
        and _sorted_unique_strings(value.get("related_identities"))
        and valid_state
        and _sorted_unique_strings(value.get("inventory"))
        and isinstance(report, dict)
        and set(report) == {"algorithm", "digest"}
        and report["algorithm"] == "sha256"
        and isinstance(report["digest"], str)
        and re.fullmatch(r"[0-9a-f]{64}", report["digest"]) is not None
    )


def revision_blob_bytes(root: Path, revision: str, path: str) -> bytes | None:
    completed = subprocess.run(
        ["git", "show", f"{revision}:{path}"],
        cwd=root,
        capture_output=True,
        check=False,
    )
    return completed.stdout if completed.returncode == 0 else None


def revision_blob_digest(root: Path, revision: str, path: str) -> str | None:
    blob = revision_blob_bytes(root, revision, path)
    return hashlib.sha256(blob).hexdigest() if blob is not None else None


def validate_checksum_policy(
    acceptance: object, catalog_paths: set[str], catalog_count: int
) -> str | None:
    if not isinstance(acceptance, dict):
        return "acceptance index schema is invalid"
    if acceptance.get("checksum_exclusions") != CHECKSUM_EXCLUSIONS:
        return "checksum exclusion policy is not the exact contracted five"
    excluded_paths = {item["path"] for item in CHECKSUM_EXCLUSIONS}
    if catalog_paths & excluded_paths:
        return "stable checksum catalog contains a generated/self-referential exclusion"
    artifacts = [
        item
        for item in acceptance.get("artifacts", [])
        if isinstance(item, dict)
        and item.get("path") == ".pi/evidence/pi-harness-incubation/H4/checksums.sha256"
    ]
    if (
        len(artifacts) != 1
        or artifacts[0].get("entry_count") != catalog_count
        or artifacts[0].get("status") != "stable_boundary_pass"
    ):
        return "stable checksum count/status does not agree with acceptance index"
    return None


def derive_test_evidence_inventory(
    root: Path, revision: str
) -> tuple[list[str], list[str], int] | str:
    """Derive maintained evidence-bearing tests and IDs only from frozen Git blobs."""
    completed = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", revision, "--", LOCAL_TEST_ROOT],
        cwd=root,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        return "maintained local test inventory is unavailable from R"
    try:
        paths = completed.stdout.decode("utf-8").splitlines()
    except UnicodeDecodeError:
        return "maintained local test path inventory in R is not UTF-8"
    candidates = sorted(
        path
        for path in paths
        if Path(path).name.startswith("test__") and path.endswith(".py")
    )
    occurrences: list[str] = []
    for path in candidates:
        blob = revision_blob_bytes(root, revision, path)
        try:
            text = blob.decode("utf-8") if blob is not None else ""
        except UnicodeDecodeError:
            return f"manifest-declared maintained text path in R is not UTF-8: {path}"
        occurrences.extend(EVIDENCE_ID_PATTERN.findall(text))
    return candidates, sorted(set(occurrences)), len(occurrences)


def validate_pytest_record(record: object, label: str = "focused") -> str | None:
    """Validate pytest success and an optional count tied to the same recorded run."""
    if not isinstance(record, dict):
        return f"{label} pytest validation record is absent"
    exit_status = record.get("exit_status")
    if (
        record.get("status") != "PASS"
        or not isinstance(exit_status, int)
        or isinstance(exit_status, bool)
        or exit_status != 0
    ):
        return (
            f"{label} pytest validation record is not PASS with "
            "integer exit_status 0"
        )
    summary = record.get("summary")
    if not isinstance(summary, str):
        return f"{label} pytest validation summary is invalid"
    summary_matches = re.findall(r"(?<![0-9])(\d+) passed\b", summary)
    has_count_contract = bool(summary_matches) or any(
        key in record for key in ("reported_count", "observed_count")
    )
    if not has_count_contract:
        return None
    reported = record.get("reported_count")
    observed = record.get("observed_count")
    if (
        len(summary_matches) != 1
        or not isinstance(reported, int)
        or isinstance(reported, bool)
        or reported < 0
        or not isinstance(observed, int)
        or isinstance(observed, bool)
        or observed < 0
        or int(summary_matches[0]) != reported
        or reported != observed
    ):
        return f"{label} pytest same-run count contract is invalid or mismatched"
    return None


def validate_generated_evidence(
    acceptance: object,
    validation: object,
    parity: object,
    root: Path = ROOT,
) -> str | None:
    if not isinstance(acceptance, dict) or not isinstance(parity, dict):
        return "generated acceptance/parity evidence schema is invalid"
    revision = parity.get("revision_identity")
    finalized = (
        acceptance.get("acceptance_status") == "implementation_pass"
        and acceptance.get("implementation_revision") == revision
    )
    if (
        acceptance.get("schema_version") != 1
        or acceptance.get("artifact_identity") != "H4.acceptance-index.v1"
        or acceptance.get("task_id") != "H4"
        or acceptance.get("record_role") != "E_finalized"
        or not finalized
        or acceptance.get("implementation_evidence_status") != "PASS"
        or acceptance.get("human_acceptance_claimed") is not False
        or acceptance.get("authoritative_route") != "legacy_pending_h4_checkpoint"
        or acceptance.get("review_gate")
        != {"required": True, "status": "pending_independent_review"}
    ):
        return "implementation acceptance index is structurally inconsistent"
    if not isinstance(validation, dict):
        return "generated validation evidence schema is invalid"
    inventory = derive_test_evidence_inventory(root, str(revision))
    if isinstance(inventory, str):
        return inventory
    modules, evidence_ids, occurrence_count = inventory
    expected_summaries = {
        "python harness/pi/validation/validate_h3_resources.py": "55 gates, 0 defects",
        "python .pi/skills/validate_skill_capabilities.py": "6 skill records, 6 filesystem skills, 0 validation errors",
    }
    commands = validation.get("commands")
    if not isinstance(commands, list) or any(
        not isinstance(item, dict) for item in commands
    ):
        return "generated validation command inventory is invalid"
    indexed = {item.get("command"): item for item in commands}
    if len(indexed) != len(commands):
        return "generated validation command identities are not unique"
    if any(
        indexed.get(command, {}).get("status") != "PASS"
        or indexed.get(command, {}).get("exit_status") != 0
        or indexed.get(command, {}).get("summary") != summary
        for command, summary in expected_summaries.items()
    ):
        return "required parent-supplied validation facts are absent"
    for label, command in (
        ("focused", FOCUSED_PYTEST_COMMAND),
        ("full", FULL_PYTEST_COMMAND),
    ):
        if reason := validate_pytest_record(indexed.get(command), label):
            return reason
    audit_command = (
        "generic AuditEvidenceIdentifiers over "
        f"{len(modules)} H4 local test modules with explicit ksdft2effmass-v2 profile"
    )
    audit = indexed.get(audit_command)
    if (
        not isinstance(audit, dict)
        or audit.get("status") != "PASS"
        or audit.get("exit_status") != 0
        or audit.get("summary")
        != f"{len(modules)} modules, {occurrence_count} occurrences, 0 issues"
        or audit.get("module_inventory") != modules
        or audit.get("evidence_id_inventory") != evidence_ids
    ):
        return "E validation module/evidence inventory does not match frozen R blobs"
    finalized_validation = (
        finalized
        and validation.get("implementation_revision") == revision
        and validation.get("replay_label") == f"clean-revision:{revision}"
        and validation.get("overall_status")
        == "IMPLEMENTATION_PASS_PENDING_INDEPENDENT_REVIEW_AND_HUMAN_ACCEPTANCE"
        and validation.get("difference_summary")
        == {
            "equivalent": 4,
            "intentional": 4,
            "defect": 0,
            "deferred": 0,
            "retained_clean_replay_revision": revision,
        }
        and validation.get("deferred") == []
    )
    if (
        validation.get("schema_version") != 1
        or validation.get("artifact_identity") != "H4.validation-results.v1"
        or validation.get("task_id") != "H4"
        or validation.get("record_role") != "E_finalized"
        or not finalized_validation
        or validation.get("defects") != []
        or validation.get("review_gate")
        != {"required": True, "status": "pending_independent_review"}
        or validation.get("authoritative_route") != "legacy_pending_human_checkpoint"
        or validation.get(
            "authoritative_cutover_allowed_without_review_and_human_acceptance"
        )
        is not False
    ):
        return "generated validation evidence is structurally inconsistent"
    return None


def validate_e_artifact_hashes(
    index: object, revision: str, root: Path = ROOT
) -> str | None:
    if not isinstance(index, dict) or index.get("schema_version") != 1:
        return "E artifact hash index schema is invalid"
    if (
        index.get("artifact_identity") != "H4.evidence-artifact-hashes.v1"
        or index.get("task_id") != "H4"
        or index.get("implementation_revision") != revision
        or index.get("algorithm") != "sha256"
    ):
        return "E artifact hash index identity is invalid"
    artifacts = index.get("artifacts")
    if not isinstance(artifacts, list) or [
        item.get("path") for item in artifacts if isinstance(item, dict)
    ] != list(GENERATED_E_PATHS):
        return "E artifact hash index does not name exactly the generated reports"
    for item in artifacts:
        if (
            not isinstance(item, dict)
            or set(item) != {"path", "sha256"}
            or re.fullmatch(r"[0-9a-f]{64}", str(item.get("sha256"))) is None
            or not (root / item["path"]).is_file()
            or digest(root / item["path"]) != item["sha256"]
        ):
            return f"E artifact hash mismatch: {item.get('path') if isinstance(item, dict) else '<invalid>'}"
    return None


def validate_unrelated_work(
    root: Path, entries: object, authorized_paths: set[str] | None = None
) -> str | None:
    if not isinstance(entries, list) or not entries:
        return "unrelated-work baseline is absent"
    baseline: dict[str, dict[str, object]] = {}
    for entry in entries:
        if (
            not isinstance(entry, dict)
            or set(entry) != {"path", "sha256", "status"}
            or not isinstance(entry.get("path"), str)
            or not isinstance(entry.get("status"), str)
            or re.fullmatch(r"[0-9a-f]{64}", str(entry.get("sha256"))) is None
            or entry["path"] in baseline
        ):
            return "unrelated-work baseline schema is invalid"
        baseline[entry["path"]] = entry
    for path, entry in baseline.items():
        if not (root / path).is_file() or digest(root / path) != entry["sha256"]:
            return f"unrelated-work baseline preservation failure: {path}"
    return None


def validate_parity(parity: object, root: Path = ROOT) -> str | None:
    if not isinstance(parity, dict) or parity.get("schema_version") != 2:
        return "shadow evidence is not schema version 2 clean replay output"
    if parity.get("artifact_identity") != "H4.shadow-parity-results.v2":
        return "shadow artifact identity is invalid"
    replay_program = (
        ".pi/evidence/pi-harness-incubation/H4/replay_selected_validators.py"
    )
    if parity.get("replay_program") != replay_program:
        return "shadow replay program identity is invalid"
    if (
        parity.get("replay_input_definition")
        != ".pi/evidence/pi-harness-incubation/H4/replay-inputs.json"
    ):
        return "shadow replay-input definition is invalid"
    revision = parity.get("revision_identity")
    if (
        not isinstance(revision, str)
        or re.fullmatch(r"[0-9a-f]{40}", revision) is None
        or parity.get("clean_revision_replay") is not True
    ):
        return "clean durable revision identity is absent"
    if parity.get("replay_program_sha256") != revision_blob_digest(
        root, revision, replay_program
    ):
        return "shadow replay program R blob identity is invalid"
    completed = subprocess.run(
        ["git", "cat-file", "-e", f"{revision}^{{commit}}"],
        cwd=root,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        return "replay revision is not a durable Git commit"
    pairs = parity.get("pairs")
    if (
        not isinstance(pairs, list)
        or tuple(x.get("pair_id") for x in pairs if isinstance(x, dict)) != PAIR_IDS
    ):
        return "shadow pair set/order is not the exact contracted eight"
    counts = {name: 0 for name in ("equivalent", "intentional", "defect", "deferred")}
    for pair in pairs:
        pair_id = pair["pair_id"]
        if pair.get("classification") != PAIR_CLASSIFICATIONS[pair_id]:
            return f"classification drift: {pair_id}"
        counts[pair["classification"]] += 1
        identities = pair.get("input_identities")
        if not isinstance(identities, list) or not identities:
            return f"empty input identities: {pair_id}"
        if any(
            not isinstance(item, dict) or set(item) != {"path", "sha256"}
            for item in identities
        ):
            return f"invalid input identity schema: {pair_id}"
        paths = [item["path"] for item in identities]
        if any(
            not isinstance(path, str) or not path for path in paths
        ) or paths != sorted(set(paths)):
            return f"invalid input path identity set: {pair_id}"
        for item in identities:
            path, expected = item["path"], item["sha256"]
            if (
                not isinstance(expected, str)
                or re.fullmatch(r"[0-9a-f]{64}", expected) is None
                or revision_blob_digest(root, revision, path) != expected
            ):
                return f"input identity mismatch: {pair_id}:{path}"
        expected_set_hash = hashlib.sha256(
            (
                json.dumps(
                    identities,
                    ensure_ascii=True,
                    separators=(",", ":"),
                    sort_keys=True,
                )
                + "\n"
            ).encode()
        ).hexdigest()
        if pair.get("input_set_hash") != expected_set_hash:
            return f"input set hash mismatch: {pair_id}"
        if not valid_observation(pair.get("legacy"), paths) or not valid_observation(
            pair.get("local"), paths
        ):
            return f"incomplete normalized observation: {pair_id}"
        for side in ("legacy", "local"):
            observation = pair[side]
            report_facts = {
                key: value
                for key, value in observation.items()
                if key not in {"command", "report_identity"}
            }
            expected_report = hashlib.sha256(
                (
                    json.dumps(
                        report_facts,
                        ensure_ascii=True,
                        separators=(",", ":"),
                        sort_keys=True,
                    )
                    + "\n"
                ).encode()
            ).hexdigest()
            if observation["report_identity"]["digest"] != expected_report:
                return f"report identity mismatch: {pair_id}:{side}"
        differences = pair.get("differences")
        actual = sorted(
            key
            for key in (
                "status",
                "exit_status",
                "issue_facts",
                "paths",
                "related_identities",
                "state",
                "inventory",
                "report_identity",
            )
            if pair["legacy"][key] != pair["local"][key]
        )
        if differences != actual:
            return f"difference facts are not observation-derived: {pair_id}"
        citations = pair.get("authority_citations")
        rationale = pair.get("rationale")
        if not isinstance(rationale, str) or not rationale:
            return f"missing rationale: {pair_id}"
        if pair["classification"] == "intentional":
            if (
                not differences
                or not isinstance(citations, list)
                or not citations
                or any(not isinstance(x, str) or not x for x in citations)
            ):
                return f"uncited intentional difference: {pair_id}"
            for citation in citations:
                cited_path = citation.split("#", 1)[0].split(" (", 1)[0]
                if revision_blob_digest(root, revision, cited_path) is None:
                    return f"authority citation is absent from R: {pair_id}:{citation}"
        elif differences or citations != []:
            return f"equivalent pair contains differences/citations: {pair_id}"
        if (
            pair.get("authoritative_eligible") is not True
            or pair["legacy"]["status"] != "PASS"
            or pair["local"]["status"] != "PASS"
            or pair["legacy"]["exit_status"] != 0
            or pair["local"]["exit_status"] != 0
        ):
            return f"pair is not authoritative eligible: {pair_id}"
    if parity.get("summary") != counts:
        return "shadow summary is not exactly pair-derived"
    if counts != {"equivalent": 4, "intentional": 4, "defect": 0, "deferred": 0}:
        return "shadow classification counts drifted"
    return None


def main() -> int:
    missing = [name for name in REQUIRED if not (EVIDENCE / name).is_file()]
    if missing:
        return fail("missing required artifacts: " + ",".join(missing))
    try:
        parity = json.loads((EVIDENCE / "shadow-parity-results.json").read_bytes())
        acceptance = json.loads((EVIDENCE / "acceptance-artifacts.json").read_bytes())
        validation = json.loads((EVIDENCE / "validation-results.json").read_bytes())
        artifact_hashes = json.loads(
            (EVIDENCE / "evidence-artifact-hashes.json").read_bytes()
        )
        traceability = json.loads((EVIDENCE / "old-new-traceability.json").read_bytes())
        baseline = json.loads(
            (EVIDENCE / "unrelated-worktree-baseline.json").read_bytes()
        )
        profile = json.loads(
            (ROOT / "harness/local/profiles/ksdft2effmass-v2.json").read_bytes()
        )
        route = json.loads((ROOT / "harness/local/validation-route.json").read_bytes())
        local_manifest = json.loads(
            (ROOT / "harness/local/resource-manifest.json").read_bytes()
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return fail(f"invalid retained JSON: {exc}")
    if (reason := validate_parity(parity)) is not None:
        return fail(reason)
    if reason := validate_generated_evidence(acceptance, validation, parity):
        return fail(reason)
    if reason := validate_e_artifact_hashes(
        artifact_hashes, parity["revision_identity"]
    ):
        return fail(reason)
    if (
        route != {"rollback_route": "legacy", "route": "legacy", "schema_version": 1}
        or parity.get("authoritative_route") != "legacy_pending_h4_checkpoint"
    ):
        return fail(
            "pending route/configuration is not consistently legacy-authoritative"
        )
    route_resources = [
        item
        for item in local_manifest.get("resources", [])
        if isinstance(item, dict)
        and item.get("resource_id") == "ksdft2effmass.profile.validation-route.v1"
    ]
    route_digest = hashlib.sha256(
        (ROOT / "harness/local/validation-route.json").read_bytes()
    ).hexdigest()
    expected_route_resource = {
        "content_identity": {
            "algorithm": "sha256",
            "digest": route_digest,
            "schema_version": 1,
        },
        "dependency_ids": ["ksdft2effmass.profile.v2"],
        "format_version": 1,
        "path": "validation-route.json",
        "resource_id": "ksdft2effmass.profile.validation-route.v1",
        "resource_kind": "profile",
        "schema_version": 1,
    }
    if (
        local_manifest.get("manifest_id") != "ksdft2effmass.local.resources"
        or local_manifest.get("manifest_version") != 2
        or local_manifest.get("layer") != "local"
        or route_resources != [expected_route_resource]
    ):
        return fail("local manifest/route resource identity is inconsistent")
    consumer = ROOT / ".pi/skills/validate_harness.py"
    if not consumer.is_file():
        return fail("concrete operational validation consumer is absent")
    completed_consumer = subprocess.run(
        [
            sys.executable,
            str(consumer),
            "--repository-root",
            str(ROOT),
            "--route-config",
            str(ROOT / "harness/local/validation-route.json"),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    try:
        consumer_result = json.loads(completed_consumer.stdout)
    except json.JSONDecodeError:
        consumer_result = None
    if (
        completed_consumer.returncode != 0
        or not isinstance(consumer_result, dict)
        or consumer_result.get("status") != "PASS"
        or consumer_result.get("selected_route") != "legacy"
        or consumer_result.get("rollback_route") != "legacy"
    ):
        return fail("maintained legacy consumer route is not operational")
    replay_blob = revision_blob_bytes(
        ROOT, parity["revision_identity"], parity["replay_program"]
    )
    replay_text = replay_blob.decode() if replay_blob is not None else ""
    if not all(
        token in replay_text for token in ("--side", "--no-write", "legacy", "local")
    ):
        return fail("replay side-selection consumer interface is absent")
    limitation = traceability.get("historical_replay_limitation")
    if (
        not isinstance(limitation, dict)
        or limitation.get("requires_pre_h4_worktree") is not True
        or not limitation.get("starting_revision")
    ):
        return fail("historical pre-H4 replay limitation is absent")
    namespace = ["SV-HL", 1, 13, 3]
    scope_ok = any(
        isinstance(x, list)
        and len(x) == 3
        and x[1] == "software_verification"
        and isinstance(x[2], list)
        and "SV-HL" in x[2]
        for x in profile.get("evidence_scope_rules", [])
    )
    if namespace not in profile.get("evidence_namespace_rules", []) or not scope_ok:
        return fail("required SV-HL profile handoff is not applied")
    catalog_path = ".pi/evidence/pi-harness-incubation/H4/checksums.sha256"
    catalog_blob = revision_blob_bytes(ROOT, parity["revision_identity"], catalog_path)
    if catalog_blob is None:
        return fail("stable checksum catalog is absent from R")
    try:
        catalog = catalog_blob.decode().splitlines()
    except UnicodeDecodeError:
        return fail("stable checksum catalog in R is not UTF-8")
    catalog_paths: set[str] = set()
    for line in catalog:
        expected, separator, relative = line.partition("  ")
        if (
            not separator
            or relative in catalog_paths
            or relative.endswith("/checksums.sha256")
            or revision_blob_digest(ROOT, parity["revision_identity"], relative)
            != expected
        ):
            return fail(f"invalid or mismatched R checksum closure entry: {relative}")
        catalog_paths.add(relative)
    if reason := validate_checksum_policy(acceptance, catalog_paths, len(catalog)):
        return fail(reason)
    required_boundary = {
        ".pi/evidence/pi-harness-incubation/H4/activation.json",
        ".pi/evidence/pi-harness-incubation/H4/cutover-and-rollback-plan.md",
        ".pi/evidence/pi-harness-incubation/H4/old-new-traceability.json",
        ".pi/evidence/pi-harness-incubation/H4/replay_selected_validators.py",
        ".pi/evidence/pi-harness-incubation/H4/finalize_h4_evidence.py",
        ".pi/evidence/pi-harness-incubation/H4/replay-inputs.json",
        ".pi/evidence/pi-harness-incubation/H4/task-ownership.json",
        ".pi/evidence/pi-harness-incubation/H4/unrelated-worktree-baseline.json",
        ".pi/evidence/pi-harness-incubation/H4/validate_h4_completion.py",
        "python/src/ksdft2effmass/harness/pi/local/__init__.py",
        "python/tests/software_verification/ksdft2effmass/harness/pi/local/__init__.py",
        ".pi/skills/skill-capability-inventory.json",
        ".pi/skills/validate_harness.py",
        "harness/pi/resource-manifest.json",
        "harness/local/resource-manifest.json",
        "harness/local/validation-route.json",
        "harness/local/profiles/ksdft2effmass-v2.json",
        "AGENTS.md",
        ".pi/chains/pi-harness-incubation.chain.json",
        "docs/harness/ksdft2effmass.harness.07.md",
    }
    if not required_boundary <= catalog_paths:
        return fail("checksum catalog omits an authorized H4 boundary class")
    if any(
        path.startswith(
            (
                ".pi/evidence/pi-harness-incubation/H1/",
                ".pi/evidence/pi-harness-incubation/H2/",
                ".pi/evidence/pi-harness-incubation/H3/",
                "docs/meetings/",
                "docs/conferences/",
                "docs/papers/",
            )
        )
        for path in catalog_paths
    ):
        return fail("checksum catalog includes historical or unrelated files")
    entries = baseline.get("entries")
    if reason := validate_unrelated_work(ROOT, entries):
        return fail(reason)
    sys.path.insert(0, str(ROOT / "python/src"))
    from ksdft2effmass.harness.pi import __all__ as generic_exports
    from ksdft2effmass.harness.pi.local import __all__ as local_exports

    if len(local_exports) != 30 or len(set(local_exports)) != 30:
        return fail("local public export inventory is not exactly 30 unique names")
    if len(generic_exports) != 41 or len(set(generic_exports)) != 41:
        return fail("accepted generic public export inventory was mutated")
    print(
        "H4 completion: PASS: pairs=8 local_exports=30 generic_exports=41 clean_revision_replay=true"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
