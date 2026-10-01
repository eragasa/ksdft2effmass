# `ManuscriptCitationGroup`

Immutable grouping of every occurrence of one literal case-sensitive key. Groups are
ordered by sorted key, retain exact occurrence indexes, separate direct and generated
counts, and optionally bind the matching bibliography entry index. Replay rejects
duplicate group IDs, wrong-key entry bindings, incomplete membership, and count drift.
