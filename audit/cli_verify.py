#!/usr/bin/env python3
"""
Independent verifier CLI for Event Trust Certificates.
"""

import argparse
import json
import sys

from .verify import verify_event_trust_certificate


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Aura Event Trust Certificate")
    parser.add_argument("--event", required=True, help="Path to canonical event JSON")
    parser.add_argument("--certificate", required=True, help="Path to certificate JSON")
    parser.add_argument("--key", required=True, help="Verification key")
    args = parser.parse_args()

    with open(args.event, "r", encoding="utf-8") as event_handle:
        event_payload = json.load(event_handle)
    with open(args.certificate, "r", encoding="utf-8") as cert_handle:
        cert_payload = json.load(cert_handle)

    is_valid = verify_event_trust_certificate(event_payload, cert_payload, args.key)
    print("PASS" if is_valid else "FAIL")
    return 0 if is_valid else 1


if __name__ == "__main__":
    sys.exit(main())

