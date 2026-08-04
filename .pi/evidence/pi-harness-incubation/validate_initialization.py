#!/usr/bin/env python3
"""Validate PI harness project initialization without claiming H0 completion."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / ".pi/evidence/pi-harness-incubation"
BASELINE = EVIDENCE / "initialization/baseline.json"
HARNESS_CHAIN = ROOT / ".pi/chains/pi-harness-incubation.chain.json"
CPN_CHAIN = ROOT / ".pi/chains/backend-neutral-kohn-sham-qe.chain.json"
P1_CHECKPOINT = ROOT / ".pi/checkpoints/P1-HC03-final-acceptance.json"
TASKS = {
    "H0": ROOT / ".pi/tasks/pi-harness-incubation-H0-inventory.md",
    "H1": ROOT / ".pi/tasks/pi-harness-incubation-H1-contract.md",
    "H2": ROOT / ".pi/tasks/pi-harness-incubation-H2-python-core.md",
    "H3": ROOT / ".pi/tasks/pi-harness-incubation-H3-resources.md",
    "H4": ROOT / ".pi/tasks/pi-harness-incubation-H4-local-shadow-cutover.md",
    "H5": ROOT / ".pi/tasks/pi-harness-incubation-H5-extraction-readiness.md",
}
HARNESS_DOCUMENTS = tuple(
    f"docs/harness/ksdft2effmass.harness.{number:02d}.md" for number in range(9)
)
PROSPECTIVE_PATHS = (
    "python/src/ksdft2effmass/harness/pi",
    "python/src/ksdft2effmass/harness/pi/local",
    "harness/pi",
    "harness/local",
)


def load_json(path: Path) -> dict[str, Any]:
    """Load one required JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"expected JSON object: {path}"
    return value


def sha256(path: Path) -> str:
    """Return one file's raw SHA-256 identity."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tracked_files(prefixes: list[str]) -> list[str]:
    """Return sorted tracked files under explicit repository roots."""
    output = subprocess.check_output(
        ["git", "ls-files", "--", *prefixes], cwd=ROOT, text=True
    )
    return sorted(
        relative for relative in output.splitlines() if (ROOT / relative).is_file()
    )


def aggregate(paths: list[str]) -> str:
    """Hash sorted path and raw-file-digest pairs from the worktree."""
    digest = hashlib.sha256()
    for relative in paths:
        digest.update(relative.encode())
        digest.update(b"\0")
        digest.update(bytes.fromhex(sha256(ROOT / relative)))
        digest.update(b"\n")
    return digest.hexdigest()


def committed_files(commit: str, prefixes: list[str]) -> list[str]:
    """Return files under explicit roots from the recorded base commit."""
    output = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", commit, "--", *prefixes],
        cwd=ROOT,
        text=True,
    )
    return sorted(output.splitlines())


def committed_aggregate(commit: str, paths: list[str]) -> str:
    """Hash path and blob-content identities directly from one commit."""
    digest = hashlib.sha256()
    for relative in paths:
        contents = subprocess.check_output(
            ["git", "show", f"{commit}:{relative}"], cwd=ROOT
        )
        digest.update(relative.encode())
        digest.update(b"\0")
        digest.update(hashlib.sha256(contents).digest())
        digest.update(b"\n")
    return digest.hexdigest()


def untracked_protected_files(prefixes: list[str]) -> list[str]:
    """Return nonignored untracked files under protected roots."""
    output = subprocess.check_output(
        ["git", "ls-files", "--others", "--exclude-standard", "--", *prefixes],
        cwd=ROOT,
        text=True,
    )
    return sorted(output.splitlines())


def include_patterns() -> list[str]:
    """Read the literal Sphinx include-pattern assignment."""
    tree = ast.parse((ROOT / "docs/conf.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(
            isinstance(target, ast.Name) and target.id == "include_patterns"
            for target in node.targets
        ):
            continue
        value = ast.literal_eval(node.value)
        assert isinstance(value, list) and all(isinstance(item, str) for item in value)
        return value
    raise AssertionError("docs/conf.py lacks literal include_patterns")


def validate_links() -> int:
    """Require every relative Markdown link in the harness pages to resolve."""
    count = 0
    pattern = re.compile(r"\[[^]]+\]\(([^)]+)\)")
    for relative in HARNESS_DOCUMENTS:
        path = ROOT / relative
        for target in pattern.findall(path.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("#"):
                continue
            destination = target.split("#", 1)[0]
            assert destination, f"empty relative link: {path}:{target}"
            assert (path.parent / destination).resolve().is_file(), (
                f"unresolved harness link: {path}:{target}"
            )
            assert not target.startswith("[["), f"wikilink used in harness page: {path}"
            count += 1
    return count


def validate_schema_files() -> None:
    """Require established control-plane JSON Schemas to remain valid."""
    for relative in (
        ".pi/checkpoints/checkpoint.schema.json",
        ".pi/task-ownership/ownership.schema.json",
        ".pi/task-ownership/ownership-v2.schema.json",
        ".pi/task-ownership/evidence-branch-matrix.schema.json",
    ):
        Draft202012Validator.check_schema(load_json(ROOT / relative))


def main() -> int:
    """Run initialization, nonmutation, documentation, and activation assertions."""
    baseline = load_json(BASELINE)
    p1 = load_json(P1_CHECKPOINT)
    assert p1["status"] == "resolved" and p1["normalized_decision"] == "A"
    assert "human_accepted_pass" in p1["resumption_status"]

    harness = load_json(HARNESS_CHAIN)
    cpn = load_json(CPN_CHAIN)
    assert harness["name"] == "pi-harness-incubation"
    assert harness["project_name"] == "PI Harness Incubation and Extraction Readiness"
    assert harness["active_task"] == "H0"
    assert harness["status"] == "h0_active_read_only_preflight"
    assert harness["production_execution_authorized"] is False
    assert harness["package_publication_authorized"] is False
    assert harness["pending_checkpoints"] == []

    expected_prerequisites = {
        "H0": ["P1:human_accepted"],
        "H1": ["H0:human_accepted"],
        "H2": ["H1:human_accepted"],
        "H3": ["H1:human_accepted"],
        "H4": ["H2:human_accepted", "H3:human_accepted"],
        "H5": ["H4:human_accepted"],
    }
    records = {item["id"]: item for item in harness["task_sequence"]}
    assert list(records) == list(expected_prerequisites)
    for task_id, prerequisites in expected_prerequisites.items():
        assert records[task_id]["prerequisites"] == prerequisites
        assert Path(records[task_id]["record"]) == TASKS[task_id].relative_to(ROOT)
    assert records["H0"]["status"] == "active_read_only_preflight"
    assert all(
        records[task]["status"] == "blocked" for task in ("H1", "H2", "H3", "H4", "H5")
    )
    assert (
        harness["concurrency_policy"]["current_concurrent_execution_authorized"]
        is False
    )
    assert harness["p2_gate"]["required"] == [
        "P1:human_accepted",
        "H5:human_accepted",
        "explicit_activation:P2",
    ]
    assert harness["p2_gate"]["automatic_activation_on_h5"] is False

    assert cpn["active_task"] is None
    assert cpn["production_execution_authorized"] is False
    assert cpn["pending_checkpoints"] == []
    cpn_tasks = {item["id"]: item for item in cpn["task_sequence"]}
    assert cpn_tasks["P1"]["status"] == "human_accepted_pass"
    assert cpn_tasks["P2"]["prerequisites"] == [
        "P1:human_accepted",
        "H5:human_accepted",
        "explicit_activation:P2",
    ]
    assert all(
        cpn_tasks[f"P{number}"]["status"] == "blocked" for number in range(2, 12)
    )

    h0 = TASKS["H0"].read_text(encoding="utf-8")
    assert "active read-only preflight" in h0
    for prohibited in (
        "no Python harness implementation",
        "source movement",
        "skill retirement",
        "validator replacement",
        "P2 work",
        "scientific execution",
    ):
        assert prohibited in h0
    assert "H0-HC01" in h0 and "genuine" in h0
    assert all(path.is_file() for path in TASKS.values())

    actual_docs = tuple(
        str(path.relative_to(ROOT))
        for path in sorted((ROOT / "docs/harness").glob("ksdft2effmass.harness.*.md"))
    )
    assert actual_docs == HARNESS_DOCUMENTS
    assert validate_links() == 30
    patterns = include_patterns()
    assert patterns.count("harness/ksdft2effmass.harness.*.md") == 1
    assert not any(pattern in {"**/*.md", "*.md"} for pattern in patterns)
    index = (ROOT / "docs/index.rst").read_text(encoding="utf-8")
    assert "harness/ksdft2effmass.harness.00" in index

    assert set(baseline["user_supplied_harness_documents"]) == set(
        baseline["integrated_harness_documents"]
    )
    for relative, expected in baseline["integrated_harness_documents"].items():
        assert sha256(ROOT / relative) == expected, (
            f"harness architecture modified after bounded integration: {relative}"
        )
    for relative in PROSPECTIVE_PATHS:
        assert not (ROOT / relative).exists(), (
            f"implementation/resource path created: {relative}"
        )

    for relative, expected in baseline["dependency_files"].items():
        assert sha256(ROOT / relative) == expected, (
            f"dependency file modified: {relative}"
        )
    protected_roots = ["python/src", "python/tests", "specification"]
    protected = tracked_files(protected_roots)
    base_commit = baseline["initialization_base_commit"]
    committed = committed_files(base_commit, protected_roots)
    expected_aggregate = baseline["protected_source_test_specification"]
    assert protected == committed, "protected tracked-file inventory differs from base"
    assert not untracked_protected_files(protected_roots), (
        "untracked file exists under a protected source/test/specification root"
    )
    assert len(protected) == expected_aggregate["file_count"]
    assert committed_aggregate(base_commit, committed) == expected_aggregate["sha256"]
    assert aggregate(protected) == expected_aggregate["sha256"]

    validate_schema_files()
    skill_inventory = load_json(ROOT / ".pi/skills/skill-capability-inventory.json")
    status = skill_inventory["harness_incubation_status"]
    assert status["project_id"] == "pi-harness-incubation"
    assert status["active_task"] == "H0"
    assert "No skill moved" in status["initialization_effect"]

    for generated in ("docs/_build", "python/build", "python/dist"):
        assert not (ROOT / generated).exists(), f"generated output remains: {generated}"
    assert not any(EVIDENCE.rglob("__pycache__")), (
        "generated __pycache__ remains under harness initialization evidence"
    )

    print("pi_harness_initialization=passed")
    print("p1_status=human_accepted_pass")
    print("active_harness_task=H0_read_only_preflight")
    print("blocked_harness_tasks=H1,H2,H3,H4,H5")
    print("blocked_cpn_tasks=P2-P11")
    print(f"harness_documents={len(actual_docs)}")
    print("harness_relative_links=30")
    print("implementation_paths_created=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
