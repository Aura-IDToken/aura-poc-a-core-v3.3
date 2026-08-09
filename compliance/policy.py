"""
Core Policy Engine for Aura PoCA
Implements EU AI Act Compliance:
- Art. 5: Prohibition of human evaluation (algorithmic assertions only)
- Art. 14: Manual emergency halt (Kill-Switch)
"""

from datetime import datetime
from typing import Callable, Dict, Any, Optional


class RegulatoryPolicy:
    """EU AI Act compliance shield (Art. 5, 14)

    Uses fixed-point int32 arithmetic (scaling factor: 10^5 = 100,000)
    """

    SCALING_FACTOR = 100000
    DRIFT_THRESHOLD = 68000
    DRIFT_PENALTY = 150000

    HALTED_AGENTS = set()

    @staticmethod
    def validate_target(target_type: str):
        if target_type != "MACHINE_ACCOUNT":
            raise ValueError("CRITICAL: Human scoring is strictly prohibited.")

    @staticmethod
    def emergency_halt(agent_id: str):
        RegulatoryPolicy.HALTED_AGENTS.add(agent_id)

    @staticmethod
    def check_halt_status(agent_id: str):
        if agent_id in RegulatoryPolicy.HALTED_AGENTS:
            raise Exception("POLICY_HALT: Operation stopped by human oversight.")

    @staticmethod
    def calculate_penalties(sa_score: int) -> int:
        """Calculate penalties for behavioral drift."""
        return RegulatoryPolicy.DRIFT_PENALTY if sa_score < RegulatoryPolicy.DRIFT_THRESHOLD else 0


class PolicyRule:
    """
    Algorithmic policy rule for deterministic evaluation.
    Art. 5 Safeguard: Only algorithmic checks, no human evaluation.
    """

    def __init__(self, name: str, check_fn: Callable[[Dict[str, Any]], bool]):
        self.name = name
        self.check_fn = check_fn
        self._validate_no_human_evaluation()

    def _validate_no_human_evaluation(self):
        """Art. 5 compliance validation for rule function type."""
        if not callable(self.check_fn):
            raise ValueError(f"Policy rule '{self.name}' must be a callable function (Art. 5 safeguard)")

    def is_violated(self, event: Dict[str, Any]) -> bool:
        """Execute algorithmic policy check."""
        try:
            return self.check_fn(event)
        except (KeyError, AttributeError, TypeError):
            return True
        except Exception as e:
            import sys

            print(f"Warning: Unexpected exception in policy '{self.name}': {e}", file=sys.stderr)
            return True


class KillSwitch:
    """
    Art. 14 oversight: mandatory manual emergency halt mechanism.
    """

    def __init__(self):
        self._active = False
        self._activated_at: Optional[datetime] = None
        self._activated_by: Optional[str] = None
        self._reason: Optional[str] = None

    def activate(self, activated_by: str, reason: str) -> Dict[str, Any]:
        if self._active:
            return {
                "status": "already_active",
                "activated_at": self._activated_at.isoformat() if self._activated_at else None,
                "activated_by": self._activated_by,
            }

        self._active = True
        self._activated_at = datetime.utcnow()
        self._activated_by = activated_by
        self._reason = reason

        return {
            "status": "activated",
            "activated_at": self._activated_at.isoformat(),
            "activated_by": activated_by,
            "reason": reason,
        }

    def deactivate(self, deactivated_by: str) -> Dict[str, Any]:
        if not self._active:
            return {"status": "not_active"}

        previous_state = {
            "activated_at": self._activated_at.isoformat() if self._activated_at else None,
            "activated_by": self._activated_by,
            "reason": self._reason,
            "deactivated_by": deactivated_by,
            "deactivated_at": datetime.utcnow().isoformat(),
        }

        self._active = False

        return {
            "status": "deactivated",
            "previous_state": previous_state,
        }

    def is_active(self) -> bool:
        return self._active

    def get_state(self) -> Dict[str, Any]:
        return {
            "active": self._active,
            "activated_at": self._activated_at.isoformat() if self._activated_at else None,
            "activated_by": self._activated_by,
            "reason": self._reason,
        }

    def assert_not_halted(self):
        if self._active:
            raise SystemHaltException(
                f"System halted by kill-switch. "
                f"Activated by: {self._activated_by}, "
                f"Reason: {self._reason}, "
                f"At: {self._activated_at.isoformat() if self._activated_at else 'unknown'}"
            )


class SystemHaltException(Exception):
    """Exception raised when system is halted via Kill-Switch."""


_global_kill_switch = KillSwitch()


def get_kill_switch() -> KillSwitch:
    """Get the global kill-switch instance."""
    return _global_kill_switch
