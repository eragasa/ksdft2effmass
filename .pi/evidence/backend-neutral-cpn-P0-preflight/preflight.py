"""Run the disposable P0 SNAKES capability preflight.

This control-plane evidence script exercises only tiny synthetic Petri nets. It
is not a project CPN contract, production workflow implementation, persistence
format, scientific calculation, or model-validation test. Run it with the
isolated Python environment recorded in ``command-manifest.json`` and write its
JSON result outside the repository before copying back the compact result.
"""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import platform
import shutil
import subprocess
import sys
import tempfile
import warnings
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import snakes.plugins
from snakes import version as snakes_version
from snakes.data import Substitution
from snakes.nets import (
    Expression,
    Marking,
    PetriNet,
    Place,
    StateGraph,
    Transition,
    Variable,
    tAll,
)
from snakes.typing import Instance


@dataclass(frozen=True, slots=True)
class SyntheticToken:
    """Immutable synthetic colored-token payload used only by this preflight."""

    family: str
    identity: str
    parent_id: str = ""
    manifest_id: str = ""
    protocol_version: int = 1
    capability: str = ""
    attempt: int = 0


@dataclass(frozen=True, slots=True)
class ProbeResult:
    """One deterministic probe result."""

    status: str
    details: dict[str, Any]


def _token(**values: Any) -> SyntheticToken:
    """Construct one synthetic token with explicit immutable fields."""

    return SyntheticToken(**values)


def _marking_snapshot(marking: Marking) -> list[dict[str, Any]]:
    """Extract a canonically sorted neutral snapshot from a SNAKES marking."""

    records: list[dict[str, Any]] = []
    for place_name, multiset in marking.items():
        for value in multiset.domain():
            multiplicity = multiset[value]
            if isinstance(value, SyntheticToken):
                payload: Any = asdict(value)
                token_type = f"{type(value).__module__}.{type(value).__qualname__}"
            elif isinstance(value, tuple):
                payload = list(value)
                token_type = "builtins.tuple"
            else:
                payload = value
                token_type = f"{type(value).__module__}.{type(value).__qualname__}"
            records.append(
                {
                    "place_identifier": place_name,
                    "token_type_identifier": token_type,
                    "token_payload": payload,
                    "multiplicity": multiplicity,
                }
            )
    return sorted(
        records,
        key=lambda record: (
            record["place_identifier"],
            record["token_type_identifier"],
            json.dumps(record["token_payload"], sort_keys=True),
        ),
    )


def _basic_and_colored_probe() -> ProbeResult:
    """Exercise construction, token colors, modes, firing, and error behavior."""

    request = _token(
        family="execution_request",
        identity="request-1",
        capability="qe.read-version",
    )
    capability = _token(
        family="tool_capability",
        identity="tool-1",
        capability="qe.read-version",
    )
    authorization = _token(
        family="execution_authorization",
        identity="auth-1",
        capability="qe.read-version",
    )
    net = PetriNet("authorization")
    net.globals.declare("from __main__ import SyntheticToken")
    net.add_place(Place("execution_request", [request], tAll))
    net.add_place(Place("tool_capability", [capability], tAll))
    net.add_place(Place("execution_authorization", [authorization], tAll))
    net.add_place(Place("authorized_request", [], tAll))
    net.add_transition(
        Transition(
            "record_authorized_request",
            Expression(
                "request.capability == capability.capability "
                "and request.capability == authorization.capability"
            ),
        )
    )
    net.add_input("execution_request", "record_authorized_request", Variable("request"))
    net.add_input(
        "tool_capability", "record_authorized_request", Variable("capability")
    )
    net.add_input(
        "execution_authorization",
        "record_authorized_request",
        Variable("authorization"),
    )
    net.add_output(
        "authorized_request",
        "record_authorized_request",
        Expression(
            "SyntheticToken('execution_result', request.identity + ':authorized', "
            "capability=request.capability)"
        ),
    )
    transition = net.transition("record_authorized_request")
    modes = transition.modes()
    if len(modes) != 1:
        raise AssertionError(f"expected one enabled mode, got {modes!r}")
    selected_mode = modes[0]
    transition.fire(selected_mode)
    resulting = net.get_marking()
    if resulting("authorized_request").size() != 1:
        raise AssertionError("authorized result was not produced")

    guard_fail = net.copy("guard-fail")
    guard_fail.set_marking(
        Marking(
            {
                "execution_request": [request],
                "tool_capability": [capability],
                "execution_authorization": [
                    _token(
                        family="execution_authorization",
                        identity="auth-denied",
                        capability="different-capability",
                    )
                ],
            }
        )
    )
    guard_fail_modes = guard_fail.transition("record_authorized_request").modes()
    if guard_fail_modes:
        raise AssertionError("guard-failing tokens unexpectedly enabled transition")

    missing_input = net.copy("missing-input")
    missing_input.set_marking(
        Marking(
            {
                "execution_request": [request],
                "tool_capability": [capability],
            }
        )
    )
    missing_modes = missing_input.transition("record_authorized_request").modes()
    if missing_modes:
        raise AssertionError("missing input unexpectedly enabled transition")

    invalid_binding = Substitution(
        request=request,
        capability=capability,
        authorization=_token(
            family="execution_authorization",
            identity="auth-invalid",
            capability="wrong",
        ),
    )
    invalid_enabled = missing_input.transition("record_authorized_request").enabled(
        invalid_binding
    )
    try:
        missing_input.transition("record_authorized_request").fire(invalid_binding)
    except Exception as error:  # SNAKES owns the concrete exception taxonomy.
        invalid_fire_error = f"{type(error).__name__}: {error}"
    else:
        raise AssertionError("invalid transition binding fired without an error")

    duplicate = _token(family="failure", identity="failure-duplicate", attempt=1)
    token_place = Place(
        "colored_values",
        [
            "text",
            7,
            ("tuple", 2),
            request,
            capability,
            authorization,
            duplicate,
            duplicate,
            _token(family="retry_authorization", identity="retry-1", attempt=2),
            _token(family="provenance_identity", identity="manifest-1"),
        ],
        tAll,
    )
    if token_place.tokens[duplicate] != 2:
        raise AssertionError("duplicate immutable token multiplicity was not retained")
    distinct_count = len(token_place.tokens.domain())
    equal_copy_count = token_place.tokens[
        _token(family="failure", identity="failure-duplicate", attempt=1)
    ]
    try:
        Place("unsupported", [["mutable", "list"]], tAll)
    except Exception as error:
        unhashable_error = f"{type(error).__name__}: {error}"
    else:
        raise AssertionError("unhashable list token was unexpectedly accepted")

    constrained_place = Place(
        "typed_synthetic_tokens", [request], Instance(SyntheticToken)
    )
    try:
        constrained_place.add("hashable-wrong-color")
    except Exception as error:
        wrong_color_error = f"{type(error).__name__}: {error}"
    else:
        raise AssertionError("hashable wrong-color token was unexpectedly accepted")

    multi_mode_net = PetriNet("multi-mode-inspection")
    multi_mode_net.add_place(
        Place(
            "candidates",
            [
                _token(family="tool_capability", identity="candidate-b"),
                _token(family="tool_capability", identity="candidate-a"),
            ],
            Instance(SyntheticToken),
        )
    )
    multi_mode_net.add_transition(Transition("inspect_candidate"))
    multi_mode_net.add_input("candidates", "inspect_candidate", Variable("candidate"))
    multi_mode_net.add_output("candidates", "inspect_candidate", Variable("candidate"))
    first_inspection = multi_mode_net.transition("inspect_candidate").modes()
    second_inspection = multi_mode_net.transition("inspect_candidate").modes()
    canonical_first = sorted(repr(mode) for mode in first_inspection)
    canonical_second = sorted(repr(mode) for mode in second_inspection)
    if len(canonical_first) != 2 or canonical_first != canonical_second:
        raise AssertionError("canonical repeated multi-mode inspection was unstable")

    return ProbeResult(
        status="PASS",
        details={
            "imports": [
                "from snakes.nets import Expression, Marking, PetriNet, Place, "
                "StateGraph, Transition, Variable, tAll",
                "from snakes.data import Substitution",
                "from snakes.typing import Instance",
            ],
            "net_name": net.name,
            "place_names": sorted(place.name for place in net.place()),
            "transition_names": sorted(
                transition.name for transition in net.transition()
            ),
            "selected_mode": repr(selected_mode),
            "resulting_marking": _marking_snapshot(resulting),
            "guard_failure_modes": len(guard_fail_modes),
            "missing_input_modes": len(missing_modes),
            "invalid_binding_enabled": invalid_enabled,
            "invalid_binding_fire_error": invalid_fire_error,
            "colored_distinct_values": distinct_count,
            "duplicate_multiplicity": token_place.tokens[duplicate],
            "equal_frozen_dataclass_lookup_multiplicity": equal_copy_count,
            "unhashable_token_error": unhashable_error,
            "constrained_color_checker": "Instance(SyntheticToken)",
            "constrained_color_positive_size": constrained_place.tokens.size(),
            "hashable_wrong_color_error": wrong_color_error,
            "multi_mode_count": len(first_inspection),
            "canonical_multi_modes_first": canonical_first,
            "canonical_multi_modes_second": canonical_second,
            "engine_mode_order_adopted_as_contract": False,
            "token_requirements": "values used as multiset keys must be hashable; "
            "frozen dataclass value equality and hashing provide value semantics",
        },
    )


def _retry_probe() -> ProbeResult:
    """Exercise retained failure history and authorization-gated retry."""

    failure = _token(
        family="failure",
        identity="attempt-1:failure",
        parent_id="run-1",
        attempt=1,
    )
    authorization = _token(
        family="retry_authorization",
        identity="retry-auth-2",
        parent_id="run-1",
        attempt=2,
    )
    net = PetriNet("retry")
    net.globals.declare("from __main__ import SyntheticToken")
    net.add_place(Place("failed_attempt", [failure], tAll))
    net.add_place(Place("retry_authorization", [authorization], tAll))
    net.add_place(Place("failure_history", [], tAll))
    net.add_place(Place("attempt_requested", [], tAll))
    net.add_transition(
        Transition(
            "authorize_retry",
            Expression(
                "failure.parent_id == authorization.parent_id "
                "and authorization.attempt == failure.attempt + 1"
            ),
        )
    )
    net.add_input("failed_attempt", "authorize_retry", Variable("failure"))
    net.add_input("retry_authorization", "authorize_retry", Variable("authorization"))
    net.add_output("failure_history", "authorize_retry", Variable("failure"))
    net.add_output(
        "attempt_requested",
        "authorize_retry",
        Expression(
            "SyntheticToken('execution_request', "
            "failure.parent_id + ':attempt-' + str(authorization.attempt), "
            "parent_id=failure.parent_id, attempt=authorization.attempt)"
        ),
    )
    modes = net.transition("authorize_retry").modes()
    if len(modes) != 1:
        raise AssertionError("authorized retry must have one mode")
    net.transition("authorize_retry").fire(modes[0])
    snapshot = _marking_snapshot(net.get_marking())
    if not any(
        record["place_identifier"] == "failure_history"
        and record["token_payload"]["identity"] == failure.identity
        for record in snapshot
    ):
        raise AssertionError("failure history was not retained")
    if not any(
        record["place_identifier"] == "attempt_requested"
        and record["token_payload"]["identity"] == "run-1:attempt-2"
        for record in snapshot
    ):
        raise AssertionError("retry did not create a distinct attempt")

    no_auth = net.copy("retry-without-authorization")
    no_auth.set_marking(Marking({"failed_attempt": [failure]}))
    disabled_without_authorization = not no_auth.transition("authorize_retry").modes()
    if not disabled_without_authorization:
        raise AssertionError("retry enabled without authorization")
    return ProbeResult(
        status="PASS",
        details={
            "enabled_modes": len(modes),
            "disabled_without_authorization": disabled_without_authorization,
            "resulting_marking": snapshot,
            "interpretation": "consumed failure is explicitly re-emitted into a "
            "history place while a new attempt identity is constructed",
        },
    )


def _join_net(branch_b: SyntheticToken) -> PetriNet:
    """Construct one synthetic guarded provenance join net."""

    branch_a = _token(
        family="branch_a_result",
        identity="A-1",
        parent_id="parent-1",
        manifest_id="manifest-1",
        protocol_version=1,
    )
    net = PetriNet("provenance-join")
    net.globals.declare("from __main__ import SyntheticToken")
    net.add_place(Place("branch_a_result", [branch_a], tAll))
    net.add_place(Place("branch_b_result", [branch_b], tAll))
    net.add_place(Place("joined", [], tAll))
    net.add_transition(
        Transition(
            "join_branches",
            Expression(
                "a.parent_id == b.parent_id "
                "and a.manifest_id == b.manifest_id "
                "and a.protocol_version == b.protocol_version"
            ),
        )
    )
    net.add_input("branch_a_result", "join_branches", Variable("a"))
    net.add_input("branch_b_result", "join_branches", Variable("b"))
    net.add_output(
        "joined",
        "join_branches",
        Expression(
            "SyntheticToken('execution_result', a.identity + '+' + b.identity, "
            "parent_id=a.parent_id, manifest_id=a.manifest_id, "
            "protocol_version=a.protocol_version)"
        ),
    )
    return net


def _join_probe() -> ProbeResult:
    """Exercise matching and mismatching provenance-compatible joins."""

    matching_b = _token(
        family="branch_b_result",
        identity="B-1",
        parent_id="parent-1",
        manifest_id="manifest-1",
        protocol_version=1,
    )
    matching = _join_net(matching_b)
    modes = matching.transition("join_branches").modes()
    if len(modes) != 1:
        raise AssertionError("matching branch results must enable join")
    matching.transition("join_branches").fire(modes[0])

    mismatches = {
        "parent": _token(
            family="branch_b_result",
            identity="B-parent-mismatch",
            parent_id="parent-2",
            manifest_id="manifest-1",
            protocol_version=1,
        ),
        "manifest": _token(
            family="branch_b_result",
            identity="B-manifest-mismatch",
            parent_id="parent-1",
            manifest_id="manifest-2",
            protocol_version=1,
        ),
        "protocol": _token(
            family="branch_b_result",
            identity="B-protocol-mismatch",
            parent_id="parent-1",
            manifest_id="manifest-1",
            protocol_version=2,
        ),
    }
    mismatch_mode_counts = {
        name: len(_join_net(token).transition("join_branches").modes())
        for name, token in mismatches.items()
    }
    if any(mismatch_mode_counts.values()):
        raise AssertionError("mismatched branch result unexpectedly enabled join")
    return ProbeResult(
        status="PASS",
        details={
            "matching_mode_count": len(modes),
            "matching_result": _marking_snapshot(matching.get_marking()),
            "mismatch_mode_counts": mismatch_mode_counts,
            "interpretation": "completion tokens alone are insufficient; all "
            "guarded provenance and protocol identifiers must match",
        },
    )


def _reachability_probe() -> ProbeResult:
    """Build a tiny bounded core StateGraph and inspect dead markings."""

    net = PetriNet("bounded-state-graph")
    net.add_place(Place("counter", [0]))
    net.add_transition(Transition("increment", Expression("value < 3")))
    net.add_input("counter", "increment", Variable("value"))
    net.add_output("counter", "increment", Expression("value + 1"))
    graph = StateGraph(net)
    graph.build()
    states = list(graph)
    markings = {str(state): repr(graph[state]) for state in states}
    successor_counts = {
        str(state): len(list(graph.successors(state))) for state in states
    }
    dead_states = [state for state in states if successor_counts[str(state)] == 0]
    edge_transition_names = {
        transition.name
        for state in states
        for _, transition, _ in graph.successors(state)
    }
    inferred_dead_transitions = sorted(
        transition.name
        for transition in net.transition()
        if transition.name not in edge_transition_names
    )
    if len(states) != 4 or len(dead_states) != 1:
        raise AssertionError("bounded reachability graph did not have 4/1 states")
    return ProbeResult(
        status="PASS",
        details={
            "provider": "core snakes.nets.StateGraph (not a plugin)",
            "state_count": len(states),
            "completed": graph.completed(),
            "markings": markings,
            "successor_counts": successor_counts,
            "dead_marking_state_ids": dead_states,
            "dead_transition_detection": "not a dedicated public detector; "
            "inferred after complete bounded exploration from transition labels",
            "inferred_dead_transitions": inferred_dead_transitions,
            "restriction": "StateGraph does not detect unboundedness; callers "
            "must bound or otherwise control exploration",
        },
    )


def _graphviz_probe(output_directory: Path) -> ProbeResult:
    """Load the SNAKES Graphviz plugin and conditionally render externally."""

    graphviz_nets = snakes.plugins.load("gv", "snakes.nets")
    plugin_names = list(graphviz_nets.__plugins__)
    net = graphviz_nets.PetriNet("graphviz-derived-view")
    net.add_place(graphviz_nets.Place("ready", ["token"]))
    net.add_place(graphviz_nets.Place("done"))
    net.add_transition(graphviz_nets.Transition("move"))
    net.add_input("ready", "move", graphviz_nets.Variable("token"))
    net.add_output("done", "move", graphviz_nets.Variable("token"))
    graph = net.draw(None)
    dot_text = graph.dot()
    dot_executable = shutil.which("dot")
    details: dict[str, Any] = {
        "plugin_import": "PASS",
        "plugin_loading_call": "snakes.plugins.load('gv', 'snakes.nets')",
        "composed_plugins": plugin_names,
        "derived_dot_constructed_without_system_dot": "digraph" in dot_text,
        "system_dot_executable": dot_executable,
        "authoritative_state": False,
    }
    if dot_executable is None:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            try:
                net.draw(str(output_directory / "net.svg"))
            except Exception as error:
                details["absent_render_error"] = f"{type(error).__name__}: {error}"
            else:
                raise AssertionError("render unexpectedly succeeded without dot")
        details["render_warnings"] = [
            f"{type(item.message).__name__}: {item.message}" for item in caught
        ]
        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecationWarning)
            try:
                net.draw(str(output_directory / "warnings-as-errors.svg"))
            except Exception as error:
                details["warnings_as_errors_render_error"] = (
                    f"{type(error).__name__}: {error}"
                )
            else:
                raise AssertionError(
                    "warnings-as-errors render unexpectedly succeeded without dot"
                )
        return ProbeResult(status="CONDITIONAL_PASS", details=details)

    version = subprocess.run(
        [dot_executable, "-V"],
        check=False,
        capture_output=True,
        text=True,
    )
    target = output_directory / "net.svg"
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        net.draw(str(target))
    render_warnings = [
        f"{type(item.message).__name__}: {item.message}" for item in caught
    ]
    details.update(
        {
            "dot_version_exit_status": version.returncode,
            "dot_version": (version.stderr or version.stdout).strip(),
            "rendered_path": str(target),
            "rendered_size": target.stat().st_size,
            "render_warnings": render_warnings,
        }
    )
    status = "CONDITIONAL_PASS" if render_warnings else "PASS"
    return ProbeResult(status=status, details=details)


def _metadata() -> dict[str, Any]:
    """Collect bounded interpreter and installed-distribution metadata."""

    distributions: dict[str, Any] = {}
    for requested_name in ("SNAKES", "myst-parser", "Sphinx"):
        distribution = importlib.metadata.distribution(requested_name)
        metadata = distribution.metadata
        distributions[requested_name] = {
            "canonical_name": metadata["Name"],
            "version": distribution.version,
            "requires_python": metadata.get("Requires-Python"),
            "license": metadata.get("License"),
            "license_expression": metadata.get("License-Expression"),
            "classifiers": metadata.get_all("Classifier") or [],
            "project_urls": metadata.get_all("Project-URL") or [],
            "requires_dist": metadata.get_all("Requires-Dist") or [],
            "license_files": sorted(
                str(path)
                for path in distribution.files or []
                if "license" in str(path).lower() or "copying" in str(path).lower()
            ),
        }
    return {
        "operating_system": platform.system(),
        "operating_system_release": platform.release(),
        "platform": platform.platform(),
        "architecture": platform.machine(),
        "python_executable": sys.executable,
        "python_version": sys.version,
        "pip_version": importlib.metadata.version("pip"),
        "snakes_import_version": snakes_version,
        "distributions": distributions,
    }


def main() -> int:
    """Run all probes and emit one deterministic JSON result."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ksdft2effmass-p0-graphviz-") as path:
        probes = {
            "basic_colored_guards_bindings": _basic_and_colored_probe(),
            "failure_retry_history": _retry_probe(),
            "provenance_join": _join_probe(),
            "reachability": _reachability_probe(),
            "graphviz": _graphviz_probe(Path(path)),
        }
    result = {
        "schema_version": 1,
        "evidence_classification": (
            "software capability preflight; not scientific validation or UQ"
        ),
        "environment": _metadata(),
        "probes": {name: asdict(probe) for name, probe in probes.items()},
        "neutral_extraction_limitations": [
            "SNAKES marking iteration order is not accepted as a durable guarantee.",
            "Canonical sorting is project-owned and was added only to this "
            "disposable extraction.",
            "Multiplicity is explicit in SNAKES MultiSet items.",
            "Arbitrary Python objects need project-owned type registries and encoders.",
            "Type reconstruction cannot rely on Python qualified names alone.",
            "Schema/model versions, lineage, correlation, retries, and provenance "
            "must be project-owned.",
            "Successful in-memory use does not establish durable serialization "
            "support.",
        ],
    }
    arguments.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"wrote {arguments.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
