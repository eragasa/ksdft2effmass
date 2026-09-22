"""Adapt accepted architecture-conformance results into foundation records."""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.harness.pi.conformance.python.dependency_graph import (
    PythonDependencyGraphAnalyzer,
    PythonDependencyGraphRequest,
    PythonDependencyModule,
)
from ksdft2effmass.harness.pi.conformance.python.production import (
    PythonProductionSource,
    PythonProductionSourceInspector,
    PythonProductionSourceProfile,
)
from python_public_import_foundation_model import (
    DependencyEdge,
    DependencyGraphView,
    DependencyGraphViewKind,
    InputCategory,
    ProductionAllResolution,
    ProductionFactOutput,
)

from public_import_foundation.input_snapshot import (
    FoundationFormatError,
    FoundationInputManifest,
)
from public_import_foundation.source_observation import PythonDefiningOriginResolver


@dataclass(frozen=True, slots=True)
class ArchitectureConformanceAdapter:
    """Execute accepted fact and named-view owners on selected bytes."""

    def execute(
        self, manifest: FoundationInputManifest, payloads: dict[str, bytes]
    ) -> tuple[tuple[ProductionFactOutput, ...], tuple[DependencyGraphView, ...]]:
        """Return closed current production and dependency-graph records."""
        selected = tuple(
            entry
            for entry in manifest.entries
            if entry.category is InputCategory.PRODUCTION_MODULE
        )
        sources = tuple(
            PythonProductionSource.from_payload(
                input_identity=entry.sha256,
                path=entry.path,
                payload=payloads[entry.path.as_posix()],
            )
            for entry in selected
        )
        production = PythonProductionSourceInspector().execute(
            PythonProductionSourceProfile(), sources
        )
        modules = tuple(
            PythonDependencyModule(
                module_name=PythonDefiningOriginResolver.module_name(
                    entry.path.as_posix()
                )[0],
                is_package_facade=PythonDefiningOriginResolver.module_name(
                    entry.path.as_posix()
                )[1],
                input_identity=entry.sha256,
                source_path=entry.path,
                source_sha256=entry.sha256,
            )
            for entry in selected
        )
        graph = PythonDependencyGraphAnalyzer().execute(
            PythonDependencyGraphRequest(
                production_facts=production,
                modules=modules,
                direction_checks=(),
            )
        )
        module_name_by_path = {
            entry.path.as_posix(): PythonDefiningOriginResolver.module_name(
                entry.path.as_posix()
            )[0]
            for entry in selected
        }
        production_records: list[ProductionFactOutput] = []
        for inspection in production.modules:
            if (
                inspection.facts is None
                or inspection.source_sha256 is None
                or inspection.source_byte_count is None
            ):
                raise FoundationFormatError(
                    f"selected production fact failed: {inspection.path.as_posix()}"
                )
            facts = inspection.facts
            production_records.append(
                ProductionFactOutput(
                    module_name=module_name_by_path[inspection.path.as_posix()],
                    path=inspection.path.as_posix(),
                    source_sha256=inspection.source_sha256,
                    source_byte_count=inspection.source_byte_count,
                    class_count=len(facts.classes),
                    callable_count=len(facts.callables),
                    import_count=len(facts.imports),
                    call_count=len(facts.calls),
                    all_syntax_count=len(facts.all_syntax),
                    effective_all_resolution=ProductionAllResolution(
                        facts.effective_all_resolution.value
                    ),
                    effective_all_names=facts.effective_all_names,
                )
            )
        source_identities = tuple(
            sorted(
                inspection.source_sha256
                for inspection in production.modules
                if inspection.source_sha256 is not None
            )
        )
        graph_records = tuple(
            DependencyGraphView(
                view=DependencyGraphViewKind(view.view.value),
                node_names=tuple(node.module_name for node in view.nodes),
                edges=tuple(
                    DependencyEdge(
                        source_module=edge.source_module,
                        target_module=edge.target_module,
                    )
                    for edge in view.edges
                ),
                strongly_connected_components=tuple(
                    component.module_names
                    for component in view.strongly_connected_components
                ),
                source_identities=source_identities,
            )
            for view in graph.views
        )
        return tuple(production_records), graph_records
