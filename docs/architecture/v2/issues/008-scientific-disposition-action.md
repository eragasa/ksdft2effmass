# V2-ISSUE-008: Scientific disposition ActionObject

**Severity:** Medium

**Scope:** Scientific authority and disposition recording

## Conflict

Analyzers are correctly prohibited from producing `ScientificDisposition`, and persistence repositories do not create domain conclusions. No named ActionObject validates intended-use scope and authority, constructs the immutable disposition, and records its reference.

## Affected contracts

- `analysis/analysis-and-disposition.md` — *Authority separation*
- `workflow/control-plane.md` — *Human authority*
- `workflow/persistence.md`
- `workflow/service-model.md`

## Required resolution

Define an explicit action such as `ScientificDispositionRecorder` that receives identified analysis revisions, intended use, conclusion, exact authority reference, and expected persistence revision.

## Acceptance condition

Every disposition has one declared creation path that cannot infer authority from analysis output, process success, CPN terminality, or repository capability.
