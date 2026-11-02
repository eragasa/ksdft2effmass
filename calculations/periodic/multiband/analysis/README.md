# Multiband aggregation analysis

This directory may contain cross-calculation aggregation that consumes explicit outputs from the dimension- and rank-specific calculation owners. Its primary product is a traceable summary of salient results, not a new simulation. The shared
[`analysis-order.md`](../analysis-order.md) requires family qualification and independent
admission before cross-family aggregation.

Aggregation order is: authenticate each source and its evidence status; establish common
operands, units, basis/gauge/energy conventions, and normalization; compare only
compatible quantities; retain unavailable or unresolved dispositions; independently
check the derived projection; and render without recalculating any source family.

Permitted work includes:

- comparing compatible normalized quantities across calculation owners;
- assembling dimension-by-rank status and result tables;
- identifying missing controls or incompatible definitions;
- plotting already verified aggregate quantities; and
- documenting why a proposed comparison is unavailable.

It must not:

- rerun or silently redefine a subcalculation;
- consume unverified simulation output in a production analysis;
- pool incompatible alignment families or model classes;
- relabel development output as retained evidence;
- duplicate generated figures owned by a subcalculation; or
- infer material or continuum validity from controlled finite models.

No executable aggregation stage is added yet because the current subcalculations do not share a closed, verified machine-readable aggregation contract. [`salient-results.md`](salient-results.md) is therefore a source-linked human-readable status summary rather than a generated result.
