---
applyTo: "**/*.rs"
---

# Rust Conformance Instructions

These instructions apply to Rust files and govern Rust-side implementation behavior in Aura conformance restoration.

## Role

Copilot performs implementation and testing work only after an approved conformance requirement exists.

## Rust-Specific Requirements

- Preserve deterministic behavior and reproducible outputs.
- Avoid semantics-changing refactors without approved conformance requirements.

## Governance Reference

Follow the canonical repository-level governance rules and authority precedence defined in `AGENTS.md`.

For language-agnostic compliance constraints (including prohibition of assert-based security/compliance enforcement), use `AGENTS.md` as the canonical source.
