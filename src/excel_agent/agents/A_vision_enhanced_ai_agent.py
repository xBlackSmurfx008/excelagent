#!/usr/bin/env python3
"""
Vision-Enhanced AI Reconciliation Agent

This agent combines OpenAI's vision capabilities with advanced reconciliation logic
to analyze training documents, images, and improve matching accuracy based on
visual examples and document analysis.
"""

import os
import json
import base64
import openai
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import pandas as pd
from ai_reconciliation_agent import AIReconciliationAgent

class VisionEnhancedAIAgent:
    """
    Enhanced AI agent with vision capabilities for analyzing training documents
    and improving reconciliation accuracy through visual understanding.
    """
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """Initialize the vision-enhanced AI agent."""
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        openai.api_key = self.openai_api_key
        self.base_agent = AIReconciliationAgent()
        self.vision_insights = {}
        self.training_analysis = {}
        
    def analyze_training_document(self, document_path: str) -> Dict[str, Any]:
        """
        Analyze a training document (text or image) to extract reconciliation rules
        and visual patterns for improved matching.
        """
        print(f"🔍 Analyzing training document: {document_path}")
        
        if not os.path.exists(document_path):
            return {"error": f"Document not found: {document_path}"}
        
        # Determine if it's an image or text document
        file_ext = Path(document_path).suffix.lower()
        
        if file_ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']:
            return self._analyze_image_document(document_path)
        elif file_ext in ['.md', '.txt', '.pdf']:
            return self._analyze_text_document(document_path)
        else:
            return {"error": f"Unsupported file type: {file_ext}"}
    
    def _analyze_image_document(self, image_path: str) -> Dict[str, Any]:
        """Analyze an image document using OpenAI's vision API."""
        try:
            # Encode image to base64
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Determine image format for API
            file_ext = Path(image_path).suffix.lower()
            if file_ext == '.png':
                image_format = "png"
            elif file_ext in ['.jpg', '.jpeg']:
                image_format = "jpeg"
            else:
                image_format = "png"  # default
            
            # Call OpenAI Vision API
            response = openai.ChatCompletion.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """Analyze this reconciliation training document image. Extract:
1. GL account mappings and rules
2. Visual patterns for transaction matching
3. Reconciliation workflow steps shown
4. Any specific formatting or layout rules
5. Timing difference examples
6. Error patterns to watch for
7. Best practices demonstrated

Provide detailed analysis in JSON format with categories for each finding."""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/{image_format};base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=2000
            )
            
            analysis = response.choices[0].message.content
            print(f"✅ Vision analysis completed for {image_path}")
            
            return {
                "document_type": "image",
                "file_path": image_path,
                "analysis": analysis,
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }
            
        except Exception as e:
            print(f"❌ Error analyzing image {image_path}: {str(e)}")
            return {
                "document_type": "image",
                "file_path": image_path,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }
    
    def _analyze_text_document(self, text_path: str) -> Dict[str, Any]:
        """Analyze a text document for reconciliation rules and patterns."""
        try:
            with open(text_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Use GPT-4 to analyze the text content
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert in financial reconciliation and credit union operations. 
                        Analyze the provided training document and extract:
                        1. GL account mapping rules
                        2. Transaction matching criteria
                        3. Timing difference patterns
                        4. Reconciliation workflow steps
                        5. Error detection methods
                        6. Best practices and procedures
                        
                        Format your response as structured JSON with clear categories."""
                    },
                    {
                        "role": "user",
                        "content": f"Analyze this reconciliation training document:\n\n{content}"
                    }
                ],
                max_tokens=2000
            )
            
            analysis = response.choices[0].message.content
            print(f"✅ Text analysis completed for {text_path}")
            
            return {
                "document_type": "text",
                "file_path": text_path,
                "analysis": analysis,
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }
            
        except Exception as e:
            print(f"❌ Error analyzing text {text_path}: {str(e)}")
            return {
                "document_type": "text",
                "file_path": text_path,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }
    
    def enhance_reconciliation_rules(self, training_analyses: List[Dict]) -> Dict[str, Any]:
        """
        Enhance reconciliation rules based on training document analysis.
        """
        print("🧠 Enhancing reconciliation rules based on training analysis...")
        
        enhanced_rules = {
            "gl_mappings": {},
            "matching_criteria": {},
            "timing_patterns": {},
            "error_patterns": {},
            "best_practices": [],
            "workflow_steps": []
        }
        
        for analysis in training_analyses:
            if analysis.get("status") == "success":
                try:
                    # Parse the analysis content (assuming it's JSON or structured text)
                    content = analysis.get("analysis", "")
                    
                    # Extract GL mappings
                    if "GL" in content or "gl" in content:
                        enhanced_rules["gl_mappings"].update(
                            self._extract_gl_mappings(content)
                        )
                    
                    # Extract matching criteria
                    if "match" in content.lower() or "reconcile" in content.lower():
                        enhanced_rules["matching_criteria"].update(
                            self._extract_matching_criteria(content)
                        )
                    
                    # Extract timing patterns
                    if "timing" in content.lower() or "difference" in content.lower():
                        enhanced_rules["timing_patterns"].update(
                            self._extract_timing_patterns(content)
                        )
                    
                except Exception as e:
                    print(f"⚠️ Error processing analysis: {str(e)}")
        
        print(f"✅ Enhanced rules extracted: {len(enhanced_rules['gl_mappings'])} GL mappings")
        return enhanced_rules
    
    def _extract_gl_mappings(self, content: str) -> Dict[str, Any]:
        """Extract GL account mappings from analysis content."""
        mappings = {}
        # Look for GL numbers and their descriptions
        import re
        
        gl_pattern = r'GL\s*(\d{5})'
        gl_matches = re.findall(gl_pattern, content)
        
        for gl_num in gl_matches:
            # Try to find description near the GL number
            context = content[content.find(f"GL {gl_num}"):content.find(f"GL {gl_num}") + 200]
            mappings[gl_num] = {
                "description": context[:100] if context else "Unknown",
                "source": "training_analysis"
            }
        
        return mappings
    
    def _extract_matching_criteria(self, content: str) -> Dict[str, Any]:
        """Extract transaction matching criteria from analysis content."""
        criteria = {}
        
        # Look for matching rules and patterns
        if "amount" in content.lower():
            criteria["amount_matching"] = "Exact amount matching required"
        if "date" in content.lower():
            criteria["date_matching"] = "Date proximity matching"
        if "description" in content.lower():
            criteria["description_matching"] = "Description similarity matching"
        
        return criteria
    
    def _extract_timing_patterns(self, content: str) -> Dict[str, Any]:
        """Extract timing difference patterns from analysis content."""
        patterns = {}
        
        # Look for timing-related information
        if "last day" in content.lower():
            patterns["month_end_timing"] = "Transactions posted on last day of month"
        if "settlement" in content.lower():
            patterns["settlement_timing"] = "Settlement activity timing differences"
        
        return patterns
    
    def run_enhanced_reconciliation(self, gl_file: str, bank_file: str, 
                                 training_docs: List[str] = None) -> Dict[str, Any]:
        """
        Run enhanced reconciliation with vision-enhanced understanding.
        """
        print("🚀 Starting Vision-Enhanced Reconciliation...")
        
        # Analyze training documents if provided
        training_analyses = []
        if training_docs:
            for doc_path in training_docs:
                analysis = self.analyze_training_document(doc_path)
                training_analyses.append(analysis)
        
        # Enhance rules based on training analysis
        enhanced_rules = self.enhance_reconciliation_rules(training_analyses)
        
        # Run base reconciliation
        base_result = self.base_agent.think_and_analyze(gl_file, bank_file)
        
        # Enhance the result with vision insights
        enhanced_result = {
            **base_result,
            "vision_enhancements": {
                "training_analyses": training_analyses,
                "enhanced_rules": enhanced_rules,
                "improvement_suggestions": self._generate_improvement_suggestions(enhanced_rules)
            }
        }
        
        # Save enhanced report
        self._save_enhanced_report(enhanced_result)
        
        return enhanced_result
    
    def _generate_improvement_suggestions(self, enhanced_rules: Dict) -> List[str]:
        """Generate improvement suggestions based on enhanced rules."""
        suggestions = []
        
        if enhanced_rules.get("gl_mappings"):
            suggestions.append("Enhanced GL mappings available for better transaction categorization")
        
        if enhanced_rules.get("matching_criteria"):
            suggestions.append("Improved matching criteria identified from training documents")
        
        if enhanced_rules.get("timing_patterns"):
            suggestions.append("Timing difference patterns documented for better reconciliation")
        
        return suggestions
    
    def _save_enhanced_report(self, result: Dict[str, Any]):
        """Save the enhanced reconciliation report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"vision_enhanced_reconciliation_report_{timestamp}.json"
        
        with open(report_path, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        
        print(f"📊 Enhanced report saved: {report_path}")

def main():
    """Main function to demonstrate vision-enhanced reconciliation."""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python vision_enhanced_ai_agent.py <gl_file> <bank_file> [training_doc1] [training_doc2] ...")
        sys.exit(1)
    
    gl_file = sys.argv[1]
    bank_file = sys.argv[2]
    training_docs = sys.argv[3:] if len(sys.argv) > 3 else []
    
    try:
        agent = VisionEnhancedAIAgent()
        result = agent.run_enhanced_reconciliation(gl_file, bank_file, training_docs)
        
        print("\n🎯 VISION-ENHANCED RECONCILIATION COMPLETE")
        print("=" * 50)
        print(f"Status: {result.get('reconciliation_status', 'Unknown')}")
        print(f"GL Balance: ${result.get('ai_analysis', {}).get('total_gl_balance', 0):.2f}")
        
        if result.get('vision_enhancements'):
            enhancements = result['vision_enhancements']
            print(f"Training Documents Analyzed: {len(enhancements.get('training_analyses', []))}")
            print(f"Enhanced GL Mappings: {len(enhancements.get('enhanced_rules', {}).get('gl_mappings', {}))}")
            print(f"Improvement Suggestions: {len(enhancements.get('improvement_suggestions', []))}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
