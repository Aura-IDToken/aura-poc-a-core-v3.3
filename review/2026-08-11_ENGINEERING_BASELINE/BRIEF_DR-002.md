# DECISION BRIEF — DR-002

**Dla:** Protocol Custodian / Chief Architect
**Data:** 2026-08-11
**Charakter:** streszczenie istniejących ustaleń. **Brak nowego audytu. Brak nowych decyzji.
Brak zmian w repozytorium normatywnym.**
**Źródła:** `00_SCOPE.md` §2, `04_DETERMINISM_AUDIT.md`, `07_CONFORMANCE_AUDIT.md`,
`08_BLOCKERS.md` §4. Cytaty normatywne pozostają w oryginalnym brzmieniu (EN) — tłumaczenie
byłoby reinterpretacją.

---

## 1. Uwaga wstępna, która wymaga rozstrzygnięcia przed resztą

Identyfikator **`DR-002` nie występuje w żadnym z pięciu zbadanych repozytoriów**
(`aura-poc-a-core-v3.3`, `aura-guard-v1.3`, oba `aura-specification`, oba
`Aura-Conformance-Kit`). Ustalone w `00_SCOPE.md` §2 przez wyczerpujące przeszukanie
`*.md`, `*.py`, `*.txt`, `*.rs`.

Najbliższy śledzony odpowiednik to dwanaście nierozstrzygniętych domen decyzyjnych
`AD-CA-001` … `AD-CA-012` w `SPEC-002 §6`.

**Ten brief nie zakłada, że DR-002 = którakolwiek z nich.** Mapowanie jest samo w sobie
otwartą kwestią governance (zarejestrowana jako **NB-000**).

---

## 2. Czego dotyczy decyzja

Zbiór rozstrzygnięć warunkujących deterministyczne i niezależnie odtwarzalne wytworzenie
Constitution Artifact i Constitution Vector. `SPEC-002 §6` rejestruje je jako **UNRESOLVED**,
z adnotacją:

> "No candidate choice listed in this table constitutes a recommendation, preference,
> default, or implied architectural decision."

Formalny stan dokumentu (`SPEC-002 §11`):

> **SPEC-002 READINESS STATUS: NOT READY**
> "CR-007 remains BLOCKED."

---

## 3. Co jest zablokowane

| Zablokowane | Domena |
|---|---|
| Wygenerowanie Constitution Vector | AD-CA-005, -006, -007 |
| Wytworzenie `constitution.json` | jw. |
| Implementacja CR-007 | wprost BLOCKED (SPEC-002 §11.B) |
| Wybór metody embeddingu | AD-CA-005 |
| Reprezentacja numeryczna (szerokość, skala, endianness, **reguła zaokrąglania**) | AD-CA-007 |
| Format serializacji kanonicznej, ciąg bajtów, domeny hash | AD-CA-008 |
| Wymagane tryby awarii przy danych niepoprawnych | REQ-002-031 |
| Testy konformancji dla SPEC-002 | wszystkie powyższe |
| Siedem warstw `ConformanceLayer` w Conformance Kit | `07_CONFORMANCE_AUDIT.md` §6b |

### Powiązanie z ustaleniami inżynierskimi

Trzy zgłoszone wcześniej problemy determinizmu mają komponent normatywny w tej właśnie
domenie — **nie są to zwykłe błędy do naprawienia**:

- **D-1** (`//` floor vs truncate) — reguła dzielenia dla ujemnych dzielnych **nie jest
  wymieniona nawet jako kandydat** w AD-CA-007. Zarejestrowana jako **NB-016**.
- **D-2** (`round()` half-to-even) — AD-CA-007 wymienia `round-half-to-even` **wyłącznie
  jako kandydata**. Obecne zachowanie implementacji odpowiada temu kandydatowi; **nie jest
  to dowód jego wyboru**.
- **D-7** (trzy kanonikalizacje JSON) — właściwa forma to AD-CA-008.

---

## 4. Co **nie** jest zablokowane

- **Cały `aura-guard-v1.3`.** Zero wystąpień `constitution`, `ari`, `poca` w `src/`,
  `tests/`, `Cargo.toml` (`06_GUARD_AUDIT.md` §9). Nie zależy od DR-002, SPEC-002, żadnego
  AD-CA ani CR-007.
- Dokumentowanie zachowania istniejącego.
- Testy charakteryzujące (rejestrujące stan AS-IS, bez orzekania o poprawności).
- Pustka Conformance Kit **jest zachowaniem poprawnym**, nie defektem — napisanie dziś
  testów SPEC-002 naruszyłoby §6 tego dokumentu.

---

## 5. Kwestie wymagające rozstrzygnięcia — w kolejności zależności

Wszystkie już zarejestrowane w `08_BLOCKERS.md` §4. **Żadna nie jest nowa.**

| ID | Pytanie | Dlaczego pierwsze |
|---|---|---|
| **NB-000** | Do czego odnosi się `DR-002` i jak mapuje się na AD-CA-001…012? | Bez tego każde odwołanie do DR-002 jest niejednoznaczne |
| **NB-001** | Które `aura-specification` jest autorytatywne — `AuraIDToken/` (pełny korpus APS) czy `aura-nomos/` (jednolinijkowy README)? | Warunkuje każdą cytowaną podstawę |
| **NB-002** | Który Conformance Kit jest autorytatywny — aktywny czy zarchiwizowany bliźniak o identycznym źródle? | Warunkuje wszelkie prace konformancyjne |
| NB-003…NB-014 | AD-CA-001 … AD-CA-012 | Rejestr własny SPEC-002 |
| NB-015 | Wymagane tryby awarii (REQ-002-031) | Warunkuje *wymaganą* reakcję na P0-1/P0-2 |
| NB-016 | Semantyka dzielenia całkowitego dla ujemnych | Nieujęta w żadnym rejestrze |
| NB-017 | Który z dwóch silników ARI jest autorytatywny i który model kary obowiązuje | Nieujęta w żadnym rejestrze |
| NB-018 | Konstrukcja Merkle (RFC 6962 vs wariant z duplikacją) | Nieujęta w żadnym rejestrze |

---

## 6. Koszt braku decyzji

- Żadna implementacja referencyjna nie może uzyskać certyfikacji: `RI-PY` i `RI-RS` obie
  **NOT CERTIFIED**, obie bez conformance runnera.
- Wszystkie dziesięć testów `CONF-001` … `CONF-010` pozostaje **DRAFT**; `APS-400` jest
  `1.0-DRAFT`.
- Conformance Kit pozostaje pusty — poprawnie, ale bezużytecznie.
- Rozbieżności międzyjęzykowe (D-1, D-2) pozostają **LATENT**; staną się **ACTIVE** przy
  pierwszym porcie lub granicy FFI.

**Brak decyzji nie generuje jednak ryzyka natychmiastowego:** żaden z tych elementów nie
jest dziś uruchamiany produkcyjnie, ponieważ nie istnieje ścieżka wykonawcza łącząca
warstwy (`02_RUNTIME_DATAFLOW.md` §1).

---

## 7. Czego ten brief nie robi

Nie rozstrzyga DR-002. Nie wybiera organu governance, formatu Constitution Vector,
semantyki normalizacji, zaokrąglania, dzielenia ani metody embeddingu. Nie generuje
Constitution Vector ani `constitution.json`. Nie implementuje CR-007. Nie traktuje
obecnego zachowania implementacji jako specyfikacji normatywnej.
