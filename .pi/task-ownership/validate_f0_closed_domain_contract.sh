#!/usr/bin/env bash
set -euo pipefail
export MYPYPATH=python/src:.pi/task-ownership
export PYTHONPATH=.pi/task-ownership:python/src
python/.venv/bin/python -m ruff check .pi/task-ownership/python_public_import_foundation_model.py
python/.venv/bin/python -m ruff format --check .pi/task-ownership/python_public_import_foundation_model.py
python/.venv/bin/python -m mypy .pi/task-ownership/python_public_import_foundation_model.py
probe_source=$(cat <<'PY'
from __future__ import annotations

import copy
from dataclasses import replace
from pathlib import Path

from python_public_import_foundation_model import (
    ClosedFoundationParser,
    FoundationJsonCodec,
    JsonRecord,
    JsonValue,
    ClosedFoundationSerializer,
    FoundationModelError,
    InputCategory,
    InputIdentity,
    ProductionAllResolution,
    ProductionFactOutput,
    PublicImportFoundation,
)


class ClosedDomainContractProbe:
    """Exercise direct construction and adversarial version-one model states."""

    __slots__ = ()

    def execute(self) -> None:
        codec = FoundationJsonCodec()
        payload = Path(
            "harness/reports/public-import-boundaries/phase3/foundation.json"
        ).read_bytes()
        base = codec.decode(payload)
        report = ClosedFoundationParser().execute(base)
        if codec.encode(ClosedFoundationSerializer().execute(report)) != payload:
            raise SystemExit(
                "closed model does not preserve canonical version-one bytes"
            )
        self._direct_construction_rejections(report)
        cases: list[tuple[JsonValue, str]] = []

        value = self._root(base)
        self._record(self._rows(value, "dependency_graph_views")[0])["view"] = (
            "unsupported_view"
        )
        cases.append((value, "unsupported graph view"))

        value = self._root(base)
        self._record(self._rows(value, "package_runtime_observations")[0])["view"] = (
            "unsupported_view"
        )
        cases.append((value, "unsupported runtime view"))

        value = self._root(base)
        failure = self._runtime_observation(value, "failure")
        self._record(failure["observation"])["failure_kind"] = "unsupported"
        cases.append((value, "unsupported runtime failure kind"))

        value = self._root(base)
        distributions = self._rows(
            self._record(value["runtime_environment"]), "distributions"
        )
        self._array(distributions[0]).append("extra")
        cases.append((value, "malformed distribution arity"))

        value = self._root(base)
        package = self._package_with_star(value)
        stars = self._rows(package, "effective_star_names")
        stars.append(stars[0])
        cases.append((value, "duplicate effective star name"))

        value = self._root(base)
        success = self._runtime_observation(value, "success")
        attributes = self._rows(self._record(success["observation"]), "attributes")
        attributes.append(copy.deepcopy(attributes[0]))
        cases.append((value, "duplicate runtime attribute"))

        value = self._root(base)
        package = self._package_with_nonstar_binding(value)
        binding = self._binding(package, False)
        binding["defining_origin"] = self._text(binding["origin"])
        binding["origin_resolution"] = "transitive_first_party_binding"
        cases.append((value, "origin fields on non-star binding"))

        value = self._root(base)
        package = self._package_with_star(value)
        binding = self._binding(package, True)
        del binding["defining_origin"]
        del binding["origin_resolution"]
        cases.append((value, "missing origin fields on star binding"))

        value = self._root(base)
        accepted = self._record(value["accepted_inventory"])
        accepted["byte_count"] = self._integer(accepted["byte_count"]) + 1
        cases.append((value, "accepted inventory byte count"))

        value = self._root(base)
        accepted = self._record(value["accepted_inventory"])
        accepted["byte_count"] = self._integer(accepted["byte_count"]) + 1
        accepted_path = self._text(accepted["path"])
        selected = next(
            self._record(item)
            for item in self._rows(
                self._record(value["input_manifest"]), "entries"
            )
            if self._text(self._record(item)["path"]) == accepted_path
        )
        selected["byte_count"] = self._integer(selected["byte_count"]) + 1
        cases.append((value, "coordinated accepted inventory byte count"))

        value = self._root(base)
        claims = self._rows(value, "claim_boundaries")
        claims[0] = "arbitrary claim"
        cases.append((value, "arbitrary claim"))

        value = self._root(base)
        production = self._rows(value, "production_fact_outputs")
        production.append(copy.deepcopy(production[0]))
        summary = self._record(value["summary"])
        summary["production_fact_output_count"] = self._integer(
            summary["production_fact_output_count"]
        ) + 1
        cases.append((value, "duplicate 217th production row"))

        value = self._root(base)
        production = self._rows(value, "production_fact_outputs")
        production[1] = copy.deepcopy(production[0])
        cases.append((value, "count-preserving production non-bijection"))

        value = self._root(base)
        production = self._rows(value, "production_fact_outputs")
        production[0], production[1] = production[1], production[0]
        cases.append((value, "noncanonical production ordering"))

        value = self._root(base)
        view = self._record(self._rows(value, "dependency_graph_views")[0])
        components = self._rows(view, "strongly_connected_components")
        merged: list[JsonValue] = []
        merged.extend(
            self._text(item)
            for item in self._array(components[0]) + self._array(components[1])
        )
        merged.sort(key=self._text)
        components[0:2] = [merged]
        components.sort(key=self._component_key)
        cases.append((value, "merged non-SCC components"))

        value = self._root(base)
        view = self._record(self._rows(value, "dependency_graph_views")[0])
        components = self._rows(view, "strongly_connected_components")
        component_index = next(
            index
            for index, component in enumerate(components)
            if len(self._array(component)) > 1
        )
        component = self._array(components[component_index])
        components[component_index : component_index + 1] = [
            [component[0]],
            component[1:],
        ]
        components.sort(key=self._component_key)
        cases.append((value, "split SCC"))

        value = self._root(base)
        success = self._runtime_observation(value, "success")
        loaded = self._rows(self._record(success["observation"]), "loaded_files")
        loaded.append(copy.deepcopy(loaded[0]))
        cases.append((value, "duplicate loaded-file key"))

        value = self._root(base)
        package = self._package_with_star(value)
        binding = self._binding(package, True)
        self._rows(package, "bindings").remove(binding)
        cases.append((value, "effective star name without binding"))

        value = self._root(base)
        packages = self._rows(value, "package_surfaces")
        packages.insert(1, copy.deepcopy(packages[0]))
        summary = self._record(value["summary"])
        summary["package_surface_count"] = self._integer(
            summary["package_surface_count"]
        ) + 1
        cases.append((value, "duplicate package surface"))

        value = self._root(base)
        lineage = self._record(self._rows(value, "phase2_lineage_inputs")[0])
        lineage["sha256"] = "0" * 64
        cases.append((value, "lineage identity mismatch"))

        value = self._root(base)
        route = self._record(self._rows(value, "predecessor_routes")[0])
        route["route"] = "!arbitrary"
        cases.append((value, "route/package/name mismatch"))

        value = self._root(base)
        imported = next(
            self._record(item)
            for item in self._rows(value, "consumer_imports")
            if self._text(self._record(item)["import_kind"]) == "import"
        )
        imported["imported_name"] = "arbitrary"
        cases.append((value, "import kind/name mismatch"))

        value = self._root(base)
        package = self._package_with_star(value)
        binding = self._binding(package, True)
        binding["defining_origin"] = "arbitrary.origin"
        cases.append((value, "arbitrary terminal defining origin"))

        value = self._root(base)
        entries = self._rows(self._record(value["input_manifest"]), "entries")
        selected = next(
            self._record(item)
            for item in entries
            if self._text(self._record(item)["path"])
            == "tasks/software/python.architecture-refactor.architecture-conformance.production-facts.json"
        )
        selected["category"] = "authority"
        entries.sort(key=self._input_key)
        cases.append((value, "lineage selected-input category mismatch"))

        value = self._root(base)
        value["schema_version"] = 2
        cases.append((value, "unsupported foundation identity"))

        value = self._root(base)
        environment = self._record(value["runtime_environment"])
        environment["environment_sha256"] = "0" * 64
        cases.append((value, "runtime environment identity mismatch"))

        for candidate, label in cases:
            try:
                ClosedFoundationParser().execute(candidate)
            except (FoundationModelError, TypeError, ValueError):
                continue
            raise SystemExit(f"closed model accepted malformed case: {label}")
        print(
            "closed-domain probes passed: "
            f"{len(cases)} malformed cases and direct construction rejected"
        )

    @staticmethod
    def _direct_construction_rejections(report: PublicImportFoundation) -> None:
        try:
            InputIdentity(InputCategory.AUTHORITY, "", -1, "x")
        except (TypeError, ValueError):
            pass
        else:
            raise SystemExit("InputIdentity accepted invalid direct construction")
        try:
            ProductionFactOutput(
                "",
                "",
                "x",
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                ProductionAllResolution.LITERAL,
                ("", ""),
            )
        except (TypeError, ValueError):
            pass
        else:
            raise SystemExit(
                "ProductionFactOutput accepted invalid direct construction"
            )
        try:
            replace(report.predecessor_routes[0], route="!arbitrary")
        except (TypeError, ValueError):
            pass
        else:
            raise SystemExit("PredecessorRoute accepted inconsistent route")
        try:
            replace(
                next(
                    item
                    for item in report.consumer_imports
                    if item.import_kind.value == "import"
                ),
                imported_name="arbitrary",
            )
        except (TypeError, ValueError):
            pass
        else:
            raise SystemExit("ImportObservation accepted inconsistent name")
        surface = next(
            item for item in report.package_surfaces if item.effective_star_names
        )
        try:
            replace(
                surface,
                bindings=tuple(
                    binding
                    for binding in surface.bindings
                    if binding.local_name != surface.effective_star_names[0]
                ),
            )
        except (TypeError, ValueError):
            pass
        else:
            raise SystemExit("PackageSurface accepted a missing star binding")
        try:
            replace(report, schema_version=2)
        except (TypeError, ValueError):
            pass
        else:
            raise SystemExit("PublicImportFoundation accepted another identity")
        try:
            replace(report.runtime_environment, environment_sha256="0" * 64)
        except (TypeError, ValueError):
            pass
        else:
            raise SystemExit("RuntimeEnvironment accepted a mismatched identity")

    @classmethod
    def _root(cls, value: JsonValue) -> JsonRecord:
        return cls._record(copy.deepcopy(value))

    @staticmethod
    def _record(value: JsonValue) -> JsonRecord:
        if type(value) is not dict:
            raise SystemExit("probe expected a JSON object")
        return value

    @staticmethod
    def _array(value: JsonValue) -> list[JsonValue]:
        if type(value) is not list:
            raise SystemExit("probe expected a JSON array")
        return value

    @classmethod
    def _rows(cls, record: JsonRecord, key: str) -> list[JsonValue]:
        return cls._array(record[key])

    @staticmethod
    def _text(value: JsonValue) -> str:
        if type(value) is not str:
            raise SystemExit("probe expected text")
        return value

    @staticmethod
    def _integer(value: JsonValue) -> int:
        if type(value) is not int:
            raise SystemExit("probe expected int")
        return value

    @classmethod
    def _runtime_observation(cls, root: JsonRecord, status: str) -> JsonRecord:
        return next(
            row
            for item in cls._rows(root, "package_runtime_observations")
            for row in [cls._record(item)]
            if cls._text(cls._record(row["observation"])["status"]) == status
        )

    @classmethod
    def _package_with_star(cls, root: JsonRecord) -> JsonRecord:
        return next(
            row
            for item in cls._rows(root, "package_surfaces")
            for row in [cls._record(item)]
            if cls._rows(row, "effective_star_names")
        )

    @classmethod
    def _package_with_nonstar_binding(cls, root: JsonRecord) -> JsonRecord:
        return next(
            row
            for item in cls._rows(root, "package_surfaces")
            for row in [cls._record(item)]
            if any(
                cls._text(cls._record(binding)["local_name"])
                not in {
                    cls._text(name)
                    for name in cls._rows(row, "effective_star_names")
                }
                for binding in cls._rows(row, "bindings")
            )
        )

    @classmethod
    def _binding(cls, package: JsonRecord, star: bool) -> JsonRecord:
        star_names = {
            cls._text(name)
            for name in cls._rows(package, "effective_star_names")
        }
        return next(
            row
            for item in cls._rows(package, "bindings")
            for row in [cls._record(item)]
            if (cls._text(row["local_name"]) in star_names) is star
        )

    @classmethod
    def _component_key(cls, value: JsonValue) -> tuple[str, ...]:
        return tuple(cls._text(item) for item in cls._array(value))

    @classmethod
    def _input_key(cls, value: JsonValue) -> tuple[str, str]:
        record = cls._record(value)
        return cls._text(record["category"]), cls._text(record["path"])


ClosedDomainContractProbe().execute()
PY
)
python/.venv/bin/python -m mypy --strict -c "$probe_source"
python/.venv/bin/python -c "$probe_source"
