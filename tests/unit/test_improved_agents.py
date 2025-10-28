
#!/usr/bin/env python3
"""
Unit tests for improved agents
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

class TestImprovedAgents(unittest.TestCase):
    """Test cases for improved agents."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = {
            "log_level": "DEBUG",
            "max_execution_time": 60,
            "retry_attempts": 1
        }
        self.training_data_path = "test_training_data"
    
    def test_ai_reconciliation_agent_initialization(self):
        """Test AI reconciliation agent initialization."""
        agent = ImprovedAIReconciliationAgent(
            config=self.config,
            training_data_path=self.training_data_path
        )
        self.assertEqual(agent.name, "ImprovedAIReconciliationAgent")
        self.assertIsNotNone(agent.get_status())
    
    def test_data_consolidation_agent_initialization(self):
        """Test data consolidation agent initialization."""
        agent = ImprovedDataConsolidationAgent(
            config=self.config,
            training_data_path=self.training_data_path
        )
        self.assertEqual(agent.name, "ImprovedDataConsolidationAgent")
        self.assertIsNotNone(agent.get_status())
    
    def test_high_variance_investigator_initialization(self):
        """Test high variance investigator initialization."""
        agent = ImprovedHighVarianceInvestigator(
            config=self.config,
            training_data_path=self.training_data_path
        )
        self.assertEqual(agent.name, "ImprovedHighVarianceInvestigator")
        self.assertIsNotNone(agent.get_status())
    
    def test_bank_cross_match_agent_initialization(self):
        """Test bank cross-match agent initialization."""
        agent = ImprovedBankCrossMatchAgent(
            config=self.config,
            training_data_path=self.training_data_path
        )
        self.assertEqual(agent.name, "ImprovedBankCrossMatchAgent")
        self.assertIsNotNone(agent.get_status())
    
    def test_enhanced_thinking_agent_initialization(self):
        """Test enhanced thinking agent initialization."""
        agent = ImprovedEnhancedThinkingAgent(
            config=self.config,
            training_data_path=self.training_data_path
        )
        self.assertEqual(agent.name, "ImprovedEnhancedThinkingAgent")
        self.assertIsNotNone(agent.get_status())
    
    def test_vision_enhanced_ai_agent_initialization(self):
        """Test vision enhanced AI agent initialization."""
        agent = ImprovedVisionEnhancedAIAgent(
            config=self.config,
            training_data_path=self.training_data_path
        )
        self.assertEqual(agent.name, "ImprovedVisionEnhancedAIAgent")
        self.assertIsNotNone(agent.get_status())

if __name__ == "__main__":
    unittest.main()
