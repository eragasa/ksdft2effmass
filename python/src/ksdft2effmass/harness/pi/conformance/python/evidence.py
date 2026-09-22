"""Independent stable evidence-identifier rule owner."""

from __future__ import annotations

import re

from .model import PythonTestModuleModel

_ID = re.compile(
    r"\b(?:(?:[A-Z][A-Z0-9]*-)+[0-9]{3,}|(?:software-verification|numerical-verification|scientific-validation|uncertainty-quantification)(?:\.[a-z0-9]+(?:-[a-z0-9]+)*){3,})\b"  # noqa: E501
)


class _PythonEvidenceIdentifierRule:
    """Own stable evidence identifier and duplicate-owner policy."""

    __slots__ = ()

    def execute(
        self, model: PythonTestModuleModel, seen: dict[str, str]
    ) -> tuple[tuple[str, str, int | None], ...]:
        """Validate one identifier per test and no identifier ownership by helpers."""
        findings: list[tuple[str, str, int | None]] = []
        for function in model.functions:
            ids = _ID.findall(function.doc.split("Requirement", 1)[0])
            if function.is_test:
                if len(ids) != 1:
                    findings.append(
                        (
                            "TE.EVIDENCE_ID",
                            "test must declare exactly one evidence ID",
                            function.line,
                        )
                    )
                for evidence_id in ids:
                    if evidence_id in seen:
                        findings.append(
                            (
                                "TE.DUPLICATE_ID",
                                f"{evidence_id} already occurs at {seen[evidence_id]}",
                                function.line,
                            )
                        )
                    else:
                        seen[evidence_id] = f"{model.path}:{function.line}"
            else:
                # Only an explicit evidence-ID paragraph can declare ownership.
                # Ordinary support prose may reference another test's identifier;
                # legacy explicit nonownership paragraphs remain references too.
                declarations = re.finditer(
                    r"(?m)^[ \t]*Evidence ID:[ \t]*([^\n]*(?:\n(?![ \t]*\n)[^\n]+)*)",
                    function.doc,
                )
                for declaration in declarations:
                    paragraph = declaration.group(1).strip()
                    nonowning = re.match(
                        r"(?i)^(?:this )?(?:helper )?owns no identifier\b", paragraph
                    )
                    if nonowning is None:
                        findings.append(
                            (
                                "TE.HELPER_ID",
                                "non-test helpers cannot own evidence identifiers; "
                                "ordinary references do not declare ownership",
                                function.line,
                            )
                        )
        return tuple(findings)


class _PythonEvidenceFactExtractor:
    """Own AST-free evidence fact projection from an immutable model."""

    __slots__ = ()

    def execute(self, model: PythonTestModuleModel) -> tuple[tuple[str, str], ...]:
        """Return immutable owner-node/evidence-ID pairs for ingestion."""
        result: list[tuple[str, str]] = []
        for function in model.functions:
            if function.is_test:
                ids = _ID.findall(function.doc.split("Requirement", 1)[0])
                result.append(
                    (function.owner_node_name, ids[0] if len(ids) == 1 else "")
                )
        return tuple(result)
