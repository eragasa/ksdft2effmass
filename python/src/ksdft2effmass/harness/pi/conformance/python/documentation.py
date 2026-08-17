"""Independent module and exact paragraph-grammar rule owner."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .model import PythonTestFunctionFact, PythonTestModuleModel
from .profile import EvidenceProfileMatrix

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
    "Provenance",
)
LEGACY_REQUIRED_FIELDS = FIELDS[:-1]


def _paragraphs(doc: str, fields: tuple[str, ...]) -> tuple[dict[str, str], str | None]:
    """Parse exact ``Label: value`` paragraphs separated by one blank line."""
    known = "|".join(map(re.escape, FIELDS))
    matches = list(
        re.finditer(rf"(?m)^[ \t]*(?P<label>{known}):[ \t]+(?P<value>\S.*)$", doc)
    )
    values: dict[str, str] = {}
    declarations = list(
        re.finditer(rf"(?m)^[ \t]*(?P<label>{known}):(?P<tail>.*)$", doc)
    )
    for declaration in declarations:
        if not re.match(r"[ \t]+\S", declaration.group("tail")):
            label = declaration.group("label")
            return {}, f"{label!r} must occur as one 'Label: value' paragraph"
    for index, match in enumerate(matches):
        label = match.group("label")
        if label in values:
            return {}, f"{label!r} must occur as one 'Label: value' paragraph"
        next_start = (
            matches[index + 1].start() if index + 1 < len(matches) else len(doc)
        )
        body = doc[match.end() : next_start]
        if index + 1 < len(matches) and not re.search(r"(?<!\n)\n\n\Z", body):
            return {}, "evidence paragraphs must be separated by one blank line"
        values[label] = f"{match.group('value')}\n{body}".strip()
    for field in fields:
        if field not in values:
            return {}, f"{field!r} must occur as one 'Label: value' paragraph"
    positions = [FIELDS.index(label) for label in values]
    if positions != sorted(positions):
        return {}, "evidence fields are out of canonical order"
    return values, None


def section_body(doc: str, label: str) -> str:
    """Return one exact evidence paragraph body."""
    values, _problem = _paragraphs(doc, ())
    return values.get(label, "")


def _validate_module_documentation(
    model: PythonTestModuleModel, profile: str | None
) -> tuple[tuple[str, str, int | None], ...]:
    """Validate headings and explicit bounded profile declarations."""
    doc = model.module_doc or ""
    findings: list[tuple[str, str, int | None]] = []
    positions: list[int] = []
    matches: list[re.Match[str]] = []
    for heading in HEADINGS:
        found = list(re.finditer(rf"(?m)^[ \t]*{re.escape(heading)}[ \t]*$", doc))
        if len(found) != 1:
            findings.append(
                ("TE.MODULE_DOC", f"{heading!r} must occur exactly once", None)
            )
            break
        positions.append(found[0].start())
        matches.append(found[0])
    if not findings and positions != sorted(positions):
        findings.append(("TE.MODULE_DOC", "required sections are out of order", None))
    if not findings:
        for index, match in enumerate(matches):
            end = matches[index + 1].start() if index + 1 < len(matches) else len(doc)
            body = doc[match.end() : end]
            if not re.match(r"\n\n(?!\n)", body) or (
                index + 1 < len(matches) and not re.search(r"(?<!\n)\n\n\Z", body)
            ):
                findings.append(
                    (
                        "TE.MODULE_DOC",
                        "module sections must use exactly one separating blank line",
                        None,
                    )
                )
                break
            if not body.strip():
                findings.append(
                    ("TE.MODULE_DOC", f"{HEADINGS[index]!r} has an empty body", None)
                )
                break
    for heading in SUPERSEDED_HEADINGS:
        if re.search(rf"(?m)^\s*{re.escape(heading)}\s*$", doc):
            findings.append(
                (
                    "TE.SUPERSEDED_HEADING",
                    f"superseded heading is prohibited: {heading}",
                    None,
                )
            )
    if profile is not None:
        expected = f"Evidence profile: {profile}"
        if doc.splitlines().count(expected) != 1:
            findings.append(
                ("TE.PROFILE_DECLARATION", f"module must declare {expected!r}", None)
            )
        if len(re.findall(r"(?m)^Bounded artifact scope:\s+\S.*$", doc)) != 1:
            findings.append(
                (
                    "TE.PROFILE_DECLARATION",
                    "module must declare one nonempty Bounded artifact scope",
                    None,
                )
            )
    return tuple(findings)


def _validate_function_documentation(
    function: PythonTestFunctionFact,
    profile: str | None,
    matrix: EvidenceProfileMatrix | None,
) -> tuple[tuple[str, str, int | None], ...]:
    """Validate required and present optional fields with identical exact grammar."""
    required: tuple[str, ...] = LEGACY_REQUIRED_FIELDS
    allowed = set(FIELDS)
    forbidden: set[str] = set()
    if profile is not None and matrix is not None and profile in matrix.profiles:
        policy = matrix.profiles[profile]
        required = tuple(
            field for field in FIELDS if field in policy.required_test_fields
        )
        allowed = set(policy.required_test_fields + policy.optional_test_fields)
        forbidden = set(policy.forbidden_test_fields)
    values, problem = _paragraphs(function.doc, required)
    if problem:
        return (("TE.FUNCTION_DOC", problem, function.line),)
    for field in values:
        if field in forbidden:
            return (
                (
                    "TE.FUNCTION_DOC",
                    f"forbidden evidence field is present: {field}",
                    function.line,
                ),
            )
        if field not in allowed:
            return (
                (
                    "TE.FUNCTION_DOC",
                    f"undeclared evidence field is present: {field}",
                    function.line,
                ),
            )
    findings: list[tuple[str, str, int | None]] = []
    if re.search(r"(?:!!|\?\?|(?<!\.)\.\.(?!\.))", function.doc):
        findings.append(
            (
                "TE.PROSE_PUNCTUATION",
                "evidence prose contains doubled terminal punctuation",
                function.line,
            )
        )
    if re.search(r"(?i)(?:\bTODO\b|\bTBD\b|<placeholder>)", function.doc):
        findings.append(
            (
                "TE.PLACEHOLDER_PROSE",
                "evidence prose contains placeholder language",
                function.line,
            )
        )
    return tuple(findings)


@dataclass(frozen=True, slots=True)
class _PythonDocumentationRuleResult:
    """Immutable module and function documentation findings."""

    module_findings: tuple[tuple[str, str, int | None], ...]
    function_findings: tuple[tuple[str, str, int | None], ...]


class _PythonDocumentationRule:
    """Own module documentation and exact paragraph grammar policy."""

    __slots__ = ()

    def execute(
        self,
        model: PythonTestModuleModel,
        profile: str | None,
        matrix: EvidenceProfileMatrix | None,
    ) -> _PythonDocumentationRuleResult:
        """Validate module prose and every required or present optional paragraph."""
        return _PythonDocumentationRuleResult(
            _validate_module_documentation(model, profile),
            tuple(
                item
                for function in model.functions
                for item in _validate_function_documentation(function, profile, matrix)
            ),
        )
