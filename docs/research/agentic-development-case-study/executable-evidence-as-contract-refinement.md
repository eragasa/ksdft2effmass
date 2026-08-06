## Executable evidence as contract refinement

During P2, software-verification work identified a distinction between testing an
accepted contract and improving that contract. Initial test expansion exposed
that `RunManifest` permitted its own `manifest_id` in
`dependency_manifest_ids`. This was not merely a missing test: it was an
underspecified intrinsic invariant in the public runtime model.

The correction prohibited direct self-dependency and added class-owned and
artifact-owned evidence. The corresponding JSON fixture remains structurally
valid under Draft 2020-12 JSON Schema because the schema cannot directly express
inequality between one scalar property and members of another array property.
The public Python constructor therefore owns the relational invariant, while the
schema owns wire structure and the fixture test owns agreement between the two
validation layers.

A subsequent evidence migration separated tests that had combined constructor
typing, stored-field behavior, equality, properties, and immutability. Each
resulting test names its actual public surface and records a requirement, method,
oracle, acceptance rule, interpretation, and limitation. This restructuring did
not automatically change production behavior. Instead, it converted broad tests
into traceable executable contract clauses and made future contract drift easier
to identify.

This episode suggests three distinct roles for maintained tests:

1. **contract verification** — checking implementation against an accepted
   requirement;
2. **contract clarification** — making an existing requirement precise enough
   to test reproducibly;
3. **contract refinement** — exposing and correcting a missing or inconsistent
   public invariant.

Only the third changes public behavior. All three remain software-engineering
evidence and do not establish numerical verification, scientific validation, or
uncertainty quantification.