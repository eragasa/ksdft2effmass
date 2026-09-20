r"""Software verification of Stage C source ownership contract.

Evidence profile: routine

Bounded artifact scope: source-module class inventories, minimal CLI entry points, and
verifier import direction.

Facet and represented meaning

The artifact is the exact class and module-level callable inventory of the maintained
Stage C implementation, verifier, and CLI adapter modules.

Intrinsic and cross-object scope

This module owns structural placement of records, wire mechanics, numerical actions,
authority, retention, Workflows, and independent verification behind minimal CLI entry
points.

VVUQ and scientific exclusions

This is structural software verification. AST inventory and import checks do not
establish numerical correctness, behavioral independence, scientific validation,
uncertainty quantification, or execution authority.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]

pytestmark = pytest.mark.software_verification


class TestStageCSourceOwnershipContract:
    """Own software verification of the Stage C source-module ownership split."""

    @staticmethod
    def repository_root() -> Path:
        """Return the repository containing the Stage C artifacts.

        Evidence ID: Helper owns no identifier.
        """

        return Path(__file__).resolve().parents[6]

    @classmethod
    def stage_directory(cls) -> Path:
        """Return the maintained defect-2D calculation directory.

        Evidence ID: Helper owns no identifier.
        """

        return (
            cls.repository_root() / "calculations/research-monograph/impurity-defect-2d"
        )

    @staticmethod
    def assert_source_inventory(
        path: Path,
        expected_classes: tuple[str, ...],
        expected_functions: tuple[str, ...] = (),
    ) -> None:
        """Assert one source module's class and module-level function inventory.

        Evidence ID: Helper owns no identifier.
        """

        tree = ast.parse(path.read_text())
        classes = tuple(
            node.name for node in tree.body if isinstance(node, ast.ClassDef)
        )
        functions = tuple(
            node.name
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        )
        assert classes == expected_classes
        assert functions == expected_functions

    def test_artifact__module_ownership__keeps_cli_adapters_minimal(self) -> None:
        """Place Stage C classes in cohesive modules behind typed CLI adapters.

        Evidence ID: SV-RM-DEFECT2D-C-029

        Requirement: Calculation-specific records, wire mechanics, numerical
        actions, authority, retention, workflows, and independent verification have
        explicit module owners; executable scripts remain typed CLI adaptation only.

        Method: Parse the maintained Python sources and compare their class and
        module-level function inventories with the declared ownership split.

        Oracle: The DataObject/ActionObject architecture assigns reusable behavior
        to precise class owners and permits only framework-owned CLI entry functions.

        Acceptance: Both wrappers contain only `main`, every implementation module
        has its exact cohesive class inventory and no module-level function, and the
        independent verifier imports no runner implementation package.

        Interpretation: Passing verifies the structural ownership boundary, not the
        numerical algorithms or scientific adequacy.

        Limitations: AST structure does not prove behavioral independence or result
        correctness; those claims remain with the behavioral tests and verifier.
        """

        stage = self.stage_directory()
        self.assert_source_inventory(
            stage / "stage_c_parent/model.py",
            (
                "ParentHopping",
                "LocalBond",
                "PointOperation",
                "ParentFixture",
                "ArtifactBinding",
                "StageCAcceptedParentExecutionAuthorization",
                "StageCResultContext",
                "ParentControls",
                "ParentCase",
                "ParentScheduleResult",
            ),
        )
        self.assert_source_inventory(
            stage / "stage_c_parent/records.py",
            (
                "ParentJsonReader",
                "AcceptedParentStageCDesignDeserializer",
                "AuthoredParentFixtureDeserializer",
                "AcceptedParentStageCArtifactAdapter",
                "AuthoredAcceptedParentAdapterFixtureDeserializer",
            ),
        )
        self.assert_source_inventory(
            stage / "stage_c_parent/operator_construction.py",
            ("ParentHoppingConstructor", "ParentMatrixConstructor"),
        )
        self.assert_source_inventory(
            stage / "stage_c_parent/model_fitting.py",
            ("ParentModelFitter", "RouteIndependenceGate"),
        )
        self.assert_source_inventory(
            stage / "stage_c_parent/scheduling.py", ("ParentScheduleExecutor",)
        )
        self.assert_source_inventory(
            stage / "stage_c_parent/evaluation.py",
            ("StageCResultProvenanceSerializer", "AcceptedParentStageCEvaluator"),
        )
        self.assert_source_inventory(
            stage / "stage_c_parent/authorization.py",
            (
                "AcceptedParentStageCExecutionAuthorizationDeserializer",
                "StageCOperationPaths",
                "ValidatedStageCExecution",
                "AcceptedParentStageCAuthorityValidator",
            ),
        )
        self.assert_source_inventory(
            stage / "stage_c_parent/retention.py",
            (
                "AcceptedParentStageCResultSerializer",
                "ExclusiveRetainedArtifactWriter",
                "StageCAttemptJournal",
                "StageCProtectedOperationFinalizer",
            ),
        )
        self.assert_source_inventory(
            stage / "stage_c_parent/context.py", ("StageCResultContextPreparer",)
        )
        self.assert_source_inventory(
            stage / "stage_c_parent/workflows.py",
            (
                "AcceptedParentStageCToyWorkflow",
                "AcceptedParentStageCAdapterFixtureWorkflow",
                "AuthoredStageCOperationWorkflow",
                "AcceptedParentStageCExecutionWorkflow",
            ),
        )
        self.assert_source_inventory(
            stage / "stage_c_parent_verification/verifier.py",
            (
                "VerificationCase",
                "VerificationJsonReader",
                "IndependentStageCParentVerifier",
            ),
        )
        self.assert_source_inventory(stage / "run_stage_c_parent.py", (), ("main",))
        self.assert_source_inventory(stage / "verify_stage_c_parent.py", (), ("main",))
        verifier_tree = ast.parse(
            (stage / "stage_c_parent_verification/verifier.py").read_text()
        )
        imported_modules = tuple(
            node.module
            for node in verifier_tree.body
            if isinstance(node, ast.ImportFrom) and node.module is not None
        )
        assert not any(
            module == "stage_c_parent" or module.startswith("stage_c_parent.")
            for module in imported_modules
        )
