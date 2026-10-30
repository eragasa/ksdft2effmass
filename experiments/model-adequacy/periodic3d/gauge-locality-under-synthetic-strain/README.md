# 3-D gauge locality under a synthetic Bain strain

Identity: `ksdft2effmass.campaign.model-adequacy.periodic3d.gauge-locality-under-synthetic-strain`

This family specializes the [shared strain protocol](../../gauge-locality-under-synthetic-strain.md)
and has a matching [architecture bundle](../../../../docs/architecture/v2/experiments/model-adequacy/periodic3d/gauge-locality-under-synthetic-strain/index.md).
to the unit-primitive-volume FCC-to-BCC Bain path. The initial action is the M0
flat-parent frozen-gauge control in a common body-centered-tetragonal primitive basis.
It is not a material phase-transition calculation. The shared protocol now fixes and
software-verifies the unimodular FCC-to-Bain common-cell map. The diamond-inspired M1
parent remains a bounded synthetic control rather than a material model. Its separate
M1/M2 action remains gated on convergence, independent reconstruction, and
retained-evidence authority.

Outputs under `analysis/development/` are replaceable figures, not convergence or
retained evidence. They are intentionally excluded from source integration and can be
recreated by the maintained constructor-bound actions. The retired calculation-local
workflow schemas are not evidence contracts for this active experiment. The bounded M0
action preserves the normalized restricted residual
at `0.1855624448` with zero stored Parseval defect at binary64 precision. From the FCC
to BCC endpoint, the first radius at tail tolerance `1e-5` changes from about `2.9698`
to `3.2734`, while the retained block count changes from `135` to `169`. At tolerance
`1e-3`, the radius is nonmonotone even though the block count rises. These are sampled
frozen-gauge geometry diagnostics, not a material transition result.

A separately labeled bounded M1/M2 smoke action now exists under
[`analysis/response-development/`](analysis/response-development/). M1's aligned
strain difference remains at roundoff. With the prospectively fixed synthetic M2 law
and `beta=1`, the BCC endpoint has a common selected-bond response of about `0.97564`
and a maximum aligned retained-space perturbation of about `0.007289 E_ref`. The M1 and
M2 action is unconverged and has no retained-evidence status; it writes replaceable
development figures only.

## Ownership and migration ledger

This directory owns the experiment composition and analysis entrypoints. Companion
calculation-output inventory and migration notes remain in
[`calculations/periodic3d/rank2/strain-locality/README.md`](../../../../calculations/periodic3d/rank2/strain-locality/README.md)
and [`migration.md`](../../../../calculations/periodic3d/rank2/strain-locality/migration.md).
