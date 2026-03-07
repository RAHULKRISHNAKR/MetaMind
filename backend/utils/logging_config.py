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
    Supports streaming callbacks for real-time frontend updates.
    """
    
    # Class-level storage for streaming callbacks
    _stream_callbacks = {}
    
    def __init__(self, agent_name: str, run_id: Optional[str] = None):
        """
        Initialize agent logger.
        
        Args:
            agent_name: Name of the agent
            run_id: Optional run ID for streaming logs to frontend
        """
        self.agent_name = agent_name
        self.run_id = run_id
        self.logger = get_logger(f"agents.{agent_name}")
    
    @classmethod
    def register_stream_callback(cls, run_id: str, callback):
        """
        Register a callback function for streaming logs.
        
        Args:
            run_id: Run ID to associate with callback
            callback: Function to call with log messages (signature: callback(level, agent, message))
        """
        cls._stream_callbacks[run_id] = callback
    
    @classmethod
    def unregister_stream_callback(cls, run_id: str):
        """
        Unregister a streaming callback.
        
        Args:
            run_id: Run ID to unregister
        """
        if run_id in cls._stream_callbacks:
            del cls._stream_callbacks[run_id]
    
    def _stream_log(self, level: str, message: str):
        """
        Stream log message to registered callback if available.
        
        Args:
            level: Log level (INFO, DEBUG, WARNING, ERROR, CRITICAL)
            message: Log message
        """
        if self.run_id and self.run_id in self._stream_callbacks:
            try:
                callback = self._stream_callbacks[self.run_id]
                callback(level, self.agent_name, message)
            except Exception as e:
                # Don't let streaming errors break the agent
                self.logger.error(f"Failed to stream log: {e}")
    
    def info(self, message: str):
        """Log info message."""
        self.logger.info(f"[{self.agent_name}] {message}")
        self._stream_log("INFO", message)
    
    def debug(self, message: str):
        """Log debug message."""
        self.logger.debug(f"[{self.agent_name}] {message}")
        self._stream_log("DEBUG", message)
    
    def warning(self, message: str):
        """Log warning message."""
        self.logger.warning(f"[{self.agent_name}] {message}")
        self._stream_log("WARNING", message)
    
    def error(self, message: str, exc_info: bool = False):
        """Log error message."""
        self.logger.error(f"[{self.agent_name}] {message}", exc_info=exc_info)
        self._stream_log("ERROR", message)
    
    def critical(self, message: str):
        """Log critical message."""
        self.logger.critical(f"[{self.agent_name}] {message}")
        self._stream_log("CRITICAL", message)
    
    def log_execution_start(self, run_id: str, version: int):
        """Log agent execution start."""
        msg = f"Starting execution - Run: {run_id}, Version: {version}"
        self.logger.info(f"[{self.agent_name}] {msg}")
        self._stream_log("INFO", f"🚀 Starting execution (Version {version})")
    
    def log_execution_success(self, run_id: str, duration_ms: float, details: Optional[str] = None):
        """Log successful execution."""
        msg = f"Execution successful - Run: {run_id}, Duration: {duration_ms:.0f}ms"
        if details:
            msg += f" - {details}"
        self.logger.info(f"[{self.agent_name}] {msg}")
        
        # Stream user-friendly message
        stream_msg = f"✅ Completed in {duration_ms:.0f}ms"
        if details:
            stream_msg += f" - {details}"
        self._stream_log("INFO", stream_msg)
    
    def log_execution_failure(self, run_id: str, error: Exception):
        """Log execution failure."""
        msg = f"Execution failed - Run: {run_id}, Error: {str(error)}"
        self.logger.error(f"[{self.agent_name}] {msg}", exc_info=True)
        self._stream_log("ERROR", f"❌ Execution failed: {str(error)}")
    
    def log_warning(self, run_id: str, message: str):
        """Log warning."""
        self.logger.warning(f"[{self.agent_name}] Warning - Run: {run_id} - {message}")
        self._stream_log("WARNING", f"⚠️ {message}")
    
    def log_metric(self, run_id: str, metric_name: str, value: float):
        """Log metric value."""
        self.logger.debug(f"[{self.agent_name}] Metric - Run: {run_id}, {metric_name}: {value:.2f}")
        self._stream_log("DEBUG", f"📊 {metric_name}: {value:.2f}")
    
    def log_llm_call(self, run_id: str, prompt_length: int, response_length: int, duration_ms: float):
        """Log LLM call details."""
        self.logger.debug(
            f"[{self.agent_name}] LLM Call - Run: {run_id}, "
            f"Prompt: {prompt_length} chars, Response: {response_length} chars, "
            f"Duration: {duration_ms:.0f}ms"
        )
        self._stream_log("DEBUG", f"🤖 LLM call completed ({duration_ms:.0f}ms)")
    
    def log_retry(self, run_id: str, attempt: int, max_attempts: int, error: str):
        """Log retry attempt."""
        self.logger.warning(
            f"[{self.agent_name}] Retry {attempt}/{max_attempts} - Run: {run_id}, Error: {error}"
        )
        self._stream_log("WARNING", f"🔄 Retry {attempt}/{max_attempts}: {error}")


# Initialize default logging
setup_logging()