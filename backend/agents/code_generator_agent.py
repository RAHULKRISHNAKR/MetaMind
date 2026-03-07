"""
Code Generator Agent
Generates production-ready code from architecture blueprints using Jinja2 templates.
"""

import os
import json
import zipfile
from pathlib import Path
from typing import Dict, List, Any, Optional
from jinja2 import Environment, FileSystemLoader, Template
import logging

logger = logging.getLogger(__name__)


class CodeGeneratorAgent:
    """
    Generates production-ready code from architecture blueprints.
    
    Supports multiple architecture types:
    - RAG Pipeline
    - Multi-Agent System
    - Fine-Tuned Model
    - Hybrid Architecture
    - Ensemble System
    """
    
    def __init__(self):
        """Initialize the code generator with template environment."""
        self.templates_dir = Path(__file__).parent.parent / "code_generation" / "templates"
        
        # Verify templates directory exists
        if not self.templates_dir.exists():
            raise FileNotFoundError(f"Templates directory not found: {self.templates_dir}")
        
        logger.info(f"✅ CodeGeneratorAgent initialized with templates at: {self.templates_dir}")
    
    def generate_code(
        self,
        architecture_blueprint: Dict[str, Any],
        project_name: str,
        output_dir: Optional[Path] = None
    ) -> Dict[str, Any]:
        """
        Generate production-ready code from architecture blueprint.
        
        Args:
            architecture_blueprint: The architecture design from MetaMind
            project_name: Name of the project to generate
            output_dir: Optional output directory (default: ./generated_projects/{project_name})
        
        Returns:
            Dictionary containing:
            - status: "success" or "error"
            - project_path: Path to generated project
            - files_generated: List of generated files
            - message: Status message
        """
        try:
            logger.info(f" Starting code generation for: {project_name}")
            logger.info(f"Blueprint keys: {list(architecture_blueprint.keys())}")
            logger.info(f"Blueprint template field: {architecture_blueprint.get('template', 'NOT FOUND')}")
            
            # Determine architecture type
            arch_type = self._detect_architecture_type(architecture_blueprint)
            logger.info(f"📋 Detected architecture type: {arch_type}")
            
            # Set output directory
            if output_dir is None:
                output_dir = Path("./generated_projects") / project_name.lower().replace(" ", "_")
            
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Extract configuration from blueprint
            config = self._extract_configuration(architecture_blueprint, project_name)
            logger.info(f"Extracted config with {len(config)} parameters")
            
            # Generate files based on architecture type
            files_generated = []
            
            if arch_type == "healthcare_monitoring":
                files_generated = self._generate_healthcare_monitoring(config, output_dir)
            elif arch_type == "rag_pipeline":
                files_generated = self._generate_rag_pipeline(config, output_dir)
            elif arch_type == "multi_agent":
                logger.warning(f"⚠️ Multi-agent templates not yet implemented. Falling back to RAG pipeline.")
                files_generated = self._generate_rag_pipeline(config, output_dir)
            elif arch_type == "fine_tuned":
                logger.warning(f"⚠️ Fine-tuned templates not yet implemented. Falling back to RAG pipeline.")
                files_generated = self._generate_rag_pipeline(config, output_dir)
            elif arch_type == "hybrid":
                logger.warning(f"⚠️ Hybrid templates not yet implemented. Falling back to RAG pipeline.")
                files_generated = self._generate_rag_pipeline(config, output_dir)
            elif arch_type == "ensemble":
                logger.warning(f"⚠️ Ensemble templates not yet implemented. Falling back to RAG pipeline.")
                files_generated = self._generate_rag_pipeline(config, output_dir)
            else:
                logger.warning(f"⚠️ Unknown architecture type '{arch_type}'. Falling back to RAG pipeline.")
                files_generated = self._generate_rag_pipeline(config, output_dir)
            
            logger.info(f"✅ Generated {len(files_generated)} files")
            
            return {
                "status": "success",
                "project_path": str(output_dir),
                "files_generated": files_generated,
                "architecture_type": arch_type,
                "message": f"Successfully generated {len(files_generated)} files for {project_name}"
            }
        
        except Exception as e:
            logger.error(f"❌ Code generation failed: {str(e)}")
            return {
                "status": "error",
                "message": f"Code generation failed: {str(e)}",
                "files_generated": []
            }
    
    def _detect_architecture_type(self, blueprint: Dict[str, Any]) -> str:
        """
        Detect architecture type from blueprint.
        
        Looks for keywords in template or modules to determine type.
        """
        # Check both 'template' and 'template_name' fields (for compatibility)
        template_name = blueprint.get("template", blueprint.get("template_name", "")).lower()
        modules = blueprint.get("modules", [])
        
        logger.info(f"🔍 Detecting architecture type from template: '{template_name}'")
        
        # Check for healthcare monitoring (real-time analytics with anomaly detection)
        if "real_time_analytics" in template_name or "patient_monitoring" in template_name:
            # Check if it has anomaly detection or healthcare components
            module_names = [m.get("component", "").lower() for m in modules]
            if any("anomaly" in m or "patient" in m or "vital" in m or "hipaa" in m for m in module_names):
                logger.info("✅ Detected: Healthcare Monitoring System")
                return "healthcare_monitoring"
        
        # Check template name first
        if "rag" in template_name or "retrieval" in template_name:
            logger.info("✅ Detected: RAG Pipeline")
            return "rag_pipeline"
        elif "multi-agent" in template_name or "multi_agent" in template_name:
            logger.info("✅ Detected: Multi-Agent System")
            return "multi_agent"
        elif "fine-tun" in template_name or "fine_tun" in template_name:
            logger.info("✅ Detected: Fine-Tuned Model")
            return "fine_tuned"
        elif "hybrid" in template_name:
            logger.info("✅ Detected: Hybrid Architecture")
            return "hybrid"
        elif "ensemble" in template_name:
            logger.info("✅ Detected: Ensemble System")
            return "ensemble"
        
        # Check modules for clues
        module_names = [m.get("component", "").lower() for m in modules]
        logger.info(f"🔍 Checking modules: {module_names[:3]}...")  # Log first 3 modules
        
        if any("vector" in m or "retrieval" in m or "embedding" in m for m in module_names):
            logger.info("✅ Detected from modules: RAG Pipeline")
            return "rag_pipeline"
        elif any("agent" in m for m in module_names):
            logger.info("✅ Detected from modules: Multi-Agent System")
            return "multi_agent"
        
        # Default to RAG pipeline
        logger.info("⚠️ No clear match, defaulting to RAG Pipeline")
        return "rag_pipeline"
    
    def _extract_configuration(self, blueprint: Dict[str, Any], project_name: str) -> Dict[str, Any]:
        """
        Extract configuration parameters from blueprint.
        
        Maps MetaMind blueprint to template variables.
        """
        modules = blueprint.get("modules", [])
        estimated_metrics = blueprint.get("estimated_metrics", {})
        
        # Extract LLM configuration
        llm_module = next((m for m in modules if "llm" in m.get("component", "").lower()), None)
        llm_config = llm_module.get("config", {}) if llm_module else {}
        
        # Extract embedding configuration
        embedding_module = next((m for m in modules if "embedding" in m.get("component", "").lower()), None)
        embedding_config = embedding_module.get("config", {}) if embedding_module else {}
        
        # Extract vector store configuration
        vector_module = next((m for m in modules if "vector" in m.get("component", "").lower()), None)
        vector_config = vector_module.get("config", {}) if vector_module else {}
        
        # Determine providers
        llm_provider = self._determine_provider(llm_config.get("model", "gpt-3.5-turbo"))
        embedding_provider = self._determine_provider(embedding_config.get("model", "text-embedding-ada-002"))
        
        config = {
            "project_name": project_name,
            
            # LLM Configuration
            "llm_provider": llm_provider,
            "llm_model": llm_config.get("model", "gpt-3.5-turbo"),
            "llm_class": self._get_llm_class(llm_provider),
            "temperature": llm_config.get("temperature", 0.7),
            
            # Embedding Configuration
            "embedding_provider": embedding_provider,
            "embedding_model": embedding_config.get("model", "text-embedding-ada-002"),
            "embedding_class": self._get_embedding_class(embedding_provider),
            
            # Vector Store Configuration
            "chunk_size": vector_config.get("chunk_size", 1000),
            "chunk_overlap": vector_config.get("chunk_overlap", 200),
            "retrieval_k": vector_config.get("top_k", 3),
            
            # Ollama Configuration
            "ollama_base_url": "http://localhost:11434",
            
            # Optional Features
            "include_monitoring": estimated_metrics.get("scalability", 0) > 70,
            "include_testing": True,
        }
        
        return config
    
    def _determine_provider(self, model_name: str) -> str:
        """Determine provider from model name."""
        model_lower = model_name.lower()
        
        if "gpt" in model_lower or "ada" in model_lower:
            return "openai"
        elif "claude" in model_lower:
            return "anthropic"
        elif "llama" in model_lower or "mistral" in model_lower:
            return "ollama"
        elif "sentence-transformers" in model_lower or "all-minilm" in model_lower:
            return "huggingface"
        
        return "openai"  # Default
    
    def _get_llm_class(self, provider: str) -> str:
        """Get LangChain LLM class name for provider."""
        mapping = {
            "openai": "ChatOpenAI",
            "anthropic": "ChatAnthropic",
            "ollama": "Ollama"
        }
        return mapping.get(provider, "ChatOpenAI")
    
    def _get_embedding_class(self, provider: str) -> str:
        """Get LangChain embedding class name for provider."""
        mapping = {
            "openai": "OpenAIEmbeddings",
            "huggingface": "HuggingFaceEmbeddings"
        }
        return mapping.get(provider, "OpenAIEmbeddings")
    
    def _generate_rag_pipeline(self, config: Dict[str, Any], output_dir: Path) -> List[str]:
        """Generate RAG pipeline project files."""
        template_dir = self.templates_dir / "rag_pipeline" / "python"
        
        # Verify template directory exists
        if not template_dir.exists():
            logger.error(f"❌ Template directory not found: {template_dir}")
            raise FileNotFoundError(f"Template directory not found: {template_dir}")
        
        logger.info(f"📁 Using template directory: {template_dir}")
        logger.info(f"📁 Template files available: {list(template_dir.glob('*.j2'))}")
        
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        
        files_to_generate = [
            ("main.py.j2", "main.py"),
            ("requirements.txt.j2", "requirements.txt"),
            ("Dockerfile.j2", "Dockerfile"),
            ("docker-compose.yml.j2", "docker-compose.yml"),
            (".env.j2", ".env"),
            ("README.md.j2", "README.md"),
        ]
        
        generated_files = []
        
        for template_name, output_name in files_to_generate:
            try:
                logger.info(f"📝 Rendering template: {template_name} -> {output_name}")
                template = env.get_template(template_name)
                content = template.render(**config)
                
                output_path = output_dir / output_name
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(content)
                
                generated_files.append(str(output_path))
                logger.info(f"✅ Generated: {output_name} ({len(content)} bytes)")
            
            except Exception as e:
                logger.error(f"❌ Failed to generate {output_name}: {str(e)}")
                import traceback
                logger.error(f"Traceback: {traceback.format_exc()}")
                raise
        
        logger.info(f"✅ RAG Pipeline generation complete: {len(generated_files)} files")
        return generated_files
    
    def _generate_healthcare_monitoring(self, config: Dict[str, Any], output_dir: Path) -> List[str]:
        """Generate Healthcare Monitoring System project files with proper structure."""
        template_dir = self.templates_dir / "healthcare_monitoring" / "python"
        
        # Verify template directory exists
        if not template_dir.exists():
            logger.error(f"❌ Template directory not found: {template_dir}")
            raise FileNotFoundError(f"Template directory not found: {template_dir}")
        
        logger.info(f"📁 Using template directory: {template_dir}")
        
        # Comprehensive file structure with proper organization
        files_to_generate = [
            # Root level files
            ("main.py.j2", "main.py"),
            ("requirements.txt.j2", "requirements.txt"),
            ("Dockerfile.j2", "Dockerfile"),
            ("docker-compose.yml.j2", "docker-compose.yml"),
            (".env.example.j2", ".env.example"),
            (".gitignore.j2", ".gitignore"),
            ("README.md.j2", "README.md"),
            
            # App module files (template path, output path)
            ("app/__init__.py.j2", "./app/__init__.py"),
            ("app/models.py.j2", "./app/models.py"),
            ("app/schemas.py.j2", "./app/schemas.py"),
            ("app/database.py.j2", "./app/database.py"),
        ]
        
        generated_files = []
        
        for template_name, output_name in files_to_generate:
            try:
                logger.info(f"📝 Rendering template: {template_name} -> {output_name}")
                
                # Construct full template path
                template_path = template_dir / template_name
                
                if not template_path.exists():
                    logger.warning(f"⚠️ Template not found: {template_path}, skipping...")
                    continue
                
                # Read template content directly
                template_content = template_path.read_text()
                
                # Create Jinja2 template from string
                from jinja2 import Template
                template = Template(template_content)
                content = template.render(**config)
                
                output_path = output_dir / output_name
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(content)
                
                generated_files.append(str(output_path))
                logger.info(f"✅ Generated: {output_name} ({len(content)} bytes)")
            
            except Exception as e:
                logger.error(f"❌ Failed to generate {output_name}: {str(e)}")
                import traceback
                logger.error(f"Traceback: {traceback.format_exc()}")
                # Continue with other files even if one fails
                continue
        
        logger.info(f"✅ Healthcare Monitoring generation complete: {len(generated_files)} files")
        return generated_files
    
    def _generate_multi_agent(self, config: Dict[str, Any], output_dir: Path) -> List[str]:
        """
        Generate multi-agent system project files.
        
        Creates a LangGraph-based multi-agent system with specialized agents
        for different tasks (research, analysis, synthesis).
        """
        logger.info("📦 Generating multi-agent system...")
        
        # Create multi-agent specific configuration
        multi_agent_config = {
            **config,
            "num_agents": 3,
            "agent_types": ["researcher", "analyzer", "synthesizer"],
            "orchestration_framework": "langgraph",
            "shared_memory": True,
            "agent_communication": "message_passing"
        }
        
        # Generate core files
        generated_files = []
        
        # Main application file
        main_content = self._create_multi_agent_main(multi_agent_config)
        main_path = output_dir / "main.py"
        main_path.write_text(main_content)
        generated_files.append(str(main_path))
        logger.info("✅ Generated main.py")
        
        # Agent definitions
        agents_dir = output_dir / "agents"
        agents_dir.mkdir(exist_ok=True)
        
        for agent_type in multi_agent_config["agent_types"]:
            agent_content = self._create_agent_file(agent_type, multi_agent_config)
            agent_path = agents_dir / f"{agent_type}_agent.py"
            agent_path.write_text(agent_content)
            generated_files.append(str(agent_path))
            logger.info(f"✅ Generated {agent_type}_agent.py")
        
        # Graph orchestration
        graph_content = self._create_agent_graph(multi_agent_config)
        graph_path = output_dir / "graph.py"
        graph_path.write_text(graph_content)
        generated_files.append(str(graph_path))
        logger.info("✅ Generated graph.py")
        
        # Common files
        generated_files.extend(self._generate_common_files(multi_agent_config, output_dir))
        
        logger.info(f"✅ Multi-agent system generation complete: {len(generated_files)} files")
        return generated_files
    
    def _generate_fine_tuned(self, config: Dict[str, Any], output_dir: Path) -> List[str]:
        """
        Generate fine-tuned model project files.
        
        Creates a project structure for fine-tuning and deploying a custom model,
        including training scripts, evaluation, and inference endpoints.
        """
        logger.info("📦 Generating fine-tuned model project...")
        
        # Create fine-tuning specific configuration
        fine_tune_config = {
            **config,
            "base_model": config.get("llm_model", "llama-3-8b"),
            "training_data_format": "jsonl",
            "lora_rank": 8,
            "lora_alpha": 16,
            "learning_rate": 2e-4,
            "num_epochs": 3,
            "batch_size": 4
        }
        
        generated_files = []
        
        # Training script
        train_content = self._create_training_script(fine_tune_config)
        train_path = output_dir / "train.py"
        train_path.write_text(train_content)
        generated_files.append(str(train_path))
        logger.info("✅ Generated train.py")
        
        # Evaluation script
        eval_content = self._create_evaluation_script(fine_tune_config)
        eval_path = output_dir / "evaluate.py"
        eval_path.write_text(eval_content)
        generated_files.append(str(eval_path))
        logger.info("✅ Generated evaluate.py")
        
        # Inference server
        inference_content = self._create_inference_server(fine_tune_config)
        inference_path = output_dir / "inference.py"
        inference_path.write_text(inference_content)
        generated_files.append(str(inference_path))
        logger.info("✅ Generated inference.py")
        
        # Data preparation script
        data_prep_content = self._create_data_prep_script(fine_tune_config)
        data_prep_path = output_dir / "prepare_data.py"
        data_prep_path.write_text(data_prep_content)
        generated_files.append(str(data_prep_path))
        logger.info("✅ Generated prepare_data.py")
        
        # Common files
        generated_files.extend(self._generate_common_files(fine_tune_config, output_dir))
        
        logger.info(f"✅ Fine-tuned model project generation complete: {len(generated_files)} files")
        return generated_files
    
    def _generate_hybrid(self, config: Dict[str, Any], output_dir: Path) -> List[str]:
        """
        Generate hybrid architecture project files.
        
        Creates a system that combines multiple approaches (RAG + fine-tuned model,
        or rule-based + LLM, etc.) with intelligent routing.
        """
        logger.info("📦 Generating hybrid architecture...")
        
        # Create hybrid specific configuration
        hybrid_config = {
            **config,
            "primary_approach": "rag",
            "secondary_approach": "fine_tuned",
            "routing_strategy": "confidence_based",
            "fallback_enabled": True,
            "confidence_threshold": 0.7
        }
        
        generated_files = []
        
        # Router component
        router_content = self._create_router(hybrid_config)
        router_path = output_dir / "router.py"
        router_path.write_text(router_content)
        generated_files.append(str(router_path))
        logger.info("✅ Generated router.py")
        
        # RAG component
        rag_content = self._create_rag_component(hybrid_config)
        rag_path = output_dir / "rag_component.py"
        rag_path.write_text(rag_content)
        generated_files.append(str(rag_path))
        logger.info("✅ Generated rag_component.py")
        
        # Fine-tuned model component
        ft_content = self._create_finetuned_component(hybrid_config)
        ft_path = output_dir / "finetuned_component.py"
        ft_path.write_text(ft_content)
        generated_files.append(str(ft_path))
        logger.info("✅ Generated finetuned_component.py")
        
        # Main orchestrator
        main_content = self._create_hybrid_main(hybrid_config)
        main_path = output_dir / "main.py"
        main_path.write_text(main_content)
        generated_files.append(str(main_path))
        logger.info("✅ Generated main.py")
        
        # Common files
        generated_files.extend(self._generate_common_files(hybrid_config, output_dir))
        
        logger.info(f"✅ Hybrid architecture generation complete: {len(generated_files)} files")
        return generated_files
    
    def _generate_ensemble(self, config: Dict[str, Any], output_dir: Path) -> List[str]:
        """
        Generate ensemble system project files.
        
        Creates a system that runs multiple models in parallel and combines
        their outputs using voting, averaging, or learned aggregation.
        """
        logger.info("📦 Generating ensemble system...")
        
        # Create ensemble specific configuration
        ensemble_config = {
            **config,
            "models": [
                {"name": "gpt-3.5-turbo", "weight": 0.4},
                {"name": "llama-3-8b", "weight": 0.3},
                {"name": "claude-3-haiku", "weight": 0.3}
            ],
            "aggregation_strategy": "weighted_average",
            "parallel_execution": True,
            "timeout_per_model": 30
        }
        
        generated_files = []
        
        # Ensemble orchestrator
        orchestrator_content = self._create_ensemble_orchestrator(ensemble_config)
        orchestrator_path = output_dir / "ensemble.py"
        orchestrator_path.write_text(orchestrator_content)
        generated_files.append(str(orchestrator_path))
        logger.info("✅ Generated ensemble.py")
        
        # Model wrappers
        wrappers_dir = output_dir / "model_wrappers"
        wrappers_dir.mkdir(exist_ok=True)
        
        for model_info in ensemble_config["models"]:
            wrapper_content = self._create_model_wrapper(model_info, ensemble_config)
            wrapper_path = wrappers_dir / f"{model_info['name'].replace('-', '_')}_wrapper.py"
            wrapper_path.write_text(wrapper_content)
            generated_files.append(str(wrapper_path))
            logger.info(f"✅ Generated {model_info['name']}_wrapper.py")
        
        # Aggregator
        aggregator_content = self._create_aggregator(ensemble_config)
        aggregator_path = output_dir / "aggregator.py"
        aggregator_path.write_text(aggregator_content)
        generated_files.append(str(aggregator_path))
        logger.info("✅ Generated aggregator.py")
        
        # Main application
        main_content = self._create_ensemble_main(ensemble_config)
        main_path = output_dir / "main.py"
        main_path.write_text(main_content)
        generated_files.append(str(main_path))
        logger.info("✅ Generated main.py")
        
        # Common files
        generated_files.extend(self._generate_common_files(ensemble_config, output_dir))
        
        logger.info(f"✅ Ensemble system generation complete: {len(generated_files)} files")
        return generated_files
    
    def _generate_common_files(self, config: Dict[str, Any], output_dir: Path) -> List[str]:
        """Generate common files needed by all project types."""
        generated_files = []
        
        # Requirements.txt
        requirements_content = self._create_requirements(config)
        req_path = output_dir / "requirements.txt"
        req_path.write_text(requirements_content)
        generated_files.append(str(req_path))
        
        # Dockerfile
        dockerfile_content = self._create_dockerfile(config)
        docker_path = output_dir / "Dockerfile"
        docker_path.write_text(dockerfile_content)
        generated_files.append(str(docker_path))
        
        # docker-compose.yml
        compose_content = self._create_docker_compose(config)
        compose_path = output_dir / "docker-compose.yml"
        compose_path.write_text(compose_content)
        generated_files.append(str(compose_path))
        
        # .env.example
        env_content = self._create_env_file(config)
        env_path = output_dir / ".env.example"
        env_path.write_text(env_content)
        generated_files.append(str(env_path))
        
        # README.md
        readme_content = self._create_readme(config)
        readme_path = output_dir / "README.md"
        readme_path.write_text(readme_content)
        generated_files.append(str(readme_path))
        
        return generated_files
    
    # Multi-Agent Helper Methods
    def _create_multi_agent_main(self, config: Dict[str, Any]) -> str:
        """Create main.py for multi-agent system."""
        return f'''"""
{config['project_name']} - Multi-Agent System
Generated by MetaMind
"""

from graph import create_agent_graph
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="{config['project_name']}")

class QueryRequest(BaseModel):
    query: str
    context: dict = {{}}

@app.post("/query")
async def process_query(request: QueryRequest):
    """Process query through multi-agent system."""
    try:
        graph = create_agent_graph()
        result = graph.invoke({{"query": request.query, "context": request.context}})
        return {{"status": "success", "result": result}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {{"status": "healthy"}}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    
    def _create_agent_file(self, agent_type: str, config: Dict[str, Any]) -> str:
        """Create individual agent file."""
        return f'''"""
{agent_type.capitalize()} Agent
"""

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os

class {agent_type.capitalize()}Agent:
    """Agent specialized in {agent_type} tasks."""
    
    def __init__(self):
        self.llm = ChatGroq(
            model="{config.get('llm_model', 'llama-3-8b')}",
            temperature={config.get('temperature', 0.7)},
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a {agent_type} agent. Your role is to {{role_description}}."),
            ("user", "{{input}}")
        ])
    
    def execute(self, input_data: dict) -> dict:
        """Execute agent task."""
        chain = self.prompt | self.llm
        result = chain.invoke(input_data)
        return {{"output": result.content, "agent": "{agent_type}"}}
'''
    
    def _create_agent_graph(self, config: Dict[str, Any]) -> str:
        """Create LangGraph orchestration."""
        return f'''"""
Multi-Agent Graph Orchestration
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from agents.researcher_agent import ResearcherAgent
from agents.analyzer_agent import AnalyzerAgent
from agents.synthesizer_agent import SynthesizerAgent

class AgentState(TypedDict):
    query: str
    context: dict
    research_results: List[str]
    analysis: str
    final_output: str

def create_agent_graph():
    """Create and compile the agent graph."""
    workflow = StateGraph(AgentState)
    
    # Initialize agents
    researcher = ResearcherAgent()
    analyzer = AnalyzerAgent()
    synthesizer = SynthesizerAgent()
    
    # Define nodes
    def research_node(state):
        result = researcher.execute({{"input": state["query"]}})
        state["research_results"] = [result["output"]]
        return state
    
    def analyze_node(state):
        result = analyzer.execute({{"input": state["research_results"]}})
        state["analysis"] = result["output"]
        return state
    
    def synthesize_node(state):
        result = synthesizer.execute({{"input": state["analysis"]}})
        state["final_output"] = result["output"]
        return state
    
    # Add nodes
    workflow.add_node("research", research_node)
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("synthesize", synthesize_node)
    
    # Define edges
    workflow.set_entry_point("research")
    workflow.add_edge("research", "analyze")
    workflow.add_edge("analyze", "synthesize")
    workflow.add_edge("synthesize", END)
    
    return workflow.compile()
'''
    
    # Fine-Tuned Helper Methods
    def _create_training_script(self, config: Dict[str, Any]) -> str:
        """Create training script for fine-tuning."""
        return f'''"""
Model Fine-Tuning Script
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import load_dataset
import os

def train_model():
    """Fine-tune model with LoRA."""
    # Load base model
    model_name = "{config['base_model']}"
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        load_in_8bit=True,
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Prepare for training
    model = prepare_model_for_kbit_training(model)
    
    # LoRA configuration
    lora_config = LoraConfig(
        r={config['lora_rank']},
        lora_alpha={config['lora_alpha']},
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    
    model = get_peft_model(model, lora_config)
    
    # Load training data
    dataset = load_dataset("json", data_files="training_data.jsonl")
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir="./checkpoints",
        num_train_epochs={config['num_epochs']},
        per_device_train_batch_size={config['batch_size']},
        learning_rate={config['learning_rate']},
        logging_steps=10,
        save_steps=100,
        evaluation_strategy="steps",
        eval_steps=100
    )
    
    # Train
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"],
        eval_dataset=dataset.get("validation")
    )
    
    trainer.train()
    model.save_pretrained("./fine_tuned_model")
    tokenizer.save_pretrained("./fine_tuned_model")
    print("✅ Training complete!")

if __name__ == "__main__":
    train_model()
'''
    
    def _create_evaluation_script(self, config: Dict[str, Any]) -> str:
        """Create evaluation script."""
        return f'''"""
Model Evaluation Script
"""

from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset
import torch
from tqdm import tqdm

def evaluate_model():
    """Evaluate fine-tuned model."""
    model = AutoModelForCausalLM.from_pretrained("./fine_tuned_model")
    tokenizer = AutoTokenizer.from_pretrained("./fine_tuned_model")
    
    # Load test data
    test_data = load_dataset("json", data_files="test_data.jsonl")
    
    correct = 0
    total = 0
    
    for example in tqdm(test_data["train"]):
        inputs = tokenizer(example["input"], return_tensors="pt")
        outputs = model.generate(**inputs, max_length=100)
        prediction = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        if prediction.strip() == example["expected_output"].strip():
            correct += 1
        total += 1
    
    accuracy = correct / total
    print(f"Accuracy: {{accuracy:.2%}}")
    return accuracy

if __name__ == "__main__":
    evaluate_model()
'''
    
    def _create_inference_server(self, config: Dict[str, Any]) -> str:
        """Create inference server."""
        return f'''"""
Inference Server for Fine-Tuned Model
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import uvicorn

app = FastAPI(title="{config['project_name']} Inference")

# Load model at startup
model = None
tokenizer = None

@app.on_event("startup")
async def load_model():
    global model, tokenizer
    model = AutoModelForCausalLM.from_pretrained("./fine_tuned_model")
    tokenizer = AutoTokenizer.from_pretrained("./fine_tuned_model")

class InferenceRequest(BaseModel):
    prompt: str
    max_length: int = 100

@app.post("/generate")
async def generate(request: InferenceRequest):
    """Generate text from fine-tuned model."""
    try:
        inputs = tokenizer(request.prompt, return_tensors="pt")
        outputs = model.generate(**inputs, max_length=request.max_length)
        text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {{"generated_text": text}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    
    def _create_data_prep_script(self, config: Dict[str, Any]) -> str:
        """Create data preparation script."""
        return f'''"""
Data Preparation Script
"""

import json
from pathlib import Path

def prepare_training_data():
    """Prepare data in JSONL format for fine-tuning."""
    # Example: Convert your data to training format
    training_data = []
    
    # Add your data processing logic here
    # Example format:
    examples = [
        {{"input": "Question: What is AI?", "output": "AI is artificial intelligence..."}},
        # Add more examples
    ]
    
    # Save as JSONL
    with open("training_data.jsonl", "w") as f:
        for example in examples:
            f.write(json.dumps(example) + "\\n")
    
    print(f"✅ Prepared {{len(examples)}} training examples")

if __name__ == "__main__":
    prepare_training_data()
'''
    
    # Hybrid Helper Methods
    def _create_router(self, config: Dict[str, Any]) -> str:
        """Create intelligent router for hybrid system."""
        return f'''"""
Intelligent Router for Hybrid Architecture
"""

class HybridRouter:
    """Routes queries to appropriate component based on confidence."""
    
    def __init__(self, confidence_threshold={config['confidence_threshold']}):
        self.threshold = confidence_threshold
    
    def route(self, query: str, rag_confidence: float, ft_confidence: float) -> str:
        """Determine which component to use."""
        if rag_confidence > self.threshold and rag_confidence > ft_confidence:
            return "rag"
        elif ft_confidence > self.threshold:
            return "fine_tuned"
        else:
            return "ensemble"  # Use both and combine
    
    def should_fallback(self, primary_result: dict) -> bool:
        """Check if fallback is needed."""
        return primary_result.get("confidence", 0) < self.threshold
'''
    
    def _create_rag_component(self, config: Dict[str, Any]) -> str:
        """Create RAG component."""
        return f'''"""
RAG Component
"""

from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

class RAGComponent:
    """Retrieval-Augmented Generation component."""
    
    def __init__(self):
        self.llm = ChatGroq(
            model="{config.get('llm_model', 'llama-3-8b')}",
            api_key=os.getenv("GROQ_API_KEY")
        )
        self.embeddings = HuggingFaceEmbeddings()
        self.vectorstore = Chroma(embedding_function=self.embeddings)
    
    def query(self, question: str) -> dict:
        """Process query with RAG."""
        docs = self.vectorstore.similarity_search(question, k=3)
        context = "\\n".join([doc.page_content for doc in docs])
        
        prompt = f"Context: {{context}}\\n\\nQuestion: {{question}}\\n\\nAnswer:"
        response = self.llm.invoke(prompt)
        
        return {{
            "answer": response.content,
            "confidence": 0.85,  # Calculate actual confidence
            "source": "rag"
        }}
'''
    
    def _create_finetuned_component(self, config: Dict[str, Any]) -> str:
        """Create fine-tuned model component."""
        return f'''"""
Fine-Tuned Model Component
"""

from transformers import AutoModelForCausalLM, AutoTokenizer

class FineTunedComponent:
    """Fine-tuned model component."""
    
    def __init__(self):
        self.model = AutoModelForCausalLM.from_pretrained("./fine_tuned_model")
        self.tokenizer = AutoTokenizer.from_pretrained("./fine_tuned_model")
    
    def query(self, question: str) -> dict:
        """Process query with fine-tuned model."""
        inputs = self.tokenizer(question, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_length=200)
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return {{
            "answer": answer,
            "confidence": 0.90,  # Calculate actual confidence
            "source": "fine_tuned"
        }}
'''
    
    def _create_hybrid_main(self, config: Dict[str, Any]) -> str:
        """Create main file for hybrid system."""
        return f'''"""
{config['project_name']} - Hybrid Architecture
"""

from fastapi import FastAPI
from pydantic import BaseModel
from router import HybridRouter
from rag_component import RAGComponent
from finetuned_component import FineTunedComponent
import uvicorn

app = FastAPI(title="{config['project_name']}")

# Initialize components
router = HybridRouter()
rag = RAGComponent()
ft = FineTunedComponent()

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def process_query(request: QueryRequest):
    """Process query through hybrid system."""
    # Get predictions from both
    rag_result = rag.query(request.query)
    ft_result = ft.query(request.query)
    
    # Route to best component
    selected = router.route(
        request.query,
        rag_result["confidence"],
        ft_result["confidence"]
    )
    
    if selected == "rag":
        return rag_result
    elif selected == "fine_tuned":
        return ft_result
    else:
        # Ensemble both results
        return {{
            "answer": f"RAG: {{rag_result['answer']}}\\n\\nFT: {{ft_result['answer']}}",
            "confidence": (rag_result["confidence"] + ft_result["confidence"]) / 2,
            "source": "ensemble"
        }}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    
    # Ensemble Helper Methods
    def _create_ensemble_orchestrator(self, config: Dict[str, Any]) -> str:
        """Create ensemble orchestrator."""
        return f'''"""
Ensemble Orchestrator
"""

import asyncio
from typing import List, Dict
from aggregator import Aggregator

class EnsembleOrchestrator:
    """Orchestrates multiple models and aggregates results."""
    
    def __init__(self, models: List[Dict], aggregator: Aggregator):
        self.models = models
        self.aggregator = aggregator
    
    async def query_all_models(self, prompt: str) -> List[Dict]:
        """Query all models in parallel."""
        tasks = [self._query_model(model, prompt) for model in self.models]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out errors
        valid_results = [r for r in results if not isinstance(r, Exception)]
        return valid_results
    
    async def _query_model(self, model: Dict, prompt: str) -> Dict:
        """Query a single model."""
        # Import appropriate wrapper
        wrapper_name = model["name"].replace("-", "_")
        module = __import__(f"model_wrappers.{{wrapper_name}}_wrapper", fromlist=["ModelWrapper"])
        wrapper = module.ModelWrapper()
        
        result = await wrapper.query(prompt)
        result["weight"] = model["weight"]
        return result
    
    async def process(self, prompt: str) -> Dict:
        """Process prompt through ensemble."""
        results = await self.query_all_models(prompt)
        aggregated = self.aggregator.aggregate(results)
        return aggregated
'''
    
    def _create_model_wrapper(self, model_info: Dict, config: Dict[str, Any]) -> str:
        """Create model wrapper."""
        model_name = model_info['name']
        return f'''"""
Wrapper for {model_name}
"""

import os
from langchain_groq import ChatGroq

class ModelWrapper:
    """Wrapper for {model_name}."""
    
    def __init__(self):
        self.llm = ChatGroq(
            model="{model_name}",
            api_key=os.getenv("GROQ_API_KEY")
        )
    
    async def query(self, prompt: str) -> dict:
        """Query the model."""
        response = self.llm.invoke(prompt)
        return {{
            "model": "{model_name}",
            "response": response.content,
            "confidence": 0.85
        }}
'''
    
    def _create_aggregator(self, config: Dict[str, Any]) -> str:
        """Create result aggregator."""
        return f'''"""
Result Aggregator
"""

from typing import List, Dict

class Aggregator:
    """Aggregates results from multiple models."""
    
    def __init__(self, strategy="{config['aggregation_strategy']}"):
        self.strategy = strategy
    
    def aggregate(self, results: List[Dict]) -> Dict:
        """Aggregate multiple model results."""
        if self.strategy == "weighted_average":
            return self._weighted_average(results)
        elif self.strategy == "voting":
            return self._voting(results)
        else:
            return self._simple_average(results)
    
    def _weighted_average(self, results: List[Dict]) -> Dict:
        """Weighted average aggregation."""
        total_weight = sum(r["weight"] for r in results)
        
        # Combine responses with weights
        combined = ""
        for result in results:
            weight_pct = result["weight"] / total_weight
            combined += f"[{{result['model']}} ({{weight_pct:.0%}})]: {{result['response']}}\\n\\n"
        
        return {{
            "aggregated_response": combined,
            "models_used": [r["model"] for r in results],
            "strategy": "weighted_average"
        }}
    
    def _voting(self, results: List[Dict]) -> Dict:
        """Majority voting aggregation."""
        # Simple implementation - can be enhanced
        return results[0] if results else {{}}
    
    def _simple_average(self, results: List[Dict]) -> Dict:
        """Simple average aggregation."""
        combined = "\\n\\n".join([r["response"] for r in results])
        return {{
            "aggregated_response": combined,
            "models_used": [r["model"] for r in results],
            "strategy": "simple_average"
        }}
'''
    
    def _create_ensemble_main(self, config: Dict[str, Any]) -> str:
        """Create main file for ensemble system."""
        return f'''"""
{config['project_name']} - Ensemble System
"""

from fastapi import FastAPI
from pydantic import BaseModel
from ensemble import EnsembleOrchestrator
from aggregator import Aggregator
import uvicorn

app = FastAPI(title="{config['project_name']}")

# Initialize ensemble
models = {config['models']}
aggregator = Aggregator()
ensemble = EnsembleOrchestrator(models, aggregator)

class QueryRequest(BaseModel):
    prompt: str

@app.post("/query")
async def process_query(request: QueryRequest):
    """Process query through ensemble."""
    result = await ensemble.process(request.prompt)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    
    # Common file generators
    def _create_requirements(self, config: Dict[str, Any]) -> str:
        """Create requirements.txt."""
        return """fastapi==0.104.1
uvicorn==0.24.0
langchain==0.1.0
langchain-groq==0.0.1
langchain-community==0.0.10
transformers==4.36.0
torch==2.1.0
peft==0.7.0
datasets==2.15.0
chromadb==0.4.18
sentence-transformers==2.2.2
pydantic==2.5.0
python-dotenv==1.0.0
"""
    
    def _create_dockerfile(self, config: Dict[str, Any]) -> str:
        """Create Dockerfile."""
        return f"""FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
"""
    
    def _create_docker_compose(self, config: Dict[str, Any]) -> str:
        """Create docker-compose.yml."""
        return f"""version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GROQ_API_KEY=${{GROQ_API_KEY}}
    volumes:
      - ./data:/app/data
"""
    
    def _create_env_file(self, config: Dict[str, Any]) -> str:
        """Create .env.example."""
        return """# API Keys
GROQ_API_KEY=your_groq_api_key_here

# Model Configuration
MODEL_NAME=llama-3-8b
TEMPERATURE=0.7

# Application Settings
PORT=8000
"""
    
    def _create_readme(self, config: Dict[str, Any]) -> str:
        """Create README.md."""
        return f"""# {config['project_name']}

Generated by MetaMind - Autonomous AI Pipeline Designer

## Overview

This project implements a production-ready AI system based on the architecture designed by MetaMind.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Run the application:
```bash
python main.py
```

## Docker Deployment

```bash
docker-compose up --build
```

## API Endpoints

- `POST /query` - Process queries
- `GET /health` - Health check

## Architecture

This system uses {config.get('project_name', 'advanced AI architecture')} with the following components:

- LLM Provider: {config.get('llm_provider', 'Groq')}
- Model: {config.get('llm_model', 'llama-3-8b')}
- Temperature: {config.get('temperature', 0.7)}

## Generated by MetaMind

This code was automatically generated based on your requirements and constraints.
"""
    
    def create_zip_archive(self, project_path: Path, output_path: Optional[Path] = None) -> Path:
        """
        Create a ZIP archive of the generated project.
        
        Args:
            project_path: Path to the generated project
            output_path: Optional output path for ZIP file
        
        Returns:
            Path to the created ZIP file
        """
        if output_path is None:
            output_path = project_path.parent / f"{project_path.name}.zip"
        
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in project_path.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(project_path.parent)
                    zipf.write(file_path, arcname)
        
        logger.info(f"✅ Created ZIP archive: {output_path}")
        return output_path


# Example usage
if __name__ == "__main__":
    # Test code generation
    generator = CodeGeneratorAgent()
    
    # Sample blueprint
    blueprint = {
        "template_name": "LLM + RAG Pipeline",
        "modules": [
            {
                "layer": "Data Ingestion",
                "component": "Vector Store",
                "config": {
                    "chunk_size": 1000,
                    "chunk_overlap": 200,
                    "top_k": 3
                }
            },
            {
                "layer": "Model",
                "component": "LLM",
                "config": {
                    "model": "gpt-3.5-turbo",
                    "temperature": 0.7
                }
            },
            {
                "layer": "Model",
                "component": "Embeddings",
                "config": {
                    "model": "text-embedding-ada-002"
                }
            }
        ],
        "estimated_metrics": {
            "accuracy": 85,
            "latency": 75,
            "cost": 60,
            "scalability": 80
        }
    }
    
    result = generator.generate_code(
        architecture_blueprint=blueprint,
        project_name="My RAG Pipeline"
    )
    
    print(json.dumps(result, indent=2))