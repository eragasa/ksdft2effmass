# Quantum ESPRESSO

Quantum ESPRESSO is the initial production backend for periodic KS/GKS electronic-structure calculations. The immediate scientific path is semilocal periodic KS for silicon. The project owns neutral periodic specifications/results and concrete QE adapters; it does not reimplement electronic-structure theory.

Prospective capabilities are selected individually:

- `pw.x` SCF;
- `pw.x` NSCF;
- `bands.x` when band ordering or symmetry output is required;
- `projwfc.x` when its specific projector diagnostics are required;
- `pw2wannier90.x` for the QE-to-Wannier90 interface.

Membership in the QE distribution does not make every executable required.

The public Python integration distinguishes four reusable software operations:
`QuantumEspressoScfTask`, `QuantumEspressoNscfTask`,
`QuantumEspressoBandPathTask`, and `QuantumEspressoBandsExtractionTask`. Each
retains an exact QE execution input and delegates through an explicitly injected
plane-wave calculator port. Downstream operations require a mechanically
completed predecessor result with exact native-state lineage. These software
contracts do not select scientific settings, establish numerical convergence, or
authorize a QE executable. `QuantumEspressoSimulation` is the immutable application
composition for one such Task: it binds the Task's equal exact execution input and
identical calculator object together with a separate Workflow dispatch-effect
executor. `LocalQuantumEspressoExecutor` implements that effect port. The composition
does not invoke either boundary or retain a result. DOS remains deferred until its
executable and result boundary is defined.

## SCF, NSCF, and band roles

A `pw.x` SCF calculation iterates the density-dependent Kohn--Sham problem to
determine a converged density and effective potential. An NSCF or band
calculation then holds that parent density and potential fixed while solving the
one-electron eigenproblem on a wavevector set chosen for its output. SCF meshes
serve density and total-energy convergence; NSCF meshes serve integration or
state extraction; symmetry paths serve band-dispersion analysis. Valley,
effective-mass, Wannier, and tight-binding workflows can require different
wavevectors, retained bands, and convergence studies even when they share the
same SCF parent.

The retained QE 7.2 tutorial SCF is a computational-bootstrap case: it verifies
identified execution, artifacts, provenance, QEXSD extraction, units, and
backend availability. Its ten wavevectors and four bands are not a production
silicon band dataset. The maintained bootstrap workflow is
`docs/computational/ksdft2effmass.computational.bootstrap.md`, production Stage
02 is `docs/computational/ksdft2Effmass.computational.02.md`, and the retained
observation is recorded in
`calculations/bulk-silicon/qe-example01-si-scf-davidson/result.md`.

For admitted QEXSD output, `QuantumEspressoObservationAdapter` implements the first
stage of observation adaptation. Callers supply a
`QuantumEspressoParsedDocumentRecord` that binds the exact parsed document to source
content, parser implementation, and parser version; the Workflow artifact manifest
and entry; the intended result identity; and the supported normalization
policy/version. The adapter requires exact agreement between the represented SHA-256
and byte count, parser identity, native format and semantic role, and neutral-record
compatibility. It returns an
immutable `QuantumEspressoExtractedObservationResult` with explicit limitations or a
closed failure that retains the reserved result identity without a partial
observation. This software transformation neither
executes QE nor establishes convergence, numerical verification, or scientific
validation. The selected two-stage architecture requires a separately activated
Workflow Task before this result can be assembled into a Workflow-owned
`NormalizedObservationSet`.

Input mapping, deterministic text serialization, mechanical output/save parsing, result adaptation, execution, and convergence analysis have separate owners. QE execution occurs outside CPN guards through immutable request/result tokens. A process exit, parsed result, converged SCF state, accepted numerical protocol, and scientifically validated result are distinct states.

The immediate path is `semilocal periodic specification -> QE -> PeriodicElectronicStructureDataset -> Wannier90`. Hybrid GKS mapping and execution are deferred; semilocal evidence cannot qualify a hybrid profile. A production QE run does not require a simultaneous ABINIT duplicate.

No QE executable or pseudopotential has been authorized by this architecture pass. Tutorial-derived future cases are interface and parser behavioral references, not numerical oracles. See [Periodic backends](dft-backends.md), [Cross-backend verification](cross-backend-verification.md), [External dependencies](external-dependencies.md), and [Troubleshooting](troubleshooting.md).
