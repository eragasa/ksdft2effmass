"""Independent semantic-name rules for parsed Python evidence modules."""

from __future__ import annotations

import re

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


def validate_test_name(name: str) -> tuple[str, str] | None:
    """Return one stable naming finding for ``name``, if any."""
    if _NAME.fullmatch(name) is None:
        return (
            "TE.TEST_NAME",
            "test name violates semantic surface/facet/behavior grammar",
        )
    parts = name.split("__")
    if len(parts) == 3 and parts[1] in _VAGUE:
        return (
            "TE.VAGUE_TEST_FACET",
            f"test facet {parts[1]!r} does not name a concrete public member "
            "or cohesive contract",
        )
    return None
