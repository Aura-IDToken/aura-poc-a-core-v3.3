# RD-1-PDF — 03 IMPACT ON RD-1

The RD-1 package (`review/2026-08-12_RD1_ARI_NORMATIVE_AUDIT/`) is **not modified**. This
document records the effect of the new evidence on it.

---

## 1. The open item, now closed

| RD-1 statement | Status after this audit |
|---|---|
| `06_DECISION_BRIEF.md` §6.1 — "PDF snapshots — UNKNOWN … no extractable text layer … not treated as evidence" | **CLOSED.** All three extracted successfully by two independent engines. Result: **zero** standalone `ARI` tokens. |
| `01_ARI_DEFINITION_EVIDENCE.md` E-4 — "Classification: UNKNOWN — not text-extractable" | **SUPERSEDED.** The files are text-extractable; the limitation was the session's tooling. |

## 2. Direction of the change: RD-1 is strengthened, not weakened

RD-1 reached `NO NORMATIVE DEFINITION FOUND` **while treating three documents as unknown**. Had
those documents contained an ARI definition, the verdict would have been wrong. They do not.
The verdict was reached on incomplete evidence and is now confirmed on complete evidence for
these three artifacts.

The strengthening is specific and material:

| RD-1 claim | Was | Now |
|---|---|---|
| `APS-400_CONFORMANCE_TEST_MATRIX.md`: 0 ARI | markdown only; PDF unknown | **markdown 0 + PDF 0** — both forms silent |
| `APS-500_REFERENCE_FIXTURES.md`: 0 ARI | markdown only; PDF unknown | **markdown 0 + PDF 0** — both forms silent |
| `APS-900_COMPLIANCE_MAPPING.md`: 0 ARI | markdown only; PDF unknown | **markdown 0 + PDF 0** — both forms silent |

The markdown and PDF forms **agree**. There is no discrepancy between the two representations
of these three documents, so no question arises about which representation governs.

## 3. Effect on the RD-1 gap matrix

`04_GAP_MATRIX.md` §2 recorded:

| Artifact required to close RD-1 | RD-1 | After this audit |
|---|---|---|
| ARI conformance test (APS-400 / CONF-xxx) | NO (markdown), PDF unknown | **NO — confirmed in both forms** |
| ARI reference fixtures (APS-500) | NO (markdown), PDF unknown | **NO — confirmed; fixture schema exists with zero instances** |

**No gap-matrix cell changes state.** Two cells move from *partially evidenced* to *fully
evidenced*, in the same direction.

## 4. A new corroborating finding

Not available to RD-1, because it required reading the PDFs:

**APS-400's determinism test does not constrain the ARI value.** CONF-001 — *"Sprawdzenie, że
identyczne dane wejściowe dają identyczny wynik. PASS: Wyniki są identyczne."* — requires only
that identical inputs produce identical outputs.

An independent implementation using **truncation toward zero** rather than floor division — the
divergence recorded as **C-3** in RD-1, producing `30000/100000` instead of `29999/100001` —
would **pass CONF-001**, because it would be internally deterministic.

This sharpens RD-1's conclusion. The conformance layer cannot detect the very divergence the
corpus already records as a P0 finding, because it tests reproducibility rather than
correctness. It does not merely lack an ARI test; the tests it does define are structurally
incapable of pinning an ARI value.

Recorded as evidence. **No remedy is proposed** — that is an architectural decision.

## 5. Effect on the RD-1 provenance chain

Edge `[7] CHARACTERIZATION TEST → INDEPENDENT IMPLEMENTATION` was marked **BROKEN** on the basis
that no fixtures and no conformance runner exist. The PDFs corroborate this from the
specification side: APS-500 defines the fixture container and supplies no instance; APS-400
defines the test matrix and includes no ARI test.

**The edge remains BROKEN.** The chain is unchanged: 1 of 7 edges sound.

## 6. Effect on the RD-1 conflicts

| Conflict | Effect |
|---|---|
| C-1 circularity (spec delegates to uncertified RI-PY) | **unchanged** — no PDF references RI-PY |
| C-2 bounds stated vs implemented | **unchanged** — no PDF states a bound |
| C-3 ADR-005 division claim | **indirectly reinforced** — §4 above shows CONF-001 could not detect the divergence |
| C-4 authority level of impl-repo documentation | **unchanged** |
| C-5 glossaries disagree on the acronym | **unchanged** |
| C-6 characterization-drifting-into-expectation | **unchanged** |

No conflict is resolved. No new conflict is introduced.

## 7. Corrections carried into the record

Two, both about characterisation rather than conclusion, detailed in `00_SCOPE.md` §5:

1. RD-1's "no extractable text layer" was inaccurate — the files are extractable; the session
   lacked tooling.
2. RD-1's "one raw `ARI` byte-match inside FlateDecode streams" was noise from matching
   compressed bytes, and should not have been reported as a partial signal. The decompressed
   text contains zero `ARI` tokens.

Neither correction alters the RD-1 verdict. Both are recorded so the evidence trail is accurate.
