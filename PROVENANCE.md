# Provenance

## Standalone publication target

- repository: `leegahuyn/SPT-1`;
- default branch: `main`;
- release line: `v1.0.0`;
- publication date: 2026-08-24.

## Frozen source authority

The standalone Lean tree is derived, without selecting a later moving branch, from:

- source repository: `leegahuyn/mathlib4`;
- source ref: `frozen-pre-release-2026-08-24`;
- exact source commit: `3fa18fa989b78eb5bd7068122ced45fc2b6a7b74`.

The frozen source snapshot remains untouched as the historical authority. The standalone publication workflow copies that tree and then applies exactly one deterministic, audit-recorded release rewrite:

- file: `PrimalitySheafVerification/Verification.lean`;
- statement: the finite `ZMod 9` kernel-cardinality certificate;
- frozen proof: `by native_decide`;
- standalone proof: `by decide`;
- purpose: remove native-code execution from the published proof source while retaining a kernel-reduced decision proof of the same proposition.

The audit report records the before-and-after source SHA-256 values and refuses to proceed unless the frozen input matches exactly one expected occurrence. No other source rewrite is approved by the release tooling.

## Dependency authority

- upstream Mathlib commit: `93594942ef3b93fae5272d7bf368676ff40f8eb1`;
- Lean toolchain: `leanprover/lean4:v4.33.0-rc1`;
- dependency resolution: committed `lake-manifest.json` generated from the pinned `lakefile.lean`.

The publication workflow checks whether the frozen source modified `Mathlib/`, `Mathlib.lean`, `lakefile.lean`, or `lean-toolchain` relative to the recorded upstream base. A nonempty core-difference report blocks the standalone release until the dependency boundary is understood and documented.

## Manuscript-bundle identity

- filename: `overleaf_bundle (Copy)(20260812-034123).pdf`;
- physical pages: 507;
- size: 4,304,556 bytes;
- SHA-256: `12eb737301b3312dbad255f7b6d2f74c43c9ba27a2955157c134d36c9c0e53c5`.

## Release evidence

A verified release preserves, at minimum:

- the exact frozen-source and dependency identifiers;
- the deterministic publication-rewrite record and before/after hashes;
- the Lean and Lake versions observed on the runner;
- an inventory and SHA-256 list for the published source files;
- the forbidden-feature audit result;
- two clean aggregate-build logs;
- two direct `BuildAll.lean` replay logs;
- repository-metadata configuration results;
- the exact GitHub release tag and target commit.

Evidence is stored under `evidence/release-v1.0.0/` and attached to the GitHub release.

## Interpretation boundary

The Lean kernel verifies compiled declarations from their formal statements and declared assumptions. Provenance and successful compilation do not by themselves establish that every Lean statement is an exact formalization of every surrounding manuscript sentence. Statement correspondence, mathematical interpretation, conditionality, and scholarly attribution require separate review.

## AI assistance

GPT and Codex were used for formal-statement translation, Lean code generation, proof search, refactoring, debugging, candidate generation, documentation, and failure investigation. AI assistance is disclosed rather than treated as an independent source of mathematical authority.