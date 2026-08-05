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
]
REQUIRED = (
    "acceptance-artifacts.json",
    "checksums.sha256",
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
    if valid_issues:
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
    if valid_state:
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


def revision_blob_digest(root: Path, revision: str, path: str) -> str | None:
    completed = subprocess.run(
        ["git", "show", f"{revision}:{path}"],
        cwd=root,
        capture_output=True,
        check=False,
    )
    return (
        hashlib.sha256(completed.stdout).hexdigest()
        if completed.returncode == 0
        else None
    )


def validate_checksum_policy(
    acceptance: object, catalog_paths: set[str], catalog_count: int
) -> str | None:
    if not isinstance(acceptance, dict):
        return "acceptance index schema is invalid"
    if acceptance.get("checksum_exclusions") != CHECKSUM_EXCLUSIONS:
        return "checksum exclusion policy is not the exact contracted four"
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


def validate_generated_evidence(
    acceptance: object, validation: object, parity: object
) -> str | None:
    if not isinstance(acceptance, dict) or not isinstance(parity, dict):
        return "generated acceptance/parity evidence schema is invalid"
    revision = parity.get("revision_identity")
    provisional = (
        acceptance.get("acceptance_status")
        == "implementation_pass_new_clean_revision_replay_required"
        and acceptance.get("last_clean_replay_revision") == revision
        and "implementation_revision" not in acceptance
    )
    finalized = (
        acceptance.get("acceptance_status") == "implementation_pass"
        and acceptance.get("implementation_revision") == revision
    )
    if (
        acceptance.get("schema_version") != 1
        or acceptance.get("artifact_identity") != "H4.acceptance-index.v1"
        or acceptance.get("task_id") != "H4"
        or not (provisional or finalized)
        or acceptance.get("implementation_evidence_status") != "PASS"
        or acceptance.get("human_acceptance_claimed") is not False
        or acceptance.get("authoritative_route") != "legacy_pending_h4_checkpoint"
        or acceptance.get("review_gate")
        != {"required": True, "status": "pending_independent_review"}
    ):
        return "implementation acceptance index is structurally inconsistent"
    if not isinstance(validation, dict):
        return "generated validation evidence schema is invalid"
    expected_summaries = {
        "python -m pytest -q python/tests/software_verification/ksdft2effmass/harness/pi/local": "21 passed",
        "pytest -q python": "1104 passed",
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
    provisional_validation = (
        provisional
        and validation.get("last_clean_replay_revision") == revision
        and "implementation_revision" not in validation
        and validation.get("replay_label") == f"last-clean-replay:{revision}"
        and validation.get("overall_status")
        == "IMPLEMENTATION_PASS_NEW_CLEAN_REVISION_REPLAY_REQUIRED"
        and validation.get("difference_summary")
        == {
            "last_clean_replay_equivalent": 4,
            "last_clean_replay_intentional": 4,
            "defect": 0,
            "deferred": 0,
            "superseded_by_evidence_edits": True,
            "last_clean_replay_revision": revision,
        }
        and validation.get("deferred")
        == [
            "A new clean replay is required at the post-evidence-edit commit because current-file/revision identity equality is fail-closed."
        ]
    )
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
        or not (provisional_validation or finalized_validation)
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


def validate_unrelated_work(
    root: Path, entries: object, authorized_paths: set[str]
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
    completed = subprocess.run(
        ["git", "status", "--porcelain", "-z", "-uall"],
        cwd=root,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        return "cannot inspect exact current worktree status"
    current: dict[str, str] = {}
    for raw in completed.stdout.decode().split("\0"):
        if not raw:
            continue
        status, path = raw[:2], raw[3:]
        if path in current:
            return f"duplicate current worktree status path: {path}"
        current[path] = status
    for path, entry in baseline.items():
        if (
            current.get(path) != entry["status"]
            or not (root / path).is_file()
            or digest(root / path) != entry["sha256"]
        ):
            return f"unrelated-work baseline preservation failure: {path}"
    extras = sorted(set(current) - set(baseline) - authorized_paths)
    if extras:
        return "dirty paths escape H4 boundary/baseline: " + ",".join(extras)
    return None


def validate_parity(parity: object, root: Path = ROOT) -> str | None:
    if not isinstance(parity, dict) or parity.get("schema_version") != 2:
        return "shadow evidence is not schema version 2 clean replay output"
    if parity.get("artifact_identity") != "H4.shadow-parity-results.v2":
        return "shadow artifact identity is invalid"
    if (
        parity.get("replay_program")
        != ".pi/evidence/pi-harness-incubation/H4/replay_selected_validators.py"
    ):
        return "shadow replay program identity is invalid"
    revision = parity.get("revision_identity")
    if (
        not isinstance(revision, str)
        or re.fullmatch(r"[0-9a-f]{40}", revision) is None
        or parity.get("clean_revision_replay") is not True
    ):
        return "clean durable revision identity is absent"
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
                or not (root / path).is_file()
                or digest(root / path) != expected
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
                if not (root / cited_path).is_file():
                    return f"authority citation is not concrete: {pair_id}:{citation}"
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
    replay_text = (EVIDENCE / "replay_selected_validators.py").read_text()
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
    catalog = (EVIDENCE / "checksums.sha256").read_text().splitlines()
    catalog_paths: set[str] = set()
    for line in catalog:
        expected, separator, relative = line.partition("  ")
        if (
            not separator
            or relative in catalog_paths
            or relative.endswith("/checksums.sha256")
            or not (ROOT / relative).is_file()
            or digest(ROOT / relative) != expected
        ):
            return fail(f"invalid or mismatched checksum closure entry: {relative}")
        catalog_paths.add(relative)
    if reason := validate_checksum_policy(acceptance, catalog_paths, len(catalog)):
        return fail(reason)
    required_boundary = {
        ".pi/evidence/pi-harness-incubation/H4/activation.json",
        ".pi/evidence/pi-harness-incubation/H4/cutover-and-rollback-plan.md",
        ".pi/evidence/pi-harness-incubation/H4/old-new-traceability.json",
        ".pi/evidence/pi-harness-incubation/H4/replay_selected_validators.py",
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
    authorized_dirty_paths = {
        *catalog_paths,
        ".pi/evidence/pi-harness-incubation/H4/checksums.sha256",
    }
    if reason := validate_unrelated_work(ROOT, entries, authorized_dirty_paths):
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
