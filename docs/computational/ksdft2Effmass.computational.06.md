back_to: [[ksdft2Effmass.computational.00]]
# Computational Stage 06: Phosphorus Impurity Operator

## Objective

Construct a converged, aligned, and spatially resolved first-principles impurity operator for substitutional phosphorus in silicon.

## Task Registry

| Task | Description | Prerequisites | Output | Initial state |
|---|---|---|---|---|
| [[ksdft2Effmass.computational.06.01.01\|06.01.01]] | Construct the P:Si specialization gate | `G01` | P:Si specialization gate | Blocked |
| [[ksdft2Effmass.computational.06.01.02\|06.01.02]] | Define the phosphorus supercell sequence | `06.01.01`, `G02` | Finite-size study design | Blocked |
| [[ksdft2Effmass.computational.06.01.03\|06.01.03]] | Run relaxed or fixed-geometry P:Si calculations | `06.01.02` | Doped first-principles datasets | Blocked |
| [[ksdft2Effmass.computational.06.02.01\|06.02.01]] | Construct P:Si Wannier operators | `06.01.03`, `G03` | Doped Wannier candidates | Blocked |
| [[ksdft2Effmass.computational.06.02.02\|06.02.02]] | Validate doped subspaces and Wannier representations | `06.02.01` | Doped Wannier validation records | Blocked |
| [[ksdft2Effmass.computational.06.03.01\|06.03.01]] | Align bulk and P:Si operators | `06.02.02`, `G05` | Aligned operator pairs | Blocked |
| [[ksdft2Effmass.computational.06.03.02\|06.03.02]] | Extract $\Delta\mathbf{H}_{\mathrm W,\mathrm P}$ | `06.03.01` | Impurity-operator sequence | Blocked |
| [[ksdft2Effmass.computational.06.03.03\|06.03.03]] | Test supercell, gauge, and alignment convergence | `06.03.02` | Impurity convergence record | Blocked |
| [[ksdft2Effmass.computational.06.03.04\|06.03.04]] | Freeze the phosphorus impurity operator | `06.03.03` | `PImpurityOperator-v1` | Blocked |

## Extraction

The principal output is

$$
\Delta\mathbf{H}_{\mathrm W,\mathrm P}
=
\overline{\mathbf{H}}_{\mathrm W,\mathrm P}
-
\mathbf{U}_{\mathrm P}
\overline{\mathbf{H}}_{\mathrm W,\mathrm b}
\mathbf{U}_{\mathrm P}^{\dagger}.
$$

Every term must include the basis, geometry, energy reference, and alignment metadata required to reproduce the subtraction.

## Completion Gate `G06`

The gate passes when the spatial blocks of $\Delta\mathbf{H}_{\mathrm W,\mathrm P}$ are stable within stated tolerances and periodic-image contamination has been quantified.

