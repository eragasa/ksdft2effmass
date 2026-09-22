"""Command, serialization, and atomic output for current-fact supplementation."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile

from python_public_import_current_fact_supplement_model import (
    AcquisitionManifest,
    CurrentFactSupplement,
    CurrentRouteObservation,
    ExtractionRole,
    InputVariant,
    SelectionEntry,
    SelectionSerializer,
    SupplementalRouteCandidate,
    SupplementJsonCodec,
    SupplementOperation,
    SupplementSummary,
    ZeroBoundaryTransition,
)
from python_public_import_foundation_model import (
    AuthorityCitation,
    AuthorityState,
    BindingKind,
    BindingOriginResolution,
    DependencyEdge,
    DependencyGraphView,
    DependencyGraphViewKind,
    DocumentationCitation,
    ImportKind,
    ImportObservation,
    JsonRecord,
    JsonValue,
    PackageBinding,
    PackageSurface,
    PredecessorRoute,
    ProductionAllResolution,
    ProductionFactOutput,
    RuntimeAttribute,
    RuntimeDistribution,
    RuntimeEnvironment,
    RuntimeFailure,
    RuntimeFailureKind,
    RuntimeLoadedFile,
    RuntimeObservation,
    RuntimeObservationView,
    RuntimeSuccess,
)

from public_import_current_fact_supplement.delta_acquisition import (
    AcquisitionManifestSerializer,
    CurrentFactSupplementAcquirer,
)
from public_import_current_fact_supplement.supplement_assembly import (
    CurrentFactSupplementAssembler,
)


@dataclass(frozen=True, slots=True)
class SupplementCommandArguments:
    """Represent one exact acquire or generate invocation."""

    operation: SupplementOperation
    repository_root: Path | None
    selection: Path | None
    snapshot_root: Path
    manifest: Path
    output: Path | None
    python_executable: Path | None

    def __post_init__(self) -> None:
        if type(self.operation) is not SupplementOperation:
            raise TypeError("operation must be SupplementOperation")

    @classmethod
    def parse(cls, arguments: tuple[str, ...]) -> SupplementCommandArguments:
        """Parse one closed command line."""
        if not arguments:
            raise ValueError("first argument must be acquire or generate")
        operation = SupplementOperation(arguments[0])
        values: dict[str, Path] = {}
        rest = arguments[1:]
        if len(rest) % 2:
            raise ValueError("every option requires one value")
        for index in range(0, len(rest), 2):
            if rest[index] in values:
                raise ValueError(f"duplicate option: {rest[index]}")
            values[rest[index]] = Path(rest[index + 1]).resolve()
        expected = (
            {"--repository-root", "--selection", "--snapshot-root", "--manifest"}
            if operation is SupplementOperation.ACQUIRE
            else {
                "--repository-root",
                "--snapshot-root",
                "--manifest",
                "--output",
                "--python-executable",
            }
        )
        if set(values) != expected:
            raise ValueError(
                f"{operation.value} options do not match the closed command contract"
            )
        return cls(
            operation=operation,
            repository_root=values.get("--repository-root"),
            selection=values.get("--selection"),
            snapshot_root=values["--snapshot-root"],
            manifest=values["--manifest"],
            output=values.get("--output"),
            python_executable=values.get("--python-executable"),
        )


class SupplementAliasPolicy:
    """Reject exact filesystem aliases before any write occurs."""

    __slots__ = ()

    @staticmethod
    def acquisition(
        repository_root: Path,
        selection_path: Path,
        snapshot_root: Path,
        manifest_path: Path,
        selections: tuple[SelectionEntry, ...],
    ) -> None:
        """Reject an acquisition output that aliases any input or destination."""
        output = manifest_path.resolve()
        aliases = {selection_path.resolve(), snapshot_root.resolve()}
        for selection in selections:
            aliases.add((repository_root / selection.path.as_posix()).resolve())
            if ExtractionRole.IDENTITY_ONLY not in selection.roles:
                namespace = (
                    "task-tools"
                    if selection.variant is InputVariant.TASK_TOOL
                    else "base"
                    if selection.variant is InputVariant.BASE_TREE
                    else "target"
                )
                aliases.add(
                    (snapshot_root / namespace / selection.path.as_posix()).resolve()
                )
        if output in aliases:
            raise ValueError(
                "acquisition manifest output aliases an input or destination"
            )

    @staticmethod
    def generation(
        repository_root: Path,
        snapshot_root: Path,
        manifest_path: Path,
        interpreter: Path,
        output_path: Path,
        manifest: AcquisitionManifest,
    ) -> None:
        """Reject a report output that aliases any decoded generation input."""
        if type(manifest) is not AcquisitionManifest:
            raise TypeError("manifest must be AcquisitionManifest")
        output = output_path.resolve()
        root = snapshot_root.resolve()
        aliases = {
            root,
            manifest_path.resolve(),
            interpreter.resolve(),
            (
                repository_root
                / "harness/reports/public-import-boundaries/phase3/current-fact-supplement-selection.tsv"
            ).resolve(),
        }
        for item in manifest.inputs:
            aliases.add((repository_root / item.selection.path.as_posix()).resolve())
            if item.snapshot_path is None:
                continue
            selected = (snapshot_root / item.snapshot_path.as_posix()).resolve()
            if not selected.is_relative_to(root):
                raise ValueError(
                    "decoded snapshot path escapes the explicit snapshot root"
                )
            aliases.add(selected)
        if output in aliases:
            raise ValueError("report output aliases a generation input")


class SupplementAtomicWriter:
    """Own same-directory atomic replacement."""

    __slots__ = ()

    def execute(self, path: Path, payload: bytes) -> None:
        """Replace an output only after complete payload construction."""
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary: Path | None = None
        try:
            with NamedTemporaryFile(
                mode="wb", dir=path.parent, prefix=f".{path.name}.", delete=False
            ) as stream:
                stream.write(payload)
                stream.flush()
                os.fsync(stream.fileno())
                temporary = Path(stream.name)
            os.replace(temporary, path)
        finally:
            if temporary is not None and temporary.exists():
                temporary.unlink()


@dataclass(frozen=True, slots=True)
class CurrentFactSupplementCommand:
    """Execute explicit acquisition or pure snapshot generation."""

    def execute(self, arguments: SupplementCommandArguments) -> None:
        """Execute one command and atomically write its output."""
        if arguments.operation is SupplementOperation.ACQUIRE:
            if arguments.repository_root is None or arguments.selection is None:
                raise AssertionError("acquire arguments are incomplete")
            selections = SelectionSerializer().decode(arguments.selection.read_bytes())
            SupplementAliasPolicy.acquisition(
                arguments.repository_root,
                arguments.selection,
                arguments.snapshot_root,
                arguments.manifest,
                selections,
            )
            if arguments.snapshot_root.exists() and any(
                arguments.snapshot_root.iterdir()
            ):
                raise ValueError("snapshot root must be absent or empty")
            arguments.snapshot_root.mkdir(parents=True, exist_ok=True)
            manifest = CurrentFactSupplementAcquirer(
                arguments.repository_root, arguments.snapshot_root
            ).execute(arguments.selection)
            SupplementAtomicWriter().execute(
                arguments.manifest, AcquisitionManifestSerializer().encode(manifest)
            )
            return
        if arguments.operation is not SupplementOperation.GENERATE:
            raise AssertionError("operation discriminant is not exhaustive")
        if (
            arguments.repository_root is None
            or arguments.output is None
            or arguments.python_executable is None
        ):
            raise AssertionError("generate arguments are incomplete")
        manifest_payload = arguments.manifest.read_bytes()
        manifest = AcquisitionManifestSerializer().decode(manifest_payload)
        SupplementAliasPolicy.generation(
            arguments.repository_root,
            arguments.snapshot_root,
            arguments.manifest,
            arguments.python_executable,
            arguments.output,
            manifest,
        )
        report = CurrentFactSupplementAssembler(
            arguments.snapshot_root, arguments.python_executable
        ).execute(manifest, __import__("hashlib").sha256(manifest_payload).hexdigest())
        SupplementAtomicWriter().execute(
            arguments.output, CurrentFactSupplementSerializer().encode(report)
        )


class CurrentFactSupplementSerializer:
    """Serialize the validated closed supplement."""

    __slots__ = ()

    def encode(self, report: CurrentFactSupplement) -> bytes:
        """Return canonical JSON bytes."""
        root: JsonRecord = {
            "authority_citations": [
                {
                    "authority_state": item.authority_state.value,
                    "column": item.column,
                    "line": item.line,
                    "matched_term": item.matched_term,
                    "path": item.path,
                }
                for item in report.authority_citations
            ],
            "claim_boundaries": list(report.claim_boundaries),
            "consumer_imports": [
                self._import(item) for item in report.consumer_imports
            ],
            "current_empty_surfaces": list(report.current_empty_surfaces),
            "current_package_surfaces": [
                self._surface(item) for item in report.current_package_surfaces
            ],
            "current_production_modules": [
                self._production(item) for item in report.current_production_modules
            ],
            "current_routes": [self._route(item) for item in report.current_routes],
            "delta_ledger": [
                AcquisitionManifestSerializer.ledger_record(item)
                for item in report.delta_ledger
            ],
            "dependency_graph_views": [
                {
                    "edges": [
                        {
                            "source_module": edge.source_module,
                            "target_module": edge.target_module,
                        }
                        for edge in item.edges
                    ],
                    "node_names": list(item.node_names),
                    "source_identities": list(item.source_identities),
                    "strongly_connected_components": [
                        list(component)
                        for component in item.strongly_connected_components
                    ],
                    "view": item.view.value,
                }
                for item in report.dependency_graph_views
            ],
            "documentation_citations": [
                {
                    "column": item.column,
                    "line": item.line,
                    "path": item.path,
                    "route_text": item.route_text,
                }
                for item in report.documentation_citations
            ],
            "manifest_sha256": report.manifest_sha256,
            "predecessor_package_observations": [
                self._surface(item) for item in report.predecessor_package_observations
            ],
            "predecessor_routes": [
                {
                    "compatibility_disposition": item.compatibility_disposition,
                    "defining_module": item.defining_module,
                    "defining_symbol": item.defining_symbol,
                    "exported_name": item.exported_name,
                    "package": item.package,
                    "route": item.route,
                    "support_status": item.support_status,
                }
                for item in report.predecessor_routes
            ],
            "runtime_environment": {
                "distributions": [
                    [item.name, item.version]
                    for item in report.runtime_environment.distributions
                ],
                "environment_sha256": report.runtime_environment.environment_sha256,
                "executable_byte_count": report.runtime_environment.executable_byte_count,
                "executable_sha256": report.runtime_environment.executable_sha256,
                "implementation": report.runtime_environment.implementation,
                "source_root": report.runtime_environment.source_root,
                "version": report.runtime_environment.version,
            },
            "runtime_observations": [
                self._runtime(item) for item in report.runtime_observations
            ],
            "schema_version": report.schema_version,
            "subject_identity": report.subject_identity,
            "subject_version": report.subject_version,
            "summary": {
                "accepted_zero_lineage_count": report.summary.accepted_zero_lineage_count,
                "added_path_count": report.summary.added_path_count,
                "current_empty_surface_count": report.summary.current_empty_surface_count,
                "current_route_count": report.summary.current_route_count,
                "deleted_path_count": report.summary.deleted_path_count,
                "delta_path_count": report.summary.delta_path_count,
                "modified_path_count": report.summary.modified_path_count,
                "package_surface_count": report.summary.package_surface_count,
                "predecessor_route_count": report.summary.predecessor_route_count,
                "production_module_count": report.summary.production_module_count,
                "supplemental_candidate_count": report.summary.supplemental_candidate_count,
                "zero_boundary_transition_count": report.summary.zero_boundary_transition_count,
            },
            "supplemental_candidates": [
                {
                    "candidate_key": item.candidate_key,
                    "compatibility_disposition": item.compatibility_disposition,
                    "route": self._route(item.route),
                    "support_status": item.support_status,
                }
                for item in report.supplemental_candidates
            ],
            "topology": AcquisitionManifestSerializer.topology_record(report.topology),
            "zero_boundary_transitions": [
                {
                    "current_route_keys": list(item.current_route_keys),
                    "current_state": item.current_state,
                    "package": item.package,
                    "predecessor_state": item.predecessor_state,
                }
                for item in report.zero_boundary_transitions
            ],
            "accepted_zero_boundary_lineages": list(
                report.accepted_zero_boundary_lineages
            ),
        }
        return SupplementJsonCodec().encode(root)

    @staticmethod
    def _binding(item: PackageBinding) -> JsonRecord:
        row: JsonRecord = {
            "imported_name": item.imported_name,
            "kind": item.kind.value,
            "line": item.line,
            "local_name": item.local_name,
            "origin": item.origin,
        }
        if item.defining_origin is not None and item.origin_resolution is not None:
            row["defining_origin"] = item.defining_origin
            row["origin_resolution"] = item.origin_resolution.value
        return row

    def _surface(self, item: PackageSurface) -> JsonRecord:
        return {
            "bindings": [self._binding(binding) for binding in item.bindings],
            "declares_all": item.declares_all,
            "effective_star_names": list(item.effective_star_names),
            "initializer_byte_count": item.initializer_byte_count,
            "initializer_path": item.initializer_path,
            "initializer_sha256": item.initializer_sha256,
            "package": item.package,
        }

    @staticmethod
    def _production(item: ProductionFactOutput) -> JsonRecord:
        return {
            "all_syntax_count": item.all_syntax_count,
            "call_count": item.call_count,
            "callable_count": item.callable_count,
            "class_count": item.class_count,
            "effective_all_names": None
            if item.effective_all_names is None
            else list(item.effective_all_names),
            "effective_all_resolution": item.effective_all_resolution.value,
            "import_count": item.import_count,
            "module_name": item.module_name,
            "path": item.path,
            "source_byte_count": item.source_byte_count,
            "source_sha256": item.source_sha256,
        }

    @staticmethod
    def _route(item: CurrentRouteObservation) -> JsonRecord:
        return {
            "defining_origin": item.defining_origin,
            "direct_origin": item.direct_origin,
            "exported_name": item.exported_name,
            "package": item.package,
            "predecessor_route": item.predecessor_route,
            "route": item.route,
        }

    @staticmethod
    def _import(item: ImportObservation) -> JsonRecord:
        return {
            "column": item.column,
            "consumer_path": item.consumer_path,
            "import_kind": item.import_kind.value,
            "imported_module": item.imported_module,
            "imported_name": item.imported_name,
            "line": item.line,
        }

    @staticmethod
    def _runtime(item: RuntimeObservation) -> JsonRecord:
        outcome = item.observation
        files: list[JsonValue] = [
            {
                "byte_count": loaded.byte_count,
                "module_name": loaded.module_name,
                "path": loaded.path,
                "sha256": loaded.sha256,
            }
            for loaded in outcome.loaded_files
        ]
        if type(outcome) is RuntimeSuccess:
            represented: JsonRecord = {
                "attributes": [
                    {
                        "defining_module": value.defining_module,
                        "name": value.name,
                        "value_type": value.value_type,
                    }
                    for value in outcome.attributes
                ],
                "loaded_files": files,
                "status": "success",
            }
        elif type(outcome) is RuntimeFailure:
            represented = {
                "exception_type": outcome.exception_type,
                "failure_kind": outcome.failure_kind.value,
                "loaded_files": files,
                "message": outcome.message,
                "status": "failure",
            }
        else:
            raise TypeError("runtime outcome is not closed")
        return {
            "environment_sha256": item.environment_sha256,
            "observation": represented,
            "package": item.package,
            "view": item.view.value,
        }


class CurrentFactSupplementParser:
    """Decode canonical supplement JSON into closed immutable records."""

    __slots__ = ()

    def decode(self, payload: bytes) -> CurrentFactSupplement:
        """Parse exact bytes and reject every unknown or malformed field."""
        value = SupplementJsonCodec().decode(payload)
        root = self._closed(
            value,
            {
                "accepted_zero_boundary_lineages",
                "authority_citations",
                "claim_boundaries",
                "consumer_imports",
                "current_empty_surfaces",
                "current_package_surfaces",
                "current_production_modules",
                "current_routes",
                "delta_ledger",
                "dependency_graph_views",
                "documentation_citations",
                "manifest_sha256",
                "predecessor_package_observations",
                "predecessor_routes",
                "runtime_environment",
                "runtime_observations",
                "schema_version",
                "subject_identity",
                "subject_version",
                "summary",
                "supplemental_candidates",
                "topology",
                "zero_boundary_transitions",
            },
            "supplement",
        )
        acquisition = AcquisitionManifestSerializer()
        report = CurrentFactSupplement(
            schema_version=self._integer(root["schema_version"], "schema_version"),
            subject_identity=self._text(root["subject_identity"], "subject_identity"),
            subject_version=self._text(root["subject_version"], "subject_version"),
            manifest_sha256=self._sha(root["manifest_sha256"], "manifest_sha256"),
            topology=acquisition.parse_topology_value(root["topology"]),
            delta_ledger=acquisition.parse_ledger_values(root["delta_ledger"]),
            predecessor_routes=tuple(
                self._route(item, index)
                for index, item in enumerate(
                    self._array(root["predecessor_routes"], "predecessor_routes")
                )
            ),
            predecessor_package_observations=tuple(
                self._package(item, index, "predecessor_package")
                for index, item in enumerate(
                    self._array(
                        root["predecessor_package_observations"],
                        "predecessor_package_observations",
                    )
                )
            ),
            current_production_modules=tuple(
                self._production(item, index)
                for index, item in enumerate(
                    self._array(
                        root["current_production_modules"], "current_production_modules"
                    )
                )
            ),
            current_package_surfaces=tuple(
                self._package(item, index, "current_package")
                for index, item in enumerate(
                    self._array(
                        root["current_package_surfaces"], "current_package_surfaces"
                    )
                )
            ),
            current_routes=tuple(
                self._current_route(item, index)
                for index, item in enumerate(
                    self._array(root["current_routes"], "current_routes")
                )
            ),
            supplemental_candidates=tuple(
                self._candidate(item, index)
                for index, item in enumerate(
                    self._array(
                        root["supplemental_candidates"], "supplemental_candidates"
                    )
                )
            ),
            accepted_zero_boundary_lineages=self._texts(
                root["accepted_zero_boundary_lineages"],
                "accepted_zero_boundary_lineages",
            ),
            current_empty_surfaces=self._texts(
                root["current_empty_surfaces"], "current_empty_surfaces"
            ),
            zero_boundary_transitions=tuple(
                self._transition(item, index)
                for index, item in enumerate(
                    self._array(
                        root["zero_boundary_transitions"], "zero_boundary_transitions"
                    )
                )
            ),
            consumer_imports=tuple(
                self._import(item, index)
                for index, item in enumerate(
                    self._array(root["consumer_imports"], "consumer_imports")
                )
            ),
            documentation_citations=tuple(
                self._documentation(item, index)
                for index, item in enumerate(
                    self._array(
                        root["documentation_citations"], "documentation_citations"
                    )
                )
            ),
            authority_citations=tuple(
                self._authority(item, index)
                for index, item in enumerate(
                    self._array(root["authority_citations"], "authority_citations")
                )
            ),
            dependency_graph_views=tuple(
                self._graph(item, index)
                for index, item in enumerate(
                    self._array(
                        root["dependency_graph_views"], "dependency_graph_views"
                    )
                )
            ),
            runtime_environment=self._runtime_environment(root["runtime_environment"]),
            runtime_observations=tuple(
                self._runtime(item, index)
                for index, item in enumerate(
                    self._array(root["runtime_observations"], "runtime_observations")
                )
            ),
            claim_boundaries=self._texts(root["claim_boundaries"], "claim_boundaries"),
            summary=self._summary(root["summary"]),
        )
        if CurrentFactSupplementSerializer().encode(report) != payload:
            raise ValueError("supplement JSON is not canonical")
        return report

    def _route(self, value: JsonValue, index: int) -> PredecessorRoute:
        row = self._closed(
            value,
            {
                "compatibility_disposition",
                "defining_module",
                "defining_symbol",
                "exported_name",
                "package",
                "route",
                "support_status",
            },
            f"predecessor_route[{index}]",
        )
        return PredecessorRoute(
            route=self._text(row["route"], "route"),
            package=self._text(row["package"], "package"),
            exported_name=self._text(row["exported_name"], "exported_name"),
            defining_module=self._text(row["defining_module"], "defining_module"),
            defining_symbol=self._text(row["defining_symbol"], "defining_symbol"),
            support_status=self._text(row["support_status"], "support_status"),
            compatibility_disposition=self._text(
                row["compatibility_disposition"], "compatibility_disposition"
            ),
        )

    def _binding(self, value: JsonValue) -> PackageBinding:
        row = self._record(value, "binding")
        base = {"imported_name", "kind", "line", "local_name", "origin"}
        if set(row) == base:
            defining = None
            resolution = None
        elif set(row) == base | {"defining_origin", "origin_resolution"}:
            defining = self._text(row["defining_origin"], "defining_origin")
            resolution = BindingOriginResolution(
                self._text(row["origin_resolution"], "origin_resolution")
            )
        else:
            raise ValueError("binding fields do not match the closed contract")
        return PackageBinding(
            kind=BindingKind(self._text(row["kind"], "kind")),
            line=self._positive(row["line"], "line"),
            local_name=self._text(row["local_name"], "local_name"),
            imported_name=self._text(row["imported_name"], "imported_name"),
            origin=self._text(row["origin"], "origin"),
            defining_origin=defining,
            origin_resolution=resolution,
        )

    def _package(self, value: JsonValue, index: int, prefix: str) -> PackageSurface:
        row = self._closed(
            value,
            {
                "bindings",
                "declares_all",
                "effective_star_names",
                "initializer_byte_count",
                "initializer_path",
                "initializer_sha256",
                "package",
            },
            f"{prefix}[{index}]",
        )
        declares = row["declares_all"]
        if type(declares) is not bool:
            raise ValueError("declares_all must be bool")
        return PackageSurface(
            package=self._text(row["package"], "package"),
            initializer_path=self._text(row["initializer_path"], "initializer_path"),
            initializer_byte_count=self._nonnegative(
                row["initializer_byte_count"], "initializer_byte_count"
            ),
            initializer_sha256=self._sha(
                row["initializer_sha256"], "initializer_sha256"
            ),
            declares_all=declares,
            effective_star_names=self._texts(
                row["effective_star_names"], "effective_star_names"
            ),
            bindings=tuple(
                self._binding(item) for item in self._array(row["bindings"], "bindings")
            ),
        )

    def _production(self, value: JsonValue, index: int) -> ProductionFactOutput:
        row = self._closed(
            value,
            {
                "all_syntax_count",
                "call_count",
                "callable_count",
                "class_count",
                "effective_all_names",
                "effective_all_resolution",
                "import_count",
                "module_name",
                "path",
                "source_byte_count",
                "source_sha256",
            },
            f"production[{index}]",
        )
        raw_names = row["effective_all_names"]
        names = (
            None if raw_names is None else self._texts(raw_names, "effective_all_names")
        )
        return ProductionFactOutput(
            module_name=self._text(row["module_name"], "module_name"),
            path=self._text(row["path"], "path"),
            source_sha256=self._sha(row["source_sha256"], "source_sha256"),
            source_byte_count=self._nonnegative(
                row["source_byte_count"], "source_byte_count"
            ),
            class_count=self._nonnegative(row["class_count"], "class_count"),
            callable_count=self._nonnegative(row["callable_count"], "callable_count"),
            import_count=self._nonnegative(row["import_count"], "import_count"),
            call_count=self._nonnegative(row["call_count"], "call_count"),
            all_syntax_count=self._nonnegative(
                row["all_syntax_count"], "all_syntax_count"
            ),
            effective_all_resolution=ProductionAllResolution(
                self._text(row["effective_all_resolution"], "effective_all_resolution")
            ),
            effective_all_names=names,
        )

    def _current_route(self, value: JsonValue, index: int) -> CurrentRouteObservation:
        row = self._closed(
            value,
            {
                "defining_origin",
                "direct_origin",
                "exported_name",
                "package",
                "predecessor_route",
                "route",
            },
            f"current_route[{index}]",
        )
        predecessor = row["predecessor_route"]
        if type(predecessor) is not bool:
            raise ValueError("predecessor_route must be bool")
        return CurrentRouteObservation(
            route=self._text(row["route"], "route"),
            package=self._text(row["package"], "package"),
            exported_name=self._text(row["exported_name"], "exported_name"),
            direct_origin=self._text(row["direct_origin"], "direct_origin"),
            defining_origin=self._text(row["defining_origin"], "defining_origin"),
            predecessor_route=predecessor,
        )

    def _candidate(self, value: JsonValue, index: int) -> SupplementalRouteCandidate:
        row = self._closed(
            value,
            {"candidate_key", "compatibility_disposition", "route", "support_status"},
            f"candidate[{index}]",
        )
        return SupplementalRouteCandidate(
            candidate_key=self._text(row["candidate_key"], "candidate_key"),
            route=self._current_route(row["route"], index),
            support_status=self._text(row["support_status"], "support_status"),
            compatibility_disposition=self._text(
                row["compatibility_disposition"], "compatibility_disposition"
            ),
        )

    def _transition(self, value: JsonValue, index: int) -> ZeroBoundaryTransition:
        row = self._closed(
            value,
            {"current_route_keys", "current_state", "package", "predecessor_state"},
            f"transition[{index}]",
        )
        return ZeroBoundaryTransition(
            package=self._text(row["package"], "package"),
            predecessor_state=self._text(row["predecessor_state"], "predecessor_state"),
            current_state=self._text(row["current_state"], "current_state"),
            current_route_keys=self._texts(
                row["current_route_keys"], "current_route_keys"
            ),
        )

    def _import(self, value: JsonValue, index: int) -> ImportObservation:
        row = self._closed(
            value,
            {
                "column",
                "consumer_path",
                "import_kind",
                "imported_module",
                "imported_name",
                "line",
            },
            f"consumer_import[{index}]",
        )
        raw_name = row["imported_name"]
        return ImportObservation(
            consumer_path=self._text(row["consumer_path"], "consumer_path"),
            line=self._positive(row["line"], "line"),
            column=self._nonnegative(row["column"], "column"),
            import_kind=ImportKind(self._text(row["import_kind"], "import_kind")),
            imported_module=self._text(row["imported_module"], "imported_module"),
            imported_name=None
            if raw_name is None
            else self._text(raw_name, "imported_name"),
        )

    def _documentation(self, value: JsonValue, index: int) -> DocumentationCitation:
        row = self._closed(
            value, {"column", "line", "path", "route_text"}, f"documentation[{index}]"
        )
        return DocumentationCitation(
            self._text(row["path"], "path"),
            self._positive(row["line"], "line"),
            self._nonnegative(row["column"], "column"),
            self._text(row["route_text"], "route_text"),
        )

    def _authority(self, value: JsonValue, index: int) -> AuthorityCitation:
        row = self._closed(
            value,
            {"authority_state", "column", "line", "matched_term", "path"},
            f"authority[{index}]",
        )
        return AuthorityCitation(
            self._text(row["path"], "path"),
            self._positive(row["line"], "line"),
            self._nonnegative(row["column"], "column"),
            self._text(row["matched_term"], "matched_term"),
            AuthorityState(self._text(row["authority_state"], "authority_state")),
        )

    def _graph(self, value: JsonValue, index: int) -> DependencyGraphView:
        row = self._closed(
            value,
            {
                "edges",
                "node_names",
                "source_identities",
                "strongly_connected_components",
                "view",
            },
            f"graph[{index}]",
        )
        edges = tuple(
            DependencyEdge(
                self._text(edge["source_module"], "source_module"),
                self._text(edge["target_module"], "target_module"),
            )
            for item in self._array(row["edges"], "edges")
            for edge in [self._closed(item, {"source_module", "target_module"}, "edge")]
        )
        components = tuple(
            self._texts(item, "component")
            for item in self._array(row["strongly_connected_components"], "components")
        )
        return DependencyGraphView(
            view=DependencyGraphViewKind(self._text(row["view"], "view")),
            node_names=self._texts(row["node_names"], "node_names"),
            edges=edges,
            strongly_connected_components=components,
            source_identities=tuple(
                self._sha(item, "source_identity")
                for item in self._array(row["source_identities"], "source_identities")
            ),
        )

    def _runtime_environment(self, value: JsonValue) -> RuntimeEnvironment:
        row = self._closed(
            value,
            {
                "distributions",
                "environment_sha256",
                "executable_byte_count",
                "executable_sha256",
                "implementation",
                "source_root",
                "version",
            },
            "runtime_environment",
        )
        distributions = tuple(
            self._distribution(item)
            for item in self._array(row["distributions"], "distributions")
        )
        return RuntimeEnvironment(
            executable_byte_count=self._nonnegative(
                row["executable_byte_count"], "executable_byte_count"
            ),
            executable_sha256=self._sha(row["executable_sha256"], "executable_sha256"),
            implementation=self._text(row["implementation"], "implementation"),
            version=self._text(row["version"], "version"),
            distributions=distributions,
            source_root=self._text(row["source_root"], "source_root"),
            environment_sha256=self._sha(
                row["environment_sha256"], "environment_sha256"
            ),
        )

    def _distribution(self, value: JsonValue) -> RuntimeDistribution:
        pair = self._array(value, "distribution")
        if len(pair) != 2:
            raise ValueError("distribution must have two fields")
        return RuntimeDistribution(
            self._text(pair[0], "distribution_name"),
            self._text(pair[1], "distribution_version"),
        )

    def _loaded(self, value: JsonValue) -> RuntimeLoadedFile:
        row = self._closed(
            value, {"byte_count", "module_name", "path", "sha256"}, "loaded_file"
        )
        return RuntimeLoadedFile(
            self._text(row["module_name"], "module_name"),
            self._text(row["path"], "path"),
            self._nonnegative(row["byte_count"], "byte_count"),
            self._sha(row["sha256"], "sha256"),
        )

    def _runtime(self, value: JsonValue, index: int) -> RuntimeObservation:
        row = self._closed(
            value,
            {"environment_sha256", "observation", "package", "view"},
            f"runtime[{index}]",
        )
        observation = self._record(row["observation"], "observation")
        status = self._text(observation.get("status"), "status")
        loaded = tuple(
            self._loaded(item)
            for item in self._array(observation.get("loaded_files"), "loaded_files")
        )
        if status == "success":
            self._keys(
                observation,
                {"attributes", "loaded_files", "status"},
                "success_observation",
            )
            attributes = tuple(
                RuntimeAttribute(
                    name=self._text(attribute["name"], "name"),
                    value_type=self._text(attribute["value_type"], "value_type"),
                    defining_module=None
                    if attribute["defining_module"] is None
                    else self._text(attribute["defining_module"], "defining_module"),
                )
                for item in self._array(observation["attributes"], "attributes")
                for attribute in [
                    self._closed(
                        item, {"defining_module", "name", "value_type"}, "attribute"
                    )
                ]
            )
            outcome: RuntimeSuccess | RuntimeFailure = RuntimeSuccess(
                attributes=attributes, loaded_files=loaded
            )
        elif status == "failure":
            self._keys(
                observation,
                {"exception_type", "failure_kind", "loaded_files", "message", "status"},
                "failure_observation",
            )
            outcome = RuntimeFailure(
                failure_kind=RuntimeFailureKind(
                    self._text(observation["failure_kind"], "failure_kind")
                ),
                exception_type=self._text(
                    observation["exception_type"], "exception_type"
                ),
                message=self._text(observation["message"], "message"),
                loaded_files=loaded,
            )
        else:
            raise ValueError("runtime status is invalid")
        return RuntimeObservation(
            package=self._text(row["package"], "package"),
            view=RuntimeObservationView(self._text(row["view"], "view")),
            environment_sha256=self._sha(
                row["environment_sha256"], "environment_sha256"
            ),
            observation=outcome,
        )

    def _summary(self, value: JsonValue) -> SupplementSummary:
        keys = {
            "accepted_zero_lineage_count",
            "added_path_count",
            "current_empty_surface_count",
            "current_route_count",
            "deleted_path_count",
            "delta_path_count",
            "modified_path_count",
            "package_surface_count",
            "predecessor_route_count",
            "production_module_count",
            "supplemental_candidate_count",
            "zero_boundary_transition_count",
        }
        row = self._closed(value, keys, "summary")
        return SupplementSummary(
            delta_path_count=self._nonnegative(
                row["delta_path_count"], "delta_path_count"
            ),
            added_path_count=self._nonnegative(
                row["added_path_count"], "added_path_count"
            ),
            modified_path_count=self._nonnegative(
                row["modified_path_count"], "modified_path_count"
            ),
            deleted_path_count=self._nonnegative(
                row["deleted_path_count"], "deleted_path_count"
            ),
            production_module_count=self._nonnegative(
                row["production_module_count"], "production_module_count"
            ),
            package_surface_count=self._nonnegative(
                row["package_surface_count"], "package_surface_count"
            ),
            predecessor_route_count=self._nonnegative(
                row["predecessor_route_count"], "predecessor_route_count"
            ),
            current_route_count=self._nonnegative(
                row["current_route_count"], "current_route_count"
            ),
            supplemental_candidate_count=self._nonnegative(
                row["supplemental_candidate_count"], "supplemental_candidate_count"
            ),
            accepted_zero_lineage_count=self._nonnegative(
                row["accepted_zero_lineage_count"], "accepted_zero_lineage_count"
            ),
            current_empty_surface_count=self._nonnegative(
                row["current_empty_surface_count"], "current_empty_surface_count"
            ),
            zero_boundary_transition_count=self._nonnegative(
                row["zero_boundary_transition_count"], "zero_boundary_transition_count"
            ),
        )

    def _texts(self, value: JsonValue, label: str) -> tuple[str, ...]:
        return tuple(self._text(item, label) for item in self._array(value, label))

    @staticmethod
    def _record(value: JsonValue | None, label: str) -> JsonRecord:
        if type(value) is not dict:
            raise ValueError(f"{label} must be an object")
        return value

    @classmethod
    def _closed(cls, value: JsonValue, keys: set[str], label: str) -> JsonRecord:
        row = cls._record(value, label)
        cls._keys(row, keys, label)
        return row

    @staticmethod
    def _keys(row: JsonRecord, keys: set[str], label: str) -> None:
        if set(row) != keys:
            raise ValueError(f"{label} fields do not match the closed contract")

    @staticmethod
    def _array(value: JsonValue | None, label: str) -> list[JsonValue]:
        if type(value) is not list:
            raise ValueError(f"{label} must be an array")
        return value

    @staticmethod
    def _text(value: JsonValue | None, label: str) -> str:
        if type(value) is not str or not value:
            raise ValueError(f"{label} must be nonempty text")
        return value

    @classmethod
    def _integer(cls, value: JsonValue | None, label: str) -> int:
        if type(value) is not int:
            raise ValueError(f"{label} must be a built-in integer")
        return value

    @classmethod
    def _nonnegative(cls, value: JsonValue | None, label: str) -> int:
        result = cls._integer(value, label)
        if result < 0:
            raise ValueError(f"{label} must be nonnegative")
        return result

    @classmethod
    def _positive(cls, value: JsonValue | None, label: str) -> int:
        result = cls._integer(value, label)
        if result < 1:
            raise ValueError(f"{label} must be positive")
        return result

    @classmethod
    def _sha(cls, value: JsonValue | None, label: str) -> str:
        result = cls._text(value, label)
        if len(result) != 64 or any(
            character not in "0123456789abcdef" for character in result
        ):
            raise ValueError(f"{label} must be SHA-256 hexadecimal")
        return result
