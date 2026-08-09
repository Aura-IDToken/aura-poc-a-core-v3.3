#!/bin/bash
# CHECK 7 — CR-004 Append-Only Evidence Hardening

set -euo pipefail

mkdir -p artifacts

echo "=========================================="
echo "CHECK 7 — CR-004 Append-Only Evidence"
echo "=========================================="
echo ""

python3 -m unittest audit.test_audit_db_integration -v 2>&1 | tee artifacts/db-append-only-check.log
test_exit_code=${PIPESTATUS[0]}

if [ "$test_exit_code" -ne 0 ]; then
  exit "$test_exit_code"
fi

echo ""
echo "DB operation log: artifacts/db-append-only-check.log"
echo "DB results JSON:  artifacts/db-append-only-results.json"
