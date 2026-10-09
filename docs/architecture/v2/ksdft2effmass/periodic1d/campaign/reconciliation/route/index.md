# `ksdft2effmass.periodic1d.campaign.reconciliation.route`

## Purpose and scientific question

The route-reconciliation campaign asks whether defect extraction commutes with a
separately implemented transformation between one accepted finite supercell
representation and folded primitive Bloch fibers. It starts only after an explicit
candidate-to-reference coordinate map and scalar energy-reference correction have been
supplied. It therefore tests a finite representation-and-subtraction diagram; it does
not infer an alignment, identify a material model, or establish a continuum result.

For retained hopping blocks $h_R$, Route A assembles the finite site-space operator and
forms

$$
H_d^{(A)}=T(\widetilde H_d-cI)T^\dagger,
\qquad
V^{(A)}=H_d^{(A)}-H_0^{(A)}.
$$

Route B separately evaluates $H(k_j)=\sum_R e^{2\pi i k_jR}h_R$, constructs the folding
map $F$, and forms

$$
V^{(B)}=F^\dagger T(\widetilde H_d-cI)T^\dagger F-\bigoplus_jH(k_j).
$$

The bounded commutativity check is $F^\dagger V^{(A)}F\approx V^{(B)}$. Separate
implementations share authenticated finite synthetic inputs by design; route separation
is not independent physical data.

## Contract mismatches and explicit reconciliation

The campaign keeps representation, alignment, quadrature/domain, truncation, route,
spectral, and eigenspace diagnostics separate. A small spectral discrepancy cannot
cancel operator noncommutativity.

Four altered contracts are fail-closed or explicitly noncommuting:

1. unequal hopping truncations remain a changed-parent comparison;
2. unequal cell/fiber domains stop before subtraction;
3. nonuniform weights stop the unitary-folding route; and
4. unequal alignment maps stop before cross-route subtraction.

Paired controls proceed only after declaring the missing contract: a common truncated
parent, a common finite domain, the inverse and induced metric for weighted coordinates,
or a relative unitary between alignment frames. These constructions do not retroactively
make the original mismatched routes comparable.

## Retained result status

The retained v1 artifact reports seven synthetic null, local, nonlocal, collinear-spin,
and spin-mixing controls within its frozen $10^{-11}$ algebraic threshold. It also
retains one explicit parent-truncation noncommutativity and three structural stops,
followed by four declared reconciliation controls. Those are retained calculated
synthetic software/numerical-verification observations. This dossier does not recompute
them or elevate them to scientific validation.

## Ownership and implementation mapping

The implemented canonical package is
`ksdft2effmass.periodic1d.campaign.reconciliation.route`. Row 066 moved the source
family there without an alias, wire change, or dependency on the former underscored
campaign route. The reviewed leaf and `reconciliation` parent facades export exactly
`RouteReconciliationCampaign`, `RouteReconciliationCampaignResultDocument`, and
`RouteReconciliationEncodedDocuments`.

| Module | Responsibility | Canonical page |
|---|---|---|
| `campaign` | Typed calculation/correlation requests and facade entry points | [Campaign](campaign/index.md) |
| `workflow` | Closed campaign contracts, authentication, explicit alignment map, two independent extraction routes, and result assembly | [Workflow](workflow/index.md) |
| `verification` | Independent retained authentication and numerical reconstruction | [Verification](verification/index.md) |
| `encoded_documents` | Exact input and retained-result bytes only | [Encoded documents](encoded_documents/index.md) |
| `result_documents` | Exact result wire and derived content identity | [Result documents](result_documents/index.md) |

Repository location is operation state, not encoded state:

- `RouteReconciliationCalculationRequest` owns exact documents, an absolute root, and
  caller-supplied execution provenance;
- `RouteReconciliationRetainedCorrelationRequest` owns exact documents and the
  absolute root used for retained reconstruction; and
- `RouteReconciliationVerificationRequest` independently owns exact documents and its
  absolute verification root.

Each request checks type and lexical absoluteness without resolving or accessing the
path. Executing calculation and verification first bind both encapsulated input bytes
and the repository input file to the declared input digest; source loaders then
authenticate directly declared source identities. Shared
strict JSON mechanics come from `serialization.json.StrictJsonDecoder` through the
campaign specialization; independent verification retains
its separate numerical reconstruction.

## Encoded-document navigation

| Crosswalk row | Canonical class page |
|---|---|
| `PERIODIC-XWALK-044` | [`RouteReconciliationEncodedDocuments`](encoded_documents/RouteReconciliationEncodedDocuments/index.md) |
| `PERIODIC-XWALK-057` | [`RouteReconciliationCampaignResultDocument`](result_documents/RouteReconciliationCampaignResultDocument/index.md) |

## Row-066 dossier

- **Supported imports:** the leaf and `reconciliation` parent facades expose only the
  campaign, exact result-document, and encoded-document owners named above. Numerical
  route and verifier classes remain available only from their defining modules.
- **Sphinx mapping:** `doc/sphinx/api/ksdft2effmass/periodic1d/campaign/route-reconciliation.rst`
  documents every defining module, both route formulas, stopped mismatches, and
  reconciliation boundaries.
- **Provenance:** exact methods, assumptions, reproduction commands, and bounded
  results remain under
  `calculations/research-monograph/impurity-defect-1d-independent-route/`; migration
  changes no retained bytes and performs no calculator execution.
- **Tests-as-evidence:** canonical facade, former-route removal, import independence,
  exact encoded-document identities, and result-document identity are bound by
  `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/reconciliation/route/`.
  Its mirrored `resources/` manifest records ownership.
- **Claim boundary:** route agreement establishes a finite algebraic commutativity
  result under authenticated synthetic inputs. It does not establish silicon behavior,
  physical adequacy, continuum or infinite-volume convergence, transferability, UQ,
  or acceptance.

Rows 044 and 057 retain the encoded-pair and result-document evidence inherited by
this family. Row 066 additionally establishes canonical ownership, former-route
removal, and independence from transitional periodic campaign imports. No Quantum
ESPRESSO or Wannier90 invocation is part of this campaign or dossier.

Original local work under the repository license.
