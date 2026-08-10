"""Independent evidence ownership rule owner."""

from __future__ import annotations

import json
import re
from typing import Any

from .model import PythonTestModuleModel

_OPENINGS = {
    "software_verification": "Software verification",
    "numerical_verification": "Numerical verification",
    "scientific_validation": "Scientific validation",
    "uncertainty_quantification": "Uncertainty quantification",
}


def _validate_owner_profile(
    mode: object, subject: object, evidence_profile: object
) -> tuple[str, str] | None:
    """Reject private class ownership and malformed profile identity."""
    if mode == "class_owned" and isinstance(subject, str) and subject.startswith("_"):
        return (
            "TE.PRIVATE_CLASS_OWNER",
            "class_owned is limited to one public class as the sole system under test",
        )
    if evidence_profile is not None and evidence_profile not in {
        "routine",
        "claim_bearing",
    }:
        return ("TE.EVIDENCE_PROFILE", "evidence_profile is invalid")
    return None


def _validate_ownership(
    model: PythonTestModuleModel, owner: dict[str, Any]
) -> tuple[tuple[str, str, int | None], ...]:
    """Validate source ownership declaration agreement completely."""
    findings: list[tuple[str, str, int | None]] = []
    mode, sut, artifact = owner.get("mode"), owner.get("sut"), owner.get("artifact")
    evidence_class = owner.get("evidence_class")
    opening = _OPENINGS.get(evidence_class) if isinstance(evidence_class, str) else None
    expected = (
        f"{opening} of ``{sut}``."
        if opening and mode == "class_owned" and isinstance(sut, str) and sut
        else f"{opening} of {artifact}."
        if opening
        and mode == "artifact_owned"
        and isinstance(artifact, str)
        and artifact.strip()
        else None
    )
    first = (model.module_doc or "").splitlines()[0].strip() if model.module_doc else ""
    if not model.source.startswith('r"""') or expected is None or first != expected:
        findings.append(
            (
                "TE.MODULE_OPENING",
                f"raw module opening must exactly match structured ownership; expected {expected!r}",  # noqa: E501
                None,
            )
        )
    if opening is None:
        findings.append(
            (
                "TE.EVIDENCE_CLASS",
                "evidence_class must be software_verification, numerical_verification, scientific_validation, or uncertainty_quantification",  # noqa: E501
                None,
            )
        )
    if mode not in {"class_owned", "artifact_owned"}:
        findings.append(
            ("TE.OWNERSHIP", "mode must be class_owned or artifact_owned", None)
        )
    elif mode == "class_owned":
        filename = model.path.rsplit("/", 1)[-1]
        if (
            not isinstance(sut, str)
            or not sut
            or not re.fullmatch(
                rf"test__{re.escape(sut)}(?:__[a-z][a-z0-9_]*)?\.py", filename
            )
        ):
            findings.append(
                (
                    "TE.SUT_FILENAME",
                    "class-owned filename must agree with the supplied SUT",
                    None,
                )
            )
        if model.sut_assignment_name != sut:
            findings.append(
                (
                    "TE.SUT_ASSIGNMENT",
                    "SUT assignment must name the supplied public class",
                    None,
                )
            )
        if sut not in model.imported_names:
            findings.append(
                (
                    "TE.SUT_IMPORT",
                    "supplied SUT must be imported through an explicit public import",
                    None,
                )
            )
    else:
        if not isinstance(artifact, str) or not artifact.strip():
            findings.append(
                (
                    "TE.ARTIFACT_OWNER",
                    "artifact_owned input must name one concrete artifact",
                    None,
                )
            )
        if not re.fullmatch(
            r"test__[a-z][a-z0-9_]*\.py", model.path.rsplit("/", 1)[-1]
        ):
            findings.append(
                (
                    "TE.ARTIFACT_FILENAME",
                    "artifact-owned filename must be descriptive lowercase snake case",
                    None,
                )
            )
    return tuple(findings)


def _load_ownership(
    path: str, payload: bytes | None, read_error: str | None, supplied: tuple[str, ...]
) -> tuple[
    tuple[dict[str, Any], ...],
    dict[str, dict[str, Any]],
    tuple[tuple[str, str, str, int | None], ...],
]:
    """Load closed ownership input and return deterministic raw findings."""
    if read_error is not None:
        return (), {}, (("TE.OWNERSHIP_INPUT", path, read_error, None),)
    assert payload is not None
    try:
        value = json.loads(payload.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        return (), {}, (("TE.OWNERSHIP_INPUT", path, str(exc), None),)
    minimal = {"modules", "schema_version"}
    projection = minimal | {
        "baseline_collected_node_count",
        "baseline_module_count",
        "baseline_revision",
        "expected_collected_node_count",
        "expected_module_count",
        "test_root",
    }
    if (
        type(value) is not dict
        or set(value) not in (minimal, projection)
        or value.get("schema_version") != 1
        or type(value.get("modules")) is not list
    ):
        return (
            (),
            {},
            (
                (
                    "TE.OWNERSHIP_INPUT",
                    path,
                    "ownership must be a closed schema-version-1 object with modules list",  # noqa: E501
                    None,
                ),
            ),
        )
    findings: list[tuple[str, str, str, int | None]] = []
    by_path: dict[str, dict[str, Any]] = {}
    seen: set[str] = set()
    for index, item in enumerate(value["modules"]):
        start = len(findings)
        if type(item) is not dict:
            findings.append(
                (
                    "TE.OWNERSHIP_ENTRY",
                    path,
                    f"modules[{index}] must be an object",
                    None,
                )
            )
            continue
        allowed = {
            "path",
            "mode",
            "evidence_class",
            "evidence_profile",
            "sut",
            "artifact",
            "conformance_status",
            "content_sha256",
        }
        if not set(item) <= allowed:
            findings.append(
                (
                    "TE.OWNERSHIP_KEYS",
                    path,
                    f"modules[{index}] has unexpected keys",
                    None,
                )
            )
        raw = item.get("path")
        if type(raw) is not str or not raw:
            findings.append(
                (
                    "TE.OWNERSHIP_PATH",
                    path,
                    f"modules[{index}].path must be a nonempty string",
                    None,
                )
            )
            continue
        if raw in seen:
            findings.append(
                (
                    "TE.DUPLICATE_OWNERSHIP_PATH",
                    path,
                    f"duplicate ownership path {raw!r}",
                    None,
                )
            )
            continue
        seen.add(raw)
        mode = item.get("mode")
        if mode not in {"class_owned", "artifact_owned"}:
            findings.append(
                ("TE.OWNERSHIP_MODE", path, f"modules[{index}].mode is invalid", None)
            )
        if item.get("evidence_class") not in _OPENINGS:
            findings.append(
                (
                    "TE.EVIDENCE_CLASS",
                    path,
                    f"modules[{index}].evidence_class is invalid",
                    None,
                )
            )
        profile = item.get("evidence_profile")
        subject = item.get("sut") if mode == "class_owned" else item.get("artifact")
        if (problem := _validate_owner_profile(mode, subject, profile)) is not None:
            findings.append((problem[0], path, f"modules[{index}]: {problem[1]}", None))
        profile_keys = {"evidence_profile"} if profile is not None else set()
        semantic = set(item) - {"conformance_status", "content_sha256"}
        if mode == "class_owned" and (
            semantic != {"path", "mode", "evidence_class", "sut"} | profile_keys
            or type(item.get("sut")) is not str
            or not item["sut"]
        ):
            findings.append(
                (
                    "TE.OWNERSHIP_SUT",
                    path,
                    f"modules[{index}] requires only a nonempty string sut",
                    None,
                )
            )
        elif mode == "artifact_owned" and (
            semantic != {"path", "mode", "evidence_class", "artifact"} | profile_keys
            or type(item.get("artifact")) is not str
            or not item["artifact"].strip()
        ):
            findings.append(
                (
                    "TE.OWNERSHIP_ARTIFACT",
                    path,
                    f"modules[{index}] requires only a concrete nonempty artifact",
                    None,
                )
            )
        if len(findings) == start:
            by_path[raw] = item
    if set(by_path) != set(supplied):
        findings.append(
            (
                "TE.OWNERSHIP_COVERAGE",
                path,
                "ownership paths must exactly equal explicitly supplied paths",
                None,
            )
        )
    return tuple(value["modules"]), by_path, tuple(findings)


class _PythonOwnershipRule:
    """Own source-to-declaration evidence ownership agreement."""

    __slots__ = ()

    def execute(
        self, model: PythonTestModuleModel, owner: dict[str, Any]
    ) -> tuple[tuple[str, str, int | None], ...]:
        """Validate one module against its explicit ownership declaration."""
        return _validate_ownership(model, owner)


class _PythonOwnershipInputLoader:
    """Own deterministic closed ownership-input loading and coverage checks."""

    __slots__ = ()

    def execute(
        self,
        path: str,
        payload: bytes | None,
        read_error: str | None,
        supplied: tuple[str, ...],
    ) -> tuple[
        tuple[dict[str, Any], ...],
        dict[str, dict[str, Any]],
        tuple[tuple[str, str, str, int | None], ...],
    ]:
        """Load one closed ownership document without filesystem access."""
        return _load_ownership(path, payload, read_error, supplied)
