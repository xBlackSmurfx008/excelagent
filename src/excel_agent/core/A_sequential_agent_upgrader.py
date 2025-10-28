#!/usr/bin/env python3
"""
Sequential Agent Upgrader
Upgrades all AI agents and tools using training document insights in proper sequence
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import openai
from pathlib import Path

class SequentialAgentUpgrader:
    def __init__(self, api_key: str = None):
        """Initialize the Sequential Agent Upgrader"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        self.training_insights = self._load_training_insights()
        self.agent_sequence = self._define_agent_sequence()
        self.upgrade_results = {}
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def _load_training_insights(self) -> Dict[str, Any]:
        """Load the training document insights"""
        try:
            with open("training_document_deep_analysis_20251026_181256.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading training insights: {e}")
            return {}
    
    def _define_agent_sequence(self) -> List[Dict[str, Any]]:
        """Define the proper sequence for agent execution based on OP training document"""
        return [
            {
                "name": "Data Quality Validator",
                "file": "data_quality_validator.py",
                "priority": 1,
                "description": "Validates data quality before any processing",
                "training_requirements": ["data_quality_requirements", "validation_procedures"]
            },
            {
                "name": "GL Extraction Agent",
                "file": "gl_extraction_agent.py", 
                "priority": 2,
                "description": "Extracts GL histories for both branches",
                "training_requirements": ["gl_extraction_procedures", "branch_handling"]
            },
            {
                "name": "Bank Statement Processor",
                "file": "bank_statement_processor.py",
                "priority": 3,
                "description": "Processes NCB bank statements",
                "training_requirements": ["bank_statement_processing", "transaction_parsing"]
            },
            {
                "name": "Reconciliation Matcher",
                "file": "reconciliation_matcher.py",
                "priority": 4,
                "description": "Matches GL transactions with bank transactions",
                "training_requirements": ["matching_criteria", "transaction_matching"]
            },
            {
                "name": "Timing Difference Handler",
                "file": "timing_difference_handler.py",
                "priority": 5,
                "description": "Handles timing differences and carry-over entries",
                "training_requirements": ["timing_differences", "carry_over_entries"]
            },
            {
                "name": "Variance Analyzer",
                "file": "variance_analyzer.py",
                "priority": 6,
                "description": "Analyzes variances and discrepancies",
                "training_requirements": ["variance_analysis", "discrepancy_detection"]
            },
            {
                "name": "Reconciliation Validator",
                "file": "reconciliation_validator.py",
                "priority": 7,
                "description": "Validates final reconciliation balance",
                "training_requirements": ["balance_validation", "reconciliation_verification"]
            },
            {
                "name": "Report Generator",
                "file": "report_generator.py",
                "priority": 8,
                "description": "Generates comprehensive reconciliation reports",
                "training_requirements": ["reporting_standards", "documentation"]
            }
        ]
    
    def extract_training_requirements(self, requirements: List[str]) -> Dict[str, Any]:
        """Extract specific training requirements for an agent"""
        extracted = {}
        
        for req in requirements:
            if req in self.training_insights:
                extracted[req] = self.training_insights[req]
        
        return extracted
    
    def upgrade_agent(self, agent_info: Dict[str, Any]) -> Dict[str, Any]:
        """Upgrade a single agent using training document insights"""
        agent_name = agent_info["name"]
        agent_file = agent_info["file"]
        
        self.logger.info(f"Upgrading agent: {agent_name}")
        
        # Extract training requirements
        training_reqs = self.extract_training_requirements(agent_info["training_requirements"])
        
        # Create upgrade prompt
        upgrade_prompt = f"""
        Upgrade the following agent to be fully compliant with OP reconciliation training document insights.
        
        Agent Name: {agent_name}
        Agent File: {agent_file}
        Description: {agent_info["description"]}
        
        Training Document Insights:
        {json.dumps(training_reqs, indent=2)}
        
        Key Training Requirements:
        1. Daily reconciliation process due to high transaction volume
        2. GL extraction for both branches with proper organization
        3. Month-end balance management in column O
        4. Transaction reconciliation with specific GL mappings
        5. Timing differences handling (ATM, shared branching, check deposits, gift cards)
        6. Variance analysis with proper thresholds
        7. Data quality validation and error handling
        8. Automation opportunities implementation
        9. Proper documentation and audit trails
        10. Segregation of duties and security measures
        
        Please create a complete, production-ready agent that:
        - Implements ALL training document requirements
        - Has proper error handling and validation
        - Includes comprehensive logging
        - Follows best practices for financial reconciliation
        - Is fully compliant with OP procedures
        - Has clear documentation and comments
        - Includes unit tests
        - Handles edge cases and exceptions
        - Provides detailed audit trails
        
        Generate the complete Python code for this agent.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert Python developer specializing in financial reconciliation systems. Create production-ready, compliant code."},
                    {"role": "user", "content": upgrade_prompt}
                ],
                max_tokens=4000,
                temperature=0.2
            )
            
            upgrade_result = {
                "agent_name": agent_name,
                "agent_file": agent_file,
                "upgrade_timestamp": datetime.now().isoformat(),
                "upgraded_code": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens if response.usage else 0,
                "training_compliance": self._assess_training_compliance(response.choices[0].message.content),
                "priority": agent_info["priority"]
            }
            
            self.logger.info(f"Completed upgrade for {agent_name}")
            return upgrade_result
            
        except Exception as e:
            self.logger.error(f"Error upgrading {agent_name}: {e}")
            return {
                "agent_name": agent_name,
                "agent_file": agent_file,
                "upgrade_timestamp": datetime.now().isoformat(),
                "upgraded_code": f"Error during upgrade: {str(e)}",
                "tokens_used": 0,
                "training_compliance": 0,
                "priority": agent_info["priority"]
            }
    
    def _assess_training_compliance(self, code: str) -> int:
        """Assess compliance with training document requirements (1-10)"""
        compliance_score = 0
        
        # Check for key training requirements
        training_checks = [
            ("daily reconciliation", "daily" in code.lower()),
            ("gl extraction", "gl" in code.lower() and "extract" in code.lower()),
            ("bank statement", "bank" in code.lower() and "statement" in code.lower()),
            ("timing differences", "timing" in code.lower() and "difference" in code.lower()),
            ("variance analysis", "variance" in code.lower() and "analysis" in code.lower()),
            ("data quality", "data" in code.lower() and "quality" in code.lower()),
            ("error handling", "error" in code.lower() and "handling" in code.lower()),
            ("logging", "log" in code.lower()),
            ("validation", "valid" in code.lower()),
            ("automation", "auto" in code.lower())
        ]
        
        for check_name, check_result in training_checks:
            if check_result:
                compliance_score += 1
        
        return compliance_score
    
    def run_sequential_upgrade(self) -> Dict[str, Any]:
        """Run sequential upgrade of all agents"""
        self.logger.info("Starting sequential agent upgrade process...")
        
        upgrade_results = []
        total_tokens = 0
        total_compliance = 0
        
        # Sort agents by priority
        sorted_agents = sorted(self.agent_sequence, key=lambda x: x["priority"])
        
        for agent_info in sorted_agents:
            self.logger.info(f"Upgrading agent {agent_info['priority']}: {agent_info['name']}")
            result = self.upgrade_agent(agent_info)
            upgrade_results.append(result)
            total_tokens += result.get('tokens_used', 0)
            total_compliance += result.get('training_compliance', 0)
            
            # Small delay to avoid rate limiting
            import time
            time.sleep(3)
        
        # Calculate overall statistics
        avg_compliance = total_compliance / len(upgrade_results) if upgrade_results else 0
        
        comprehensive_results = {
            "upgrade_timestamp": datetime.now().isoformat(),
            "total_agents_upgraded": len(upgrade_results),
            "total_tokens_used": total_tokens,
            "average_compliance_score": round(avg_compliance, 2),
            "agent_upgrades": upgrade_results,
            "sequence_order": [agent["name"] for agent in sorted_agents],
            "summary": self._generate_upgrade_summary(upgrade_results)
        }
        
        self.upgrade_results = comprehensive_results
        self.logger.info(f"Completed sequential upgrade: {len(upgrade_results)} agents, avg compliance {avg_compliance:.2f}/10")
        
        return comprehensive_results
    
    def _generate_upgrade_summary(self, upgrade_results: List[Dict]) -> Dict[str, Any]:
        """Generate summary of upgrade results"""
        compliance_scores = [r.get('training_compliance', 0) for r in upgrade_results]
        
        return {
            "total_agents": len(upgrade_results),
            "average_compliance": round(sum(compliance_scores) / len(compliance_scores), 2) if compliance_scores else 0,
            "highest_compliance": max(compliance_scores) if compliance_scores else 0,
            "lowest_compliance": min(compliance_scores) if compliance_scores else 0,
            "fully_compliant_agents": len([s for s in compliance_scores if s >= 9]),
            "needs_improvement": len([s for s in compliance_scores if s < 7]),
            "compliance_distribution": {
                "excellent (9-10)": len([s for s in compliance_scores if s >= 9]),
                "good (7-8)": len([s for s in compliance_scores if 7 <= s < 9]),
                "fair (5-6)": len([s for s in compliance_scores if 5 <= s < 7]),
                "poor (1-4)": len([s for s in compliance_scores if s < 5])
            }
        }
    
    def save_upgraded_agents(self) -> List[str]:
        """Save all upgraded agents to files"""
        saved_files = []
        
        for upgrade in self.upgrade_results.get('agent_upgrades', []):
            agent_name = upgrade['agent_name']
            agent_file = upgrade['agent_file']
            upgraded_code = upgrade['upgraded_code']
            
            # Clean up the code (remove markdown formatting if present)
            if "```python" in upgraded_code:
                code_start = upgraded_code.find("```python") + 9
                code_end = upgraded_code.find("```", code_start)
                if code_end != -1:
                    upgraded_code = upgraded_code[code_start:code_end].strip()
            elif "```" in upgraded_code:
                code_start = upgraded_code.find("```") + 3
                code_end = upgraded_code.find("```", code_start)
                if code_end != -1:
                    upgraded_code = upgraded_code[code_start:code_end].strip()
            
            # Save to file
            with open(agent_file, 'w', encoding='utf-8') as f:
                f.write(upgraded_code)
            
            saved_files.append(agent_file)
            self.logger.info(f"Saved upgraded agent: {agent_file}")
        
        return saved_files
    
    def save_results(self, filename: str = None) -> str:
        """Save the upgrade results to a file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"sequential_agent_upgrade_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.upgrade_results, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Upgrade results saved to: {filename}")
        return filename
    
    def generate_summary_report(self) -> str:
        """Generate a human-readable summary report"""
        if not self.upgrade_results:
            return "No upgrade results available. Run upgrade first."
        
        summary = self.upgrade_results.get('summary', {})
        sequence = self.upgrade_results.get('sequence_order', [])
        
        report = f"""
# Sequential Agent Upgrade Report

## Upgrade Overview
- **Upgrade Date**: {self.upgrade_results.get('upgrade_timestamp', 'Unknown')}
- **Total Agents Upgraded**: {summary.get('total_agents', 0)}
- **Average Compliance Score**: {summary.get('average_compliance', 0)}/10
- **Highest Compliance**: {summary.get('highest_compliance', 0)}/10
- **Lowest Compliance**: {summary.get('lowest_compliance', 0)}/10

## Execution Sequence
"""
        
        for i, agent_name in enumerate(sequence, 1):
            report += f"{i}. {agent_name}\n"
        
        report += "\n## Compliance Distribution\n"
        dist = summary.get('compliance_distribution', {})
        report += f"- **Excellent (9-10)**: {dist.get('excellent (9-10)', 0)} agents\n"
        report += f"- **Good (7-8)**: {dist.get('good (7-8)', 0)} agents\n"
        report += f"- **Fair (5-6)**: {dist.get('fair (5-6)', 0)} agents\n"
        report += f"- **Poor (1-4)**: {dist.get('poor (1-4)', 0)} agents\n"
        
        report += "\n## Individual Agent Results\n"
        for upgrade in self.upgrade_results.get('agent_upgrades', []):
            report += f"\n### {upgrade.get('agent_name', 'Unknown')}\n"
            report += f"- **File**: {upgrade.get('agent_file', 'Unknown')}\n"
            report += f"- **Compliance Score**: {upgrade.get('training_compliance', 0)}/10\n"
            report += f"- **Priority**: {upgrade.get('priority', 'Unknown')}\n"
        
        return report

def main():
    """Main execution function"""
    try:
        # Initialize the upgrader
        upgrader = SequentialAgentUpgrader()
        
        # Run sequential upgrade
        print("🚀 Starting Sequential Agent Upgrade...")
        print("📋 Using training document insights for upgrades...")
        print(f"🔄 Upgrading {len(upgrader.agent_sequence)} agents in sequence...")
        
        results = upgrader.run_sequential_upgrade()
        
        # Save upgraded agents
        saved_files = upgrader.save_upgraded_agents()
        print(f"💾 Saved {len(saved_files)} upgraded agents")
        
        # Save results
        json_file = upgrader.save_results()
        print(f"💾 Upgrade results saved to: {json_file}")
        
        # Generate and save summary report
        summary = upgrader.generate_summary_report()
        summary_file = f"sequential_agent_upgrade_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        print(f"📋 Summary report saved to: {summary_file}")
        
        print("\n✅ Sequential Agent Upgrade Complete!")
        print(f"📊 Total Agents: {results['total_agents_upgraded']}")
        print(f"🎯 Average Compliance: {results['average_compliance_score']}/10")
        print(f"📁 Saved Files: {len(saved_files)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
