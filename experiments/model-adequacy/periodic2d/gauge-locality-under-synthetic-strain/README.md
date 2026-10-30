# 2-D gauge locality under synthetic rhombic strain

Identity: `ksdft2effmass.campaign.model-adequacy.periodic2d.gauge-locality-under-synthetic-strain`

This family specializes the [shared strain protocol](../../gauge-locality-under-synthetic-strain.md)
and has a matching [architecture bundle](../../../../docs/architecture/v2/experiments/model-adequacy/periodic2d/gauge-locality-under-synthetic-strain/index.md).
to the unit-area triangular-to-square-metric rhombic path. The initial action is the M0
flat-parent frozen-gauge control only. Its square-metric endpoint retains the strained
three-bond network and is not the existing square directed-hopping parent.

Replaceable outputs and executable composition are maintained by the
[calculation owner](../../../../calculations/periodic2d/rank2/strain-locality/); they are
not convergence or retained evidence. This experiment directory retains the identity,
scientific interpretation, and shared-protocol specialization rather than duplicate
entrypoints. The bounded M0
action preserves the normalized restricted residual
at `0.3418465443` and Parseval to `1.2e-16`. From the triangular to square-metric
endpoint, the first radius at tail tolerance `1e-5` changes from about `3.7224` to
`4.2426`, while the retained block count changes from `43` to `61`. This is a sampled
frozen-gauge geometry result, not a material strain result.

A separately labeled bounded M1/M2 smoke action exists at the calculation owner. M1's aligned
strain difference remains at roundoff. With the prospectively fixed synthetic M2 law
and `beta=1`, the square-metric endpoint has hopping responses from about `0.81758` to
`1.27146` and a maximum aligned retained-space perturbation of about
`0.063575 E_ref`. The M1 and M2 action is unconverged and has no retained-evidence
status; it writes replaceable development figures only.

## Ownership and migration ledger

This directory owns the experiment identity and protocol specialization. Executable
composition, analysis output paths, and migration notes are owned by
[`calculations/periodic2d/rank2/strain-locality/README.md`](../../../../calculations/periodic2d/rank2/strain-locality/README.md)
and [`migration.md`](../../../../calculations/periodic2d/rank2/strain-locality/migration.md).
