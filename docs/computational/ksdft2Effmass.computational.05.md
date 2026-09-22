back_to: [[ksdft2Effmass.computational.00]]
# Computational Stage 05: Alignment and Common Comparison Spaces

## Objective

Construct reproducible state-space identifications between independently generated projected or Wannier operators and quantify their dependence on gauge, windows, geometry, and numerical choices.

## Task Registry

| Task | Description | Prerequisites | Output | Initial state |
|---|---|---|---|---|
| [[ksdft2Effmass.computational.05.01.01\|05.01.01]] | Implement overlap and principal-angle diagnostics on synthetic subspaces | accepted `01.02.01` and required `01.03.01` metrics | Alignment diagnostics contributing to `G01b` | Blocked |
| [[ksdft2Effmass.computational.05.01.02\|05.01.02]] | Implement polar and Procrustes alignment | `05.01.01` | Alignment-map constructor | Blocked |
| [[ksdft2Effmass.computational.05.01.03\|05.01.03]] | Verify exact recovery on controlled gauge transformations | `05.01.02`, `01.03.02` | Synthetic gauge-validation record | Blocked |
| [[ksdft2Effmass.computational.05.02.01\|05.02.01]] | Define common supercell and orbital indexing conventions | `G03` | Comparison-space specification | Blocked |
| [[ksdft2Effmass.computational.05.02.02\|05.02.02]] | Test alignment on independently generated bulk Wannier operators | `05.01.03`, `05.02.01` | First-principles alignment dataset | Blocked |
| [[ksdft2Effmass.computational.05.02.03\|05.02.03]] | Quantify sensitivity to windows, projections, and localization | `05.02.02` | Alignment-sensitivity record | Blocked |
| [[ksdft2Effmass.computational.05.02.04\|05.02.04]] | Freeze the alignment protocol | `05.02.03` | `AlignmentProtocol-v1` | Blocked |

## Accepted marking `G05`

The G05 accepted marking requires an alignment-protocol token containing:

$$
\mathbf{U},
\qquad
\{\theta_j\},
\qquad
\varepsilon_{\mathrm{overlap}},
\qquad
\varepsilon_{\mathrm g},
$$

where $\mathbf{U}$ is the finite-dimensional alignment matrix, $\theta_j$ are principal angles, $\varepsilon_{\mathrm{overlap}}$ measures subspace mismatch, and $\varepsilon_{\mathrm g}$ measures gauge-equivariance error.

## Parallelization

Tasks `05.01.01`--`05.01.03` are independent of first-principles production and should proceed in parallel with Stages `02` and `03`.

