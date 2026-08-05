# ruff: noqa: E501
"""Evidence class and represented meaning
Software verification of explicit-root composition, package imports, dependency direction, and generic public-surface nonmutation.
Owned contract, oracle, and scope
The artifact owner is the local/generic package integration boundary; current explicit v2 resources and the accepted H2 41-name inventory are exact oracles.
VVUQ and scientific exclusions
Passing establishes import and composition properties only, not numerical verification, scientific validation, UQ, physical correctness, or cross-language conformance.
"""

import ast
from pathlib import Path

import pytest

import ksdft2effmass.harness.pi as generic
from ksdft2effmass.harness.pi.local import (
    LoadLocalHarnessContext,
    LocalHarnessContext,
    RepositoryRoots,
)

from .conftest import local_context, repository_root

pytestmark = pytest.mark.software_verification

GENERIC_41 = (
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
    "ValidationIssue",
    "ValidationResult",
    "ProjectProfileLoadResult",
    "ResourceResolutionResult",
    "ChainEvaluationResult",
    "EvidenceAuditResult",
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
    "ValidateChecksumManifest",
    "ValidateSkillResources",
    "Identifier",
    "ResourcePath",
    "OwnershipScopePath",
    "DiagnosticPath",
    "Version",
)


def test_artifact__explicit_context__loads_v2_resources_and_rejects_ambient_or_mismatched_inputs(
    tmp_path: Path,
) -> None:
    "Evidence ID\nSV-HL-006\nRequirement\n        Local composition requires explicit existing roots and exact supplied profile/manifest bytes, with no current-directory or environment fallback.\nMethod\n        Load the provisional current-tree v2 profile and manifests, then pass an invalid profile and invalid/non-repository roots.\nOracle\n        H1/H4 require caller-owned roots and fail-closed generic validation of represented resources.\nAcceptance\n        Valid explicit inputs yield LocalHarnessContext; invalid profile yields PIHL.CONTEXT.PROFILE_INVALID; relative or outside roots raise ValueError.\nInterpretation\n        Failure indicates ambient discovery, weakened composition, provisional resource incompatibility, or fixture error.\nLimitations\n        Symlink races, installation relocation, science, numerical verification, UQ, and cross-language behavior are excluded."
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


def test_artifact__generic_local_dependency__is_one_way_and_generic_exports_are_unchanged() -> (
    None
):
    "Evidence ID\nSV-HL-007\nRequirement\n        Generic code never imports local code, local code depends only upward on generic code, and H4 does not mutate the accepted generic 41-name surface.\nMethod\n        Parse every generic and local source module AST and compare generic ``__all__`` to a fixed accepted H2 inventory before and after importing local.\nOracle\n        The accepted H2 acceptance index fixes 41 exports and the H4 architecture fixes ``local -> generic`` direction.\nAcceptance\n        Generic exports equal the 41-name oracle; no generic import names local; local relative imports never traverse outside ``pi``.\nInterpretation\n        Failure indicates generic mutation, reverse dependency, or an incorrect fixed inventory.\nLimitations\n        Dynamic imports and runtime monkeypatching outside these package modules, science, UQ, and portability are excluded."
    root = repository_root() / "python/src/ksdft2effmass/harness/pi"
    assert tuple(generic.__all__) == GENERIC_41
    assert len(generic.__all__) == 41
    for path in root.glob("*.py"):
        tree = ast.parse(path.read_text())
        assert not any(
            isinstance(node, (ast.Import, ast.ImportFrom))
            and "local"
            in (
                (node.module or "")
                if isinstance(node, ast.ImportFrom)
                else " ".join(x.name for x in node.names)
            )
            for node in ast.walk(tree)
        )
    for path in (root / "local").glob("*.py"):
        tree = ast.parse(path.read_text())
        assert not any(
            isinstance(node, ast.ImportFrom) and node.level > 2
            for node in ast.walk(tree)
        )
    assert tuple(generic.__all__) == GENERIC_41


def test_public_api__package_local_imports__resolve_without_execution_side_effects() -> (
    None
):
    "Evidence ID\nSV-HL-008\nRequirement\n        Installed-source package imports expose all 30 local symbols without initiating validation or command execution.\nMethod\n        Import all seven local submodules and inspect their public action classes and package export inventory.\nOracle\n        Python import semantics and the exact local module inventory define the expected represented state.\nAcceptance\n        Every module imports, all 30 names remain available, and no route or subprocess result is produced by import.\nInterpretation\n        Failure identifies packaging, circular-import, or import-side-effect regression.\nLimitations\n        A built wheel and alternate Python implementations are not tested; numerical, scientific, and UQ claims are excluded."
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
