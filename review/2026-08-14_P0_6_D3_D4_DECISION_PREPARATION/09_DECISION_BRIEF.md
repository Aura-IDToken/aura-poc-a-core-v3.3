# 09 — D-3 + D-4 Decision Brief

**For:** Human Architectural Authority and Independent Reviewer
**Evidence commit:** `aura-guard-v1.3` @ `443f72e58483c3ea6112ea517647cc0dbf459960`
**Accepted inputs:** D-1 = YES (CLOSED), D-2 = YES (CLOSED)

**Human decision required.** This brief selects nothing, ranks nothing and
recommends nothing.

---

## 1. D-3 — Canonical Representation

**Question.** How is integrity-domain data reduced to bytes so that two
independent implementations produce an identical digest for an identical
`AuditEntry`?

**What is established.** All 26 required elements are enumerated with observed
behaviour and citations (`01_…`). The current representation — `"|"`-joined UTF-8
text, unescaped, decimal integers, RFC 3339 timestamp text, no version marker, no
domain separation — is recorded as **IMPLEMENTATION-DERIVED / NON-NORMATIVE**
throughout and is not treated as a baseline.

**Three findings shape the decision:**

1. **The current preimage is not injective.** `context` is arbitrary caller text
   joined unescaped with `"|"` (`src/chain.rs:41`), and the separator's own
   comment asserts a non-overlap property that does not hold for that field
   (`src/chain.rs:18–19`) — CONFIRMED.
2. **The float question cannot be avoided.** `confidence: f32`
   (`src/models.rs:38`) is the only float in the record and has never been
   hashed. Every candidate must answer it; none makes it disappear.
3. **`None` versus absent is already erased on disk.** `skip_serializing_if`
   removes `validator` entirely when `None` (`src/models.rs:40`). Any
   representation that distinguishes them cannot re-derive historical records.

**Candidates.** A delimiter-based · B length-prefixed · C canonical JSON ·
D canonical binary · E typed field encoding · F domain-separated · G sub-digest
composition (`03_…`). F and G are modifiers that compose with A–E, so a decision
is likely a tuple rather than a single letter.

**Register status.** 23 OPEN · 1 NORMATIVE CONFLICT (NC-1, `score` range) ·
2 EVIDENCE GAP (D3-Q-018 `NaN`/`inf`, D3-Q-026 cross-language requirement).

---

## 2. D-4 — Collection Semantics

**Question.** What is `violations` as a collection?

**What is established.** All 15 required aspects are enumerated (`02_…`). The
current `Vec<Violation>` is ordered and duplicate-permitting, order follows YAML
authoring, and at most one violation arises per rule — all recorded as
**IMPLEMENTATION-DERIVED**, none assumed normative.

**Three findings shape the decision:**

1. **Order is already semantically ambiguous.** The type is ordered
   (`src/models.rs:90`) but the decision aggregate is order-independent
   (`src/engine.rs:58–65`) — CONFIRMED. Nothing states which is intended.
2. **Element equality is already contested.** `action` is compared
   case-insensitively (`src/engine.rs:44`) but stored verbatim (`:51`) — the
   engine and the record already disagree about what "the same violation" is.
   Recorded as **NORMATIVE CONFLICT** (NC-2).
3. **The candidates differ in only three places.** Modification, distinct-element
   addition and distinct-element removal are detectable under every candidate.
   They diverge only on reorder, duplicate insertion and duplicate removal
   (`05_…` §3) — which is what the D-4 choice is actually about.

**Candidates.** A ordered list · B unordered set · C multiset · D canonically
sorted · E ordered-but-declared-non-semantic · F composite identity (`04_…`).

**Register status.** 12 OPEN · 1 NORMATIVE CONFLICT (NC-2) · 1 EVIDENCE GAP
(D4-Q-006 all-match requirement).

---

## 3. Coupling

**D-3 ↔ D-4 is HARD and BIDIRECTIONAL**, with evidence cited in both directions
(`06_…` E-03). D-4's semantics determine whether the digest must be
order-invariant or duplicate-collapsing; D-3's encoding determines which
semantics are expressible. **They form one closure unit** — closing either alone
silently reduces the other's option space.

Onward edges: D-3 → D-7 (whether a version marker is bound inside the digest);
D-3 → D-5 and D-4 → D-5 (both conditional, and both capable of foreclosing
faithful migration before D-5 is taken); D-3 → D-6 and D-4 → D-6.

---

## 4. Reference Model — future deliverables

**Not built here. Nothing below exists yet, and none of it may be produced as a
normative artifact before D-3 and D-4 close.** Listed so the scope after closure
is visible.

| Element | What it must contain | Depends on |
|---|---|---|
| **Mathematical definition** | The digest as a function: domain, codomain, composition with the existing chain, and the injectivity property if mandated (D3-Q-021) | D-2, D-3 |
| **Canonical representation** | Byte-level encoding rules for every type in the domain: encoding, integers, floats, timestamps, optionals, empties, separators or lengths, escaping, ordering, nesting, domain tag | D-3 (all 26 questions) |
| **Collection semantics** | Element identity, ordering, multiplicity, empty and absent semantics, equivalence class | D-4 (all 15 questions) |
| **Test vectors** | Published input→digest pairs covering every boundary case in `07_…`, sufficient for an independent implementation to self-check | D-3, D-4; scope set by D3-Q-026 |
| **Expected digest** | Known-answer values for a reference `AuditEntry`, including the empty-collection case and at least one duplicate case | D-3, D-4 |
| **Version selection** | How a verifier determines which representation applies to a given record | **D-7**, not D-3/D-4 |

These are six separable artifacts. Producing any of them now would convert a
candidate into a normative rule, which this package is prohibited from doing.

---

## 5. Status summary

```
D-3 STATUS: DECISION-READY  (not decided)
D-4 STATUS: DECISION-READY  (not decided)

Decisions prepared:
    D-3 — canonical representation: 26-element register, 7 candidate classes,
          consequence matrix, dependency edges, evidence gaps
    D-4 — collection semantics: 15-question register, 6 candidate classes,
          12-case security test design, dependency edges, evidence gaps

Decisions selected:
    NONE

Normative semantics selected:
    NONE

Production code changed:
    NO

SPEC-002 changed:
    NO

ADR created:
    NO

Fixtures created:
    NO

Recommendations:
    NONE

Human decision required:
    YES

Independent review required:
    YES
```

**Basis for DECISION-READY.** Both registers are complete against the required
element lists; every candidate class carries definition, source, source status,
advantages, limitations, and cross-language / replay / migration / security /
ambiguity analysis; consequences are matrixed; dependencies are evidenced in both
directions; and the remaining gaps (`08_…`) are statements of intent that only
the Authority can supply, not facts that further investigation would uncover.

**What DECISION-READY does not mean.** It does not mean a decision is due, that
one option is better, or that the gaps are immaterial — EG-2 in particular
(is independent cross-language reproduction required?) changes how the cost side
of every D-3 candidate should be weighed.

---

## 6. Decision Record — to be completed by the Authority

### D-3

| Field | Value |
|---|---|
| Base encoding class (A–E) | |
| Domain separation (F) applied? | |
| Sub-digest composition (G) applied? | |
| Answers to D3-Q-001 … D3-Q-026 | |
| Resolution of NC-1 (`score` range) | |
| Decided by (HAA) | |
| Independent Reviewer | |
| Date | |
| Authority basis | |

### D-4

| Field | Value |
|---|---|
| Collection class (A–F) | |
| Element identity rule | |
| Answers to D4-Q-001 … D4-Q-015 | |
| Resolution of NC-2 (`action` equality) | |
| Decided by (HAA) | |
| Independent Reviewer | |
| Date | |
| Authority basis | |

---

*This package has no normative effect. It records evidence, options and
consequences. It selects nothing and implements nothing. No production code was
modified; no file in `aura-guard-v1.3` was created, modified or deleted; the
source was read from a pristine read-only clone pinned at `443f72e`.*
