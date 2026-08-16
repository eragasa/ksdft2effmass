# ksdft2effmass

`ksdft2effmass` is an open-source research project for constructing and testing
effective models of dopants in semiconductors from first-principles electronic
structure calculations.

The project compares atomistic dopant Hamiltonians with the screened impurity
potentials used in effective-mass theory. It is part of a broader effort to
develop and validate systematic Hamiltonian-reduction methods connecting
first-principles operators to effective lattice and continuum models.

> **Development status:** Active development occurs on the `dev` branch.
> The `main` branch contains the latest reviewed software snapshot associated
> with a conference presentation, paper, or other formal research output.
> Intermediate commits and automated builds from `dev` are provisional.
>
> Only signed semantic-version releases of the form `vMAJOR.MINOR.PATCH` are
> intended to be cited as reviewed research software.
## Approach

The central reduction is

$$
\hat H_{\mathrm{KS}}
\longrightarrow
\hat H^{(P)}
\longleftrightarrow
\mathbf H_{\mathrm W}
\longrightarrow
\mathbf H_{\mathrm{red}}
\longrightarrow
\hat H_{\mathrm{continuum}}.
$$

This connects a converged Kohn-Sham Hamiltonian to a selected band subspace, a
localized Wannier representation, a reduced lattice model, and finally a
continuum effective-mass Hamiltonian.

Pristine and doped Wannier Hamiltonians are aligned before their difference is
taken. The resulting impurity operator is then simplified through a hierarchy
of models, from the full atomistic operator to finite-range, onsite, and
screened scalar approximations. Each reduction is tested against the model
above it using operator, spectral, bound-state, and subspace errors.

The goal is not simply to fit an effective-mass model. It is to identify the
simplest model that satisfies declared tolerances and to report where that
model ceases to be reliable.

## Software scope

The Python package will provide tools for:

- importing DFT and Wannier outputs;
- representing Hamiltonians, bases, projectors, and state spaces;
- recording finite operator matrices through the public `ksdft2effmass.operators` API and its versioned operator-record JSON text serialization format (`schema_version = 1`);
- aligning pristine and doped Wannier subspaces;
- extracting and reducing impurity operators;
- solving reduced lattice and continuum models;
- calculating validation metrics and recording provenance.

Large electronic-structure calculations remain with established tools such as
[Quantum ESPRESSO](https://www.quantum-espresso.org/) and
[Wannier90](https://wannier.org/). 

## AI disclosure

Artificial intelligence is used extensively in research planning, software
design, code generation, testing, documentation, literature discovery, and
preliminary analysis.

Material on development branches is provisional and may include incomplete or
unreviewed AI-assisted work. Human review and reproducible scientific
validation are performed when preparing a versioned conference, paper
release, or versioned release.

The author accepts scholarly responsibility for the code, documentation,
numerical results, and scientific claims explicitly included in signed
versioned releases. Intermediate commits, development branches, automated
builds, and continuous-integration artifacts are not designated as reviewed
scientific outputs.

### A note from the author

I am primarily a systems designer and computational materials scientist—not a
computer scientist, mathematician, or theoretical physicist, despite this
repository's occasional attempts to impersonate all three. Some of the territory
covered here is new to me, and the project is consequently broad, exploratory,
and deliberately explicit about its assumptions and uncertainties.

This is also my first sustained professional experience using an AI-agent
harness adapted to scientific-computing workflows and scientific analytical
requirements. AI is used not only to generate code or edit prose, but also to
help externalize context, examine assumptions, organize proof obligations,
coordinate verification, and maintain links between scientific claims and their
computational evidence.

In that sense, the repository contains two experiments. The first is the stated
scientific program: reducing first-principles semiconductor Hamiltonians to
controlled lattice and continuum models. The second is an experiment in whether
an AI-assisted development harness can help one researcher work responsibly
across unusually broad disciplinary boundaries without concealing uncertainty,
discarding provenance, or confusing generated material with validated results.

The experiment is ongoing. AI assistance does not make me an instant expert in
the fields the project touches, and a large volume of structured output is not a
substitute for understanding. Development material should therefore be read as
provisional until its assumptions, derivations, implementation, and scientific
claims have received the review and validation appropriate to a signed release
or publication.

This disclosure does not modify the warranty and liability terms of the
[Apache License 2.0](LICENSE).

## Documentation

The Sphinx documentation includes the finite-operator-record concept page and API reference:

- `docs/concepts/operator-records.rst`
- `docs/api/operators.rst`

These pages document why operator metadata are part of the implementation, the supported `ksdft2effmass.operators` import path, and the versioned operator-record serialization format.

## Citation

This project is developed as research in the open. If you use its software,
methods, or results, cite the exact software release and the relevant research
paper when available. Machine-readable metadata is provided in
[`CITATION.cff`](CITATION.cff).

Suggested citation for the current development version:

> Ragasa, E. J. (2026). *ksdft2effmass: Controlled reduction of Kohn-Sham DFT
> operators to effective-mass models* [Research software]. GitHub.
> <https://github.com/eragasa/ksdft2effmass>

Author: [Eugene J. Ragasa](https://orcid.org/0000-0002-3856-734X),
Department of Physics, De La Salle University, Manila, Philippines.

## License

Copyright 2026 Eugene J. Ragasa.

Licensed under the [Apache License 2.0](LICENSE). Separately installed optional
dependencies retain their own licenses; see
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).
