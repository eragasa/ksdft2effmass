# Quantum ESPRESSO simulation design informed by finite-rank studies

## Status

**Draft campaign design under the accepted PseudoDojo scalar-relativistic baseline. Exact artifacts, numerical qualification, and execution preflights remain pending. No Quantum ESPRESSO execution is authorized by this document.**

This record translates lessons from the periodic finite-rank calculations into the
ordering and evidence boundaries of a new bulk-silicon parent campaign. It does not
transfer synthetic ranks, meshes, coefficients, tolerances, or results into silicon.
Exact executable identities, resource bounds, occurrence inventories, and input files
must be frozen in later preflights before any protected execution.

## Current pseudopotential status

The accepted [pseudopotential-library specification](../../../../../specification/dft-pseudopotential-library/v1/index.md)
selects **PseudoDojo ONCVPSP v0.5, PBE, scalar-relativistic, stringent** as the common
B/Si/P baseline. The immediate pristine-Si QE campaign uses the selected Si UPF2
representation after its exact native-file identity is verified. PSP8 remains the
separately identified ABINIT representation; no cross-code agreement is inferred from
common source-entry membership.

The family selection is settled. Exact current artifact identities, local set
membership, catalog admission, and observable-specific convergence are still required.
A historical standard-table `Si.upf` is not relabeled as a v0.5 stringent artifact.

The retained **SSSP 1.3.0 PBE Efficiency** silicon parent is a separate
scalar-relativistic ultrasoft development source. Its UPF header reports PBE, not LDA;
UPF is a file format, not an exchange--correlation label. Its `42/336 Ry` observations,
relaxed structure, and Wannier source do not establish PseudoDojo convergence or
production adequacy. They remain available for their existing development diagnosis,
including the blocked common-space rank gate. The separately authorized **SSSP v2.0
Precision** comparison is not a replacement of this common baseline.

Final B:Si acceptor/SOC work uses the separate PseudoDojo v0.4 PBE fully relativistic
stringent branch and a matching fully relativistic Si host. It is not part of the
non-SOC pristine-Si QE0--QE8 campaign below.

Source-family names, artifact identity, library membership, software verification,
numerical convergence, and scientific acceptance remain distinct. No previous cutoff,
structure, or convergence result is transferred between these parent models.

## Finite-rank lessons that do transfer

The rank-N studies contribute workflow rules rather than silicon parameters:

1. Define the parent state space, basis, units, geometry, and energy reference before
   comparing or subtracting represented operators.
2. Separate parent qualification, projection, disentanglement, basis transformation,
   gauge alignment, Fourier interpolation, support truncation, and parameter fitting.
3. Carry the retained rank and ambient parent dimension explicitly. Never infer a state
   space from a matrix size, filename, band count, or campaign code.
4. Keep construction meshes separate from disjoint development and confirmation
   inventories.
5. Treat rank deficiency, failed transport, optimizer failure, nonfinite arithmetic, and
   scientific inadequacy as different outcomes.
6. Verify decisive results through a producer-independent route.
7. Characterize the complete hopping representation before removing support.
8. Freeze candidates, diagnostics, tolerances, and stop rules before observing
   confirmation values.

## Required QE campaign

### QE0: deployment and identity qualification

This is a prerequisite, not a scientific convergence result.

- Bind the exact selected PseudoDojo v0.5 PBE scalar-relativistic stringent Si UPF2
  bytes, full checksum, byte count, source-entry and table identities, and admitted
  local library occurrence. Exact artifact acquisition and verification remain pending;
  the historical standard-table and SSSP files are not substitutes.
- Bind one primary `pw.x` executable and one genuinely independent established
  QE/toolchain comparator.
- Record compiler, BLAS/LAPACK, FFT, MPI, and runtime-library identities.
- Render and compare one identical, bounded primitive-cell SCF input through both
  toolchains.
- Require finite output, native completion, SCF convergence, consistent electron and
  band counts, and agreed parsed conventions.
- Retain IEEE diagnostics without interpreting process success as numerical or
  scientific acceptance.

**Gate:** unresolved input, pseudopotential, executable, or parsed-convention identity
stops the scientific campaign.

### QE1: cutoff and SCF-mesh qualification on the seed geometry

Use the exact two-atom right-handed diamond seed only as a qualification geometry.
Design the inventory for the verified PseudoDojo v0.5 stringent norm-conserving Si
artifact. The retained SSSP ultrasoft cutoff pair does not qualify this parent.

The authored preflight must freeze:

- a monotone `ecutwfc` sequence bracketing the selected source's normal/high silicon
  hints, `36/48 Ry`, and extending above them; these hints are not accepted cutoffs;
- a separately controlled `ecutrho` sequence for the exact norm-conserving artifact,
  with a prospectively fixed conservative density cutoff during the wavefunction axis
  and a fixed wavefunction cutoff during the density axis, including a higher guard;
- uniform SCF meshes beginning with the numerical specification's `6x6x6`, `8x8x8`,
  `10x10x10`, and `12x12x12` ladder unless prospectively revised;
- one frozen Gamma-centered or shifted convention selected before execution; and
- explicit mixed cutoff--mesh corner controls.

The exact cutoff grid must be written before execution. The numerical specification's
initial norm-conserving ratio is a screening suggestion, not convergence evidence.
No setting is inherited from the retained SSSP `42/336 Ry` occurrence.

Each admitted setting requires an independent SCF occurrence. Linked NSCF observations
must evaluate the quantities that actually govern the downstream parent:

- total energy per atom;
- stress;
- indirect Kohn--Sham gap;
- conduction-valley position;
- longitudinal and transverse electron effective masses; and
- fixed, prospectively declared band-energy probes.

Use the numerical-specification tolerances. Do not select settings from total energy
alone, and do not call adjacent-setting stability an infinite-basis result.

**Gate:** produce a provisional setting tuple for the exact seed geometry, or a bounded
inconclusive/budget-exhausted disposition.

### QE2: PBE equilibrium structure

With settings at least as strict as the QE1 provisional tuple:

- calculate a symmetric equation-of-state grid containing at least seven lattice
  constants and spanning compressed and expanded cells;
- fit the declared equation of state or local polynomial;
- retain all included/excluded points and residuals;
- refine around the minimum until the lattice-constant rule is met or the fit
  uncertainty dominates; and
- verify the candidate with a symmetry-constrained variable-cell relaxation or an
  additional energy/stress calculation.

The experimental lattice constant remains an external comparison, not the parent input.

**Gate:** freeze one exact primitive structure for the explicitly selected PBE parent, with uncertainty and
lineage, or stop without a production lattice.

### QE3: final setting confirmation on the relaxed structure

Repeat the relevant cutoff, mesh, and mixed-corner controls on the QE2 structure.

If the selected setting changes, the structure must be relaxed again under the new
setting and reconfirmed within a prospectively bounded loop. A setting selected on the
seed geometry does not automatically transfer to the relaxed geometry.

**Gate:** accept one exact structure/settings pair or retain an inconclusive result.

### QE4: final parent SCF

Run one fresh parent SCF from the accepted QE3 pair. A convergence or relaxation
occurrence cannot double as the final parent merely because its settings match.

Retain the saved-state identity, density, eigenvalue metadata, warnings, and exact input
required by every downstream NSCF.

**Gate:** one authenticated, reproducible scalar-relativistic non-SOC PBE parent state.

### QE5: direct-parent band-manifold characterization

From the QE4 saved state, perform separate NSCF calculations for separate scientific
roles:

1. a contextual high-symmetry band path;
2. a local conduction-valley search rather than an assumed fixed `Delta_0.85` point;
3. longitudinal and transverse effective-mass stencils with at least one smaller-stencil
   stability check;
4. the prospectively declared fixed band-energy probes; and
5. a high-enough band inventory to determine the ambient space needed by a rank-ten
   Wannier target.

Band identities, degeneracies, projector/cluster identities where available, reciprocal
coordinates, axes, units, and energy reference must be explicit.

**Gate:** an authenticated parent band manifold and observable baseline. This stage does
not select Wannier windows or claim experimental agreement.

### QE6: Wannier construction-grid NSCF refinement

Only after QE5 determines the relevant parent-band inventory, define a small prospective
uniform-mesh ladder for the QE-to-Wannier interface.

For every candidate construction mesh:

- use the same QE4 density and frozen physical branch;
- carry an explicit ambient parent-band count greater than the retained rank ten;
- record lower and upper energy margins around the proposed target space;
- retain ordered reciprocal points and exact weights;
- verify finite eigenvalues and eigenpair diagnostics; and
- forbid automatic progression to a finer mesh after a failed localization or alignment
  gate.

The mesh ladder, parent-band inventory, outer window, frozen window, and projections are
separate coordinates. They must not be changed together in one diagnostic occurrence.

**Gate:** select at most one QE NSCF interface source for a separately authorized
Wannier90 preprocessing/conversion/localization route.

### QE7: development direct-parent inventory

A development NSCF inventory must be disjoint from the selected construction grid and
must support the same observable channels used to assess the parent and later source:

- spectra and gap;
- valley identity and position;
- curvature and effective masses; and
- any declared projector/cluster comparisons.

Previously revealed parent values may inform scientific understanding, but they cannot
be reused as a confirmation set or used to tune a supposedly prospective diagnostic.

**Gate:** development evaluation evidence only. It does not select support, fit a model,
or establish confirmation.

### QE8: confirmation-only parent inventory

Run only after the Wannier source, common-space disposition, hopping analysis, selected
model class, fitting rules, and all numerical comparison policies are frozen.

The existing 402-point geometry may remain reserved if a later preflight confirms that
its coordinate convention and separation contract remain valid for the new parent. Its
parent values must remain unobserved until this stage.

**Gate:** confirmation comparison without refitting, recalibration, support reselection,
or model-class revision.

## Simulations that are deliberately excluded

The following are not part of the first new QE campaign:

- another optimizer-only extension of the old Wannier source;
- automatic `6x6x6` to `8x8x8` or `12x12x12` escalation;
- a production claim based on retained finite-setting observations alone;
- a QE band-path calculation used as a substitute for SCF-mesh convergence;
- a new Wannier construction before the explicitly selected parent is qualified;
- a Slater--Koster fit before common-space and hopping gates pass; or
- confirmation points used to choose windows, projections, support, or fit settings.

## Order of protected execution

If separately authorized later, protected QE execution must occur in this order:

```text
QE0 deployment comparison
  -> QE1 cutoff/mesh qualification
  -> QE2 equilibrium structure
  -> QE3 final setting confirmation
  -> QE4 final parent SCF
  -> QE5 parent band-manifold characterization
  -> QE6 construction-grid NSCF refinement
  -> separately authorized Wannier90 route
  -> QE7 development evaluation as declared
  -> freeze all reduction/model choices
  -> QE8 confirmation-only evaluation
```

Each arrow is a gate, not automatic progression. Quantum ESPRESSO and Wannier90 remain
separate protected calculators even when they participate in one scientific program.

## Immediate non-execution work

Before requesting QE0 or QE1 authorization:

1. choose one explicit current campaign owner and preserve provenance bindings; moving
   historical calculation directories is not a prerequisite for parent qualification;
2. acquire and authenticate the selected PseudoDojo v0.5 stringent Si UPF2 and exact
   checksum, then bind its admitted local library occurrence;
3. identify the independent QE/toolchain comparator;
4. write typed QE0 and QE1 requests with exact inputs, output inventories, runtime and
   resource estimates, stop rules, and nonexistent output roots;
5. define the linked NSCF observable extraction and independent-verification routes; and
6. review the exact occurrence count before any authorization request.
