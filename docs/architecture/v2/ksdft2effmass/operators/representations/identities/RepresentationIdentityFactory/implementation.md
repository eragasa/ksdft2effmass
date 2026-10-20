# Implementation

`RepresentationIdentityFactory` is a final stateless slotted class. Its two typed methods
require exact carrier-domain and role types before constructing a final frozen
`RepresentationIdentity`.

It is not an ABC, registry, serializer, dependency-injection container, or generic helper.
Its cohesive responsibility is canonical representation-identity construction.
