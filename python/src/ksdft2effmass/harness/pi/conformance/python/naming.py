"""Independent complete semantic naming rule owner."""

from __future__ import annotations

import re

from .model import PythonTestModuleModel

_SURFACES = (
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
_NAME = re.compile(
    r"^test_(" + "|".join(_SURFACES) + r")__[a-z][a-z0-9_]*__[a-z][a-z0-9_]*$"
)
_VAGUE = frozenset({"behavior", "contract", "general", "misc"})


def _validate_test_name(name: str) -> tuple[str, str] | None:
    """Return one stable naming finding for ``name``, if any."""
    if _NAME.fullmatch(name) is None:
        return (
            "TE.TEST_NAME",
            "test name violates semantic surface/facet/behavior grammar",
        )
    if name.split("__")[1] in _VAGUE:
        return (
            "TE.VAGUE_TEST_FACET",
            f"test facet {name.split('__')[1]!r} does not name a concrete public member or cohesive contract",  # noqa: E501
        )
    return None


class _PythonNamingRule:
    """Own complete test and helper semantic-name policy."""

    __slots__ = ()

    def execute(
        self, model: PythonTestModuleModel
    ) -> tuple[tuple[str, str, int | None], ...]:
        """Validate every test and helper name in one model."""
        findings: list[tuple[str, str, int | None]] = []
        for function in model.functions:
            if function.is_test:
                problem = _validate_test_name(function.name)
                if problem:
                    findings.append((*problem, function.line))
            elif function.name.startswith("_"):
                findings.append(
                    (
                        "TE.HELPER_PRIVATE",
                        "evidence helper must have a nonprivate semantic name",
                        function.line,
                    )
                )
            elif function.name in {"helper", "setup", "check"} or re.search(
                r"_[0-9]+$", function.name
            ):
                findings.append(
                    ("TE.HELPER_NAME", "helper name is not semantic", function.line)
                )
        return tuple(findings)
