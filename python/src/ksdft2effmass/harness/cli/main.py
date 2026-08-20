"""Single command dispatcher for repository-local Harness development operations.

The dispatcher owns only subcommand selection. Individual command adapters parse their
explicit inputs, invoke exact Harness operation owners, render deterministic output,
and map operation outcomes to process exit status. Command availability does not grant
Task, scientific, protected-execution, or release authority.
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from importlib import import_module

_COMMAND_MODULES = {
    "harness-projection": "harness_projection",
    "inspect-task-state": "inspect_task_state",
    "refresh-resource-manifest": "refresh_resource_manifest",
    "validate-agent-definitions": "validate_agent_definitions",
    "validate-architecture-decision-cases": "validate_architecture_decision_cases",
    "validate-checkpoints": "validate_checkpoints",
    "validate-documentation-projection": "validate_documentation_projection",
    "validate-evidence-repository-conformance": (
        "validate_evidence_repository_conformance"
    ),
    "validate-harness": "validate_harness",
    "validate-local-harness-resources": "validate_local_harness_resources",
    "validate-python-conformance": "validate_python_conformance",
    "validate-skill-capabilities": "validate_skill_capabilities",
    "validate-task-ownership": "validate_task_ownership",
}


def _usage() -> str:
    commands = "\n".join(f"  {name}" for name in sorted(_COMMAND_MODULES))
    usage = "Usage: python3 -m ksdft2effmass.harness.cli <command> [arguments]"
    return f"{usage}\n\nCommands:\n{commands}"


def run(argv: Sequence[str] | None = None) -> int:
    """Dispatch one explicit Harness development subcommand.

    Parameters
    ----------
    argv
        Arguments excluding the interpreter and module name. When omitted, arguments
        are read from :data:`sys.argv`.

    Returns
    -------
    int
        ``0`` for dispatcher help or the selected command's exit status. Unknown or
        missing commands return ``2``.
    """
    arguments = list(sys.argv[1:] if argv is None else argv)
    if arguments and arguments[0] in {"-h", "--help"}:
        print(_usage())
        return 0
    if not arguments:
        print(_usage(), file=sys.stderr)
        return 2
    command = arguments.pop(0)
    module_name = _COMMAND_MODULES.get(command)
    if module_name is None:
        print(f"unknown Harness command: {command}", file=sys.stderr)
        print(_usage(), file=sys.stderr)
        return 2
    module = import_module(f"{__package__}.{module_name}")
    return module.run(arguments)
