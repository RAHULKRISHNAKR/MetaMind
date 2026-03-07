"""
ReflectionAgent - Critique architecture and assess confidence

This LLM-based agent evaluates the selected architecture and determines if iteration is needed.
"""

import json
import time
from langchain_core.prompts import PromptTemplate
from ..orchestration.state import MetaMindState, ReflectionFeedback
from ..utils.llm_utils import create_llm_from_env, invoke_llm_with_retry, parse_json_with_retry
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
            ollama_base_url: Base URL for Ollama service (fallback if env not set)
            model_name: Name of the model to use (fallback if env not set)
        """
        # Use environment-based LLM creation for seamless provider switching (Groq priority)
        self.llm = create_llm_from_env(temperature=0.2, timeout=90)
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
        
        # Initialize logger with run_id for streaming
        if self.logger is None or self.logger.run_id != run_id:
            self.logger = AgentLogger("ReflectionAgent", run_id=run_id)
        
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
            
            # Add detailed score explanations
            reflection["score_explanations"] = self._generate_score_explanations(metrics, selected_arch.get("final_score", 0))
            
            # Add cost breakdown if available
            for sim_result in state.get("simulation_results", []):
                if sim_result["architecture_id"] == arch_id:
                    cost_breakdown = sim_result["raw_metrics"].get("cost_breakdown")
                    if cost_breakdown:
                        reflection["cost_breakdown"] = cost_breakdown
                        self.logger.info(f"Added cost breakdown to reflection: Total ${cost_breakdown['total']}/month")
                    break
            
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
        Format metrics for display with detailed explanations.
        
        Args:
            metrics: Metrics dict
            final_score: Final score
            
        Returns:
            str: Formatted metrics with context
        """
        summary = f"Final Score: {final_score:.1f}/100\n\n"
        summary += "Individual Metrics (0-100 scale, higher is better):\n\n"
        
        # Cost metric with explanation
        cost_score = metrics.get('cost', 0)
        summary += f"- Cost: {cost_score:.1f}/100\n"
        summary += f"  How calculated: Compares estimated monthly cost against budget constraint\n"
        summary += f"  What it means: {self._get_score_interpretation(cost_score)}\n"
        summary += f"  Use case: Ensures solution stays within budget while maximizing value\n\n"
        
        # Latency metric with explanation
        latency_score = metrics.get('latency', 0)
        summary += f"- Latency: {latency_score:.1f}/100\n"
        summary += f"  How calculated: Compares P95 response time against latency target\n"
        summary += f"  What it means: {self._get_score_interpretation(latency_score)}\n"
        summary += f"  Use case: Critical for real-time applications and user experience\n\n"
        
        # Risk metric with explanation
        risk_score = metrics.get('risk', 0)
        summary += f"- Risk: {risk_score:.1f}/100\n"
        summary += f"  How calculated: LLM-based assessment of security, reliability, and failure modes\n"
        summary += f"  What it means: {self._get_score_interpretation(risk_score)}\n"
        summary += f"  Use case: Ensures system resilience and data protection\n\n"
        
        # Compliance metric with explanation
        compliance_score = metrics.get('compliance', 0)
        summary += f"- Compliance: {compliance_score:.1f}/100\n"
        summary += f"  How calculated: LLM-based evaluation against regulatory requirements (GDPR, HIPAA, etc.)\n"
        summary += f"  What it means: {self._get_score_interpretation(compliance_score)}\n"
        summary += f"  Use case: Critical for regulated industries (healthcare, finance, legal)\n\n"
        
        # Scalability metric with explanation
        scalability_score = metrics.get('scalability', 0)
        summary += f"- Scalability: {scalability_score:.1f}/100\n"
        summary += f"  How calculated: Compares max concurrent users capacity against expected load\n"
        summary += f"  What it means: {self._get_score_interpretation(scalability_score)}\n"
        summary += f"  Use case: Ensures system can handle growth and traffic spikes\n\n"
        
        # Complexity metric with explanation
        complexity_score = metrics.get('complexity', 0)
        summary += f"- Complexity: {complexity_score:.1f}/100\n"
        summary += f"  How calculated: Based on number of components, topology, and integration points\n"
        summary += f"  What it means: {self._get_score_interpretation(complexity_score)}\n"
        summary += f"  Use case: Lower complexity means faster implementation and easier maintenance\n"
        
        return summary
    
    def _get_score_interpretation(self, score: float) -> str:
        """
        Get human-readable interpretation of a score.
        
        Args:
            score: Score value (0-100)
            
        Returns:
            str: Interpretation text
        """
        if score >= 90:
            return "Excellent - Exceeds requirements significantly"
        elif score >= 80:
            return "Very Good - Meets requirements with margin"
        elif score >= 70:
            return "Good - Meets requirements adequately"
        elif score >= 60:
            return "Acceptable - Meets minimum requirements"
        elif score >= 50:
            return "Below Target - May need optimization"
        else:
            return "Poor - Requires significant improvement"
    
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
            should_iterate=False)
    
    def _generate_score_explanations(self, metrics: dict, final_score: float) -> dict:
        """
        Generate detailed explanations for each metric score.
        
        Args:
            metrics: Architecture metrics
            final_score: Final weighted score
            
        Returns:
            dict: Detailed explanations for each metric
        """
        explanations = {
            "overall": {
                "score": final_score,
                "interpretation": self._get_score_interpretation(final_score),
                "description": "Weighted combination of all metrics based on domain priorities"
            },
            "cost": {
                "score": metrics.get("cost", 0),
                "interpretation": self._get_score_interpretation(metrics.get("cost", 0)),
                "how_calculated": "Compares estimated monthly operational cost against budget constraint. Includes detailed breakdown: model inference (token usage × pricing), infrastructure (databases, caching, monitoring), storage (S3, vector DBs), and networking overhead (15% of base costs).",
                "what_it_means": "Higher scores indicate better cost efficiency. Score of 100 means costs ≤70% of budget, 70-80 means within budget, below 60 means over budget. Check cost_breakdown field for detailed per-component costs.",
                "use_case": "Critical for cost-sensitive projects. Detailed breakdown helps identify optimization opportunities (e.g., switching models, reducing infrastructure, optimizing storage)."
            },
            "latency": {
                "score": metrics.get("latency", 0),
                "interpretation": self._get_score_interpretation(metrics.get("latency", 0)),
                "how_calculated": "Compares P95 response time against latency target. Factors in model inference time, database queries, network latency, and topology (parallel vs sequential).",
                "what_it_means": "Higher scores indicate faster response times. Score of 100 means significantly faster than target, 70-80 meets target, below 60 exceeds target.",
                "use_case": "Essential for real-time applications, user-facing systems, and time-sensitive operations. Directly impacts user experience."
            },
            "risk": {
                "score": metrics.get("risk", 0),
                "interpretation": self._get_score_interpretation(metrics.get("risk", 0)),
                "how_calculated": "LLM-based assessment evaluating data security, model reliability, system availability, failure modes, and operational risks. Considers validation layers, monitoring, and redundancy.",
                "what_it_means": "Higher scores indicate lower risk. Score of 100 means comprehensive risk mitigation, 70-80 means adequate safeguards, below 60 means significant vulnerabilities.",
                "use_case": "Critical for production systems handling sensitive data or mission-critical operations. Ensures system resilience and business continuity."
            },
            "compliance": {
                "score": metrics.get("compliance", 0),
                "interpretation": self._get_score_interpretation(metrics.get("compliance", 0)),
                "how_calculated": "LLM-based evaluation against regulatory requirements (GDPR, HIPAA, SOC2, etc.). Assesses data protection, audit trails, transparency, and industry-specific regulations.",
                "what_it_means": "Higher scores indicate better regulatory alignment. Score of 100 means fully compliant, 70-80 means mostly compliant with minor gaps, below 60 means significant compliance issues.",
                "use_case": "Mandatory for regulated industries (healthcare, finance, legal). Non-compliance can result in fines, legal issues, and reputational damage."
            },
            "scalability": {
                "score": metrics.get("scalability", 0),
                "interpretation": self._get_score_interpretation(metrics.get("scalability", 0)),
                "how_calculated": "Compares maximum concurrent users capacity against expected load. Considers horizontal scaling (Kubernetes), caching (Redis), load balancing, and topology.",
                "what_it_means": "Higher scores indicate better growth capacity. Score of 100 means 150%+ headroom, 70-80 means adequate capacity, below 60 means insufficient for expected load.",
                "use_case": "Important for growing businesses and applications with variable traffic. Prevents performance degradation during peak usage."
            },
            "complexity": {
                "score": metrics.get("complexity", 0),
                "interpretation": self._get_score_interpretation(metrics.get("complexity", 0)),
                "how_calculated": "Based on number of components, topology type (hierarchical adds complexity), integration points, and specialized technologies (Kubernetes, multi-agent systems).",
                "what_it_means": "Higher scores indicate simpler implementation. Score of 100 means minimal complexity, 70-80 means moderate complexity, below 60 means high complexity requiring specialized expertise.",
                "use_case": "Affects development time, maintenance costs, and team skill requirements. Simpler systems are faster to deploy and easier to debug."
            }
        }
        
        return explanations