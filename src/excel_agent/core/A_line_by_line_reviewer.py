#!/usr/bin/env python3
"""
Line-by-Line Reviewer
Reviews each agent line by line for accuracy against OP training document
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import openai
from pathlib import Path
import ast
import re

class LineByLineReviewer:
    def __init__(self, api_key: str = None):
        """Initialize the Line-by-Line Reviewer"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        self.training_insights = self._load_training_insights()
        self.op_requirements = self._extract_op_requirements()
        self.review_results = {}
        
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
    
    def _extract_op_requirements(self) -> Dict[str, List[str]]:
        """Extract specific OP requirements from training document"""
        return {
            "daily_reconciliation": [
                "Daily reconciliation process due to high transaction volume",
                "Reconcile transactions daily to prevent errors from accumulating",
                "Timely identification and correction of discrepancies"
            ],
            "gl_extraction": [
                "Extract GL history for both branches",
                "Double-click GL number in blue twice to ensure both branches",
                "Export the table for each GL",
                "Organize each GL history in its own Excel tab",
                "Label each tab with GL number (74400, 74505, etc.)"
            ],
            "month_end_balances": [
                "Enter month-end balance for each GL in column O",
                "Current balance is highlighted in blue for each GL",
                "Balance per Books linked to cell O17",
                "Sum of month-end GL balances in GLs 74400 through 74570"
            ],
            "bank_statement_processing": [
                "Obtain month-end NCB statement from Networks Folder",
                "Navigate to Accounting > NCB Statements > Settlement Account",
                "Find ending balance boxed in Account Summary for CB Interest Settlement",
                "Enter ending balance in Balance per Statement cell"
            ],
            "transaction_matching": [
                "Reconcile each individual transaction with corresponding GL activity",
                "ACH ADV File activity reconciled with GL 74530",
                "ACH ADV FILE - Orig CR activity reconciled with GL 74540",
                "ACH ADV FILE - Orig DB activity reconciled with GL 74570",
                "RBC activity reconciled with GL 74400",
                "CNS Settlement activity reconciled with GL 74505",
                "EFUNDS Corp - DLY SETTLE reconciled with GL 74510",
                "EFUNDS Corp - FEE SETTLE reconciled with GL 74400",
                "PULSE FEES reconciled with GL 74505",
                "Withdrawal Coin/Currency reconciled with GL 74400",
                "1591 Image CL Presentment reconciled with GL 74520",
                "1590 Image CL Presentment reconciled with GL 74560 and 74525",
                "Cooperative Business reconciled with GL 74550",
                "Currency Exchange Payment reconciled with GL 74400",
                "ICUL ServCorp reconciled with GL 74535",
                "CRIF Select Corp reconciled with GL 74400",
                "Wire transfers reconciled with GL 74400",
                "Cash Letter Corr reconciled with GL 74515",
                "OCUL SERVICES CO fees reconciled with GL 74400",
                "Analysis Service Charge reconciled with GL 74400",
                "VISA U.S.A., INC reconciled with GL 74400"
            ],
            "timing_differences": [
                "ATM settlement activity posted to GL 74505 on last day of month",
                "Shared Branching activity recorded in GL 74510 on last day of month",
                "Check deposit activity at Barks or MtG posted to GL 74560 on last day of month",
                "Gift Card activity posted to GL 74535 on last day of month",
                "CBS activity posted to GL 74550 on last day of month",
                "CRIF indirect loan activity posted to GL 74540 on last day of month"
            ],
            "discrepancy_handling": [
                "Add deposits/credits not posted to GL in top left corner",
                "Add checks/debits not posted to GL in bottom left corner",
                "Add credits not posted to bank in top right corner",
                "Add debits not posted to bank in bottom right corner",
                "Investigate items from previous month that may have cleared",
                "Reverify all current month reconciling items for accuracy"
            ],
            "balance_validation": [
                "Adjusted Total under Balance per Books equals Adjusted Total under Balance per Statement",
                "No difference between the two adjusted totals",
                "Investigate any differences found"
            ]
        }
    
    def review_agent_line_by_line(self, agent_file: str) -> Dict[str, Any]:
        """Review an agent file line by line for OP compliance"""
        self.logger.info(f"Starting line-by-line review of: {agent_file}")
        
        try:
            # Read the agent file
            with open(agent_file, 'r', encoding='utf-8') as f:
                agent_code = f.read()
            
            # Parse the code into lines
            lines = agent_code.split('\n')
            
            # Review each line
            line_reviews = []
            total_issues = 0
            compliance_score = 0
            
            for line_num, line in enumerate(lines, 1):
                line_review = self._review_single_line(line, line_num, agent_file)
                line_reviews.append(line_review)
                
                if line_review['has_issues']:
                    total_issues += len(line_review['issues'])
                
                if line_review['compliance_score'] > 0:
                    compliance_score += line_review['compliance_score']
            
            # Calculate overall compliance
            avg_compliance = compliance_score / len(lines) if lines else 0
            
            # Generate summary
            summary = self._generate_line_review_summary(line_reviews, total_issues, avg_compliance)
            
            review_result = {
                "agent_file": agent_file,
                "review_timestamp": datetime.now().isoformat(),
                "total_lines": len(lines),
                "total_issues": total_issues,
                "average_compliance": round(avg_compliance, 2),
                "line_reviews": line_reviews,
                "summary": summary,
                "op_requirements_coverage": self._assess_op_requirements_coverage(agent_code)
            }
            
            self.logger.info(f"Completed line-by-line review for {agent_file}: {total_issues} issues, {avg_compliance:.2f} compliance")
            return review_result
            
        except Exception as e:
            self.logger.error(f"Error reviewing {agent_file}: {e}")
            return {
                "agent_file": agent_file,
                "review_timestamp": datetime.now().isoformat(),
                "total_lines": 0,
                "total_issues": 1,
                "average_compliance": 0,
                "line_reviews": [],
                "summary": {"error": str(e)},
                "op_requirements_coverage": {}
            }
    
    def _review_single_line(self, line: str, line_num: int, agent_file: str) -> Dict[str, Any]:
        """Review a single line of code for OP compliance"""
        line_review = {
            "line_number": line_num,
            "line_content": line.strip(),
            "has_issues": False,
            "issues": [],
            "compliance_score": 0,
            "op_requirements_met": [],
            "suggestions": []
        }
        
        # Skip empty lines and comments
        if not line.strip() or line.strip().startswith('#'):
            return line_review
        
        # Check for OP requirements compliance
        op_checks = self._check_op_requirements(line)
        line_review["op_requirements_met"] = op_checks["met"]
        line_review["compliance_score"] = len(op_checks["met"])
        
        # Check for common issues
        issues = self._check_common_issues(line, line_num)
        if issues:
            line_review["has_issues"] = True
            line_review["issues"] = issues
        
        # Generate suggestions
        suggestions = self._generate_line_suggestions(line, op_checks["met"])
        line_review["suggestions"] = suggestions
        
        return line_review
    
    def _check_op_requirements(self, line: str) -> Dict[str, Any]:
        """Check if line meets OP requirements"""
        met_requirements = []
        missing_requirements = []
        
        line_lower = line.lower()
        
        # Check each OP requirement category
        for category, requirements in self.op_requirements.items():
            for requirement in requirements:
                # Check if line contains relevant keywords
                keywords = self._extract_keywords_from_requirement(requirement)
                if any(keyword in line_lower for keyword in keywords):
                    met_requirements.append(f"{category}: {requirement}")
                else:
                    # Check if this is a critical requirement that should be present
                    if self._is_critical_requirement(requirement):
                        missing_requirements.append(f"{category}: {requirement}")
        
        return {
            "met": met_requirements,
            "missing": missing_requirements
        }
    
    def _extract_keywords_from_requirement(self, requirement: str) -> List[str]:
        """Extract keywords from a requirement for matching"""
        # Extract key terms and convert to lowercase
        keywords = []
        
        # Common financial terms
        financial_terms = [
            "gl", "general ledger", "bank", "statement", "reconcile", "balance",
            "transaction", "ach", "atm", "settlement", "variance", "discrepancy",
            "timing", "difference", "validation", "error", "handling"
        ]
        
        # Extract specific terms from requirement
        requirement_lower = requirement.lower()
        for term in financial_terms:
            if term in requirement_lower:
                keywords.append(term)
        
        # Add specific GL numbers
        gl_numbers = re.findall(r'\b(74400|74505|74510|74515|74520|74525|74530|74535|74540|74550|74560|74570)\b', requirement)
        keywords.extend(gl_numbers)
        
        return keywords
    
    def _is_critical_requirement(self, requirement: str) -> bool:
        """Check if a requirement is critical for OP compliance"""
        critical_terms = [
            "daily reconciliation", "gl extraction", "month-end balance",
            "bank statement", "transaction matching", "timing differences",
            "balance validation", "error handling", "data quality"
        ]
        
        return any(term in requirement.lower() for term in critical_terms)
    
    def _check_common_issues(self, line: str, line_num: int) -> List[str]:
        """Check for common code issues"""
        issues = []
        
        # Check for hardcoded values that should be configurable
        if re.search(r'\b\d{5}\b', line):  # 5-digit numbers (likely GL codes)
            if not any(gl in line for gl in ['74400', '74505', '74510', '74515', '74520', '74525', '74530', '74535', '74540', '74550', '74560', '74570']):
                issues.append(f"Line {line_num}: Hardcoded number that might be a GL code - consider using configuration")
        
        # Check for missing error handling
        if any(keyword in line.lower() for keyword in ['open', 'read', 'write', 'process', 'extract']):
            if 'try:' not in line and 'except' not in line and 'if' not in line:
                issues.append(f"Line {line_num}: Operation without error handling - consider adding try/except")
        
        # Check for missing logging
        if any(keyword in line.lower() for keyword in ['process', 'extract', 'reconcile', 'validate']):
            if 'log' not in line.lower() and 'print' not in line.lower():
                issues.append(f"Line {line_num}: Important operation without logging - consider adding log statement")
        
        # Check for missing validation
        if any(keyword in line.lower() for keyword in ['data', 'balance', 'transaction', 'gl']):
            if 'valid' not in line.lower() and 'check' not in line.lower() and 'verify' not in line.lower():
                issues.append(f"Line {line_num}: Data processing without validation - consider adding validation")
        
        return issues
    
    def _generate_line_suggestions(self, line: str, met_requirements: List[str]) -> List[str]:
        """Generate suggestions for improving line compliance"""
        suggestions = []
        
        line_lower = line.lower()
        
        # Suggest improvements based on missing requirements
        if 'gl' in line_lower and 'extract' not in line_lower:
            suggestions.append("Consider adding GL extraction logic as per OP requirements")
        
        if 'bank' in line_lower and 'statement' not in line_lower:
            suggestions.append("Consider adding bank statement processing logic")
        
        if 'reconcile' in line_lower and 'timing' not in line_lower:
            suggestions.append("Consider adding timing difference handling")
        
        if 'balance' in line_lower and 'valid' not in line_lower:
            suggestions.append("Consider adding balance validation logic")
        
        if 'error' in line_lower and 'log' not in line_lower:
            suggestions.append("Consider adding error logging")
        
        return suggestions
    
    def _assess_op_requirements_coverage(self, agent_code: str) -> Dict[str, Any]:
        """Assess overall OP requirements coverage for the agent"""
        coverage = {}
        code_lower = agent_code.lower()
        
        for category, requirements in self.op_requirements.items():
            met_count = 0
            for requirement in requirements:
                keywords = self._extract_keywords_from_requirement(requirement)
                if any(keyword in code_lower for keyword in keywords):
                    met_count += 1
            
            coverage[category] = {
                "total_requirements": len(requirements),
                "met_requirements": met_count,
                "coverage_percentage": round((met_count / len(requirements)) * 100, 2) if requirements else 0
            }
        
        return coverage
    
    def _generate_line_review_summary(self, line_reviews: List[Dict], total_issues: int, avg_compliance: float) -> Dict[str, Any]:
        """Generate summary of line-by-line review"""
        lines_with_issues = len([r for r in line_reviews if r['has_issues']])
        lines_with_compliance = len([r for r in line_reviews if r['compliance_score'] > 0])
        
        return {
            "total_lines_reviewed": len(line_reviews),
            "lines_with_issues": lines_with_issues,
            "lines_with_compliance": lines_with_compliance,
            "total_issues_found": total_issues,
            "average_compliance_per_line": round(avg_compliance, 2),
            "compliance_percentage": round((lines_with_compliance / len(line_reviews)) * 100, 2) if line_reviews else 0
        }
    
    def run_comprehensive_line_review(self) -> Dict[str, Any]:
        """Run line-by-line review of all upgraded agents"""
        self.logger.info("Starting comprehensive line-by-line review...")
        
        # Find all upgraded agent files
        agent_files = [
            "data_quality_validator.py",
            "gl_extraction_agent.py",
            "bank_statement_processor.py",
            "reconciliation_matcher.py",
            "timing_difference_handler.py",
            "variance_analyzer.py",
            "reconciliation_validator.py",
            "report_generator.py"
        ]
        
        review_results = []
        total_issues = 0
        total_compliance = 0
        
        for agent_file in agent_files:
            if os.path.exists(agent_file):
                self.logger.info(f"Reviewing {agent_file}...")
                result = self.review_agent_line_by_line(agent_file)
                review_results.append(result)
                total_issues += result.get('total_issues', 0)
                total_compliance += result.get('average_compliance', 0)
            else:
                self.logger.warning(f"Agent file not found: {agent_file}")
        
        # Calculate overall statistics
        avg_compliance = total_compliance / len(review_results) if review_results else 0
        
        comprehensive_results = {
            "review_timestamp": datetime.now().isoformat(),
            "total_agents_reviewed": len(review_results),
            "total_issues_found": total_issues,
            "average_compliance": round(avg_compliance, 2),
            "agent_reviews": review_results,
            "summary": self._generate_overall_summary(review_results)
        }
        
        self.review_results = comprehensive_results
        self.logger.info(f"Completed line-by-line review: {len(review_results)} agents, {total_issues} issues, {avg_compliance:.2f} compliance")
        
        return comprehensive_results
    
    def _generate_overall_summary(self, review_results: List[Dict]) -> Dict[str, Any]:
        """Generate overall summary of all reviews"""
        total_lines = sum(r.get('total_lines', 0) for r in review_results)
        total_issues = sum(r.get('total_issues', 0) for r in review_results)
        avg_compliance = sum(r.get('average_compliance', 0) for r in review_results) / len(review_results) if review_results else 0
        
        return {
            "total_agents": len(review_results),
            "total_lines_reviewed": total_lines,
            "total_issues_found": total_issues,
            "average_compliance": round(avg_compliance, 2),
            "issues_per_line": round(total_issues / total_lines, 4) if total_lines > 0 else 0,
            "compliance_distribution": {
                "excellent (8-10)": len([r for r in review_results if r.get('average_compliance', 0) >= 8]),
                "good (6-7)": len([r for r in review_results if 6 <= r.get('average_compliance', 0) < 8]),
                "fair (4-5)": len([r for r in review_results if 4 <= r.get('average_compliance', 0) < 6]),
                "poor (1-3)": len([r for r in review_results if r.get('average_compliance', 0) < 4])
            }
        }
    
    def save_results(self, filename: str = None) -> str:
        """Save the review results to a file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"line_by_line_review_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.review_results, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Line-by-line review results saved to: {filename}")
        return filename
    
    def generate_summary_report(self) -> str:
        """Generate a human-readable summary report"""
        if not self.review_results:
            return "No review results available. Run line-by-line review first."
        
        summary = self.review_results.get('summary', {})
        
        report = f"""
# Line-by-Line Review Report

## Review Overview
- **Review Date**: {self.review_results.get('review_timestamp', 'Unknown')}
- **Total Agents Reviewed**: {summary.get('total_agents', 0)}
- **Total Lines Reviewed**: {summary.get('total_lines_reviewed', 0)}
- **Total Issues Found**: {summary.get('total_issues_found', 0)}
- **Average Compliance**: {summary.get('average_compliance', 0)}/10
- **Issues per Line**: {summary.get('issues_per_line', 0)}

## Compliance Distribution
"""
        
        dist = summary.get('compliance_distribution', {})
        report += f"- **Excellent (8-10)**: {dist.get('excellent (8-10)', 0)} agents\n"
        report += f"- **Good (6-7)**: {dist.get('good (6-7)', 0)} agents\n"
        report += f"- **Fair (4-5)**: {dist.get('fair (4-5)', 0)} agents\n"
        report += f"- **Poor (1-3)**: {dist.get('poor (1-3)', 0)} agents\n"
        
        report += "\n## Individual Agent Results\n"
        for agent_review in self.review_results.get('agent_reviews', []):
            report += f"\n### {agent_review.get('agent_file', 'Unknown')}\n"
            report += f"- **Total Lines**: {agent_review.get('total_lines', 0)}\n"
            report += f"- **Issues Found**: {agent_review.get('total_issues', 0)}\n"
            report += f"- **Compliance Score**: {agent_review.get('average_compliance', 0)}/10\n"
            
            # Show OP requirements coverage
            coverage = agent_review.get('op_requirements_coverage', {})
            report += f"- **OP Requirements Coverage**:\n"
            for category, cov in coverage.items():
                report += f"  - {category}: {cov.get('coverage_percentage', 0)}% ({cov.get('met_requirements', 0)}/{cov.get('total_requirements', 0)})\n"
        
        return report

def main():
    """Main execution function"""
    try:
        # Initialize the reviewer
        reviewer = LineByLineReviewer()
        
        # Run comprehensive line-by-line review
        print("🔍 Starting Line-by-Line Review...")
        print("📋 Reviewing each agent line by line for OP compliance...")
        
        results = reviewer.run_comprehensive_line_review()
        
        # Save results
        json_file = reviewer.save_results()
        print(f"💾 Review results saved to: {json_file}")
        
        # Generate and save summary report
        summary = reviewer.generate_summary_report()
        summary_file = f"line_by_line_review_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        print(f"📋 Summary report saved to: {summary_file}")
        
        print("\n✅ Line-by-Line Review Complete!")
        print(f"📊 Total Agents: {results['total_agents_reviewed']}")
        print(f"🔍 Total Issues: {results['total_issues_found']}")
        print(f"🎯 Average Compliance: {results['average_compliance']}/10")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
