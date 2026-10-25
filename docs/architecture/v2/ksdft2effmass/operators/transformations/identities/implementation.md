# Implementation

`identities.py` contains one Python `Enum`, one final frozen slotted edge-identity
DataObject, and one final stateless identity factory. It imports intrinsic node identities
and carrier-local roles from `operators.representations.identities`, establishing the
selected one-way dependency.

`TransformationIdentityFactory.create` constructs metadata only. It is not an operational
transformation factory, does not dispatch algorithms by enum, and does not execute matrix
operations.

The module imports no concrete operator family, analysis, campaign, serializer, schema,
Workflow, retained-data, or formal runtime owner.
