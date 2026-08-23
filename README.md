# Research Paper Formalization Audit

[![Verify standalone artifact](https://github.com/leegahuyn/SPT-1/actions/workflows/verify.yml/badge.svg?branch=main)](https://github.com/leegahuyn/SPT-1/actions/workflows/verify.yml)
[![Publish verified release](https://github.com/leegahuyn/SPT-1/actions/workflows/publish.yml/badge.svg?branch=main)](https://github.com/leegahuyn/SPT-1/actions/workflows/publish.yml)
[![GitHub release](https://img.shields.io/github/v/release/leegahuyn/SPT-1?display_name=tag)](https://github.com/leegahuyn/SPT-1/releases)

**Standalone public artifact for an AI-assisted Lean 4 / Mathlib audit of ten mathematical manuscript sketches (507 pages).** GPT and Codex were used to help translate statements, generate and repair Lean code, search for proofs, isolate assumptions, construct counterexamples, and document the audit. The Lean kernel checks compiled proof terms; separate human review remains necessary to decide whether each formal statement faithfully represents the corresponding manuscript claim.

**Scope:** 10 manuscript sketches · 507 physical PDF pages · approximately 352,000 lines of Lean source  
**Proof assistant:** Lean 4 + Mathlib  
**Pinned Lean toolchain:** `leanprover/lean4:v4.33.0-rc1`  
**Release line:** `v1.0.0`  
**License:** Apache-2.0

> This repository does **not** claim that every sentence in all ten manuscripts has been proved. It publishes machine-checkable proofs, conditional results, certificates, formal interfaces, corrections, counterexamples, and reproducible verification evidence for the formalizable cores represented by the Lean declarations.

## Publication authority

The repository default branch is `main`. A branch name, README statement, file size, warning count, or workflow name is not by itself verification evidence.

The immutable publication authority is the exact commit targeted by a GitHub release tag. The `v1.0.0` release is created by `.github/workflows/publish.yml` only after all release gates succeed:

1. the project sources are copied from the frozen source commit recorded below;
2. Lean and Mathlib dependencies are pinned;
3. a source audit rejects `sorry`, `admit`, `sorryAx`, explicit `axiom` declarations, and `native_decide` in the published project sources;
4. the aggregate Lake target is built twice from a deleted local build directory;
5. `BuildAll.lean` is replayed after each build;
6. source hashes, environment information, inventories, audit output, and build logs are preserved under `evidence/release-v1.0.0/` and attached to the GitHub release.

The ordinary verification workflow repeats the audit and aggregate build for subsequent pushes and pull requests.

## Frozen provenance

This standalone artifact is generated from the following immutable source snapshot:

- source repository: `leegahuyn/mathlib4`;
- source ref: `frozen-pre-release-2026-08-24`;
- source commit: `3fa18fa989b78eb5bd7068122ced45fc2b6a7b74`;
- pinned upstream Mathlib base: `93594942ef3b93fae5272d7bf368676ff40f8eb1`;
- Lean toolchain: `leanprover/lean4:v4.33.0-rc1`.

The source snapshot remains untouched as a historical provenance anchor. This repository is the smaller, project-facing standalone publication copy.

## Manuscript bundle

Integrated bundle: [10 manuscripts / 507 pages](https://drive.google.com/file/d/1nmbfHF5Qkw8kFMwHn9CmnjWpGZuGKi2X/view)

Exact audited bundle identity:

- filename: `overleaf_bundle (Copy)(20260812-034123).pdf`;
- physical pages: `507`;
- size: `4,304,556` bytes;
- SHA-256: `12eb737301b3312dbad255f7b6d2f74c43c9ba27a2955157c134d36c9c0e53c5`.

The access URL is convenient for reading; the filename, size, and SHA-256 are the identity anchor for exact-byte comparison.

## Manuscripts and primary Lean modules

| # | Manuscript | Bundle pages | Primary Lean authority |
|---:|---|---:|---|
| 1 | **Primality Sheaf via Local Filters and Derived Equalizers** | 5–26 | `Spt1.lean`; focused audit in `Verification.lean` |
| 2 | **Master Equivalence on Arithmetic Curves** | 27–51 | `Spt2.lean` |
| 3 | **A Primality Sheaf and Global Certification** | 52–91 | `Spt3.lean` |
| 4 | **Primality Sheaves and the Étale–Motivic–Derived Package on Arithmetic Curves** | 92–145 | `Spt4.lean` |
| 5 | **Principal-Open Methods on Arithmetic Curves: From Equalizer–Tor to Supersingular Dichotomy** | 146–183 | `Spt5.lean` |
| 6 | **Equalizer–Tor, Gate Synchronization, and Étale–Motivic Detectors on Arithmetic Curves** | 184–226 | `Spt6.lean` |
| 7 | **Geometric Reformulation of the Riemann Hypothesis via a Four-Layer Sheaf Framework** | 227–297 | `Spt7.lean` |
| 8 | **Entropy–Growth and Sheaf Stability for Mock/Partial Theta and Jacobi Objects** | 298–397 | `Mock1.lean`, `Mock1_Advanced.lean` |
| 9 | **Global Poincaré Matching and Kloosterman-Compatible Test Kernels for Half-Integral Weight Mock–Theta Gauge Objects** | 398–458 | `Mock2.lean`, `Mock2_Advanced.lean`, `Mock2_FunctionalAnalysis.lean` |
| 10 | **Modular q–Yang–Mills on Γ(2)\H: Admissible Gauge Slices, Modular Flow, and a Spectral Mass–Gap Mechanism** | 459–507 | `QYM.lean` |

The thirteen primary verification modules are `Spt1`–`Spt7`, the two Mock 1 modules, the three Mock 2 modules, and `QYM`. `Mock2_FunctionalAnalysis_Integrated.lean` and `Mock3.lean` are mandatory integration bridges. `Verification.lean` is a focused Paper 1 audit and is not counted among the thirteen primary modules.

The canonical aggregate importer is `PrimalitySheafVerification/BuildAll.lean`; the repository-root `BuildAll.lean` is the public entry point.

## Reproduce the release check

```bash
git clone https://github.com/leegahuyn/SPT-1.git
cd SPT-1
git checkout v1.0.0

lake exe cache get
python3 scripts/audit_lean.py --json-out /tmp/lean-audit.json

rm -rf .lake/build
lake build ResearchPaperFormalizationAudit
lake env lean BuildAll.lean
```

To repeat the clean project build:

```bash
rm -rf .lake/build
lake build ResearchPaperFormalizationAudit
lake env lean BuildAll.lean
```

The release workflow records the actual exit status and complete logs. A successful local command checks the formal artifact under the local environment; it does not replace statement-correspondence review.

## Result-status vocabulary

| Label | Meaning |
|---|---|
| **PROVED** | The stated Lean theorem has a kernel-checked proof from its declared imports and assumptions, without a silent project-specific conjecture. |
| **CONDITIONAL** | Lean proves the result from explicit hypotheses that encode assumptions not established by this project. |
| **CERTIFICATE** | Lean checks a concrete witness, finite computation, identity, or bound relevant to a manuscript claim. |
| **INTERFACE** | A formal specification or abstraction boundary is provided without claiming the complete surrounding narrative. |
| **CORRECTED** | Formalization exposed a problem and the repository proves or checks a corrected formulation. |
| **NO-GO** | The original formulation is false, inconsistent, or unsupported at the claimed level; blocker or counterexample evidence is preserved where available. |

These are semantic audit labels, not decorations. They must be assigned only after checking both the Lean declaration and its manuscript interpretation.

## Example of a correction exposed by formalization

The primality-sheaf audit distinguishes two quantities that had been conflated in the manuscript narrative:

- the `p`-adic valuation of the relevant `lcm` / localized intersection uses `max`;
- the valuation of the `gcd` / common-residue-fiber / `Tor₁` quantity uses `min`.

For `M = 12`, `p = 3`, and `k = 2`, the intersection is generated by `lcm(12, 9) = 36`, whose 3-adic thickness is `2 = max(1, 2)`, whereas the common-residue quantity has exponent `1 = min(1, 2)`. This illustrates the repository's intended role: formal checking separates mathematically different objects and can force a manuscript statement to be corrected.

## AI-use disclosure

This project is explicitly AI-assisted. GPT and Codex contributed to manuscript-to-formal-statement translation, Lean code generation, proof-search assistance, refactoring, debugging, candidate generation, documentation, and failure analysis.

The project does not claim that one person manually typed or independently discovered every line. AI output is also not accepted as mathematical authority merely because it is plausible or extensive. For compiled declarations, Lean's kernel checks the proof term. Human and scholarly responsibility remains for at least the following questions:

1. Does the Lean statement express the manuscript claim it is said to audit?
2. Were hypotheses weakened, strengthened, or silently changed?
3. Is the result unconditional, conditional, a certificate, or only an interface?
4. Does a computational certificate support the broader interpretation attached to it?
5. Has a correction or counterexample been interpreted properly in context?

## What an independent reviewer should inspect first

1. Confirm the release tag and exact target commit.
2. Compare the manuscript bundle with the recorded SHA-256 when exact identity matters.
3. Run the aggregate build from a clean checkout.
4. Read `evidence/release-v1.0.0/forbidden-audit.json` and the build logs.
5. Check theorem statements against the corresponding manuscript passages.
6. Identify every explicit hypothesis behind results described as conditional.
7. Review the correction and counterexample catalogue rather than relying on line count.

## Repository layout

```text
BuildAll.lean
PrimalitySheafVerification/
  BuildAll.lean
  Verification.lean
  Spt1.lean … Spt7.lean
  Mock1.lean
  Mock1_Advanced.lean
  Mock2.lean
  Mock2_Advanced.lean
  Mock2_FunctionalAnalysis.lean
  Mock2_FunctionalAnalysis_Integrated.lean
  QYM.lean
  Mock3.lean
scripts/
  audit_lean.py
  generate_evidence.py
evidence/
  release-v1.0.0/
CITATION.cff
CITATION.md
PROVENANCE.md
RELEASE_NOTES.md
lakefile.lean
lake-manifest.json
lean-toolchain
```

## Citation

GitHub displays citation metadata from `CITATION.cff`. For a stable scholarly reference, cite the exact release tag rather than a moving branch. See `CITATION.md` for a ready-to-use reference and BibTeX entry. Cite the manuscript bundle and Mathlib separately when they are substantively used.

## Discovery metadata

Intended GitHub topics:

`lean4` · `mathlib` · `formal-mathematics` · `theorem-proving` · `formal-verification` · `ai-assisted-mathematics`

No Zulip or community announcement is required for this artifact to remain public and independently discoverable.