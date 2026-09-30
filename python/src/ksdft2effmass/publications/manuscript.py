"""Typed structural auditing for the research-monograph LaTeX source graph.

The audit checks source composition, cross-reference and literal citation-key
integrity, and explicitly selected equation-explanation contracts. It does not
interpret mathematical meaning, establish citation quality, or replace a LaTeX
build.
"""

import re
from dataclasses import dataclass
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


class LatexManuscriptAuditor:
    """Audit one LaTeX source graph without invoking external programs."""

    __slots__ = ()

    _bibliography_pattern = re.compile(
        r"\\addbibresource(?:\s*\[[^\]]*\])?\{([^{}]+)\}"
    )
    _bibliography_key_pattern = re.compile(
        r"^[ \t]*@[A-Za-z]+\s*[{(]\s*([^,\s]+)\s*,", re.MULTILINE
    )
    _citation_pattern = re.compile(
        r"\\(?:cite|parencite|textcite|autocite|footcite|supercite|nocite)\*?"
        r"(?:\s*\[[^\]]*\]){0,2}\s*\{([^{}]+)\}"
    )
    _include_pattern = re.compile(r"\\(?:include|input)\{([^{}]+)\}")
    _label_pattern = re.compile(r"\\label\{([^{}]+)\}")
    _reference_pattern = re.compile(r"\\(?:ref|eqref|pageref|autoref)\{([^{}]+)\}")
    _display_pattern = re.compile(
        r"\\begin\{(?P<environment>"
        r"equation\*?|align\*?|gather\*?|multline\*?"
        r")\}"
        r"(?P<body>.*?)"
        r"\\end\{(?P=environment)\}",
        re.DOTALL,
    )
    _equation_terms_pattern = re.compile(
        r"\\begin\{equationterms\}"
        r"(?:\{(?P<label>[^{}]*)\})?"
        r"(?P<body>.*?)"
        r"\\end\{equationterms\}",
        re.DOTALL,
    )
    _equation_term_command = r"\equationterm"

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

        issues: list[LatexManuscriptAuditIssue] = []
        sources: dict[Path, str] = {}
        self._load_source_graph(
            request,
            request.composition_path,
            (),
            sources,
            issues,
        )
        bibliographies = self._load_bibliographies(request, sources, issues)
        self._audit_labels_and_references(sources, issues)
        self._audit_citations(sources, bibliographies, issues)
        self._audit_equation_terms(request, sources, issues)
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
        inspected_paths = tuple(sorted(set(sources) | set(bibliographies)))
        return LatexManuscriptAuditResult(inspected_paths, ordered_issues)

    def _load_source_graph(
        self,
        request: LatexManuscriptAuditRequest,
        path: Path,
        ancestors: tuple[Path, ...],
        sources: dict[Path, str],
        issues: list[LatexManuscriptAuditIssue],
    ) -> None:
        """Load one source and recursively follow its LaTeX composition edges."""
        if path in ancestors:
            parent = ancestors[-1] if ancestors else request.composition_path
            issues.append(
                LatexManuscriptAuditIssue(
                    LatexManuscriptAuditIssueCode.INCLUDE_CYCLE,
                    parent,
                    1,
                    str(path.relative_to(request.source_root)),
                )
            )
            return
        if path in sources:
            return
        if not path.is_file():
            issues.append(
                LatexManuscriptAuditIssue(
                    LatexManuscriptAuditIssueCode.MISSING_SOURCE,
                    path,
                    1,
                    str(path),
                )
            )
            return

        text = path.read_text(encoding="utf-8")
        sources[path] = text
        visible = self._without_comments(text)
        for match in self._include_pattern.finditer(visible):
            target = self._include_path(request.source_root, match.group(1))
            line = self._line(visible, match.start())
            if target is None:
                issues.append(
                    LatexManuscriptAuditIssue(
                        LatexManuscriptAuditIssueCode.INCLUDE_PATH_ESCAPE,
                        path,
                        line,
                        match.group(1),
                    )
                )
                continue
            if not target.is_file():
                issues.append(
                    LatexManuscriptAuditIssue(
                        LatexManuscriptAuditIssueCode.MISSING_INCLUDE,
                        path,
                        line,
                        match.group(1),
                    )
                )
                continue
            self._load_source_graph(
                request,
                target,
                (*ancestors, path),
                sources,
                issues,
            )

    def _load_bibliographies(
        self,
        request: LatexManuscriptAuditRequest,
        sources: dict[Path, str],
        issues: list[LatexManuscriptAuditIssue],
    ) -> dict[Path, str]:
        """Load contained BibLaTeX resources declared by composition sources."""
        bibliographies: dict[Path, str] = {}
        for source_path in sorted(sources):
            visible = self._without_comments(sources[source_path])
            for match in self._bibliography_pattern.finditer(visible):
                target_text = match.group(1).strip()
                target = self._bibliography_path(request.source_root, target_text)
                line = self._line(visible, match.start())
                if target is None:
                    issues.append(
                        LatexManuscriptAuditIssue(
                            LatexManuscriptAuditIssueCode.BIBLIOGRAPHY_PATH_ESCAPE,
                            source_path,
                            line,
                            target_text,
                        )
                    )
                    continue
                if not target.is_file():
                    issues.append(
                        LatexManuscriptAuditIssue(
                            LatexManuscriptAuditIssueCode.MISSING_BIBLIOGRAPHY,
                            source_path,
                            line,
                            target_text,
                        )
                    )
                    continue
                if target not in bibliographies:
                    bibliographies[target] = target.read_text(encoding="utf-8")
        return bibliographies

    def _audit_labels_and_references(
        self,
        sources: dict[Path, str],
        issues: list[LatexManuscriptAuditIssue],
    ) -> None:
        """Report duplicate labels and references absent from the source graph."""
        label_locations: dict[str, tuple[Path, int]] = {}
        references: list[tuple[str, Path, int]] = []
        for path in sorted(sources):
            visible = self._without_comments(sources[path])
            for match in self._label_pattern.finditer(visible):
                label = match.group(1)
                line = self._line(visible, match.start())
                first = label_locations.get(label)
                if first is None:
                    label_locations[label] = (path, line)
                else:
                    issues.append(
                        LatexManuscriptAuditIssue(
                            LatexManuscriptAuditIssueCode.DUPLICATE_LABEL,
                            path,
                            line,
                            f"{label}; first at {first[0]}:{first[1]}",
                        )
                    )
            for match in self._reference_pattern.finditer(visible):
                references.append(
                    (match.group(1), path, self._line(visible, match.start()))
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
        sources: dict[Path, str],
        bibliographies: dict[Path, str],
        issues: list[LatexManuscriptAuditIssue],
    ) -> None:
        """Report duplicate bibliography keys and unresolved literal citations."""
        key_locations: dict[str, tuple[Path, int]] = {}
        for path in sorted(bibliographies):
            visible = self._without_comments(bibliographies[path])
            for match in self._bibliography_key_pattern.finditer(visible):
                key = match.group(1)
                line = self._line(visible, match.start())
                first = key_locations.get(key)
                if first is None:
                    key_locations[key] = (path, line)
                else:
                    issues.append(
                        LatexManuscriptAuditIssue(
                            LatexManuscriptAuditIssueCode.DUPLICATE_BIBLIOGRAPHY_KEY,
                            path,
                            line,
                            f"{key}; first at {first[0]}:{first[1]}",
                        )
                    )

        for path in sorted(sources):
            visible = self._without_comments(sources[path])
            for match in self._citation_pattern.finditer(visible):
                line = self._line(visible, match.start())
                for raw_key in match.group(1).split(","):
                    key = raw_key.strip()
                    if not key or key == "*" or "#" in key:
                        continue
                    if key not in key_locations:
                        issues.append(
                            LatexManuscriptAuditIssue(
                                LatexManuscriptAuditIssueCode.UNRESOLVED_CITATION,
                                path,
                                line,
                                key,
                            )
                        )

    def _audit_equation_terms(
        self,
        request: LatexManuscriptAuditRequest,
        sources: dict[Path, str],
        issues: list[LatexManuscriptAuditIssue],
    ) -> None:
        """Require stable equation labels and paired, well-formed term definitions."""
        for path in request.equation_terms_paths:
            text = sources.get(path)
            if text is None:
                issues.append(
                    LatexManuscriptAuditIssue(
                        LatexManuscriptAuditIssueCode.MISSING_SOURCE,
                        path,
                        1,
                        "equation-terms source was not loaded by the composition",
                    )
                )
                continue
            visible = self._without_comments(text)
            term_spans = [
                match.span() for match in self._equation_terms_pattern.finditer(visible)
            ]
            consumed_term_starts: set[int] = set()
            for display in self._display_pattern.finditer(visible):
                display_line = self._line(visible, display.start())
                display_environment = display.group("environment")
                display_labels = tuple(
                    self._label_pattern.findall(display.group("body"))
                )
                equation_label: str | None = None
                if not display_labels:
                    issues.append(
                        LatexManuscriptAuditIssue(
                            LatexManuscriptAuditIssueCode.MISSING_EQUATION_LABEL,
                            path,
                            display_line,
                            display_environment,
                        )
                    )
                elif len(display_labels) > 1:
                    issues.append(
                        LatexManuscriptAuditIssue(
                            LatexManuscriptAuditIssueCode.MULTIPLE_EQUATION_LABELS,
                            path,
                            display_line,
                            ",".join(display_labels),
                        )
                    )
                else:
                    equation_label = display_labels[0]

                following = visible[display.end() :]
                terms = self._equation_terms_pattern.match(following.lstrip())
                if terms is None:
                    issues.append(
                        LatexManuscriptAuditIssue(
                            LatexManuscriptAuditIssueCode.MISSING_EQUATION_TERMS,
                            path,
                            display_line,
                            equation_label or display_environment,
                        )
                    )
                    continue
                whitespace = len(following) - len(following.lstrip())
                term_start = display.end() + whitespace + terms.start()
                term_line = self._line(visible, term_start)
                consumed_term_starts.add(term_start)

                term_label = terms.group("label")
                if term_label is None or not term_label.strip():
                    issues.append(
                        LatexManuscriptAuditIssue(
                            LatexManuscriptAuditIssueCode.MISSING_EQUATION_TERMS_LABEL,
                            path,
                            term_line,
                            equation_label or display_environment,
                        )
                    )
                elif equation_label is not None and term_label != equation_label:
                    issues.append(
                        LatexManuscriptAuditIssue(
                            LatexManuscriptAuditIssueCode.MISMATCHED_EQUATION_TERMS_LABEL,
                            path,
                            term_line,
                            f"{equation_label}!={term_label}",
                        )
                    )

                entries = self._equation_term_entries(terms.group("body"))
                if entries is None:
                    issues.append(
                        LatexManuscriptAuditIssue(
                            LatexManuscriptAuditIssueCode.MALFORMED_EQUATION_TERM,
                            path,
                            term_line,
                            equation_label or display_environment,
                        )
                    )
                    continue
                if not entries:
                    issues.append(
                        LatexManuscriptAuditIssue(
                            LatexManuscriptAuditIssueCode.EMPTY_EQUATION_TERMS,
                            path,
                            term_line,
                            equation_label or display_environment,
                        )
                    )
                    continue

                seen_symbols: set[str] = set()
                for symbol, definition in entries:
                    if not symbol:
                        issues.append(
                            LatexManuscriptAuditIssue(
                                LatexManuscriptAuditIssueCode.EMPTY_EQUATION_TERM_SYMBOL,
                                path,
                                term_line,
                                equation_label or display_environment,
                            )
                        )
                    elif symbol in seen_symbols:
                        issues.append(
                            LatexManuscriptAuditIssue(
                                LatexManuscriptAuditIssueCode.DUPLICATE_EQUATION_TERM_SYMBOL,
                                path,
                                term_line,
                                symbol,
                            )
                        )
                    else:
                        seen_symbols.add(symbol)
                    if not definition:
                        issues.append(
                            LatexManuscriptAuditIssue(
                                LatexManuscriptAuditIssueCode.EMPTY_EQUATION_TERM_DEFINITION,
                                path,
                                term_line,
                                symbol or equation_label or display_environment,
                            )
                        )
            for start, _ in term_spans:
                if start not in consumed_term_starts:
                    issues.append(
                        LatexManuscriptAuditIssue(
                            LatexManuscriptAuditIssueCode.ORPHAN_EQUATION_TERMS,
                            path,
                            self._line(visible, start),
                            "equationterms",
                        )
                    )

    def _equation_term_entries(self, body: str) -> tuple[tuple[str, str], ...] | None:
        """Parse consecutive ``equationterm`` commands with balanced arguments."""
        entries: list[tuple[str, str]] = []
        cursor = 0
        while True:
            cursor = self._skip_whitespace(body, cursor)
            if cursor == len(body):
                return tuple(entries)
            if not body.startswith(self._equation_term_command, cursor):
                return None
            cursor += len(self._equation_term_command)
            symbol_group = self._braced_group(body, cursor)
            if symbol_group is None:
                return None
            symbol, cursor = symbol_group
            definition_group = self._braced_group(body, cursor)
            if definition_group is None:
                return None
            definition, cursor = definition_group
            entries.append((symbol.strip(), definition.strip()))

    @classmethod
    def _braced_group(cls, text: str, cursor: int) -> tuple[str, int] | None:
        """Read one nested, whitespace-prefixed TeX brace group."""
        cursor = cls._skip_whitespace(text, cursor)
        if cursor == len(text) or text[cursor] != "{":
            return None
        start = cursor + 1
        depth = 1
        cursor = start
        while cursor < len(text):
            character = text[cursor]
            if character in "{}" and not cls._is_escaped(text, cursor):
                if character == "{":
                    depth += 1
                else:
                    depth -= 1
                    if depth == 0:
                        return text[start:cursor], cursor + 1
            cursor += 1
        return None

    @staticmethod
    def _is_escaped(text: str, cursor: int) -> bool:
        """Return whether the character at ``cursor`` has an odd backslash prefix."""
        backslashes = 0
        cursor -= 1
        while cursor >= 0 and text[cursor] == "\\":
            backslashes += 1
            cursor -= 1
        return backslashes % 2 == 1

    @staticmethod
    def _skip_whitespace(text: str, cursor: int) -> int:
        """Advance one cursor over whitespace without changing other text."""
        while cursor < len(text) and text[cursor].isspace():
            cursor += 1
        return cursor

    @staticmethod
    def _bibliography_path(source_root: Path, target_text: str) -> Path | None:
        """Resolve one extension-optional bibliography path beneath the source root."""
        target = Path(target_text)
        if target.suffix == "":
            target = target.with_suffix(".bib")
        resolved = source_root / target
        try:
            resolved.relative_to(source_root)
        except ValueError:
            return None
        if ".." in target.parts:
            return None
        return resolved

    @staticmethod
    def _include_path(source_root: Path, target_text: str) -> Path | None:
        """Resolve one extension-optional include path within the source root."""
        target = Path(target_text)
        if target.suffix == "":
            target = target.with_suffix(".tex")
        resolved = source_root / target
        try:
            resolved.relative_to(source_root)
        except ValueError:
            return None
        if ".." in target.parts:
            return None
        return resolved

    @staticmethod
    def _without_comments(text: str) -> str:
        """Replace unescaped TeX comments while preserving source line numbers."""
        visible_lines: list[str] = []
        for line in text.splitlines(keepends=True):
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
        return "".join(visible_lines)

    @staticmethod
    def _line(text: str, offset: int) -> int:
        """Return a one-based line number for one character offset."""
        return text.count("\n", 0, offset) + 1
