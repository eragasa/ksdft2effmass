# `periodic1d.campaign.reduction_challenge.verified_workflow`

## Responsibility

`Periodic1DReductionChallengeVerifiedWorkflow` composes the read-only correlation
Workflow and independent numerical verifier while preserving two distinct Results.
Its request owns the exact payload request plus an explicit tolerance; its Result owns
the complete correlated campaign outcome plus the complete verification outcome.

The Workflow constructs fresh request-scoped operation owners. It is not a registry,
plugin, generic workflow engine, static utility namespace, or protected-execution
surface. Aggregate passing establishes bounded numerical consistency only.
