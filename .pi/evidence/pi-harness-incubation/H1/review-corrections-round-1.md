# H1 bounded correction round 1

The four initial independent reviews are retained unchanged as
`review-*-initial.md`. This correction round responds to their findings; it does
not claim acceptance or erase failed history.

## Architecture and public-contract corrections

1. Added the distinct public `OwnershipScope` DataObject and
   `OwnershipScopePath` semantic type with explicit `file` versus
   `directory_tree` containment and overlap rules. `ResourcePath` remains a
   regular-file resource path.
2. Added the normalized `AgentDescriptorView`; generic ownership validation now
   consumes this view instead of raw project frontmatter bytes. Frontmatter
   parsing remains local.
3. Made policy inputs complete and data-only in `ProjectProfile`: closed
   resource-format and skill-behavior pairs, exact evidence namespace/range
   rules, protected evidence IDs, markers, lifecycle vocabularies, and local
   extension/version facts. Generic evidence auditing no longer claims filename
   policy; filename validation remains local.
4. Added named serializer/deserializer ActionObjects and concrete operation
   ResultObjects. Removed unnamed action-result tuples. DataObjects do not own
   serialization.
5. Fixed canonical JSON to RFC 8785 plus one LF and defined a closed explicit
   wire-record union and record-kind enum.
6. Made version 1 a closed integer contract. Removed unrepresented minor-version
   negotiation; new codes/enums/fields require a new integer version and explicit
   migration.
7. Defined exact Rust newtypes, structs/enums, filesystem/bytes mappings,
   internal-error boundary, and all ActionObject method shapes.
8. Removed speculative `SkillDescriptor.result_contract_id` and
   `failure_contract_id` fields. Added field/argument-to-current-consumer evidence
   to the interface matrix.
9. Fixed issue severity and precedence: every v1 generic code is `ERROR` except
   the explicit protected-gap `WARNING`; capability-specific checksum and profile
   identity precedence prevents duplicate interpretations.
10. Removed scientific/domain semantics from the harness capability-primary
    ownership table; they remain explicitly excluded and owned outside the
    harness by existing domain source/specification/evidence.

## Integration and path-plan corrections

1. Replaced H4 bare writer-role strings with exact roles, future agent-record
   paths, and pairwise disjoint local-source, local-test, retained-evidence, and
   maintained-doc paths. The H4 completion validator is now owned by the shadow
   evidence writer.
2. Added H4 schema, fixture, test, and documentation ownership statements.
3. Corrected the H3 schema owner to the declared
   `harness-generic-resource-writer` role.
4. Added exact stable handoff artifact IDs and paths, acceptance indexes, and
   exact H1/H3/H2/H4 cross-task references. Successor acceptance indexes must
   enumerate every accepted artifact identity rather than relying on prose
   categories.
5. Added disjoint H3/H2 verification-evidence writer paths for retained
   acceptance indexes.
6. Corrected `docs/harness/ksdft2effmass.harness.00.md` to show H1 active and
   contract-only.
7. Corrected the inactive H2 task objective so H2 has no possible local-Python
   exception; H4 owns the entire `local/` Python boundary.

## Evidence/VVUQ review

The initial evidence/VVUQ review passed. Its findings required no correction.
The accepted two-kind ownership model and structural-claim boundary remain
unchanged.

## Human-decision boundary

These are consistency corrections within the explicitly requested H1 proposal.
The corrected exact public surface and wire/path/version/ownership choices remain
unaccepted until the human selects an option at `H1-HC01`.
