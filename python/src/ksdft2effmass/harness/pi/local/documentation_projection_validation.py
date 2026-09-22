"""Private explicit-input documentation projection mechanics."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator  # type: ignore[import-untyped]


class DuplicateKeyError(ValueError):
    """Raised when one caller-supplied JSON object repeats a key."""


def _pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    """Load one exact JSON object with duplicate-key rejection."""
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_pairs)
    if type(value) is not dict:
        raise TypeError("top-level JSON value must be an object")
    return value


def schema_diagnostics(
    instance: dict[str, Any], schema: dict[str, Any]
) -> tuple[str, ...]:
    """Return deterministic Draft-2020-12 validation diagnostics."""
    Draft202012Validator.check_schema(schema)
    errors = Draft202012Validator(schema).iter_errors(instance)
    return tuple(
        "SCHEMA:"
        f"{'/'.join(str(part) for part in error.absolute_path) or '$'}:"
        f"{error.validator}"
        for error in sorted(
            errors,
            key=lambda item: (
                tuple(str(x) for x in item.absolute_path),
                item.validator or "",
            ),
        )
    )


def _markdown(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("`", "\\`")


def _select(context: dict[str, Any], selector: str) -> object:
    owner, field = selector.split(".", 1)
    return context[owner][field]


def render(context: dict[str, Any], profile: dict[str, Any]) -> bytes:
    """Render caller-normalized context in profile-declared order."""
    title = _select(context, profile["output_title_selector"])
    lines = [f"# {_markdown(title)}", "", f"> **{profile['generated_notice']}**"]
    for section in profile["sections"]:
        lines.extend(("", f"## {section['heading']}"))
        for item in section["items"]:
            value = _select(context, item["selector"])
            label = item["label"]
            form = item["format"]
            if form == "list":
                if not isinstance(value, list):
                    raise TypeError("list projection value must be a list")
                lines.extend(("", f"**{label}:**"))
                lines.extend(f"- {_markdown(entry)}" for entry in value)
                if not value:
                    lines.append("- None.")
            elif form == "link":
                lines.extend(
                    ("", f"**{label}:** [{_markdown(value)}]({_markdown(value)})")
                )
            elif form == "boolean":
                lines.extend(("", f"**{label}:** {'true' if value else 'false'}"))
            else:
                lines.extend(("", f"**{label}:** {_markdown(value)}"))
    text = "\n".join(lines)
    if profile["final_lf"]:
        text += "\n"
    return text.encode("utf-8")


@dataclass(frozen=True, slots=True)
class _DocumentationProjectionValidationResult:
    """Immutable diagnostics from one explicit projection validation."""

    diagnostics: tuple[str, ...]

    @property
    def status(self) -> str:
        return "PASS" if not self.diagnostics else "FAIL"


class _DocumentationProjectionValidator:
    """Validate schema inputs and optional exact documentation projection bytes."""

    __slots__ = ()

    def execute(
        self,
        schema_path: Path,
        instance_path: Path,
        projection_paths: tuple[
            Path | None, Path | None, Path | None, Path | None, Path | None
        ],
    ) -> _DocumentationProjectionValidationResult:
        diagnostics: list[str] = []
        try:
            diagnostics.extend(
                schema_diagnostics(load_json(instance_path), load_json(schema_path))
            )
            if any(projection_paths):
                if not all(projection_paths):
                    raise ValueError("all projection inputs must be supplied together")
                profile_schema, profile_path, context_path, expected, generated = (
                    projection_paths
                )
                assert profile_schema is not None and profile_path is not None
                assert (
                    context_path is not None
                    and expected is not None
                    and generated is not None
                )
                profile = load_json(profile_path)
                diagnostics.extend(
                    schema_diagnostics(profile, load_json(profile_schema))
                )
                rendered = render(load_json(context_path), profile)
                if rendered != expected.read_bytes():
                    diagnostics.append("DRIFT:expected")
                if rendered != generated.read_bytes():
                    diagnostics.append("DRIFT:generated")
        except (
            OSError,
            UnicodeError,
            json.JSONDecodeError,
            DuplicateKeyError,
            TypeError,
            ValueError,
        ) as exc:
            diagnostics.append(f"INPUT:{type(exc).__name__}:{exc}")
        return _DocumentationProjectionValidationResult(tuple(sorted(diagnostics)))
