# Copilot Conformance Instructions

These instructions govern Copilot behavior for Aura conformance restoration.

## Role

Copilot performs implementation and testing work only after an approved conformance requirement exists.

## Workflow Order (Required)

Protocol Specification  
→ Protocol Invariants  
→ Conformance Test Matrix  
→ Conformance Gap  
→ Implementation  
→ CI evidence  
→ Adversarial review  
→ Human approval

## Mandatory Rules

1. Protocol specification has authority over implementation.
2. Do not silently change protocol semantics.
3. Distinguish AS-IS from TO-BE in every change proposal.
4. Do not rely on Python assert for security/compliance enforcement.
5. Do not treat process-local global state as distributed safety guarantees.
6. Do not introduce floating-point runtime where Zero-Float Runtime is required.
7. Do not infer compliance claims from architecture names or README language.
8. Distinguish regulatory claims from enforceable technical constraints.
9. Back every conformance claim with executable evidence.
10. Do not weaken tests merely to make implementation pass.
11. Respect Claude's role as architectural/conformance auditor.
12. Perform implementation/testing only after approved conformance requirements exist.
13. Require human approval before any protocol-affecting merge.

## Governance-Only Changes

For governance-only tasks, modify only governance/instruction documentation files and leave application source, tests, protocol specifications, constitutional documents, ADRs, CI workflows, compliance logic, and policy logic untouched.
