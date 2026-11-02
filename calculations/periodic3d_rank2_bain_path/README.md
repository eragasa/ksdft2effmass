# Periodic-3D rank-two Bain path

**Status: implemented replaceable calculation actions; no retained execution**

This calculation context owns the unit-primitive-volume controlled Bain path between FCC
and BCC metric endpoints in the declared common body-centered-tetragonal coordinate
system. The path is a synthetic geometry and response control. It is not an elastic,
phase-stability, martensitic-transition, silicon, or material-strain calculation.

The context separates its scientific operations:

- [`gauge_alignment/`](gauge_alignment/README.md);
- [`frame_transport/`](frame_transport/README.md);
- [`band_equivalence/`](band_equivalence/README.md);
- [`hopping_locality/`](hopping_locality/README.md);
- [`support_truncation/`](support_truncation/README.md); and
- [`band_equivalence_hopping_locality/`](band_equivalence_hopping_locality/README.md),
  which owns the authoritative protocol, thin aggregate M0/M1/M2/scan composition,
  replaceable outputs, migration record, and technical report.

M0 geometry/frozen-gauge locality, M1 frozen four-state response, M2 prescribed radial
response, qualification witnesses, and sampled transition scans remain distinct
channels. The aggregate may sequence them but does not merge their meanings or claims.

The former experiment-tree location is a legacy forward pointer only. No execution,
retention, sealing, promotion, or publication is authorized by this organization.
