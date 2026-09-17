"""Python script entry point for a local synthetic dispatch-entry worker.

No scientific executable runs. The maintained test owner supplies typed fixture
adaptation; process termination intentionally occurs before the fake effect.
"""

import sys
from pathlib import Path

# Match the test package's existing ``control`` module identity.
sys.path.insert(0, str(Path(__file__).parents[2]))
from control import (  # noqa: E402
    test__WorkflowRunDispatchEntryCommitter as entry_evidence,
)

if __name__ == "__main__":
    entry_evidence.TestWorkflowRunDispatchEntryCommitter.run_worker(
        Path(sys.argv[1]), sys.argv[2], sys.argv[3]
    )
