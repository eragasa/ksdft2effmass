# H1 migration and compatibility plan

Status: proposed for `H1-HC01`. H1 moves, copies, retires, executes, or cuts over
nothing.

## Governing principle

Current validators, skills, schemas, fixtures, task/checkpoint/chain records, and
historical evidence remain authoritative in their existing scope until H4 proves
accepted shadow parity and a human approves cutover. A new generic record or
action does not retroactively rewrite historical meaning.

The migration order is fixed:

```text
accepted H1 contract
-> separately activated and accepted H3 resources
-> separately activated and accepted H2 generic Python
-> separately activated H4 local adapters and shadow parity
-> human cutover decision
```

No acceptance automatically activates a successor.

## Compatibility classes

### Direct generic inputs

Current version-2 ownership structure, resource identities, checksum entries,
and profile-free structural facts may be converted to accepted generic records
without preserving project literals in generic code. The caller supplies roots,
records, and profile explicitly.

### Project-local adapters

The following remain local and require a versioned H4 adapter:

- `.pi` directory layout and heterogeneous task/chain/checkpoint file shapes;
- agent frontmatter and agent identities;
- Git branch, remote, commit, push, and durability policy;
- evidence prefixes, pytest markers, filename and node-ID rules;
- protected/migrated/warning evidence-ID states;
- lifecycle vocabulary and explicit task activation rules;
- P1 version-1 ownership inventory, exceptions, object kinds, exact artifact
  filenames, and completion command;
- current local skill precedence and routing;
- CPN, SNAKES, QE, Wannier90, operator, and scientific semantics.

Adapters preserve source identity, target contract version, adapter version,
structured conversion findings, and the original input. They do not silently
repair or overwrite accepted records.

### Legacy `boundary_owned`

P1's accepted `boundary_owned` value remains unchanged in historical/local
input. The H4 adapter may present it to the generic comparison surface as
`artifact_owned` with relation metadata naming both sides and direction. That
mapping is compatibility behavior, not a rename, new primary ownership kind, or
permission to change P1 test names, manifests, schemas, fixtures, or evidence.

### Deferred command and decision-boundary records

Existing command manifests/results and Git decision-boundary evidence remain
local historical/task records. H1 does not force them into a speculative common
wire contract. Shadow comparison may compare explicitly selected facts through
H4 local adapters without declaring a generic public command or Git API.

## H3 resource migration

H3 derives one generic evidence-writing resource from the accepted
`document-research-python` grammar and directly referenced test-evidence file.
It must:

1. retain exact source identities and attribution;
2. preserve the accepted `class_owned`/`artifact_owned` grammar;
3. move project prefixes, markers, P1 filename exceptions, and domain rules into
   the local profile/extensions;
4. manifest every entry, direct reference, script, schema, template, profile,
   and fixture by stable ID and byte identity;
5. retain the existing `.pi/skills/document-research-python/` source unchanged
   until H4 cutover;
6. create no competing evidence grammar or automatic dispatch path.

H3 resource schemas and fixtures are normative implementation resources for the
accepted H1 contract only after H3 human acceptance. H1 field tables remain the
contract decision source; discrepancies block H3 acceptance rather than silently
changing H1.

## H2 implementation compatibility

H2 implements the accepted API against accepted H3 identities. It must keep
internal imports relative, expose only the exact H1 public names, reject hidden
root discovery, and produce deterministic structured results. It creates no
local Python and no compatibility facade to a speculative standalone package.

Class-owned tests cover each public class. Artifact-owned tests cover public
imports, H1/H3 Python-wire agreement, generic/local dependency direction, path
confinement, and resource resolution. Boundary agreement and direction use
artifact relation metadata, not a fake Workflow or third ownership kind.

## H4 shadow replay

H4 runs old and new behavior against identical declared inputs from a clean
revision. Optional pre-commit worktree checks are separate and cannot replace
that result. Comparison includes:

- validation status and stable issue codes;
- subjects, serialized paths, related identities, severities, and ordering;
- ownership role/path/reviewer/completion findings;
- checkpoint-set unresolved/resolved facts without choosing a decision;
- task/chain active, blocked, and structurally-ready facts;
- evidence-ID inventories and known protected gaps;
- checksum inventories and byte mismatches;
- skill resource closure and selected identities;
- explicit exit status only where the legacy local artifact records it.

Differences are classified as:

- `EXACT_PARITY`;
- `APPROVED_REPRESENTATION_CHANGE` with a named normalization and human authority;
- `EXPECTED_NEW_STRICTNESS` requiring explicit acceptance;
- `DEFECT_OR_UNEXPLAINED_DIFFERENCE`, which blocks cutover.

Timestamps, temporary absolute roots, and presentation prose may be normalized
only by a named approved rule. Codes, severities, paths, identities, ordering,
authorization facts, or protected evidence states are never silently normalized.

## Cutover and rollback

H4's genuine checkpoint must name old and new authoritative routes, parity
results, intentional differences, every proposed retirement, a rollback action,
and retained evidence. Before human cutover acceptance, both paths remain and
the legacy route remains authoritative.

Rollback changes routing back to the exact pre-cutover identity without deleting
new evidence or rewriting history. Validator/skill retirement is a later
explicitly accepted cutover effect; historical evidence, checkpoints, manifests,
reviews, checksums, and node maps are retained permanently unless separately and
explicitly authorized for another reason.

## Compatibility risks and controls

| Risk | Control |
| --- | --- |
| Divergent duplicate evidence grammar | one H3 resource derived from `document-research-python`; local extensions reference it |
| Implicit repository discovery | every generic action receives bytes, records, and roots explicitly; negative tests |
| Loss of historical evidence identity | immutable old/new path and content identities; no rewrite |
| P1 v1 compatibility drift | versioned local adapter and exact legacy replay |
| Premature validator/skill retirement | H4 parity plus genuine human cutover checkpoint |
| Local replacement hiding generic content | v1 extension-only overlays; duplicate identity/path fails |
| Case/symlink/workstation path drift | portable ResourcePath plus lexical/resolved confinement and exact-case checks |
| False scientific or authorization claim from PASS | explicit result claim boundary and VVUQ review |
| Personal/concurrent notes entering validation | not manifestable H1 resources; clean-revision and pre-commit modes separate |

## Deferred migration choices

The standalone distribution/import/CLI identity, package metadata, installation,
publishing, Graphify integration, generic command/result contract, and generic
Git decision-boundary result remain outside H1-H4 unless separately authorized.
Optional H5 may evaluate extraction readiness after accepted H4; H5 is not a P2
prerequisite and neither branch activates automatically.
