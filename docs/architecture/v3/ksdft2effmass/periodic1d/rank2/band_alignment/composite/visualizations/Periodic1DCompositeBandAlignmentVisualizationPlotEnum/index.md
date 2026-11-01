# `Periodic1DCompositeBandAlignmentVisualizationPlotEnum`

The closed filename inventory contains six publication-facing render outputs:

1. `rank2-composite-alignment.png`;
2. `rank2-composite-recovery-controls.png`;
3. `rank2-composite-hopping-diagnostics.png`;
4. `rank2-composite-locality.png`;
5. `rank2-composite-error-channels.png`; and
6. `rank2-composite-error-trajectories.png`.

Enum ownership prevents callers from silently adding or renaming outputs. The hopping
diagnostic and retained-support figures remain separate even though they use the same
declared integer ranges.

## Related pages

- [Numerics](numerics.md)
- [Scientific contract](scientifics.md)
- [Mermaid schematic](schematics.md)
- [Owning module](../index.md)
