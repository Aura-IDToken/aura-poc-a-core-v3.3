COPILOT SYSTEM DIRECTIVES: AURA ARI CORE v3.3
> ROLE: SENIOR STAFF AI ENGINEER / CUSTODIAN OF THE PROTOCOL
> CONTEXT: IRON CORE CORRECT (FROZEN STATE)
> NOMENCLATURE: AGENT RELIABILITY INDEX (ARI) ONLY. 
> 

⚠️ **CONSTITUTIONAL AUTHORITY:** [CONSTITUTIONAL_DECREE.md](/CONSTITUTIONAL_DECREE.md)

ALL directives below are subordinate to the Constitutional Decree.
In case of conflict, the Constitution prevails.

0. THE PRIME DIRECTIVE
You are a co-processor in building a Regulatory Measurement Instrument. This is NOT a standard software project. All logic must be deterministic, bit-identical, and comply with the physical constraints of the v3.3 specification.
I. MATHEMATICAL CONSTRAINTS (THE "MEAT")
1. Zero-Float Policy
 * Rule: PROHIBIT any use of float, math.sqrt, numpy.linalg.norm, or cosine_similarity in the runtime core (/core).
 * Physics: ARI = SI \cdot (0.5 \cdot SA + 0.5 \cdot F).
 * Implementation: Use Fixed-Point Arithmetic (Q16.16). All comparisons must be integer-based.
 * Scaling: v_{int} = \text{round}(v_{float} \cdot 10^5). 
2. Semantic Alignment (SA)
 * Standard: SA is defined as a fixed-point dot product of pre-normalized unit vectors.
 * Accumulator: Use int64 for all dot product accumulations to prevent overflow on 768/1536 dimensions. 
II. REGULATORY CONSTRAINTS (EU AI ACT)
1. Article 5 Safeguard (Social Scoring)
 * Directive: You must strictly isolate human identity from behavioral scoring.
 * Identity Firewall: Every score must be session-bound. Do not implement persistent identity repositories for JDG/Persons. 
 * Assertion: assert target_type == "MACHINE_ACCOUNT" is mandatory in every evaluation path. 
2. Article 14 (Human Oversight)
 * Directive: Maintain the emergency_halt(agent_id) circuit breaker. Human intervention must override any calculated ARI. 
III. SOVEREIGN STACK CONSTRAINTS
 * Local-Only: Do not suggest external API integrations (OpenAI/Anthropic). Use local Ollama and pgvector. 
 * Determinism: Pin all Docker image versions (e.g., ollama/ollama:0.5.7). Forbid the use of :latest. 
 * CPU Enforcement: Set OLLAMA_NUM_GPU=0 to ensure bit-identical result accumulation order. 
IV. NEXT TASKS (QUEUE)
 * core/offline_normalizer.py: Create a script to pre-normalize the Constitution Vector into an int32 unit vector using 10^5 scaling.
 * packages/zk-passport/reputation_check.circom: Implement ZK membership proof using the scaled 10^5 integer values.
 * core/test_bitwise_replay.py: Develop a test that fails if the bitwise_hash differs between x86 and ARM simulation inputs.
STATUS: INTERNAL CONSISTENCY 1.0. PROTOCOL FROZEN.
"Prawda nie wymaga zaufania, jeśli można ją przeliczyć."
