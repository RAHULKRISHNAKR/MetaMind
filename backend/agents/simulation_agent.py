"""
SimulationAgent - Estimate metrics for architecture candidates

This hybrid agent combines rule-based calculations with LLM-based assessments.
"""

import json
import time
from typing import Dict, List
from langchain_core.prompts import PromptTemplate
from ..orchestration.state import (
    MetaMindState,
    Architecture,
    RawMetrics,
    SimulationResult
)
from ..utils.llm_utils import create_llm_with_retry, invoke_llm_with_retry, parse_json_with_retry
from ..utils.logging_config import AgentLogger


class SimulationAgent:
    """
    Hybrid agent that simulates architecture performance.
    
    Estimates:
    - Cost (rule-based)
    - Latency (rule-based + topology analysis)
    - Risk (LLM-based)
    - Compliance (LLM-based)
    - Scalability (rule-based)
    - Complexity (rule-based)
    """
    
    # Model pricing (per 1K tokens)
    MODEL_COSTS = {
        "llama3-8b": 0.0001,
        "llama3-70b": 0.0008,
        "llama 3 8b": 0.0001,
        "llama 3 70b": 0.0008,
        "gpt-4": 0.03,
        "gpt-3.5": 0.002,
        "claude-3": 0.015,
        "claude-2": 0.008,
        "gemini-pro": 0.0005,
        "fine-tuned": 0.0002
    }
    
    # Infrastructure costs (per month)
    INFRA_COSTS = {
        "postgresql": 50,
        "mongodb": 60,
        "redis": 30,
        "chromadb": 40,
        "s3": 25,
        "kubernetes": 200,
        "docker": 50,
        "prometheus": 30,
        "grafana": 20
    }
    
    def __init__(self, ollama_base_url: str = "http://localhost:11434", model_name: str = "llama3"):
        """
        Initialize the SimulationAgent.
        
        Args:
            ollama_base_url: Base URL for Ollama service
            model_name: Name of the Ollama model to use
        """
        self.llm = create_llm_with_retry(
            base_url=ollama_base_url,
            model=model_name,
            temperature=0.2,  # Low temperature for consistent assessment
            timeout=90
        )
        self.logger = AgentLogger("SimulationAgent")
        
        self.risk_prompt = PromptTemplate(
            input_variables=["architecture", "domain", "risk_tolerance"],
            template="""You are a security and risk assessment expert. Evaluate the risk level of this AI architecture.

Architecture:
{architecture}

Domain: {domain}
Risk Tolerance: {risk_tolerance}

Assess risks including:
1. Data security and privacy
2. Model reliability and failure modes
3. System availability and resilience
4. Compliance and regulatory risks
5. Operational risks

Output ONLY a JSON object:
{{
    "risk_score": <0-100, where 100 is lowest risk>,
    "risk_factors": ["factor1", "factor2", ...],
    "mitigation_recommendations": ["rec1", "rec2", ...]
}}

JSON Output:"""
        )
        
        self.compliance_prompt = PromptTemplate(
            input_variables=["architecture", "domain", "compliance_level"],
            template="""You are a compliance and regulatory expert. Evaluate the compliance readiness of this AI architecture.

Architecture:
{architecture}

Domain: {domain}
Compliance Level Required: {compliance_level}

Assess compliance with:
1. Data protection regulations (GDPR, CCPA, etc.)
2. Industry-specific regulations
3. AI ethics and fairness
4. Audit trail and transparency
5. Data retention and deletion

Output ONLY a JSON object:
{{
    "compliance_score": <0-100, where 100 is fully compliant>,
    "compliance_gaps": ["gap1", "gap2", ...],
    "compliance_recommendations": ["rec1", "rec2", ...]
}}

JSON Output:"""
        )
    
    def execute(self, state: MetaMindState) -> MetaMindState:
        """
        Execute simulation for all candidate architectures.
        
        Args:
            state: Current MetaMind state
            
        Returns:
            MetaMindState: Updated state with simulation results
        """
        try:
            candidates = state.get("candidate_architectures", [])
            
            if not candidates:
                raise ValueError("No candidate architectures to simulate")
            
            simulation_results = []
            
            for i, arch in enumerate(candidates, 1):
                print(f"  Simulating architecture {i}/{len(candidates)}: {arch['name']}")
                
                # Estimate all metrics
                raw_metrics = self._simulate_architecture(arch, state)
                
                # Create simulation result
                sim_result = SimulationResult(
                    architecture_id=arch["architecture_id"],
                    raw_metrics=raw_metrics,
                    normalized_scores={},  # Will be filled by scoring engine
                    final_score=0.0  # Will be filled by scoring engine
                )
                
                simulation_results.append(sim_result)
            
            # Update state
            state["simulation_results"] = simulation_results
            
            print(f"✓ Simulated {len(simulation_results)} architectures")
        
        except Exception as e:
            error_msg = f"SimulationAgent failed: {str(e)}"
            print(f"✗ {error_msg}")
            state["errors"].append(error_msg)
        
        return state
    
    def _simulate_architecture(
        self,
        architecture: Architecture,
        state: MetaMindState
    ) -> RawMetrics:
        """
        Simulate a single architecture.
        
        Args:
            architecture: Architecture to simulate
            state: Current state
            
        Returns:
            RawMetrics: Estimated metrics
        """
        constraints = state["constraints"]
        
        # Estimate cost
        cost = self._estimate_cost(architecture, constraints)
        
        # Estimate latency
        latency = self._estimate_latency(architecture, constraints)
        
        # Assess risk (LLM-based)
        risk_score = self._assess_risk(architecture, state)
        
        # Check compliance (LLM-based)
        compliance_score = self._check_compliance(architecture, state)
        
        # Analyze scalability
        max_users = self._analyze_scalability(architecture, constraints)
        
        # Calculate complexity
        complexity = self._calculate_complexity(architecture)
        
        return RawMetrics(
            estimated_monthly_cost=cost,
            p95_latency_ms=latency,
            risk_score=risk_score,
            compliance_score=compliance_score,
            max_concurrent_users=max_users,
            implementation_complexity=complexity
        )
    
    def _estimate_cost(self, architecture: Architecture, constraints: Dict) -> float:
        """
        Estimate monthly cost.
        
        Args:
            architecture: Architecture specification
            constraints: System constraints
            
        Returns:
            float: Estimated monthly cost in USD
        """
        total_cost = 0.0
        
        # Model costs (based on expected usage)
        expected_users = constraints["expected_users"]
        avg_requests_per_user = 100  # per month
        avg_tokens_per_request = 1000
        
        total_tokens = expected_users * avg_requests_per_user * avg_tokens_per_request
        total_tokens_k = total_tokens / 1000
        
        # Find model in modules
        model_cost_per_k = 0.0001  # default
        for module in architecture["modules"]:
            if module["layer"] == "Model Layer":
                component = module["component"].lower()
                for model_name, cost in self.MODEL_COSTS.items():
                    if model_name in component:
                        model_cost_per_k = cost
                        break
        
        model_cost = total_tokens_k * model_cost_per_k
        total_cost += model_cost
        
        # Infrastructure costs
        for module in architecture["modules"]:
            component = module["component"].lower()
            for infra_name, cost in self.INFRA_COSTS.items():
                if infra_name in component:
                    total_cost += cost
        
        # Add 20% overhead for networking, storage, etc.
        total_cost *= 1.2
        
        return round(total_cost, 2)
    
    def _estimate_latency(self, architecture: Architecture, constraints: Dict) -> int:
        """
        Estimate P95 latency in milliseconds.
        
        Args:
            architecture: Architecture specification
            constraints: System constraints
            
        Returns:
            int: Estimated P95 latency in ms
        """
        base_latency = 100  # Base processing time
        
        # Model latency
        for module in architecture["modules"]:
            if module["layer"] == "Model Layer":
                component = module["component"].lower()
                if "70b" in component or "gpt-4" in component:
                    base_latency += 300  # Large models are slower
                elif "8b" in component or "fine-tuned" in component:
                    base_latency += 150  # Medium models
                else:
                    base_latency += 200  # Default
        
        # Embedding latency
        for module in architecture["modules"]:
            if module["layer"] == "Embedding Layer":
                base_latency += 50
        
        # Database/retrieval latency
        for module in architecture["modules"]:
            if module["layer"] == "Data Layer":
                component = module["component"].lower()
                if "chromadb" in component or "vector" in component:
                    base_latency += 30  # Vector search
                if "postgresql" in component or "mongodb" in component:
                    base_latency += 20  # Database query
        
        # Topology impact
        if architecture["topology"] == "parallel":
            base_latency *= 0.7  # Parallel processing is faster
        elif architecture["topology"] == "hierarchical":
            base_latency *= 1.3  # Hierarchical adds overhead
        
        # Add network latency
        base_latency += 50
        
        return int(base_latency)
    
    def _assess_risk(self, architecture: Architecture, state: MetaMindState) -> float:
        """
        Assess risk using LLM.
        
        Args:
            architecture: Architecture specification
            state: Current state
            
        Returns:
            float: Risk score (0-100, higher is better)
        """
        try:
            # Prepare architecture summary
            arch_summary = f"Template: {architecture['template']}\n"
            arch_summary += f"Topology: {architecture['topology']}\n"
            arch_summary += "Modules:\n"
            for module in architecture["modules"]:
                arch_summary += f"- {module['layer']}: {module['component']}\n"
            
            # Generate prompt
            prompt = self.risk_prompt.format(
                architecture=arch_summary,
                domain=state["domain"],
                risk_tolerance=state["constraints"]["risk_tolerance"]
            )
            
            # Get LLM response with retry
            response = invoke_llm_with_retry(
                self.llm,
                prompt,
                max_retries=3,
                timeout=60
            )
            
            # Parse response
            parsed = parse_json_with_retry(response, max_attempts=2)
            risk_score = parsed.get("risk_score", 75.0)
            
            # Ensure valid range
            return max(0.0, min(100.0, float(risk_score)))
        
        except Exception as e:
            print(f"  ⚠ Risk assessment failed: {str(e)}, using default")
            return 75.0  # Default moderate risk score
    
    def _check_compliance(self, architecture: Architecture, state: MetaMindState) -> float:
        """
        Check compliance using LLM.
        
        Args:
            architecture: Architecture specification
            state: Current state
            
        Returns:
            float: Compliance score (0-100, higher is better)
        """
        try:
            # Prepare architecture summary
            arch_summary = f"Template: {architecture['template']}\n"
            arch_summary += f"Topology: {architecture['topology']}\n"
            arch_summary += "Modules:\n"
            for module in architecture["modules"]:
                arch_summary += f"- {module['layer']}: {module['component']}\n"
            
            # Generate prompt
            prompt = self.compliance_prompt.format(
                architecture=arch_summary,
                domain=state["domain"],
                compliance_level=state["constraints"]["compliance_level"]
            )
            
            # Get LLM response with retry
            response = invoke_llm_with_retry(
                self.llm,
                prompt,
                max_retries=3,
                timeout=60
            )
            
            # Parse response
            parsed = parse_json_with_retry(response, max_attempts=2)
            compliance_score = parsed.get("compliance_score", 80.0)
            
            # Ensure valid range
            return max(0.0, min(100.0, float(compliance_score)))
        
        except Exception as e:
            print(f"  ⚠ Compliance check failed: {str(e)}, using default")
            return 80.0  # Default good compliance score
    
    def _analyze_scalability(self, architecture: Architecture, constraints: Dict) -> int:
        """
        Analyze scalability.
        
        Args:
            architecture: Architecture specification
            constraints: System constraints
            
        Returns:
            int: Maximum concurrent users supported
        """
        base_capacity = 5000  # Base capacity
        
        # Check for scalability components
        for module in architecture["modules"]:
            component = module["component"].lower()
            
            # Kubernetes adds significant scalability
            if "kubernetes" in component:
                base_capacity *= 3
            
            # Redis caching improves scalability
            if "redis" in component or "cache" in component:
                base_capacity *= 1.5
            
            # Load balancing
            if "load balanc" in component or "nginx" in component:
                base_capacity *= 1.3
        
        # Topology impact
        if architecture["topology"] == "parallel":
            base_capacity *= 1.5
        
        return int(base_capacity)
    
    def _calculate_complexity(self, architecture: Architecture) -> int:
        """
        Calculate implementation complexity (1-10 scale).
        
        Args:
            architecture: Architecture specification
            
        Returns:
            int: Complexity score (1=simplest, 10=most complex)
        """
        complexity = 3  # Base complexity
        
        # Number of modules adds complexity
        num_modules = len(architecture["modules"])
        complexity += min(3, num_modules // 3)
        
        # Topology complexity
        if architecture["topology"] == "hierarchical":
            complexity += 2
        elif architecture["topology"] == "parallel":
            complexity += 1
        
        # Specific components add complexity
        for module in architecture["modules"]:
            component = module["component"].lower()
            
            if "kubernetes" in component:
                complexity += 1
            if "multi-agent" in component or "orchestration" in component:
                complexity += 1
            if "fine-tun" in component:
                complexity += 1
        
        # Clamp to 1-10
        return max(1, min(10, complexity))
    

# Made with Bob
