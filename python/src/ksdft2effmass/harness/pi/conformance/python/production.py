"""Neutral explicit-input syntax facts for Python production source.

The records in this module represent caller-supplied source bytes, exact source
identity, lexical definitions, imports, calls, and ``__all__`` syntax.  The
:class:`PythonProductionSourceInspector` parses only supplied bytes and performs no
filesystem discovery, current-directory lookup, policy classification, source repair,
or runtime inference.  Its descriptive implementation classes are intentionally not
re-exported as supported package APIs.

A successful parse is software structure evidence only.  It does not establish
runtime behavior, architectural conformance, support status, ownership quality,
numerical verification, scientific validation, uncertainty quantification, or human
acceptance.
"""

from __future__ import annotations

import ast
import hashlib
import unicodedata
from dataclasses import dataclass
from enum import StrEnum
from pathlib import PurePosixPath
from typing import ClassVar


class PythonProductionScopeKind(StrEnum):
    """Closed lexical owner kinds represented by production-source facts."""

    CLASS = "class"
    CALLABLE = "callable"


class PythonProductionCallableKind(StrEnum):
    """Closed callable-definition syntax kinds."""

    FUNCTION = "function"
    ASYNC_FUNCTION = "async_function"
    LAMBDA = "lambda"


class PythonProductionContextKind(StrEnum):
    """Closed neutral statement contexts that may affect execution."""

    IF_BODY = "if_body"
    IF_ELSE = "if_else"
    TRY_BODY = "try_body"
    TRY_HANDLER = "try_handler"
    TRY_ELSE = "try_else"
    TRY_FINALLY = "try_finally"
    LOOP_BODY = "loop_body"
    LOOP_ELSE = "loop_else"
    WITH_BODY = "with_body"
    MATCH_CASE = "match_case"
    COMPREHENSION = "comprehension"


class PythonProductionImportKind(StrEnum):
    """Closed import statement syntax kinds."""

    IMPORT = "import"
    FROM_IMPORT = "from_import"


class PythonProductionAllOperation(StrEnum):
    """Closed module ``__all__`` syntax operations."""

    ASSIGN = "assign"
    ANNOTATED_ASSIGN = "annotated_assign"
    AUGMENTED_ASSIGN = "augmented_assign"
    MUTATION = "mutation"
    DELETE = "delete"


class PythonProductionAugmentedOperator(StrEnum):
    """Closed Python augmented-assignment operator syntax kinds."""

    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    MATRIX_MULTIPLY = "matrix_multiply"
    DIVIDE = "divide"
    FLOOR_DIVIDE = "floor_divide"
    MODULO = "modulo"
    POWER = "power"
    LEFT_SHIFT = "left_shift"
    RIGHT_SHIFT = "right_shift"
    BIT_OR = "bit_or"
    BIT_XOR = "bit_xor"
    BIT_AND = "bit_and"


class PythonProductionLiteralSequenceKind(StrEnum):
    """Closed literal sequence forms retained for bounded export resolution."""

    LIST = "list"
    TUPLE = "tuple"


class PythonProductionAllResolution(StrEnum):
    """Closed effective module ``__all__`` syntax states."""

    ABSENT = "absent"
    LITERAL = "literal"
    DYNAMIC = "dynamic"


class PythonProductionFailureKind(StrEnum):
    """Closed deterministic source failure kinds."""

    READ = "read"
    DECODE = "decode"
    SYNTAX = "syntax"


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonProductionSourceProfile:
    """Identify the unsupported sibling production-source fact profile.

    Parameters
    ----------
    subject_family_identity
        Exact sibling subject family.  It is distinct from the accepted
        ``python.test-evidence`` family.
    profile_identity
        Exact neutral syntax-fact profile identity.
    profile_version
        Exact profile behavior version.
    """

    SUBJECT_FAMILY_IDENTITY: ClassVar[str] = "python.production-source"
    PROFILE_IDENTITY: ClassVar[str] = "ksdft2effmass.python.production-facts"
    PROFILE_VERSION: ClassVar[str] = "1"

    subject_family_identity: str = SUBJECT_FAMILY_IDENTITY
    profile_identity: str = PROFILE_IDENTITY
    profile_version: str = PROFILE_VERSION

    def __post_init__(self) -> None:
        """Require the exact implemented profile identity triple."""
        if any(
            type(value) is not str
            for value in (
                self.subject_family_identity,
                self.profile_identity,
                self.profile_version,
            )
        ):
            raise TypeError("profile identities must be built-in str values")
        expected = (
            self.SUBJECT_FAMILY_IDENTITY,
            self.PROFILE_IDENTITY,
            self.PROFILE_VERSION,
        )
        if (
            self.subject_family_identity,
            self.profile_identity,
            self.profile_version,
        ) != expected:
            raise ValueError("production-source profile identity is unsupported")


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonProductionSource:
    """Represent one exact caller-supplied Python module input.

    Parameters
    ----------
    input_identity
        Nonempty normalized single-line identity supplied by the caller.  Identities
        and paths may repeat; every tuple entry is inspected and retained.
    path
        Exact normalized repository-relative POSIX diagnostic path.
    payload, read_error
        Exactly one byte payload or caller-supplied deterministic read failure.
    """

    input_identity: str
    path: PurePosixPath
    payload: bytes | None
    read_error: str | None

    def __post_init__(self) -> None:
        """Enforce intrinsic identity, path, and payload/failure invariants."""
        self._require_text(self.input_identity, "input_identity")
        if type(self.path) is not PurePosixPath:
            raise TypeError("path must be PurePosixPath")
        rendered = self.path.as_posix()
        if (
            rendered in {"", "."}
            or self.path.is_absolute()
            or ".." in self.path.parts
            or "\\" in rendered
            or unicodedata.normalize("NFC", rendered) != rendered
        ):
            raise ValueError("path must be a normalized repository-relative POSIX path")
        if self.payload is not None and type(self.payload) is not bytes:
            raise TypeError("payload must be bytes or None")
        if self.read_error is not None:
            self._require_text(self.read_error, "read_error")
        if (self.payload is None) == (self.read_error is None):
            raise ValueError("exactly one payload or read_error is required")

    @classmethod
    def from_payload(
        cls, *, input_identity: str, path: PurePosixPath, payload: bytes
    ) -> PythonProductionSource:
        """Construct one successful explicit byte input.

        Parameters
        ----------
        input_identity
            Caller-supplied input identity.
        path
            Exact diagnostic path.
        payload
            Exact bytes to inspect.

        Returns
        -------
        PythonProductionSource
            Immutable explicit source input.
        """
        if type(payload) is not bytes:
            raise TypeError("payload must be bytes")
        return cls(
            input_identity=input_identity,
            path=path,
            payload=payload,
            read_error=None,
        )

    @staticmethod
    def _require_text(value: str, name: str) -> None:
        """Require normalized nonempty single-line built-in text."""
        if type(value) is not str:
            raise TypeError(f"{name} must be a built-in str")
        if (
            not value
            or "\n" in value
            or "\r" in value
            or unicodedata.normalize("NFC", value) != value
        ):
            raise ValueError(f"{name} must be normalized nonempty single-line text")


@dataclass(frozen=True, slots=True, order=True, kw_only=True)
class PythonProductionLocation:
    """Represent one exact AST source span.

    Parameters
    ----------
    line, column
        One-based line and zero-based UTF-8 byte column of the first token.
    end_line, end_column
        One-based line and zero-based UTF-8 byte column immediately after the span.
    """

    line: int
    column: int
    end_line: int
    end_column: int

    def __post_init__(self) -> None:
        """Require positive lines and nonnegative columns in source order."""
        values = (self.line, self.column, self.end_line, self.end_column)
        if any(type(value) is not int for value in values):
            raise TypeError("source location values must be built-in int values")
        if self.line < 1 or self.end_line < self.line:
            raise ValueError("source lines must be positive and ordered")
        if self.column < 0 or self.end_column < 0:
            raise ValueError("source columns must be nonnegative")
        if self.end_line == self.line and self.end_column < self.column:
            raise ValueError("same-line source columns must be ordered")


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonProductionLexicalOwner:
    """Represent one enclosing class or callable.

    Parameters
    ----------
    name
        Syntactic owner name, including a deterministic location name for lambdas.
    qualified_name
        Dot-separated lexical qualification within the module.
    kind
        Whether the owner is a class or callable.
    """

    name: str
    qualified_name: str
    kind: PythonProductionScopeKind

    def __post_init__(self) -> None:
        """Require nonempty names and one exact lexical owner kind."""
        if type(self.name) is not str or not self.name:
            raise ValueError("lexical owner name must be nonempty built-in text")
        if type(self.qualified_name) is not str or not self.qualified_name:
            raise ValueError("qualified_name must be nonempty built-in text")
        if type(self.kind) is not PythonProductionScopeKind:
            raise TypeError("kind must be PythonProductionScopeKind")


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonProductionExecutionContext:
    """Represent one neutral enclosing execution context.

    Parameters
    ----------
    kind
        Syntactic branch or body kind.
    expression
        Canonical ``ast.unparse`` text for the controlling expression when present.
    location
        Source span of the controlling syntax node.
    """

    kind: PythonProductionContextKind
    expression: str | None
    location: PythonProductionLocation

    def __post_init__(self) -> None:
        """Require exact context, expression, and location types."""
        if type(self.kind) is not PythonProductionContextKind:
            raise TypeError("kind must be PythonProductionContextKind")
        if self.expression is not None and type(self.expression) is not str:
            raise TypeError("expression must be built-in str or None")
        if type(self.location) is not PythonProductionLocation:
            raise TypeError("location must be PythonProductionLocation")


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonProductionClassFact:
    """Represent one class definition.

    Parameters
    ----------
    name, qualified_name
        Syntactic name and dot-separated lexical qualification.
    owners
        Outer lexical owners, in outer-to-inner order.
    location
        Exact definition span.
    """

    name: str
    qualified_name: str
    owners: tuple[PythonProductionLexicalOwner, ...]
    location: PythonProductionLocation

    def __post_init__(self) -> None:
        """Require complete class naming, owners, and location."""
        if type(self.name) is not str or not self.name:
            raise ValueError("class name must be nonempty built-in text")
        if type(self.qualified_name) is not str or not self.qualified_name:
            raise ValueError("qualified_name must be nonempty built-in text")
        if type(self.owners) is not tuple or any(
            type(owner) is not PythonProductionLexicalOwner for owner in self.owners
        ):
            raise TypeError("owners must contain PythonProductionLexicalOwner values")
        if type(self.location) is not PythonProductionLocation:
            raise TypeError("location must be PythonProductionLocation")

    @property
    def sort_key(self) -> tuple[int, int, str]:
        """Return canonical source-order sorting state."""
        return (self.location.line, self.location.column, self.qualified_name)


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonProductionCallableFact:
    """Represent one named or lambda callable definition.

    Parameters
    ----------
    name, qualified_name
        Syntactic name and dot-separated lexical qualification.
    kind
        Function, asynchronous function, or lambda syntax.
    owners
        Outer lexical owners, distinguishing module, class, and nested callables.
    location
        Exact definition span.
    """

    name: str
    qualified_name: str
    kind: PythonProductionCallableKind
    owners: tuple[PythonProductionLexicalOwner, ...]
    location: PythonProductionLocation

    def __post_init__(self) -> None:
        """Require complete callable naming, kind, owners, and location."""
        if type(self.name) is not str or not self.name:
            raise ValueError("callable name must be nonempty built-in text")
        if type(self.qualified_name) is not str or not self.qualified_name:
            raise ValueError("qualified_name must be nonempty built-in text")
        if type(self.kind) is not PythonProductionCallableKind:
            raise TypeError("kind must be PythonProductionCallableKind")
        if type(self.owners) is not tuple or any(
            type(owner) is not PythonProductionLexicalOwner for owner in self.owners
        ):
            raise TypeError("owners must contain PythonProductionLexicalOwner values")
        if type(self.location) is not PythonProductionLocation:
            raise TypeError("location must be PythonProductionLocation")

    @property
    def sort_key(self) -> tuple[int, int, str]:
        """Return canonical source-order sorting state."""
        return (self.location.line, self.location.column, self.qualified_name)


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonProductionImportFact:
    """Represent one imported name edge with exact lexical attribution.

    Parameters
    ----------
    kind
        ``import`` or ``from ... import ...`` syntax.
    module
        Imported module text, or ``None`` for a module-less relative from-import.
    name
        Imported module for plain imports or imported member for from-imports.
    alias
        Explicit ``as`` alias when present.
    relative_level
        Number of leading dots for from-imports; zero for plain imports.
    owners
        Enclosing lexical owners.  A callable owner identifies a local import.
    contexts
        Outer-to-inner neutral conditional or guarded contexts.
    location
        Exact span of this imported name and its optional alias, not the enclosing
        import statement span.
    """

    kind: PythonProductionImportKind
    module: str | None
    name: str
    alias: str | None
    relative_level: int
    owners: tuple[PythonProductionLexicalOwner, ...]
    contexts: tuple[PythonProductionExecutionContext, ...]
    location: PythonProductionLocation

    def __post_init__(self) -> None:
        """Require exact import syntax, attribution, and relative level."""
        if type(self.kind) is not PythonProductionImportKind:
            raise TypeError("kind must be PythonProductionImportKind")
        if self.module is not None and type(self.module) is not str:
            raise TypeError("module must be built-in str or None")
        if type(self.name) is not str or not self.name:
            raise ValueError("import name must be nonempty built-in text")
        if self.alias is not None and type(self.alias) is not str:
            raise TypeError("alias must be built-in str or None")
        if type(self.relative_level) is not int:
            raise TypeError("relative_level must be a built-in int")
        if self.relative_level < 0:
            raise ValueError("relative_level must be nonnegative")
        if self.kind is PythonProductionImportKind.IMPORT and (
            self.module != self.name or self.relative_level != 0
        ):
            raise ValueError("plain import module/name and relative level disagree")
        if type(self.owners) is not tuple or any(
            type(owner) is not PythonProductionLexicalOwner for owner in self.owners
        ):
            raise TypeError("owners must contain PythonProductionLexicalOwner values")
        if type(self.contexts) is not tuple or any(
            type(context) is not PythonProductionExecutionContext
            for context in self.contexts
        ):
            raise TypeError("contexts must contain execution-context values")
        if type(self.location) is not PythonProductionLocation:
            raise TypeError("location must be PythonProductionLocation")

    @property
    def sort_key(self) -> tuple[int, int, str, str, str]:
        """Return canonical source-order and alias-order sorting state."""
        return (
            self.location.line,
            self.location.column,
            self.kind.value,
            self.name,
            self.alias or "",
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonProductionCallFact:
    """Represent one call site without resolving runtime dispatch.

    Parameters
    ----------
    callee_expression
        Canonical syntactic expression used as the callable.
    receiver_expression
        Canonical receiver expression for attribute calls, otherwise ``None``.
    callee_name
        Attribute or direct name when syntactically available, otherwise ``None``.
    owners
        Enclosing lexical owners; the innermost callable is the syntactic caller.
    contexts
        Outer-to-inner neutral execution contexts.
    location
        Exact call-expression span.
    """

    callee_expression: str
    receiver_expression: str | None
    callee_name: str | None
    owners: tuple[PythonProductionLexicalOwner, ...]
    contexts: tuple[PythonProductionExecutionContext, ...]
    location: PythonProductionLocation

    def __post_init__(self) -> None:
        """Require exact syntactic call text, attribution, and location."""
        if type(self.callee_expression) is not str or not self.callee_expression:
            raise ValueError("callee_expression must be nonempty built-in text")
        if (
            self.receiver_expression is not None
            and type(self.receiver_expression) is not str
        ):
            raise TypeError("receiver_expression must be built-in str or None")
        if self.callee_name is not None and type(self.callee_name) is not str:
            raise TypeError("callee_name must be built-in str or None")
        if type(self.owners) is not tuple or any(
            type(owner) is not PythonProductionLexicalOwner for owner in self.owners
        ):
            raise TypeError("owners must contain PythonProductionLexicalOwner values")
        if type(self.contexts) is not tuple or any(
            type(context) is not PythonProductionExecutionContext
            for context in self.contexts
        ):
            raise TypeError("contexts must contain execution-context values")
        if type(self.location) is not PythonProductionLocation:
            raise TypeError("location must be PythonProductionLocation")

    @property
    def sort_key(self) -> tuple[int, int, str]:
        """Return canonical source-order sorting state."""
        return (self.location.line, self.location.column, self.callee_expression)


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonProductionAllSyntaxFact:
    """Represent one raw module-level ``__all__`` operation.

    Parameters
    ----------
    operation
        Assignment, augmented assignment, mutation, or deletion syntax.
    raw_expression
        Canonical syntax text for the value or mutation; ``None`` for deletion.
    literal_names
        Exact ordered string names for a list or tuple literal, otherwise ``None``.
    literal_sequence_kind
        Exact list or tuple literal form when ``literal_names`` is present.
    augmented_operator
        Exact closed operator kind only for augmented assignment.
    contexts
        Neutral enclosing contexts.  Contextual operations make the effective state
        dynamic because runtime branch selection is not inferred.
    location
        Exact operation span.
    """

    operation: PythonProductionAllOperation
    raw_expression: str | None
    literal_names: tuple[str, ...] | None
    literal_sequence_kind: PythonProductionLiteralSequenceKind | None
    augmented_operator: PythonProductionAugmentedOperator | None
    contexts: tuple[PythonProductionExecutionContext, ...]
    location: PythonProductionLocation

    def __post_init__(self) -> None:
        """Require exact export operation, literal, context, and location types."""
        if type(self.operation) is not PythonProductionAllOperation:
            raise TypeError("operation must be PythonProductionAllOperation")
        if self.raw_expression is not None and type(self.raw_expression) is not str:
            raise TypeError("raw_expression must be built-in str or None")
        if self.literal_names is not None and (
            type(self.literal_names) is not tuple
            or any(type(name) is not str for name in self.literal_names)
        ):
            raise TypeError("literal_names must contain built-in str values")
        if (self.literal_names is None) != (self.literal_sequence_kind is None):
            raise ValueError("literal names and sequence kind must be present together")
        if (
            self.literal_sequence_kind is not None
            and type(self.literal_sequence_kind)
            is not PythonProductionLiteralSequenceKind
        ):
            raise TypeError("literal_sequence_kind has the wrong type")
        if (self.operation is PythonProductionAllOperation.AUGMENTED_ASSIGN) != (
            self.augmented_operator is not None
        ):
            raise ValueError("only augmented assignment requires an exact operator")
        if (
            self.augmented_operator is not None
            and type(self.augmented_operator) is not PythonProductionAugmentedOperator
        ):
            raise TypeError("augmented_operator has the wrong type")
        if type(self.contexts) is not tuple or any(
            type(context) is not PythonProductionExecutionContext
            for context in self.contexts
        ):
            raise TypeError("contexts must contain execution-context values")
        if type(self.location) is not PythonProductionLocation:
            raise TypeError("location must be PythonProductionLocation")

    @property
    def sort_key(self) -> tuple[int, int, str]:
        """Return canonical source-order sorting state."""
        return (self.location.line, self.location.column, self.operation.value)


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonProductionModuleFacts:
    """Represent all neutral facts from one successfully parsed module.

    Parameters
    ----------
    classes, callables, imports, calls, all_syntax
        Canonical source-ordered immutable syntax facts.
    effective_all_resolution
        ``absent``, exactly resolved ``literal``, or unresolved ``dynamic`` state.
    effective_all_names
        Exact effective literal names only when resolution is ``literal``.
    """

    classes: tuple[PythonProductionClassFact, ...]
    callables: tuple[PythonProductionCallableFact, ...]
    imports: tuple[PythonProductionImportFact, ...]
    calls: tuple[PythonProductionCallFact, ...]
    all_syntax: tuple[PythonProductionAllSyntaxFact, ...]
    effective_all_resolution: PythonProductionAllResolution
    effective_all_names: tuple[str, ...] | None

    def __post_init__(self) -> None:
        """Require canonical fact ordering and consistent effective export state."""
        typed_facts = (
            ("classes", self.classes, PythonProductionClassFact),
            ("callables", self.callables, PythonProductionCallableFact),
            ("imports", self.imports, PythonProductionImportFact),
            ("calls", self.calls, PythonProductionCallFact),
            ("all_syntax", self.all_syntax, PythonProductionAllSyntaxFact),
        )
        for name, facts, expected_type in typed_facts:
            if type(facts) is not tuple or any(
                type(fact) is not expected_type for fact in facts
            ):
                raise TypeError(f"{name} contains an invalid fact type")
            if facts != tuple(sorted(facts, key=lambda fact: fact.sort_key)):
                raise ValueError(f"{name} must be in canonical source order")
        if type(self.effective_all_resolution) is not PythonProductionAllResolution:
            raise TypeError("effective_all_resolution has the wrong type")
        if (self.effective_all_resolution is PythonProductionAllResolution.LITERAL) != (
            self.effective_all_names is not None
        ):
            raise ValueError(
                "effective __all__ names require exactly literal resolution"
            )
        if self.effective_all_names is not None and (
            type(self.effective_all_names) is not tuple
            or any(type(name) is not str for name in self.effective_all_names)
        ):
            raise TypeError("effective_all_names must contain built-in str values")


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonProductionSourceFailure:
    """Represent one deterministic read, UTF-8 decode, or syntax failure.

    Parameters
    ----------
    kind
        Failure stage.
    message
        Deterministic caller or parser diagnostic.
    line, column
        Optional one-based line and zero-based column for syntax failures.
    """

    kind: PythonProductionFailureKind
    message: str
    line: int | None
    column: int | None

    def __post_init__(self) -> None:
        """Require one exact failure kind, message, and optional source position."""
        if type(self.kind) is not PythonProductionFailureKind:
            raise TypeError("kind must be PythonProductionFailureKind")
        if type(self.message) is not str or not self.message:
            raise ValueError("message must be nonempty built-in text")
        if self.line is not None and (type(self.line) is not int or self.line < 1):
            raise ValueError("line must be a positive built-in int or None")
        if self.column is not None and (
            type(self.column) is not int or self.column < 0
        ):
            raise ValueError("column must be a nonnegative built-in int or None")
        if self.kind is not PythonProductionFailureKind.SYNTAX and (
            self.line is not None or self.column is not None
        ):
            raise ValueError("only syntax failures may have a source position")


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonProductionModuleInspection:
    """Represent the complete outcome for one supplied module entry.

    Parameters
    ----------
    input_identity, path
        Exact caller identity and diagnostic path.
    source_sha256, source_byte_count
        SHA-256 and byte count for supplied bytes, or ``None`` for a read failure.
    facts, failure
        Exactly one successful neutral fact set or deterministic failure.
    """

    input_identity: str
    path: PurePosixPath
    source_sha256: str | None
    source_byte_count: int | None
    facts: PythonProductionModuleFacts | None
    failure: PythonProductionSourceFailure | None

    def __post_init__(self) -> None:
        """Require exactly one outcome and bytes identity except on read failure."""
        if (
            type(self.input_identity) is not str
            or not self.input_identity
            or "\n" in self.input_identity
            or "\r" in self.input_identity
            or unicodedata.normalize("NFC", self.input_identity) != self.input_identity
        ):
            raise ValueError(
                "input_identity must be normalized nonempty single-line text"
            )
        if type(self.path) is not PurePosixPath:
            raise TypeError("path must be PurePosixPath")
        rendered = self.path.as_posix()
        if (
            rendered in {"", "."}
            or self.path.is_absolute()
            or ".." in self.path.parts
            or "\\" in rendered
            or unicodedata.normalize("NFC", rendered) != rendered
        ):
            raise ValueError("path must be a normalized repository-relative POSIX path")
        if (
            self.facts is not None
            and type(self.facts) is not PythonProductionModuleFacts
        ):
            raise TypeError("facts must be PythonProductionModuleFacts or None")
        if (
            self.failure is not None
            and type(self.failure) is not PythonProductionSourceFailure
        ):
            raise TypeError("failure must be PythonProductionSourceFailure or None")
        if (self.facts is None) == (self.failure is None):
            raise ValueError("exactly one facts or failure outcome is required")
        has_identity = (
            self.source_sha256 is not None and self.source_byte_count is not None
        )
        is_read_failure = (
            self.failure is not None
            and self.failure.kind is PythonProductionFailureKind.READ
        )
        if has_identity == is_read_failure:
            raise ValueError("only read failures omit source byte identity")
        if self.source_sha256 is not None and (
            len(self.source_sha256) != 64
            or any(
                character not in "0123456789abcdef" for character in self.source_sha256
            )
        ):
            raise ValueError("source_sha256 must be lowercase SHA-256 hexadecimal")
        if self.source_byte_count is not None and (
            type(self.source_byte_count) is not int or self.source_byte_count < 0
        ):
            raise ValueError("source_byte_count must be a nonnegative built-in int")

    @property
    def sort_key(self) -> tuple[str, str, str, int, str, str, int, int]:
        """Return complete canonical identity ordering while retaining duplicates."""
        failure_kind = "" if self.failure is None else self.failure.kind.value
        failure_message = "" if self.failure is None else self.failure.message
        failure_line = (
            -1
            if self.failure is None or self.failure.line is None
            else self.failure.line
        )
        failure_column = (
            -1
            if self.failure is None or self.failure.column is None
            else self.failure.column
        )
        return (
            self.path.as_posix(),
            self.input_identity,
            self.source_sha256 or "",
            -1 if self.source_byte_count is None else self.source_byte_count,
            failure_kind,
            failure_message,
            failure_line,
            failure_column,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonProductionInspectionResult:
    """Represent canonical outcomes for every supplied module.

    Parameters
    ----------
    profile
        Exact production-source profile used for parsing.
    modules
        Canonically ordered outcomes.  Duplicate paths or identities remain distinct
        tuple entries and are never collapsed.
    """

    profile: PythonProductionSourceProfile
    modules: tuple[PythonProductionModuleInspection, ...]

    def __post_init__(self) -> None:
        """Require the exact profile, nonempty result, and canonical module order."""
        if type(self.profile) is not PythonProductionSourceProfile:
            raise TypeError("profile must be PythonProductionSourceProfile")
        if type(self.modules) is not tuple:
            raise TypeError("modules must be a tuple")
        if not self.modules:
            raise ValueError("modules must be nonempty")
        if any(
            type(module) is not PythonProductionModuleInspection
            for module in self.modules
        ):
            raise TypeError("modules must contain module-inspection values")
        if self.modules != tuple(sorted(self.modules, key=lambda item: item.sort_key)):
            raise ValueError("modules must be in canonical order")


class PythonProductionSourceInspector:
    """Parse explicit Python bytes into immutable neutral syntax facts.

    The inspector retains no AST, reads no paths, discovers no modules, and applies no
    architecture policy. Canonical ordering is by diagnostic path, caller input
    identity, byte identity/count, and complete represented failure kind, message, and
    source position; exact duplicates remain repeated.
    """

    __slots__ = ()

    def execute(
        self,
        profile: PythonProductionSourceProfile,
        sources: tuple[PythonProductionSource, ...],
    ) -> PythonProductionInspectionResult:
        """Inspect every explicitly supplied module.

        Parameters
        ----------
        profile
            Exact sibling production-source fact profile.
        sources
            Nonempty tuple of explicit source or read-failure entries.

        Returns
        -------
        PythonProductionInspectionResult
            One canonical immutable outcome per supplied entry.

        Raises
        ------
        TypeError
            If profile or source container types are wrong.
        ValueError
            If no source entry is supplied.
        """
        if type(profile) is not PythonProductionSourceProfile:
            raise TypeError("profile must be PythonProductionSourceProfile")
        if type(sources) is not tuple or any(
            type(source) is not PythonProductionSource for source in sources
        ):
            raise TypeError("sources must contain PythonProductionSource values")
        if not sources:
            raise ValueError("at least one explicit source is required")
        modules = tuple(
            sorted(
                (self._inspect(source) for source in sources),
                key=lambda item: item.sort_key,
            )
        )
        return PythonProductionInspectionResult(profile=profile, modules=modules)

    def _inspect(
        self, source: PythonProductionSource
    ) -> PythonProductionModuleInspection:
        """Return the complete outcome for one explicit entry."""
        if source.read_error is not None:
            return PythonProductionModuleInspection(
                input_identity=source.input_identity,
                path=source.path,
                source_sha256=None,
                source_byte_count=None,
                facts=None,
                failure=PythonProductionSourceFailure(
                    kind=PythonProductionFailureKind.READ,
                    message=source.read_error,
                    line=None,
                    column=None,
                ),
            )
        payload = source.payload
        if payload is None:
            raise AssertionError("source invariant requires payload bytes")
        identity = hashlib.sha256(payload).hexdigest()
        byte_count = len(payload)
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError as error:
            return PythonProductionModuleInspection(
                input_identity=source.input_identity,
                path=source.path,
                source_sha256=identity,
                source_byte_count=byte_count,
                facts=None,
                failure=PythonProductionSourceFailure(
                    kind=PythonProductionFailureKind.DECODE,
                    message=(f"invalid UTF-8 at byte {error.start}: {error.reason}"),
                    line=None,
                    column=None,
                ),
            )
        try:
            module = ast.parse(text, filename=source.path.as_posix(), mode="exec")
        except SyntaxError as error:
            return PythonProductionModuleInspection(
                input_identity=source.input_identity,
                path=source.path,
                source_sha256=identity,
                source_byte_count=byte_count,
                facts=None,
                failure=PythonProductionSourceFailure(
                    kind=PythonProductionFailureKind.SYNTAX,
                    message=error.msg,
                    line=error.lineno,
                    column=None if error.offset is None else error.offset - 1,
                ),
            )
        classes: list[PythonProductionClassFact] = []
        callables: list[PythonProductionCallableFact] = []
        imports: list[PythonProductionImportFact] = []
        calls: list[PythonProductionCallFact] = []
        all_syntax: list[PythonProductionAllSyntaxFact] = []
        self._visit(
            module,
            (),
            (),
            classes,
            callables,
            imports,
            calls,
            all_syntax,
        )
        ordered_all = tuple(sorted(all_syntax, key=lambda fact: fact.sort_key))
        resolution, names = self._effective_all(ordered_all)
        facts = PythonProductionModuleFacts(
            classes=tuple(sorted(classes, key=lambda fact: fact.sort_key)),
            callables=tuple(sorted(callables, key=lambda fact: fact.sort_key)),
            imports=tuple(sorted(imports, key=lambda fact: fact.sort_key)),
            calls=tuple(sorted(calls, key=lambda fact: fact.sort_key)),
            all_syntax=ordered_all,
            effective_all_resolution=resolution,
            effective_all_names=names,
        )
        return PythonProductionModuleInspection(
            input_identity=source.input_identity,
            path=source.path,
            source_sha256=identity,
            source_byte_count=byte_count,
            facts=facts,
            failure=None,
        )

    def _visit(
        self,
        node: ast.AST,
        owners: tuple[PythonProductionLexicalOwner, ...],
        contexts: tuple[PythonProductionExecutionContext, ...],
        classes: list[PythonProductionClassFact],
        callables: list[PythonProductionCallableFact],
        imports: list[PythonProductionImportFact],
        calls: list[PythonProductionCallFact],
        all_syntax: list[PythonProductionAllSyntaxFact],
    ) -> None:
        """Visit one AST node with explicit lexical and execution state."""
        if isinstance(node, ast.ClassDef):
            qualified_name = self._qualified(owners, node.name)
            classes.append(
                PythonProductionClassFact(
                    name=node.name,
                    qualified_name=qualified_name,
                    owners=owners,
                    location=self._location(node),
                )
            )
            for external in (
                *node.decorator_list,
                *node.bases,
                *node.keywords,
                *node.type_params,
            ):
                self._visit(
                    external,
                    owners,
                    contexts,
                    classes,
                    callables,
                    imports,
                    calls,
                    all_syntax,
                )
            class_owner = PythonProductionLexicalOwner(
                name=node.name,
                qualified_name=qualified_name,
                kind=PythonProductionScopeKind.CLASS,
            )
            for statement in node.body:
                self._visit(
                    statement,
                    (*owners, class_owner),
                    contexts,
                    classes,
                    callables,
                    imports,
                    calls,
                    all_syntax,
                )
            return
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            kind = (
                PythonProductionCallableKind.ASYNC_FUNCTION
                if isinstance(node, ast.AsyncFunctionDef)
                else PythonProductionCallableKind.FUNCTION
            )
            qualified_name = self._qualified(owners, node.name)
            callables.append(
                PythonProductionCallableFact(
                    name=node.name,
                    qualified_name=qualified_name,
                    kind=kind,
                    owners=owners,
                    location=self._location(node),
                )
            )
            externals: tuple[ast.AST | None, ...] = (
                *node.decorator_list,
                *node.args.defaults,
                *node.args.kw_defaults,
                *(argument.annotation for argument in node.args.posonlyargs),
                *(argument.annotation for argument in node.args.args),
                *(argument.annotation for argument in node.args.kwonlyargs),
                None if node.args.vararg is None else node.args.vararg.annotation,
                None if node.args.kwarg is None else node.args.kwarg.annotation,
                node.returns,
                *node.type_params,
            )
            for function_external in externals:
                if function_external is not None:
                    self._visit(
                        function_external,
                        owners,
                        contexts,
                        classes,
                        callables,
                        imports,
                        calls,
                        all_syntax,
                    )
            callable_owner = PythonProductionLexicalOwner(
                name=node.name,
                qualified_name=qualified_name,
                kind=PythonProductionScopeKind.CALLABLE,
            )
            for statement in node.body:
                self._visit(
                    statement,
                    (*owners, callable_owner),
                    contexts,
                    classes,
                    callables,
                    imports,
                    calls,
                    all_syntax,
                )
            return
        if isinstance(node, ast.Lambda):
            name = f"<lambda>@{node.lineno}:{node.col_offset}"
            qualified_name = self._qualified(owners, name)
            callables.append(
                PythonProductionCallableFact(
                    name=name,
                    qualified_name=qualified_name,
                    kind=PythonProductionCallableKind.LAMBDA,
                    owners=owners,
                    location=self._location(node),
                )
            )
            for default in (*node.args.defaults, *node.args.kw_defaults):
                if default is not None:
                    self._visit(
                        default,
                        owners,
                        contexts,
                        classes,
                        callables,
                        imports,
                        calls,
                        all_syntax,
                    )
            lambda_owner = PythonProductionLexicalOwner(
                name=name,
                qualified_name=qualified_name,
                kind=PythonProductionScopeKind.CALLABLE,
            )
            self._visit(
                node.body,
                (*owners, lambda_owner),
                contexts,
                classes,
                callables,
                imports,
                calls,
                all_syntax,
            )
            return
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(
                    PythonProductionImportFact(
                        kind=PythonProductionImportKind.IMPORT,
                        module=alias.name,
                        name=alias.name,
                        alias=alias.asname,
                        relative_level=0,
                        owners=owners,
                        contexts=contexts,
                        location=self._location(alias),
                    )
                )
            return
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imports.append(
                    PythonProductionImportFact(
                        kind=PythonProductionImportKind.FROM_IMPORT,
                        module=node.module,
                        name=alias.name,
                        alias=alias.asname,
                        relative_level=node.level,
                        owners=owners,
                        contexts=contexts,
                        location=self._location(alias),
                    )
                )
            return
        if isinstance(node, ast.If):
            self._visit(
                node.test,
                owners,
                contexts,
                classes,
                callables,
                imports,
                calls,
                all_syntax,
            )
            expression = ast.unparse(node.test)
            self._visit_statements_with_context(
                node.body,
                PythonProductionContextKind.IF_BODY,
                expression,
                node,
                owners,
                contexts,
                classes,
                callables,
                imports,
                calls,
                all_syntax,
            )
            self._visit_statements_with_context(
                node.orelse,
                PythonProductionContextKind.IF_ELSE,
                expression,
                node,
                owners,
                contexts,
                classes,
                callables,
                imports,
                calls,
                all_syntax,
            )
            return
        if isinstance(node, (ast.Try, ast.TryStar)):
            self._visit_statements_with_context(
                node.body,
                PythonProductionContextKind.TRY_BODY,
                None,
                node,
                owners,
                contexts,
                classes,
                callables,
                imports,
                calls,
                all_syntax,
            )
            for handler in node.handlers:
                handler_expression = (
                    None if handler.type is None else ast.unparse(handler.type)
                )
                if handler.type is not None:
                    self._visit(
                        handler.type,
                        owners,
                        contexts,
                        classes,
                        callables,
                        imports,
                        calls,
                        all_syntax,
                    )
                self._visit_statements_with_context(
                    handler.body,
                    PythonProductionContextKind.TRY_HANDLER,
                    handler_expression,
                    handler,
                    owners,
                    contexts,
                    classes,
                    callables,
                    imports,
                    calls,
                    all_syntax,
                )
            self._visit_statements_with_context(
                node.orelse,
                PythonProductionContextKind.TRY_ELSE,
                None,
                node,
                owners,
                contexts,
                classes,
                callables,
                imports,
                calls,
                all_syntax,
            )
            self._visit_statements_with_context(
                node.finalbody,
                PythonProductionContextKind.TRY_FINALLY,
                None,
                node,
                owners,
                contexts,
                classes,
                callables,
                imports,
                calls,
                all_syntax,
            )
            return
        if isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
            control = node.test if isinstance(node, ast.While) else node.iter
            self._visit(
                control,
                owners,
                contexts,
                classes,
                callables,
                imports,
                calls,
                all_syntax,
            )
            if not isinstance(node, ast.While):
                self._visit(
                    node.target,
                    owners,
                    contexts,
                    classes,
                    callables,
                    imports,
                    calls,
                    all_syntax,
                )
            expression = ast.unparse(control)
            self._visit_statements_with_context(
                node.body,
                PythonProductionContextKind.LOOP_BODY,
                expression,
                node,
                owners,
                contexts,
                classes,
                callables,
                imports,
                calls,
                all_syntax,
            )
            self._visit_statements_with_context(
                node.orelse,
                PythonProductionContextKind.LOOP_ELSE,
                expression,
                node,
                owners,
                contexts,
                classes,
                callables,
                imports,
                calls,
                all_syntax,
            )
            return
        if isinstance(node, (ast.With, ast.AsyncWith)):
            for item in node.items:
                self._visit(
                    item.context_expr,
                    owners,
                    contexts,
                    classes,
                    callables,
                    imports,
                    calls,
                    all_syntax,
                )
                if item.optional_vars is not None:
                    self._visit(
                        item.optional_vars,
                        owners,
                        contexts,
                        classes,
                        callables,
                        imports,
                        calls,
                        all_syntax,
                    )
            self._visit_statements_with_context(
                node.body,
                PythonProductionContextKind.WITH_BODY,
                None,
                node,
                owners,
                contexts,
                classes,
                callables,
                imports,
                calls,
                all_syntax,
            )
            return
        if isinstance(node, ast.Match):
            self._visit(
                node.subject,
                owners,
                contexts,
                classes,
                callables,
                imports,
                calls,
                all_syntax,
            )
            for case in node.cases:
                expression = ast.unparse(case.pattern)
                if case.guard is not None:
                    expression = f"{expression} if {ast.unparse(case.guard)}"
                    self._visit(
                        case.guard,
                        owners,
                        contexts,
                        classes,
                        callables,
                        imports,
                        calls,
                        all_syntax,
                    )
                self._visit_statements_with_context(
                    case.body,
                    PythonProductionContextKind.MATCH_CASE,
                    expression,
                    case.pattern,
                    owners,
                    contexts,
                    classes,
                    callables,
                    imports,
                    calls,
                    all_syntax,
                )
            return
        if isinstance(
            node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)
        ):
            expression = ", ".join(
                ast.unparse(generator.iter) for generator in node.generators
            )
            context = PythonProductionExecutionContext(
                kind=PythonProductionContextKind.COMPREHENSION,
                expression=expression,
                location=self._location(node),
            )
            nested_contexts = (*contexts, context)
            for child in ast.iter_child_nodes(node):
                self._visit(
                    child,
                    owners,
                    nested_contexts,
                    classes,
                    callables,
                    imports,
                    calls,
                    all_syntax,
                )
            return

        if isinstance(node, ast.Call):
            receiver: str | None = None
            callee_name: str | None = None
            if isinstance(node.func, ast.Attribute):
                receiver = ast.unparse(node.func.value)
                callee_name = node.func.attr
            elif isinstance(node.func, ast.Name):
                callee_name = node.func.id
            calls.append(
                PythonProductionCallFact(
                    callee_expression=ast.unparse(node.func),
                    receiver_expression=receiver,
                    callee_name=callee_name,
                    owners=owners,
                    contexts=contexts,
                    location=self._location(node),
                )
            )
            if (
                not owners
                and receiver == "__all__"
                and callee_name
                in {
                    "append",
                    "extend",
                    "insert",
                    "remove",
                    "pop",
                    "clear",
                    "sort",
                    "reverse",
                }
            ):
                all_syntax.append(
                    PythonProductionAllSyntaxFact(
                        operation=PythonProductionAllOperation.MUTATION,
                        raw_expression=ast.unparse(node),
                        literal_names=None,
                        literal_sequence_kind=None,
                        augmented_operator=None,
                        contexts=contexts,
                        location=self._location(node),
                    )
                )
        self._record_all(node, owners, contexts, all_syntax)
        for child in ast.iter_child_nodes(node):
            self._visit(
                child, owners, contexts, classes, callables, imports, calls, all_syntax
            )

    def _visit_statements_with_context(
        self,
        statements: list[ast.stmt],
        kind: PythonProductionContextKind,
        expression: str | None,
        context_node: ast.stmt | ast.expr | ast.pattern | ast.excepthandler,
        owners: tuple[PythonProductionLexicalOwner, ...],
        contexts: tuple[PythonProductionExecutionContext, ...],
        classes: list[PythonProductionClassFact],
        callables: list[PythonProductionCallableFact],
        imports: list[PythonProductionImportFact],
        calls: list[PythonProductionCallFact],
        all_syntax: list[PythonProductionAllSyntaxFact],
    ) -> None:
        """Visit statements under one explicitly represented neutral context."""
        if not statements:
            return
        context = PythonProductionExecutionContext(
            kind=kind,
            expression=expression,
            location=self._location(context_node),
        )
        for statement in statements:
            self._visit(
                statement,
                owners,
                (*contexts, context),
                classes,
                callables,
                imports,
                calls,
                all_syntax,
            )

    def _record_all(
        self,
        node: ast.AST,
        owners: tuple[PythonProductionLexicalOwner, ...],
        contexts: tuple[PythonProductionExecutionContext, ...],
        facts: list[PythonProductionAllSyntaxFact],
    ) -> None:
        """Record direct module ``__all__`` assignment and deletion syntax."""
        if owners:
            return
        value: ast.expr | None = None
        operation: PythonProductionAllOperation | None = None
        augmented_operator: PythonProductionAugmentedOperator | None = None
        statement: ast.stmt | None = None
        target_is_all = False
        if isinstance(node, ast.Assign):
            statement = node
            target_is_all = any(
                isinstance(target, ast.Name) and target.id == "__all__"
                for target in node.targets
            )
            value = node.value
            operation = PythonProductionAllOperation.ASSIGN
        elif isinstance(node, ast.AnnAssign):
            statement = node
            target_is_all = (
                isinstance(node.target, ast.Name) and node.target.id == "__all__"
            )
            value = node.value
            operation = PythonProductionAllOperation.ANNOTATED_ASSIGN
        elif isinstance(node, ast.AugAssign):
            statement = node
            target_is_all = (
                isinstance(node.target, ast.Name) and node.target.id == "__all__"
            )
            value = node.value
            operation = PythonProductionAllOperation.AUGMENTED_ASSIGN
            augmented_operator = self._augmented_operator(node.op)
        elif isinstance(node, ast.Delete):
            statement = node
            target_is_all = any(
                isinstance(target, ast.Name) and target.id == "__all__"
                for target in node.targets
            )
            operation = PythonProductionAllOperation.DELETE
        if not target_is_all or operation is None or statement is None:
            return
        literal_names, literal_sequence_kind = (
            (None, None) if value is None else self._literal_sequence(value)
        )
        facts.append(
            PythonProductionAllSyntaxFact(
                operation=operation,
                raw_expression=None if value is None else ast.unparse(value),
                literal_names=literal_names,
                literal_sequence_kind=literal_sequence_kind,
                augmented_operator=augmented_operator,
                contexts=contexts,
                location=self._location(statement),
            )
        )

    @staticmethod
    def _literal_sequence(
        value: ast.expr,
    ) -> tuple[tuple[str, ...] | None, PythonProductionLiteralSequenceKind | None]:
        """Return exact string names and list/tuple literal form without evaluation."""
        if isinstance(value, ast.List):
            kind = PythonProductionLiteralSequenceKind.LIST
        elif isinstance(value, ast.Tuple):
            kind = PythonProductionLiteralSequenceKind.TUPLE
        else:
            return None, None
        names: list[str] = []
        for element in value.elts:
            if not isinstance(element, ast.Constant) or type(element.value) is not str:
                return None, None
            names.append(element.value)
        return tuple(names), kind

    @staticmethod
    def _augmented_operator(
        operator: ast.operator,
    ) -> PythonProductionAugmentedOperator:
        """Map every Python augmented-assignment operator to one closed syntax kind."""
        operator_types = (
            (ast.Add, PythonProductionAugmentedOperator.ADD),
            (ast.Sub, PythonProductionAugmentedOperator.SUBTRACT),
            (ast.Mult, PythonProductionAugmentedOperator.MULTIPLY),
            (ast.MatMult, PythonProductionAugmentedOperator.MATRIX_MULTIPLY),
            (ast.Div, PythonProductionAugmentedOperator.DIVIDE),
            (ast.FloorDiv, PythonProductionAugmentedOperator.FLOOR_DIVIDE),
            (ast.Mod, PythonProductionAugmentedOperator.MODULO),
            (ast.Pow, PythonProductionAugmentedOperator.POWER),
            (ast.LShift, PythonProductionAugmentedOperator.LEFT_SHIFT),
            (ast.RShift, PythonProductionAugmentedOperator.RIGHT_SHIFT),
            (ast.BitOr, PythonProductionAugmentedOperator.BIT_OR),
            (ast.BitXor, PythonProductionAugmentedOperator.BIT_XOR),
            (ast.BitAnd, PythonProductionAugmentedOperator.BIT_AND),
        )
        for operator_type, kind in operator_types:
            if isinstance(operator, operator_type):
                return kind
        raise ValueError("unsupported augmented-assignment operator")

    @staticmethod
    def _effective_all(
        facts: tuple[PythonProductionAllSyntaxFact, ...],
    ) -> tuple[PythonProductionAllResolution, tuple[str, ...] | None]:
        """Resolve only proven direct literal sequence assignment and ``+=`` cases.

        A direct list or tuple string-literal assignment establishes exact names and
        sequence form. For ``+=``, a list accepts an exact list or tuple literal,
        while a tuple accepts only an exact tuple literal. Every other operator,
        sequence pairing, context, expression, mutation, or deletion is unresolved.
        A later direct literal assignment can establish a new exact state.
        """
        if not facts:
            return PythonProductionAllResolution.ABSENT, None
        names: tuple[str, ...] | None = None
        sequence_kind: PythonProductionLiteralSequenceKind | None = None
        dynamic = False
        for fact in facts:
            if fact.contexts:
                dynamic = True
                names = None
                sequence_kind = None
            elif fact.operation in {
                PythonProductionAllOperation.ASSIGN,
                PythonProductionAllOperation.ANNOTATED_ASSIGN,
            }:
                names = fact.literal_names
                sequence_kind = fact.literal_sequence_kind
                dynamic = names is None or sequence_kind is None
            elif fact.operation is PythonProductionAllOperation.AUGMENTED_ASSIGN:
                rhs_kind = fact.literal_sequence_kind
                if (
                    fact.augmented_operator is PythonProductionAugmentedOperator.ADD
                    and names is not None
                    and sequence_kind is not None
                    and fact.literal_names is not None
                    and rhs_kind is not None
                    and (
                        sequence_kind is PythonProductionLiteralSequenceKind.LIST
                        or rhs_kind is PythonProductionLiteralSequenceKind.TUPLE
                    )
                ):
                    names = (*names, *fact.literal_names)
                    dynamic = False
                else:
                    dynamic = True
                    names = None
                    sequence_kind = None
            else:
                dynamic = True
                names = None
                sequence_kind = None
        if dynamic or names is None:
            return PythonProductionAllResolution.DYNAMIC, None
        return PythonProductionAllResolution.LITERAL, names

    @staticmethod
    def _qualified(owners: tuple[PythonProductionLexicalOwner, ...], name: str) -> str:
        """Return deterministic dot-separated lexical qualification."""
        return ".".join((*tuple(owner.name for owner in owners), name))

    @staticmethod
    def _location(
        node: ast.stmt | ast.expr | ast.pattern | ast.excepthandler | ast.alias,
    ) -> PythonProductionLocation:
        """Return one exact span from a parsed Python syntax node."""
        line = node.lineno
        column = node.col_offset
        end_line = node.end_lineno
        end_column = node.end_col_offset
        if end_line is None or end_column is None:
            raise ValueError("parsed syntax node lacks an end location")
        return PythonProductionLocation(
            line=line,
            column=column,
            end_line=end_line,
            end_column=end_column,
        )
