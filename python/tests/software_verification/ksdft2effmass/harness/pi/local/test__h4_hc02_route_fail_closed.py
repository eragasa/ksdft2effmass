r"""Software verification of h4 hc02 route fail closed.

Facet and represented meaning
Focused software verification for the authorized H4-HC02 route correction.

Intrinsic and cross-object scope
The primary owner is h4 hc02 route fail closed; public behavior and fixed repository
resources provide the exact oracle.

VVUQ and scientific exclusions
Passing establishes only the stated software contract. Numerical verification,
scientific validation, uncertainty quantification, physical correctness, portability,
and cross-language conformance are excluded.
"""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
from typing import Any

import pytest

from ksdft2effmass.harness.pi.local import (
    RollBackValidationRoute,
    RouteConfiguration,
    ValidationRoute,
)

from .conftest import repository_root

pytestmark = pytest.mark.software_verification


def load_module(path: Path, name: str) -> Any:
    """Evidence ID
    Owns no identifier; supports SV-HL-014.
    Requirement
    Provide explicit setup mechanics for the h4 hc02 route fail closed evidence without
    owning an independent result.
    Method
    Construct the named route or replay partition, substitute only the public route
    dependency, and invoke the maintained H3 gate or route consumer.
    Oracle
    The closed route schema, exact current-local check inventory, and retained-legacy
    observation shape fix the result independently of the consumer.
    Acceptance
    Status, command exit values, route identity, and issue text match exactly; no
    approximate or warning acceptance is used.
    Interpretation
    Failure identifies route-schema drift, consumer precedence drift, controlled-payload
    error, or stale current-resource evidence.
    Limitations
    This is deterministic software verification only; numerical verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def h3_route_result(tmp_path: Path, route: object) -> Any:
    """Evidence ID
    Owns no identifier; supports SV-HL-014.
    Requirement
    Provide explicit setup mechanics for the h4 hc02 route fail closed evidence without
    owning an independent result.
    Method
    Construct the named route or replay partition, substitute only the public route
    dependency, and invoke the maintained H3 gate or route consumer.
    Oracle
    The closed route schema, exact current-local check inventory, and retained-legacy
    observation shape fix the result independently of the consumer.
    Acceptance
    Status, command exit values, route identity, and issue text match exactly; no
    approximate or warning acceptance is used.
    Interpretation
    Failure identifies route-schema drift, consumer precedence drift, controlled-payload
    error, or stale current-resource evidence.
    Limitations
    This is deterministic software verification only; numerical verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    validator = load_module(
        repository_root() / "harness/pi/validation/validate_h3_resources.py",
        "h4_hc02_h3_validator",
    )
    (tmp_path / "validation-route.json").write_text(json.dumps(route), encoding="utf-8")
    validator.LOCAL = tmp_path
    validator.R = validator.Report()
    validator.validation_route_gate(
        {
            "resources": [
                {
                    "dependency_ids": ["current-local-replay", "project-profile"],
                    "format_version": 1,
                    "path": "validation-route.json",
                    "resource_kind": "profile",
                },
                {
                    "path": "profiles/project.json",
                    "resource_id": "project-profile",
                },
                {
                    "path": "validation/replay_current_validators.py",
                    "resource_id": "current-local-replay",
                },
            ]
        }
    )
    return validator.R


def route_configuration(route: str) -> dict[str, object]:
    """Evidence ID
    Owns no identifier; supports SV-HL-014.
    Requirement
    Provide explicit setup mechanics for the h4 hc02 route fail closed evidence without
    owning an independent result.
    Method
    Construct the named route or replay partition, substitute only the public route
    dependency, and invoke the maintained H3 gate or route consumer.
    Oracle
    The closed route schema, exact current-local check inventory, and retained-legacy
    observation shape fix the result independently of the consumer.
    Acceptance
    Status, command exit values, route identity, and issue text match exactly; no
    approximate or warning acceptance is used.
    Interpretation
    Failure identifies route-schema drift, consumer precedence drift, controlled-payload
    error, or stale current-resource evidence.
    Limitations
    This is deterministic software verification only; numerical verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    return {"rollback_route": "legacy", "route": route, "schema_version": 1}


@pytest.mark.parametrize(
    "route", ["legacy", "local"], ids=["legacy_route", "local_route"]
)
def test_artifact__h3_route_gate__accepts_authorized_maintained_routes(
    tmp_path: Path, route: str
) -> None:
    """Evidence ID
    SV-HL-014
    Requirement
    The maintained H3 route permits only the authorized legacy/local choices.
    Method
    Construct the named route or replay partition, substitute only the public route
    dependency, and invoke the maintained H3 gate or route consumer.
    Oracle
    The closed route schema, exact current-local check inventory, and retained-legacy
    observation shape fix the result independently of the consumer.
    Acceptance
    Status, command exit values, route identity, and issue text match exactly; no
    approximate or warning acceptance is used.
    Interpretation
    Failure identifies route-schema drift, consumer precedence drift, controlled-payload
    error, or stale current-resource evidence.
    Limitations
    This is deterministic software verification only; numerical verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    report = h3_route_result(tmp_path, route_configuration(route))
    assert report.failures == []
    assert "route.explicit-maintained-route" in report.passes
    assert "route.manifest-identity" in report.passes


@pytest.mark.parametrize(
    "candidate",
    [
        pytest.param(
            {"rollback_route": "legacy", "route": "legacy"}, id="missing_schema_version"
        ),
        pytest.param(
            {
                **route_configuration("legacy"),
                "unexpected": True,
            },
            id="unexpected_field",
        ),
        pytest.param(route_configuration("shadow"), id="shadow"),
        pytest.param(route_configuration("unknown"), id="unknown"),
        pytest.param(route_configuration("unsupported"), id="unsupported"),
        pytest.param(
            {**route_configuration("local"), "schema_version": 2},
            id="unsupported_schema_version",
        ),
        pytest.param(
            {**route_configuration("local"), "rollback_route": "local"},
            id="nonlegacy_rollback_route",
        ),
    ],
)
def test_artifact__h3_route_gate__rejects_invalid_maintained_routes(
    tmp_path: Path, candidate: dict[str, object]
) -> None:
    """Evidence ID
    SV-HL-015
    Requirement
    Malformed or unauthorized maintained routes fail the closed H3 gate.
    Method
    Construct the named route or replay partition, substitute only the public route
    dependency, and invoke the maintained H3 gate or route consumer.
    Oracle
    The closed route schema, exact current-local check inventory, and retained-legacy
    observation shape fix the result independently of the consumer.
    Acceptance
    Status, command exit values, route identity, and issue text match exactly; no
    approximate or warning acceptance is used.
    Interpretation
    Failure identifies route-schema drift, consumer precedence drift, controlled-payload
    error, or stale current-resource evidence.
    Limitations
    This is deterministic software verification only; numerical verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    report = h3_route_result(tmp_path, candidate)
    assert report.failures == [
        "route.explicit-maintained-route: validation route must be a closed "
        "schema-version-1 legacy/local route with legacy rollback"
    ]
    assert "route.manifest-identity" in report.passes


def replay_payload(consumer: Any, side: str) -> dict[str, Any]:
    """Evidence ID
    Owns no identifier; supports SV-HL-014.
    Requirement
    Provide explicit setup mechanics for the h4 hc02 route fail closed evidence without
    owning an independent result.
    Method
    Construct the named route or replay partition, substitute only the public route
    dependency, and invoke the maintained H3 gate or route consumer.
    Oracle
    The closed route schema, exact current-local check inventory, and retained-legacy
    observation shape fix the result independently of the consumer.
    Acceptance
    Status, command exit values, route identity, and issue text match exactly; no
    approximate or warning acceptance is used.
    Interpretation
    Failure identifies route-schema drift, consumer precedence drift, controlled-payload
    error, or stale current-resource evidence.
    Limitations
    This is deterministic software verification only; numerical verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    observations = []
    pair_ids = sorted(consumer.PAIR_CLASSIFICATIONS)

    def exercise_pair_id_case_215_2(pair_id: Any) -> Any:
        observations.append(
            {
                "input_identities": [],
                "input_set_hash": f"hash-{pair_id}",
                "observation": {
                    "command": ["represented", pair_id],
                    "exit_status": 0,
                    "inventory": [],
                    "issue_facts": [],
                    "paths": [],
                    "related_identities": [],
                    "report_identity": None,
                    "state": [],
                    "status": "PASS",
                },
                "pair_id": pair_id,
            }
        )

    _ = [exercise_pair_id_case_215_2(pair_id) for pair_id in (pair_ids)]
    return {
        "observations": observations,
        "pair_ids": pair_ids,
        "schema_version": 1,
        "side": side,
    }


def load_consumer() -> Any:
    """Evidence ID
    Owns no identifier; supports SV-HL-014.
    Requirement
    Provide explicit setup mechanics for the h4 hc02 route fail closed evidence without
    owning an independent result.
    Method
    Construct the named route or replay partition, substitute only the public route
    dependency, and invoke the maintained H3 gate or route consumer.
    Oracle
    The closed route schema, exact current-local check inventory, and retained-legacy
    observation shape fix the result independently of the consumer.
    Acceptance
    Status, command exit values, route identity, and issue text match exactly; no
    approximate or warning acceptance is used.
    Interpretation
    Failure identifies route-schema drift, consumer precedence drift, controlled-payload
    error, or stale current-resource evidence.
    Limitations
    This is deterministic software verification only; numerical verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    return load_module(
        repository_root() / ".pi/skills/validate_harness.py",
        "h4_hc02_route_consumer",
    )


def test_artifact__run_route__fails_on_failed_h3_observation(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Evidence ID
    SV-HL-016
    Requirement
    A successful process cannot mask a failed H3 observation.
    Method
    Construct the named route or replay partition, substitute only the public route
    dependency, and invoke the maintained H3 gate or route consumer.
    Oracle
    The closed route schema, exact current-local check inventory, and retained-legacy
    observation shape fix the result independently of the consumer.
    Acceptance
    Status, command exit values, route identity, and issue text match exactly; no
    approximate or warning acceptance is used.
    Interpretation
    Failure identifies route-schema drift, consumer precedence drift, controlled-payload
    error, or stale current-resource evidence.
    Limitations
    This is deterministic software verification only; numerical verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    consumer = load_consumer()
    payload = replay_payload(consumer, "local")
    h3 = next(
        item
        for item in payload["observations"]
        if item["pair_id"] == "h3-resource-validator"
    )
    h3["observation"]["status"] = "FAIL"
    h3["observation"]["exit_status"] = 1
    monkeypatch.setattr(
        consumer,
        "run_replay",
        lambda _root, _side: (
            {"command_id": "selected-validator-replay-local", "exit_status": 0},
            payload,
        ),
    )
    assert consumer.run_route(tmp_path, "local")["status"] == "FAIL"


@pytest.mark.parametrize("side", ["local", "legacy"], ids=["local_side", "legacy_side"])
def test_artifact__run_route__accepts_exact_all_pass_observations(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, side: str
) -> None:
    """Evidence ID
    SV-HL-017
    Requirement
    Exact all-PASS payloads preserve local and retained legacy behavior.
    Method
    Construct the named route or replay partition, substitute only the public route
    dependency, and invoke the maintained H3 gate or route consumer.
    Oracle
    The closed route schema, exact current-local check inventory, and retained-legacy
    observation shape fix the result independently of the consumer.
    Acceptance
    Status, command exit values, route identity, and issue text match exactly; no
    approximate or warning acceptance is used.
    Interpretation
    Failure identifies route-schema drift, consumer precedence drift, controlled-payload
    error, or stale current-resource evidence.
    Limitations
    This is deterministic software verification only; numerical verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    consumer = load_consumer()
    payload = replay_payload(consumer, side)
    if side == "local":
        local_payload = {
            "checks": [
                {"check_id": check_id, "exit_status": 0, "status": "PASS"}
                for check_id in sorted(consumer.CURRENT_LOCAL_CHECK_IDS)
            ],
            "schema_version": 1,
            "side": "local",
            "status": "PASS",
        }
        monkeypatch.setattr(
            consumer,
            "run_current_local",
            lambda _root: (
                {"command_id": "selected-validator-replay-local", "exit_status": 0},
                local_payload,
            ),
        )
    else:
        monkeypatch.setattr(
            consumer,
            "run_replay",
            lambda _root, _side: (
                {"command_id": "selected-validator-replay-legacy", "exit_status": 0},
                payload,
            ),
        )
    assert consumer.run_route(tmp_path, side) == {
        "commands": [
            {"command_id": f"selected-validator-replay-{side}", "exit_status": 0}
        ],
        "route": side,
        "status": "PASS",
    }


@pytest.mark.parametrize(
    "defect",
    ["missing", "duplicate", "malformed"],
    ids=["missing_observation", "duplicate_observation", "malformed_observation"],
)
def test_artifact__run_route__rejects_incomplete_or_malformed_observations(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, defect: str
) -> None:
    """Evidence ID
    SV-HL-018
    Requirement
    Missing, duplicate, and malformed observations fail closed.
    Method
    Construct the named route or replay partition, substitute only the public route
    dependency, and invoke the maintained H3 gate or route consumer.
    Oracle
    The closed route schema, exact current-local check inventory, and retained-legacy
    observation shape fix the result independently of the consumer.
    Acceptance
    Status, command exit values, route identity, and issue text match exactly; no
    approximate or warning acceptance is used.
    Interpretation
    Failure identifies route-schema drift, consumer precedence drift, controlled-payload
    error, or stale current-resource evidence.
    Limitations
    This is deterministic software verification only; numerical verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    consumer = load_consumer()
    payload = replay_payload(consumer, "local")
    observations = payload["observations"]
    if defect == "missing":
        observations.pop()
    elif defect == "duplicate":
        observations.append(copy.deepcopy(observations[0]))
    else:
        observations[0]["observation"].pop("report_identity")
    monkeypatch.setattr(
        consumer,
        "run_replay",
        lambda _root, _side: (
            {"command_id": "selected-validator-replay-local", "exit_status": 0},
            payload,
        ),
    )
    assert consumer.run_route(tmp_path, "local")["status"] == "FAIL"


def test_method__execute__returns_retained_legacy_route() -> None:
    """Evidence ID
    SV-HL-019
    Requirement
    Rollback from every non-legacy route returns the legacy configuration.
    Method
    Construct the named route or replay partition, substitute only the public route
    dependency, and invoke the maintained H3 gate or route consumer.
    Oracle
    The closed route schema, exact current-local check inventory, and retained-legacy
    observation shape fix the result independently of the consumer.
    Acceptance
    Status, command exit values, route identity, and issue text match exactly; no
    approximate or warning acceptance is used.
    Interpretation
    Failure identifies route-schema drift, consumer precedence drift, controlled-payload
    error, or stale current-resource evidence.
    Limitations
    This is deterministic software verification only; numerical verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    action = RollBackValidationRoute()

    def exercise_route_case_396_1(route: Any) -> Any:
        assert action.execute(RouteConfiguration(route)) == RouteConfiguration(
            ValidationRoute.LEGACY
        )

    _ = [
        exercise_route_case_396_1(route)
        for route in ((ValidationRoute.LOCAL, ValidationRoute.SHADOW))
    ]
