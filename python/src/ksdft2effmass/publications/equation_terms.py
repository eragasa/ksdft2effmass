"""Structural auditing of labelled LaTeX equation-term contracts."""

import re

from ksdft2effmass.publications.audit_records import (
    LatexManuscriptAuditIssue,
    LatexManuscriptAuditIssueCode,
    LatexManuscriptAuditRequest,
    LatexSource,
    LatexSourceGraph,
)


class LatexEquationTermsAuditor:
    """Audit labelled display equations and their structured term definitions."""

    __slots__ = ()

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
    _label_pattern = re.compile(r"\\label\{([^{}]+)\}")

    def execute(
        self,
        request: LatexManuscriptAuditRequest,
        graph: LatexSourceGraph,
    ) -> tuple[LatexManuscriptAuditIssue, ...]:
        """Return equation-contract findings for explicitly selected sources."""
        if type(request) is not LatexManuscriptAuditRequest:
            raise TypeError("request must be LatexManuscriptAuditRequest")
        if type(graph) is not LatexSourceGraph:
            raise TypeError("graph must be LatexSourceGraph")

        issues: list[LatexManuscriptAuditIssue] = []
        for path in request.equation_terms_paths:
            source = graph.composition_source_for(path)
            if source is None:
                issues.append(
                    LatexManuscriptAuditIssue(
                        LatexManuscriptAuditIssueCode.MISSING_SOURCE,
                        path,
                        1,
                        "equation-terms source was not loaded by the composition",
                    )
                )
                continue
            self._audit_source(source, issues)
        return tuple(issues)

    def _audit_source(
        self,
        source: LatexSource,
        issues: list[LatexManuscriptAuditIssue],
    ) -> None:
        """Audit equation-term bindings within one loaded composition source."""
        visible = source.visible_text
        term_spans = [
            match.span() for match in self._equation_terms_pattern.finditer(visible)
        ]
        consumed_term_starts: set[int] = set()
        for display in self._display_pattern.finditer(visible):
            display_line = source.line_number(display.start())
            display_environment = display.group("environment")
            display_labels = tuple(self._label_pattern.findall(display.group("body")))
            equation_label: str | None = None
            if not display_labels:
                issues.append(
                    LatexManuscriptAuditIssue(
                        LatexManuscriptAuditIssueCode.MISSING_EQUATION_LABEL,
                        source.path,
                        display_line,
                        display_environment,
                    )
                )
            elif len(display_labels) > 1:
                issues.append(
                    LatexManuscriptAuditIssue(
                        LatexManuscriptAuditIssueCode.MULTIPLE_EQUATION_LABELS,
                        source.path,
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
                        source.path,
                        display_line,
                        equation_label or display_environment,
                    )
                )
                continue
            whitespace = len(following) - len(following.lstrip())
            term_start = display.end() + whitespace + terms.start()
            term_line = source.line_number(term_start)
            consumed_term_starts.add(term_start)

            term_label = terms.group("label")
            if term_label is None or not term_label.strip():
                issues.append(
                    LatexManuscriptAuditIssue(
                        LatexManuscriptAuditIssueCode.MISSING_EQUATION_TERMS_LABEL,
                        source.path,
                        term_line,
                        equation_label or display_environment,
                    )
                )
            elif equation_label is not None and term_label != equation_label:
                issues.append(
                    LatexManuscriptAuditIssue(
                        LatexManuscriptAuditIssueCode.MISMATCHED_EQUATION_TERMS_LABEL,
                        source.path,
                        term_line,
                        f"{equation_label}!={term_label}",
                    )
                )

            entries = self._equation_term_entries(terms.group("body"))
            if entries is None:
                issues.append(
                    LatexManuscriptAuditIssue(
                        LatexManuscriptAuditIssueCode.MALFORMED_EQUATION_TERM,
                        source.path,
                        term_line,
                        equation_label or display_environment,
                    )
                )
                continue
            if not entries:
                issues.append(
                    LatexManuscriptAuditIssue(
                        LatexManuscriptAuditIssueCode.EMPTY_EQUATION_TERMS,
                        source.path,
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
                            source.path,
                            term_line,
                            equation_label or display_environment,
                        )
                    )
                elif symbol in seen_symbols:
                    issues.append(
                        LatexManuscriptAuditIssue(
                            LatexManuscriptAuditIssueCode.DUPLICATE_EQUATION_TERM_SYMBOL,
                            source.path,
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
                            source.path,
                            term_line,
                            symbol or equation_label or display_environment,
                        )
                    )
        for start, _ in term_spans:
            if start not in consumed_term_starts:
                issues.append(
                    LatexManuscriptAuditIssue(
                        LatexManuscriptAuditIssueCode.ORPHAN_EQUATION_TERMS,
                        source.path,
                        source.line_number(start),
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
