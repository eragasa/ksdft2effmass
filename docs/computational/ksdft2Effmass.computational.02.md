back_to: [[ksdft2Effmass.computational.00]]
# Computational Stage 02: Bulk-Silicon First-Principles Reference

## Objective

Construct one converged and frozen Kohn--Sham reference for bulk silicon from which all Wannier, tight-binding, impurity, and continuum parameters are derived.

## Bootstrap relationship

Production Stage 02 begins only after the simulation bootstrap has demonstrated
the required execution, artifact, and extraction boundaries using non-production
tutorial calculations. The bootstrap does not satisfy the Stage 02 convergence
or production-authorization gates.

## SCF parent and sampled child calculations

The production SCF calculation determines the accepted parent density
$n_{\mathrm{SCF}}(\mathbf r)$ and corresponding effective Kohn--Sham operator
$\hat H_{\mathrm{KS}}[n_{\mathrm{SCF}}]$. Its mesh is selected to converge the
density, total energy, and every parent quantity required by the numerical
specification. Subsequent NSCF and band calculations reuse that fixed parent but
sample different wavevector sets: uniform or targeted meshes for integration and
state extraction, symmetry paths for dispersion, and valley-resolved points for
curvature and effective masses. Sharing the parent potential does not make these
children interchangeable.

G02 owns only the path, valley, effective-mass, and other diagnostic children
needed for bulk validation. Stage 03 separately chooses the retained bands,
projections, windows, and uniform NSCF mesh needed by Wannier90. Each child must
identify the same accepted SCF parent manifest while retaining its own mesh,
band count, purpose, convergence evidence, and energy-reference convention.

## Task Registry

| Task | Description | Prerequisites | Output | Initial state |
|---|---|---|---|---|
| [[ksdft2Effmass.computational.02.01.01\|02.01.01]] | Construct and verify the primitive-cell input | `G01a` | Verified silicon input | Blocked |
| [[ksdft2Effmass.computational.02.01.02\|02.01.02]] | Converge kinetic-energy and charge-density cutoffs | `02.01.01` | Cutoff convergence record | Blocked |
| [[ksdft2Effmass.computational.02.01.03\|02.01.03]] | Converge the Brillouin-zone sampling | `02.01.02` | $\mathbf{k}$-mesh convergence record | Blocked |
| [[ksdft2Effmass.computational.02.01.04\|02.01.04]] | Determine or freeze the lattice geometry | `02.01.03` | Frozen bulk geometry | Blocked |
| [[ksdft2Effmass.computational.02.02.01\|02.02.01]] | Run the production SCF parent and bulk-validation NSCF calculations | `02.01.04` | SCF parent and validation spectra | Blocked |
| [[ksdft2Effmass.computational.02.02.02\|02.02.02]] | Extract band edges, valley positions, and effective masses | `02.02.01` | Bulk validation record | Blocked |
| [[ksdft2Effmass.computational.02.02.03\|02.02.03]] | Freeze the bulk reference dataset | `02.02.02` | `BulkSiReference-v1` | Blocked |

## Convergence Order

The convergence sequence is

$$
\text{basis cutoffs}
\longrightarrow
\mathbf{k}\text{-point sampling}
\longrightarrow
\text{geometry}
\longrightarrow
\text{production electronic structure}.
$$

Each convergence study must evaluate the quantities used later, rather than total energy alone. SCF convergence of the code-specific iterative criterion is distinct from convergence with respect to cutoffs, wavevector sampling, bands, geometry, and the downstream observable.

## Accepted marking `G02`

The `G02` marking is accepted only when `BulkSiReference-v1` and its typed evidence tokens contain:

- input and output manifests;
- converged crystal geometry;
- accepted SCF parent density and manifest;
- path, valley, effective-mass, or other diagnostic NSCF data required for bulk validation;
- high-symmetry and valley-resolved band data;
- band-edge energies, valley position, and effective masses;
- convergence uncertainties for the retained observables.

The G02 marking does not contain or predict the Wannier-compatible uniform-grid
NSCF child. Stage 03 selects and owns that child after its retained bands,
projections, outer/inner windows, and uniform grid are approved. The Stage 03
child token must reference this accepted G02 SCF parent manifest. Meeting notes
or unmanifested historical calculations cannot supply an accepted G02 token.

## Parallelization

Workflow scripts and observable-extraction code may be developed before `G01a`,
but production results cannot be accepted until G01a and the common
specifications and validation records are accepted. A real QE run additionally
requires the separate production-environment authorization checkpoint.

