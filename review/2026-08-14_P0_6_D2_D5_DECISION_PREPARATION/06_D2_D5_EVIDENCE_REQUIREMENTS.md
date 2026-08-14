# 06 — D-2 / D-5 Evidence Requirements

**Purpose:** state precisely what is **not** known, what each gap blocks, and what
would close it. Gaps are not filled by assumption anywhere in this package.

Classification legend: see `00_SCOPE_AND_DECISION_CONTEXT.md` §4.

---

## 1. Evidence gaps

| ID | Gap | Blocks | What would close it | Closable by |
|---|---|---|---|---|
| **G-1** | Do real production v1 logs exist? | D-5 strategy selection; the entire question is hypothetical without them | A statement of deployment state from the operator | Human input |
| **G-2** | Are any v1 logs externally relied upon (customers, auditors, regulators, counterparties)? | D-5; determines whether "historical verifiability" is a product requirement or an internal convenience | Operator / commercial statement | Human input |
| **G-3** | Do any logs carry legal or compliance retention obligations, and for how long? | D-5; a retention obligation may make D-5-B/D inadmissible and D-5-C legally sensitive | Legal / compliance statement | Human input |
| **G-4** | Have RFC 3161 tokens been obtained **in production** (as distinct from the two in-repo fixtures)? | D-5-C admissibility; `04_...` §E | Operator statement on TSA usage | Human input |
| **G-5** | Are there external integrators consuming `/v1/audit` whose contract would break if the response shape changes? | D-2 scope, D-7 | Integrator inventory | Human input |
| **G-6** | Is there an intended integrity domain recorded anywhere outside the code? | D-2 — determines whether D-2 *defines* the domain or *recovers* it | Search of governance sources outside the Guard repo, or a statement that none exists | Human input / archival search |
| **G-7** | Does a digest-domain change count as a "protocol version" bump per `src/crypto.rs:25`? | D-2 (D2-Q14), D-7; affects whether the genesis constant moves | Authority interpretation of ADR-0001 and the genesis constraint | Human decision |
| **G-8** | Which continuity properties (historical / chain / Merkle / segment / TSA) are **requirements** rather than preferences? | D-5; `04_...` §E maps effects but cannot rank obligations | Authority statement | Human decision |
| **G-9** | Full migration cost of any D-5 strategy | D-5 | Resolution of D-2 (shape) and D-3 (reduction), then estimation | Later decisions |
| **G-10** | Whether violations tampering should surface as the existing exit code `2` or a distinct class | D-6 (recorded here because it shapes D-5-E's verifier contract) | D-6 | Later decision |

---

## 2. Gaps that are *not* gaps

Recorded so they are not re-litigated. Each was checked against source.

| Question | Answer | Cite | Tag |
|---|---|---|---|
| Is the persisted record sufficient to re-derive a widened digest? | Yes — the full entry including `violations` is on disk | `src/log_writer.rs:96`; `src/models.rs:90` | CONFIRMED |
| Do audit-log (`.jsonl`) fixtures exist in-repo? | No — none anywhere in the repository | `find -name "*.jsonl"` → empty | CONFIRMED |
| Do segment-manifest fixtures exist? | Yes — two, with concrete roots and hashes | `tests/fixtures/tsa/segment-00{1,2}.manifest.json` | CONFIRMED |
| Do real RFC 3161 tokens exist in-repo? | Yes — two FreeTSA tokens with anchors, verified in tests | `tests/fixtures/tsa/segment-00{1,2}.tsr`; `tests/tst_verify.rs:3–9`, `:20–48` | CONFIRMED |
| Is there an in-band discriminator today? | A `schema` string exists but is unread and unprotected | `src/api/audit.rs:132`; `src/log_writer.rs:151–170`; `src/chain.rs:25–49` | CONFIRMED |
| Is there a schema-rejection precedent in the codebase? | Yes, on the segment path only | `src/segment.rs:341–342`; `src/sealer.rs:100` | CONFIRMED |
| Does an accepted ADR govern the chain? | Yes — ADR-0001, "Accepted in v1.3, still current", but it does not enumerate the protected fields | `docs/adrs/0001-hash-chain.md` | CONFIRMED |

---

## 3. Effect of the gaps on decision readiness

| Decision | Gaps affecting it | Effect on readiness |
|---|---|---|
| **D-2** | G-6, G-7 | **Does not block.** G-6 changes the *character* of D-2 (defining vs recovering a domain) but not the Authority's ability to decide it; G-7 is itself a question D-2 can answer (D2-Q14). The field-level evidence is complete: all fourteen fields are enumerated with type, source, current protection status and citations |
| **D-5** | G-1, G-2, G-3, G-4, G-8 | **Blocks a responsible selection.** The strategy *space* is fully mapped and each class's consequences are evidence-derived, but choosing among them turns on facts about deployment, reliance and retention that the repository cannot supply. Selecting a strategy without G-1–G-3 would be choosing by assumption |

**Consequence.** D-2 and D-5 are at different readiness levels. This is stated as
a finding, not as advice on sequencing — see `07_D2_D5_DECISION_BRIEF.md` §4.

---

## 4. Evidence not gathered, deliberately

Per task scope, the following were **not** performed and are not gaps in this
package's sense: a full Guard repository re-audit; re-execution of the D-1
mutation harness; RD-1; the ARI governance track; any inspection of deployed
systems, live logs, or non-repository artifacts.
