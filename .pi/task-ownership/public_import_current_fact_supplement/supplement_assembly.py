"""Assemble current facts from an explicit content-identified snapshot."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, replace
from pathlib import Path

from public_import_foundation.architecture_conformance_adapter import (
    ArchitectureConformanceAdapter,
)
from public_import_foundation.input_snapshot import (
    FoundationInputEntry,
    FoundationInputManifest,
)
from public_import_foundation.runtime_observation import PythonPackageRuntimeInspector
from public_import_foundation.source_observation import (
    PythonConsumerImportInspector,
    PythonDefiningOriginResolver,
    PythonInitializerInspector,
)
from python_public_import_current_fact_supplement_model import (
    AcquisitionManifest,
    CurrentFactSupplement,
    CurrentRouteObservation,
    ExtractionRole,
    SelectionCategory,
    SupplementalRouteCandidate,
    SupplementSummary,
    ZeroBoundaryTransition,
)
from python_public_import_foundation_model import (
    AuthorityCitation,
    AuthorityState,
    BindingOriginResolution,
    DocumentationCitation,
    ImportObservation,
    InputCategory,
    PackageSurface,
    RuntimeFailure,
    RuntimeLoadedFile,
    RuntimeObservation,
    RuntimeSuccess,
)

from public_import_current_fact_supplement.f0_adapter import AcceptedF0Adapter


@dataclass(frozen=True, slots=True)
class CurrentFactSupplementAssembler:
    """Build the neutral supplement from reidentified snapshot bytes."""

    snapshot_root: Path
    python_executable: Path

    def execute(
        self, manifest: AcquisitionManifest, manifest_sha256: str
    ) -> CurrentFactSupplement:
        """Return one closed current-fact supplement."""
        payloads = self._payloads(manifest)
        foundation_manifest = self._foundation_manifest(manifest)
        f0_path = self._path_for(
            manifest, "harness/reports/public-import-boundaries/phase3/foundation.json"
        )
        f0 = AcceptedF0Adapter().execute(f0_path)
        bindings = PythonDefiningOriginResolver.execute(foundation_manifest, payloads)
        surfaces = self._surfaces(foundation_manifest, payloads, bindings)
        production, graphs = ArchitectureConformanceAdapter().execute(
            foundation_manifest, payloads
        )
        consumers = self._consumers(manifest, payloads)
        documentation = self._documentation(manifest, payloads)
        authority = self._authority(manifest, payloads)
        current_routes = self._routes(
            surfaces, {item.route for item in f0.predecessor_routes}
        )
        supplemental = tuple(
            SupplementalRouteCandidate(
                candidate_key=f"current-route:{item.route}", route=item
            )
            for item in current_routes
            if not item.predecessor_route
        )
        empty = tuple(
            item.package for item in surfaces if not item.effective_star_names
        )
        runtime_inspector = PythonPackageRuntimeInspector(
            self.python_executable, self.snapshot_root / "target"
        )
        environment = runtime_inspector.environment()
        runtime = tuple(
            self._normalized_runtime(
                runtime_inspector.execute(item.package, environment.environment_sha256)
            )
            for item in surfaces
        )
        if self._payloads(manifest) != payloads:
            raise ValueError("selected snapshot inputs changed during observation")
        summary = SupplementSummary(
            delta_path_count=len(manifest.delta_ledger),
            added_path_count=sum(
                item.status.value == "Added" for item in manifest.delta_ledger
            ),
            modified_path_count=sum(
                item.status.value == "Modified" for item in manifest.delta_ledger
            ),
            deleted_path_count=sum(
                item.status.value == "Deleted" for item in manifest.delta_ledger
            ),
            production_module_count=len(production),
            package_surface_count=len(surfaces),
            predecessor_route_count=len(f0.predecessor_routes),
            current_route_count=len(current_routes),
            supplemental_candidate_count=len(supplemental),
            accepted_zero_lineage_count=len(f0.zero_route_surfaces),
            current_empty_surface_count=len(empty),
            zero_boundary_transition_count=1,
        )
        return CurrentFactSupplement(
            schema_version=1,
            subject_identity="ksdft2effmass.python.public-import-current-fact-supplement",
            subject_version="1",
            manifest_sha256=manifest_sha256,
            topology=manifest.topology,
            delta_ledger=manifest.delta_ledger,
            predecessor_routes=f0.predecessor_routes,
            predecessor_package_observations=f0.package_surfaces,
            current_production_modules=production,
            current_package_surfaces=surfaces,
            current_routes=current_routes,
            supplemental_candidates=supplemental,
            accepted_zero_boundary_lineages=f0.zero_route_surfaces,
            current_empty_surfaces=empty,
            zero_boundary_transitions=(
                ZeroBoundaryTransition(
                    package="ksdft2effmass.campaigns",
                    predecessor_state="accepted_empty",
                    current_state="nonempty",
                    current_route_keys=(
                        "ksdft2effmass.campaigns.PlaneWaveParameterStudyCompiler",
                    ),
                ),
            ),
            consumer_imports=consumers,
            documentation_citations=documentation,
            authority_citations=authority,
            dependency_graph_views=graphs,
            runtime_environment=environment,
            runtime_observations=runtime,
            claim_boundaries=(
                "derived neutral syntax, identity, and bounded runtime facts only",
                "importability, bindings, __all__, tests, documentation, and consumer use do not establish support",
                "no support, compatibility, disposition, dependency, licensing, conformance-debt, scientific-validation, release, or human-acceptance conclusion",
                "changed syntax is not adjudicated as conforming or nonconforming by this report",
            ),
            summary=summary,
        )

    def _payloads(self, manifest: AcquisitionManifest) -> dict[str, bytes]:
        result: dict[str, bytes] = {}
        for item in manifest.inputs:
            if item.snapshot_path is None:
                continue
            root = self.snapshot_root.resolve()
            path = (self.snapshot_root / item.snapshot_path.as_posix()).resolve()
            if not path.is_relative_to(root) or not path.is_file() or path.is_symlink():
                raise ValueError(
                    f"snapshot input is not a confined regular file: {item.selection.path}"
                )
            payload = path.read_bytes()
            if (
                hashlib.sha256(payload).hexdigest() != item.tree_entry.sha256
                or len(payload) != item.tree_entry.byte_count
            ):
                raise ValueError(f"snapshot identity mismatch: {item.selection.path}")
            result[item.selection.path.as_posix()] = payload
        return result

    def _foundation_manifest(
        self, manifest: AcquisitionManifest
    ) -> FoundationInputManifest:
        entries: list[FoundationInputEntry] = []
        for item in manifest.inputs:
            if item.snapshot_path is None:
                continue
            category = self._category(item.selection.roles, item.selection.category)
            entries.append(
                FoundationInputEntry(
                    category=category,
                    path=item.selection.path,
                    sha256=item.tree_entry.sha256,
                    byte_count=item.tree_entry.byte_count,
                )
            )
        return FoundationInputManifest(
            schema_version=1,
            subject_identity="ksdft2effmass.python.public-import-foundation-inputs",
            subject_version="1",
            entries=tuple(sorted(entries, key=lambda item: item.sort_key)),
        )

    @staticmethod
    def _category(
        roles: tuple[ExtractionRole, ...], category: SelectionCategory
    ) -> InputCategory:
        if ExtractionRole.PRODUCTION in roles or ExtractionRole.RUNTIME in roles:
            return InputCategory.PRODUCTION_MODULE
        if ExtractionRole.CONSUMER in roles:
            return (
                InputCategory.MAINTAINED_TEST
                if category is SelectionCategory.MAINTAINED_TEST
                else InputCategory.OTHER_FIRST_PARTY_PYTHON
            )
        if ExtractionRole.DOCUMENTATION in roles:
            return InputCategory.PUBLIC_DOCUMENTATION
        if ExtractionRole.AUTHORITY in roles:
            return InputCategory.AUTHORITY
        if ExtractionRole.TASK_TOOL in roles:
            return InputCategory.TASK_TOOL
        if ExtractionRole.F0_LINEAGE in roles:
            return InputCategory.ACCEPTED_INVENTORY
        return InputCategory.PYTHON_RESOURCE

    def _path_for(self, manifest: AcquisitionManifest, selected_path: str) -> Path:
        matches = tuple(
            item
            for item in manifest.inputs
            if item.selection.path.as_posix() == selected_path
        )
        if len(matches) != 1 or matches[0].snapshot_path is None:
            raise ValueError(f"required selected input is unavailable: {selected_path}")
        return self.snapshot_root / matches[0].snapshot_path.as_posix()

    @staticmethod
    def _surfaces(
        manifest: FoundationInputManifest,
        payloads: dict[str, bytes],
        binding_table: tuple[tuple[str, tuple[tuple[str, str, str], ...]], ...],
    ) -> tuple[PackageSurface, ...]:
        records: list[PackageSurface] = []
        for entry in manifest.entries:
            path = entry.path.as_posix()
            if (
                entry.category is not InputCategory.PRODUCTION_MODULE
                or not path.endswith("/__init__.py")
            ):
                continue
            package = PythonDefiningOriginResolver.module_name(path)[0]
            declares, names, raw_bindings = PythonInitializerInspector().execute(
                package, path, payloads[path]
            )
            star = set(names)
            bindings = tuple(
                replace(
                    item,
                    defining_origin=PythonDefiningOriginResolver.resolve(
                        item.origin, binding_table
                    ),
                    origin_resolution=BindingOriginResolution.TRANSITIVE_FIRST_PARTY,
                )
                if item.local_name in star
                else item
                for item in raw_bindings
            )
            records.append(
                PackageSurface(
                    package=package,
                    initializer_path=path,
                    initializer_byte_count=len(payloads[path]),
                    initializer_sha256=hashlib.sha256(payloads[path]).hexdigest(),
                    declares_all=declares,
                    effective_star_names=names,
                    bindings=bindings,
                )
            )
        return tuple(sorted(records, key=lambda item: item.package))

    @staticmethod
    def _routes(
        surfaces: tuple[PackageSurface, ...], predecessors: set[str]
    ) -> tuple[CurrentRouteObservation, ...]:
        rows: list[CurrentRouteObservation] = []
        for surface in surfaces:
            by_name = {item.local_name: item for item in surface.bindings}
            for name in surface.effective_star_names:
                binding = by_name[name]
                if binding.defining_origin is None:
                    raise ValueError(
                        f"current route has no defining origin: {surface.package}.{name}"
                    )
                route = f"{surface.package}.{name}"
                rows.append(
                    CurrentRouteObservation(
                        route=route,
                        package=surface.package,
                        exported_name=name,
                        direct_origin=binding.origin,
                        defining_origin=binding.defining_origin,
                        predecessor_route=route in predecessors,
                    )
                )
        return tuple(sorted(rows, key=lambda item: item.route))

    @staticmethod
    def _consumers(
        manifest: AcquisitionManifest, payloads: dict[str, bytes]
    ) -> tuple[ImportObservation, ...]:
        rows: list[ImportObservation] = []
        inspector = PythonConsumerImportInspector()
        for item in manifest.inputs:
            path = item.selection.path.as_posix()
            if (
                ExtractionRole.CONSUMER in item.selection.roles
                or ExtractionRole.PRODUCTION in item.selection.roles
                or ExtractionRole.TASK_TOOL in item.selection.roles
            ):
                rows.extend(inspector.execute(path, payloads[path]))
        return tuple(
            sorted(
                rows,
                key=lambda item: (
                    item.consumer_path,
                    item.line,
                    item.column,
                    item.import_kind.value,
                    item.imported_module,
                    item.imported_name or "",
                ),
            )
        )

    @staticmethod
    def _documentation(
        manifest: AcquisitionManifest, payloads: dict[str, bytes]
    ) -> tuple[DocumentationCitation, ...]:
        pattern = re.compile(
            r"(?<![A-Za-z0-9_])ksdft2effmass(?:\.[A-Za-z_][A-Za-z0-9_]*)+"
        )
        rows: list[DocumentationCitation] = []
        for item in manifest.inputs:
            if ExtractionRole.DOCUMENTATION not in item.selection.roles:
                continue
            path = item.selection.path.as_posix()
            text = payloads[path].decode("utf-8")
            for line_number, line in enumerate(text.splitlines(), start=1):
                rows.extend(
                    DocumentationCitation(
                        path=path,
                        line=line_number,
                        column=match.start(),
                        route_text=match.group(0),
                    )
                    for match in pattern.finditer(line)
                )
        return tuple(
            sorted(
                rows,
                key=lambda item: (item.path, item.line, item.column, item.route_text),
            )
        )

    @staticmethod
    def _authority(
        manifest: AcquisitionManifest, payloads: dict[str, bytes]
    ) -> tuple[AuthorityCitation, ...]:
        pattern = re.compile(
            r"(?i)\b(?:ambiguous|compatibility|public|route|support(?:ed)?|unknown|__all__)\b"
        )
        rows: list[AuthorityCitation] = []
        for item in manifest.inputs:
            if ExtractionRole.AUTHORITY not in item.selection.roles:
                continue
            path = item.selection.path.as_posix()
            text = payloads[path].decode("utf-8")
            for line_number, line in enumerate(text.splitlines(), start=1):
                rows.extend(
                    AuthorityCitation(
                        path=path,
                        line=line_number,
                        column=match.start(),
                        matched_term=match.group(0),
                        authority_state=AuthorityState.RAW_UNADJUDICATED,
                    )
                    for match in pattern.finditer(line)
                )
        return tuple(
            sorted(
                rows,
                key=lambda item: (item.path, item.line, item.column, item.matched_term),
            )
        )

    def _normalized_runtime(self, item: RuntimeObservation) -> RuntimeObservation:
        source_root = (self.snapshot_root / "target/python/src").resolve()
        loaded = tuple(
            RuntimeLoadedFile(
                module_name=value.module_name,
                path=(
                    f"target-source:{Path(value.path).resolve().relative_to(source_root).as_posix()}"
                    if Path(value.path).resolve().is_relative_to(source_root)
                    else f"environment-file:{value.sha256}"
                ),
                byte_count=value.byte_count,
                sha256=value.sha256,
            )
            for value in item.observation.loaded_files
        )
        if type(item.observation) is RuntimeSuccess:
            outcome: RuntimeSuccess | RuntimeFailure = RuntimeSuccess(
                attributes=item.observation.attributes,
                loaded_files=loaded,
            )
        elif type(item.observation) is RuntimeFailure:
            outcome = RuntimeFailure(
                failure_kind=item.observation.failure_kind,
                exception_type=item.observation.exception_type,
                message=item.observation.message,
                loaded_files=loaded,
            )
        else:
            raise TypeError("runtime outcome is not closed")
        return RuntimeObservation(
            package=item.package,
            view=item.view,
            environment_sha256=item.environment_sha256,
            observation=outcome,
        )
