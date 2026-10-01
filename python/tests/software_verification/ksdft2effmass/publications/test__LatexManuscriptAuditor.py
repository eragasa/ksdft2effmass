"""Software verification of deterministic LaTeX manuscript-source auditing.

A pass establishes only the documented structural source checks. It does not establish
mathematical correctness, citation quality, numerical verification, scientific
validation, uncertainty quantification, publication, or human acceptance.
"""

from pathlib import Path

import pytest

from ksdft2effmass.publications.manuscript import (
    LatexManuscriptAuditIssueCode,
    LatexManuscriptAuditor,
    LatexManuscriptAuditRequest,
)

pytestmark = pytest.mark.software_verification
SUT = LatexManuscriptAuditor


class TestLatexManuscriptAuditor:
    """Own structural evidence for the manuscript source auditor."""

    @staticmethod
    def _request(
        source_root: Path,
        *,
        equation_terms_paths: tuple[Path, ...] = (),
    ) -> LatexManuscriptAuditRequest:
        return LatexManuscriptAuditRequest(
            source_root,
            source_root / "manuscript.tex",
            equation_terms_paths,
        )

    @staticmethod
    def _repository_root() -> Path:
        for parent in Path(__file__).resolve().parents:
            if (parent / "AGENTS.md").is_file() and (parent / "python").is_dir():
                return parent
        raise RuntimeError("repository root was not found from the test path")

    def test_execute__reports_composition_and_reference_defects(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-PUBLICATION-MANUSCRIPT-AUDIT-001

        Requirement: Missing composition inputs, duplicate labels, and unresolved
        references must be explicit deterministic findings.

        Method: Audit a small authored composition containing one missing include, a
        label duplicated across two loaded sources, and one unresolved reference.

        Oracle: Exact issue-code inventory.

        Acceptance: The audit returns each expected issue code and does not pass.

        Interpretation: A pass establishes structural defect reporting.

        Limitations: The synthetic source does not exercise a TeX engine.
        """
        (tmp_path / "manuscript.tex").write_text(
            "\\include{chapter-a}\n"
            "\\include{chapter-b}\n"
            "\\include{missing}\n"
            "\\ref{absent}\n",
            encoding="utf-8",
        )
        (tmp_path / "chapter-a.tex").write_text(
            "\\section{A}\\label{sec:duplicate}\n", encoding="utf-8"
        )
        (tmp_path / "chapter-b.tex").write_text(
            "\\section{B}\\label{sec:duplicate}\n", encoding="utf-8"
        )

        result = SUT().execute(self._request(tmp_path))

        assert not result.passes
        assert {issue.code for issue in result.issues} == {
            LatexManuscriptAuditIssueCode.DUPLICATE_LABEL,
            LatexManuscriptAuditIssueCode.MISSING_INCLUDE,
            LatexManuscriptAuditIssueCode.UNRESOLVED_REFERENCE,
        }

    def test_execute__accepts_explained_equation_in_selected_source(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-PUBLICATION-MANUSCRIPT-AUDIT-002

        Requirement: An equation source under the stricter contract passes only when
        each display is followed by a nonempty equation-term list.

        Method: Audit one included chapter containing an equation and one term item.

        Oracle: The explicit ``equationterms`` source convention.

        Acceptance: The audit passes with both sources in its graph.

        Interpretation: A pass establishes positive equation-explanation recognition.

        Limitations: The auditor checks structure, not whether prose definitions are
        mathematically adequate.
        """
        chapter = tmp_path / "chapter.tex"
        (tmp_path / "manuscript.tex").write_text(
            "\\include{chapter}\n", encoding="utf-8"
        )
        chapter.write_text(
            "\\begin{equation}\n"
            "x=y.\\label{eq:balance}\n"
            "\\end{equation}\n"
            "\\begin{equationterms}{eq:balance}\n"
            "  \\equationterm{$x$}{the result.}\n"
            "  \\equationterm{$y$}{the input.}\n"
            "\\end{equationterms}\n",
            encoding="utf-8",
        )

        result = SUT().execute(self._request(tmp_path, equation_terms_paths=(chapter,)))

        assert result.passes
        assert result.source_paths == (
            chapter,
            tmp_path / "manuscript.tex",
        )

    @pytest.mark.parametrize(
        ("chapter_text", "expected_code"),
        (
            pytest.param(
                "\\begin{equation}x=y\\label{eq:missing}\\end{equation}\n",
                LatexManuscriptAuditIssueCode.MISSING_EQUATION_TERMS,
                id="missing_terms",
            ),
            pytest.param(
                "\\begin{equation}x=y\\label{eq:empty}\\end{equation}\n"
                "\\begin{equationterms}{eq:empty}\\end{equationterms}\n",
                LatexManuscriptAuditIssueCode.EMPTY_EQUATION_TERMS,
                id="empty_terms",
            ),
            pytest.param(
                "\\begin{equationterms}{eq:orphan}"
                "\\equationterm{$x$}{orphan.}"
                "\\end{equationterms}\n",
                LatexManuscriptAuditIssueCode.ORPHAN_EQUATION_TERMS,
                id="orphan_terms",
            ),
        ),
    )
    def test_execute__reports_equation_explanation_contract_defects(
        self,
        tmp_path: Path,
        chapter_text: str,
        expected_code: LatexManuscriptAuditIssueCode,
    ) -> None:
        """Evidence ID: SV-PUBLICATION-MANUSCRIPT-AUDIT-003

        Requirement: Missing, empty, and orphan term lists have distinct findings.

        Method: Audit one minimal source for each malformed explanation structure.

        Oracle: Parameter-specific exact issue code.

        Acceptance: The expected issue is the only finding.

        Interpretation: A pass establishes the bounded negative contract.

        Limitations: Symbol coverage inside a nonempty list remains human-reviewed.
        """
        chapter = tmp_path / "chapter.tex"
        (tmp_path / "manuscript.tex").write_text(
            "\\include{chapter}\n", encoding="utf-8"
        )
        chapter.write_text(chapter_text, encoding="utf-8")

        result = SUT().execute(self._request(tmp_path, equation_terms_paths=(chapter,)))

        assert tuple(issue.code for issue in result.issues) == (expected_code,)

    @pytest.mark.parametrize(
        ("chapter_text", "expected_code"),
        (
            pytest.param(
                "\\begin{equation}x=y\\end{equation}\n"
                "\\begin{equationterms}{eq:unbound}"
                "\\equationterm{$x$}{the result.}"
                "\\end{equationterms}\n",
                LatexManuscriptAuditIssueCode.MISSING_EQUATION_LABEL,
                id="missing_equation_label",
            ),
            pytest.param(
                "\\begin{equation}x=y\\label{eq:first}\\label{eq:second}"
                "\\end{equation}\n"
                "\\begin{equationterms}{eq:first}"
                "\\equationterm{$x$}{the result.}"
                "\\end{equationterms}\n",
                LatexManuscriptAuditIssueCode.MULTIPLE_EQUATION_LABELS,
                id="multiple_equation_labels",
            ),
            pytest.param(
                "\\begin{equation}x=y\\label{eq:missing-term-label}"
                "\\end{equation}\n"
                "\\begin{equationterms}"
                "\\equationterm{$x$}{the result.}"
                "\\end{equationterms}\n",
                LatexManuscriptAuditIssueCode.MISSING_EQUATION_TERMS_LABEL,
                id="missing_terms_label",
            ),
            pytest.param(
                "\\begin{equation}x=y\\label{eq:expected}\\end{equation}\n"
                "\\begin{equationterms}{eq:other}"
                "\\equationterm{$x$}{the result.}"
                "\\end{equationterms}\n",
                LatexManuscriptAuditIssueCode.MISMATCHED_EQUATION_TERMS_LABEL,
                id="mismatched_label",
            ),
            pytest.param(
                "\\begin{equation}x=y\\label{eq:empty-symbol}"
                "\\end{equation}\n"
                "\\begin{equationterms}{eq:empty-symbol}"
                "\\equationterm{}{the result.}"
                "\\end{equationterms}\n",
                LatexManuscriptAuditIssueCode.EMPTY_EQUATION_TERM_SYMBOL,
                id="empty_symbol",
            ),
            pytest.param(
                "\\begin{equation}x=y\\label{eq:empty-definition}"
                "\\end{equation}\n"
                "\\begin{equationterms}{eq:empty-definition}"
                "\\equationterm{$x$}{}"
                "\\end{equationterms}\n",
                LatexManuscriptAuditIssueCode.EMPTY_EQUATION_TERM_DEFINITION,
                id="empty_definition",
            ),
            pytest.param(
                "\\begin{equation}x=y\\label{eq:duplicate-symbol}"
                "\\end{equation}\n"
                "\\begin{equationterms}{eq:duplicate-symbol}"
                "\\equationterm{$x$}{first.}"
                "\\equationterm{$x$}{second.}"
                "\\end{equationterms}\n",
                LatexManuscriptAuditIssueCode.DUPLICATE_EQUATION_TERM_SYMBOL,
                id="duplicate_symbol",
            ),
            pytest.param(
                "\\begin{equation}x=y\\label{eq:malformed}\\end{equation}\n"
                "\\begin{equationterms}{eq:malformed}prose only"
                "\\end{equationterms}\n",
                LatexManuscriptAuditIssueCode.MALFORMED_EQUATION_TERM,
                id="malformed_term",
            ),
        ),
    )
    def test_execute__reports_equation_binding_and_term_defects(
        self,
        tmp_path: Path,
        chapter_text: str,
        expected_code: LatexManuscriptAuditIssueCode,
    ) -> None:
        """Evidence ID: SV-PUBLICATION-MANUSCRIPT-AUDIT-005

        Requirement: Governed equations and term lists must share one stable label,
        and every term must have one unique nonempty symbol and nonempty definition.

        Method: Audit one minimal source for each malformed binding or term entry.

        Oracle: Parameter-specific exact issue code.

        Acceptance: The expected issue is the only finding.

        Interpretation: A pass establishes deterministic structural enforcement of
        equation-to-definition bindings and term-entry completeness.

        Limitations: Matching labels and populated fields do not prove that every
        mathematical variable is listed or that any definition is scientifically right.
        """
        chapter = tmp_path / "chapter.tex"
        (tmp_path / "manuscript.tex").write_text(
            "\\include{chapter}\n", encoding="utf-8"
        )
        chapter.write_text(chapter_text, encoding="utf-8")

        result = SUT().execute(self._request(tmp_path, equation_terms_paths=(chapter,)))

        assert tuple(issue.code for issue in result.issues) == (expected_code,)

    def test_execute__accepts_resolved_literal_citations(self, tmp_path: Path) -> None:
        """Evidence ID: SV-PUBLICATION-MANUSCRIPT-AUDIT-006

        Requirement: Literal citation keys resolve against unique entries in declared,
        contained BibLaTeX resources.

        Method: Audit two citation commands whose keys are supplied by one bibliography.

        Oracle: The declared bibliography entries and literal citation-key lists.

        Acceptance: The audit passes and records the bibliography as inspected.

        Interpretation: A pass establishes citation-key presence and uniqueness only.

        Limitations: Bibliographic metadata and citation suitability are not assessed.
        """
        bibliography = tmp_path / "references.bib"
        (tmp_path / "manuscript.tex").write_text(
            "\\addbibresource{references.bib}\n"
            "\\cite{alpha,beta}\n"
            "\\textcite[section 2]{alpha}\n",
            encoding="utf-8",
        )
        bibliography.write_text(
            "@article{alpha,\n  title = {Alpha}\n}\n@book{beta,\n  title = {Beta}\n}\n",
            encoding="utf-8",
        )

        result = SUT().execute(self._request(tmp_path))

        assert result.passes
        assert bibliography in result.source_paths

    def test_execute__reports_bibliography_and_citation_defects(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-PUBLICATION-MANUSCRIPT-AUDIT-007

        Requirement: Escaping and missing bibliographies, duplicate keys, and unresolved
        literal citations must remain distinct deterministic findings.

        Method: Audit one composition containing all four independently authored
        defects.

        Oracle: Exact issue-code inventory.

        Acceptance: Each expected issue code occurs exactly once.

        Interpretation: A pass establishes bounded citation-structure defect reporting.

        Limitations: The test does not establish bibliography metadata correctness.
        """
        (tmp_path / "manuscript.tex").write_text(
            "\\addbibresource{references.bib}\n"
            "\\addbibresource{missing.bib}\n"
            "\\addbibresource{../outside.bib}\n"
            "\\cite{present,absent}\n",
            encoding="utf-8",
        )
        (tmp_path / "references.bib").write_text(
            "@article{present,\n  title = {First}\n}\n"
            "@book{present,\n  title = {Second}\n}\n",
            encoding="utf-8",
        )

        result = SUT().execute(self._request(tmp_path))

        assert len(result.issues) == 4
        assert {issue.code for issue in result.issues} == {
            LatexManuscriptAuditIssueCode.BIBLIOGRAPHY_PATH_ESCAPE,
            LatexManuscriptAuditIssueCode.DUPLICATE_BIBLIOGRAPHY_KEY,
            LatexManuscriptAuditIssueCode.MISSING_BIBLIOGRAPHY,
            LatexManuscriptAuditIssueCode.UNRESOLVED_CITATION,
        }

    def test_execute__current_monograph_composition_has_resolved_structure(
        self,
    ) -> None:
        """Evidence ID: SV-PUBLICATION-MANUSCRIPT-AUDIT-004

        Requirement: The maintained monograph composition graph has present includes,
        unique labels, and resolved internal references.

        Method: Audit the repository manuscript root and every recursively included
        LaTeX source without invoking external programs.

        Oracle: The source graph's explicit include, label, and reference declarations.

        Acceptance: No structural finding is returned.

        Interpretation: A pass establishes bounded source-graph consistency at the
        tested repository state.

        Limitations: LaTeX compilation, citation quality, bibliography metadata,
        equations, and scientific meaning require separate checks.
        """
        monograph_root = (
            self._repository_root() / "docs/publications/research-monograph"
        )

        result = SUT().execute(
            LatexManuscriptAuditRequest(
                monograph_root,
                monograph_root / "manuscript/manuscript.tex",
                (
                    monograph_root / "chapters/10-impurity-operator-extraction.tex",
                    monograph_root
                    / "appendices/J-two-dimensional-defect-extraction.tex",
                ),
            )
        )

        assert result.passes, result.issues
        assert monograph_root / "manuscript/manuscript.tex" in result.source_paths
        assert (
            monograph_root / "chapters/10-impurity-operator-extraction.tex"
            in result.source_paths
        )
        assert (
            monograph_root / "appendices/J-two-dimensional-defect-extraction.tex"
            in result.source_paths
        )
