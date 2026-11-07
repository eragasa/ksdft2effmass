# Implementation and ownership

## Import surface

Consumers import from `operators.transformations.identities` or
`operators.transformations.base`. The package initializer and `operators` root do not
re-export these names.

## Identity implementation

`RepresentationTransformationKind` is a standard enum whose integer values are internal
discriminants. `TransformationIdentity` is a frozen, slotted dataclass.
`TransformationIdentityFactory` is stateless and identity-only. No enum member is a wire
token, serializer key, algorithm registry, or universal factory selector.

## Nominal transformation implementation

`RepresentationTransformationRequestABC` and
`RepresentationTransformationResultABC` require an abstract `transformation_kind`
property. Non-generic `RepresentationTransformationABC` requires an abstract
`transformation_kind` property and abstract request-bound
`transform(self) -> RepresentationTransformationResultABC`.

Each future final concrete transformation binds one exact request in its constructor and
narrows `transform` covariantly to its exact concrete result. It must check the exact
request type, apply the shared request-kind helper, directly construct the exact result,
check that exact result type, and apply the shared result-kind helper. Its request, result,
and transformation hard-code the same enum member.

The base validators are helper methods; the ABC cannot force a concrete override to call
them. One direct verification module per concrete triple is therefore mandatory. The
architecture uses no generic request/result parameters, structural protocols, universal
registry, result-constructor seam, or dynamically typed keyword bag.

## Dependency boundary

This package imports intrinsic representation identities and roles. The dependency may
not be reversed. It imports no concrete operator family, analysis, campaign, Workflow,
serializer, schema, retained-data, publication, or formal runtime package.

## Absent interfaces

There is no operation-specific Action, transformation graph, traversal framework,
registry, serializer, schema, evidence record, certificate, or compatibility facade in
this source tranche.
