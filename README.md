# Aura Protocol: Iron Core (Sandbox Minimal)
Deterministic Proof-of-Consistent-Agency (PoCA) for the 2026 AI Regulatory Sandbox.

---

## Overview

**aura-poc-a-core** is a minimal, deterministic core for evaluating and proving
the consistency of autonomous AI agents (MACHINE_ACCOUNT entities only) against 
their declared intent and hard constraints.

**SCOPE:** Strictly limited to MACHINE_ACCOUNT entities.
**PROHIBITION:** Absolute prohibition of human profiling or biometric data processing (AI Act Art. 5).

This repository implements the *foundational execution layer* only.

No UX.  
No tokens.  
No narratives.

Only verifiable logic.

---

## What This Is

A **Proof-of-Consistent-Agency (PoCA)** engine that:

- deterministically evaluates agent actions
- detects semantic drift from declared intent
- produces cryptographically verifiable audit artifacts
- generates compliance-ready outputs (AI Act–oriented)

---

## What This Is NOT

Out of scope by design:

- ❌ UI / dashboards
- ❌ wallets / tokens / blockchain protocols
- ❌ monetization logic
- ❌ identity issuance
- ❌ orchestration layers
- ❌ hype abstractions

This repo is a **core primitive**, not a product.

---

## Core Components

### `/core`
Deterministic execution layer.

Responsibilities:
- Structural integrity validation
- Semantic alignment scoring (cosine similarity in ℝ¹⁵³⁶ space)
- Policy enforcement
- Agent Reliability Index (ARI) calculation

Output:
- Agent Reliability Index (ARI) ∈ [0.0 – 1.0]
- Drift signal
- Deterministic metadata

**Formula:** ARI = 0.3 × StructuralIntegrity + 0.7 × SemanticAlignment - Penalties

**Note:** Uses "Agent Reliability Index" (ARI), NOT "Trust Score" to avoid Social Scoring classification.

---

### `/compliance`
Cryptographic audit layer.

Responsibilities:
- Merkle tree construction
- Immutable event anchoring
- Proof-of-existence generation
- Non-repudiation support

Output:
- Merkle root
- Per-event Merkle proofs
- Verifiable audit artifacts

---

### `/docs`
Specification & intent layer.

Responsibilities:
- System assumptions
- Threat model
- Determinism constraints
- Regulatory mapping (e.g. AI Act transparency)

---

## Determinism Guarantee

This system is designed to be:

- deterministic by construction
- reproducible across environments
- auditable without privileged access
- explainable via cryptographic proofs, not narratives

Same input → same output.  
No hidden state.  
No stochastic execution paths.

---

## Compliance Orientation

Designed with:
- AI Act (Art. 13 – transparency & traceability)
- audit-first architecture
- privacy-preserving verification (Merkle proofs)
- regulator-facing evidence generation

This is **Law-as-Code**, not post-hoc reporting.

---

## Project Status

**Status:** Research-backed prototype  
**Phase:** Core implementation  
**Stability:** Interfaces subject to refinement, logic is fixed

---

## License

MIT  
(New codebase. No code continuity with archived repositories.)

---

## Guiding Principles

### Krasinski Principle
> **T ∝ 1/S**  
> Transparency (T) is inversely proportional to Secrecy/Entropy (S).  
> Trust is modeled as behavioral consistency, not moral virtue.

### Core Axiom
> Trust is not asserted.  
> Trust is computed — and proven.

### Regulatory Compliance
- **Agent-Only Scope:** MACHINE_ACCOUNT entities exclusively
- **AI Act Art. 5:** Absolute prohibition of human profiling or biometric data
- **Nomenclature:** "Agent Reliability Index" (ARI) - NOT "Trust Score"
- **Determinism:** Same input → Same ARI (Proof of Consistent Agency)

---

## Execution Checks

All changes MUST pass mandatory execution checks before merge.

### Running the Checks

```bash
./scripts/run_all_checks.sh
```

### The 5 Mandatory Checks

1. **Bit Identity** - Tests produce identical hashes on x86 and ARM
2. **Integer Only** - No float/sqrt/numpy in runtime core
3. **Layer Separation** - core/ measures only, doesn't decide
4. **Audit Path** - Every metric traceable to integer math → Merkle leaf
5. **Entropy** - No changes that increase system entropy/nondeterminism

**If any check fails: DO NOT MERGE**

For details, see:
- `.github/copilot-checks.md` - Check definitions
- `scripts/checks/README.md` - Check documentation

---
