"""Structural auditing of LaTeX references and literal citation keys."""

import re
from pathlib import Path

from ksdft2effmass.publications.audit_records import (
    LatexManuscriptAuditIssue,
    LatexManuscriptAuditIssueCode,
    LatexSourceGraph,
)


class LatexReferenceAuditor:
    """Audit labels, references, bibliographies, and literal citation keys."""

    __slots__ = ()

    _bibliography_key_pattern = re.compile(
        r"^[ \t]*@[A-Za-z]+\s*[{(]\s*([^,\s]+)\s*,", re.MULTILINE
    )
    _citation_pattern = re.compile(
        r"\\(?:cite|parencite|textcite|autocite|footcite|supercite|nocite)\*?"
        r"(?:\s*\[[^\]]*\]){0,2}\s*\{([^{}]+)\}"
    )
    _label_pattern = re.compile(r"\\label\{([^{}]+)\}")
    _reference_pattern = re.compile(r"\\(?:ref|eqref|pageref|autoref)\{([^{}]+)\}")

    def execute(self, graph: LatexSourceGraph) -> tuple[LatexManuscriptAuditIssue, ...]:
        """Return deterministic reference and citation findings for one graph."""
        if type(graph) is not LatexSourceGraph:
            raise TypeError("graph must be LatexSourceGraph")
        issues: list[LatexManuscriptAuditIssue] = []
        self._audit_labels_and_references(graph, issues)
        self._audit_citations(graph, issues)
        return tuple(issues)

    def _audit_labels_and_references(
        self,
        graph: LatexSourceGraph,
        issues: list[LatexManuscriptAuditIssue],
    ) -> None:
        """Report duplicate labels and references absent from the source graph."""
        label_locations: dict[str, tuple[Path, int]] = {}
        references: list[tuple[str, Path, int]] = []
        for source in graph.composition_sources:
            for match in self._label_pattern.finditer(source.visible_text):
                label = match.group(1)
                line = source.line_number(match.start())
                first = label_locations.get(label)
                if first is None:
                    label_locations[label] = (source.path, line)
                else:
                    issues.append(
                        LatexManuscriptAuditIssue(
                            LatexManuscriptAuditIssueCode.DUPLICATE_LABEL,
                            source.path,
                            line,
                            f"{label}; first at {first[0]}:{first[1]}",
                        )
                    )
            for match in self._reference_pattern.finditer(source.visible_text):
                references.append(
                    (
                        match.group(1),
                        source.path,
                        source.line_number(match.start()),
                    )
                )
        for label, path, line in references:
            if label not in label_locations:
                issues.append(
                    LatexManuscriptAuditIssue(
                        LatexManuscriptAuditIssueCode.UNRESOLVED_REFERENCE,
                        path,
                        line,
                        label,
                    )
                )

    def _audit_citations(
        self,
        graph: LatexSourceGraph,
        issues: list[LatexManuscriptAuditIssue],
    ) -> None:
        """Report duplicate bibliography keys and unresolved literal citations."""
        key_locations: dict[str, tuple[Path, int]] = {}
        for source in graph.bibliography_sources:
            for match in self._bibliography_key_pattern.finditer(source.visible_text):
                key = match.group(1)
                line = source.line_number(match.start())
                first = key_locations.get(key)
                if first is None:
                    key_locations[key] = (source.path, line)
                else:
                    issues.append(
                        LatexManuscriptAuditIssue(
                            LatexManuscriptAuditIssueCode.DUPLICATE_BIBLIOGRAPHY_KEY,
                            source.path,
                            line,
                            f"{key}; first at {first[0]}:{first[1]}",
                        )
                    )

        for source in graph.composition_sources:
            for match in self._citation_pattern.finditer(source.visible_text):
                line = source.line_number(match.start())
                for raw_key in match.group(1).split(","):
                    key = raw_key.strip()
                    if not key or key == "*" or "#" in key:
                        continue
                    if key not in key_locations:
                        issues.append(
                            LatexManuscriptAuditIssue(
                                LatexManuscriptAuditIssueCode.UNRESOLVED_CITATION,
                                source.path,
                                line,
                                key,
                            )
                        )
