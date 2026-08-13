# Identity, version, and failure contracts

## Identity taxonomy

| Identity | Meaning |
|---|---|
| `DefinitionIdentity` | Stable logical identity of a versioned definition |
| `RecordIdentity` | Stable logical identity of one persisted record |
| `RevisionIdentity` | Identity of one immutable record revision |
| `AttemptIdentity` | Unique identity of one bounded execution attempt |
| `RequestIdentity` | Identity of one requested external operation |
| `ResultIdentity` | Identity of one correlated operation result |
| `ArtifactIdentity` | Stable logical artifact identity |
| `ContentIdentity` | Digest identity of exact bytes under a named algorithm |
| `ImplementationIdentity` | Exact software implementation and version identity |
| `AuthorityIdentity` | Identity of the decision or grant authorizing an operation |

Logical identity, revision identity, and exact-byte identity are not interchangeable. Filenames and deployment paths are not identities unless an owning contract explicitly makes them so.

## Version dimensions

Records declare only applicable dimensions:

- record schema version;
- wire-format version;
- campaign-definition version;
- CPN-definition and expression version;
- simulation-payload version;
- analyzer and numerical-policy version;
- normalization-policy version;
- artifact-format version; and
- implementation identity.

One overloaded `schema_version` must not conceal behaviorally independent versions.

## Failure taxonomy

```text
ConfigurationFailure
AuthorizationFailure
InputIdentityFailure
DispatchFailure
ProcessFailure
CompletionContractFailure
ArtifactPublicationFailure
NativeParsingFailure
ObservationNormalizationFailure
AnalysisFailure
PersistenceConflict
CampaignTransitionFailure
```

A failure record includes failure identity, phase, attempt or operation identity, implementation identity, stable code, sanitized diagnostic, retryability when explicitly known, and related artifact identities. Retry creates a new attempt and does not erase the failure.

## Correlation rules

- Request and result identities are unique within their owning run.
- A result references exactly one request and attempt.
- Artifact producer identities reference exact request/result revisions.
- Analysis references normalized observation and analyzer versions.
- Disposition references exact analysis revisions and authority.
- Cross-harness references use immutable identities only.

## Unresolved issues

- Canonical lexical forms and namespace ownership for each identity.
- UUID, content-derived, or repository-assigned identity strategies by family.
- Hash algorithm agility and content-identity migration.
- Failure-code registries and extension policy.
- Representation of partially known implementation identity for external tools.
