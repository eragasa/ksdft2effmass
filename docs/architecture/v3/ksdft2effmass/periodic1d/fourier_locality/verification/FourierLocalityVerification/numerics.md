# `FourierLocalityVerification` numerics

Comparison names are deterministic strings supplied by the independent verifier.
`CompositeVerification.evaluate()` records each comparison's maximum absolute
observation, applicable mixed tolerance, and pass result. Duplicate names cannot enter
the input mapping, and an empty component is rejected by shared verification admission.

The component passes only when every included scientific comparison passes. It does not
combine observations across units, replace fieldwise tolerances with one global value,
or include projection correlation checks.
