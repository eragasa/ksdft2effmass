# Implementation

All three bases are nominal ABCs with empty slots. There are no generic parameters,
protocols, registries, dispatchers, broad unspecified payloads, or configurable result
constructors.

A future final concrete transformation binds `_request: ExactRequest` during
construction, performs `type(request) is ExactRequest`, and applies the request-kind
helper. Its parameterless `transform()` directly constructs `ExactResult`, checks that
exact type, applies the result-kind helper, and returns it. Request, result, and
transformation hard-code the same enum member rather than accepting it from callers.

The ABC helpers are marked `final` for strict static checking, but normal Python does not
make validator invocation automatic. Concrete-source review and one direct test module per
actual triple remain mandatory.
