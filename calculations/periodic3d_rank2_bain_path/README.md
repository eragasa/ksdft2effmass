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

## Analysis order

This family follows the continuous rank-two path order in the shared
[periodic analysis order](../periodic/multiband/analysis-order.md):

1. qualify the unit-volume path, FCC/BCC endpoint identities, common-cell map, offsets,
   oriented bonds, reciprocal convention, and common state space;
2. analyze M0 geometry-only/frozen-gauge locality;
3. analyze M1 frozen four-state response;
4. analyze M2 prescribed radial response separately;
5. evaluate channel-specific alignment, Fourier/locality, support, and separate error
   operands;
6. evaluate qualification witnesses;
7. apply only the declared sampled scan and transition-refinement rule;
8. independently verify each source channel and derived scan; and
9. render response and scan views from admitted stored data.

A missing or failed source gate blocks dependent scan interpretation. No channel is
elastic, phase-stability, martensitic, silicon, or material evidence.

The former experiment-tree location is a legacy forward pointer only. No execution,
retention, sealing, promotion, or publication is authorized by this organization.
