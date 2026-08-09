# Prompt 01 — Claude First Audit

Use this prompt when starting conformance restoration.

## Role

Claude performs architectural/conformance audit and requirement definition before implementation.

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

## Governance Reference

Follow `AGENTS.md` for canonical common governance rules and authority precedence.
