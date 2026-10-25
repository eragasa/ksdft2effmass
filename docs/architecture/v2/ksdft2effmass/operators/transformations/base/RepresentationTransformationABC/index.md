# `RepresentationTransformationABC`

## Status and role

Generic nominal Phase 1 Action ABC for one operation-specific request/result family. The
selected public subclass contract is abstract `transform(request, /) -> result`.

## Public contract

```python
class FrameCompression(
    RepresentationTransformationABC[FrameCompressionRequest, FrameCompressionResult]
):
    @property
    def transformation_kind(self) -> RepresentationTransformationKind:
        return RepresentationTransformationKind.frame_compression

    def transform(
        self,
        request: FrameCompressionRequest,
        /,
    ) -> FrameCompressionResult:
        self._require_compatible_request_kind(request)
        result = ...
        return self._require_compatible_result_kind(result)
```

Every concrete Action owns its public operation and must preserve exact enum agreement.
The protected validators centralize the required fail-closed checks without replacing the
abstract public override point.

## Five-way detail

- [Scientific interpretation](scientifics.md)
- [Numerical contract](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)

## Tests

- `test__RepresentationTransformationABC.py`
