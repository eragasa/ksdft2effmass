#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$root"
python_bin="python/.venv/bin/python"
parent="python.architecture-refactor.public-import-boundaries.current-fact-foundation"
children=(
  closed-domain-contract
  typed-domain-construction
  initializer-acquisition-closure
  runtime-file-completeness
  adversarial-validation
  aggregate-verification
)
"$python_bin" - <<'PY'
import json
from pathlib import Path
root = Path.cwd()
parent = "python.architecture-refactor.public-import-boundaries.current-fact-foundation"
children = (
    "closed-domain-contract",
    "typed-domain-construction",
    "initializer-acquisition-closure",
    "runtime-file-completeness",
    "adversarial-validation",
    "aggregate-verification",
)
selection = json.loads((root / "harness/task-selection.json").read_text())
if selection["active_task_id"] != parent or selection["automatic_successor_activation"] is not False:
    raise SystemExit("F0 selection or automatic-successor state changed")
parent_record = json.loads((root / f"tasks/software/{parent}.json").read_text())
if parent_record["status"] != "planning":
    raise SystemExit("F0 parent must remain planning")
for suffix in children:
    task_id = f"{parent}.{suffix}"
    record = json.loads((root / f"tasks/software/{task_id}.json").read_text())
    if record["task_id"] != task_id or record["parent_task_id"] != parent:
        raise SystemExit(f"invalid child identity: {task_id}")
    if record["status"] != "inactive" or record["explicit_activation_required"] is not True:
        raise SystemExit(f"child is not inactive and explicit: {task_id}")
plan = (root / "harness/reports/python-public-import-foundation-remediation-plan.md").read_text()
for text in (
    "# Corrected finite F0 remediation task list",
    "Six children are the smallest sound decomposition",
    "## C1 — Closed domain contract",
    "## C2 — Typed generated-domain construction",
    "## C3 — Fail-closed initializer acquisition",
    "## C4 — Complete runtime-file acquisition",
    "## C5 — Maintained adversarial validation and final generated pair",
    "## C6 — Final aggregate verification",
    "**ReviewOutcome: NO_BLOCKING_FINDINGS**",
    "**OperatorRequest: AUTHORIZATION_REQUIRED**",
):
    if text not in plan:
        raise SystemExit(f"missing remediation planning text: {text}")
PY
for suffix in "${children[@]}"; do
  task_id="$parent.$suffix"
  "$python_bin" -m ksdft2effmass.harness.cli validate-task-ownership \
    --repository-root "$root" \
    --task "$task_id" \
    --task-record "tasks/software/$task_id.json" \
    --ownership-manifest ".pi/task-ownership/$task_id.json"
done
"$python_bin" -m ksdft2effmass.harness.cli harness-projection --repository-root "$root" check
"$python_bin" -m ksdft2effmass.harness.cli validate-harness --repository-root "$root"
git diff --check
