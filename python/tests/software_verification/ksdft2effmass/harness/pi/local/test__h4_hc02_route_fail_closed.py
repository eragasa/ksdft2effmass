"""Focused software verification for the authorized H4-HC02 route correction."""

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
    """Load one repository validator without executing its command-line entry point."""
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def h3_route_result(tmp_path: Path, route: object) -> Any:
    """Evaluate only the H3 route gate against a disposable route file."""
    validator = load_module(
        repository_root() / "harness/pi/validation/validate_h3_resources.py",
        "h4_hc02_h3_validator",
    )
    (tmp_path / "validation-route.json").write_text(
        json.dumps(route), encoding="utf-8"
    )
    validator.LOCAL = tmp_path
    validator.R = validator.Report()
    validator.validation_route_gate(
        {
            "resources": [
                {
                    "dependency_ids": ["project-profile"],
                    "format_version": 1,
                    "path": "validation-route.json",
                    "resource_kind": "profile",
                },
                {
                    "path": "profiles/project.json",
                    "resource_id": "project-profile",
                },
            ]
        }
    )
    return validator.R


def route_configuration(route: str) -> dict[str, object]:
    """Return the exact maintained-route wire shape."""
    return {"rollback_route": "legacy", "route": route, "schema_version": 1}


@pytest.mark.parametrize("route", ["legacy", "local"])
def test_h3_route_gate_accepts_exact_authorized_maintained_routes(
    tmp_path: Path, route: str
) -> None:
    """The maintained H3 route permits only the authorized legacy/local choices."""
    report = h3_route_result(tmp_path, route_configuration(route))
    assert report.failures == []
    assert "route.explicit-maintained-route" in report.passes
    assert "route.manifest-identity" in report.passes


@pytest.mark.parametrize(
    "candidate",
    [
        pytest.param(
            {"rollback_route": "legacy", "route": "legacy"}, id="malformed-missing"
        ),
        pytest.param(
            {
                **route_configuration("legacy"),
                "unexpected": True,
            },
            id="malformed-extra",
        ),
        pytest.param(route_configuration("shadow"), id="shadow"),
        pytest.param(route_configuration("unknown"), id="unknown"),
        pytest.param(route_configuration("unsupported"), id="unsupported"),
        pytest.param(
            {**route_configuration("local"), "schema_version": 2},
            id="wrong-schema",
        ),
        pytest.param(
            {**route_configuration("local"), "rollback_route": "local"},
            id="non-legacy-rollback",
        ),
    ],
)
def test_h3_route_gate_rejects_invalid_maintained_routes(
    tmp_path: Path, candidate: dict[str, object]
) -> None:
    """Malformed or unauthorized maintained routes fail the closed H3 gate."""
    report = h3_route_result(tmp_path, candidate)
    assert report.failures == [
        "route.explicit-maintained-route: validation route must be a closed "
        "schema-version-1 legacy/local route with legacy rollback"
    ]
    assert "route.manifest-identity" in report.passes


def replay_payload(consumer: Any, side: str) -> dict[str, Any]:
    """Build the exact closed eight-pair replay payload without running replay."""
    observations = []
    pair_ids = sorted(consumer.PAIR_CLASSIFICATIONS)
    for pair_id in pair_ids:
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
    return {
        "observations": observations,
        "pair_ids": pair_ids,
        "schema_version": 1,
        "side": side,
    }


def load_consumer() -> Any:
    """Load the concrete route consumer without invoking retained replay."""
    return load_module(
        repository_root() / ".pi/skills/validate_harness.py",
        "h4_hc02_route_consumer",
    )


def test_run_route_fails_on_failed_h3_observation(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """A successful process cannot mask a failed H3 observation."""
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


@pytest.mark.parametrize("side", ["local", "legacy"])
def test_run_route_accepts_exact_all_pass_observations(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, side: str
) -> None:
    """Exact all-PASS payloads preserve local and retained legacy behavior."""
    consumer = load_consumer()
    payload = replay_payload(consumer, side)
    monkeypatch.setattr(
        consumer,
        "run_replay",
        lambda _root, _side: (
            {"command_id": f"selected-validator-replay-{side}", "exit_status": 0},
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


@pytest.mark.parametrize("defect", ["missing", "duplicate", "malformed"])
def test_run_route_rejects_incomplete_or_malformed_observations(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, defect: str
) -> None:
    """Missing, duplicate, and malformed observations fail closed."""
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


def test_rollback_action_still_returns_retained_legacy() -> None:
    """Rollback from every non-legacy route returns the legacy configuration."""
    action = RollBackValidationRoute()
    for route in (ValidationRoute.LOCAL, ValidationRoute.SHADOW):
        assert action.execute(RouteConfiguration(route)) == RouteConfiguration(
            ValidationRoute.LEGACY
        )
