# Citation Guide

## Recommended citation

Lee, Ga Hyun. **Research Paper Formalization Audit**. Version 1.0.0, 2026. Lean 4 / Mathlib software and verification artifact. GitHub release `v1.0.0`, `https://github.com/leegahuyn/SPT-1/releases/tag/v1.0.0`.

The exact release tag should be cited rather than the moving `main` branch. GitHub's **Cite this repository** interface reads the machine-readable metadata in `CITATION.cff`.

## BibTeX

```bibtex
@software{lee_research_paper_formalization_audit_2026,
  author  = {Lee, Ga Hyun},
  title   = {Research Paper Formalization Audit},
  year    = {2026},
  version = {1.0.0},
  url     = {https://github.com/leegahuyn/SPT-1/releases/tag/v1.0.0},
  note    = {AI-assisted Lean 4 / Mathlib audit of ten mathematical manuscript sketches (507 pages)}
}
```

## Exact source provenance

The standalone release is generated from:

- repository: `leegahuyn/mathlib4`;
- ref: `frozen-pre-release-2026-08-24`;
- commit: `3fa18fa989b78eb5bd7068122ced45fc2b6a7b74`;
- upstream Mathlib base: `93594942ef3b93fae5272d7bf368676ff40f8eb1`;
- Lean toolchain: `leanprover/lean4:v4.33.0-rc1`.

## Related sources that should be cited separately

Citing this repository does not replace citation of the mathematical manuscripts, Mathlib, Lean, or any external mathematical sources used by a paper.

When the integrated manuscript bundle is substantively used, identify it by its recorded snapshot:

- `overleaf_bundle (Copy)(20260812-034123).pdf`;
- 507 physical pages;
- 4,304,556 bytes;
- SHA-256 `12eb737301b3312dbad255f7b6d2f74c43c9ba27a2955157c134d36c9c0e53c5`.

When Mathlib is substantively used, follow the citation guidance distributed with the pinned Mathlib revision.

## Scope of the citation

This citation identifies the software and formal-audit artifact. It must not be paraphrased as a claim that all ten manuscripts were proved in full. The repository contains a mixture of kernel-checked proofs, conditional results, certificates, interfaces, corrected statements, and no-go or counterexample evidence.