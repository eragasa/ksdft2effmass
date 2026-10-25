# Rank-two dimensional-comparison technical report

## Scope

This report covers the cross-family comparison of four controlled rank-two calculations: orthogonal and nonorthogonal families in two and three spatial dimensions. It does not define a fifth physical model.

## Method

The analysis entrypoints load each calculation-owned typed family definition explicitly. They calculate a common tolerance-requirement map and the sampled shell--scale decision landscapes, including matched Bravais controls and the two basis-aware families.

## Evidence status

The generated comparison records and figures are replaceable development artifacts. They are not an immutable retained run or a paper-specific production package.

## Interpretation boundary

A difference among these controlled families is not, by itself, a dimensional law or a material trend. Spatial dimension, lattice geometry, basis structure, parent scale, and retained rank must remain separately identified.

## Provenance

The comparison protocol remains in the experiment tree. Each model definition is loaded from its calculation owner, while reusable calculators, serializers, and plotters remain under `python/src/ksdft2effmass/`.
