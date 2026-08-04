# Scientific workflow semantics

## Purpose

This note separates the scientific sequence of model reductions from the stateful computational workflow used to produce and validate evidence.

The displayed operator reduction

$$
\hat H_{\mathrm{KS}}
\longrightarrow
\hat H^{(P)}
\longrightarrow
\mathbf H_{\mathrm W}
\longrightarrow
\mathbf H_{\mathrm{red}}
\longrightarrow
\hat H_{\mathrm{continuum}}
$$

is a mathematical relationship among models and representations. It is not a claim that calculations execute once along a directed acyclic workflow.

## Stateful research workflow

The scientific and computational workflow is represented prospectively as a Colored Petri Net. Its markings may simultaneously contain multiple candidate calculations, accepted parent datasets, failed attempts, retry authorizations, direct-TB and Wannier branches, validation evidence, and blocked downstream requests.

Repeated cutoff, k-point, window, projection, supercell, fitting, and validation iterations are cycles in workflow state. Failures and recovery are first-class. A static dependency diagram may summarize prerequisites or publication logic, but it does not replace the durable marking.

Computational gates are accepted marking predicates. In particular:

- G01a requires accepted computational-foundation and reproducibility capabilities;
- G01b requires accepted composed synthetic scientific workflows;
- G02 requires an accepted bulk-Si SCF parent and bulk-validation evidence;
- Stage 03's Wannier-compatible NSCF child retains the accepted G02 parent manifest identity.

Meeting notes and unmanifested historical calculations cannot create these accepted tokens.

## Parent and branch semantics

One accepted neutral `PeriodicElectronicStructureDataset` supplies a common parent for:

```text
direct spectral/TB reconstruction
Wannier specification and Wannier90 reconstruction
```

Comparison is scientifically admissible only when the branch results carry compatible parent provenance, specification versions, representation metadata, and required validation state. Merely observing two completed computations does not define a common state space or authorize operator comparison.

## Epistemic boundary

A CPN organizes state, authorization, execution evidence, lineage, and acceptance. It does not establish physical truth. External process completion, solver convergence, numerical verification, scientific validation, and uncertainty quantification remain distinct evidence classes.

The integration domain is periodic KS/GKS electronic structure for crystalline solids organized in Bloch fibers. Molecular-orbital and finite-system calculations are outside scope. The authoritative workflow architecture is [`docs/architecture/colored-petri-net-workflows.md`](../architecture/colored-petri-net-workflows.md), and the scientific boundary is [`docs/architecture/periodic-electronic-structure-integration.md`](../architecture/periodic-electronic-structure-integration.md). Operational guidance is under [`docs/user-guide/`](../user-guide/).
