# DECISION BRIEF — NB-021

**Dla:** Protocol Custodian / Chief Architect
**Data:** 2026-08-11
**Charakter:** streszczenie istniejących ustaleń. **Brak nowego audytu. Brak nowych decyzji.
Brak zmian w repozytorium normatywnym.**
**Źródło:** `NB-021_FROZEN_SEMANTICS_AUDIT.md`. Cytaty normatywne w oryginalnym brzmieniu (EN).

---

## 1. Pytanie

Czy niesemantyczna (nienormatywna) korekta defektu inżynierskiego może zostać wprowadzona
do implementacji powiązanej z FROZEN v3.3 **bez zmiany jej tożsamości normatywnej**?

## 2. Werdykt

# INDETERMINATE

Pochodne:

| Kategoria | Werdykt |
|---|---|
| Zmiana specyfikacji (in place, ta sama tożsamość) | **PROHIBITED** |
| Zmiana wyłącznie testowa | **PERMITTED** (w granicach Decree Art. VII) |
| Poprawka defektu bezpieczeństwa | **INDETERMINATE** |
| Zmiany kodu inżynierskiego | **BLOCKED** do czasu rozstrzygnięcia |

---

## 3. Trzy fakty, które przesądziły

**(a) Ramy decyzyjne unieważniają same siebie.**
`ROLE_OF_THE_PROTOCOL_CUSTODIAN.md` §4.1 stosuje dwie bramki sekwencyjnie:

> Bramka 1: "Mathematical error? → Acceptable"
> Bramka 2: "Does this change preserve bit-identity? … NO → REJECTED. UNCERTAIN → REJECTED."

Każda poprawka błędu zmienia wynik, więc Bramka 2 odrzuca dokładnie to, na co Bramka 1
zezwala.

**(b) Zezwolenie na poprawki bezpieczeństwa jest węższe, niż się wydaje.**
Trzy niezależne wystąpienia (`Decree Art. III`, `ROLE §2.1.2`, `ROLE §3.2.3`) konsekwentnie
zawężają je do **"in changed lines" / "in changed code"**. Dla defektu w kodzie
niezmienionym i już zamrożonym — czyli w sytuacji faktycznej — korpus nie udziela
zezwolenia w ogóle.

**(c) v3.3 nie ma tożsamości, którą można by zachować.**
Brak tagu git, brak katalogu `releases/`, brak sumy kontrolnej.
`docs/LEGACY_PROTOCOL.md:78` wciąż zawiera niewypełniony placeholder:

> "SHA-256 checksum: `[COMPUTED_AT_SEALING_v3.3]`"

Wobec definicji własnej korpusu (`GLOSSARY`: "The cryptographic identity of each frozen
protocol version is defined by hashes and archival artifacts") tożsamość v3.3 jest
**niezdefiniowana**. Pytanie „bez zmiany tożsamości" nie ma dziś desygnatu.

---

## 4. Rozróżnienie, które może okazać się kluczowe

**FROZEN ≠ SEALED.** Korpus implementacyjny wiąże bezwzględną niezmienność z **zapieczętowaniem**, nie z zamrożeniem:

> `OPS_PROTOCOL_CANONICAL.md` §4.1: "**Once sealed**, the artifact is immutable."
> `ROLE` §6.5: "**Post-Seal:** Archive receives notation: `v3.3-SEALED` · No further changes
> permitted to this version"

**Zapieczętowanie nie nastąpiło.** Brak notacji `v3.3-SEALED`, brak M-DISC, brak
certyfikatu kustodialnego, placeholder SHA niewypełniony.

To najmocniejszy dowód przeciw czytaniu FROZEN jako bezwzględnej niezmienności — i zarazem
**nie** dowód, że FROZEN dopuszcza korektę.

---

## 5. Praktyka rozeszła się z regułami

Zarejestrowane jako fakty, **nie** jako precedens normatywny.

| ID | Fakt | SHA |
|---|---|---|
| P-1 | `docs/mathematical_foundation.md` — dokument o treści „immutable" — otrzymał przepisanie sekcji formuły **in place**, ze znacznikiem FROZEN pozostawionym bez zmian, bez inkrementacji wersji i bez dokumentu zastępującego | `4ced103` |
| P-2 | `compliance/policy.py`: `assert` → `raise ValueError`. Zmiana obserwowalna (typ wyjątku; zachowanie pod `python -O`). Etykieta v3.3 zachowana, brak nowej linii rodowej | `4ced103` |
| P-3 | `core/evaluator.py`: zmiana sygnatury `evaluate()` i zachowania — czyli „core logic" w rozumieniu Decree Art. VIII, który mówi, że to tworzy **NOWY INSTRUMENT**. Nowy instrument nie powstał | `4ced103` |

**Okoliczność obciążająca:** `CONSTITUTIONAL_DECREE.md` Art. IX nadal stanowi, że
`assert target_type == "MACHINE_ACCOUNT"` jest **MANDATORY in every evaluation path**.
P-2 usunął tę asercję. Dekret nie został znowelizowany (ostatnia zmiana: styczeń 2026).
Implementacja i dokument nieuchylalny pozostają w bezpośredniej sprzeczności.

Dla żadnej z tych zmian nie odnaleziono zapisu autoryzacji kustodialnej, mimo że
`Decree Art. X` wymaga: "Custodian Signature: [Required for core/ changes]".

**Precedens zgodny z regułami:** P-4 — korekty wyłącznie dokumentacyjne (CORE-007) zostały
wykonane z zapisanym oświadczeniem o autoryzacji w `CHANGELOG.md`.

---

## 6. Pytania do rozstrzygnięcia — w kolejności zależności

Wszystkie już zarejestrowane w `NB-021 §14`. **Żadne nie jest nowe.**

1. Czy status FROZEN korpusu specyfikacyjnego w ogóle stosuje się do implementacji v3.3,
   czy są to dwa niezwiązane terminy?
2. Czy granicą niezmienności jest FROZEN, czy SEALED?
3. Czy „nienormatywna korekta defektu" jest kategorią uznaną — a jeśli tak, jaka jest jej
   procedura, organ, forma artefaktu i skutek dla tożsamości?
4. Czym jest tożsamość normatywna v3.3, skoro nie istnieje tag, SHA ani artefakt archiwalny?
5. Czy bramka bit-identity (`ROLE §4.1`) i zezwolenie na korektę (`Decree Art. III`)
   obowiązują łącznie — a jeśli tak, które ma pierwszeństwo?
6. Gdy implementacja i specyfikacja są sprzeczne, która ma moc rozstrzygającą?
   (`AUDIT_LAYER_SPEC.md` mówi „implementation governs"; Konstytucja Art. IV P1 i
   `CONTRIBUTING.md` mówią dokładnie odwrotnie.)
7. Czy zmiany P-1, P-2, P-3 były autoryzowane, a jeśli tak — na jakiej podstawie?

---

## 7. Co odblokowuje która odpowiedź

| Rozstrzygnięcie | Odblokowuje |
|---|---|
| Pytanie 2 → „granicą jest SEALED" | Korekty defektów w v3.3 przed zapieczętowaniem; P0-1 (długość wektora), P1-3 (`drift`), P1-5 (`demo.py`) |
| Pytanie 3 → uznanie kategorii + procedura | Cała §1.3 z `09_SAFE_WORK.md` |
| Pytanie 5 → pierwszeństwo Art. III nad bramką 2 | Poprawki zmieniające wynik |
| Pytanie 4 → związanie tożsamości (tag/SHA) | Możliwość w ogóle *oceniania* zachowania tożsamości |
| Pytanie 7 → ratyfikacja albo cofnięcie | Usunięcie rozbieżności między Dekretem Art. IX a kodem |

**Bez rozstrzygnięcia** pozostaje dostępna praca opisana w `SAFE_ENGINEERING_WORK.md`.

---

## 8. Czego ten brief nie robi

Nie rozstrzyga NB-021. Nie wybiera modelu governance. Nie proponuje trybu nadzwyczajnego,
nowego stanu cyklu życia ani nowej procedury. Nie zmienia statusu żadnego dokumentu. Nie
naprawia żadnego defektu. Nie orzeka, czy zmiany P-1…P-3 były dopuszczalne.
