#!/usr/bin/env python3
"""
CORE-006 CI: Compare two determinism reports.

Usage:
    python scripts/compare_determinism_reports.py <report_a.json> <report_b.json>

Exits with code 0 if all vectors match (PASS), 1 if any differ (FAIL).
"""

import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT))

from scripts.generate_determinism_report import compare_reports

if len(sys.argv) != 3:
    print("Usage: compare_determinism_reports.py <report_a.json> <report_b.json>")
    sys.exit(1)

path_a = Path(sys.argv[1])
path_b = Path(sys.argv[2])

report_a = json.loads(path_a.read_text(encoding="utf-8"))
report_b = json.loads(path_b.read_text(encoding="utf-8"))

_, mismatches = compare_reports(report_a, report_b)

platform_a = f"{report_a['platform']['system']}/{report_a['platform']['machine']}"
platform_b = f"{report_b['platform']['system']}/{report_b['platform']['machine']}"

print("=" * 70)
print("Aura Protocol v3.3 — Cross-Platform Determinism Comparison")
print("=" * 70)
print(f"Platform A : {platform_a}  (Python {report_a['platform']['python_version']})")
print(f"Platform B : {platform_b}  (Python {report_b['platform']['python_version']})")
print()

if mismatches:
    print("❌ DETERMINISM FAILURE — the following vectors differ:\n")
    for field, val_a, val_b in mismatches:
        print(f"  Field : {field}")
        print(f"    A   : {val_a}")
        print(f"    B   : {val_b}")
    print()
    print("BIT-IDENTITY IS LAW: same input must produce identical bits.")
    print("=" * 70)
    sys.exit(1)
else:
    vectors = report_a["determinism_vectors"]
    for k, v in vectors.items():
        print(f"  {k}: {v}")
    print()
    provenance = report_a.get("constitution_vector_provenance", {})
    print("CONSTITUTION VECTOR PROVENANCE")
    print(f"dimension = {provenance.get('dimension')}")
    print(f"scaling_factor = {provenance.get('scaling_factor')}")
    print(f"encoding = {provenance.get('byte_encoding')}")
    print(f"vector_sha256 = {provenance.get('vector_sha256')}")
    print(f"commit_sha = {provenance.get('tested_commit_sha')}")
    print("RESULT = PASS")
    print()
    print("✅ DETERMINISM PASS — all vectors are bit-identical across platforms.")
    print("=" * 70)
    sys.exit(0)
