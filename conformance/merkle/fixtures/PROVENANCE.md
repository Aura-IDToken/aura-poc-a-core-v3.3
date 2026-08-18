# DQ-002 fixture provenance

These files are verbatim copies of the DQ-002 fixtures held in
`Aura-IDToken/aura-specification`. They are vendored so that the RI-PY
conformance suite is executable in this repository's CI without a
cross-repository checkout. **This repository is not their authority.**

| Item | Value |
| --- | --- |
| Source repository | Aura-IDToken/aura-specification |
| Source branch | claude/aura-cross-language-002-6t2kdo |
| Source path | `ck003/dq-002-hash-domain/fixtures/` |
| Copied | 2026-08-18 |

| File | SHA-256 |
| --- | --- |
| `FIX-CK003-DQ002-RFC6962-2LEAF.json` | `bf21d2b8f3c947ebaf23bc7662f1ac8e590ef6c3a77850e27c84422967ce9aae` |
| `FIX-CK003-DQ002-RFC6962-EDGE-MATRIX.json` | `dfa5320cb06ba1a3eb88ad60424869e9722384b29f310ee9978390811f9f3eb8` |

If a fixture changes upstream, these copies and the recorded digests MUST be
refreshed in the same change. A divergence between the two is a conformance
defect, not a merge inconvenience.

`FIX-CK003-DQ002-RFC6962-2LEAF.json` carries status `PROPOSED`;
`ADR-CK003-DQ002-HASH-DOMAIN` is `PROPOSED — awaiting Chief Architect
approval`. Passing this suite is conformance evidence against a proposed
contract; it does not by itself make the contract normative and does not
close DQ-002.
