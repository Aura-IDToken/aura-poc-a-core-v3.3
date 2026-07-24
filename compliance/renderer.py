"""
Certificate Renderer
Converts AuraEventCertificate to various output formats.
"""

import json
from typing import Dict, Any, Union
from .certificate import AuraEventCertificate


def render_certificate(cert: AuraEventCertificate, format: str = "json") -> Union[str, Dict[str, Any]]:
    """
    Render an AuraEventCertificate to the specified format.
    
    Args:
        cert: The certificate to render
        format: Output format ('json', 'text', or 'dict')
        
    Returns:
        Rendered certificate as string or dict
    """
    if format == "dict":
        return cert.to_dict()
    elif format == "json":
        return json.dumps(cert.to_dict(), indent=2)
    elif format == "text":
        d = cert.to_dict()
        lines = [
            "=" * 60,
            "AURA EVENT CERTIFICATE",
            "=" * 60,
            f"Agent ID: {d['agent_id']}",
            f"Timestamp: {d['timestamp']}",
            "",
            "PoCA Score:",
            f"  Score: {d['poca']['score']:.3f}",
            f"  Drift: {d['poca']['drift']:.3f}",
            f"  Status: {d['poca']['status']}",
            "",
            "Audit Trail:",
            f"  Leaf Hash: {d['audit']['leaf_hash'][:32]}...",
            f"  Merkle Root: {d['audit']['merkle_root'][:32]}...",
            "",
            f"Certificate Fingerprint: {cert.fingerprint()[:32]}...",
            "=" * 60,
        ]
        return "\n".join(lines)
    else:
        raise ValueError(f"Unsupported format: {format}")
