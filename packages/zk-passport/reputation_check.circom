pragma circom 2.1.0;

include "comparators.circom";

/**
 * REPUTATION CHECK CIRCUIT v3.3 (Iron Core Correct)
 * Rola: Dowód ZK przynależności do progu reputacji ARI.
 * Rygor: Operacje na liczbach całkowitych (Integer Scaling $10^5$).
 */
template ReputationCheck() {
    // Wejścia prywatne
    signal input secretARI;        // Skalowany wskaźnik ARI ($v_{int}=v_{float}\cdot10^5$)
    signal input isMachine;       // Asercja Art. 5: 1 dla MACHINE_ACCOUNT
    signal input schemaIntegrity; // Binarne SI (1 = sukces, 0 = błąd)

    // Wejścia publiczne
    signal input threshold;       // Próg akceptacji (np. 80000 dla 0.8)

    // Wyjście
    signal output isVerified;

    // 1. Weryfikacja Art. 5 AI Act
    // Dowód jest nieprawidłowy, jeśli celem oceny nie jest maszyna.
    isMachine === 1;

    // 2. Multiplier logic: Brama SI
    // W rygorze v3.3 błąd strukturalny (SI=0) uniemożliwia walidację.
    schemaIntegrity === 1;

    // 3. Sprawdzenie progu reputacji
    // Porównanie zdeterminowane skalowaniem 10^5.
    component geq = GreaterEqThan(32);
    geq.in[0] <== secretARI;
    geq.in[1] <== threshold;

    isVerified <== geq.out;

    // Wymuszenie binarnego wyniku (0 lub 1)
    isVerified * (isVerified - 1) === 0;
}

component main {public [threshold]} = ReputationCheck();
