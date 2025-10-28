#!/usr/bin/env python3
"""
Integrated Vision-Enhanced Reconciliation System

This system combines the base AI reconciliation agent with vision capabilities
and enhanced thinking to provide comprehensive reconciliation analysis with
training document insights and visual pattern recognition.
"""

import os
import json
import base64
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from ai_reconciliation_agent import AIReconciliationAgent
from enhanced_thinking_agent import EnhancedThinkingAgent
from vision_enhanced_ai_agent import VisionEnhancedAIAgent

class IntegratedVisionReconciliation:
    """
    Integrated system that combines all AI capabilities for comprehensive
    reconciliation analysis with training document insights.
    """
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """Initialize the integrated vision reconciliation system."""
        self.api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        
        # Initialize component agents
        self.base_agent = AIReconciliationAgent()
        
        # Initialize enhanced agents if API key is available
        self.thinking_agent = None
        self.vision_agent = None
        
        if self.api_key and self.api_key != 'test-key-for-demo':
            try:
                self.thinking_agent = EnhancedThinkingAgent(self.api_key)
                self.vision_agent = VisionEnhancedAIAgent(self.api_key)
                print("✅ Enhanced AI agents initialized with OpenAI API")
            except Exception as e:
                print(f"⚠️ Enhanced agents not available: {str(e)}")
        else:
            print("⚠️ Enhanced agents not available (no valid OpenAI API key)")
    
    def analyze_training_documents(self, training_docs: List[str]) -> Dict[str, Any]:
        """
        Analyze all available training documents for reconciliation insights.
        """
        print("📚 Analyzing training documents for reconciliation insights...")
        
        analysis_results = {
            "op_training_analysis": None,
            "visual_analysis": [],
            "enhanced_rules": {},
            "total_documents": len(training_docs),
            "successful_analyses": 0
        }
        
        for doc_path in training_docs:
            if not os.path.exists(doc_path):
                print(f"⚠️ Document not found: {doc_path}")
                continue
            
            print(f"🔍 Analyzing: {doc_path}")
            
            # Analyze OP training document
            if "op-ncb-reconciliation" in doc_path.lower():
                if self.thinking_agent:
                    try:
                        op_analysis = self.thinking_agent.analyze_op_training_document(doc_path)
                        analysis_results["op_training_analysis"] = op_analysis
                        analysis_results["successful_analyses"] += 1
                        print(f"✅ OP training document analyzed")
                    except Exception as e:
                        print(f"❌ Error analyzing OP document: {str(e)}")
                else:
                    # Fallback analysis without API
                    analysis_results["op_training_analysis"] = self._fallback_op_analysis(doc_path)
                    analysis_results["successful_analyses"] += 1
            
            # Analyze visual documents
            elif doc_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                if self.vision_agent:
                    try:
                        visual_analysis = self.vision_agent.analyze_training_document(doc_path)
                        analysis_results["visual_analysis"].append(visual_analysis)
                        analysis_results["successful_analyses"] += 1
                        print(f"✅ Visual document analyzed")
                    except Exception as e:
                        print(f"❌ Error analyzing visual document: {str(e)}")
                else:
                    print(f"⚠️ Vision analysis not available for: {doc_path}")
        
        # Extract enhanced rules from all analyses
        analysis_results["enhanced_rules"] = self._extract_enhanced_rules(analysis_results)
        
        print(f"📊 Training analysis complete: {analysis_results['successful_analyses']}/{analysis_results['total_documents']} documents analyzed")
        return analysis_results
    
    def _fallback_op_analysis(self, doc_path: str) -> Dict[str, Any]:
        """Fallback OP analysis without API calls."""
        try:
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract GL mappings manually
            import re
            gl_mappings = {}
            gl_pattern = r'GL\s*(\d{5})'
            gl_matches = re.findall(gl_pattern, content)
            
            for gl_num in gl_matches:
                # Find context around GL number
                start_idx = content.find(f"GL {gl_num}")
                if start_idx != -1:
                    context = content[start_idx:start_idx + 200]
                    gl_mappings[gl_num] = {
                        "description": context[:100],
                        "extracted_from": "op_training_document_fallback"
                    }
            
            return {
                "document_type": "op_training",
                "file_path": doc_path,
                "gl_mappings": gl_mappings,
                "analysis_method": "fallback_manual_extraction",
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }
            
        except Exception as e:
            return {
                "document_type": "op_training",
                "file_path": doc_path,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }
    
    def _extract_enhanced_rules(self, analysis_results: Dict) -> Dict[str, Any]:
        """Extract enhanced rules from all training analyses."""
        enhanced_rules = {
            "gl_mappings": {},
            "matching_criteria": {},
            "timing_patterns": {},
            "best_practices": []
        }
        
        # Extract from OP training analysis
        if analysis_results.get("op_training_analysis"):
            op_analysis = analysis_results["op_training_analysis"]
            if op_analysis.get("gl_mappings"):
                enhanced_rules["gl_mappings"].update(op_analysis["gl_mappings"])
        
        # Extract from visual analyses
        for visual_analysis in analysis_results.get("visual_analysis", []):
            if visual_analysis.get("status") == "success":
                # Would extract rules from visual analysis
                pass
        
        return enhanced_rules
    
    def run_comprehensive_reconciliation(self, gl_file: str, bank_file: str, 
                                       training_docs: List[str] = None) -> Dict[str, Any]:
        """
        Run comprehensive reconciliation with all AI capabilities.
        """
        print("🚀 Starting Comprehensive Vision-Enhanced Reconciliation...")
        
        # Step 1: Analyze training documents
        training_insights = {}
        if training_docs:
            training_insights = self.analyze_training_documents(training_docs)
            print(f"📚 Training insights: {training_insights['successful_analyses']} documents analyzed")
        
        # Step 2: Run base reconciliation
        print("🤖 Running base AI reconciliation...")
        base_result = self.base_agent.think_and_analyze(gl_file, bank_file)
        
        # Step 3: Apply enhanced thinking if available
        thinking_enhancements = {}
        if self.thinking_agent and training_insights.get("op_training_analysis"):
            try:
                print("🧠 Applying enhanced thinking analysis...")
                thinking_result = self.thinking_agent.think_about_reconciliation_challenges(
                    {
                        "total_balance": base_result.get('ai_analysis', {}).get('total_gl_balance', 0),
                        "accounts": base_result.get('gl_analysis', {}),
                        "transaction_count": sum(len(acc.get('transactions', [])) for acc in base_result.get('gl_analysis', {}).values())
                    },
                    {"transaction_count": 0, "total_balance": 0},
                    training_insights.get("op_training_analysis", {}).get("gl_mappings", {})
                )
                thinking_enhancements["thinking_analysis"] = thinking_result
            except Exception as e:
                print(f"⚠️ Enhanced thinking not available: {str(e)}")
        
        # Step 4: Apply vision enhancements if available
        vision_enhancements = {}
        if self.vision_agent and training_insights.get("visual_analysis"):
            try:
                print("👁️ Applying vision enhancements...")
                vision_result = self.vision_agent.enhance_reconciliation_rules(
                    training_insights["visual_analysis"]
                )
                vision_enhancements["vision_rules"] = vision_result
            except Exception as e:
                print(f"⚠️ Vision enhancements not available: {str(e)}")
        
        # Step 5: Combine all results
        comprehensive_result = {
            **base_result,
            "training_insights": training_insights,
            "thinking_enhancements": thinking_enhancements,
            "vision_enhancements": vision_enhancements,
            "comprehensive_analysis": {
                "training_documents_analyzed": training_insights.get("successful_analyses", 0),
                "enhanced_rules_applied": len(training_insights.get("enhanced_rules", {}).get("gl_mappings", {})),
                "thinking_analysis_available": bool(thinking_enhancements),
                "vision_analysis_available": bool(vision_enhancements)
            }
        }
        
        # Step 6: Save comprehensive report
        self._save_comprehensive_report(comprehensive_result)
        
        return comprehensive_result
    
    def _save_comprehensive_report(self, result: Dict[str, Any]):
        """Save the comprehensive reconciliation report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"comprehensive_vision_reconciliation_report_{timestamp}.json"
        
        with open(report_path, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        
        print(f"📊 Comprehensive report saved: {report_path}")

def main():
    """Main function to demonstrate comprehensive vision reconciliation."""
    import sys
    from excel_agent.utils.paths import list_excel_files
    
    if len(sys.argv) < 3:
        print("Usage: python integrated_vision_reconciliation.py <gl_file> <bank_file> [training_doc1] [training_doc2] ...")
        sys.exit(1)
    
    gl_file = sys.argv[1]
    bank_file = sys.argv[2]
    training_docs = sys.argv[3:] if len(sys.argv) > 3 else []
    
    # Add default training document if none provided
    if not training_docs:
        default_training = "Knowledge Base/op-ncb-reconciliation-8-28-25.md"
        if os.path.exists(default_training):
            training_docs = [default_training]
            print(f"📚 Using default training document: {default_training}")
    
    try:
        # Initialize integrated system
        system = IntegratedVisionReconciliation()
        
        # Run comprehensive reconciliation
        result = system.run_comprehensive_reconciliation(gl_file, bank_file, training_docs)
        
        print("\n🎯 COMPREHENSIVE VISION RECONCILIATION COMPLETE")
        print("=" * 60)
        print(f"Status: {result.get('reconciliation_status', 'Unknown')}")
        print(f"GL Balance: ${result.get('ai_analysis', {}).get('total_gl_balance', 0):.2f}")
        
        comprehensive = result.get('comprehensive_analysis', {})
        print(f"Training Documents Analyzed: {comprehensive.get('training_documents_analyzed', 0)}")
        print(f"Enhanced Rules Applied: {comprehensive.get('enhanced_rules_applied', 0)}")
        print(f"Thinking Analysis: {'Available' if comprehensive.get('thinking_analysis_available') else 'Not Available'}")
        print(f"Vision Analysis: {'Available' if comprehensive.get('vision_analysis_available') else 'Not Available'}")
        
        # Show training insights if available
        training_insights = result.get('training_insights', {})
        if training_insights.get('enhanced_rules', {}).get('gl_mappings'):
            print(f"\n📚 Enhanced GL Mappings Extracted:")
            for gl_num, mapping in list(training_insights['enhanced_rules']['gl_mappings'].items())[:5]:
                print(f"  GL {gl_num}: {mapping.get('description', 'No description')[:50]}...")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
