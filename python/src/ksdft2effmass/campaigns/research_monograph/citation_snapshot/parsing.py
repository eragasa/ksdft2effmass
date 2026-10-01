"""Focused TeX and BibLaTeX source parsers for citation snapshot compilation.

The parsers implement a closed source grammar rather than executing TeX. Unknown
citation-capable macros and unsafe macro definitions fail closed. Parsed records are
internal structural observations and contain only keys, command metadata, paths, and
byte spans.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Never

from .records import (
    CitationSnapshotError,
    CitationSnapshotErrorCode,
    ManuscriptCitationCommandKind,
    ManuscriptCitationOrigin,
    ManuscriptCitationPriority,
)


@dataclass(frozen=True, slots=True)
class ParsedCitationKey:
    """Retain one parsed key and exact character span."""

    key: str
    char_start: int
    char_end: int


@dataclass(frozen=True, slots=True)
class ParsedCitationCall:
    """Retain one rendered source-level or macro-generated citation call."""

    command_kind: ManuscriptCitationCommandKind
    origin: ManuscriptCitationOrigin
    char_start: int
    char_end: int
    keys: tuple[ParsedCitationKey, ...]
    todo_local_index: int | None


@dataclass(frozen=True, slots=True)
class ParsedCitationTodo:
    """Retain one citationtodo marker and its generated calls."""

    char_start: int
    char_end: int
    priority_start: int
    priority_end: int
    priority: ManuscriptCitationPriority
    calls: tuple[ParsedCitationCall, ...]


@dataclass(frozen=True, slots=True)
class ParsedInclude:
    """Retain one include/input directive and exact path-token span."""

    char_start: int
    char_end: int
    path_start: int
    path_end: int
    relative_path: str
    ordinal: int


@dataclass(frozen=True, slots=True)
class ParsedSourceGap:
    """Retain one placeholder identifier token without an invented cite key."""

    char_start: int
    char_end: int
    placeholder_identifier: str


@dataclass(frozen=True, slots=True)
class ParsedTexSource:
    """Retain deterministic citation-bearing events from one TeX source."""

    text: str
    calls: tuple[ParsedCitationCall, ...]
    todos: tuple[ParsedCitationTodo, ...]
    includes: tuple[ParsedInclude, ...]
    gaps: tuple[ParsedSourceGap, ...]

    def byte_offset(self, char_offset: int) -> int:
        """Translate a character offset to an exact UTF-8 byte offset."""
        return len(self.text[:char_offset].encode("utf-8"))

    def line_column(self, char_offset: int) -> tuple[int, int]:
        """Return a one-based line and column for a character offset."""
        line = self.text.count("\n", 0, char_offset) + 1
        previous = self.text.rfind("\n", 0, char_offset)
        return line, char_offset - previous


@dataclass(frozen=True, slots=True)
class ParsedBibliographyEntry:
    """Retain one BibLaTeX entry's structural fields and exact character span."""

    entry_type: str
    key: str
    char_start: int
    char_end: int


@dataclass(frozen=True, slots=True)
class ParsedBibliography:
    """Retain ordered bibliography entries from exact UTF-8 source text."""

    text: str
    entries: tuple[ParsedBibliographyEntry, ...]

    def byte_offset(self, char_offset: int) -> int:
        """Translate a character offset to an exact UTF-8 byte offset."""
        return len(self.text[:char_offset].encode("utf-8"))

    def line_column(self, char_offset: int) -> tuple[int, int]:
        """Return a one-based line and column for a character offset."""
        line = self.text.count("\n", 0, char_offset) + 1
        previous = self.text.rfind("\n", 0, char_offset)
        return line, char_offset - previous


@dataclass(frozen=True, slots=True)
class TexCitationSourceParser:
    """Parse the closed citation grammar of one exact TeX source.

    The parser recognizes direct ``cite`` and ``eqincite`` calls, contextual
    ``citationtodo``/``texttt`` expansion, includes, balanced arguments, TeX
    comments, and harmless definitions. It never executes TeX.
    """

    def execute(self, source_bytes: bytes, source_path: str) -> ParsedTexSource:
        """Parse one UTF-8 TeX source or raise a fail-closed structural error."""
        if type(source_bytes) is not bytes:
            raise TypeError("source_bytes must be built-in bytes")
        if type(source_path) is not str or not source_path:
            raise TypeError("source_path must be a nonempty string")
        try:
            text = source_bytes.decode("utf-8")
        except UnicodeDecodeError as error:
            raise CitationSnapshotError(
                CitationSnapshotErrorCode.SOURCE_NOT_UTF8,
                source_path,
                error.start,
                "TeX source is not valid UTF-8",
            ) from None
        masked = self._mask_comments(text)
        self._validate_balanced_braces(masked, source_path)
        calls: list[ParsedCitationCall] = []
        todos: list[ParsedCitationTodo] = []
        includes: list[ParsedInclude] = []
        gaps: list[ParsedSourceGap] = []
        include_ordinal = 0
        index = 0
        while index < len(masked):
            if masked[index] != "\\":
                index += 1
                continue
            command_start = index
            name, after_name = self._command_name(masked, index)
            if name in {"def", "newcommand", "renewcommand", "newenvironment"}:
                index = self._definition_end(masked, after_name, name, source_path)
                continue
            if name in {"include", "input"}:
                argument, end = self._required_argument(
                    masked, after_name, source_path, command_start
                )
                value = masked[argument[0] : argument[1]].strip()
                if not value:
                    self._fail(
                        CitationSnapshotErrorCode.MALFORMED_TEX,
                        source_path,
                        command_start,
                        "include path is empty",
                    )
                left = argument[0]
                while left < argument[1] and masked[left].isspace():
                    left += 1
                right = argument[1]
                while right > left and masked[right - 1].isspace():
                    right -= 1
                includes.append(
                    ParsedInclude(
                        command_start,
                        end,
                        left,
                        right,
                        value,
                        include_ordinal,
                    )
                )
                include_ordinal += 1
                index = end
                continue
            if name == "cite":
                call, end = self._cite_call(
                    masked,
                    command_start,
                    after_name,
                    source_path,
                    ManuscriptCitationCommandKind.CITE,
                    ManuscriptCitationOrigin.DIRECT,
                    None,
                )
                calls.append(call)
                index = end
                continue
            if name == "eqincite":
                call, end = self._eqincite_call(
                    masked, command_start, after_name, source_path
                )
                calls.append(call)
                index = end
                continue
            if name == "citationtodo":
                todo, end = self._citation_todo(
                    masked, command_start, after_name, source_path
                )
                todos.append(todo)
                index = end
                continue
            if name == "path":
                argument, end = self._required_argument(
                    masked, after_name, source_path, command_start
                )
                value = masked[argument[0] : argument[1]].strip()
                if len(value) >= 4 and set(value) == {"X"}:
                    left = argument[0]
                    while left < argument[1] and masked[left].isspace():
                        left += 1
                    gaps.append(ParsedSourceGap(left, left + len(value), value))
                index = end
                continue
            if "cite" in name.lower():
                self._fail(
                    CitationSnapshotErrorCode.UNKNOWN_CITATION_MACRO,
                    source_path,
                    command_start,
                    f"unsupported citation-capable macro {name}",
                )
            index = after_name
        return ParsedTexSource(
            text,
            tuple(calls),
            tuple(todos),
            tuple(includes),
            tuple(gaps),
        )

    def _definition_end(
        self, text: str, index: int, kind: str, source_path: str
    ) -> int:
        start = index
        index = self._skip_space(text, index)
        macro_name = ""
        bodies: list[tuple[int, int]] = []
        if kind == "def":
            if index >= len(text) or text[index] != "\\":
                self._fail(
                    CitationSnapshotErrorCode.MALFORMED_TEX,
                    source_path,
                    start,
                    "def does not name a control sequence",
                )
            macro_name, index = self._command_name(text, index)
            while index < len(text) and text[index] != "{":
                index += 1
            body, index = self._balanced(text, index, "{", "}", source_path)
            bodies.append(body)
        else:
            if index < len(text) and text[index] == "*":
                index = self._skip_space(text, index + 1)
            if index < len(text) and text[index] == "{":
                argument, index = self._required_argument(
                    text, index, source_path, start
                )
                token = text[argument[0] : argument[1]].strip()
                if kind == "newenvironment":
                    if not token or any(
                        not (character.isalnum() or character in "@*-")
                        for character in token
                    ):
                        self._fail(
                            CitationSnapshotErrorCode.MALFORMED_TEX,
                            source_path,
                            start,
                            "environment definition name is malformed",
                        )
                    macro_name = token
                else:
                    if not token.startswith("\\"):
                        self._fail(
                            CitationSnapshotErrorCode.MALFORMED_TEX,
                            source_path,
                            start,
                            "definition does not name a control sequence",
                        )
                    macro_name, token_end = self._command_name(token, 0)
                    if token_end != len(token):
                        self._fail(
                            CitationSnapshotErrorCode.MALFORMED_TEX,
                            source_path,
                            start,
                            "definition control sequence is malformed",
                        )
            elif index < len(text) and text[index] == "\\":
                macro_name, index = self._command_name(text, index)
            else:
                self._fail(
                    CitationSnapshotErrorCode.MALFORMED_TEX,
                    source_path,
                    start,
                    "definition does not name a control sequence",
                )
            index = self._skip_optional_arguments(text, index, source_path)
            body_count = 2 if kind == "newenvironment" else 1
            for _ in range(body_count):
                body, index = self._required_argument(text, index, source_path, start)
                bodies.append(body)
        if macro_name in {"citationtodo", "eqincite"}:
            if kind not in {"newcommand", "renewcommand"}:
                self._fail(
                    CitationSnapshotErrorCode.UNSAFE_DEFINITION,
                    source_path,
                    start,
                    "known citation macro must use newcommand or renewcommand",
                )
            body_text = "".join(
                "".join(text[left:right].split()) for left, right in bodies
            )
            expected_bodies = {
                "eqincite": "Eq.~(#2)in~\\cite{#1}",
                "citationtodo": (
                    "\\begin{tcolorbox}[monographeditorial]"
                    "\\let\\editorialtexttt\\texttt"
                    "\\renewcommand{\\texttt}[1]"
                    "{\\editorialtexttt{##1}~\\cite{##1}}"
                    "{\\color{readingred}\\bfseries"
                    "Prospectivecitationnote---#1\\par}"
                    "#2\\par\\smallskip"
                    "\\textit{Editorialstatus:prospective."
                    "Readthecandidatesourcesandchecktheexactclaimbeforeaddingor"
                    "changingacitation.}"
                    "\\end{tcolorbox}"
                ),
            }
            if body_text != expected_bodies[macro_name]:
                self._fail(
                    CitationSnapshotErrorCode.UNSAFE_DEFINITION,
                    source_path,
                    start,
                    f"known citation macro {macro_name} has unsupported semantics",
                )
            return index
        if "cite" in macro_name.lower():
            self._fail(
                CitationSnapshotErrorCode.UNKNOWN_CITATION_MACRO,
                source_path,
                start,
                f"unsupported citation macro definition {macro_name}",
            )
        for body_start, body_end in bodies:
            body_text = text[body_start:body_end]
            if self._contains_citation_command(body_text):
                self._fail(
                    CitationSnapshotErrorCode.UNSAFE_DEFINITION,
                    source_path,
                    body_start,
                    f"noncitation definition {macro_name} contains citation syntax",
                )
        return index

    def _contains_citation_command(self, text: str) -> bool:
        index = 0
        while index < len(text):
            if text[index] != "\\":
                index += 1
                continue
            name, index = self._command_name(text, index)
            if "cite" in name.lower() or name == "citationtodo":
                return True
        return False

    def _cite_call(
        self,
        text: str,
        command_start: int,
        index: int,
        source_path: str,
        command_kind: ManuscriptCitationCommandKind,
        origin: ManuscriptCitationOrigin,
        todo_local_index: int | None,
    ) -> tuple[ParsedCitationCall, int]:
        index = self._skip_optional_arguments(text, index, source_path)
        argument, end = self._required_argument(text, index, source_path, command_start)
        keys = self._citation_keys(text, argument, source_path)
        return (
            ParsedCitationCall(
                command_kind,
                origin,
                command_start,
                end,
                keys,
                todo_local_index,
            ),
            end,
        )

    def _eqincite_call(
        self, text: str, command_start: int, index: int, source_path: str
    ) -> tuple[ParsedCitationCall, int]:
        first, index = self._required_argument(text, index, source_path, command_start)
        _, end = self._required_argument(text, index, source_path, command_start)
        keys = self._citation_keys(text, first, source_path)
        if len(keys) != 1:
            self._fail(
                CitationSnapshotErrorCode.MALFORMED_TEX,
                source_path,
                command_start,
                "eqincite requires exactly one citation key",
            )
        return (
            ParsedCitationCall(
                ManuscriptCitationCommandKind.EQINCITE,
                ManuscriptCitationOrigin.EQINCITE_EXPANSION,
                command_start,
                end,
                keys,
                None,
            ),
            end,
        )

    def _citation_todo(
        self, text: str, command_start: int, index: int, source_path: str
    ) -> tuple[ParsedCitationTodo, int]:
        priority_argument, index = self._required_argument(
            text, index, source_path, command_start
        )
        body_argument, end = self._required_argument(
            text, index, source_path, command_start
        )
        priority_text = text[priority_argument[0] : priority_argument[1]].strip()
        priorities = {
            "high priority": ManuscriptCitationPriority.HIGH,
            "medium priority": ManuscriptCitationPriority.MEDIUM,
            "low priority": ManuscriptCitationPriority.LOW,
        }
        priority = priorities.get(priority_text)
        if priority is None:
            self._fail(
                CitationSnapshotErrorCode.MALFORMED_TEX,
                source_path,
                priority_argument[0],
                "citationtodo priority is outside the closed vocabulary",
            )
        generated: list[ParsedCitationCall] = []
        cursor = body_argument[0]
        local_index = 0
        while cursor < body_argument[1]:
            if text[cursor] != "\\":
                cursor += 1
                continue
            nested_start = cursor
            name, nested_after = self._command_name(text, cursor)
            if name == "texttt":
                argument, nested_end = self._required_argument(
                    text, nested_after, source_path, nested_start
                )
                keys = self._citation_keys(text, argument, source_path)
                if len(keys) != 1:
                    self._fail(
                        CitationSnapshotErrorCode.MALFORMED_TEX,
                        source_path,
                        nested_start,
                        "citationtodo texttt token must contain exactly one key",
                    )
                generated.append(
                    ParsedCitationCall(
                        ManuscriptCitationCommandKind.CITE,
                        ManuscriptCitationOrigin.CITATION_TODO_EXPANSION,
                        nested_start,
                        nested_end,
                        keys,
                        local_index,
                    )
                )
                local_index += 1
                cursor = nested_end
                continue
            if "cite" in name.lower() or name == "citationtodo":
                self._fail(
                    CitationSnapshotErrorCode.UNKNOWN_CITATION_MACRO,
                    source_path,
                    nested_start,
                    "citationtodo body contains unsupported citation syntax",
                )
            cursor = nested_after
        if not generated:
            self._fail(
                CitationSnapshotErrorCode.MALFORMED_TEX,
                source_path,
                command_start,
                "citationtodo must contain at least one texttt citation key",
            )
        priority_start = priority_argument[0]
        while priority_start < priority_argument[1] and text[priority_start].isspace():
            priority_start += 1
        priority_end = priority_argument[1]
        while priority_end > priority_start and text[priority_end - 1].isspace():
            priority_end -= 1
        return (
            ParsedCitationTodo(
                command_start,
                end,
                priority_start,
                priority_end,
                priority,
                tuple(generated),
            ),
            end,
        )

    def _citation_keys(
        self, text: str, argument: tuple[int, int], source_path: str
    ) -> tuple[ParsedCitationKey, ...]:
        keys: list[ParsedCitationKey] = []
        start, end = argument
        token_start = start
        depth = 0
        cursor = start
        boundaries: list[tuple[int, int]] = []
        while cursor < end:
            character = text[cursor]
            if character == "\\":
                cursor += 2
                continue
            if character == "{":
                depth += 1
            elif character == "}":
                depth -= 1
            elif character == "," and depth == 0:
                boundaries.append((token_start, cursor))
                token_start = cursor + 1
            cursor += 1
        boundaries.append((token_start, end))
        for left, right in boundaries:
            while left < right and text[left].isspace():
                left += 1
            while right > left and text[right - 1].isspace():
                right -= 1
            key = text[left:right]
            if not key or any(character.isspace() for character in key):
                self._fail(
                    CitationSnapshotErrorCode.MALFORMED_TEX,
                    source_path,
                    left,
                    "citation key is empty or contains whitespace",
                )
            keys.append(ParsedCitationKey(key, left, right))
        return tuple(keys)

    def _skip_optional_arguments(self, text: str, index: int, source_path: str) -> int:
        index = self._skip_space(text, index)
        while index < len(text) and text[index] == "[":
            _, index = self._balanced(text, index, "[", "]", source_path)
            index = self._skip_space(text, index)
        return index

    def _required_argument(
        self, text: str, index: int, source_path: str, command_start: int
    ) -> tuple[tuple[int, int], int]:
        index = self._skip_space(text, index)
        if index >= len(text) or text[index] != "{":
            self._fail(
                CitationSnapshotErrorCode.MALFORMED_TEX,
                source_path,
                command_start,
                "command is missing a required braced argument",
            )
        return self._balanced(text, index, "{", "}", source_path)

    def _balanced(
        self, text: str, index: int, opening: str, closing: str, source_path: str
    ) -> tuple[tuple[int, int], int]:
        if index >= len(text) or text[index] != opening:
            self._fail(
                CitationSnapshotErrorCode.MALFORMED_TEX,
                source_path,
                index,
                "balanced group does not begin with its opening delimiter",
            )
        depth = 1
        cursor = index + 1
        while cursor < len(text):
            if text[cursor] == "\\":
                cursor += 2
                continue
            if text[cursor] == opening:
                depth += 1
            elif text[cursor] == closing:
                depth -= 1
                if depth == 0:
                    return (index + 1, cursor), cursor + 1
            cursor += 1
        self._fail(
            CitationSnapshotErrorCode.MALFORMED_TEX,
            source_path,
            index,
            "source contains an unbalanced group",
        )

    def _validate_balanced_braces(self, text: str, source_path: str) -> None:
        """Reject globally unbalanced TeX braces before semantic extraction."""
        stack: list[int] = []
        cursor = 0
        while cursor < len(text):
            if text[cursor] == "\\":
                cursor += 2
                continue
            if text[cursor] == "{":
                stack.append(cursor)
            elif text[cursor] == "}":
                if not stack:
                    self._fail(
                        CitationSnapshotErrorCode.MALFORMED_TEX,
                        source_path,
                        cursor,
                        "source contains an unmatched closing brace",
                    )
                stack.pop()
            cursor += 1
        if stack:
            self._fail(
                CitationSnapshotErrorCode.MALFORMED_TEX,
                source_path,
                stack[-1],
                "source contains an unmatched opening brace",
            )

    @staticmethod
    def _skip_space(text: str, index: int) -> int:
        while index < len(text) and text[index].isspace():
            index += 1
        return index

    def _command_name(self, text: str, index: int) -> tuple[str, int]:
        if index >= len(text) or text[index] != "\\":
            return "", index
        cursor = index + 1
        if cursor < len(text) and (text[cursor].isalpha() or text[cursor] == "@"):
            while cursor < len(text) and (
                text[cursor].isalpha() or text[cursor] == "@"
            ):
                cursor += 1
            return text[index + 1 : cursor], cursor
        if cursor < len(text):
            return text[cursor], cursor + 1
        return "", cursor

    def _mask_comments(self, text: str) -> str:
        characters = list(text)
        line_start = 0
        while line_start < len(characters):
            newline = text.find("\n", line_start)
            line_end = len(characters) if newline == -1 else newline
            cursor = line_start
            while cursor < line_end:
                if characters[cursor] == "%":
                    backslashes = 0
                    previous = cursor - 1
                    while previous >= line_start and characters[previous] == "\\":
                        backslashes += 1
                        previous -= 1
                    if backslashes % 2 == 0:
                        for position in range(cursor, line_end):
                            characters[position] = " "
                        break
                cursor += 1
            if newline == -1:
                break
            line_start = newline + 1
        return "".join(characters)

    @staticmethod
    def _fail(
        code: CitationSnapshotErrorCode,
        source_path: str,
        offset: int,
        detail: str,
    ) -> Never:
        raise CitationSnapshotError(code, source_path, offset, detail)


@dataclass(frozen=True, slots=True)
class BiblatexSourceParser:
    """Parse ordered entry boundaries and keys from one BibLaTeX source."""

    def execute(self, source_bytes: bytes, source_path: str) -> ParsedBibliography:
        """Parse exact UTF-8 bibliography bytes and reject malformed entries."""
        if type(source_bytes) is not bytes:
            raise TypeError("source_bytes must be built-in bytes")
        try:
            text = source_bytes.decode("utf-8")
        except UnicodeDecodeError as error:
            raise CitationSnapshotError(
                CitationSnapshotErrorCode.SOURCE_NOT_UTF8,
                source_path,
                error.start,
                "bibliography source is not valid UTF-8",
            ) from None
        masked = self._mask_comments(text)
        entries: list[ParsedBibliographyEntry] = []
        keys: set[str] = set()
        cursor = 0
        while cursor < len(masked):
            marker = masked.find("@", cursor)
            if marker == -1:
                break
            type_start = marker + 1
            type_end = type_start
            while type_end < len(masked) and masked[type_end].isalpha():
                type_end += 1
            entry_type = masked[type_start:type_end].lower()
            if not entry_type:
                raise CitationSnapshotError(
                    CitationSnapshotErrorCode.MALFORMED_BIBLIOGRAPHY,
                    source_path,
                    marker,
                    "bibliography at-sign does not begin an entry type",
                )
            opening_index = self._skip_space(masked, type_end)
            if opening_index >= len(masked) or masked[opening_index] not in "{(":
                raise CitationSnapshotError(
                    CitationSnapshotErrorCode.MALFORMED_BIBLIOGRAPHY,
                    source_path,
                    marker,
                    "bibliography entry lacks an opening delimiter",
                )
            opening = masked[opening_index]
            closing = "}" if opening == "{" else ")"
            body, end = self._balanced(
                masked, opening_index, opening, closing, source_path
            )
            if entry_type in {"comment", "string", "preamble"}:
                cursor = end
                continue
            comma = masked.find(",", body[0], body[1])
            if comma == -1:
                raise CitationSnapshotError(
                    CitationSnapshotErrorCode.MALFORMED_BIBLIOGRAPHY,
                    source_path,
                    marker,
                    "bibliography entry lacks a key separator",
                )
            key = masked[body[0] : comma].strip()
            if not key or any(character.isspace() for character in key):
                raise CitationSnapshotError(
                    CitationSnapshotErrorCode.MALFORMED_BIBLIOGRAPHY,
                    source_path,
                    body[0],
                    "bibliography key is empty or contains whitespace",
                )
            if key in keys:
                raise CitationSnapshotError(
                    CitationSnapshotErrorCode.BIBLIOGRAPHY_DUPLICATE_KEY,
                    source_path,
                    body[0],
                    f"duplicate bibliography key {key}",
                )
            keys.add(key)
            entries.append(ParsedBibliographyEntry(entry_type, key, marker, end))
            cursor = end
        return ParsedBibliography(text, tuple(entries))

    @staticmethod
    def _skip_space(text: str, index: int) -> int:
        while index < len(text) and text[index].isspace():
            index += 1
        return index

    def _mask_comments(self, text: str) -> str:
        characters = list(text)
        line_start = 0
        while line_start < len(characters):
            newline = text.find("\n", line_start)
            line_end = len(characters) if newline == -1 else newline
            cursor = line_start
            while cursor < line_end:
                if characters[cursor] == "%":
                    backslashes = 0
                    previous = cursor - 1
                    while previous >= line_start and characters[previous] == "\\":
                        backslashes += 1
                        previous -= 1
                    if backslashes % 2 == 0:
                        for position in range(cursor, line_end):
                            characters[position] = " "
                        break
                cursor += 1
            if newline == -1:
                break
            line_start = newline + 1
        return "".join(characters)

    def _balanced(
        self, text: str, index: int, opening: str, closing: str, source_path: str
    ) -> tuple[tuple[int, int], int]:
        depth = 1
        cursor = index + 1
        while cursor < len(text):
            if text[cursor] == "\\":
                cursor += 2
                continue
            if text[cursor] == opening:
                depth += 1
            elif text[cursor] == closing:
                depth -= 1
                if depth == 0:
                    return (index + 1, cursor), cursor + 1
            cursor += 1
        raise CitationSnapshotError(
            CitationSnapshotErrorCode.MALFORMED_BIBLIOGRAPHY,
            source_path,
            index,
            "bibliography source contains an unbalanced entry",
        )
