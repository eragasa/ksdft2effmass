# Control-plane cleanup intake

## Human request

> let's do a control plane clean up, plan a task with immediate priority, but not active to do this, this should include an audit of AGENTS.md, skills, prompts, and all control plane surfaces. start first with the inventory

## Clarified objective

The immediate planned priority is `harness.control-plane-cleanup`, but it remains
inactive until the active `harness.simplify-2` boundary is explicitly accepted and
the cleanup Task is explicitly activated. Automatic successor activation remains
disabled.

The objective is authority reduction, not arbitrary file-count reduction. The live
control plane should contain only the minimum operational authority required for
current and prospective work. This repository is pre-alpha, and Git history is
sufficient historical retention. Unused live compatibility, deprecated aliases,
archived copies, resolved control records, and historical ceremony do not need to
remain tracked merely to preserve old interfaces.

## Inventory and cleanup interpretation

Every inventoried surface is classified as exactly one of `live_authority`,
`live_runtime`, `generated_projection`, `current_documentation`,
`removable_history`, `obsolete_compatibility`, `cache_or_temporary`, or
`unresolved`. The inventory distinguishes source authority, generated state,
runtime implementation, tests, current operational documentation, historical
material, and cache contamination. Counts are descriptive only; they are not
acceptance targets.

The future cleanup may inspect and rationalize `AGENTS.md`, live agents and skills,
prompt and template resources, Tasks and relationships, chains, checkpoints,
ownership, `.pi/evidence/**`, `harness/archive/**`, intake and reports, schemas,
fixtures, profiles, extensions, manifests, generated control artifacts, harness
Python modules and commands, harness tests, and tracked cache or temporary
artifacts. It must not create another archival layer before deleting the existing
one.

The CLI target is one synchronization command, one source-aware validation
command, and additional commands only for distinct maintained user operations. No
CLI should remain solely as a wrapper around another CLI, and maintained commands
must not parse one another's output.

This intake and its initial inventory authorize planning only. They do not activate
the cleanup or authorize scientific or numerical implementation, simulation,
telemetry, a new persistence architecture, dependency or lockfile changes, release
work, protected operations, parent acceptance, or automatic successor activation.
