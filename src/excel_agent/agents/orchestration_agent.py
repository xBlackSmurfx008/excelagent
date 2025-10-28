"""
Excel Agent - Orchestration Agent

Master agent that orchestrates all other agents in the system.
"""

from typing import Dict, Any, List
from datetime import datetime

class OrchestrationAgent:
    """Master orchestration agent"""
    
    def __init__(self):
        """Initialize orchestration agent"""
        self.name = "OrchestrationAgent"
        self.agents = {}
        self.execution_history = []
    
    def add_agent(self, name: str, agent):
        """Add an agent to orchestration"""
        self.agents[name] = agent
    
    def orchestrate(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrate execution of all agents
        
        Args:
            input_data: Input data for processing
            
        Returns:
            Dict containing orchestration results
        """
        results = {}
        
        for name, agent in self.agents.items():
            try:
                result = agent.run(input_data)
                results[name] = result
            except Exception as e:
                results[name] = {"status": "error", "error": str(e)}
        
        return {
            "status": "success",
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
