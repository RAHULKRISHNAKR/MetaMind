"""
ArchitectureGenerationAgent - Generate candidate AI pipeline architectures

This LLM-based agent creates 3-5 distinct architecture candidates using predefined templates.
"""

import json
import uuid
from typing import List
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from ..orchestration.state import (
    MetaMindState,
    Architecture,
    ArchitectureModule,
    ARCHITECTURE_TEMPLATES
)
from .architecture_components import validate_component, get_default_component


class ArchitectureGenerationAgent:
    """
    LLM-based agent that generates candidate architectures.
    
    Uses predefined templates and modules to create 3-5 distinct
    architecture candidates tailored to requirements.
    """
    
    def __init__(self, ollama_base_url: str = "http://localhost:11434", model_name: str = "llama3"):
        """
        Initialize the ArchitectureGenerationAgent.
        
        Args:
            ollama_base_url: Base URL for Ollama service
            model_name: Name of the Ollama model to use
        """
        self.llm = Ollama(
            base_url=ollama_base_url,
            model=model_name,
            temperature=0.7  # Higher temperature for diversity
        )
        
        self.prompt_template = PromptTemplate(
            input_variables=["business_goal", "domain", "modalities", "budget", "latency", "users", "risk", "compliance", "templates"],
            template="""You are an expert AI architecture designer. Generate 3-5 DISTINCT AI pipeline architectures.

Requirements:
- Business Goal: {business_goal}
- Domain: {domain}
- Modalities: {modalities}
- Budget: ${budget}/month
- Latency Target: {latency}ms
- Expected Users: {users}
- Risk Tolerance: {risk}
- Compliance Level: {compliance}

Available Templates:
{templates}

For EACH architecture (generate 3-5), provide:
1. Unique name (descriptive)
2. Template used (from list above)
3. Modules for each layer:
   - Data Layer (e.g., PostgreSQL, MongoDB, S3, Redis)
   - Preprocessing Layer (e.g., Data Validation, Cleaning, Feature Engineering)
   - Embedding Layer (e.g., Sentence Transformers, OpenAI Embeddings, CLIP)
   - Model Layer (e.g., Llama 3 8B, GPT-4, Claude, Fine-tuned model)
   - Tool Layer (e.g., Web Search, Code Execution, Database Query)
   - Agent Orchestration Layer (e.g., LangGraph, CrewAI, Custom)
   - Validation & Safety Layer (e.g., Input Sanitization, Output Validation)
   - Monitoring Layer (e.g., Prometheus, OpenTelemetry, Logging)
   - Deployment Layer (e.g., Docker, Kubernetes, API Gateway)
4. Topology (sequential, parallel, or hierarchical)

Make architectures DIVERSE - vary models, components, and approaches.

Output ONLY valid JSON array:
[
  {{
    "name": "Architecture name",
    "template": "Template name",
    "modules": [
      {{
        "layer": "Data Layer",
        "component": "PostgreSQL + Redis",
        "config": {{"connection_pool": 20}}
      }},
      ...
    ],
    "topology": "sequential"
  }},
  ...
]

JSON Output:"""
        )
    
    def execute(self, state: MetaMindState) -> MetaMindState:
        """
        Execute architecture generation.
        
        Args:
            state: Current MetaMind state
            
        Returns:
            MetaMindState: Updated state with candidate architectures
        """
        try:
            # Prepare templates list
            templates_str = "\n".join([f"- {t}" for t in ARCHITECTURE_TEMPLATES])
            
            # Extract constraint values
            constraints = state["constraints"]
            
            # Generate prompt
            prompt = self.prompt_template.format(
                business_goal=state["business_goal"],
                domain=state["domain"],
                modalities=", ".join(state["modalities"]),
                budget=constraints.get("budget", 10000),
                latency=constraints.get("latency_target_ms", 500),
                users=constraints.get("expected_users", 10000),
                risk=constraints.get("risk_tolerance", "medium"),
                compliance=constraints.get("compliance_level", "medium"),
                templates=templates_str
            )
            
            # Get LLM response
            response = self.llm.invoke(prompt)
            
            # Parse architectures
            architectures = self._parse_architectures(response)
            
            # Validate and enhance architectures
            architectures = self._validate_architectures(architectures, state)
            
            # Ensure diversity
            architectures = self._ensure_diversity(architectures)
            
            # Limit to 3-5 candidates
            if len(architectures) > 5:
                architectures = architectures[:5]
            elif len(architectures) < 3:
                # Generate more if needed
                state["warnings"].append(f"Only {len(architectures)} architectures generated, expected 3-5")
            
            # Update state
            state["candidate_architectures"] = architectures
            
            print(f"✓ Generated {len(architectures)} candidate architectures:")
            for i, arch in enumerate(architectures, 1):
                print(f"  {i}. {arch['name']} ({arch['template']})")
        
        except Exception as e:
            error_msg = f"ArchitectureGenerationAgent failed: {str(e)}"
            print(f"✗ {error_msg}")
            state["errors"].append(error_msg)
            # Generate fallback architectures
            state["candidate_architectures"] = self._generate_fallback_architectures(state)
        
        return state
    
    def _parse_architectures(self, response: str) -> List[Architecture]:
        """
        Parse LLM response into Architecture objects.
        
        Args:
            response: Raw LLM response
            
        Returns:
            List[Architecture]: Parsed architectures
        """
        try:
            # Find JSON array
            start = response.find("[")
            end = response.rfind("]") + 1
            
            if start == -1 or end == 0:
                raise ValueError("No JSON array found in response")
            
            json_str = response[start:end]
            parsed = json.loads(json_str)
            
            # Convert to Architecture objects
            architectures = []
            for arch_data in parsed:
                architecture = Architecture(
                    architecture_id=str(uuid.uuid4()),
                    name=arch_data.get("name", "Unnamed Architecture"),
                    template=arch_data.get("template", "General Pipeline"),
                    modules=[
                        ArchitectureModule(**module)
                        for module in arch_data.get("modules", [])
                    ],
                    topology=arch_data.get("topology", "sequential"),
                    estimated_metrics=None,
                    final_score=None
                )
                architectures.append(architecture)
            
            return architectures
        
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in LLM response: {str(e)}")
    
    def _validate_architectures(
        self,
        architectures: List[Architecture],
        state: MetaMindState
    ) -> List[Architecture]:
        """
        Validate and enhance architectures.
        
        Args:
            architectures: List of architectures
            state: Current state
            
        Returns:
            List[Architecture]: Validated architectures
        """
        validated = []
        
        for arch in architectures:
            # Ensure template is valid
            if arch["template"] not in ARCHITECTURE_TEMPLATES:
                state["warnings"].append(
                    f"Invalid template '{arch['template']}', using 'LLM + RAG Pipeline'"
                )
                arch["template"] = "LLM + RAG Pipeline"
            
            # Ensure topology is valid
            if arch["topology"] not in ["sequential", "parallel", "hierarchical"]:
                arch["topology"] = "sequential"
            
            # Ensure modules exist
            if not arch["modules"] or len(arch["modules"]) == 0:
                # Add default modules
                arch["modules"] = self._get_default_modules(arch["template"])
            
            # Validate each module component
            for module in arch["modules"]:
                is_valid, message = validate_component(module["layer"], module["component"])
                if not is_valid:
                    state["warnings"].append(message)
                    # Replace with default component
                    module["component"] = get_default_component(module["layer"])
            
            validated.append(arch)
        
        return validated
    
    def _ensure_diversity(self, architectures: List[Architecture]) -> List[Architecture]:
        """
        Ensure architectures are diverse.
        
        Args:
            architectures: List of architectures
            
        Returns:
            List[Architecture]: Diverse architectures
        """
        # Check for duplicate templates
        templates_used = {}
        diverse_archs = []
        
        for arch in architectures:
            template = arch["template"]
            if template not in templates_used:
                templates_used[template] = 0
            
            # Allow max 2 architectures per template
            if templates_used[template] < 2:
                templates_used[template] += 1
                diverse_archs.append(arch)
        
        return diverse_archs
    
    def _get_default_modules(self, template: str) -> List[ArchitectureModule]:
        """
        Get default modules for a template.
        
        Args:
            template: Template name
            
        Returns:
            List[ArchitectureModule]: Default modules
        """
        if template == "LLM + RAG Pipeline":
            return [
                ArchitectureModule(
                    layer="Data Layer",
                    component="PostgreSQL + ChromaDB",
                    config={"connection_pool": 20}
                ),
                ArchitectureModule(
                    layer="Embedding Layer",
                    component="Sentence Transformers",
                    config={"model": "all-MiniLM-L6-v2"}
                ),
                ArchitectureModule(
                    layer="Model Layer",
                    component="Llama 3 8B",
                    config={"temperature": 0.7, "max_tokens": 512}
                ),
                ArchitectureModule(
                    layer="Monitoring Layer",
                    component="Prometheus + Grafana",
                    config={}
                ),
                ArchitectureModule(
                    layer="Deployment Layer",
                    component="Docker + Kubernetes",
                    config={}
                )
            ]
        else:
            # Generic default
            return [
                ArchitectureModule(
                    layer="Data Layer",
                    component="PostgreSQL",
                    config={}
                ),
                ArchitectureModule(
                    layer="Model Layer",
                    component="Llama 3 8B",
                    config={}
                ),
                ArchitectureModule(
                    layer="Deployment Layer",
                    component="Docker",
                    config={}
                )
            ]
    
    def _generate_fallback_architectures(self, state: MetaMindState) -> List[Architecture]:
        """
        Generate fallback architectures when LLM fails.
        
        Args:
            state: Current state
            
        Returns:
            List[Architecture]: Fallback architectures
        """
        print("⚠ Generating fallback architectures...")
        
        fallback_archs = []
        
        # Architecture 1: Simple RAG
        fallback_archs.append(Architecture(
            architecture_id=str(uuid.uuid4()),
            name="Simple RAG Pipeline",
            template="LLM + RAG Pipeline",
            modules=self._get_default_modules("LLM + RAG Pipeline"),
            topology="sequential",
            estimated_metrics=None,
            final_score=None
        ))
        
        # Architecture 2: Multi-Agent
        fallback_archs.append(Architecture(
            architecture_id=str(uuid.uuid4()),
            name="Multi-Agent System",
            template="Multi-Agent LLM System",
            modules=[
                ArchitectureModule(
                    layer="Data Layer",
                    component="PostgreSQL",
                    config={}
                ),
                ArchitectureModule(
                    layer="Agent Orchestration Layer",
                    component="LangGraph",
                    config={"num_agents": 3}
                ),
                ArchitectureModule(
                    layer="Model Layer",
                    component="Llama 3 8B",
                    config={}
                ),
                ArchitectureModule(
                    layer="Deployment Layer",
                    component="Docker",
                    config={}
                )
            ],
            topology="hierarchical",
            estimated_metrics=None,
            final_score=None
        ))
        
        # Architecture 3: Compact Model
        fallback_archs.append(Architecture(
            architecture_id=str(uuid.uuid4()),
            name="Fine-Tuned Compact Model",
            template="Fine-Tuned Compact Model Pipeline",
            modules=[
                ArchitectureModule(
                    layer="Data Layer",
                    component="SQLite",
                    config={}
                ),
                ArchitectureModule(
                    layer="Model Layer",
                    component="Fine-tuned Llama 3 8B",
                    config={"quantization": "4-bit"}
                ),
                ArchitectureModule(
                    layer="Deployment Layer",
                    component="Docker",
                    config={}
                )
            ],
            topology="sequential",
            estimated_metrics=None,
            final_score=None
        ))
        
        return fallback_archs

# Made with Bob
