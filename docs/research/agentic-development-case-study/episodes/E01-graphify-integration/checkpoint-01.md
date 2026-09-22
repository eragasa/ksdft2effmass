# E01 checkpoint 01: read-only Graphify integration inspection

## Checkpoint type

Read-only pre-integration inspection and human decision checkpoint.

## Graphify version

`graphify 0.9.2`

Detected command path:

```text
/Users/eugene/.local/bin/graphify
```

The Python package used by the command was under:

```text
/Users/eugene/.local/share/uv/tools/graphifyy/lib/python3.14/site-packages/graphify/
```

## Files inspected

- `AGENTS.md`
- `.pi/skills/choose-next-task/SKILL.md`
- `.pi/skills/design-data-action-objects/SKILL.md`
- `.pi/skills/develop-operator-records/SKILL.md`
- `.pi/chains/operator-record-refactor.chain.json`
- `.pi/agents/*.md`
- `.pi/tasks/operator-record-refactor.md`
- `docs/architecture/repository-layout.md`
- `docs/architecture/repository-layout.rst`
- `python/pyproject.toml`
- `.gitignore`
- `/Users/eugene/.pi/agent/skills/graphify/SKILL.md`
- Graphify installer source in the installed package, especially
  `graphify/__main__.py`
- packaged Graphify `skill-codex.md`
- packaged Graphify `always_on/agents-md.md`

## Installer behavior discovered

The command:

```bash
graphify install --project --platform codex
```

would install a project-local Codex skill, but would also:

- write or replace a Graphify section in `AGENTS.md`;
- create/update `.codex/hooks.json` with a Codex `PreToolUse` hook;
- copy the Codex skill and references under `.codex/skills/graphify/`.

Because the repository requires explicit human approval for `AGENTS.md`, hooks,
and external-processing policy, the installer was not run.

## Detected skill surfaces

- pi repository-local skills: `.pi/skills/`
- global pi Graphify skill: `/Users/eugene/.pi/agent/skills/graphify/SKILL.md`
- Codex project skill target from installer source:
  `.codex/skills/graphify/SKILL.md`

No evidence was found that `.pi/skills` and `.codex/skills` automatically expose
each other. They are treated as separate discovery surfaces.

## Hooks before integration

No existing Graphify hook was found in `.git/hooks/`. No `.codex/hooks.json` was
present before integration.

## External API keys and remote processing

At checkpoint time, the environment did not contain:

- `GEMINI_API_KEY`
- `GOOGLE_API_KEY`
- `OPENAI_API_KEY`

No external semantic-processing backend was enabled or configured.

## Repository transmission status

No Graphify generation was run before approval. No repository content was
transmitted externally before approval.

## Options presented

1. Run `graphify install --project --platform codex` as-is.
2. Manually install the Codex skill under `.codex/skills/graphify/` and add a
   narrow repository policy manually.
3. Defer Codex installation and add pi-only routing.

## Human resolution

The human approved Option B on 2026-07-30.

Approved constraints:

- do not run `graphify install --project --platform codex`;
- do not install `.codex/hooks.json`;
- do not install hooks;
- do not enable Gemini, OpenAI API, or another external semantic-processing
  backend;
- do not configure or store API keys;
- manually copy Graphify 0.9.2 Codex skill files;
- add narrow `AGENTS.md` policy;
- update `choose-next-task` so Graphify is optional supporting evidence;
- add `graphify-out/` to `.gitignore`;
- treat Graphify outputs as locally persistent but untracked.

## Rejected options

- automatic installer-controlled `AGENTS.md` rewrite;
- Codex hook installation;
- remote semantic processing;
- global skill modification;
- generated graph artifacts committed without separate human review.

## Scientific-validity boundary

E01 is infrastructure. It is not evidence of scientific validity of a Hamiltonian,
operator reduction, numerical method, or physical claim.
