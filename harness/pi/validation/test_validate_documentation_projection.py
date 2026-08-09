"""Software verification for generic documentation-projection resource mechanics."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).with_name("validate_documentation_projection.py")
SPEC = importlib.util.spec_from_file_location("documentation_projection", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_render_uses_profile_order_links_and_final_lf() -> None:
    context = {
        "item": {
            "title": "Neutral reference",
            "name": "neutral",
            "values": ["first", "second"],
            "reference": "notes/input.md",
        }
    }
    profile = {
        "schema_version": 1,
        "output_title_selector": "item.title",
        "generated_notice": "Generated from explicit inputs.",
        "sections": [
            {
                "section_id": "values",
                "heading": "Values",
                "items": [
                    {"label": "Name", "selector": "item.name", "format": "scalar"},
                    {"label": "Values", "selector": "item.values", "format": "list"},
                    {
                        "label": "Reference",
                        "selector": "item.reference",
                        "format": "link",
                    },
                ],
            }
        ],
        "final_lf": True,
    }
    profile_schema = MODULE.load_json(
        MODULE_PATH.parent.parent
        / "schemas"
        / "documentation-projection-profile.schema.json"
    )
    assert MODULE.schema_diagnostics(profile, profile_schema) == ()
    rendered = MODULE.render(context, profile)
    assert rendered.startswith(b"# Neutral reference\n")
    changed_context = {"item": {**context["item"], "title": "Changed title"}}
    assert MODULE.render(changed_context, profile).startswith(b"# Changed title\n")
    assert rendered.endswith(b"\n")
    assert rendered.index(b"first") < rendered.index(b"second")
    assert b"[notes/input.md](notes/input.md)" in rendered


def test_schema_diagnostics_and_drift_are_exact(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": ["name"],
    }
    assert MODULE.schema_diagnostics({}, schema) == ("SCHEMA:$:required",)

    paths = {
        name: tmp_path / name
        for name in (
            "schema.json",
            "instance.json",
            "profile-schema.json",
            "profile.json",
            "context.json",
            "expected.md",
            "generated.md",
        )
    }
    paths["schema.json"].write_text(json.dumps(schema))
    paths["instance.json"].write_text('{"name":"value"}')
    paths["profile-schema.json"].write_text('{"type":"object"}')
    profile = {
        "output_title_selector": "item.title",
        "generated_notice": "Generated.",
        "sections": [
            {
                "heading": "Values",
                "items": [
                    {"label": "Name", "selector": "item.name", "format": "scalar"}
                ],
            }
        ],
        "final_lf": True,
    }
    paths["profile.json"].write_text(json.dumps(profile))
    paths["context.json"].write_text('{"item":{"name":"value","title":"Reference"}}')
    rendered = MODULE.render({"item": {"name": "value", "title": "Reference"}}, profile)
    paths["expected.md"].write_bytes(rendered)
    paths["generated.md"].write_bytes(rendered + b"drift\n")

    arguments = []
    for name in (
        "schema",
        "instance",
        "profile-schema",
        "profile",
        "context",
        "expected",
        "generated",
    ):
        arguments.extend(
            (
                f"--{name}",
                str(
                    paths[f"{name}.json"]
                    if name not in {"expected", "generated"}
                    else paths[f"{name}.md"]
                ),
            )
        )
    assert MODULE.main(arguments) == 1
    result = json.loads(capsys.readouterr().out)
    assert result["diagnostics"] == ["DRIFT:generated"]


def test_duplicate_json_keys_fail_closed(tmp_path: Path) -> None:
    path = tmp_path / "duplicate.json"
    path.write_text('{"name":1,"name":2}\n', encoding="utf-8")
    with pytest.raises(MODULE.DuplicateKeyError):
        MODULE.load_json(path)
