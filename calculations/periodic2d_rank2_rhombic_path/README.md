# Periodic-2D rank-two rhombic path

**Status: development calculation; no retained execution**

This calculation context owns the unit-area continuous rhombic path between the
triangular and square metrics. The maintained strain coordinate runs from the
triangular metric to the square metric. The path is a controlled synthetic geometry
study, not an elastic, graphene, phase-stability, or material-strain model.

The context keeps its scientific operations separate:

- [`gauge_alignment/`](gauge_alignment/README.md) owns alignment operands and residuals;
- [`band_equivalence/`](band_equivalence/README.md) owns represented-operator and ordered-band comparisons;
- [`hopping_locality/`](hopping_locality/README.md) owns descriptive real-space hopping diagnostics;
- [`support_truncation/`](support_truncation/README.md) owns irreversible support selection; and
- [`band_equivalence_hopping_locality/`](band_equivalence_hopping_locality/README.md) owns the thin calculation composition and current development artifacts.

M0 geometry/frozen-response, M1 frozen represented response, M2 prescribed radial
response, qualification witnesses, and sampled transition scans remain distinct
channels. The aggregate directory may sequence these channels but does not merge their
scientific meanings or evidence claims.

The aggregate calculation owner contains the authoritative
[research protocol](band_equivalence_hopping_locality/protocol.md), actions, migration
record, and technical report. The former experiment-tree location is a legacy forward
pointer only. No calculation execution, retention, sealing, promotion, or publication is
authorized by this filesystem organization.
