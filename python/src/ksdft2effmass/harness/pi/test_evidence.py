"""Explicit-input structural validation of Python test evidence.

The module represents caller-supplied source and JSON bytes; it never reads a
filesystem or discovers a repository, root, current directory, Git checkout, or
process state.  :class:`ValidatePythonTestEvidence` checks the maintained static
syntax, documentation, ownership, evidence-identifier, parameter-inventory, and
optional migration-map conventions inherited from the compatibility command.
Its findings are deterministic software-verification diagnostics for the
supplied representation.  A passing result does not establish oracle
independence, mathematical correctness, test cohesion, tolerance adequacy,
scientific validity, uncertainty quantification, or human acceptance.
"""

from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass
from typing import Any

from .identity import _require_builtin_str, _require_tuple

HEADINGS = (
    "Facet and represented meaning",
    "Intrinsic and cross-object scope",
    "VVUQ and scientific exclusions",
)
SUPERSEDED_HEADINGS = (
    "Evidence class and represented meaning",
    "Owned contract, oracle, and scope",
)
FIELDS = (
    "Evidence ID",
    "Requirement",
    "Method",
    "Oracle",
    "Acceptance",
    "Interpretation",
    "Limitations",
)
SURFACES = (
    "constructor",
    "field",
    "property",
    "method",
    "classmethod",
    "staticmethod",
    "protocol",
    "public_api",
    "artifact",
    "workflow",
)
NAME_RE = re.compile(
    r"^test_(" + "|".join(SURFACES) + r")__[a-z][a-z0-9_]*__[a-z][a-z0-9_]*$"
)
ID_RE = re.compile(r"\b(?:[A-Z][A-Z0-9]*-)+[0-9]{3,}\b")
SEMANTIC_PARAM_RE = re.compile(
    r"^(?:[a-z][a-z0-9]*(?:_[a-z0-9]+)*|(?:[A-Z][A-Z0-9]*-)+[0-9]{3,}-[a-z][a-z0-9]*(?:[-_][a-z0-9]+)*)$"
)
EVIDENCE_OPENINGS = {
    "software_verification": "Software verification",
    "numerical_verification": "Numerical verification",
    "scientific_validation": "Scientific validation",
    "uncertainty_quantification": "Uncertainty quantification",
}
VAGUE_FACETS = {"behavior", "contract", "general", "misc"}
UNKNOWN_VALUE_ID_WORDS = {"unknown", "unsupported", "unrecognized"}
WRONG_TYPE_ID_WORDS = {
    "boolean",
    "bytes",
    "float",
    "integer",
    "none",
    "string",
    "wrong_type",
}
COMPLETENESS_WORDS = re.compile(r"\b(?:all|complete|entire|every|field-complete)\b")
STATE_WORDS = re.compile(
    r"\b(?:dataclass state|public state|represented state|fields?)\b"
)
EQUALITY_WORDS = re.compile(
    r"\b(?:equality|compares?|distinguishes?|equal exactly|makes? them unequal)\b"
)
FROZEN_WORDS = re.compile(
    r"\b(?:frozen|immutable|rejects? post-construction assignment|"
    r"assignments? raise)\b"
)


def claims_complete_equality(function_name: str, requirement: str) -> bool:
    """Recognize complete equality claims without matching unrelated prose."""
    equality_context = "__eq__" in function_name or EQUALITY_WORDS.search(requirement)
    return bool(
        equality_context
        and COMPLETENESS_WORDS.search(requirement)
        and STATE_WORDS.search(requirement)
    )


def claims_complete_frozen(function_name: str, requirement: str) -> bool:
    """Recognize complete frozen-state claims without matching ordinary immutability."""
    frozen_context = (
        "frozen" in function_name
        or "immutable" in function_name
        or bool(
            FROZEN_WORDS.search(requirement)
            and re.search(
                r"\b(?:assignment|reassignment|mutation|frozen)\b", requirement
            )
        )
    )
    return bool(
        frozen_context
        and COMPLETENESS_WORDS.search(requirement)
        and STATE_WORDS.search(requirement)
    )


@dataclass(frozen=True, slots=True)
class PythonTestEvidenceSource:
    """One explicitly supplied module and its caller-observed read outcome.

    Attributes
    ----------
    path
        Caller-supplied diagnostic path.  Absolute paths are accepted because
        the generic validator assigns no repository-root meaning to the value.
    payload
        Exact module bytes, or ``None`` when the caller could not supply bytes.
    is_regular_file
        Whether the caller observed a regular, nonsymlink file.  Generic code
        trusts this explicit observation and performs no filesystem query.
    read_error
        Caller-rendered read failure, or ``None``.  A regular source has exactly
        one of ``payload`` and ``read_error``; a nonregular source has neither.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If a string is empty or the represented read outcome is contradictory.
    """

    path: str
    payload: bytes | None
    is_regular_file: bool = True
    read_error: str | None = None

    def __post_init__(self) -> None:
        _require_builtin_str(self.path, "path")
        if type(self.is_regular_file) is not bool:
            raise TypeError("is_regular_file must be a bool")
        if self.payload is not None and type(self.payload) is not bytes:
            raise TypeError("payload must be bytes or None")
        if self.read_error is not None:
            _require_builtin_str(self.read_error, "read_error")
        if not self.is_regular_file and (self.payload is not None or self.read_error):
            raise ValueError(
                "a non-regular source cannot contain payload or read_error"
            )
        if self.is_regular_file and (self.payload is None) == (self.read_error is None):
            raise ValueError(
                "a regular source requires exactly one payload or read_error"
            )


@dataclass(frozen=True, slots=True)
class PythonTestEvidenceRequest:
    """Closed explicit inputs for one test-evidence validation.

    Attributes
    ----------
    sources
        Nonempty tuple of explicitly supplied module inputs, in command order.
        Duplicate paths remain representable and produce a validation finding.
    ownership_path
        Diagnostic path for the ownership input.
    ownership_payload
        Exact ownership JSON bytes, or ``None`` after a caller read failure.
    ownership_read_error
        Caller-rendered ownership read failure, or ``None`` when bytes exist.
    migration_path
        Diagnostic path for an optional migration map.
    migration_payload
        Exact optional migration-map JSON bytes.
    migration_read_error
        Caller-rendered optional migration-map read failure.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If required input is absent or a payload/read-error state conflicts.
    """

    sources: tuple[PythonTestEvidenceSource, ...]
    ownership_path: str
    ownership_payload: bytes | None
    ownership_read_error: str | None = None
    migration_path: str | None = None
    migration_payload: bytes | None = None
    migration_read_error: str | None = None

    def __post_init__(self) -> None:
        _require_tuple(self.sources, "sources")
        if not self.sources:
            raise ValueError("sources must be nonempty")
        if any(type(source) is not PythonTestEvidenceSource for source in self.sources):
            raise TypeError("sources must contain PythonTestEvidenceSource values")
        _require_builtin_str(self.ownership_path, "ownership_path")
        if (
            self.ownership_payload is not None
            and type(self.ownership_payload) is not bytes
        ):
            raise TypeError("ownership_payload must be bytes or None")
        if self.ownership_read_error is not None:
            _require_builtin_str(self.ownership_read_error, "ownership_read_error")
        if (self.ownership_payload is None) == (self.ownership_read_error is None):
            raise ValueError("ownership requires exactly one payload or read error")
        if self.migration_path is None:
            if (
                self.migration_payload is not None
                or self.migration_read_error is not None
            ):
                raise ValueError("migration data requires migration_path")
        else:
            _require_builtin_str(self.migration_path, "migration_path")
            if (
                self.migration_payload is not None
                and type(self.migration_payload) is not bytes
            ):
                raise TypeError("migration_payload must be bytes or None")
            if self.migration_read_error is not None:
                _require_builtin_str(self.migration_read_error, "migration_read_error")
            if (self.migration_payload is None) == (self.migration_read_error is None):
                raise ValueError("migration requires exactly one payload or read error")


@dataclass(frozen=True, slots=True)
class PythonTestEvidenceFinding:
    """One expected-invalidity finding for supplied evidence.

    Attributes
    ----------
    code
        Stable compatibility diagnostic code in the ``TE.`` namespace.
    path
        Caller-supplied diagnostic path associated with the finding.
    message
        Deterministic human-readable diagnostic detail.
    severity
        Compatibility severity, currently fixed to ``"error"``.
    line
        Optional one-based source line.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If a value violates its intrinsic lexical or range invariant.
    """

    code: str
    path: str
    message: str
    severity: str = "error"
    line: int | None = None

    def __post_init__(self) -> None:
        _require_builtin_str(self.code, "code")
        if not self.code.startswith("TE."):
            raise ValueError("code must use the TE namespace")
        _require_builtin_str(self.path, "path")
        _require_builtin_str(self.message, "message")
        _require_builtin_str(self.severity, "severity")
        if self.severity != "error":
            raise ValueError("severity must equal 'error'")
        if self.line is not None:
            if type(self.line) is not int:
                raise TypeError("line must be an int excluding bool or None")
            if self.line < 1:
                raise ValueError("line must be positive")


def finding(
    code: str, path: str, message: str, line: int | None = None
) -> PythonTestEvidenceFinding:
    return PythonTestEvidenceFinding(code, path, message, "error", line)


def sections(doc: str | None, labels: tuple[str, ...]) -> tuple[bool, str]:
    if not doc:
        return False, "docstring is missing"
    positions: list[int] = []
    matches_by_label: list[re.Match[str]] = []
    inline_fields = labels == FIELDS
    for label in labels:
        pattern = (
            rf"(?m)^[ \t]*{re.escape(label)}:[ \t]+\S.*$"
            if inline_fields
            else rf"(?m)^[ \t]*{re.escape(label)}[ \t]*$"
        )
        matches = list(re.finditer(pattern, doc))
        if len(matches) != 1:
            style = "one 'Label: value' paragraph" if inline_fields else "exactly once"
            return False, f"{label!r} must occur as {style}"
        positions.append(matches[0].start())
        matches_by_label.append(matches[0])
    if positions != sorted(positions):
        return False, "required sections are out of order"
    if inline_fields:
        for current, following in zip(
            matches_by_label, matches_by_label[1:], strict=False
        ):
            between = doc[current.end() : following.start()]
            if not re.search(r"(?<!\n)\n\n\Z", between):
                return False, "evidence paragraphs must be separated by one blank line"
        return True, ""
    for index, match in enumerate(matches_by_label):
        next_start = (
            matches_by_label[index + 1].start()
            if index + 1 < len(matches_by_label)
            else len(doc)
        )
        body = doc[match.end() : next_start]
        if not re.match(r"\n\n(?!\n)", body):
            return False, "module sections must begin after one blank line"
        if index + 1 < len(matches_by_label) and not re.search(r"(?<!\n)\n\n\Z", body):
            return False, "module sections must be separated by one blank line"
        if not body.strip():
            return False, f"{labels[index]!r} has an empty body"
    return True, ""


@dataclass(frozen=True)
class ParameterCaseInventory:
    """Statically resolved parameter cases and inventory-specific findings."""

    elements: tuple[ast.expr, ...] | None
    findings: tuple[tuple[str, str], ...]
    named: bool


def assigned_names(target: ast.expr) -> set[str]:
    """Return simple names stored anywhere in one assignment target."""
    if isinstance(target, ast.Name):
        return {target.id}
    if isinstance(target, (ast.List, ast.Tuple)):
        return {name for element in target.elts for name in assigned_names(element)}
    return set()


def module_scope_statements(tree: ast.Module) -> tuple[ast.stmt, ...]:
    """Return statements executed at module scope, including compound bodies."""
    statements: list[ast.stmt] = []

    def visit(node: ast.AST) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                statements.append(child)
                continue
            if isinstance(child, ast.stmt):
                statements.append(child)
            visit(child)

    visit(tree)
    return tuple(statements)


def imported_module_names(tree: ast.Module) -> set[str]:
    """Return names introduced by imports in module-executed statements."""
    names: set[str] = set()
    for statement in module_scope_statements(tree):
        if isinstance(statement, ast.Import):
            names.update(
                alias.asname or alias.name.split(".", 1)[0] for alias in statement.names
            )
        elif isinstance(statement, ast.ImportFrom):
            names.update(alias.asname or alias.name for alias in statement.names)
    return names


def module_assignments(tree: ast.Module, name: str) -> list[ast.Assign | ast.AnnAssign]:
    """Return module-level ordinary assignments that store one requested name."""
    assignments: list[ast.Assign | ast.AnnAssign] = []
    for statement in tree.body:
        if isinstance(statement, ast.Assign) and any(
            name in assigned_names(target) for target in statement.targets
        ):
            assignments.append(statement)
        elif isinstance(statement, ast.AnnAssign) and name in assigned_names(
            statement.target
        ):
            assignments.append(statement)
    return assignments


def inventory_mutation_findings(
    tree: ast.Module,
    name: str,
    assignment: ast.Assign | ast.AnnAssign,
) -> list[tuple[str, str]]:
    """Reject module-level reassignment and statically visible inventory mutation."""
    findings: list[tuple[str, str]] = []
    for statement in module_scope_statements(tree):
        if statement is assignment:
            continue
        if isinstance(statement, ast.Assign) and any(
            name in assigned_names(target) for target in statement.targets
        ):
            findings.append(
                (
                    "TE.PARAMETER_INVENTORY",
                    f"named parameter inventory {name!r} is reassigned",
                )
            )
        elif isinstance(statement, ast.AnnAssign) and name in assigned_names(
            statement.target
        ):
            findings.append(
                (
                    "TE.PARAMETER_INVENTORY",
                    f"named parameter inventory {name!r} is reassigned",
                )
            )
        elif isinstance(statement, ast.AugAssign) and (
            isinstance(statement.target, ast.Name) and statement.target.id == name
        ):
            findings.append(
                (
                    "TE.PARAMETER_INVENTORY",
                    f"named parameter inventory {name!r} uses augmented assignment",
                )
            )
    mutating_methods = {"append", "clear", "extend", "insert", "reverse", "sort"}
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == name
            and node.func.attr in mutating_methods
        ):
            findings.append(
                (
                    "TE.PARAMETER_INVENTORY",
                    f"named parameter inventory {name!r} is mutated with "
                    f"{node.func.attr}()",
                )
            )
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(
                isinstance(target, ast.Subscript)
                and isinstance(target.value, ast.Name)
                and target.value.id == name
                for target in targets
            ):
                findings.append(
                    (
                        "TE.PARAMETER_INVENTORY",
                        f"named parameter inventory {name!r} is mutated by "
                        "subscript assignment",
                    )
                )
    return findings


def resolve_parameter_case_inventory(
    tree: ast.Module, decorator: ast.Call
) -> ParameterCaseInventory:
    """Resolve inline cases or one restricted module-local named literal inventory."""
    values = decorator.args[1] if len(decorator.args) > 1 else None
    if isinstance(values, (ast.List, ast.Tuple)):
        return ParameterCaseInventory(tuple(values.elts), (), False)
    if not isinstance(values, ast.Name):
        return ParameterCaseInventory(
            None,
            (
                (
                    "TE.PARAMETER_ID",
                    "parameterization requires a literal case list and explicit IDs",
                ),
            ),
            False,
        )
    name = values.id
    if name in imported_module_names(tree):
        return ParameterCaseInventory(
            None,
            (
                (
                    "TE.PARAMETER_INVENTORY",
                    f"named parameter inventory {name!r} must not be imported",
                ),
            ),
            True,
        )
    assignments = module_assignments(tree, name)
    if not assignments:
        return ParameterCaseInventory(
            None,
            (
                (
                    "TE.PARAMETER_INVENTORY",
                    f"named parameter inventory {name!r} is unresolved in this module",
                ),
            ),
            True,
        )
    if len(assignments) != 1:
        return ParameterCaseInventory(
            None,
            (
                (
                    "TE.PARAMETER_INVENTORY",
                    f"named parameter inventory {name!r} must have exactly one "
                    "module-level assignment",
                ),
            ),
            True,
        )
    assignment = assignments[0]
    targets = (
        assignment.targets
        if isinstance(assignment, ast.Assign)
        else [assignment.target]
    )
    if len(targets) != 1 or not isinstance(targets[0], ast.Name):
        return ParameterCaseInventory(
            None,
            (
                (
                    "TE.PARAMETER_INVENTORY",
                    f"named parameter inventory {name!r} requires one "
                    "simple-name assignment",
                ),
            ),
            True,
        )
    if assignment.lineno >= decorator.lineno:
        return ParameterCaseInventory(
            None,
            (
                (
                    "TE.PARAMETER_INVENTORY",
                    f"named parameter inventory {name!r} must be assigned before "
                    "its consuming decorator",
                ),
            ),
            True,
        )
    value = assignment.value
    if not isinstance(value, (ast.List, ast.Tuple)):
        return ParameterCaseInventory(
            None,
            (
                (
                    "TE.PARAMETER_INVENTORY",
                    f"named parameter inventory {name!r} must be assigned directly "
                    "to a literal tuple or list",
                ),
            ),
            True,
        )
    if any(isinstance(element, ast.Starred) for element in value.elts):
        return ParameterCaseInventory(
            None,
            (
                (
                    "TE.PARAMETER_INVENTORY",
                    f"named parameter inventory {name!r} must not contain "
                    "starred expansion",
                ),
            ),
            True,
        )
    findings = inventory_mutation_findings(tree, name, assignment)
    return ParameterCaseInventory(tuple(value.elts), tuple(findings), True)


def semantic_parameter_id_problem(value: str) -> str | None:
    """Return the existing semantic-ID finding text for one static string."""
    unstable = (
        not SEMANTIC_PARAM_RE.fullmatch(value)
        or bool(re.fullmatch(r"(?:case[_-]?)?[0-9]+", value, re.IGNORECASE))
        or "::" in value
        or "/" in value
        or "\\" in value
        or bool(re.search(r"0x[0-9a-f]+", value, re.IGNORECASE))
        or any(0xD800 <= ord(char) <= 0xDFFF or char.isspace() for char in value)
    )
    if unstable:
        return f"pathological, ordinal, raw, or nonsemantic parameter ID {value!r}"
    return None


def decorator_parameter_findings(
    node: ast.FunctionDef | ast.AsyncFunctionDef, tree: ast.Module
) -> list[tuple[str, str]]:
    """Validate inline and named parameter case IDs without executing test code."""
    findings: list[tuple[str, str]] = []
    for dec in node.decorator_list:
        call = dec if isinstance(dec, ast.Call) else None
        if call is None or not (
            isinstance(call.func, ast.Attribute) and call.func.attr == "parametrize"
        ):
            continue
        ids = next((kw.value for kw in call.keywords if kw.arg == "ids"), None)
        resolution = resolve_parameter_case_inventory(tree, call)
        findings.extend(resolution.findings)
        if resolution.elements is None:
            continue
        explicit: list[str] = []
        if isinstance(ids, (ast.List, ast.Tuple)) and not resolution.named:
            explicit = [
                item.value
                for item in ids.elts
                if isinstance(item, ast.Constant) and isinstance(item.value, str)
            ]
            if len(explicit) != len(ids.elts):
                findings.append(
                    ("TE.PARAMETER_ID", "parameter IDs must be literal strings")
                )
        elif ids is None:
            for item in resolution.elements:
                valid_call = (
                    isinstance(item, ast.Call)
                    and isinstance(item.func, ast.Attribute)
                    and item.func.attr == "param"
                    and (
                        not resolution.named
                        or (
                            isinstance(item.func.value, ast.Name)
                            and item.func.value.id == "pytest"
                        )
                    )
                )
                if not valid_call:
                    message = (
                        "named parameter inventory elements must be direct "
                        "pytest.param(...) calls"
                        if resolution.named
                        else "parameterization requires explicit ids=... or "
                        "pytest.param(id=...)"
                    )
                    findings.append(
                        (
                            "TE.PARAMETER_INVENTORY"
                            if resolution.named
                            else "TE.PARAMETER_ID",
                            message,
                        )
                    )
                    continue
                assert isinstance(item, ast.Call)
                id_keywords = [kw.value for kw in item.keywords if kw.arg == "id"]
                if len(id_keywords) != 1:
                    findings.append(
                        (
                            "TE.PARAMETER_ID",
                            "every pytest.param case requires exactly one id=...",
                        )
                    )
                elif not (
                    isinstance(id_keywords[0], ast.Constant)
                    and isinstance(id_keywords[0].value, str)
                ):
                    findings.append(
                        (
                            "TE.PARAMETER_ID",
                            "every pytest.param id=... must be a static string literal",
                        )
                    )
                else:
                    explicit.append(id_keywords[0].value)
        elif resolution.named:
            findings.append(
                (
                    "TE.PARAMETER_INVENTORY",
                    "named parameter inventories own their explicit pytest.param "
                    "IDs and cannot use decorator ids=",
                )
            )
        else:
            findings.append(
                (
                    "TE.PARAMETER_ID",
                    "parameterization requires a literal case list and explicit IDs",
                )
            )
        if resolution.named and len(explicit) != len(set(explicit)):
            findings.append(
                ("TE.PARAMETER_ID", "named parameter inventory IDs must be unique")
            )
        for value in explicit:
            problem = semantic_parameter_id_problem(value)
            if problem is not None:
                findings.append(("TE.PARAMETER_ID", problem))
    return findings


def section_body(doc: str, label: str) -> str:
    """Return one exact evidence-field body, or an empty string when absent."""
    field_pattern = "|".join(map(re.escape, FIELDS))
    match = re.search(
        rf"(?ms)^[ \t]*{re.escape(label)}:[ \t]+(?P<first>\S.*?)[ \t]*$"
        rf"(?P<rest>.*?)(?=^[ \t]*(?:{field_pattern}):[ \t]+\S.*$|\Z)",
        doc,
    )
    if match is None:
        return ""
    return f"{match.group('first')}\n{match.group('rest')}".strip()


def literal_string_inventory(tree: ast.Module, name: str) -> tuple[str, ...] | None:
    """Resolve one module-level literal tuple/list of unique nonempty strings."""
    assignments = module_assignments(tree, name)
    if len(assignments) != 1:
        return None
    value = assignments[0].value
    if not isinstance(value, (ast.Tuple, ast.List)):
        return None
    strings = tuple(
        element.value
        for element in value.elts
        if isinstance(element, ast.Constant) and isinstance(element.value, str)
    )
    if (
        len(strings) != len(value.elts)
        or any(not item for item in strings)
        or len(strings) != len(set(strings))
    ):
        return None
    return strings


def parameter_case_ids(
    node: ast.FunctionDef | ast.AsyncFunctionDef, tree: ast.Module
) -> set[str]:
    """Return statically declared semantic case IDs for one test function."""
    ids: set[str] = set()
    for decorator in node.decorator_list:
        if not (
            isinstance(decorator, ast.Call)
            and isinstance(decorator.func, ast.Attribute)
            and decorator.func.attr == "parametrize"
        ):
            continue
        resolution = resolve_parameter_case_inventory(tree, decorator)
        if resolution.elements is None:
            continue
        for element in resolution.elements:
            if not isinstance(element, ast.Call):
                continue
            for keyword in element.keywords:
                if (
                    keyword.arg == "id"
                    and isinstance(keyword.value, ast.Constant)
                    and isinstance(keyword.value.value, str)
                ):
                    ids.add(keyword.value.value)
    return ids


def validate_file(
    source_input: PythonTestEvidenceSource,
    owner: dict[str, Any],
    seen_ids: dict[str, str],
) -> list[PythonTestEvidenceFinding]:
    path = source_input.path
    out: list[PythonTestEvidenceFinding] = []
    if source_input.read_error is not None:
        return [finding("TE.PARSE", path, source_input.read_error)]
    assert source_input.payload is not None
    try:
        source = source_input.payload.decode("utf-8")
        tree = ast.parse(source, filename=path)
    except (UnicodeError, SyntaxError) as exc:
        return [finding("TE.PARSE", path, str(exc))]
    module_doc = ast.get_docstring(tree, clean=False)
    first_line = (module_doc or "").splitlines()[0].strip() if module_doc else ""
    if re.search(r"(?m)^#\s*ruff:\s*noqa:\s*E501\s*$", source):
        out.append(
            finding(
                "TE.BLANKET_SUPPRESSION",
                path,
                "file-level E501 suppression is prohibited; use ordinary formatting "
                "or one targeted justified suppression",
            )
        )
    mode, sut = owner.get("mode"), owner.get("sut")
    evidence_class = owner.get("evidence_class")
    opening_label = (
        EVIDENCE_OPENINGS.get(evidence_class)
        if isinstance(evidence_class, str)
        else None
    )
    artifact = owner.get("artifact")
    if opening_label is None:
        out.append(
            finding(
                "TE.EVIDENCE_CLASS",
                path,
                "evidence_class must be software_verification, "
                "numerical_verification, scientific_validation, or "
                "uncertainty_quantification",
            )
        )
        expected_opening = None
    elif mode == "class_owned" and isinstance(sut, str) and sut:
        expected_opening = f"{opening_label} of ``{sut}``."
    elif mode == "artifact_owned" and isinstance(artifact, str) and artifact.strip():
        expected_opening = f"{opening_label} of {artifact}."
    else:
        expected_opening = None
    if (
        not source.startswith('r"""')
        or expected_opening is None
        or first_line != expected_opening
    ):
        out.append(
            finding(
                "TE.MODULE_OPENING",
                path,
                "raw module opening must exactly match structured ownership; "
                f"expected {expected_opening!r}",
            )
        )
    ok, detail = sections(module_doc, HEADINGS)
    if not ok:
        out.append(finding("TE.MODULE_DOC", path, detail))
    for heading in SUPERSEDED_HEADINGS:
        if module_doc and re.search(rf"(?m)^\s*{re.escape(heading)}\s*$", module_doc):
            out.append(
                finding(
                    "TE.SUPERSEDED_HEADING",
                    path,
                    f"superseded heading is prohibited: {heading}",
                )
            )
    if mode not in {"class_owned", "artifact_owned"}:
        out.append(
            finding("TE.OWNERSHIP", path, "mode must be class_owned or artifact_owned")
        )
    if mode == "class_owned":
        expected = re.compile(
            rf"^test__{re.escape(str(sut))}(?:__[a-z][a-z0-9_]*)?\.py$"
        )
        if (
            not isinstance(sut, str)
            or not sut
            or not expected.fullmatch(path.rsplit("/", 1)[-1])
        ):
            out.append(
                finding(
                    "TE.SUT_FILENAME",
                    path,
                    "class-owned filename must agree with the supplied SUT",
                )
            )
        assignment = next(
            (
                n
                for n in tree.body
                if isinstance(n, (ast.Assign, ast.AnnAssign))
                and any(
                    isinstance(t, ast.Name) and t.id == "SUT"
                    for t in (n.targets if isinstance(n, ast.Assign) else [n.target])
                )
            ),
            None,
        )
        value = assignment.value if assignment else None
        if not isinstance(value, ast.Name) or value.id != sut:
            out.append(
                finding(
                    "TE.SUT_ASSIGNMENT",
                    path,
                    "SUT assignment must name the supplied public class",
                )
            )
        imported = {
            alias.asname or alias.name
            for node in tree.body
            if isinstance(node, ast.ImportFrom)
            for alias in node.names
        }
        if sut not in imported:
            out.append(
                finding(
                    "TE.SUT_IMPORT",
                    path,
                    "supplied SUT must be imported through an explicit public import",
                )
            )
    elif mode == "artifact_owned":
        if not isinstance(artifact, str) or not artifact.strip():
            out.append(
                finding(
                    "TE.ARTIFACT_OWNER",
                    path,
                    "artifact_owned input must name one concrete artifact",
                )
            )
        if not re.fullmatch(r"test__[a-z][a-z0-9_]*\.py", path.rsplit("/", 1)[-1]):
            out.append(
                finding(
                    "TE.ARTIFACT_FILENAME",
                    path,
                    "artifact-owned filename must be descriptive lowercase snake case",
                )
            )
    for node in (
        n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
    ):
        is_test = node.name.startswith("test_")
        if is_test and not NAME_RE.fullmatch(node.name):
            out.append(
                finding(
                    "TE.TEST_NAME",
                    path,
                    "test name violates semantic surface/facet/behavior grammar",
                    node.lineno,
                )
            )
        elif is_test:
            parts = node.name.split("__")
            if len(parts) == 3 and parts[1] in VAGUE_FACETS:
                out.append(
                    finding(
                        "TE.VAGUE_TEST_FACET",
                        path,
                        f"test facet {parts[1]!r} does not name a concrete public "
                        "member or cohesive contract",
                        node.lineno,
                    )
                )
            calls_sut = any(
                isinstance(child, ast.Call)
                and isinstance(child.func, ast.Name)
                and child.func.id == "SUT"
                for child in ast.walk(node)
            )
            indexes_sut = any(
                isinstance(child, ast.Subscript)
                and isinstance(child.value, ast.Name)
                and child.value.id == "SUT"
                for child in ast.walk(node)
            )
            if calls_sut and indexes_sut:
                out.append(
                    finding(
                        "TE.MIXED_ENUM_LOOKUP",
                        path,
                        "one owner combines EnumType(value) construction with "
                        "EnumType[name] lookup",
                        node.lineno,
                    )
                )
            circular_member = any(
                isinstance(child, ast.Subscript)
                and isinstance(child.value, ast.Attribute)
                and isinstance(child.value.value, ast.Name)
                and child.value.value.id == "SUT"
                and child.value.attr == "__members__"
                for child in ast.walk(node)
            )
            if circular_member and indexes_sut:
                out.append(
                    finding(
                        "TE.CIRCULAR_ENUM_ORACLE",
                        path,
                        "successful name lookup must not derive its sole expected "
                        "member from SUT.__members__",
                        node.lineno,
                    )
                )
            case_ids = parameter_case_ids(node, tree)
            id_words = {word for case_id in case_ids for word in case_id.split("_")}
            has_unknown = bool(id_words & UNKNOWN_VALUE_ID_WORDS)
            has_wrong_type = any(
                word in case_id for case_id in case_ids for word in WRONG_TYPE_ID_WORDS
            )
            if has_unknown and has_wrong_type:
                out.append(
                    finding(
                        "TE.MIXED_INVALID_PARTITION",
                        path,
                        "one parameter family combines unknown accepted-type values "
                        "with wrong-semantic-type values",
                        node.lineno,
                    )
                )
        if not is_test and node.name.startswith("_"):
            out.append(
                finding(
                    "TE.HELPER_PRIVATE",
                    path,
                    "evidence helper must have a nonprivate semantic name",
                    node.lineno,
                )
            )
        if not is_test and (
            node.name in {"helper", "setup", "check"}
            or re.search(r"_[0-9]+$", node.name)
        ):
            out.append(
                finding(
                    "TE.HELPER_NAME", path, "helper name is not semantic", node.lineno
                )
            )
        if any(
            isinstance(child, (ast.For, ast.AsyncFor, ast.While))
            for child in ast.walk(node)
        ):
            out.append(
                finding(
                    "TE.HIDDEN_LOOP",
                    path,
                    "test/helper contains a loop that hides collected case identity",
                    node.lineno,
                )
            )
        for code, param_detail in decorator_parameter_findings(node, tree):
            out.append(finding(code, path, param_detail, node.lineno))
        ok, detail = sections(ast.get_docstring(node, clean=False), FIELDS)
        if not ok:
            out.append(finding("TE.FUNCTION_DOC", path, detail, node.lineno))
            continue
        doc = ast.get_docstring(node, clean=False) or ""
        if re.search(r"(?:!!|\?\?|(?<!\.)\.\.(?!\.))", doc):
            out.append(
                finding(
                    "TE.PROSE_PUNCTUATION",
                    path,
                    "evidence prose contains doubled terminal punctuation",
                    node.lineno,
                )
            )
        if re.search(r"(?i)(?:\bTODO\b|\bTBD\b|<placeholder>)", doc):
            out.append(
                finding(
                    "TE.PLACEHOLDER_PROSE",
                    path,
                    "evidence prose contains placeholder language",
                    node.lineno,
                )
            )
        requirement = section_body(doc, "Requirement").lower()
        if (
            claims_complete_equality(node.name, requirement)
            and literal_string_inventory(tree, "EQUALITY_FIELDS") is None
        ):
            out.append(
                finding(
                    "TE.EQUALITY_FIELD_INVENTORY",
                    path,
                    "complete-equality claims require one literal EQUALITY_FIELDS "
                    "inventory",
                    node.lineno,
                )
            )
        if (
            claims_complete_frozen(node.name, requirement)
            and literal_string_inventory(tree, "FROZEN_FIELDS") is None
        ):
            out.append(
                finding(
                    "TE.FROZEN_FIELD_INVENTORY",
                    path,
                    "all-fields-frozen claims require one literal FROZEN_FIELDS "
                    "inventory",
                    node.lineno,
                )
            )
        ids = ID_RE.findall(doc.split("Requirement", 1)[0])
        if is_test:
            if len(ids) != 1:
                out.append(
                    finding(
                        "TE.EVIDENCE_ID",
                        path,
                        "test must declare exactly one evidence ID",
                        node.lineno,
                    )
                )
            for eid in ids:
                if eid in seen_ids:
                    out.append(
                        finding(
                            "TE.DUPLICATE_ID",
                            path,
                            f"{eid} already occurs at {seen_ids[eid]}",
                            node.lineno,
                        )
                    )
                else:
                    seen_ids[eid] = f"{path}:{node.lineno}"
        elif "owns no identifier" not in doc.split("Requirement", 1)[0].lower():
            out.append(
                finding(
                    "TE.HELPER_ID",
                    path,
                    "helper must say it owns no identifier; referenced supported "
                    "IDs are not owned",
                    node.lineno,
                )
            )
    return out


def static_parameter_case_count(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    tree: ast.Module,
) -> int | None:
    """Return the static collected case product, or None when not derivable."""
    counts: list[int] = []
    for dec in node.decorator_list:
        if not (
            isinstance(dec, ast.Call)
            and isinstance(dec.func, ast.Attribute)
            and dec.func.attr == "parametrize"
        ):
            continue
        resolution = resolve_parameter_case_inventory(tree, dec)
        if resolution.elements is None or resolution.findings:
            return None
        counts.append(len(resolution.elements))
    if not counts:
        return 0
    result = 1
    for count in counts:
        result *= count
    return result


def load_ownership(
    path: str,
    payload: bytes | None,
    read_error: str | None,
    supplied: list[str],
) -> tuple[
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
    list[PythonTestEvidenceFinding],
]:
    """Load closed structured ownership without raising on malformed input."""
    out: list[PythonTestEvidenceFinding] = []
    if read_error is not None:
        return [], {}, [finding("TE.OWNERSHIP_INPUT", path, read_error)]
    assert payload is not None
    try:
        value = json.loads(payload.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        return [], {}, [finding("TE.OWNERSHIP_INPUT", path, str(exc))]
    if (
        not isinstance(value, dict)
        or set(value) != {"modules", "schema_version"}
        or value.get("schema_version") != 1
        or not isinstance(value.get("modules"), list)
    ):
        return (
            [],
            {},
            [
                finding(
                    "TE.OWNERSHIP_INPUT",
                    path,
                    "ownership must be a closed schema-version-1 object with "
                    "modules list",
                )
            ],
        )
    seen_paths: set[str] = set()
    by_path: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(value["modules"]):
        entry_issue_start = len(out)
        if not isinstance(item, dict):
            out.append(
                finding(
                    "TE.OWNERSHIP_ENTRY", path, f"modules[{index}] must be an object"
                )
            )
            continue
        allowed = {"path", "mode", "evidence_class", "sut", "artifact"}
        if not set(item) <= allowed:
            out.append(
                finding(
                    "TE.OWNERSHIP_KEYS", path, f"modules[{index}] has unexpected keys"
                )
            )
        raw_path = item.get("path")
        if not isinstance(raw_path, str) or not raw_path:
            out.append(
                finding(
                    "TE.OWNERSHIP_PATH",
                    path,
                    f"modules[{index}].path must be a nonempty string",
                )
            )
            continue
        if raw_path in seen_paths:
            out.append(
                finding(
                    "TE.DUPLICATE_OWNERSHIP_PATH",
                    path,
                    f"duplicate ownership path {raw_path!r}",
                )
            )
            continue
        seen_paths.add(raw_path)
        mode = item.get("mode")
        if mode not in {"class_owned", "artifact_owned"}:
            out.append(
                finding("TE.OWNERSHIP_MODE", path, f"modules[{index}].mode is invalid")
            )
        if item.get("evidence_class") not in EVIDENCE_OPENINGS:
            out.append(
                finding(
                    "TE.EVIDENCE_CLASS",
                    path,
                    f"modules[{index}].evidence_class is invalid",
                )
            )
        if mode == "class_owned":
            if (
                set(item) != {"path", "mode", "evidence_class", "sut"}
                or not isinstance(item.get("sut"), str)
                or not item["sut"]
            ):
                out.append(
                    finding(
                        "TE.OWNERSHIP_SUT",
                        path,
                        f"modules[{index}] requires only a nonempty string sut",
                    )
                )
        elif mode == "artifact_owned" and (
            set(item) != {"path", "mode", "evidence_class", "artifact"}
            or not isinstance(item.get("artifact"), str)
            or not item["artifact"].strip()
        ):
            out.append(
                finding(
                    "TE.OWNERSHIP_ARTIFACT",
                    path,
                    f"modules[{index}] requires only a concrete nonempty artifact",
                )
            )
        if len(out) == entry_issue_start:
            by_path[raw_path] = item
    if set(by_path) != set(supplied):
        out.append(
            finding(
                "TE.OWNERSHIP_COVERAGE",
                path,
                "ownership paths must exactly equal explicitly supplied paths",
            )
        )
    return value["modules"], by_path, out


def validate_migration(
    path: str, payload: bytes | None, read_error: str | None
) -> list[PythonTestEvidenceFinding]:
    """Validate a closed, complete one-to-one old/new node inventory and map."""
    out: list[PythonTestEvidenceFinding] = []
    if read_error is not None:
        return [finding("TE.MIGRATION_INPUT", path, read_error)]
    assert payload is not None
    try:
        value = json.loads(payload.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        return [finding("TE.MIGRATION_INPUT", path, str(exc))]
    required = {
        "schema_version",
        "expected_old_node_ids",
        "expected_new_node_ids",
        "mappings",
    }
    if (
        not isinstance(value, dict)
        or set(value) != required
        or value.get("schema_version") != 1
    ):
        return [
            finding(
                "TE.MIGRATION_INPUT",
                path,
                "migration input must have the exact schema-version-1 keys",
            )
        ]
    old_expected, new_expected, mappings = (
        value.get("expected_old_node_ids"),
        value.get("expected_new_node_ids"),
        value.get("mappings"),
    )
    for label, inventory in (("old", old_expected), ("new", new_expected)):
        if (
            not isinstance(inventory, list)
            or any(not isinstance(item, str) or not item for item in inventory)
            or len(inventory) != len(set(inventory))
        ):
            out.append(
                finding(
                    "TE.MIGRATION_INVENTORY",
                    path,
                    f"expected {label} inventory must contain unique nonempty strings",
                )
            )
    if not isinstance(mappings, list):
        out.append(finding("TE.MIGRATION_INPUT", path, "mappings must be a list"))
        return out
    pairs: list[tuple[str, str]] = []
    for index, item in enumerate(mappings):
        if (
            not isinstance(item, dict)
            or set(item) != {"old_node_id", "new_node_id"}
            or not isinstance(item.get("old_node_id"), str)
            or not item.get("old_node_id")
            or not isinstance(item.get("new_node_id"), str)
            or not item.get("new_node_id")
        ):
            out.append(
                finding(
                    "TE.MIGRATION_ENTRY",
                    path,
                    f"mappings[{index}] must be one exact nonempty old/new pair",
                )
            )
            continue
        pairs.append((item["old_node_id"], item["new_node_id"]))
    old_actual = [item[0] for item in pairs]
    new_actual = [item[1] for item in pairs]
    if len(old_actual) != len(set(old_actual)) or len(new_actual) != len(
        set(new_actual)
    ):
        out.append(
            finding(
                "TE.MIGRATION_ONE_TO_ONE", path, "mapping sides must both be unique"
            )
        )
    if (
        isinstance(old_expected, list)
        and isinstance(new_expected, list)
        and (
            set(old_actual) != set(old_expected)
            or set(new_actual) != set(new_expected)
            or len(pairs) != len(old_expected)
            or len(pairs) != len(new_expected)
        )
    ):
        out.append(
            finding(
                "TE.MIGRATION_INCOMPLETE",
                path,
                "mapping must exactly cover both expected node inventories",
            )
        )
    return out


@dataclass(frozen=True, slots=True)
class PythonTestEvidenceValidationResult:
    """Immutable compatibility-complete structural validation result.

    The scalar count fields and sorted key/count tuples represent the legacy
    command's ``counts`` object without exposing mutable dictionaries.  ``paths``
    preserves request order, and ``findings`` preserves the deterministic rule
    and source traversal order.

    Attributes
    ----------
    schema_version
        Result contract version, fixed to ``1``.
    status
        ``"PASS"`` when ``findings`` is empty, otherwise ``"FAIL"``.
    claim_boundary
        Ordered tuple of conclusions explicitly not established by this result.
    paths
        Supplied module paths in request order.
    findings
        Structured expected-invalidity findings in deterministic traversal order.
    artifact_owned_modules, class_owned_modules
        Counts derived from all syntactically object-shaped ownership entries.
    evidence_class_modules
        Sorted evidence-class/count pairs.
    findings_by_code
        Sorted finding-code/count pairs.
    helper_functions, modules, parameterized_functions, test_functions
        Static module and top-level-function inventory counts.
    static_collected_parameter_cases
        Static parameter-case count, or ``None`` if any count is unresolved.
    unique_evidence_owners
        Number of unique evidence identifiers retained during validation.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If status, ordering, version, or a nonnegative-count invariant fails.
    """

    schema_version: int
    status: str
    claim_boundary: tuple[str, ...]
    paths: tuple[str, ...]
    findings: tuple[PythonTestEvidenceFinding, ...]
    artifact_owned_modules: int
    class_owned_modules: int
    evidence_class_modules: tuple[tuple[str, int], ...]
    findings_by_code: tuple[tuple[str, int], ...]
    helper_functions: int
    modules: int
    parameterized_functions: int
    static_collected_parameter_cases: int | None
    test_functions: int
    unique_evidence_owners: int

    def __post_init__(self) -> None:
        if type(self.schema_version) is not int:
            raise TypeError("schema_version must be an int excluding bool")
        if self.schema_version != 1:
            raise ValueError("schema_version must equal 1")
        _require_builtin_str(self.status, "status")
        _require_tuple(self.claim_boundary, "claim_boundary")
        _require_tuple(self.paths, "paths")
        _require_tuple(self.findings, "findings")
        _require_tuple(self.evidence_class_modules, "evidence_class_modules")
        _require_tuple(self.findings_by_code, "findings_by_code")
        if any(type(item) is not str for item in self.claim_boundary + self.paths):
            raise TypeError("claim_boundary and paths must contain strings")
        if any(type(item) is not PythonTestEvidenceFinding for item in self.findings):
            raise TypeError("findings must contain PythonTestEvidenceFinding values")
        if self.status != ("PASS" if not self.findings else "FAIL"):
            raise ValueError("status must agree with findings")
        for name in (
            "artifact_owned_modules",
            "class_owned_modules",
            "helper_functions",
            "modules",
            "parameterized_functions",
            "test_functions",
            "unique_evidence_owners",
        ):
            value = getattr(self, name)
            if type(value) is not int:
                raise TypeError(f"{name} must be an int excluding bool")
            if value < 0:
                raise ValueError(f"{name} must be nonnegative")
        if self.static_collected_parameter_cases is not None:
            if type(self.static_collected_parameter_cases) is not int:
                raise TypeError(
                    "static_collected_parameter_cases must be an int excluding "
                    "bool or None"
                )
            if self.static_collected_parameter_cases < 0:
                raise ValueError("static_collected_parameter_cases must be nonnegative")
        for name in ("evidence_class_modules", "findings_by_code"):
            values = getattr(self, name)
            if tuple(sorted(values)) != values:
                raise ValueError(f"{name} must be sorted")
            if any(
                type(key) is not str or type(count) is not int or count < 0
                for key, count in values
            ):
                raise TypeError(f"{name} must contain str/nonnegative-int pairs")


class ValidatePythonTestEvidence:
    """Validate explicit Python source and metadata bytes without performing I/O.

    The fieldless action owns all relational and static-analysis policy.  It has
    no configuration, retained state, mutation, or environmental dependency.
    """

    __slots__ = ()

    def execute(
        self, request: PythonTestEvidenceRequest
    ) -> PythonTestEvidenceValidationResult:
        """Validate one closed request.

        Parameters
        ----------
        request
            Explicit module, ownership, and optional migration-map inputs.

        Returns
        -------
        PythonTestEvidenceValidationResult
            Immutable findings and compatibility-complete inventory counts.
            Malformed supplied evidence is represented as findings, not raised.

        Raises
        ------
        TypeError
            If ``request`` is not exactly :class:`PythonTestEvidenceRequest`.
        """
        if type(request) is not PythonTestEvidenceRequest:
            raise TypeError("request must be PythonTestEvidenceRequest")
        findings: list[PythonTestEvidenceFinding] = []
        supplied = [source.path for source in request.sources]
        if len(supplied) != len(set(supplied)):
            findings.append(
                finding(
                    "TE.DUPLICATE_PATH",
                    request.ownership_path,
                    "supplied paths must be unique",
                )
            )
        entries, by_path, ownership_findings = load_ownership(
            request.ownership_path,
            request.ownership_payload,
            request.ownership_read_error,
            supplied,
        )
        findings.extend(ownership_findings)
        seen: dict[str, str] = {}
        for source in request.sources:
            if not source.is_regular_file:
                findings.append(
                    finding(
                        "TE.EXPLICIT_PATH",
                        source.path,
                        "supplied path must be a regular file",
                    )
                )
                continue
            owner = by_path.get(source.path)
            if owner is not None:
                findings.extend(validate_file(source, owner, seen))
        if request.migration_path is not None:
            findings.extend(
                validate_migration(
                    request.migration_path,
                    request.migration_payload,
                    request.migration_read_error,
                )
            )
        tests = helpers = parameterized = 0
        static_parameter_cases = 0
        static_parameter_cases_known = True
        for source in request.sources:
            if not source.is_regular_file or source.payload is None:
                continue
            try:
                tree = ast.parse(source.payload.decode("utf-8"))
            except UnicodeError, SyntaxError:
                continue
            functions = [
                node
                for node in tree.body
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            ]
            tests += sum(node.name.startswith("test_") for node in functions)
            helpers += sum(not node.name.startswith("test_") for node in functions)
            for node in functions:
                count = static_parameter_case_count(node, tree)
                if count is None:
                    static_parameter_cases_known = False
                elif count:
                    parameterized += 1
                    static_parameter_cases += count
        findings_by_code: dict[str, int] = {}
        for item in findings:
            findings_by_code[item.code] = findings_by_code.get(item.code, 0) + 1
        ownership_counts = {
            kind: sum(
                item.get("mode") == kind for item in entries if isinstance(item, dict)
            )
            for kind in ("class_owned", "artifact_owned")
        }
        evidence_class_counts = {
            kind: sum(
                item.get("evidence_class") == kind
                for item in entries
                if isinstance(item, dict)
            )
            for kind in EVIDENCE_OPENINGS
        }
        return PythonTestEvidenceValidationResult(
            1,
            "PASS" if not findings else "FAIL",
            (
                "oracle independence",
                "mathematical correctness",
                "property/surface correctness",
                "test cohesion",
                "tolerance adequacy",
                "scientific validity",
                "uncertainty quantification",
                "human acceptance",
            ),
            tuple(supplied),
            tuple(findings),
            ownership_counts["artifact_owned"],
            ownership_counts["class_owned"],
            tuple(sorted(evidence_class_counts.items())),
            tuple(sorted(findings_by_code.items())),
            helpers,
            len(request.sources),
            parameterized,
            static_parameter_cases if static_parameter_cases_known else None,
            tests,
            len(seen),
        )
