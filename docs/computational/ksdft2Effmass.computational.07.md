back_to: [[ksdft2Effmass.computational.00]]
# Computational Stage 07: Boron Impurity Operator

## Objective

Construct a converged first-principles impurity operator for substitutional boron in silicon while retaining the valence-band, orbital, degeneracy, and spin--orbit structure required by the acceptor problem.

## Task Registry

| Task | Description | Prerequisites | Output | Initial state |
|---|---|---|---|---|
| [[ksdft2Effmass.computational.07.01.01|07.01.01]] | Define charge, relaxation, spin, and spin--orbit conventions | `G01` | B:Si physical specification | Blocked |
| [[ksdft2Effmass.computational.07.01.02|07.01.02]] | Define the boron supercell and valence-subspace study | `07.01.01`, `G02` | Finite-size and subspace design | Blocked |
| [[ksdft2Effmass.computational.07.01.03|07.01.03]] | Run B:Si first-principles calculations | `07.01.02` | Doped first-principles datasets | Blocked |
| [[ksdft2Effmass.computational.07.02.01|07.02.01]] | Construct multiband B:Si Wannier operators | `07.01.03`, `G03` | Doped Wannier candidates | Blocked |
| [[ksdft2Effmass.computational.07.02.02|07.02.02]] | Validate degeneracies, orbital content, and spin--orbit structure | `07.02.01` | Doped subspace validation | Blocked |
| [[ksdft2Effmass.computational.07.03.01|07.03.01]] | Align bulk and B:Si operators | `07.02.02`, `G05` | Aligned operator pairs | Blocked |
| [[ksdft2Effmass.computational.07.03.02|07.03.02]] | Extract $\Delta\mathbf{H}_{\mathrm W,\mathrm B}$ | `07.03.01` | Impurity-operator sequence | Blocked |
| [[ksdft2Effmass.computational.07.03.03|07.03.03]] | Test supercell, gauge, and alignment convergence | `07.03.02` | Impurity convergence record | Blocked |
| [[ksdft2Effmass.computational.07.03.04|07.03.04]] | Freeze the boron impurity operator | `07.03.03` | `BImpurityOperator-v1` | Blocked |

## Branching Rule

Tasks `07.01.01` and `07.01.02` may begin while the phosphorus calculations are running. The production boron workflow should reuse the validated alignment and provenance protocols, but it must not assume that the phosphorus target subspace or scalar model class transfers unchanged.

## Completion Gate `G07`

The gate passes when the retained valence subspace and the extracted operator are stable against the numerical choices that affect degeneracy, orbital mixing, and spin--orbit splitting.

