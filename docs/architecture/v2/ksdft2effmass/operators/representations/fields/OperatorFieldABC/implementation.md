# Implementation

`OperatorFieldABC` is an empty-slot semantic ABC inheriting
`SquareMatrixFieldABC`. It deliberately contains no optimistic property marker or
constructor behavior.

Concrete implementations provide storage and validation. Property evidence belongs to
later immutable evidence records, not subclass names.
