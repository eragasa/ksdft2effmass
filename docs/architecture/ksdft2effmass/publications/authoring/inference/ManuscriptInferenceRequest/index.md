# `ManuscriptInferenceRequest`

`ManuscriptInferenceRequest` carries the deterministic prompt, originating authoring
request ID, owner-derived expected citations, complete lexical evidence-ID set,
required lexical gap-marker IDs, and requested text/citation limits. The three lineage
fields form an exact disjoint citation/marker partition and are bound into the request
identity. A model cannot supply or alter them.
