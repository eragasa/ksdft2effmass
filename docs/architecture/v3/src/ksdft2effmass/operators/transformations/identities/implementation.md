# Implementation

`RepresentationTransformationKind` is a standard enum with internal integer
discriminants. `TransformationIdentity` is final, frozen, and slotted.
`TransformationIdentityFactory` is a stateless slotted identity factory with one explicit
`create` method; it neither selects nor runs an algorithm.

The module depends on representation identities and roles. That dependency is deliberately
one-way. It exports the enum, identity, and factory; text and role-transition validators
remain private.
