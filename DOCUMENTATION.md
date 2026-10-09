# Documentation policy

## Organizing principle

Documentation should make each durable concern easy to find, understand, and apply
without reconstructing it from conversation history or unrelated prose.

- Give each distinct concern its own level-two (`##`) section.
- Begin the section with one short paragraph stating its scope, purpose, or rationale.
- Follow that paragraph with concise bullets containing the actionable rules.
- Keep authorization, scientific claims, implementation constraints, and operational
  procedures in separate sections rather than blending their meanings.
- Link to an authoritative owner instead of copying detailed contracts into several
  files that can drift apart.

## Implementation-bound documentation

A Markdown policy is not sufficient when forgetting a boundary could change software
behavior, scientific meaning, provenance, or numerical acceptance.

- Put the boundary in the owning class or method docstring.
- Add a concise inline comment at the non-obvious enforcement point explaining why the
  code must not be simplified into the incorrect behavior.
- Add a regression test that fails if the boundary is removed or conflated.
- Record broader ownership and rationale in the applicable architecture document.
- Keep public API documentation, source docstrings, tests, and architecture statements
  consistent.

## Numerical identity and portability

Exact byte identity and portable numerical equivalence are different claims and must
remain visibly separate in documentation and code.

- Describe SHA-256 as an identity of exact bytes, not as proof of numerical or
  scientific equivalence.
- Compare reconstructed floating-point quantities under explicit reviewed tolerances.
- Preserve historical fingerprints and artifacts rather than replacing them with values
  generated on another platform.
- Record the operating system, architecture, Python, NumPy, BLAS/LAPACK, and relevant
  math runtime whenever bitwise numerical replay is required.
- State explicitly that numerical consistency does not establish convergence, physical
  adequacy, validation, uncertainty quantification, transferability, or acceptance.

## Change closeout

Documentation is part of the implementation gate rather than an after-the-fact summary.

- Reproduce the exact bounded CI command and its checkout assumptions before opening or
  updating a pull request.
- Build Sphinx with warnings treated as errors when its sources or documented APIs
  change.
- Check local documentation links when architecture pages are added or moved.
- Report changed paths, checks, assumptions, and residual limitations.
- Use a message file with `git commit -F` for multiline commit messages; never encode
  paragraph breaks as literal `\\n` sequences in a command argument.
