#!/usr/bin/env python3
"""CLI adapter for independent accepted-parent Stage C verification."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from stage_c_parent_verification.verifier import IndependentStageCParentVerifier


def main() -> None:
    """Adapt argparse inputs into the independent verification ActionObject."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--accepted-parent-design", type=Path)
    fixtures = parser.add_mutually_exclusive_group()
    fixtures.add_argument("--authored-parent-fixture", type=Path)
    fixtures.add_argument("--authored-adapter-fixture", type=Path)
    parser.add_argument("--execution-authorization", type=Path)
    parser.add_argument("--repository-root", type=Path)
    parser.add_argument("--result", type=Path, required=True)
    arguments = parser.parse_args()
    fixture = (
        arguments.authored_parent_fixture
        if arguments.authored_parent_fixture is not None
        else arguments.authored_adapter_fixture
    )
    authored_mode = fixture is not None or arguments.accepted_parent_design is not None
    accepted_mode = (
        arguments.execution_authorization is not None
        or arguments.repository_root is not None
    )
    if authored_mode == accepted_mode:
        parser.error("select exactly one authored or accepted verification mode")
    verifier = IndependentStageCParentVerifier()
    if authored_mode:
        if fixture is None or arguments.accepted_parent_design is None:
            parser.error("authored verification requires design and fixture")
        report = verifier.execute(
            arguments.accepted_parent_design,
            fixture,
            arguments.result,
        )
    else:
        if (
            arguments.execution_authorization is None
            or arguments.repository_root is None
        ):
            parser.error("accepted verification requires authorization and root")
        report = verifier.execute_accepted(
            arguments.execution_authorization,
            arguments.repository_root,
            arguments.result,
        )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
