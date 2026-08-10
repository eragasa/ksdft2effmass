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
