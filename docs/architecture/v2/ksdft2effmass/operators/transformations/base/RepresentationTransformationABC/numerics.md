# Numerical contract

Concrete public `transform` implementations must reject a non-nominal request, require
request kind to equal Action kind, and require result kind to equal Action kind before
return. The protected final validators provide these exact checks.

This nominal agreement does not evaluate arrays, tolerances, witnesses, qualification, or
scientific validity.
