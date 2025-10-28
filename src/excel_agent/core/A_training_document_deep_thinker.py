#!/usr/bin/env python3
"""
Training Document Deep Thinker
Performs 10 rounds of deep thinking analysis on OP training documents
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import openai
from pathlib import Path

class TrainingDocumentDeepThinker:
    def __init__(self, api_key: str = None):
        """Initialize the Training Document Deep Thinker"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        self.training_document_path = "Knowledge Base/op-ncb-reconciliation-8-28-25.md"
        self.results = {}
        self.thinking_rounds = 10
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def load_training_document(self) -> str:
        """Load the OP training document"""
        try:
            with open(self.training_document_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.logger.info(f"Loaded training document: {len(content)} characters")
            return content
        except Exception as e:
            self.logger.error(f"Error loading training document: {e}")
            raise
    
    def perform_deep_thinking_round(self, content: str, round_number: int) -> Dict[str, Any]:
        """Perform a single round of deep thinking analysis"""
        
        thinking_prompts = {
            1: "Analyze the basic structure and organization of this reconciliation training document. What are the main sections and how do they relate to each other?",
            2: "Examine the timing differences and variance analysis procedures described. What are the key rules and thresholds?",
            3: "Review the matching criteria and keyword analysis methods. What patterns should be used for successful reconciliation?",
            4: "Analyze the bank activity description patterns and how they should be interpreted for GL matching.",
            5: "Evaluate the variance threshold effectiveness and when adjustments should be made.",
            6: "Study the historical failure patterns mentioned and what causes reconciliation errors.",
            7: "Identify the success patterns and best practices that lead to accurate reconciliation.",
            8: "Examine the data quality requirements and how they impact reconciliation accuracy.",
            9: "Synthesize the cross-pattern relationships between different reconciliation elements.",
            10: "Provide comprehensive insights and strategic recommendations based on all previous analysis rounds."
        }
        
        prompt = thinking_prompts.get(round_number, "Perform deep analysis of this reconciliation training document.")
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert reconciliation analyst with deep knowledge of financial processes. Provide detailed, actionable insights."},
                    {"role": "user", "content": f"{prompt}\n\nDocument Content:\n{content[:8000]}"}  # Limit content to avoid token limits
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            thinking_result = {
                "round": round_number,
                "prompt": prompt,
                "insights": response.choices[0].message.content,
                "timestamp": datetime.now().isoformat(),
                "tokens_used": response.usage.total_tokens if response.usage else 0
            }
            
            self.logger.info(f"Completed thinking round {round_number}")
            return thinking_result
            
        except Exception as e:
            self.logger.error(f"Error in thinking round {round_number}: {e}")
            return {
                "round": round_number,
                "prompt": prompt,
                "insights": f"Error in analysis: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "tokens_used": 0
            }
    
    def run_comprehensive_training_analysis(self) -> Dict[str, Any]:
        """Run 10 rounds of deep thinking on the training document"""
        self.logger.info("Starting comprehensive training document analysis...")
        
        # Load training document
        content = self.load_training_document()
        
        # Perform 10 rounds of deep thinking
        thinking_results = []
        total_tokens = 0
        
        for round_num in range(1, self.thinking_rounds + 1):
            self.logger.info(f"Performing thinking round {round_num}/10...")
            result = self.perform_deep_thinking_round(content, round_num)
            thinking_results.append(result)
            total_tokens += result.get('tokens_used', 0)
            
            # Small delay to avoid rate limiting
            import time
            time.sleep(1)
        
        # Compile comprehensive results
        comprehensive_results = {
            "analysis_timestamp": datetime.now().isoformat(),
            "training_document": self.training_document_path,
            "total_rounds": self.thinking_rounds,
            "total_tokens_used": total_tokens,
            "thinking_results": thinking_results,
            "key_insights": self._extract_key_insights(thinking_results),
            "strategic_recommendations": self._generate_strategic_recommendations(thinking_results),
            "reconciliation_rules": self._extract_reconciliation_rules(thinking_results),
            "data_quality_requirements": self._extract_data_quality_requirements(thinking_results),
            "matching_criteria": self._extract_matching_criteria(thinking_results)
        }
        
        self.results = comprehensive_results
        self.logger.info(f"Completed comprehensive training analysis: {len(thinking_results)} rounds, {total_tokens} tokens")
        
        return comprehensive_results
    
    def _extract_key_insights(self, thinking_results: List[Dict]) -> List[str]:
        """Extract key insights from all thinking rounds"""
        insights = []
        for result in thinking_results:
            if "insights" in result and "Error" not in result["insights"]:
                # Extract key points from each round
                content = result["insights"]
                if "key insight" in content.lower() or "important" in content.lower():
                    insights.append(f"Round {result['round']}: {content[:200]}...")
        return insights
    
    def _generate_strategic_recommendations(self, thinking_results: List[Dict]) -> List[str]:
        """Generate strategic recommendations based on all thinking rounds"""
        recommendations = []
        for result in thinking_results:
            if "insights" in result and "Error" not in result["insights"]:
                content = result["insights"]
                if "recommend" in content.lower() or "should" in content.lower():
                    recommendations.append(f"Round {result['round']}: {content[:200]}...")
        return recommendations
    
    def _extract_reconciliation_rules(self, thinking_results: List[Dict]) -> List[str]:
        """Extract reconciliation rules from thinking results"""
        rules = []
        for result in thinking_results:
            if "insights" in result and "Error" not in result["insights"]:
                content = result["insights"]
                if "rule" in content.lower() or "procedure" in content.lower():
                    rules.append(f"Round {result['round']}: {content[:200]}...")
        return rules
    
    def _extract_data_quality_requirements(self, thinking_results: List[Dict]) -> List[str]:
        """Extract data quality requirements from thinking results"""
        requirements = []
        for result in thinking_results:
            if "insights" in result and "Error" not in result["insights"]:
                content = result["insights"]
                if "quality" in content.lower() or "validation" in content.lower():
                    requirements.append(f"Round {result['round']}: {content[:200]}...")
        return requirements
    
    def _extract_matching_criteria(self, thinking_results: List[Dict]) -> List[str]:
        """Extract matching criteria from thinking results"""
        criteria = []
        for result in thinking_results:
            if "insights" in result and "Error" not in result["insights"]:
                content = result["insights"]
                if "match" in content.lower() or "criteria" in content.lower():
                    criteria.append(f"Round {result['round']}: {content[:200]}...")
        return criteria
    
    def save_results(self, filename: str = None) -> str:
        """Save the analysis results to a file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"training_document_deep_analysis_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Results saved to: {filename}")
        return filename
    
    def generate_summary_report(self) -> str:
        """Generate a human-readable summary report"""
        if not self.results:
            return "No analysis results available. Run analysis first."
        
        report = f"""
# Training Document Deep Thinking Analysis Report

## Analysis Overview
- **Document**: {self.results.get('training_document', 'Unknown')}
- **Analysis Date**: {self.results.get('analysis_timestamp', 'Unknown')}
- **Total Rounds**: {self.results.get('total_rounds', 0)}
- **Total Tokens Used**: {self.results.get('total_tokens_used', 0)}

## Key Insights
"""
        
        for i, insight in enumerate(self.results.get('key_insights', []), 1):
            report += f"{i}. {insight}\n"
        
        report += "\n## Strategic Recommendations\n"
        for i, rec in enumerate(self.results.get('strategic_recommendations', []), 1):
            report += f"{i}. {rec}\n"
        
        report += "\n## Reconciliation Rules\n"
        for i, rule in enumerate(self.results.get('reconciliation_rules', []), 1):
            report += f"{i}. {rule}\n"
        
        report += "\n## Data Quality Requirements\n"
        for i, req in enumerate(self.results.get('data_quality_requirements', []), 1):
            report += f"{i}. {req}\n"
        
        report += "\n## Matching Criteria\n"
        for i, criteria in enumerate(self.results.get('matching_criteria', []), 1):
            report += f"{i}. {criteria}\n"
        
        return report

def main():
    """Main execution function"""
    try:
        # Initialize the deep thinker
        thinker = TrainingDocumentDeepThinker()
        
        # Run comprehensive analysis
        print("🧠 Starting Training Document Deep Thinking Analysis...")
        print("📄 Analyzing OP reconciliation training document...")
        print("🔄 Performing 10 rounds of deep thinking...")
        
        results = thinker.run_comprehensive_training_analysis()
        
        # Save results
        json_file = thinker.save_results()
        print(f"💾 Results saved to: {json_file}")
        
        # Generate and save summary report
        summary = thinker.generate_summary_report()
        summary_file = f"training_document_analysis_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        print(f"📋 Summary report saved to: {summary_file}")
        
        print("\n✅ Training Document Deep Thinking Analysis Complete!")
        print(f"📊 Total Rounds: {results['total_rounds']}")
        print(f"🔑 Key Insights: {len(results['key_insights'])}")
        print(f"💡 Strategic Recommendations: {len(results['strategic_recommendations'])}")
        print(f"📋 Reconciliation Rules: {len(results['reconciliation_rules'])}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
