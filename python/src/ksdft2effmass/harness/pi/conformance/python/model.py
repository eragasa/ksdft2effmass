"""Deeply immutable AST-free facts for parsed Python evidence modules."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PythonParameterInventoryKind(Enum):
    """Neutral static shape of one parameter case inventory."""

    INLINE = "inline"
    NAMED = "named"
    NON_LITERAL = "non_literal"
    IMPORTED = "imported"
    UNRESOLVED = "unresolved"
    MULTIPLE_ASSIGNMENTS = "multiple_assignments"
    COMPLEX_ASSIGNMENT = "complex_assignment"
    ASSIGNED_AFTER_DECORATOR = "assigned_after_decorator"
    NON_LITERAL_ASSIGNMENT = "non_literal_assignment"
    STARRED_EXPANSION = "starred_expansion"


class PythonParameterMutationKind(Enum):
    """Neutral statically observed mutation of a named inventory."""

    REASSIGNMENT = "reassignment"
    AUGMENTED_ASSIGNMENT = "augmented_assignment"
    METHOD_CALL = "method_call"
    SUBSCRIPT_ASSIGNMENT = "subscript_assignment"


@dataclass(frozen=True, slots=True)
class PythonParameterMutationFact:
    """One immutable named-inventory mutation fact."""

    kind: PythonParameterMutationKind
    method_name: str | None = None


@dataclass(frozen=True, slots=True)
class PythonParameterCaseFact:
    """Neutral immutable syntax facts for one parameter case expression."""

    is_param_call: bool
    is_direct_pytest_param: bool
    id_keyword_count: int
    literal_id: str | None


@dataclass(frozen=True, slots=True)
class PythonParameterizationFact:
    """Neutral immutable syntax facts for one ``parametrize`` decorator."""

    inventory_kind: PythonParameterInventoryKind
    inventory_name: str | None
    cases: tuple[PythonParameterCaseFact, ...]
    decorator_ids_present: bool
    decorator_ids_are_literal_sequence: bool
    decorator_ids_are_literal_strings: bool
    decorator_ids: tuple[str, ...]
    mutations: tuple[PythonParameterMutationFact, ...]


@dataclass(frozen=True, slots=True)
class PythonCallableFact:
    """Neutral syntax facts for one module function or direct class method."""

    name: str
    line: int
    owner_class_name: str | None
    decorator_names: tuple[str, ...]
    has_documentation: bool

    @property
    def is_test(self) -> bool:
        """Whether the callable uses pytest test-name syntax."""
        return self.name.startswith("test_")


@dataclass(frozen=True, slots=True)
class PythonTestFunctionFact:
    """Immutable syntax-derived facts for one top-level function."""

    name: str
    line: int
    doc: str
    calls_sut: bool
    indexes_sut: bool
    circular_member_lookup: bool
    has_loop: bool
    parameterizations: tuple[PythonParameterizationFact, ...]

    @property
    def is_test(self) -> bool:
        """Whether this function is an evidence-owning test."""
        return self.name.startswith("test_")


@dataclass(frozen=True, slots=True)
class PythonTestModuleModel:
    """One immutable AST-free model derived from exactly one source parse."""

    path: str
    source: str
    source_bytes: bytes
    source_sha256: str
    source_byte_count: int
    module_doc: str | None
    functions: tuple[PythonTestFunctionFact, ...]
    evidence_class: str
    evidence_profile: str
    ownership_kind: str
    owner_subject: str
    sut_assignment_name: str | None
    imported_names: tuple[str, ...]
    equality_fields: tuple[str, ...] | None
    frozen_fields: tuple[str, ...] | None
    numeric_export_count_assertion_lines: tuple[int, ...]
    callables: tuple[PythonCallableFact, ...]
    any_reference_lines: tuple[int, ...]
    cast_any_lines: tuple[int, ...]
    object_annotation_lines: tuple[int, ...]
    erased_container_annotation_lines: tuple[int, ...]

    @property
    def function_names(self) -> tuple[str, ...]:
        """Top-level function names in source order."""
        return tuple(function.name for function in self.functions)


@dataclass(frozen=True, slots=True)
class _PythonTestModuleParseFailure:
    """One deterministic decode or syntax failure in an explicit corpus."""

    path: str
    message: str


@dataclass(frozen=True, slots=True)
class _PythonTestModuleCorpus:
    """One cohesive immutable corpus built from explicit source snapshots."""

    models: tuple[PythonTestModuleModel, ...]
    failures: tuple[_PythonTestModuleParseFailure, ...]

    def model_for(self, path: str) -> PythonTestModuleModel | None:
        """Return the model for ``path`` without exposing mutable indexing state."""
        return next((model for model in self.models if model.path == path), None)
