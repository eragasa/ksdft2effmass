# `Mathieu1dRangeResult`

Implemented immutable section for one symmetric finite hopping range.

It keeps the mediated truncation and direct weighted-fit routes distinct, then records
training and withheld errors, omitted coefficient norm, Parseval channels, fit rank and
conditioning, route defects, bandwidth, curvature, and imaginary residual. The
constructor correlates representative completeness, identification, and every stored
pass disposition.

```python
from ksdft2effmass.model_systems.mathieu1d import Mathieu1dRangeResult
```

The class reports one authored finite range. It neither selects that range nor promotes
its diagnostics to continuum error, uncertainty, or model acceptance.
