# Prompt 01 — Claude First Audit

Use this prompt when starting conformance restoration.

## Objective

Produce an architectural/conformance audit before implementation.

## Required Sequence

Protocol Specification  
→ Protocol Invariants  
→ Conformance Test Matrix  
→ Conformance Gap

Stop before implementation and hand off approved requirements.

## Output Requirements

- Explicit AS-IS vs TO-BE sections.
- Enumerated conformance requirements with rationale.
- Mapping from each conformance claim to executable evidence expectations.
- Clear statement of any protocol-affecting implications requiring human approval.

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
