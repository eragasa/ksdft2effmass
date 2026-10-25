# Numerical contract

The ABC performs no arithmetic or tolerance evaluation. Concrete results define their
own numerical payload and failure semantics. Each concrete Action must validate the
result's exact enum member against its own kind before returning it; the base provides a
protected final validator for that check.
