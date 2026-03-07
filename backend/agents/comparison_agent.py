"""
ComparisonAgent - Compare two architecture versions

This rule-based agent analyzes differences between architecture versions.
"""

from typing import Dict, Any
from ..orchestration.state import MetaMindState
from ..utils.logging_config import AgentLogger


class ComparisonAgent:
    """
    Rule-based agent that compares architecture versions.
    
    Provides:
    - Metric delta calculation
    - Score improvement analysis
    - Change summary
    - Recommendation generation
    """
    
    def __init__(self):
        """Initialize the ComparisonAgent."""
        self.logger = AgentLogger("ComparisonAgent")
    
    def execute(self, state: MetaMindState) -> MetaMindState:
        """
        Execute version comparison.
        
        Args:
            state: Current MetaMind state
            
        Returns:
            MetaMindState: Updated state with comparison results
        """
        try:
            self.logger.info("Starting version comparison")
            iteration_history = state.get("iteration_history", [])
            
            if len(iteration_history) < 2:
                self.logger.info("Only one version exists, no comparison needed")
                print("ℹ Only one version exists, no comparison needed")
                return state
            
            # Compare all consecutive versions
            comparisons = []
            for i in range(1, len(iteration_history)):
                prev_version = iteration_history[i-1]
                curr_version = iteration_history[i]
                
                comparison = self._compare_versions(prev_version, curr_version)
                comparisons.append(comparison)
            
            # Store comparisons in state
            state["_version_comparisons"] = comparisons
            
            # Print summary
            self.logger.info(f"Compared {len(comparisons)} version transitions")
            print(f"✓ Compared {len(comparisons)} version transitions:")
            for comp in comparisons:
                v1 = comp["version_1"]
                v2 = comp["version_2"]
                delta = comp["score_delta"]
                self.logger.info(f"v{v1} → v{v2}: Score {delta:+.1f} ({comp['recommendation']})")
                print(f"  v{v1} → v{v2}: Score {delta:+.1f} ({comp['recommendation']})")
        
        except Exception as e:
            error_msg = f"ComparisonAgent failed: {str(e)}"
            self.logger.error(error_msg)
            print(f"✗ {error_msg}")
            state["errors"].append(error_msg)
        
        return state
    
    def _compare_versions(self, v1: Dict, v2: Dict) -> Dict[str, Any]:
        """
        Compare two versions.
        
        Args:
            v1: First version record
            v2: Second version record
            
        Returns:
            Dict: Comparison results
        """
        # Calculate score delta
        score_delta = v2["score"] - v1["score"]
        
        # Calculate metric deltas
        metric_deltas = {}
        for metric in ["cost", "latency", "risk", "compliance", "scalability", "complexity"]:
            v1_val = v1["metrics"].get(metric, 0)
            v2_val = v2["metrics"].get(metric, 0)
            metric_deltas[metric] = v2_val - v1_val
        
        # Identify improvements and regressions
        improvements = []
        regressions = []
        
        for metric, delta in metric_deltas.items():
            if delta > 1.0:  # Threshold for significant change
                improvements.append(f"{metric} +{delta:.1f}")
            elif delta < -1.0:
                regressions.append(f"{metric} {delta:.1f}")
        
        # Generate recommendation
        if score_delta > 2.0:
            recommendation = "Significant improvement"
        elif score_delta > 0.5:
            recommendation = "Minor improvement"
        elif score_delta > -0.5:
            recommendation = "Negligible change"
        elif score_delta > -2.0:
            recommendation = "Minor regression"
        else:
            recommendation = "Significant regression"
        
        # Create comparison summary
        comparison = {
            "version_1": v1["version"],
            "version_2": v2["version"],
            "score_delta": score_delta,
            "metric_deltas": metric_deltas,
            "improvements": improvements,
            "regressions": regressions,
            "changes_made": v2["changes_made"],
            "recommendation": recommendation
        }
        
        return comparison
    
    def compare_specific_versions(
        self,
        state: MetaMindState,
        v1_num: int,
        v2_num: int
    ) -> Dict[str, Any]:
        """
        Compare two specific versions.
        
        Args:
            state: Current state
            v1_num: First version number
            v2_num: Second version number
            
        Returns:
            Dict: Comparison results
        """
        iteration_history = state.get("iteration_history", [])
        
        # Find versions
        v1 = None
        v2 = None
        
        for version in iteration_history:
            if version["version"] == v1_num:
                v1 = version
            if version["version"] == v2_num:
                v2 = version
        
        if not v1 or not v2:
            raise ValueError(f"Version {v1_num} or {v2_num} not found")
        
        return self._compare_versions(v1, v2)
    
    def generate_comparison_report(self, comparison: Dict[str, Any]) -> str:
        """
        Generate human-readable comparison report.
        
        Args:
            comparison: Comparison results
            
        Returns:
            str: Formatted report
        """
        report = f"# Version Comparison: v{comparison['version_1']} → v{comparison['version_2']}\n\n"
        
        # Score change
        score_delta = comparison["score_delta"]
        report += f"## Overall Score Change: {score_delta:+.1f}\n"
        report += f"**Assessment**: {comparison['recommendation']}\n\n"
        
        # Metric changes
        report += "## Metric Changes\n\n"
        report += "| Metric | Change | Direction |\n"
        report += "|--------|--------|----------|\n"
        
        for metric, delta in comparison["metric_deltas"].items():
            direction = "↑" if delta > 0 else "↓" if delta < 0 else "→"
            report += f"| {metric.capitalize()} | {delta:+.1f} | {direction} |\n"
        
        # Improvements
        if comparison["improvements"]:
            report += "\n## Improvements\n\n"
            for improvement in comparison["improvements"]:
                report += f"- ✅ {improvement}\n"
        
        # Regressions
        if comparison["regressions"]:
            report += "\n## Regressions\n\n"
            for regression in comparison["regressions"]:
                report += f"- ⚠️ {regression}\n"
        
        # Changes made
        if comparison["changes_made"]:
            report += "\n## Changes Applied\n\n"
            for change in comparison["changes_made"]:
                report += f"- {change}\n"
        
        return report
    
    def get_best_version(self, state: MetaMindState) -> Dict:
        """
        Identify the best version based on score.
        
        Args:
            state: Current state
            
        Returns:
            Dict: Best version record
        """
        iteration_history = state.get("iteration_history", [])
        
        if not iteration_history:
            raise ValueError("No versions to compare")
        
        # Sort by score
        sorted_versions = sorted(
            iteration_history,
            key=lambda x: x["score"],
            reverse=True
        )
        
        return sorted_versions[0]
    
    def get_evolution_summary(self, state: MetaMindState) -> str:
        """
        Generate summary of architecture evolution.
        
        Args:
            state: Current state
            
        Returns:
            str: Evolution summary
        """
        iteration_history = state.get("iteration_history", [])
        
        if not iteration_history:
            return "No version history available"
        
        summary = f"# Architecture Evolution Summary\n\n"
        summary += f"**Total Versions**: {len(iteration_history)}\n"
        summary += f"**Domain**: {state['domain']}\n"
        summary += f"**Business Goal**: {state['business_goal']}\n\n"
        
        # Score progression
        summary += "## Score Progression\n\n"
        for version in iteration_history:
            v_num = version["version"]
            score = version["score"]
            changes = len(version["changes_made"])
            summary += f"- **v{v_num}**: Score {score:.1f} ({changes} changes)\n"
        
        # Overall improvement
        if len(iteration_history) > 1:
            first_score = iteration_history[0]["score"]
            last_score = iteration_history[-1]["score"]
            total_improvement = last_score - first_score
            
            summary += f"\n**Total Improvement**: {total_improvement:+.1f} points\n"
        
        # Best version
        best = self.get_best_version(state)
        summary += f"\n**Best Version**: v{best['version']} (Score: {best['score']:.1f})\n"
        
        return summary