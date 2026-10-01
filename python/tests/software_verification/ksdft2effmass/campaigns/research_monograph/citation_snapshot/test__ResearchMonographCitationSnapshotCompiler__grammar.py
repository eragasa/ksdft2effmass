r"""Software verification of ``ResearchMonographCitationSnapshotCompiler``.

Evidence profile: routine

Bounded artifact scope: synthetic compact TeX/BibLaTeX graphs exercising the closed
citation grammar and fail-closed graph/parser boundaries.

Facet and represented meaning

The compiler recognizes comments, balanced multiline/multikey calls, exact supported
macro expansion, safe noncitation definitions, and includes.

Intrinsic and cross-object scope

Evidence covers compiler-owned graph and parser behavior against authored compact
source bytes; it does not inspect private parser state.

VVUQ and scientific exclusions

This is structural software verification only. It establishes no TeX typesetting
agreement beyond the declared grammar, bibliographic truth, scientific validation,
UQ, rights decision, or source acceptance.
"""

from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph import (
    CitationSnapshotError,
    CitationSnapshotErrorCode,
    ManuscriptCitationOrigin,
    ManuscriptCitationSnapshot,
    ResearchMonographCitationSnapshotCompiler,
    ResearchMonographCitationSnapshotRequest,
)

pytestmark = pytest.mark.software_verification
SUT = ResearchMonographCitationSnapshotCompiler


class TestResearchMonographCitationSnapshotCompiler:
    """Own software evidence for the closed citation source grammar."""

    def test_method__execute__parses_supported_compact_graph(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-CITATION-SNAPSHOT-COMPILER-GRAMMAR-001

        Requirement: Comments, safe def, multiline multikey cite, eqincite,
        citationtodo texttt expansion, unresolved source gaps, and includes must retain
        deterministic rendered semantics.

        Acceptance: The compact graph yields two files, four calls, five occurrences,
        two groups, one editorial marker, one source gap, and complete bibliography
        closure.
        """
        root = self.make_repository(
            tmp_path,
            r"""\documentclass{report}
\def\ps@safe{plain}
\begin{document}
% \cite{ignored}
\cite{alpha,
 beta}
\eqincite{alpha}{4}
\citationtodo{medium priority}{Candidate \texttt{beta}.}
\path{XXXX}
\include{chapters/child}
\end{document}
""",
            "@article{alpha, title={A}}\n@book{beta, title={B}}\n",
            "chapters/child.tex",
            "Child \\cite{alpha}.\n",
        )

        snapshot = self.compile(root)

        assert snapshot.repository_revision == "a" * 40
        assert len(snapshot.source_files) == 2
        assert len(snapshot.calls) == 4
        assert len(snapshot.occurrences) == 5
        assert len(snapshot.groups) == 2
        assert len(snapshot.todos) == 1
        assert len(snapshot.source_gaps) == 1
        assert snapshot.missing_keys == ()
        assert snapshot.uncited_keys == ()
        assert (
            snapshot.occurrences[2].origin
            is ManuscriptCitationOrigin.EQINCITE_EXPANSION
        )
        assert (
            snapshot.occurrences[3].origin
            is ManuscriptCitationOrigin.CITATION_TODO_EXPANSION
        )

    @pytest.mark.parametrize(
        (
            "manuscript",
            "bibliography",
            "extra_file_path",
            "extra_file_content",
            "expected_code",
        ),
        (
            pytest.param(
                "\\include{chapters/missing}\n",
                "@article{alpha, title={A}}\n",
                None,
                None,
                CitationSnapshotErrorCode.SOURCE_MISSING,
                id="missing_include",
            ),
            pytest.param(
                "\\include{chapters/child}\n",
                "@article{alpha, title={A}}\n",
                "chapters/child.tex",
                "\\include{../manuscript}\n",
                CitationSnapshotErrorCode.INCLUDE_CYCLE,
                id="include_cycle",
            ),
            pytest.param(
                "\\include{../../../outside}\n",
                "@article{alpha, title={A}}\n",
                None,
                None,
                CitationSnapshotErrorCode.PATH_ESCAPE,
                id="path_escape",
            ),
            pytest.param(
                "\\parencite{alpha}\n",
                "@article{alpha, title={A}}\n",
                None,
                None,
                CitationSnapshotErrorCode.UNKNOWN_CITATION_MACRO,
                id="unknown_citation_macro",
            ),
            pytest.param(
                "\\newcommand{\\source}{\\cite{alpha}}\n",
                "@article{alpha, title={A}}\n",
                None,
                None,
                CitationSnapshotErrorCode.UNSAFE_DEFINITION,
                id="citation_bearing_definition",
            ),
            pytest.param(
                "\\newcommand{\\eqincite}[2]{\\cite{#1}\\cite{#2}}\n",
                "@article{alpha, title={A}}\n",
                None,
                None,
                CitationSnapshotErrorCode.UNSAFE_DEFINITION,
                id="altered_known_macro_semantics",
            ),
            pytest.param(
                "\\cite{alpha\n",
                "@article{alpha, title={A}}\n",
                None,
                None,
                CitationSnapshotErrorCode.MALFORMED_TEX,
                id="malformed_tex",
            ),
            pytest.param(
                "\\cite{alpha}\n",
                "@article{alpha, title={A}\n",
                None,
                None,
                CitationSnapshotErrorCode.MALFORMED_BIBLIOGRAPHY,
                id="malformed_bibliography",
            ),
            pytest.param(
                "\\cite{alpha}\n",
                "@article{alpha, title={A}}\n@book{alpha, title={B}}\n",
                None,
                None,
                CitationSnapshotErrorCode.BIBLIOGRAPHY_DUPLICATE_KEY,
                id="duplicate_bibliography_key",
            ),
        ),
    )
    def test_method__execute__fails_closed_on_unsupported_or_unsafe_source(
        self,
        tmp_path: Path,
        manuscript: str,
        bibliography: str,
        extra_file_path: str | None,
        extra_file_content: str | None,
        expected_code: CitationSnapshotErrorCode,
    ) -> None:
        """Evidence ID: SV-CITATION-SNAPSHOT-COMPILER-GRAMMAR-002

        Requirement: Missing, cyclic, escaping, unknown citation-capable, altered
        macro, malformed source, and duplicate-key inputs must not yield partial
        snapshots.

        Acceptance: Each semantic partition raises CitationSnapshotError with its
        exact fail-closed code.
        """
        root = self.make_repository(
            tmp_path,
            manuscript,
            bibliography,
            extra_file_path,
            extra_file_content,
        )

        with pytest.raises(CitationSnapshotError) as captured:
            self.compile(root)

        assert captured.value.code is expected_code

    @staticmethod
    def compile(root: Path) -> ManuscriptCitationSnapshot:
        """Compile one authored compact repository through the supported API."""
        return (
            SUT()
            .execute(ResearchMonographCitationSnapshotRequest(root.as_posix()))
            .snapshot
        )

    @staticmethod
    def make_repository(
        root: Path,
        manuscript: str,
        bibliography: str,
        extra_file_path: str | None,
        extra_file_content: str | None,
    ) -> Path:
        """Create exact compact repository bytes and a detached Git HEAD identity."""
        (root / ".git").mkdir()
        (root / ".git" / "HEAD").write_text("a" * 40 + "\n", encoding="utf-8")
        monograph = root / "docs" / "publications" / "research-monograph"
        monograph.mkdir(parents=True)
        (monograph / "manuscript.tex").write_text(manuscript, encoding="utf-8")
        (monograph / "references.bib").write_text(bibliography, encoding="utf-8")
        if extra_file_path is not None and extra_file_content is not None:
            destination = monograph / extra_file_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(extra_file_content, encoding="utf-8")
        return root
