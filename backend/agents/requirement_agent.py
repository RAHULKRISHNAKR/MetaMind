"""
RequirementAgent - Parse natural language requirements into structured JSON

This LLM-based agent converts user descriptions into validated constraint schemas.
"""

import json
from typing import Dict, Any
from langchain_core.prompts import PromptTemplate
from ..orchestration.state import MetaMindState, VALID_DOMAINS, VALID_MODALITIES
from ..utils.llm_utils import create_llm_from_env, invoke_llm_with_retry, parse_json_with_retry
from ..utils.validation import RequirementInput, ConstraintsInput
from ..utils.logging_config import AgentLogger


class RequirementAgent:
    """
    LLM-based agent that parses natural language requirements.
    
    Converts user input into structured constraints including:
    - Business goal
    - Domain
    - Modalities
    - Budget, latency, users
    - Risk and compliance levels
    """
    
    def __init__(self, ollama_base_url: str = "http://localhost:11434", model_name: str = "llama3"):
        """
        Initialize the RequirementAgent.
        
        Args:
            ollama_base_url: Base URL for Ollama service (fallback if env not set)
            model_name: Name of the model to use (fallback if env not set)
        """
        # Use environment-based LLM creation for seamless provider switching (Groq priority)
        self.llm = create_llm_from_env(temperature=0.1, timeout=60)
        self.logger = AgentLogger("RequirementAgent")
        
        self.prompt_template = PromptTemplate(
            input_variables=["business_goal", "domain", "modalities", "constraints"],
            template="""You are an AI requirements analyst. Your task is to validate and structure the user's requirements.

User Input:
- Business Goal: {business_goal}
- Domain: {domain}
- Modalities: {modalities}
- Constraints: {constraints}

Validate and extract:
1. Business goal (clear, measurable objective)
2. Domain (must be one of: healthcare, finance, ecommerce, education, legal, general)
3. Modalities (must be from: text, vision, multimodal, tabular)
4. Budget constraint (USD/month, must be positive)
5. Latency target (milliseconds, must be positive)
6. Expected users (concurrent users, must be positive)
7. Risk tolerance (must be: low, medium, or high)
8. Compliance level (must be: low, medium, or high)

If any field is missing or invalid, provide a reasonable default based on the domain.

Output ONLY valid JSON in this exact format:
{{
    "business_goal": "string",
    "domain": "string",
    "modalities": ["string"],
    "constraints": {{
        "budget": number,
        "latency_target_ms": number,
        "expected_users": number,
        "risk_tolerance": "string",
        "compliance_level": "string"
    }},
    "validation_notes": ["any issues or assumptions made"]
}}

JSON Output:"""
        )
    
    def execute(self, state: MetaMindState) -> MetaMindState:
        """
        Execute requirement parsing and validation.
        
        Args:
            state: Current MetaMind state
            
        Returns:
            MetaMindState: Updated state with validated requirements
        """
        try:
            # Initialize logger with run_id for streaming
            run_id = state.get("run_id", "unknown")
            if self.logger is None or self.logger.run_id != run_id:
                self.logger = AgentLogger("RequirementAgent", run_id=run_id)
            
            self.logger.info("🔍 Analyzing your requirements...")
            
            # Prepare input for LLM
            # Convert complex objects to strings for template
            constraints_dict = state.get("constraints", {})
            constraints_str = json.dumps(constraints_dict, indent=2)
            modalities_list = state.get("modalities", ["text"])
            modalities_str = ", ".join(modalities_list)
            
            prompt = self.prompt_template.format(
                business_goal=state.get("business_goal", ""),
                domain=state.get("domain", "general"),
                modalities=modalities_str,
                constraints=constraints_str
            )
            
            # Get LLM response with retry logic
            response = invoke_llm_with_retry(
                self.llm,
                prompt,
                max_retries=3,
                timeout=60
            )
            
            # Parse JSON response with retry
            parsed = parse_json_with_retry(response, max_attempts=3)
            
            # Validate and update state
            state = self._validate_and_update_state(state, parsed)
            
            # Add validation notes as warnings if any
            if parsed.get("validation_notes"):
                state["warnings"].extend(parsed["validation_notes"])
            
            self.logger.info(f"✅ Requirements validated: {state['domain']} domain, {len(state['modalities'])} modalities")
            
        except Exception as e:
            error_msg = f"RequirementAgent failed: {str(e)}"
            if self.logger:
                self.logger.error(f"❌ {error_msg}")
            state["errors"].append(error_msg)
            # Apply defaults on failure
            state = self._apply_defaults(state)
        
        return state
    
    def _validate_and_update_state(self, state: MetaMindState, parsed: Dict[str, Any]) -> MetaMindState:
        """
        Validate parsed requirements and update state.
        
        Args:
            state: Current state
            parsed: Parsed requirements from LLM
            
        Returns:
            MetaMindState: Updated state
        """
        # Validate domain
        domain = parsed.get("domain", "general").lower()
        if domain not in VALID_DOMAINS:
            state["warnings"].append(f"Invalid domain '{domain}', defaulting to 'general'")
            domain = "general"
        state["domain"] = domain
        
        # Validate modalities
        modalities = parsed.get("modalities", ["text"])
        valid_modalities = [m for m in modalities if m.lower() in VALID_MODALITIES]
        if not valid_modalities:
            state["warnings"].append("No valid modalities, defaulting to ['text']")
            valid_modalities = ["text"]
        state["modalities"] = valid_modalities
        
        # Update business goal
        if parsed.get("business_goal"):
            state["business_goal"] = parsed["business_goal"]
        
        # Validate and update constraints
        constraints = parsed.get("constraints", {})
        
        # Budget
        budget = constraints.get("budget", 10000)
        if budget <= 0:
            state["warnings"].append(f"Invalid budget {budget}, defaulting to 10000")
            budget = 10000
        state["constraints"]["budget"] = float(budget)
        
        # Latency
        latency = constraints.get("latency_target_ms", 500)
        if latency <= 0:
            state["warnings"].append(f"Invalid latency {latency}, defaulting to 500ms")
            latency = 500
        state["constraints"]["latency_target_ms"] = int(latency)
        
        # Users
        users = constraints.get("expected_users", 10000)
        if users <= 0:
            state["warnings"].append(f"Invalid user count {users}, defaulting to 10000")
            users = 10000
        state["constraints"]["expected_users"] = int(users)
        
        # Risk tolerance
        risk = constraints.get("risk_tolerance", "medium").lower()
        if risk not in ["low", "medium", "high"]:
            state["warnings"].append(f"Invalid risk tolerance '{risk}', defaulting to 'medium'")
            risk = "medium"
        state["constraints"]["risk_tolerance"] = risk
        
        # Compliance level
        compliance = constraints.get("compliance_level", "medium").lower()
        if compliance not in ["low", "medium", "high"]:
            state["warnings"].append(f"Invalid compliance level '{compliance}', defaulting to 'medium'")
            compliance = "medium"
        state["constraints"]["compliance_level"] = compliance
        
        return state
    
    def _apply_defaults(self, state: MetaMindState) -> MetaMindState:
        """
        Apply default values when parsing fails.
        
        Args:
            state: Current state
            
        Returns:
            MetaMindState: State with defaults applied
        """
        if not state.get("domain") or state["domain"] not in VALID_DOMAINS:
            state["domain"] = "general"
        
        if not state.get("modalities"):
            state["modalities"] = ["text"]
        
        if not state.get("constraints"):
            state["constraints"] = {
                "budget": 10000.0,
                "latency_target_ms": 500,
                "expected_users": 10000,
                "risk_tolerance": "medium",
                "compliance_level": "medium"
            }
        
        state["warnings"].append("Applied default values due to parsing failure")
        return state