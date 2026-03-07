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
            temperature=0.1
        )
        
        self.prompt_template = PromptTemplate(
            input_variables=["business_goal", "domain", "modalities", "budget", "latency", "users", "risk", "compliance", "templates"],
            template="""You are a senior AI systems architect with deep expertise in production ML pipelines, LLMOps, and enterprise AI deployments. Your task is to design 3-5 DISTINCT, production-ready AI pipeline architectures tailored to the exact constraints provided.

## CONTEXT & REQUIREMENTS

| Parameter         | Value                          |
|-------------------|-------------------------------|
| Business Goal     | {business_goal}               |
| Domain            | {domain}                      |
| Modalities        | {modalities}                  |
| Monthly Budget    | ${budget}/month               |
| Latency Target    | {latency}ms (p95)             |
| Expected Users    | {users}                       |
| Risk Tolerance    | {risk}                        |
| Compliance Level  | {compliance}                  |

## AVAILABLE TEMPLATES
{templates}

---

## ARCHITECTURE DESIGN RULES

### Diversity Requirements
Each architecture MUST differ in at least 3 of the following dimensions:
- Primary model provider (OpenAI / Anthropic / open-source / fine-tuned)
- Orchestration strategy (single-agent / multi-agent / pipeline / RAG-only)
- Deployment model (serverless / containerized / edge / managed API)
- Cost profile (premium / balanced / cost-optimized)
- Latency strategy (streaming / batch / cached / real-time)

### Budget Adherence
Explicitly map each component to a monthly cost estimate. Total must stay within ${budget}/month. Include a cost_breakdown field.

### Risk & Compliance Sensitivity
- HIGH risk or HIPAA/SOC2/GDPR compliance → mandatory guardrails, audit logging, PII redaction, output validation
- LOW risk → lighter validation stack is acceptable
- Reflect compliance posture in the Validation & Safety and Monitoring layers

### Latency Realism
- <200ms → avoid large models without caching; prefer streaming or smaller fine-tuned models
- 200–1000ms → mid-size models acceptable; caching recommended
- >1000ms → large models, agentic loops, and multi-step pipelines are viable

---

## LAYER DEFINITIONS & COMPONENT GUIDANCE

For EACH architecture, populate ALL 9 layers:

1. **Data Layer** — Storage & retrieval infrastructure  
   Examples: PostgreSQL, MongoDB, Pinecone, Weaviate, S3, Redis, Snowflake, BigQuery

2. **Preprocessing Layer** — Data ingestion, transformation, quality  
   Examples: Data Validation, PII Scrubbing, Chunking Strategy, OCR, Tokenization, Feature Engineering

3. **Embedding Layer** — Vector representation of inputs  
   Examples: text-embedding-3-small, text-embedding-3-large, Sentence Transformers (all-MiniLM), CLIP, Cohere Embed, BGE-M3

4. **Model Layer** — Core inference engine  
   Examples: GPT-4o, GPT-4o-mini, Claude 3.5 Sonnet, Claude 3 Haiku, Llama 3 70B, Mistral 7B, fine-tuned domain model, Gemini 1.5 Pro

5. **Tool Layer** — External capabilities and integrations  
   Examples: Web Search, Code Execution (E2B), SQL Query, REST API Calls, File I/O, Calculator, Knowledge Base Lookup

6. **Agent Orchestration Layer** — Control flow and reasoning strategy  
   Examples: LangGraph (stateful), CrewAI (multi-agent), AutoGen, LlamaIndex (RAG pipeline), Custom FSM, Single-shot chain

7. **Validation & Safety Layer** — Input/output guardrails  
   Examples: Prompt Injection Detection, Llama Guard, Output Schema Validation, PII Redaction, Toxicity Filter, Hallucination Scorer, Rate Limiting

8. **Monitoring Layer** — Observability and feedback  
   Examples: LangSmith, Helicone, OpenTelemetry, Prometheus + Grafana, Arize Phoenix, Custom Logging, Evals Pipeline

9. **Deployment Layer** — Runtime and serving infrastructure  
   Examples: Docker + Kubernetes, AWS Lambda, Modal, Fly.io, Azure OpenAI Managed, Vercel Edge, FastAPI + NGINX

---

## TOPOLOGY OPTIONS

- **sequential** — Layers execute one after another; simplest control flow
- **parallel** — Multiple branches run concurrently, results merged (e.g., ensemble models, multi-retriever)
- **hierarchical** — Orchestrator delegates to specialized sub-agents or pipelines
- **hybrid** — Combination (specify which stages are parallel vs sequential)

---

## OUTPUT FORMAT

Output ONLY a valid JSON array. No markdown, no explanation, no preamble. Each architecture object must follow this schema exactly:

[
  {
    "name": "Descriptive architecture name (e.g., 'Lean RAG Chatbot with Haiku')",
    "template": "Template name from provided list",
    "rationale": "2–3 sentence justification of why this architecture fits the requirements",
    "topology": "sequential | parallel | hierarchical | hybrid",
    "cost_estimate": "$XXX/month (brief breakdown)",
    "tradeoffs": {
      "strengths": ["strength 1", "strength 2"],
      "weaknesses": ["weakness 1", "weakness 2"]
    },
    "modules": [
      {
        "layer": "Data Layer",
        "component": "Component name(s)",
        "config": { "key": "value" },
        "cost_note": "~$X/month or free tier"
      },
      {
        "layer": "Preprocessing Layer",
        "component": "Component name(s)",
        "config": { "key": "value" },
        "cost_note": "~$X/month or free tier"
      },
      {
        "layer": "Embedding Layer",
        "component": "Component name(s)",
        "config": { "model": "...", "dimensions": 0 },
        "cost_note": "~$X/month"
      },
      {
        "layer": "Model Layer",
        "component": "Component name(s)",
        "config": { "model": "...", "temperature": 0.0, "max_tokens": 0 },
        "cost_note": "~$X/month"
      },
      {
        "layer": "Tool Layer",
        "component": "Component name(s)",
        "config": { "key": "value" },
        "cost_note": "~$X/month or N/A"
      },
      {
        "layer": "Agent Orchestration Layer",
        "component": "Component name(s)",
        "config": { "strategy": "...", "max_iterations": 0 },
        "cost_note": "open-source / $X/month"
      },
      {
        "layer": "Validation & Safety Layer",
        "component": "Component name(s)",
        "config": { "checks": [] },
        "cost_note": "~$X/month or open-source"
      },
      {
        "layer": "Monitoring Layer",
        "component": "Component name(s)",
        "config": { "metrics": [], "alert_thresholds": {} },
        "cost_note": "~$X/month or open-source"
      },
      {
        "layer": "Deployment Layer",
        "component": "Component name(s)",
        "config": { "replicas": 0, "autoscaling": true },
        "cost_note": "~$X/month"
      }
    ]
  }
]"""
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

"""You are an expert AI architecture designer. Generate 3-5 DISTINCT AI pipeline architectures.

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