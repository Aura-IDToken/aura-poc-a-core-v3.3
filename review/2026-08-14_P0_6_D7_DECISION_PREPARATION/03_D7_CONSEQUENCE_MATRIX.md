# 03 — D-7 Consequence Matrix

Cross-candidate consequences. **No column is a score and no row is a ranking.**
Cells are evidence-derived where cited, and marked **[INFERENCE]** where reasoned.

Candidates: `02_…` A–G. Baseline facts F1–F13: `01_…`.

---

## 1. Core properties

| Property | A outside digest | B inside digest | C external selection | D self-describing | E dual/parallel | F verifier families | G structural / genesis |
|---|---|---|---|---|---|---|---|
| Discriminator is in the record | Yes | Yes | No | Implicit | No | No | Implicit |
| Discriminator is cryptographically bound | **No** (F3) | Yes | n/a | Yes | n/a | n/a | Partly — genesis is bound transitively (F7) |
| Legacy self-identifies | Yes (F2) | **No** (F1) | No | By absence of tag | By verifying | No | By structure |
| Record format changes | Optional | **Yes** | No | Depends on D-3 | No | No | Follows D-3/D-4 |
| Requires trial verification | No | Likely (D7-Q-006) | No | Likely | **Yes, by definition** | No | No |
| Requires an operational boundary | No | Yes | **Yes** | No | No | **Yes** | Only the `seq` variant |
| Precedent exists in-repo | Field exists, unused (F2/F4) | None | **Yes** (F11) | Merkle layer only (F9) | None | None | F5, F7, F8 |

## 2. Failure-mode behaviour

Behaviour on each anomalous input. "Undefined" means the candidate does not fix
it and it must be specified (D7-Q-011 … D7-Q-015).

| Input | A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|---|
| Marker absent | Undefined — must specify | Legacy has none by construction | n/a | Untagged = generation 1 | n/a | n/a | Parse failure → exit `1`, not `2` (F5, F10) — CONFIRMED |
| Marker unknown | Undefined | Fails recomputation | n/a | Fails closed | No generation verifies | n/a | n/a |
| Marker malformed | Undefined | Parse failure → exit `1` | n/a | Fails closed | n/a | n/a | Parse failure → exit `1` |
| Claims newer than supported | Undefined | Fails | Operator error | Fails closed | No generation verifies | Artifact refuses | n/a |
| Claims older | **Accepted as claimed** | Fails unless the old rule is supported | Operator-determined | Verifier tries the old domain | Accepted if it verifies | Artifact-determined | Determined by structure |

**CONFIRMED — the exit-code asymmetry matters.** Under G (and under B/D for
malformed markers), a version problem surfaces through the **parse** path as exit
`1` ("runtime error / malformed log") rather than the integrity path's exit `2`
(`docs/exit-codes.md`; `src/log_writer.rs:163–166`). Any candidate relying on
structural determination inherits a diagnostic that names the wrong problem.

## 3. Security consequence summary

Full models in `04_…`.

| Exposure | A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|---|
| Discriminator tampering | **Structural** (F3) | Breaks digest | No in-record target | No target | No target | No target | No label to edit |
| Downgrade | **Available by construction** | Bootstrap-limited | Invocation-controlled | Trial-limited | **Inherent to the accept rule** | Artifact-controlled | Depends on EG-1 |
| Forward confusion | Undefined | Fails | Operator error | Fails closed | Fails | Artifact refuses | Structural |
| Verifier disagreement | Two verifiers reading the same field may branch differently if the value set is unspecified [INFERENCE] | Lower — the rule is bound | **Higher** — different invocations legitimately give different results | Lower | **Higher** — "any generation verifies" is a policy each verifier could apply differently | Lower per artifact | Depends on structural rules being specified |
| Legacy ambiguity | Resolved by the field, if trusted | **Unresolved** — legacy carries no marker | Resolved by context | Resolved by domain | Resolved by outcome | Resolved by artifact | Resolved by structure |

## 4. Evidence and continuity impact

| Dimension | A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|---|
| Existing TSA tokens (F12) | Preserved | Preserved if legacy stays verifiable | Preserved | Preserved | Preserved | Preserved | Preserved |
| Merkle continuity | Unaffected | Unaffected | Unaffected | Unaffected | Unaffected | Unaffected | Unaffected |
| Historical data rewritten | No | No | No | No | No | No | No |
| Requires re-sealing | No | No | No | No | No | No | No |

**CONFIRMED — no D-7 candidate by itself requires rewriting history.** Every
candidate above leaves sealed segments and their tokens intact. **The destruction
scenario belongs to D-5** (a re-sealing migration), not to D-7. This is an
important separation: D-7 chooses *how a rule is selected*, not *what happens to
old records* — that is D-5's question. See `08_…` §3.

## 5. D-5 impact

| Candidate | What it leaves open for D-5 | What it forecloses |
|---|---|---|
| A | All D-5 strategies | Nothing |
| B | All, but legacy cannot self-identify, so D-5 must supply the boundary | Nothing structurally |
| C | All; D-5 must define and publish a boundary | Nothing |
| D | All; boundary discoverable per record | Nothing |
| E | All; no boundary required | Nothing — but no boundary is *enforced* either |
| F | All; D-5 must set an operational boundary and a retention period for the legacy artifact | Nothing |
| G | All; the `seq` variant needs a declared boundary | Nothing |

**CONFIRMED.** **No D-7 candidate makes any D-5 strategy impossible.** The
dependency runs the other way: D-5 strategies A and E (from the D-2/D-5 package)
*require* D-7 to supply a selection mechanism, and several D-7 candidates supply
one. See `05_…` §3.

## 6. Implementation surface

| Candidate | Record format | Writer | Library verifier | CLI | Docs contract |
|---|---|---|---|---|---|
| A | Field already exists (F2) | Set a value | Read + branch | — | Possibly a new exit code (F10) |
| B | Changes | Bind marker | Rule selection + bootstrap | — | New exit code likely |
| C | Unchanged | Unchanged | Optional | **Flag/config** — precedented (F11) | Flag documented; F11 shows the pattern incl. a stderr warning |
| D | Depends on D-3 | Emit tag | Trial or hint | — | New exit code likely |
| E | Unchanged | Unchanged | **Multi-rule loop** | Report which generation | Reporting contract change |
| F | Unchanged | Unchanged | Two artifacts | Two tools | `docs/exit-codes.md` spans binaries (F10) |
| G | Follows D-3/D-4 | Unchanged | Structural branch | — | Parse-vs-integrity diagnostic (see §2) |

## 7. What the matrix cannot yet decide

**EVIDENCE GAP (EG-1).** Three cells above — B's feasibility, D's tag mechanics,
and E's central accept-rule safety — depend on the **accepted D-3 values**, which
were not supplied to this package. The most consequential is E's, because it
determines whether a new-generation record can satisfy the legacy rule
(D7-Q-018).

**EVIDENCE GAP (G-1/G-2/G-3).** Whether C and F are operationally viable depends
on facts about production logs, external consumers and retention that lie outside
the repository (`06_…`).
