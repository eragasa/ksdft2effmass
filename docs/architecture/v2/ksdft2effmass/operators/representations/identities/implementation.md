# Implementation

`identities.py` contains two standard Python `Enum` classes, one final frozen slotted
identity DataObject, and one final stateless slotted factory. Raw strings and integers are
rejected where enum members are required.

`RepresentationIdentityFactory` has carrier-specific creation methods and prevents
parallel rank and domain-ID inputs. The module imports only sibling representation domain
and space contracts plus standard-library types. It does not import transformations,
concrete operator families, analysis, campaigns, Workflow, serializers, schemas, retained
data, or formal code.

There is no serializer in Phase 1. Future adapters must map enum members to versioned wire
tokens explicitly.
