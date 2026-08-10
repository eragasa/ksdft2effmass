"""Independent AST-free parameterization rule owner."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .model import (
    PythonParameterInventoryKind,
    PythonParameterMutationKind,
    PythonTestModuleModel,
)

_SEMANTIC_ID = re.compile(
    r"^(?:[a-z][a-z0-9]*(?:_[a-z0-9]+)*|(?:[A-Z][A-Z0-9]*-)+[0-9]{3,}-[a-z][a-z0-9]*(?:[-_][a-z0-9]+)*)$"  # noqa: E501
)


@dataclass(frozen=True, slots=True)
class _PythonParameterizationRuleResult:
    """Immutable parameterization findings and static counts."""

    findings: tuple[tuple[str, str, int | None], ...]
    parameterized_functions: int
    static_case_count: int | None


class _PythonParameterizationRule:
    """Own parameter-inventory, semantic-ID, and static-count policy."""

    __slots__ = ()

    @staticmethod
    def _id_problem(value: str) -> str | None:
        if (
            not _SEMANTIC_ID.fullmatch(value)
            or re.fullmatch(r"(?:case[_-]?)?[0-9]+", value, re.I)
            or "::" in value
            or "/" in value
            or "\\" in value
            or re.search(r"0x[0-9a-f]+", value, re.I)
            or any(0xD800 <= ord(char) <= 0xDFFF or char.isspace() for char in value)
        ):
            return f"pathological, ordinal, raw, or nonsemantic parameter ID {value!r}"
        return None

    def execute(
        self, model: PythonTestModuleModel
    ) -> _PythonParameterizationRuleResult:
        """Validate neutral facts and derive deterministic static counts."""
        findings: list[tuple[str, str, int | None]] = []
        parameterized = 0
        total = 0
        known = True
        for function in model.functions:
            function_valid = True
            function_product = 1
            for fact in function.parameterizations:
                name = fact.inventory_name
                inventory_problem = {
                    PythonParameterInventoryKind.NON_LITERAL: (
                        "TE.PARAMETER_ID",
                        "parameterization requires a literal case list and explicit IDs",  # noqa: E501
                    ),
                    PythonParameterInventoryKind.IMPORTED: (
                        "TE.PARAMETER_INVENTORY",
                        f"named parameter inventory {name!r} must not be imported",
                    ),
                    PythonParameterInventoryKind.UNRESOLVED: (
                        "TE.PARAMETER_INVENTORY",
                        f"named parameter inventory {name!r} is unresolved in this module",  # noqa: E501
                    ),
                    PythonParameterInventoryKind.MULTIPLE_ASSIGNMENTS: (
                        "TE.PARAMETER_INVENTORY",
                        f"named parameter inventory {name!r} must have exactly one module-level assignment",  # noqa: E501
                    ),
                    PythonParameterInventoryKind.COMPLEX_ASSIGNMENT: (
                        "TE.PARAMETER_INVENTORY",
                        f"named parameter inventory {name!r} requires one simple-name assignment",  # noqa: E501
                    ),
                    PythonParameterInventoryKind.ASSIGNED_AFTER_DECORATOR: (
                        "TE.PARAMETER_INVENTORY",
                        f"named parameter inventory {name!r} must be assigned before its consuming decorator",  # noqa: E501
                    ),
                    PythonParameterInventoryKind.NON_LITERAL_ASSIGNMENT: (
                        "TE.PARAMETER_INVENTORY",
                        f"named parameter inventory {name!r} must be assigned directly to a literal tuple or list",  # noqa: E501
                    ),
                    PythonParameterInventoryKind.STARRED_EXPANSION: (
                        "TE.PARAMETER_INVENTORY",
                        f"named parameter inventory {name!r} must not contain starred expansion",  # noqa: E501
                    ),
                }.get(fact.inventory_kind)
                if inventory_problem is not None:
                    findings.append((*inventory_problem, function.line))
                    function_valid = False
                    continue
                named = fact.inventory_kind is PythonParameterInventoryKind.NAMED
                for mutation in fact.mutations:
                    if mutation.kind is PythonParameterMutationKind.REASSIGNMENT:
                        message = f"named parameter inventory {name!r} is reassigned"
                    elif (
                        mutation.kind
                        is PythonParameterMutationKind.AUGMENTED_ASSIGNMENT
                    ):
                        message = f"named parameter inventory {name!r} uses augmented assignment"  # noqa: E501
                    elif mutation.kind is PythonParameterMutationKind.METHOD_CALL:
                        message = (
                            f"named parameter inventory {name!r} is mutated with "
                            f"{mutation.method_name}()"
                        )
                    else:
                        message = (
                            f"named parameter inventory {name!r} is mutated by "
                            "subscript assignment"
                        )
                    findings.append(("TE.PARAMETER_INVENTORY", message, function.line))
                    function_valid = False
                explicit: list[str] = []
                if fact.decorator_ids_present and not named:
                    if not fact.decorator_ids_are_literal_sequence:
                        findings.append(
                            (
                                "TE.PARAMETER_ID",
                                "parameterization requires a literal case list and explicit IDs",  # noqa: E501
                                function.line,
                            )
                        )
                        function_valid = False
                    elif not fact.decorator_ids_are_literal_strings:
                        findings.append(
                            (
                                "TE.PARAMETER_ID",
                                "parameter IDs must be literal strings",
                                function.line,
                            )
                        )
                        function_valid = False
                    explicit.extend(fact.decorator_ids)
                elif not fact.decorator_ids_present:
                    for case in fact.cases:
                        valid = case.is_param_call and (
                            not named or case.is_direct_pytest_param
                        )
                        if not valid:
                            findings.append(
                                (
                                    "TE.PARAMETER_INVENTORY"
                                    if named
                                    else "TE.PARAMETER_ID",
                                    "named parameter inventory elements must be direct "
                                    "pytest.param(...) calls"
                                    if named
                                    else "parameterization requires explicit ids=... or "  # noqa: E501
                                    "pytest.param(id=...)",
                                    function.line,
                                )
                            )
                            function_valid = False
                        elif case.id_keyword_count != 1:
                            findings.append(
                                (
                                    "TE.PARAMETER_ID",
                                    "every pytest.param case requires exactly one id=...",  # noqa: E501
                                    function.line,
                                )
                            )
                            function_valid = False
                        elif case.literal_id is None:
                            findings.append(
                                (
                                    "TE.PARAMETER_ID",
                                    "every pytest.param id=... must be a static string literal",  # noqa: E501
                                    function.line,
                                )
                            )
                            function_valid = False
                        else:
                            explicit.append(case.literal_id)
                elif named:
                    findings.append(
                        (
                            "TE.PARAMETER_INVENTORY",
                            "named parameter inventories own their explicit pytest.param "  # noqa: E501
                            "IDs and cannot use decorator ids=",
                            function.line,
                        )
                    )
                    function_valid = False
                if named and len(explicit) != len(set(explicit)):
                    findings.append(
                        (
                            "TE.PARAMETER_ID",
                            "named parameter inventory IDs must be unique",
                            function.line,
                        )
                    )
                    function_valid = False
                for value in explicit:
                    problem = self._id_problem(value)
                    if problem is not None:
                        findings.append(("TE.PARAMETER_ID", problem, function.line))
                        function_valid = False
                function_product *= len(fact.cases)
            if function.parameterizations:
                if function_valid:
                    parameterized += 1
                    total += function_product
                else:
                    known = False
        return _PythonParameterizationRuleResult(
            tuple(findings), parameterized, total if known else None
        )
