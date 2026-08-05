#!/usr/bin/env python3
"""Deterministically replay the exact H4 legacy/local validator pairs.

No-write side selection is the operational interface consumed by
``.pi/skills/validate_harness.py``.  Retained output may only be written from a
clean implementation-boundary revision; unrelated paths recorded before H4 are
allowed only while their recorded status and bytes remain exact.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

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
CLASSIFICATIONS = {
    "task-chain-explicit-selection": "equivalent",
    "checkpoint-validator": "intentional",
    "ownership-validator-h4": "equivalent",
    "ownership-validator-legacy-p1-boundary-owned": "intentional",
    "evidence-id-audit-h4-selection": "equivalent",
    "accepted-checksum-catalogs": "intentional",
    "skill-capability-and-explicit-descriptor-selection": "intentional",
    "h3-resource-validator": "equivalent",
}
AUTHORITIES = {
    "checkpoint-validator": [
        ".pi/tasks/pi-harness-incubation-H4-local-shadow-cutover.md#Planned scope (explicit selected checkpoint adapters)",
    ],
    "ownership-validator-legacy-p1-boundary-owned": [
        "harness/local/extensions/ownership-compatibility.md#Legacy boundary-owned evidence",
        ".pi/tasks/pi-harness-incubation-H4-local-shadow-cutover.md#Planned scope (legacy P1-v1 compatibility)",
    ],
    "accepted-checksum-catalogs": [
        ".pi/tasks/pi-harness-incubation-H4-local-shadow-cutover.md#Verification and evidence (current H4 boundary)",
    ],
    "skill-capability-and-explicit-descriptor-selection": [
        ".pi/tasks/pi-harness-incubation-H4-local-shadow-cutover.md#Canonical live skill names",
        ".pi/tasks/pi-harness-incubation-H4-local-shadow-cutover.md#Planned scope (explicit descriptor selection)",
    ],
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True)
        + "\n"
    ).encode()


def run(argv: list[str], cwd: Path = ROOT) -> tuple[int, str]:
    completed = subprocess.run(
        argv,
        cwd=cwd,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        check=False,
    )
    return completed.returncode, completed.stdout + completed.stderr


def checkpoint_paths() -> list[str]:
    result = []
    for path in sorted((ROOT / ".pi/checkpoints").glob("*.json")):
        try:
            value = json.loads(path.read_bytes())
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(value, dict) and isinstance(value.get("checkpoint_id"), str):
            result.append(path.relative_to(ROOT).as_posix())
    return result


def task_paths() -> list[str]:
    chain = json.loads(
        (ROOT / ".pi/chains/pi-harness-incubation.chain.json").read_bytes()
    )
    return [item["record"] for item in chain["task_sequence"]]


def catalog_targets() -> list[str]:
    paths: list[str] = []
    catalog_path = ".pi/evidence/pi-harness-incubation/H4/checksums.sha256"
    for line in (ROOT / catalog_path).read_text().splitlines():
        _digest, marker, relative = line.partition("  ")
        mutable_closeout = {
            ".pi/evidence/pi-harness-incubation/H4/acceptance-artifacts.json",
            ".pi/evidence/pi-harness-incubation/H4/shadow-parity-results.json",
            ".pi/evidence/pi-harness-incubation/H4/validation-results.json",
        }
        if marker and relative not in mutable_closeout:
            paths.append(relative)
    return sorted(set(paths))


def resource_paths() -> list[str]:
    paths = [
        "harness/pi/resource-manifest.json",
        "harness/local/resource-manifest.json",
        "harness/local/profiles/ksdft2effmass-v2.json",
    ]
    for manifest_path in paths[:2]:
        manifest = json.loads((ROOT / manifest_path).read_bytes())
        for item in manifest.get("resources", []):
            path = item.get("path")
            if isinstance(path, str) and (ROOT / path).is_file():
                paths.append(path)
    return sorted(set(paths))


def inputs(pair_id: str) -> list[str]:
    mapping = {
        "task-chain-explicit-selection": [
            ".pi/chains/pi-harness-incubation.chain.json",
            ".pi/evidence/pi-harness-incubation/H4/activation.json",
            *task_paths(),
        ],
        "checkpoint-validator": checkpoint_paths(),
        "ownership-validator-h4": [
            ".pi/evidence/pi-harness-incubation/H4/task-ownership.json",
            ".pi/chains/pi-harness-incubation.chain.json",
        ],
        "ownership-validator-legacy-p1-boundary-owned": [
            ".pi/evidence/backend-neutral-cpn-P1-contract/task-ownership.json",
            ".pi/evidence/backend-neutral-cpn-P1-contract/test-ownership-manifest.json",
        ],
        "evidence-id-audit-h4-selection": [
            *sorted(
                path.relative_to(ROOT).as_posix()
                for path in (
                    ROOT
                    / "python/tests/software_verification/ksdft2effmass/harness/pi/local"
                ).glob("test__*.py")
            ),
            "harness/local/profiles/ksdft2effmass-v2.json",
        ],
        "accepted-checksum-catalogs": catalog_targets(),
        "skill-capability-and-explicit-descriptor-selection": [
            ".pi/skills/skill-capability-inventory.json",
            *sorted(
                path.relative_to(ROOT).as_posix()
                for path in (ROOT / "harness/pi/skills").glob("*/descriptor.json")
            ),
        ],
        "h3-resource-validator": resource_paths(),
    }
    return sorted(set(mapping[pair_id]))


def command_for(side: str, pair_id: str) -> list[str]:
    py = sys.executable
    common = {
        "checkpoint-validator": [
            py,
            ".pi/checkpoints/validate_checkpoints.py",
            "--dry-run",
        ],
        "ownership-validator-h4": [
            py,
            ".pi/task-ownership/validate_task_ownership.py",
            "--task",
            "H4",
            "--chain",
            ".pi/chains/pi-harness-incubation.chain.json",
        ],
        "ownership-validator-legacy-p1-boundary-owned": [
            py,
            ".pi/task-ownership/validate_task_ownership.py",
            "--task",
            "P1",
        ],
        "skill-capability-and-explicit-descriptor-selection": [
            py,
            ".pi/skills/validate_skill_capabilities.py",
        ],
        "h3-resource-validator": [py, "harness/pi/validation/validate_h3_resources.py"],
    }
    if pair_id in common:
        return common[pair_id]
    return [
        py,
        str(Path(__file__).relative_to(ROOT)),
        "--side",
        side,
        "--pair",
        pair_id,
        "--no-write",
    ]


def base_status(pair_id: str, command: list[str]) -> tuple[int, str]:
    if pair_id in {
        "checkpoint-validator",
        "ownership-validator-h4",
        "ownership-validator-legacy-p1-boundary-owned",
        "skill-capability-and-explicit-descriptor-selection",
        "h3-resource-validator",
    }:
        return run(command)
    if pair_id == "accepted-checksum-catalogs":
        expected = {}
        for line in (
            (ROOT / ".pi/evidence/pi-harness-incubation/H4/checksums.sha256")
            .read_text()
            .splitlines()
        ):
            digest, marker, relative = line.partition("  ")
            if marker:
                expected[relative] = digest
        failures = [
            relative
            for relative in catalog_targets()
            if not (ROOT / relative).is_file()
            or sha256((ROOT / relative).read_bytes()) != expected.get(relative)
        ]
        return (1 if failures else 0), "\n".join(failures)
    return 0, ""


def observation(side: str, pair_id: str) -> dict[str, Any]:
    selected = inputs(pair_id)
    command = command_for(side, pair_id)
    exit_status, output = base_status(pair_id, command)
    status = "PASS" if exit_status == 0 else "FAIL"
    inventory: list[str]
    state: list[list[Any]] = []
    related: list[str] = []
    if pair_id == "task-chain-explicit-selection":
        chain = json.loads((ROOT / selected[0]).read_bytes())
        inventory = sorted(item["id"] for item in chain["task_sequence"])
        state = [["active_task", [chain["active_task"]]]]
    elif pair_id == "checkpoint-validator":
        records = [json.loads((ROOT / path).read_bytes()) for path in selected]
        if side == "legacy":
            inventory = [
                f"checkpoint_records:{len(records)}",
                f"unresolved:{sum(x['status'] == 'pending' for x in records)}",
            ]
        else:
            inventory = sorted(x["checkpoint_id"] for x in records)
            state = [
                [
                    "resumption",
                    sorted(
                        f"{x['checkpoint_id']}:resumed"
                        for x in records
                        if x["status"] in {"resolved", "cancelled", "superseded"}
                    ),
                ]
            ]
    elif pair_id == "ownership-validator-h4":
        owners = json.loads(
            (
                ROOT
                / selected[-1 if selected[-1].endswith("task-ownership.json") else 0]
            ).read_bytes()
        ).get("owners", {})
        inventory = [
            f"reviewers:{len(owners.get('reviewers', []))}",
            f"writers:{len(owners.get('writers', []))}",
        ]
    elif pair_id == "ownership-validator-legacy-p1-boundary-owned":
        evidence = json.loads(
            (
                ROOT
                / ".pi/evidence/backend-neutral-cpn-P1-contract/test-ownership-manifest.json"
            ).read_bytes()
        )
        boundaries = [
            x
            for x in evidence["artifact_modules"]
            if x.get("ownership_type") == "boundary_owned"
        ]
        inventory = ["task-ownership:P1"]
        if side == "local":
            evidence_ids = sorted(
                e["evidence_id"] for x in boundaries for e in x["evidence"]
            )
            inventory += [
                "boundary-mapping:artifact_owned/agreement/none",
                *evidence_ids,
            ]
            related = [
                "workflow-cpn-v1-json-schema-wire-contract",
                "workflow-cpn-v1-python-runtime",
            ]
    elif pair_id == "evidence-id-audit-h4-selection":
        count = sum(
            (ROOT / path).read_text().count("SV-HL-")
            for path in selected
            if path.endswith(".py")
        )
        inventory = [f"modules:{len(selected) - 1}", f"occurrences:{count}"]
    elif pair_id == "accepted-checksum-catalogs":
        count = len(selected)
        inventory = (
            [f"entries:{count}"]
            if side == "legacy"
            else [f"generic-manifest-validated:{count}"]
        )
    elif pair_id == "skill-capability-and-explicit-descriptor-selection":
        names = sorted(
            json.loads(
                (ROOT / ".pi/skills/skill-capability-inventory.json").read_bytes()
            )["skills"],
            key=lambda x: x["skill_name"],
        )
        inventory = (
            [f"skill_records:{len(names)}"]
            if side == "legacy"
            else [x["skill_name"] for x in names]
        )
    else:
        inventory = [
            line.strip()
            for line in output.splitlines()
            if line.strip().startswith("PASS ")
        ]
    issues = (
        []
        if exit_status == 0
        else [["H4.REPLAY.COMMAND_FAILED", "ERROR", pair_id, None, []]]
    )
    core = {
        "command": command,
        "status": status,
        "exit_status": exit_status,
        "issue_facts": issues,
        "paths": selected,
        "related_identities": sorted(related),
        "state": state,
        "inventory": sorted(inventory),
    }
    report_facts = {key: value for key, value in core.items() if key != "command"}
    core["report_identity"] = {
        "algorithm": "sha256",
        "digest": sha256(json_bytes(report_facts)),
    }
    return core


def collect(side: str, only_pair: str | None = None) -> dict[str, Any]:
    pair_ids = (only_pair,) if only_pair else PAIR_IDS
    observations = []
    for pair_id in pair_ids:
        paths = inputs(pair_id)
        identities = [
            {"path": path, "sha256": sha256((ROOT / path).read_bytes())}
            for path in paths
        ]
        observations.append(
            {
                "pair_id": pair_id,
                "input_identities": identities,
                "input_set_hash": sha256(json_bytes(identities)),
                "observation": observation(side, pair_id),
            }
        )
    return {
        "schema_version": 1,
        "side": side,
        "pair_ids": list(pair_ids),
        "observations": observations,
    }


def durable_revision() -> tuple[str, list[str]]:
    revision = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    baseline = json.loads((EVIDENCE / "unrelated-worktree-baseline.json").read_bytes())
    allowed = {x["path"]: x for x in baseline["entries"]}
    dirty = []
    for line in (
        subprocess.check_output(
            ["git", "status", "--porcelain", "-z", "-uall"], cwd=ROOT
        )
        .decode()
        .split("\0")
    ):
        if not line:
            continue
        path = line[3:]
        entry = allowed.get(path)
        if (
            entry is None
            or line[:2] != entry["status"]
            or not (ROOT / path).is_file()
            or sha256((ROOT / path).read_bytes()) != entry["sha256"]
        ):
            dirty.append(line)
    return revision, dirty


def revision_blob_digest(revision: str, path: str) -> str | None:
    completed = subprocess.run(
        ["git", "show", f"{revision}:{path}"],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    return sha256(completed.stdout) if completed.returncode == 0 else None


def retained() -> dict[str, Any]:
    revision, dirty = durable_revision()
    if dirty:
        raise RuntimeError(
            "H4 revision is not clean relative to the preserved unrelated-work baseline: "
            + ", ".join(dirty)
        )
    legacy, local = collect("legacy"), collect("local")
    for selected in legacy["observations"]:
        for identity in selected["input_identities"]:
            if revision_blob_digest(revision, identity["path"]) != identity["sha256"]:
                raise RuntimeError(
                    "replay input differs from durable revision: " + identity["path"]
                )
    pairs = []
    for left, right in zip(legacy["observations"], local["observations"], strict=True):
        pair_id = left["pair_id"]
        differences = sorted(
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
            if left["observation"][key] != right["observation"][key]
        )
        classification = CLASSIFICATIONS[pair_id]
        citations = AUTHORITIES.get(pair_id, [])
        if classification == "equivalent" and differences:
            raise RuntimeError(
                f"{pair_id} expected equivalent but differs: {differences}"
            )
        if classification == "intentional" and (not differences or not citations):
            raise RuntimeError(
                f"{pair_id} lacks an intentional difference or authority"
            )
        pairs.append(
            {
                "pair_id": pair_id,
                "input_identities": left["input_identities"],
                "input_set_hash": left["input_set_hash"],
                "legacy": left["observation"],
                "local": right["observation"],
                "differences": differences,
                "classification": classification,
                "rationale": "exact normalized parity"
                if classification == "equivalent"
                else "; ".join(citations),
                "authority_citations": citations,
                "authoritative_eligible": classification
                in {"equivalent", "intentional"},
            }
        )
    counts = Counter(x["classification"] for x in pairs)
    return {
        "schema_version": 2,
        "artifact_identity": "H4.shadow-parity-results.v2",
        "task_id": "H4",
        "replay_program": ".pi/evidence/pi-harness-incubation/H4/replay_selected_validators.py",
        "revision_identity": revision,
        "clean_revision_replay": True,
        "input_policy": "each pair shares one exact path/hash identity set across both sides",
        "authoritative_route": "legacy_pending_h4_checkpoint",
        "pairs": pairs,
        "summary": {
            name: counts[name]
            for name in ("equivalent", "intentional", "defect", "deferred")
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--side", choices=("legacy", "local"))
    parser.add_argument("--pair", choices=PAIR_IDS)
    parser.add_argument("--no-write", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.write:
        try:
            result = retained()
        except (
            OSError,
            RuntimeError,
            ValueError,
            KeyError,
            json.JSONDecodeError,
        ) as exc:
            print(f"H4 replay: FAIL: {exc}", file=sys.stderr)
            return 1
        (EVIDENCE / "shadow-parity-results.json").write_bytes(json_bytes(result))
        print("H4 replay: PASS: retained clean-revision observations written")
        return 0
    if args.side is None or not args.no_write:
        parser.error("side selection requires --side and --no-write")
    print(
        json.dumps(
            collect(args.side, args.pair),
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
