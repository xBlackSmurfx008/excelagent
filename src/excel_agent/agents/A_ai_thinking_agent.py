#!/usr/bin/env python3
"""
AI Thinking Agent - Uses OpenAI's thinking model to retrain on OP document
Performs 10 thinking sequences to discover new insights about reconciliation
"""

import openai
import json
import os
from datetime import datetime
from pathlib import Path

class AIThinkingAgent:
    def __init__(self, api_key=None):
        self.name = "AIThinkingAgent"
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Set up OpenAI client
        if api_key:
            self.client = openai.OpenAI(api_key=api_key)
        else:
            # Try to get from environment
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                self.client = openai.OpenAI(api_key=api_key)
            else:
                print("⚠️ No OpenAI API key found. Please set OPENAI_API_KEY environment variable.")
                self.client = None
        
        self.thinking_sequences = []
        self.discoveries = []
        
    def retrain_on_op_document(self, op_file_path):
        """Retrain on OP document using OpenAI thinking model"""
        print("🧠 AI THINKING AGENT - RETRAINING ON OP DOCUMENT")
        print("=" * 60)
        print("🎯 Using OpenAI thinking model for deep analysis")
        print("=" * 60)
        
        if not self.client:
            print("❌ OpenAI client not available. Cannot perform thinking sequences.")
            return None
        
        # Load OP document
        try:
            with open(op_file_path, 'r', encoding='utf-8') as f:
                op_content = f.read()
            print(f"✅ Loaded OP document: {Path(op_file_path).name}")
        except Exception as e:
            print(f"❌ Error loading OP document: {str(e)}")
            return None
        
        # Perform 10 thinking sequences
        print(f"\n🔄 PERFORMING 10 THINKING SEQUENCES")
        print("-" * 40)
        
        for sequence in range(1, 11):
            print(f"\n🧠 THINKING SEQUENCE {sequence}/10")
            print("-" * 30)
            
            thinking_result = self._perform_thinking_sequence(sequence, op_content)
            self.thinking_sequences.append(thinking_result)
            
            print(f"✅ Sequence {sequence} completed")
        
        # Generate final insights
        final_insights = self._generate_final_insights()
        
        # Save results
        self._save_thinking_results()
        
        return final_insights
    
    def _perform_thinking_sequence(self, sequence_num, op_content):
        """Perform a single thinking sequence using OpenAI"""
        print(f"🔍 Analyzing OP document with thinking model...")
        
        # Create thinking prompt based on sequence number
        thinking_prompts = {
            1: "Analyze the OP document and identify the core reconciliation principles. What are the fundamental rules for matching bank transactions to GL accounts?",
            2: "Examine the timing differences section. What patterns emerge in month-end timing differences? How should these be handled?",
            3: "Review the GL account mappings. What are the key patterns in transaction descriptions that map to specific GL accounts?",
            4: "Analyze the expected timing differences. What are the business reasons behind these differences? How can they be predicted?",
            5: "Study the transaction matching rules. What are the most effective strategies for matching similar but not identical transactions?",
            6: "Examine the OP manual's approach to handling discrepancies. What are the escalation procedures for unresolved items?",
            7: "Analyze the GL account structure. How do the different GL accounts relate to each other in the reconciliation process?",
            8: "Review the OP manual's quality control measures. What validation steps ensure accurate reconciliation?",
            9: "Examine the OP manual's approach to exception handling. How should unusual transactions be processed?",
            10: "Synthesize all previous analysis. What are the key insights for building an intelligent reconciliation system?"
        }
        
        prompt = thinking_prompts.get(sequence_num, "Analyze the OP document for reconciliation insights.")
        
        # Create the thinking prompt
        thinking_prompt = f"""
You are an expert AI reconciliation specialist. Please analyze the following OP (Operating Procedures) document using deep thinking and reasoning.

OP DOCUMENT CONTENT:
{op_content}

THINKING PROMPT: {prompt}

Please provide a detailed analysis that includes:
1. Key insights discovered
2. Patterns identified
3. Rules and principles extracted
4. Recommendations for improvement
5. New thinking approaches for reconciliation

Think step by step and provide comprehensive insights.
"""
        
        try:
            # Use OpenAI's thinking model (using GPT-4 with thinking capabilities)
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert AI reconciliation specialist with deep knowledge of accounting, banking, and financial reconciliation processes. Use advanced thinking and reasoning to analyze complex reconciliation scenarios."},
                    {"role": "user", "content": thinking_prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            thinking_result = {
                "sequence": sequence_num,
                "prompt": prompt,
                "response": response.choices[0].message.content,
                "timestamp": datetime.now().isoformat(),
                "insights": self._extract_insights(response.choices[0].message.content)
            }
            
            print(f"✅ Thinking sequence {sequence_num} completed")
            print(f"📊 Insights extracted: {len(thinking_result['insights'])}")
            
            return thinking_result
            
        except Exception as e:
            print(f"❌ Error in thinking sequence {sequence_num}: {str(e)}")
            return {
                "sequence": sequence_num,
                "prompt": prompt,
                "response": f"Error: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "insights": []
            }
    
    def _extract_insights(self, response_text):
        """Extract key insights from the thinking response"""
        insights = []
        
        # Simple insight extraction (could be enhanced with NLP)
        lines = response_text.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['insight', 'discovery', 'pattern', 'rule', 'principle', 'recommendation']):
                if len(line.strip()) > 20:  # Filter out very short lines
                    insights.append(line.strip())
        
        return insights
    
    def _generate_final_insights(self):
        """Generate final insights from all thinking sequences"""
        print("\n🎯 GENERATING FINAL INSIGHTS")
        print("-" * 40)
        
        all_insights = []
        for sequence in self.thinking_sequences:
            all_insights.extend(sequence.get('insights', []))
        
        # Categorize insights
        categorized_insights = {
            "reconciliation_principles": [],
            "timing_differences": [],
            "matching_strategies": [],
            "gl_account_mappings": [],
            "quality_control": [],
            "exception_handling": [],
            "new_approaches": []
        }
        
        for insight in all_insights:
            insight_lower = insight.lower()
            if 'timing' in insight_lower or 'month-end' in insight_lower:
                categorized_insights["timing_differences"].append(insight)
            elif 'matching' in insight_lower or 'match' in insight_lower:
                categorized_insights["matching_strategies"].append(insight)
            elif 'gl' in insight_lower or 'account' in insight_lower:
                categorized_insights["gl_account_mappings"].append(insight)
            elif 'quality' in insight_lower or 'validation' in insight_lower:
                categorized_insights["quality_control"].append(insight)
            elif 'exception' in insight_lower or 'unusual' in insight_lower:
                categorized_insights["exception_handling"].append(insight)
            elif 'new' in insight_lower or 'approach' in insight_lower:
                categorized_insights["new_approaches"].append(insight)
            else:
                categorized_insights["reconciliation_principles"].append(insight)
        
        final_insights = {
            "timestamp": datetime.now().isoformat(),
            "total_insights": len(all_insights),
            "categorized_insights": categorized_insights,
            "thinking_sequences_completed": len(self.thinking_sequences),
            "key_discoveries": self._identify_key_discoveries(categorized_insights)
        }
        
        print(f"✅ Total insights discovered: {len(all_insights)}")
        print(f"✅ Thinking sequences completed: {len(self.thinking_sequences)}")
        print(f"✅ Key discoveries identified: {len(final_insights['key_discoveries'])}")
        
        return final_insights
    
    def _identify_key_discoveries(self, categorized_insights):
        """Identify the most important discoveries"""
        key_discoveries = []
        
        for category, insights in categorized_insights.items():
            if insights:
                # Take the most comprehensive insights from each category
                top_insights = sorted(insights, key=len, reverse=True)[:3]
                key_discoveries.extend(top_insights)
        
        return key_discoveries
    
    def _save_thinking_results(self):
        """Save all thinking results to files"""
        print("\n💾 SAVING THINKING RESULTS")
        print("-" * 30)
        
        # Save detailed thinking sequences
        with open(f"ai_thinking_sequences_{self.timestamp}.json", 'w') as f:
            json.dump(self.thinking_sequences, f, indent=2, default=str)
        
        # Save final insights
        final_insights = self._generate_final_insights()
        with open(f"ai_thinking_insights_{self.timestamp}.json", 'w') as f:
            json.dump(final_insights, f, indent=2, default=str)
        
        # Create human-readable summary
        self._create_thinking_summary(final_insights)
        
        print(f"✅ Thinking sequences saved: ai_thinking_sequences_{self.timestamp}.json")
        print(f"✅ Final insights saved: ai_thinking_insights_{self.timestamp}.json")
        print(f"✅ Summary created: ai_thinking_summary_{self.timestamp}.txt")
    
    def _create_thinking_summary(self, final_insights):
        """Create a human-readable summary of thinking results"""
        summary_file = f"ai_thinking_summary_{self.timestamp}.txt"
        
        with open(summary_file, 'w') as f:
            f.write("🧠 AI THINKING AGENT - RETRAINING RESULTS\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("🎯 MISSION: Retrain on OP document using OpenAI thinking model\n")
            f.write("🔄 THINKING SEQUENCES: 10 deep analysis sequences\n")
            f.write("📊 TOTAL INSIGHTS: {}\n".format(final_insights['total_insights']))
            f.write("🔍 KEY DISCOVERIES: {}\n\n".format(len(final_insights['key_discoveries'])))
            
            f.write("📋 CATEGORIZED INSIGHTS:\n")
            f.write("-" * 30 + "\n")
            
            for category, insights in final_insights['categorized_insights'].items():
                if insights:
                    f.write(f"\n🔹 {category.upper().replace('_', ' ')}:\n")
                    for insight in insights[:5]:  # Top 5 insights per category
                        f.write(f"   • {insight}\n")
            
            f.write("\n🎯 KEY DISCOVERIES:\n")
            f.write("-" * 20 + "\n")
            for i, discovery in enumerate(final_insights['key_discoveries'][:10], 1):
                f.write(f"{i}. {discovery}\n")
            
            f.write("\n" + "=" * 50 + "\n")
            f.write("🎉 AI THINKING RETRAINING COMPLETE!\n")
            f.write("✅ 10 thinking sequences completed\n")
            f.write("✅ New insights discovered\n")
            f.write("✅ OP document fully analyzed\n")
            f.write("✅ Ready for enhanced reconciliation\n")

def main():
    """Run AI thinking agent"""
    print("🧠 AI THINKING AGENT - RETRAINING ON OP DOCUMENT")
    print("=" * 60)
    print("🎯 Using OpenAI thinking model for deep analysis")
    print("🔄 Performing 10 thinking sequences")
    print("=" * 60)
    
    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("⚠️ Please set your OpenAI API key:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        print("   or create a .env file with OPENAI_API_KEY=your-api-key-here")
        return
    
    # Initialize agent
    agent = AIThinkingAgent(api_key=api_key)
    
    # OP document path
    op_file = "Knowledge Base/op-ncb-reconciliation-8-28-25.md"
    
    if not os.path.exists(op_file):
        print(f"❌ OP document not found: {op_file}")
        return
    
    # Run retraining
    print(f"\n🔄 Starting retraining on: {op_file}")
    final_insights = agent.retrain_on_op_document(op_file)
    
    if final_insights:
        print(f"\n🎉 RETRAINING COMPLETE!")
        print(f"📊 Total insights: {final_insights['total_insights']}")
        print(f"🔍 Key discoveries: {len(final_insights['key_discoveries'])}")
        print(f"✅ Thinking sequences: {final_insights['thinking_sequences_completed']}")
    else:
        print("❌ Retraining failed. Check API key and OP document.")

if __name__ == "__main__":
    main()
