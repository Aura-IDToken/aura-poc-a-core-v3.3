# compliance/certificate.py

from dataclasses import dataclass
from typing import Dict, Any
import json
import hashlib

from audit.pipeline import AuditLayerPipeline, AuditPipelineResult


@dataclass(frozen=True)
class AuraEventCertificate:
    """
    Deterministic, compliance-ready representation of a single evaluated event.
    This object is the ONLY external-facing output of the PoCA core.
    
    SCOPE: MACHINE_ACCOUNT entities only (AI Act Art. 5 compliant)
    PROHIBITION: No human profiling or biometric data
    
    Uses Agent Reliability Index (ARI) - NOT "Trust Score" to avoid 
    Social Scoring classification under EU AI Act.

    ## Layer 0 / Layer 2 Representation

    The Layer 0 measurement engine (`core/evaluator.py`) produces ARI and drift
    as **int32 values scaled by 10^5** (e.g., 0.85 → 85000).

    This certificate stores those values as **float** for human-readable output
    and external API compatibility.  The conversion is:

        ari_score  = ari_int32  / SCALING_FACTOR   (e.g., 85000 / 100000 = 0.85)
        drift      = drift_int32 / SCALING_FACTOR

    This conversion is intentional and limited to the presentation/reporting layer.
    Raw int32 values remain the normative measurement.  Callers that need bit-exact
    int32 values should read them directly from the evaluator result dict before
    constructing this certificate.
    """

    agent_id: str  # MACHINE_ACCOUNT identifier only
    timestamp: str

    ari_score: float  # Agent Reliability Index ∈ [0.0, 1.0]
    drift: float
    status: str

    merkle_root: str
    leaf_hash: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": "1.0.0",
            "agent_id": self.agent_id,
            "timestamp": self.timestamp,
            "ari": {
                "score": self.ari_score,
                "drift": self.drift,
                "status": self.status,
            },
            "audit": {
                "leaf_hash": self.leaf_hash,
                "merkle_root": self.merkle_root,
            },
        }

    def fingerprint(self) -> str:
        """
        Deterministic hash of the entire certificate.
        This is what can be anchored, signed, or published.
        """
        payload = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def issue_audit_certificate(
    pipeline: AuditLayerPipeline,
    event_id: str,
    timestamp: str,
    agent_id: str,
    ari: int,
    drift: int,
    schema_valid: bool,
    engine_version: str,
    policy_version: str,
) -> AuditPipelineResult:
    """
    Compliance-layer entry point for issuing an audit-layer certificate.
    """
    return pipeline.append_and_certify(
        {
            "event_id": event_id,
            "timestamp": timestamp,
            "agent_id": agent_id,
            "ari": ari,
            "drift": drift,
            "schema_valid": schema_valid,
            "engine_version": engine_version,
            "policy_version": policy_version,
        }
    )
