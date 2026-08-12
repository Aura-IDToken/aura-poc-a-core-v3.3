# 08 — TWO-KEY DECISION PROTOCOL

**Package:** RD-1-ARI-DECISION-READINESS · **Normative effect:** NONE

---

## 1. The gate, stated explicitly

### CLAUDE MAY:

- discover decision points;
- classify existing evidence;
- identify candidate semantics;
- identify consequences;
- identify dependencies;
- identify evidence requirements;
- identify contradictions;
- prepare decision questions.

### CLAUDE MAY NOT:

- choose the answer;
- declare an ARI semantic authoritative;
- convert a candidate into a requirement;
- create normative fixtures;
- modify implementation to match a candidate;
- amend the specification;
- create an approving ADR.

**This package was produced entirely within the first list.** Its compliance with the second list
is recorded in `00_SCOPE_AND_GOVERNING_CONTEXT.md` §4 and re-verified in `10_DECISION_BRIEF.md`
§6.

---

## 2. The two keys

| Key | Holder | Role in this protocol |
|---|---|---|
| **KEY 1** | **Human Architectural Authority** | Decides. Holds jurisdiction over ARI semantics and over the governance questions the semantics depend on. |
| **KEY 2** | **ChatGPT architectural review** | Reviews. Independently examines the decision package and any proposed resolution for architectural soundness, completeness and internal consistency. |

**Only after both keys accept a decision may Claude formalize it.**

"Formalize" means: write the accepted decision into a specification, an ADR, a fixture, a
conformance test, or an implementation. Until both keys have accepted, none of those artifacts may
be created for that decision.

---

## 3. Process

```
  (1) DECISION PREPARATION            ← this package (COMPLETE for RD-1-ARI)
          Claude discovers, classifies, maps. Chooses nothing.
                 ↓
  (2) HUMAN REVIEW                    ← KEY 1
          Human Architectural Authority reviews the decision space,
          rejects/extends/corrects it, and decides — or defers.
                 ↓
  (3) CHATGPT ARCHITECTURAL REVIEW    ← KEY 2
          Independent architectural review of the same material and of
          any resolution KEY 1 proposes.
                 ↓
  (4) EXPLICIT MUTUAL ACCEPTANCE
          Both keys record acceptance of the same, identified decision text.
          Silence is not acceptance. Partial acceptance is not acceptance.
                 ↓
  (5) FORMALIZATION                   ← Claude may act here, and only here
          The accepted decision is written into the artifact its own terms
          designate: specification section, ADR, fixture, conformance test.
                 ↓
  (6) IMPLEMENTATION
          Subject to whatever governance gate applies to changing the
          instrument — an unresolved question recorded elsewhere and
          NOT reopened by this package.
```

### Stage entry/exit conditions

| Stage | Entry condition | Exit condition |
|---|---|---|
| (1) Preparation | A decision domain exists without an authoritative answer | A decision package exists: register, matrix, candidates, consequences, dependencies, evidence requirements, open questions |
| (2) Human review | Stage (1) delivered | KEY 1 records, per decision identifier: ACCEPT / REJECT / DEFER / AMEND, with reasons |
| (3) ChatGPT review | Stage (2) recorded | KEY 2 records, per decision identifier: ACCEPT / REJECT / DEFER / AMEND, with reasons |
| (4) Mutual acceptance | Both keys have recorded a position on the same decision text | Both positions are ACCEPT on identical text, recorded with the text's identifier and version |
| (5) Formalization | Stage (4) complete for that decision | The accepted decision exists in a governance artifact citing both acceptances |
| (6) Implementation | Stage (5) complete **and** the applicable governance gate is satisfied | Out of scope for this package |

---

## 4. Rules binding stages (2)–(5)

1. **Per-decision granularity.** Acceptance is recorded per `ARI-D-nnn` identifier. Accepting the
   package as a whole accepts *the map*, not any answer within it.
2. **Identical text.** Both keys must accept the same text at the same version. If KEY 1 amends
   after KEY 2's acceptance, KEY 2's acceptance lapses for that decision.
3. **Dependency order.** A decision whose prerequisites (`05_DEPENDENCY_GRAPH.md` §3) are
   undecided may still be *reviewed*, but its acceptance must record that its prerequisites are
   open — otherwise the acceptance is conditional in fact and unconditional on paper.
4. **Unresolved dependencies must be resolved before the decisions they gate.** The six
   uncertainties in `05_DEPENDENCY_GRAPH.md` §4 (U-1 … U-6) are themselves decision items for
   KEY 1.
5. **No implicit acceptance.** Absence of objection, silence, elapsed time, CI success, or
   merge of this package do not constitute acceptance by either key.
6. **No delegation to Claude.** Claude may draft text at either key's instruction, but drafting
   is not deciding; the drafted text still requires both acceptances.
7. **Candidate promotion requires an act.** No candidate in `03_NON_NORMATIVE_CANDIDATES.md`
   becomes a requirement by being reviewed, discussed, or found convenient. It becomes a
   requirement only through stages (4) and (5).
8. **Rejection is recorded, not discarded.** A rejected alternative stays in the record with its
   rejection reason, so that a later reader can see the decision space as it was.
9. **Scope of a decision.** Each acceptance must state whether it binds the protocol
   (cross-language, cross-implementation) or only the instrument. The two authority ladders
   recorded in `00_SCOPE_AND_GOVERNING_CONTEXT.md` §7 make this distinction load-bearing.
10. **Evidence before acceptance.** A decision accepted without the evidence set in
    `06_EVIDENCE_REQUIREMENTS.md` §4 should record which evidence was waived, so the gap is
    visible rather than absorbed.

---

## 5. What each key is being asked to do with this package

### KEY 1 — Human Architectural Authority

Asked to determine, in this order:

1. Whether the decision space is **complete** — are there ARI decisions this package failed to
   discover?
2. Whether the decision space is **correctly separated** — are any two decisions here really one,
   or any one really two?
3. Whether the **classifications are right** — in particular the DISPUTED AUTHORITY — SCOPE
   UNRESOLVED marking of `CONSTITUTIONAL_DECREE.md` Article I §8 (`09_OPEN_QUESTIONS.md` OQ-A,
   OQ-B).
4. Which decisions are **in jurisdiction** and which require the Protocol Custodian, the Chief
   Architect, or another authority named by the corpus.
5. Which decisions to **take now**, which to **defer**, and in what order — noting the dependency
   graph but not being bound by this package's reading of it.

### KEY 2 — ChatGPT architectural review

Asked to review, independently:

1. Whether any candidate in `03_NON_NORMATIVE_CANDIDATES.md` has been **mislabelled** — in
   particular, whether anything treated as non-normative is in fact normative, or the reverse.
2. Whether the **consequence statements** in `04_CONSEQUENCE_MATRIX.md` are accurate and
   genuinely unranked.
3. Whether the **dependency edges** in `05_DEPENDENCY_GRAPH.md` §3 are justified by the evidence
   cited, and whether the four departures (Δ1–Δ4) and six uncertainties (U-1…U-6) are right.
4. Whether the **evidence requirements** in `06_EVIDENCE_REQUIREMENTS.md` are sufficient to make
   a decision defensible, or over/under-specified.
5. Whether this package has **anywhere selected a semantic** while claiming not to — the
   adversarial check on hard boundaries 4–15 and 21–23.

---

## 6. Disagreement handling

| Situation | Handling |
|---|---|
| KEY 1 accepts, KEY 2 rejects | No formalization. The rejection reason is recorded against the decision identifier and returns to stage (2). |
| KEY 2 accepts, KEY 1 rejects | No formalization. KEY 1's jurisdiction is not overridden by KEY 2's acceptance. |
| Both defer | The decision stays open; dependent decisions remain blocked per `05_DEPENDENCY_GRAPH.md`. |
| Keys accept different variants | Not mutual acceptance. One text must be produced and re-accepted by both. |
| A decision is found to conflict with a higher authority tier | Per `aura-poc-a-core-v3.3/CLAUDE.md` and `docs/conformance/README.md`: do not silently reconcile; stop; report the conflict; request human/Protocol Custodian resolution. |

---

## 7. Standing prohibitions during stages (1)–(4)

Until both keys have accepted a given decision, and for that decision:

- no fixture carrying its value may be created;
- no test asserting its value may be added;
- no implementation may be changed to match it;
- no specification text may be amended to state it;
- no ADR approving it may be written;
- no documentation may describe it as settled.

These restate hard boundaries 4–15 and 19–23 and `NB-021_FROZEN_SEMANTICS_AUDIT.md` §8 CASE E,
which records the prohibition on encoding an unresolved normative value as a test expectation as
the corpus's single unanimous finding.

---

*This document has no normative effect. It describes a review process. It selects no ARI
semantics, creates no ADR, amends no specification, and modifies no code.*
