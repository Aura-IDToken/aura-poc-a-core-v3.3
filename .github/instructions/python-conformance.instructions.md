---
applyTo: "**/*.py"
---

# Python Conformance Instructions

These instructions apply to Python files and govern Python-side implementation behavior in Aura conformance restoration.

## Role

Copilot performs implementation and testing work only after an approved conformance requirement exists.

## Python-Specific Requirements

- Do not use Python `assert` for security or compliance enforcement.
- Preserve deterministic behavior and avoid semantics-changing refactors without approved conformance requirements.

## Governance Reference

Follow the canonical repository-level governance rules and authority precedence defined in `AGENTS.md`.
