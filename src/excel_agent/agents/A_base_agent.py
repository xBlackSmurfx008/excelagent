"""
Excel Agent - Base Agent Class

Base class for all AI agents with common functionality.
"""

import logging
import json
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class AgentResult:
    """Standard result format for all agents"""
    status: str  # success, error, warning
    message: str
    data: Dict[str, Any]
    timestamp: datetime
    execution_time: float
    agent_name: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        result = asdict(self)
        result['timestamp'] = self.timestamp.isoformat()
        return result

class BaseAgent(ABC):
    """Base class for all AI agents"""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize base agent
        
        Args:
            name: Agent name
            config: Agent configuration
        """
        self.name = name
        self.config = config or {}
        self.logger = self._setup_logging()
        self.execution_history: List[AgentResult] = []
        
        self.logger.info(f"Initialized {self.name} agent")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the agent"""
        logger = logging.getLogger(f"excel_agent.{self.name}")
        logger.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # File handler
        file_handler = logging.FileHandler(f'logs/{self.name}.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    @abstractmethod
    def execute(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Execute the agent's main functionality
        
        Args:
            input_data: Input data for processing
            
        Returns:
            AgentResult: Execution result
        """
        pass
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """
        Validate input data
        
        Args:
            input_data: Input data to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            # Basic validation - can be overridden by subclasses
            if not isinstance(input_data, dict):
                self.logger.error("Input data must be a dictionary")
                return False
            
            return True
        except Exception as e:
            self.logger.error(f"Input validation error: {e}")
            return False
    
    def handle_error(self, error: Exception, context: str = "") -> AgentResult:
        """
        Handle errors consistently
        
        Args:
            error: Exception that occurred
            context: Additional context
            
        Returns:
            AgentResult: Error result
        """
        error_msg = f"Error in {self.name}: {str(error)}"
        if context:
            error_msg += f" (Context: {context})"
        
        self.logger.error(error_msg)
        
        return AgentResult(
            status="error",
            message=error_msg,
            data={"error": str(error), "context": context},
            timestamp=datetime.now(),
            execution_time=0.0,
            agent_name=self.name
        )
    
    def run(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Run the agent with error handling and logging
        
        Args:
            input_data: Input data for processing
            
        Returns:
            AgentResult: Execution result
        """
        start_time = datetime.now()
        
        try:
            self.logger.info(f"Starting {self.name} execution")
            
            # Validate input
            if not self.validate_input(input_data):
                return self.handle_error(
                    ValueError("Invalid input data"), 
                    "Input validation failed"
                )
            
            # Execute agent logic
            result = self.execute(input_data)
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()
            result.execution_time = execution_time
            
            # Store in history
            self.execution_history.append(result)
            
            # Log result
            if result.status == "success":
                self.logger.info(f"{self.name} completed successfully in {execution_time:.2f}s")
            else:
                self.logger.warning(f"{self.name} completed with status: {result.status}")
            
            return result
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            result = self.handle_error(e, "Main execution")
            result.execution_time = execution_time
            self.execution_history.append(result)
            return result
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get execution history"""
        return [result.to_dict() for result in self.execution_history]
    
    def get_last_result(self) -> Optional[AgentResult]:
        """Get the last execution result"""
        return self.execution_history[-1] if self.execution_history else None
    
    def clear_history(self):
        """Clear execution history"""
        self.execution_history.clear()
        self.logger.info(f"Cleared execution history for {self.name}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "name": self.name,
            "status": "active",
            "execution_count": len(self.execution_history),
            "last_execution": self.execution_history[-1].timestamp.isoformat() if self.execution_history else None,
            "config": self.config
        }
    
    def save_result(self, result: AgentResult, filename: Optional[str] = None):
        """
        Save result to file
        
        Args:
            result: Result to save
            filename: Optional filename (defaults to timestamp)
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.name}_result_{timestamp}.json"
        
        filepath = Path("reports") / filename
        
        try:
            with open(filepath, 'w') as f:
                json.dump(result.to_dict(), f, indent=2, default=str)
            
            self.logger.info(f"Result saved to {filepath}")
        except Exception as e:
            self.logger.error(f"Failed to save result: {e}")
    
    def __str__(self) -> str:
        return f"{self.name} Agent"
    
    def __repr__(self) -> str:
        return f"BaseAgent(name='{self.name}', config={self.config})"
