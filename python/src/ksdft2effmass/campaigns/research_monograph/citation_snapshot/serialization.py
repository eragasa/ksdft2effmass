"""Canonical unversioned JSON wire for complete citation snapshot results.

The codec maps one replay-valid owner Result to deterministic UTF-8 JSON bytes and
reconstructs the exact immutable Result from those bytes.  It owns no source
selection, file writing, persistence, runtime state, downstream authority, or
scientific acceptance.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from ksdft2effmass.serialization import JsonCodec

from .integrity import ResearchMonographCitationSnapshotIntegrityValidator
from .records import (
    CitationContentAlgorithm,
    CitationContentIdentity,
    ManuscriptBibliographyEntrySnapshot,
    ManuscriptCitationCall,
    ManuscriptCitationCommandKind,
    ManuscriptCitationGroup,
    ManuscriptCitationOccurrence,
    ManuscriptCitationOrigin,
    ManuscriptCitationPriority,
    ManuscriptCitationSnapshot,
    ManuscriptCitationSourceGap,
    ManuscriptCitationSourceGapReason,
    ManuscriptCitationTodo,
    ManuscriptIncludeInstance,
    ManuscriptSourceFileSnapshot,
    ManuscriptSourceLocator,
    ResearchMonographCitationSnapshotResult,
)

type CitationJsonValue = (
    None | int | str | list[CitationJsonValue] | dict[str, CitationJsonValue]
)

_MAX_CANONICAL_RESULT_JSON_BYTES = 20_000_000
_MAX_JSON_NESTING_DEPTH = 64
_MAX_JSON_INTEGER_DIGITS = 20


@dataclass(frozen=True, slots=True)
class _CanonicalCitationJsonParser:
    """Parse bounded JSON into the codec's closed representation union."""

    def execute(self, payload: bytes) -> CitationJsonValue:
        """Return one complete JSON value with duplicate names rejected."""
        if type(payload) is not bytes:
            raise TypeError("payload must be built-in bytes")
        if not payload or len(payload) > _MAX_CANONICAL_RESULT_JSON_BYTES:
            raise ValueError("payload size is outside 1 through 20,000,000 bytes")
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError("payload must be UTF-8") from error
        if not text.endswith("\n"):
            raise ValueError("payload must end with one canonical newline")
        value, index = self._parse_value(text, 0, 0)
        if index != len(text) - 1:
            raise ValueError("payload contains trailing JSON content or whitespace")
        return value

    def _parse_value(
        self, text: str, index: int, depth: int
    ) -> tuple[CitationJsonValue, int]:
        """Parse one value beginning after insignificant JSON whitespace."""
        if depth > _MAX_JSON_NESTING_DEPTH:
            raise ValueError("JSON nesting exceeds 64 levels")
        index = self._skip_whitespace(text, index)
        if index >= len(text) - 1:
            raise ValueError("payload contains an incomplete JSON value")
        character = text[index]
        if character == "{":
            return self._parse_object(text, index, depth)
        if character == "[":
            return self._parse_array(text, index, depth)
        if character == '"':
            return self._parse_string(text, index)
        if text.startswith("null", index):
            return None, index + 4
        if character == "-" or character.isdigit():
            return self._parse_integer(text, index)
        raise ValueError("payload contains an unsupported JSON value")

    def _parse_object(
        self, text: str, index: int, depth: int
    ) -> tuple[dict[str, CitationJsonValue], int]:
        """Parse an object while rejecting duplicate member names."""
        values: dict[str, CitationJsonValue] = {}
        index = self._skip_whitespace(text, index + 1)
        if index < len(text) and text[index] == "}":
            return values, index + 1
        while True:
            if index >= len(text) or text[index] != '"':
                raise ValueError("JSON object member name must be a string")
            key, index = self._parse_string(text, index)
            if key in values:
                raise ValueError(f"JSON object contains duplicate member {key!r}")
            index = self._skip_whitespace(text, index)
            if index >= len(text) or text[index] != ":":
                raise ValueError("JSON object member requires a colon")
            value, index = self._parse_value(text, index + 1, depth + 1)
            values[key] = value
            index = self._skip_whitespace(text, index)
            if index >= len(text):
                raise ValueError("JSON object is incomplete")
            if text[index] == "}":
                return values, index + 1
            if text[index] != ",":
                raise ValueError("JSON object members require commas")
            index = self._skip_whitespace(text, index + 1)

    def _parse_array(
        self, text: str, index: int, depth: int
    ) -> tuple[list[CitationJsonValue], int]:
        """Parse one ordered JSON array."""
        values: list[CitationJsonValue] = []
        index = self._skip_whitespace(text, index + 1)
        if index < len(text) and text[index] == "]":
            return values, index + 1
        while True:
            value, index = self._parse_value(text, index, depth + 1)
            values.append(value)
            index = self._skip_whitespace(text, index)
            if index >= len(text):
                raise ValueError("JSON array is incomplete")
            if text[index] == "]":
                return values, index + 1
            if text[index] != ",":
                raise ValueError("JSON array items require commas")
            index = self._skip_whitespace(text, index + 1)

    def _parse_string(self, text: str, index: int) -> tuple[str, int]:
        """Parse one JSON string including Unicode escape pairs."""
        characters: list[str] = []
        index += 1
        while index < len(text):
            character = text[index]
            if character == '"':
                return "".join(characters), index + 1
            if ord(character) < 0x20:
                raise ValueError("JSON string contains an unescaped control character")
            if character != "\\":
                characters.append(character)
                index += 1
                continue
            if index + 1 >= len(text):
                raise ValueError("JSON string escape is incomplete")
            escape = text[index + 1]
            simple = {
                '"': '"',
                "\\": "\\",
                "/": "/",
                "b": "\b",
                "f": "\f",
                "n": "\n",
                "r": "\r",
                "t": "\t",
            }
            replacement = simple.get(escape)
            if replacement is not None:
                characters.append(replacement)
                index += 2
                continue
            if escape != "u":
                raise ValueError("JSON string contains an unsupported escape")
            codepoint, index = self._parse_unicode_escape(text, index)
            if 0xD800 <= codepoint <= 0xDBFF:
                if not text.startswith("\\u", index):
                    raise ValueError("JSON high surrogate lacks a low surrogate")
                low, index = self._parse_unicode_escape(text, index)
                if not 0xDC00 <= low <= 0xDFFF:
                    raise ValueError("JSON high surrogate has an invalid low surrogate")
                codepoint = 0x10000 + ((codepoint - 0xD800) << 10) + (low - 0xDC00)
            elif 0xDC00 <= codepoint <= 0xDFFF:
                raise ValueError("JSON low surrogate lacks a high surrogate")
            characters.append(chr(codepoint))
        raise ValueError("JSON string is unterminated")

    @staticmethod
    def _parse_unicode_escape(text: str, index: int) -> tuple[int, int]:
        """Parse ``\\u`` followed by exactly four hexadecimal digits."""
        end = index + 6
        if end > len(text) or not text.startswith("\\u", index):
            raise ValueError("JSON Unicode escape is incomplete")
        digits = text[index + 2 : end]
        if len(digits) != 4 or any(
            character not in "0123456789abcdefABCDEF" for character in digits
        ):
            raise ValueError("JSON Unicode escape is malformed")
        return int(digits, 16), end

    @staticmethod
    def _parse_integer(text: str, index: int) -> tuple[int, int]:
        """Parse the integer-only numeric subset used by the wire."""
        start = index
        if text[index] == "-":
            index += 1
            if index >= len(text) or not text[index].isdigit():
                raise ValueError("JSON integer is malformed")
        if text[index] == "0":
            index += 1
            if index < len(text) and text[index].isdigit():
                raise ValueError("JSON integer has a leading zero")
        else:
            if not "1" <= text[index] <= "9":
                raise ValueError("JSON integer is malformed")
            while index < len(text) and text[index].isdigit():
                index += 1
        if index < len(text) and text[index] in ".eE":
            raise ValueError("citation snapshot JSON does not accept real numbers")
        digit_count = index - start - int(text[start] == "-")
        if digit_count > _MAX_JSON_INTEGER_DIGITS:
            raise ValueError("JSON integer exceeds 20 decimal digits")
        return int(text[start:index]), index

    @staticmethod
    def _skip_whitespace(text: str, index: int) -> int:
        """Return the first index after JSON whitespace."""
        while index < len(text) and text[index] in " \t\r\n":
            index += 1
        return index


@dataclass(frozen=True, slots=True)
class ResearchMonographCitationSnapshotResultJsonCodec(
    JsonCodec[ResearchMonographCitationSnapshotResult, bytes]
):
    """Encode and decode one complete citation snapshot Result as canonical JSON.

    The wire is unversioned and contains exactly ``request_id``, ``result_id``, and
    the complete stored snapshot.  Array order is owner order; object names are
    lexically sorted in the canonical bytes.  The wire contains no repository root,
    source excerpts, timestamps, runtime status, downstream authority, or fabricated
    References identities.
    """

    def serialize(self, result: ResearchMonographCitationSnapshotResult) -> bytes:
        """Return deterministic newline-terminated UTF-8 JSON for ``result``.

        Parameters
        ----------
        result
            Exact replay-valid owner Result.

        Returns
        -------
        bytes
            Complete canonical JSON, bounded to 20,000,000 bytes.

        Raises
        ------
        TypeError
            ``result`` is not the exact supported Result type.
        ValueError
            Integrity replay fails or the encoded bytes exceed the wire bound.
        """
        if type(result) is not ResearchMonographCitationSnapshotResult:
            raise TypeError("result must be ResearchMonographCitationSnapshotResult")
        expected = ResearchMonographCitationSnapshotIntegrityValidator().execute(
            result.snapshot, result.request_id
        )
        if result.result_id != expected:
            raise ValueError("result_id does not replay from the complete snapshot")
        payload = self._result_value(result)
        encoded = (
            json.dumps(
                payload,
                allow_nan=False,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n"
        ).encode("utf-8")
        if len(encoded) > _MAX_CANONICAL_RESULT_JSON_BYTES:
            raise ValueError("canonical result JSON exceeds 20,000,000 bytes")
        return encoded

    def deserialize(self, payload: bytes) -> ResearchMonographCitationSnapshotResult:
        """Reconstruct and replay one exact canonical Result JSON payload.

        Parameters
        ----------
        payload
            Canonical newline-terminated UTF-8 JSON bytes.

        Returns
        -------
        ResearchMonographCitationSnapshotResult
            Exact immutable Result represented by ``payload``.

        Raises
        ------
        TypeError
            ``payload`` is not built-in ``bytes`` or a represented field has the
            wrong semantic type.
        ValueError
            JSON is malformed, duplicated, incomplete, unknown, noncanonical,
            overbound, or fails owner integrity replay.
        """
        root = self._object(_CanonicalCitationJsonParser().execute(payload), "payload")
        self._fields(root, {"request_id", "result_id", "snapshot"}, "payload")
        snapshot = self._snapshot(self._object(root["snapshot"], "snapshot"))
        result = ResearchMonographCitationSnapshotResult(
            self._text(root["request_id"], "request_id"),
            self._text(root["result_id"], "result_id"),
            snapshot,
        )
        if self.serialize(result) != payload:
            raise ValueError("payload is valid JSON but not the canonical result wire")
        return result

    def _result_value(
        self, result: ResearchMonographCitationSnapshotResult
    ) -> dict[str, CitationJsonValue]:
        """Return the closed JSON representation of one Result."""
        return {
            "request_id": result.request_id,
            "result_id": result.result_id,
            "snapshot": self._snapshot_value(result.snapshot),
        }

    def _snapshot_value(
        self, snapshot: ManuscriptCitationSnapshot
    ) -> dict[str, CitationJsonValue]:
        """Return every stored snapshot field in the canonical representation."""
        return {
            "bibliography_content_identity": self._content_identity_value(
                snapshot.bibliography_content_identity
            ),
            "bibliography_entries": [
                self._entry_value(value) for value in snapshot.bibliography_entries
            ],
            "bibliography_path": snapshot.bibliography_path,
            "calls": [self._call_value(value) for value in snapshot.calls],
            "contract_id": snapshot.contract_id,
            "duplicate_keys": list(snapshot.duplicate_keys),
            "entrypoint_path": snapshot.entrypoint_path,
            "generator_identity": snapshot.generator_identity,
            "groups": [self._group_value(value) for value in snapshot.groups],
            "include_instances": [
                self._include_value(value) for value in snapshot.include_instances
            ],
            "missing_keys": list(snapshot.missing_keys),
            "occurrences": [
                self._occurrence_value(value) for value in snapshot.occurrences
            ],
            "parser_identity": snapshot.parser_identity,
            "repository_revision": snapshot.repository_revision,
            "snapshot_id": snapshot.snapshot_id,
            "source_files": [
                self._source_file_value(value) for value in snapshot.source_files
            ],
            "source_gaps": [
                self._source_gap_value(value) for value in snapshot.source_gaps
            ],
            "todos": [self._todo_value(value) for value in snapshot.todos],
            "uncited_keys": list(snapshot.uncited_keys),
        }

    @staticmethod
    def _content_identity_value(
        value: CitationContentIdentity,
    ) -> dict[str, CitationJsonValue]:
        return {
            "algorithm": value.algorithm.value,
            "byte_count": value.byte_count,
            "digest": value.digest,
        }

    def _locator_value(
        self, value: ManuscriptSourceLocator
    ) -> dict[str, CitationJsonValue]:
        return {
            "byte_end": value.byte_end,
            "byte_start": value.byte_start,
            "column": value.column,
            "include_index": value.include_index,
            "line": value.line,
            "source_content_identity": self._content_identity_value(
                value.source_content_identity
            ),
            "source_path": value.source_path,
        }

    @staticmethod
    def _source_file_value(
        value: ManuscriptSourceFileSnapshot,
    ) -> dict[str, CitationJsonValue]:
        return {
            "byte_size": value.byte_size,
            "file_id": value.file_id,
            "graph_order": value.graph_order,
            "sha256": value.sha256,
            "source_path": value.source_path,
        }

    @staticmethod
    def _include_value(
        value: ManuscriptIncludeInstance,
    ) -> dict[str, CitationJsonValue]:
        return {
            "child_file_id": value.child_file_id,
            "depth": value.depth,
            "include_index": value.include_index,
            "include_instance_id": value.include_instance_id,
            "ordinal": value.ordinal,
            "parent_file_id": value.parent_file_id,
            "parent_include_instance_id": value.parent_include_instance_id,
            "source_byte_end": value.source_byte_end,
            "source_byte_start": value.source_byte_start,
            "source_path": value.source_path,
        }

    def _entry_value(
        self, value: ManuscriptBibliographyEntrySnapshot
    ) -> dict[str, CitationJsonValue]:
        return {
            "bibliography_entry_id": value.bibliography_entry_id,
            "entry_content_identity": self._content_identity_value(
                value.entry_content_identity
            ),
            "entry_index": value.entry_index,
            "entry_type": value.entry_type,
            "key": value.key,
            "locator": self._locator_value(value.locator),
            "source_bibliography_observation_id": (
                value.source_bibliography_observation_id
            ),
        }

    def _call_value(
        self, value: ManuscriptCitationCall
    ) -> dict[str, CitationJsonValue]:
        return {
            "call_id": value.call_id,
            "call_index": value.call_index,
            "command_kind": value.command_kind.value,
            "file_id": value.file_id,
            "include_instance_id": value.include_instance_id,
            "locator": self._locator_value(value.locator),
            "occurrence_indexes": list(value.occurrence_indexes),
            "origin": value.origin.value,
            "todo_marker_index": value.todo_marker_index,
        }

    def _occurrence_value(
        self, value: ManuscriptCitationOccurrence
    ) -> dict[str, CitationJsonValue]:
        return {
            "bibliography_entry_index": value.bibliography_entry_index,
            "call_index": value.call_index,
            "key": value.key,
            "key_index": value.key_index,
            "locator": self._locator_value(value.locator),
            "occurrence_id": value.occurrence_id,
            "occurrence_index": value.occurrence_index,
            "origin": value.origin.value,
            "todo_marker_index": value.todo_marker_index,
        }

    @staticmethod
    def _group_value(
        value: ManuscriptCitationGroup,
    ) -> dict[str, CitationJsonValue]:
        return {
            "bibliography_entry_index": value.bibliography_entry_index,
            "direct_occurrence_count": value.direct_occurrence_count,
            "generated_occurrence_count": value.generated_occurrence_count,
            "group_id": value.group_id,
            "group_index": value.group_index,
            "key": value.key,
            "occurrence_indexes": list(value.occurrence_indexes),
        }

    def _todo_value(
        self, value: ManuscriptCitationTodo
    ) -> dict[str, CitationJsonValue]:
        return {
            "generated_call_ids": list(value.generated_call_ids),
            "generated_occurrence_ids": list(value.generated_occurrence_ids),
            "locator": self._locator_value(value.locator),
            "priority": value.priority.value,
            "priority_locator": self._locator_value(value.priority_locator),
            "todo_id": value.todo_id,
            "todo_marker_index": value.todo_marker_index,
        }

    def _source_gap_value(
        self, value: ManuscriptCitationSourceGap
    ) -> dict[str, CitationJsonValue]:
        return {
            "locator": self._locator_value(value.locator),
            "placeholder_identifier": value.placeholder_identifier,
            "reason": value.reason.value,
            "source_gap_id": value.source_gap_id,
            "source_gap_index": value.source_gap_index,
        }

    def _snapshot(
        self, value: dict[str, CitationJsonValue]
    ) -> ManuscriptCitationSnapshot:
        """Construct the complete immutable snapshot from exact wire fields."""
        expected = {
            "bibliography_content_identity",
            "bibliography_entries",
            "bibliography_path",
            "calls",
            "contract_id",
            "duplicate_keys",
            "entrypoint_path",
            "generator_identity",
            "groups",
            "include_instances",
            "missing_keys",
            "occurrences",
            "parser_identity",
            "repository_revision",
            "snapshot_id",
            "source_files",
            "source_gaps",
            "todos",
            "uncited_keys",
        }
        self._fields(value, expected, "snapshot")
        return ManuscriptCitationSnapshot(
            self._text(value["contract_id"], "contract_id"),
            self._text(value["snapshot_id"], "snapshot_id"),
            self._text(value["repository_revision"], "repository_revision"),
            self._text(value["entrypoint_path"], "entrypoint_path"),
            self._text(value["bibliography_path"], "bibliography_path"),
            self._text(value["parser_identity"], "parser_identity"),
            self._text(value["generator_identity"], "generator_identity"),
            self._content_identity(
                self._object(
                    value["bibliography_content_identity"],
                    "bibliography_content_identity",
                )
            ),
            tuple(
                self._source_file(self._object(item, "source_file"))
                for item in self._array(value["source_files"], "source_files")
            ),
            tuple(
                self._include(self._object(item, "include_instance"))
                for item in self._array(value["include_instances"], "include_instances")
            ),
            tuple(
                self._entry(self._object(item, "bibliography_entry"))
                for item in self._array(
                    value["bibliography_entries"], "bibliography_entries"
                )
            ),
            tuple(
                self._call(self._object(item, "call"))
                for item in self._array(value["calls"], "calls")
            ),
            tuple(
                self._occurrence(self._object(item, "occurrence"))
                for item in self._array(value["occurrences"], "occurrences")
            ),
            tuple(
                self._group(self._object(item, "group"))
                for item in self._array(value["groups"], "groups")
            ),
            tuple(
                self._todo(self._object(item, "todo"))
                for item in self._array(value["todos"], "todos")
            ),
            tuple(
                self._source_gap(self._object(item, "source_gap"))
                for item in self._array(value["source_gaps"], "source_gaps")
            ),
            self._text_tuple(value["missing_keys"], "missing_keys"),
            self._text_tuple(value["duplicate_keys"], "duplicate_keys"),
            self._text_tuple(value["uncited_keys"], "uncited_keys"),
        )

    def _content_identity(
        self, value: dict[str, CitationJsonValue]
    ) -> CitationContentIdentity:
        self._fields(value, {"algorithm", "byte_count", "digest"}, "content_identity")
        return CitationContentIdentity(
            CitationContentAlgorithm(
                self._text(value["algorithm"], "content algorithm")
            ),
            self._text(value["digest"], "content digest"),
            self._integer(value["byte_count"], "content byte_count"),
        )

    def _locator(self, value: dict[str, CitationJsonValue]) -> ManuscriptSourceLocator:
        self._fields(
            value,
            {
                "byte_end",
                "byte_start",
                "column",
                "include_index",
                "line",
                "source_content_identity",
                "source_path",
            },
            "locator",
        )
        return ManuscriptSourceLocator(
            self._text(value["source_path"], "locator source_path"),
            self._content_identity(
                self._object(
                    value["source_content_identity"], "source_content_identity"
                )
            ),
            self._integer(value["include_index"], "locator include_index"),
            self._integer(value["byte_start"], "locator byte_start"),
            self._integer(value["byte_end"], "locator byte_end"),
            self._integer(value["line"], "locator line"),
            self._integer(value["column"], "locator column"),
        )

    def _source_file(
        self, value: dict[str, CitationJsonValue]
    ) -> ManuscriptSourceFileSnapshot:
        self._fields(
            value,
            {"byte_size", "file_id", "graph_order", "sha256", "source_path"},
            "source_file",
        )
        return ManuscriptSourceFileSnapshot(
            self._text(value["file_id"], "file_id"),
            self._text(value["source_path"], "source_path"),
            self._integer(value["byte_size"], "byte_size"),
            self._text(value["sha256"], "sha256"),
            self._integer(value["graph_order"], "graph_order"),
        )

    def _include(
        self, value: dict[str, CitationJsonValue]
    ) -> ManuscriptIncludeInstance:
        self._fields(
            value,
            {
                "child_file_id",
                "depth",
                "include_index",
                "include_instance_id",
                "ordinal",
                "parent_file_id",
                "parent_include_instance_id",
                "source_byte_end",
                "source_byte_start",
                "source_path",
            },
            "include_instance",
        )
        return ManuscriptIncludeInstance(
            self._text(value["include_instance_id"], "include_instance_id"),
            self._integer(value["include_index"], "include_index"),
            self._optional_text(value["parent_file_id"], "parent_file_id"),
            self._optional_text(
                value["parent_include_instance_id"],
                "parent_include_instance_id",
            ),
            self._text(value["child_file_id"], "child_file_id"),
            self._text(value["source_path"], "include source_path"),
            self._integer(value["source_byte_start"], "source_byte_start"),
            self._integer(value["source_byte_end"], "source_byte_end"),
            self._integer(value["ordinal"], "include ordinal"),
            self._integer(value["depth"], "include depth"),
        )

    def _entry(
        self, value: dict[str, CitationJsonValue]
    ) -> ManuscriptBibliographyEntrySnapshot:
        self._fields(
            value,
            {
                "bibliography_entry_id",
                "entry_content_identity",
                "entry_index",
                "entry_type",
                "key",
                "locator",
                "source_bibliography_observation_id",
            },
            "bibliography_entry",
        )
        return ManuscriptBibliographyEntrySnapshot(
            self._text(value["bibliography_entry_id"], "bibliography_entry_id"),
            self._integer(value["entry_index"], "entry_index"),
            self._text(value["key"], "entry key"),
            self._text(value["entry_type"], "entry_type"),
            self._locator(self._object(value["locator"], "entry locator")),
            self._content_identity(
                self._object(value["entry_content_identity"], "entry_content_identity")
            ),
            self._optional_text(
                value["source_bibliography_observation_id"],
                "source_bibliography_observation_id",
            ),
        )

    def _call(self, value: dict[str, CitationJsonValue]) -> ManuscriptCitationCall:
        self._fields(
            value,
            {
                "call_id",
                "call_index",
                "command_kind",
                "file_id",
                "include_instance_id",
                "locator",
                "occurrence_indexes",
                "origin",
                "todo_marker_index",
            },
            "call",
        )
        return ManuscriptCitationCall(
            self._text(value["call_id"], "call_id"),
            self._integer(value["call_index"], "call_index"),
            self._text(value["include_instance_id"], "include_instance_id"),
            self._text(value["file_id"], "file_id"),
            ManuscriptCitationCommandKind(
                self._text(value["command_kind"], "command_kind")
            ),
            ManuscriptCitationOrigin(self._text(value["origin"], "call origin")),
            self._locator(self._object(value["locator"], "call locator")),
            self._integer_tuple(value["occurrence_indexes"], "occurrence_indexes"),
            self._optional_integer(value["todo_marker_index"], "todo_marker_index"),
        )

    def _occurrence(
        self, value: dict[str, CitationJsonValue]
    ) -> ManuscriptCitationOccurrence:
        self._fields(
            value,
            {
                "bibliography_entry_index",
                "call_index",
                "key",
                "key_index",
                "locator",
                "occurrence_id",
                "occurrence_index",
                "origin",
                "todo_marker_index",
            },
            "occurrence",
        )
        return ManuscriptCitationOccurrence(
            self._text(value["occurrence_id"], "occurrence_id"),
            self._integer(value["occurrence_index"], "occurrence_index"),
            self._integer(value["call_index"], "occurrence call_index"),
            self._integer(value["key_index"], "key_index"),
            self._text(value["key"], "occurrence key"),
            ManuscriptCitationOrigin(self._text(value["origin"], "occurrence origin")),
            self._locator(self._object(value["locator"], "occurrence locator")),
            self._optional_integer(
                value["bibliography_entry_index"], "bibliography_entry_index"
            ),
            self._optional_integer(value["todo_marker_index"], "todo_marker_index"),
        )

    def _group(self, value: dict[str, CitationJsonValue]) -> ManuscriptCitationGroup:
        self._fields(
            value,
            {
                "bibliography_entry_index",
                "direct_occurrence_count",
                "generated_occurrence_count",
                "group_id",
                "group_index",
                "key",
                "occurrence_indexes",
            },
            "group",
        )
        return ManuscriptCitationGroup(
            self._text(value["group_id"], "group_id"),
            self._integer(value["group_index"], "group_index"),
            self._text(value["key"], "group key"),
            self._integer_tuple(value["occurrence_indexes"], "occurrence_indexes"),
            self._integer(value["direct_occurrence_count"], "direct_occurrence_count"),
            self._integer(
                value["generated_occurrence_count"], "generated_occurrence_count"
            ),
            self._optional_integer(
                value["bibliography_entry_index"], "bibliography_entry_index"
            ),
        )

    def _todo(self, value: dict[str, CitationJsonValue]) -> ManuscriptCitationTodo:
        self._fields(
            value,
            {
                "generated_call_ids",
                "generated_occurrence_ids",
                "locator",
                "priority",
                "priority_locator",
                "todo_id",
                "todo_marker_index",
            },
            "todo",
        )
        return ManuscriptCitationTodo(
            self._text(value["todo_id"], "todo_id"),
            self._integer(value["todo_marker_index"], "todo_marker_index"),
            self._locator(self._object(value["locator"], "todo locator")),
            self._locator(self._object(value["priority_locator"], "priority_locator")),
            ManuscriptCitationPriority(self._text(value["priority"], "todo priority")),
            self._text_tuple(value["generated_call_ids"], "generated_call_ids"),
            self._text_tuple(
                value["generated_occurrence_ids"], "generated_occurrence_ids"
            ),
        )

    def _source_gap(
        self, value: dict[str, CitationJsonValue]
    ) -> ManuscriptCitationSourceGap:
        self._fields(
            value,
            {
                "locator",
                "placeholder_identifier",
                "reason",
                "source_gap_id",
                "source_gap_index",
            },
            "source_gap",
        )
        return ManuscriptCitationSourceGap(
            self._text(value["source_gap_id"], "source_gap_id"),
            self._integer(value["source_gap_index"], "source_gap_index"),
            self._locator(self._object(value["locator"], "source_gap locator")),
            ManuscriptCitationSourceGapReason(
                self._text(value["reason"], "source_gap reason")
            ),
            self._text(value["placeholder_identifier"], "placeholder_identifier"),
        )

    @staticmethod
    def _fields(
        value: dict[str, CitationJsonValue], expected: set[str], label: str
    ) -> None:
        actual = set(value)
        if actual != expected:
            missing = sorted(expected - actual)
            unknown = sorted(actual - expected)
            raise ValueError(
                f"{label} fields differ; missing={missing!r}, unknown={unknown!r}"
            )

    @staticmethod
    def _object(value: CitationJsonValue, label: str) -> dict[str, CitationJsonValue]:
        if type(value) is not dict:
            raise TypeError(f"{label} must be a JSON object")
        return value

    @staticmethod
    def _array(value: CitationJsonValue, label: str) -> list[CitationJsonValue]:
        if type(value) is not list:
            raise TypeError(f"{label} must be a JSON array")
        return value

    @staticmethod
    def _text(value: CitationJsonValue, label: str) -> str:
        if type(value) is not str:
            raise TypeError(f"{label} must be a JSON string")
        return value

    @staticmethod
    def _optional_text(value: CitationJsonValue, label: str) -> str | None:
        if value is None:
            return None
        if type(value) is not str:
            raise TypeError(f"{label} must be null or a JSON string")
        return value

    @staticmethod
    def _integer(value: CitationJsonValue, label: str) -> int:
        if type(value) is not int:
            raise TypeError(f"{label} must be a JSON integer")
        return value

    @staticmethod
    def _optional_integer(value: CitationJsonValue, label: str) -> int | None:
        if value is None:
            return None
        if type(value) is not int:
            raise TypeError(f"{label} must be null or a JSON integer")
        return value

    def _text_tuple(self, value: CitationJsonValue, label: str) -> tuple[str, ...]:
        return tuple(
            self._text(item, f"{label} item") for item in self._array(value, label)
        )

    def _integer_tuple(self, value: CitationJsonValue, label: str) -> tuple[int, ...]:
        return tuple(
            self._integer(item, f"{label} item") for item in self._array(value, label)
        )
