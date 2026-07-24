"""
DEPRECATED: Layer Separation Compatibility Wrapper

This module violates Layer Separation (Layer 0 importing from Layer 2).
It exists ONLY for backward compatibility in v3.3.

MIGRATION NOTICE:
Import directly from compliance.policy instead:
    
    from compliance.policy import RegulatoryPolicy, PolicyRule, KillSwitch, ...

This wrapper will be REMOVED in Aura Protocol v4.0.

Architectural Context:
- Layer 0 (core/) should perform MEASUREMENT only
- Layer 2 (compliance/) handles POLICY decisions
- This wrapper temporarily bridges the gap for existing code

See: docs/GAP-001.md CORE-005, docs/KNOWN_LIMITATIONS.md KL-001
"""
import warnings

# Issue deprecation warning
warnings.warn(
    "Importing from core.policy is deprecated and violates Layer Separation. "
    "Use 'from compliance.policy import ...' instead. "
    "This wrapper will be removed in Aura Protocol v4.0. "
    "See docs/GAP-001.md CORE-005 for migration details.",
    DeprecationWarning,
    stacklevel=2
)

# Re-export for backward compatibility only
from compliance.policy import (
    KillSwitch,
    PolicyRule,
    RegulatoryPolicy,
    SystemHaltException,
    get_kill_switch,
)

__all__ = [
    "KillSwitch",
    "PolicyRule",
    "RegulatoryPolicy",
    "SystemHaltException",
    "get_kill_switch",
]
