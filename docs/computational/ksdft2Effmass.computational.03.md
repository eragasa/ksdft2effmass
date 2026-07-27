back_to: [[ksdft2Effmass.computational.00]]
# Computational Stage 03: Bulk-Silicon Wannier Operator

## Objective

Construct a localized representation of the selected bulk-silicon Kohn--Sham subspace and freeze a validated real-space Wannier Hamiltonian.

## Task Registry

| Task | Description | Prerequisites | Output | Initial state |
|---|---|---|---|---|
| [[ksdft2Effmass.computational.03.01.01|03.01.01]] | Define the target band-edge subspace | `G02` | Target-subspace specification | Blocked |
| [[ksdft2Effmass.computational.03.01.02|03.01.02]] | Select initial orbital projections | `03.01.01` | Projection set | Blocked |
| [[ksdft2Effmass.computational.03.01.03|03.01.03]] | Scan outer and frozen disentanglement windows | `03.01.01`, `03.01.02` | Window-sensitivity dataset | Blocked |
| [[ksdft2Effmass.computational.03.02.01|03.02.01]] | Construct candidate Wannier Hamiltonians | `03.01.03` | Candidate operator records | Blocked |
| [[ksdft2Effmass.computational.03.02.02|03.02.02]] | Validate interpolation, centers, spreads, and hopping decay | `03.02.01`, `01.03.01` | Wannier validation records | Blocked |
| [[ksdft2Effmass.computational.03.02.03|03.02.03]] | Freeze the reference Wannier operator | `03.02.02` | `BulkSiWannier-v1` | Blocked |

## Required Validation

The selected construction must be assessed using:

$$
\varepsilon_{\mathrm{interp}},
\qquad
\Omega_{\mathrm{spread}},
\qquad
\varepsilon_{\mathrm{edge}},
\qquad
\left\|
\mathbf{H}_{\mathrm W}(\mathbf{R})
\right\|_{\mathrm F}.
$$

These quantities respectively measure interpolation error, total Wannier spread, band-edge errors, and the spatial decay of the real-space Hamiltonian blocks.

## Completion Gate `G03`

The gate passes when the retained subspace, gauge-construction procedure, interpolation domain, and real-space truncation status are explicit and reproducible.

## Parallelization

Projection and window scans may run concurrently after the target subspace is fixed. Candidate constructions must be compared using the same validation grid.

