# `ksdft2effmass.campaigns` package

The prospective `ksdft2effmass.campaigns` package owns project-specific
composition definitions that bind accepted scientific work into workflow
contracts. It does not own generic Workflow, Petri-net, calculator, integration,
or analysis semantics.

```mermaid
flowchart LR
    campaigns["campaign definitions"] --> workflows["ksdft2effmass.workflows"]
    campaigns -. no dependency .-> analysis["ksdft2effmass.analysis"]
    app["ksdft2effmass.application"] --> campaigns
```

Campaign definitions do not activate protected execution, grant authority, or
establish scientific acceptance. Exact internal submodules and wire exports
remain deferred.
