# 3-D gauge locality under a synthetic Bain strain

Identity: `ksdft2effmass.campaign.model-adequacy.periodic3d.gauge-locality-under-synthetic-strain`

This family specializes the [shared strain protocol](../../gauge-locality-under-synthetic-strain.md)
and has a matching [architecture bundle](../../../../docs/architecture/v2/experiments/model-adequacy/periodic3d/gauge-locality-under-synthetic-strain/index.md).
to the unit-primitive-volume FCC-to-BCC Bain path. The initial action is the M0
flat-parent frozen-gauge control in a common body-centered-tetragonal primitive basis.
It is not a material phase-transition calculation. The shared protocol now fixes and
software-verifies the unimodular FCC-to-Bain common-cell map. The diamond-inspired M1
parent remains a bounded synthetic control rather than a material model. Its separate
M1/M2 action now has strict packaged result schemas but remains gated on convergence,
independent reconstruction, and retained-evidence authority.

Outputs under `analysis/development/` are replaceable diagnostics, not convergence or
retained evidence. Generated JSON and figures are intentionally excluded from this
source integration and can be recreated by the maintained actions. The M0 JSON is canonically encoded and validated against the strict
packaged `synthetic-strain-m0-result.v1` schema; this establishes the wire contract,
not independent scientific verification. The bounded M0 action preserves the normalized restricted residual
at `0.1855624448` with zero stored Parseval defect at binary64 precision. From the FCC
to BCC endpoint, the first radius at tail tolerance `1e-5` changes from about `2.9698`
to `3.2734`, while the retained block count changes from `135` to `169`. At tolerance
`1e-3`, the radius is nonmonotone even though the block count rises. These are sampled
frozen-gauge geometry diagnostics, not a material transition result.

A separately labeled bounded M1/M2 smoke action now exists under
[`analysis/response-development/`](analysis/response-development/). M1's aligned
strain difference remains at roundoff. With the prospectively fixed synthetic M2 law
and `beta=1`, the BCC endpoint has a common selected-bond response of about `0.97564`
and a maximum aligned retained-space perturbation of about `0.007289 E_ref`. The M1 and M2 JSON documents are canonically encoded and validated against distinct
strict packaged v1 schemas. The action is unconverged and has no retained-evidence
status.
