# Post-S110 Level 1 foundation disposition

Status: `implemented-software-verification-only`.

The separately continued Level 1 work extracted the reusable Slater--Koster foundation
from calculation-owned scripts into
`python/src/ksdft2effmass/model_systems/slater_koster/`. The supported surface now owns:

- the spinless ten-orbital homopolar diamond $sp^3s^*$ Hamiltonian;
- the exact right-handed primitive geometry and full-center Bloch phase convention;
- complete first- and second-neighbor shell maps;
- the declared 15-entry real eV parameter inventory, with first-neighbor $ss^*$ and
  $s^*s^*$ channels structurally fixed to zero;
- exact-Hermitian assembly and synthetic time-reversal, reciprocal-covariance, and
  cubic-symmetry checks; and
- deterministic model-definition serialization through the maintained KSD typed-JSON
  boundary.

The architecture contract is documented at
[`docs/architecture/v3/ksdft2effmass/model_systems/slater_koster/`](../../../../../docs/architecture/v3/ksdft2effmass/model_systems/slater_koster/index.md).
Focused synthetic software-verification tests are under
`python/tests/ksdft2effmass/model_systems/slater_koster/`.

This disposition does not revise the failed S110 alignment result. It produced no fit,
parameter vector, Slater--Koster reduction, prediction freeze, or model-adequacy claim.
It consumed no 408-point or 402-point parent values and invoked no calculator. Level 2
spectral-only feasibility and every later continuation level remain unauthorized by
this disposition. S50 remains blocked.
