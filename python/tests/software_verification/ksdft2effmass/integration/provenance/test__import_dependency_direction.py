r"""Software verification of import dependency direction.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This artifact-owned software verification represents the static import graph of the
``ksdft2effmass.provenance`` package. Exact fixed relative-adjacency and per-file
absolute-import mappings are the independent oracles.

Intrinsic and cross-object scope

--------------------------------
The artifact is the AST-visible static import graph of the seven production provenance
modules. Package export identity is owned by ``test__public_api.py``. Each import form
retains its complete module, imported names, and relative level before comparison.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the declared static import inventories. Dynamic and transitive
imports, imports performed by dependencies, runtime service construction, and
semantically equivalent architectures without a static import are excluded. This is not
numerical verification, scientific validation, UQ, provenance truth, execution
validity, portability evidence, or cross-language conformance.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import pytest

REPO_ROOT = Path(__file__).resolve().parents[6]
SOURCE = REPO_ROOT / "python/src/ksdft2effmass/provenance"
pytestmark = pytest.mark.software_verification

EXPECTED_INTERNAL_IMPORTS = {
    "__init__.py": {
        "actions",
        "external_execution",
        "external_tools",
        "records",
        "serialization",
        "tool_observations",
    },
    "actions.py": {"external_execution", "records"},
    "external_execution.py": set(),
    "external_tools.py": set(),
    "records.py": set(),
    "serialization.py": {
        "actions",
        "external_execution",
        "external_tools",
        "records",
        "tool_observations",
    },
    "tool_observations.py": set(),
}

EXPECTED_ABSOLUTE_IMPORTS = {
    "__init__.py": set(),
    "actions.py": {
        "__future__",
        "dataclasses",
        "enum",
        "re",
    },
    "external_execution.py": {
        "__future__",
        "dataclasses",
        "enum",
        "re",
        "unicodedata",
    },
    "external_tools.py": {
        "__future__",
        "dataclasses",
        "enum",
        "re",
        "unicodedata",
    },
    "records.py": {
        "__future__",
        "dataclasses",
        "datetime",
        "enum",
        "re",
        "unicodedata",
    },
    "serialization.py": {
        "__future__",
        "dataclasses",
        "json",
        "typing",
    },
    "tool_observations.py": {
        "__future__",
        "dataclasses",
        "enum",
        "re",
        "unicodedata",
    },
}


@dataclass(frozen=True)
class StaticImportDependency:
    """One AST-visible import statement with its unresolved syntactic coordinates."""

    form: Literal["import", "from"]
    module: str | None
    imported_names: tuple[str, ...]
    relative_level: int


def extract_static_import_dependencies(
    path: Path,
) -> frozenset[StaticImportDependency]:
    """Evidence ID: Owns no identifier; supports SV-PROV-070 and SV-PROV-071.

    Requirement: Static imports retain the syntax needed by both exact dependency
    oracles.

    Method: Parse one Python file and represent each Import alias or complete ImportFrom
    node.

    Oracle: Python AST fields define form, full module, imported names, and relative
    level.

    Acceptance: Return immutable records without root reduction or discarded relative
    forms.

    Interpretation: A mismatch indicates incomplete extraction rather than package
    behavior.

    Limitations: Dynamic and transitive imports and runtime service construction are
    excluded.
    """
    nodes = tuple(ast.walk(ast.parse(path.read_text(encoding="utf-8"))))
    direct_imports = {
        StaticImportDependency("import", alias.name, (), 0)
        for node in nodes
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    from_imports = {
        StaticImportDependency(
            "from",
            node.module,
            tuple(alias.name for alias in node.names),
            node.level,
        )
        for node in nodes
        if isinstance(node, ast.ImportFrom)
    }
    return frozenset(direct_imports | from_imports)


def test_artifact__internal_import_graph__matches_exact_relative_layering(
    tmp_path: Path,
) -> None:
    """Evidence ID: SV-PROV-070

    Requirement: The exact provenance module inventory uses only the accepted level-one
    relative
    imports and the accepted internal adjacency, never absolute internal or ambiguous
    relative forms.

    Method: Extract every production import and each controlled accepted,
    absolute-internal,
    module-less-relative, and higher-level-relative syntax example; then classify each
    controlled prohibited form with the production predicates.

    Oracle: The accepted P2 decomposition fixes EXPECTED_INTERNAL_IMPORTS, permits only
    ``from .module import name`` for internal edges, and fixes each controlled AST form
    and its prohibited category exactly.

    Acceptance: Filenames and adjacency match exactly; production has no ambiguous
    relative or
    absolute internal records; every controlled import equals its exact immutable
    record, and each prohibited record appears in its exact prohibited classification.

    Interpretation: Failure identifies source inventory drift, an unauthorized internal
    edge or form,
    discarded import syntax, incorrect extraction, or incorrect classification.

    Limitations: Dynamic imports, call architecture, runtime behavior, and package
    export identity
    are not assessed.
    """
    paths = {path.name: path for path in SOURCE.glob("*.py")}
    assert set(paths) == set(EXPECTED_INTERNAL_IMPORTS)

    dependencies_by_file = {
        name: extract_static_import_dependencies(path) for name, path in paths.items()
    }
    observed_internal = {
        name: {
            dependency.module
            for dependency in dependencies
            if dependency.form == "from"
            and dependency.relative_level == 1
            and dependency.module is not None
        }
        for name, dependencies in dependencies_by_file.items()
    }
    ambiguous_relative = {
        name: {
            dependency
            for dependency in dependencies
            if dependency.relative_level > 0
            and not (
                dependency.form == "from"
                and dependency.relative_level == 1
                and dependency.module is not None
            )
        }
        for name, dependencies in dependencies_by_file.items()
    }
    absolute_internal = {
        name: {
            dependency
            for dependency in dependencies
            if dependency.relative_level == 0
            and dependency.module is not None
            and (
                dependency.module == "ksdft2effmass.provenance"
                or dependency.module.startswith("ksdft2effmass.provenance.")
            )
        }
        for name, dependencies in dependencies_by_file.items()
    }

    assert observed_internal == EXPECTED_INTERNAL_IMPORTS
    assert all(not dependencies for dependencies in ambiguous_relative.values())
    assert all(not dependencies for dependencies in absolute_internal.values())

    accepted_path = tmp_path / "accepted_level_one.py"
    accepted_path.write_text(
        "from .records import ArtifactIdentity\n", encoding="utf-8"
    )
    assert extract_static_import_dependencies(accepted_path) == frozenset(
        {
            StaticImportDependency(
                "from",
                "records",
                ("ArtifactIdentity",),
                1,
            )
        }
    )

    absolute_path = tmp_path / "absolute_internal.py"
    absolute_path.write_text(
        "from ksdft2effmass.provenance.records import ArtifactIdentity\n",
        encoding="utf-8",
    )
    absolute_dependencies = extract_static_import_dependencies(absolute_path)
    assert absolute_dependencies == frozenset(
        {
            StaticImportDependency(
                "from",
                "ksdft2effmass.provenance.records",
                ("ArtifactIdentity",),
                0,
            )
        }
    )
    absolute_classification = {
        dependency
        for dependency in absolute_dependencies
        if dependency.relative_level == 0
        and dependency.module is not None
        and (
            dependency.module == "ksdft2effmass.provenance"
            or dependency.module.startswith("ksdft2effmass.provenance.")
        )
    }
    assert absolute_classification == set(absolute_dependencies)

    moduleless_path = tmp_path / "moduleless_relative.py"
    moduleless_path.write_text("from . import records\n", encoding="utf-8")
    moduleless_dependencies = extract_static_import_dependencies(moduleless_path)
    assert moduleless_dependencies == frozenset(
        {
            StaticImportDependency(
                "from",
                None,
                ("records",),
                1,
            )
        }
    )
    moduleless_classification = {
        dependency
        for dependency in moduleless_dependencies
        if dependency.relative_level > 0
        and not (
            dependency.form == "from"
            and dependency.relative_level == 1
            and dependency.module is not None
        )
    }
    assert moduleless_classification == set(moduleless_dependencies)

    higher_level_path = tmp_path / "higher_level_relative.py"
    higher_level_path.write_text("from ..provenance import records\n", encoding="utf-8")
    higher_level_dependencies = extract_static_import_dependencies(higher_level_path)
    assert higher_level_dependencies == frozenset(
        {
            StaticImportDependency(
                "from",
                "provenance",
                ("records",),
                2,
            )
        }
    )
    higher_level_classification = {
        dependency
        for dependency in higher_level_dependencies
        if dependency.relative_level > 0
        and not (
            dependency.form == "from"
            and dependency.relative_level == 1
            and dependency.module is not None
        )
    }
    assert higher_level_classification == set(higher_level_dependencies)


def test_artifact__absolute_import_inventory__matches_exact_dependency_boundary(
    tmp_path: Path,
) -> None:
    """Evidence ID: SV-PROV-071

    Requirement: Every provenance production module has exactly its accepted static
    absolute-import
    modules and no undeclared standard-library, project-package, or third-party edge.

    Method: Compare full AST module names per file and exercise controlled undeclared
    imports
    spanning standard-library, project, scheduler, plugin, and third-party packages.

    Oracle: The accepted P2 architecture and current source decomposition fix
    EXPECTED_ABSOLUTE_IMPORTS independently of production constants and source prose.

    Acceptance: The per-file mapping equals the fixed mapping exactly, and the
    controlled source
    produces exactly the fixed set of six undeclared full-module names.

    Interpretation: Failure indicates dependency-boundary drift or extraction that
    truncates a module
    path; it does not establish that an imported dependency executes.

    Limitations: Dynamic and transitive imports, dependency internals, runtime service
    construction,
    equivalent architectures without static imports, and scientific behavior are
    excluded.
    """
    paths = {path.name: path for path in SOURCE.glob("*.py")}
    assert set(paths) == set(EXPECTED_ABSOLUTE_IMPORTS)
    observed_absolute = {
        name: {
            dependency.module
            for dependency in extract_static_import_dependencies(path)
            if dependency.relative_level == 0 and dependency.module is not None
        }
        for name, path in paths.items()
    }
    assert observed_absolute == EXPECTED_ABSOLUTE_IMPORTS

    undeclared_path = tmp_path / "undeclared_absolute_imports.py"
    undeclared_path.write_text(
        "\n".join(
            (
                "import snakes",
                "import subprocess",
                "from ksdft2effmass.workflows.cpn import workflow",
                "from ksdft2effmass.backends import registry",
                "import scheduler.client",
                "from pluggy import PluginManager",
            )
        )
        + "\n",
        encoding="utf-8",
    )
    undeclared_modules = {
        dependency.module
        for dependency in extract_static_import_dependencies(undeclared_path)
        if dependency.relative_level == 0 and dependency.module is not None
    }
    assert undeclared_modules == {
        "ksdft2effmass.backends",
        "ksdft2effmass.workflows.cpn",
        "pluggy",
        "scheduler.client",
        "snakes",
        "subprocess",
    }
