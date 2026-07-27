back_to: [[ksdft2Effmass.computational.00]]
# Computational Stage 08: Reduced Impurity Hierarchies

## Objective

Decompose each validated atomistic impurity operator into nested model classes and identify the least complex model that preserves the selected operator, subspace, spectral, and observable quantities.

## Task Registry

| Task | Description | Prerequisites | Output | Initial state |
|---|---|---|---|---|
| [[ksdft2Effmass.computational.08.01.01|08.01.01]] | Implement spatial and orbital operator decomposition | `G01` | Decomposition library | Blocked |
| [[ksdft2Effmass.computational.08.01.02|08.01.02]] | Implement scalar, orbital, onsite, hopping, and range-restricted model classes | `08.01.01` | Model-class library | Blocked |
| [[ksdft2Effmass.computational.08.01.03|08.01.03]] | Implement projection or fitting into each model class | `08.01.02`, `01.03.01` | Reduction engine | Blocked |
| [[ksdft2Effmass.computational.08.02.01|08.02.01]] | Construct the phosphorus model hierarchy | `08.01.03`, `G06` | P reduced operators | Blocked |
| [[ksdft2Effmass.computational.08.02.02|08.02.02]] | Solve and validate every phosphorus model level | `08.02.01` | P acceptance table | Blocked |
| [[ksdft2Effmass.computational.08.02.03|08.02.03]] | Select the minimal phosphorus model | `08.02.02` | `PMinimalModel-v1` | Blocked |
| [[ksdft2Effmass.computational.08.03.01|08.03.01]] | Construct the boron model hierarchy | `08.01.03`, `G07` | B reduced operators | Blocked |
| [[ksdft2Effmass.computational.08.03.02|08.03.02]] | Solve and validate every boron model level | `08.03.01` | B acceptance table | Blocked |
| [[ksdft2Effmass.computational.08.03.03|08.03.03]] | Select the minimal boron model | `08.03.02` | `BMinimalModel-v1` | Blocked |
| [[ksdft2Effmass.computational.08.04.01|08.04.01]] | Compare donor and acceptor reduction hierarchies | `08.02.03`, `08.03.03` | Comparative reduction record | Blocked |

## Acceptance Vector

Each model level is evaluated using

$$
\boldsymbol{\varepsilon}_{m,d}
=
\left(
\varepsilon_{H,m,d},
\varepsilon_{\Pi,m,d},
\Delta E_{b,m,d},
1-F_{m,d}
\right),
$$

where $m$ identifies the model level and $d\in\{\mathrm P,\mathrm B\}$ identifies the dopant.

## Completion Gates `G08-P` and `G08-B`

Each dopant-specific gate passes when its minimal model has been selected. The minimal model is the least complex member of the nested hierarchy satisfying every prespecified tolerance. If no reduced model passes, the full atomistic operator remains the accepted model.

## Parallelization

The phosphorus and boron hierarchy calculations are independent after their corresponding impurity gates pass. The shared reduction engine must be frozen before comparing the two dopants.
