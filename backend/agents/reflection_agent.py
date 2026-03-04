"""
ReflectionAgent - Critique architecture and assess confidence

This LLM-based agent evaluates the selected architecture and determines if iteration is needed.
"""

import json
import time
from langchain_core.prompts import PromptTemplate
from ..orchestration.state import MetaMindState, ReflectionFeedback
from ..utils.llm_utils import create_llm_with_retry, invoke_llm_with_retry, parse_json_with_retry
from ..utils.logging_config import AgentLogger
from ..utils.validation import ReflectionOutput


class ReflectionAgent:
    """
    LLM-based agent that critiques architectures and assesses confidence.
    
    Provides:
    - Confidence score (0.0-1.0)
    - Strength analysis
    - Weakness identification
    - Specific improvement suggestions
    - Iteration decision
    """
    
    CONFIDENCE_THRESHOLD = 0.85
    
    def __init__(self, ollama_base_url: str = "http://localhost:11434", model_name: str = "llama3"):
        """
        Initialize the ReflectionAgent.
        
        Args:
            ollama_base_url: Base URL for Ollama service
            model_name: Name of the Ollama model to use
        """
        self.llm = create_llm_with_retry(
            base_url=ollama_base_url,
            model=model_name,
            temperature=0.2,  # Moderate temperature for balanced critique
            timeout=90
        )
        self.logger = AgentLogger("ReflectionAgent")
        
        self.prompt_template = PromptTemplate(
            input_variables=["architecture", "metrics", "constraints", "domain", "business_goal"],
            template="""You are an expert AI architecture critic. Analyze this selected architecture and provide honest feedback.

Business Goal: {business_goal}
Domain: {domain}

Selected Architecture:
{architecture}

Metrics:
{metrics}

Constraints:
{constraints}

Critically analyze:
1. Does this architecture truly meet the business goal?
2. Are there any significant weaknesses or risks?
3. Could the architecture be improved?
4. Are the metrics acceptable given the constraints?
5. Is this production-ready?

Be HONEST and CRITICAL. If there are issues, identify them clearly.

Output ONLY valid JSON:
{{
    "confidence_score": <0.0-1.0, where 1.0 is complete confidence>,
    "strengths": ["strength1", "strength2", ...],
    "weaknesses": ["weakness1", "weakness2", ...],
    "improvement_suggestions": ["specific suggestion1", "specific suggestion2", ...],
    "should_iterate": <true if confidence < 0.85 or major issues found>,
    "reasoning": "Brief explanation of confidence score"
}}

Be specific in improvement suggestions. For example:
- "Add Redis caching layer to reduce latency"
- "Switch from Llama 3 70B to 8B to reduce cost"
- "Implement rate limiting for better scalability"

JSON Output:"""
        )
    
    def execute(self, state: MetaMindState) -> MetaMindState:
        """
        Execute reflection on selected architecture.
        
        Args:
            state: Current MetaMind state
            
        Returns:
            MetaMindState: Updated state with reflection feedback
        """
        start_time = time.time()
        run_id = state.get("run_id", "unknown")
        version = state.get("version", 0)
        
        try:
            self.logger.log_execution_start(run_id, version)
            
            selected_arch = state.get("selected_architecture")
            
            if not selected_arch:
                raise ValueError("No selected architecture to reflect on")
            
            # Get metrics for selected architecture
            arch_id = selected_arch["architecture_id"]
            metrics = selected_arch.get("estimated_metrics", {})
            
            # Prepare architecture summary
            arch_summary = self._format_architecture(selected_arch)
            metrics_summary = self._format_metrics(metrics, selected_arch.get("final_score", 0))
            constraints_summary = self._format_constraints(state["constraints"])
            
            # Generate prompt
            prompt = self.prompt_template.format(
                architecture=arch_summary,
                metrics=metrics_summary,
                constraints=constraints_summary,
                domain=state["domain"],
                business_goal=state["business_goal"]
            )
            
            # Get LLM response with retry
            llm_start = time.time()
            response = invoke_llm_with_retry(
                self.llm,
                prompt,
                max_retries=3,
                timeout=90
            )
            llm_duration = (time.time() - llm_start) * 1000
            self.logger.log_llm_call(run_id, len(prompt), len(response), llm_duration)
            
            # Parse reflection with retry
            parsed = parse_json_with_retry(response, max_attempts=3)
            
            # Validate with Pydantic
            reflection_validated = ReflectionOutput(**parsed)
            reflection = reflection_validated.dict()
            
            # Enhance reflection
            reflection = self._validate_reflection(reflection, metrics, state)
            
            # Update state
            state["reflection_feedback"] = reflection
            
            # Log success
            duration = (time.time() - start_time) * 1000
            details = f"Confidence: {reflection['confidence_score']:.2f}, Iterate: {reflection['should_iterate']}"
            self.logger.log_execution_success(run_id, duration, details)
            
            print(f"✓ Reflection complete:")
            print(f"  Confidence: {reflection['confidence_score']:.2f}")
            print(f"  Strengths: {len(reflection['strengths'])}")
            print(f"  Weaknesses: {len(reflection['weaknesses'])}")
            print(f"  Suggestions: {len(reflection['improvement_suggestions'])}")
            print(f"  Should iterate: {reflection['should_iterate']}")
        
        except Exception as e:
            self.logger.log_execution_failure(run_id, e)
            error_msg = f"ReflectionAgent failed: {str(e)}"
            print(f"✗ {error_msg}")
            state["errors"].append(error_msg)
            # Provide default reflection
            state["reflection_feedback"] = self._default_reflection()
        
        return state
    
    def _format_architecture(self, architecture: dict) -> str:
        """
        Format architecture for display.
        
        Args:
            architecture: Architecture dict
            
        Returns:
            str: Formatted architecture
        """
        summary = f"Name: {architecture['name']}\n"
        summary += f"Template: {architecture['template']}\n"
        summary += f"Topology: {architecture['topology']}\n\n"
        summary += "Modules:\n"
        
        for module in architecture.get("modules", []):
            summary += f"- {module['layer']}: {module['component']}\n"
        
        return summary
    
    def _format_metrics(self, metrics: dict, final_score: float) -> str:
        """
        Format metrics for display.
        
        Args:
            metrics: Metrics dict
            final_score: Final score
            
        Returns:
            str: Formatted metrics
        """
        summary = f"Final Score: {final_score:.1f}/100\n\n"
        summary += "Individual Metrics (0-100 scale):\n"
        summary += f"- Cost: {metrics.get('cost', 0):.1f}\n"
        summary += f"- Latency: {metrics.get('latency', 0):.1f}\n"
        summary += f"- Risk: {metrics.get('risk', 0):.1f}\n"
        summary += f"- Compliance: {metrics.get('compliance', 0):.1f}\n"
        summary += f"- Scalability: {metrics.get('scalability', 0):.1f}\n"
        summary += f"- Complexity: {metrics.get('complexity', 0):.1f}\n"
        
        return summary
    
    def _format_constraints(self, constraints: dict) -> str:
        """
        Format constraints for display.
        
        Args:
            constraints: Constraints dict
            
        Returns:
            str: Formatted constraints
        """
        summary = f"Budget: ${constraints['budget']}/month\n"
        summary += f"Latency Target: {constraints['latency_target_ms']}ms\n"
        summary += f"Expected Users: {constraints['expected_users']}\n"
        summary += f"Risk Tolerance: {constraints['risk_tolerance']}\n"
        summary += f"Compliance Level: {constraints['compliance_level']}\n"
        
        return summary
    
    def _validate_reflection(
        self,
        reflection: ReflectionFeedback,
        metrics: dict,
        state: MetaMindState
    ) -> ReflectionFeedback:
        """
        Validate and enhance reflection.
        
        Args:
            reflection: Parsed reflection
            metrics: Architecture metrics
            state: Current state
            
        Returns:
            ReflectionFeedback: Validated reflection
        """
        # Ensure confidence is in valid range
        confidence = max(0.0, min(1.0, reflection["confidence_score"]))
        reflection["confidence_score"] = confidence
        
        # Auto-detect weaknesses from metrics
        auto_weaknesses = []
        if metrics.get("cost", 100) < 60:
            auto_weaknesses.append("Cost exceeds budget significantly")
        if metrics.get("latency", 100) < 60:
            auto_weaknesses.append("Latency exceeds target significantly")
        if metrics.get("risk", 100) < 70:
            auto_weaknesses.append("Risk level is concerning")
        if metrics.get("compliance", 100) < 70:
            auto_weaknesses.append("Compliance gaps identified")
        
        # Add auto-detected weaknesses if not already present
        for weakness in auto_weaknesses:
            if weakness not in reflection["weaknesses"]:
                reflection["weaknesses"].append(weakness)
        
        # Auto-generate improvement suggestions based on weaknesses
        auto_suggestions = []
        if metrics.get("cost", 100) < 70:
            auto_suggestions.append("Consider switching to a smaller model to reduce cost")
        if metrics.get("latency", 100) < 70:
            auto_suggestions.append("Add caching layer to improve latency")
        if metrics.get("scalability", 100) < 70:
            auto_suggestions.append("Add load balancing and horizontal scaling")
        
        # Add auto-suggestions if not already present
        for suggestion in auto_suggestions:
            if suggestion not in reflection["improvement_suggestions"]:
                reflection["improvement_suggestions"].append(suggestion)
        
        # Determine should_iterate based on confidence and metrics
        if confidence < self.CONFIDENCE_THRESHOLD:
            reflection["should_iterate"] = True
        elif any(score < 60 for score in metrics.values()):
            reflection["should_iterate"] = True
            if confidence >= self.CONFIDENCE_THRESHOLD:
                # Lower confidence if metrics are poor
                reflection["confidence_score"] = min(confidence, 0.80)
        
        # Check iteration limit
        if state["current_iteration"] >= state["max_iterations"]:
            reflection["should_iterate"] = False
            state["warnings"].append("Max iterations reached, stopping iteration")
        
        return reflection
    
    def _default_reflection(self) -> ReflectionFeedback:
        """
        Provide default reflection when parsing fails.
        
        Returns:
            ReflectionFeedback: Default reflection
        """
        return ReflectionFeedback(
            confidence_score=0.75,
            strengths=["Architecture follows best practices"],
            weaknesses=["Unable to perform detailed analysis"],
            improvement_suggestions=["Manual review recommended"],
            should_iterate=False
        )

# Made with Bob
