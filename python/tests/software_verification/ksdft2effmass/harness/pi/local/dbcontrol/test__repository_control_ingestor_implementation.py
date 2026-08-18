r"""Software verification of project-local dbcontrol repository-control-ingestor implementation artifact.

Evidence profile: routine

Bounded artifact scope: project-local dbcontrol private repository-control-ingestor implementation behavior.

Facet and represented meaning

The module owns the intrinsic represented behavior of ``_RepositoryControlIngestor``.

Intrinsic and cross-object scope

Only the owner's bounded contract is exercised with literal or immutable inputs.

VVUQ and scientific exclusions

This is software verification only; scientific validation and UQ are excluded.
"""  # noqa: E501

import sqlite3
from pathlib import Path

import pytest

from ksdft2effmass.harness.pi.local.dbcontrol.ingestion import (
    _RepositoryControlIngestor,
)
from ksdft2effmass.harness.pi.local.dbcontrol.schema import _SCHEMA

SUT = _RepositoryControlIngestor

pytestmark = pytest.mark.software_verification


def test_method__frontmatter__parses_literal_descriptor(tmp_path: Path) -> None:
    """Evidence ID: software-verification.harness.dbcontrol.repository-control-ingestor.method.literal-frontmatter

    Requirement: Repository ingestion recognizes bounded descriptor frontmatter without consuming body prose.

    Method: Parse immutable literal frontmatter and body text.

    Oracle: Only the two colon-delimited lines between exact delimiters are metadata.

    Acceptance: The result equals exactly the two supplied key/value pairs.

    Interpretation: Failure indicates repository descriptor ingestion drift.

    Limitations: Complete repository migration is owned by the migrator evidence.
    """  # noqa: E501
    with sqlite3.connect(":memory:") as connection:
        ingestor = _RepositoryControlIngestor(connection, tmp_path, [])
        assert ingestor._frontmatter(
            "---\nname: demo\nskills: one, two\n---\nBody: ignored\n"
        ) == {"name": "demo", "skills": "one, two"}


def test_method__migrate_tasks__ingests_only_authoritative_task_files(
    tmp_path: Path,
) -> None:
    """Evidence ID: software-verification.harness.dbcontrol.repository-control-ingestor.method.authoritative-task-files

    Requirement: Repository Task ingestion mirrors the authoritative Task directory
    without synthesizing completed legacy Tasks that are absent from that registry.

    Method: Initialize the control schema, supply an empty explicit Task directory,
    migrate Tasks, and inspect the resulting Task definitions.

    Oracle: The empty authoritative directory contains exactly zero Task identities.

    Acceptance: The generated control database contains exactly zero Task definitions.

    Interpretation: Failure indicates that ingestion reintroduces retired Task history.

    Limitations: Schema and relationship validation for retained Tasks are covered by
    separate focused evidence.
    """  # noqa: E501
    task_root = tmp_path / "harness/tasks"
    task_root.mkdir(parents=True)
    with sqlite3.connect(":memory:") as connection:
        connection.executescript(_SCHEMA)
        ingestor = _RepositoryControlIngestor(connection, tmp_path, [])
        ingestor._migrate_tasks()
        rows = connection.execute("SELECT task_id FROM task_definition").fetchall()
        assert rows == []
