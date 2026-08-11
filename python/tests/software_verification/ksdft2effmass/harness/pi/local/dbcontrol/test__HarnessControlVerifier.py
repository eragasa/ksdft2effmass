r"""Software verification of ``HarnessControlVerifier``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module owns source-aware, nonmutating represented behavior of
``HarnessControlVerifier``.

Intrinsic and cross-object scope

The public verifier is exercised against isolated exact copies of canonical source and
maintained control state. Private collaborators are replaced only at explicit failure
seams.

VVUQ and scientific exclusions

This is structural software verification only. It does not establish pytest success,
numerical verification, scientific validation, uncertainty quantification, protected
execution, or human acceptance.
"""

import hashlib
import json
import shutil
import sqlite3
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import pytest

from ksdft2effmass.harness.pi.local import (
    HarnessControlMigrator,
    HarnessControlVerifier,
)
from ksdft2effmass.harness.pi.local.control.generation import (
    _HarnessControlGenerationBuilder,
)
from ksdft2effmass.harness.pi.local.control.inputs import (
    _HarnessControlInputResolver,
)

SUT = HarnessControlVerifier

pytestmark = pytest.mark.software_verification


@pytest.fixture
def control_root(tmp_path: Path) -> Path:
    """Evidence ID: Owns no identifier; supplies an isolated canonical repository.

    Requirement: Verifier tests must not mutate the maintained checkout.

    Method: Copy each frozen source and comparison-target root; node identities remain
    deterministically projected from the copied parsed Python evidence models.

    Oracle: The R2.7 frozen authority and generated-root maps enumerate these roots.

    Acceptance: Return one absolute isolated root with every canonical source input.

    Interpretation: Failure indicates fixture construction drift.

    Limitations: The helper establishes no independent conformance claim.
    """
    repository = Path(__file__).resolve().parents[8]
    root = tmp_path / "repository"
    root.mkdir()
    shutil.copytree(repository / "harness", root / "harness")
    shutil.copytree(repository / "docs/harness/tasks", root / "docs/harness/tasks")
    shutil.copytree(repository / "python/tests", root / "python/tests")
    shutil.copy2(repository / "python/pyproject.toml", root / "python/pyproject.toml")
    shutil.copytree(repository / ".pi/agents", root / ".pi/agents")
    shutil.copytree(repository / ".pi/checkpoints", root / ".pi/checkpoints")
    shutil.copytree(repository / ".pi/skills", root / ".pi/skills")
    shutil.copytree(
        repository / ".pi/evidence/python-conformance",
        root / ".pi/evidence/python-conformance",
    )
    shutil.copytree(repository / ".agents/skills", root / ".agents/skills")
    return root.resolve()


def mutate_source(root: Path, kind: str) -> None:
    """Evidence ID: Owns no identifier; applies one valid canonical-source change.

    Requirement: Source-aware partitions alter authority without editing generated
    comparison targets.

    Method: Change one Task field, graph relationship, evidence source, or resource and
    its authoritative manifest identity according to ``kind``.

    Oracle: The frozen authority map assigns each edited field or byte sequence to its
    named source domain.

    Acceptance: Exactly the requested canonical source domain changes validly.

    Interpretation: Failure indicates fixture partition drift.

    Limitations: This helper does not assert verifier behavior.
    """
    if kind == "task":
        path = root / "harness/tasks/P1.json"
        value = json.loads(path.read_text())
        value["title"] += " source drift"
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    elif kind == "graph":
        path = root / (
            "harness/tasks/"
            "harness.simplify-2.validation-retirement.integration-closeout.json"
        )
        value = json.loads(path.read_text())
        value["task_prerequisite_ids"].append(
            "harness.simplify-2.validation-retirement.repository-validation"
        )
        value["task_prerequisite_ids"].sort()
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    elif kind == "evidence":
        path = root / "python/tests/test__import.py"
        path.write_bytes(path.read_bytes() + b"\n# source-aware drift\n")
    elif kind == "resource":
        resource = root / "harness/pi/skills/develop-harness-resources/SKILL.md"
        resource.write_bytes(resource.read_bytes() + b"\nsource-aware drift\n")
        manifest_path = root / "harness/pi/resource-manifest.json"
        manifest = json.loads(manifest_path.read_text())
        entry = next(
            item
            for item in manifest["resources"]
            if item["path"] == "skills/develop-harness-resources/SKILL.md"
        )
        entry["content_identity"]["digest"] = hashlib.sha256(
            resource.read_bytes()
        ).hexdigest()
        manifest_path.write_text(
            json.dumps(
                manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")
            )
            + "\n"
        )
    else:
        raise ValueError(kind)


def generation_snapshot(root: Path) -> tuple[bytes, bytes, bytes, bytes]:
    """Evidence ID: Owns no identifier; snapshots representative maintained outputs.

    Requirement: Nonpublication evidence observes authority and generated projections.

    Method: Read the database, SQL, manifest, and one generated Task page exactly.

    Oracle: The generated-output ownership map identifies these four disjoint outputs.

    Acceptance: Return their bytes without transforming them.

    Interpretation: Failure indicates incomplete fixture state.

    Limitations: Exhaustive path comparison is owned by verifier implementation checks.
    """
    return (
        (root / "harness/state/harness-control.sqlite3").read_bytes(),
        (root / "harness/state/harness-control.sql").read_bytes(),
        (root / "harness/state/projection-manifest.json").read_bytes(),
        (root / "docs/harness/tasks/P1.md").read_bytes(),
    )


def test_method__execute_relative_root__raises_value_error() -> None:
    """Evidence ID: software-verification.harness.sqlite-control.verification-action.relative-root-raises-value-error

    Requirement: Verification uses an explicit absolute repository boundary.

    Method: Call the public verifier with a relative path.

    Oracle: ``Path('.')`` is not absolute.

    Acceptance: The call raises exactly ``ValueError`` before opening SQLite.

    Interpretation: Failure indicates ambient-root verification behavior.

    Limitations: Valid source-aware comparison is covered separately.
    """  # noqa: E501
    with pytest.raises(ValueError):
        HarnessControlVerifier().execute(Path("."))


def test_method__execute_valid_source_state__reports_exact_semantic_agreement(
    control_root: Path,
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.verification-action.valid-source-state

    Requirement: Valid maintained state agrees with a candidate generated from canonical
    source authority without requiring a raw SQLite byte contract.

    Method: Verify an isolated exact repository copy, then change only SQLite
    ``application_id`` and verify again.

    Oracle: ``application_id`` changes SQLite bytes but not represented harness tables,
    canonical SQL, or projections.

    Acceptance: Both results have no findings and semantic, schema, SQL, manifest, and
    projection agreement; the second raw hashes differ.

    Interpretation: Failure identifies source reconstruction or raw-byte comparison.

    Limitations: Individual drift domains are covered separately.
    """  # noqa: E501
    result = HarnessControlVerifier().execute(control_root)
    assert result.findings == ()
    database = control_root / "harness/state/harness-control.sqlite3"
    with sqlite3.connect(database) as connection:
        connection.execute("PRAGMA journal_mode=DELETE")
        connection.execute("PRAGMA application_id=1")
    changed = HarnessControlVerifier().execute(control_root)
    assert changed.findings == ()
    assert changed.semantic_digest == changed.reconstructed_semantic_digest
    assert changed.raw_database_sha256 != changed.reconstructed_database_sha256
    assert (
        changed.schema_version_agrees,
        changed.sql_identical,
        changed.manifest_identical,
        changed.projections_identical,
    ) == (True, True, True, True)


@pytest.mark.parametrize(
    "kind",
    (
        pytest.param("task", id="task_source"),
        pytest.param("graph", id="graph_source"),
        pytest.param("evidence", id="evidence_source"),
        pytest.param("resource", id="resource_source"),
    ),
)
def test_method__execute_authoritative_source_drift__reports_disagreement(
    control_root: Path, kind: str
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.verification-action.authoritative-source-drift

    Requirement: Valid changes to Task, graph, Python evidence, and resource authority
    are detected when maintained control artifacts still represent the prior sources.

    Method: Apply one valid source-domain mutation and execute public verification.

    Oracle: The untouched maintained database and SQL cannot represent the changed
    authoritative source selected by the frozen map.

    Acceptance: Every partition reports semantic disagreement and changed generated
    artifacts without publishing the candidate.

    Interpretation: Failure identifies source-insensitive or circular verification.

    Limitations: Malformed source rejection is outside this valid-drift partition.
    """  # noqa: E501
    before = generation_snapshot(control_root)
    mutate_source(control_root, kind)
    result = HarnessControlVerifier().execute(control_root)
    assert "semantic_disagreement" in {item.code for item in result.findings}
    assert "changed_artifact" in {item.code for item in result.findings}
    assert generation_snapshot(control_root) == before


def test_method__execute_jointly_modified_sqlite_and_sql__rejects_stale_sources(
    control_root: Path,
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.verification-action.jointly-modified-state

    Requirement: Agreement between maintained SQLite and SQL cannot conceal disagreement
    with canonical source authority.

    Method: Change one evidence source, publish that internally consistent generation,
    restore the original source, and execute public verification.

    Oracle: Restored source bytes define a candidate distinct from both jointly changed
    maintained persistence artifacts.

    Acceptance: Verification reports semantic disagreement and changed canonical SQL.

    Interpretation: Failure identifies circular SQLite/SQL verification.

    Limitations: This fixture uses the authorized migrator only inside its isolated root.
    """  # noqa: E501
    source = control_root / "python/tests/test__import.py"
    original = source.read_bytes()
    mutate_source(control_root, "evidence")
    request = _HarnessControlInputResolver().execute(control_root).request
    HarnessControlMigrator().execute(request)
    source.write_bytes(original)
    result = HarnessControlVerifier().execute(control_root)
    assert "semantic_disagreement" in {item.code for item in result.findings}
    assert result.sql_identical is False


@pytest.mark.parametrize(
    ("kind", "expected_code", "passes"),
    (
        pytest.param("missing", "missing_artifact", False, id="missing_projection"),
        pytest.param("changed", "changed_artifact", False, id="changed_projection"),
        pytest.param("unexpected", "unexpected_artifact", False, id="unexpected_owned"),
        pytest.param("unrelated", None, True, id="unrelated_human_authored"),
    ),
)
def test_method__execute_projection_ownership__confines_drift_detection(
    control_root: Path, kind: str, expected_code: str | None, passes: bool
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.verification-action.projection-ownership

    Requirement: Missing, changed, and unexpected files inside publisher ownership are
    drift, while unrelated human-authored neighboring files are outside comparison.

    Method: Apply one exact filesystem partition and execute public verification.

    Oracle: The frozen generated-root ownership map classifies each selected path.

    Acceptance: Owned drift reports the expected code and fails projection agreement;
    the unrelated partition has no findings and passes.

    Interpretation: Failure identifies incomplete or overbroad generated-root scanning.

    Limitations: Database, SQL, and manifest partitions are covered separately.
    """  # noqa: E501
    page = control_root / "docs/harness/tasks/P1.md"
    if kind == "missing":
        page.unlink()
    elif kind == "changed":
        page.write_bytes(b"changed\n")
    elif kind == "unexpected":
        (control_root / "docs/harness/tasks/unexpected.md").write_bytes(b"extra\n")
    else:
        report = control_root / "harness/reports/human-authored.txt"
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_bytes(b"outside ownership\n")
    result = HarnessControlVerifier().execute(control_root)
    assert (not result.findings) is passes
    assert (expected_code is None) is passes
    if expected_code is not None:
        assert expected_code in {item.code for item in result.findings}
        assert result.projections_identical is False


def test_method__execute_temporary_workspace__cleans_after_success_and_failure(
    monkeypatch: pytest.MonkeyPatch, control_root: Path, tmp_path: Path
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.verification-action.temporary-cleanup

    Requirement: Verification owns and removes only its isolated candidate workspace on
    both successful comparison and unexpected candidate-validation failure.

    Method: Inject caller-observable standard temporary workspaces for one success and
    one validation failure while leaving repository paths untouched.

    Oracle: ``TemporaryDirectory`` removes its owned path on context exit for both
    normal and exceptional control flow.

    Acceptance: Both recorded workspace paths are absent afterward and representative
    maintained generation bytes remain unchanged.

    Interpretation: Failure identifies leaked candidate artifacts or maintained writes.

    Limitations: Repository-wide deletion is intentionally not exercised.
    """  # noqa: E501
    before = generation_snapshot(control_root)
    success = TemporaryDirectory(dir=tmp_path, prefix="success-")
    success_path = Path(success.name)
    monkeypatch.setattr(
        "ksdft2effmass.harness.pi.local.control.verification.TemporaryDirectory",
        lambda **kwargs: success,
    )
    HarnessControlVerifier().execute(control_root)
    assert success_path.exists() is False
    failure = TemporaryDirectory(dir=tmp_path, prefix="failure-")
    failure_path = Path(failure.name)
    monkeypatch.setattr(
        "ksdft2effmass.harness.pi.local.control.verification.TemporaryDirectory",
        lambda **kwargs: failure,
    )

    def reject(self: Any, generation: Any) -> None:
        raise RuntimeError("injected verification failure")

    monkeypatch.setattr(_HarnessControlGenerationBuilder, "validate", reject)
    with pytest.raises(RuntimeError, match="injected verification failure"):
        HarnessControlVerifier().execute(control_root)
    assert failure_path.exists() is False
    assert generation_snapshot(control_root) == before
