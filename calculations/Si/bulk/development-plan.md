# Bulk-silicon calculation development plan

## Objective

Construct and qualify one scalar-relativistic, non-spin-polarized, non-SOC bulk-silicon
parent; build a compatible ten-spatial-orbital Wannier representation; and determine
whether a frozen finite hierarchy contains a common witness satisfying both spectral
and aligned-operator tolerances.

Every conclusion is bounded by the declared pseudopotential, exchange--correlation
approximation, geometry, meshes, retained manifold, alignment family, candidate
inventory, and verification tolerances.

## Stage 0 — close the audited-bootstrap disposition

Inputs:

- the retained direct-results audit;
- the finite-setting analysis and decision packet;
- the setting-disposition record; and
- the IEEE-warning investigations.

Completed decisions and diagnoses:

1. C48/K8 (48/192 Ry and a shifted $8\times8\times8$ mesh) was selected as a
   provisional finite-setting parameter pair;
2. the first instrumented trap was localized to external OpenCL discovery during
   startup; and
3. a separate cross-BLAS, cross-MPI `ZHEGVX` operation during initial-wavefunction
   subspace diagonalization was classified as IEEE divide-by-zero.

Remaining production-acceptance gates:

1. compare C48/K8 observables and residuals through an independently identified
   established QE/toolchain path;
2. retain or further classify the invalid, overflow, and underflow flags according to
   the comparator evidence;
3. freeze the exact mixed cutoff--mesh interaction corner implied by C48/K8; and
4. authorize every bounded successor execution separately.

These items do not block explicitly labelled downstream development or exploratory
analysis under the [provisional-use disposition](provisional-use-disposition.md). They
do block production-parent and publication-grade acceptance. The provisional selection
is not an infinite-setting result.

## Stage 1 — freeze the production parent contract

Before execution, bind:

- the accepted production lattice and physical branch;
- exact Quantum ESPRESSO executable and input identities;
- exact pseudopotential content identity and redistribution boundary;
- exchange--correlation approximation, occupations, cutoffs, meshes, and solver policy;
- warning, retry, and stop policies;
- expected compact and external native artifacts; and
- explicit bounded execution authorization.

A failed identity or authority gate stops the calculation.

## Stage 2 — qualify numerical settings

Evaluate the prospectively declared cutoff, reciprocal-mesh, and required mixed-corner
controls. Keep total-energy, stress, fixed-point band/gap, branch identity, and later
curvature requirements separate. Finite adjacent-setting stability must not be reported
as an infinite-basis bound.

Outputs must include an independent compact-result verifier and either an accepted
finite-setting disposition or a bounded failure/inconclusive record.

## Stage 3 — characterize the retained band manifold

Locate and identity-track the conduction valley rather than assuming the nominal
`Delta_0.85` probe is the minimum. Define disjoint construction and withheld momentum
sets. Retain eigenpair residuals, projector or cluster identities, isolating gaps where
available, and explicit degeneracy handling.

Effective-mass analysis requires a separately reviewed stencil or fit window,
conditioning assessment, and convergence rule; fixed-point band agreement is
insufficient.

## Stage 4 — construct and qualify the Wannier bridge

Subject to separate Wannier90 authorization, freeze projections, windows, meshes,
centers, spreads, convergence status, symmetry conventions, reciprocal sewing, and
energy reference. Compare direct-parent and Wannier bands, projectors, and represented
operators on construction and withheld meshes.

### Staggered withheld momentum validation

Use separate reciprocal-space roles rather than evaluating interpolation only on the
Wannier90 construction mesh:

1. the SCF mesh qualifies the self-consistent density under Stage 2;
2. a uniform construction mesh supplies the wavefunctions and overlaps used to build
   the frozen `spd` Wannier representation; and
3. a separately calculated staggered mesh supplies withheld parent values for
   interpolation and truncation assessment.

Freeze all three point sets in reduced reciprocal coordinates, including origins,
shifts, weights, reciprocal-cell conventions, symmetry reduction and unfolding, and
canonical ordering. The construction and withheld sets must be disjoint after
reciprocal-lattice equivalence and every symmetry identification used by the
calculation. A three-dimensional shifted Monkhorst--Pack mesh may provide the withheld
set, but its dimensions and shift require their own prospective review; the rational
one-dimensional stagger used by controlled models is a design pattern, not a silicon
mesh prescription. A high-symmetry band path is a presentation and targeted-diagnostic
inventory, not a substitute for the withheld uniform mesh.

Evaluate the withheld Quantum ESPRESSO parent values with the same frozen SCF density,
pseudopotential, cutoffs, geometry, occupations, spin branch, symmetry policy, units,
and scalar energy reference used by the construction calculation. This isolates
Wannier interpolation for one finite parent. It does not test SCF reciprocal-mesh
convergence, which remains a separate Stage 2 obligation.

For every admitted momentum and matched retained band, retain the parent value
$E_n^{\mathrm{DFT}}(\mathbf{k})$, the complete Wannier-interpolated value
$E_n^{\mathrm{W}}(\mathbf{k})$, and each support-truncated value
$E_{n,R}^{\mathrm{W}}(\mathbf{k})$. Report maximum and declared weighted-RMS forms of
three separate channels:

\[
 e_{\mathrm{interp}}=\lVert E^{\mathrm{DFT}}-E^{\mathrm{W}}\rVert,
 \qquad
 e_{\mathrm{trunc}}(R)=\lVert E^{\mathrm{W}}-E_R^{\mathrm{W}}\rVert,
 \qquad
 e_{\mathrm{total}}(R)=\lVert E^{\mathrm{DFT}}-E_R^{\mathrm{W}}\rVert.
\]

The residuals telescope pointwise, but their reported norms are not independent terms
to be added. Check the applicable triangle inequality and preserve all three values.
Stage 5 may use the total withheld error in an attained support--error or Pareto
analysis; interpolation and deliberate truncation remain separately visible so an
interpolation floor is not misreported as a locality limit.

For entangled bands, freeze the outer and frozen windows, retained rank, projector or
cluster matching, degeneracy policy, and failure disposition before evaluating these
channels. Direct operator differences require an explicitly identified common retained
space, basis or alignment, units, and energy reference. Without that bridge, report
matched spectral and projector diagnostics rather than subtracting the plane-wave and
Wannier matrices.

A finite staggered mesh establishes only a withheld finite-sample result. It does not
certify a continuum supremum, eliminate aliasing, or prove Wannier convergence. Any
validation-mesh refinement or additional shifts must be declared prospectively and
retained as separate sensitivity controls.

The tutorial-scale silicon Wannier preview is a software/integration precursor only and
cannot fill this gate.

## Stage 5 — freeze the local-model decision problem

Before fitting, declare:

- the finite `sp3s*` hierarchy and every support extension;
- the retained rank and orbital semantics;
- alignment family and group constraints;
- spectral and operator losses with exact normalizations;
- training and withheld sets;
- cost ordering;
- search budgets and global/exhaustive status; and
- thresholds justified from measured numerical floors.

Separate channel optima do not constitute a common witness.

The calculation-local Vogl 1983 LCAO `sp3s*` control now provides the accepted complete
Table 1 transcription and an independently implemented spinless ten-band Bloch
Hamiltonian. It can test representation conventions and later reduction machinery, but
it neither freezes the candidate hierarchy nor supplies evidence of adequacy against the
future accepted first-principles parent.

## Stage 6 — perform joint admissibility analysis

For every candidate, evaluate the spectral set and aligned-operator set under the same
model, support, alignment, and energy reference. Produce either:

- a common witness;
- a reviewed separation certificate for the frozen finite inventory; or
- an explicit inconclusive outcome.

A failed local optimizer is not evidence that the feasible set is empty.

## Stage 7 — withheld validation and attribution

Evaluate disjoint band, gap, valley, mass, projector, operator, and locality channels.
Attribute stable residuals by onsite/hopping block, orbital semantics, symmetry channel,
and support shell where justified. Repeat prospectively declared parent, Wannier,
stencil, map-resolution, and threshold sensitivities.

## Stage 8 — retain and verify

Create a no-overwrite package containing exact inputs, compact outputs, schemas,
provenance, checksums, source identities, candidate inventory, thresholds, independent
verification, plots derived only from verified inputs, and a calculation-facing
technical report.

Only after these gates may Paper D promote authenticated values into a completed
material result. Formal certificates may check exact finite claims but do not certify
Quantum ESPRESSO, Wannier90, binary64 execution, or physical validation.
