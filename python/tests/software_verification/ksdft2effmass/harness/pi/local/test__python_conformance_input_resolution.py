r"""Software verification of project-local Python conformance input resolution.

Evidence profile: claim_bearing

Bounded artifact scope: Python conformance input-selection boundary.

Facet and represented meaning

The module owns canonical selection of maintained Python source, profile, and migration
inputs independently of Harness projection construction.

Intrinsic and cross-object scope

Exact root confinement, configured test-root selection, deterministic source ordering,
and dependency direction are represented. Conformance-rule behavior is excluded.

VVUQ and scientific exclusions

This is structural software verification only. It establishes no test success,
numerical verification, scientific validation, UQ, or execution authority.
"""

from pathlib import Path

import pytest

from ksdft2effmass.harness.pi.local.conformance_inputs import (
    _PythonConformanceInputResolver,
)

pytestmark = pytest.mark.software_verification


def test_method__execute__returns_exact_canonical_conformance_inputs(
    tmp_path: Path,
) -> None:
    """Evidence ID: software-verification.harness.python-conformance-inputs.exact-selection

    Requirement: Conformance input resolution uses the configured Python test root and
    returns exact repository-relative source, profile, and migration paths in
    deterministic order.

    Method: Construct one controlled repository with reversed lexical creation order,
    exact pytest configuration, and explicit profile and migration files, then resolve
    it.

    Oracle: The controlled path literals and lexical ordering independently define the
    complete expected result.

    Acceptance: The resolved root and all three input fields equal the exact literals.

    Interpretation: Failure identifies discovery, ordering, or input-identity drift.

    Limitations: File content interpretation belongs to the conformance owner.
    """  # noqa: E501
    root = tmp_path.resolve()
    (root / "python/tests/nested").mkdir(parents=True)
    (root / "python/pyproject.toml").write_text(
        '[tool.pytest.ini_options]\ntestpaths = ["tests"]\n'
    )
    (root / "python/tests/nested/test_z.py").write_text("def test_z(): pass\n")
    (root / "python/tests/test_a.py").write_text("def test_a(): pass\n")
    profile = root / "harness/pi/evidence/python-test-evidence-profile-matrix-v1.json"
    profile.parent.mkdir(parents=True)
    profile.write_text("{}\n")
    migration = (
        root / ".pi/evidence/python-conformance/r2.3-private-owner-migration.json"
    )
    migration.parent.mkdir(parents=True)
    migration.write_text("{}\n")

    result = _PythonConformanceInputResolver().execute(
        root,
        pyproject_path=Path("python/pyproject.toml"),
        test_root_path=Path("python/tests"),
        profile_path=Path(
            "harness/pi/evidence/python-test-evidence-profile-matrix-v1.json"
        ),
        migration_path=Path(
            ".pi/evidence/python-conformance/r2.3-private-owner-migration.json"
        ),
    )

    assert result.repository_root == root
    assert result.profile_path == Path(
        "harness/pi/evidence/python-test-evidence-profile-matrix-v1.json"
    )
    assert result.module_paths == (
        Path("python/tests/nested/test_z.py"),
        Path("python/tests/test_a.py"),
    )
    assert result.migration_path == Path(
        ".pi/evidence/python-conformance/r2.3-private-owner-migration.json"
    )


@pytest.mark.parametrize(
    "relative",
    (
        pytest.param(
            "python/src/ksdft2effmass/harness/pi/local/validation.py",
            id="repository_validator",
        ),
        pytest.param(
            "python/src/ksdft2effmass/harness/pi/local/_commands/"
            "validate_evidence_repository_conformance.py",
            id="repository_conformance_command",
        ),
    ),
)
def test_artifact__dependency__validation_does_not_import_projection_inputs(
    relative: str,
) -> None:
    """Evidence ID: software-verification.harness.python-conformance-inputs.projection-independence

    Requirement: Repository conformance validation depends on the shared canonical
    HarnessConfiguration input boundary rather than the projection input resolver.

    Method: Inspect each maintained validation consumer for the retired projection
    dependency and required conformance dependency.

    Oracle: The accepted dependency direction prohibits the projection resolver and
    requires the configuration plus dedicated conformance resolvers in both consumers.

    Acceptance: Each consumer names ``_HarnessConfigurationInputResolver`` and
    ``_PythonConformanceInputResolver`` without naming
    ``_HarnessProjectionInputResolver`` or importing ``local.control.inputs``.

    Interpretation: Failure identifies renewed projection coupling.

    Limitations: Static dependency inspection does not establish runtime conformance.
    """  # noqa: E501
    root = Path(__file__).resolve().parents[7]
    source = (root / relative).read_text()
    assert "_HarnessConfigurationInputResolver" in source
    assert "_PythonConformanceInputResolver" in source
    assert "_HarnessProjectionInputResolver" not in source
    assert "local.control.inputs" not in source


@pytest.mark.parametrize(
    "escaped_input",
    (
        pytest.param("test_root", id="symlinked_test_root"),
        pytest.param("profile", id="symlinked_profile"),
        pytest.param("migration", id="symlinked_migration"),
    ),
)
def test_method__execute__rejects_inputs_that_escape_the_repository_root(
    escaped_input: str,
    tmp_path: Path,
) -> None:
    """Evidence ID: software-verification.harness.python-conformance-inputs.root-confinement

    Requirement: The configured test root, profile, and migration inputs must resolve
    beneath the explicit repository root.

    Method: Replace each independently selected input with a symlink to a controlled
    path outside the repository and execute canonical resolution.

    Oracle: Resolved-path containment requires rejection for every escaping symlink.

    Acceptance: Every semantic input partition raises ``ValueError``.

    Interpretation: Failure permits conformance input selection outside its explicit
    repository boundary.

    Limitations: Selection-time confinement does not snapshot later filesystem state.
    """  # noqa: E501
    root = (tmp_path / "repository").resolve()
    outside = (tmp_path / "outside").resolve()
    (root / "python").mkdir(parents=True)
    outside.mkdir()
    (root / "python/pyproject.toml").write_text(
        '[tool.pytest.ini_options]\ntestpaths = ["tests"]\n'
    )
    if escaped_input == "test_root":
        (outside / "tests").mkdir()
        (outside / "tests/test_external.py").write_text("def test_external(): pass\n")
        (root / "python/tests").symlink_to(outside / "tests", target_is_directory=True)
    else:
        (root / "python/tests").mkdir()
        (root / "python/tests/test_local.py").write_text("def test_local(): pass\n")
    profile = root / "harness/pi/evidence/python-test-evidence-profile-matrix-v1.json"
    profile.parent.mkdir(parents=True)
    migration = (
        root / ".pi/evidence/python-conformance/r2.3-private-owner-migration.json"
    )
    migration.parent.mkdir(parents=True)
    if escaped_input == "profile":
        (outside / "profile.json").write_text("{}\n")
        profile.symlink_to(outside / "profile.json")
    else:
        profile.write_text("{}\n")
    if escaped_input == "migration":
        (outside / "migration.json").write_text("{}\n")
        migration.symlink_to(outside / "migration.json")
    else:
        migration.write_text("{}\n")

    with pytest.raises(ValueError):
        _PythonConformanceInputResolver().execute(
            root,
            pyproject_path=Path("python/pyproject.toml"),
            test_root_path=Path("python/tests"),
            profile_path=Path(
                "harness/pi/evidence/python-test-evidence-profile-matrix-v1.json"
            ),
            migration_path=Path(
                ".pi/evidence/python-conformance/r2.3-private-owner-migration.json"
            ),
        )


def test_artifact__dependency__projection_composes_canonical_conformance_inputs() -> (
    None
):
    """Evidence ID: software-verification.harness.python-conformance-inputs.projection-composition

    Requirement: Projection input construction composes conformance enumeration from
    the resolved HarnessConfiguration and does not independently parse pytest policy.

    Method: Inspect projection-input source for configured resolver arguments and sole
    module-observation forwarding, and prohibit independent test-tree traversal.

    Oracle: HarnessConfiguration owns policy paths while the conformance resolver owns
    source enumeration beneath the configured test root.

    Acceptance: Every configured argument and module forwarding expression is present;
    superseded request-level policy forwarding, ``tomllib``, and traversal are absent.

    Interpretation: Failure identifies duplicated or bypassed conformance selection.

    Limitations: Static composition inspection does not establish projection behavior.
    """  # noqa: E501
    root = Path(__file__).resolve().parents[7]
    source = (
        root / "python/src/ksdft2effmass/harness/pi/local/control/inputs.py"
    ).read_text()
    assert "_PythonConformanceInputResolver().execute(" in source
    assert (
        "pyproject_path=Path(configuration.python_conformance.pyproject_path)" in source
    )
    assert "test_root_path=Path(configuration.python_conformance.test_root)" in source
    assert (
        "profile_path=Path(configuration.python_conformance.profile_matrix_path)"
        in source
    )
    assert (
        "migration_path=Path(configuration.python_conformance.migration_map_path)"
        in source
    )
    assert "evidence_module_paths=conformance.module_paths" in source
    assert "evidence_profile_matrix_path=conformance.profile_path" not in source
    assert "evidence_migration_path=conformance.migration_path" not in source
    assert "tomllib" not in source
    assert ".rglob(" not in source
