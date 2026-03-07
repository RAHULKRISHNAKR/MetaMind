"""
DomainWeightTuningAgent - Map domain to optimization weights

This rule-based agent assigns optimization weights based on the application domain.
"""

from typing import Dict
from ..orchestration.state import MetaMindState, Weights
from ..utils.logging_config import AgentLogger


class DomainWeightTuningAgent:
    """
    Rule-based agent that sets optimization weights based on domain.
    
    Different domains have different priorities:
    - Healthcare: Risk and compliance are critical
    - Finance: Latency, risk, and compliance are critical
    - E-commerce: Cost, latency, and scalability are important
    - Education: Cost is very important
    - General: Balanced weights
    """
    
    # Domain-specific weight mappings
    DOMAIN_WEIGHTS: Dict[str, Weights] = {
        "healthcare": Weights(
            cost=0.10,
            latency=0.15,
            risk=0.30,       # Critical
            compliance=0.30,  # Critical
            scalability=0.10,
            complexity=0.05
        ),
        "finance": Weights(
            cost=0.15,
            latency=0.25,     # Critical
            risk=0.25,        # Critical
            compliance=0.25,  # Critical
            scalability=0.05,
            complexity=0.05
        ),
        "ecommerce": Weights(
            cost=0.25,        # Important
            latency=0.25,     # Important
            risk=0.10,
            compliance=0.10,
            scalability=0.20,  # Important
            complexity=0.10
        ),
        "education": Weights(
            cost=0.30,        # Very important
            latency=0.15,
            risk=0.15,
            compliance=0.15,
            scalability=0.15,
            complexity=0.10
        ),
        "legal": Weights(
            cost=0.10,
            latency=0.15,
            risk=0.25,        # Critical
            compliance=0.35,  # Most critical
            scalability=0.10,
            complexity=0.05
        ),
        "general": Weights(
            cost=0.20,
            latency=0.20,
            risk=0.15,
            compliance=0.15,
            scalability=0.15,
            complexity=0.15
        )
    }
    
    def __init__(self):
        """Initialize the DomainWeightTuningAgent."""
        self.logger = AgentLogger("DomainWeightTuningAgent")
    
    def execute(self, state: MetaMindState) -> MetaMindState:
        """
        Execute weight tuning based on domain.
        
        Args:
            state: Current MetaMind state
            
        Returns:
            MetaMindState: Updated state with domain-specific weights
        """
        try:
            self.logger.info("Starting domain weight tuning")
            domain = state.get("domain", "general").lower()
            
            # Get weights for domain
            if domain in self.DOMAIN_WEIGHTS:
                weights = self.DOMAIN_WEIGHTS[domain]
                self.logger.info(f"Applied {domain} domain weights")
            else:
                weights = self.DOMAIN_WEIGHTS["general"]
                warning = f"Unknown domain '{domain}', using general weights"
                self.logger.warning(warning)
                state["warnings"].append(warning)
            
            # Update state with weights
            state["weights"] = weights
            
            # Validate weights sum to 1.0
            weight_sum = sum([
                weights["cost"],
                weights["latency"],
                weights["risk"],
                weights["compliance"],
                weights["scalability"],
                weights["complexity"]
            ])
            
            if abs(weight_sum - 1.0) > 0.01:
                error_msg = f"Weights sum to {weight_sum}, expected 1.0"
                self.logger.error(error_msg)
                state["errors"].append(error_msg)
                print(f"✗ {error_msg}")
            else:
                self.logger.info(f"Weights validated: sum={weight_sum:.3f}")
                print(f"✓ Weights tuned for {domain} domain:")
                print(f"  Cost: {weights['cost']:.0%}, Latency: {weights['latency']:.0%}, "
                      f"Risk: {weights['risk']:.0%}, Compliance: {weights['compliance']:.0%}, "
                      f"Scalability: {weights['scalability']:.0%}, Complexity: {weights['complexity']:.0%}")
        
        except Exception as e:
            error_msg = f"DomainWeightTuningAgent failed: {str(e)}"
            self.logger.error(error_msg)
            print(f"✗ {error_msg}")
            state["errors"].append(error_msg)
            # Apply default weights on failure
            state["weights"] = self.DOMAIN_WEIGHTS["general"]
        
        return state
    
    def get_weight_explanation(self, domain: str) -> str:
        """
        Get explanation for why weights are set for a domain.
        
        Args:
            domain: Domain name
            
        Returns:
            str: Explanation of weight priorities
        """
        explanations = {
            "healthcare": "Healthcare prioritizes risk management (30%) and regulatory compliance (30%) "
                         "due to patient safety and HIPAA requirements. Cost and latency are secondary.",
            
            "finance": "Finance balances latency (25%), risk (25%), and compliance (25%) equally "
                      "due to real-time trading needs, fraud prevention, and regulatory requirements.",
            
            "ecommerce": "E-commerce prioritizes cost efficiency (25%), low latency (25%), and "
                        "scalability (20%) to handle traffic spikes and maintain profitability.",
            
            "education": "Education prioritizes cost efficiency (30%) to make solutions accessible, "
                        "with balanced attention to other factors.",
            
            "legal": "Legal prioritizes compliance (35%) above all due to regulatory requirements, "
                    "with significant attention to risk management (25%).",
            
            "general": "General domain uses balanced weights (15-20% each) suitable for most applications."
        }
        
        return explanations.get(domain.lower(), explanations["general"])
    
    def customize_weights(
        self,
        state: MetaMindState,
        custom_weights: Dict[str, float]
    ) -> MetaMindState:
        """
        Allow custom weight override (advanced feature).
        
        Args:
            state: Current state
            custom_weights: Custom weight values
            
        Returns:
            MetaMindState: Updated state with custom weights
        """
        try:
            # Validate custom weights
            required_keys = ["cost", "latency", "risk", "compliance", "scalability", "complexity"]
            
            for key in required_keys:
                if key not in custom_weights:
                    raise ValueError(f"Missing weight: {key}")
            
            # Check sum
            weight_sum = sum(custom_weights.values())
            if abs(weight_sum - 1.0) > 0.01:
                raise ValueError(f"Weights must sum to 1.0, got {weight_sum}")
            
            # Apply custom weights
            state["weights"] = Weights(**custom_weights)
            state["warnings"].append("Using custom weights instead of domain defaults")
            
            print("✓ Custom weights applied")
        
        except Exception as e:
            error_msg = f"Failed to apply custom weights: {str(e)}"
            print(f"✗ {error_msg}")
            state["errors"].append(error_msg)
        
        return state