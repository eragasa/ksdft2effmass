# Rank-two band alignment

The rank-two band-alignment namespace owns the frozen four-state study configuration and
its composite calculation. The configuration is shared study input; the
`composite/` child owns orchestration, aggregate result bytes, independent verification,
and authenticated visualization.

Gauge selection is consumed from the sibling `rank2/gauge_alignment/` capability.
Hopping locality and support truncation remain separate rank-first capabilities and are
not redefined by the composite namespace.

- [Configuration](configuration/index.md)
- [Composite study](composite/index.md)
