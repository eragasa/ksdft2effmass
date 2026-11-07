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

    @classmethod
    def phase1_modules(cls) -> tuple[Path, ...]:
        """Return the exact authorized Phase 1 source-module inventory."""
        operators = cls.python_root() / "src" / "ksdft2effmass" / "operators"
        representations = operators / "representations"
        transformations = operators / "transformations"
        return (
            representations / "__init__.py",
            representations / "domains.py",
            representations / "fields.py",
            representations / "identities.py",
            representations / "spaces.py",
            transformations / "__init__.py",
            transformations / "base.py",
            transformations / "identities.py",
        )

    @classmethod
    def imports(cls, path: Path) -> tuple[str, ...]:
        """Return imports resolved to absolute source-module names."""
        source_root = cls.python_root() / "src"
        package_parts = path.parent.relative_to(source_root).parts
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        imported: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                module_parts = (
                    () if node.module is None else tuple(node.module.split("."))
                )
                if node.level == 0:
                    imported.append(".".join(module_parts))
                    continue
                retained_package_count = len(package_parts) - (node.level - 1)
                if retained_package_count < 0:
                    raise AssertionError(f"invalid relative import in {path}")
                absolute_parts = (
                    *package_parts[:retained_package_count],
                    *module_parts,
                )
                imported.append(".".join(absolute_parts))
        return tuple(imported)

    @staticmethod
    def is_module_or_descendant(imported: str, module: str, /) -> bool:
        """Return whether one absolute import names a module or its descendant."""
        return imported == module or imported.startswith(f"{module}.")

    def test_packages__do_not_import_outward_or_wire_owners(self) -> None:
        """Both sibling packages depend only on approved inward owners."""
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
        for path in self.phase1_modules():
            for imported in self.imports(path):
                if any(token in imported.split(".") for token in forbidden_tokens):
                    failures.append(f"{path.parent.name}/{path.name}: {imported}")
        assert failures == []

    def test_representations__does_not_import_transformations(self) -> None:
        """Intrinsic representation nodes remain inward of directed edges."""
        forbidden = "ksdft2effmass.operators.transformations"

        failures: list[str] = []
        for path in self.phase1_modules():
            if path.parent.name != "representations":
                continue
            if any(
                self.is_module_or_descendant(imported, forbidden)
                for imported in self.imports(path)
            ):
                failures.append(path.name)
        assert failures == []

    def test_inward_owners__do_not_import_provisional_sibling_packages(self) -> None:
        """Core operators, periodic primitives, and diagnostics remain inward."""
        source = self.python_root() / "src" / "ksdft2effmass"
        representations = source / "operators" / "representations"
        transformations = source / "operators" / "transformations"
        owner_module_directories = (
            source / "operators",
            source / "periodic",
            source / "analysis" / "matrix_field",
            source / "analysis" / "matrix_field" / "diagnostics",
        )
        owner_modules = tuple(
            sorted(
                path
                for directory in owner_module_directories
                for path in directory.iterdir()
                if path.is_file() and path.suffix == ".py"
            )
        )
        forbidden = (
            "ksdft2effmass.operators.representations",
            "ksdft2effmass.operators.transformations",
        )

        failures: list[str] = []
        for path in owner_modules:
            if representations in path.parents or transformations in path.parents:
                continue
            imports = self.imports(path)
            if any(
                self.is_module_or_descendant(imported, prefix)
                for imported in imports
                for prefix in forbidden
            ):
                failures.append(str(path.relative_to(source)))
        assert failures == []

    def test_phase1_modules__are_the_complete_direct_module_inventory(self) -> None:
        """Unreviewed modules or nested subpackages cannot enter Phase 1 implicitly."""
        operators = self.python_root() / "src" / "ksdft2effmass" / "operators"
        packages = (operators / "representations", operators / "transformations")
        actual_modules = tuple(
            sorted(
                path
                for package in packages
                for path in package.iterdir()
                if path.is_file() and path.suffix == ".py"
            )
        )
        nested_directories = tuple(
            sorted(
                path
                for package in packages
                for path in package.iterdir()
                if path.is_dir() and path.name != "__pycache__"
            )
        )

        assert actual_modules == tuple(sorted(self.phase1_modules()))
        assert nested_directories == ()

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
        forbidden = (
            "ksdft2effmass.operators.representations",
            "ksdft2effmass.operators.transformations",
        )

        assert not any(
            self.is_module_or_descendant(imported, prefix)
            for imported in imports
            for prefix in forbidden
        )

    def test_is_module_or_descendant__matches_exact_and_nested_imports(self) -> None:
        """Boundary matching includes descendants but excludes near-name siblings."""
        module = "ksdft2effmass.operators.transformations"

        assert self.is_module_or_descendant(module, module)
        assert self.is_module_or_descendant(f"{module}.identities", module)
        assert not self.is_module_or_descendant(
            "ksdft2effmass.operators.transformations_extra",
            module,
        )
