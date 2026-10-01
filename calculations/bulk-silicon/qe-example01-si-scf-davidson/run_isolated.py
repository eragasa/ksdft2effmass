#!/usr/bin/env python3
"""Plan one manifest-defined Quantum ESPRESSO composition without effects.

This packaging-owned adapter remains fail-closed until generic Workflow authorization,
reservation, claim, and dispatch own process entry.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from ksdft2effmass.simulations.quantumespresso import (
    QuantumEspressoExecutionRequest,
    QuantumEspressoPlanner,
)


def main() -> int:
    """Adapt one manifest path into the simulation-owned planner and Workflow."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--plan-only", action="store_true")
    arguments = parser.parse_args()
    request = QuantumEspressoExecutionRequest(
        manifest_path=arguments.manifest.resolve(strict=True)
    )
    execution = QuantumEspressoPlanner().execute(request)
    print(f"manifest_schema_identity={execution.plan.manifest_schema_identity}")
    print(f"run_identity={execution.plan.run_identity.value}")
    print(f"development_decision_id={execution.plan.development_decision_id}")
    print(
        "execution_grant_identity="
        f"{execution.plan.authority_reference.grant_identity.value}"
    )
    print(
        "authority_snapshot_identity="
        f"{execution.plan.authority_reference.snapshot_identity.value}"
    )
    print(
        "workflow_run_identity="
        f"{execution.local_execution_plan.workflow_run_identity.value}"
    )
    print(
        "dispatch_outcome_identity="
        f"{execution.local_execution_plan.dispatch_outcome_identity.value}"
    )
    print(f"workspace={execution.plan.workspace}")
    if arguments.plan_only:
        print("effect=not_performed")
        return 0
    print("effect=blocked")
    print("reason=authorized Workflow dispatch is required")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
