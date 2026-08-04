back_to: [[ksdft2Effmass.computational.00]]
# Computational Stage 03: Bulk-Silicon Wannier Operator

## Objective

Construct a localized representation of the selected bulk-silicon Kohn--Sham subspace and freeze a validated real-space Wannier Hamiltonian.

## Task Registry

| Task | Description | Prerequisites | Output | Initial state |
|---|---|---|---|---|
| [[ksdft2Effmass.computational.03.01.01\|03.01.01]] | Define the target band-edge subspace | `G02` | Target-subspace specification | Blocked |
| [[ksdft2Effmass.computational.03.01.02\|03.01.02]] | Select initial orbital projections | `03.01.01` | Projection set | Blocked |
| [[ksdft2Effmass.computational.03.01.03\|03.01.03]] | Approve retained bands, projections, windows, and the uniform grid | `03.01.01`, `03.01.02` | Wannier-interface specification | Blocked |
| [[ksdft2Effmass.computational.03.01.04\|03.01.04]] | Run the Wannier-compatible uniform-grid NSCF child and QE–Wannier bridge | `03.01.03`, accepted G02 SCF parent manifest, production authorization | Wannier interface artifact set | Blocked |
| [[ksdft2Effmass.computational.03.02.01\|03.02.01]] | Construct candidate Wannier Hamiltonians | `03.01.04` | Candidate operator records | Blocked |
| [[ksdft2Effmass.computational.03.02.02\|03.02.02]] | Validate interpolation, centers, spreads, and hopping decay | `03.02.01`, `01.03.01` | Wannier validation records | Blocked |
| [[ksdft2Effmass.computational.03.02.03\|03.02.03]] | Freeze the reference Wannier operator | `03.02.02` | `BulkSiWannier-v1` | Blocked |

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

## Accepted marking `G03`

The G03 accepted marking exists when the retained subspace, gauge-construction procedure, interpolation domain, and real-space truncation status are explicit and reproducible.

## NSCF ownership and parallelization

G02 supplies the accepted SCF parent and bulk-validation spectra. Stage 03 owns
the Wannier-compatible uniform-grid NSCF child because its grid and retained
bands cannot be frozen until the target subspace, projections, and window
specification are approved. Task `03.01.04` must reference the accepted G02 SCF
parent-manifest token and may execute only after the separate production-environment
authorization checkpoint.

Projection and non-executing window/grid design may proceed after the target
subspace is fixed. Candidate constructions must consume the same accepted
interface artifact set and be compared on the same validation grid.

