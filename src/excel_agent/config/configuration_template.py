
# Configuration management template
import os
import json
from typing import Dict, Any, Optional
from pathlib import Path

class AgentConfig:
    """Configuration management for agents."""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or environment."""
        if self.config_file and Path(self.config_file).exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        
        # Fallback to environment variables
        return {
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
            "max_execution_time": int(os.getenv("MAX_EXECUTION_TIME", "300")),
            "retry_attempts": int(os.getenv("RETRY_ATTEMPTS", "3"))
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)
