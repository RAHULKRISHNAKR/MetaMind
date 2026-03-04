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
            logger.info(f"🚀 Starting code generation for: {project_name}")
            logger.info(f"📦 Blueprint keys: {list(architecture_blueprint.keys())}")
            logger.info(f"📦 Blueprint template field: {architecture_blueprint.get('template', 'NOT FOUND')}")
            
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
            logger.info(f"📝 Extracted config with {len(config)} parameters")
            
            # Generate files based on architecture type
            files_generated = []
            
            if arch_type == "rag_pipeline":
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
    
    def _generate_multi_agent(self, config: Dict[str, Any], output_dir: Path) -> List[str]:
        """Generate multi-agent system project files."""
        # TODO: Implement multi-agent templates
        logger.warning("⚠️ Multi-agent templates not yet implemented")
        return []
    
    def _generate_fine_tuned(self, config: Dict[str, Any], output_dir: Path) -> List[str]:
        """Generate fine-tuned model project files."""
        # TODO: Implement fine-tuned templates
        logger.warning("⚠️ Fine-tuned templates not yet implemented")
        return []
    
    def _generate_hybrid(self, config: Dict[str, Any], output_dir: Path) -> List[str]:
        """Generate hybrid architecture project files."""
        # TODO: Implement hybrid templates
        logger.warning("⚠️ Hybrid templates not yet implemented")
        return []
    
    def _generate_ensemble(self, config: Dict[str, Any], output_dir: Path) -> List[str]:
        """Generate ensemble system project files."""
        # TODO: Implement ensemble templates
        logger.warning("⚠️ Ensemble templates not yet implemented")
        return []
    
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

# Made with Bob
