"""
SpecGeneratorAgent - Generate comprehensive architecture documentation

This LLM-based agent creates production-ready specifications and reports.
"""

from langchain_core.prompts import PromptTemplate
from ..orchestration.state import MetaMindState
from ..utils.llm_utils import create_llm_with_retry, invoke_llm_with_retry
from ..utils.logging_config import AgentLogger


class SpecGeneratorAgent:
    """
    LLM-based agent that generates comprehensive documentation.
    
    Generates:
    - Executive summary
    - Technical specification
    - Deployment plan
    - Monitoring strategy
    """
    
    def __init__(self, ollama_base_url: str = "http://localhost:11434", model_name: str = "llama3"):
        """
        Initialize the SpecGeneratorAgent.
        
        Args:
            ollama_base_url: Base URL for Ollama service
            model_name: Name of the Ollama model to use
        """
        self.llm = create_llm_with_retry(
            base_url=ollama_base_url,
            model=model_name,
            temperature=0.2,  # Moderate temperature for creative but structured output
            timeout=120  # Longer timeout for documentation generation
        )
        self.logger = AgentLogger("SpecGeneratorAgent")
        
        self.exec_summary_prompt = PromptTemplate(
            input_variables=["business_goal", "domain", "architecture", "metrics", "iterations"],
            template="""Generate an executive summary for this AI architecture design.

Business Goal: {business_goal}
Domain: {domain}
Iterations: {iterations}

Selected Architecture:
{architecture}

Performance Metrics:
{metrics}

Write a 2-3 paragraph executive summary for stakeholders that:
1. Explains what was designed and why
2. Highlights key performance metrics
3. Addresses business value and ROI
4. Mentions any trade-offs made

Use clear, non-technical language suitable for executives.

Executive Summary:"""
        )
        
        self.tech_spec_prompt = PromptTemplate(
            input_variables=["architecture", "metrics", "domain"],
            template="""Generate a detailed technical specification for this AI architecture.

Architecture:
{architecture}

Metrics:
{metrics}

Domain: {domain}

Create a comprehensive technical specification including:
1. Architecture Overview
2. Component Breakdown (for each module)
3. Data Flow
4. Technology Stack
5. Scalability Considerations
6. Security Measures
7. Performance Characteristics
8. Integration Points

Use markdown format with clear sections and technical details.

Technical Specification:"""
        )
        
        self.deployment_prompt = PromptTemplate(
            input_variables=["architecture", "domain"],
            template="""Generate a step-by-step deployment plan for this AI architecture.

Architecture:
{architecture}

Domain: {domain}

Create a deployment plan including:
1. Prerequisites
2. Infrastructure Setup
3. Component Deployment Steps
4. Configuration
5. Testing & Validation
6. Go-Live Checklist
7. Rollback Plan

Use markdown format with numbered steps.

Deployment Plan:"""
        )
        
        self.monitoring_prompt = PromptTemplate(
            input_variables=["architecture", "metrics"],
            template="""Generate a monitoring strategy for this AI architecture.

Architecture:
{architecture}

Key Metrics:
{metrics}

Create a monitoring strategy including:
1. Key Performance Indicators (KPIs)
2. Metrics to Track
3. Alerting Rules
4. Dashboard Requirements
5. Log Aggregation
6. Health Checks
7. Incident Response

Use markdown format.

Monitoring Strategy:"""
        )
    
    def execute(self, state: MetaMindState) -> MetaMindState:
        """
        Execute specification generation.
        
        Args:
            state: Current MetaMind state
            
        Returns:
            MetaMindState: Updated state with generated specifications
        """
        try:
            self.logger.info("Starting specification generation")
            selected_arch = state.get("selected_architecture")
            
            if not selected_arch:
                self.logger.error("No selected architecture to document")
                raise ValueError("No selected architecture to document")
            
            # Generate executive summary
            self.logger.info("Generating executive summary")
            print("  Generating executive summary...")
            exec_summary = self._generate_executive_summary(state)
            state["executive_report"] = exec_summary
            
            # Generate technical specification
            self.logger.info("Generating technical specification")
            print("  Generating technical specification...")
            tech_spec = self._generate_technical_spec(state)
            state["technical_specification"] = tech_spec
            
            # Generate deployment plan
            self.logger.info("Generating deployment plan")
            print("  Generating deployment plan...")
            deployment = self._generate_deployment_plan(state)
            state["deployment_plan"] = deployment
            
            # Generate monitoring strategy
            self.logger.info("Generating monitoring strategy")
            print("  Generating monitoring strategy...")
            monitoring = self._generate_monitoring_strategy(state)
            state["monitoring_strategy"] = monitoring
            
            self.logger.info("Generated complete architecture specification")
            print("✓ Generated complete architecture specification")
        
        except Exception as e:
            error_msg = f"SpecGeneratorAgent failed: {str(e)}"
            self.logger.error(error_msg)
            print(f"✗ {error_msg}")
            state["errors"].append(error_msg)
            # Provide fallback documentation
            self._generate_fallback_specs(state)
        
        return state
    
    def _generate_executive_summary(self, state: MetaMindState) -> str:
        """Generate executive summary."""
        try:
            selected_arch = state["selected_architecture"]
            metrics = selected_arch.get("estimated_metrics", {})
            
            arch_summary = self._format_architecture_brief(selected_arch)
            metrics_summary = self._format_metrics_brief(metrics, selected_arch.get("final_score", 0))
            
            prompt = self.exec_summary_prompt.format(
                business_goal=state["business_goal"],
                domain=state["domain"],
                architecture=arch_summary,
                metrics=metrics_summary,
                iterations=len(state.get("iteration_history", []))
            )
            
            return invoke_llm_with_retry(
                self.llm,
                prompt,
                max_retries=3,
                timeout=120
            )
        
        except Exception as e:
            self.logger.error(f"Failed to generate executive summary: {e}")
            return self._fallback_executive_summary(state)
    
    def _generate_technical_spec(self, state: MetaMindState) -> str:
        """Generate technical specification."""
        try:
            selected_arch = state["selected_architecture"]
            metrics = selected_arch.get("estimated_metrics", {})
            
            arch_detail = self._format_architecture_detail(selected_arch)
            metrics_detail = self._format_metrics_detail(metrics)
            
            prompt = self.tech_spec_prompt.format(
                architecture=arch_detail,
                metrics=metrics_detail,
                domain=state["domain"]
            )
            
            return invoke_llm_with_retry(
                self.llm,
                prompt,
                max_retries=3,
                timeout=120
            )
        
        except Exception as e:
            self.logger.error(f"Failed to generate technical spec: {e}")
            return self._fallback_technical_spec(state)
    
    def _generate_deployment_plan(self, state: MetaMindState) -> str:
        """Generate deployment plan."""
        try:
            selected_arch = state["selected_architecture"]
            arch_detail = self._format_architecture_detail(selected_arch)
            
            prompt = self.deployment_prompt.format(
                architecture=arch_detail,
                domain=state["domain"]
            )
            
            return invoke_llm_with_retry(
                self.llm,
                prompt,
                max_retries=3,
                timeout=120
            )
        
        except Exception as e:
            self.logger.error(f"Failed to generate deployment plan: {e}")
            return self._fallback_deployment_plan(state)
    
    def _generate_monitoring_strategy(self, state: MetaMindState) -> str:
        """Generate monitoring strategy."""
        try:
            selected_arch = state["selected_architecture"]
            metrics = selected_arch.get("estimated_metrics", {})
            
            arch_detail = self._format_architecture_detail(selected_arch)
            metrics_detail = self._format_metrics_detail(metrics)
            
            prompt = self.monitoring_prompt.format(
                architecture=arch_detail,
                metrics=metrics_detail
            )
            
            return invoke_llm_with_retry(
                self.llm,
                prompt,
                max_retries=3,
                timeout=120
            )
        
        except Exception as e:
            self.logger.error(f"Failed to generate monitoring strategy: {e}")
            return self._fallback_monitoring_strategy(state)
    
    def _format_architecture_brief(self, architecture: dict) -> str:
        """Format architecture for brief display."""
        return f"{architecture['name']} using {architecture['template']} pattern with {len(architecture.get('modules', []))} components"
    
    def _format_architecture_detail(self, architecture: dict) -> str:
        """Format architecture for detailed display."""
        detail = f"Name: {architecture['name']}\n"
        detail += f"Template: {architecture['template']}\n"
        detail += f"Topology: {architecture['topology']}\n\n"
        detail += "Components:\n"
        for module in architecture.get("modules", []):
            detail += f"- {module['layer']}: {module['component']}\n"
        return detail
    
    def _format_metrics_brief(self, metrics: dict, score: float) -> str:
        """Format metrics for brief display."""
        return f"Overall Score: {score:.1f}/100 (Cost: {metrics.get('cost', 0):.0f}, Latency: {metrics.get('latency', 0):.0f}, Risk: {metrics.get('risk', 0):.0f})"
    
    def _format_metrics_detail(self, metrics: dict) -> str:
        """Format metrics for detailed display."""
        detail = "Performance Metrics (0-100 scale):\n"
        for metric, value in metrics.items():
            detail += f"- {metric.capitalize()}: {value:.1f}\n"
        return detail
    
    def _generate_fallback_specs(self, state: MetaMindState):
        """Generate fallback specifications when LLM fails."""
        state["executive_report"] = self._fallback_executive_summary(state)
        state["technical_specification"] = self._fallback_technical_spec(state)
        state["deployment_plan"] = self._fallback_deployment_plan(state)
        state["monitoring_strategy"] = self._fallback_monitoring_strategy(state)
    
    def _fallback_executive_summary(self, state: MetaMindState) -> str:
        """Fallback executive summary."""
        selected_arch = state.get("selected_architecture", {})
        return f"""# Executive Summary

## Overview
MetaMind has designed an AI architecture for: {state.get('business_goal', 'N/A')}

## Solution
Selected Architecture: {selected_arch.get('name', 'N/A')}
Template: {selected_arch.get('template', 'N/A')}
Overall Score: {selected_arch.get('final_score', 0):.1f}/100

## Key Benefits
- Optimized for {state.get('domain', 'general')} domain
- Meets performance and compliance requirements
- Production-ready design

## Next Steps
Review the technical specification and deployment plan for implementation details.
"""
    
    def _fallback_technical_spec(self, state: MetaMindState) -> str:
        """Fallback technical specification."""
        selected_arch = state.get("selected_architecture", {})
        spec = f"""# Technical Specification

## Architecture Overview
- **Name**: {selected_arch.get('name', 'N/A')}
- **Template**: {selected_arch.get('template', 'N/A')}
- **Topology**: {selected_arch.get('topology', 'N/A')}

## Components

"""
        for module in selected_arch.get("modules", []):
            spec += f"### {module['layer']}\n"
            spec += f"- Component: {module['component']}\n"
            spec += f"- Configuration: {module.get('config', {})}\n\n"
        
        return spec
    
    def _fallback_deployment_plan(self, state: MetaMindState) -> str:
        """Fallback deployment plan."""
        return """# Deployment Plan

## Prerequisites
1. Docker and Docker Compose installed
2. Required cloud resources provisioned
3. Environment variables configured

## Deployment Steps
1. Build container images
2. Deploy infrastructure components
3. Deploy application services
4. Configure networking and security
5. Run integration tests
6. Perform load testing
7. Go live

## Rollback Plan
1. Stop new services
2. Restore previous version
3. Verify system health
"""
    
    def _fallback_monitoring_strategy(self, state: MetaMindState) -> str:
        """Fallback monitoring strategy."""
        return """# Monitoring Strategy

## Key Metrics
- Request latency (P50, P95, P99)
- Error rate
- Throughput (requests/second)
- Resource utilization (CPU, memory)
- Cost per request

## Alerting Rules
- Latency > target: Warning
- Error rate > 1%: Critical
- Resource utilization > 80%: Warning

## Dashboards
- System health overview
- Performance metrics
- Cost tracking
- Error analysis

## Health Checks
- Endpoint availability
- Database connectivity
- Model responsiveness
"""

# Made with Bob
