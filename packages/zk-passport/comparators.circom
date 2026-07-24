pragma circom 2.1.0;

/**
 * COMPARATORS - Standard circomlib components for comparison operations
 * 
 * This is a minimal implementation of comparison circuits needed for
 * reputation_check.circom. Based on circomlib standard library.
 */

/**
 * LessThan - Check if in[0] < in[1]
 * n: Number of bits to represent each input
 */
template LessThan(n) {
    assert(n <= 252);
    signal input in[2];
    signal output out;

    component n2b = Num2Bits(n+1);
    n2b.in <== in[0]+ (1<<n) - in[1];

    out <== 1-n2b.out[n];
}

/**
 * GreaterEqThan - Check if in[0] >= in[1]
 * n: Number of bits to represent each input
 */
template GreaterEqThan(n) {
    signal input in[2];
    signal output out;

    component lt = LessThan(n);
    lt.in[0] <== in[0];
    lt.in[1] <== in[1];

    out <== 1 - lt.out;
}

/**
 * Num2Bits - Convert number to binary representation
 * n: Number of bits
 */
template Num2Bits(n) {
    signal input in;
    signal output out[n];
    var lc1=0;

    var e2=1;
    for (var i = 0; i<n; i++) {
        out[i] <-- (in >> i) & 1;
        out[i] * (out[i] -1 ) === 0;
        lc1 += out[i] * e2;
        e2 = e2+e2;
    }

    lc1 === in;
}
