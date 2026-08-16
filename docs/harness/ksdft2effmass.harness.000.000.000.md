---
document_id: ksdft2effmass.harness.000.000.000
task_id: harness
parent: null
status: current
sphinx: excluded
---

# Harness documentation

The PI harness is the repository control-plane support used to represent explicit
records, validate bounded work, route maintained resources, and preserve evidence.
It does not perform scientific calculations or grant scientific, release, or
protected-execution authority.

The maintained hierarchy separates current architecture, simplification, proposed
human review, and historical documentation. Current architecture describes
implemented behavior. Simplification pages combine completed bounded slices with
explicit proposals and deferrals. Human-review pages are proposals only and do not
implement an interface or activate work. Historical pages preserve prior context.

## Document hierarchy

| Document | Task identity | Title | Status | Sphinx |
|---|---|---|---|---|
| [harness.000.000.000](ksdft2effmass.harness.000.000.000.md) | `harness` | Harness documentation | Current | Excluded |
| [harness.001.000.000](ksdft2effmass.harness.001.000.000.md) | `harness-current` | Current harness architecture | Current | Included |
| [harness.001.001.000](ksdft2effmass.harness.001.001.000.md) | `harness-current.boundaries` | Generic and project-local boundaries | Current | Included |
| [harness.001.002.000](ksdft2effmass.harness.001.002.000.md) | `harness-current.resources` | Resources, profiles, and skills | Current | Included |
| [harness.001.003.000](ksdft2effmass.harness.001.003.000.md) | `harness-current.python` | Python implementation | Current | Included |
| [harness.001.004.000](ksdft2effmass.harness.001.004.000.md) | `harness-current.evidence` | Validation and evidence | Current | Included |
| [harness.001.006.000](ksdft2effmass.harness.001.006.000.md) | `harness-current.status` | Current status and limitations | Current | Included |
| [harness.002.000.000](ksdft2effmass.harness.002.000.000.md) | `harness-simplification` | Harness simplification plan | Proposed | Excluded |
| [harness.002.001.000](ksdft2effmass.harness.002.001.000.md) | — | First harness simplification round | Current index | Excluded |
| [harness.002.001.001](ksdft2effmass.harness.002.001.001.md) | `harness-simplification.state` | Unified state model | Proposed | Excluded |
| [harness.002.001.002](ksdft2effmass.harness.002.001.002.md) | `harness-simplification.evidence` | Extractable evidence subsystem | Proposed | Excluded |
| [harness.002.001.003](ksdft2effmass.harness.002.001.003.md) | `harness-simplification.agents` | Durable agent architecture | Mixed | Excluded |
| [harness.002.001.004](ksdft2effmass.harness.002.001.004.md) | `harness-simplification.agents.durable-roles` | Create durable harness roles | Completed | Excluded |
| [harness.002.001.005](ksdft2effmass.harness.002.001.005.md) | `harness-simplification.agents.project-architecture` | Simplify durable project roles | Completed | Excluded |
| [harness.002.001.006](ksdft2effmass.harness.002.001.006.md) | `harness-simplification.agents.executable-tool-placement-contract` | Executable harness-tool placement contract | Completed | Excluded |
| [harness.002.001.007](ksdft2effmass.harness.002.001.007.md) | `harness-simplification.execution` | Maintained execution interface | Proposed | Excluded |
| [harness.002.001.008](ksdft2effmass.harness.002.001.008.md) | `harness-simplification.capability-rationalization` | Harness capability ownership rationalization | Mixed; Slice 7 deferred | Excluded |
| [harness.002.001.009](ksdft2effmass.harness.002.001.009.md) | `harness-simplification.migration` | Incremental migration plan | Historical proposal; migration subsystem deferred | Excluded |
| [harness.002.001.010](ksdft2effmass.harness.002.001.010.md) | `harness.simplification.docs-json.task-model-contract` | Human review: per-file Task-document migration | Historical accepted contract; subsystem deferred | Excluded |
| [harness.002.001.011](ksdft2effmass.harness.002.001.011.md) | `harness.simplification.docs-json.task-model-contract` | HarnessTask model contract | Core Task model retained | Excluded |
| [harness.002.001.012](ksdft2effmass.harness.002.001.012.md) | `harness.simplification.docs-json.task-implementation-hardening` | HarnessTask implementation and hardening | Superseded without architecture acceptance | Excluded |
| [harness.002.001.013](ksdft2effmass.harness.002.001.013.md) | `harness.simplification.docs-json.task-document-migration` | Serial Task-document migration | Deferred inactive | Excluded |
| [harness.002.002.005](ksdft2effmass.harness.002.002.005.md) | `harness.simplification.docs-json.documentation-correction` | Documentation/control consistency correction | Narrative; JSON authoritative | Excluded |
| [harness.003.000.000](ksdft2effmass.harness.003.000.000.md) | — | Human review interface | Pilot packet ready; broader program inactive | Excluded |
| [harness.003.001.000](ksdft2effmass.harness.003.001.000.md) | `human-review-interface.review-packet-pilot` | Initial human-review interface round | Pilot packet ready | Excluded |
| [harness.003.001.001](ksdft2effmass.harness.003.001.001.md) | — | Human Review Packet and Decision Workflow | `proposed_inactive` | Excluded |
| [harness.004.000.000](ksdft2effmass.harness.004.000.000.md) | `harness.telemetry` | Harness telemetry | Proposed inactive | Excluded |
| [Versioned architecture](../architecture/index.md) | `harness.architecture-v2.plan` | V1 snapshot, normative v2 target, and migration crosswalk | Planning-only Task active; implementation Task deferred | Excluded |
| [harness.090.000.000](ksdft2effmass.harness.090.000.000.md) | `harness-history` | Historical documentation index | Historical | Excluded |

## Program boundaries

- [harness.001](ksdft2effmass.harness.001.000.000.md) documents the current,
  implemented harness architecture.
- [harness.002](ksdft2effmass.harness.002.000.000.md) documents simplification,
  including completed bounded work and explicitly inactive proposals.
- [harness.003](ksdft2effmass.harness.003.000.000.md) implements bounded
  human-review packet preparation while decision recording, persistence, and the
  broader workflow remain inactive proposals.
- [harness.004](ksdft2effmass.harness.004.000.000.md) indexes the inactive
  operational telemetry implementation and evaluation sequence.
- [Versioned architecture](../architecture/index.md) separates the implemented v1 snapshot, normative v2 target, and migration crosswalk. Its planning-only Task is active; the implementation Task remains deferred, and no scientific Task or execution is activated by the planning work.
- [harness.090](ksdft2effmass.harness.090.000.000.md) indexes historical material.

Maintained documentation explains architecture and contributor practice. Mutable
authorization and operational state remain in their owning repository records.
Historical evidence records previous conditions and does not govern current work.
A proposed page cannot activate implementation or replace an accepted contract.

## Historical migration

| Previous document | Current document | Disposition |
|---|---|---|
| `ksdft2effmass.harness.00.md` | [harness.000.000.000](ksdft2effmass.harness.000.000.000.md) | Replaced by the coordinate-based root index. |
| `ksdft2effmass.harness.01.md` | [harness.001.000.000](ksdft2effmass.harness.001.000.000.md) | Updated from prospective boundaries to the current architecture. |
| `ksdft2effmass.harness.02.md` | [harness.001.006.000](ksdft2effmass.harness.001.006.000.md) | Current contract status and limitations consolidated. |
| `ksdft2effmass.harness.03.md` | [harness.001.003.000](ksdft2effmass.harness.001.003.000.md) | Current Python implementation retained and shortened. |
| `ksdft2effmass.harness.04.md` | [harness.001.002.000](ksdft2effmass.harness.001.002.000.md) | Resource, profile, and skill material consolidated. |
| `ksdft2effmass.harness.05.md` | [harness.001.004.000](ksdft2effmass.harness.001.004.000.md) | Evidence grammar corrected and combined with validation. |
| `ksdft2effmass.harness.06.md` | [harness.001.001.000](ksdft2effmass.harness.001.001.000.md) | Generic/local boundary updated to implemented paths. |
| `ksdft2effmass.harness.07.md` | [harness.090.000.000](ksdft2effmass.harness.090.000.000.md) | Shadow-replay and cutover narrative retained as history. |
| `ksdft2effmass.harness.08.md` | [harness.002.001.009](ksdft2effmass.harness.002.001.009.md) | Extraction-readiness material incorporated into the proposed migration plan. |
