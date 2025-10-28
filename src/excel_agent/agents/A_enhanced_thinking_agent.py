#!/usr/bin/env python3
"""
Enhanced Thinking Agent with Document Review

This agent provides advanced thinking capabilities for reconciliation analysis,
including document review, pattern recognition, and continuous learning from
training materials and visual examples.
"""

import os
import json
import openai
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import pandas as pd
from ai_reconciliation_agent import AIReconciliationAgent

class EnhancedThinkingAgent:
    """
    Advanced thinking agent that combines document analysis, pattern recognition,
    and continuous learning to improve reconciliation accuracy.
    """
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """Initialize the enhanced thinking agent."""
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.client = openai.OpenAI(api_key=self.openai_api_key)
        self.base_agent = AIReconciliationAgent()
        self.thinking_history = []
        self.learning_insights = {}
        self.document_knowledge = {}
        
    def analyze_op_training_document(self, document_path: str) -> Dict[str, Any]:
        """
        Analyze the OP training document to extract reconciliation rules,
        patterns, and best practices for improved matching.
        """
        print(f"📚 Analyzing OP training document: {document_path}")
        
        if not os.path.exists(document_path):
            return {"error": f"Document not found: {document_path}"}
        
        try:
            with open(document_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Use advanced GPT-4 analysis for comprehensive understanding
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert financial reconciliation analyst with deep knowledge of 
                        credit union operations and NCB reconciliation processes. Analyze the provided OP training 
                        document and extract comprehensive reconciliation intelligence including:
                        
                        1. GL Account Mappings: Extract all GL numbers and their specific purposes
                        2. Transaction Matching Rules: Identify exact matching criteria for each transaction type
                        3. Timing Difference Patterns: Document expected timing differences and their causes
                        4. Reconciliation Workflow: Map out the complete reconciliation process
                        5. Error Detection Methods: Identify common errors and how to detect them
                        6. Best Practices: Extract proven reconciliation techniques
                        7. Visual Patterns: If images are referenced, describe visual reconciliation patterns
                        8. Exception Handling: Document how to handle unusual transactions
                        
                        Provide your analysis in a structured JSON format with detailed explanations for each category."""
                    },
                    {
                        "role": "user",
                        "content": f"""Analyze this NCB reconciliation training document and extract all reconciliation 
                        intelligence for AI agent training:
                        
                        {content}
                        
                        Focus on actionable insights that can improve automated reconciliation accuracy."""
                    }
                ],
                max_tokens=3000,
                temperature=0.3
            )
            
            analysis = response.choices[0].message.content
            print(f"✅ OP document analysis completed")
            
            # Parse and structure the analysis
            structured_analysis = self._parse_training_analysis(analysis)
            
            return {
                "document_type": "op_training",
                "file_path": document_path,
                "analysis": analysis,
                "structured_analysis": structured_analysis,
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }
            
        except Exception as e:
            print(f"❌ Error analyzing OP document {document_path}: {str(e)}")
            return {
                "document_type": "op_training",
                "file_path": document_path,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }
    
    def _parse_training_analysis(self, analysis_content: str) -> Dict[str, Any]:
        """Parse and structure the training analysis content."""
        structured = {
            "gl_mappings": {},
            "matching_rules": {},
            "timing_patterns": {},
            "workflow_steps": [],
            "error_patterns": {},
            "best_practices": [],
            "visual_insights": []
        }
        
        try:
            # Extract GL mappings using regex
            import re
            
            # Find GL numbers and their descriptions
            gl_pattern = r'GL\s*(\d{5})'
            gl_matches = re.findall(gl_pattern, analysis_content)
            
            for gl_num in gl_matches:
                # Extract context around the GL number
                start_idx = analysis_content.find(f"GL {gl_num}")
                if start_idx != -1:
                    context = analysis_content[start_idx:start_idx + 300]
                    structured["gl_mappings"][gl_num] = {
                        "description": context[:150],
                        "extracted_from": "op_training_document"
                    }
            
            # Extract matching rules
            if "match" in analysis_content.lower():
                structured["matching_rules"]["transaction_matching"] = "Extracted from OP training"
            
            # Extract timing patterns
            if "timing" in analysis_content.lower() or "difference" in analysis_content.lower():
                structured["timing_patterns"]["month_end_timing"] = "Month-end timing differences documented"
            
            # Extract workflow steps
            if "reconcile" in analysis_content.lower():
                structured["workflow_steps"].append("Reconciliation process documented")
            
            # Extract best practices
            if "best" in analysis_content.lower() or "practice" in analysis_content.lower():
                structured["best_practices"].append("Best practices identified from training")
            
        except Exception as e:
            print(f"⚠️ Error parsing training analysis: {str(e)}")
        
        return structured
    
    def think_about_reconciliation_challenges(self, gl_data: Dict, bank_data: Dict, 
                                            training_insights: Dict = None) -> Dict[str, Any]:
        """
        Advanced thinking about reconciliation challenges using AI reasoning.
        """
        print("🧠 Advanced thinking about reconciliation challenges...")
        
        thinking_prompt = f"""
        As an expert reconciliation analyst, analyze these reconciliation challenges:
        
        GL Data Summary:
        - Total GL Balance: ${gl_data.get('total_balance', 0):.2f}
        - GL Accounts: {len(gl_data.get('accounts', {}))}
        - Transaction Count: {gl_data.get('transaction_count', 0)}
        
        Bank Data Summary:
        - Bank Transactions: {bank_data.get('transaction_count', 0)}
        - Bank Balance: ${bank_data.get('total_balance', 0):.2f}
        
        Training Insights Available: {bool(training_insights)}
        
        Think through:
        1. What are the most likely causes of discrepancies?
        2. Which GL accounts typically have timing differences?
        3. What matching strategies would be most effective?
        4. How can training document insights improve accuracy?
        5. What are the highest priority items to investigate?
        
        Provide detailed reasoning and actionable recommendations.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert reconciliation analyst with deep knowledge of credit union 
                        operations. Provide detailed, actionable analysis of reconciliation challenges with 
                        specific recommendations for improvement."""
                    },
                    {
                        "role": "user",
                        "content": thinking_prompt
                    }
                ],
                max_tokens=2000,
                temperature=0.4
            )
            
            thinking_result = response.choices[0].message.content
            print("✅ Advanced thinking analysis completed")
            
            return {
                "thinking_analysis": thinking_result,
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }
            
        except Exception as e:
            print(f"❌ Error in thinking analysis: {str(e)}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }
    
    def learn_from_matching_failures(self, unmatched_transactions: List[Dict], 
                                   training_insights: Dict = None) -> Dict[str, Any]:
        """
        Learn from matching failures to improve future reconciliation accuracy.
        """
        print("📚 Learning from matching failures...")
        
        learning_prompt = f"""
        Analyze these unmatched transactions to identify patterns and improve matching:
        
        Unmatched Transactions: {len(unmatched_transactions)}
        Sample transactions: {unmatched_transactions[:5] if unmatched_transactions else 'None'}
        
        Training Insights: {training_insights.get('gl_mappings', {}) if training_insights else 'None'}
        
        Identify:
        1. Common patterns in unmatched transactions
        2. Potential matching rule improvements
        3. Timing difference indicators
        4. Description similarity issues
        5. Amount matching problems
        6. Recommendations for rule enhancement
        
        Provide specific, actionable insights for improving matching accuracy.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert in transaction matching and reconciliation. 
                        Analyze unmatched transactions to identify patterns and provide specific 
                        recommendations for improving matching accuracy."""
                    },
                    {
                        "role": "user",
                        "content": learning_prompt
                    }
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            learning_insights = response.choices[0].message.content
            print("✅ Learning analysis completed")
            
            return {
                "learning_insights": learning_insights,
                "unmatched_count": len(unmatched_transactions),
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }
            
        except Exception as e:
            print(f"❌ Error in learning analysis: {str(e)}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }
    
    def run_enhanced_reconciliation_with_thinking(self, gl_file: str, bank_file: str, 
                                                training_doc: str = None) -> Dict[str, Any]:
        """
        Run enhanced reconciliation with advanced thinking and learning capabilities.
        """
        print("🚀 Starting Enhanced Thinking Reconciliation...")
        
        # Analyze training document if provided
        training_insights = None
        if training_doc and os.path.exists(training_doc):
            training_analysis = self.analyze_op_training_document(training_doc)
            if training_analysis.get("status") == "success":
                training_insights = training_analysis.get("structured_analysis", {})
                print(f"📚 Training insights loaded: {len(training_insights.get('gl_mappings', {}))} GL mappings")
        
        # Run base reconciliation
        base_result = self.base_agent.think_and_analyze(gl_file, bank_file)
        
        # Extract data for thinking analysis
        gl_data = {
            "total_balance": base_result.get('ai_analysis', {}).get('total_gl_balance', 0),
            "accounts": base_result.get('gl_analysis', {}),
            "transaction_count": sum(len(acc.get('transactions', [])) for acc in base_result.get('gl_analysis', {}).values())
        }
        
        bank_data = {
            "transaction_count": base_result.get('bank_analysis', {}).get('transaction_count', 0),
            "total_balance": 0  # Would need to calculate from bank data
        }
        
        # Advanced thinking about challenges
        thinking_result = self.think_about_reconciliation_challenges(
            gl_data, bank_data, training_insights
        )
        
        # Learn from any unmatched transactions
        unmatched_transactions = []  # Would extract from base_result
        learning_result = self.learn_from_matching_failures(unmatched_transactions, training_insights)
        
        # Combine all results
        enhanced_result = {
            **base_result,
            "enhanced_thinking": {
                "training_analysis": training_analysis if training_doc else None,
                "thinking_analysis": thinking_result,
                "learning_insights": learning_result,
                "training_insights_applied": bool(training_insights)
            }
        }
        
        # Save enhanced report
        self._save_enhanced_thinking_report(enhanced_result)
        
        return enhanced_result
    
    def _save_enhanced_thinking_report(self, result: Dict[str, Any]):
        """Save the enhanced thinking reconciliation report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"enhanced_thinking_reconciliation_report_{timestamp}.json"
        
        with open(report_path, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        
        print(f"📊 Enhanced thinking report saved: {report_path}")

def main():
    """Main function to demonstrate enhanced thinking reconciliation."""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python enhanced_thinking_agent.py <gl_file> <bank_file> [training_doc]")
        sys.exit(1)
    
    gl_file = sys.argv[1]
    bank_file = sys.argv[2]
    training_doc = sys.argv[3] if len(sys.argv) > 3 else None
    
    try:
        agent = EnhancedThinkingAgent()
        result = agent.run_enhanced_reconciliation_with_thinking(gl_file, bank_file, training_doc)
        
        print("\n🎯 ENHANCED THINKING RECONCILIATION COMPLETE")
        print("=" * 50)
        print(f"Status: {result.get('reconciliation_status', 'Unknown')}")
        print(f"GL Balance: ${result.get('ai_analysis', {}).get('total_gl_balance', 0):.2f}")
        
        if result.get('enhanced_thinking'):
            thinking = result['enhanced_thinking']
            print(f"Training Document Analyzed: {thinking.get('training_analysis') is not None}")
            print(f"Thinking Analysis: {thinking.get('thinking_analysis', {}).get('status', 'Unknown')}")
            print(f"Learning Insights: {thinking.get('learning_insights', {}).get('status', 'Unknown')}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
