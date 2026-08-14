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

## Prompt contracts

Enabled writer prompts require explicit Task assignment and path ownership, preserve project authority boundaries, forbid Task activation and protected execution, and request concise handoffs. Reviewer prompts are read-only and forbid mutation, human decisions, acceptance, and self-approval.

The prompt text is policy guidance interpreted by the child. Tool restrictions and disabled state are separately enforced by Pi configuration and discovery.

## Known limitations

- Role boundaries are repeated across several prompt bodies.
- No repository validator currently establishes one closed descriptor schema for all project roles.
- Disabled historical overrides and present descriptors require two surfaces to determine executability.
- Descriptor frontmatter does not itself prove that a Task assignment or ownership manifest exists.
