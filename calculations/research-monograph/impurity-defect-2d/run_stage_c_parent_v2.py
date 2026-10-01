#!/usr/bin/env python3
"""Version-two CLI adapter for encapsulated accepted-parent Stage C Workflows.

This adapter adds no calculation behavior. Historical retained results remain bound to
``run_stage_c_parent.py`` and its authenticated implementation identities.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import cast

from stage_c_parent.model import JsonValue
from stage_c_parent.workflows import (
    AcceptedParentStageCAdapterFixtureWorkflow,
    AcceptedParentStageCExecutionWorkflow,
    AcceptedParentStageCToyWorkflow,
    AuthoredStageCOperationWorkflow,
)


def main() -> None:
    """Adapt command-line paths into exactly one encapsulated Workflow call."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--accepted-parent-design", type=Path, required=True)
    parser.add_argument("--authored-parent-fixture", type=Path)
    parser.add_argument("--authored-parent-output", type=Path)
    parser.add_argument("--authored-adapter-fixture", type=Path)
    parser.add_argument("--authored-adapter-output", type=Path)
    parser.add_argument("--authored-operation-fixture", type=Path)
    parser.add_argument("--authored-operation-directory", type=Path)
    parser.add_argument("--execution-authorization", type=Path)
    parser.add_argument("--repository-root", type=Path)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    authored_mode = arguments.authored_parent_fixture is not None or (
        arguments.authored_parent_output is not None
    )
    adapter_mode = arguments.authored_adapter_fixture is not None or (
        arguments.authored_adapter_output is not None
    )
    operation_mode = arguments.authored_operation_fixture is not None or (
        arguments.authored_operation_directory is not None
    )
    execution_mode = any(
        value is not None
        for value in (
            arguments.execution_authorization,
            arguments.repository_root,
            arguments.output,
        )
    )
    if sum((authored_mode, adapter_mode, operation_mode, execution_mode)) != 1:
        parser.error(
            "select exactly one authored, adapter, operation, or execution mode"
        )
    if authored_mode:
        if (
            arguments.authored_parent_fixture is None
            or arguments.authored_parent_output is None
        ):
            parser.error("authored mode requires fixture and output")
        result = AcceptedParentStageCToyWorkflow().execute(
            arguments.accepted_parent_design,
            arguments.authored_parent_fixture,
            arguments.authored_parent_output,
        )
    elif adapter_mode:
        if (
            arguments.authored_adapter_fixture is None
            or arguments.authored_adapter_output is None
        ):
            parser.error("adapter mode requires fixture and output")
        result = AcceptedParentStageCAdapterFixtureWorkflow().execute(
            arguments.accepted_parent_design,
            arguments.authored_adapter_fixture,
            arguments.authored_adapter_output,
        )
    elif operation_mode:
        if (
            arguments.authored_operation_fixture is None
            or arguments.authored_operation_directory is None
        ):
            parser.error("authored operation mode requires fixture and directory")
        result = AuthoredStageCOperationWorkflow().execute(
            arguments.accepted_parent_design,
            arguments.authored_operation_fixture,
            arguments.authored_operation_directory,
        )
    else:
        if (
            arguments.execution_authorization is None
            or arguments.repository_root is None
            or arguments.output is None
        ):
            parser.error(
                "execution mode requires authorization, repository root, and output"
            )
        result = AcceptedParentStageCExecutionWorkflow().execute(
            arguments.accepted_parent_design,
            arguments.execution_authorization,
            arguments.repository_root,
            arguments.output,
        )
    inventory = cast(dict[str, JsonValue], result["inventory"])
    summary = cast(dict[str, JsonValue], result["summary"])
    print(
        "stage_c_parent_criteria="
        f"{'PASS' if summary['all_criteria_passed'] else 'FAIL'}"
    )
    print(f"route_evaluations={inventory['route_evaluations']}")
    print(f"model_fit_records={inventory['model_fit_records']}")


if __name__ == "__main__":
    main()
