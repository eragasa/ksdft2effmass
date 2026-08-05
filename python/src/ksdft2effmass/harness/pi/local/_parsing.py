"""Private strict parsing support for project-local adapters."""

from __future__ import annotations

import json
from typing import Any

from .models import AdaptationResult, LocalIssue, LocalValidationResult


class _DuplicateKey(ValueError):
    pass


def _pairs(items: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in items:
        if key in result:
            raise _DuplicateKey(key)
        result[key] = value
    return result


def parse_object(
    payload: bytes, path: str
) -> tuple[dict[str, Any] | None, LocalIssue | None]:
    if type(payload) is not bytes:
        raise TypeError("payload must be bytes")
    if type(path) is not str:
        raise TypeError("path must be str")
    try:
        value = json.loads(payload.decode("utf-8"), object_pairs_hook=_pairs)
    except UnicodeDecodeError:
        return None, LocalIssue("PIHL.WIRE.INVALID_UTF8", path, "input is not UTF-8")
    except _DuplicateKey as exc:
        return None, LocalIssue("PIHL.WIRE.DUPLICATE_KEY", path, str(exc))
    except (json.JSONDecodeError, ValueError) as exc:
        return None, LocalIssue("PIHL.WIRE.INVALID_JSON", path, str(exc))
    if type(value) is not dict:
        return None, LocalIssue(
            "PIHL.WIRE.INVALID_TYPE", path, "top level must be an object"
        )
    return value, None


def require_fields(
    obj: dict[str, Any], required: set[str], path: str
) -> LocalIssue | None:
    missing = sorted(required - set(obj))
    if missing:
        return LocalIssue("PIHL.RECORD.MISSING_FIELD", path, missing[0])
    return None


def success(value: object) -> AdaptationResult:
    return AdaptationResult(value, LocalValidationResult("PASS", ()))


def failure(*issues: LocalIssue) -> AdaptationResult:
    return AdaptationResult(
        None,
        LocalValidationResult(
            "FAIL",
            tuple(sorted(set(issues), key=lambda x: (x.code, x.path or "", x.detail))),
        ),
    )


def as_str(value: object, field: str) -> str:
    if type(value) is not str or not value:
        raise TypeError(f"{field} must be a nonempty built-in str")
    return value


def as_bool(value: object, field: str) -> bool:
    if type(value) is not bool:
        raise TypeError(f"{field} must be bool")
    return value


def strings(value: object, field: str) -> tuple[str, ...]:
    if type(value) is not list or any(type(x) is not str or not x for x in value):
        raise TypeError(f"{field} must be an array of nonempty strings")
    return tuple(sorted(value))
