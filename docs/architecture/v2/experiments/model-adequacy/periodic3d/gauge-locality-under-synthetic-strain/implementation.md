# Implementation

Reusable metric, Fourier-power, complete-radius, and M0 diagnostic behavior lives in
`python/src/ksdft2effmass/analysis/model_adequacy/band_equivalence_locality/strain.py`.
M1/M2 parent, frame alignment, strain-difference, and three-channel behavior lives in
`strain_response.py`, with presentation in `strain_response_plotting.py`.
The family action and presentation remain owned by
`experiments/model-adequacy/periodic3d/gauge-locality-under-synthetic-strain/`.

Campaign-owned typed serializers now map M0, M1, and M2 records explicitly to canonical
JSON and validate them against three immutable packaged strict result schemas. The
experiment action does not own a recursive JSON value type or use `dataclasses.asdict`
as its wire contract. Plotting still writes vector PDF and 600-dpi PNG development
figures. These artifacts remain explicitly replaceable. Before retained use, the family
still needs typed canonical input and verification documents, exact request/result
binding, environment provenance, an independent artifact-reading verifier that does not
invoke the calculator, at least three justified transform levels, frozen resource gates,
and separate authorization. The FCC-to-Bain common-cell map is explicit and
software-verified; the frozen M1 and fixed-response M2 smoke actions do not alter its
state-space identification.
