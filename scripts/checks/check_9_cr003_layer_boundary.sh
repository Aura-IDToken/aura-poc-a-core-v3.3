#!/bin/bash
# CHECK 9 — CR-003 Layer 0 Boundary (AST / Structural Evidence)
# CLASS B: AST-based proof that Layer 0 (core/*.py) contains no
#          forbidden imports (DB drivers, audit, compliance, network, etc.).

set -euo pipefail

mkdir -p artifacts

echo "=========================================="
echo "CHECK 9 — CR-003 Layer 0 Static Boundary"
echo "=========================================="
echo ""

set +e
python3 scripts/check_cr003_layer_boundary.py 2>&1 | tee artifacts/cr-003-layer-boundary.log
pipe_status=("${PIPESTATUS[@]}")
check_exit_code=${pipe_status[0]}
tee_exit_code=${pipe_status[1]:-0}
set -e

if [ "$check_exit_code" -ne 0 ]; then
  echo ""
  echo "❌ CR-003 Layer 0 boundary check FAILED"
  exit "$check_exit_code"
fi

if [ "$tee_exit_code" -ne 0 ]; then
  exit "$tee_exit_code"
fi

echo ""
echo "Structural evidence log:  artifacts/cr-003-layer-boundary.log"
echo "Structural evidence JSON: artifacts/cr-003-layer-boundary.json"
