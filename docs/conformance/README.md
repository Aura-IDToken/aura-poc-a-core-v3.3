# Aura Conformance Governance

This directory documents governance for conformance restoration.

## Workflow

Protocol Specification  
→ Protocol Invariants  
→ Conformance Test Matrix  
→ Conformance Gap  
→ Implementation  
→ CI evidence  
→ Adversarial review  
→ Human approval

## Governance Model

- `AGENTS.md` is the canonical repository-level source for common agent governance rules.
- `CLAUDE.md` defines Claude's role for architectural/conformance audit.
- Path-specific instructions in `.github/instructions/` define language-scoped behavior and reference canonical governance in `AGENTS.md`.
- Prompt files in `prompts/` define task-specific execution flow and expected outputs.

## Authority and Conflict Handling

Use the authority precedence defined in `AGENTS.md` and `CLAUDE.md`.

Lower-level instructions MUST NOT override higher-level authority.

If a conflict is detected:
- do not silently reconcile it;
- stop;
- report the conflict;
- request human/Protocol Custodian resolution.

## Scope

Governance-only documentation in this area must not modify protocol semantics or application behavior.
