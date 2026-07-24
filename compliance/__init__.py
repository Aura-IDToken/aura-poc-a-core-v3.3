"""
Aura Protocol — Compliance Layer

This package contains Layer 2 modules that sit above the deterministic
measurement core.

Current responsibilities:
- policy enforcement utilities (`compliance.policy`)
- policy-aware orchestration (`compliance.evaluator_wrapper`)
- consistency-layer helpers (`compliance.consistency`)
- certificate generation and rendering

Layer 2 may interpret measurement outputs for orchestration purposes.
Layer 0 (`core/`) remains measurement-only.
"""

from .certificate import AuraEventCertificate
from .renderer import render_certificate

__all__ = [
    "AuraEventCertificate",
    "render_certificate",
]
