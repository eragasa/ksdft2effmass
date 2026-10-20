# Numerical contract

The module performs no array allocation or numerical transformation. It validates exact
enum and endpoint types, nonempty textual metadata, and the declared Phase 1 transition
between source and target role families.

The enum's integer `.value` is not serialized. Future serializers must provide an explicit
versioned mapping. Any emitted `TransformationIdentity.kind` should agree with the request,
Action, and result kinds, but that agreement remains nominal rather than numerical
evidence.
