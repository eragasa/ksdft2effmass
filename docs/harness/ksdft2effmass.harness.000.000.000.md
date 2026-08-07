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

The current implementation and the simplification proposal are deliberately
separate below. Pages marked **Proposed** describe future architecture only; they
are not implemented or accepted contracts.

## Document hierarchy

| Document | Task identity | Title | Status | Sphinx |
|---|---|---|---|---|
| [harness.001.000.000](./ksdft2effmass.harness.001.000.000.md) | `harness-current` | Current harness architecture | Current | Included |
| [harness.001.010.000](./ksdft2effmass.harness.001.010.000.md) | `harness-current.boundaries` | Generic and project-local boundaries | Current | Included |
| [harness.001.020.000](./ksdft2effmass.harness.001.020.000.md) | `harness-current.resources` | Resources, profiles, and skills | Current | Included |
| [harness.001.030.000](./ksdft2effmass.harness.001.030.000.md) | `harness-current.python` | Python implementation | Current | Included |
| [harness.001.040.000](./ksdft2effmass.harness.001.040.000.md) | `harness-current.evidence` | Validation and evidence | Current | Included |
| [harness.001.050.000](./ksdft2effmass.harness.001.050.000.md) | `harness-current.agents` | Agent and ownership inventory | Current | Excluded |
| [harness.001.060.000](./ksdft2effmass.harness.001.060.000.md) | `harness-current.status` | Current status and limitations | Current | Included |
| [harness.010.000.000](./ksdft2effmass.harness.010.000.000.md) | `harness-simplification` | Harness simplification proposal | Proposed | Excluded |
| [harness.010.010.000](./ksdft2effmass.harness.010.010.000.md) | `harness-simplification.state` | Unified state model | Proposed | Excluded |
| [harness.010.020.000](./ksdft2effmass.harness.010.020.000.md) | `harness-simplification.evidence` | Extractable evidence subsystem | Proposed | Excluded |
| [harness.010.030.000](./ksdft2effmass.harness.010.030.000.md) | `harness-simplification.agents` | Durable agent architecture | Proposed | Excluded |
| [harness.010.040.000](./ksdft2effmass.harness.010.040.000.md) | `harness-simplification.execution` | Maintained execution interface | Proposed | Excluded |
| [harness.010.050.000](./ksdft2effmass.harness.010.050.000.md) | `harness-simplification.migration` | Incremental migration plan | Proposed | Excluded |
| [harness.090.000.000](./ksdft2effmass.harness.090.000.000.md) | `harness-history` | Historical documentation index | Historical | Excluded |

## Authority boundary

Maintained documentation explains architecture and contributor practice. Mutable
authorization and operational state remain in their owning repository records.
Historical evidence records previous conditions and does not govern current work.
A proposed page cannot activate implementation or replace an accepted contract.

## Historical migration

| Previous document | Current document | Disposition |
|---|---|---|
| `ksdft2effmass.harness.00.md` | [harness.000.000.000](./ksdft2effmass.harness.000.000.000.md) | Replaced by the coordinate-based root index. |
| `ksdft2effmass.harness.01.md` | [harness.001.000.000](./ksdft2effmass.harness.001.000.000.md) | Updated from prospective boundaries to the current architecture. |
| `ksdft2effmass.harness.02.md` | [harness.001.060.000](./ksdft2effmass.harness.001.060.000.md) | Current contract status and limitations consolidated. |
| `ksdft2effmass.harness.03.md` | [harness.001.030.000](./ksdft2effmass.harness.001.030.000.md) | Current Python implementation retained and shortened. |
| `ksdft2effmass.harness.04.md` | [harness.001.020.000](./ksdft2effmass.harness.001.020.000.md) | Resource, profile, and skill material consolidated. |
| `ksdft2effmass.harness.05.md` | [harness.001.040.000](./ksdft2effmass.harness.001.040.000.md) | Evidence grammar corrected and combined with validation. |
| `ksdft2effmass.harness.06.md` | [harness.001.010.000](./ksdft2effmass.harness.001.010.000.md) | Generic/local boundary updated to implemented paths. |
| `ksdft2effmass.harness.07.md` | [harness.090.000.000](./ksdft2effmass.harness.090.000.000.md) | Shadow-replay and cutover narrative retained as history. |
| `ksdft2effmass.harness.08.md` | [harness.010.050.000](./ksdft2effmass.harness.010.050.000.md) | Extraction-readiness material incorporated into the proposed migration plan. |
