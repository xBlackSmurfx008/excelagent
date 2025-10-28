"""
Excel Agent - Main Package

AI-powered Excel reconciliation agent with advanced thinking capabilities.
"""

__version__ = "1.0.0"
__author__ = "Excel Agent Team"
__email__ = "team@excelagent.com"

from .core.reconciliation_engine import ReconciliationEngine
from .agents.orchestration_agent import OrchestrationAgent
from .api.dashboard import create_app

__all__ = [
    "ReconciliationEngine",
    "OrchestrationAgent", 
    "create_app",
]
