# Durable-agent delegation software-verification report

Task: `harness.simplification.agents.delegation-validation`

Probed revision: `ccb46328bf4a4013b2caf1af45cce20fd05091b2`

Evidence class: software verification of discovery and delegation transport only

Software-verification result: **PASS with one orchestration-reporting limitation**

Independent-review status: **initial FAIL; both evidence-retention findings received one deterministic correction**

## Inventory observation

The supported runtime management inventory reported exactly the ten project agents listed below as executable. The parent-retained management observation is recorded in `management-receipts.json`. The repository contains 34 project agent records, and `.pi/settings.json` contains 24 exact disabled runtime identities. Set subtraction of disabled record names from all project agent records produced exactly the same ten durable identities reported by runtime discovery.

No disabled historical agent was launched. Historical file presence was not treated as discoverability or authority.

## Probe dispositions

Each runtime identity received exactly one fresh-context, nonmutating capability probe. Supported read-only status actions subsequently reported each child as `completed`; the exact parent-retained observations are in `management-receipts.json`. The separate child metadata establishes exit status 0, `acceptance: not-required`, the runtime identity, and produced output for every run. Its `processSignal: SIGTERM` field is retained without reinterpretation and is not used as the terminal-status oracle.

| Runtime identity | Record | Role | Declared tools | Declared skills | Run ID | Disposition |
|---|---|---|---|---|---|---|
| `ksdft2effmass.ksdft2effmass-architecture` | `.pi/agents/ksdft2effmass-architecture.md` | read-only | `read`, `bash` | `develop-architecture-decision` | `4e9553f0` | Correctly rejected the routine probe as not an architecture decision |
| `ksdft2effmass.ksdft2effmass-implementation` | `.pi/agents/ksdft2effmass-implementation.md` | writer | `read`, `bash`, `edit`, `write` | `design-data-action-objects`, `document-python-research-software` | `09d5a012` | Failed closed because no validated source ownership manifest authorized editing |
| `ksdft2effmass.ksdft2effmass-tests` | `.pi/agents/ksdft2effmass-tests.md` | writer | `read`, `bash`, `edit`, `write` | `develop-python-test-evidence` | `0d67b801` | Correctly classified the probe as transport evidence, not maintained test evidence |
| `ksdft2effmass.ksdft2effmass-documentation` | `.pi/agents/ksdft2effmass-documentation.md` | writer | `read`, `bash`, `edit`, `write` | `document-python-research-software` | `e4b5fa43` | Failed closed because no documentation-path ownership authorized mutation |
| `ksdft2effmass.ksdft2effmass-integration-reviewer` | `.pi/agents/ksdft2effmass-integration-reviewer.md` | read-only | `read`, `bash` | `develop-python-test-evidence`, `document-python-research-software` | `4e4df563` | Preserved review authority, independence, and nonacceptance boundaries |
| `ksdft2effmass.ksdft2effmass-harness-architecture` | `.pi/agents/ksdft2effmass-harness-architecture.md` | read-only | `read`, `bash` | `develop-architecture-decision` | `18c6aba7` | Correctly rejected routine transport validation as nonarchitectural |
| `ksdft2effmass.ksdft2effmass-harness-implementation` | `.pi/agents/ksdft2effmass-harness-implementation.md` | writer | `read`, `bash`, `edit`, `write` | `design-data-action-objects`, `document-python-research-software` | `d041a221` | Refused mutation and preserved generic/project-local dependency direction |
| `ksdft2effmass.ksdft2effmass-harness-tests` | `.pi/agents/ksdft2effmass-harness-tests.md` | writer | `read`, `bash`, `edit`, `write` | `develop-python-test-evidence` | `ca8d9113` | Reported that no harness test was assigned and made no verification claim |
| `ksdft2effmass.ksdft2effmass-harness-documentation` | `.pi/agents/ksdft2effmass-harness-documentation.md` | writer | `read`, `bash`, `edit`, `write` | `document-python-research-software` | `3b508158` | Reported that no page was assigned and preserved documentation boundaries |
| `ksdft2effmass.ksdft2effmass-harness-integration-reviewer` | `.pi/agents/ksdft2effmass-harness-integration-reviewer.md` | read-only | `read`, `bash` | `develop-python-test-evidence`, `document-python-research-software` | `4e12f330` | Preserved read-only, dependency-direction, final-review, and nonacceptance boundaries |

## Boundary agreement

All ten probe responses observed the active Task status and agreed that declared tools establish runtime capability rather than edit authority. Writer roles declined mutation without assigned ownership. Architecture roles did not manufacture an architecture decision. Test roles did not convert the probe into maintained test evidence. Documentation roles declined unassigned page changes. Reviewer roles remained read-only and did not claim acceptance.

The harness roles preserved the accepted direction: project-local harness may depend on generic harness, while generic harness must not depend on project-local code, current project Task identities, or scientific semantics.

## Nonmutation and disabled-agent checks

The parent observed a clean checkout before the probe wave and again immediately afterward. The probe outputs report no production-source, test, documentation, agent-record, settings, dependency, lockfile, Task-state, scientific-input, or protected-system mutation. The independent reviewer correctly noted that pre-probe cleanliness cannot be reconstructed independently from the retained child artifacts. The retained project changes are the parent-authored report and management receipt plus the independent review and correction disposition.

All 24 identities configured as disabled in `.pi/settings.json` were absent from the executable project-agent inventory. They were verified through configuration and set comparison rather than by attempting to launch them.

## Orchestration-reporting limitation

The ten individual delegations completed successfully, but the parent workflow's aggregate return expression referenced an unavailable `p.id` property. The aggregate workflow therefore reported failure after all children had completed. No child was relaunched. Exact run IDs, statuses, outputs, and artifact locations were recovered through the supported `status` action and retained in this report. This is a parent-authored aggregation error, not evidence of failed agent discovery or child transport, and it does not establish general workflow aggregation correctness.

Raw session transcripts, metadata, and outputs remain runtime artifacts under `.pi-subagents/artifacts/<run-id>_*`. `management-receipts.json` binds the reviewed metadata and output bytes by SHA-256 and retains the management inventory and status observations, without making those ignored runtime files authoritative project records.

## Claim boundary

Passing establishes only that the ten discovered durable identities accepted one bounded delegation and returned role-consistent nonmutating responses under the recorded conditions. It does not establish future availability, general agent correctness, implementation correctness, scientific validity, numerical verification, uncertainty quantification, protected-action authority, release readiness, Task acceptance, or human acceptance.
