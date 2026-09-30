"""Immutable records for repository-local LaTeX manuscript auditing."""

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path


class LatexManuscriptAuditIssueCode(StrEnum):
    """Classify one deterministic manuscript-source finding."""

    BIBLIOGRAPHY_PATH_ESCAPE = "bibliography_path_escape"
    COMPOSITION_PATH_ESCAPE = "composition_path_escape"
    DUPLICATE_BIBLIOGRAPHY_KEY = "duplicate_bibliography_key"
    DUPLICATE_EQUATION_TERM_SYMBOL = "duplicate_equation_term_symbol"
    DUPLICATE_LABEL = "duplicate_label"
    EMPTY_EQUATION_TERM_DEFINITION = "empty_equation_term_definition"
    EMPTY_EQUATION_TERM_SYMBOL = "empty_equation_term_symbol"
    EMPTY_EQUATION_TERMS = "empty_equation_terms"
    INCLUDE_CYCLE = "include_cycle"
    INCLUDE_PATH_ESCAPE = "include_path_escape"
    MALFORMED_EQUATION_TERM = "malformed_equation_term"
    MISMATCHED_EQUATION_TERMS_LABEL = "mismatched_equation_terms_label"
    MISSING_BIBLIOGRAPHY = "missing_bibliography"
    MISSING_EQUATION_LABEL = "missing_equation_label"
    MISSING_EQUATION_TERMS = "missing_equation_terms"
    MISSING_EQUATION_TERMS_LABEL = "missing_equation_terms_label"
    MISSING_INCLUDE = "missing_include"
    MISSING_SOURCE = "missing_source"
    MULTIPLE_EQUATION_LABELS = "multiple_equation_labels"
    ORPHAN_EQUATION_TERMS = "orphan_equation_terms"
    UNRESOLVED_CITATION = "unresolved_citation"
    UNRESOLVED_REFERENCE = "unresolved_reference"


@dataclass(frozen=True, slots=True)
class LatexManuscriptAuditRequest:
    """Identify one manuscript composition and its stricter equation sources.

    Parameters
    ----------
    source_root
        Absolute directory against which LaTeX ``include`` and ``input`` paths are
        resolved.
    composition_path
        Absolute path to the root LaTeX composition file.
    equation_terms_paths
        Absolute paths whose display-math environments must be followed immediately
        by a nonempty ``equationterms`` environment.
    """

    source_root: Path
    composition_path: Path
    equation_terms_paths: tuple[Path, ...] = ()

    def __post_init__(self) -> None:
        """Require absolute, lexically contained, duplicate-free source paths."""
        if not isinstance(self.source_root, Path):
            raise TypeError("source_root must be pathlib.Path")
        if not isinstance(self.composition_path, Path):
            raise TypeError("composition_path must be pathlib.Path")
        if type(self.equation_terms_paths) is not tuple:
            raise TypeError("equation_terms_paths must be a tuple")
        if not self.source_root.is_absolute():
            raise ValueError("source_root must be absolute")
        if not self.composition_path.is_absolute():
            raise ValueError("composition_path must be absolute")
        self._require_contained(self.composition_path, "composition_path")
        if len(set(self.equation_terms_paths)) != len(self.equation_terms_paths):
            raise ValueError("equation_terms_paths must not contain duplicates")
        for path in self.equation_terms_paths:
            if not isinstance(path, Path):
                raise TypeError(
                    "every equation_terms_paths member must be pathlib.Path"
                )
            if not path.is_absolute():
                raise ValueError("every equation_terms_paths member must be absolute")
            self._require_contained(path, "equation_terms_paths member")

    def _require_contained(self, path: Path, field: str) -> None:
        """Require one lexical path to remain beneath the source root."""
        try:
            path.relative_to(self.source_root)
        except ValueError as error:
            raise ValueError(f"{field} must be beneath source_root") from error


@dataclass(frozen=True, slots=True)
class LatexManuscriptAuditIssue:
    """Record one structural manuscript-source finding."""

    code: LatexManuscriptAuditIssueCode
    source_path: Path
    line: int
    subject: str

    def __post_init__(self) -> None:
        """Require exact issue fields and one-based source locations."""
        if type(self.code) is not LatexManuscriptAuditIssueCode:
            raise TypeError("code must be LatexManuscriptAuditIssueCode")
        if not isinstance(self.source_path, Path):
            raise TypeError("source_path must be pathlib.Path")
        if type(self.line) is not int:
            raise TypeError("line must be a built-in int")
        if self.line < 1:
            raise ValueError("line must be positive")
        if type(self.subject) is not str:
            raise TypeError("subject must be a built-in str")
        if not self.subject:
            raise ValueError("subject must be nonempty")


@dataclass(frozen=True, slots=True)
class LatexManuscriptAuditResult:
    """Retain the inspected source graph and deterministic findings."""

    source_paths: tuple[Path, ...]
    issues: tuple[LatexManuscriptAuditIssue, ...]

    def __post_init__(self) -> None:
        """Require deterministic, duplicate-free source and finding inventories."""
        if type(self.source_paths) is not tuple:
            raise TypeError("source_paths must be a tuple")
        if type(self.issues) is not tuple:
            raise TypeError("issues must be a tuple")
        if len(set(self.source_paths)) != len(self.source_paths):
            raise ValueError("source_paths must not contain duplicates")
        if tuple(sorted(self.source_paths)) != self.source_paths:
            raise ValueError("source_paths must be sorted")
        for path in self.source_paths:
            if not isinstance(path, Path):
                raise TypeError("every source_paths member must be pathlib.Path")
        for issue in self.issues:
            if type(issue) is not LatexManuscriptAuditIssue:
                raise TypeError("every issues member must be LatexManuscriptAuditIssue")

    @property
    def passes(self) -> bool:
        """Return whether the structural audit produced no findings."""
        return not self.issues


@dataclass(frozen=True, slots=True)
class LatexSource:
    """Retain one decoded LaTeX or bibliography source."""

    path: Path
    text: str
    visible_text: str = field(init=False)

    def __post_init__(self) -> None:
        """Require one absolute path and retain comment-stripped visible text."""
        if not isinstance(self.path, Path):
            raise TypeError("path must be pathlib.Path")
        if not self.path.is_absolute():
            raise ValueError("path must be absolute")
        if type(self.text) is not str:
            raise TypeError("text must be a built-in str")
        visible_lines: list[str] = []
        for line in self.text.splitlines(keepends=True):
            comment_start = len(line)
            for index, character in enumerate(line):
                if character != "%":
                    continue
                backslashes = 0
                cursor = index - 1
                while cursor >= 0 and line[cursor] == "\\":
                    backslashes += 1
                    cursor -= 1
                if backslashes % 2 == 0:
                    comment_start = index
                    break
            ending = "\n" if line.endswith("\n") else ""
            visible_lines.append(line[:comment_start].rstrip("\n") + ending)
        object.__setattr__(self, "visible_text", "".join(visible_lines))

    def line_number(self, offset: int) -> int:
        """Return a one-based line number for one visible-text offset."""
        if type(offset) is not int:
            raise TypeError("offset must be a built-in int")
        if offset < 0 or offset > len(self.visible_text):
            raise ValueError("offset must identify a visible-text position")
        return self.visible_text.count("\n", 0, offset) + 1


@dataclass(frozen=True, slots=True)
class LatexSourceGraph:
    """Retain decoded composition and bibliography sources in deterministic order."""

    composition_sources: tuple[LatexSource, ...]
    bibliography_sources: tuple[LatexSource, ...]

    def __post_init__(self) -> None:
        """Require sorted, duplicate-free, disjoint source collections."""
        if type(self.composition_sources) is not tuple:
            raise TypeError("composition_sources must be a tuple")
        if type(self.bibliography_sources) is not tuple:
            raise TypeError("bibliography_sources must be a tuple")
        for source in (*self.composition_sources, *self.bibliography_sources):
            if type(source) is not LatexSource:
                raise TypeError("every source graph member must be LatexSource")
        composition_paths = tuple(source.path for source in self.composition_sources)
        bibliography_paths = tuple(source.path for source in self.bibliography_sources)
        if composition_paths != tuple(sorted(composition_paths)):
            raise ValueError("composition_sources must be sorted by path")
        if bibliography_paths != tuple(sorted(bibliography_paths)):
            raise ValueError("bibliography_sources must be sorted by path")
        if len(set(composition_paths)) != len(composition_paths):
            raise ValueError("composition_sources must not contain duplicate paths")
        if len(set(bibliography_paths)) != len(bibliography_paths):
            raise ValueError("bibliography_sources must not contain duplicate paths")
        if set(composition_paths) & set(bibliography_paths):
            raise ValueError("composition and bibliography paths must be disjoint")

    @property
    def inspected_paths(self) -> tuple[Path, ...]:
        """Return every inspected path in deterministic order."""
        return tuple(
            sorted(
                source.path
                for source in (*self.composition_sources, *self.bibliography_sources)
            )
        )

    def composition_source_for(self, path: Path) -> LatexSource | None:
        """Return the composition source at ``path`` when it was loaded."""
        if not isinstance(path, Path):
            raise TypeError("path must be pathlib.Path")
        for source in self.composition_sources:
            if source.path == path:
                return source
        return None


@dataclass(frozen=True, slots=True)
class LatexSourceGraphConstructionResult:
    """Retain one constructed source graph and its composition findings."""

    graph: LatexSourceGraph
    issues: tuple[LatexManuscriptAuditIssue, ...]

    def __post_init__(self) -> None:
        """Require an exact source graph and issue tuple."""
        if type(self.graph) is not LatexSourceGraph:
            raise TypeError("graph must be LatexSourceGraph")
        if type(self.issues) is not tuple:
            raise TypeError("issues must be a tuple")
        for issue in self.issues:
            if type(issue) is not LatexManuscriptAuditIssue:
                raise TypeError("every issues member must be LatexManuscriptAuditIssue")
