#!/bin/bash
# CHECK 10 — P0-1 Vector Dimension Validation (Runtime / Behavioral Evidence)
# CLASS A: Proves that a vector whose dimension differs from the constitution
#          vector is rejected fail-closed, and that NO ARI value is produced.
#
# Rationale: core/test_ari.py was previously only checked for EXISTENCE by
# CHECK 4 (check_4_audit_path.sh) and was never executed. AGENTS.md rule 9
# requires executable evidence for every conformance claim, so the P0-1 suite
# is executed here.
#
# The guard is also re-run under -O and -OO because AGENTS.md rule 4 forbids
# security/compliance enforcement from relying on Python `assert`.

set -euo pipefail

mkdir -p artifacts

echo "=========================================="
echo "CHECK 10 — P0-1 Vector Dimension Validation"
echo "=========================================="
echo ""

set +e
python3 -m unittest core.test_ari -v 2>&1 | tee artifacts/p0-1-dimension-validation.log
pipe_status=("${PIPESTATUS[@]}")
test_exit_code=${pipe_status[0]}
tee_exit_code=${pipe_status[1]:-0}
set -e

if [ "$test_exit_code" -ne 0 ]; then
  echo ""
  echo "❌ P0-1 dimension validation suite FAILED"
  exit "$test_exit_code"
fi

if [ "$tee_exit_code" -ne 0 ]; then
  exit "$tee_exit_code"
fi

# Independent fail-closed proof under optimized bytecode.
echo ""
echo "--- Fail-closed guard under optimized bytecode (AGENTS.md rule 4) ---"

GUARD_PROGRAM='
from core.evaluator import PoCAEvaluator
ev = PoCAEvaluator([31622] * 10)
try:
    ev.evaluate("check10", [50000] * 5, True)
except ValueError:
    print("REJECTED")
else:
    print("ACCEPTED")
'

# NOTE: this loop is deliberately NOT piped into `tee`. Piping would run the
# loop body in a subshell, where `exit 1` cannot fail the check — a fail-open
# defect. Output is appended to the log explicitly instead.
for flag in "" "-O" "-OO"; do
  label="${flag:-DEFAULT}"
  # shellcheck disable=SC2086
  output=$(python3 $flag -c "$GUARD_PROGRAM")
  if [ "$output" != "REJECTED" ]; then
    echo "❌ Guard bypassed under ${label}: ${output}" \
      | tee -a artifacts/p0-1-dimension-validation.log
    exit 1
  fi
  echo "✅ ${label}: dimension mismatch REJECTED" \
    | tee -a artifacts/p0-1-dimension-validation.log
done

echo ""
echo "✅ CHECK 10 PASSED: P0-1 dimension mismatch is rejected fail-closed"
echo ""
echo "Runtime evidence log: artifacts/p0-1-dimension-validation.log"
