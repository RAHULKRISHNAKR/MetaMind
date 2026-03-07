"""
LLM Utility Functions

Provides retry logic, timeout safeguards, and error handling for LLM operations.
Supports multiple LLM providers: Ollama, xAI Grok, OpenAI, Anthropic.
"""

import os
import time
import logging
from typing import Optional, Callable, Union
from langchain_community.llms import Ollama

# Configure logging
logger = logging.getLogger(__name__)


class LLMError(Exception):
    """Base exception for LLM-related errors."""
    pass


class LLMTimeoutError(LLMError):
    """Raised when LLM call times out."""
    pass


class LLMRetryExhaustedError(LLMError):
    """Raised when all retry attempts are exhausted."""
    pass


def create_llm_with_retry(
    base_url: str = "http://localhost:11434",
    model_name: str = "llama3",
    temperature: float = 0.2,
    timeout: int = 120,
    **kwargs
) -> Ollama:
    """
    Create an Ollama LLM instance with timeout configuration.
    
    Args:
        base_url: Base URL for Ollama service
        model_name: Name of the model to use
        temperature: Temperature for generation (0.0-1.0)
        timeout: Timeout in seconds for LLM calls
        **kwargs: Additional arguments for Ollama
        
    Returns:
        Ollama: Configured LLM instance
    """
    # Remove 'model' from kwargs if present to avoid conflict
    kwargs.pop('model', None)
    
    return Ollama(
        base_url=base_url,
        model=model_name,
        temperature=temperature,
        timeout=timeout,
        **kwargs
    )


def invoke_llm_with_retry(
    llm: Ollama,
    prompt: str,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    timeout: Optional[int] = None,
    on_retry: Optional[Callable[[int, Exception], None]] = None
) -> str:
    """
    Invoke LLM with exponential backoff retry logic.
    
    Args:
        llm: Ollama LLM instance
        prompt: Prompt to send to LLM
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay between retries in seconds
        backoff_factor: Multiplier for delay after each retry
        timeout: Optional timeout override in seconds
        on_retry: Optional callback function called on each retry
        
    Returns:
        str: LLM response
        
    Raises:
        LLMTimeoutError: If LLM call times out
        LLMRetryExhaustedError: If all retries are exhausted
        LLMError: For other LLM-related errors
    """
    delay = initial_delay
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            # Set timeout if provided
            if timeout:
                llm.timeout = timeout
            
            # Invoke LLM
            logger.debug(f"LLM invocation attempt {attempt + 1}/{max_retries}")
            response = llm.invoke(prompt)
            
            # Success
            logger.debug(f"LLM invocation successful on attempt {attempt + 1}")
            return response
            
        except TimeoutError as e:
            last_exception = LLMTimeoutError(f"LLM call timed out: {str(e)}")
            logger.warning(f"Attempt {attempt + 1}/{max_retries} timed out: {str(e)}")
            
        except Exception as e:
            last_exception = LLMError(f"LLM call failed: {str(e)}")
            logger.warning(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
        
        # If not last attempt, wait and retry
        if attempt < max_retries - 1:
            logger.info(f"Retrying in {delay:.1f} seconds...")
            
            # Call retry callback if provided
            if on_retry:
                try:
                    on_retry(attempt + 1, last_exception)
                except Exception as callback_error:
                    logger.error(f"Retry callback failed: {str(callback_error)}")
            
            time.sleep(delay)
            delay *= backoff_factor
    
    # All retries exhausted
    error_msg = f"LLM invocation failed after {max_retries} attempts"
    logger.error(error_msg)
    raise LLMRetryExhaustedError(error_msg) from last_exception


def parse_json_with_retry(
    response: str,
    max_attempts: int = 3
) -> dict:
    """
    Parse JSON from LLM response with multiple extraction strategies.
    
    Args:
        response: Raw LLM response
        max_attempts: Maximum parsing attempts with different strategies
        
    Returns:
        dict: Parsed JSON object
        
    Raises:
        ValueError: If JSON cannot be parsed
    """
    import json
    
    strategies = [
        # Strategy 1: Find first JSON object
        lambda r: r[r.find("{"):r.rfind("}") + 1],
        # Strategy 2: Find first JSON array
        lambda r: r[r.find("["):r.rfind("]") + 1],
        # Strategy 3: Strip markdown code blocks
        lambda r: r.replace("```json", "").replace("```", "").strip(),
    ]
    
    for i, strategy in enumerate(strategies[:max_attempts]):
        try:
            json_str = strategy(response)
            if json_str:
                return json.loads(json_str)
        except (json.JSONDecodeError, ValueError) as e:
            logger.debug(f"JSON parsing strategy {i + 1} failed: {str(e)}")
            continue
    
    raise ValueError("Failed to parse JSON from LLM response")


def validate_llm_response(
    response: str,
    min_length: int = 10,
    max_length: int = 50000,
    required_keywords: Optional[list] = None
) -> tuple[bool, str]:
    """
    Validate LLM response quality.
    
    Args:
        response: LLM response to validate
        min_length: Minimum acceptable response length
        max_length: Maximum acceptable response length
        required_keywords: Optional list of keywords that must be present
        
    Returns:
        tuple: (is_valid, error_message)
    """
    # Check length
    if len(response) < min_length:
        return False, f"Response too short ({len(response)} < {min_length})"
    
    if len(response) > max_length:
        return False, f"Response too long ({len(response)} > {max_length})"
    
    # Check for common error patterns
    error_patterns = [
        "I cannot",
        "I'm unable to",
        "I don't have access",
        "Error:",
        "Exception:",
    ]
    
    response_lower = response.lower()
    for pattern in error_patterns:
        if pattern.lower() in response_lower:
            return False, f"Response contains error pattern: {pattern}"
    
    # Check required keywords
    if required_keywords:
        missing_keywords = [kw for kw in required_keywords if kw.lower() not in response_lower]
        if missing_keywords:
            return False, f"Response missing required keywords: {', '.join(missing_keywords)}"
    
    return True, "Response is valid"


# Retry configuration presets
RETRY_CONFIGS = {
    "fast": {
        "max_retries": 2,
        "initial_delay": 0.5,
        "backoff_factor": 1.5,
        "timeout": 30,
    },
    "standard": {
        "max_retries": 3,
        "initial_delay": 1.0,
        "backoff_factor": 2.0,
        "timeout": 60,
    },
    "robust": {
        "max_retries": 5,
        "initial_delay": 2.0,
        "backoff_factor": 2.0,
        "timeout": 120,
    },
}


def get_retry_config(preset: str = "standard") -> dict:
    """
    Get retry configuration preset.
    
    Args:
        preset: Preset name ("fast", "standard", or "robust")
        
    Returns:
        dict: Retry configuration
    """
    return RETRY_CONFIGS.get(preset, RETRY_CONFIGS["standard"])

def create_llm_from_env(**kwargs):
    """
    Create LLM instance based on environment variables.
    
    Reads LLM_PROVIDER from environment and creates appropriate instance.
    Supports: groq (default), ollama, xai, openai, anthropic
    
    Args:
        **kwargs: Additional arguments (temperature, timeout, etc.)
        
    Returns:
        LLM instance configured based on environment
        
    Environment Variables:
        LLM_PROVIDER: Provider to use (groq, ollama, xai, openai, anthropic)
        
        For Groq:
            GROQ_API_KEY: API key
            GROQ_MODEL: Model name (default: llama-3.1-70b-versatile)
            GROQ_BASE_URL: Base URL (default: https://api.groq.com/openai/v1)
        
        For Ollama:
            OLLAMA_BASE_URL: Base URL (default: http://localhost:11434)
            OLLAMA_MODEL: Model name (default: llama3)
            
        For xAI Grok:
            XAI_API_KEY: API key
            XAI_MODEL: Model name (default: grok-beta)
            XAI_BASE_URL: Base URL (default: https://api.x.ai/v1)
            
        For OpenAI:
            OPENAI_API_KEY: API key
            OPENAI_MODEL: Model name (default: gpt-4)
            
        For Anthropic:
            ANTHROPIC_API_KEY: API key
            ANTHROPIC_MODEL: Model name (default: claude-3-opus-20240229)
    """
    provider = os.getenv("LLM_PROVIDER", "groq").lower()
    temperature = kwargs.get("temperature", 0.7)
    timeout = kwargs.get("timeout", 120)
    
    logger.info(f"Creating LLM with provider: {provider}")
    
    if provider == "groq":
        try:
            from langchain_openai import ChatOpenAI
        except ImportError:
            raise ImportError("langchain-openai not installed. Run: pip install langchain-openai")
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")
        
        return ChatOpenAI(
            api_key=api_key,
            base_url=os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1"),
            model=os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile"),
            temperature=temperature,
            timeout=timeout,
            max_retries=3
        )
    
    elif provider == "xai":
        try:
            from langchain_openai import ChatOpenAI
        except ImportError:
            raise ImportError("langchain-openai not installed. Run: pip install langchain-openai")
        
        api_key = os.getenv("XAI_API_KEY")
        if not api_key:
            raise ValueError("XAI_API_KEY environment variable not set")
        
        return ChatOpenAI(
            api_key=api_key,
            base_url=os.getenv("XAI_BASE_URL", "https://api.x.ai/v1"),
            model=os.getenv("XAI_MODEL", "grok-beta"),
            temperature=temperature,
            timeout=timeout,
            max_retries=3
        )
    
    elif provider == "openai":
        try:
            from langchain_openai import ChatOpenAI
        except ImportError:
            raise ImportError("langchain-openai not installed. Run: pip install langchain-openai")
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        return ChatOpenAI(
            api_key=api_key,
            model=os.getenv("OPENAI_MODEL", "gpt-4"),
            temperature=temperature,
            timeout=timeout,
            max_retries=3
        )
    
    elif provider == "anthropic":
        try:
            from langchain_anthropic import ChatAnthropic
        except ImportError:
            raise ImportError("langchain-anthropic not installed. Run: pip install langchain-anthropic")
        
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        
        return ChatAnthropic(
            api_key=api_key,
            model=os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229"),
            temperature=temperature,
            timeout=timeout,
            max_retries=3
        )
    
    else:  # ollama (default)
        return create_llm_with_retry(
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            model_name=os.getenv("OLLAMA_MODEL", "llama3"),
            temperature=temperature,
            timeout=timeout
        )


def get_provider_info() -> dict:
    """
    Get information about the current LLM provider configuration.
    
    Returns:
        dict: Provider information
    """
    provider = os.getenv("LLM_PROVIDER", "groq").lower()
    
    info = {
        "provider": provider,
        "model": None,
        "base_url": None
    }
    
    if provider == "groq":
        info["model"] = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
        info["base_url"] = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
    elif provider == "xai":
        info["model"] = os.getenv("XAI_MODEL", "grok-beta")
        info["base_url"] = os.getenv("XAI_BASE_URL", "https://api.x.ai/v1")
    elif provider == "openai":
        info["model"] = os.getenv("OPENAI_MODEL", "gpt-4")
        info["base_url"] = "https://api.openai.com/v1"
    elif provider == "anthropic":
        info["model"] = os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")
        info["base_url"] = "https://api.anthropic.com"
    else:  # ollama
        info["model"] = os.getenv("OLLAMA_MODEL", "llama3")
        info["base_url"] = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    return info