# Numerical contract

The factory performs no array allocation or numerical transformation. It validates exact
nominal enum and endpoint types, then delegates immutable metadata and role-transition
validation to `TransformationIdentity`.

No matrix dimensions, witnesses, residuals, tolerances, or evidence are calculated.
