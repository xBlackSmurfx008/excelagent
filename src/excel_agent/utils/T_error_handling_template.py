
# Comprehensive error handling template
import logging
from typing import Dict, Any, Optional
from datetime import datetime

class AgentError(Exception):
    """Base exception for agent errors."""
    pass

class ValidationError(AgentError):
    """Exception for validation errors."""
    pass

class ProcessingError(AgentError):
    """Exception for processing errors."""
    pass

def safe_execute(func, *args, **kwargs):
    """Safely execute a function with error handling."""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Error in {func.__name__}: {str(e)}")
        raise
