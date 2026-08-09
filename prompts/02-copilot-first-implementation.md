# Prompt 02 — Copilot First Implementation

Use this prompt only after approved conformance requirements exist.

## Role

Copilot performs implementation/testing after approved conformance requirements exist.

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

## Governance Reference

Follow `AGENTS.md` for canonical common governance rules and authority precedence.
