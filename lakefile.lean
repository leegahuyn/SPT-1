import Lake

open Lake DSL

package «research-paper-formalization-audit» where
  version := v!"1.0.0"

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "93594942ef3b93fae5272d7bf368676ff40f8eb1"

@[default_target]
lean_lib ResearchPaperFormalizationAudit where
  roots := #[`BuildAll]
