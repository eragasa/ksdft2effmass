r"""Software verification of explicit-input dependency graph view contract.

Evidence profile: claim_bearing

Bounded artifact scope: explicit-input dependency graph view contract.

Facet and represented meaning

This module verifies separately identified lexical, runtime-unconditional, and
package-facade-excluded nodes, edges, provenance, SCCs, ordering, and exact direction
checks.

Intrinsic and cross-object scope

Immutable graph records own intrinsic closure; one analyzer derives views and evaluates
only caller-requested checks over accepted production facts. Exact authored source,
Python import syntax, graph reachability, and supplied contracts are the oracles.

VVUQ and scientific exclusions

Passing establishes bounded structural software behavior only. It establishes no
universal dependency interpretation, runtime import failure, source defect, numerical
verification, scientific validation, uncertainty quantification, repair authority,
support disposition, or human acceptance.
"""

from __future__ import annotations

import hashlib
from dataclasses import FrozenInstanceError, replace
from pathlib import Path, PurePosixPath
from typing import Literal

import pytest

from ksdft2effmass.harness.pi.conformance.python.dependency_graph import (
    PythonAcceptedDependencyContract,
    PythonDependencyDirection,
    PythonDependencyDirectionCheck,
    PythonDependencyDirectionResult,
    PythonDependencyDirectionStatus,
    PythonDependencyGraphAnalyzer,
    PythonDependencyGraphEdge,
    PythonDependencyGraphNode,
    PythonDependencyGraphRequest,
    PythonDependencyGraphResult,
    PythonDependencyGraphView,
    PythonDependencyGraphViewResult,
    PythonDependencyModule,
    PythonDependencyResolutionKind,
    PythonDependencyStronglyConnectedComponent,
)
from ksdft2effmass.harness.pi.conformance.python.production import (
    PythonProductionInspectionResult,
    PythonProductionScopeKind,
    PythonProductionSource,
    PythonProductionSourceInspector,
    PythonProductionSourceProfile,
)

pytestmark = pytest.mark.software_verification
RESOURCE_ROOT = Path(__file__).parent / "resources/dependency_graph_views/pkg"
MODULE_CASES = (
    ("pkg", "__init__.py.txt", "pkg/__init__.py", True),
    ("pkg.alpha", "alpha.py.txt", "pkg/alpha.py", False),
    ("pkg.beta", "beta.py.txt", "pkg/beta.py", False),
    ("pkg.conditional", "conditional.py.txt", "pkg/conditional.py", False),
    ("pkg.local", "local.py.txt", "pkg/local.py", False),
)
type ExpectedContribution = tuple[
    int,
    str,
    PythonDependencyResolutionKind,
    tuple[str, ...],
    tuple[tuple[str, str | None], ...],
    tuple[int, int, int, int],
]
PROVENANCE_CASES = (
    pytest.param(
        "pkg",
        "pkg.alpha",
        "__init__.py.txt",
        "pkg/__init__.py",
        True,
        (
            (
                1,
                "alpha",
                PythonDependencyResolutionKind.FROM_IMPORTED_SUBMODULE,
                (),
                (),
                (1, 14, 1, 19),
            ),
        ),
        id="facade_to_imported_alpha",
    ),
    pytest.param(
        "pkg.alpha",
        "pkg",
        "alpha.py.txt",
        "pkg/alpha.py",
        False,
        (
            (
                3,
                "beta",
                PythonDependencyResolutionKind.FROM_FACADE,
                (),
                (),
                (3, 14, 3, 18),
            ),
            (
                6,
                "conditional",
                PythonDependencyResolutionKind.FROM_FACADE,
                (),
                (("if_body", "TYPE_CHECKING"),),
                (6, 18, 6, 29),
            ),
            (
                10,
                "local",
                PythonDependencyResolutionKind.FROM_FACADE,
                ("load",),
                (),
                (10, 18, 10, 23),
            ),
        ),
        id="alpha_to_facade_all_contexts",
    ),
    pytest.param(
        "pkg.alpha",
        "pkg.beta",
        "alpha.py.txt",
        "pkg/alpha.py",
        False,
        (
            (
                3,
                "beta",
                PythonDependencyResolutionKind.FROM_IMPORTED_SUBMODULE,
                (),
                (),
                (3, 14, 3, 18),
            ),
        ),
        id="alpha_to_imported_beta",
    ),
    pytest.param(
        "pkg.alpha",
        "pkg.conditional",
        "alpha.py.txt",
        "pkg/alpha.py",
        False,
        (
            (
                6,
                "conditional",
                PythonDependencyResolutionKind.FROM_IMPORTED_SUBMODULE,
                (),
                (("if_body", "TYPE_CHECKING"),),
                (6, 18, 6, 29),
            ),
        ),
        id="alpha_to_conditional_submodule",
    ),
    pytest.param(
        "pkg.alpha",
        "pkg.local",
        "alpha.py.txt",
        "pkg/alpha.py",
        False,
        (
            (
                10,
                "local",
                PythonDependencyResolutionKind.FROM_IMPORTED_SUBMODULE,
                ("load",),
                (),
                (10, 18, 10, 23),
            ),
        ),
        id="alpha_to_callable_local_submodule",
    ),
    pytest.param(
        "pkg.beta",
        "pkg",
        "beta.py.txt",
        "pkg/beta.py",
        False,
        (
            (
                1,
                "alpha",
                PythonDependencyResolutionKind.FROM_FACADE,
                (),
                (),
                (1, 14, 1, 19),
            ),
        ),
        id="beta_to_facade",
    ),
    pytest.param(
        "pkg.beta",
        "pkg.alpha",
        "beta.py.txt",
        "pkg/beta.py",
        False,
        (
            (
                1,
                "alpha",
                PythonDependencyResolutionKind.FROM_IMPORTED_SUBMODULE,
                (),
                (),
                (1, 14, 1, 19),
            ),
        ),
        id="beta_to_imported_alpha",
    ),
    pytest.param(
        "pkg.conditional",
        "pkg",
        "conditional.py.txt",
        "pkg/conditional.py",
        False,
        (
            (
                1,
                "alpha",
                PythonDependencyResolutionKind.FROM_FACADE,
                (),
                (),
                (1, 14, 1, 19),
            ),
        ),
        id="conditional_module_to_facade",
    ),
    pytest.param(
        "pkg.conditional",
        "pkg.alpha",
        "conditional.py.txt",
        "pkg/conditional.py",
        False,
        (
            (
                1,
                "alpha",
                PythonDependencyResolutionKind.FROM_IMPORTED_SUBMODULE,
                (),
                (),
                (1, 14, 1, 19),
            ),
        ),
        id="conditional_module_to_alpha",
    ),
    pytest.param(
        "pkg.local",
        "pkg",
        "local.py.txt",
        "pkg/local.py",
        False,
        (
            (
                1,
                "alpha",
                PythonDependencyResolutionKind.FROM_FACADE,
                (),
                (),
                (1, 14, 1, 19),
            ),
        ),
        id="local_module_to_facade",
    ),
    pytest.param(
        "pkg.local",
        "pkg.alpha",
        "local.py.txt",
        "pkg/local.py",
        False,
        (
            (
                1,
                "alpha",
                PythonDependencyResolutionKind.FROM_IMPORTED_SUBMODULE,
                (),
                (),
                (1, 14, 1, 19),
            ),
        ),
        id="local_module_to_alpha",
    ),
)


class TestDependencyGraphViews:
    """Verify the artifact through exact unsupported implementation values."""

    @staticmethod
    def inspect_resources() -> PythonProductionInspectionResult:
        """Produce accepted facts from exact maintained module resources."""
        sources = tuple(
            PythonProductionSource.from_payload(
                input_identity=module_name,
                path=PurePosixPath(source_path),
                payload=(RESOURCE_ROOT / resource_name).read_bytes(),
            )
            for module_name, resource_name, source_path, _is_facade in MODULE_CASES
        )
        return PythonProductionSourceInspector().execute(
            PythonProductionSourceProfile(), sources
        )

    @staticmethod
    def bindings(
        inspection: PythonProductionInspectionResult,
    ) -> tuple[PythonDependencyModule, ...]:
        """Bind exact module names and explicit facade identities to fact outcomes."""
        modules_by_identity = {
            module.input_identity: module for module in inspection.modules
        }
        return tuple(
            PythonDependencyModule(
                module_name=module_name,
                is_package_facade=is_facade,
                input_identity=module_name,
                source_path=PurePosixPath(source_path),
                source_sha256=modules_by_identity[module_name].source_sha256 or "",
            )
            for module_name, _resource_name, source_path, is_facade in MODULE_CASES
        )

    @classmethod
    def analyze(
        cls,
        inspection: PythonProductionInspectionResult,
        checks: tuple[PythonDependencyDirectionCheck, ...] = (),
        modules: tuple[PythonDependencyModule, ...] | None = None,
    ) -> PythonDependencyGraphResult:
        """Execute the analyzer with exact facts, bindings, and requested checks."""
        selected_modules = cls.bindings(inspection) if modules is None else modules
        return PythonDependencyGraphAnalyzer().execute(
            PythonDependencyGraphRequest(
                production_facts=inspection,
                modules=selected_modules,
                direction_checks=checks,
            )
        )

    @staticmethod
    def view(
        result: PythonDependencyGraphResult, view: PythonDependencyGraphView
    ) -> tuple[
        tuple[str, ...],
        tuple[tuple[str, str], ...],
        tuple[tuple[str, ...], ...],
    ]:
        """Project one named result to exact nodes, endpoints, and SCC members."""
        selected = next(item for item in result.views if item.view is view)
        return (
            tuple(node.module_name for node in selected.nodes),
            tuple((edge.source_module, edge.target_module) for edge in selected.edges),
            tuple(
                component.module_names
                for component in selected.strongly_connected_components
            ),
        )

    def test_artifact__dependency_graph_views__distinguishes_edges_sccs_and_provenance(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness.dependency-graphs.views

        Requirement: Lexical, runtime-unconditional, and facade-excluded views remain
        separately identified with deterministic nodes, internal edges, SCCs, and
        exact source-edge provenance.

        Method: Inspect five maintained modules containing unconditional, conditional,
        callable-local, relative facade, and imported-submodule edges, then project
        every named view and selected provenance.

        Oracle: Python import syntax, the accepted dual facade/submodule edge rule, and
        manually derived reachability of the exact authored fixture.

        Acceptance: Each view has the exact nodes, edge set, SCC partition, and view
        identity; lexical provenance retains lines 3/6/10 while runtime provenance
        retains only line 3 with exact source identity and resolution.

        Interpretation: Failure identifies view conflation, lost source attribution,
        unstable ordering, or incorrect graph reachability.

        Limitations: The sources are parsed but never imported or executed; SCCs are
        structural results for their named views only.
        """
        inspection = self.inspect_resources()
        result = self.analyze(inspection)
        lexical = self.view(result, PythonDependencyGraphView.LEXICAL)
        runtime = self.view(result, PythonDependencyGraphView.RUNTIME_UNCONDITIONAL)
        facade_excluded = self.view(
            result, PythonDependencyGraphView.PACKAGE_FACADE_EXCLUDED
        )
        all_nodes = (
            "pkg",
            "pkg.alpha",
            "pkg.beta",
            "pkg.conditional",
            "pkg.local",
        )
        assert lexical == (
            all_nodes,
            (
                ("pkg", "pkg.alpha"),
                ("pkg.alpha", "pkg"),
                ("pkg.alpha", "pkg.beta"),
                ("pkg.alpha", "pkg.conditional"),
                ("pkg.alpha", "pkg.local"),
                ("pkg.beta", "pkg"),
                ("pkg.beta", "pkg.alpha"),
                ("pkg.conditional", "pkg"),
                ("pkg.conditional", "pkg.alpha"),
                ("pkg.local", "pkg"),
                ("pkg.local", "pkg.alpha"),
            ),
            (all_nodes,),
        )
        assert runtime == (
            all_nodes,
            (
                ("pkg", "pkg.alpha"),
                ("pkg.alpha", "pkg"),
                ("pkg.alpha", "pkg.beta"),
                ("pkg.beta", "pkg"),
                ("pkg.beta", "pkg.alpha"),
                ("pkg.conditional", "pkg"),
                ("pkg.conditional", "pkg.alpha"),
                ("pkg.local", "pkg"),
                ("pkg.local", "pkg.alpha"),
            ),
            (("pkg", "pkg.alpha", "pkg.beta"), ("pkg.conditional",), ("pkg.local",)),
        )
        assert facade_excluded == (
            ("pkg.alpha", "pkg.beta", "pkg.conditional", "pkg.local"),
            (
                ("pkg.alpha", "pkg.beta"),
                ("pkg.alpha", "pkg.conditional"),
                ("pkg.alpha", "pkg.local"),
                ("pkg.beta", "pkg.alpha"),
                ("pkg.conditional", "pkg.alpha"),
                ("pkg.local", "pkg.alpha"),
            ),
            (("pkg.alpha", "pkg.beta", "pkg.conditional", "pkg.local"),),
        )
        lexical_result = result.views[0]
        runtime_result = result.views[1]
        lexical_edge = next(
            edge
            for edge in lexical_result.edges
            if (edge.source_module, edge.target_module) == ("pkg.alpha", "pkg")
        )
        runtime_edge = next(
            edge
            for edge in runtime_result.edges
            if (edge.source_module, edge.target_module) == ("pkg.alpha", "pkg")
        )
        assert tuple(
            item.import_fact.location.line for item in lexical_edge.provenance
        ) == (
            3,
            6,
            10,
        )
        assert tuple(
            item.import_fact.location.line for item in runtime_edge.provenance
        ) == (3,)
        assert lexical_edge.provenance[0].resolution is (
            PythonDependencyResolutionKind.FROM_FACADE
        )
        assert lexical_edge.provenance[1].import_fact.contexts
        assert lexical_edge.provenance[2].import_fact.owners[-1].kind is (
            PythonProductionScopeKind.CALLABLE
        )
        assert all(
            item.source.source_path == PurePosixPath("pkg/alpha.py")
            for item in lexical_edge.provenance
        )
        assert all(node.view is result.views[0].view for node in result.views[0].nodes)
        assert all(edge.view is result.views[0].view for edge in result.views[0].edges)

    @pytest.mark.parametrize(
        (
            "source_module",
            "target_module",
            "resource_name",
            "source_path",
            "is_facade",
            "expected",
        ),
        PROVENANCE_CASES,
    )
    def test_artifact__dependency_edge_provenance__retains_every_exact_contribution(
        self,
        source_module: str,
        target_module: str,
        resource_name: str,
        source_path: str,
        is_facade: bool,
        expected: tuple[ExpectedContribution, ...],
    ) -> None:
        """Evidence ID: software-verification.harness.dependency-graphs.provenance

        Requirement: Every internal lexical edge retains every exact contributing
        production outcome, module binding, import field/span, owner/context, and
        resolution kind without requiring the original request for attribution.

        Method: Project each semantic lexical edge from the maintained five-module
        fixture and compare every field with manually derived source expectations and
        independently computed SHA-256 identities.

        Oracle: Exact authored fixture bytes, SHA-256, Python import syntax, and the
        accepted dual facade/submodule resolution rule.

        Acceptance: Each contribution agrees exactly on source module/input/path/
        digest/facade identity, import syntax and span, owner/context, endpoint, and
        resolution.

        Interpretation: Failure identifies omitted, substituted, collapsed, or
        structurally inconsistent edge provenance.

        Limitations: Provenance establishes represented syntax identity, not runtime
        import success or semantic dependency ownership.
        """
        lexical = self.analyze(self.inspect_resources()).views[0]
        edge = next(
            item
            for item in lexical.edges
            if (item.source_module, item.target_module)
            == (source_module, target_module)
        )
        digest = hashlib.sha256(
            (RESOURCE_ROOT / resource_name).read_bytes()
        ).hexdigest()
        assert {
            (
                item.source.module_name,
                item.source.input_identity,
                item.source.source_path,
                item.source.source_sha256,
                item.source.is_package_facade,
            )
            for item in edge.provenance
        } == {
            (
                source_module,
                source_module,
                PurePosixPath(source_path),
                digest,
                is_facade,
            )
        }
        assert all(
            item.import_fact.kind.value == "from_import"
            and item.import_fact.module is None
            and item.import_fact.alias is None
            and item.import_fact.relative_level == 1
            and item.resolved_target == target_module
            for item in edge.provenance
        )
        assert (
            tuple(
                (
                    item.import_fact.location.line,
                    item.import_fact.name,
                    item.resolution,
                    tuple(owner.qualified_name for owner in item.import_fact.owners),
                    tuple(
                        (context.kind.value, context.expression)
                        for context in item.import_fact.contexts
                    ),
                    (
                        item.import_fact.location.line,
                        item.import_fact.location.column,
                        item.import_fact.location.end_line,
                        item.import_fact.location.end_column,
                    ),
                )
                for item in edge.provenance
            )
            == expected
        )

    def test_artifact__dependency_edge_provenance__distinguishes_source_outcomes(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness.dependency-graphs.source-outcomes

        Requirement: Distinct successful outcomes with equal paths and bytes remain
        attributable by input identity in each edge contribution.

        Method: Analyze two equal-path/equal-payload source outcomes, then swap their
        explicit module bindings while retaining the same target module.

        Oracle: Exact production input identities and immutable module bindings.

        Acceptance: Each result retains the bound input identity on its source edge,
        and swapping identities changes the result rather than producing an
        indistinguishable graph.

        Interpretation: Failure identifies lost source-outcome provenance.

        Limitations: Equal input identities remain prohibited because they cannot name
        distinct accepted outcomes.
        """
        payload = (RESOURCE_ROOT / "beta.py.txt").read_bytes()
        sources = (
            PythonProductionSource.from_payload(
                input_identity="first-outcome",
                path=PurePosixPath("pkg/shared.py"),
                payload=payload,
            ),
            PythonProductionSource.from_payload(
                input_identity="second-outcome",
                path=PurePosixPath("pkg/shared.py"),
                payload=payload,
            ),
            PythonProductionSource.from_payload(
                input_identity="target-outcome",
                path=PurePosixPath("pkg/alpha.py"),
                payload=(RESOURCE_ROOT / "conditional.py.txt").read_bytes(),
            ),
        )
        inspection = PythonProductionSourceInspector().execute(
            PythonProductionSourceProfile(), sources
        )
        by_identity = {module.input_identity: module for module in inspection.modules}
        digest = hashlib.sha256(payload).hexdigest()
        first = PythonDependencyModule(
            module_name="pkg.first",
            is_package_facade=False,
            input_identity="first-outcome",
            source_path=PurePosixPath("pkg/shared.py"),
            source_sha256=digest,
        )
        second = replace(
            first, module_name="pkg.second", input_identity="second-outcome"
        )
        target = PythonDependencyModule(
            module_name="pkg.alpha",
            is_package_facade=False,
            input_identity="target-outcome",
            source_path=PurePosixPath("pkg/alpha.py"),
            source_sha256=by_identity["target-outcome"].source_sha256 or "",
        )
        forward = self.analyze(inspection, modules=(first, second, target))
        swapped = self.analyze(
            inspection,
            modules=(
                replace(first, input_identity="second-outcome"),
                replace(second, input_identity="first-outcome"),
                target,
            ),
        )
        forward_edges = forward.views[0].edges
        assert tuple(
            (edge.source_module, edge.provenance[0].source.input_identity)
            for edge in forward_edges
        ) == (("pkg.first", "first-outcome"), ("pkg.second", "second-outcome"))
        assert forward != swapped

    @pytest.mark.parametrize(
        "case",
        (
            pytest.param("all_failed", id="all_inputs_are_represented_failures"),
            pytest.param("mixed", id="successful_and_failed_inputs_are_mixed"),
        ),
    )
    def test_artifact__dependency_graph_inputs__preserves_failure_partitions(
        self, case: Literal["all_failed", "mixed"]
    ) -> None:
        """Evidence ID: software-verification.harness.dependency-graphs.failures

        Requirement: Exact module bindings cover successful production outcomes only;
        represented failures remain accepted inputs and an all-failure result returns
        all three empty graph views.

        Method: Analyze all-failed and mixed success/failure semantic partitions from
        accepted production-fact results.

        Oracle: The accepted production-facts success/failure union and exact binding
        coverage documented for the graph request.

        Acceptance: All represented failures remain in the supplied facts; all-failed
        input yields three empty views, while mixed input yields one node and singleton
        SCC in each view without a node for the failure.

        Interpretation: Failure identifies rejection or silent graph representation of
        accepted source failures.

        Limitations: Read failures are caller-represented and perform no filesystem
        access.
        """
        failed = PythonProductionSource(
            input_identity="failed",
            path=PurePosixPath("pkg/failed.py"),
            payload=None,
            read_error="represented read failure",
        )
        sources: tuple[PythonProductionSource, ...]
        if case == "all_failed":
            sources = (
                failed,
                PythonProductionSource(
                    input_identity="also-failed",
                    path=PurePosixPath("pkg/also_failed.py"),
                    payload=None,
                    read_error="second represented read failure",
                ),
            )
        else:
            sources = (
                PythonProductionSource.from_payload(
                    input_identity="pkg.only",
                    path=PurePosixPath("pkg/only.py"),
                    payload=(RESOURCE_ROOT / "local.py.txt").read_bytes(),
                ),
                failed,
            )
        inspection = PythonProductionSourceInspector().execute(
            PythonProductionSourceProfile(), sources
        )
        successful = tuple(
            module
            for module in inspection.modules
            if module.facts is not None and module.source_sha256 is not None
        )
        modules = tuple(
            PythonDependencyModule(
                module_name="pkg.only",
                is_package_facade=False,
                input_identity=module.input_identity,
                source_path=module.path,
                source_sha256=module.source_sha256 or "",
            )
            for module in successful
        )
        result = self.analyze(inspection, modules=modules)
        assert sum(module.failure is not None for module in inspection.modules) == (
            2 if case == "all_failed" else 1
        )
        assert len(result.views) == 3
        if case == "all_failed":
            assert all(not view.nodes for view in result.views)
            assert all(not view.edges for view in result.views)
            assert all(not view.strongly_connected_components for view in result.views)
        else:
            assert all(
                tuple(node.module_name for node in view.nodes) == ("pkg.only",)
                for view in result.views
            )
            assert all(not view.edges for view in result.views)
            assert all(
                tuple(
                    component.module_names
                    for component in view.strongly_connected_components
                )
                == (("pkg.only",),)
                for view in result.views
            )

    def test_artifact__dependency_graph_views__orders_independently_of_input_order(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness.dependency-graphs.ordering

        Requirement: Module-binding and direction-check caller order cannot alter the
        canonical result.

        Method: Analyze the same accepted facts with forward and reverse binding and
        check tuples.

        Oracle: Exact DataObject equality and the documented canonical module, edge,
        provenance, component, and direction-check ordering keys.

        Acceptance: Forward and reversed inputs produce equal immutable result values.

        Interpretation: Failure identifies caller-order leakage.

        Limitations: Source order remains intentionally present inside provenance.
        """
        inspection = self.inspect_resources()
        modules = self.bindings(inspection)
        allow = PythonAcceptedDependencyContract(
            contract_identity="architecture.edge.alpha-beta.allow.v1",
            view=PythonDependencyGraphView.LEXICAL,
            source_module="pkg.alpha",
            target_module="pkg.beta",
            direction=PythonDependencyDirection.ALLOW,
        )
        prohibit = PythonAcceptedDependencyContract(
            contract_identity="architecture.edge.beta-alpha.prohibit.v1",
            view=PythonDependencyGraphView.LEXICAL,
            source_module="pkg.beta",
            target_module="pkg.alpha",
            direction=PythonDependencyDirection.PROHIBIT,
        )
        checks = (
            PythonDependencyDirectionCheck(
                view=allow.view,
                source_module=allow.source_module,
                target_module=allow.target_module,
                accepted_contract=allow,
            ),
            PythonDependencyDirectionCheck(
                view=prohibit.view,
                source_module=prohibit.source_module,
                target_module=prohibit.target_module,
                accepted_contract=prohibit,
            ),
        )
        forward = self.analyze(inspection, checks, modules)
        reverse = self.analyze(
            inspection, tuple(reversed(checks)), tuple(reversed(modules))
        )
        assert forward == reverse

    @pytest.mark.parametrize(
        ("case", "expected_status"),
        (
            pytest.param(
                "missing",
                PythonDependencyDirectionStatus.MISSING_CONTRACT,
                id="missing_exact_contract",
            ),
            pytest.param(
                "mismatched",
                PythonDependencyDirectionStatus.MISMATCHED_CONTRACT,
                id="contract_for_different_view",
            ),
            pytest.param(
                "prohibited",
                PythonDependencyDirectionStatus.PROHIBITED,
                id="exact_prohibition",
            ),
            pytest.param(
                "allowed",
                PythonDependencyDirectionStatus.ALLOWED,
                id="exact_allowance",
            ),
            pytest.param(
                "absent",
                PythonDependencyDirectionStatus.EDGE_ABSENT,
                id="contracted_edge_absent_from_view",
            ),
        ),
    )
    def test_artifact__dependency_direction__fails_closed_for_exact_requested_edge(
        self,
        case: Literal["missing", "mismatched", "prohibited", "allowed", "absent"],
        expected_status: PythonDependencyDirectionStatus,
    ) -> None:
        """Evidence ID: software-verification.harness.dependency-graphs.direction

        Requirement: Direction enforcement applies only to an explicitly requested
        exact observed edge and passes only under a supplied accepted contract for the
        same view and endpoints.

        Method: Evaluate semantic partitions for missing, mismatched, prohibiting,
        allowing, and edge-absent exact contracts.

        Oracle: Exact tuple equality of view/endpoints plus the supplied closed
        contract disposition; no repository architecture contract is inferred.

        Acceptance: Every case has the expected fail-closed status, only exact
        allowance passes, and other unrequested observed edges receive no result.

        Interpretation: Failure identifies invented dependency authority, contract
        substitution, or universal treatment of unlisted architecture edges.

        Limitations: Contract acceptance is an explicit caller input; this analyzer
        neither discovers nor human-accepts architecture policy.
        """
        inspection = self.inspect_resources()
        view = PythonDependencyGraphView.LEXICAL
        source = "pkg.alpha"
        target = "pkg.beta"
        contract: PythonAcceptedDependencyContract | None
        if case == "missing":
            contract = None
        elif case == "mismatched":
            contract = PythonAcceptedDependencyContract(
                contract_identity="architecture.edge.runtime-alpha-beta.allow.v1",
                view=PythonDependencyGraphView.RUNTIME_UNCONDITIONAL,
                source_module=source,
                target_module=target,
                direction=PythonDependencyDirection.ALLOW,
            )
        elif case == "prohibited":
            contract = PythonAcceptedDependencyContract(
                contract_identity="architecture.edge.alpha-beta.prohibit.v1",
                view=view,
                source_module=source,
                target_module=target,
                direction=PythonDependencyDirection.PROHIBIT,
            )
        elif case == "allowed":
            contract = PythonAcceptedDependencyContract(
                contract_identity="architecture.edge.alpha-beta.allow.v1",
                view=view,
                source_module=source,
                target_module=target,
                direction=PythonDependencyDirection.ALLOW,
            )
        else:
            target = "pkg.missing"
            contract = PythonAcceptedDependencyContract(
                contract_identity="architecture.edge.alpha-missing.allow.v1",
                view=view,
                source_module=source,
                target_module=target,
                direction=PythonDependencyDirection.ALLOW,
            )
        check = PythonDependencyDirectionCheck(
            view=view,
            source_module=source,
            target_module=target,
            accepted_contract=contract,
        )
        result = self.analyze(inspection, (check,))
        assert len(result.direction_results) == 1
        direction_result = result.direction_results[0]
        assert direction_result.status is expected_status
        assert direction_result.passed is (
            expected_status is PythonDependencyDirectionStatus.ALLOWED
        )
        lexical_edges = result.views[0].edges
        matching_edge = next(
            (
                edge
                for edge in lexical_edges
                if edge.source_module == source and edge.target_module == target
            ),
            None,
        )
        assert direction_result.edge == matching_edge
        if matching_edge is not None:
            assert direction_result.edge is not None
            assert direction_result.edge.provenance == matching_edge.provenance
        assert len(lexical_edges) > len(result.direction_results)
        assert not any(
            item.source_module == "pkg.beta" and item.target_module == "pkg.alpha"
            for item in result.direction_results
        )

    @pytest.mark.parametrize(
        "case",
        (
            pytest.param("identity_reuse", id="one_identity_two_payloads"),
            pytest.param("opposing_directions", id="one_edge_opposing_identities"),
        ),
    )
    def test_artifact__dependency_direction__rejects_conflicting_contracts(
        self, case: Literal["identity_reuse", "opposing_directions"]
    ) -> None:
        """Evidence ID: software-verification.harness.dependency-graphs.contract-id

        Requirement: One accepted-contract identity maps to exactly one payload, and
        one exact view/source/target edge cannot receive opposing directions even from
        differently identified contracts.

        Method: Supply direct request probes for identity reuse across payloads and
        distinct contract identities that allow and prohibit the same exact edge.

        Oracle: Exact contract identity, edge identity, and direction equality.

        Acceptance: Request construction fails before analysis without selecting a
        direction or inventing precedence.

        Interpretation: Failure identifies ambiguous or contradictory dependency
        authority capable of producing order-dependent results.

        Limitations: Human acceptance of each supplied contract remains external.
        """
        inspection = self.inspect_resources()
        identity = "architecture.edge.shared-identity.v1"
        allow = PythonAcceptedDependencyContract(
            contract_identity=identity,
            view=PythonDependencyGraphView.LEXICAL,
            source_module="pkg.alpha",
            target_module="pkg.beta",
            direction=PythonDependencyDirection.ALLOW,
        )
        if case == "identity_reuse":
            prohibit_identity = identity
            prohibit_source = "pkg.beta"
            prohibit_target = "pkg.alpha"
            error = "identity must map to one exact payload"
        else:
            prohibit_identity = "architecture.edge.alpha-beta.prohibit.v1"
            prohibit_source = allow.source_module
            prohibit_target = allow.target_module
            error = "exact dependency edge cannot have opposing contracts"
        prohibit = PythonAcceptedDependencyContract(
            contract_identity=prohibit_identity,
            view=PythonDependencyGraphView.LEXICAL,
            source_module=prohibit_source,
            target_module=prohibit_target,
            direction=PythonDependencyDirection.PROHIBIT,
        )
        checks = (
            PythonDependencyDirectionCheck(
                view=allow.view,
                source_module=allow.source_module,
                target_module=allow.target_module,
                accepted_contract=allow,
            ),
            PythonDependencyDirectionCheck(
                view=prohibit.view,
                source_module=prohibit.source_module,
                target_module=prohibit.target_module,
                accepted_contract=prohibit,
            ),
        )
        with pytest.raises(ValueError, match=error):
            PythonDependencyGraphRequest(
                production_facts=inspection,
                modules=self.bindings(inspection),
                direction_checks=checks,
            )

    @pytest.mark.parametrize(
        "case",
        (
            pytest.param("boolean_impostor", id="boolean_facade_impostor"),
            pytest.param("source_mismatch", id="binding_source_identity_mismatch"),
            pytest.param("outside_path", id="binding_path_escapes_repository"),
            pytest.param("request_impostor", id="request_subclass_impostor"),
        ),
    )
    def test_artifact__dependency_graph_records__rejects_malformed_and_impostor_inputs(
        self,
        case: Literal[
            "boolean_impostor",
            "source_mismatch",
            "outside_path",
            "request_impostor",
        ],
    ) -> None:
        """Evidence ID: software-verification.harness.dependency-graphs.rejection

        Requirement: Exact record and ActionObject boundaries reject wrong semantic
        scalar types, mismatched source bindings, and nominal request impostors.

        Method: Alter one binding dimension or supply an exact-type request subclass
        for each semantic parameter partition.

        Oracle: Built-in Boolean identity, accepted production source identity, and
        exact closed request type semantics.

        Acceptance: Wrong semantic types and impostors raise ``TypeError`` while an
        unmatched same-type source identity raises ``ValueError``.

        Interpretation: Failure identifies coercion, substitutable fact identity, or
        an open erased operation boundary.

        Limitations: Digest collision resistance is not tested.
        """
        inspection = self.inspect_resources()
        modules = self.bindings(inspection)
        if case == "boolean_impostor":
            with pytest.raises(TypeError, match="built-in bool"):
                replace(modules[0], is_package_facade=1)  # type: ignore[arg-type]
        elif case == "source_mismatch":
            malformed = (replace(modules[0], source_sha256="0" * 64), *modules[1:])
            with pytest.raises(ValueError, match="exactly cover"):
                PythonDependencyGraphRequest(
                    production_facts=inspection,
                    modules=malformed,
                    direction_checks=(),
                )
        elif case == "outside_path":
            with pytest.raises(ValueError, match="repository-relative POSIX"):
                replace(modules[0], source_path=PurePosixPath("../outside.py"))
        else:

            class ImpostorRequest(PythonDependencyGraphRequest):
                """Nominal impostor used only at the exact ActionObject boundary."""

            impostor = ImpostorRequest(
                production_facts=inspection,
                modules=modules,
                direction_checks=(),
            )
            with pytest.raises(TypeError, match="must be PythonDependencyGraphRequest"):
                PythonDependencyGraphAnalyzer().execute(impostor)

    @pytest.mark.parametrize(
        "case",
        (
            pytest.param("duplicate_nodes", id="duplicate_node_identity"),
            pytest.param("duplicate_edges", id="duplicate_edge_endpoints"),
            pytest.param("false_scc", id="partition_is_not_graph_scc"),
            pytest.param("wrong_provenance", id="provenance_resolves_elsewhere"),
            pytest.param("absent_allowed", id="allowed_result_edge_is_absent"),
            pytest.param("missing_erased", id="missing_contract_erases_observed_edge"),
            pytest.param(
                "mismatch_erased", id="mismatched_contract_erases_observed_edge"
            ),
            pytest.param("opposing_results", id="aggregate_retains_opposing_contracts"),
        ),
    )
    def test_artifact__dependency_graph_results__rejects_structurally_false_values(
        self,
        case: Literal[
            "duplicate_nodes",
            "duplicate_edges",
            "false_scc",
            "wrong_provenance",
            "absent_allowed",
            "missing_erased",
            "mismatch_erased",
            "opposing_results",
        ],
    ) -> None:
        """Evidence ID: software-verification.harness.dependency-graphs.result-closure

        Requirement: Closed graph results reject duplicate node/edge identities,
        provenance inconsistent with endpoints, non-SCC partitions, contradictory
        contracts, passing outcomes for absent edges, and erased observed-edge
        provenance for missing or mismatched contracts.

        Method: Alter exactly one derived result dimension per semantic partition and
        construct the applicable edge, view, or aggregate result directly.

        Oracle: Exact endpoint identity, provenance resolution, graph reachability,
        set uniqueness, contract direction consistency, and documented status meaning.

        Acceptance: Every structurally false construction raises ``ValueError`` at
        its owning record or graph-consistency boundary.

        Interpretation: Failure identifies a forgeable contradictory graph result.

        Limitations: Runtime import behavior and semantic architecture ownership remain
        outside structural result closure.
        """
        result = self.analyze(self.inspect_resources())
        lexical = result.views[0]
        if case == "duplicate_nodes":
            duplicate_node = PythonDependencyGraphNode(
                view=lexical.view, module_name=lexical.nodes[0].module_name
            )
            nodes = tuple(
                sorted(
                    (*lexical.nodes, duplicate_node),
                    key=lambda item: item.module_name,
                )
            )
            with pytest.raises(ValueError, match="unique module identities"):
                PythonDependencyGraphViewResult(
                    view=lexical.view,
                    nodes=nodes,
                    edges=lexical.edges,
                    strongly_connected_components=(
                        lexical.strongly_connected_components
                    ),
                )
        elif case == "duplicate_edges":
            edge = lexical.edges[-1]
            duplicate_edge = PythonDependencyGraphEdge(
                view=edge.view,
                source_module=edge.source_module,
                target_module=edge.target_module,
                provenance=edge.provenance,
            )
            edges = tuple(
                sorted(
                    (*lexical.edges, duplicate_edge),
                    key=lambda item: item.sort_key,
                )
            )
            with pytest.raises(ValueError, match="unique endpoint pairs"):
                PythonDependencyGraphViewResult(
                    view=lexical.view,
                    nodes=lexical.nodes,
                    edges=edges,
                    strongly_connected_components=(
                        lexical.strongly_connected_components
                    ),
                )
        elif case == "false_scc":
            false_components = tuple(
                PythonDependencyStronglyConnectedComponent(
                    view=lexical.view, module_names=(node.module_name,)
                )
                for node in lexical.nodes
            )
            with pytest.raises(ValueError, match="exact graph SCCs"):
                PythonDependencyGraphViewResult(
                    view=lexical.view,
                    nodes=lexical.nodes,
                    edges=lexical.edges,
                    strongly_connected_components=false_components,
                )
        elif case == "wrong_provenance":
            edge = next(
                item
                for item in lexical.edges
                if (item.source_module, item.target_module) == ("pkg.alpha", "pkg.beta")
            )
            elsewhere = next(
                item
                for item in lexical.edges
                if (item.source_module, item.target_module) == ("pkg.alpha", "pkg")
            )
            with pytest.raises(ValueError, match="exact edge endpoints"):
                PythonDependencyGraphEdge(
                    view=edge.view,
                    source_module=edge.source_module,
                    target_module=edge.target_module,
                    provenance=(elsewhere.provenance[0],),
                )
        elif case == "absent_allowed":
            contract = PythonAcceptedDependencyContract(
                contract_identity="architecture.edge.absent.allow.v1",
                view=PythonDependencyGraphView.LEXICAL,
                source_module="pkg.alpha",
                target_module="pkg.missing",
                direction=PythonDependencyDirection.ALLOW,
            )
            with pytest.raises(ValueError, match="requires an observed edge"):
                PythonDependencyDirectionResult(
                    view=contract.view,
                    source_module=contract.source_module,
                    target_module=contract.target_module,
                    accepted_contract=contract,
                    edge=None,
                    status=PythonDependencyDirectionStatus.ALLOWED,
                )
        else:
            edge = next(
                item
                for item in lexical.edges
                if (item.source_module, item.target_module) == ("pkg.alpha", "pkg.beta")
            )
            direction_results: tuple[PythonDependencyDirectionResult, ...]
            if case == "missing_erased":
                erased = PythonDependencyDirectionResult(
                    view=edge.view,
                    source_module=edge.source_module,
                    target_module=edge.target_module,
                    accepted_contract=None,
                    edge=None,
                    status=PythonDependencyDirectionStatus.MISSING_CONTRACT,
                )
                direction_results = (erased,)
                error = "observed direction edge and exact provenance"
            elif case == "mismatch_erased":
                mismatch = PythonAcceptedDependencyContract(
                    contract_identity="architecture.edge.runtime-alpha-beta.allow.v1",
                    view=PythonDependencyGraphView.RUNTIME_UNCONDITIONAL,
                    source_module=edge.source_module,
                    target_module=edge.target_module,
                    direction=PythonDependencyDirection.ALLOW,
                )
                erased = PythonDependencyDirectionResult(
                    view=edge.view,
                    source_module=edge.source_module,
                    target_module=edge.target_module,
                    accepted_contract=mismatch,
                    edge=None,
                    status=PythonDependencyDirectionStatus.MISMATCHED_CONTRACT,
                )
                direction_results = (erased,)
                error = "observed direction edge and exact provenance"
            else:
                allow = PythonAcceptedDependencyContract(
                    contract_identity="architecture.edge.alpha-beta.allow.v1",
                    view=edge.view,
                    source_module=edge.source_module,
                    target_module=edge.target_module,
                    direction=PythonDependencyDirection.ALLOW,
                )
                prohibit = PythonAcceptedDependencyContract(
                    contract_identity="architecture.edge.alpha-beta.prohibit.v1",
                    view=edge.view,
                    source_module=edge.source_module,
                    target_module=edge.target_module,
                    direction=PythonDependencyDirection.PROHIBIT,
                )
                direction_results = tuple(
                    sorted(
                        (
                            PythonDependencyDirectionResult(
                                view=edge.view,
                                source_module=edge.source_module,
                                target_module=edge.target_module,
                                accepted_contract=allow,
                                edge=edge,
                                status=PythonDependencyDirectionStatus.ALLOWED,
                            ),
                            PythonDependencyDirectionResult(
                                view=edge.view,
                                source_module=edge.source_module,
                                target_module=edge.target_module,
                                accepted_contract=prohibit,
                                edge=edge,
                                status=PythonDependencyDirectionStatus.PROHIBITED,
                            ),
                        ),
                        key=lambda item: item.sort_key,
                    )
                )
                error = "result dependency edge cannot have opposing contracts"
            with pytest.raises(ValueError, match=error):
                PythonDependencyGraphResult(
                    views=result.views,
                    direction_results=direction_results,
                )

    def test_artifact__dependency_graph_records__are_deeply_immutable(self) -> None:
        """Evidence ID: software-verification.harness.dependency-graphs.immutability

        Requirement: Requests, nodes, edges, provenance, components, contracts, checks,
        and results are operationally immutable with tuple-owned collections.

        Method: Construct the complete record graph, assert tuple nesting, and attempt
        representative field assignments on input and output records.

        Oracle: Frozen slotted dataclass and tuple semantics.

        Acceptance: Nested collections are tuples and assignment raises
        ``FrozenInstanceError`` without changing the result.

        Interpretation: Failure identifies mutable retained graph or policy state.

        Limitations: Reflection outside ordinary public APIs is excluded.
        """
        inspection = self.inspect_resources()
        modules = self.bindings(inspection)
        contract = PythonAcceptedDependencyContract(
            contract_identity="architecture.edge.alpha-beta.allow.v1",
            view=PythonDependencyGraphView.LEXICAL,
            source_module="pkg.alpha",
            target_module="pkg.beta",
            direction=PythonDependencyDirection.ALLOW,
        )
        check = PythonDependencyDirectionCheck(
            view=contract.view,
            source_module=contract.source_module,
            target_module=contract.target_module,
            accepted_contract=contract,
        )
        request = PythonDependencyGraphRequest(
            production_facts=inspection,
            modules=modules,
            direction_checks=(check,),
        )
        result = PythonDependencyGraphAnalyzer().execute(request)
        assert type(result.views) is tuple
        assert type(result.views[0].nodes) is tuple
        assert type(result.views[0].edges[0].provenance) is tuple
        assert type(result.views[0].strongly_connected_components) is tuple
        assert type(result.direction_results) is tuple
        with pytest.raises(FrozenInstanceError):
            request.modules = ()  # type: ignore[misc]
        with pytest.raises(FrozenInstanceError):
            result.views = ()  # type: ignore[misc]
        assert result.direction_results[0].passed

    def test_artifact__dependency_graph_views__has_no_discovery_or_mutation(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Evidence ID: software-verification.harness.dependency-graphs.boundaries

        Requirement: Analysis consumes only supplied facts/bindings, mutates neither,
        performs no discovery or repair, and creates no supported import route.

        Method: Build exact inputs first, prohibit path reads/writes during analysis,
        compare values after execution, and inspect the accepted package namespace.

        Oracle: Frozen input equality, prohibited filesystem effects, and deliberate
        package export membership.

        Acceptance: Analysis succeeds without reads/writes, inputs remain equal, and
        the analyzer is absent from the conformance package namespace.

        Interpretation: Failure identifies ambient discovery, mutation, repair, or
        supported-export widening.

        Limitations: Git and external processes are not invoked by the analyzer.
        """
        inspection = self.inspect_resources()
        modules = self.bindings(inspection)
        original_inspection = inspection
        original_modules = modules

        def prohibit_read(path: Path) -> bytes:
            raise AssertionError(f"unexpected read: {path}")

        def prohibit_write(path: Path, data: bytes) -> int:
            raise AssertionError(f"unexpected write: {path} {len(data)}")

        monkeypatch.setattr(Path, "read_bytes", prohibit_read)
        monkeypatch.setattr(Path, "write_bytes", prohibit_write)
        result = self.analyze(inspection, modules=modules)
        assert result.views
        assert inspection == original_inspection
        assert modules == original_modules

        import ksdft2effmass.harness.pi.conformance.python as python_conformance

        assert not hasattr(python_conformance, "PythonDependencyGraphAnalyzer")
