# Periodic campaign execution

## Campaign meaning

A campaign is what is run. The target separates immutable campaign state from the
ActionObject or Workflow that performs the study:

```text
CampaignDefinition
       |
CampaignExecutionRequest
       |
       v
Campaign ActionObject or Workflow
       |
       v
CampaignResult
       |
       +--> correlation
       +--> independent verification
```

A campaign definition selects scientific models, model cases, quantities of interest,
numerical controls, and provenance inputs. A request binds one exact execution. A
result records observations and identities. Correlation authenticates or relates
representations without making a numerical claim. Independent verification applies
its own stated oracle and acceptance rule.

## Loose coupling from scientific models

Campaigns depend on the scientific hierarchy and compose exact model instances or an
immutable model-catalog snapshot. A model has no campaign back-reference and owns no
campaign path, retained result identity, campaign tolerance, report status, or
execution authority.

The generalized campaign layer must not place incompatible operations on one base
class. One-dimensional retained verification currently takes caller-owned numerical
tolerances, while existing two-dimensional retained verification may require a
repository boundary. Such signatures remain on concrete request and Action types.
Shared nominal campaign membership, if introduced, cannot erase these inputs.

## Executable ownership

Reusable numerical construction, transformation, alignment, comparison, and
verification belong to cohesive ActionObjects. Multi-step campaign orchestration
belongs to a Workflow. Exact framework-owned CLI entry points may adapt typed files and
arguments, but they do not own scientific behavior.

A campaign must report the exact model identity and definition or request from which a
result arose. Iteration order and case identity are explicit. Ambient filesystem
discovery, implicit global registration, and mutation of source models are excluded.

## Evidence and execution boundaries

Running a deterministic toy campaign can provide software or numerical verification
only for its declared claims. A successful material-reference campaign is not by
itself scientific validation. Parent-model error, discretization error, and
model-reduction error remain separate.

Production Quantum ESPRESSO or Wannier90 calculations, remote jobs, destructive data
operations, dependency changes, and publication actions remain protected. This
campaign architecture supplies no authority to perform them.

## Relationship to retained campaigns

Existing retained periodic1d and periodic2d classes mix historical façade naming,
immutable retained-wire models, correlation, and verification delegation. Migration
must preserve their exact retained payloads and result provenance while separating
future scientific-model ownership from executable campaign ownership. No retained
result is rewritten merely to adopt the target hierarchy.
