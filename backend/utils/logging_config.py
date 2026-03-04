"""
Centralized Logging Configuration

Provides structured logging for the MetaMind system.
"""

import logging
import sys
from typing import Optional
from datetime import datetime


# Log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Setup centralized logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for log output
        format_string: Optional custom format string
        
    Returns:
        logging.Logger: Configured root logger
    """
    # Get root logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    logger.handlers = []
    
    # Create formatter
    formatter = logging.Formatter(
        format_string or LOG_FORMAT,
        datefmt=DATE_FORMAT
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, level.upper()))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name)


class AgentLogger:
    """
    Specialized logger for agents with structured output.
    """
    
    def __init__(self, agent_name: str):
        """
        Initialize agent logger.
        
        Args:
            agent_name: Name of the agent
        """
        self.agent_name = agent_name
        self.logger = get_logger(f"agents.{agent_name}")
    
    def info(self, message: str):
        """Log info message."""
        self.logger.info(f"[{self.agent_name}] {message}")
    
    def debug(self, message: str):
        """Log debug message."""
        self.logger.debug(f"[{self.agent_name}] {message}")
    
    def warning(self, message: str):
        """Log warning message."""
        self.logger.warning(f"[{self.agent_name}] {message}")
    
    def error(self, message: str, exc_info: bool = False):
        """Log error message."""
        self.logger.error(f"[{self.agent_name}] {message}", exc_info=exc_info)
    
    def critical(self, message: str):
        """Log critical message."""
        self.logger.critical(f"[{self.agent_name}] {message}")
    
    def log_execution_start(self, run_id: str, version: int):
        """Log agent execution start."""
        self.logger.info(
            f"[{self.agent_name}] Starting execution - Run: {run_id}, Version: {version}"
        )
    
    def log_execution_success(self, run_id: str, duration_ms: float, details: Optional[str] = None):
        """Log successful execution."""
        msg = f"[{self.agent_name}] Execution successful - Run: {run_id}, Duration: {duration_ms:.0f}ms"
        if details:
            msg += f" - {details}"
        self.logger.info(msg)
    
    def log_execution_failure(self, run_id: str, error: Exception):
        """Log execution failure."""
        self.logger.error(
            f"[{self.agent_name}] Execution failed - Run: {run_id}, Error: {str(error)}",
            exc_info=True
        )
    
    def log_warning(self, run_id: str, message: str):
        """Log warning."""
        self.logger.warning(f"[{self.agent_name}] Warning - Run: {run_id} - {message}")
    
    def log_metric(self, run_id: str, metric_name: str, value: float):
        """Log metric value."""
        self.logger.debug(f"[{self.agent_name}] Metric - Run: {run_id}, {metric_name}: {value:.2f}")
    
    def log_llm_call(self, run_id: str, prompt_length: int, response_length: int, duration_ms: float):
        """Log LLM call details."""
        self.logger.debug(
            f"[{self.agent_name}] LLM Call - Run: {run_id}, "
            f"Prompt: {prompt_length} chars, Response: {response_length} chars, "
            f"Duration: {duration_ms:.0f}ms"
        )
    
    def log_retry(self, run_id: str, attempt: int, max_attempts: int, error: str):
        """Log retry attempt."""
        self.logger.warning(
            f"[{self.agent_name}] Retry {attempt}/{max_attempts} - Run: {run_id}, Error: {error}"
        )


# Initialize default logging
setup_logging()

# Made with Bob
