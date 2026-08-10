"""Independent stable evidence-identifier rule owner."""

from __future__ import annotations

import re

from .model import PythonTestModuleModel

_ID = re.compile(
    r"\b(?:(?:[A-Z][A-Z0-9]*-)+[0-9]{3,}|(?:software-verification|numerical-verification|scientific-validation|uncertainty-quantification)(?:\.[a-z0-9]+(?:-[a-z0-9]+)*){3,})\b"  # noqa: E501
)


def _validate_evidence_ids(
    model: PythonTestModuleModel, seen: dict[str, str]
) -> tuple[tuple[str, str, int | None], ...]:
    """Validate one identifier per test, no identifier ownership by helpers."""
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
        elif (
            "owns no identifier" not in function.doc.split("Requirement", 1)[0].lower()
        ):
            findings.append(
                (
                    "TE.HELPER_ID",
                    "helper must say it owns no identifier; referenced supported IDs are not owned",  # noqa: E501
                    function.line,
                )
            )
    return tuple(findings)


def _extracted_evidence(model: PythonTestModuleModel) -> tuple[tuple[str, str], ...]:
    """Return immutable ``(function name, evidence ID)`` facts for ingestion."""
    result: list[tuple[str, str]] = []
    for function in model.functions:
        if function.is_test:
            ids = _ID.findall(function.doc.split("Requirement", 1)[0])
            result.append((function.name, ids[0] if len(ids) == 1 else ""))
    return tuple(result)


class _PythonEvidenceIdentifierRule:
    """Own stable evidence identifier and duplicate-owner policy."""

    __slots__ = ()

    def execute(
        self, model: PythonTestModuleModel, seen: dict[str, str]
    ) -> tuple[tuple[str, str, int | None], ...]:
        """Validate identifier ownership in deterministic function order."""
        return _validate_evidence_ids(model, seen)


class _PythonEvidenceFactExtractor:
    """Own AST-free evidence fact projection from an immutable model."""

    __slots__ = ()

    def execute(self, model: PythonTestModuleModel) -> tuple[tuple[str, str], ...]:
        """Return immutable function/evidence-ID pairs for ingestion."""
        return _extracted_evidence(model)
