#!/usr/bin/env python3
"""
Compare determinism reports from two platforms.

Usage:
    python scripts/compare_determinism_reports.py <report_a> <report_b> [<report_c> ...]

Exits 0 if all hash values are bit-identical across all reports.
Exits 1 if any value differs (CI failure).

Compared fields:
  hash_values.ari
  hash_values.drift
  hash_values.canonical_event_hash
  hash_values.merkle_root
  hash_values.audit_certificate_hash
"""

import json
import sys

COMPARED_KEYS = [
    "ari",
    "drift",
    "canonical_event_hash",
    "merkle_root",
    "audit_certificate_hash",
]


def load_report(path: str) -> dict:
    with open(path) as fh:
        return json.load(fh)


def main(report_paths: list) -> int:
    if len(report_paths) < 2:
        print("ERROR: At least two report files are required for comparison.")
        return 1

    reports = []
    for path in report_paths:
        report = load_report(path)
        platform = report.get("platform", {})
        machine = platform.get("machine", "unknown")
        print(f"Loaded report: {path}  (platform: {machine})")
        reports.append((path, report))

    reference_path, reference = reports[0]
    ref_hashes = reference["hash_values"]
    ref_platform = reference["platform"]["machine"]

    all_pass = True

    print()
    print("=" * 70)
    print("CROSS-PLATFORM DETERMINISM COMPARISON")
    print("=" * 70)
    print(f"Reference platform: {ref_platform}")
    print()

    for path, report in reports[1:]:
        platform_machine = report["platform"]["machine"]
        hashes = report["hash_values"]

        print(f"Comparing against: {platform_machine}  ({path})")
        platform_pass = True

        for key in COMPARED_KEYS:
            ref_val = ref_hashes.get(key)
            cmp_val = hashes.get(key)
            if ref_val == cmp_val:
                print(f"  ✓ {key}: MATCH")
            else:
                print(f"  ✗ {key}: MISMATCH")
                print(f"      {ref_platform}: {ref_val}")
                print(f"      {platform_machine}: {cmp_val}")
                platform_pass = False
                all_pass = False

        status = "PASS" if platform_pass else "FAIL"
        print(f"  Result: {status}")
        print()

    print("=" * 70)
    if all_pass:
        print("✅ ALL PLATFORMS: BIT-IDENTICAL — DETERMINISM VERIFIED")
        print("=" * 70)
        return 0
    else:
        print("❌ DETERMINISM FAILURE: Hash mismatch detected across platforms.")
        print("   This is a CRITICAL FAILURE for the metrological instrument.")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    paths = sys.argv[1:]
    sys.exit(main(paths))
