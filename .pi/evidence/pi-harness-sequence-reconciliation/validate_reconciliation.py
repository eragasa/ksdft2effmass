#!/usr/bin/env python3
"""Validate the bounded harness-sequence and P2-gate reconciliation.

This is structural control-plane validation only. It does not establish
numerical verification, scientific validation, or uncertainty quantification.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = "82fe79d91a79ac305303b27c5d2e585214ccdd75"
HARNESS_CHAIN = ROOT / ".pi/chains/pi-harness-incubation.chain.json"
CPN_CHAIN = ROOT / ".pi/chains/backend-neutral-kohn-sham-qe.chain.json"
DECISION = ROOT / ".pi/checkpoints/HARNESS-SEQ-HC01-h3-h2-h4-p2-h5-governance.json"

ALLOWED_FILES = {
    "AGENTS.md",
    ".pi/chains/pi-harness-incubation.chain.json",
    ".pi/chains/backend-neutral-kohn-sham-qe.chain.json",
    ".pi/tasks/pi-harness-incubation-H1-contract.md",
    ".pi/tasks/pi-harness-incubation-H2-python-core.md",
    ".pi/tasks/pi-harness-incubation-H3-resources.md",
    ".pi/tasks/pi-harness-incubation-H4-local-shadow-cutover.md",
    ".pi/tasks/pi-harness-incubation-H5-extraction-readiness.md",
    ".pi/tasks/backend-neutral-cpn-P2-tools-provenance.md",
    ".pi/checkpoints/HARNESS-SEQ-HC01-h3-h2-h4-p2-h5-governance.json",
    "docs/harness/ksdft2effmass.harness.00.md",
    "docs/harness/ksdft2effmass.harness.08.md",
    ".pi/evidence/pi-harness-sequence-reconciliation/validate_reconciliation.py",
    ".pi/evidence/pi-harness-sequence-reconciliation/stale-claim-audit.md",
    ".pi/evidence/pi-harness-sequence-reconciliation/validation-results.json",
    ".pi/evidence/pi-harness-sequence-reconciliation/review-integration-control-plane.md",
}
PREEXISTING_UNRELATED_TRACKED = {"docs/meetings/20260728-LLENARIZAS.md"}
PREEXISTING_UNRELATED_UNTRACKED = {
    "docs/conferences/ICMSEP2026/ICMSEP-extended-abstract_02.docx",
    "docs/conferences/ICMSEP2026/~$MSEP-extended-abstract_02.docx",
    "docs/meetings/20260804-LLENARIZAS.md",
    "docs/papers/ksdft2efffmas.P03.md",
}
PROSPECTIVE_ROOTS = (
    "python/src/ksdft2effmass/harness/pi",
    "harness/pi",
    "harness/local",
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, text=True, capture_output=True, check=False
    )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def task_map(chain: dict) -> dict[str, dict]:
    return {task["id"]: task for task in chain["task_sequence"]}


def baseline_text(path: str) -> str:
    result = git("show", f"{BASE}:{path}")
    require(result.returncode == 0, f"cannot read baseline path: {path}")
    return result.stdout


def section(text: str, start: str, end: str) -> str:
    return text.split(start, 1)[1].split(end, 1)[0]


def validate_state() -> None:
    harness = load(HARNESS_CHAIN)
    cpn = load(CPN_CHAIN)
    decision = load(DECISION)
    htasks = task_map(harness)
    ptasks = task_map(cpn)

    require(harness["active_task"] is None, "harness active_task must be null")
    require(cpn["active_task"] is None, "CPN active_task must be null")
    require(harness["pending_checkpoints"] == [], "harness checkpoints unresolved")
    require(cpn["pending_checkpoints"] == [], "CPN checkpoints unresolved")
    require(htasks["H0"]["status"] == "human_accepted_pass", "H0 not accepted")
    require(htasks["H1"]["prerequisites"] == ["H0:human_accepted"], "H1 gate")
    require(htasks["H3"]["prerequisites"] == ["H1:human_accepted"], "H3 gate")
    require(htasks["H2"]["prerequisites"] == ["H3:human_accepted"], "H2 gate")
    require(htasks["H4"]["prerequisites"] == ["H2:human_accepted"], "H4 gate")
    require(
        htasks["H5"]["prerequisites"]
        == ["H4:human_accepted", "explicit_activation:H5"],
        "H5 gate",
    )
    require(
        ptasks["P2"]["prerequisites"]
        == ["P1:human_accepted", "H4:human_accepted", "explicit_activation:P2"],
        "P2 gate",
    )
    require(
        harness["p2_gate"]["required"] == ptasks["P2"]["prerequisites"],
        "chains disagree on P2 gate",
    )
    require("concurrency_policy" not in harness, "H2/H3 concurrency remains")
    require(
        all(
            htasks[key]["status"] == "blocked" for key in ("H1", "H3", "H2", "H4", "H5")
        ),
        "harness successor active",
    )
    require(
        all(ptasks[f"P{i}"]["status"] == "blocked" for i in range(2, 12)),
        "P2-P11 not all blocked",
    )
    baseline_cpn = json.loads(
        baseline_text(".pi/chains/backend-neutral-kohn-sham-qe.chain.json")
    )
    baseline_ptasks = task_map(baseline_cpn)
    for task_id in (f"P{i}" for i in range(3, 12)):
        require(
            ptasks[task_id]["prerequisites"]
            == baseline_ptasks[task_id]["prerequisites"],
            f"{task_id} prerequisites changed",
        )
    policy = harness["successor_activation_policy"]
    for key in (
        "automatic_H1_activation",
        "automatic_H2_activation",
        "automatic_H3_activation",
        "automatic_H4_activation",
        "automatic_H5_activation",
        "automatic_P2_activation",
    ):
        require(policy[key] is False, f"{key} must be false")
    require(decision["status"] == "resolved", "decision not resolved")
    require(decision["decision_class"] == "genuine_human_decision", "decision class")
    expected_response = (
        "The pre-P2 harness sequence is H1 → H3 → H2 → H4. H3 establishes "
        "the accepted generic and local textual resource identities consumed by "
        "H2. H2 implements the accepted generic Python contract against those "
        "resources. H4 performs project-local integration, shadow replay, and "
        "controlled cutover. After human acceptance of H4, P2 may be activated "
        "only by a separate explicit human decision and only while P1 remains "
        "human-accepted. H5 remains optional standalone extraction-readiness "
        "work after H4; H5 is not a prerequisite for P2 and does not activate P2."
    )
    require(
        decision["human_response"] == expected_response,
        "human decision text changed",
    )
    require(decision["task_id"] is None, "governance decision task_id must be null")
    require(
        decision["resumption_status"].find("active_task_null") >= 0,
        "decision resumption state",
    )


def validate_prose() -> None:
    texts = {
        name: (ROOT / name).read_text(encoding="utf-8")
        for name in (
            ".pi/tasks/pi-harness-incubation-H1-contract.md",
            ".pi/tasks/pi-harness-incubation-H2-python-core.md",
            ".pi/tasks/pi-harness-incubation-H3-resources.md",
            ".pi/tasks/pi-harness-incubation-H4-local-shadow-cutover.md",
            ".pi/tasks/pi-harness-incubation-H5-extraction-readiness.md",
            ".pi/tasks/backend-neutral-cpn-P2-tools-provenance.md",
            "docs/harness/ksdft2effmass.harness.00.md",
            "docs/harness/ksdft2effmass.harness.08.md",
        )
    }
    require(
        "must not overlap H3"
        in texts[".pi/tasks/pi-harness-incubation-H2-python-core.md"],
        "H2 overlap prose",
    )
    require(
        "must not overlap H2"
        in texts[".pi/tasks/pi-harness-incubation-H3-resources.md"],
        "H3 overlap prose",
    )
    require(
        "does not establish standalone package readiness"
        in texts["docs/harness/ksdft2effmass.harness.08.md"],
        "H4 readiness boundary",
    )
    require(
        "H5 is not required for P2"
        in texts["docs/harness/ksdft2effmass.harness.08.md"],
        "H5/P2 docs gate",
    )
    require(
        "H5 is optional extraction-readiness"
        in texts[".pi/tasks/backend-neutral-cpn-P2-tools-provenance.md"],
        "P2 task H5 boundary",
    )
    current_h1 = texts[".pi/tasks/pi-harness-incubation-H1-contract.md"]
    baseline_h1 = baseline_text(".pi/tasks/pi-harness-incubation-H1-contract.md")
    require(
        section(current_h1, "## Planned scope", "## Exclusions")
        == section(baseline_h1, "## Planned scope", "## Exclusions"),
        "accepted H1 contract surface changed",
    )


def validate_scope(staged: bool) -> None:
    diff_args = ["diff", "--name-only"]
    if staged:
        diff_args.append("--cached")
    changed = set(filter(None, git(*diff_args).stdout.splitlines()))
    unexpected = changed - ALLOWED_FILES
    if not staged:
        unexpected -= PREEXISTING_UNRELATED_TRACKED
    require(not unexpected, f"non-allowlisted changed paths: {sorted(unexpected)}")
    if staged:
        require(
            not (changed & PREEXISTING_UNRELATED_TRACKED),
            "unrelated tracked path staged",
        )

    untracked = set(
        filter(
            None, git("ls-files", "--others", "--exclude-standard").stdout.splitlines()
        )
    )
    permitted_untracked = set(PREEXISTING_UNRELATED_UNTRACKED)
    if not staged:
        permitted_untracked.update(ALLOWED_FILES)
    unexpected_untracked = untracked - permitted_untracked
    require(
        not unexpected_untracked,
        f"non-allowlisted untracked paths: {sorted(unexpected_untracked)}",
    )
    if staged:
        require(not (untracked & ALLOWED_FILES), "task-owned paths remain untracked")

    for protected in (
        ".pi/checkpoints/H0-HC01-harness-inventory-and-h1-scope.json",
        ".pi/tasks/pi-harness-incubation-H0-inventory.md",
        ".pi/evidence/pi-harness-incubation/H0",
        "python/src",
        "python/tests",
        "rust",
        "specification",
        "fixtures",
        "pyproject.toml",
        "python/pyproject.toml",
        "uv.lock",
        "python/uv.lock",
    ):
        result = git("diff", "--quiet", BASE, "--", protected)
        require(
            result.returncode == 0, f"protected path changed from baseline: {protected}"
        )

    for root in PROSPECTIVE_ROOTS:
        require(
            not (ROOT / root).exists(), f"prohibited prospective root exists: {root}"
        )
    evidence_root = ROOT / ".pi/evidence/pi-harness-sequence-reconciliation"
    require(
        not any(evidence_root.rglob("__pycache__")), "task evidence __pycache__ present"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staged", action="store_true")
    args = parser.parse_args()
    validate_state()
    validate_prose()
    validate_scope(args.staged)
    print("control_plane_state=PASS")
    print("task_and_documentation_consistency=PASS")
    print("protected_scope_and_historical_immutability=PASS")
    print("staging_scope=PASS" if args.staged else "worktree_scope=PASS")
    print("vvuq=structural_software_verification_only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
