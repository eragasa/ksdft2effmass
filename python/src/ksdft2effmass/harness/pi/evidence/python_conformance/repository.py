"""Independent repository-conformance rule owner over immutable facts."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .documentation import section_body
from .model import PythonTestModuleModel

_UNKNOWN = {"unknown", "unsupported", "unrecognized"}
_WRONG = {"boolean", "bytes", "float", "integer", "none", "string", "wrong_type"}
_COMPLETENESS = re.compile(r"\b(?:all|complete|entire|every|field-complete)\b")
_STATE = re.compile(r"\b(?:dataclass state|public state|represented state|fields?)\b")
_EQUALITY = re.compile(
    r"\b(?:equality|compares?|distinguishes?|equal exactly|makes? them unequal)\b"
)
_FROZEN = re.compile(
    r"\b(?:frozen|immutable|rejects? post-construction assignment|assignments? raise)\b"
)


def _function_counts(model: PythonTestModuleModel) -> tuple[int, int]:
    """Return top-level test and helper counts."""
    tests = sum(function.is_test for function in model.functions)
    return tests, len(model.functions) - tests


def _validate_repository_conformance(
    model: PythonTestModuleModel,
) -> tuple[tuple[str, str, int | None], ...]:
    """Validate cross-cutting static repository conventions."""
    findings: list[tuple[str, str, int | None]] = []
    if re.search(r"(?m)^#\s*ruff:\s*noqa:\s*E501\s*$", model.source):
        findings.append(
            (
                "TE.BLANKET_SUPPRESSION",
                "file-level E501 suppression is prohibited; use ordinary formatting or one targeted justified suppression",  # noqa: E501
                None,
            )
        )
    for function in model.functions:
        if function.calls_sut and function.indexes_sut:
            findings.append(
                (
                    "TE.MIXED_ENUM_LOOKUP",
                    "one owner combines EnumType(value) construction with EnumType[name] lookup",  # noqa: E501
                    function.line,
                )
            )
        if function.circular_member_lookup and function.indexes_sut:
            findings.append(
                (
                    "TE.CIRCULAR_ENUM_ORACLE",
                    "successful name lookup must not derive its sole expected member from SUT.__members__",  # noqa: E501
                    function.line,
                )
            )
        raw_ids = tuple(
            case_id
            for item in function.parameterizations
            for case_id in (
                *item.decorator_ids,
                *(
                    case.literal_id
                    for case in item.cases
                    if case.literal_id is not None
                ),
            )
        )
        ids = {word for case_id in raw_ids for word in case_id.split("_")}
        if ids & _UNKNOWN and any(
            word in case_id for case_id in raw_ids for word in _WRONG
        ):
            findings.append(
                (
                    "TE.MIXED_INVALID_PARTITION",
                    "one parameter family combines unknown accepted-type values with wrong-semantic-type values",  # noqa: E501
                    function.line,
                )
            )
        if function.has_loop:
            findings.append(
                (
                    "TE.HIDDEN_LOOP",
                    "test/helper contains a loop that hides collected case identity",
                    function.line,
                )
            )
        requirement = section_body(function.doc, "Requirement").lower()
        equality = (
            ("__eq__" in function.name or _EQUALITY.search(requirement))
            and _COMPLETENESS.search(requirement)
            and _STATE.search(requirement)
        )
        frozen = (
            (
                "frozen" in function.name
                or "immutable" in function.name
                or (
                    _FROZEN.search(requirement)
                    and re.search(
                        r"\b(?:assignment|reassignment|mutation|frozen)\b", requirement
                    )
                )
            )
            and _COMPLETENESS.search(requirement)
            and _STATE.search(requirement)
        )
        if equality and model.equality_fields is None:
            findings.append(
                (
                    "TE.EQUALITY_FIELD_INVENTORY",
                    "complete-equality claims require one literal EQUALITY_FIELDS inventory",  # noqa: E501
                    function.line,
                )
            )
        if frozen and model.frozen_fields is None:
            findings.append(
                (
                    "TE.FROZEN_FIELD_INVENTORY",
                    "all-fields-frozen claims require one literal FROZEN_FIELDS inventory",  # noqa: E501
                    function.line,
                )
            )
    return tuple(findings)


@dataclass(frozen=True, slots=True)
class _PythonRepositoryConformanceRuleResult:
    """Immutable repository-conformance findings and function counts."""

    findings: tuple[tuple[str, str, int | None], ...]
    test_functions: int
    helper_functions: int


class _PythonRepositoryConformanceRule:
    """Own repository uniqueness and cross-cutting conformance policy."""

    __slots__ = ()

    def execute(
        self, model: PythonTestModuleModel
    ) -> _PythonRepositoryConformanceRuleResult:
        """Validate one model and derive its deterministic function inventory."""
        tests, helpers = _function_counts(model)
        return _PythonRepositoryConformanceRuleResult(
            _validate_repository_conformance(model), tests, helpers
        )


class _PythonRepositoryUniquenessRule:
    """Own uniqueness of explicitly selected repository module paths."""

    __slots__ = ()

    def execute(self, paths: tuple[str, ...]) -> tuple[tuple[str, str], ...]:
        """Return the compatibility duplicate-path finding, if applicable."""
        if len(paths) != len(set(paths)):
            return (("TE.DUPLICATE_PATH", "supplied paths must be unique"),)
        return ()
