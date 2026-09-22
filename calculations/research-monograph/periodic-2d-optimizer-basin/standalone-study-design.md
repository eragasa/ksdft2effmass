# Proposed standalone optimizer-convergence study

## Status

**Proposed work; not authorized for execution.**

The human selected the standalone-paper route after review of the completed
72-start follow-up. This document converts that publication target into a
controlled computational design. It does not authorize Wannier90 execution,
publication, submission, dependency changes, or external transmission.

The exact machine-readable proposal is `standalone-study-proposal.json`.

## Scientific question

For the frozen synthetic rank-three periodic-2D parent, determine whether the
localized representation selected by Wannier90 is reproducible across a
systematic deterministic initialization design and numerically stable under
separately controlled reciprocal mesh, plane-wave cutoff, inactive embedding,
and optimizer preconditioning.

A negative result is publishable if every failed, nonconverged, and unfavorable
trajectory remains visible and the conclusions are restricted to this synthetic
model and declared protocol.

## Changes relative to the completed follow-up

### Decouple mesh and inactive embedding

The completed balanced sequence changed $N$ and $c$ together. The proposed study
adds a fixed-$c=31$ sequence at $N=11,15,19,23,27,31$ and retains a parallel
balanced sequence $c=N$. Their difference is reported as inactive-embedding
sensitivity rather than folded into mesh error.

The fixed value $c=31$ must pass a preprocessing-only structural check at every
mesh before localization begins. An unexpected neighbor-shell or interface
failure stops execution; it is not repaired automatically.

### Replace hand-selected starts with a deterministic design

Every configuration receives the same 16 starts: identity plus Halton indices
1--15. Each nonidentity start contains three ordered smooth periodic unitary
terms. Separate Halton dimensions choose generator, harmonic, amplitude, and
phase. This provides deterministic space-filling coverage without introducing
random seeds or claiming a probability distribution over gauges.

The exact generated table is retained in `standalone-initial-gauges.json`; its
unitarity defect is at most $2.32\times10^{-15}$ on the declared $31^2$ check
mesh. `generate_standalone_starts.py` regenerates it deterministically.

All starts are retained. Basin frequencies are descriptive algorithmic
frequencies, not uncertainty quantification.

### Separate optimizer protocols

The baseline retains preconditioning, 5000 iterations, tolerance $10^{-12}$,
and a five-step convergence window. At the fixed and balanced $N=23$
configurations, all 16 starts also run with the preconditioner disabled while
every other control is fixed.

Every start that lacks the native convergence statement at 5000 iterations is
continued from its exact checkpoint for at most 15000 additional iterations.
This applies uniformly to all baseline and optimizer-control failures. The
continuation is a separate diagnostic result and never replaces or reclassifies
the original endpoint.

Before execution authorization, the preflight must verify the documented
Wannier90 restart semantics and exact checkpoint identity behavior.

## Numerical design

### Configuration count

There are 14 unique baseline interfaces:

- six fixed-$c=31$ mesh cases;
- six balanced mesh cases, with the $N=c=31$ point shared with the fixed
  sequence;
- three additional cutoff cases at $N=23,c=31$, with $P=4$ shared with the
  fixed mesh sequence.

Sixteen starts give 224 baseline localizations. Two preconditioner-control
interfaces add 32. At most 256 conditional continuations are permitted, for a
hard maximum of 512 localization stages.

### Spread and convergence ownership

The analysis keeps

$$
\Omega=\Omega_I+\widetilde\Omega,
\qquad
\widetilde\Omega=\Omega_D+\Omega_{OD}
$$

separate. $\Omega_I$ tracks represented-subspace and reciprocal-discretization
change; $\widetilde\Omega$ tracks the gauge-dependent localization objective.
Total spread remains reported but is not used alone to infer optimizer behavior.

For the finest fixed-embedding mesh pair $N=27\to31$ and cutoff pair
$P=5\to6$, both best and median converged-start summaries must satisfy:

- relative $\Omega_I$ change at most 1%;
- relative $\widetilde\Omega$ change at most 1%;
- unordered symmetry-matched center distance at most 0.01 cell;
- relative radius-18 hopping-tail change at most 10%;
- at least 75% of starts natively converged; and
- the best canonical basin has occupancy at least four and appears in both
  eight-start blocks.

A holdout check fits $a+b/N^2$ on $N=15,19,23,27$ and requires the $N=31$
prediction residual to be at most 1%. This is a finite-sequence diagnostic, not
an asymptotic theorem.

Fixed and balanced representations are compared only at common $N$. Their
difference remains an embedding result and is not merged with mesh error.

### Basin equivalence

Converged endpoints are compared using:

- $\widetilde\Omega$;
- active-plane centers under orbital permutation, lattice wrapping, and all
  eight $D_4$ operations; and
- matched active-plane real-space density distance on the common grid.

The proposed tolerances are $10^{-6}a^2$ in $\widetilde\Omega$, $10^{-3}$ cell
in centers, and $10^{-5}$ in matched density $L^2$ mismatch. Before execution,
these values must be checked against reconstruction roundoff and exact
self-symmetry controls without looking at new basin outcomes.

**Post-execution record.** No retained record demonstrates that this check was
performed before execution. The omission is preserved as a protocol deviation;
it cannot be corrected retroactively. Subsequent offline exact-equivalence and
threshold-sensitivity controls are reported as post-hoc diagnostics only.

The resulting objects are called observed numerical basins. They do not exhaust
all stationary points or prove a global minimum.

### Represented diagnostics

The common finite-supercell estimator uses $1024^2$, justified by the completed
$256^2$--$1024^2$ refinement. Hopping comparisons use $R^2=8$ and 18, both
supported throughout the mesh sequence. Parent cutoff, reciprocal mesh,
auxiliary embedding, optimizer convergence, optimizer basin, hopping
truncation, serialization, and common-estimator errors remain separate.

## Storage and provenance

The earlier study duplicated large immutable interface files in every start
directory. The proposed driver instead writes `.eig`, `.mmn`, `.nnkp`, and
`.win` once per configuration and exposes retained symbolic links in each start
directory. Start-specific `.amn`, checkpoint, localization, unitary, hopping,
log, and resource files remain separate.

The existing native evidence tree and archive are never modified. A new output
root, manifest, compact extraction, checksum catalog, and local archive are
required. Public deposit remains a later separately authorized action.

## Proposed resource envelope

- local Wannier90 3.1.0 only;
- serial execution;
- expected normal runtime: 2--4 hours;
- hard total runtime: 8 hours;
- at most 600 seconds and 1 GiB resident memory per stage;
- at most 8 MiB per localization and 1.5 GiB total external output;
- no automatic retry or parameter change;
- stop on the first exceeded bound or unexpected interface ambiguity.

The preflight must update the expected runtime after dry preparation and static
size checks, without running localization.

## Required evidence package

A publication-facing completion package must contain:

1. frozen proposal and authorized execution input;
2. exact executable and script identities;
3. preprocessing and localization resource records;
4. every original and continuation endpoint;
5. spread-component and terminal-trace records;
6. symmetry- and density-aware basin assignments;
7. fixed and balanced mesh sequences;
8. cutoff and preconditioner controls;
9. best, median, and convergence-fraction diagnostics;
10. independent represented reconstruction;
11. figures, tables, limitations, and reproduction instructions;
12. compact repository checksums and a local native-evidence archive.

Passing software checks establishes only the declared numerical-verification
contracts. Scientific validation, material transferability, uncertainty
quantification, publication acceptance, and release remain separate.

## Decision boundary before execution

Execution requires a new durable checkpoint that presents:

- the generated exact 16-start table;
- validated restart semantics;
- preprocessing-only neighbor results for all 14 interfaces;
- the new external output root;
- updated runtime and storage estimates;
- final scripts and checksums; and
- the exact protected operation and stopping policy.

Until that checkpoint is explicitly authorized, the study remains proposed
work and no new Wannier90 process may start.
