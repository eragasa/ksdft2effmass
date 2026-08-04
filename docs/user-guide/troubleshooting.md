# Troubleshooting

## A transition is not enabled

Inspect the durable marking and verify that required input, capability, authorization, manifest, parentage, and validation tokens exist with compatible bindings. Do not bypass a guard or fabricate a completion flag.

## An external request exists but no result arrived

The CPN must retain the requested state. Diagnose the external adapter, scheduler, or transfer system outside guard evaluation. Record a correlated failure or result token; do not mutate the request token silently.

## A retry is desired

A failure token alone does not authorize retry. Add an explicit `RetryAuthorizationToken` through the approved human or policy path, then fire the retry-request transition with a new attempt/manifest identity.

## Direct and Wannier-derived results will not join

Verify that both identify the same accepted `PeriodicElectronicStructureDataset` parent and compatible physical, numerical, pseudopotential, workflow-schema, representation, energy, artifact, and manifest metadata. Completion of both branches is not enough.

## Sphinx does not render a Markdown page

Install the declared `docs` extra and build through the locked environment. Sphinx intentionally collects only `docs/user-guide/*.md`; architecture, computational, research, conference, paper, and meeting Markdown are excluded from parsing. Add a maintained user-guide page to the explicit toctree rather than broadening collection. Do not duplicate Markdown pages in RST or suppress warnings to conceal a missing target.

## An executable or package is missing

Do not dynamically probe it from a transition guard. Use a preflight adapter to produce a structured installation/verification result and capability token.

## A calculation appears available from prior notes

Meeting notes or unmanifested historical calculations cannot satisfy a computational gate. Required accepted artifact, manifest, validation, and parentage tokens must exist.
