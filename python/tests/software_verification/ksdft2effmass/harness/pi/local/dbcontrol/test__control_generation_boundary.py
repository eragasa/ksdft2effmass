r"""Software verification of private generation and public sole-publication agreement.

Evidence profile: claim_bearing

Bounded artifact scope: private generation and public sole-publication agreement.

Facet and represented meaning

The module owns the architectural agreement between isolated complete candidate
construction and public migration publication.

Intrinsic and cross-object scope

The artifact-owned tests compare candidate and published representations and verify
validation ordering without treating private classes as public systems under test.

VVUQ and scientific exclusions

This is structural software verification only. Pytest success does not establish
numerical verification, scientific validation, uncertainty quantification, protected
execution, or human acceptance.
"""

import sqlite3
from pathlib import Path

import pytest

from ksdft2effmass.harness.pi.local import (
    HarnessControlMigrationRequest,
    HarnessControlMigrator,
)
from ksdft2effmass.harness.pi.local.control.generation import (
    _HarnessControlGenerationBuilder,
)
from ksdft2effmass.harness.pi.local.dbcontrol.database import _ControlDatabase
from ksdft2effmass.harness.pi.local.dbcontrol.ingestion import (
    _RepositoryControlIngestor,
)
from ksdft2effmass.harness.pi.local.dbcontrol.projections import _ControlProjector

pytestmark = pytest.mark.software_verification


def configure_literal_generation(monkeypatch: pytest.MonkeyPatch) -> None:
    """Evidence ID: Owns no identifier; supports bounded generation fixtures.

    Requirement: Generation tests isolate catalog ingestion from orchestration.

    Method: Replace ingestion and projection with one literal complete projection.

    Oracle: The fixture contract defines one exact literal projection.

    Acceptance: Both collaborators are replaced for the calling test lifetime.

    Interpretation: Failure indicates fixture setup drift.

    Limitations: This helper establishes no independent product claim.
    """
    monkeypatch.setattr(_RepositoryControlIngestor, "execute", lambda self: None)
    monkeypatch.setattr(
        _ControlProjector,
        "render_all",
        lambda self: {"generated/literal.txt": ("task-json", b"literal\n")},
    )


def semantic_digest(path: Path) -> str:
    """Evidence ID: Owns no identifier; reads synthetic semantic identity.

    Requirement: Tests compare SQLite by represented table content, not file bytes.

    Method: Open one synthetic database and invoke its normalized semantic reader.

    Oracle: The accepted control database identity excludes its stored digest field.

    Acceptance: Return the reader's exact normalized digest.

    Interpretation: Failure indicates invalid synthetic fixture state.

    Limitations: This helper establishes no independent product claim.
    """
    with sqlite3.connect(path) as connection:
        return _ControlDatabase(connection).normalized_semantic_digest()


def test_artifact__generation__candidate_and_publication_are_equivalent(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.generation-boundary.candidate-publication-equivalence

    Requirement: The private builder and public migrator use one complete generation
    algorithm whose database semantics, canonical SQL, manifest, and projections agree.

    Method: Build one isolated literal candidate, then migrate the same noncanonical
    request through the public facade and compare every represented artifact.

    Oracle: The candidate descriptor fixes exact SQL, manifest, and projection bytes;
    normalized SQLite table content independently defines database semantic identity.

    Acceptance: Semantic digests and every non-SQLite artifact are exactly equal, and
    the custom repository-relative database destination is published.

    Interpretation: Failure identifies a second construction path or representation
    change between candidate generation and publication.

    Limitations: The bounded fixture excludes repository catalog discovery and physical
    filesystem crash atomicity.
    """  # noqa: E501
    configure_literal_generation(monkeypatch)
    repository = tmp_path / "repository"
    workspace = tmp_path / "workspace"
    repository.mkdir()
    workspace.mkdir()
    request = HarnessControlMigrationRequest(
        repository.resolve(), database_path=Path("custom/control.sqlite3")
    )
    generation = _HarnessControlGenerationBuilder().execute(
        request, workspace.resolve()
    )
    _HarnessControlGenerationBuilder().validate(generation)
    candidate = dict(generation.artifacts)
    result = HarnessControlMigrator().execute(request)
    assert result.semantic_digest == generation.semantic_digest
    assert semantic_digest(repository / request.database_path) == semantic_digest(
        generation.database_path
    )
    assert (repository / "harness/state/harness-control.sql").read_bytes() == (
        candidate[Path("harness/state/harness-control.sql")].read_bytes()
    )
    assert (repository / "harness/state/projection-manifest.json").read_bytes() == (
        candidate[Path("harness/state/projection-manifest.json")].read_bytes()
    )
    assert (repository / "generated/literal.txt").read_bytes() == b"literal\n"
    assert (repository / request.database_path).is_file()


def test_artifact__generation__builder_writes_only_to_owned_workspace(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.generation-boundary.builder-nonpublication

    Requirement: Private candidate generation has no maintained publication authority.

    Method: Snapshot an empty explicit repository, build a candidate in a sibling
    workspace, and inspect both trees before invoking the public migrator.

    Oracle: The request identifies the repository source root while the builder's
    explicit workspace identifies every permissible output location.

    Acceptance: The repository remains empty and every descriptor artifact resolves
    beneath the workspace.

    Interpretation: Failure identifies maintained writes by the private builder.

    Limitations: Publication behavior is covered by the separate public-facade test.
    """  # noqa: E501
    configure_literal_generation(monkeypatch)
    repository = tmp_path / "repository"
    workspace = tmp_path / "workspace"
    repository.mkdir()
    workspace.mkdir()
    generation = _HarnessControlGenerationBuilder().execute(
        HarnessControlMigrationRequest(repository.resolve()), workspace.resolve()
    )
    assert tuple(repository.rglob("*")) == ()
    candidates = dict(generation.artifacts)
    assert (
        candidates[Path("harness/state/harness-control.sqlite3")]
        .resolve()
        .is_relative_to(workspace.resolve())
    )
    assert (
        candidates[Path("harness/state/harness-control.sql")]
        .resolve()
        .is_relative_to(workspace.resolve())
    )
    assert (
        candidates[Path("harness/state/projection-manifest.json")]
        .resolve()
        .is_relative_to(workspace.resolve())
    )
    assert (
        candidates[Path("generated/literal.txt")]
        .resolve()
        .is_relative_to(workspace.resolve())
    )


def test_artifact__publication__candidate_validation_precedes_publisher(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.generation-boundary.validation-before-publication

    Requirement: The migrator validates the complete candidate before invoking its sole
    maintained publisher, and a validation failure publishes no partial generation.

    Method: Build a valid bounded candidate while injecting a validation failure and a
    publisher observer into the public migration path.

    Oracle: The required build, validate, publish sequence excludes publisher entry
    after validation raises.

    Acceptance: The exact validation error propagates, the publisher observer remains
    false, and the repository contains no generated output.

    Interpretation: Failure identifies publication before candidate validation or
    swallowed validation failure.

    Limitations: Rollback after an injected replacement failure is covered by the
    public migrator's focused evidence.
    """  # noqa: E501
    configure_literal_generation(monkeypatch)
    repository = tmp_path / "repository"
    repository.mkdir()
    published = False

    def reject_candidate(self: object, generation: object) -> None:
        raise RuntimeError("injected candidate validation failure")

    def observe_publication(*args: object, **kwargs: object) -> None:
        nonlocal published
        published = True

    monkeypatch.setattr(_HarnessControlGenerationBuilder, "validate", reject_candidate)
    monkeypatch.setattr(
        HarnessControlMigrator, "_publish_generation", observe_publication
    )
    with pytest.raises(RuntimeError, match="candidate validation failure"):
        HarnessControlMigrator().execute(
            HarnessControlMigrationRequest(repository.resolve())
        )
    assert published is False
    assert tuple(repository.rglob("*")) == ()
