#!/usr/bin/env python3
"""
Agent Accuracy Reviewer
Reviews all agents for accuracy and compliance with training document insights
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import openai
from pathlib import Path

class AgentAccuracyReviewer:
    def __init__(self, api_key: str = None):
        """Initialize the Agent Accuracy Reviewer"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        self.training_insights = self._load_training_insights()
        self.agents_to_review = self._identify_agents()
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
    
    def _identify_agents(self) -> List[str]:
        """Identify all agent files to review"""
        agent_files = []
        current_dir = Path(".")
        
        # Look for agent files
        for file_path in current_dir.glob("*agent*.py"):
            if file_path.name not in ["agent_accuracy_reviewer.py", "agent_review_and_improvements.py"]:
                agent_files.append(str(file_path))
        
        return agent_files
    
    def review_agent_accuracy(self, agent_file: str) -> Dict[str, Any]:
        """Review a single agent for accuracy against training insights"""
        self.logger.info(f"Reviewing agent: {agent_file}")
        
        try:
            # Read the agent file
            with open(agent_file, 'r', encoding='utf-8') as f:
                agent_code = f.read()
            
            # Extract training insights for comparison
            training_rules = self._extract_training_rules()
            reconciliation_patterns = self._extract_reconciliation_patterns()
            data_quality_requirements = self._extract_data_quality_requirements()
            
            # Create review prompt
            review_prompt = f"""
            Review the following agent code for accuracy and compliance with OP reconciliation training document insights.
            
            Agent File: {agent_file}
            
            Training Document Insights:
            {json.dumps(training_rules, indent=2)}
            
            Reconciliation Patterns:
            {json.dumps(reconciliation_patterns, indent=2)}
            
            Data Quality Requirements:
            {json.dumps(data_quality_requirements, indent=2)}
            
            Agent Code:
            {agent_code[:4000]}  # Limit to avoid token limits
            
            Please provide a detailed review covering:
            1. Compliance with training document rules
            2. Accuracy of reconciliation logic
            3. Data quality handling
            4. Error handling and validation
            5. Specific recommendations for improvement
            6. Overall accuracy score (1-10)
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert code reviewer specializing in financial reconciliation systems. Provide detailed, actionable feedback."},
                    {"role": "user", "content": review_prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            review_result = {
                "agent_file": agent_file,
                "review_timestamp": datetime.now().isoformat(),
                "review_content": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens if response.usage else 0
            }
            
            # Extract accuracy score from review
            review_text = review_result["review_content"]
            accuracy_score = self._extract_accuracy_score(review_text)
            review_result["accuracy_score"] = accuracy_score
            
            self.logger.info(f"Completed review for {agent_file}: Score {accuracy_score}/10")
            return review_result
            
        except Exception as e:
            self.logger.error(f"Error reviewing {agent_file}: {e}")
            return {
                "agent_file": agent_file,
                "review_timestamp": datetime.now().isoformat(),
                "review_content": f"Error during review: {str(e)}",
                "tokens_used": 0,
                "accuracy_score": 0
            }
    
    def _extract_training_rules(self) -> List[str]:
        """Extract reconciliation rules from training insights"""
        rules = []
        if "reconciliation_rules" in self.training_insights:
            for rule in self.training_insights["reconciliation_rules"]:
                if "Round" in rule and ":" in rule:
                    rule_text = rule.split(":", 1)[1].strip()
                    rules.append(rule_text)
        return rules
    
    def _extract_reconciliation_patterns(self) -> List[str]:
        """Extract reconciliation patterns from training insights"""
        patterns = []
        if "matching_criteria" in self.training_insights:
            for criteria in self.training_insights["matching_criteria"]:
                if "Round" in criteria and ":" in criteria:
                    pattern_text = criteria.split(":", 1)[1].strip()
                    patterns.append(pattern_text)
        return patterns
    
    def _extract_data_quality_requirements(self) -> List[str]:
        """Extract data quality requirements from training insights"""
        requirements = []
        if "data_quality_requirements" in self.training_insights:
            for req in self.training_insights["data_quality_requirements"]:
                if "Round" in req and ":" in req:
                    req_text = req.split(":", 1)[1].strip()
                    requirements.append(req_text)
        return requirements
    
    def _extract_accuracy_score(self, review_text: str) -> int:
        """Extract accuracy score from review text"""
        import re
        # Look for patterns like "Score: 8/10" or "8/10" or "Score: 8"
        score_patterns = [
            r"score[:\s]+(\d+)/10",
            r"(\d+)/10",
            r"score[:\s]+(\d+)",
            r"accuracy[:\s]+(\d+)"
        ]
        
        for pattern in score_patterns:
            match = re.search(pattern, review_text.lower())
            if match:
                return int(match.group(1))
        
        # If no score found, try to infer from text
        if "excellent" in review_text.lower() or "perfect" in review_text.lower():
            return 9
        elif "good" in review_text.lower() or "well" in review_text.lower():
            return 7
        elif "fair" in review_text.lower() or "adequate" in review_text.lower():
            return 5
        elif "poor" in review_text.lower() or "needs improvement" in review_text.lower():
            return 3
        else:
            return 5  # Default middle score
    
    def run_comprehensive_agent_review(self) -> Dict[str, Any]:
        """Run comprehensive review of all agents"""
        self.logger.info("Starting comprehensive agent accuracy review...")
        
        review_results = []
        total_tokens = 0
        total_score = 0
        
        for agent_file in self.agents_to_review:
            self.logger.info(f"Reviewing agent: {agent_file}")
            result = self.review_agent_accuracy(agent_file)
            review_results.append(result)
            total_tokens += result.get('tokens_used', 0)
            total_score += result.get('accuracy_score', 0)
            
            # Small delay to avoid rate limiting
            import time
            time.sleep(2)
        
        # Calculate overall statistics
        avg_score = total_score / len(review_results) if review_results else 0
        
        comprehensive_results = {
            "review_timestamp": datetime.now().isoformat(),
            "total_agents_reviewed": len(review_results),
            "total_tokens_used": total_tokens,
            "average_accuracy_score": round(avg_score, 2),
            "agent_reviews": review_results,
            "summary": self._generate_review_summary(review_results),
            "recommendations": self._generate_overall_recommendations(review_results)
        }
        
        self.review_results = comprehensive_results
        self.logger.info(f"Completed comprehensive agent review: {len(review_results)} agents, avg score {avg_score:.2f}/10")
        
        return comprehensive_results
    
    def _generate_review_summary(self, review_results: List[Dict]) -> Dict[str, Any]:
        """Generate summary of review results"""
        scores = [r.get('accuracy_score', 0) for r in review_results]
        
        return {
            "total_agents": len(review_results),
            "average_score": round(sum(scores) / len(scores), 2) if scores else 0,
            "highest_score": max(scores) if scores else 0,
            "lowest_score": min(scores) if scores else 0,
            "agents_above_8": len([s for s in scores if s >= 8]),
            "agents_below_5": len([s for s in scores if s < 5]),
            "score_distribution": {
                "excellent (9-10)": len([s for s in scores if s >= 9]),
                "good (7-8)": len([s for s in scores if 7 <= s < 9]),
                "fair (5-6)": len([s for s in scores if 5 <= s < 7]),
                "poor (1-4)": len([s for s in scores if s < 5])
            }
        }
    
    def _generate_overall_recommendations(self, review_results: List[Dict]) -> List[str]:
        """Generate overall recommendations based on review results"""
        recommendations = []
        
        # Analyze common issues
        low_score_agents = [r for r in review_results if r.get('accuracy_score', 0) < 5]
        if low_score_agents:
            recommendations.append(f"Priority: {len(low_score_agents)} agents need immediate attention (score < 5)")
        
        # Check for common patterns
        all_reviews = [r.get('review_content', '') for r in review_results]
        
        if any("data quality" in review.lower() for review in all_reviews):
            recommendations.append("Implement comprehensive data quality validation across all agents")
        
        if any("error handling" in review.lower() for review in all_reviews):
            recommendations.append("Enhance error handling and validation mechanisms")
        
        if any("training document" in review.lower() for review in all_reviews):
            recommendations.append("Better integrate training document insights into agent logic")
        
        if any("reconciliation logic" in review.lower() for review in all_reviews):
            recommendations.append("Review and improve reconciliation logic accuracy")
        
        recommendations.append("Conduct regular agent accuracy reviews to maintain quality")
        recommendations.append("Implement automated testing based on training document rules")
        
        return recommendations
    
    def save_results(self, filename: str = None) -> str:
        """Save the review results to a file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"agent_accuracy_review_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.review_results, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Review results saved to: {filename}")
        return filename
    
    def generate_summary_report(self) -> str:
        """Generate a human-readable summary report"""
        if not self.review_results:
            return "No review results available. Run agent review first."
        
        summary = self.review_results.get('summary', {})
        recommendations = self.review_results.get('recommendations', [])
        
        report = f"""
# Agent Accuracy Review Report

## Review Overview
- **Review Date**: {self.review_results.get('review_timestamp', 'Unknown')}
- **Total Agents Reviewed**: {summary.get('total_agents', 0)}
- **Average Accuracy Score**: {summary.get('average_score', 0)}/10
- **Highest Score**: {summary.get('highest_score', 0)}/10
- **Lowest Score**: {summary.get('lowest_score', 0)}/10

## Score Distribution
- **Excellent (9-10)**: {summary.get('score_distribution', {}).get('excellent (9-10)', 0)} agents
- **Good (7-8)**: {summary.get('score_distribution', {}).get('good (7-8)', 0)} agents
- **Fair (5-6)**: {summary.get('score_distribution', {}).get('fair (5-6)', 0)} agents
- **Poor (1-4)**: {summary.get('score_distribution', {}).get('poor (1-4)', 0)} agents

## Individual Agent Results
"""
        
        for agent_review in self.review_results.get('agent_reviews', []):
            report += f"\n### {agent_review.get('agent_file', 'Unknown')}\n"
            report += f"- **Accuracy Score**: {agent_review.get('accuracy_score', 0)}/10\n"
            report += f"- **Review**: {agent_review.get('review_content', 'No review available')[:300]}...\n"
        
        report += "\n## Overall Recommendations\n"
        for i, rec in enumerate(recommendations, 1):
            report += f"{i}. {rec}\n"
        
        return report

def main():
    """Main execution function"""
    try:
        # Initialize the reviewer
        reviewer = AgentAccuracyReviewer()
        
        # Run comprehensive review
        print("🔍 Starting Agent Accuracy Review...")
        print("📋 Reviewing agents against training document insights...")
        print(f"🤖 Found {len(reviewer.agents_to_review)} agents to review")
        
        results = reviewer.run_comprehensive_agent_review()
        
        # Save results
        json_file = reviewer.save_results()
        print(f"💾 Review results saved to: {json_file}")
        
        # Generate and save summary report
        summary = reviewer.generate_summary_report()
        summary_file = f"agent_accuracy_review_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        print(f"📋 Summary report saved to: {summary_file}")
        
        print("\n✅ Agent Accuracy Review Complete!")
        print(f"📊 Total Agents: {results['total_agents_reviewed']}")
        print(f"🎯 Average Score: {results['average_accuracy_score']}/10")
        print(f"💡 Recommendations: {len(results['recommendations'])}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
