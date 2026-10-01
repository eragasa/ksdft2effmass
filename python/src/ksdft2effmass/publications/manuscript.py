"""Typed structural auditing for the research-monograph LaTeX source graph.

The audit checks source composition, cross-reference and literal citation-key
integrity, and explicitly selected equation-explanation contracts. It does not
interpret mathematical meaning, establish citation quality, or replace a LaTeX
build.
"""

from ksdft2effmass.publications.audit_records import (
    LatexManuscriptAuditIssue,
    LatexManuscriptAuditIssueCode,
    LatexManuscriptAuditRequest,
    LatexManuscriptAuditResult,
)
from ksdft2effmass.publications.equation_terms import LatexEquationTermsAuditor
from ksdft2effmass.publications.references import LatexReferenceAuditor
from ksdft2effmass.publications.source_graph import LatexSourceGraphConstructor

__all__ = (
    "LatexManuscriptAuditIssue",
    "LatexManuscriptAuditIssueCode",
    "LatexManuscriptAuditRequest",
    "LatexManuscriptAuditResult",
    "LatexManuscriptAuditor",
)


class LatexManuscriptAuditor:
    """Audit one LaTeX source graph without invoking external programs."""

    __slots__ = ()

    def execute(
        self, request: LatexManuscriptAuditRequest
    ) -> LatexManuscriptAuditResult:
        """Inspect composition, references, citations, and equation explanations.

        The action performs no TeX execution. Paths are resolved lexically beneath the
        declared source root, source files are decoded as UTF-8, comments are excluded
        from structural matching, and findings are returned in deterministic order.
        """
        if type(request) is not LatexManuscriptAuditRequest:
            raise TypeError("request must be LatexManuscriptAuditRequest")

        construction = LatexSourceGraphConstructor().execute(request)
        issues: list[LatexManuscriptAuditIssue] = list(construction.issues)
        issues.extend(LatexReferenceAuditor().execute(construction.graph))
        issues.extend(LatexEquationTermsAuditor().execute(request, construction.graph))
        ordered_issues = tuple(
            sorted(
                issues,
                key=lambda issue: (
                    str(issue.source_path),
                    issue.line,
                    issue.code.value,
                    issue.subject,
                ),
            )
        )
        return LatexManuscriptAuditResult(
            construction.graph.inspected_paths,
            ordered_issues,
        )
