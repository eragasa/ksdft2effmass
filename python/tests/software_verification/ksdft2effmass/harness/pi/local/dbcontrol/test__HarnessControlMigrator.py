r"""Software verification of ``HarnessControlMigrator``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module owns the intrinsic represented behavior of ``HarnessControlMigrator``.

Intrinsic and cross-object scope

Only the owner's bounded contract is exercised with literal or immutable inputs.

VVUQ and scientific exclusions

This is software verification only; scientific validation and UQ are excluded.
"""

import json
import sqlite3
from pathlib import Path
from textwrap import dedent
from typing import Any

import pytest

from ksdft2effmass.harness.pi.local import (
    HarnessControlMigrationRequest,
    HarnessControlMigrationResult,
    HarnessControlMigrator,
)
from ksdft2effmass.harness.pi.local.dbcontrol.ingestion import (
    _RepositoryControlIngestor,
)
from ksdft2effmass.harness.pi.local.dbcontrol.projections import _ControlProjector

SUT = HarnessControlMigrator

pytestmark = pytest.mark.software_verification


class SyntheticEvidenceFixture:
    """Synthetic explicit-input fixture support outside evidence ownership."""

    @staticmethod
    def write_conforming_module(root: Path, path: str, *, artifact_owned: bool) -> None:
        """Write one synthetic structurally conforming module for migration support."""
        represented = "demo artifact" if artifact_owned else "``migration_request``"
        sut = (
            ""
            if artifact_owned
            else (
                "\n            from ksdft2effmass.harness.pi.local import "
                "HarnessControlMigrationRequest as migration_request\n\n"
                "            SUT = migration_request\n"
            )
        )
        surface = "artifact__inventory" if artifact_owned else "constructor__fields"
        evidence_subject = (
            Path(path).stem.removeprefix("test__").lower().replace("_", "-")
        )
        evidence_id = (
            f"software-verification.synthetic.inventory.{evidence_subject}.is-explicit"
        )
        source = dedent(
            f'''\
            r"""Software verification of {represented}.

            Evidence profile: claim_bearing

            Bounded artifact scope: one synthetic maintained evidence module.

            Facet and represented meaning

            The module owns the represented behavior of {represented}.

            Intrinsic and cross-object scope

            Only the explicit synthetic contract is exercised.

            VVUQ and scientific exclusions

            This is software verification only; scientific validation and UQ are
            excluded.
            """

            import pytest
            {sut}
            pytestmark = pytest.mark.software_verification


            def test_{surface}__is_explicit() -> None:
                """Evidence ID: {evidence_id}

                Requirement: The synthetic module has one explicit maintained evidence
                owner.

                Method: Evaluate an exact literal truth value.

                Oracle: Python defines ``True`` as true.

                Acceptance: The literal is exactly true.

                Interpretation: Failure indicates synthetic fixture drift.

                Limitations: This fixture establishes no production or scientific claim.
                """
                assert True
            '''
        )
        destination = root / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(source)

    @staticmethod
    def write_ownership(root: Path, entries: list[dict[str, str]]) -> Path:
        """Write one closed explicit ownership snapshot and return its relative path."""
        relative = Path("updates/evidence-modules.json")
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps({"schema_version": 1, "modules": entries}))
        return relative

    @staticmethod
    def inventory_entry(path: str, *, artifact_owned: bool = False) -> dict[str, str]:
        """Return one minimal ownership entry accepted by Python conformance."""
        entry = {
            "path": path,
            "mode": "artifact_owned" if artifact_owned else "class_owned",
            "evidence_class": "software_verification",
        }
        entry["artifact" if artifact_owned else "sut"] = (
            "demo artifact" if artifact_owned else "migration_request"
        )
        return entry

    @staticmethod
    def migrate_evidence_only(
        monkeypatch: pytest.MonkeyPatch, root: Path, entries: list[dict[str, str]]
    ) -> HarnessControlMigrationResult:
        """Execute public migration while limiting synthetic ingestion to evidence."""

        def execute_evidence(ingestor: _RepositoryControlIngestor) -> None:
            ingestor._migrate_evidence()

        monkeypatch.setattr(_RepositoryControlIngestor, "execute", execute_evidence)
        profile = Path("harness/pi/evidence/profile.json")
        profile_file = root / profile
        profile_file.parent.mkdir(parents=True, exist_ok=True)
        repository_profile = (
            Path(__file__).resolve().parents[8]
            / "harness/pi/evidence/python-test-evidence-profile-matrix-v1.json"
        )
        profile_file.write_bytes(repository_profile.read_bytes())
        migration = Path("updates/evidence-migration.json")
        migration_file = root / migration
        migration_file.parent.mkdir(parents=True, exist_ok=True)
        migration_file.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "expected_old_node_ids": [],
                    "expected_new_node_ids": [],
                    "mappings": [],
                }
            )
        )
        return HarnessControlMigrator().execute(
            HarnessControlMigrationRequest(
                root.resolve(),
                evidence_profile_matrix_path=profile,
                evidence_module_paths=tuple(Path(entry["path"]) for entry in entries),
                evidence_migration_path=migration,
            )
        )

    @staticmethod
    def authoritative_modules(root: Path) -> list[tuple[str, str, str]]:
        """Read exact module ownership from the authoritative synthetic database."""
        with sqlite3.connect(
            root / "harness/state/harness-control.sqlite3"
        ) as connection:
            return list(
                connection.execute(
                    "SELECT source_path,ownership_kind,owner_subject "
                    "FROM test_module ORDER BY source_path"
                )
            )

    @staticmethod
    def projected_modules(root: Path) -> list[dict[str, Any]]:
        """Read generated module projection entries from the synthetic root."""
        document = json.loads(
            (root / ".pi/evidence/python-conformance/module-inventory.json").read_text()
        )
        return document["modules"]

    @staticmethod
    def generation_bytes(
        root: Path, projection_paths: tuple[str, ...]
    ) -> dict[str, bytes]:
        """Read one complete published synthetic generation."""
        paths = (
            "harness/state/harness-control.sqlite3",
            "harness/state/harness-control.sql",
            "harness/state/projection-manifest.json",
            *projection_paths,
        )
        return {path: (root / path).read_bytes() for path in paths}


def test_method__execute_wrong_request_type__raises_type_error() -> None:
    """Evidence ID: software-verification.harness.sqlite-control.migration-action.wrong-request-type-raises-type-error

    Requirement: The migration ActionObject rejects values outside its request contract.

    Method: Call public ``execute`` with a plain object.

    Oracle: The public signature requires ``HarnessControlMigrationRequest`` exactly.

    Acceptance: The call raises exactly ``TypeError`` before filesystem mutation.

    Interpretation: Failure indicates a weakened structured-write boundary.

    Limitations: Valid migration is covered separately.
    """  # noqa: E501
    with pytest.raises(TypeError):
        HarnessControlMigrator().execute(object())  # type: ignore[arg-type]


def test_method__execute_valid_literal_corpus__writes_authority_and_projection(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.migration-action.valid-literal-corpus

    Requirement: A valid migration writes SQLite authority, deterministic SQL, declared projection bytes, and manifest metadata and returns their paths.

    Method: Execute the public Action at an isolated absolute root while repository ingestion supplies an empty valid catalog and projection supplies one immutable literal artifact.

    Oracle: The independently supplied projection is exactly ``b"literal\n"`` at ``generated/literal.txt``.

    Acceptance: Result schema is three, the database and SQL exist, projection bytes match exactly, its path is returned, and manifest names the path.

    Interpretation: Failure indicates valid-path migration orchestration or write-boundary drift.

    Limitations: Full repository discovery is excluded; constituent ingestion has separate focused evidence.
    """  # noqa: E501
    observed: list[object] = []

    def execute_empty(ingestor: _RepositoryControlIngestor) -> None:
        observed.append(ingestor.module_inventory)

    monkeypatch.setattr(_RepositoryControlIngestor, "execute", execute_empty)
    monkeypatch.setattr(
        _ControlProjector,
        "render_all",
        lambda self: {"generated/literal.txt": ("task-json", b"literal\n")},
    )
    result = HarnessControlMigrator().execute(
        HarnessControlMigrationRequest(tmp_path.resolve())
    )
    assert observed == [()]
    assert result.schema_version == 3
    assert result.projection_paths == ("generated/literal.txt",)
    assert (tmp_path / "harness/state/harness-control.sqlite3").is_file()
    assert (tmp_path / "harness/state/harness-control.sql").is_file()
    assert (tmp_path / "generated/literal.txt").read_bytes() == b"literal\n"
    assert (
        b"generated/literal.txt"
        in (tmp_path / "harness/state/projection-manifest.json").read_bytes()
    )


def test_method__execute_ownership_symlink_escape__preserves_published_generation(
    tmp_path: Path,
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.migration-action.ownership-symlink-escape-preserves-published-generation

    Requirement: An ownership input whose repository-relative symlink resolves outside the explicit root is rejected before authoritative outputs change.

    Method: Retain literal authoritative SQL bytes, create an in-root ownership symlink to a sibling file, and invoke the public migration Action.

    Oracle: Resolved-path containment excludes the sibling target from the repository root.

    Acceptance: The call raises ``ValueError`` and the retained authoritative bytes remain exact.

    Interpretation: Failure indicates a root-confinement or pre-publication validation regression.

    Limitations: Platforms without symlink support are not represented by this POSIX repository environment.
    """  # noqa: E501
    authoritative = tmp_path / "harness/state/harness-control.sql"
    authoritative.parent.mkdir(parents=True)
    authoritative.write_bytes(b"previous-generation\n")
    external = tmp_path.parent / f"{tmp_path.name}-external-ownership.json"
    external.write_text('{"schema_version":1,"modules":[]}')
    link = tmp_path / "updates/modules.json"
    link.parent.mkdir(parents=True)
    link.symlink_to(external)
    with pytest.raises(ValueError, match="not root-confined"):
        HarnessControlMigrator().execute(
            HarnessControlMigrationRequest(
                tmp_path.resolve(),
                evidence_module_ownership_path=Path("updates/modules.json"),
            )
        )
    assert authoritative.read_bytes() == b"previous-generation\n"


def test_method__execute_invalid_ownership_snapshots__preserve_published_generation(
    tmp_path: Path,
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.migration-action.invalid-ownership-snapshots-preserve-published-generation

    Requirement: Malformed JSON and structurally nonconforming explicit ownership snapshots are rejected before authoritative outputs change.

    Method: Invoke the public migration first with malformed JSON and then with a closed ownership document whose named module violates Python conformance.

    Oracle: JSON decoding and ``PythonConformanceValidator`` independently reject the two explicit inputs.

    Acceptance: Both calls raise ``ValueError`` and retained authoritative SQL bytes remain exact after each rejection.

    Interpretation: Failure indicates validation after publication or weakened ownership metadata enforcement.

    Limitations: Valid reconciliation behavior is covered separately.
    """  # noqa: E501
    authoritative = tmp_path / "harness/state/harness-control.sql"
    authoritative.parent.mkdir(parents=True)
    authoritative.write_bytes(b"previous-generation\n")
    ownership = tmp_path / "updates/modules.json"
    ownership.parent.mkdir(parents=True)
    ownership.write_text("{malformed")
    request = HarnessControlMigrationRequest(
        tmp_path.resolve(), evidence_module_ownership_path=Path("updates/modules.json")
    )
    with pytest.raises(ValueError, match="projection-only"):
        HarnessControlMigrator().execute(request)
    assert authoritative.read_bytes() == b"previous-generation\n"
    module_path = "python/tests/test__invalid_snapshot.py"
    module = tmp_path / module_path
    module.parent.mkdir(parents=True)
    module.write_text("def test_artifact__snapshot__is_invalid(): pass\n")
    ownership.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "modules": [
                    SyntheticEvidenceFixture.inventory_entry(
                        module_path, artifact_owned=True
                    )
                ],
            }
        )
    )
    with pytest.raises(ValueError, match="projection-only"):
        HarnessControlMigrator().execute(request)
    assert authoritative.read_bytes() == b"previous-generation\n"


def test_method__execute_explicit_ownership_addition__updates_authority_and_projection(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.migration-action.explicit-ownership-addition-updates-authority-and-projection

    Requirement: An explicit validated ownership snapshot can add maintained evidence modules transactionally and regenerate SQLite, deterministic SQL, and the inventory projection.

    Method: Migrate a synthetic root from an explicit two-module ownership snapshot while bounded ingestion processes only those modules.

    Oracle: The caller-supplied closed snapshot names exactly two artifact-owned paths and owners.

    Acceptance: Authoritative SQLite and the generated projection contain exactly both entries, and deterministic SQL names both paths.

    Interpretation: Failure indicates that additions still require generated-file editing or ad-hoc database mutation.

    Limitations: Other repository catalogs are intentionally excluded from this isolated software-verification fixture.
    """  # noqa: E501
    paths = ["python/tests/test__alpha.py", "python/tests/test__beta.py"]
    SyntheticEvidenceFixture.write_conforming_module(
        tmp_path, paths[0], artifact_owned=True
    )
    SyntheticEvidenceFixture.write_conforming_module(
        tmp_path, paths[1], artifact_owned=True
    )
    SyntheticEvidenceFixture.migrate_evidence_only(
        monkeypatch,
        tmp_path,
        [
            SyntheticEvidenceFixture.inventory_entry(path, artifact_owned=True)
            for path in paths
        ],
    )
    assert SyntheticEvidenceFixture.authoritative_modules(tmp_path) == [
        (path, "artifact_owned", "demo artifact") for path in paths
    ]
    assert [
        entry["path"] for entry in SyntheticEvidenceFixture.projected_modules(tmp_path)
    ] == paths
    sql = (tmp_path / "harness/state/harness-control.sql").read_text()
    assert all(path in sql for path in paths)


def test_method__execute_publish_failure__restores_complete_previous_generation(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.migration-action.publish-failure-restores-complete-previous-generation

    Requirement: All authoritative database, SQL, projection, and manifest outputs are staged and verified before publication, and an individual replacement failure restores the complete previous generation.

    Method: Publish one valid explicit ownership generation, inject one failure during the second staged-file replacement for a changed generation, and reread every prior output.

    Oracle: The exact byte snapshot returned by the first successful public migration is independent of the second generation.

    Acceptance: The second call raises the documented rollback error and every previously published output remains byte-identical.

    Interpretation: Failure indicates a mixed or incomplete published control generation after replacement failure.

    Limitations: This verifies rollback after an injected process-level replacement failure, not filesystem-wide multi-file atomicity across crashes or power loss.
    """  # noqa: E501
    alpha = "python/tests/test__alpha.py"
    beta = "python/tests/test__beta.py"
    SyntheticEvidenceFixture.write_conforming_module(
        tmp_path, alpha, artifact_owned=True
    )
    SyntheticEvidenceFixture.write_conforming_module(
        tmp_path, beta, artifact_owned=True
    )
    result = SyntheticEvidenceFixture.migrate_evidence_only(
        monkeypatch,
        tmp_path,
        [SyntheticEvidenceFixture.inventory_entry(alpha, artifact_owned=True)],
    )
    projection_paths = result.projection_paths
    previous = SyntheticEvidenceFixture.generation_bytes(tmp_path, projection_paths)
    original_replace = Path.replace
    staged_replacements = 0

    def fail_second_staged_replace(source: Path, target: Path) -> Path:
        nonlocal staged_replacements
        if source.name.endswith(".harness-control-staged"):
            staged_replacements += 1
            if staged_replacements == 2:
                raise OSError("injected publish failure")
        return original_replace(source, target)

    monkeypatch.setattr(Path, "replace", fail_second_staged_replace)
    with pytest.raises(RuntimeError, match="previous generation restored"):
        SyntheticEvidenceFixture.migrate_evidence_only(
            monkeypatch,
            tmp_path,
            [
                SyntheticEvidenceFixture.inventory_entry(alpha, artifact_owned=True),
                SyntheticEvidenceFixture.inventory_entry(beta, artifact_owned=True),
            ],
        )
    assert (
        SyntheticEvidenceFixture.generation_bytes(tmp_path, projection_paths)
        == previous
    )


def test_method__execute_explicit_ownership_removal_and_move__reconciles_snapshot(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.migration-action.explicit-ownership-removal-and-move-reconciles-snapshot

    Requirement: Replacing the explicit ownership snapshot can remove one module and move another without direct SQLite transactions.

    Method: Migrate an initial two-module snapshot, then migrate a snapshot containing only the moved path.

    Oracle: A closed ownership snapshot defines the complete desired maintained-module set rather than an append-only patch.

    Acceptance: SQLite, SQL, and projection contain only the moved path after the second public migration.

    Interpretation: Failure indicates stale module retention or a nontransactional reconciliation boundary.

    Limitations: Evidence-identity migration maps are outside this ownership-inventory test.
    """  # noqa: E501
    removed = "python/tests/test__removed.py"
    old = "python/tests/test__before_move.py"
    moved = "python/tests/moved/test__after_move.py"
    SyntheticEvidenceFixture.write_conforming_module(
        tmp_path, removed, artifact_owned=True
    )
    SyntheticEvidenceFixture.write_conforming_module(tmp_path, old, artifact_owned=True)
    SyntheticEvidenceFixture.write_conforming_module(
        tmp_path, moved, artifact_owned=True
    )
    SyntheticEvidenceFixture.migrate_evidence_only(
        monkeypatch,
        tmp_path,
        [
            SyntheticEvidenceFixture.inventory_entry(removed, artifact_owned=True),
            SyntheticEvidenceFixture.inventory_entry(old, artifact_owned=True),
        ],
    )
    SyntheticEvidenceFixture.migrate_evidence_only(
        monkeypatch,
        tmp_path,
        [SyntheticEvidenceFixture.inventory_entry(moved, artifact_owned=True)],
    )
    assert SyntheticEvidenceFixture.authoritative_modules(tmp_path) == [
        (moved, "artifact_owned", "demo artifact")
    ]
    assert [
        entry["path"] for entry in SyntheticEvidenceFixture.projected_modules(tmp_path)
    ] == [moved]
    sql = (tmp_path / "harness/state/harness-control.sql").read_text()
    assert moved in sql
    assert removed not in sql
    assert old not in sql


def test_method__execute_explicit_ownership_mode_change__reconciles_owner_kind(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.migration-action.explicit-ownership-mode-change-reconciles-owner-kind

    Requirement: An explicit ownership snapshot can replace class ownership with artifact ownership for an existing module path.

    Method: Migrate the path as class-owned, replace its source with an artifact-owned conforming module, and migrate the new ownership snapshot.

    Oracle: The second closed snapshot declares ``artifact_owned`` and the concrete owner ``demo artifact``.

    Acceptance: SQLite and the generated projection contain exactly the artifact ownership kind and subject after migration.

    Interpretation: Failure indicates stale ownership mode or subject state in authoritative control data.

    Limitations: This structural test makes no claim about scientific evidence classification.
    """  # noqa: E501
    path = "python/tests/test__migration_request.py"
    SyntheticEvidenceFixture.write_conforming_module(
        tmp_path, path, artifact_owned=False
    )
    SyntheticEvidenceFixture.migrate_evidence_only(
        monkeypatch, tmp_path, [SyntheticEvidenceFixture.inventory_entry(path)]
    )
    SyntheticEvidenceFixture.write_conforming_module(
        tmp_path, path, artifact_owned=True
    )
    SyntheticEvidenceFixture.migrate_evidence_only(
        monkeypatch,
        tmp_path,
        [SyntheticEvidenceFixture.inventory_entry(path, artifact_owned=True)],
    )
    assert SyntheticEvidenceFixture.authoritative_modules(tmp_path) == [
        (path, "artifact_owned", "demo artifact")
    ]
    assert (
        SyntheticEvidenceFixture.projected_modules(tmp_path)[0]["mode"]
        == "artifact_owned"
    )
    assert (
        SyntheticEvidenceFixture.projected_modules(tmp_path)[0]["artifact"]
        == "demo artifact"
    )


def test_method__execute_canonical_corpus__reads_and_parses_each_source_once(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.migrator.single-corpus

    Requirement: One migration operation reads each evidence source exactly once,
    parses it exactly once, and reuses its immutable bytes and extracted facts during
    ingestion.

    Method: Count reads of one synthetic source and calls to the parser AST boundary
    while executing the canonical evidence-only migration path.

    Oracle: The bounded R2.3 corpus contract fixes both counts at exactly one.

    Acceptance: Migration succeeds and both observed counts equal one.

    Interpretation: Failure identifies a duplicate corpus build, source reread, or
    duplicate AST parse.

    Limitations: Profile and predecessor-map reads are separate explicit inputs.
    """
    path = "python/tests/test__demo_artifact.py"
    SyntheticEvidenceFixture.write_conforming_module(
        tmp_path, path, artifact_owned=True
    )
    entries = [SyntheticEvidenceFixture.inventory_entry(path, artifact_owned=True)]
    source_path = (tmp_path / path).resolve()
    original_read = Path.read_bytes
    reads = 0

    def counted_read(candidate: Path) -> bytes:
        nonlocal reads
        if candidate.resolve() == source_path:
            reads += 1
        return original_read(candidate)

    from ksdft2effmass.harness.pi.evidence.python_conformance import parser

    original_parse = parser.ast.parse
    parses = 0

    def counted_parse(*args: Any, **kwargs: Any) -> Any:
        nonlocal parses
        parses += 1
        return original_parse(*args, **kwargs)

    monkeypatch.setattr(Path, "read_bytes", counted_read)
    monkeypatch.setattr(parser.ast, "parse", counted_parse)
    SyntheticEvidenceFixture.migrate_evidence_only(monkeypatch, tmp_path, entries)
    assert (reads, parses) == (1, 1)
