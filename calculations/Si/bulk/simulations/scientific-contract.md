# Scientific contract

## Scope

This route-level binding states the scientific information that reusable software must
carry without allowing Project Koios to select values owned by this calculation. It
composes the bulk-silicon development plan and the authoritative
[Si-VC component-locality campaign](../../../../docs/computational/Si-bulk/wannier-component-locality/index.md);
it does not replace or duplicate that campaign's operator and CPN definitions. Every
future exact declaration must distinguish a physical model, its mathematical
operators, and each finite matrix representation.

## Fixed branch intent

The prospective pristine-silicon parent has the following branch intent:

| Field | Required declaration |
| --- | --- |
| Material | Pristine bulk silicon |
| Exchange-correlation approximation | PBE |
| Relativistic branch | Scalar relativistic |
| Spin branch | Non-spin-polarized |
| Spin-orbit coupling | Excluded from this parent |
| Net charge | Neutral |
| Periodicity | Three-dimensional bulk |
| Primitive contents | Two silicon atoms after exact structure acceptance |
| Parent calculator route | Quantum ESPRESSO `pw.x` SCF and NSCF |
| Interface route | `wannier90.x -pp` then `pw2wannier90.x` |
| Localized representation | Wannier90, with exact windows, projections, rank, and convergence controls declared prospectively |

The table fixes a branch, not a completed simulation. Exact geometry,
pseudopotential bytes, settings, windows, projections, and tolerances remain
separate declarations and gates.

## State spaces and representations

The route must identify the following spaces before comparing or subtracting
objects:

1. **SCF parent state.** The self-consistent charge density, potential, and saved
   state for one exact structure, pseudopotential set, reciprocal mesh, cutoff,
   occupation rule, and solver policy.
2. **NSCF Bloch frame.** Eigenpairs on one explicitly ordered, full unreduced
   uniform reciprocal grid. The declaration must carry band count, k-point
   coordinates and weights, spin convention, basis convention, and exact SCF
   parent identity.
3. **Wannier construction subspace.** The outer and frozen energy windows,
   projections, retained band inventory, Wannier rank, neighbor graph, and
   gauge/disentanglement matrices used for construction.
4. **Wannier real-space representation.** Exact lattice-vector-indexed Hamiltonian
   blocks and degeneracies, together with orbital ordering, centers, spreads,
   energy reference, and truncation status.
5. **Comparison spaces.** Construction and withheld momentum sets on which direct
   parent and Wannier spectra, projectors, or represented operators are aligned.
   A direct Bloch matrix and a Wannier matrix must not be subtracted until their
   represented state spaces and gauge/alignment map are declared.

Projection, disentanglement, basis transformation, and real-space truncation are
separate operations. A successful localization does not prove that these operations
preserve the targeted observables.

## Route profiles and plane-wave evidence

This calculation distinguishes two nested evidence profiles:

1. **Spectral Wannier qualification.** This profile requires the full-grid parent
   eigenvalues, neighbor topology, projection and overlap interface data, Wannier
   gauge/disentanglement records, localization evidence, and real-space Hamiltonian.
   An authenticated AMN/MMN/EIG interface may satisfy this profile without UNK output.
2. **Component-operator qualification.** This profile extends the spectral profile
   with authenticated parent plane-wave eigenvectors or equivalent coefficient
   evidence sufficient to construct the common-frame canonical kinetic operator
   \(T^W\) and remainder \(R^W=H^W-T^W\). The authoritative
   [Si-VC numerical definition](../../../../docs/computational/Si-bulk/wannier-component-locality/numerics.md)
   requires those coefficients and separate gauge/disentanglement transformations.

The Si-VC component-locality campaign requires the second profile. UNK files are one
possible provider-native carrier of sampled real-space periodic wavefunctions, but an
UNK basename is not itself the scientific requirement and must not become globally
mandatory for the spectral profile. UNK samples are not presumed interchangeable with
native plane-wave coefficients: any use for constructing or checking \(C(\mathbf{k})\)
must prospectively bind the FFT grid, normalization, ordering, completeness, and exact
forward/inverse transform. Before component-route execution, this calculation must
freeze whether authenticated QE wavefunction coefficients, verified UNK-derived
samples and transforms, or a prospectively verified pair of representations supplies
the required coefficient evidence and independent checks. Project Koios owns the
route-specific provider manifest; this calculation owns which profile is required.

## Basis, geometry, and reciprocal conventions

Every exact structure declaration must bind:

- ordered direct-lattice vectors and whether vectors are rows or columns;
- length unit and lattice-parameter meaning;
- ordered fractional atomic coordinates;
- handedness and cell representation;
- reciprocal-vector convention, including any factor of `2 pi`;
- structure identifier, byte size, and complete SHA-256; and
- source and acceptance provenance.

The repository currently contains more than one cyclic ordering of the same nominal
5.43 Å primitive silicon basis. They are legitimate explicit representations but are
not interchangeable by filename or material label. A route that changes basis must
retain the exact integer-unimodular direct-basis transform and the corresponding
reciprocal-coordinate transform.

The production lattice remains unresolved and must be obtained from the separately
authorized zero-pressure PBE structural-convergence stage that follows provisional
cutoff/k-point qualification. An exact fixed reference lattice may define a labelled
comparison branch, but it cannot replace structural convergence for the primary
production parent.

The Project Koios 5.43 Å example and the historical 10.20-bohr provisional geometry
must not be silently promoted.

## Numerical and structural qualification order

Cutoff/k-point qualification precedes structural convergence, but its result is scoped
to one exact seed structure. The selected \(S_0\) is the 680-byte
[`Si.PrimitiveUnitCell`](seed-structure-decision.md) record at inspected ProjectKoios
revision `bbb9f1d8110ed9fe3ea1873c2366073c98f48c71`, SHA-256
`6e048c7001f329459e85f321e7bd406f4dd871d6fabf8d12fa349a1623f87ccc`.
It is explicitly provisional. Let \(Q_0@S_0\) denote the selected coupled-cutoff and
reciprocal-sampling setting on that structure. The structural route consumes \(Q_0@S_0\) and may produce a mechanically
qualified structure \(S_1\). A fresh joint confirmation study on \(S_1\) then produces
\(Q_1@S_1\).

The production parent requires a stable accepted pair \((S_*,Q_*)\), not two
independently accepted labels. If confirmation changes the selected setting, the
structure must be recomputed under that setting and the numerical study repeated on
the new structure within a prospectively frozen budget. A changed lattice changes the
reciprocal basis, so an unchanged integer k-mesh is not evidence that sampling quality
transferred.

Project Koios owns the reusable qualification/feedback mechanics and exact lineage.
This calculation owns the seed structure, candidate coordinates, observables,
tolerances, cell mode, target pressure, iteration budget, and scientific disposition.
Every SCF or relaxation process remains separately authorized. Stable-pair acceptance
emits a new parent-SCF requirement; the final confirmation occurrence is not reused as
the downstream parent under this architecture.

## Accepted Tranche 1 route policies

The operator accepted the following bounded architecture and campaign policies:

1. An accepted correlated cutoff/k-point grid selects its highest tested
   mesh/cutoff corner as the production coordinate. Selecting a lower stable-tail
   corner would require a separately reviewed selection and verification rule.
2. Variable-cell zero-pressure qualification requires finite maximum-force and
   scalar-pressure observations plus a complete finite stress tensor. Provider
   completion and optimizer flags remain insufficient. Exact force and pressure
   tolerances, cell mode, and feedback budget remain prospective calculation-owned
   declarations.
3. The first reusable Wannier90 `.win` renderer supports a generic non-spin spectral
   subset. This calculation must still supply every silicon-specific structure,
   projection, window, reciprocal mesh, rank, and control value.
4. Successful localization evidence requires `.wout` and `_hr.dat`. `_u.mat` and
   `_u_dis.mat` are additionally required exactly when the declared construction
   uses their corresponding gauge or disentanglement transformations. Incidental
   native work-directory files are not silently promoted into retained route
   evidence.

These selections close only the four Tranche 1 policy choices. They do not accept
numerical values, establish scientific qualification, authorize implementation or
artifact acquisition, or authorize any calculator occurrence.

## Pseudopotential branch and artifact identity

The project pseudopotential specification selects PseudoDojo ONCVPSP v0.5, PBE,
scalar-relativistic, stringent UPF2 for the primary silicon branch. That source entry
is not an artifact identity. Before composition, the exact local artifact must have:

- native filename and format version;
- compressed identity when acquired compressed;
- uncompressed byte size and SHA-256;
- embedded element, functional, formalism, relativity, and valence metadata;
- source URL and acquisition record;
- license and citation record; and
- verified content-addressed library location.

The historical 225,602-byte Si UPF with SHA-256
`39822757f53f36e3bf3bfb779356152a8d3f21199c7db9dd5a931e5d18c45282`
identifies the earlier standard branch. It may be reused only to reproduce or compare
that historical parent model. It cannot establish a v0.5/stringent result. The Si-VC
planning now follows the later accepted v0.5/stringent family decision while retaining
this exact identity only as historical comparator evidence.

The SSSP 1.3.0 efficiency/precision Si USPP with SHA-256
`ae3aefd0811f9499dbc4a72f1f9ae02ef4fc7f3568bf6f559b68668719c69e2b`
is represented by existing Project Koios examples. It is neither the accepted common
baseline nor an automatic comparator; a QE-only comparison using SSSP requires a
separate scientific declaration and authorization.

Changing pseudopotential family or native artifact creates a different parent model.
Earlier cutoff, lattice, valley, or mass observations do not transfer as convergence
evidence.

## Numerical declarations

Each calculation version must freeze, at minimum:

- the exact structure to which any numerical qualification applies;
- wavefunction and charge-density cutoffs and their units;
- reciprocal mesh, offset, symmetry, and time-reversal reduction policy;
- occupation and smearing policy;
- electronic convergence tolerance and maximum iterations;
- diagonalization and mixing policy where relevant;
- band count and explicit full-grid NSCF ordering;
- warning, retry, timeout, and stop policy; and
- observable-specific comparison tolerances.

Pseudo-library cutoff hints are starting points, not calculated convergence. Total
energy, stress, fixed-point eigenvalues, valley location, curvature/effective mass,
Wannier interpolation, projectors, and represented operators require distinct
acceptance criteria.

## Energy, gauge, and alignment

Every retained result must state its energy zero. Permitted alignment operations must
be prospectively declared and must not absorb physical disagreement by convenience.
At minimum, the route must distinguish:

- calculator-native eigenvalue reference;
- any Fermi, valence-band, or selected-band scalar shift;
- Wannier90's reported reference convention;
- scalar spectral alignment from unitary subspace alignment; and
- comparison of individual states from comparison of degenerate clusters or
  projectors.

Valley and effective-mass analysis must identity-track the relevant band or isolated
cluster. It must not assume that a nominal `Delta_0.85` probe is the conduction
minimum.

## Error separation

Retained conclusions must keep these errors separate unless an explicit model relates
them:

1. parent-model error: functional, pseudopotential, relativity, spin, and geometry;
2. numerical/discretization error: cutoffs, meshes, solver tolerances, finite
   differences, and arithmetic/toolchain behavior;
3. Wannier/model-reduction error: selected manifold, disentanglement, gauge,
   localization, interpolation, and real-space truncation; and
4. downstream fitting error: finite candidate hierarchy, alignment family, training
   set, and optimization/search limits.

A passed software test establishes software behavior only. A successful process and
`JOB DONE.` establish process facts only. Neither is scientific validation.

## Scientific decision register

| Decision | Owner | Required before |
| --- | --- | --- |
| Exact provisional seed structure \(S_0\) and non-transfer label | Selected in [`seed-structure-decision.md`](seed-structure-decision.md) | Closed before new cutoff/k-point qualification |
| Coupled-cutoff, k-point, mixed-corner, observable, and selection policy | Highest tested accepted correlated-grid corner selected above; exact coordinates, observables, and tolerances remain with this calculation's scientific owner | New cutoff/k-point qualification |
| Structural cell mode, zero-pressure/force criteria, and iteration budget | Complete force/pressure/stress evidence selected above; exact mode, thresholds, and budget remain with this calculation's scientific owner | Structural convergence |
| Stable accepted pair \((S_*,Q_*)\) and source lineage | This calculation's scientific owner | Production-parent declaration |
| Exact v0.5/stringent Si UPF2 identity | Project pseudopotential specification and acquisition record | Any v0.5 QE input |
| Independent QE/toolchain comparator | This calculation's scientific owner | Historical C48/K8 acceptance review |
| Valley search and mass-fit protocol | This calculation's scientific owner | Valley/mass execution |
| Wannier rank, projections, and windows | This calculation's scientific owner | Wannier preprocessing |
| Parent-wavefunction evidence and any sample-to-coefficient transform for component operators | This calculation's scientific owner, constrained by verified provider routes | Component-route execution |
| Construction and withheld sets | This calculation's scientific owner | Wannier qualification |
| Warning disposition | This calculation's scientific owner, informed by toolchain evidence | Evidence promotion |

Project Koios may validate the shape and internal consistency of these declarations; it
must not choose their scientific values.
