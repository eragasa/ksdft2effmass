back_to: [[ksdft2Effmass.computational.00]]
# Computational Stage 04: Tight-Binding Reductions

## Objective

Construct direct DFT-to-tight-binding and Wannier-to-tight-binding reductions within the same prescribed model class and compare them on common validation data.

## Task Registry

| Task | Description | Prerequisites | Output | Initial state |
|---|---|---|---|---|
| [[ksdft2Effmass.computational.04.01.01\|04.01.01]] | Implement the orthogonal $sp^3s^*$ Slater--Koster model | `G01a` | Executable TB operator | Blocked |
| [[ksdft2Effmass.computational.04.01.02\|04.01.02]] | Verify Hermiticity, symmetry, and limiting cases | `04.01.01`, `01.03.02` | TB regression record | Blocked |
| [[ksdft2Effmass.computational.04.02.01\|04.02.01]] | Define training and withheld validation sets | `G02` | Frozen fitting datasets | Blocked |
| [[ksdft2Effmass.computational.04.02.02\|04.02.02]] | Fit the direct DFT-to-TB model | `04.01.02`, `04.02.01` | `DirectTB-v1` | Blocked |
| [[ksdft2Effmass.computational.04.03.01\|04.03.01]] | Align the Wannier and TB orbital spaces | `G03`, `04.01.02` | Common operator representation | Blocked |
| [[ksdft2Effmass.computational.04.03.02\|04.03.02]] | Fit or project the Wannier-to-TB model | `04.03.01` | `WannierTB-v1` | Blocked |
| [[ksdft2Effmass.computational.04.04.01\|04.04.01]] | Apply common bulk validation metrics | `04.02.02`, `04.03.02` | Comparative validation record | Blocked |
| [[ksdft2Effmass.computational.04.04.02\|04.04.02]] | Freeze the accepted model class and parameters | `04.04.01` | `BulkTBReference-v1` | Blocked |

## Parallel Routes

The direct route

$$
\mathrm{DFT}
\longrightarrow
\mathrm{TB}
$$

may begin after `G02`, while the operator-mediated route

$$
\mathrm{DFT}
\longrightarrow
\mathrm{Wannier}
\longrightarrow
\mathrm{TB}
$$

waits for `G03`.

## Accepted marking `G04`

Before comparison, `join_common_parent_results` must bind direct and
Wannier-derived result tokens with:

- the same accepted Kohn–Sham parent dataset and source manifest;
- compatible physical, numerical, pseudopotential-set, and workflow schema versions;
- explicit compatible energy and representation metadata for every requested metric;
- verified artifact and manifest lineage;
- accepted branch-specific validation states.

Two completed branch tokens are insufficient. After this provenance-compatible
join, the G04 accepted marking requires typed evidence from both models reporting:

- model parameters and constraints;
- training objective and weights;
- withheld validation errors;
- indirect gap and valley-position errors;
- longitudinal and transverse effective-mass errors;
- operator residuals where a common operator representation exists;
- parameter and model-class sensitivity.

