# Prompt 02 — Copilot First Implementation

Use this prompt only after approved conformance requirements exist.

## Objective

Implement and test against approved conformance requirements while preserving protocol semantics.

## Required Sequence

Conformance Gap  
→ Implementation  
→ CI evidence  
→ Adversarial review  
→ Human approval

## Output Requirements

- Explicit references to approved requirements.
- AS-IS vs TO-BE mapping in implementation notes.
- Evidence checklist tying each conformance claim to executable validation.
- Explicit callout for any change that could affect protocol semantics.

## Mandatory Governance Rules

1. Protocol specification has authority over implementation.
2. Agents must not silently change protocol semantics.
3. Agents must distinguish AS-IS from TO-BE.
4. No security or compliance enforcement may rely on Python assert.
5. No process-local global state may be treated as a distributed safety guarantee.
6. No floating-point runtime must be introduced where the protocol requires Zero-Float Runtime.
7. Compliance claims must not be inferred merely from architecture names or README language.
8. Regulatory claims must be distinguished from enforceable technical constraints.
9. Every conformance claim must have executable evidence.
10. Tests must not be weakened merely to make implementation pass.
11. Claude's role is architectural/conformance audit.
12. Copilot's role is implementation/testing after an approved conformance requirement exists.
13. Human approval is required before merging protocol-affecting changes.
