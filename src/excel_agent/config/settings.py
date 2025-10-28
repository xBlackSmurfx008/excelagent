"""
Excel Agent - Configuration Management

Centralized configuration management with environment-specific settings.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class DatabaseConfig:
    """Database configuration"""
    url: str = "sqlite:///excel_agent.db"
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10

@dataclass
class LoggingConfig:
    """Logging configuration"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: Optional[str] = None
    audit_file: Optional[str] = None
    max_bytes: int = 10485760  # 10MB
    backup_count: int = 5

@dataclass
class APIConfig:
    """API configuration"""
    host: str = "0.0.0.0"
    port: int = 5000
    debug: bool = False
    secret_key: str = "dev-secret-key"
    cors_origins: list = None
    
    def __post_init__(self):
        if self.cors_origins is None:
            self.cors_origins = ["http://localhost:3000", "http://localhost:5000"]

@dataclass
class FileConfig:
    """File handling configuration"""
    upload_folder: str = "uploads"
    data_folder: str = "data"
    reports_folder: str = "reports"
    max_content_length: int = 16777216  # 16MB
    allowed_extensions: set = None
    
    def __post_init__(self):
        if self.allowed_extensions is None:
            self.allowed_extensions = {"xlsx", "xls", "csv"}

@dataclass
class OpenAIConfig:
    """OpenAI configuration"""
    api_key: Optional[str] = None
    model: str = "gpt-4"
    max_tokens: int = 3000
    temperature: float = 0.3
    timeout: int = 30

@dataclass
class PerformanceConfig:
    """Performance configuration"""
    max_workers: int = 4
    timeout_seconds: int = 300
    enable_profiling: bool = False
    cache_size: int = 1000

@dataclass
class SecurityConfig:
    """Security configuration"""
    rate_limit_per_minute: int = 60
    enable_csrf: bool = True
    session_timeout: int = 3600  # 1 hour

class Config:
    """Main configuration class"""
    
    def __init__(self, environment: str = None):
        self.environment = environment or os.getenv("FLASK_ENV", "development")
        self._load_config()
    
    def _load_config(self):
        """Load configuration from environment and config files"""
        # Load from environment variables
        self.database = DatabaseConfig(
            url=os.getenv("DATABASE_URL", "sqlite:///excel_agent.db"),
            echo=os.getenv("DATABASE_ECHO", "false").lower() == "true"
        )
        
        self.logging = LoggingConfig(
            level=os.getenv("LOG_LEVEL", "INFO"),
            file=os.getenv("LOG_FILE"),
            audit_file=os.getenv("AUDIT_LOG_FILE")
        )
        
        self.api = APIConfig(
            host=os.getenv("FLASK_HOST", "0.0.0.0"),
            port=int(os.getenv("FLASK_PORT", "5000")),
            debug=os.getenv("FLASK_DEBUG", "false").lower() == "true",
            secret_key=os.getenv("SECRET_KEY", "dev-secret-key")
        )
        
        self.files = FileConfig(
            upload_folder=os.getenv("UPLOAD_FOLDER", "uploads"),
            data_folder=os.getenv("DATA_FOLDER", "data"),
            reports_folder=os.getenv("REPORTS_FOLDER", "reports"),
            max_content_length=int(os.getenv("MAX_CONTENT_LENGTH", "16777216"))
        )
        
        self.openai = OpenAIConfig(
            api_key=os.getenv("OPENAI_API_KEY"),
            model=os.getenv("OPENAI_MODEL", "gpt-4"),
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "3000")),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.3"))
        )
        
        self.performance = PerformanceConfig(
            max_workers=int(os.getenv("MAX_WORKERS", "4")),
            timeout_seconds=int(os.getenv("TIMEOUT_SECONDS", "300")),
            enable_profiling=os.getenv("ENABLE_PROFILING", "false").lower() == "true"
        )
        
        self.security = SecurityConfig(
            rate_limit_per_minute=int(os.getenv("RATE_LIMIT_PER_MINUTE", "60")),
            enable_csrf=os.getenv("ENABLE_CSRF", "true").lower() == "true"
        )
        
        # Load environment-specific config file if exists
        config_file = Path(f"config/{self.environment}/settings.yaml")
        if config_file.exists():
            self._load_yaml_config(config_file)
    
    def _load_yaml_config(self, config_file: Path):
        """Load configuration from YAML file"""
        try:
            with open(config_file, 'r') as f:
                yaml_config = yaml.safe_load(f)
            
            # Override with YAML values
            for section, values in yaml_config.items():
                if hasattr(self, section) and isinstance(values, dict):
                    section_obj = getattr(self, section)
                    for key, value in values.items():
                        if hasattr(section_obj, key):
                            setattr(section_obj, key, value)
        except Exception as e:
            print(f"Warning: Could not load YAML config {config_file}: {e}")
    
    def validate(self) -> bool:
        """Validate configuration"""
        errors = []
        
        # Validate OpenAI API key
        if not self.openai.api_key:
            errors.append("OpenAI API key is required")
        
        # Validate file paths
        for folder in [self.files.upload_folder, self.files.data_folder, self.files.reports_folder]:
            if not os.path.exists(folder):
                try:
                    os.makedirs(folder, exist_ok=True)
                except Exception as e:
                    errors.append(f"Cannot create folder {folder}: {e}")
        
        # Validate port
        if not (1 <= self.api.port <= 65535):
            errors.append(f"Invalid port number: {self.api.port}")
        
        if errors:
            print("Configuration validation errors:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "environment": self.environment,
            "database": {
                "url": self.database.url,
                "echo": self.database.echo
            },
            "logging": {
                "level": self.logging.level,
                "file": self.logging.file,
                "audit_file": self.logging.audit_file
            },
            "api": {
                "host": self.api.host,
                "port": self.api.port,
                "debug": self.api.debug
            },
            "files": {
                "upload_folder": self.files.upload_folder,
                "data_folder": self.files.data_folder,
                "reports_folder": self.files.reports_folder,
                "max_content_length": self.files.max_content_length
            },
            "openai": {
                "model": self.openai.model,
                "max_tokens": self.openai.max_tokens,
                "temperature": self.openai.temperature
            },
            "performance": {
                "max_workers": self.performance.max_workers,
                "timeout_seconds": self.performance.timeout_seconds
            },
            "security": {
                "rate_limit_per_minute": self.security.rate_limit_per_minute,
                "enable_csrf": self.security.enable_csrf
            }
        }

# Global configuration instance
config = Config()

def get_config() -> Config:
    """Get the global configuration instance"""
    return config

def reload_config(environment: str = None) -> Config:
    """Reload configuration"""
    global config
    config = Config(environment)
    return config
