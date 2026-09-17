r"""Software verification of configured Task catalog integration.

Evidence profile: routine

Bounded artifact scope: explicit discovery, source-path preservation and current
Task records through local SQL ingestion and projection.

Facet and represented meaning

Synthetic Tasks and temporary directories exercise three alternate catalog roots.
Literal identities and paths, not prefix classification, are independent oracles.

Intrinsic and cross-object scope

The private reader, immutable observations and SQL projection compose the public
schema-3 Task representation. Canonical Task serialization is a collaborator.

VVUQ and scientific exclusions

Software verification only; no scientific calculation, historical acceptance or
filesystem race elimination is established.
"""

import sqlite3
from pathlib import Path

import pytest
from ksdft2effmass.harness import (
    ArchivedTaskSource,
    HarnessTask,
    HarnessTaskDeserializer,
    HarnessTaskSerializer,
)
from ksdft2effmass.harness.pi.local.dbcontrol.ingestion import (
    _RepositoryControlIngestor,
)
from ksdft2effmass.harness.pi.local.dbcontrol.projections import _ControlProjector
from ksdft2effmass.harness.pi.local.dbcontrol.schema import _SCHEMA
from ksdft2effmass.harness.pi.local.task_catalog import _TaskCatalogReader

pytestmark = pytest.mark.software_verification


class TestTaskCatalogIntegration:
    """Own explicit catalog-to-SQL-to-source agreement."""

    @staticmethod
    def make_task(identity: str, dependencies: tuple[str, ...] = ()) -> HarnessTask:
        return HarnessTask(
            3,
            identity,
            "Synthetic Task",
            "inactive",
            "Synthetic current detail.",
            None,
            dependencies,
            (),
            (),
            True,
            "Verify catalog preservation.",
            ("AGENTS.md",),
            ("Synthetic software inputs only.",),
            ("Exact values survive.",),
            ("No scientific execution.",),
            f"harness/intake/{identity}.md",
            ArchivedTaskSource("archive/source.md", "a" * 64),
            f"docs/{identity}.md",
        )

    @staticmethod
    def create_roots(root: Path) -> tuple[Path, ...]:
        roots = (
            Path("catalogs/questions"),
            Path("catalogs/calculations"),
            Path("catalogs/code"),
        )
        (root / "catalogs/questions").mkdir(parents=True)
        (root / "catalogs/calculations").mkdir(parents=True)
        (root / "catalogs/code").mkdir(parents=True)
        return roots

    @staticmethod
    def write_task(root: Path, path: str, task: HarnessTask) -> None:
        (root / path).write_bytes(HarnessTaskSerializer().execute(task))

    def test_artifact__round_trip__preserves_identity_paths_and_metadata(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: software-verification.task-catalog.integration.round-trip

        Requirement: Current Task values and actual paths survive cross-catalog SQL
        projection without H5 rewriting, flattening or dropped optional metadata.

        Oracle: Two explicit synthetic Tasks and literal independent source paths.

        Acceptance: Projected Tasks equal originals; all paths, relationships and
        optional archive/documentation fields survive, with no legacy alias table.
        """
        roots = self.create_roots(tmp_path)
        historical_name = self.make_task("H5")
        extraction = self.make_task("harness.extraction", ("H5",))
        self.write_task(tmp_path, "catalogs/questions/H5.json", historical_name)
        self.write_task(tmp_path, "catalogs/code/harness.extraction.json", extraction)
        sources = _TaskCatalogReader().execute(tmp_path, roots)
        assert tuple(source.source_path for source in sources) == (
            "catalogs/code/harness.extraction.json",
            "catalogs/questions/H5.json",
        )
        with sqlite3.connect(":memory:") as connection:
            connection.executescript(_SCHEMA)
            _RepositoryControlIngestor(
                connection, tmp_path, [], task_sources=sources
            )._migrate_tasks()
            projections = _ControlProjector(connection, task_roots=roots).render_all()
            assert (
                connection.execute(
                    "SELECT name FROM sqlite_master WHERE name='task_alias'"
                ).fetchall()
                == []
            )
            assert connection.execute(
                "SELECT task_id,source_path FROM task_definition ORDER BY task_id"
            ).fetchall() == [
                ("H5", "catalogs/questions/H5.json"),
                ("harness.extraction", "catalogs/code/harness.extraction.json"),
            ]
        assert (
            HarnessTaskDeserializer().execute(
                projections["catalogs/questions/H5.json"][1]
            )
            == historical_name
        )
        assert (
            HarnessTaskDeserializer().execute(
                projections["catalogs/code/harness.extraction.json"][1]
            )
            == extraction
        )
        assert not any(path.startswith("harness/tasks/") for path in projections)

    def test_artifact__duplicates__rejects_cross_catalog_shadowing(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: software-verification.task-catalog.integration.duplicates

        Requirement: Repeated IDs across categories cannot shadow one another.

        Acceptance: The reader rejects two matching IDs before returning observations.
        """
        roots = self.create_roots(tmp_path)
        task = self.make_task("same")
        self.write_task(tmp_path, "catalogs/questions/same.json", task)
        self.write_task(tmp_path, "catalogs/code/same.json", task)
        with pytest.raises(ValueError, match="duplicate Task identity"):
            _TaskCatalogReader().execute(tmp_path, roots)

    def test_artifact__empty_total__rejects_missing_catalog_content(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: software-verification.task-catalog.integration.empty-total

        Requirement: Empty individual categories are allowed but an empty total is not.

        Acceptance: Three empty directories produce an explicit nonempty-catalog error.
        """
        roots = self.create_roots(tmp_path)
        with pytest.raises(ValueError, match="complete Task catalog must be nonempty"):
            _TaskCatalogReader().execute(tmp_path, roots)

    def test_artifact__missing_root__does_not_fall_back(self, tmp_path: Path) -> None:
        """Evidence ID: software-verification.task-catalog.integration.missing-root

        Requirement: Every configured directory is required, even with Tasks elsewhere.

        Acceptance: A missing category fails instead of accepting the available subset.
        """
        roots = self.create_roots(tmp_path)
        self.write_task(tmp_path, "catalogs/questions/one.json", self.make_task("one"))
        (tmp_path / roots[1]).rmdir()
        with pytest.raises(ValueError, match="resource root"):
            _TaskCatalogReader().execute(tmp_path, roots)

    @pytest.mark.parametrize(
        "directory",
        (
            pytest.param(False, id="record_symlink"),
            pytest.param(True, id="root_symlink"),
        ),
    )
    def test_artifact__symlinks__rejects_indirect_sources(
        self, tmp_path: Path, directory: bool
    ) -> None:
        """Evidence ID: software-verification.task-catalog.integration.symlinks

        Requirement: Catalog roots and Task files cannot redirect through symlinks.

        Acceptance: Both symlink forms are rejected before returning observations.
        """
        roots = self.create_roots(tmp_path)
        if directory:
            (tmp_path / roots[1]).rmdir()
            (tmp_path / roots[1]).symlink_to(
                tmp_path / roots[0], target_is_directory=True
            )
        else:
            target = tmp_path / "outside.json"
            target.write_bytes(HarnessTaskSerializer().execute(self.make_task("one")))
            (tmp_path / roots[0] / "one.json").symlink_to(target)
        with pytest.raises(ValueError, match="symlinks|regular JSON"):
            _TaskCatalogReader().execute(tmp_path, roots)

    @pytest.mark.parametrize(
        "path",
        (
            pytest.param("outside/one.json", id="unselected_root"),
            pytest.param("/outside/one.json", id="absolute_path"),
            pytest.param("catalogs/questions/../one.json", id="parent_traversal"),
            pytest.param("catalogs/questions/other.json", id="identity_mismatch"),
        ),
    )
    def test_artifact__stored_paths__rejects_unsafe_reconstruction(
        self, tmp_path: Path, path: str
    ) -> None:
        """Evidence ID: software-verification.task-catalog.integration.stored-paths

        Requirement: Stored source paths must remain confined to the selected roots
        and retain the exact Task filename rather than becoming arbitrary destinations.

        Acceptance: Each malformed stored-path partition fails projection.
        """
        roots = self.create_roots(tmp_path)
        self.write_task(tmp_path, "catalogs/questions/one.json", self.make_task("one"))
        sources = _TaskCatalogReader().execute(tmp_path, roots)
        with sqlite3.connect(":memory:") as connection:
            connection.executescript(_SCHEMA)
            _RepositoryControlIngestor(
                connection, tmp_path, [], task_sources=sources
            )._migrate_tasks()
            connection.execute("UPDATE task_definition SET source_path=?", (path,))
            with pytest.raises(ValueError):
                _ControlProjector(connection, task_roots=roots).render_all()

    def test_artifact__relationships__rejects_missing_dependency_before_rows(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: software-verification.task-catalog.integration.relationships

        Requirement: Ingestion must not silently drop an unresolved Task dependency.

        Acceptance: Graph rejection occurs before any Task definition is inserted.
        """
        roots = self.create_roots(tmp_path)
        self.write_task(
            tmp_path, "catalogs/questions/one.json", self.make_task("one", ("missing",))
        )
        sources = _TaskCatalogReader().execute(tmp_path, roots)
        with sqlite3.connect(":memory:") as connection:
            connection.executescript(_SCHEMA)
            with pytest.raises(ValueError, match="invalid Task catalog graph"):
                _RepositoryControlIngestor(
                    connection, tmp_path, [], task_sources=sources
                )._migrate_tasks()
            assert (
                connection.execute("SELECT task_id FROM task_definition").fetchall()
                == []
            )
