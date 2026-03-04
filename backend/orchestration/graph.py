"""
MetaMind LangGraph Orchestration Pipeline

This module defines the multi-agent workflow for autonomous AI pipeline design.
"""

from typing import Dict, Any
from langgraph.graph import StateGraph, END
from .state import (
    MetaMindState,
    create_initial_state,
    should_continue_iteration,
    increment_version,
    add_version_to_history
)


class MetaMindOrchestrator:
    """
    Orchestrates the MetaMind architecture design pipeline.
    
    Execution flow:
    1. RequirementAgent - Parse and structure requirements
    2. DomainWeightTuningAgent - Set optimization weights
    3. ArchitectureGenerationAgent - Generate 3-5 candidates
    4. SimulationAgent - Estimate metrics for each candidate
    5. DeterministicScoringEngine - Normalize and score
    6. OptimizationAgent - Select best architecture
    7. ReflectionAgent - Critique and assess confidence
    8. Decision: confidence >= 0.85?
       - YES → VersioningAgent → SpecGeneratorAgent → END
       - NO → IterationAgent → back to SimulationAgent
    9. ComparisonAgent - Compare versions (if multiple iterations)
    10. SpecGeneratorAgent - Generate final documentation
    """
    
    def __init__(
        self,
        ollama_base_url: str = "http://localhost:11434",
        model_name: str = "llama3",
        db_path: str = "./metamind.db"
    ):
        """
        Initialize the orchestrator with all agents.
        
        Args:
            ollama_base_url: Base URL for Ollama service
            model_name: Name of the Ollama model to use
            db_path: Path to SQLite database
        """
        self.ollama_base_url = ollama_base_url
        self.model_name = model_name
        self.db_path = db_path
        
        # Initialize agents (will be implemented in separate files)
        self._initialize_agents()
        
        # Build the graph
        self.graph = self._build_graph()
    
    def _initialize_agents(self):
        """Initialize all agent instances."""
        # Import agents (to be implemented)
        from ..agents import (
            RequirementAgent,
            DomainWeightTuningAgent,
            ArchitectureGenerationAgent,
            SimulationAgent,
            DeterministicScoringEngine,
            OptimizationAgent,
            ReflectionAgent,
            IterationAgent,
            VersioningAgent,
            ComparisonAgent,
            SpecGeneratorAgent
        )
        
        self.requirement_agent = RequirementAgent(
            ollama_base_url=self.ollama_base_url,
            model_name=self.model_name
        )
        
        self.weight_tuning_agent = DomainWeightTuningAgent()
        
        self.architecture_generation_agent = ArchitectureGenerationAgent(
            ollama_base_url=self.ollama_base_url,
            model_name=self.model_name
        )
        
        self.simulation_agent = SimulationAgent(
            ollama_base_url=self.ollama_base_url,
            model_name=self.model_name
        )
        
        self.scoring_engine = DeterministicScoringEngine()
        
        self.optimization_agent = OptimizationAgent()
        
        self.reflection_agent = ReflectionAgent(
            ollama_base_url=self.ollama_base_url,
            model_name=self.model_name
        )
        
        self.iteration_agent = IterationAgent(
            ollama_base_url=self.ollama_base_url,
            model_name=self.model_name
        )
        
        self.versioning_agent = VersioningAgent(db_path=self.db_path)
        
        self.comparison_agent = ComparisonAgent()
        
        self.spec_generator_agent = SpecGeneratorAgent(
            ollama_base_url=self.ollama_base_url,
            model_name=self.model_name
        )
    
    def _build_graph(self) -> StateGraph:
        """
        Build the LangGraph state graph with agent nodes.
        
        Returns:
            StateGraph: Compiled graph ready for execution
        """
        # Create state graph
        workflow = StateGraph(MetaMindState)
        
        # Add agent nodes
        workflow.add_node("requirement", self._requirement_node)
        workflow.add_node("weight_tuning", self._weight_tuning_node)
        workflow.add_node("architecture_generation", self._architecture_generation_node)
        workflow.add_node("simulation", self._simulation_node)
        workflow.add_node("scoring", self._scoring_node)
        workflow.add_node("optimization", self._optimization_node)
        workflow.add_node("reflection", self._reflection_node)
        workflow.add_node("iteration", self._iteration_node)
        workflow.add_node("versioning", self._versioning_node)
        workflow.add_node("comparison", self._comparison_node)
        workflow.add_node("spec_generation", self._spec_generation_node)
        
        # Define edges
        workflow.set_entry_point("requirement")
        workflow.add_edge("requirement", "weight_tuning")
        workflow.add_edge("weight_tuning", "architecture_generation")
        workflow.add_edge("architecture_generation", "simulation")
        workflow.add_edge("simulation", "scoring")
        workflow.add_edge("scoring", "optimization")
        workflow.add_edge("optimization", "reflection")
        
        # Conditional edge: iterate or finalize?
        workflow.add_conditional_edges(
            "reflection",
            self._should_iterate,
            {
                "iterate": "iteration",
                "finalize": "versioning"
            }
        )
        
        # Iteration loop
        workflow.add_edge("iteration", "simulation")
        
        # Finalization path
        workflow.add_edge("versioning", "comparison")
        workflow.add_edge("comparison", "spec_generation")
        workflow.add_edge("spec_generation", END)
        
        # Compile the graph
        return workflow.compile()
    
    def _requirement_node(self, state: MetaMindState) -> MetaMindState:
        """
        Execute RequirementAgent to parse and validate requirements.
        
        Args:
            state: Current state
            
        Returns:
            MetaMindState: Updated state
        """
        print(f"[{state['run_id']}] Executing RequirementAgent...")
        state["status"] = "parsing_requirements"
        return self.requirement_agent.execute(state)
    
    def _weight_tuning_node(self, state: MetaMindState) -> MetaMindState:
        """
        Execute DomainWeightTuningAgent to set optimization weights.
        
        Args:
            state: Current state
            
        Returns:
            MetaMindState: Updated state
        """
        print(f"[{state['run_id']}] Executing DomainWeightTuningAgent...")
        state["status"] = "tuning_weights"
        return self.weight_tuning_agent.execute(state)
    
    def _architecture_generation_node(self, state: MetaMindState) -> MetaMindState:
        """
        Execute ArchitectureGenerationAgent to create candidate architectures.
        
        Args:
            state: Current state
            
        Returns:
            MetaMindState: Updated state
        """
        print(f"[{state['run_id']}] Executing ArchitectureGenerationAgent...")
        state["status"] = "generating_architectures"
        return self.architecture_generation_agent.execute(state)
    
    def _simulation_node(self, state: MetaMindState) -> MetaMindState:
        """
        Execute SimulationAgent to estimate metrics for all candidates.
        
        Args:
            state: Current state
            
        Returns:
            MetaMindState: Updated state
        """
        print(f"[{state['run_id']}] Executing SimulationAgent...")
        state["status"] = "simulating_metrics"
        return self.simulation_agent.execute(state)
    
    def _scoring_node(self, state: MetaMindState) -> MetaMindState:
        """
        Execute DeterministicScoringEngine to normalize and score.
        
        Args:
            state: Current state
            
        Returns:
            MetaMindState: Updated state
        """
        print(f"[{state['run_id']}] Executing DeterministicScoringEngine...")
        state["status"] = "scoring_architectures"
        return self.scoring_engine.execute(state)
    
    def _optimization_node(self, state: MetaMindState) -> MetaMindState:
        """
        Execute OptimizationAgent to select best architecture.
        
        Args:
            state: Current state
            
        Returns:
            MetaMindState: Updated state
        """
        print(f"[{state['run_id']}] Executing OptimizationAgent...")
        state["status"] = "selecting_optimal"
        return self.optimization_agent.execute(state)
    
    def _reflection_node(self, state: MetaMindState) -> MetaMindState:
        """
        Execute ReflectionAgent to critique and assess confidence.
        
        Args:
            state: Current state
            
        Returns:
            MetaMindState: Updated state
        """
        print(f"[{state['run_id']}] Executing ReflectionAgent...")
        state["status"] = "reflecting"
        return self.reflection_agent.execute(state)
    
    def _should_iterate(self, state: MetaMindState) -> str:
        """
        Determine if iteration should continue or finalize.
        
        Args:
            state: Current state
            
        Returns:
            str: "iterate" or "finalize"
        """
        if should_continue_iteration(state):
            print(f"[{state['run_id']}] Confidence below threshold, iterating...")
            return "iterate"
        else:
            print(f"[{state['run_id']}] Confidence sufficient or max iterations reached, finalizing...")
            return "finalize"
    
    def _iteration_node(self, state: MetaMindState) -> MetaMindState:
        """
        Execute IterationAgent to improve architecture.
        
        Args:
            state: Current state
            
        Returns:
            MetaMindState: Updated state
        """
        print(f"[{state['run_id']}] Executing IterationAgent...")
        state["status"] = "iterating"
        
        # Increment version
        state = increment_version(state)
        
        return self.iteration_agent.execute(state)
    
    def _versioning_node(self, state: MetaMindState) -> MetaMindState:
        """
        Execute VersioningAgent to store final version.
        
        Args:
            state: Current state
            
        Returns:
            MetaMindState: Updated state
        """
        print(f"[{state['run_id']}] Executing VersioningAgent...")
        state["status"] = "versioning"
        return self.versioning_agent.execute(state)
    
    def _comparison_node(self, state: MetaMindState) -> MetaMindState:
        """
        Execute ComparisonAgent to compare versions.
        
        Args:
            state: Current state
            
        Returns:
            MetaMindState: Updated state
        """
        print(f"[{state['run_id']}] Executing ComparisonAgent...")
        state["status"] = "comparing_versions"
        return self.comparison_agent.execute(state)
    
    def _spec_generation_node(self, state: MetaMindState) -> MetaMindState:
        """
        Execute SpecGeneratorAgent to create final documentation.
        
        Args:
            state: Current state
            
        Returns:
            MetaMindState: Updated state
        """
        print(f"[{state['run_id']}] Executing SpecGeneratorAgent...")
        state["status"] = "generating_specification"
        return self.spec_generator_agent.execute(state)
    
    def design(
        self,
        business_goal: str,
        domain: str,
        modalities: list,
        constraints: Dict[str, Any],
        max_iterations: int = 5,
        progress_callback: callable = None
    ) -> Dict[str, Any]:
        """
        Run the complete architecture design pipeline.
        
        Args:
            business_goal: Clear description of system purpose
            domain: Application domain (healthcare, finance, etc.)
            modalities: Data types to handle (text, vision, etc.)
            constraints: System constraints (budget, latency, etc.)
            max_iterations: Maximum improvement iterations
            progress_callback: Optional callback function for progress updates
            
        Returns:
            Dict: Complete design results
        """
        # Create initial state
        initial_state = create_initial_state(
            business_goal=business_goal,
            domain=domain,
            modalities=modalities,
            constraints=constraints,
            max_iterations=max_iterations
        )
        
        # Store progress callback in state
        if progress_callback:
            initial_state["progress_callback"] = progress_callback
        
        # Execute the graph
        print(f"Starting MetaMind architecture design pipeline...")
        print(f"Run ID: {initial_state['run_id']}")
        print(f"Domain: {domain}")
        print(f"Business Goal: {business_goal}")
        
        if progress_callback:
            progress_callback("generation", "🎨 Generating architecture candidates...")
        
        try:
            final_state = self.graph.invoke(initial_state)
            final_state["status"] = "completed"
            print(f"Design complete! Final version: {final_state['version']}")
            
            if progress_callback:
                progress_callback("finalization", "📝 Generating documentation...")
            
            # Extract key data for API response
            selected_arch = final_state.get("selected_architecture", {})
            
            # Build clean response with score and metrics at top level
            response = {
                "run_id": final_state["run_id"],
                "version": final_state["version"],
                "selected_architecture": selected_arch,
                "score": selected_arch.get("final_score", 0.0),
                "metrics": selected_arch.get("estimated_metrics", {}),
                "reflection": final_state.get("reflection", {}),
                "executive_report": final_state.get("executive_report"),
                "technical_specification": final_state.get("technical_specification"),
                "deployment_plan": final_state.get("deployment_plan"),
                "monitoring_strategy": final_state.get("monitoring_strategy"),
                "status": "completed"
            }
            
            return response
        except Exception as e:
            print(f"Design failed: {str(e)}")
            initial_state["status"] = "failed"
            initial_state["errors"].append(str(e))
            return initial_state
    
    def get_graph_visualization(self) -> str:
        """
        Get a text representation of the graph structure.
        
        Returns:
            str: Graph visualization
        """
        return """
MetaMind Architecture Design Pipeline:

    START
      ↓
[RequirementAgent] - Parse and validate requirements
      ↓
[DomainWeightTuningAgent] - Set optimization weights
      ↓
[ArchitectureGenerationAgent] - Generate 3-5 candidates
      ↓
[SimulationAgent] - Estimate metrics
      ↓
[DeterministicScoringEngine] - Normalize and score
      ↓
[OptimizationAgent] - Select best architecture
      ↓
[ReflectionAgent] - Critique and assess confidence
      ↓
   Decision: confidence >= 0.85?
      ├─ NO → [IterationAgent] - Improve architecture
      │         ↓
      │    (loop back to SimulationAgent)
      │
      └─ YES → [VersioningAgent] - Store final version
                ↓
            [ComparisonAgent] - Compare versions
                ↓
            [SpecGeneratorAgent] - Generate documentation
                ↓
               END

Each agent updates the shared state with its results.
The pipeline recursively improves until confidence threshold is met.
"""


# Utility function for external use
def create_orchestrator(
    ollama_base_url: str = "http://localhost:11434",
    model_name: str = "llama3",
    db_path: str = "./metamind.db"
) -> MetaMindOrchestrator:
    """
    Factory function to create a MetaMind orchestrator.
    
    Args:
        ollama_base_url: Base URL for Ollama service
        model_name: Name of the Ollama model
        db_path: Path to database
        
    Returns:
        MetaMindOrchestrator: Configured orchestrator instance
    """
    return MetaMindOrchestrator(
        ollama_base_url=ollama_base_url,
        model_name=model_name,
        db_path=db_path
    )

# Made with Bob
