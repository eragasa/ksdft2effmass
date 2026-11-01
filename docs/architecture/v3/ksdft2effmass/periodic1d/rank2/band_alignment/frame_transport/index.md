# Rank-two frame transport

`ksdft2effmass.periodic1d.rank2.band_alignment.frame_transport` owns the rank-two
specialization that binds the frozen study configuration to one raw orthonormal frame
path and constructs its closed polar-transported gauge.

The capability retains the transported path, the minimum neighbor-or-closure overlap
singular value, and the ordered closure-unitary eigenphases. These are finite-mesh
transport diagnostics. They are not continuum isolation certificates or gauge-alignment
results.

The package initializer is an inert namespace. Consumers import the request, action, and
result directly from their defining modules:

- `frame_transport.request.Periodic1DRank2TransportAnalysisRequest`
- `frame_transport.analysis.Periodic1DRank2TransportAnalyzer`
- `frame_transport.result.Periodic1DRank2ResolvedTransportAnalysis`

These names mirror the rank-$N$ transport request, analyzer, and resolved-analysis
vocabulary. Rank two has no retained typed backend-failure branch, so it does not
manufacture the rank-$N$ failed-analysis variant.

The rank-two composite calculation sequences this capability before applying the known
gauge attack. Composite orchestration does not own the transport operation or its
capability result. Extraction changes Python ownership only; the established aggregate
result wire is unchanged.
