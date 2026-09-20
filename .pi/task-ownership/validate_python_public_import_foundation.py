#!/usr/bin/env python3
"""Validate the explicit-input Phase 3 current-fact foundation.

The validator reproduces the authored input manifest and foundation from exact inputs,
checks tracked first-party Python selection coverage, exercises one identity-mismatch
failure, and verifies bounded task/Harness state. Passing establishes deterministic
software structure evidence only, not route support or compatibility.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import TypeAlias

from public_import_foundation.architecture_conformance_adapter import (
    ArchitectureConformanceAdapter,
)
from public_import_foundation.input_snapshot import (
    FoundationFormatError,
    FoundationInputManifestSerializer,
)
from public_import_foundation.runtime_observation import PythonPackageRuntimeInspector
from public_import_foundation.source_observation import (
    PythonDefiningOriginResolver,
    PythonInitializerInspector,
)
from python_public_import_foundation_model import (
    ClaimBoundary,
    ClosedFoundationParser,
    FoundationJsonCodec,
    FoundationModelError,
    PublicImportFoundation,
)

JsonScalar: TypeAlias = None | bool | int | float | str
JsonValue: TypeAlias = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]
JsonRecord: TypeAlias = dict[str, JsonValue]


class DuplicateFoundationKeyError(ValueError):
    """Report one duplicate JSON object key."""


@dataclass(frozen=True, slots=True)
class PublicImportFoundationValidator:
    """Own deterministic F0 reproduction and failure checks."""

    repository_root: Path

    def execute(self) -> int:
        """Return zero only when every bounded F0 check passes."""
        diagnostic = self._validate_selection_coverage()
        if diagnostic is not None:
            print(diagnostic)
            return 1
        interpreter = self.repository_root / "python/.venv/bin/python"
        generator = (
            self.repository_root
            / ".pi/task-ownership/generate_python_public_import_foundation.py"
        )
        selection = (
            self.repository_root
            / "harness/reports/public-import-boundaries/phase3/foundation-selection.tsv"
        )
        manifest = (
            self.repository_root
            / "harness/reports/public-import-boundaries/phase3/foundation-inputs.json"
        )
        inventory = (
            self.repository_root / "harness/reports/python-architecture-inventory.json"
        )
        foundation = (
            self.repository_root
            / "harness/reports/public-import-boundaries/phase3/foundation.json"
        )
        with tempfile.TemporaryDirectory(prefix="public-import-foundation-") as raw:
            temporary = Path(raw)
            reproduced_manifest = temporary / "foundation-inputs.json"
            reproduced_foundation = temporary / "foundation.json"
            prepare = (
                interpreter,
                generator,
                "prepare",
                "--repository-root",
                self.repository_root,
                "--selection",
                selection,
                "--output",
                reproduced_manifest,
            )
            generate = (
                interpreter,
                generator,
                "generate",
                "--repository-root",
                self.repository_root,
                "--manifest",
                reproduced_manifest,
                "--accepted-inventory",
                inventory,
                "--output",
                reproduced_foundation,
                "--python-executable",
                interpreter,
            )
            for reproduction_command in (prepare, generate):
                completed = subprocess.run(
                    reproduction_command, cwd=self.repository_root, check=False
                )
                if completed.returncode != 0:
                    return completed.returncode
            if reproduced_manifest.read_bytes() != manifest.read_bytes():
                print("reproduced F0 input manifest differs from maintained bytes")
                return 1
            if reproduced_foundation.read_bytes() != foundation.read_bytes():
                print("reproduced F0 foundation differs from maintained bytes")
                return 1
            if not self._identity_mismatch_fails(
                interpreter, generator, reproduced_manifest, inventory, temporary
            ):
                print("tampered F0 input identity did not fail closed")
                return 1
            if not self._output_aliases_fail(
                interpreter, generator, selection, reproduced_manifest, inventory
            ):
                print("F0 output/input alias did not fail closed")
                return 1
            diagnostic = self._initializer_rejection_probes()
            if diagnostic is not None:
                print(diagnostic)
                return 1
            diagnostic = self._runtime_file_probe(interpreter, temporary)
            if diagnostic is not None:
                print(diagnostic)
                return 1
        diagnostic = self._validate_foundation_schema(foundation)
        if diagnostic is not None:
            print(diagnostic)
            return 1
        report = ClosedFoundationParser().execute(
            FoundationJsonCodec().decode(foundation.read_bytes())
        )
        for diagnostic in (
            self._validate_selected_identities(report),
            self._validate_phase2_reexecution(report, manifest),
            self._validate_documentation_and_claims(report),
            self._validate_scc_witnesses(),
            self._validate_origin_witnesses(),
            self._validate_recursive_json_confinement(),
            self._validate_path_isolation(),
        ):
            if diagnostic is not None:
                print(diagnostic)
                return 1
        commands: tuple[tuple[str | Path, ...], ...] = (
            (interpreter, "-m", "json.tool", manifest),
            (interpreter, "-m", "json.tool", foundation),
            (
                interpreter,
                "-m",
                "ksdft2effmass.harness.cli",
                "harness-projection",
                "--repository-root",
                self.repository_root,
                "check",
            ),
            (
                interpreter,
                "-m",
                "ksdft2effmass.harness.cli",
                "validate-harness",
                "--repository-root",
                self.repository_root,
            ),
            (
                interpreter,
                "-m",
                "ruff",
                "check",
                ".pi/task-ownership/generate_python_public_import_foundation.py",
                ".pi/task-ownership/python_public_import_foundation_model.py",
                ".pi/task-ownership/public_import_foundation",
                ".pi/task-ownership/validate_python_public_import_foundation.py",
            ),
            (
                interpreter,
                "-m",
                "ruff",
                "format",
                "--check",
                ".pi/task-ownership/generate_python_public_import_foundation.py",
                ".pi/task-ownership/python_public_import_foundation_model.py",
                ".pi/task-ownership/public_import_foundation",
                ".pi/task-ownership/validate_python_public_import_foundation.py",
            ),
            ("git", "diff", "--check"),
        )
        for check_command in commands:
            check_result = subprocess.run(
                check_command,
                cwd=self.repository_root,
                check=False,
                capture_output=True,
                text=True,
            )
            if check_result.returncode != 0:
                check_diagnostic = (check_result.stderr or check_result.stdout)[-4000:]
                if check_diagnostic:
                    print(check_diagnostic, file=sys.stderr)
                return check_result.returncode
        type_environment = dict(os.environ)
        type_environment["MYPYPATH"] = ".pi/task-ownership:python/src"
        type_check = subprocess.run(
            (
                interpreter,
                "-m",
                "mypy",
                "--strict",
                ".pi/task-ownership/generate_python_public_import_foundation.py",
                ".pi/task-ownership/python_public_import_foundation_model.py",
                ".pi/task-ownership/public_import_foundation",
                ".pi/task-ownership/validate_python_public_import_foundation.py",
            ),
            cwd=self.repository_root,
            env=type_environment,
            check=False,
            capture_output=True,
            text=True,
        )
        if type_check.returncode != 0:
            print((type_check.stderr or type_check.stdout)[-4000:], file=sys.stderr)
            return type_check.returncode
        return 0

    def _validate_selection_coverage(self) -> str | None:
        """Require every tracked first-party Python path exactly once."""
        selection_path = (
            self.repository_root
            / "harness/reports/public-import-boundaries/phase3/foundation-selection.tsv"
        )
        selected: list[str] = []
        selected_by_category: dict[str, set[str]] = {}
        for line_number, line in enumerate(
            selection_path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if not line or line.startswith("#"):
                continue
            fields = line.split("\t")
            if len(fields) != 2:
                return f"invalid selection line {line_number}"
            selected.append(fields[1])
            selected_by_category.setdefault(fields[0], set()).add(fields[1])
        if len(selected) != len(set(selected)):
            return "F0 selection contains duplicate paths"
        completed = subprocess.run(
            ("git", "ls-files", "*.py"),
            cwd=self.repository_root,
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            return "cannot enumerate tracked Python paths for selection coverage"
        tracked = set(completed.stdout.splitlines())
        required_new = {
            ".pi/task-ownership/generate_python_public_import_foundation.py",
            ".pi/task-ownership/python_public_import_foundation_model.py",
            ".pi/task-ownership/validate_python_public_import_foundation.py",
        }
        expected = tracked | required_new
        selected_python = {path for path in selected if path.endswith(".py")}
        if selected_python != expected:
            missing = sorted(expected - selected_python)
            unexpected = sorted(selected_python - expected)
            return f"F0 Python selection mismatch; missing={missing}, unexpected={unexpected}"
        documentation_result = subprocess.run(
            (
                "git",
                "ls-files",
                "docs/api",
                "docs/concepts",
                "docs/user-guide",
                "docs/verification",
                "docs/architecture/migration",
                "docs/development/source-documentation.rst",
            ),
            cwd=self.repository_root,
            check=False,
            capture_output=True,
            text=True,
        )
        if documentation_result.returncode != 0:
            return "cannot enumerate public-import documentation coverage"
        expected_documentation = {
            path
            for path in documentation_result.stdout.splitlines()
            if path.endswith((".md", ".rst"))
        }
        selected_documentation = selected_by_category.get("public_documentation", set())
        if selected_documentation != expected_documentation:
            missing = sorted(expected_documentation - selected_documentation)
            unexpected = sorted(selected_documentation - expected_documentation)
            return f"F0 documentation selection mismatch; missing={missing}, unexpected={unexpected}"
        phase2_paths = {
            ".pi/task-ownership/python.architecture-refactor.architecture-conformance.dependency-graph-views.json",
            ".pi/task-ownership/python.architecture-refactor.architecture-conformance.production-facts.json",
            "tasks/software/python.architecture-refactor.architecture-conformance.dependency-graph-views.json",
            "tasks/software/python.architecture-refactor.architecture-conformance.production-facts.json",
        }
        if not phase2_paths.issubset(selected_by_category.get("phase2_view", set())):
            return "F0 selection omits required accepted Phase 2 view records"
        return None

    def _identity_mismatch_fails(
        self,
        interpreter: Path,
        generator: Path,
        manifest: Path,
        inventory: Path,
        temporary: Path,
    ) -> bool:
        """Return whether one changed selected identity is rejected."""
        text = manifest.read_text(encoding="utf-8")
        marker = '"sha256":"'
        start = text.find(marker)
        if start < 0:
            return False
        value_start = start + len(marker)
        tampered = text[:value_start] + ("0" * 64) + text[value_start + 64 :]
        tampered_manifest = temporary / "tampered-inputs.json"
        tampered_output = temporary / "tampered-foundation.json"
        tampered_manifest.write_text(tampered, encoding="utf-8")
        sentinel = b"pre-existing output must survive failure\n"
        tampered_output.write_bytes(sentinel)
        completed = subprocess.run(
            (
                interpreter,
                generator,
                "generate",
                "--repository-root",
                self.repository_root,
                "--manifest",
                tampered_manifest,
                "--accepted-inventory",
                inventory,
                "--output",
                tampered_output,
                "--python-executable",
                interpreter,
            ),
            cwd=self.repository_root,
            check=False,
            capture_output=True,
        )
        return completed.returncode != 0 and tampered_output.read_bytes() == sentinel

    def _output_aliases_fail(
        self,
        interpreter: Path,
        generator: Path,
        selection: Path,
        manifest: Path,
        inventory: Path,
    ) -> bool:
        """Return whether prepare/generate reject every tested input alias."""
        selection_before = selection.read_bytes()
        prepare = subprocess.run(
            (
                interpreter,
                generator,
                "prepare",
                "--repository-root",
                self.repository_root,
                "--selection",
                selection,
                "--output",
                selection,
            ),
            cwd=self.repository_root,
            check=False,
            capture_output=True,
        )
        if prepare.returncode == 0 or selection.read_bytes() != selection_before:
            return False
        manifest_before = manifest.read_bytes()
        manifest_alias = subprocess.run(
            (
                interpreter,
                generator,
                "generate",
                "--repository-root",
                self.repository_root,
                "--manifest",
                manifest,
                "--accepted-inventory",
                inventory,
                "--output",
                manifest,
                "--python-executable",
                interpreter,
            ),
            cwd=self.repository_root,
            check=False,
            capture_output=True,
        )
        if manifest_alias.returncode == 0 or manifest.read_bytes() != manifest_before:
            return False
        inventory_before = inventory.read_bytes()
        inventory_alias = subprocess.run(
            (
                interpreter,
                generator,
                "generate",
                "--repository-root",
                self.repository_root,
                "--manifest",
                manifest,
                "--accepted-inventory",
                inventory,
                "--output",
                inventory,
                "--python-executable",
                interpreter,
            ),
            cwd=self.repository_root,
            check=False,
            capture_output=True,
        )
        return (
            inventory_alias.returncode != 0
            and inventory.read_bytes() == inventory_before
        )

    def _initializer_rejection_probes(self) -> str | None:
        """Exercise the literal success case and all eleven authored escape forms."""
        inspector = PythonInitializerInspector()
        valid = inspector.execute(
            "probe", "probe.py", b"from x import X\n__all__ = ['X']\n"
        )
        if valid[1] != ("X",):
            return "literal initializer probe did not preserve source order"
        invalid = (
            (b"globals()['__all__'] = ['A']\n", "indirect __all__ access"),
            (b"del vars()['__all__']\n", "indirect __all__ access"),
            (
                b"__all__ = ['A']\nalias = __all__\nalias.append('B')\n",
                "aliased __all__ access",
            ),
            (
                b"__all__ = ['A']\n__all__.append('B')\n",
                "unrepresented __all__ mutation",
            ),
            (
                b"if flag:\n    __all__ = ['A']\n",
                "unrepresented __all__ assignment",
            ),
            (
                b"ns = globals()\nns['__all__'] = ['A']\n",
                "namespace alias can mutate __all__",
            ),
            (
                b"ns = vars()\nns['__all__'] = ['A']\n",
                "namespace alias can mutate __all__",
            ),
            (
                b"globals().update(__all__=['A'])\n",
                "namespace call can mutate __all__",
            ),
            (
                b"globals().__setitem__('__all__', ['A'])\n",
                "namespace call can mutate __all__",
            ),
            (
                b"__all__ = ['A']\nmutate(__all__)\n",
                "unrepresented __all__ load or escape",
            ),
            (
                b"__all__ = ['A']\n(alias := __all__).append('B')\n",
                "unrepresented __all__ load or escape",
            ),
        )
        for payload, expected in invalid:
            try:
                inspector.execute("probe", "probe.py", payload)
            except FoundationFormatError as exc:
                if expected not in str(exc):
                    return (
                        f"initializer probe has wrong diagnostic for {expected}: {exc}"
                    )
                continue
            return f"initializer escape was accepted: {expected}"
        return None

    def _runtime_file_probe(self, interpreter: Path, temporary: Path) -> str | None:
        """Require unreadable string paths to fail without changing an output."""
        source_root = temporary / "runtime-repository/python/src"
        broken_package = source_root / "broken_probe"
        broken_package.mkdir(parents=True)
        (broken_package / "__init__.py").write_text(
            "import sys\n"
            "import types\n"
            "broken = types.ModuleType('broken_probe.unreadable')\n"
            "broken.__file__ = '/deterministic/nonexistent/module.py'\n"
            "sys.modules[broken.__name__] = broken\n",
            encoding="utf-8",
        )
        sentinel = temporary / "runtime-sentinel.json"
        sentinel.write_bytes(b"sentinel\n")
        inspector = PythonPackageRuntimeInspector(
            python_executable=interpreter.resolve(),
            repository_root=temporary / "runtime-repository",
        )
        environment = inspector.environment()
        try:
            inspector.execute("broken_probe", environment.environment_sha256)
        except FoundationFormatError as exc:
            expected = (
                "runtime package import failed for broken_probe: "
                "unreadable loaded module file: broken_probe.unreadable"
            )
            if str(exc) != expected:
                return f"runtime unreadable-file diagnostic disagrees: {exc}"
        else:
            return "unreadable string-valued runtime file was silently omitted"
        if sentinel.read_bytes() != b"sentinel\n":
            return "runtime failure changed pre-existing output"
        safe_package = source_root / "safe_probe"
        safe_package.mkdir()
        (safe_package / "__init__.py").write_text(
            "import sys\n"
            "import types\n"
            "virtual = types.ModuleType('safe_probe.virtual')\n"
            "sys.modules[virtual.__name__] = virtual\n",
            encoding="utf-8",
        )
        safe = inspector.execute("safe_probe", environment.environment_sha256)
        if any(
            item.module_name == "safe_probe.virtual"
            for item in safe.observation.loaded_files
        ):
            return "non-file-backed module entered the loaded-file view"
        return None

    def _validate_foundation_schema(self, path: Path) -> str | None:
        """Decode strictly, validate the closed model, then check external identities."""
        try:
            value: JsonValue = json.loads(
                path.read_text(encoding="utf-8"),
                object_pairs_hook=self._unique_pairs,
            )
        except (json.JSONDecodeError, UnicodeError, DuplicateFoundationKeyError) as exc:
            return f"foundation JSON cannot be decoded strictly: {exc}"
        try:
            report = ClosedFoundationParser().execute(value)
        except FoundationModelError as exc:
            return f"foundation closed schema is invalid: {exc}"
        root = self._record(value, "foundation")
        if root is None:
            return "foundation must be an object"
        input_by_path = {item.path: item for item in report.inputs}
        for package in report.package_surfaces:
            selected = input_by_path.get(package.initializer_path)
            if (
                selected is None
                or selected.sha256 != package.initializer_sha256
                or selected.byte_count != package.initializer_byte_count
            ):
                return (
                    f"initializer/input identity mismatch: {package.initializer_path}"
                )
        lineage_roles = tuple(item.role for item in report.phase2_lineage_inputs)
        expected_roles = (
            "production_facts_task",
            "production_facts_ownership",
            "production_facts_implementation",
            "dependency_graph_task",
            "dependency_graph_ownership",
            "dependency_graph_implementation",
        )
        if lineage_roles != expected_roles:
            return "Phase 2 lineage roles are incomplete or unordered"
        for item in report.phase2_lineage_inputs:
            selected = input_by_path.get(item.path)
            if (
                selected is None
                or selected.sha256 != item.sha256
                or selected.byte_count != item.byte_count
            ):
                return f"Phase 2 lineage identity mismatch: {item.path}"
        for observation in report.runtime_observations:
            loaded_files = observation.observation.loaded_files
            loaded_keys = tuple((item.module_name, item.path) for item in loaded_files)
            if loaded_keys != tuple(sorted(loaded_keys)) or len(loaded_keys) != len(
                set(loaded_keys)
            ):
                return f"runtime loaded-file identities are not unique and sorted: {observation.package}"
            for loaded in loaded_files:
                loaded_path = Path(loaded.path)
                try:
                    payload = loaded_path.read_bytes()
                except OSError as exc:
                    return f"runtime loaded file cannot be reidentified: {loaded.path}: {exc}"
                if (
                    len(payload) != loaded.byte_count
                    or hashlib.sha256(payload).hexdigest() != loaded.sha256
                ):
                    return f"runtime loaded-file identity mismatch: {loaded.path}"
        diagnostic = self._validate_terminal_origins(report)
        if diagnostic is not None:
            return diagnostic
        diagnostic = self._validate_accepted_anchor(root)
        if diagnostic is not None:
            return diagnostic
        return self._closed_schema_mutations_fail(value)

    def _validate_terminal_origins(self, report: PublicImportFoundation) -> str | None:
        """Independently require each resolved first-party target to be terminal."""
        imports: dict[str, set[str]] = {}
        definitions: dict[str, set[str]] = {}
        for output in report.production_fact_outputs:
            try:
                tree = ast.parse(
                    (self.repository_root / output.path).read_bytes(),
                    filename=output.path,
                )
            except (OSError, SyntaxError, UnicodeError) as exc:
                return f"cannot inspect terminal origin source {output.path}: {exc}"
            imported: set[str] = set()
            defined: set[str] = set()
            for node in tree.body:
                if isinstance(node, ast.Import):
                    imported.update(
                        alias.asname or alias.name.split(".")[0] for alias in node.names
                    )
                elif isinstance(node, ast.ImportFrom):
                    imported.update(
                        alias.asname or alias.name
                        for alias in node.names
                        if alias.name != "*"
                    )
                elif isinstance(
                    node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
                ):
                    defined.add(node.name)
                elif isinstance(node, ast.TypeAlias) and isinstance(
                    node.name, ast.Name
                ):
                    defined.add(node.name.id)
                elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                    targets = (
                        node.targets if isinstance(node, ast.Assign) else [node.target]
                    )
                    defined.update(
                        target.id for target in targets if isinstance(target, ast.Name)
                    )
            imports[output.module_name] = imported
            definitions[output.module_name] = defined
        module_names = tuple(sorted(imports, key=len, reverse=True))
        for package in report.package_surfaces:
            for binding in package.bindings:
                target = binding.defining_origin
                if target is None or target in imports:
                    continue
                matching = next(
                    (
                        module
                        for module in module_names
                        if target.startswith(f"{module}.")
                    ),
                    None,
                )
                if matching is None:
                    continue
                symbol = target[len(matching) + 1 :]
                if "." in symbol:
                    continue
                if symbol in imports[matching]:
                    return f"defining origin still names a re-export: {target}"
                if symbol not in definitions[matching]:
                    return f"defining origin is absent from selected source: {target}"
        return None

    @staticmethod
    def _unique_pairs(pairs: list[tuple[str, JsonValue]]) -> JsonRecord:
        """Reject duplicate object members during independent JSON decoding."""
        record: JsonRecord = {}
        for key, value in pairs:
            if key in record:
                raise DuplicateFoundationKeyError(f"duplicate JSON key: {key}")
            record[key] = value
        return record

    def _closed_schema_mutations_fail(self, value: JsonValue) -> str | None:
        """Exercise each authored malformed relation with attributed diagnostics."""
        probes: list[tuple[str, JsonValue, tuple[str, ...], str]] = []

        graph_discriminant = self._clone(value)
        graphs = self._required_array(
            self._required_record(graph_discriminant, "foundation")[
                "dependency_graph_views"
            ],
            "dependency_graph_views",
        )
        self._required_record(graphs[0], "graph[0]")["view"] = "unsupported"
        probes.append(
            (
                "graph discriminant",
                graph_discriminant,
                ("$.dependency_graph_views[0].view",),
                "view has an unsupported value",
            )
        )

        runtime_view = self._clone(value)
        runtime_rows = self._required_array(
            self._required_record(runtime_view, "foundation")[
                "package_runtime_observations"
            ],
            "runtime observations",
        )
        self._required_record(runtime_rows[0], "runtime[0]")["view"] = "unsupported"
        probes.append(
            (
                "runtime view discriminant",
                runtime_view,
                ("$.package_runtime_observations[0].view",),
                "view has an unsupported value",
            )
        )

        runtime_status = self._clone(value)
        runtime_rows = self._required_array(
            self._required_record(runtime_status, "foundation")[
                "package_runtime_observations"
            ],
            "runtime observations",
        )
        self._required_record(
            self._required_record(runtime_rows[0], "runtime[0]")["observation"],
            "observation",
        )["status"] = "unsupported"
        probes.append(
            (
                "runtime status discriminant",
                runtime_status,
                ("$.package_runtime_observations[0].observation.status",),
                "runtime status is invalid",
            )
        )

        runtime_failure = self._clone(value)
        runtime_rows = self._required_array(
            self._required_record(runtime_failure, "foundation")[
                "package_runtime_observations"
            ],
            "runtime observations",
        )
        failure_index = next(
            index
            for index, row in enumerate(runtime_rows)
            if self._required_record(
                self._required_record(row, "runtime row")["observation"],
                "observation",
            ).get("status")
            == "failure"
        )
        self._required_record(
            self._required_record(runtime_rows[failure_index], "runtime row")[
                "observation"
            ],
            "observation",
        )["failure_kind"] = "unsupported"
        probes.append(
            (
                "runtime failure discriminant",
                runtime_failure,
                (
                    f"$.package_runtime_observations[{failure_index}].observation.failure_kind",
                ),
                "failure_kind has an unsupported value",
            )
        )

        distribution = self._clone(value)
        distributions = self._required_array(
            self._required_record(
                self._required_record(distribution, "foundation")[
                    "runtime_environment"
                ],
                "runtime_environment",
            )["distributions"],
            "distributions",
        )
        first_distribution = self._required_array(distributions[0], "distribution[0]")
        first_distribution.append("third")
        probes.append(
            (
                "three-item distribution",
                distribution,
                ("$.runtime_environment.distributions[0].length",),
                "distribution must contain exactly two fields",
            )
        )

        duplicate_star = self._clone(value)
        package_rows = self._required_array(
            self._required_record(duplicate_star, "foundation")["package_surfaces"],
            "package_surfaces",
        )
        package_index = next(
            index
            for index, row in enumerate(package_rows)
            if len(
                self._required_array(
                    self._required_record(row, "package")["effective_star_names"],
                    "effective_star_names",
                )
            )
            > 1
        )
        names = self._required_array(
            self._required_record(package_rows[package_index], "package")[
                "effective_star_names"
            ],
            "effective_star_names",
        )
        names[1] = names[0]
        probes.append(
            (
                "duplicate effective-star name",
                duplicate_star,
                (f"$.package_surfaces[{package_index}].effective_star_names[1]",),
                "effective_star_names must be unique",
            )
        )

        duplicate_attribute = self._clone(value)
        runtime_rows = self._required_array(
            self._required_record(duplicate_attribute, "foundation")[
                "package_runtime_observations"
            ],
            "runtime observations",
        )
        attribute_index = next(
            index
            for index, row in enumerate(runtime_rows)
            if len(
                self._required_array(
                    self._required_record(
                        self._required_record(row, "runtime")["observation"],
                        "observation",
                    ).get("attributes"),
                    "attributes",
                )
            )
            > 1
        )
        attributes = self._required_array(
            self._required_record(
                self._required_record(runtime_rows[attribute_index], "runtime")[
                    "observation"
                ],
                "observation",
            )["attributes"],
            "attributes",
        )
        self._required_record(attributes[1], "attribute[1]")["name"] = (
            self._required_record(attributes[0], "attribute[0]")["name"]
        )
        probes.append(
            (
                "duplicate runtime attribute",
                duplicate_attribute,
                (
                    f"$.package_runtime_observations[{attribute_index}].observation.attributes[1].name",
                ),
                "runtime attributes must be name-sorted and unique",
            )
        )

        origin_nonstar = self._clone(value)
        package_rows = self._required_array(
            self._required_record(origin_nonstar, "foundation")["package_surfaces"],
            "package_surfaces",
        )
        nonstar_package, nonstar_binding = self._find_binding(
            package_rows, require_star=False
        )
        nonstar_row = self._required_record(
            self._required_array(
                self._required_record(package_rows[nonstar_package], "package")[
                    "bindings"
                ],
                "bindings",
            )[nonstar_binding],
            "binding",
        )
        nonstar_row["defining_origin"] = "invented.module.Symbol"
        nonstar_row["origin_resolution"] = "transitive_first_party_binding"
        probes.append(
            (
                "origin pair on non-star binding",
                origin_nonstar,
                (
                    f"$.package_surfaces[{nonstar_package}].bindings[{nonstar_binding}].defining_origin",
                    f"$.package_surfaces[{nonstar_package}].bindings[{nonstar_binding}].origin_resolution",
                ),
                "non-star bindings cannot retain origin pairs",
            )
        )

        missing_star_origin = self._clone(value)
        package_rows = self._required_array(
            self._required_record(missing_star_origin, "foundation")[
                "package_surfaces"
            ],
            "package_surfaces",
        )
        star_package, star_binding = self._find_binding(package_rows, require_star=True)
        star_row = self._required_record(
            self._required_array(
                self._required_record(package_rows[star_package], "package")[
                    "bindings"
                ],
                "bindings",
            )[star_binding],
            "binding",
        )
        del star_row["defining_origin"]
        del star_row["origin_resolution"]
        probes.append(
            (
                "missing origin pair on star binding",
                missing_star_origin,
                (
                    f"$.package_surfaces[{star_package}].bindings[{star_binding}].defining_origin",
                    f"$.package_surfaces[{star_package}].bindings[{star_binding}].origin_resolution",
                ),
                "each effective star name requires an origin pair",
            )
        )

        accepted_count = self._clone(value)
        accepted = self._required_record(
            self._required_record(accepted_count, "foundation")["accepted_inventory"],
            "accepted_inventory",
        )
        accepted["byte_count"] = (
            self._required_integer(accepted["byte_count"], "accepted byte_count") + 1
        )
        probes.append(
            (
                "accepted byte count",
                accepted_count,
                ("$.accepted_inventory.byte_count",),
                "accepted inventory anchor is unsupported",
            )
        )

        arbitrary_claim = self._clone(value)
        claims = self._required_array(
            self._required_record(arbitrary_claim, "foundation")["claim_boundaries"],
            "claim_boundaries",
        )
        claims[0] = "arbitrary support claim"
        probes.append(
            (
                "arbitrary claim text",
                arbitrary_claim,
                ("$.claim_boundaries[0]",),
                "claim has an unsupported value",
            )
        )

        duplicate_production = self._clone(value)
        production = self._required_array(
            self._required_record(duplicate_production, "foundation")[
                "production_fact_outputs"
            ],
            "production_fact_outputs",
        )
        production.append(self._clone(production[0]))
        probes.append(
            (
                "duplicate 217th production row",
                duplicate_production,
                ("$.production_fact_outputs.length",),
                "production_fact_outputs must be module-name-sorted and unique",
            )
        )

        nonbijection = self._clone(value)
        production = self._required_array(
            self._required_record(nonbijection, "foundation")[
                "production_fact_outputs"
            ],
            "production_fact_outputs",
        )
        last = self._required_record(production[-1], "last production row")
        last_index = len(production) - 1
        last["path"] = "python/src/zzzz/unselected.py"
        probes.append(
            (
                "count-preserving production non-bijection",
                nonbijection,
                (f"$.production_fact_outputs[{last_index}].path",),
                "production-fact outputs must bijectively cover 216 selected modules",
            )
        )

        duplicate_loaded = self._clone(value)
        runtime_rows = self._required_array(
            self._required_record(duplicate_loaded, "foundation")[
                "package_runtime_observations"
            ],
            "runtime observations",
        )
        loaded_runtime = next(
            index
            for index, row in enumerate(runtime_rows)
            if len(
                self._required_array(
                    self._required_record(
                        self._required_record(row, "runtime")["observation"],
                        "observation",
                    )["loaded_files"],
                    "loaded_files",
                )
            )
            > 1
        )
        loaded = self._required_array(
            self._required_record(
                self._required_record(runtime_rows[loaded_runtime], "runtime")[
                    "observation"
                ],
                "observation",
            )["loaded_files"],
            "loaded_files",
        )
        first_loaded = self._required_record(loaded[0], "loaded[0]")
        second_loaded = self._required_record(loaded[1], "loaded[1]")
        second_loaded["module_name"] = first_loaded["module_name"]
        second_loaded["path"] = first_loaded["path"]
        probes.append(
            (
                "duplicate loaded-file key",
                duplicate_loaded,
                (
                    f"$.package_runtime_observations[{loaded_runtime}].observation.loaded_files[1].module_name",
                    f"$.package_runtime_observations[{loaded_runtime}].observation.loaded_files[1].path",
                ),
                "runtime loaded files must be key-sorted and unique",
            )
        )

        noncanonical_components = self._clone(value)
        graph_rows = self._required_array(
            self._required_record(noncanonical_components, "foundation")[
                "dependency_graph_views"
            ],
            "dependency_graph_views",
        )
        components = self._required_array(
            self._required_record(graph_rows[0], "graph[0]")[
                "strongly_connected_components"
            ],
            "components",
        )
        components[0], components[1] = components[1], components[0]
        probes.append(
            (
                "noncanonical components",
                noncanonical_components,
                (
                    "$.dependency_graph_views[0].strongly_connected_components[0][0]",
                    "$.dependency_graph_views[0].strongly_connected_components[1][0]",
                ),
                "represented components must be canonically ordered",
            )
        )

        for label, mutated, expected_paths, diagnostic in probes:
            rejection = self._expect_mutation_rejection(
                value, mutated, label, expected_paths, diagnostic
            )
            if rejection is not None:
                return rejection

        canonical = json.dumps(value, sort_keys=True, separators=(",", ":"))
        duplicate_key = canonical.replace("{", '{"schema_version":1,', 1)
        try:
            json.loads(duplicate_key, object_pairs_hook=self._unique_pairs)
        except DuplicateFoundationKeyError as exc:
            if str(exc) != "duplicate JSON key: schema_version":
                return f"duplicate-key diagnostic disagrees: {exc}"
        else:
            return "duplicate JSON key was accepted"
        return None

    def _expect_mutation_rejection(
        self,
        original: JsonValue,
        mutated: JsonValue,
        label: str,
        expected_paths: tuple[str, ...],
        expected_diagnostic: str,
    ) -> str | None:
        differences = self._differences(original, mutated, "$")
        if differences != expected_paths:
            return (
                f"{label} changed the wrong fields: "
                f"expected={expected_paths}, actual={differences}"
            )
        try:
            ClosedFoundationParser().execute(mutated)
        except (FoundationModelError, TypeError, ValueError) as exc:
            if expected_diagnostic not in str(exc):
                return f"{label} has wrong diagnostic: {exc}"
            return None
        return f"malformed state was accepted: {label}"

    @classmethod
    def _differences(
        cls, left: JsonValue, right: JsonValue, path: str
    ) -> tuple[str, ...]:
        if type(left) is not type(right):
            return (path,)
        if type(left) is dict and type(right) is dict:
            paths: list[str] = []
            for key in sorted(set(left) | set(right)):
                if key not in left or key not in right:
                    paths.append(f"{path}.{key}")
                else:
                    paths.extend(
                        cls._differences(left[key], right[key], f"{path}.{key}")
                    )
            return tuple(paths)
        if type(left) is list and type(right) is list:
            paths = []
            for index, (left_item, right_item) in enumerate(
                zip(left, right, strict=False)
            ):
                paths.extend(
                    cls._differences(left_item, right_item, f"{path}[{index}]")
                )
            if len(left) != len(right):
                paths.append(f"{path}.length")
            return tuple(paths)
        return () if left == right else (path,)

    @staticmethod
    def _clone(value: JsonValue) -> JsonValue:
        codec = FoundationJsonCodec()
        return codec.decode(codec.encode(value))

    @staticmethod
    def _required_record(value: JsonValue | None, label: str) -> JsonRecord:
        if type(value) is not dict:
            raise FoundationModelError(f"{label} must be an object")
        return value

    @staticmethod
    def _required_array(value: JsonValue | None, label: str) -> list[JsonValue]:
        if type(value) is not list:
            raise FoundationModelError(f"{label} must be an array")
        return value

    @staticmethod
    def _required_integer(value: JsonValue | None, label: str) -> int:
        if type(value) is not int:
            raise FoundationModelError(f"{label} must be an int")
        return value

    def _find_binding(
        self, package_rows: list[JsonValue], *, require_star: bool
    ) -> tuple[int, int]:
        for package_index, package_value in enumerate(package_rows):
            package = self._required_record(package_value, "package")
            names = {
                name
                for name in self._required_array(
                    package["effective_star_names"], "effective_star_names"
                )
                if type(name) is str
            }
            for binding_index, binding_value in enumerate(
                self._required_array(package["bindings"], "bindings")
            ):
                binding = self._required_record(binding_value, "binding")
                local_name = binding.get("local_name")
                if type(local_name) is str and (local_name in names) is require_star:
                    return package_index, binding_index
        raise FoundationModelError("required binding probe cannot be constructed")

    def _validate_selected_identities(
        self, report: PublicImportFoundation
    ) -> str | None:
        """Reidentify every selected byte stream independently of generation."""
        for item in report.inputs:
            path = self.repository_root / item.path
            try:
                payload = path.read_bytes()
            except OSError as exc:
                return f"selected input cannot be read: {item.path}: {exc}"
            if len(payload) != item.byte_count:
                return f"selected input byte count changed: {item.path}"
            if hashlib.sha256(payload).hexdigest() != item.sha256:
                return f"selected input digest changed: {item.path}"
        return None

    def _validate_phase2_reexecution(
        self, report: PublicImportFoundation, manifest_path: Path
    ) -> str | None:
        """Execute accepted Phase 2 owners again on the exact selected bytes."""
        try:
            manifest = FoundationInputManifestSerializer().decode(
                manifest_path.read_bytes()
            )
            payloads = {
                item.path.as_posix(): (self.repository_root / item.path).read_bytes()
                for item in manifest.entries
            }
            production, graphs = ArchitectureConformanceAdapter().execute(
                manifest, payloads
            )
        except (FoundationFormatError, OSError, UnicodeError, ValueError) as exc:
            return f"Phase 2 owner reexecution failed: {exc}"
        if production != report.production_fact_outputs:
            return "accepted Phase 2 production records disagree with foundation"
        if graphs != report.dependency_graph_views:
            return "accepted Phase 2 graph views disagree with foundation"
        return None

    def _validate_documentation_and_claims(
        self, report: PublicImportFoundation
    ) -> str | None:
        """Retain exact document coverage and neutral claim boundaries."""
        selected_documents = {
            item.path
            for item in report.inputs
            if item.category.value == "public_documentation"
        }
        if len(selected_documents) != 93:
            return f"selected public-document count changed: {len(selected_documents)}"
        if len(report.documentation_citations) != 246:
            return (
                "represented documentation-citation count changed: "
                f"{len(report.documentation_citations)}"
            )
        if any(
            item.path not in selected_documents
            for item in report.documentation_citations
        ):
            return "documentation citation names an unselected document"
        if report.claim_boundaries != tuple(ClaimBoundary):
            return "claim boundaries are not the exact neutral closed set"
        if any(
            route.support_status != "unknown_no_exact_accepted_support_evidence"
            or route.compatibility_disposition
            != "unclassified_pending_bounded_option_b_application"
            for route in report.predecessor_routes
        ):
            return "predecessor routes no longer retain neutral states"
        return None

    def _validate_scc_witnesses(self) -> str | None:
        """Exercise independent directed SCC witnesses and malformed partitions."""
        cases = (
            (("A", "B"), (("A", "B"),), (("A",), ("B",)), True, "A -> B"),
            (
                ("A", "B"),
                (("A", "B"), ("B", "A")),
                (("A", "B"),),
                True,
                "A <-> B",
            ),
            (("A",), (), (("A",),), True, "isolated node"),
            (
                ("A", "B"),
                (("A", "B"),),
                (("A",), ("A", "B")),
                False,
                "duplicate membership",
            ),
            (
                ("A", "B"),
                (),
                (("B",), ("A",)),
                False,
                "noncanonical components",
            ),
        )
        for nodes, edges, components, expected, label in cases:
            if self._sccs_agree(nodes, edges, components) is not expected:
                return f"SCC witness disagrees: {label}"
        return None

    @staticmethod
    def _sccs_agree(
        nodes: tuple[str, ...],
        edges: tuple[tuple[str, str], ...],
        components: tuple[tuple[str, ...], ...],
    ) -> bool:
        if nodes != tuple(sorted(set(nodes))):
            return False
        if edges != tuple(sorted(set(edges))):
            return False
        if any(source not in nodes or target not in nodes for source, target in edges):
            return False
        if any(component != tuple(sorted(set(component))) for component in components):
            return False
        if components != tuple(sorted(set(components))):
            return False
        flattened = tuple(name for component in components for name in component)
        if len(flattened) != len(set(flattened)) or set(flattened) != set(nodes):
            return False
        adjacency = {
            node: tuple(target for source, target in edges if source == node)
            for node in nodes
        }
        reachable: dict[str, frozenset[str]] = {}
        for node in nodes:
            pending = [node]
            visited: set[str] = set()
            while pending:
                current = pending.pop()
                if current in visited:
                    continue
                visited.add(current)
                pending.extend(adjacency[current])
            reachable[node] = frozenset(visited)
        component_by_node = {
            node: index
            for index, component in enumerate(components)
            for node in component
        }
        return all(
            (target in reachable[source] and source in reachable[target])
            is (component_by_node[source] == component_by_node[target])
            for source in nodes
            for target in nodes
        )

    @staticmethod
    def _validate_origin_witnesses() -> str | None:
        """Retain terminal, cycle, and missing defining-origin witnesses."""
        acyclic = (
            ("p.a", (("X", "from_import", "p.b.X"),)),
            ("p.b", (("X", "definition", "p.b.X"),)),
        )
        if PythonDefiningOriginResolver.resolve("p.a.X", acyclic) != "p.b.X":
            return "acyclic defining-origin witness did not reach its terminal"
        cycle = (
            ("p.a", (("X", "from_import", "p.b.X"),)),
            ("p.b", (("X", "from_import", "p.a.X"),)),
        )
        try:
            PythonDefiningOriginResolver.resolve("p.a.X", cycle)
        except FoundationFormatError as exc:
            if str(exc) != "cyclic defining origin: p.a.X":
                return f"cycle witness has wrong diagnostic: {exc}"
        else:
            return "cyclic defining-origin witness was accepted"
        missing = (("p.a", ()),)
        try:
            PythonDefiningOriginResolver.resolve("p.a.X", missing)
        except FoundationFormatError as exc:
            if str(exc) != "missing defining origin: p.a.X":
                return f"missing-origin witness has wrong diagnostic: {exc}"
        else:
            return "missing defining-origin witness was accepted"
        return None

    def _validate_recursive_json_confinement(self) -> str | None:
        """Require recursive JSON aliases only at immediate representation boundaries."""
        root = self.repository_root / ".pi/task-ownership"
        allowed = {
            "python_public_import_foundation_model.py",
            "public_import_foundation/input_snapshot.py",
            "public_import_foundation/runtime_observation.py",
            "public_import_foundation/foundation_assembly.py",
            "validate_python_public_import_foundation.py",
        }
        inspected = {
            "generate_python_public_import_foundation.py",
            "python_public_import_foundation_model.py",
            "validate_python_public_import_foundation.py",
            *{
                f"public_import_foundation/{path.name}"
                for path in (root / "public_import_foundation").glob("*.py")
            },
        }
        observed = {
            relative
            for relative in inspected
            if "JsonValue" in (root / relative).read_text(encoding="utf-8")
            or "JsonRecord" in (root / relative).read_text(encoding="utf-8")
        }
        if observed != allowed:
            return (
                "recursive JSON escaped or disappeared from the reviewed boundary: "
                f"{sorted(observed)}"
            )
        for relative in inspected - allowed:
            tree = ast.parse((root / relative).read_bytes(), filename=relative)
            if any(
                isinstance(node, ast.Name) and node.id in {"JsonValue", "JsonRecord"}
                for node in ast.walk(tree)
            ):
                return f"recursive JSON annotation escaped its boundary: {relative}"
        return None

    def _validate_path_isolation(self) -> str | None:
        """Verify protected and deferred paths retained their activation identities."""
        forbidden = (
            "python/src",
            "docs/api",
            "docs/concepts",
            "docs/user-guide",
            "docs/verification",
            "docs/architecture/migration",
            "docs/development/source-documentation.rst",
            "python/pyproject.toml",
            "python/uv.lock",
            "python/tests",
        )
        completed = subprocess.run(
            ("git", "diff", "--name-only", "HEAD", "--", *forbidden),
            cwd=self.repository_root,
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0 or completed.stdout.strip():
            return f"C5 path isolation failed: {completed.stdout.strip()}"
        manuscript = (
            self.repository_root
            / "docs/publications/research-monograph/appendices/J-two-dimensional-defect-extraction.tex"
        )
        if hashlib.sha256(manuscript.read_bytes()).hexdigest() != (
            "2beffed910248be8d7474836841015c81d84f0f063b7502ddf4dbb0c9cb6a517"
        ):
            return "excluded manuscript changed during C5"
        codec = FoundationJsonCodec()
        selection = self._required_record(
            codec.decode(
                (self.repository_root / "harness/task-selection.json").read_bytes()
            ),
            "task selection",
        )
        if selection.get("automatic_successor_activation") is not False:
            return "automatic successor activation changed"
        aggregate = self._required_record(
            codec.decode(
                (
                    self.repository_root
                    / "tasks/software/python.architecture-refactor.public-import-boundaries.current-fact-foundation.aggregate-verification.json"
                ).read_bytes()
            ),
            "aggregate task",
        )
        if aggregate.get("status") != "inactive":
            return "C6 became active during C5"
        return None

    def _validate_accepted_anchor(self, root: JsonRecord) -> str | None:
        """Verify current and accepted-closeout Phase 1 inventory identities."""
        accepted = self._record(root["accepted_inventory"], "accepted_inventory")
        expected = "fb180c5d8aa9ecd33a319d03a5795ab24343d9b2b553acac580ec452b5795c7e"
        if accepted is None or accepted.get("sha256") != expected:
            return "foundation accepted inventory anchor is invalid"
        completed = subprocess.run(
            (
                "git",
                "show",
                "f5ce3e981880fdfa336aa781664595b61a829557:harness/reports/python-architecture-inventory.json",
            ),
            cwd=self.repository_root,
            check=False,
            capture_output=True,
        )
        if (
            completed.returncode != 0
            or hashlib.sha256(completed.stdout).hexdigest() != expected
        ):
            return "Phase 1 accepted-closeout inventory anchor cannot be verified"
        return None

    @staticmethod
    def _record(value: JsonValue, label: str) -> JsonRecord | None:
        """Return one exact object or None; label documents the checked boundary."""
        del label
        return value if type(value) is dict else None

    @staticmethod
    def _text(value: JsonValue | None) -> str | None:
        return value if type(value) is str else None


def main() -> int:
    """Adapt the process entry point to the validator ActionObject."""
    root = Path(__file__).resolve().parents[2]
    return PublicImportFoundationValidator(root).execute()


if __name__ == "__main__":
    sys.exit(main())
