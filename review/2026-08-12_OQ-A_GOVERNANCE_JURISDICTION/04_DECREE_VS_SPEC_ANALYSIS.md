# 04 — DECREE VS SPEC ANALYSIS (OQ-A-003)

**Question:** *Does `CONSTITUTIONAL_DECREE.md` have formal precedence over SPEC?*
**Required result:** CONFIRMED / UNRESOLVED (or PARTIALLY ESTABLISHED / NORMATIVE CONFLICT)
**Normative effect:** NONE

> **This document does not decide whether the Decree outranks SPEC.** It executes the seven-step
> analysis required by the method and reports what the evidence supports.

---

## 1. Terms of the question

"SPEC" is read in two senses, because the corpus uses both and they behave differently:

| Reading | Referent | Why it matters |
|---|---|---|
| **SPEC(a)** | The specification **corpus** — AURA-CON-001, APS-001…APS-950, invariants | This is what `AGENTS.md` tier 2 calls "Aura Protocol Specification" |
| **SPEC(b)** | The **SPEC document class**, concretely `SPEC-002_CONSTITUTION_ARTIFACT_CONTRACT.md` | This is the artifact the ARI decisions actually touch |

Both are analysed. They give different results.

---

## 2. Step 1 — What the Decree claims

> **SOURCE** `aura-poc-a-core-v3.3/CONSTITUTIONAL_DECREE.md` · **VERSION** 1.0

| Claim | Text | Line |
|---|---|---|
| Status | "**STATUS:** MANDATORY / NON-OVERRIDABLE" | `:4` |
| Scope | "**SCOPE:** ALL AI ASSISTANCE" | `:5` |
| Authority basis | "**AUTHORITY:** Custodian of the Protocol" | `:6` |
| Duration | "**EFFECTIVE:** Immediate and Perpetual" | `:7` |
| Subject | "This **repository** is a FROZEN REGULATORY MEASUREMENT INSTRUMENT" | `:13` |
| Binding force | "The AI Copilot MUST treat the following as **absolute law**." | `:19` |
| Conflict clause | "If a **user request** conflicts with constitutional principles: **The Constitution prevails.** You MUST refuse the request and cite this decree." | `:253-259` |
| Closing | "This decree is **MANDATORY**, **BINDING**, and **PERMANENT**." | `:529` |

**Findings on the claim itself:**

1. The Decree's declared **scope is "ALL AI ASSISTANCE"** and its declared **subject is this
   repository**. It nowhere claims scope over the specification corpus, over other
   implementations, or over the protocol as such.
2. Its conflict clause resolves **user request vs Decree**, not **document vs document**. The
   phrase "the Constitution prevails" in that clause denotes the Decree itself, not AURA-CON-001
   — which the Decree never mentions.
3. The Decree contains **no reference** to: `AURA-CON-001`, `AURA_CONSTITUTION`, `APS-000`,
   `APS-001`, `APS-100`, `SPEC-002`, `GOV-001`, `POL-VER-001`, or `aura-specification` (verified
   by full read).
4. Its authority basis is the Custodian — i.e. it is **self-referential with ROLE**: the Decree
   cites the Custodian as its authority, and `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md` cites
   "Constitutional Decree Article V" as *its* authority. Neither is grounded in a source outside
   this pair.

---

## 3. Step 2 — What SPEC claims

### SPEC(a) — the specification corpus

| Claim | Text | Source |
|---|---|---|
| Supremacy of the Constitution | "All documents, implementations, and architectural decisions MUST remain consistent with it." | AURA-CON-001 Preamble |
| Document precedence | "A higher-level document has authority over a lower-level document in all cases of conflict." (hierarchy ends: … → Repository Documentation → Implementation) | AURA-CON-001 Art. V |
| Direction of authority | "**Specification First.** Architecture precedes implementation. Implementation follows specification." | AURA-CON-001 Art. IV P1 |
| Contribution rule | "**Specification is the source of truth. Implementation follows specification.** Never propose changes to specifications to match existing implementations." | `CONTRIBUTING.md:11-13` |
| Terminology | "An implementation does not define the protocol." | APS-000 TERM-002 |
| Scope of GOV-001 | "how the **`aura-specification` repository** is governed" | `GOVERNANCE.md:11` |

**Finding:** the specification corpus claims general supremacy over implementations and over
"architectural decisions", but **its governance document explicitly scopes itself to its own
repository**, and its hierarchy never names the Decree.

### SPEC(b) — SPEC-002 specifically

| Claim | Text | Source |
|---|---|---|
| Normative effect | "**Normative effect: NONE until APPROVED.** No requirement in this document, including any REQ-002-* identifier, constitutes an approved architectural or implementation decision while this document remains in DRAFT status." | `SPEC-002:11-12` |
| Readiness | "**SPEC-002 READINESS STATUS: NOT READY**" | `SPEC-002:543` |
| Non-goals | "This document MUST NOT: Modify `aura-poc-a-core-v3.3` …" | `SPEC-002:85-88` |
| Direction of authority | "Implementation behaviour does not constitute normative evidence unless an approved governance artifact explicitly grants that implementation normative authority." | `SPEC-002:37` |

**Finding:** SPEC-002 **disclaims** normative effect and **disclaims** any power to modify the
implementation repository. A conflict between the Decree and SPEC-002 is therefore, on
SPEC-002's own terms, not a conflict of two binding texts.

---

## 4. Step 3 — Does either explicitly claim precedence over the other?

| Direction | Explicit claim? | Evidence |
|---|---|---|
| Decree → over SPEC(a)/(b) | **No** | The Decree never mentions the specification corpus. Its "prevails" clause is scoped to user requests. |
| SPEC(a) → over Decree | **Not by name.** Generically yes, *if* the Decree is "Repository Documentation" or "Implementation" under AURA-CON-001 Art. V | Art. V lists neither the Decree nor any implementation-repository document by name |
| SPEC(b) → over Decree | **No** — it disclaims normative effect entirely | `SPEC-002:11` |

**Neither document claims precedence over the other by name.**

---

## 5. Step 4 — Does another source establish precedence?

| Source | Statement | Assessment |
|---|---|---|
| `AGENTS.md:36-37` / `CLAUDE.md` | Tier 1 "Aura Constitutional Decree / Constitutional Authority"; tier 2 "Aura Protocol Specification" | **This is the only text in either corpus that orders the two.** It is asserted by a document that the same list places at **tier 6**, and no tier-1…tier-5 source authorizes it to do so. Its own status is undeclared: no document ID, no version, no lifecycle status, not in any registry. |
| `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md` §9.2 | "1. Constitutional Decree (highest) … The Constitutional Decree ALWAYS prevails." | Orders five implementation-corpus documents. **The specification corpus does not appear at any level**, so this establishes nothing about SPEC. |
| `.github/github/copilot-instructions.md:9-10` | "ALL directives below are subordinate to the Constitutional Decree. In case of conflict, the Constitution prevails." | Establishes the Decree's precedence over **Copilot directives**, not over SPEC. |
| AURA-CON-001 Art. V | The 7-level hierarchy | Establishes precedence among the documents it names. The Decree is not among them. Applying it to the Decree requires classifying the Decree as "Repository Documentation" — a classification **no source makes**. |
| AURA-CON-001 Art. XII / GOV-001 §10 | Interpretation priority: mission → principles → conformance → determinism → auditability | Ranks **values**, not documents. Cannot adjudicate which document wins. |

**Finding:** exactly one text orders them (`AGENTS.md`/`CLAUDE.md` tier 1 vs tier 2), and that
text's authority to do so is not established by any source above it. Everything else either
omits one side or ranks something other than documents.

> **Explicitly not concluded:** that the `AGENTS.md` ordering is wrong, or that it is right. Its
> authority basis is simply not established, which is a different finding from either.

---

## 6. Step 5 — Does the precedence, if any, apply to ARI?

| Test | Result |
|---|---|
| Does the Decree state ARI semantics? | It states **constants and prohibitions** — scaling factor, sentinel threshold, no-float, layer separation (Art. I) — and no ARI formula, division rule, rounding rule, bound, or dimension. Per RD-1 (CLOSED), no normative ARI definition exists anywhere. |
| Does SPEC-002 state ARI semantics? | No. Its subject is the Constitution Artifact / Vector contract. Whether ARI operands fall inside AD-CA-007's "numeric representation of **vector values**" is itself unresolved (recorded as U-2 in `review/2026-08-12_RD1_ARI_DECISION_READINESS/05_DEPENDENCY_GRAPH.md`). |
| Does either claim ARI jurisdiction? | **Neither.** |

**Finding: JURISDICTION UNRESOLVED for ARI.** Even if precedence between the two were settled,
neither document currently regulates ARI semantics, so the precedence would not by itself
determine who decides them.

---

## 7. Step 6 — Does a conflict-resolution mechanism exist?

| Mechanism | Covers Decree vs SPEC? |
|---|---|
| AURA-CON-001 Art. V | Only for documents it names — **no** |
| AURA-CON-001 Art. XII / GOV-001 §10 | Ranks values — **no** |
| ROLE §9.2 | Implementation corpus only — **no** |
| Decree Art. V ("When Authority Conflicts Arise") | User request vs Decree — **no** |
| `AGENTS.md:49-53` escalation rule ("do not silently reconcile … request human/Protocol Custodian resolution") | **Partially.** It routes the conflict to a human rather than resolving it, and names the resolver as "human/Protocol Custodian" — which, for a cross-corpus conflict, presupposes the unanswered question of whether the Custodian has jurisdiction over the specification corpus |
| GOV-001 §5.2 / Art. XI amendment procedures | Change procedures within the specification corpus — **no** |

**Finding:** no mechanism adjudicates this conflict. One mechanism escalates it, to an actor
whose jurisdiction over the other corpus is not established.

---

## 8. Step 7 — Is that mechanism operational?

The escalation route (`AGENTS.md`) is operational in the weak sense that an agent can stop and
report — this package is an instance of doing so. It is **not** operational as a resolution
mechanism, because:

1. the resolver is named ambiguously ("human/Protocol Custodian");
2. whether the Protocol Custodian has jurisdiction over `aura-specification` is unestablished
   (`03_AUTHORITY_AND_APPROVAL_MATRIX.md` §4);
3. whether the Chief Architect and the Protocol Custodian are the same actor is unestablished;
4. the specification corpus's own resolution path (RFC → ARB → Chief Architect) requires an ARB
   with no established existence and has never been exercised (`rfcs/README.md:16` — "*No RFCs
   submitted yet.*").

---

## 9. OQ-A-003 — finding

### For SPEC(a) — the specification corpus

# NORMATIVE CONFLICT

Two documents order the same pair incompatibly:

- `AGENTS.md`/`CLAUDE.md` place the Decree **above** the Protocol Specification;
- AURA-CON-001 Art. V places the Constitution and APS-001/APS-100 above "Repository
  Documentation" and "Implementation", which is where an implementation-repository decree would
  fall if it were classified at all — and it is not.

Neither corpus cites the other; no source subordinates one ordering to the other; no mechanism
adjudicates. The one text that does order them is itself of undeclared status and self-placed at
tier 6.

### For SPEC(b) — SPEC-002 specifically

# UNRESOLVED — and not currently a live conflict

SPEC-002 declares "Normative effect: NONE until APPROVED" and disclaims any power to modify the
implementation repository. A document with no normative effect cannot be outranked or outrank.
The question becomes live only if SPEC-002 advances beyond DRAFT — and **who may advance it is
itself an EVIDENCE GAP** (`03_AUTHORITY_AND_APPROVAL_MATRIX.md` §2, SPEC row).

### For the ARI question that motivated this analysis

# JURISDICTION UNRESOLVED

Neither document regulates ARI semantics. Settling precedence between them would not, on its own,
establish who may decide `ARI-D-001 … ARI-D-027`.

---

*This document has no normative effect. It records claims, scopes and conflicts. It does not
decide whether the Decree outranks SPEC, and it selects no document, actor, or mechanism.*
