# Architecture v2 control plane

Architecture v2 has two control planes with disjoint state authority.

## Development control plane

The development control plane owns:

- applicable software-development policy;
- `HarnessTask` definitions;
- `DevelopmentTaskSelection`;
- development authorization;
- unresolved development decisions;
- software capabilities;
- software-verification findings; and
- development review state.

It may reference immutable scientific contract identities when implementing or
verifying them. It does not store a `CpnMarking`, calculator execution status,
scientific finding, or `ScientificDisposition`.

## Scientific control plane

The scientific control plane owns:

- the `ScientificService` catalog;
- `Campaign` definitions;
- `CampaignRun` state;
- `Simulation` references;
- execution authorization scoped to exact requests;
- `SimulationExecutionResult` references;
- `ArtifactManifest` lineage;
- `ScientificAnalysis`; and
- `ScientificDisposition`.

It may reference an immutable implementation or software-verification identity
required by a service. It does not activate, complete, or review a
`HarnessTask`.

## Authority isolation

- Evidence supports a claim but does not grant execution authority.
- Catalog membership states capability but does not authorize an effect.
- A CPN enabled transition permits deterministic firing under the campaign
  contract; an external effect additionally requires applicable human and
  resource authority.
- A successful result does not create a scientific disposition.
- A development review does not accept scientific findings.
- A scientific disposition does not accept software changes.

## Explicit context

Repository-sensitive development operations receive an explicit repository root
and operation-specific requirements. Scientific operations receive explicit
calculator configuration, artifact stores, resource ceilings, and request
identity. Ambient current-directory discovery is never authority.

## Capability selection

One running service uses an immutable capability catalog. Calculator selection is
explicit from the typed `Simulation` and configured executor composition. No
runtime registry may mutate available implementations or silently fall back to a
different calculator.

## Human authority

Human authority is represented at the boundary it governs: development
architecture and acceptance in the development plane; protected scientific
execution and scientific disposition in the scientific plane. Human decisions
are not inferred from silence, terminal markings, reviews, or passing checks.
