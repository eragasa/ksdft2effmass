# Periodic electronic-structure integration

## Status and authority

This page records a bounded correction to the prospective electronic-structure
integration architecture. The human PI granted final acceptance through `CPN-HC01` on 2026-08-03. It preserves the accepted stateful Colored Petri Net
(CPN), pure guards, two-phase request/result execution, failure/retry semantics,
provenance-aware tight-binding (TB)/Wannier fan-out, SNAKES isolation, and
project-owned persistence boundary.

This is architecture only. Quantum ESPRESSO (QE) remains the initial production
backend. Hybrid generalized Kohn–Sham (GKS) support and ABINIT conformance work
are planned and deferred. No backend integration, dependency, serializer, test,
fixture, or calculation is implemented or authorized here.

## Scientific domain boundary

The approved integration domain is:

> periodic KS/GKS electronic-structure calculations for crystalline solids that
> produce Bloch-band representations suitable for band analysis, tight-binding
> reduction, and Wannierization.

For a periodic crystal, the one-particle operator decomposes schematically into
Bloch fibers,

$$
\hat H
\cong
\int_{\mathrm{BZ}}^\oplus
\hat H(\mathbf k)\,\mathrm d\mathbf k,
$$

where $\mathrm{BZ}$ is the Brillouin zone and $\mathbf k$ labels a Bloch fiber.
The neutral contract therefore owns periodic concepts including:

- direct and reciprocal lattices;
- Brillouin-zone conventions;
- $k$-points, paths, meshes, shifts, weights, and coordinate conventions;
- Bloch-band indices, eigenvalues, and occupations;
- energy-reference metadata;
- spin channels and relativistic treatment;
- convergence evidence;
- pseudopotential or projector-augmented-wave (PAW) provenance;
- downstream representation capabilities.

Molecular-orbital and finite-system calculations are outside the current
domain. The architecture is not a universal DFT API, does not cover all
Kohn–Sham implementations, and does not claim coverage of all PAW
implementations. In particular, it does not authorize an ORCA adapter or any
molecular quantum-chemistry package.

## Prospective neutral object names

The active prospective contract uses domain-accurate names:

```text
PeriodicElectronicStructureSpecification
PeriodicElectronicStructurePhysicalSpecification
PeriodicElectronicStructureNumericalSpecification
PeriodicElectronicStructureDataset
PeriodicBandStructure
PeriodicElectronicStructureArtifactSet
```

`PeriodicElectronicStructureSpecification` is the calculation-level composition of explicit physical and numerical specification facets; the names do not collapse their validation or ownership boundaries.

These names replace the overly broad or semilocal-only prospective names
`KohnShamSpecification`, `KohnShamDataset`, `KohnShamBandStructure`, and
`KohnShamArtifactSet`. Historical architecture and review records may retain old
names as chronology, but new public contracts must use the periodic names unless
a future stored contract genuinely supports periodic KS, periodic GKS,
molecular, and finite-system calculations without misleading or empty fields.
No such broader contract is approved now.

`PeriodicElectronicStructureDataset` is an immutable ResultObject. Its
construction does not imply SCF convergence, numerical-protocol acceptance,
backend qualification, scientific validation, or uncertainty quantification.

## Independent architectural axes

The integration domain is not a hierarchy of `DFT -> PAW -> QE`. The neutral
contract records independent axes:

```text
System domain:
    periodic crystal

Boundary conditions:
    periodic

State organization:
    Bloch fibers

Electronic-structure operator class:
    Kohn–Sham
    generalized Kohn–Sham

Method/functional identity:
    exact functional and method profile

Core treatment:
    norm-conserving pseudopotential
    ultrasoft pseudopotential
    PAW
    future all-electron comparison

Numerical representation:
    plane waves
    future real-space grid
    future compatible representations

Backend implementation:
    Quantum ESPRESSO
    deferred ABINIT conformance adapter

Available products:
    SCF state
    band path
    uniform-grid NSCF data
    densities
    projectors
    Wannier overlaps and projections
```

PAW is a core-treatment formalism and a set of representation capabilities. It
is not a backend, the integration hierarchy, or a universal base class. A
generic `PAWCalculator` superclass is not authorized. Norm-conserving and
ultrasoft pseudopotential calculations remain representable independently of
PAW.

## Directional integration boundary

The long-term objective is:

> an extensible integration layer for periodic KS/GKS electronic-structure
> backends, initially centered on PAW and pseudopotential calculations.

The boundary is directional:

```text
neutral periodic specification
    -> capability negotiation
    -> backend-specific mapping
    -> backend-specific serialization
    -> immutable execution request

backend artifacts
    -> backend-specific parser
    -> semantic result adapter
    -> neutral periodic dataset
```

The neutral contract contains no QE or ABINIT variable names. Backend-specific
variables, file syntax, execution settings, and parsing mechanics remain owned
by concrete backend adapters. No bidirectional QE-to-other-backend semantic
translator is authorized, and no empty package is created for a future backend.

Downstream consumers depend on neutral capabilities rather than backend names:

```text
PeriodicElectronicStructureDataset
├── direct spectral/TB reconstruction
└── Wannierization preparation
```

The two branches retain their common neutral parent and manifest. Their join
still requires compatible specification versions, representations, energy
conventions, pseudopotential provenance, artifact lineage, and accepted branch
states.

## KS and planned GKS methods

The currently selected semilocal calculations may continue to use accurate
historical notation such as $\hat H_{\mathrm{KS}}$. The neutral architecture
must not make periodic GKS parents impossible.

A hybrid GKS operator is represented schematically by

$$
\hat H_{\mathrm{GKS}}
=
\hat T
+
\hat V_{\mathrm{ext}}
+
\hat V_{\mathrm H}
+
\hat V_{\mathrm{xc}}^{\mathrm{local}}
+
\alpha\hat V_{\mathrm x}^{\mathrm{Fock}},
$$

where $\alpha$ is the exact-exchange fraction. Range-separated hybrids may also
require a range-separation parameter $\omega$.

Prospective method categories are:

```text
SEMILOCAL_KS
GLOBAL_HYBRID_GKS
SCREENED_HYBRID_GKS
RANGE_SEPARATED_HYBRID_GKS
```

Prospective capability profiles are:

```text
PERIODIC_SEMILOCAL_KS_V1
PERIODIC_GLOBAL_HYBRID_GKS_V1
PERIODIC_SCREENED_HYBRID_GKS_V1
PERIODIC_RANGE_SEPARATED_HYBRID_GKS_V1
```

These categories and profiles are planning concepts, not implemented enums or
runtime capabilities. A future hybrid specification must distinguish:

- exact functional identity;
- exact-exchange fraction;
- screening or range-separation form;
- $\omega$ where applicable;
- spin treatment;
- pseudopotential compatibility;
- backend-specific numerical implementation;
- convergence and execution policy.

Hybrid dependencies, serializers, tests, backend option classes, CPN
implementation, and support claims remain deferred. Semilocal qualification
must never be presented as hybrid qualification. DFT+$U is not assigned a method profile by this correction and no current support claim is made for it.

## PAW representation semantics

The PAW transformation is

$$
|\psi_{n\mathbf k}\rangle
=
\hat{\mathcal T}
|\widetilde{\psi}_{n\mathbf k}\rangle,
$$

where $|\widetilde{\psi}_{n\mathbf k}\rangle$ is an auxiliary smooth Bloch
state and $|\psi_{n\mathbf k}\rangle$ is the reconstructed all-electron Bloch
state. The architecture distinguishes these states from projector coefficients,
augmentation information, Wannier overlap matrices, and Wannier projection
matrices.

Every future wavefunction-like artifact must declare its representation.
Prospective mixed artifact representation, semantic-role, and availability categories are:

```text
AUXILIARY_PSEUDO
PAW_RECONSTRUCTED
PROJECTOR_COEFFICIENTS
WANNIER_OVERLAP_MATRICES
WANNIER_PROJECTION_MATRICES
NOT_AVAILABLE
```

These are prospective artifact representation/semantic-role categories, not all wavefunction representations: `AUXILIARY_PSEUDO` and `PAW_RECONSTRUCTED` identify wavefunction representations; projector and Wannier matrix values identify distinct product roles; `NOT_AVAILABLE` records absence. A future contract may separate these into representation, semantic-role, and availability fields. This correction does not introduce a generic wavefunction DataObject. Artifacts in different categories must not be compared or substituted as though they were identical.

## Deferred ABINIT conformance backend

ABINIT is the planned secondary conformance backend. Its role is:

```text
software verification of the neutral input/output abstractions
+
bounded cross-backend numerical verification
```

ABINIT is not an oracle, a production calculator required for every campaign, a
mandatory duplicate of every QE run, an initial complete Wannier pipeline,
scientific truth, or a replacement for experiment or future all-electron
validation. QE remains the initial production backend.

The first future ABINIT implementation is deliberately narrow:

- tutorial-derived semilocal SCF cases;
- one periodic silicon case;
- neutral specification mapping;
- deterministic input serialization;
- output parsing;
- neutral dataset adaptation;
- capability reporting;
- selected paired numerical comparisons.

It is deferred until after the first accepted end-to-end dopant result. No
ABINIT dependency, module, test, fixture, or execution is authorized now.

## Paired-backend conformance architecture

Future QE and ABINIT cases derive independently from one neutral periodic parent:

```text
one neutral periodic specification
├── QE mapper
│   -> QE tutorial-equivalent execution
│   -> QE parser
│   -> neutral periodic dataset
└── ABINIT mapper
    -> ABINIT tutorial-equivalent execution
    -> ABINIT parser
    -> neutral periodic dataset
```

QE input is never translated directly into ABINIT input. The common parent
records, where applicable:

- crystal lattice and coordinate convention;
- atomic species and positions;
- periodic boundary conditions;
- exchange-correlation specification;
- charge and spin treatment;
- relativistic treatment;
- pseudopotential requirements;
- $k$-point mesh, shifts, path, weights, and conventions;
- band count;
- occupation and smearing intent;
- SCF convergence intent;
- requested observables.

Backend-specific variables remain backend-owned.

Upstream tutorials are behavioral references, not numerical oracles. The future
corpus has three evidence layers:

```text
Layer 1:
    retained tutorial-output parser fixtures
    classification: software verification

Layer 2:
    bounded tutorial-equivalent executable cases
    classification: software verification (integration evidence)

Layer 3:
    matched and independently converged paired cases
    classification: numerical verification
```

Scientific validation remains separate. Every imported future tutorial fixture
must record the source project, tutorial identifier and URL, upstream version or
revision, retrieval date, license and attribution, original checksum, local
modifications, convergence status, and permitted VVUQ classification. No
tutorial files are copied by this architecture correction.

## Pseudopotential matching for paired comparisons

Future paired comparisons classify pseudopotential matching as:

```text
EXACT_ARTIFACT
    Both backends officially support the same checksummed artifact with the
    same semantics.

COMMON_GENERATION_LINEAGE
    Backend-specific artifacts share generator, generation inputs, XC
    functional, valence configuration, relativistic treatment, and core model.

MATCHED_PHYSICAL_SPECIFICATION
    Artifacts are not identically generated but have explicitly matched
    physical characteristics.

UNMATCHED
    Pseudopotential differences materially confound the numerical comparison.
```

`EXACT_ARTIFACT` is preferred only where both backends genuinely support the
same artifact with the same semantics. Otherwise
`COMMON_GENERATION_LINEAGE` is preferred, potentially with a common
norm-conserving generation lineage and backend-specific formats.

Two pseudopotentials are not identical merely because they represent the same
element, use the same exchange-correlation functional, are both PAW, or are both
norm-conserving. A future named pseudopotential-conformance ActionObject must own this relational classification and return a structured immutable result with evidence identities and confounding limitations; it is not an intrinsic invariant of either artifact. `MATCHED_PHYSICAL_SPECIFICATION` does not imply numerical equivalence. No pseudopotential family is selected here; selection remains a later human scientific decision.

## Prospective CPN backend semantics

The concrete QE production subnet remains unchanged. Prospective token concepts
for future conformance work specialize the approved external-tool lifecycle with concrete backend payloads; they do not create a parallel token hierarchy, plugin registry, or generic backend framework:

```text
BackendIdentityToken
BackendCapabilityToken
BackendQualificationToken
BackendExecutionRequestToken
BackendExecutionResultToken
NeutralPeriodicDatasetToken
UnsupportedCapabilityToken
BackendDisagreementToken
```

A future `BackendQualificationToken` is scoped by at least:

- neutral specification-schema version;
- neutral dataset-schema version;
- backend identity and executable version;
- adapter version;
- method profile;
- pseudopotential lineage;
- numerical-verification protocol.

It must not collapse qualification to a Boolean such as `qualified=True`.

A future paired-backend qualification subnet may fan one neutral parent into QE
and ABINIT mappings, collect independently adapted neutral datasets, classify
unsupported capabilities, and emit structured disagreement evidence. It remains
outside the prospective QE production path. A production QE run never requires a
simultaneous ABINIT duplicate.

Representative periodic CPN places include:

```text
periodic_electronic_structure_specification_ready
periodic_electronic_structure_dataset_accepted
```

The corresponding QE adaptation transition is:

```text
adapt_qe_result_to_periodic_dataset
```

The existing pure-guard and two-phase execution policies apply unchanged to
future backend work.

## Implementation staging

The immediate scientific path remains:

```text
semilocal periodic specification
    -> Quantum ESPRESSO
    -> neutral periodic electronic-structure dataset
    -> Wannier90
    -> aligned bulk and dopant operators
    -> impurity operator
    -> reduced impurity model
    -> effective-mass comparison
```

Staging is:

```text
Current architecture:
    CPN and periodic electronic-structure extension seams

Near-term scientific objective after separately authorized prerequisite tasks:
    QE semilocal dopant pipeline

After the first accepted end-to-end dopant result:
    minimal ABINIT conformance adapter
    paired QE–ABINIT VVUQ
    reusable periodic-backend conformance kit composed from concrete adapters, fixtures, and evidence contracts (not a plugin framework or superclass)
    additional PAW/pseudopotential adapters
    hybrid GKS implementation and VVUQ
```

The post-dopant work has status `deferred` and launch condition `accepted
end-to-end dopant result`. Before launch, a separate human-approved deferred task must map that phrase to an explicit accepted CPN marking and evidence set. This architecture does not alter P0–P11 to make that mapping.
Broad backend generalization must not delay the immediate QE semilocal path.

Before any public claim of demonstrated backend neutrality, the deferred ABINIT
conformance evidence must exist and pass its declared reviews. Architecture
designed for multiple backends is not equivalent to multiple backends
implemented and verified.

## Explicit exclusions

This correction does not authorize ORCA or molecular quantum chemistry, a
universal DFT API, hybrid execution, ABINIT execution, GPAW integration,
all-electron integration, Hartree–Fock as a separate domain, MP2, coupled
cluster, configuration interaction, GW, BSE, DMFT, production source or test
changes, external dependencies, or real calculations.
