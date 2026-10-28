# `Mathieu1dIndependentVerification`

Implemented `CompositeVerification` containing the field-by-field independent
reconstruction observations for a complete Mathieu1D result.

Observation names retain typed field paths, including tuple lengths and indices. Missing,
additional, structurally different, or numerically different values therefore remain
visible rather than collapsing into one aggregate norm.

```python
from ksdft2effmass.model_systems.mathieu1d import Mathieu1dIndependentVerification
```

This value is one component of `Mathieu1dVerification`; callers normally obtain it from
`Mathieu1dVerifier` rather than constructing it directly.
