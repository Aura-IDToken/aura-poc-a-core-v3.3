class RegulatoryPolicy:
    """EU AI Act compliance shield (Art. 5, 14)
    
    Uses fixed-point int32 arithmetic (scaling factor: 10^5 = 100,000)
    """
    
    # Regulatory constants (fixed-point int32)
    SCALING_FACTOR = 100000  # 10^5
    DRIFT_THRESHOLD = 68000  # 0.68 * 10^5 - Semantic alignment threshold for drift detection
    DRIFT_PENALTY = 150000   # 1.5 * 10^5 - Penalty applied when drift is detected
    
    HALTED_AGENTS = set()

    @staticmethod
    def validate_target(target_type: str):
        # Art. 5: Prohibition of human social scoring
        assert target_type == "MACHINE_ACCOUNT", "CRITICAL: Human scoring is strictly prohibited."

    @staticmethod
    def emergency_halt(agent_id: str):
        # Art. 14: Human oversight (Kill-Switch)
        RegulatoryPolicy.HALTED_AGENTS.add(agent_id)

    @staticmethod
    def check_halt_status(agent_id: str):
        if agent_id in RegulatoryPolicy.HALTED_AGENTS:
            raise Exception("POLICY_HALT: Operation stopped by human oversight.")

    @staticmethod
    def calculate_penalties(sa_score: int) -> int:
        """
        Calculate penalties for behavioral drift.
        
        Args:
            sa_score: Semantic alignment score (int32, scaled by 10^5)
            
        Returns:
            Penalty value (int32, scaled by 10^5)
        """
        # Penalty for sudden behavioral drift (Sim < DRIFT_THRESHOLD)
        return RegulatoryPolicy.DRIFT_PENALTY if sa_score < RegulatoryPolicy.DRIFT_THRESHOLD else 0


class PolicyRule:
    def __init__(self, name, check_fn):
        self.name = name
        self.check_fn = check_fn

    def is_violated(self, event):
        return self.check_fn(event)
