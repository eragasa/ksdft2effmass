# Implementation

The generic ABC binds nominal request and result roots and declares abstract
`transformation_kind` and abstract public `transform(request, /) -> result` contracts.
Concrete Actions implement `transform` directly.

Final protected request/result validators reject non-nominal values, raw-string kinds,
and enum disagreement. Concrete implementations call them before computation and before
return. The Action is not an enum-dispatched factory, serializer, evidence object, or
formal relation.
