
#!/usr/bin/env python3
"""
Integration tests for agent interactions
"""

import unittest
import json
from pathlib import Path
from improved_ai_reconciliation_agent import ImprovedAIReconciliationAgent
from improved_data_consolidation_agent import ImprovedDataConsolidationAgent
from improved_high_variance_investigator import ImprovedHighVarianceInvestigator
from improved_bank_cross_match_agent import ImprovedBankCrossMatchAgent
from improved_enhanced_thinking_agent import ImprovedEnhancedThinkingAgent
from improved_vision_enhanced_ai_agent import ImprovedVisionEnhancedAIAgent

class TestAgentIntegration(unittest.TestCase):
    """Test cases for agent integration."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = {
            "log_level": "DEBUG",
            "max_execution_time": 60,
            "retry_attempts": 1
        }
        self.training_data_path = "test_training_data"
        
        # Initialize all agents
        self.agents = {
            "reconciliation": ImprovedAIReconciliationAgent(
                config=self.config,
                training_data_path=self.training_data_path
            ),
            "consolidation": ImprovedDataConsolidationAgent(
                config=self.config,
                training_data_path=self.training_data_path
            ),
            "variance_investigator": ImprovedHighVarianceInvestigator(
                config=self.config,
                training_data_path=self.training_data_path
            ),
            "bank_cross_match": ImprovedBankCrossMatchAgent(
                config=self.config,
                training_data_path=self.training_data_path
            ),
            "thinking": ImprovedEnhancedThinkingAgent(
                config=self.config,
                training_data_path=self.training_data_path
            ),
            "vision": ImprovedVisionEnhancedAIAgent(
                config=self.config,
                training_data_path=self.training_data_path
            )
        }
    
    def test_agent_initialization(self):
        """Test that all agents initialize correctly."""
        for agent_name, agent in self.agents.items():
            with self.subTest(agent=agent_name):
                self.assertIsNotNone(agent)
                self.assertIsNotNone(agent.get_status())
    
    def test_agent_status_consistency(self):
        """Test that all agents have consistent status format."""
        for agent_name, agent in self.agents.items():
            with self.subTest(agent=agent_name):
                status = agent.get_status()
                self.assertIn("agent_name", status)
                self.assertIn("status", status)
                self.assertIn("uptime_seconds", status)
                self.assertIn("metrics", status)
    
    def test_training_data_integration(self):
        """Test that all agents integrate training data correctly."""
        for agent_name, agent in self.agents.items():
            with self.subTest(agent=agent_name):
                # Test that agents can access training data
                op_manual = agent.get_training_data("op_manual")
                self.assertIsNotNone(op_manual)
                
                historical_patterns = agent.get_training_data("historical_patterns")
                self.assertIsNotNone(historical_patterns)

if __name__ == "__main__":
    unittest.main()
