# Retire historical phase agents from live discovery

Status: completed under `.pi/chains/harness-simplification.chain.json`

Task identity: `harness-simplification.agents.live-discovery-cleanup`

Starting revision: `bc4c95b801d6f161fc458deed4519bb8b2ac695f` (`origin/dev` at task start).

Authority: the current human instruction authorized one bounded root-agent discovery cleanup, direct documentation and chain reconciliation, validation, commit, and push. It prohibited subagents, reviewers, historical-agent edits or deletion, new ownership/evidence/checkpoint artifacts, Python or scientific tests, and successor activation.

## Discovery disposition

Project-level PI configuration in `.pi/settings.json` is the live-discovery authority for this cleanup. Its `subagents.agentOverrides` mapping disables the 24 exact package-qualified historical runtime identities reported by PI. All 34 `.pi/agents/*.md` records remain retained: the 10 durable records stay selectable and the 24 phase-specific records remain byte-unchanged historical artifacts. Discoverability does not authorize a task or agent launch.

PI's management `list` action reported 34 selectable project agents before the change and exactly 10 afterward: five durable project roles and five durable harness roles. No historical phase-specific role remains selectable, and no agent was launched for verification.

## Chain reconciliation

The conceptual `harness-simplification.agents.live-discovery` and `harness-simplification.agents.historical-retirement` stages are retained and marked completed by this cleanup. Historical retirement means removal from selectable discovery, not repository deletion. Review-dispatch idempotency is `deferred_inactive`: PI already supplies run IDs, status, resume, and runtime artifacts; the duplicate cause has not been reconstructed; and repository SQLite would not intercept native `subagent(...)` dispatch. This deferral does not block unrelated cleanup.

`active_task` remains `null` and automatic successor activation remains disabled. `harness-simplification.agents.delegation-validation` is the next inactive, unauthorized harness task. Evidence/SQLite, P3, and scientific or protected execution remain inactive and unauthorized.
