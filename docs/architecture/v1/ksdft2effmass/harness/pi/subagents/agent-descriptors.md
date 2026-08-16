# Pi subagent descriptors in v1

## Discovery resources

The repository contains thirteen project descriptor files under `.pi/agents/`. Each uses YAML frontmatter plus a Markdown role prompt. Every descriptor declares:

- `name` and `package: ksdft2effmass`;
- a role description;
- a strict `tools` allowlist;
- `systemPromptMode: append`;
- project-context inheritance;
- skill inheritance or explicit selected skills; and
- `acceptanceRole` as `writer` or `read-only`.

Because local names already begin with `ksdft2effmass-` while the package is also `ksdft2effmass`, resolved runtime names repeat that prefix, for example `ksdft2effmass.ksdft2effmass-implementation`.

## Enabled project roles

The current Pi discovery surface exposes these non-disabled project roles:

| Descriptor | Role | Tools | Acceptance role |
|---|---|---|---|
| `ksdft2effmass-architecture` | Optional project architecture analysis | `read`, `bash` | Read-only |
| `ksdft2effmass-documentation` | Maintained documentation writer | `read`, `bash`, `edit`, `write` | Writer |
| `ksdft2effmass-harness-architecture` | Harness architecture analysis | `read`, `bash` | Read-only |
| `ksdft2effmass-harness-documentation` | Harness documentation writer | `read`, `bash`, `edit`, `write` | Writer |
| `ksdft2effmass-harness-implementation` | Harness implementation writer | `read`, `bash`, `edit`, `write` | Writer |
| `ksdft2effmass-harness-integration-reviewer` | Harness integration review | `read`, `bash` | Read-only |
| `ksdft2effmass-harness-tests` | Harness software-verification test writer | `read`, `bash`, `edit`, `write` | Writer |
| `ksdft2effmass-implementation` | Project production-source writer | `read`, `bash`, `edit`, `write` | Writer |
| `ksdft2effmass-integration-reviewer` | Project integration review | `read`, `bash` | Read-only |
| `ksdft2effmass-tests` | Project test-evidence writer | `read`, `bash`, `edit`, `write` | Writer |

Project architecture, documentation, implementation, integration-review, and test roles select applicable project-local skills explicitly. Harness roles generally receive skills only through a specific assignment.

## Present but disabled descriptors

Three task-specific descriptor files remain present but are disabled by `.pi/settings.json`:

- `ksdft2effmass-harness-local-test-parity-writer` for active-H4-only work;
- `ksdft2effmass-harness-python-evidence-vvuq-reviewer` for active-H2-only review; and
- `ksdft2effmass-harness-python-test-writer` for active-H2-only test writing.

Project settings also retain disabled overrides for additional retired harness roles whose descriptor files are no longer present. A disabled override prevents runtime execution but preserves the historical name and prevents accidental fallback discovery.

## Harness catalog projection

The generic harness represents only normalized agent identity and acceptance role through `AgentDescriptorView` in `python/src/ksdft2effmass/harness/pi/ownership.py`, with the corresponding schema and fixture under `harness/pi/`. This narrow view supports ownership validation; it is not a complete Pi descriptor model and does not determine runtime discovery.

`PiHarnessConfigurationDeserializer` converts the applicable `.pi/settings.json` bytes into public immutable `PiHarnessConfiguration`. `PiHarnessAgentDefinitionResolver` combines that value with each selected `.pi/agents/*.md` descriptor to produce public immutable `PiHarnessAgentDefinition` before database ingestion. Project-local persistence projects those definitions into `agent_definition` and `agent_skill_route` rows in `harness/state/harness-control.sqlite3` and its generated SQL. Exact package-qualified disabled names set the corresponding present descriptor row to disabled; names for absent historical descriptors create no row. `harness/pi/docs/pi-project-settings.md` records the consumed structure and claim boundary. Repository descriptors and project settings remain the implemented inputs, while the SQLite rows are a generated projection and cannot enable an agent.

## Prompt contracts

Enabled writer prompts require explicit Task assignment and path ownership, preserve project authority boundaries, forbid Task activation and protected execution, and request concise handoffs. Reviewer prompts are read-only and forbid mutation, human decisions, acceptance, and self-approval.

The prompt text is policy guidance interpreted by the child. Tool restrictions and disabled state are separately enforced by Pi configuration and discovery.

## Known limitations

- Role boundaries are repeated across several prompt bodies.
- No repository validator currently establishes one closed descriptor schema for all project roles.
- Disabled historical overrides and present descriptors require two surfaces to determine executability; control generation combines them for its repository projection, while Pi remains responsible for runtime discovery.
- Descriptor frontmatter does not itself prove that a Task assignment or ownership manifest exists.
