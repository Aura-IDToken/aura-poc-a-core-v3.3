# BEZPIECZNE PRACE INŻYNIERSKIE — bez dotykania semantyki FROZEN Core

**Data:** 2026-08-11
**Charakter:** filtr na już wytworzonych listach. **Brak nowego audytu. Brak nowych decyzji.**
**Podstawa:** `09_SAFE_WORK.md` przefiltrowane przez bramkę `NB-021 §13`.
**Zakres wyłączony:** `aura-specification` — nie jest dotykane.

---

## 0. Zastosowane kryterium

Praca trafia na listę tylko wtedy, gdy spełnia **wszystkie** cztery warunki:

1. nie zmienia żadnej wartości obliczanej przez system;
2. nie wymaga wyboru semantyki protokołu (DR-002 / AD-CA-xxx pozostają nietknięte);
3. nie zmienia żadnego hasha, ciągu bajtów ani formatu serializacji;
4. mieści się w kategorii wprost dopuszczonej przez korpus (`Decree Art. III`, `Art. VII`)
   **albo** leży całkowicie poza granicą FROZEN.

Warunek 4 jest tym, który odcina większość „normalnie bezpiecznych" prac.

---

## 1. DOPUSZCZONE — wprost, na podstawie cytowanego zezwolenia

### 1.1 Testy charakteryzujące (`core/`, `compliance/`)

Podstawa: `Decree Art. VII → Testing`, `Art. III` poz. 4. Kwalifikacja: NB-021 CASE D →
**PERMITTED**.

Test charakteryzujący **rejestruje zachowanie dzisiejsze**, nie orzeka o jego poprawności.
Nie tworzy zobowiązania normatywnego i uwidacznia każdą przyszłą zmianę zachowania.

| ID | Zakres | Co rejestruje |
|---|---|---|
| S-1 | wektory różnej długości → `vector_similarity_int32`, `_semantic_alignment` | `zip` obcina; wektor 2-elementowy wobec 4-elementowej konstytucji daje `100000` |
| S-2 | ujemny iloczyn skalarny | `-1 // 100000 == -1` |
| S-3 | `round()` na granicy `.5`, dodatniej i ujemnej | `[0, 2, 2]` / `[0, -2, -2]` |
| S-4 | górna granica `drift` | zmierzone `200000` i `100001`, wbrew docstringowi |
| S-5 | górna granica `ari` przy wektorze nieznormalizowanym | zmierzone `310000` |
| S-6 | rząd wielkości akumulatora dla 1536 wymiarów | `1.536 × 10¹³`, powyżej zakresu i32 |
| S-7 | test różnicowy: to samo wejście do obu silników ARI | że dają różny wynik |
| S-8 | trzy kanonikalizacje JSON na jednym obiekcie | że dają różne bajty |

**Warunek brzegowy, obowiązkowy:** każdy taki test musi być nazwany i opisany jako
*characterization*, nie *specification*. W S-2 i S-3 należy w treści testu odnotować, że
wartość jest zależna od języka i nierozstrzygnięta (NB-009 / NB-016).

**Granica:** `AGENTS.md` reguła 10 — "Tests must not be weakened merely to make
implementation pass".

### 1.2 Dokumentowanie zachowania istniejącego

Podstawa: `Decree Art. VII → Documentation`, `Art. III` poz. 5. Kwalifikacja: NB-021
CASE A → **PERMITTED**. Precedens zgodny: P-4 (CORE-007).

| ID | Praca |
|---|---|
| S-27 | Wpisy `KL-00x` w `docs/KNOWN_LIMITATIONS.md` dla D-1…D-7 — z adnotacją, że zachowanie poprawne jest nierozstrzygnięte |
| S-28 | Korekta `docs/GAP-001.md` GAP-C5 z „LARGELY RESOLVED" na stan zmierzony (dwa rozbieżne silniki) |
| S-29 | Tabela AS-IS czterech współistniejących reguł zaokrąglenia/redukcji (half-to-even, floor `//`, SQL half-up, dzielenie float) |
| S-30 | Odnotowanie, że `packages/**` jest niebudowalne |
| S-31 | Odnotowanie, że CHECK 1/2/4 są kontrolami leksykalnymi lub obecnościowymi, nie behawioralnymi |

**Granica:** `Decree Art. VII` — dokumentacja "❌ Do NOT advocate for forbidden changes".
Opis zachowania nie może przejść w opis zachowania *wymaganego*.

### 1.3 Cały `aura-guard-v1.3`

Podstawa: repozytorium zawiera **zero** wystąpień `frozen` / `freeze`. Żadna deklaracja
zamrożenia go nie obejmuje. Zero zależności od Constitution / Vector / ARI. NB-021 §13:
**UNAFFECTED**. Brief DR-002 §4: niezablokowane.

| ID | Praca | Priorytet z `08_BLOCKERS.md` |
|---|---|---|
| G-1 | `violations` poza zasięgiem integralności — `chain_hash` obejmuje 9 pól, tablica naruszeń nie jest jednym z nich; operator może przepisać reguły, akcje i confidence, a `aura-replay` nadal zgłasza `CHAIN OK` | **P0-6** |
| G-2 | Sprostowanie zdania o determinizmie w README (decyzja jest deterministyczna; `chain_hash` nie jest odtwarzalny z samego wejścia — zawiera `seq` i `timestamp`) | P2 |
| G-3 + P1-14 | `f32` w rekordzie dowodowym — planować **łącznie** z G-1, inaczej dodanie `violations` do skrótu tworzy nową powierzchnię niedeterminizmu formatowania float | P2 |
| G-4 | `AURA_AUTH_DISABLED=true` wyłącza jednocześnie auth i weryfikację podpisu | P2-18 |
| P1-9 | CI wyłącznie jednoplatformowe — brak arm64 | P1 |
| P2-19 | Wersja crate `1.3.0` wobec funkcji v1.4 obecnych w źródle | P2 |
| S-33 | Nieaktualna liczba testów w `docs/ROADMAP.md` (21+2+10+6 → 240) | P2 |

**Uwaga:** G-1 wymaga decyzji **produktowej** o formacie logu (zmiana łamiąca format).
To nie jest decyzja konstytucyjna i **nie zależy** od DR-002 ani NB-021.

---

## 2. WYKLUCZONE — z podaniem podstawy

Pozycje, które figurowały jako kandydaci w `09_SAFE_WORK.md`, a które bramka NB-021 odcina.

| Praca | Status | Podstawa |
|---|---|---|
| Naprawa P0-1 (obcinanie przy niezgodnej długości) | **BLOCKED** | NB-021 CASE C; dodatkowo nie przechodzi bramki 2 (`ROLE §4.1`) — poprawka zmienia wynik |
| Naprawa P1-3 (`drift` poza zadeklarowanym zakresem) | **BLOCKED** | CASE C — mimo że sprzeczność kodu z własnym docstringiem jest czysto inżynierska |
| Naprawa `demo.py` (S-21, S-22) | **BLOCKED** | CASE C |
| Jakakolwiek walidacja wejścia z reakcją (raise / sentinel / clamp) | **BLOCKED** | Wykrycie jest bezpieczne; wymagana *reakcja* to NB-015 (REQ-002-031) |
| Refaktoryzacja `core/` | **PROHIBITED** | `Decree Art. I` §9, §10; `Art. III` poz. 5–6; `copilot-guardrails.md` |
| Typowanie statyczne `core/` | **PROHIBITED** | jw.; ponadto adnotacja zawierająca token `float` wywróciłaby `check_2_integer_only.sh`, który jest zwykłym grepem |
| Logowanie / telemetria / metryki w `core/` lub `compliance/` | **PROHIBITED** | `Decree Art. III` poz. 7–9: "Adding logging decorators / Adding telemetry / Adding monitoring hooks" |
| Ujednolicenie trzech kanonikalizacji JSON | **BLOCKED** | Wybór jednej formy = AD-CA-008 |
| Podpięcie testów jednostkowych do CI (S-10, S-11) | **INDETERMINATE** | Pliki CI nie są ani logiką `core/`, ani dokumentacją, ani testami — kategoria nieujęta w `Decree Art. III` |
| Ruff / mypy / coverage / pip-audit / CodeQL w CI rdzenia (S-12…S-16) | **INDETERMINATE** | jw. |
| Benchmarki wydajności (S-39) | **INDETERMINATE** | Narzędzia wyłącznie pomiarowe nie są ujęte |
| Fixture z wartością oczekiwaną zależną od nierozstrzygniętej decyzji | **PROHIBITED** | NB-021 CASE E — **jedyne ustalenie jednomyślne w całym audycie**; cztery niezależne podstawy |

**Pozycje INDETERMINATE nie są zakazane — są nieobjęte.** Wymagają jednozdaniowego
rozstrzygnięcia kustodialnego (czy infrastruktura CI mieści się w granicy FROZEN), a nie
pełnego rozstrzygnięcia NB-021.

---

## 3. Kolejność wykonania

Uszeregowane wg stosunku wartości do ryzyka, nie wg etykiety priorytetu:

1. **§1.1 testy charakteryzujące** — zerowe ryzyko, zerowa treść normatywna; zamieniają
   każde otwarte pytanie o determinizm w zarejestrowany fakt, czyli dostarczają dokładnie
   tych danych, których potrzebują zablokowane decyzje DR-002 i NB-021.
2. **§1.3 prace nad `aura-guard`** — całkowicie poza granicą FROZEN; G-1 to najpoważniejsze
   ustalenie integralnościowe w ekosystemie poza P0-1.
3. **§1.2 dokumentacja** — prostuje trzy nieaktualne twierdzenia, które dziś wprowadzają
   w błąd.
4. **Zapytanie kustodialne** o pozycje INDETERMINATE z §2 — jedno zdanie odblokowuje CI.

Żaden z punktów 1–3 nie wymaga rozstrzygnięcia DR-002 ani NB-021.

---

## 4. Zastrzeżenie

Ten dokument **nie autoryzuje** żadnej pracy. Odtwarza granicę wynikającą z już
zarejestrowanych dowodów. Autoryzacja należy do Protocol Custodian; `Decree Art. X` wymaga
podpisu kustodialnego dla zmian w `core/`, a `AGENTS.md` reguła 13 — zgody człowieka przed
scaleniem zmian dotykających protokołu.

**W tym zadaniu nie wykonano żadnej z wymienionych prac.**
