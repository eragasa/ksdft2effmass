back_to: [[ksdft2Effmass.computational.00]]
# Computational Stage 02: Bulk-Silicon First-Principles Reference

## Objective

Construct one converged and frozen Kohn--Sham reference for bulk silicon from which all Wannier, tight-binding, impurity, and continuum parameters are derived.

## Task Registry

| Task | Description | Prerequisites | Output | Initial state |
|---|---|---|---|---|
| [[ksdft2Effmass.computational.02.01.01|02.01.01]] | Construct and verify the primitive-cell input | `G01` | Verified silicon input | Blocked |
| [[ksdft2Effmass.computational.02.01.02|02.01.02]] | Converge kinetic-energy and charge-density cutoffs | `02.01.01` | Cutoff convergence record | Blocked |
| [[ksdft2Effmass.computational.02.01.03|02.01.03]] | Converge the Brillouin-zone sampling | `02.01.02` | $\mathbf{k}$-mesh convergence record | Blocked |
| [[ksdft2Effmass.computational.02.01.04|02.01.04]] | Determine or freeze the lattice geometry | `02.01.03` | Frozen bulk geometry | Blocked |
| [[ksdft2Effmass.computational.02.02.01|02.02.01]] | Run production SCF and NSCF calculations | `02.01.04` | Production wavefunctions and eigenvalues | Blocked |
| [[ksdft2Effmass.computational.02.02.02|02.02.02]] | Extract band edges, valley positions, and effective masses | `02.02.01` | Bulk validation record | Blocked |
| [[ksdft2Effmass.computational.02.02.03|02.02.03]] | Freeze the bulk reference dataset | `02.02.02` | `BulkSiReference-v1` | Blocked |

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

Each convergence study must evaluate the quantities used later, rather than total energy alone.

## Completion Gate `G02`

`BulkSiReference-v1` must contain:

- input and output manifests;
- converged crystal geometry;
- SCF charge density;
- dense-grid NSCF eigenvalues and wavefunctions;
- high-symmetry and valley-resolved band data;
- band-edge energies, valley position, and effective masses;
- convergence uncertainties for the retained observables.

## Parallelization

Workflow scripts and observable-extraction code may be developed before `G01`, but production results cannot be accepted until the common specifications and validation records are available.

