# RM-REVIEW-001 candidate planning

## Identity

| Field | Current value |
|---|---|
| Campaign | `RM-REVIEW-001` |
| Campaign state | `PLANNING` |
| Candidate version | not assigned |
| Candidate state | not frozen |
| Proposed protocol | `v0.1` |
| Protocol Git revision | pending |
| Proposed baseline | `2f30d7a37eab8306c7c17da0e2b316d63da8c74c` |
| Frozen candidate Git revision | pending |
| Human freeze confirmation | pending |

The proposed baseline is a navigation aid for planning. It is not the candidate
binding required by the protocol.

## Proposed purpose and audience

- Proposed purpose: internally reviewed working research monograph with a
  bounded technical and evidentiary conclusion.
- Proposed audience: numerate undergraduate physics majors progressing toward
  specialist semiconductor, mathematical, and computational material.
- Proposed publication-readiness claim: none.
- Proposed scientific-validation claim: none.

These remain subject to the human decisions in [`decisions.md`](decisions.md).

## Composition issue requiring a human decision

At commit `2f30d7a3`, `manuscript/manuscript.tex` composes Appendices A--L. A
separately developed Appendix M, concerning preliminary silicon work, was not
part of that commit or composition. The campaign must choose between:

- freezing a candidate based on the committed A--L composition; or
- preparing and independently checking a clean successor that includes
  Appendix M before freeze.

The campaign must not review unretained dirty bytes and later describe them as
if they were commit `2f30d7a3`.

## Freeze-gate checklist

- [ ] Protocol version and exact Git revision recorded.
- [ ] Human purpose, audience, and definition-of-done decisions recorded.
- [ ] Appendix M inclusion decision recorded.
- [ ] Exact clean candidate commit selected.
- [ ] Ordered LaTeX composition graph retained.
- [ ] Source and bibliography SHA-256 manifest retained.
- [ ] Rendered PDF SHA-256 and page count retained.
- [ ] Build commands and relevant tool versions retained.
- [ ] Structural, citation, and document-build results retained.
- [ ] Calculation and evidence indexes bound to exact revisions.
- [ ] Included and excluded supplements declared.
- [ ] Known unavailable evidence and replay limitations declared.
- [ ] Lead editor and initial human reviewers identified.
- [ ] Human decision owner confirms the intended candidate.

## Artifact and check record

No artifact or check result is entered here yet. Previously reported builds are
useful planning information but do not satisfy this campaign's freeze gate until
they are reproduced against and bound to the selected candidate.

## Candidate-version retention

After freeze, instantiate the protocol's candidate template as
`candidates/RM-REVIEW-001-C0.md`. Each revision candidate receives a new file
and identifier; no candidate record is overwritten to describe later bytes.
