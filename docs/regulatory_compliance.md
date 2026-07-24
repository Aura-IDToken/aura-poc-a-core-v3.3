# Aura Protocol: Regulatory Compliance

## Positioning

Aura Protocol is a deterministic measurement protocol.
It performs measurement only; compliance decisions are external.

## Article 5 — Prohibited AI practices

**Status:** COMPLIANT

Current implementation points:
- `compliance.policy.RegulatoryPolicy.validate_target()` enforces `MACHINE_ACCOUNT`
- documentation and examples use machine-account scope only
- no human identity persistence is documented as part of the measurement flow

## Article 13 — Transparency

**Status:** COMPLIANT

Current implementation points:
- Layer 0 measurement is implemented in `core.evaluator.PoCAEvaluator`
- outputs are integer-scaled and deterministic
- cryptographic audit helpers exist in `core.merkle` and `audit.merkle`
- certificate rendering is implemented in `compliance.renderer`

The documented runtime formula is:

```text
ARI = weighted structural integrity + weighted semantic alignment - Layer 2 penalty
```

The repository documents the exact integer-scaled implementation in `docs/mathematical_foundation.md`.

## Article 14 — Human oversight

**Status:** COMPLIANT

Current implementation points:
- `compliance.policy.KillSwitch`
- `compliance.policy.get_kill_switch()`
- `compliance.policy.RegulatoryPolicy.emergency_halt()`
- `compliance.evaluator_wrapper.evaluate_with_policy()` performs halt checks before policy-aware measurement

## Layer separation

CORE-005 restored the documented layer boundary.

- Layer 0 measures.
- Layer 1 provides cryptographic proofs.
- Layer 2 applies policy and renders outputs.
- `core.policy` and `core.consistency` remain deprecated compatibility wrappers only.

## Naming rules

Approved repository terminology:
- **Aura Protocol**
- **deterministic measurement protocol**
- **PoCA** for the measurement method
- **ARI** for the measurement value

Avoid describing Aura Protocol as a decision engine, monitoring platform, product, or service.
