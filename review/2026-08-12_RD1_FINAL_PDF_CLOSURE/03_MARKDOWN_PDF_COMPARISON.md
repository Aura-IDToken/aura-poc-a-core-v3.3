# RD-1-FINAL-PDF — 03 MARKDOWN / PDF COMPARISON

The governing question: **does the PDF representation contain ARI-related normative content
absent from the already-audited Markdown representation?**

**Answer: NO — for all six artifacts.**

---

## 1. Pairing and headline comparison

Every PDF in scope has a markdown counterpart in the same repository.

| Artifact | Markdown counterpart | MD exists | MD `ARI` | PDF `ARI` | Delta |
|---|---|---|---|---|---|
| Constitution | `constitution/AURA_CONSTITUTION.md` | ✅ | **0** | **0** | **none** |
| APS-000 | `aps/APS-000_FOUNDATION_AND_TERMINOLOGY.md` | ✅ | **0** | **0** | **none** |
| APS-100 | `aps/APS-100_PROTOCOL_INVARIANTS.md` | ✅ | **0** | **0** | **none** |
| APS-200 | `aps/APS-200_CANONICAL_DATA_MODEL.md` | ✅ | **0** | **0** | **none** |
| APS-300 | `aps/APS-300_EVIDENCE_MODEL.md` | ✅ | **0** | **0** | **none** |
| APS-950 | `aps/APS-950_REFERENCE_IMPLEMENTATION_REQUIREMENTS.md` | ✅ | **0** | **0** | **none** |

## 2. Directed test — terms present in PDF but absent from Markdown

The test that matters is asymmetric: content the PDF has and the markdown lacks.

| Artifact | PDF-only ARI-relevant content |
|---|---|
| Constitution | **none** |
| APS-000 | **none** |
| APS-100 | **none** |
| APS-200 | **none** |
| APS-300 | **none** |
| APS-950 | `RI-PY` pdf=2 md=1 — **explained below, not new content** |

### 2.1 The single delta, resolved

APS-950's PDF yields two `RI-PY` occurrences against the markdown's one. Located by page:

```
occurrence 1: page 9
occurrence 2: page 10
```

Both are the same registry row. The §11 table spans the page 9/10 boundary and its rows are
re-rendered at the top of page 10 — a standard PDF table-continuation artifact.

The markdown carries the same table **once**, and in richer form (it adds `Language` and
`Status` columns the PDF layout drops):

> `| RI-PY | aura-poc-a-core | Python | Deterministic measurement engine (Layer 0) | Active |`

**The markdown is the superset. The PDF adds nothing.**

## 3. Character-count differences

Raw sizes differ, in **both** directions, and none of the differences is ARI-relevant:

| Artifact | MD chars | PDF chars | Direction |
|---|---|---|---|
| Constitution | 5 031 | 4 513 | markdown larger |
| APS-000 | 4 926 | 5 299 | PDF larger (table repeats) |
| APS-100 | 4 792 | 4 537 | markdown larger |
| **APS-200** | **8 356** | **3 200** | **markdown substantially larger** |
| APS-300 | 5 295 | 4 107 | markdown larger |
| APS-950 | 4 016 | 3 886 | markdown larger |

Two systematic causes, both verified:

- **PDF larger** — page-break table repetition (APS-000, and the APS-950 case above). Duplicated
  content, not additional content.
- **Markdown larger** — markdown link syntax, extra table columns, and (notably for APS-200) more
  fully populated tables. In APS-200 the markdown is more than twice the PDF; the PDF layout
  collapses table cells across line breaks and drops columns.

**In no case does the PDF carry substantive content the markdown lacks.** Where the two differ
in substance, the markdown is the more complete representation.

## 4. Article V — present in both

Worth recording explicitly, because it is the finding that corrects RD-1 (`02` §2):

| Location | Article V — Canonical Hierarchy |
|---|---|
| `AURA Constitution_260723_190157.pdf`, page 5 | ✅ present |
| `constitution/AURA_CONSTITUTION.md`, lines 73–88 | ✅ present, with `(APS-001)` / `(APS-100)` annotations the PDF omits |

Article V was **never PDF-only**. It has been in the markdown corpus throughout. RD-1 did not
surface it because RD-1's search enumerated ARI-bearing files and `AURA_CONSTITUTION.md`
contains zero ARI tokens. This is a correction to RD-1's *authority-level* reasoning, not to its
ARI finding.

## 5. A note on `.txt` sidecars

Two pre-extracted text sidecars are tracked in the repository:
`AURA Constitution_260723_190157.txt` and `APS-500 Reference Fixtures_260723_194023.txt`. They
exist for only two of the nine PDFs and were not relied upon; all evidence in this package comes
from fresh dual-engine extraction. Their presence is recorded for completeness.

## 6. Conclusion

For all six artifacts, the markdown and PDF representations **agree on ARI: both contain none**.

No question arises as to which representation governs, because they do not conflict. RD-1's
assessment of these six documents — performed on the markdown alone — is confirmed against the
PDF representation.
