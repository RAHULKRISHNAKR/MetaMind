"""
IterationAgent - Apply improvements to architecture based on reflection feedback

This hybrid agent modifies architectures using rule-based improvements and LLM guidance.
"""

import copy
from typing import List
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from ..orchestration.state import MetaMindState, Architecture, ArchitectureModule


class IterationAgent:
    """
    Hybrid agent that applies improvements to architectures.
    
    Applies improvements based on:
    - Reflection feedback suggestions
    - Rule-based optimization patterns
    - LLM-guided modifications
    """
    
    def __init__(self, ollama_base_url: str = "http://localhost:11434", model_name: str = "llama3"):
        """
        Initialize the IterationAgent.
        
        Args:
            ollama_base_url: Base URL for Ollama service
            model_name: Name of the Ollama model to use
        """
        self.llm = Ollama(
            base_url=ollama_base_url,
            model=model_name,
            temperature=0.1
        )
    
    def execute(self, state: MetaMindState) -> MetaMindState:
        """
        Execute architecture improvement.
        
        Args:
            state: Current MetaMind state
            
        Returns:
            MetaMindState: Updated state with improved architecture
        """
        try:
            selected_arch = state.get("selected_architecture")
            reflection = state.get("reflection_feedback")
            
            if not selected_arch or not reflection:
                raise ValueError("Missing architecture or reflection feedback")
            
            # Get improvement suggestions
            suggestions = reflection.get("improvement_suggestions", [])
            
            if not suggestions:
                state["warnings"].append("No improvement suggestions, keeping current architecture")
                return state
            
            # Create improved architecture
            improved_arch, changes_made = self._apply_improvements(
                selected_arch,
                suggestions,
                state
            )
            
            # Update candidate architectures with improved version
            state["candidate_architectures"] = [improved_arch]
            
            # Track changes
            print(f"✓ Applied {len(changes_made)} improvements:")
            for change in changes_made:
                print(f"  - {change}")
            
            # Store changes for version history
            state["_iteration_changes"] = changes_made
        
        except Exception as e:
            error_msg = f"IterationAgent failed: {str(e)}"
            print(f"✗ {error_msg}")
            state["errors"].append(error_msg)
        
        return state
    
    def _apply_improvements(
        self,
        architecture: Architecture,
        suggestions: List[str],
        state: MetaMindState
    ) -> tuple[Architecture, List[str]]:
        """
        Apply improvements to architecture.
        
        Args:
            architecture: Current architecture
            suggestions: List of improvement suggestions
            state: Current state
            
        Returns:
            tuple: (improved_architecture, list_of_changes_made)
        """
        # Deep copy architecture to avoid modifying original
        improved = copy.deepcopy(architecture)
        improved["name"] = f"{improved['name']} (v{state['version']})"
        
        changes_made = []
        
        for suggestion in suggestions:
            suggestion_lower = suggestion.lower()
            
            # Apply rule-based improvements
            if "cach" in suggestion_lower or "redis" in suggestion_lower:
                if self._add_caching(improved):
                    changes_made.append("Added Redis caching layer")
            
            elif "smaller model" in suggestion_lower or "reduce cost" in suggestion_lower:
                if self._optimize_model_size(improved):
                    changes_made.append("Switched to smaller model")
            
            elif "latency" in suggestion_lower and "optim" in suggestion_lower:
                if self._optimize_latency(improved):
                    changes_made.append("Optimized for latency")
            
            elif "load balanc" in suggestion_lower or "scalab" in suggestion_lower:
                if self._add_load_balancing(improved):
                    changes_made.append("Added load balancing")
            
            elif "monitor" in suggestion_lower:
                if self._enhance_monitoring(improved):
                    changes_made.append("Enhanced monitoring")
            
            elif "validat" in suggestion_lower or "safety" in suggestion_lower:
                if self._add_validation(improved):
                    changes_made.append("Added validation layer")
            
            elif "compli" in suggestion_lower:
                if self._enhance_compliance(improved):
                    changes_made.append("Enhanced compliance measures")
        
        # If no changes were made, try generic optimization
        if not changes_made:
            if self._generic_optimization(improved, state):
                changes_made.append("Applied generic optimizations")
        
        return improved, changes_made
    
    def _add_caching(self, architecture: Architecture) -> bool:
        """
        Add Redis caching layer.
        
        Args:
            architecture: Architecture to modify
            
        Returns:
            bool: True if added, False if already exists
        """
        # Check if caching already exists
        for module in architecture["modules"]:
            if "redis" in module["component"].lower() or "cache" in module["component"].lower():
                return False
        
        # Add Redis to Data Layer
        cache_module = ArchitectureModule(
            layer="Data Layer",
            component="Redis Cache",
            config={"ttl": 3600, "max_memory": "2gb"}
        )
        
        # Insert after first data layer module
        for i, module in enumerate(architecture["modules"]):
            if module["layer"] == "Data Layer":
                architecture["modules"].insert(i + 1, cache_module)
                return True
        
        # If no data layer, add at beginning
        architecture["modules"].insert(0, cache_module)
        return True
    
    def _optimize_model_size(self, architecture: Architecture) -> bool:
        """
        Switch to smaller model.
        
        Args:
            architecture: Architecture to modify
            
        Returns:
            bool: True if optimized, False otherwise
        """
        for module in architecture["modules"]:
            if module["layer"] == "Model Layer":
                component = module["component"]
                
                # Switch large models to smaller ones
                if "70b" in component.lower():
                    module["component"] = component.replace("70B", "8B").replace("70b", "8b")
                    return True
                elif "gpt-4" in component.lower():
                    module["component"] = "Llama 3 8B"
                    return True
                elif "claude-3" in component.lower():
                    module["component"] = "Llama 3 8B"
                    return True
        
        return False
    
    def _optimize_latency(self, architecture: Architecture) -> bool:
        """
        Optimize for latency.
        
        Args:
            architecture: Architecture to modify
            
        Returns:
            bool: True if optimized, False otherwise
        """
        changes = False
        
        # Switch to parallel topology if sequential
        if architecture["topology"] == "sequential":
            architecture["topology"] = "parallel"
            changes = True
        
        # Add caching if not present
        if self._add_caching(architecture):
            changes = True
        
        return changes
    
    def _add_load_balancing(self, architecture: Architecture) -> bool:
        """
        Add load balancing.
        
        Args:
            architecture: Architecture to modify
            
        Returns:
            bool: True if added, False if already exists
        """
        # Check if load balancing exists
        for module in architecture["modules"]:
            if "load balanc" in module["component"].lower() or "nginx" in module["component"].lower():
                return False
        
        # Add load balancer to Deployment Layer
        lb_module = ArchitectureModule(
            layer="Deployment Layer",
            component="Nginx Load Balancer",
            config={"algorithm": "round_robin", "health_check": True}
        )
        
        # Add to deployment layer
        for i, module in enumerate(architecture["modules"]):
            if module["layer"] == "Deployment Layer":
                architecture["modules"].insert(i, lb_module)
                return True
        
        # If no deployment layer, add at end
        architecture["modules"].append(lb_module)
        return True
    
    def _enhance_monitoring(self, architecture: Architecture) -> bool:
        """
        Enhance monitoring capabilities.
        
        Args:
            architecture: Architecture to modify
            
        Returns:
            bool: True if enhanced, False otherwise
        """
        # Check current monitoring
        has_prometheus = False
        has_grafana = False
        
        for module in architecture["modules"]:
            if module["layer"] == "Monitoring Layer":
                if "prometheus" in module["component"].lower():
                    has_prometheus = True
                if "grafana" in module["component"].lower():
                    has_grafana = True
        
        changes = False
        
        # Add Prometheus if missing
        if not has_prometheus:
            prom_module = ArchitectureModule(
                layer="Monitoring Layer",
                component="Prometheus",
                config={"scrape_interval": "15s"}
            )
            architecture["modules"].append(prom_module)
            changes = True
        
        # Add Grafana if missing
        if not has_grafana:
            grafana_module = ArchitectureModule(
                layer="Monitoring Layer",
                component="Grafana",
                config={"dashboards": ["system", "application"]}
            )
            architecture["modules"].append(grafana_module)
            changes = True
        
        return changes
    
    def _add_validation(self, architecture: Architecture) -> bool:
        """
        Add validation and safety layer.
        
        Args:
            architecture: Architecture to modify
            
        Returns:
            bool: True if added, False if already exists
        """
        # Check if validation exists
        for module in architecture["modules"]:
            if module["layer"] == "Validation & Safety Layer":
                return False
        
        # Add validation modules
        validation_modules = [
            ArchitectureModule(
                layer="Validation & Safety Layer",
                component="Input Sanitization",
                config={"xss_protection": True, "sql_injection_protection": True}
            ),
            ArchitectureModule(
                layer="Validation & Safety Layer",
                component="Output Validation",
                config={"schema_validation": True, "content_filtering": True}
            )
        ]
        
        # Insert before model layer
        for i, module in enumerate(architecture["modules"]):
            if module["layer"] == "Model Layer":
                for val_module in reversed(validation_modules):
                    architecture["modules"].insert(i, val_module)
                return True
        
        # If no model layer, add at beginning
        architecture["modules"] = validation_modules + architecture["modules"]
        return True
    
    def _enhance_compliance(self, architecture: Architecture) -> bool:
        """
        Enhance compliance measures.
        
        Args:
            architecture: Architecture to modify
            
        Returns:
            bool: True if enhanced, False otherwise
        """
        changes = False
        
        # Add audit logging
        has_audit = False
        for module in architecture["modules"]:
            if "audit" in module["component"].lower() or "logging" in module["component"].lower():
                has_audit = True
                break
        
        if not has_audit:
            audit_module = ArchitectureModule(
                layer="Monitoring Layer",
                component="Audit Logging",
                config={"retention_days": 365, "encryption": True}
            )
            architecture["modules"].append(audit_module)
            changes = True
        
        # Add data encryption
        has_encryption = False
        for module in architecture["modules"]:
            if "encrypt" in module["component"].lower():
                has_encryption = True
                break
        
        if not has_encryption:
            # Add encryption config to data layer
            for module in architecture["modules"]:
                if module["layer"] == "Data Layer":
                    module["config"]["encryption_at_rest"] = True
                    module["config"]["encryption_in_transit"] = True
                    changes = True
                    break
        
        return changes
    
    def _generic_optimization(self, architecture: Architecture, state: MetaMindState) -> bool:
        """
        Apply generic optimizations based on metrics.
        
        Args:
            architecture: Architecture to modify
            state: Current state
            
        Returns:
            bool: True if optimized, False otherwise
        """
        metrics = architecture.get("estimated_metrics", {})
        
        # If cost is low, try adding caching
        if metrics.get("cost", 100) < 70:
            return self._add_caching(architecture)
        
        # If latency is low, try optimization
        if metrics.get("latency", 100) < 70:
            return self._optimize_latency(architecture)
        
        # If scalability is low, add load balancing
        if metrics.get("scalability", 100) < 70:
            return self._add_load_balancing(architecture)
        
        return False

# Made with Bob
