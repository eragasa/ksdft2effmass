# Rank-two hopping locality

`ksdft2effmass.periodic1d.rank2.hopping_locality` owns rank-two diagnostics of
unchanged real-space hopping coefficients. Its package initializer is an inert
namespace.

For the frozen band-alignment study,
`Periodic1DRank2HoppingLocalityAnalyzer` measures one channel's ordinary omitted-block
Frobenius $\ell^2$ norm outside every configured symmetric range. Like the rank-$N$
action, one request binds one alignment channel and the analysis retains a tuple of
`Periodic1DRank2HoppingTailResult` values. The action does not construct or expose
truncated operators. Its request and results are defined separately in `request.py` and
`result.py`. The request exposes a typed conjugate-closed ordinary translation
inventory, the configuration exposes a `Periodic1DHoppingDiagnosticRangeInventory`,
and every tail exposes one neutral `Periodic1DSymmetricTranslationRange`.
These index values carry no physical distance and do not imply support removal.

The older `Periodic1DRank2HoppingPower` value remains the authoritative per-displacement
comparison value consumed by the embedded-subspace band-equivalence study. Both values
belong to hopping locality, but they answer different retained-study questions.

The rank-two composite band-alignment calculation consumes the band-alignment locality
analysis and combines it with separate support-truncation consequences only when
assembling the established aggregate result wire.
