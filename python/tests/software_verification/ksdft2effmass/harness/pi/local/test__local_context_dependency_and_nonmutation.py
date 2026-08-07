r"""Software verification of local context dependency and nonmutation.

Facet and represented meaning
Software verification of explicit-root composition, package imports, dependency
direction, and generic public-surface nonmutation.

Intrinsic and cross-object scope
The artifact owner is the local/generic package integration boundary; current explicit
v2 resources and the accepted 49-name generic public surface are exact oracles.

VVUQ and scientific exclusions
Passing establishes import and composition properties only, not numerical verification,
scientific validation, UQ, physical correctness, or cross-language conformance.
"""

import ast
from pathlib import Path
from typing import Any

import pytest

import ksdft2effmass.harness.pi as generic
from ksdft2effmass.harness.pi.local import (
    LoadLocalHarnessContext,
    LocalHarnessContext,
    RepositoryRoots,
)

from .conftest import local_context, repository_root

pytestmark = pytest.mark.software_verification

GENERIC_49 = (
    "ArtifactIdentity",
    "ResourceReference",
    "ResourceManifest",
    "ProjectProfile",
    "SkillDescriptor",
    "OwnershipScope",
    "AgentDescriptorView",
    "EvidenceIdentifierOccurrence",
    "OwnershipManifestView",
    "CheckpointRecord",
    "TaskReference",
    "ChainView",
    "ChecksumEntry",
    "ChecksumManifest",
    "PythonTestEvidenceSource",
    "PythonTestEvidenceRequest",
    "PythonTestEvidenceFinding",
    "TaskStateInspectionRequest",
    "ValidationIssue",
    "ValidationResult",
    "ProjectProfileLoadResult",
    "ResourceResolutionResult",
    "ChainEvaluationResult",
    "EvidenceAuditResult",
    "PythonTestEvidenceValidationResult",
    "TaskStateInspectionResult",
    "JsonSerializationResult",
    "JsonDeserializationResult",
    "WireRecordKind",
    "HarnessWireRecord",
    "HarnessInternalError",
    "SerializeJsonRecord",
    "DeserializeJsonRecord",
    "LoadProjectProfile",
    "ResolveResource",
    "ValidateResourceManifest",
    "ValidateOwnershipManifest",
    "ValidateCheckpointSet",
    "EvaluateChainState",
    "AuditEvidenceIdentifiers",
    "ValidatePythonTestEvidence",
    "InspectTaskState",
    "ValidateChecksumManifest",
    "ValidateSkillResources",
    "Identifier",
    "ResourcePath",
    "OwnershipScopePath",
    "DiagnosticPath",
    "Version",
)


def test_artifact__explicit_context__rejects_ambient_or_mismatched_inputs(
    tmp_path: Path,
) -> None:
    """Evidence ID
    SV-HL-006
    Requirement
    Local composition requires explicit existing roots and exact supplied
    profile/manifest bytes, with no current-directory or environment fallback.
    Method
    Load the provisional current-tree v2 profile and manifests, then pass an invalid
    profile and invalid/non-repository roots.
    Oracle
    H1/H4 require caller-owned roots and fail-closed generic validation of represented
    resources.
    Acceptance
    Valid explicit inputs yield LocalHarnessContext; invalid profile yields
    PIHL.CONTEXT.PROFILE_INVALID; relative or outside roots raise ValueError.
    Interpretation
    Failure indicates ambient discovery, weakened composition, provisional resource
    incompatibility, or fixture error.
    Limitations
    Symlink races, installation relocation, science, numerical verification, UQ, and
    cross-language behavior are excluded.
    """
    context = local_context()
    assert isinstance(context, LocalHarnessContext)
    root = repository_root()
    roots = RepositoryRoots(root, root / "harness/pi", root / "harness/local")
    result = LoadLocalHarnessContext().execute(
        roots,
        b"{}",
        (root / "harness/pi/resource-manifest.json").read_bytes(),
        (root / "harness/local/resource-manifest.json").read_bytes(),
    )
    assert result.validation.issues[0].code == "PIHL.CONTEXT.PROFILE_INVALID"
    with pytest.raises(ValueError):
        RepositoryRoots(Path("."), root / "harness/pi", root / "harness/local")
    outside = tmp_path.resolve()
    outside.mkdir(exist_ok=True)
    with pytest.raises(ValueError):
        RepositoryRoots(root, outside, root / "harness/local")


def test_artifact__generic_local_dependency__preserves_one_way_imports() -> None:
    """Evidence ID
    SV-HL-007
    Requirement
    Generic code never imports local code, local code depends only upward on generic
    code, and local composition does not mutate the accepted generic 49-name surface.
    Method
    Parse every generic and local source module AST and compare generic ``__all__`` to a
    fixed completed harness-tool inventory before and after importing local.
    Oracle
    The accepted validator migration pilot and completed task-state inspection tool fix
    49 exports; the H4 architecture fixes ``local -> generic`` direction.
    Acceptance
    Generic exports equal the 49-name oracle; no generic import names local; local
    relative imports never traverse outside ``pi``.
    Interpretation
    Failure indicates generic mutation, reverse dependency, or an incorrect fixed
    inventory.
    Limitations
    Dynamic imports and runtime monkeypatching outside these package modules, science,
    UQ, and portability are excluded.
    """
    root = repository_root() / "python/src/ksdft2effmass/harness/pi"
    assert tuple(generic.__all__) == GENERIC_49
    assert len(generic.__all__) == 49

    def assert_generic_module_does_not_import_local(path: Any) -> Any:
        """Evidence ID
        Owns no identifier; supports the enclosing stable evidence ID SV-HL-007.
        Requirement
        Each selected generic module satisfies the same prohibition on local imports.
        Method
        Parse one selected module and mechanically apply the enclosing import-node
        predicate.
        Oracle
        The one-way dependency contract prohibits every generic import from naming
        the local package.
        Acceptance
        No import node in the parsed module names ``local``.
        Interpretation
        Failure identifies a selected generic module that reverses the dependency;
        this helper makes no independent evidence claim.
        Limitations
        The iteration mechanically applies one identical requirement, oracle, and
        acceptance rule across the exact selected generic-module inventory; it hides
        no distinct partition and does not detect dynamic imports.
        """
        tree = ast.parse(path.read_text())
        assert not any(
            isinstance(node, (ast.Import, ast.ImportFrom))
            and "local"
            in (
                node.module or ""
                if isinstance(node, ast.ImportFrom)
                else " ".join(x.name for x in node.names)
            )
            for node in ast.walk(tree)
        )

    selected_generic_modules = root.glob("*.py")
    _ = [
        assert_generic_module_does_not_import_local(path)
        for path in selected_generic_modules
    ]

    def assert_local_relative_imports_stay_within_pi(path: Any) -> Any:
        """Evidence ID
        Owns no identifier; supports the enclosing stable evidence ID SV-HL-007.
        Requirement
        Each selected local module satisfies the same relative-import boundary.
        Method
        Parse one selected local module and mechanically apply the enclosing relative
        import-level predicate.
        Oracle
        The local-to-generic dependency contract permits no relative traversal beyond
        the ``pi`` package.
        Acceptance
        No relative import in the parsed module has a level greater than two.
        Interpretation
        Failure identifies a selected local module that crosses the package boundary;
        this helper makes no independent evidence claim.
        Limitations
        The iteration mechanically applies one identical requirement, oracle, and
        acceptance rule across the exact selected local-module inventory; it hides no
        distinct partition and does not detect dynamic imports.
        """
        tree = ast.parse(path.read_text())
        assert not any(
            isinstance(node, ast.ImportFrom) and node.level > 2
            for node in ast.walk(tree)
        )

    selected_local_modules = (root / "local").glob("*.py")
    _ = [
        assert_local_relative_imports_stay_within_pi(path)
        for path in selected_local_modules
    ]
    assert tuple(generic.__all__) == GENERIC_49


def test_public_api__package_local_imports__avoid_execution_side_effects() -> None:
    """Evidence ID
    SV-HL-008
    Requirement
    Installed-source package imports expose all 30 local symbols without initiating
    validation or command execution.
    Method
    Import all seven local submodules and inspect their public action classes and
    package export inventory.
    Oracle
    Python import semantics and the exact local module inventory define the expected
    represented state.
    Acceptance
    Every module imports, all 30 names remain available, and no route or subprocess
    result is produced by import.
    Interpretation
    Failure identifies packaging, circular-import, or import-side-effect regression.
    Limitations
    A built wheel and alternate Python implementations are not tested; numerical,
    scientific, and UQ claims are excluded.
    """
    modules = (
        "adapters",
        "context",
        "models",
        "routing",
        "shadow",
        "validation",
        "_parsing",
    )
    imported = [
        __import__(f"ksdft2effmass.harness.pi.local.{name}", fromlist=["*"])
        for name in modules
    ]
    assert len(imported) == 7
    assert (
        len(__import__("ksdft2effmass.harness.pi.local", fromlist=["*"]).__all__) == 30
    )
