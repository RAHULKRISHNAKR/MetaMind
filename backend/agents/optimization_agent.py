"""
OptimizationAgent - Select the best architecture from scored candidates

This rule-based agent selects the highest scoring architecture.
"""

from typing import Optional
from ..orchestration.state import MetaMindState, Architecture
from ..utils.logging_config import AgentLogger


class OptimizationAgent:
    """
    Rule-based agent that selects the optimal architecture.
    
    Selection criteria:
    1. Highest final score
    2. Tie-breaking by specific metrics if needed
    3. Justification generation
    """
    
    def __init__(self):
        """Initialize the OptimizationAgent."""
        self.logger = AgentLogger("OptimizationAgent")
    
    def execute(self, state: MetaMindState) -> MetaMindState:
        """
        Execute architecture selection.
        
        Args:
            state: Current MetaMind state
            
        Returns:
            MetaMindState: Updated state with selected architecture
        """
        try:
            self.logger.info("Starting architecture selection")
            candidates = state.get("candidate_architectures", [])
            
            if not candidates:
                self.logger.error("No candidate architectures to select from")
                raise ValueError("No candidate architectures to select from")
            
            # Ensure all candidates have scores
            scored_candidates = [c for c in candidates if c.get("final_score") is not None]
            
            if not scored_candidates:
                raise ValueError("No scored candidates available")
            
            # Select best architecture
            best_architecture = self._select_best(scored_candidates, state)
            
            # Update state
            state["selected_architecture"] = best_architecture
            state["selected_architecture_id"] = best_architecture["architecture_id"]
            
            # Generate selection justification
            justification = self._generate_justification(
                best_architecture,
                scored_candidates,
                state
            )
            
            self.logger.info(f"Selected architecture: {best_architecture['name']}")
            self.logger.info(f"Score: {best_architecture['final_score']:.1f}/100")
            self.logger.info(f"Template: {best_architecture['template']}")
            self.logger.info(f"Justification: {justification}")
            
            print(f"✓ Selected architecture: {best_architecture['name']}")
            print(f"  Score: {best_architecture['final_score']:.1f}/100")
            print(f"  Template: {best_architecture['template']}")
            print(f"  Justification: {justification}")
        
        except Exception as e:
            error_msg = f"OptimizationAgent failed: {str(e)}"
            self.logger.error(error_msg)
            print(f"✗ {error_msg}")
            state["errors"].append(error_msg)
        
        return state
    
    def _select_best(
        self,
        candidates: list,
        state: MetaMindState
    ) -> Architecture:
        """
        Select the best architecture from candidates.
        
        Args:
            candidates: List of scored architectures
            state: Current state
            
        Returns:
            Architecture: Best architecture
        """
        # Sort by final score (descending)
        sorted_candidates = sorted(
            candidates,
            key=lambda x: x["final_score"],
            reverse=True
        )
        
        # Check for ties (within 0.5 points)
        best_score = sorted_candidates[0]["final_score"]
        tied_candidates = [
            c for c in sorted_candidates
            if abs(c["final_score"] - best_score) < 0.5
        ]
        
        if len(tied_candidates) > 1:
            # Tie-breaking: prefer lower complexity
            tied_candidates.sort(
                key=lambda x: x.get("estimated_metrics", {}).get("complexity", 50)
            )
            state["warnings"].append(
                f"Tie detected ({len(tied_candidates)} architectures within 0.5 points), "
                "selected based on lower complexity"
            )
        
        return tied_candidates[0] if tied_candidates else sorted_candidates[0]
    
    def _generate_justification(
        self,
        selected: Architecture,
        all_candidates: list,
        state: MetaMindState
    ) -> str:
        """
        Generate justification for selection.
        
        Args:
            selected: Selected architecture
            all_candidates: All candidate architectures
            state: Current state
            
        Returns:
            str: Selection justification
        """
        score = selected["final_score"]
        metrics = selected.get("estimated_metrics", {})
        weights = state["weights"]
        
        # Find strongest metrics
        sorted_metrics = sorted(
            metrics.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        top_metrics = [m[0] for m in sorted_metrics[:2]]
        
        # Calculate score advantage
        scores = [c["final_score"] for c in all_candidates]
        avg_score = sum(scores) / len(scores)
        advantage = score - avg_score
        
        justification = (
            f"Selected for {advantage:.1f} point advantage over average. "
            f"Excels in {', '.join(top_metrics)}."
        )
        
        # Add domain-specific note
        domain = state.get("domain", "general")
        if domain == "healthcare" and metrics.get("risk", 0) >= 85:
            justification += " Strong risk management suitable for healthcare."
        elif domain == "finance" and metrics.get("latency", 0) >= 85:
            justification += " Low latency suitable for financial applications."
        elif domain == "ecommerce" and metrics.get("scalability", 0) >= 85:
            justification += " High scalability suitable for e-commerce."
        
        return justification
    
    def compare_candidates(self, state: MetaMindState) -> str:
        """
        Generate comparison summary of all candidates.
        
        Args:
            state: Current state
            
        Returns:
            str: Comparison summary
        """
        candidates = state.get("candidate_architectures", [])
        
        if not candidates:
            return "No candidates to compare"
        
        summary = "Architecture Comparison:\n\n"
        
        # Sort by score
        sorted_candidates = sorted(
            candidates,
            key=lambda x: x.get("final_score", 0),
            reverse=True
        )
        
        for i, arch in enumerate(sorted_candidates, 1):
            score = arch.get("final_score", 0)
            name = arch.get("name", "Unknown")
            template = arch.get("template", "Unknown")
            metrics = arch.get("estimated_metrics", {})
            
            summary += f"{i}. {name} (Score: {score:.1f})\n"
            summary += f"   Template: {template}\n"
            summary += f"   Metrics: "
            summary += f"Cost={metrics.get('cost', 0):.0f}, "
            summary += f"Latency={metrics.get('latency', 0):.0f}, "
            summary += f"Risk={metrics.get('risk', 0):.0f}\n\n"
        
        return summary