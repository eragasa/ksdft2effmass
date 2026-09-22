# Architecture-v2 HarnessConfiguration contract review

## Review purpose

This report supports direct human review of the prospective Architecture-v2
`HarnessConfiguration` documentation contract. It explains the proposed decision,
recommendation, evidence, limitations, unresolved issues, and acceptance boundary.
It is not itself a human decision, implementation authorization, Task activation,
scientific claim, or release record.

## Reviewed subject

The candidate is the uncommitted documentation change based on revision
`cba1251` (`record human review acceptance`). The principal contract is:

- `docs/architecture/v2/ksdft2effmass/harness/configuration.md`

The synchronized navigation and neighboring architecture surfaces are:

- `docs/architecture/v2/index.md`;
- `docs/architecture/v2/ksdft2effmass/application/index.md`;
- `docs/architecture/v2/ksdft2effmass/harness/index.md`;
- `docs/architecture/v2/ksdft2effmass/harness/object-model.md`;
- `docs/architecture/v2/ksdft2effmass/harness/persistence.md`; and
- `docs/index.rst`.

No Python source, test, schema, fixture, dependency, lockfile, runtime
configuration, control state, scientific artifact, or protected-execution surface is
part of this candidate.

## Proposed architecture

The candidate selects a resolved immutable `HarnessConfiguration` aggregate for
application composition. It centralizes the effective configuration value while
retaining subsystem ownership through concrete nested DataObjects:

- `PiHarnessConfiguration` owns the normalized Pi-settings subset consumed by the
  harness;
- `HumanReviewConfiguration` owns review-packet and non-authoritative decision-view
  configuration;
- `HarnessPersistenceConfiguration` owns immutable construction values for the
  development `HarnessState` repository; and
- exact source identities bind the source payloads used to resolve the aggregate.

`HarnessConfigurationResolver` receives explicit identified harness-native and Pi
source bytes and returns the resolved aggregate. There is no ambient file discovery,
implicit environment selection, fallback source, or generic `ConfigurationProtocol`.
Runtime repositories, stores, connections, validators, publishers, credentials, and
authority grants remain separately constructed dependencies rather than configuration
fields.

Canonical versioned JSON is selected as the initial configuration wire format through
format-specific serializer and deserializer ActionObjects. YAML is deferred pending a
separate wire-contract and dependency decision.

Authoritative development decisions remain `DevelopmentDecision` values inside the
complete `HarnessState` aggregate. `HumanReviewConfiguration` may select transient
packet-artifact and human-readable projection destinations, but cannot create a second
authoritative decision store.

## Recommendation

**Recommendation: accept the documentation contract as the bounded Architecture-v2
direction, while keeping source implementation separately unauthorized.**

The recommendation is based on these considerations:

1. **Centralized effective configuration without monolithic ownership.** One resolved
   aggregate gives application composition an exact immutable input, while nested
   configuration objects remain with their domain owners.
2. **No duplicate Pi authority.** The aggregate encapsulates the normalized consumed
   Pi subset and its source identity without replacing or copying ownership of Pi's
   complete `.pi/settings.json` format.
3. **Preserved HarnessState boundary.** Human decisions continue to share the complete
   development aggregate and revision history rather than acquiring an inconsistent
   second persistence authority.
4. **Explicit dependency direction.** Configuration contains construction values;
   application composition constructs and injects runtime capabilities separately.
5. **Deterministic initial wire contract.** Canonical JSON supports strict duplicate-key,
   version, checksum, and round-trip behavior using the standard library.
6. **Proportionate scope.** Deferring YAML avoids making an unreviewed parser dependency
   and scalar-semantics decision during the architecture-contract slice.

## Alternatives considered

### One monolithic configuration owner

A single `HarnessConfiguration` could own every nested rule and parse every external
format itself. This centralizes code as well as values, but transfers subsystem policy
to a generic owner, duplicates Pi parsing rules, and tends toward a service-locator
boundary. It is not recommended.

### Independent subsystem configuration documents coordinated by protocols

Each subsystem could expose an independent document and structural configuration
protocol. This preserves local ownership, but leaves application composition without
one identity-bound effective snapshot and allows conflicting or partially selected
configuration authorities. Protocols add little value for closed versioned data
contracts. It is not recommended.

### One resolved aggregate with subsystem-owned concrete values

This is the proposed architecture. It distinguishes centralized composition from
distributed domain ownership and uses protocols only for demonstrated runtime
capabilities. It is recommended.

## Verification and review evidence

The following checks were performed against the candidate:

- `git diff --check` passed.
- Sphinx read and rendered the new page and all links in the HTML build.
- The warnings-as-errors Sphinx command retained exactly nine pre-existing
  `toc.not_included` warnings from unrelated architecture pages and introduced no new
  warning.
- A fallback independent reviewer identified one high-severity wording defect: the
  original generic statement about rejecting unsupported members could have implied
  rejection of Pi-owned fields outside the consumed subset, contrary to the
  implemented open Pi-settings adapter boundary.
- The contract was corrected to apply strict unknown-member rejection only to the
  harness-native and canonical aggregate wires while preserving Pi's ownership and
  open external format.
- An independent correction review returned `PASS` with no remaining blocker-level
  contradiction.

The initially requested specialist architecture review was interrupted before it
returned a finding set. It is not counted as review evidence. The completed fallback
review and correction re-review are the review evidence used here.

## Known limitations

- This is static architecture and documentation review, not implemented software
  verification.
- No canonical JSON bytes exist yet; a separate JSON Schema is not required for the first slice.
- No configuration source was loaded, resolved, serialized, or deserialized.
- No repository, SQLite database, or review-artifact destination was constructed.
- No YAML parser or dependency was selected.
- No migration from the implemented Architecture-v1 `PiHarnessConfiguration` was
  exercised.
- Existing Sphinx warnings prevent a clean repository-wide warnings-as-errors result,
  although the candidate introduced no new warning.
- Reviewer agreement does not provide human acceptance.

## Unresolved issues intentionally deferred

The following questions remain open for a later public-contract implementation task:

1. Exact fields, semantic types, defaults, and constructor order of each configuration
   DataObject.
2. The root-relative location and canonical JSON contract of the harness-native authoring document.
3. Whether source bindings reuse existing Architecture-v2 `SnapshotIdentity` and
   `ContentIdentity` records directly or require a dedicated configuration-source
   record.
4. Exact resolver result and closed failure variants.
5. Canonical JSON member names, ordering, final-newline rule, and duplicate-key behavior; a separate schema artifact should be added only for a demonstrated consumer.
6. Root-confinement rules and explicit authorization requirements for intentionally
   external artifact or database locations.
7. SQLite path, connection lifetime, isolation, locking, busy timeout, recovery,
   retention, and backup parameters.
8. Whether transient review packets and non-authoritative decision projections share
   one artifact root.
9. Exact retention-policy vocabulary for non-authoritative review artifacts.
10. Compatibility and migration behavior for the implemented
    `PiHarnessConfiguration` and `PiHarnessConfigurationDeserializer`.
11. Whether YAML is required, which parser is acceptable, and how YAML scalar and key
    semantics map deterministically to the normalized aggregate.
12. Exact public package/module locations and import paths.

These deferred issues do not prevent acceptance of the ownership and dependency
direction documented by the candidate. They do prevent source implementation until a
later task resolves the fields and public contracts it needs.

## Risks and mitigations

| Risk | Mitigation in the proposed contract |
|---|---|
| `HarnessConfiguration` becomes a generic policy owner | Nested concrete DataObjects retain subsystem invariants and ownership |
| Pi settings acquire a second editable authority | Resolution consumes explicit Pi-owned bytes and retains their source identity |
| A review projection is mistaken for authoritative acceptance | `DevelopmentDecision` remains inside `HarnessState`; projections are explicitly non-authoritative |
| Configuration becomes a service locator | Live services, repositories, connections, publishers, credentials, and grants are excluded |
| Invalid or stale source combinations are silently accepted | Explicit resolution is fail-closed and binds exact source identities |
| YAML changes scalar meaning or adds dependency risk | YAML is deferred to a separate decision and format-specific adapter |
| Configuration authorizes work | The contract explicitly grants no Task, operation, scientific, protected, publication, or release authority |

## Acceptance boundary

Acceptance would establish only the prospective Architecture-v2 ownership and
dependency direction documented in the candidate. It would authorize no Python source
implementation, schema, fixture, dependency, YAML support, persistence migration,
Task activation, automatic successor, scientific work, protected execution,
publication, release, commit, or push.

A later implementation proposal must return for review with exact public fields, wire
contract, compatibility behavior, tests, and any dependency decision. The defensible
human dispositions for this candidate are:

- `accepted` — accept the documented Architecture-v2 direction only;
- `bounded_correction` — identify exact documentation corrections before acceptance;
- `deferred` — retain the candidate without accepting the direction; or
- `rejected` — reject the proposed ownership or dependency model.
