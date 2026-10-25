# Implementation

The request and result roots are nominal ABCs with abstract `transformation_kind`
properties. `RepresentationTransformationABC[RequestT, ResultT]` binds both generic
parameters to those roots and exposes two abstract public requirements:
`transformation_kind` and `transform(request, /) -> result`.

Concrete Actions implement `transform` directly. They must reject request/Action/result
kind disagreement. Final protected `_require_compatible_request_kind` and
`_require_compatible_result_kind` methods provide shared exact nominal and enum checks;
operation-specific code invokes them before numerical work and before returning a result.

The module imports only `RepresentationTransformationKind` and standard-library
ABC/typing contracts. It does not import NumPy, analysis, campaigns, serializers,
Workflow, retained data, or formal code.
