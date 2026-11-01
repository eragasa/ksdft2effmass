# Rank-two support truncation

`ksdft2effmass.periodic1d.rank2.support_truncation` owns irreversible symmetric support
removal and its consequences. Its package initializer is an inert namespace.

The embedded-subspace band-equivalence family continues to use the request, action, and
result definitions in `request.py`, `analysis.py`, and `results.py`. The frozen
band-alignment study uses the distinct inert `band_alignment/` specialization because
it binds different parent fields, meshes, and evidence.

Within that specialization, `Periodic1DRank2SupportTruncationAnalysisRequest`,
`Periodic1DRank2SupportTruncationAnalyzer`,
`Periodic1DRank2SupportTruncationAnalysis`, and `Periodic1DRank2SupportResult` mirror
the rank-$N$ naming and one-channel action scope. The analyzer consumes one
already-computed hopping-locality analysis, constructs each truncated ordinary model,
and retains construction total error plus evaluation truncation and total error
channels. It does not re-own or duplicate the unchanged omitted-block locality
diagnostic. Each consequence exposes both the neutral symmetric translation range used
to correlate it with locality and the distinct `SymmetricRangeSupport1D` policy that
identifies irreversible retained support. The frozen embedded-subspace family uses the
same `Periodic1DSymmetricSupportInventory` without changing its established request
fields. This support inventory is distinct from the hopping diagnostic inventory even
when their underlying neutral integer ranges coincide.

The composite calculation sequences this capability and merges its consequences with
the corresponding locality values during aggregate assembly. This ownership extraction
does not alter established aggregate result bytes.
