
#!/usr/bin/env python3
"""
Performance testing for improved agents
"""

import time
import json
from pathlib import Path
from improved_ai_reconciliation_agent import ImprovedAIReconciliationAgent
from improved_data_consolidation_agent import ImprovedDataConsolidationAgent
from improved_high_variance_investigator import ImprovedHighVarianceInvestigator
from improved_bank_cross_match_agent import ImprovedBankCrossMatchAgent
from improved_enhanced_thinking_agent import ImprovedEnhancedThinkingAgent
from improved_vision_enhanced_ai_agent import ImprovedVisionEnhancedAIAgent

class PerformanceTester:
    """Performance testing for improved agents."""
    
    def __init__(self):
        self.config = {
            "log_level": "WARNING",  # Reduce logging for performance testing
            "max_execution_time": 300,
            "retry_attempts": 1
        }
        self.training_data_path = "test_training_data"
        
        # Initialize agents
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
    
    def run_performance_tests(self):
        """Run comprehensive performance tests."""
        print("🚀 Running performance tests for improved agents...")
        
        results = {}
        
        for agent_name, agent in self.agents.items():
            print(f"\n📊 Testing {agent_name}...")
            
            # Test initialization time
            start_time = time.time()
            status = agent.get_status()
            init_time = time.time() - start_time
            
            # Test execution time (with mock data)
            start_time = time.time()
            try:
                result = agent.execute_with_monitoring({"test": "data"})
                execution_time = time.time() - start_time
                success = result["status"] == "success"
            except Exception as e:
                execution_time = time.time() - start_time
                success = False
            
            results[agent_name] = {
                "initialization_time": init_time,
                "execution_time": execution_time,
                "success": success,
                "status": status
            }
            
            print(f"  ✅ Initialization: {init_time:.3f}s")
            print(f"  ✅ Execution: {execution_time:.3f}s")
            print(f"  ✅ Success: {success}")
        
        # Save results
        with open("performance_test_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n📄 Performance test results saved to: performance_test_results.json")
        return results

if __name__ == "__main__":
    tester = PerformanceTester()
    results = tester.run_performance_tests()
