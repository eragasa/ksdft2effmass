# Numerical representation

## Implemented checks

`TransformationIdentity` performs metadata validation only. It checks exact enum and
endpoint types, nonempty textual metadata, and source/target role compatibility. It does
not allocate matrices or calculate residuals.

The non-generic transformation ABC supplies final protected validators. When a concrete
transformation invokes them, they reject:

- a request outside the nominal request ABC;
- a result outside the nominal result ABC;
- a raw string or other non-enum kind;
- request/Action kind disagreement; and
- result/Action kind disagreement.

Concrete final transformations remain responsible for exact request admission, invoking
the kind helpers, directly constructing and exactly checking their result, and
implementing request-bound `transform(self) -> ExactConcreteResult`. The base does not
make validator invocation automatic; direct tests of every actual concrete triple are
part of that concrete type's definition of done.

## Absent numerical contract

No source module here currently defines operation-specific dimensions, arrays, units,
precision, overflow behavior, Fourier sign or normalization, alignment objective,
tolerance, evidence, or failure disposition. Those details cannot be inferred from the
kind enum or edge identity.
