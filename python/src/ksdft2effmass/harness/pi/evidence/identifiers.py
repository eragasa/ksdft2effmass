"""Caller-supplied Python evidence-identifier auditing."""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..identity import (
    Identifier,
    ResourcePath,
    _require_identifier,
    _require_path,
    _require_tuple,
    _require_version,
)
from ..validation import ValidationResult, _issue, _result

if TYPE_CHECKING:
    from ..profiles import ProjectProfile


@dataclass(frozen=True, slots=True)
class IdentifierOccurrence:
    """One retained evidence identifier occurrence at a one-based source line.

    Attributes
    ----------
    schema_version
        Record contract version, fixed to ``1``.
    evidence_id
        Identifier declared by one evidence-owning Python test function.
    path
        Caller-supplied resource path of the containing Python module.
    line
        Positive one-based line of the owning test function.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If a value violates the version, identifier, path, or line contract.
    """

    schema_version: int
    evidence_id: Identifier
    path: ResourcePath
    line: int

    def __post_init__(self) -> None:
        if _require_version(self.schema_version, "schema_version") != 1:
            raise ValueError("schema_version must equal 1")
        _require_identifier(self.evidence_id, "evidence_id")
        _require_path(self.path, "path")
        _require_version(self.line, "line")


@dataclass(frozen=True, slots=True)
class IdentifierAuditResult:
    """Immutable occurrences and validation from one identifier audit.

    Attributes
    ----------
    occurrences
        Deterministically sorted occurrences. A failed validation has none.
    validation
        Structural validation result for the supplied modules and profile.

    Raises
    ------
    TypeError
        If an occurrence or validation value has the wrong semantic type.
    ValueError
        If occurrences are unsorted or coexist with failed validation.
    """

    occurrences: tuple[IdentifierOccurrence, ...]
    validation: ValidationResult

    def __post_init__(self) -> None:
        _require_tuple(self.occurrences, "occurrences")
        if any(type(value) is not IdentifierOccurrence for value in self.occurrences):
            raise TypeError("occurrences have wrong type")
        if (
            tuple(
                sorted(
                    self.occurrences,
                    key=lambda value: (value.evidence_id, value.path, value.line),
                )
            )
            != self.occurrences
        ):
            raise ValueError("occurrences are not sorted")
        if type(self.validation) is not ValidationResult:
            raise TypeError("validation has wrong type")
        if self.validation.status == "FAIL" and self.occurrences:
            raise ValueError("failed result must have empty occurrences")


def _dotted(node: ast.expr) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _dotted(node.value)
        return f"{parent}.{node.attr}" if parent else None
    return None


def _markers(tree: ast.Module) -> tuple[str, ...]:
    found = []
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        if not any(isinstance(t, ast.Name) and t.id == "pytestmark" for t in targets):
            continue
        value = node.value
        if value is None:
            continue
        values = value.elts if isinstance(value, (ast.List, ast.Tuple)) else [value]
        for item in values:
            name = _dotted(item)
            if name:
                found.append(name.rsplit(".", 1)[-1])
    return tuple(found)


_EVIDENCE_ID = re.compile(r"\b([A-Za-z0-9][A-Za-z0-9._:/-]*-\d+)\b")
_EVIDENCE_RANGE = re.compile(
    r"(?P<start>[A-Za-z0-9][A-Za-z0-9._:/-]*-\d+)(?:``)?\s+through\s+"
    r"(?:``)?(?P<end>[A-Za-z0-9][A-Za-z0-9._:/-]*-\d+)"
)


@dataclass(frozen=True, slots=True)
class _EvidenceDeclaration:
    ids: tuple[str, ...]
    issue_code: str | None = None
    issue_message: str | None = None
    missing: bool = False


def _declaration(doc: str) -> _EvidenceDeclaration:
    """Parse one normalized fielded or historical owner declaration."""
    matches = list(re.finditer(r"(?m)^Evidence ID:\s*(?P<value>.*)$", doc))
    if len(matches) > 1:
        return _EvidenceDeclaration(
            (),
            "PIH.EVIDENCE.ID_INVALID",
            "Test function has multiple Evidence ID fields.",
        )
    if matches:
        declaration = matches[0].group("value").strip()
        if not declaration:
            return _EvidenceDeclaration(
                (),
                "PIH.EVIDENCE.ID_INVALID",
                "Evidence ID field is empty.",
            )
    else:
        declaration = doc.splitlines()[0].strip() if doc else ""
        if not declaration:
            return _EvidenceDeclaration((), missing=True)

    ranges = list(_EVIDENCE_RANGE.finditer(declaration))
    if len(ranges) > 1:
        return _EvidenceDeclaration(
            (),
            "PIH.EVIDENCE.RANGE_CONFLICT",
            "Owner declares multiple evidence ranges.",
        )
    if ranges:
        match = ranges[0]
        start_id = match.group("start")
        end_id = match.group("end")
        start_prefix, start_number = start_id.rsplit("-", 1)
        end_prefix, end_number = end_id.rsplit("-", 1)
        remainder = declaration[: match.start()] + declaration[match.end() :]
        if _EVIDENCE_ID.search(remainder):
            return _EvidenceDeclaration(
                (),
                "PIH.EVIDENCE.RANGE_CONFLICT",
                "Evidence range includes an independent identifier.",
            )
        if (
            start_prefix != end_prefix
            or len(start_number) != len(end_number)
            or int(start_number) > int(end_number)
        ):
            return _EvidenceDeclaration(
                (),
                "PIH.EVIDENCE.RANGE_CONFLICT",
                "Evidence range is invalid.",
            )
        return _EvidenceDeclaration(
            tuple(
                f"{start_prefix}-{number:0{len(start_number)}d}"
                for number in range(int(start_number), int(end_number) + 1)
            )
        )

    identifiers = tuple(sorted(set(_EVIDENCE_ID.findall(declaration))))
    if len(identifiers) > 1:
        return _EvidenceDeclaration(
            (),
            "PIH.EVIDENCE.RANGE_CONFLICT",
            "Owner declares multiple IDs without one range.",
        )
    if not identifiers:
        return _EvidenceDeclaration(
            (),
            "PIH.EVIDENCE.ID_INVALID",
            "Test function has no valid evidence owner.",
        )
    return _EvidenceDeclaration(identifiers)


class IdentifierAuditor:
    """Audit supplied module bytes against explicit profile namespace policy.

    The fieldless action performs no file discovery or I/O. It owns marker,
    namespace, identifier-range, ownership, and duplicate detection for the
    exact module bytes and profile supplied to :meth:`execute`.
    """

    __slots__ = ()

    def execute(
        self, modules: tuple[tuple[ResourcePath, bytes], ...], profile: ProjectProfile
    ) -> IdentifierAuditResult:
        """Audit one nonempty explicit module collection.

        Parameters
        ----------
        modules
            Path/UTF-8-byte pairs. Paths are sorted before deterministic audit.
        profile
            Explicit project profile defining scopes, markers, namespaces, and
            protected unowned functions.

        Returns
        -------
        IdentifierAuditResult
            Sorted occurrences on success or warning, and structured validation.
            Failed results contain no occurrences.

        Raises
        ------
        TypeError
            If the profile, collection, entry, path, or payload has the wrong
            semantic type.
        ValueError
            If the module collection is empty or an identifier/path is invalid.
        """
        from ..profiles import ProjectProfile

        _require_tuple(modules, "modules")
        if not modules:
            raise ValueError("modules must be nonempty")
        if type(profile) is not ProjectProfile:
            raise TypeError("profile has wrong type")
        rules = {
            prefix: (minimum, maximum, width)
            for prefix, minimum, maximum, width in profile.evidence_namespace_rules
        }
        occurrences: list[IdentifierOccurrence] = []
        issues = []
        owners: dict[str, list[IdentifierOccurrence]] = {}
        protected = set(profile.protected_unowned_functions)
        for module in sorted(modules, key=lambda x: x[0]):
            if type(module) is not tuple or len(module) != 2:
                raise TypeError("module entries must be path/bytes pairs")
            path, payload = module
            _require_path(path, "module path")
            if type(payload) is not bytes:
                raise TypeError("module payload must be bytes")
            try:
                source = payload.decode("utf-8")
                tree = ast.parse(source, filename=path)
            except UnicodeDecodeError, SyntaxError:
                issues.append(
                    _issue(
                        "PIH.EVIDENCE.SOURCE_INVALID",
                        "Python source is invalid.",
                        path=path,
                    )
                )
                continue
            matching = [
                rule for rule in profile.evidence_scope_rules if rule[0].contains(path)
            ]
            if len(matching) != 1:
                issues.append(
                    _issue(
                        "PIH.EVIDENCE.NAMESPACE_UNDECLARED",
                        "Module is outside one declared evidence scope.",
                        path=path,
                    )
                )
                continue
            scope, required_marker, allowed = matching[0]
            declared = _markers(tree)
            if declared != (required_marker,):
                issues.append(
                    _issue(
                        "PIH.EVIDENCE.MARKER_UNDECLARED",
                        "Module marker does not match its scope.",
                        path=path,
                        related_ids=(required_marker,),
                    )
                )
            for node in tree.body:
                if not isinstance(
                    node, (ast.FunctionDef, ast.AsyncFunctionDef)
                ) or not node.name.startswith("test_"):
                    continue
                declaration = _declaration(ast.get_docstring(node, clean=True) or "")
                if declaration.issue_code is not None:
                    issues.append(
                        _issue(
                            declaration.issue_code,
                            declaration.issue_message
                            or "Evidence declaration is invalid.",
                            path=path,
                        )
                    )
                    continue
                if declaration.missing:
                    code = (
                        "PIH.EVIDENCE.PROTECTED_GAP"
                        if (path, node.name) in protected
                        else "PIH.EVIDENCE.ID_INVALID"
                    )
                    issues.append(
                        _issue(
                            code,
                            "Test function has no valid evidence owner.",
                            path=path,
                        )
                    )
                    continue
                for eid in declaration.ids:
                    try:
                        prefix, number = eid.rsplit("-", 1)
                        _require_identifier(eid, "evidence_id")
                    except TypeError, ValueError:
                        issues.append(
                            _issue(
                                "PIH.EVIDENCE.ID_INVALID",
                                "Evidence ID syntax is invalid.",
                                path=path,
                            )
                        )
                        continue
                    if prefix not in rules or prefix not in allowed:
                        issues.append(
                            _issue(
                                "PIH.EVIDENCE.NAMESPACE_UNDECLARED",
                                "Evidence namespace is not allowed for module.",
                                eid,
                                path,
                            )
                        )
                        continue
                    minimum, maximum, width = rules[prefix]
                    if (
                        len(number) != width
                        or not number.isascii()
                        or not number.isdigit()
                        or not minimum <= int(number) <= maximum
                    ):
                        issues.append(
                            _issue(
                                "PIH.EVIDENCE.ID_INVALID",
                                "Evidence ID is outside its declared range/width.",
                                eid,
                                path,
                            )
                        )
                        continue
                    occurrence = IdentifierOccurrence(1, eid, path, node.lineno)
                    occurrences.append(occurrence)
                    owners.setdefault(eid, []).append(occurrence)
        for eid, items in owners.items():
            if len(items) > 1:
                issues.append(
                    _issue(
                        "PIH.EVIDENCE.ID_DUPLICATE",
                        "Evidence ID has multiple owners.",
                        eid,
                        related_ids=tuple(sorted({x.path for x in items})),
                    )
                )
        validation = _result(tuple(issues))
        return IdentifierAuditResult(
            ()
            if validation.status == "FAIL"
            else tuple(
                sorted(occurrences, key=lambda x: (x.evidence_id, x.path, x.line))
            ),
            validation,
        )
