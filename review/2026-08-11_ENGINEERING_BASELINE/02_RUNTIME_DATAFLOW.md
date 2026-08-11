# 02 — RUNTIME DATA FLOW (TASK 2)

**Rule applied:** document only what the code actually does. Missing steps are recorded
as missing. No step is inferred, completed, or assumed.

---

## 1. Headline Finding

**There is no single runtime pipeline.**

The canonical flow named in the task —
`input → normalization → vector → arithmetic → similarity → policy → result →
serialization → evidence` — does **not** exist as a connected code path in
`aura-poc-a-core-v3.3`.

What exists is **three disconnected fragments**, plus one broken demo. No caller in the
repository traverses the full chain. The longest actually-executed path
(`test_compliance.py::test_integrated_poca_flow`) stops before persistence and uses a
different arithmetic engine than the one CI exercises.

---

## 2. Fragment A — Offline Normalization (complete, isolated)

```
constitution_float : list[float]  (caller-supplied, or generate_sample_constitution())
        │
        │ core/offline_normalizer.py:178   normalize_vector()
        ▼
  magnitude = math.sqrt(sum(x*x))          ← FLOAT (offline, by design)
  normalized = [x / magnitude for x in v]  ← FLOAT division
        │
        │ core/offline_normalizer.py:181   scale_to_fixed_point()
        ▼
  int_vector = [round(x * 100000) for x in normalized]   ← Python round() = half-to-even
        │
        │ core/offline_normalizer.py:185   verify_unit_vector()  [optional, default on]
        ▼
  assert 99000 <= sqrt(sum(v_i^2)) <= 101000     (1 % tolerance)
        │
        │ core/offline_normalizer.py:192   [optional]
        ▼
  JSON file: {"vector": [...], "dimension": 1536, "scaling_factor": 100000,
              "spec_version": "v3.3", "description": "..."}
```

**Dimension is enforced here** (`:171`, must equal 1536) and **only** here.

**Terminates.** No code path takes the output of this fragment and feeds it to Fragment B
or C at runtime. The only consumers are:
- `core/test_bitwise_replay.py:57` (hashes it),
- `scripts/generate_determinism_report.py:83` (hashes it),
- `core/test_offline_normalizer.py` (asserts on it).

**No production caller.** The written `constitution_int32.json` is never read back by any
non-test code.

---

## 3. Fragment B — Layer 0 / Layer 2 Evaluation (the CI-adjacent path)

```
caller supplies:  agent_id: str
                  vector: list[int]      ← ASSUMED already normalized; never checked
                  valid_schema: bool
                  constitution: list[int] ← passed to PoCAEvaluator.__init__
        │
        │ compliance/evaluator_wrapper.py:59
        ▼
  RegulatoryPolicy.check_halt_status(agent_id)
        │   → raises Exception("POLICY_HALT: …") if agent_id in a PROCESS-LOCAL set
        │     (compliance/policy.py:29,33)
        ▼
        │ compliance/evaluator_wrapper.py:63
        ▼
  sa = evaluator.vector_similarity_int32(vector, evaluator.constitution)
        │   dot = sum(a*b for a,b in zip(v1, v2))       ← zip: silent truncation
        │   sa  = dot // 100000                          ← floor division
        ▼
        │ compliance/evaluator_wrapper.py:66
        ▼
  penalty = RegulatoryPolicy.calculate_penalties(sa)
        │   = 150000 if sa < 68000 else 0                (compliance/policy.py:39)
        ▼
        │ compliance/evaluator_wrapper.py:69
        ▼
  result = evaluator.evaluate(agent_id, vector, valid_schema)
        │   si  = 100000 if valid_schema else 0
        │   sa  = vector_similarity_int32(vector, constitution)   ← RECOMPUTED (2nd time)
        │   raw = (30000*si)//100000 + (70000*sa)//100000
        │   raw = max(0, raw)                              ← no upper clamp
        │   drift = min(max(0, 100000 - sa), 200000)
        │   → {"ari": raw, "drift": drift}
        ▼
        │ compliance/evaluator_wrapper.py:72
        ▼
  adjusted_ari = max(0, result["ari"] - penalty)
        ▼
  RETURN {"ari": int, "drift": int}
```

**Where this fragment ends:** at a plain Python dict. There is **no** serialization, **no**
certificate, **no** hashing, **no** persistence downstream of `evaluate_with_policy`.

**Observations:**
- `SA` is computed **twice** per call on identical inputs (`:63` and inside `evaluate`).
  Both use the same code, so results agree; the cost is redundancy, not divergence.
- The halt check reads process memory only. `init.sql`'s `kill_switch_state` table is
  never consulted.
- No input validation of any kind occurs on `vector`: not length, not magnitude, not
  element type, not `None`.

**Callers:** `core/test_ari.py`, `core/test_integration.py`, `demo.py`. **Not** called by
any CI check.

---

## 4. Fragment C — Compliance / Evidence (the `test_compliance.py` path)

This is the only fragment that reaches an evidence artefact. It uses a **different**
arithmetic engine than Fragment B.

```
constitution_text : str
        │
        │ core/embedding.py:19        ← PLACEHOLDER embedder
        ▼
  constitution_vec = [(ord(c) % 32) * 3125 …] tiled to 1536
        │
event dict {timestamp, embedding, content, …}
   where embedding = embed_text(event_content)   ← same placeholder
        │
        │ compliance/consistency.py:28   ConsistencyCalculator.calculate()
        ▼
  kill_switch.assert_not_halted()
        │   → returns {"score":0,"status":"HALTED"} instead of raising  (:47-54)
        ▼
  structural = 100000 if {"timestamp","embedding","content"} ⊆ event else 0   (:76)
        │   → if 0: return {"score":0,"status":"FAIL"}
        ▼
  semantic = _semantic_alignment(event["embedding"])                          (:79)
        │   guards: empty → 0 ; all-zero → 0 ; |v| > 100000 → raise ValueError
        │   dot = sum(a*b for a,b in zip(event_vec, constitution))  ← zip truncation
        │   semantic = dot // 100000                                 ← floor division
        ▼
  penalty = 10000 × (number of PolicyRule violations)                         (:99)
        ▼
  score = 30000*structural//100000 + 70000*semantic//100000 - penalty
  score = max(0, min(100000, score))                                          (:62)
        ▼
  {"score", "structural", "semantic", "penalty", "halted"}
        │
        │ test_compliance.py:~230   [test code, not production code]
        ▼
  audit/merkle.py  MerkleTree([event strings])
        │   leaves = SHA-256(utf-8 of each leaf string)
        │   tree built pairwise, odd node duplicated                (audit/merkle.py:157)
        │   root = tree[-1][0]
        ▼
  create_etc(leaf_index, timestamp, batch_id)  → EventTrustCertificate
        │   .verify()          → recompute root from proof
        │   .sign(HMACSigner)  → HMAC-SHA256 over
        │                        json({event_hash, merkle_root, timestamp},
        │                             sort_keys=True, separators=(",",":"))
        ▼
  compliance/certificate.py  AuraEventCertificate(
        agent_id, timestamp, ari_score: FLOAT, drift: FLOAT, status,
        merkle_root, leaf_hash)
        │   ← int32 → float conversion happens HERE (documented at :22-33)
        ▼
  .to_dict()      → {"schema_version":"1.0.0", "agent_id", "timestamp",
                     "ari":{"score","drift","status"}, "audit":{"leaf_hash","merkle_root"}}
  .fingerprint()  → SHA-256(json.dumps(to_dict(), sort_keys=True))
                     ← DEFAULT separators (", " / ": "), unlike the ETC payload above
```

**Where this fragment ends:** at an in-memory certificate and a hex fingerprint. Nothing
is written to disk or to a database.

**Observations:**
- The glue between `ConsistencyCalculator` → `MerkleTree` → `AuraEventCertificate` exists
  **only inside `test_compliance.py`**. There is no production module that performs this
  composition.
- `test_compliance.py` is not collected by `unittest discover` and is not run by CI
  (see `01_CORE_INVENTORY.md` §2.14).
- `compliance/renderer.py` (`render_certificate`) is exported but called by **nothing** —
  not by tests, not by CI, not by `demo.py`.

---

## 5. Fragment D — `demo.py` (broken)

```
constitution = [0.5, 0.3, 0.8, 0.1] * 4        ← FLOATS, 16 elements
PoCAEvaluator(constitution)                     ← accepted without complaint
MerkleAttestor()                                ← core/merkle.py PLACEHOLDER
        │
RegulatoryPolicy.validate_target("MACHINE_ACCOUNT")   → ok
        │
evaluate_with_policy(evaluator, agent_id, [0.52,0.31,0.79,0.09]*4, True)
        │   dot of floats // 100000 → 0
        │   penalty = 150000 (since 0 < 68000)
        │   ari = max(0, 30000 - 150000) = 0
        │   drift = 100000
        ▼
print(f"{ari_result['ari']:.4f}")   → "0.0000"       ← int formatted as float
print(f"{ari_result['drift']:.4f}") → "100000.0000"  ← int32 printed as if a ratio
        │
attestor.generate_etc(ari_result)
        │   returns {"certificate": "AURA-ETC-<leaf[:16]>", "proof": [leaf]}
        │   ← "proof" is the leaf itself; there is no root and nothing to verify against
        ▼
DEMO 2 → RegulatoryPolicy.validate_target("HUMAN") raises ValueError
         demo.py:66 catches AssertionError only  →  UNCAUGHT, PROCESS ABORTS
         DEMO 3 and DEMO 4 never run.
```

Executed verbatim this session; output reproduced in `01_CORE_INVENTORY.md` §2.13.

---

## 6. Stage-by-Stage Reality Check

| Canonical stage | Exists? | Where | Notes |
|---|---|---|---|
| **input** | PARTIAL | caller-supplied dicts / lists | No input schema, no parser, no validation layer. `valid_schema: bool` is supplied *by the caller*, not determined by the system. |
| **normalization** | SPLIT | `core/offline_normalizer.py` (offline only) | Not connected to the runtime path. Runtime assumes normalized input and (in `PoCAEvaluator`) never verifies it. |
| **vector representation** | PARTIAL | `list[int]` in memory | No canonical byte encoding in production code. LE-int32 encoding exists only in `core/test_bitwise_replay.py:295` and `scripts/generate_determinism_report.py:65`. |
| **arithmetic** | YES | `core/evaluator.py:41-47`, `compliance/consistency.py:96-97` | Two implementations. Integer-only at runtime. |
| **similarity / evaluation** | YES | same | Dot product on assumed-unit vectors; floor-divide rescale. |
| **policy** | YES, TWO MODELS | `compliance/policy.py:39` (threshold penalty 150000) and `compliance/consistency.py:99` (10000/violation) | Mutually incompatible; different callers get different semantics. |
| **result** | YES | dict | `{"ari","drift"}` from Fragment B; `{"score","structural","semantic","penalty","halted"}` from Fragment C. Different shapes. |
| **serialization** | PARTIAL | `compliance/certificate.py`, `compliance/renderer.py`, `audit/merkle.py:48` | Reachable only from Fragment C, i.e. only from a test file. Three different JSON canonicalizations. |
| **evidence** | PARTIAL | `audit/merkle.py` ETC + HMAC | Real and well-tested as a subsystem. **Not wired to the evaluation result** by any production module. |
| **persistence** | ABSENT (as code) | `init.sql` schema only | No writer exists. Only test harnesses touch the DB, via `psql` subprocess. |

---

## 7. Connection Points That Do Not Exist

Recorded as absences, with the grep that establishes each:

| Missing link | Evidence of absence |
|---|---|
| `offline_normalizer` output → `PoCAEvaluator` input | No non-test file imports both. `generate_sample_constitution` has 3 callers, all test/script. |
| `PoCAEvaluator` result → `AuraEventCertificate` | `compliance/certificate.py` is imported only by `compliance/__init__.py`, `compliance/renderer.py` and `test_compliance.py`. `evaluator_wrapper.py` imports neither. |
| `PoCAEvaluator` result → `audit/merkle.py` | `audit/` is never imported by `core/` or by `compliance/` (enforced by CHECK 3 and `check_cr003_layer_boundary.py`). Nothing in `compliance/` imports `audit` either. |
| evaluation result → `audit_events` table | 0 hits for `psycopg|asyncpg|sqlalchemy` in all non-test `*.py`. |
| `certificate_schema.json` → any validator | 0 references to the filename anywhere in the repo. |
| `render_certificate` → any caller | 0 call sites outside its own definition and `__all__`. |
| `core/embedding.py` → runtime | 1 caller: `test_compliance.py`. |

---

## 8. What Actually Runs in CI, End to End

For completeness, the only data flow CI genuinely exercises on every push:

```
generate_sample_constitution()          [float → round() → int32, 1536 dims]
        → first 1000 elements
        → LE int32 bytes
        → SHA-256                        = ari_vector_hash

4 fixed event strings
        → SHA-256 leaves
        → MerkleTree                     = merkle_root
        → create_etc(0)  → to_dict()
        → SHA-256                        = etc_hash
        → _signing_payload() → HMAC-SHA256 = hmac_signature_hex

  … then x86_64 vs arm64 comparison of those five hex strings.
```

**No ARI is computed in CI.** `PoCAEvaluator` is imported by CI only indirectly, via
CHECK 1 → `core/test_bitwise_replay.py`, which does **not** import it either. The
evaluation engine's cross-platform behaviour is therefore unverified by the pipeline that
exists to verify cross-platform behaviour.
