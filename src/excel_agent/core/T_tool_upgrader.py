#!/usr/bin/env python3
"""
Tool Upgrader
Upgrades all tools to integrate training document insights
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import openai
from pathlib import Path

class ToolUpgrader:
    def __init__(self, api_key: str = None):
        """Initialize the Tool Upgrader"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        self.training_insights = self._load_training_insights()
        self.tools_to_upgrade = self._identify_tools()
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
    
    def _identify_tools(self) -> List[Dict[str, Any]]:
        """Identify all tools that need upgrading"""
        tools = []
        current_dir = Path(".")
        
        # Look for tool files (non-agent Python files)
        for file_path in current_dir.glob("*.py"):
            if file_path.name not in [
                "sequential_agent_upgrader.py", "line_by_line_reviewer.py", "tool_upgrader.py",
                "agent_accuracy_reviewer.py", "training_document_deep_thinker.py",
                "master_deep_thinking_orchestrator.py", "deep_thinking_orchestrator.py",
                "training_document_analyzer.py", "master_orchestrator.py"
            ] and not file_path.name.startswith("test_") and not file_path.name.startswith("agent_"):
                tools.append({
                    "name": file_path.stem,
                    "file": str(file_path),
                    "type": self._classify_tool_type(file_path)
                })
        
        return tools
    
    def _classify_tool_type(self, file_path: Path) -> str:
        """Classify the type of tool"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "reconciliation" in content.lower():
                return "reconciliation_tool"
            elif "validation" in content.lower():
                return "validation_tool"
            elif "analysis" in content.lower():
                return "analysis_tool"
            elif "report" in content.lower():
                return "reporting_tool"
            elif "data" in content.lower():
                return "data_tool"
            else:
                return "utility_tool"
        except:
            return "unknown_tool"
    
    def upgrade_tool(self, tool_info: Dict[str, Any]) -> Dict[str, Any]:
        """Upgrade a single tool using training document insights"""
        tool_name = tool_info["name"]
        tool_file = tool_info["file"]
        tool_type = tool_info["type"]
        
        self.logger.info(f"Upgrading tool: {tool_name}")
        
        try:
            # Read the current tool
            with open(tool_file, 'r', encoding='utf-8') as f:
                current_code = f.read()
            
            # Create upgrade prompt based on tool type
            upgrade_prompt = self._create_tool_upgrade_prompt(tool_name, tool_type, current_code)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert Python developer specializing in financial reconciliation tools. Create production-ready, OP-compliant code."},
                    {"role": "user", "content": upgrade_prompt}
                ],
                max_tokens=3000,
                temperature=0.2
            )
            
            upgrade_result = {
                "tool_name": tool_name,
                "tool_file": tool_file,
                "tool_type": tool_type,
                "upgrade_timestamp": datetime.now().isoformat(),
                "upgraded_code": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens if response.usage else 0,
                "training_compliance": self._assess_tool_compliance(response.choices[0].message.content),
                "improvements_made": self._identify_improvements(current_code, response.choices[0].message.content)
            }
            
            self.logger.info(f"Completed upgrade for {tool_name}")
            return upgrade_result
            
        except Exception as e:
            self.logger.error(f"Error upgrading {tool_name}: {e}")
            return {
                "tool_name": tool_name,
                "tool_file": tool_file,
                "tool_type": tool_type,
                "upgrade_timestamp": datetime.now().isoformat(),
                "upgraded_code": f"Error during upgrade: {str(e)}",
                "tokens_used": 0,
                "training_compliance": 0,
                "improvements_made": []
            }
    
    def _create_tool_upgrade_prompt(self, tool_name: str, tool_type: str, current_code: str) -> str:
        """Create upgrade prompt based on tool type"""
        
        base_prompt = f"""
        Upgrade the following {tool_type} to be fully compliant with OP reconciliation training document insights.
        
        Tool Name: {tool_name}
        Tool Type: {tool_type}
        
        Training Document Insights:
        {json.dumps(self.training_insights, indent=2)}
        
        Current Tool Code:
        {current_code[:2000]}  # Limit to avoid token limits
        
        Key OP Requirements to Implement:
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
        
        Please create a complete, production-ready tool that:
        - Implements ALL relevant training document requirements
        - Has proper error handling and validation
        - Includes comprehensive logging
        - Follows best practices for financial reconciliation
        - Is fully compliant with OP procedures
        - Has clear documentation and comments
        - Includes unit tests
        - Handles edge cases and exceptions
        - Provides detailed audit trails
        - Integrates seamlessly with the agent system
        """
        
        # Add specific requirements based on tool type
        if tool_type == "reconciliation_tool":
            base_prompt += "\n\nSpecific Reconciliation Tool Requirements:\n- Implement transaction matching logic\n- Handle timing differences\n- Validate reconciliation balances\n- Generate reconciliation reports"
        elif tool_type == "validation_tool":
            base_prompt += "\n\nSpecific Validation Tool Requirements:\n- Validate data quality\n- Check GL balances\n- Verify transaction integrity\n- Ensure compliance with OP procedures"
        elif tool_type == "analysis_tool":
            base_prompt += "\n\nSpecific Analysis Tool Requirements:\n- Analyze variances and discrepancies\n- Identify patterns and trends\n- Generate insights and recommendations\n- Support decision making"
        elif tool_type == "reporting_tool":
            base_prompt += "\n\nSpecific Reporting Tool Requirements:\n- Generate comprehensive reports\n- Include audit trails\n- Support multiple formats\n- Ensure accuracy and completeness"
        elif tool_type == "data_tool":
            base_prompt += "\n\nSpecific Data Tool Requirements:\n- Handle data extraction and processing\n- Ensure data quality\n- Support multiple formats\n- Provide data validation"
        
        return base_prompt
    
    def _assess_tool_compliance(self, code: str) -> int:
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
            ("automation", "auto" in code.lower()),
            ("audit trail", "audit" in code.lower()),
            ("documentation", "doc" in code.lower() or "comment" in code.lower())
        ]
        
        for check_name, check_result in training_checks:
            if check_result:
                compliance_score += 1
        
        return min(compliance_score, 10)  # Cap at 10
    
    def _identify_improvements(self, old_code: str, new_code: str) -> List[str]:
        """Identify improvements made in the upgrade"""
        improvements = []
        
        old_lower = old_code.lower()
        new_lower = new_code.lower()
        
        # Check for specific improvements
        if "error handling" in new_lower and "error handling" not in old_lower:
            improvements.append("Added comprehensive error handling")
        
        if "logging" in new_lower and "logging" not in old_lower:
            improvements.append("Added detailed logging")
        
        if "validation" in new_lower and "validation" not in old_lower:
            improvements.append("Added data validation")
        
        if "automation" in new_lower and "automation" not in old_lower:
            improvements.append("Added automation features")
        
        if "audit" in new_lower and "audit" not in old_lower:
            improvements.append("Added audit trail functionality")
        
        if "test" in new_lower and "test" not in old_lower:
            improvements.append("Added unit tests")
        
        if "doc" in new_lower and "doc" not in old_lower:
            improvements.append("Added comprehensive documentation")
        
        return improvements
    
    def run_comprehensive_tool_upgrade(self) -> Dict[str, Any]:
        """Run comprehensive upgrade of all tools"""
        self.logger.info("Starting comprehensive tool upgrade process...")
        
        upgrade_results = []
        total_tokens = 0
        total_compliance = 0
        
        for tool_info in self.tools_to_upgrade:
            self.logger.info(f"Upgrading tool: {tool_info['name']}")
            result = self.upgrade_tool(tool_info)
            upgrade_results.append(result)
            total_tokens += result.get('tokens_used', 0)
            total_compliance += result.get('training_compliance', 0)
            
            # Small delay to avoid rate limiting
            import time
            time.sleep(2)
        
        # Calculate overall statistics
        avg_compliance = total_compliance / len(upgrade_results) if upgrade_results else 0
        
        comprehensive_results = {
            "upgrade_timestamp": datetime.now().isoformat(),
            "total_tools_upgraded": len(upgrade_results),
            "total_tokens_used": total_tokens,
            "average_compliance_score": round(avg_compliance, 2),
            "tool_upgrades": upgrade_results,
            "summary": self._generate_tool_upgrade_summary(upgrade_results)
        }
        
        self.upgrade_results = comprehensive_results
        self.logger.info(f"Completed tool upgrade: {len(upgrade_results)} tools, avg compliance {avg_compliance:.2f}/10")
        
        return comprehensive_results
    
    def _generate_tool_upgrade_summary(self, upgrade_results: List[Dict]) -> Dict[str, Any]:
        """Generate summary of tool upgrade results"""
        compliance_scores = [r.get('training_compliance', 0) for r in upgrade_results]
        
        return {
            "total_tools": len(upgrade_results),
            "average_compliance": round(sum(compliance_scores) / len(compliance_scores), 2) if compliance_scores else 0,
            "highest_compliance": max(compliance_scores) if compliance_scores else 0,
            "lowest_compliance": min(compliance_scores) if compliance_scores else 0,
            "fully_compliant_tools": len([s for s in compliance_scores if s >= 9]),
            "needs_improvement": len([s for s in compliance_scores if s < 7]),
            "compliance_distribution": {
                "excellent (9-10)": len([s for s in compliance_scores if s >= 9]),
                "good (7-8)": len([s for s in compliance_scores if 7 <= s < 9]),
                "fair (5-6)": len([s for s in compliance_scores if 5 <= s < 7]),
                "poor (1-4)": len([s for s in compliance_scores if s < 5])
            }
        }
    
    def save_upgraded_tools(self) -> List[str]:
        """Save all upgraded tools to files"""
        saved_files = []
        
        for upgrade in self.upgrade_results.get('tool_upgrades', []):
            tool_name = upgrade['tool_name']
            tool_file = upgrade['tool_file']
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
            with open(tool_file, 'w', encoding='utf-8') as f:
                f.write(upgraded_code)
            
            saved_files.append(tool_file)
            self.logger.info(f"Saved upgraded tool: {tool_file}")
        
        return saved_files
    
    def save_results(self, filename: str = None) -> str:
        """Save the upgrade results to a file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tool_upgrade_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.upgrade_results, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Tool upgrade results saved to: {filename}")
        return filename
    
    def generate_summary_report(self) -> str:
        """Generate a human-readable summary report"""
        if not self.upgrade_results:
            return "No upgrade results available. Run tool upgrade first."
        
        summary = self.upgrade_results.get('summary', {})
        
        report = f"""
# Tool Upgrade Report

## Upgrade Overview
- **Upgrade Date**: {self.upgrade_results.get('upgrade_timestamp', 'Unknown')}
- **Total Tools Upgraded**: {summary.get('total_tools', 0)}
- **Average Compliance Score**: {summary.get('average_compliance', 0)}/10
- **Highest Compliance**: {summary.get('highest_compliance', 0)}/10
- **Lowest Compliance**: {summary.get('lowest_compliance', 0)}/10

## Compliance Distribution
"""
        
        dist = summary.get('compliance_distribution', {})
        report += f"- **Excellent (9-10)**: {dist.get('excellent (9-10)', 0)} tools\n"
        report += f"- **Good (7-8)**: {dist.get('good (7-8)', 0)} tools\n"
        report += f"- **Fair (5-6)**: {dist.get('fair (5-6)', 0)} tools\n"
        report += f"- **Poor (1-4)**: {dist.get('poor (1-4)', 0)} tools\n"
        
        report += "\n## Individual Tool Results\n"
        for tool_upgrade in self.upgrade_results.get('tool_upgrades', []):
            report += f"\n### {tool_upgrade.get('tool_name', 'Unknown')}\n"
            report += f"- **File**: {tool_upgrade.get('tool_file', 'Unknown')}\n"
            report += f"- **Type**: {tool_upgrade.get('tool_type', 'Unknown')}\n"
            report += f"- **Compliance Score**: {tool_upgrade.get('training_compliance', 0)}/10\n"
            report += f"- **Improvements**: {', '.join(tool_upgrade.get('improvements_made', []))}\n"
        
        return report

def main():
    """Main execution function"""
    try:
        # Initialize the upgrader
        upgrader = ToolUpgrader()
        
        # Run comprehensive tool upgrade
        print("🔧 Starting Tool Upgrade...")
        print("📋 Using training document insights for tool upgrades...")
        print(f"🛠️ Found {len(upgrader.tools_to_upgrade)} tools to upgrade")
        
        results = upgrader.run_comprehensive_tool_upgrade()
        
        # Save upgraded tools
        saved_files = upgrader.save_upgraded_tools()
        print(f"💾 Saved {len(saved_files)} upgraded tools")
        
        # Save results
        json_file = upgrader.save_results()
        print(f"💾 Tool upgrade results saved to: {json_file}")
        
        # Generate and save summary report
        summary = upgrader.generate_summary_report()
        summary_file = f"tool_upgrade_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        print(f"📋 Summary report saved to: {summary_file}")
        
        print("\n✅ Tool Upgrade Complete!")
        print(f"📊 Total Tools: {results['total_tools_upgraded']}")
        print(f"🎯 Average Compliance: {results['average_compliance_score']}/10")
        print(f"📁 Saved Files: {len(saved_files)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
