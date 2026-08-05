"""Caller-supplied Python evidence-identifier auditing."""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .identity import (
    Identifier,
    ResourcePath,
    _require_identifier,
    _require_path,
    _require_tuple,
    _require_version,
)
from .validation import EvidenceAuditResult, _issue, _result

if TYPE_CHECKING:
    from .profiles import ProjectProfile


@dataclass(frozen=True, slots=True)
class EvidenceIdentifierOccurrence:
    """One retained evidence identifier occurrence at a one-based source line."""

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


def _declaration(doc: str) -> str:
    matches = list(re.finditer(r"(?m)^Evidence ID\s*$", doc))
    if len(matches) > 1:
        return ""
    if not matches:
        return doc.splitlines()[0] if doc else ""
    start = matches[0].end()
    end = re.search(r"(?m)^Requirement\s*$", doc[start:])
    return (
        doc[start : start + end.start()].strip()
        if end
        else doc.splitlines()[0]
        if doc
        else ""
    )


class AuditEvidenceIdentifiers:
    """Audit supplied module bytes against explicit profile namespace policy."""

    __slots__ = ()

    def execute(
        self, modules: tuple[tuple[ResourcePath, bytes], ...], profile: ProjectProfile
    ) -> EvidenceAuditResult:
        from .profiles import ProjectProfile

        _require_tuple(modules, "modules")
        if type(profile) is not ProjectProfile:
            raise TypeError("profile has wrong type")
        rules = {
            prefix: (minimum, maximum, width)
            for prefix, minimum, maximum, width in profile.evidence_namespace_rules
        }
        occurrences: list[EvidenceIdentifierOccurrence] = []
        issues = []
        owners: dict[str, list[EvidenceIdentifierOccurrence]] = {}
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
                declaration = _declaration(ast.get_docstring(node, clean=False) or "")
                found = re.findall(
                    r"\b([A-Za-z0-9][A-Za-z0-9._:/-]*-\d+)\b", declaration
                )
                range_match = re.search(
                    r"([A-Za-z0-9][A-Za-z0-9._:/-]*-\d+)\s*(?:``)?\s+through\s+(?:``)?\s*([A-Za-z0-9][A-Za-z0-9._:/-]*-\d+)",
                    declaration,
                )
                ids = []
                if range_match:
                    a, b = range_match.groups()
                    ap, an = a.rsplit("-", 1)
                    bp, bn = b.rsplit("-", 1)
                    if ap == bp and int(an) <= int(bn):
                        ids = [
                            f"{ap}-{n:0{len(an)}d}" for n in range(int(an), int(bn) + 1)
                        ]
                    else:
                        issues.append(
                            _issue(
                                "PIH.EVIDENCE.RANGE_CONFLICT",
                                "Evidence range is invalid.",
                                path=path,
                            )
                        )
                else:
                    ids = sorted(set(found))
                if len(ids) > 1 and not range_match:
                    issues.append(
                        _issue(
                            "PIH.EVIDENCE.RANGE_CONFLICT",
                            "Owner declares multiple IDs without one range.",
                            path=path,
                        )
                    )
                if not ids:
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
                for eid in ids:
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
                    occurrence = EvidenceIdentifierOccurrence(1, eid, path, node.lineno)
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
        return EvidenceAuditResult(
            ()
            if validation.status == "FAIL"
            else tuple(
                sorted(occurrences, key=lambda x: (x.evidence_id, x.path, x.line))
            ),
            validation,
        )
