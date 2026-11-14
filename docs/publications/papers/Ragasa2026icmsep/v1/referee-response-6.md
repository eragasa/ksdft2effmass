# Response to continued technical review 6

## Bounded outcome

- **Review outcome:** `CHANGES_REQUIRED`
- **Operator request:** `NONE`

The manuscript-level mathematical, methodological, citation, and figure defects raised
in this review were corrected. Submission readiness remains blocked by the already
stated need for independent reconstruction and a public reproduction archive; this
response does not authorize either protected work or submission.

## Responses

### Rank-two theorem assumptions

**Disposition:** `NO_ACTION_REQUIRED` after revision

Appendix A now states the nonnegative invariant correlation term explicitly,
$b_0=\sum_i\alpha_i y(q_i)^2/E_{\rm ref}^2\ge0$, explains why the positive-scale
optimum is not clipped for the declared family, and records the alternative
$\lambda=0$ boundary for a negative maximal correlation. The residual--locality
identity is now explicitly restricted to a real-symmetric parent, real rotations, and
normalized continuum measure or uniform finite weights. The finite-mesh statement now
identifies the optimal constant with the unweighted zero Fourier block.

### Gauge-alignment implementation

**Disposition:** `NO_ACTION_REQUIRED` after revision

The Methods now describe the actual stacked-frame Procrustes construction, pointwise
polar alignment, reduced/Cartesian reciprocal coordinates, Givens-layer ordering and
sign convention, attack-angle functions, and the distinction from a quartic direct
matrix-conjugation optimization.

### Finite Fourier conversion

**Disposition:** `SAFE_TO_DEFER`

The exact 216-to-125 inventory and the 91 removed negative-Nyquist-boundary records are
reported. The retained result does not contain all 216 cyclic coefficient matrices or
the two scalar removed-power totals. The manuscript and Figure 15 caption now state this
archival omission directly rather than implying that the missing numerical totals are
available. Revisit only during the separately required independent Fourier
reconstruction; no values were inferred from the figure.

### Reproducibility details

**Disposition:** `NO_ACTION_REQUIRED` after revision

The revision records the 1D construction and evaluation meshes, shifted evaluation
coordinates, cutoff criteria, homotopy, silicon 408-point geometry, `wsvec` unfolding,
reciprocal-coordinate conventions, optimizer weights, starts, continuation rule,
on-site trace coupling, tie-breaking, Brillouin-zone folding, valley search boxes,
finite-difference steps, and the 52-point valence fit inventory.

### Effective-mass conversion and curvature reporting

**Disposition:** `NO_ACTION_REQUIRED` after revision

The curvature constant is now
$\hbar^2/m_e\simeq7.619964\ \mathrm{eV\,\AA^2}$, with explicit SI-to-eV/angstrom
conversion. The manuscript also clarifies the nonlinear cancellation that makes the
DOS-mass error nonmonotone and corrects the H-shell-10 wording to the reported maximum
principal and valence-channel changes.

### Upstream disentanglement/projectability limitation

**Disposition:** `NO_ACTION_REQUIRED` after revision

The Discussion now distinguishes logical error-channel separation from causal
independence and identifies over-constrained frozen-window disentanglement or limited
projectability as a plausible shared cause of parent-fidelity failure and long-range
Fourier tails. It explicitly states that no alternative window, `3d`-augmented trial
space, or projectability-disentangled source was constructed, so the mechanism remains
a future comparison rather than a result.

### Truncation ansatz limitation

**Disposition:** `NO_ACTION_REQUIRED` after revision

The near-full-support conclusion is now bounded to the tested whole-block
Bravais-shell family. Entrywise, orbital-pair-distance, orbital-channel, and
symmetry-constrained alternatives are named as untested comparison families.

### Citations and bibliography

**Disposition:** `NO_ACTION_REQUIRED` after revision

The bibliography and text now cite Quantum ESPRESSO updates, SSSP, automated and
projectability-based Wannier workflows, Wannier-derived tight binding, Slater--Koster
and semiconductor tight binding, symmetry-adapted/symmetrized Wannier models,
WannSymm, and Davis--Kahan invariant-subspace perturbation theory. The Pizzi entry was
corrected to `Bl\"ugel` and `G\'eranton`.

### Figures and terminology

**Disposition:** `NO_ACTION_REQUIRED` after revision

Layout-only immutable successors were rendered from retained machine-readable data:

- comprehensive band-edge `figures-v3/` separates legends from titles and increases
  conduction-mass panel spacing;
- literal witness `figures-v5/` moves the clipped `H00` annotation inside the axes.

The manuscript uses these successors, defines fit *half-window*, explains missing
positive-curvature hole-mass curves, and changes “provides a real tradeoff” to
“exhibits a real tradeoff.” No Hamiltonian, valley, Hessian, or optimization producer
was rerun.

### Table rounding

**Disposition:** `NO_ACTION_REQUIRED` after revision

The fidelity table now has a numbered caption and states that ratios are computed from
full binary64 records before displayed RMS values are rounded, explaining last-digit
discrepancies from division of the printed values.

### Internal lifecycle language

**Disposition:** `NO_ACTION_REQUIRED` after revision

The article now defines `unsealed`, provider eligibility, and typed verification in
plain scientific terms, and replaces the unexplained “Paper D” reference with an
earlier planned Slater--Koster study.

### Public repository and DOI

**Disposition:** `HUMAN_DECISION_REQUIRED`

The Data and code availability section now states that no public repository URL or DOI
currently contains the complete authenticated source data and reconstruction
environment. Public deposition remains mandatory before submission. Archive selection,
release scope, DOI creation, and publication authorization are human/protected
boundaries and were not performed here.

### Broader validation

**Disposition:** `SAFE_TO_DEFER`

The current retained evidence cannot support another semiconductor, an alternative
Wannier window, a `3d`-augmented basis, or an SOC source without new authorized
calculations. The manuscript now frames these as future robustness studies rather than
present evidence. Revisit when a separately authorized source-comparison campaign is
defined prospectively.

## Validation performed

- regenerated the layout-only figure successors with no-overwrite behavior;
- Ruff formatting and checks passed for the changed renderers;
- all manuscript citation keys resolve to bibliography entries;
- `latexmk` completed successfully with `biber`;
- no new QE, Wannier90, Hamiltonian construction, optimization, valley search, Hessian,
  or frozen-confirmation calculation was run.
