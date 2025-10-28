#!/usr/bin/env python3
"""
Strands Base Agent
Base class following Strands Agent best practices for all Excel Agent system agents
"""

import os
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime
from pathlib import Path
import traceback

class StrandsBaseAgent(ABC):
    """
    Base class for all agents following Strands Agent best practices.
    
    This class provides:
    - Model-driven development pattern
    - Comprehensive error handling
    - Structured logging
    - Configuration management
    - Data validation
    - Training data integration
    - Performance monitoring
    """
    
    def __init__(self, 
                 name: str,
                 config: Optional[Dict[str, Any]] = None,
                 training_data_path: Optional[str] = None,
                 log_level: str = "INFO"):
        """
        Initialize the base agent with Strands Agent best practices.
        
        Args:
            name: Agent name for identification
            config: Configuration dictionary
            training_data_path: Path to training data directory
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        """
        self.name = name
        self.config = config or {}
        self.training_data_path = Path(training_data_path) if training_data_path else None
        self.start_time = datetime.now()
        
        # Initialize logging
        self._setup_logging(log_level)
        
        # Initialize training data
        self.training_data = {}
        self._load_training_data()
        
        # Initialize performance metrics
        self.metrics = {
            "executions": 0,
            "successes": 0,
            "failures": 0,
            "total_execution_time": 0,
            "average_execution_time": 0
        }
        
        self.logger.info(f"Initialized {self.name} agent")
    
    def _setup_logging(self, log_level: str):
        """Setup structured logging for the agent."""
        self.logger = logging.getLogger(f"strands_agent.{self.name}")
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Create handler if not exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def _load_training_data(self):
        """Load training data for the agent."""
        if not self.training_data_path or not self.training_data_path.exists():
            self.logger.warning(f"No training data path provided or path doesn't exist: {self.training_data_path}")
            return
        
        try:
            # Load OP manual data
            op_manual_path = self.training_data_path / "op_manual.json"
            if op_manual_path.exists():
                with open(op_manual_path, 'r') as f:
                    self.training_data["op_manual"] = json.load(f)
                self.logger.info("Loaded OP manual training data")
            
            # Load historical patterns
            patterns_path = self.training_data_path / "historical_patterns.json"
            if patterns_path.exists():
                with open(patterns_path, 'r') as f:
                    self.training_data["historical_patterns"] = json.load(f)
                self.logger.info("Loaded historical patterns training data")
            
            # Load configuration rules
            rules_path = self.training_data_path / "reconciliation_rules.json"
            if rules_path.exists():
                with open(rules_path, 'r') as f:
                    self.training_data["reconciliation_rules"] = json.load(f)
                self.logger.info("Loaded reconciliation rules training data")
                
        except Exception as e:
            self.logger.error(f"Error loading training data: {str(e)}")
            self.training_data = {}
    
    @abstractmethod
    def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Process input data and return results.
        
        This is the main processing method that must be implemented by subclasses.
        
        Args:
            input_data: Input data to process
            
        Returns:
            Dictionary containing processing results
        """
        pass
    
    def validate_input(self, input_data: Any) -> Tuple[bool, List[str]]:
        """
        Validate input data format and content.
        
        Args:
            input_data: Input data to validate
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        if input_data is None:
            errors.append("Input data cannot be None")
        
        # Add specific validation logic in subclasses
        return len(errors) == 0, errors
    
    def execute_with_monitoring(self, input_data: Any) -> Dict[str, Any]:
        """
        Execute the agent with comprehensive monitoring and error handling.
        
        Args:
            input_data: Input data to process
            
        Returns:
            Dictionary containing execution results
        """
        execution_id = f"{self.name}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        start_time = datetime.now()
        
        self.logger.info(f"Starting execution {execution_id}")
        
        try:
            # Validate input
            is_valid, errors = self.validate_input(input_data)
            if not is_valid:
                raise ValueError(f"Input validation failed: {', '.join(errors)}")
            
            # Execute processing
            result = self.process(input_data)
            
            # Update metrics
            execution_time = (datetime.now() - start_time).total_seconds()
            self._update_metrics(success=True, execution_time=execution_time)
            
            self.logger.info(f"Execution {execution_id} completed successfully in {execution_time:.2f}s")
            
            return {
                "status": "success",
                "execution_id": execution_id,
                "execution_time": execution_time,
                "result": result,
                "agent_name": self.name,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            # Update metrics
            execution_time = (datetime.now() - start_time).total_seconds()
            self._update_metrics(success=False, execution_time=execution_time)
            
            error_info = {
                "error_type": type(e).__name__,
                "error_message": str(e),
                "traceback": traceback.format_exc()
            }
            
            self.logger.error(f"Execution {execution_id} failed: {str(e)}")
            self.logger.debug(f"Full traceback: {traceback.format_exc()}")
            
            return {
                "status": "error",
                "execution_id": execution_id,
                "execution_time": execution_time,
                "error": error_info,
                "agent_name": self.name,
                "timestamp": datetime.now().isoformat()
            }
    
    def _update_metrics(self, success: bool, execution_time: float):
        """Update performance metrics."""
        self.metrics["executions"] += 1
        self.metrics["total_execution_time"] += execution_time
        self.metrics["average_execution_time"] = (
            self.metrics["total_execution_time"] / self.metrics["executions"]
        )
        
        if success:
            self.metrics["successes"] += 1
        else:
            self.metrics["failures"] += 1
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current agent status and metrics.
        
        Returns:
            Dictionary containing agent status information
        """
        uptime = (datetime.now() - self.start_time).total_seconds()
        success_rate = (
            self.metrics["successes"] / self.metrics["executions"] * 100
            if self.metrics["executions"] > 0 else 0
        )
        
        return {
            "agent_name": self.name,
            "status": "running",
            "uptime_seconds": uptime,
            "metrics": self.metrics.copy(),
            "success_rate": success_rate,
            "training_data_loaded": len(self.training_data) > 0,
            "config": self.config,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_training_data(self, data_type: str) -> Optional[Dict[str, Any]]:
        """
        Get specific training data by type.
        
        Args:
            data_type: Type of training data to retrieve
            
        Returns:
            Training data dictionary or None if not found
        """
        return self.training_data.get(data_type)
    
    def update_training_data(self, data_type: str, data: Dict[str, Any]):
        """
        Update training data for continuous learning.
        
        Args:
            data_type: Type of training data to update
            data: New training data
        """
        self.training_data[data_type] = data
        self.logger.info(f"Updated training data for type: {data_type}")
    
    def save_training_data(self, output_path: Optional[str] = None):
        """
        Save current training data to file.
        
        Args:
            output_path: Path to save training data (optional)
        """
        if not output_path:
            output_path = f"{self.name}_training_data.json"
        
        try:
            with open(output_path, 'w') as f:
                json.dump(self.training_data, f, indent=2, default=str)
            self.logger.info(f"Saved training data to {output_path}")
        except Exception as e:
            self.logger.error(f"Error saving training data: {str(e)}")
    
    def reset_metrics(self):
        """Reset performance metrics."""
        self.metrics = {
            "executions": 0,
            "successes": 0,
            "failures": 0,
            "total_execution_time": 0,
            "average_execution_time": 0
        }
        self.logger.info("Reset performance metrics")
    
    def __str__(self) -> str:
        """String representation of the agent."""
        return f"StrandsAgent(name={self.name}, status=running, executions={self.metrics['executions']})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the agent."""
        return f"StrandsAgent(name={self.name}, config={self.config}, training_data_types={list(self.training_data.keys())})"


class StrandsReconciliationAgent(StrandsBaseAgent):
    """
    Specialized reconciliation agent following Strands Agent best practices.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None, training_data_path: Optional[str] = None):
        super().__init__(
            name="ReconciliationAgent",
            config=config,
            training_data_path=training_data_path
        )
        
        # Load reconciliation-specific training data
        self._load_reconciliation_training_data()
    
    def _load_reconciliation_training_data(self):
        """Load reconciliation-specific training data."""
        # Load OP manual if available
        op_manual = self.get_training_data("op_manual")
        if not op_manual:
            # Fallback to default OP manual
            op_manual = self._get_default_op_manual()
            self.update_training_data("op_manual", op_manual)
    
    def _get_default_op_manual(self) -> Dict[str, Any]:
        """Get default OP manual data as fallback."""
        return {
            "gl_accounts": {
                "74400": {"name": "RBC Activity", "bank_activities": ["RBC activity", "EFUNDS Corp – FEE SETTLE"]},
                "74505": {"name": "CNS Settlement", "bank_activities": ["CNS Settlement activity", "PULSE FEES activity"]},
                "74510": {"name": "EFUNDS Corp Daily Settlement", "bank_activities": ["EFUNDS Corp – DLY SETTLE activity"]},
                "74520": {"name": "Image Check Presentment", "bank_activities": ["1591 Image CL Presentment activity"]},
                "74530": {"name": "ACH Activity", "bank_activities": ["ACH ADV File activity"]},
                "74540": {"name": "CRIF Loans", "bank_activities": ["ACH ADV FILE - Orig CR activity (CRIF loans)"]},
                "74550": {"name": "Cooperative Business", "bank_activities": ["Cooperative Business activity"]},
                "74560": {"name": "Check Deposits", "bank_activities": ["1590 Image CL Presentment activity (deposits)"]},
                "74570": {"name": "ACH Returns", "bank_activities": ["ACH ADV FILE - Orig DB activity (ACH returns)"]}
            },
            "timing_differences": {
                "74505": {"description": "ATM settlement activity posted to GL on last day of month", "expected": True},
                "74510": {"description": "Shared Branching activity recorded in GL on last day of month", "expected": True},
                "74560": {"description": "Check deposit activity at branches posted to GL on last day of month", "expected": True}
            }
        }
    
    def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Process reconciliation data.
        
        Args:
            input_data: Dictionary containing GL and bank file paths
            
        Returns:
            Reconciliation results
        """
        # This is a template - implement specific reconciliation logic
        return {
            "reconciliation_status": "processed",
            "gl_file": input_data.get("gl_file"),
            "bank_file": input_data.get("bank_file"),
            "timestamp": datetime.now().isoformat()
        }
    
    def validate_input(self, input_data: Any) -> Tuple[bool, List[str]]:
        """Validate reconciliation input data."""
        errors = []
        
        if not isinstance(input_data, dict):
            errors.append("Input data must be a dictionary")
            return False, errors
        
        if "gl_file" not in input_data:
            errors.append("GL file path is required")
        
        if "bank_file" not in input_data:
            errors.append("Bank file path is required")
        
        return len(errors) == 0, errors


# Example usage and testing
if __name__ == "__main__":
    # Example usage
    config = {
        "log_level": "INFO",
        "max_execution_time": 300,
        "retry_attempts": 3
    }
    
    agent = StrandsReconciliationAgent(
        config=config,
        training_data_path="training_data"
    )
    
    # Test execution
    test_input = {
        "gl_file": "test_gl.xlsx",
        "bank_file": "test_bank.xlsx"
    }
    
    result = agent.execute_with_monitoring(test_input)
    print(f"Execution result: {result}")
    
    # Get status
    status = agent.get_status()
    print(f"Agent status: {status}")
