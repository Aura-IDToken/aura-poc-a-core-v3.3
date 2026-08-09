#!/bin/bash
# CHECK 8 — CR-003 Layer 0 History-Independence (Runtime / Behavioral Evidence)
# CLASS A: Proves that evaluate(same_inputs) == evaluate(same_inputs)
#          regardless of persisted audit history in PostgreSQL.

set -euo pipefail

mkdir -p artifacts

echo "=========================================="
echo "CHECK 8 — CR-003 Layer 0 History-Independence"
echo "=========================================="
echo ""

set +e
python3 -m unittest core.test_cr003_statelessness -v 2>&1 | tee artifacts/cr-003-statelessness.log
pipe_status=("${PIPESTATUS[@]}")
test_exit_code=${pipe_status[0]}
tee_exit_code=${pipe_status[1]:-0}
set -e

if [ "$test_exit_code" -ne 0 ]; then
  echo ""
  echo "❌ CR-003 runtime history-independence test FAILED"
  exit "$test_exit_code"
fi

if [ "$tee_exit_code" -ne 0 ]; then
  exit "$tee_exit_code"
fi

echo ""
echo "Runtime evidence log:    artifacts/cr-003-statelessness.log"
echo "Runtime evidence JSON:   artifacts/cr-003-statelessness-results.json"
