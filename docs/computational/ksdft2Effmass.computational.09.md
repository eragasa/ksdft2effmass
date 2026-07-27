back_to: [[ksdft2Effmass.computational.00]]
# Computational Stage 09: Continuum Reduction and Crossover

## Objective

Construct multichannel effective-mass solvers, embed their operators into the atomistic comparison space, and determine the atomistic-to-continuum crossover for each dopant.

## Task Registry

| Task | Description | Prerequisites | Output | Initial state |
|---|---|---|---|---|
| [[ksdft2Effmass.computational.09.01.01|09.01.01]] | Extract bulk band-edge tensors and channel data | `G02` | Continuum host parameters | Blocked |
| [[ksdft2Effmass.computational.09.01.02|09.01.02]] | Implement and verify the multivalley donor solver | `G01` | Donor continuum solver | Blocked |
| [[ksdft2Effmass.computational.09.01.03|09.01.03]] | Implement and verify the multiband acceptor solver | `G01` | Acceptor continuum solver | Blocked |
| [[ksdft2Effmass.computational.09.01.04|09.01.04]] | Implement screened Coulomb and central-cell model families | `09.01.02`, `09.01.03` | Continuum impurity library | Blocked |
| [[ksdft2Effmass.computational.09.02.01|09.02.01]] | Construct the continuum-to-Wannier embedding | `G03`, `09.01.01` | Embedding operator | Blocked |
| [[ksdft2Effmass.computational.09.02.02|09.02.02]] | Verify the embedding using synthetic envelopes | `09.02.01`, `01.03.02` | Embedding validation record | Blocked |
| [[ksdft2Effmass.computational.09.03.01|09.03.01]] | Compute phosphorus exterior and cross-coupling errors | `09.01.04`, `09.02.02`, `08.02.03` | P spatial-error curves | Blocked |
| [[ksdft2Effmass.computational.09.03.02|09.03.02]] | Determine $r_{c,\mathrm P}$ | `09.03.01` | P crossover record | Blocked |
| [[ksdft2Effmass.computational.09.03.03|09.03.03]] | Validate phosphorus bound states | `09.03.02` | P continuum validation | Blocked |
| [[ksdft2Effmass.computational.09.04.01|09.04.01]] | Compute boron exterior and cross-coupling errors | `09.01.04`, `09.02.02`, `08.03.03` | B spatial-error curves | Blocked |
| [[ksdft2Effmass.computational.09.04.02|09.04.02]] | Determine $r_{c,\mathrm B}$ | `09.04.01` | B crossover record | Blocked |
| [[ksdft2Effmass.computational.09.04.03|09.04.03]] | Validate boron bound states | `09.04.02` | B continuum validation | Blocked |

## Early Parallel Work

Tasks `09.01.02`--`09.01.04` may begin immediately after `G01` using analytic and synthetic potentials. Their completion does not establish a first-principles continuum reduction.

## Completion Gates `G09-P` and `G09-B`

For each dopant, the corresponding gate reports either:

$$
r_{c,d}<+\infty,
$$

with its tolerance and uncertainty, or

$$
r_{c,d}=+\infty,
$$

when no tested radius satisfies the exterior and cross-coupling criteria.
