"""Software verification for representation-owner dependency boundaries."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

pytestmark = pytest.mark.software_verification


class TestRepresentationIdentityDependencyBoundary:
    """Protect representations <- transformations dependency direction."""

    @staticmethod
    def python_root() -> Path:
        """Return the repository Python root from this maintained test path."""
        for parent in Path(__file__).resolve().parents:
            if parent.name == "python":
                return parent
        raise AssertionError("test path is not under the repository Python root")

    @staticmethod
    def imports(path: Path) -> tuple[str, ...]:
        """Return absolute module text retained by Python import syntax."""
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        imported: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                imported.append(f"{'.' * node.level}{module}")
        return tuple(imported)

    def test_packages__do_not_import_outward_or_wire_owners(self) -> None:
        """Both sibling packages depend only on approved inward owners."""
        operators = self.python_root() / "src" / "ksdft2effmass" / "operators"
        packages = (operators / "representations", operators / "transformations")
        forbidden_tokens = (
            "analysis",
            "application",
            "campaigns",
            "formal",
            "model_adequacy",
            "projectkoios_formal",
            "publication",
            "publications",
            "schema",
            "schemas",
            "serialization",
            "serializers",
            "workflow",
        )

        failures: list[str] = []
        for package in packages:
            for path in sorted(package.glob("*.py")):
                for imported in self.imports(path):
                    if any(token in imported.split(".") for token in forbidden_tokens):
                        failures.append(f"{package.name}/{path.name}: {imported}")
        assert failures == []

    def test_representations__does_not_import_transformations(self) -> None:
        """Intrinsic representation nodes remain inward of directed edges."""
        package = (
            self.python_root()
            / "src"
            / "ksdft2effmass"
            / "operators"
            / "representations"
        )
        forbidden = "ksdft2effmass.operators.transformations"

        failures: list[str] = []
        for path in sorted(package.glob("*.py")):
            if any(
                imported.startswith(forbidden) or imported == "..transformations"
                for imported in self.imports(path)
            ):
                failures.append(path.name)
        assert failures == []

    def test_inward_owners__do_not_import_provisional_sibling_packages(self) -> None:
        """Core operators, periodic primitives, and diagnostics remain inward."""
        source = self.python_root() / "src" / "ksdft2effmass"
        representations = source / "operators" / "representations"
        transformations = source / "operators" / "transformations"
        owners = (
            source / "operators",
            source / "periodic",
            source / "analysis" / "matrix_field",
        )
        forbidden = (
            "ksdft2effmass.operators.representations",
            "ksdft2effmass.operators.transformations",
        )

        failures: list[str] = []
        for owner in owners:
            for path in sorted(owner.rglob("*.py")):
                if representations in path.parents or transformations in path.parents:
                    continue
                imports = self.imports(path)
                if any(
                    imported.startswith(prefix)
                    for imported in imports
                    for prefix in forbidden
                ):
                    failures.append(str(path.relative_to(source)))
        assert failures == []

    @pytest.mark.parametrize("package_name", ["representations", "transformations"])
    def test_package_initializer__does_not_flatten_module_owners(
        self,
        package_name: str,
    ) -> None:
        """Both package initializers remain documentation-only."""
        package_init = (
            self.python_root()
            / "src"
            / "ksdft2effmass"
            / "operators"
            / package_name
            / "__init__.py"
        )

        assert self.imports(package_init) == ()

    def test_operators_root__does_not_reexport_provisional_surfaces(self) -> None:
        """Sibling packages remain available only through defining modules."""
        operators_init = (
            self.python_root() / "src" / "ksdft2effmass" / "operators" / "__init__.py"
        )
        imports = self.imports(operators_init)

        assert ".representations" not in imports
        assert ".transformations" not in imports
