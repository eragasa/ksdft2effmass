# Periodic KS/GKS electronic structure and Quantum ESPRESSO architecture

## Status and scope

The human PI approved the scientific object and adapter architecture on 2026-08-03. A later correction replaces its linear/DAG-like workflow assumption with the stateful project-owned Colored Petri Net in [`colored-petri-net-workflows.md`](colored-petri-net-workflows.md); the human PI granted final acceptance to the corrected architecture through `CPN-HC01` on 2026-08-03. The authoritative domain and extension seams are recorded in [`periodic-electronic-structure-integration.md`](periodic-electronic-structure-integration.md).

The integration domain is periodic KS/GKS electronic structure for crystalline solids with Bloch-band representations suitable for band analysis, TB reduction, and Wannierization. Molecular-orbital and finite-system calculations are outside scope. This document does not define a universal DFT API, implement a public API or schema, authorize a Quantum ESPRESSO or ABINIT run, select a production environment or pseudopotential, accept convergence evidence, or establish scientific validation or uncertainty quantification.

The original bounded A–H scientific decomposition is preserved, but its linear/DAG-like workflow sequencing is prospectively superseded by the P0–P11 Colored Petri Net program in `.pi/tasks/backend-neutral-cpn-workflow-architecture.md` and `.pi/chains/backend-neutral-kohn-sham-qe.chain.json`. P0 is closed as human-accepted `CONDITIONAL_PASS`, and P0A is closed as human-accepted `PASS`. `P1-HC01` Option A and `P1-HC02` Option B are resolved. Final P1 acceptance was granted as Option A through `P1-HC03` on 2026-08-04, after reviews and parent verification; P1 is closed as human-accepted `PASS`. No successor was selected or launched, and P2–P11 and production or scientific execution remain blocked and unauthorized.

## Package ownership

The approved prospective package tree is:

```text
python/src/ksdft2effmass/
├── dft/
│   ├── __init__.py
│   ├── structure.py
│   ├── pseudopotentials.py
│   ├── specifications.py
│   └── datasets.py
├── provenance/
│   ├── __init__.py
│   ├── records.py
│   ├── serialization.py
│   └── verification.py
├── io/
│   ├── quantum_espresso/
│   │   ├── __init__.py
│   │   ├── input.py
│   │   ├── output.py
│   │   └── save.py
│   └── wannier90/                 # introduced only by the approved Wannier task
│       ├── __init__.py
│       ├── input.py
│       └── output.py
├── backends/
│   ├── quantum_espresso/
│   │   ├── __init__.py
│   │   ├── configuration.py
│   │   ├── mapping.py
│   │   ├── execution.py
│   │   ├── artifacts.py
│   │   └── wannier90_bridge.py
│   └── wannier90/                 # separate execution backend
│       ├── __init__.py
│       ├── configuration.py
│       └── execution.py
├── tight_binding/
│   ├── __init__.py
│   └── targets.py
├── wannier/
│   ├── __init__.py
│   ├── specifications.py
│   └── inputs.py
└── operators/                     # existing accepted finite-operator subsystem
```

This is prospective ownership, not authorization to create every listed module at once. No generic backend, runner, serializer, DataObject, ActionObject, or Workflow base class is approved. No `dft/paw.py` is approved.

## Object categories and semantic mapping

### DataObjects

The following are immutable DataObjects where introduced:

- `CrystalStructure`;
- `AtomicSpecies` and `AtomicSite`;
- `PseudopotentialSpecification`, `PseudopotentialSet`, and `PseudopotentialFormalism`;
- `PeriodicElectronicStructurePhysicalSpecification`, `PeriodicElectronicStructureNumericalSpecification`, and `PeriodicElectronicStructureSpecification`;
- `KPointSet` and declared sampling specifications;
- `PeriodicBandStructure`;
- `PeriodicElectronicStructureArtifactSet`;
- `ArtifactReference`, `ArtifactLocation`, and `RunManifest`.

These names cover periodic KS and GKS without implying molecular coverage. Earlier `KohnSham*` names in historical decision records are prospectively corrected by this active contract.

`ArtifactLocation` is deployment metadata rather than scientific identity. Whether it is represented as a DataObject or supplied only through a resolver ActionObject is deferred to the provenance contract task.

### ResultObjects

The following are explicit immutable ResultObjects:

- `PeriodicElectronicStructureDataset`;
- `QuantumEspressoExecutionResult`;
- `SCFConvergenceResult`.

`PeriodicElectronicStructureDataset` is the output of adapting one completed periodic KS/GKS calculation. Construction does not imply solver convergence, numerical-protocol acceptance, backend qualification, scientific validation, or uncertainty quantification.

### ActionObjects

Input and result adaptation have separate owners:

```text
QuantumEspressoInputMapper
    PeriodicElectronicStructureSpecification
    + QuantumEspressoNumericalOptions
    → QuantumEspressoInputRecord

QuantumEspressoInputSerializer
    QuantumEspressoInputRecord
    → deterministic QE input text

QuantumEspressoOutputParser
    native QE output
    → mechanically parsed QE output record

QuantumEspressoSaveParser
    native QE save data
    → mechanically parsed QE save record

QuantumEspressoResultAdapter
    parsed QE output/save records
    + accepted periodic calculation specification
    + execution/manifest identity
    → PeriodicElectronicStructureDataset
```

No object owns both neutral-to-QE input mapping and QE-to-neutral result adaptation. Parsers own no scientific mapping. The serializer owns no scientific choices. Named ActionObjects own conversion, execution, convergence analysis, artifact verification, TB target construction, and Wannier input construction.

## Scientific and numerical conventions

Direct-lattice vectors are rows:

$$
C=
\begin{pmatrix}
\mathbf a_1^{\mathsf T}\\
\mathbf a_2^{\mathsf T}\\
\mathbf a_3^{\mathsf T}
\end{pmatrix}.
$$

The reciprocal-lattice rows are

$$
B=2\pi C^{-\mathsf T},
\qquad
CB^{\mathsf T}=2\pi I.
$$

Approved neutral conventions are:

```text
length unit                 Å
energy unit                 eV
QE plane-wave cutoff input  Ry
site coordinates            fractional direct-lattice coordinates
primary k-point coordinates fractional reciprocal coordinates
neutral band index          zero based
band-array axes             (spin, k, band)
Fourier phase               exp(+i k·R)
```

The QE result adapter retains source conventions and performs named, documented conversion into these neutral conventions. Occupation capacity and spin degeneracy are explicit metadata. The initial scientific scope proposed for validation is non-spin-polarized bulk silicon. The architecture may represent future spin modes but does not claim their implementation or validation.

The accepted `operators.Geometry` remains finite-operator representation metadata and is not the full `CrystalStructure`. Conversion between them requires an explicit future ActionObject where their contracts are compatible.

## Common periodic electronic-structure result boundary

`PeriodicElectronicStructureDataset` version 1 contains compact, immutable:

- dataset identity and schema version;
- physical-, numerical-, and pseudopotential-set identities;
- realized `CrystalStructure`;
- reciprocal convention and `KPointSet`;
- spin and relativistic convention;
- zero-based band indices;
- eigenvalues and occupations with axes `(spin, k, band)`;
- electron count;
- Fermi-level or chemical-potential representation;
- energy unit and energy-zero convention;
- optional symmetry metadata;
- source manifest identity;
- `PeriodicElectronicStructureArtifactSet`.

Compact arrays must be defensively owned and operationally immutable. Large data remain sealed external artifacts referenced by identity:

- charge density;
- wavefunctions;
- QE `.save` trees;
- FFT grids;
- restart state;
- Wannier bridge files.

Version 1 contains no generic operator matrices or spectral projectors. Eigenvalues alone are not a complete operator representation. Density and wavefunction artifacts are not called backend-neutral merely because a neutral record references them.

## Artifact identity, location, and provenance

Portable content identity and deployment location are separate:

```text
ArtifactReference
    artifact_id
    logical_path
    sha256
    byte_size
    format
    semantic_role
    retention_policy
    producer_manifest_id

ArtifactLocation
    artifact_id
    storage_uri
```

Checksums and sizes define verified content identity. `logical_path` records a stable role inside a run or campaign. A storage URI may change without changing scientific identity. Portable manifests do not use local absolute paths as identities. Pseudopotential source URIs are provenance metadata, not artifact identities. Storage technology remains deferred.

`provenance.records` is foundational and imports no DFT, QE, TB, Wannier, or operator module. A manifest uses opaque preallocated identities and does not embed its own checksum-bearing artifact reference. Environment capture is sanitized and allowlisted; secrets and unrestricted environment dictionaries are prohibited. Retention policy is metadata and never deletion authority.

## Static Python import dependency direction

```text
dft.structure ─────────────────────┐
dft.pseudopotentials ──────────────┼→ dft.specifications
provenance.records ────────────────┘          │
                                              ↓
                                         dft.datasets

io.quantum_espresso ───────────────────────────────┐
dft.specifications + dft.datasets ────────────────┼→ backends.quantum_espresso.mapping
provenance.records ────────────────────────────────┘

io.quantum_espresso + provenance.records
    → backends.quantum_espresso.execution

dft.datasets → tight_binding.targets
dft.datasets → wannier.specifications / wannier.inputs

dft.datasets + provenance.records + QE mechanical records
    → backends.quantum_espresso.wannier90_bridge
    → wannier.inputs

io.wannier90 → backends.wannier90
```

Additional constraints:

- `dft.structure` imports no provenance or backend package.
- `dft.pseudopotentials` may refer only to a narrow portable artifact identity.
- `dft.specifications` composes structure and pseudopotential objects.
- `dft.datasets` may retain manifest and artifact foreign keys.
- concrete QE mapping imports DFT, provenance, and QE mechanical records.
- the neutral periodic electronic-structure domain imports no QE package.
- TB and Wannier packages import neutral datasets and never QE I/O.
- provenance imports no DFT or downstream domain.
- the existing operator package does not absorb general run provenance or QE artifacts.

This is a static import-direction constraint, not the scientific or computational workflow model. Static imports remain acyclic where practical: provenance and the structure/pseudopotential records are parallel foundations; the only import convergence is in specifications/datasets and concrete adapters. There is no provenance-to-DFT return edge.

The scientific/computational workflow is the stateful project-owned Colored Petri Net defined in [`colored-petri-net-workflows.md`](colored-petri-net-workflows.md). It supports multiset markings, guarded transitions, independent branches, synchronization, retries, failure/recovery, repeated convergence iterations, durable provenance, parent-child runs, and accepted/rejected/failed/blocked states.

## Pseudopotential and PAW scope

Version 1 may represent:

```text
PseudopotentialFormalism
    NORM_CONSERVING
    ULTRASOFT
    PAW
```

Core treatment, electronic-structure theory, numerical representation, backend identity, and available products are independent axes. PAW is a formalism/capability, not a backend, integration hierarchy, or universal base class; no generic `PAWCalculator` is authorized. Representation does not claim execution support.

For PAW,

$$
|\psi_{n\mathbf k}\rangle
=
\hat{\mathcal T}|\widetilde{\psi}_{n\mathbf k}\rangle.
$$

Auxiliary smooth and reconstructed all-electron Bloch states remain distinct declared wavefunction representations. Projector coefficients, augmentation information, Wannier overlaps, and Wannier projections remain distinct semantic product roles, with separately declared availability. The first validated pseudopotential execution lane remains unresolved until the actual Si artifact, checksum/provenance, formalism, XC compatibility, relativistic treatment, and intended Wannier workflow are audited. Detailed representation and paired-backend matching rules are in [`periodic-electronic-structure-integration.md`](periodic-electronic-structure-integration.md).

## Downstream fan-out

The approved fan-out is:

```text
PeriodicElectronicStructureDataset
├── TightBindingTargetBuilder
└── WannierizationInputBuilder
```

The initial direct branch is **direct spectral DFT-to-TB fitting**. It is not operator fitting without an explicit common operator representation.

The Wannier branch additionally consumes retained wavefunction artifacts and the QE–Wannier bridge products `.nnkp`, `.amn`, `.mmn`, and `.eig`. `wannier90.x -pp` creates `.nnkp`; `pw2wannier90.x` creates the QE-to-Wannier interface outputs; Wannier90 execution remains a separate backend. Bridge filenames, QE prefixes, and output directories do not become fields of the neutral scientific core.

## Computational gate correction

Historical `G01` evidence is preserved. The old unsplit gate is superseded prospectively by:

```text
G01a — computational foundation
    specifications
    provenance and manifests
    common metrics required by early calculation validation
    synthetic execution and parser infrastructure

G01b — composed synthetic scientific workflows
    basis/state-space alignment
    composed reduction paths
    later synthetic end-to-end evidence
```

`G02` depends on accepted `G01a`, not `G01b`, and does not depend on basis or gauge alignment. `G01b` alignment work depends on the accepted operator-record foundation and the required metrics. This removes the former `G01 → alignment → G01` cycle without rewriting historical records.

`G02` owns the accepted SCF parent and path/diagnostic NSCF calculations needed for bulk validation. Stage 03 owns the Wannier-compatible uniform-grid NSCF child after retained bands, outer and inner windows, and the uniform grid are approved. The Stage 03 child references the accepted G02 SCF parent manifest. G02 does not predict an unknown Wannier grid.

## PhysKit decision

The approved policy is:

```text
contractual reimplementation
no PhysKit runtime dependency
no new shared package
```

Only focused k-path interpolation logic may later be adapted, and only after source, convention, typing, test, and license review. Any adaptation must retain the PhysKit repository URL, exact source commit, source path, MIT notice, adaptation description, and repository-native tests. This architecture task copies no PhysKit code.

## Superseded A–H sequence and CPN task program

A–H preserve the useful decomposition into contract, provenance, neutral DFT, QE mechanics, QE semantics/execution, direct TB, and Wannier work. They were never launched. Their workflow sequencing is prospectively superseded by P0–P11:

```text
P0  SNAKES and documentation-tooling preflight
P1  project-owned CPN contract
P2  provenance and external-tool capability records
P3  SNAKES adapter and project-owned marking persistence
P4  neutral periodic electronic-structure structures/specifications/datasets
P5  QE mechanical I/O and immutable execution boundary
P6  QE semantic adapter and SCF-validation subnet
P7  direct spectral/TB fan-out subnet
P8  Wannier specification and QE-to-Wannier90 bridge
P9  Wannier90 execution/result-adaptation subnet
P10 synthetic composed workflow verification
P11 human-authorized bulk-Si campaign
```

Every task has its own evidence, tests where implementation exists, documentation, independent review, parent verification, and human acceptance. No task begins automatically from a predecessor's acceptance.

## Production authorization checkpoint

Synthetic rendering, parsing, and command-executor fixtures are permitted within approved tasks before a production checkpoint. Before any real QE run, a separate human authorization checkpoint must record:

- machine or cluster;
- QE version and executable identity;
- exact pseudopotential artifact;
- resource request;
- working and artifact roots;
- expected runtime;
- retained outputs;
- data-transfer policy.

Absent that checkpoint, no local, remote, cluster, cloud, or HPC QE execution is authorized.

## Validation boundaries

Software verification of constructors, rendering, parsing, adapters, manifests, import direction, and synthetic execution does not establish numerical convergence or scientific validity. Numerical verification of coordinate conversions or analytical algorithms does not establish bulk-Si validation. Scientific validation and uncertainty quantification require separate approved evidence. Process completion, SCF convergence, numerical-protocol acceptance, and scientific-validation acceptance remain distinct states.
