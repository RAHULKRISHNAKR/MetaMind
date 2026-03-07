"""
DeterministicScoringEngine - Normalize metrics and compute weighted scores

This rule-based engine provides reproducible, explainable scoring.
"""

from typing import Dict, List
from ..orchestration.state import (
    MetaMindState,
    Architecture,
    RawMetrics,
    NormalizedScores,
    SimulationResult
)
from ..utils.logging_config import AgentLogger


class DeterministicScoringEngine:
    """
    Rule-based scoring engine that normalizes metrics and computes final scores.
    
    All scoring is deterministic and reproducible:
    - Metrics normalized to 0-100 scale
    - Weighted sum based on domain priorities
    - Clear normalization curves
    """
    
    def __init__(self):
        """Initialize the DeterministicScoringEngine."""
        self.logger = AgentLogger("DeterministicScoringEngine")
    
    def execute(self, state: MetaMindState) -> MetaMindState:
        """
        Execute scoring for all simulated architectures.
        
        Args:
            state: Current MetaMind state
            
        Returns:
            MetaMindState: Updated state with normalized scores and final scores
        """
        try:
            self.logger.info("Starting deterministic scoring")
            simulation_results = state.get("simulation_results", [])
            
            if not simulation_results:
                self.logger.error("No simulation results to score")
                raise ValueError("No simulation results to score")
            
            constraints = state["constraints"]
            weights = state["weights"]
            
            # Score each architecture
            scored_results = []
            for sim_result in simulation_results:
                # Normalize metrics
                normalized = self._normalize_metrics(
                    sim_result["raw_metrics"],
                    constraints
                )
                
                # Calculate final score
                final_score = self._calculate_final_score(normalized, weights)
                
                # Update simulation result
                sim_result["normalized_scores"] = normalized
                sim_result["final_score"] = final_score
                
                scored_results.append(sim_result)
            
            # Update state
            state["simulation_results"] = scored_results
            
            # Update candidate architectures with scores
            for arch in state["candidate_architectures"]:
                arch_id = arch["architecture_id"]
                # Find matching simulation result
                for sim_result in scored_results:
                    if sim_result["architecture_id"] == arch_id:
                        arch["estimated_metrics"] = sim_result["normalized_scores"]
                        arch["final_score"] = sim_result["final_score"]
                        break
            
            self.logger.info(f"Scored {len(scored_results)} architectures")
            print(f"✓ Scored {len(scored_results)} architectures")
            for i, result in enumerate(scored_results, 1):
                score = result['final_score']
                self.logger.info(f"Architecture {i}: Score = {score:.1f}")
                print(f"  Architecture {i}: Score = {score:.1f}")
        
        except Exception as e:
            error_msg = f"DeterministicScoringEngine failed: {str(e)}"
            self.logger.error(error_msg)
            print(f"✗ {error_msg}")
            state["errors"].append(error_msg)
        
        return state
    
    def _normalize_metrics(
        self,
        raw_metrics: RawMetrics,
        constraints: Dict
    ) -> NormalizedScores:
        """
        Normalize raw metrics to 0-100 scale.
        
        Args:
            raw_metrics: Raw simulation metrics
            constraints: System constraints
            
        Returns:
            NormalizedScores: Normalized scores (0-100)
        """
        return NormalizedScores(
            cost=self._normalize_cost(
                raw_metrics["estimated_monthly_cost"],
                constraints["budget"]
            ),
            latency=self._normalize_latency(
                raw_metrics["p95_latency_ms"],
                constraints["latency_target_ms"]
            ),
            risk=raw_metrics["risk_score"],  # Already 0-100
            compliance=raw_metrics["compliance_score"],  # Already 0-100
            scalability=self._normalize_scalability(
                raw_metrics["max_concurrent_users"],
                constraints["expected_users"]
            ),
            complexity=self._normalize_complexity(
                raw_metrics["implementation_complexity"]
            )
        )
    
    def _normalize_cost(self, actual_cost: float, budget: float) -> float:
        """
        Normalize cost metric (lower is better).
        
        Scoring curve:
        - <= 70% of budget: 100 points
        - 70-100% of budget: 100-70 points (linear)
        - > budget: 70-0 points (linear decay)
        
        Args:
            actual_cost: Estimated monthly cost
            budget: Budget constraint
            
        Returns:
            float: Normalized score (0-100)
        """
        if actual_cost <= budget * 0.7:
            return 100.0
        elif actual_cost <= budget:
            # Linear interpolation between 100 and 70
            ratio = (actual_cost - budget * 0.7) / (budget * 0.3)
            return 100.0 - (ratio * 30.0)
        else:
            # Linear decay from 70 to 0
            overage_ratio = (actual_cost - budget) / budget
            score = max(0.0, 70.0 - (overage_ratio * 70.0))
            return score
    
    def _normalize_latency(self, actual_latency: int, target_latency: int) -> float:
        """
        Normalize latency metric (lower is better).
        
        Scoring curve:
        - <= 80% of target: 100 points
        - 80-100% of target: 100-80 points (linear)
        - > target: 80-0 points (linear decay)
        
        Args:
            actual_latency: P95 latency in ms
            target_latency: Target latency in ms
            
        Returns:
            float: Normalized score (0-100)
        """
        if actual_latency <= target_latency * 0.8:
            return 100.0
        elif actual_latency <= target_latency:
            # Linear interpolation between 100 and 80
            ratio = (actual_latency - target_latency * 0.8) / (target_latency * 0.2)
            return 100.0 - (ratio * 20.0)
        else:
            # Linear decay from 80 to 0
            overage_ratio = (actual_latency - target_latency) / target_latency
            score = max(0.0, 80.0 - (overage_ratio * 80.0))
            return score
    
    def _normalize_scalability(self, max_users: int, expected_users: int) -> float:
        """
        Normalize scalability metric (higher is better).
        
        Scoring curve:
        - >= 150% of expected: 100 points
        - 100-150% of expected: 80-100 points (linear)
        - < 100% of expected: 0-80 points (linear)
        
        Args:
            max_users: Maximum concurrent users supported
            expected_users: Expected concurrent users
            
        Returns:
            float: Normalized score (0-100)
        """
        if max_users >= expected_users * 1.5:
            return 100.0
        elif max_users >= expected_users:
            # Linear interpolation between 80 and 100
            ratio = (max_users - expected_users) / (expected_users * 0.5)
            return 80.0 + (ratio * 20.0)
        else:
            # Linear interpolation between 0 and 80
            ratio = max_users / expected_users
            return ratio * 80.0
    
    def _normalize_complexity(self, complexity: int) -> float:
        """
        Normalize complexity metric (lower is better).
        
        Complexity is on 1-10 scale:
        - 1 (simplest): 100 points
        - 10 (most complex): 0 points
        - Linear interpolation
        
        Args:
            complexity: Implementation complexity (1-10)
            
        Returns:
            float: Normalized score (0-100)
        """
        # Clamp to valid range
        complexity = max(1, min(10, complexity))
        
        # Linear mapping: 1 -> 100, 10 -> 0
        return 100.0 - ((complexity - 1) * 11.11)
    
    def _calculate_final_score(
        self,
        normalized: NormalizedScores,
        weights: Dict[str, float]
    ) -> float:
        """
        Calculate weighted final score.
        
        Args:
            normalized: Normalized scores (0-100)
            weights: Optimization weights
            
        Returns:
            float: Final weighted score (0-100)
        """
        final_score = (
            normalized["cost"] * weights["cost"] +
            normalized["latency"] * weights["latency"] +
            normalized["risk"] * weights["risk"] +
            normalized["compliance"] * weights["compliance"] +
            normalized["scalability"] * weights["scalability"] +
            normalized["complexity"] * weights["complexity"]
        )
        
        # Ensure score is in valid range
        return max(0.0, min(100.0, final_score))
    
    def explain_score(
        self,
        normalized: NormalizedScores,
        weights: Dict[str, float],
        final_score: float
    ) -> str:
        """
        Generate human-readable explanation of score.
        
        Args:
            normalized: Normalized scores
            weights: Optimization weights
            final_score: Final weighted score
            
        Returns:
            str: Score explanation
        """
        contributions = {
            "cost": normalized["cost"] * weights["cost"],
            "latency": normalized["latency"] * weights["latency"],
            "risk": normalized["risk"] * weights["risk"],
            "compliance": normalized["compliance"] * weights["compliance"],
            "scalability": normalized["scalability"] * weights["scalability"],
            "complexity": normalized["complexity"] * weights["complexity"]
        }
        
        # Sort by contribution
        sorted_contrib = sorted(
            contributions.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        explanation = f"Final Score: {final_score:.1f}/100\n\n"
        explanation += "Score Breakdown:\n"
        
        for metric, contribution in sorted_contrib:
            weight = weights[metric]
            score = normalized[metric]
            explanation += f"  {metric.capitalize()}: {score:.1f} × {weight:.0%} = {contribution:.1f}\n"
        
        # Identify strengths and weaknesses
        strengths = [m for m, s in normalized.items() if s >= 80]
        weaknesses = [m for m, s in normalized.items() if s < 60]
        
        if strengths:
            explanation += f"\nStrengths: {', '.join(strengths)}"
        if weaknesses:
            explanation += f"\nWeaknesses: {', '.join(weaknesses)}"
        
        return explanation