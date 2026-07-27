back_to: [[ksdft2Effmass.computational.00]]
# Computational Stage 10: Cross-Path Consistency

## Objective

Evaluate the representation dependence, path dependence, and error composition of the completed reduction workflows.

## Task Registry

| Task | Description | Prerequisites | Output | Initial state |
|---|---|---|---|---|
| [[ksdft2Effmass.computational.10.01.01|10.01.01]] | Measure Wannier and alignment gauge-equivariance defects | `G03`, `G05` | Gauge-consistency record | Blocked |
| [[ksdft2Effmass.computational.10.01.02|10.01.02]] | Compare direct and Wannier-mediated TB paths | `G04` | TB path-consistency record | Blocked |
| [[ksdft2Effmass.computational.10.02.01|10.02.01]] | Reduce extracted impurity operators | `G08-P` or `G08-B` | Extract-then-reduce outputs | Blocked |
| [[ksdft2Effmass.computational.10.02.02|10.02.02]] | Reduce parent operators before impurity extraction | `G06` or `G07`, `G04` | Reduce-then-extract outputs | Blocked |
| [[ksdft2Effmass.computational.10.02.03|10.02.03]] | Measure impurity extraction commutators | `10.02.01`, `10.02.02` | $\varepsilon_{\mathrm{ext},d}$ records | Blocked |
| [[ksdft2Effmass.computational.10.03.01|10.03.01]] | Measure error amplification under successive reductions | `G08-P` and `G09-P`, or `G08-B` and `G09-B` | Composition dataset | Blocked |
| [[ksdft2Effmass.computational.10.03.02|10.03.02]] | Fit or bound stagewise stability factors | `10.03.01` | Error-propagation rule | Blocked |
| [[ksdft2Effmass.computational.10.04.01|10.04.01]] | Determine the supported compositional claims | `10.01.01`, `10.01.02`, `10.02.03`, `10.03.02` | `CompositionalAssessment-v1` | Blocked |

## Primary Defects

The stage evaluates

$$
\varepsilon_{\mathrm g},
\qquad
\varepsilon_{\mathrm{path}}^{\mathrm{TB}},
\qquad
\varepsilon_{\mathrm{ext},d},
\qquad
\varepsilon_{\mathrm{comm}}.
$$

These quantities measure gauge dependence, disagreement between tight-binding routes, disagreement between impurity-extraction orders, and general path dependence.

## Completion Gate `G10`

The gate does not require every diagram to commute. It requires each tested diagram to have:

- precisely defined paths;
- aligned outputs;
- a stated norm and validation domain;
- a measured defect;
- an interpretation of the physical or numerical source of noncommutativity.
