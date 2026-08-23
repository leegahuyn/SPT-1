# Release Notes — v1.0.0

## Research Paper Formalization Audit

This is the first standalone publication release of the AI-assisted Lean 4 / Mathlib audit of ten mathematical manuscript sketches comprising 507 pages.

## Included

- thirteen primary verification modules covering `Spt1`–`Spt7`, Mock 1, Mock 2, and QYM;
- the mandatory integration bridges `Mock2_FunctionalAnalysis_Integrated.lean` and `Mock3.lean`;
- the focused Paper 1 audit `Verification.lean`;
- the aggregate importers `PrimalitySheafVerification/BuildAll.lean` and root `BuildAll.lean`;
- pinned Lean and Mathlib dependencies;
- explicit AI-use disclosure and result-status vocabulary;
- machine-readable and human-readable citation metadata;
- immutable frozen-source provenance plus an audit-recorded derived-release patch;
- forbidden-feature audit tooling;
- clean-build and direct-replay logs;
- source inventories and SHA-256 hashes.

## Frozen inputs

- source commit: `3fa18fa989b78eb5bd7068122ced45fc2b6a7b74`;
- upstream Mathlib commit: `93594942ef3b93fae5272d7bf368676ff40f8eb1`;
- Lean toolchain: `leanprover/lean4:v4.33.0-rc1`;
- manuscript bundle SHA-256: `12eb737301b3312dbad255f7b6d2f74c43c9ba27a2955157c134d36c9c0e53c5`.

## Deterministic publication rewrite

The frozen source is not altered. In the standalone copy, the sole `native_decide` occurrence in `PrimalitySheafVerification/Verification.lean`—a nine-element `ZMod 9` finite-cardinality certificate—is replaced with `decide`. The proposition is unchanged. The release audit records the exact before/after text and source SHA-256 values and rejects any unexpected match count.

## Release gate

The release is created only after the publication workflow reports success for the deterministic rewrite, the prohibited-feature audit, two clean aggregate builds, and two direct `BuildAll.lean` replays. The corresponding evidence files are attached to the release and committed under `evidence/release-v1.0.0/`.

## Scope limitation

This release does not claim that every sentence of every manuscript has been formally proved. The artifact contains a mixture of kernel-checked proofs, explicit conditional results, certificates, formal interfaces, corrected statements, and no-go or counterexample evidence. Mathematical interpretation and statement correspondence require independent review.