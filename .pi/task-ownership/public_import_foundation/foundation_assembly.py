"""Assemble the closed public-import foundation from explicit observations."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, replace
from pathlib import Path, PurePosixPath
from typing import TypeAlias

from python_public_import_foundation_model import (
    AcceptedInventoryIdentity,
    AuthorityCitation,
    AuthorityState,
    BindingOriginResolution,
    ClaimBoundary,
    DeepImportCandidate,
    DocumentationCitation,
    FoundationJsonCodec,
    FoundationSummary,
    ImportObservation,
    InputCategory,
    InputIdentity,
    JsonRecord,
    JsonValue,
    PackageBindingCandidate,
    PackageSurface,
    Phase2LineageInput,
    Phase2LineageRole,
    PredecessorRoute,
    PublicImportFoundation,
    SupplementalCandidate,
    SupplementalKind,
)

from public_import_foundation.architecture_conformance_adapter import (
    ArchitectureConformanceAdapter,
)
from public_import_foundation.input_snapshot import (
    FoundationFormatError,
    FoundationInputManifest,
    FoundationInputManifestSerializer,
    FoundationPathPolicy,
)
from public_import_foundation.runtime_observation import PythonPackageRuntimeInspector
from public_import_foundation.source_observation import (
    DefiningBindingTable,
    PythonConsumerImportInspector,
    PythonDefiningOriginResolver,
    PythonInitializerInspector,
)

AcceptedPackageInput: TypeAlias = tuple[str, str, tuple[str, ...]]


@dataclass(frozen=True, slots=True)
class PublicImportFactFoundationBuilder:
    """Build the deterministic neutral report from exact manifest inputs."""

    repository_root: Path
    python_executable: Path

    def execute(
        self,
        manifest: FoundationInputManifest,
        accepted_inventory_path: PurePosixPath,
    ) -> PublicImportFoundation:
        """Validate all identities and return one closed immutable foundation."""
        payloads = self._validated_payloads(manifest)
        inventory_payload = payloads.get(accepted_inventory_path.as_posix())
        if inventory_payload is None:
            raise FoundationFormatError(
                "accepted inventory is absent from input manifest"
            )
        inventory_sha256 = hashlib.sha256(inventory_payload).hexdigest()
        if (
            inventory_sha256
            != "fb180c5d8aa9ecd33a319d03a5795ab24343d9b2b553acac580ec452b5795c7e"
        ):
            raise FoundationFormatError("accepted Phase 1 inventory identity mismatch")
        inventory = FoundationInputManifestSerializer.record(
            FoundationJsonCodec().decode(inventory_payload), "accepted inventory"
        )
        routes = FoundationInputManifestSerializer.array(
            self._required(inventory, "export_routes", "accepted inventory"),
            "accepted inventory export_routes",
        )
        packages = FoundationInputManifestSerializer.array(
            self._required(inventory, "package_exports", "accepted inventory"),
            "accepted inventory package_exports",
        )
        if len(routes) != 985:
            raise FoundationFormatError("accepted predecessor route count is not 985")
        if len(packages) != 35:
            raise FoundationFormatError("accepted package-surface count is not 35")
        predecessor_routes = self._predecessor_routes(routes)
        accepted_packages = self._accepted_packages(packages)
        initializer_identities = self._accepted_initializer_identities(inventory)
        defining_bindings = PythonDefiningOriginResolver.execute(manifest, payloads)
        package_surfaces = self._package_records(
            accepted_packages,
            payloads,
            predecessor_routes,
            initializer_identities,
            defining_bindings,
        )
        package_names = tuple(item.package for item in package_surfaces)
        consumers = self._consumer_records(manifest, payloads)
        documentation = self._documentation_records(manifest, payloads)
        authority = self._authority_records(manifest, payloads)
        phase2_lineage = self._phase2_input_records(payloads)
        production, graph_views = ArchitectureConformanceAdapter().execute(
            manifest, payloads
        )
        runtime = PythonPackageRuntimeInspector(
            python_executable=self.python_executable,
            repository_root=self.repository_root,
        )
        runtime_environment = runtime.environment()
        runtime_records = tuple(
            runtime.execute(package, runtime_environment.environment_sha256)
            for package in package_names
        )
        if self._validated_payloads(manifest) != payloads:
            raise FoundationFormatError(
                "selected inputs changed during runtime observation"
            )
        package_set = set(package_names)
        deep_imports = tuple(
            item for item in consumers if item.imported_module not in package_set
        )
        supplemental = self._supplemental_records(package_surfaces, consumers)
        zero_surfaces = tuple(
            item.package for item in package_surfaces if not item.effective_star_names
        )
        if len(zero_surfaces) != 10:
            raise FoundationFormatError("current zero-route surface count is not 10")
        inputs = tuple(
            InputIdentity(
                category=entry.category,
                path=entry.path.as_posix(),
                byte_count=entry.byte_count,
                sha256=entry.sha256,
            )
            for entry in manifest.entries
        )
        summary = FoundationSummary(
            input_count=len(inputs),
            predecessor_route_count=len(predecessor_routes),
            package_surface_count=len(package_surfaces),
            zero_route_surface_count=len(zero_surfaces),
            consumer_import_count=len(consumers),
            deep_non_initializer_module_import_count=len(deep_imports),
            documentation_citation_count=len(documentation),
            authority_citation_count=len(authority),
            phase2_lineage_input_count=len(phase2_lineage),
            production_fact_output_count=len(production),
            dependency_graph_view_count=len(graph_views),
            supplemental_candidate_count=len(supplemental),
            runtime_package_observation_count=len(runtime_records),
        )
        return PublicImportFoundation(
            schema_version=1,
            subject_identity="ksdft2effmass.python.public-import-foundation",
            subject_version="1",
            input_manifest_schema_version=manifest.schema_version,
            inputs=inputs,
            accepted_inventory=AcceptedInventoryIdentity(
                path=accepted_inventory_path.as_posix(),
                byte_count=len(inventory_payload),
                sha256=inventory_sha256,
                accepted_closeout_commit=("f5ce3e981880fdfa336aa781664595b61a829557"),
            ),
            predecessor_routes=predecessor_routes,
            package_surfaces=package_surfaces,
            zero_route_surfaces=zero_surfaces,
            consumer_imports=consumers,
            deep_imports=deep_imports,
            documentation_citations=documentation,
            authority_citations=authority,
            phase2_lineage_inputs=phase2_lineage,
            production_fact_outputs=production,
            dependency_graph_views=graph_views,
            runtime_environment=runtime_environment,
            runtime_observations=runtime_records,
            supplemental_candidates=supplemental,
            claim_boundaries=tuple(ClaimBoundary),
            summary=summary,
        )

    def _validated_payloads(
        self, manifest: FoundationInputManifest
    ) -> dict[str, bytes]:
        payloads: dict[str, bytes] = {}
        for entry in manifest.entries:
            selected = FoundationPathPolicy.resolve(self.repository_root, entry.path)
            if not selected.is_file() or selected.is_symlink():
                raise FoundationFormatError(
                    f"input is not a nonsymlink regular file: {entry.path}"
                )
            payload = selected.read_bytes()
            if (
                len(payload) != entry.byte_count
                or hashlib.sha256(payload).hexdigest() != entry.sha256
            ):
                raise FoundationFormatError(f"input identity mismatch: {entry.path}")
            payloads[entry.path.as_posix()] = payload
        return payloads

    @staticmethod
    def _predecessor_routes(
        routes: list[JsonValue],
    ) -> tuple[PredecessorRoute, ...]:
        records: list[PredecessorRoute] = []
        seen: set[str] = set()
        for index, value in enumerate(routes):
            label = f"export_routes[{index}]"
            source = FoundationInputManifestSerializer.record(value, label)
            record = PredecessorRoute(
                route=FoundationInputManifestSerializer.text(
                    PublicImportFactFoundationBuilder._required(source, "route", label),
                    f"{label}.route",
                ),
                package=FoundationInputManifestSerializer.text(
                    PublicImportFactFoundationBuilder._required(
                        source, "package", label
                    ),
                    f"{label}.package",
                ),
                exported_name=FoundationInputManifestSerializer.text(
                    PublicImportFactFoundationBuilder._required(
                        source, "exported_name", label
                    ),
                    f"{label}.exported_name",
                ),
                defining_module=FoundationInputManifestSerializer.text(
                    PublicImportFactFoundationBuilder._required(
                        source, "defining_module", label
                    ),
                    f"{label}.defining_module",
                ),
                defining_symbol=FoundationInputManifestSerializer.text(
                    PublicImportFactFoundationBuilder._required(
                        source, "defining_symbol", label
                    ),
                    f"{label}.defining_symbol",
                ),
                support_status=FoundationInputManifestSerializer.text(
                    PublicImportFactFoundationBuilder._required(
                        source, "support_status", label
                    ),
                    f"{label}.support_status",
                ),
                compatibility_disposition=FoundationInputManifestSerializer.text(
                    PublicImportFactFoundationBuilder._required(
                        source, "compatibility_disposition", label
                    ),
                    f"{label}.compatibility_disposition",
                ),
            )
            if record.route in seen:
                raise FoundationFormatError(
                    f"duplicate predecessor route: {record.route}"
                )
            seen.add(record.route)
            records.append(record)
        return tuple(sorted(records, key=lambda item: item.route))

    @staticmethod
    def _accepted_packages(
        packages: list[JsonValue],
    ) -> tuple[AcceptedPackageInput, ...]:
        records: list[AcceptedPackageInput] = []
        for index, value in enumerate(packages):
            label = f"package_exports[{index}]"
            source = FoundationInputManifestSerializer.record(value, label)
            package = FoundationInputManifestSerializer.text(
                PublicImportFactFoundationBuilder._required(source, "package", label),
                f"{label}.package",
            )
            path = FoundationInputManifestSerializer.text(
                PublicImportFactFoundationBuilder._required(source, "path", label),
                f"{label}.path",
            )
            names = tuple(
                FoundationInputManifestSerializer.text(item, "accepted star name")
                for item in FoundationInputManifestSerializer.array(
                    PublicImportFactFoundationBuilder._required(
                        source, "effective_star_exports", label
                    ),
                    f"{label}.effective_star_exports",
                )
            )
            records.append((package, path, names))
        return tuple(sorted(records, key=lambda item: item[0]))

    @staticmethod
    def _accepted_initializer_identities(
        inventory: JsonRecord,
    ) -> dict[str, str]:
        identities = FoundationInputManifestSerializer.record(
            PublicImportFactFoundationBuilder._required(
                inventory, "source_identities", "accepted inventory"
            ),
            "source_identities",
        )
        files = FoundationInputManifestSerializer.array(
            PublicImportFactFoundationBuilder._required(
                identities, "files", "source_identities"
            ),
            "source_identities.files",
        )
        result: dict[str, str] = {}
        for index, value in enumerate(files):
            record = FoundationInputManifestSerializer.record(
                value, f"source_identities.files[{index}]"
            )
            path = FoundationInputManifestSerializer.text(
                PublicImportFactFoundationBuilder._required(
                    record, "path", "source identity"
                ),
                "source identity.path",
            )
            result[path] = FoundationInputManifestSerializer.text(
                PublicImportFactFoundationBuilder._required(
                    record, "sha256", "source identity"
                ),
                "source identity.sha256",
            )
        return result

    @staticmethod
    def _package_records(
        packages: tuple[AcceptedPackageInput, ...],
        payloads: dict[str, bytes],
        routes: tuple[PredecessorRoute, ...],
        initializer_identities: dict[str, str],
        defining_bindings: DefiningBindingTable,
    ) -> tuple[PackageSurface, ...]:
        records: list[PackageSurface] = []
        route_by_pair = {
            (route.package, route.exported_name): route for route in routes
        }
        for package, path, accepted_names in packages:
            payload = payloads.get(path)
            if payload is None:
                raise FoundationFormatError(f"initializer absent from manifest: {path}")
            current_sha256 = hashlib.sha256(payload).hexdigest()
            if initializer_identities.get(path) != current_sha256:
                raise FoundationFormatError(
                    f"initializer differs from accepted Phase 1 identity: {path}"
                )
            declares_all, current_names, inspected_bindings = (
                PythonInitializerInspector().execute(package, path, payload)
            )
            if current_names != accepted_names:
                raise FoundationFormatError(
                    f"current and predecessor star names differ: {package}"
                )
            bindings_by_name = {
                binding.local_name: binding for binding in inspected_bindings
            }
            resolved = []
            star_names = set(accepted_names)
            for binding in inspected_bindings:
                if binding.local_name not in star_names:
                    resolved.append(binding)
                    continue
                route = route_by_pair.get((package, binding.local_name))
                if route is None:
                    raise FoundationFormatError(
                        f"unresolved effective star origin: {package}.{binding.local_name}"
                    )
                predecessor_origin = f"{route.defining_module}.{route.defining_symbol}"
                if binding.origin != predecessor_origin:
                    raise FoundationFormatError(
                        "current and predecessor direct origins differ: "
                        f"{package}.{binding.local_name}"
                    )
                resolved.append(
                    replace(
                        binding,
                        defining_origin=PythonDefiningOriginResolver.resolve(
                            binding.origin, defining_bindings
                        ),
                        origin_resolution=(
                            BindingOriginResolution.TRANSITIVE_FIRST_PARTY
                        ),
                    )
                )
            if any(name not in bindings_by_name for name in accepted_names):
                raise FoundationFormatError(
                    f"unresolved effective star origin in {package}"
                )
            records.append(
                PackageSurface(
                    package=package,
                    initializer_path=path,
                    initializer_byte_count=len(payload),
                    initializer_sha256=current_sha256,
                    declares_all=declares_all,
                    effective_star_names=accepted_names,
                    bindings=tuple(resolved),
                )
            )
        return tuple(sorted(records, key=lambda item: item.package))

    @staticmethod
    def _consumer_records(
        manifest: FoundationInputManifest, payloads: dict[str, bytes]
    ) -> tuple[ImportObservation, ...]:
        parse_categories = {
            InputCategory.EXAMPLE,
            InputCategory.HARNESS_CHECK,
            InputCategory.MAINTAINED_TEST,
            InputCategory.OTHER_FIRST_PARTY_PYTHON,
            InputCategory.PRODUCTION_MODULE,
            InputCategory.TASK_TOOL,
        }
        records: list[ImportObservation] = []
        inspector = PythonConsumerImportInspector()
        for entry in manifest.entries:
            if entry.category in parse_categories:
                records.extend(
                    inspector.execute(
                        entry.path.as_posix(), payloads[entry.path.as_posix()]
                    )
                )
        return tuple(
            sorted(
                records,
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
    def _authority_records(
        manifest: FoundationInputManifest, payloads: dict[str, bytes]
    ) -> tuple[AuthorityCitation, ...]:
        pattern = re.compile(
            r"(?i)\b(?:ambiguous|compatibility|public|route|support(?:ed)?|unknown|__all__)\b"
        )
        records: list[AuthorityCitation] = []
        categories = {InputCategory.AUTHORITY, InputCategory.PHASE2_VIEW}
        for entry in manifest.entries:
            if entry.category not in categories:
                continue
            try:
                text = payloads[entry.path.as_posix()].decode("utf-8")
            except UnicodeDecodeError as exc:
                raise FoundationFormatError(
                    f"authority input is not UTF-8: {entry.path}"
                ) from exc
            for line_number, line in enumerate(text.splitlines(), start=1):
                records.extend(
                    AuthorityCitation(
                        path=entry.path.as_posix(),
                        line=line_number,
                        column=match.start(),
                        matched_term=match.group(0),
                        authority_state=AuthorityState.RAW_UNADJUDICATED,
                    )
                    for match in pattern.finditer(line)
                )
        return tuple(
            sorted(
                records,
                key=lambda item: (
                    item.path,
                    item.line,
                    item.column,
                    item.matched_term,
                ),
            )
        )

    @staticmethod
    def _phase2_input_records(
        payloads: dict[str, bytes],
    ) -> tuple[Phase2LineageInput, ...]:
        paths = (
            (
                Phase2LineageRole.PRODUCTION_FACTS_TASK,
                "tasks/software/python.architecture-refactor.architecture-conformance.production-facts.json",
            ),
            (
                Phase2LineageRole.PRODUCTION_FACTS_OWNERSHIP,
                ".pi/task-ownership/python.architecture-refactor.architecture-conformance.production-facts.json",
            ),
            (
                Phase2LineageRole.PRODUCTION_FACTS_IMPLEMENTATION,
                "python/src/ksdft2effmass/harness/pi/conformance/python/production.py",
            ),
            (
                Phase2LineageRole.DEPENDENCY_GRAPH_TASK,
                "tasks/software/python.architecture-refactor.architecture-conformance.dependency-graph-views.json",
            ),
            (
                Phase2LineageRole.DEPENDENCY_GRAPH_OWNERSHIP,
                ".pi/task-ownership/python.architecture-refactor.architecture-conformance.dependency-graph-views.json",
            ),
            (
                Phase2LineageRole.DEPENDENCY_GRAPH_IMPLEMENTATION,
                "python/src/ksdft2effmass/harness/pi/conformance/python/dependency_graph.py",
            ),
        )
        records: list[Phase2LineageInput] = []
        for role, path in paths:
            payload = payloads.get(path)
            if payload is None:
                raise FoundationFormatError(
                    f"required accepted Phase 2 input is absent: {path}"
                )
            records.append(
                Phase2LineageInput(
                    role=role,
                    path=path,
                    byte_count=len(payload),
                    sha256=hashlib.sha256(payload).hexdigest(),
                )
            )
        return tuple(records)

    @staticmethod
    def _documentation_records(
        manifest: FoundationInputManifest, payloads: dict[str, bytes]
    ) -> tuple[DocumentationCitation, ...]:
        pattern = re.compile(
            r"(?<![A-Za-z0-9_])ksdft2effmass(?:\.[A-Za-z_][A-Za-z0-9_]*)+"
        )
        records: list[DocumentationCitation] = []
        for entry in manifest.entries:
            if entry.category is not InputCategory.PUBLIC_DOCUMENTATION:
                continue
            try:
                text = payloads[entry.path.as_posix()].decode("utf-8")
            except UnicodeDecodeError as exc:
                raise FoundationFormatError(
                    f"documentation is not UTF-8: {entry.path}"
                ) from exc
            for line_number, line in enumerate(text.splitlines(), start=1):
                records.extend(
                    DocumentationCitation(
                        path=entry.path.as_posix(),
                        line=line_number,
                        column=match.start(),
                        route_text=match.group(0),
                    )
                    for match in pattern.finditer(line)
                )
        return tuple(
            sorted(
                records,
                key=lambda item: (
                    item.path,
                    item.line,
                    item.column,
                    item.route_text,
                ),
            )
        )

    @staticmethod
    def _supplemental_records(
        packages: tuple[PackageSurface, ...],
        consumers: tuple[ImportObservation, ...],
    ) -> tuple[SupplementalCandidate, ...]:
        records: list[SupplementalCandidate] = []
        keys: set[str] = set()
        for package in packages:
            star_names = set(package.effective_star_names)
            for binding in package.bindings:
                if binding.local_name in star_names or binding.local_name == "__all__":
                    continue
                key = f"package-binding:{package.package}:{binding.local_name}"
                keys.add(key)
                records.append(
                    PackageBindingCandidate(
                        candidate_key=key,
                        candidate_kind=SupplementalKind.PACKAGE_BINDING,
                        support_status="unknown",
                        package=package.package,
                        binding=binding,
                    )
                )
        package_names = {package.package for package in packages}
        for consumer in consumers:
            if consumer.imported_module in package_names:
                continue
            key = f"deep-route:{consumer.imported_module}:{consumer.imported_name}"
            if key in keys:
                continue
            keys.add(key)
            records.append(
                DeepImportCandidate(
                    candidate_key=key,
                    candidate_kind=SupplementalKind.DEEP_IMPORT,
                    support_status="unknown",
                    consumer_path=consumer.consumer_path,
                    imported_module=consumer.imported_module,
                    imported_name=consumer.imported_name,
                )
            )
        return tuple(sorted(records, key=lambda item: item.candidate_key))

    @staticmethod
    def _required(record: JsonRecord, key: str, label: str) -> JsonValue:
        if key not in record:
            raise FoundationFormatError(f"{label} is missing {key}")
        return record[key]
