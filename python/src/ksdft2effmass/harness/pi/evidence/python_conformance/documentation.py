"""Independent module-profile documentation rules."""

from __future__ import annotations

import re


def validate_profile_declaration(
    module_doc: str | None, evidence_profile: str
) -> tuple[tuple[str, str], ...]:
    """Validate explicit profile, bounded scope, and VVUQ-exclusion metadata."""
    problems: list[tuple[str, str]] = []
    expected = f"Evidence profile: {evidence_profile}"
    if module_doc is None or expected not in module_doc.splitlines():
        problems.append(("TE.PROFILE_DECLARATION", f"module must declare {expected!r}"))
    if module_doc is None or not re.search(
        r"(?m)^Bounded artifact scope:\s+\S", module_doc
    ):
        problems.append(
            (
                "TE.PROFILE_DECLARATION",
                "module must declare one nonempty Bounded artifact scope",
            )
        )
    if module_doc is None or not re.search(
        r"(?m)^VVUQ and scientific exclusions\s*$", module_doc
    ):
        problems.append(
            (
                "TE.PROFILE_DECLARATION",
                "module must include the VVUQ and scientific exclusions section",
            )
        )
    return tuple(problems)
