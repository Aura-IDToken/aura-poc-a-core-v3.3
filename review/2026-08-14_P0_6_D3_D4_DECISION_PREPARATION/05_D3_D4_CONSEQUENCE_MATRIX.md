# 05 — D-3 × D-4 Consequence Matrix

**Purpose:** show what each combination *entails*, so the Authority can see the
cost of a pairing before choosing either half. **No combination is selected,
ranked or endorsed.**

Legend: `00_…` §5. D-3 classes: `03_…` A–G. D-4 classes: `04_…` A–F.

---

## 1. What each D-4 choice demands of D-3

| D-4 choice | Demand placed on D-3 | Which D-3 questions become load-bearing |
|---|---|---|
| **A** ordered list | Emit elements in stored order. No sort, no collation. | D3-Q-013 (nesting) only |
| **B** unordered set | Digest must be order-invariant **and** duplicate-collapsing. Requires canonical order or commutative accumulation, plus an element-equality rule. | D3-Q-012, D3-Q-014, D3-Q-015, D3-Q-021 |
| **C** multiset | Order-invariant, multiplicity-preserving. Requires canonical order or a commutative construction that counts. | D3-Q-012, D3-Q-014, D3-Q-021 |
| **D** canonically sorted | A **total** sort key and a specified collation. | D3-Q-001, D3-Q-012, D3-Q-015, D3-Q-016 |
| **E** ordered, declared non-semantic | Same as A technically. | D3-Q-013 only |
| **F** composite identity | An element-equality rule that D-3's normalization must implement consistently. | D3-Q-015, D3-Q-016, D3-Q-002 |

## 2. What each D-3 choice demands of D-4

| D-3 choice | Demand placed on D-4 | Note |
|---|---|---|
| **A** delimiter | An element separator distinct from the field separator, and an escaping rule that survives both levels. | Under D-4 B/C/D the sort must happen before joining |
| **B** length-prefixed | Element count must be explicit or derivable — which forces D-4 to state whether count is semantic. | Interacts with D4-Q-007 |
| **C** canonical JSON | A profile answer for `[]` vs absent, and for omitted vs null keys. | Directly hits D4-Q-008, D4-Q-009 |
| **D** canonical binary | Element boundaries by width or length; float policy decided. | D4-Q-010 unaffected |
| **E** typed encoding | Element type identity must be stable across versions. | Interacts with D4-Q-005 |
| **F** domain-separated | Nothing additional from D-4. | Orthogonal |
| **G** sub-digest | Whether an empty collection yields a defined sub-digest or no component at all. | Directly hits D4-Q-008 |

## 3. Detection consequences by D-4 class

Applies **after** D-1's mandate is implemented. "Detectable" means the mutation
changes the digest.

| Mutation | D-4 A | D-4 B | D-4 C | D-4 D | D-4 E | D-4 F |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| T-D4-01 modify element | ✅ | ✅ | ✅ | ✅ | ✅ | depends on identity rule |
| T-D4-02 remove distinct element | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| T-D4-03 add distinct element | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| T-D4-04 reorder | ✅ | ❌ equivalence | ❌ equivalence | ❌ equivalence | ✅ (declared non-semantic) | inherits base |
| T-D4-05 duplicate insertion | ✅ | ❌ **undetectable** | ✅ | inherits B or C | ✅ | inherits base |
| T-D4-06 duplicate removal | ✅ | ❌ **undetectable** | ✅ | inherits B or C | ✅ | inherits base |
| T-D4-07 empty → non-empty | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| T-D4-10/11 semantic equivalence | byte-equality unless D-3 normalizes | same | same | same | same | **governed here** |

**CONFIRMED.** The two ❌ **undetectable** cells under D-4 B are the only places
in this matrix where a candidate reduces detection below what D-1 made possible.
Stated as a property of set semantics, not as an argument against it.

## 4. Migration consequences (input to D-5, not a D-5 decision)

| Combination property | Consequence for historical re-derivation |
|---|---|
| Any D-3 that treats absent ≠ `None` for `validator` | Historical entries **cannot** be faithfully re-derived — the distinction was never stored (`src/models.rs:40`) — CONFIRMED. Forecloses faithful migration for those records |
| Any D-4 requiring an element-equality rule finer than the stored data | Same foreclosure |
| D-3 G with the sub-digest inside the outer preimage | Historical digests change; the D-2/D-5 package `02_…` §5 consequence set applies |
| D-4 B or C over historical records containing duplicates | Historical duplicates change meaning under the new semantics; a rule for them is required |
| D-3 C (canonical JSON) reading from stored JSON | Re-derivation depends on the stored line parsing losslessly, which it does not for omitted keys |

**These are inputs to D-5. D-5 is BLOCKED and is not decided here.**

## 5. Cross-language consequences

| Combination | Reproduction difficulty for an independent implementation |
|---|---|
| D-3 A + D-4 A | Text join over stored order; escaping is the sole reproduction hazard |
| D-3 B/D + D-4 A | Number and width rules must be stated; no collation needed |
| D-3 any + D-4 B/C/D | Adds collation and element-equality to the reproduction surface |
| D-3 C + any | Depends on a named canonical-JSON profile; "canonical JSON" alone is not a single function |
| Any combination including `confidence` as text | Float rendering must be specified independently of any library (D3-Q-006) |
| Any combination excluding `confidence` | Removes the float surface entirely; leaves `confidence` outside detection |

**EVIDENCE GAP.** Whether independent reproduction is a requirement for the entry
digest is unestablished (`01_…` D3-Q-026). Until it is, the rows above describe
cost without a criterion to weigh it against.

## 6. Interaction with closed and pending decisions

| Decision | Interaction | Status |
|---|---|---|
| D-1 (CLOSED) | Mandates that violations affect the digest. Every combination above satisfies it **except** where a D-4 B cell is undetectable — those cells concern *duplicates*, not membership, so D-1 is still satisfied | Not reopened |
| D-2 (CLOSED) | Fixed membership and shape. The shape outcome constrains D-3 G (whether a sub-digest enters the outer preimage) | Not reopened; **membership list not supplied to this package** — `00_…` §8 |
| D-7 (OPEN) | D3-Q-023 asks whether a version marker is bound into the digest — a joint constraint | Not resolved |
| D-5 (BLOCKED) | §4 above is its input | Not resolved |
| D-6 (OPEN) | Determines how a detection failure is reported, not whether it occurs | Not resolved |
