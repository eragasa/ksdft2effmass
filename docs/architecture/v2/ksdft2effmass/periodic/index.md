# `ksdft2effmass.periodic` compatibility package

`ksdft2effmass.periodic` temporarily re-exports the former public inventory without
defining independent classes. New code imports crystal geometry from
[`ksdft2effmass.structures.periodic`](../structures/periodic.md) and electronic
$k$-point sampling from `ksdft2effmass.electronic_structure`.

The compatibility package acquires no new behavior, serializer, calculator policy,
native-format adaptation, molecular topology, or scientific acceptance. Its removal
requires a separately reviewed compatibility decision after current consumers have
migrated.
