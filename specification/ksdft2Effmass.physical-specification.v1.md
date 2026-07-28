# Physical Reference Specification v1

Task: `ksdft2Effmass.computational.01.01.01`
Artifact: `PhysicalSpecification-v1`
Scope: pristine bulk silicon, substitutional phosphorus in silicon, and substitutional boron in silicon.

This document freezes the **physical parent problems** used by downstream Kohn--Sham, projection, Wannier, alignment, impurity-extraction, lattice-reduction, and continuum-reduction tasks. It intentionally does **not** specify plane-wave cutoffs, charge-density cutoffs, $k$-point meshes, convergence tolerances, eigensolver settings, or production input files; those are numerical approximations for `01.01.02`.

## Status labels

| Status | Meaning |
|---|---|
| Frozen | Adopted by this specification and available to downstream tasks. |
| Proposed | Technically recommended here but requiring PI review before production calculations or claims. |
| Blocking | Scientifically consequential choice that must be explicitly approved or revised before the affected downstream physical branch can proceed. |

## Program boundary

The immediate two-month bulk-silicon pilot is the pristine-Si path from a Kohn--Sham reference through a bulk Wannier Hamiltonian to an orthogonal $sp^3s^*$ tight-binding reduction. It supports `G02`, `G03`, `G04`, and paper path `P01`/`P02`-type bulk claims.

The complete dopant program extends the same parent physical conventions to substitutional P:Si and B:Si supercells, aligns pristine and doped projected Wannier operators, extracts impurity operators, reduces them through nested local/nonlocal model classes, and later tests continuum donor/acceptor descriptions. Dopant branches must remain compatible with the approved bulk-pilot parent choices, but unresolved dopant-specific choices do not block the pristine-bulk `G02`--`G04` pilot path.

## Parent physical problems

### 1. Pristine bulk silicon

The bulk parent problem is a periodic Kohn--Sham DFT calculation for crystalline silicon in the diamond structure. It defines the host lattice, band-edge reference, target subspace, and bulk operator consumed by all later Wannier, tight-binding, alignment, and impurity tasks.

### 2. Substitutional phosphorus in silicon

The phosphorus parent problem is a periodic silicon supercell in which one Si atom is replaced by P at a substitutional diamond-lattice site. The primary v1 branch is neutral P$_\mathrm{Si}^0$, which has an odd valence-electron count and is treated with a collinear spin-polarized, scalar-relativistic, non-SOC Kohn--Sham calculation. A neutral donor calculation contains both the extra electron and the positively charged donor core relative to Si; the ionized-donor-core potential relevant to screened-Coulomb effective-mass models must therefore be obtained by a stated interpretation or controlled branch, not by silently relabeling the neutral supercell as an ionized defect. Charged P$_\mathrm{Si}^{+}$ is deferred to a separately specified controlled branch. The extracted object is the P-induced projected impurity operator after common-space and energy alignment to a matched pristine supercell.

### 3. Substitutional boron in silicon

The boron parent problem is a periodic silicon supercell in which one Si atom is replaced by B at a substitutional diamond-lattice site. The primary v1 branch is neutral B$_\mathrm{Si}^0$, which has an odd valence-electron count. For final acceptor and continuum claims, B:Si uses a fully relativistic, noncollinear spinor Kohn--Sham calculation with SOC. A scalar-relativistic non-SOC B:Si calculation may be retained only as an early method-development branch. Charged B$_\mathrm{Si}^{-}$ is deferred to a separately specified controlled branch.

## Physical decisions and validation record

| Decision | Selected value | Physical justification | Computational consequence | Shared by bulk and dopant systems? | Downstream tasks affected | Status |
|---|---|---|---|---|---|---|
| Parent electronic-structure theory | Self-consistent Kohn--Sham DFT within the Born--Oppenheimer fixed-ion framework. | Existing research notes define the parent operator as the converged Kohn--Sham one-particle operator, not a many-body excitation Hamiltonian. | All reductions measure fidelity to the chosen Kohn--Sham parent, not to the exact quasiparticle spectrum or experiment. | Yes. | All stages, especially `02`, `03`, `05`--`10`. | Frozen |
| Material system | Silicon host; dopants limited to substitutional P and substitutional B. | This is the declared initial application and avoids scope expansion to other defects/materials. | Supercell generation and operator metadata need only encode pristine Si, P:Si, and B:Si in v1. | Yes. | `02`, `06`, `07`, `08`, `09`. | Frozen |
| Exchange-correlation approximation | PBE GGA for the v1 parent reference. | PBE is the approved semilocal solid-state baseline with compatible PseudoDojo ONCV pseudopotentials. The project tests operator reductions relative to the DFT parent; PBE band-gap error must be reported as parent-model error, not reduction error. | Produces a reproducible semilocal Kohn--Sham parent but underestimates the Si gap; numerical convergence and validation tolerances must be relative to this parent. | Yes; changing XC between bulk and doped systems invalidates direct impurity-operator subtraction. | `01.01.02`, `02`, `03`, `04`, `06`, `07`, `08`, `09`. | Frozen |
| Pseudopotential family | Optimized norm-conserving Vanderbilt pseudopotentials from one PseudoDojo PBE standard table; use UPF files from the same released table for Si, P, and B. | A common PBE ONCV source table fixes the electron--ion representation so impurity differences are physical dopant perturbations rather than pseudopotential-family artifacts. | `01.01.02` must select and record the exact release, UPF filenames, versions, SHA-256 hashes, suggested cutoffs, converged cutoffs, and Quantum ESPRESSO compatibility. These details do not block entry into `01.01.02`. | Yes; Si, P, and B must use UPF files from the same released PseudoDojo PBE standard table. | `01.01.02`, `02.01.01`, `06.01.01`, `07.01.01`. | Frozen |
| Si valence configuration | Si $3s^2 3p^2$ with frozen core. | These are the chemically active valence states for tetrahedral silicon bonding. | Determines electron count, occupied bands, and valence basis content; semicore-free Si keeps the parent problem focused. | Yes wherever Si appears. | `01.01.02`, `02`, `03`, `06`, `07`. | Frozen |
| P valence configuration | P $3s^2 3p^3$ with frozen core. | Captures the extra group-V valence electron responsible for donor behavior relative to Si. | Neutral P:Si supercells contain one additional valence electron relative to the replaced Si site and therefore have an odd total valence-electron count for any supercell containing an integer number of Si primitive cells. | Applies to P:Si branch and any P-specific comparison. | `06`, `08-P`, `09-P`. | Frozen |
| B valence configuration | B $2s^2 2p^1$ with frozen core. | Captures the group-III acceptor valence deficiency relative to Si. | Neutral B:Si supercells contain one fewer valence electron relative to the replaced Si site and therefore have an odd total valence-electron count for any supercell containing an integer number of Si primitive cells. | Applies to B:Si branch and any B-specific comparison. | `07`, `08-B`, `09-B`. | Frozen |
| Bulk relativistic and spin treatment | Immediate pristine-Si bulk pilot: scalar-relativistic, non-SOC, non-spin-polarized parent. | Scalar-relativistic non-SOC treatment is sufficient for the first pristine-Si operator-reduction pilot, and pristine diamond-structure Si is nonmagnetic in this parent problem. | Keeps the bulk pilot spinless, keeps spin degeneracy implicit, and avoids spinor Wannier/TB bookkeeping in `G02`--`G04`. | This approved bulk branch is the host reference for matching scalar-relativistic non-SOC method-development dopant branches. | `02`, `03`, `04`. | Frozen |
| P:Si relativistic and spin treatment | Primary P:Si branch: neutral P$_\mathrm{Si}^0$, scalar-relativistic, collinear spin-polarized, non-SOC. A non-spin-polarized fractional-occupation calculation may be retained only as a controlled ensemble or method-development branch. | Neutral P:Si has an odd valence-electron count and represents a donor electron bound to/screening the donor core; the physical baseline must not hide this open-shell character in a non-spin-polarized default. SOC is excluded from the primary P:Si branch. | Requires spin-labeled occupations and operator metadata for the P branch; the non-spin-polarized fractional-occupation branch cannot be used as the primary physical branch. | Must be compared to a compatible bulk reference with documented spin/SOC conventions. | `06`, `08-P`, `09-P`. | Frozen |
| B:Si relativistic and spin treatment | Primary B:Si branch: neutral B$_\mathrm{Si}^0$. For final acceptor and continuum claims, use a fully relativistic, noncollinear spinor calculation with SOC. A scalar-relativistic non-SOC B:Si calculation may be retained only as an early method-development branch. | Neutral B:Si has an odd valence-electron count, and acceptor physics is tied to the spin-orbit-coupled valence-band manifold. | Final B:Si operator records require spinor degrees of freedom, SOC-compatible pseudopotentials, spin labels, and B-specific Wannier/alignment conventions; non-SOC B data are explicitly non-final. | Must be compared to a compatible bulk reference branch with matching relativistic/SOC conventions for final B claims. | `07`, `08-B`, `09-B`, `10`. | Frozen |
| Bulk crystal convention | Diamond-structure silicon: an fcc Bravais lattice with a two-Si-atom basis, equivalently a conventional cubic cell containing eight Si atoms. Primitive vectors, conventional-cell axes when used, and site basis must be recorded explicitly in the operator metadata. | Silicon’s band valleys, symmetry, and $sp^3s^*$ model are tied to the diamond lattice. | Primitive-cell and supercell folding conventions determine Brillouin-zone labels, valley indexing, Wannier site labels, and TB orbital ordering. | Yes. | `02.01.01`, `03`, `04`, `05`, `06`, `07`. | Frozen |
| Primitive-cell convention | Use a two-Si primitive cell for primitive bulk calculations; allow conventional-cell notation only as a documented coordinate description. | The primitive cell is the minimal translational unit for bulk band and Wannier references. | Requires exact mapping between primitive and supercell coordinates for folding and comparison. | Bulk primitive and dopant supercell branches must share the same underlying coordinate convention. | `02`, `03`, `04`, `05`, `06`, `07`. | Frozen |
| Lattice-constant convention | Determine the production lattice constant by a zero-pressure PBE bulk relaxation using the selected Si pseudopotential. Freeze that lattice constant for the bulk and dopant-supercell lattice vectors. Treat the experimental lattice constant only as an external validation branch. | The production geometry is internally consistent with the approved PBE parent and Si pseudopotential; the experimental lattice constant remains useful for external comparison but is not the primary parent problem. | Affects all geometries, reciprocal-space coordinates, Wannier centers, valley positions, and impurity distances. `02.01.04` determines and freezes the numerical value. | Yes, unless an explicitly controlled validation branch is recorded. | `02.01.04`, `03`, `04`, `06`, `07`, `09`. | Frozen |
| Dopant supercell convention | Periodic $N_1\times N_2\times N_3$ multiples of the frozen bulk primitive/conventional cell with one substitutional dopant per cell; exact sizes deferred to numerical specification and convergence. | Doped periodic cells approximate an isolated dopant only through supercell-size convergence. | Supercell size controls artificial dopant concentration and image interactions; numerical choice belongs to `01.01.02`/dopant convergence tasks. | Bulk comparison supercell must match each doped supercell. | `05`, `06`, `07`, `08`, `09`. | Frozen convention; numerical sizes deferred |
| Substitutional dopant site | Replace one Si atom on a diamond-lattice sublattice site; choose a symmetry-central site in the finite supercell when possible. | P and B are substitutional dopants in the stated program. A central/symmetry site simplifies radial shell assignment and image diagnostics. | Determines site labels, dopant-relative distances, orbital correspondence, and impurity operator center. | Host site convention must be shared for P and B branches. | `06.01.01`, `07.01.01`, `08`, `09`. | Frozen |
| Neutral defect interpretation | Primary extraction branches: neutral substitutional P$_\mathrm{Si}^0$ and neutral substitutional B$_\mathrm{Si}^0$, with electron count determined by pseudopotential valence electrons. Both neutral P:Si and neutral B:Si have odd valence-electron counts relative to an even-electron pristine Si supercell. For P:Si, the neutral donor includes the positively charged donor core relative to Si and the extra bound/screening electron in the same periodic Kohn--Sham problem. | Neutral cells avoid compensating-background artifacts in the first impurity-operator extraction and define direct Kohn--Sham perturbations. The ionized donor-core potential used in continuum effective-mass language is related but not identical to the full neutral-supercell perturbation unless a controlled extraction or charge-state branch states what electronic screening has been removed or retained. | Donor/acceptor binding interpretations must state occupation, spin treatment, and band-edge reference; neutral-supercell results must not be relabeled as ionized charged-defect results. | Bulk remains neutral; dopant branches use their species-specific neutral electron count. | `06`, `07`, `08`, `09`. | Frozen |
| Charged defect interpretation | Charged P$_\mathrm{Si}^{+}$ and B$_\mathrm{Si}^{-}$ calculations are deferred to separately specified controlled branches and are not part of the primary v1 production path. | Continuum screened Coulomb models often describe ionized dopants, but periodic charged DFT requires explicit electrostatic conventions and corrections. | Charged branches require compensating backgrounds, finite-size corrections, charge-transition reference conventions, and separate manifests before use. | If used later, correction conventions must be common and branch-specific. | Later controlled branches of `06`, `07`, `08`, `09`. | Frozen deferral |
| Atomic relaxation protocol | For the primary dopant branches, relax internal atomic coordinates while keeping the approved bulk lattice vectors fixed. Retain unrelaxed dopant structures only as diagnostics. | Local relaxation is part of the physical impurity perturbation, while changing supercell lattice vectors would mix dilute-defect physics with finite-concentration strain. | Relaxed and unrelaxed operators differ; downstream records must identify which structural branch they consume. | Bulk lattice vectors shared; dopant internal relaxations species-specific. | `02.01.04`, `06`, `07`, `08`, `09`. | Frozen |
| Boundary conditions | Periodic boundary conditions for all DFT and Wannier parent calculations. Doped supercells represent periodic dopant arrays until a supercell-size convergence study supports isolated-impurity interpretation. | Plane-wave Kohn--Sham and Wannier workflows are periodic; isolated impurities are approximated by large supercells, not by open-boundary DFT here. | Image interactions and folding must be tracked as physical finite-supercell effects. | Yes. | `02`, `03`, `05`, `06`, `07`, `08`, `09`. | Frozen |
| Periodic-image interpretation | Treat every doped calculation as a periodic array at the calculated supercell size; isolated-dopant statements require convergence of selected operator and bound-state observables with size. | Avoids falsely interpreting one finite periodic calculation as an isolated impurity. | Supercell dependence becomes a reported error source, separate from numerical convergence and model-reduction error. | Yes for dopant branches; bulk comparison supercells share periodicity. | `06`, `07`, `08`, `09`. | Frozen |
| Electrostatic alignment convention | Physical requirement: bulk and dopant Hamiltonians must be placed on a common scalar energy zero before subtraction. The exact estimator, sampling region, and uncertainty protocol are deferred to Stage `05`. | Direct matrix subtraction requires a common energy reference, but choosing the operational estimator is part of the alignment methodology rather than the pristine-bulk pilot. | Stage `05` must define and validate the estimator before impurity extraction; no `G02`--`G04` bulk task is blocked by the exact dopant-alignment estimator. | Required for dopant comparisons; not required for standalone pristine-bulk observables. | `05`, `06`, `07`, `08`, `10`. | Frozen requirement; estimator deferred to Stage `05` |
| Energy zero for bulk band quantities | Report band-edge energies relative to the selected valence-band maximum for bulk validation; use the common scalar energy-reference requirement for bulk-dopant operator subtraction, with the operational estimator selected in Stage `05`. | Band gaps/effective masses and operator differences require distinct but documented references. | Prevents mixing a plotting convention with the subtraction reference. | Yes within each reported comparison. | `02.02.02`, `03`, `04`, `05`, `06`, `07`. | Frozen |
| Bulk target observables | Immediate non-SOC bulk pilot: indirect Kohn--Sham gap, conduction-valley position, longitudinal electron effective mass, transverse electron effective mass, and withheld-point band errors. | These are the required quantities for the non-SOC bulk-pilot and TB-reduction path without overclaiming valence-band acceptor physics. | Determines which eigenvalues and derivatives must be extracted after numerical convergence for `G02`--`G04`; valence-manifold observables require a separately approved branch. | Bulk pilot values are shared as host references for matching non-SOC dopant branches. | `02.02.02`, `03`, `04`; possible later `07`, `09-B` branch. | Frozen |
| Target band-edge subspace | Immediate bulk pilot: silicon band-edge subspace sufficient for $sp^3s^*$ bulk reduction, including valence and low conduction bands needed to describe the indirect gap and electron effective masses. Exact band count/windows belong to `03.01.01`. | The target subspace must include the states whose operator and band-edge physics are to be preserved. | Fixes Wannier rank, TB orbital correspondence, and operator-record dimensions. | The corresponding host subspace must be compatible with dopant projections. | `03.01.01`, `04.01.01`, `05`, `06`, `07`. | Frozen |
| P impurity target observables | Donor bound-state energies relative to the relevant conduction-band edge, valley composition/subspace fidelity, spatial localization/envelope diagnostics, and impurity-operator norms by radial shell. | P in Si is a donor; continuum reduction tests whether the donor can be described by screened/central-cell effective-mass physics. | Requires conduction-valley channel tracking and bound-state matching after impurity extraction. | Uses the shared host conduction-band reference. | `06`, `08-P`, `09-P`. | Frozen |
| B impurity target observables | Acceptor bound-state energies relative to the valence-band edge, valence-band subspace fidelity, spatial localization/envelope diagnostics, and impurity-operator norms by radial shell. | B in Si is an acceptor; final acceptor and continuum interpretation uses the approved fully relativistic SOC branch. | Requires valence-manifold tracking in a spinor/SOC representation for final B claims. | Uses the shared host valence-band reference from the compatible SOC branch. | `07`, `08-B`, `09-B`. | Frozen |
| Separation of physical and numerical approximations | Physical assumptions are those listed here; numerical approximations are cutoffs, meshes, tolerances, smearing/eigensolver choices, and software-version execution details. | The research plan separately tracks parent-model, numerical/discretization, and model-reduction errors. | `01.01.02` may not alter physical choices without revising this specification or recording a branch. | Yes. | All stages. | Frozen |

## Immediate pilot versus complete dopant program

For the **immediate bulk-silicon pilot**, the operational physical branch is:

- Kohn--Sham DFT parent for pristine diamond-structure Si;
- PBE GGA;
- optimized norm-conserving Vanderbilt Si pseudopotential from a PseudoDojo PBE standard table, with exact release and UPF metadata selected in `01.01.02`;
- scalar-relativistic, non-SOC, non-spin-polarized baseline;
- diamond-lattice convention with a production lattice constant determined by zero-pressure PBE bulk relaxation using the selected Si pseudopotential;
- required bulk observables: indirect Kohn--Sham gap, conduction-valley position, longitudinal electron effective mass, transverse electron effective mass, and withheld-point band errors.

For the **complete dopant program**, the same host and parent choices must be extended to P:Si and B:Si supercells. Dopant-specialization items are separated from the bulk-pilot gate so that P:Si or B:Si branch construction does not block `G02`--`G04`.

## Decision gates and downstream eligibility

### Bulk Pilot gate

The physical Bulk Pilot gate is frozen by this specification. It fixes:

- PBE GGA for the pristine-Si parent;
- PseudoDojo PBE standard-table ONCV pseudopotential family, with exact Si UPF metadata to be selected in `01.01.02` rather than as a prerequisite for entering `01.01.02`;
- Si $3s^2 3p^2$ valence;
- zero-pressure PBE-relaxed production lattice constant to be determined in `02.01.04` using the selected Si pseudopotential;
- scalar-relativistic, non-SOC, non-spin-polarized bulk branch;
- target band-edge and $sp^3s^*$-compatible subspace definition for the non-SOC pilot, with exact Wannier band counts/windows assigned to `03.01.01`.

Eligible now that `01.01.01` is Passed:

- `01.01.02`: numerical conventions and software stack;
- `01.02.01`: operator-record schema using frozen physical metadata fields.

Eligible after their normal numerical/methodological prerequisites, without dopant-specific decisions blocking them:

- `02.01.01`--`02.01.04`: bulk primitive-cell input, convergence order, and frozen geometry;
- `03.01.01`: target band-edge subspace definition;
- `04.01.01`: $sp^3s^*$ model implementation for the approved non-SOC bulk branch.

### P:Si specialization gate

`06.01.01` constructs the P:Si specialization gate from this frozen v1 specification. It must record or point to:

- exact P UPF filename, version, SHA-256 hash, suggested cutoff, converged cutoff, and compatibility with the selected PseudoDojo PBE standard table;
- P $3s^2 3p^3$ valence;
- primary neutral P$_\mathrm{Si}^0$ branch and deferral of charged P$_\mathrm{Si}^{+}$ to a separate controlled branch;
- collinear spin-polarized scalar-relativistic non-SOC P:Si baseline;
- dopant internal-relaxation protocol at fixed approved host lattice vectors;
- Stage `05` energy-alignment estimator and uncertainty protocol once Stage `05` supplies it;
- P donor target observables and interpretation of the neutral donor perturbation versus ionized donor-core potential.

Eligible before the P:Si specialization gate is complete:

- `06.01.01`: construct the phosphorus physical-specialization gate.

Eligible after the P:Si specialization gate and remaining prerequisites pass:

- P-specific branches of `06`, `08-P`, and `09-P`.

### B:Si specialization gate

`07.01.01` constructs the B:Si specialization gate from this frozen v1 specification. It must record or point to:

- exact B UPF filename, version, SHA-256 hash, suggested cutoff, converged cutoff, and compatibility with the selected PseudoDojo PBE standard table;
- B $2s^2 2p^1$ valence;
- primary neutral B$_\mathrm{Si}^0$ branch and deferral of charged B$_\mathrm{Si}^{-}$ to a separate controlled branch;
- fully relativistic noncollinear spinor calculation with SOC for final acceptor and continuum claims;
- scalar-relativistic non-SOC B:Si calculation only as an early method-development branch;
- dopant internal-relaxation protocol at fixed approved host lattice vectors;
- Stage `05` energy-alignment estimator and uncertainty protocol once Stage `05` supplies it;
- B acceptor target observables.

Eligible before the B:Si specialization gate is complete:

- `07.01.01`: construct the boron physical-specialization gate.

Eligible after the B:Si specialization gate and remaining prerequisites pass:

- B-specific branches of `07`, `08-B`, and `09-B`.

## Explicit limitations

- No first-principles calculation has been run for this specification.
- No Quantum ESPRESSO input file is created here.
- No numerical convergence parameter is selected here.
- A successful downstream code run will not by itself validate the physical parent model.
- Bulk-pilot production claims require the Bulk Pilot gate only; dopant specialization, charged-defect branches, dopant SOC branches, and Stage `05` energy-alignment-estimator implementation do not block `G02`--`G04`.
- `01.01.02` selects exact pseudopotential releases/files/hashes and numerical parameters; this selection is required before downstream numerical production but not before entering `01.01.02`.
- Stage `05` selects and validates the operational energy-alignment estimator before impurity-operator extraction; the common scalar energy-reference requirement is already frozen here.
