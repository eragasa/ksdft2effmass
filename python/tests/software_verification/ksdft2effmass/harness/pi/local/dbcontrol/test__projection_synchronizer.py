r"""Software verification of ``_HarnessProjectionSynchronizer``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module owns the intrinsic represented behavior of
``_HarnessProjectionSynchronizer``.

Intrinsic and cross-object scope

Only the owner's bounded contract is exercised with literal or immutable inputs.

VVUQ and scientific exclusions

This is software verification only; scientific validation and UQ are excluded.
"""

import json
import shutil
import sqlite3
from pathlib import Path
from textwrap import dedent
from typing import Any

import pytest

from ksdft2effmass.harness.pi import (
    PiHarnessConfiguration,
    PiHarnessConfigurationDeserializer,
)
from ksdft2effmass.harness.pi.local.dbcontrol.ingestion import (
    _RepositoryControlIngestor,
)
from ksdft2effmass.harness.pi.local.dbcontrol.migration import (
    _HarnessProjectionSynchronizer,
)
from ksdft2effmass.harness.pi.local.dbcontrol.projections import _ControlProjector
from ksdft2effmass.harness.pi.local.dbcontrol.records import (
    _HarnessProjectionRequest,
    _HarnessProjectionSyncResult,
)

SUT = _HarnessProjectionSynchronizer

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
                "\n            from "
                "ksdft2effmass.harness.pi.local.dbcontrol.records import "
                "_HarnessProjectionRequest as migration_request\n\n"
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
    def expected_module(path: str, *, artifact_owned: bool = False) -> dict[str, str]:
        """Return one minimal expected module accepted by Python conformance."""
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
        monkeypatch: pytest.MonkeyPatch,
        root: Path,
        expected_modules: list[dict[str, str]],
    ) -> _HarnessProjectionSyncResult:
        """Execute private migration while limiting synthetic ingestion to evidence."""

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
        return _HarnessProjectionSynchronizer().execute(
            _HarnessProjectionRequest(
                root.resolve(),
                evidence_profile_matrix_path=profile,
                evidence_module_paths=tuple(
                    Path(expected_module["path"])
                    for expected_module in expected_modules
                ),
                evidence_migration_path=migration,
            )
        )

    @staticmethod
    def migrate_agents_only(
        monkeypatch: pytest.MonkeyPatch, root: Path
    ) -> _HarnessProjectionSyncResult:
        """Execute private migration with only synthetic agent ingestion enabled."""

        def execute_agents(ingestor: _RepositoryControlIngestor) -> None:
            ingestor._migrate_agents_and_skills()

        monkeypatch.setattr(_RepositoryControlIngestor, "execute", execute_agents)
        settings_path = root / ".pi/settings.json"
        configuration = (
            PiHarnessConfigurationDeserializer().execute(settings_path.read_bytes())
            if settings_path.exists()
            else PiHarnessConfiguration(1, ())
        )
        return _HarnessProjectionSynchronizer().execute(
            _HarnessProjectionRequest(
                root.resolve(), pi_harness_configuration=configuration
            )
        )

    @staticmethod
    def write_agent(
        root: Path,
        name: str,
        *,
        package: str = "example",
        acceptance_role: str = "writer",
    ) -> None:
        """Write one minimal synthetic Pi agent descriptor."""
        destination = root / ".pi/agents" / f"{name}.md"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            dedent(
                f"""\
                ---
                name: {name}
                package: {package}
                acceptanceRole: {acceptance_role}
                ---
                """
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


def make_canonical_resource_request(tmp_path: Path) -> _HarnessProjectionRequest:
    """Evidence ID: Owns no identifier; supports canonical resource migration evidence.

    Requirement: Canonical resource migration tests receive one isolated complete
    control-input tree without mutating repository-owned state.

    Method: Copy maintained harness control, agent, skill, and checkpoint inputs and
    construct a request naming every canonical resource path.

    Oracle: The maintained control roots and fixed request fields define the fixture.

    Acceptance: Return one immutable request rooted at the isolated directory.

    Interpretation: Failure indicates invalid fixture setup, not migrator behavior.

    Limitations: The helper owns no evidence identity or product behavior.
    """
    repository = Path(__file__).resolve().parents[8]
    shutil.copytree(repository / "harness", tmp_path / "harness")
    shutil.copytree(repository / ".pi/agents", tmp_path / ".pi/agents")
    shutil.copytree(repository / ".pi/checkpoints", tmp_path / ".pi/checkpoints")
    shutil.copytree(repository / ".pi/skills", tmp_path / ".pi/skills")
    shutil.copytree(repository / ".agents/skills", tmp_path / ".agents/skills")
    return _HarnessProjectionRequest(
        tmp_path.resolve(),
        resource_profile_path=Path("harness/local/profiles/ksdft2effmass-v2.json"),
        generic_resource_manifest_path=Path("harness/pi/resource-manifest.json"),
        generic_resource_root_path=Path("harness/pi"),
        local_resource_manifest_path=Path("harness/local/resource-manifest.json"),
        local_resource_root_path=Path("harness/local"),
    )


def test_method__execute_canonical_resources__participate_in_full_reconstruction(
    tmp_path: Path,
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.migration-action.canonical-resources-participate-in-full-reconstruction

    Requirement: Explicit canonical resources participate in the same complete control
    reconstruction that ingests Tasks, agents, skills, decisions, and projections.

    Method: Copy a bounded complete repository-control fixture, replace only external
    pytest collection with an empty successful observation, and execute the private
    projection synchronizer without replacing or narrowing repository ingestion.

    Oracle: The input manifests enumerate the expected resources, while the other
    copied control catalogs independently require nonempty Task, agent, skill, and
    decision rows.

    Acceptance: The result and SQLite contain exactly the resources enumerated by the
    two disjoint input manifests and nonempty rows for every other copied control
    domain, and both projected manifests equal their input bytes.

    Interpretation: Failure indicates resources use a partial or separate construction
    route rather than the complete full-control migration.

    Limitations: The isolated request intentionally supplies no evidence modules, so
    the source-derived node projection is empty.
    """  # noqa: E501
    request = make_canonical_resource_request(tmp_path)
    expected_generic = (tmp_path / "harness/pi/resource-manifest.json").read_bytes()
    expected_local = (tmp_path / "harness/local/resource-manifest.json").read_bytes()
    generic_resources = json.loads(expected_generic)["resources"]
    local_resources = json.loads(expected_local)["resources"]
    generic_resource_ids = {resource["resource_id"] for resource in generic_resources}
    local_resource_ids = {resource["resource_id"] for resource in local_resources}
    assert generic_resource_ids.isdisjoint(local_resource_ids)
    expected_resource_count = len(generic_resources) + len(local_resources)

    result = _HarnessProjectionSynchronizer().execute(request)
    counts = dict(result.counts)
    assert counts["resource_definition"] == expected_resource_count
    assert counts["task_definition"] > 0
    assert counts["agent_definition"] > 0
    assert counts["skill_definition"] > 0
    assert counts["decision_reference"] > 0
    assert counts["projection_record"] > 0
    assert (
        tmp_path / "harness/pi/resource-manifest.json"
    ).read_bytes() == expected_generic
    assert (
        tmp_path / "harness/local/resource-manifest.json"
    ).read_bytes() == expected_local


def test_method__execute_resource_hash_mismatch__preserves_published_generation(
    tmp_path: Path,
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.migration-action.resource-hash-mismatch-preserves-generation

    Requirement: A manifest/source identity mismatch is rejected before any artifact
    in a complete previously published control generation changes.

    Method: Publish one full isolated generation, snapshot its database, SQL, manifest,
    and every projection, alter one declared generic source, and migrate again.

    Oracle: The manifest-declared SHA-256 and changed source bytes disagree exactly,
    while the independent byte snapshot fixes the complete retained generation.

    Acceptance: The second call raises ``ValueError`` naming hash mismatch and every
    previously published generation artifact remains byte-identical.

    Interpretation: Failure indicates live hash substitution or prevalidation writes.

    Limitations: Filesystem-level failure during publication is covered separately.
    """  # noqa: E501
    request = make_canonical_resource_request(tmp_path)

    published = _HarnessProjectionSynchronizer().execute(request)
    retained = SyntheticEvidenceFixture.generation_bytes(
        tmp_path, published.projection_paths
    )
    changed = tmp_path / "harness/pi/skills/develop-harness-resources/SKILL.md"
    changed.write_bytes(changed.read_bytes() + b"\nchanged\n")
    with pytest.raises(ValueError, match="HASH_MISMATCH"):
        _HarnessProjectionSynchronizer().execute(request)
    assert (
        SyntheticEvidenceFixture.generation_bytes(tmp_path, published.projection_paths)
        == retained
    )


def test_method__execute_agent_settings__projects_exact_enabled_roles(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Evidence ID: software-verification.harness.agent-settings.enabled-projection

    Requirement: Control migration derives repository-declared agent enablement from
    exact package-qualified project overrides without importing runtime observations.

    Method: Migrate three synthetic descriptors with one exact disabled override, one
    wrong-package override, and one disabled override for an absent historical role.

    Oracle: Pi project override identity is the exact ``package.name`` pair; only the
    matching present descriptor is disabled and absent descriptors create no row.

    Acceptance: SQLite contains exactly the three descriptors in identity order with
    enabled values ``1, 0, 1`` for the unoverridden, exactly disabled, and
    wrong-package cases respectively.

    Interpretation: Failure indicates settings are ignored, identities are matched
    loosely, or runtime configuration is being projected as nonexistent roles.

    Limitations: The synthetic test does not invoke Pi or establish runtime discovery,
    Task authority, scientific validity, or UQ.
    """
    SyntheticEvidenceFixture.write_agent(tmp_path, "alpha")
    SyntheticEvidenceFixture.write_agent(tmp_path, "beta")
    SyntheticEvidenceFixture.write_agent(tmp_path, "gamma")
    settings = {
        "subagents": {
            "agentOverrides": {
                "example.beta": {"disabled": True},
                "other.gamma": {"disabled": True},
                "example.retired": {"disabled": True},
            }
        }
    }
    settings_path = tmp_path / ".pi/settings.json"
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    settings_path.write_text(json.dumps(settings))

    SyntheticEvidenceFixture.migrate_agents_only(monkeypatch, tmp_path)

    with sqlite3.connect(
        tmp_path / "harness/state/harness-control.sqlite3"
    ) as connection:
        rows = list(
            connection.execute(
                "SELECT agent_id,enabled FROM agent_definition ORDER BY agent_id"
            )
        )
    assert rows == [("alpha", 1), ("beta", 0), ("gamma", 1)]


def test_method__execute_wrong_request_type__raises_type_error() -> None:
    """Evidence ID: software-verification.harness.sqlite-control.migration-action.wrong-request-type-raises-type-error

    Requirement: The migration ActionObject rejects values outside its request contract.

    Method: Call private ``execute`` with a plain object.

    Oracle: The private signature requires ``_HarnessProjectionRequest`` exactly.

    Acceptance: The call raises exactly ``TypeError`` before filesystem mutation.

    Interpretation: Failure indicates a weakened structured-write boundary.

    Limitations: Valid migration is covered separately.
    """  # noqa: E501
    with pytest.raises(TypeError):
        _HarnessProjectionSynchronizer().execute(object())  # type: ignore[arg-type]


def test_method__execute_valid_literal_corpus__writes_authority_and_projection(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.migration-action.valid-literal-corpus

    Requirement: A valid migration writes SQLite authority, deterministic SQL, declared projection bytes, and manifest metadata and returns their paths.

    Method: Execute the private Action at an isolated absolute root while repository ingestion supplies an empty valid catalog and projection supplies one immutable literal artifact.

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
    result = _HarnessProjectionSynchronizer().execute(
        _HarnessProjectionRequest(tmp_path.resolve())
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


def test_method__execute_source_corpus_addition__updates_authority_and_projection(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.migration-action.explicit-ownership-addition-updates-authority-and-projection

    Requirement: Source-declared ownership can add maintained evidence modules transactionally and regenerate SQLite, deterministic SQL, and the inventory projection.

    Method: Migrate a synthetic root from two source modules with embedded ownership declarations while bounded ingestion processes only those modules.

    Oracle: The two source modules independently declare exact artifact-owned paths and owners.

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
            SyntheticEvidenceFixture.expected_module(path, artifact_owned=True)
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

    Oracle: The exact byte snapshot returned by the first successful private migration is independent of the second generation.

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
        [SyntheticEvidenceFixture.expected_module(alpha, artifact_owned=True)],
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
                SyntheticEvidenceFixture.expected_module(alpha, artifact_owned=True),
                SyntheticEvidenceFixture.expected_module(beta, artifact_owned=True),
            ],
        )
    assert (
        SyntheticEvidenceFixture.generation_bytes(tmp_path, projection_paths)
        == previous
    )


def test_method__execute_source_corpus_removal_and_move__reconciles_snapshot(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.migration-action.explicit-ownership-removal-and-move-reconciles-snapshot

    Requirement: Replacing the source corpus can remove one module and move another without direct SQLite transactions.

    Method: Migrate an initial two-module snapshot, then migrate a snapshot containing only the moved path.

    Oracle: The explicit source corpus defines the complete desired maintained-module set rather than an append-only patch.

    Acceptance: SQLite, SQL, and projection contain only the moved path after the second private migration.

    Interpretation: Failure indicates stale module retention or a nontransactional reconciliation boundary.

    Limitations: Evidence-identity migration maps are outside this source-corpus test.
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
            SyntheticEvidenceFixture.expected_module(removed, artifact_owned=True),
            SyntheticEvidenceFixture.expected_module(old, artifact_owned=True),
        ],
    )
    SyntheticEvidenceFixture.migrate_evidence_only(
        monkeypatch,
        tmp_path,
        [SyntheticEvidenceFixture.expected_module(moved, artifact_owned=True)],
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


def test_method__execute_source_declared_ownership_kind_change__reconciles_owner_kind(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.migration-action.explicit-ownership-mode-change-reconciles-owner-kind

    Requirement: An source corpus can replace class ownership with artifact ownership for an existing module path.

    Method: Migrate the path as class-owned, replace its source with an artifact-owned conforming module, and migrate the new source corpus.

    Oracle: The second source declaration specifies ``artifact_owned`` and the concrete owner ``demo artifact``.

    Acceptance: SQLite and the generated projection contain exactly the artifact ownership kind and subject after migration.

    Interpretation: Failure indicates stale ownership mode or subject state in authoritative control data.

    Limitations: This structural test makes no claim about scientific evidence classification.
    """  # noqa: E501
    path = "python/tests/test__migration_request.py"
    SyntheticEvidenceFixture.write_conforming_module(
        tmp_path, path, artifact_owned=False
    )
    SyntheticEvidenceFixture.migrate_evidence_only(
        monkeypatch, tmp_path, [SyntheticEvidenceFixture.expected_module(path)]
    )
    SyntheticEvidenceFixture.write_conforming_module(
        tmp_path, path, artifact_owned=True
    )
    SyntheticEvidenceFixture.migrate_evidence_only(
        monkeypatch,
        tmp_path,
        [SyntheticEvidenceFixture.expected_module(path, artifact_owned=True)],
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
    expected_modules = [
        SyntheticEvidenceFixture.expected_module(path, artifact_owned=True)
    ]
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
    SyntheticEvidenceFixture.migrate_evidence_only(
        monkeypatch, tmp_path, expected_modules
    )
    assert (reads, parses) == (1, 1)
