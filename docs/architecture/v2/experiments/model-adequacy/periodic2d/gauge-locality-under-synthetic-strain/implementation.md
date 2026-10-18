# Implementation

Reusable metric, Fourier-power, complete-radius, and M0 diagnostic behavior lives in
`python/src/ksdft2effmass/analysis/model_adequacy/band_equivalence_locality/strain.py`.
M1/M2 parent, frame alignment, strain-difference, and three-channel behavior lives in
analysis-owned `strain_response.py`. Campaign-owned presentation lives in
`python/src/ksdft2effmass/campaigns/model_adequacy/band_equivalence_locality/strain_response_plotting.py`, including a public caller-supplied-axes renderer.
The family action and presentation remain owned by
`experiments/model-adequacy/periodic2d/gauge-locality-under-synthetic-strain/`.

Campaign-owned typed serializers now map M0, M1, and M2 records explicitly to canonical
JSON and validate them against three immutable packaged strict result schemas. The
experiment action does not own a recursive JSON value type or use `dataclasses.asdict`
as its wire contract. Plotting still writes vector PDF and 600-dpi PNG development
figures. These artifacts remain explicitly replaceable. Typed canonical source, request,
result, verification, environment, and exact SHA-256 binding documents now exist for the
development scan, together with artifact-reading semantic reconstruction. Before retained
use, the family still needs at least three justified transform levels, frozen resource
gates, independent evidence review, and separate execution authorization.
