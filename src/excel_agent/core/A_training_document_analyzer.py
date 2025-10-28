#!/usr/bin/env python3
"""
Training Document Analyzer
Analyzes training documents using deep thinking and OpenAI API for comprehensive insights
"""

import os
import json
import openai
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import pandas as pd
import openpyxl
from strands_base_agent import StrandsBaseAgent
from training_data_manager import TrainingDataManager

class TrainingDocumentAnalyzer(StrandsBaseAgent):
    """
    Advanced analyzer that performs deep thinking analysis on training documents
    to extract comprehensive insights for reconciliation processes.
    """
    
    def __init__(self, 
                 config: Optional[Dict[str, Any]] = None,
                 training_data_path: Optional[str] = None,
                 openai_api_key: Optional[str] = None):
        """
        Initialize the training document analyzer.
        
        Args:
            config: Configuration dictionary
            training_data_path: Path to training data directory
            openai_api_key: OpenAI API key for deep thinking capabilities
        """
        super().__init__(
            name="TrainingDocumentAnalyzer",
            config=config,
            training_data_path=training_data_path
        )
        
        # Initialize OpenAI
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required for deep thinking capabilities")
        
        openai.api_key = self.openai_api_key
        
        # Initialize training data manager
        self.tdm = TrainingDataManager(training_data_path)
        
        # Analysis configuration
        self.analysis_rounds = 10
        self.deep_insights = {}
        self.pattern_library = {}
        self.rule_effectiveness = {}
        
        self.logger.info("Training Document Analyzer initialized with OpenAI API")
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process deep analysis of training documents.
        
        Args:
            input_data: Dictionary containing analysis parameters
            
        Returns:
            Comprehensive training document analysis results
        """
        try:
            self.logger.info("Starting deep training document analysis")
            
            # Phase 1: Analyze OP manual with deep thinking
            op_analysis = self._analyze_op_manual_with_deep_thinking()
            
            # Phase 2: Analyze historical patterns with deep thinking
            pattern_analysis = self._analyze_historical_patterns_with_deep_thinking()
            
            # Phase 3: Analyze reconciliation rules with deep thinking
            rules_analysis = self._analyze_reconciliation_rules_with_deep_thinking()
            
            # Phase 4: Synthesize all insights
            synthesis = self._synthesize_training_insights(op_analysis, pattern_analysis, rules_analysis)
            
            # Phase 5: Generate actionable recommendations
            recommendations = self._generate_training_recommendations(synthesis)
            
            return {
                "training_analysis_results": {
                    "op_manual_analysis": op_analysis,
                    "pattern_analysis": pattern_analysis,
                    "rules_analysis": rules_analysis,
                    "synthesis": synthesis,
                    "recommendations": recommendations
                },
                "analysis_rounds_completed": self.analysis_rounds,
                "analysis_timestamp": datetime.now().isoformat(),
                "total_insights_generated": len(self.deep_insights)
            }
            
        except Exception as e:
            self.logger.error(f"Error in training document analysis: {str(e)}")
            raise
    
    def _analyze_op_manual_with_deep_thinking(self) -> Dict[str, Any]:
        """Analyze OP manual with 10 rounds of deep thinking."""
        self.logger.info("🧠 Starting deep thinking analysis of OP manual...")
        
        op_manual = self.tdm.get_training_data("op_manual")
        if not op_manual:
            self.logger.warning("No OP manual data found")
            return {"error": "No OP manual data available"}
        
        op_analysis = {
            "rounds_completed": 0,
            "insights_per_round": [],
            "cumulative_insights": [],
            "gl_account_analysis": {},
            "timing_analysis": {},
            "matching_rules_analysis": {},
            "confidence_evolution": []
        }
        
        for round_num in range(1, self.analysis_rounds + 1):
            self.logger.info(f"🔄 OP Manual Deep Thinking Round {round_num}/10")
            
            # Create thinking prompt for this round
            thinking_prompt = self._create_op_manual_thinking_prompt(round_num, op_manual)
            
            # Perform deep thinking using OpenAI
            round_insights = self._perform_openai_thinking(thinking_prompt, round_num)
            
            # Process and store insights
            op_analysis["insights_per_round"].append(round_insights)
            op_analysis["rounds_completed"] = round_num
            
            # Update cumulative insights
            self._update_cumulative_insights(round_insights, op_analysis)
            
            # Calculate confidence score for this round
            confidence = self._calculate_confidence_score(round_insights)
            op_analysis["confidence_evolution"].append(confidence)
            
            self.logger.info(f"✅ OP Manual Round {round_num} completed - Confidence: {confidence:.2f}")
        
        # Generate final insights
        op_analysis["final_insights"] = self._generate_op_manual_final_insights(op_analysis, op_manual)
        
        self.logger.info("🎯 OP manual deep analysis completed")
        return op_analysis
    
    def _create_op_manual_thinking_prompt(self, round_num: int, op_manual: Dict[str, Any]) -> str:
        """Create a sophisticated thinking prompt for OP manual analysis."""
        
        base_prompt = f"""
You are an expert financial reconciliation analyst performing round {round_num} of 10 deep thinking sessions to analyze the OP manual for reconciliation processes. Your goal is to extract increasingly sophisticated insights about GL account mappings, bank activity patterns, and reconciliation rules.

OP MANUAL DATA STRUCTURE:
- GL Accounts: {len(op_manual.get('gl_accounts', {}))} accounts defined
- Timing Differences: {len(op_manual.get('timing_differences', {}))} timing rules
- Validation Rules: {len(op_manual.get('validation_rules', {}))} validation criteria

GL ACCOUNTS AVAILABLE:
{json.dumps(list(op_manual.get('gl_accounts', {}).keys()), indent=2)}

TIMING DIFFERENCES:
{json.dumps(op_manual.get('timing_differences', {}), indent=2)}

THINKING FOCUS FOR ROUND {round_num}:
"""
        
        if round_num == 1:
            focus = "Focus on understanding the basic structure and relationships between GL accounts and bank activities. Identify fundamental patterns and rules."
        elif round_num == 2:
            focus = "Analyze the variance thresholds for each GL account. Consider why different accounts have different tolerance levels and their effectiveness."
        elif round_num == 3:
            focus = "Examine the matching keywords and their reliability. Analyze which keywords work best for different types of transactions."
        elif round_num == 4:
            focus = "Investigate timing differences and their impact on reconciliation accuracy. Look for patterns in when transactions are posted vs when they appear in bank statements."
        elif round_num == 5:
            focus = "Analyze the bank activity descriptions and their consistency. Look for patterns that could improve matching accuracy."
        elif round_num == 6:
            focus = "Examine the expected timing patterns and their reliability. Consider how timing differences affect reconciliation success."
        elif round_num == 7:
            focus = "Look for edge cases and exceptions in the GL account mappings. Identify scenarios where standard rules might not apply."
        elif round_num == 8:
            focus = "Analyze the validation rules and their effectiveness. Consider how these rules prevent reconciliation errors."
        elif round_num == 9:
            focus = "Synthesize insights from previous rounds. Look for connections and relationships between different aspects of the OP manual."
        else:  # round_num == 10
            focus = "Generate final comprehensive insights and recommendations. Create actionable strategies for improving reconciliation processes based on OP manual analysis."
        
        prompt = f"{base_prompt}\n{focus}\n\nProvide your deep analysis in the following format:\n1. Key Insights Discovered\n2. Pattern Analysis\n3. Rule Effectiveness Assessment\n4. GL Account Specific Insights\n5. Recommendations for Improvement\n6. Confidence Level (1-10)\n7. Questions for Further Investigation"
        
        return prompt
    
    def _analyze_historical_patterns_with_deep_thinking(self) -> Dict[str, Any]:
        """Analyze historical patterns with 10 rounds of deep thinking."""
        self.logger.info("🧠 Starting deep thinking analysis of historical patterns...")
        
        historical_patterns = self.tdm.get_training_data("historical_patterns")
        if not historical_patterns:
            self.logger.warning("No historical patterns data found")
            return {"error": "No historical patterns data available"}
        
        pattern_analysis = {
            "rounds_completed": 0,
            "insights_per_round": [],
            "cumulative_insights": [],
            "discrepancy_analysis": {},
            "success_pattern_analysis": {},
            "learning_insights_analysis": {},
            "confidence_evolution": []
        }
        
        for round_num in range(1, self.analysis_rounds + 1):
            self.logger.info(f"🔄 Historical Patterns Deep Thinking Round {round_num}/10")
            
            # Create thinking prompt for this round
            thinking_prompt = self._create_historical_patterns_thinking_prompt(round_num, historical_patterns)
            
            # Perform deep thinking using OpenAI
            round_insights = self._perform_openai_thinking(thinking_prompt, round_num)
            
            # Process and store insights
            pattern_analysis["insights_per_round"].append(round_insights)
            pattern_analysis["rounds_completed"] = round_num
            
            # Update cumulative insights
            self._update_cumulative_insights(round_insights, pattern_analysis)
            
            # Calculate confidence score for this round
            confidence = self._calculate_confidence_score(round_insights)
            pattern_analysis["confidence_evolution"].append(confidence)
            
            self.logger.info(f"✅ Historical Patterns Round {round_num} completed - Confidence: {confidence:.2f}")
        
        # Generate final insights
        pattern_analysis["final_insights"] = self._generate_historical_patterns_final_insights(pattern_analysis, historical_patterns)
        
        self.logger.info("🎯 Historical patterns deep analysis completed")
        return pattern_analysis
    
    def _create_historical_patterns_thinking_prompt(self, round_num: int, historical_patterns: Dict[str, Any]) -> str:
        """Create a sophisticated thinking prompt for historical patterns analysis."""
        
        base_prompt = f"""
You are an expert financial reconciliation analyst performing round {round_num} of 10 deep thinking sessions to analyze historical patterns in reconciliation processes. Your goal is to extract insights about common discrepancies, success patterns, and learning opportunities.

HISTORICAL PATTERNS DATA:
- Common Discrepancies: {len(historical_patterns.get('common_discrepancies', []))} types identified
- Success Patterns: {len(historical_patterns.get('success_patterns', []))} success patterns
- Learning Insights: {len(historical_patterns.get('learning_insights', {}))} learning metrics

COMMON DISCREPANCIES:
{json.dumps(historical_patterns.get('common_discrepancies', []), indent=2)}

SUCCESS PATTERNS:
{json.dumps(historical_patterns.get('success_patterns', []), indent=2)}

LEARNING INSIGHTS:
{json.dumps(historical_patterns.get('learning_insights', {}), indent=2)}

THINKING FOCUS FOR ROUND {round_num}:
"""
        
        if round_num == 1:
            focus = "Focus on understanding the types and frequencies of common discrepancies. Identify patterns in reconciliation failures."
        elif round_num == 2:
            focus = "Analyze success patterns and their characteristics. Understand what makes reconciliations successful."
        elif round_num == 3:
            focus = "Examine the frequency and severity of different discrepancy types. Look for patterns in when and why they occur."
        elif round_num == 4:
            focus = "Investigate the resolution strategies for different discrepancy types. Analyze their effectiveness."
        elif round_num == 5:
            focus = "Analyze the confidence levels of different success patterns. Understand which patterns are most reliable."
        elif round_num == 6:
            focus = "Examine the learning insights and their implications. Look for trends in reconciliation performance."
        elif round_num == 7:
            focus = "Look for correlations between discrepancy types and success patterns. Identify prevention strategies."
        elif round_num == 8:
            focus = "Analyze the improvement areas and their priority. Consider which areas need the most attention."
        elif round_num == 9:
            focus = "Synthesize insights from previous rounds. Look for connections between patterns and learning opportunities."
        else:  # round_num == 10
            focus = "Generate final comprehensive insights and recommendations. Create actionable strategies for improving reconciliation processes based on historical patterns."
        
        prompt = f"{base_prompt}\n{focus}\n\nProvide your deep analysis in the following format:\n1. Key Insights Discovered\n2. Pattern Analysis\n3. Discrepancy Analysis\n4. Success Pattern Analysis\n5. Learning Insights Analysis\n6. Recommendations for Improvement\n7. Confidence Level (1-10)\n8. Questions for Further Investigation"
        
        return prompt
    
    def _analyze_reconciliation_rules_with_deep_thinking(self) -> Dict[str, Any]:
        """Analyze reconciliation rules with 10 rounds of deep thinking."""
        self.logger.info("🧠 Starting deep thinking analysis of reconciliation rules...")
        
        reconciliation_rules = self.tdm.get_training_data("reconciliation_rules")
        if not reconciliation_rules:
            self.logger.warning("No reconciliation rules data found")
            return {"error": "No reconciliation rules data available"}
        
        rules_analysis = {
            "rounds_completed": 0,
            "insights_per_round": [],
            "cumulative_insights": [],
            "matching_criteria_analysis": {},
            "validation_rules_analysis": {},
            "reporting_rules_analysis": {},
            "quality_thresholds_analysis": {},
            "confidence_evolution": []
        }
        
        for round_num in range(1, self.analysis_rounds + 1):
            self.logger.info(f"🔄 Reconciliation Rules Deep Thinking Round {round_num}/10")
            
            # Create thinking prompt for this round
            thinking_prompt = self._create_reconciliation_rules_thinking_prompt(round_num, reconciliation_rules)
            
            # Perform deep thinking using OpenAI
            round_insights = self._perform_openai_thinking(thinking_prompt, round_num)
            
            # Process and store insights
            rules_analysis["insights_per_round"].append(round_insights)
            rules_analysis["rounds_completed"] = round_num
            
            # Update cumulative insights
            self._update_cumulative_insights(round_insights, rules_analysis)
            
            # Calculate confidence score for this round
            confidence = self._calculate_confidence_score(round_insights)
            rules_analysis["confidence_evolution"].append(confidence)
            
            self.logger.info(f"✅ Reconciliation Rules Round {round_num} completed - Confidence: {confidence:.2f}")
        
        # Generate final insights
        rules_analysis["final_insights"] = self._generate_reconciliation_rules_final_insights(rules_analysis, reconciliation_rules)
        
        self.logger.info("🎯 Reconciliation rules deep analysis completed")
        return rules_analysis
    
    def _create_reconciliation_rules_thinking_prompt(self, round_num: int, reconciliation_rules: Dict[str, Any]) -> str:
        """Create a sophisticated thinking prompt for reconciliation rules analysis."""
        
        base_prompt = f"""
You are an expert financial reconciliation analyst performing round {round_num} of 10 deep thinking sessions to analyze reconciliation rules and their effectiveness. Your goal is to extract insights about matching criteria, validation rules, and quality thresholds.

RECONCILIATION RULES DATA:
- Matching Criteria: {len(reconciliation_rules.get('matching_criteria', {}))} criteria defined
- Validation Rules: {len(reconciliation_rules.get('validation_rules', {}))} validation rules
- Reporting Rules: {len(reconciliation_rules.get('reporting_rules', {}))} reporting rules
- Quality Thresholds: {len(reconciliation_rules.get('quality_thresholds', {}))} quality thresholds

MATCHING CRITERIA:
{json.dumps(reconciliation_rules.get('matching_criteria', {}), indent=2)}

VALIDATION RULES:
{json.dumps(reconciliation_rules.get('validation_rules', {}), indent=2)}

REPORTING RULES:
{json.dumps(reconciliation_rules.get('reporting_rules', {}), indent=2)}

QUALITY THRESHOLDS:
{json.dumps(reconciliation_rules.get('quality_thresholds', {}), indent=2)}

THINKING FOCUS FOR ROUND {round_num}:
"""
        
        if round_num == 1:
            focus = "Focus on understanding the matching criteria and their effectiveness. Identify which criteria work best for different types of transactions."
        elif round_num == 2:
            focus = "Analyze the validation rules and their impact on data quality. Consider how these rules prevent reconciliation errors."
        elif round_num == 3:
            focus = "Examine the reporting rules and their usefulness. Understand how these rules support reconciliation processes."
        elif round_num == 4:
            focus = "Investigate the quality thresholds and their appropriateness. Consider whether these thresholds are too strict or too lenient."
        elif round_num == 5:
            focus = "Analyze the tolerance levels in matching criteria. Look for patterns in what works best for different scenarios."
        elif round_num == 6:
            focus = "Examine the required fields and their necessity. Consider which fields are essential for successful reconciliation."
        elif round_num == 7:
            focus = "Look for edge cases and exceptions in the rules. Identify scenarios where standard rules might not apply."
        elif round_num == 8:
            focus = "Analyze the interaction between different rule types. Consider how they work together to ensure reconciliation success."
        elif round_num == 9:
            focus = "Synthesize insights from previous rounds. Look for connections between different aspects of the reconciliation rules."
        else:  # round_num == 10
            focus = "Generate final comprehensive insights and recommendations. Create actionable strategies for improving reconciliation rules based on analysis."
        
        prompt = f"{base_prompt}\n{focus}\n\nProvide your deep analysis in the following format:\n1. Key Insights Discovered\n2. Matching Criteria Analysis\n3. Validation Rules Analysis\n4. Reporting Rules Analysis\n5. Quality Thresholds Analysis\n6. Recommendations for Improvement\n7. Confidence Level (1-10)\n8. Questions for Further Investigation"
        
        return prompt
    
    def _perform_openai_thinking(self, prompt: str, round_num: int) -> Dict[str, Any]:
        """Perform deep thinking using OpenAI API."""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert financial reconciliation analyst with deep expertise in GL accounting, bank statement analysis, and reconciliation processes. Provide detailed, analytical responses with specific insights and actionable recommendations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2500,
                temperature=0.7,
                top_p=0.9
            )
            
            thinking_result = {
                "round": round_num,
                "timestamp": datetime.now().isoformat(),
                "raw_response": response.choices[0].message.content,
                "parsed_insights": self._parse_thinking_response(response.choices[0].message.content),
                "model_used": "gpt-4",
                "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else 0
            }
            
            return thinking_result
            
        except Exception as e:
            self.logger.error(f"Error in OpenAI thinking round {round_num}: {str(e)}")
            return {
                "round": round_num,
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "parsed_insights": {}
            }
    
    def _parse_thinking_response(self, response: str) -> Dict[str, Any]:
        """Parse the thinking response to extract structured insights."""
        try:
            lines = response.split('\n')
            insights = {
                "key_insights": [],
                "pattern_analysis": [],
                "rule_assessment": [],
                "recommendations": [],
                "confidence_level": 5,
                "questions": []
            }
            
            current_section = None
            for line in lines:
                line = line.strip()
                if line.startswith('1.') or 'Key Insights' in line:
                    current_section = 'key_insights'
                elif line.startswith('2.') or 'Pattern Analysis' in line:
                    current_section = 'pattern_analysis'
                elif line.startswith('3.') or 'Rule Effectiveness' in line or 'Rule Assessment' in line:
                    current_section = 'rule_assessment'
                elif line.startswith('4.') or 'Recommendations' in line:
                    current_section = 'recommendations'
                elif line.startswith('5.') or 'Confidence Level' in line:
                    current_section = 'confidence'
                elif line.startswith('6.') or 'Questions' in line:
                    current_section = 'questions'
                elif line and current_section and not line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.')):
                    if current_section == 'confidence':
                        try:
                            insights['confidence_level'] = float(line.split(':')[-1].strip())
                        except:
                            pass
                    else:
                        insights[current_section].append(line)
            
            return insights
            
        except Exception as e:
            self.logger.error(f"Error parsing thinking response: {str(e)}")
            return {"error": str(e)}
    
    def _update_cumulative_insights(self, round_insights: Dict[str, Any], analysis: Dict[str, Any]):
        """Update cumulative insights from each round."""
        if "parsed_insights" in round_insights:
            insights = round_insights["parsed_insights"]
            
            # Add to cumulative insights
            for key, value in insights.items():
                if key != "confidence_level" and isinstance(value, list):
                    if key not in analysis["cumulative_insights"]:
                        analysis["cumulative_insights"][key] = []
                    analysis["cumulative_insights"][key].extend(value)
    
    def _calculate_confidence_score(self, round_insights: Dict[str, Any]) -> float:
        """Calculate confidence score for a round."""
        if "parsed_insights" in round_insights and "confidence_level" in round_insights["parsed_insights"]:
            return round_insights["parsed_insights"]["confidence_level"]
        return 5.0  # Default confidence
    
    def _generate_op_manual_final_insights(self, op_analysis: Dict[str, Any], op_manual: Dict[str, Any]) -> Dict[str, Any]:
        """Generate final insights from OP manual analysis."""
        final_insights = {
            "total_rounds": op_analysis["rounds_completed"],
            "average_confidence": sum(op_analysis["confidence_evolution"]) / len(op_analysis["confidence_evolution"]) if op_analysis["confidence_evolution"] else 0,
            "key_discoveries": [],
            "pattern_insights": [],
            "rule_insights": [],
            "recommendations": [],
            "gl_account_insights": {},
            "synthesis": ""
        }
        
        # Extract unique insights
        cumulative = op_analysis["cumulative_insights"]
        final_insights["key_discoveries"] = list(set(cumulative.get("key_insights", [])))
        final_insights["pattern_insights"] = list(set(cumulative.get("pattern_analysis", [])))
        final_insights["rule_insights"] = list(set(cumulative.get("rule_assessment", [])))
        final_insights["recommendations"] = list(set(cumulative.get("recommendations", [])))
        
        # Generate GL account specific insights
        for gl_account in op_manual.get("gl_accounts", {}).keys():
            final_insights["gl_account_insights"][gl_account] = {
                "account_name": op_manual["gl_accounts"][gl_account].get("name", ""),
                "variance_threshold": op_manual["gl_accounts"][gl_account].get("variance_threshold", 0),
                "matching_keywords": op_manual["gl_accounts"][gl_account].get("matching_keywords", []),
                "expected_timing": op_manual["gl_accounts"][gl_account].get("expected_timing", "")
            }
        
        # Generate synthesis
        final_insights["synthesis"] = self._generate_op_manual_synthesis(final_insights)
        
        return final_insights
    
    def _generate_historical_patterns_final_insights(self, pattern_analysis: Dict[str, Any], historical_patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Generate final insights from historical patterns analysis."""
        final_insights = {
            "total_rounds": pattern_analysis["rounds_completed"],
            "average_confidence": sum(pattern_analysis["confidence_evolution"]) / len(pattern_analysis["confidence_evolution"]) if pattern_analysis["confidence_evolution"] else 0,
            "key_discoveries": [],
            "pattern_insights": [],
            "discrepancy_insights": [],
            "success_insights": [],
            "recommendations": [],
            "synthesis": ""
        }
        
        # Extract unique insights
        cumulative = pattern_analysis["cumulative_insights"]
        final_insights["key_discoveries"] = list(set(cumulative.get("key_insights", [])))
        final_insights["pattern_insights"] = list(set(cumulative.get("pattern_analysis", [])))
        final_insights["discrepancy_insights"] = list(set(cumulative.get("discrepancy_analysis", [])))
        final_insights["success_insights"] = list(set(cumulative.get("success_pattern_analysis", [])))
        final_insights["recommendations"] = list(set(cumulative.get("recommendations", [])))
        
        # Generate synthesis
        final_insights["synthesis"] = self._generate_historical_patterns_synthesis(final_insights)
        
        return final_insights
    
    def _generate_reconciliation_rules_final_insights(self, rules_analysis: Dict[str, Any], reconciliation_rules: Dict[str, Any]) -> Dict[str, Any]:
        """Generate final insights from reconciliation rules analysis."""
        final_insights = {
            "total_rounds": rules_analysis["rounds_completed"],
            "average_confidence": sum(rules_analysis["confidence_evolution"]) / len(rules_analysis["confidence_evolution"]) if rules_analysis["confidence_evolution"] else 0,
            "key_discoveries": [],
            "matching_insights": [],
            "validation_insights": [],
            "reporting_insights": [],
            "quality_insights": [],
            "recommendations": [],
            "synthesis": ""
        }
        
        # Extract unique insights
        cumulative = rules_analysis["cumulative_insights"]
        final_insights["key_discoveries"] = list(set(cumulative.get("key_insights", [])))
        final_insights["matching_insights"] = list(set(cumulative.get("matching_criteria_analysis", [])))
        final_insights["validation_insights"] = list(set(cumulative.get("validation_rules_analysis", [])))
        final_insights["reporting_insights"] = list(set(cumulative.get("reporting_rules_analysis", [])))
        final_insights["quality_insights"] = list(set(cumulative.get("quality_thresholds_analysis", [])))
        final_insights["recommendations"] = list(set(cumulative.get("recommendations", [])))
        
        # Generate synthesis
        final_insights["synthesis"] = self._generate_reconciliation_rules_synthesis(final_insights)
        
        return final_insights
    
    def _generate_op_manual_synthesis(self, insights: Dict[str, Any]) -> str:
        """Generate synthesis text for OP manual insights."""
        synthesis = f"""
Based on {insights['total_rounds']} rounds of deep thinking analysis with an average confidence of {insights['average_confidence']:.1f}/10, the following key insights have been discovered about the OP manual:

KEY DISCOVERIES ({len(insights['key_discoveries'])}):
{chr(10).join(f"- {discovery}" for discovery in insights['key_discoveries'][:10])}

PATTERN INSIGHTS ({len(insights['pattern_insights'])}):
{chr(10).join(f"- {pattern}" for pattern in insights['pattern_insights'][:10])}

RULE INSIGHTS ({len(insights['rule_insights'])}):
{chr(10).join(f"- {rule}" for rule in insights['rule_insights'][:10])}

GL ACCOUNT INSIGHTS:
- {len(insights['gl_account_insights'])} GL accounts analyzed
- Variance thresholds range from ${min(acc.get('variance_threshold', 0) for acc in insights['gl_account_insights'].values()):,.2f} to ${max(acc.get('variance_threshold', 0) for acc in insights['gl_account_insights'].values()):,.2f}

RECOMMENDATIONS ({len(insights['recommendations'])}):
{chr(10).join(f"- {rec}" for rec in insights['recommendations'][:10])}
"""
        return synthesis
    
    def _generate_historical_patterns_synthesis(self, insights: Dict[str, Any]) -> str:
        """Generate synthesis text for historical patterns insights."""
        synthesis = f"""
Based on {insights['total_rounds']} rounds of deep thinking analysis with an average confidence of {insights['average_confidence']:.1f}/10, the following key insights have been discovered about historical patterns:

KEY DISCOVERIES ({len(insights['key_discoveries'])}):
{chr(10).join(f"- {discovery}" for discovery in insights['key_discoveries'][:10])}

PATTERN INSIGHTS ({len(insights['pattern_insights'])}):
{chr(10).join(f"- {pattern}" for pattern in insights['pattern_insights'][:10])}

DISCREPANCY INSIGHTS ({len(insights['discrepancy_insights'])}):
{chr(10).join(f"- {discrepancy}" for discrepancy in insights['discrepancy_insights'][:10])}

SUCCESS INSIGHTS ({len(insights['success_insights'])}):
{chr(10).join(f"- {success}" for success in insights['success_insights'][:10])}

RECOMMENDATIONS ({len(insights['recommendations'])}):
{chr(10).join(f"- {rec}" for rec in insights['recommendations'][:10])}
"""
        return synthesis
    
    def _generate_reconciliation_rules_synthesis(self, insights: Dict[str, Any]) -> str:
        """Generate synthesis text for reconciliation rules insights."""
        synthesis = f"""
Based on {insights['total_rounds']} rounds of deep thinking analysis with an average confidence of {insights['average_confidence']:.1f}/10, the following key insights have been discovered about reconciliation rules:

KEY DISCOVERIES ({len(insights['key_discoveries'])}):
{chr(10).join(f"- {discovery}" for discovery in insights['key_discoveries'][:10])}

MATCHING INSIGHTS ({len(insights['matching_insights'])}):
{chr(10).join(f"- {matching}" for matching in insights['matching_insights'][:10])}

VALIDATION INSIGHTS ({len(insights['validation_insights'])}):
{chr(10).join(f"- {validation}" for validation in insights['validation_insights'][:10])}

REPORTING INSIGHTS ({len(insights['reporting_insights'])}):
{chr(10).join(f"- {reporting}" for reporting in insights['reporting_insights'][:10])}

QUALITY INSIGHTS ({len(insights['quality_insights'])}):
{chr(10).join(f"- {quality}" for quality in insights['quality_insights'][:10])}

RECOMMENDATIONS ({len(insights['recommendations'])}):
{chr(10).join(f"- {rec}" for rec in insights['recommendations'][:10])}
"""
        return synthesis
    
    def _synthesize_training_insights(self, op_analysis: Dict[str, Any], pattern_analysis: Dict[str, Any], rules_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize insights from all training analysis phases."""
        synthesis = {
            "synthesis_timestamp": datetime.now().isoformat(),
            "total_rounds_completed": op_analysis["rounds_completed"] + pattern_analysis["rounds_completed"] + rules_analysis["rounds_completed"],
            "average_confidence": 0,
            "key_findings": [],
            "pattern_correlations": {},
            "rule_effectiveness": {},
            "strategic_insights": [],
            "comprehensive_recommendations": []
        }
        
        # Calculate average confidence
        confidences = []
        if op_analysis.get("confidence_evolution"):
            confidences.extend(op_analysis["confidence_evolution"])
        if pattern_analysis.get("confidence_evolution"):
            confidences.extend(pattern_analysis["confidence_evolution"])
        if rules_analysis.get("confidence_evolution"):
            confidences.extend(rules_analysis["confidence_evolution"])
        
        synthesis["average_confidence"] = sum(confidences) / len(confidences) if confidences else 0
        
        # Extract key findings
        synthesis["key_findings"] = [
            f"OP Manual analysis completed {op_analysis['rounds_completed']} rounds with avg confidence {op_analysis['final_insights']['average_confidence']:.1f}/10",
            f"Historical patterns analysis completed {pattern_analysis['rounds_completed']} rounds with avg confidence {pattern_analysis['final_insights']['average_confidence']:.1f}/10",
            f"Reconciliation rules analysis completed {rules_analysis['rounds_completed']} rounds with avg confidence {rules_analysis['final_insights']['average_confidence']:.1f}/10"
        ]
        
        # Generate strategic insights
        synthesis["strategic_insights"] = [
            "Deep thinking analysis provides comprehensive insights into reconciliation processes",
            "Pattern recognition is crucial for improving reconciliation accuracy",
            "Rule effectiveness varies across different scenarios and needs continuous monitoring",
            "Historical patterns provide valuable learning opportunities for process improvement"
        ]
        
        # Generate comprehensive recommendations
        synthesis["comprehensive_recommendations"] = [
            "Implement deep thinking analysis as a standard practice for reconciliation processes",
            "Use pattern recognition insights to improve matching accuracy",
            "Apply rule effectiveness insights to optimize reconciliation rules",
            "Establish continuous learning feedback loops based on historical patterns",
            "Create automated systems that incorporate deep thinking insights"
        ]
        
        return synthesis
    
    def _generate_training_recommendations(self, synthesis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate comprehensive recommendations based on training analysis."""
        recommendations = [
            {
                "category": "Process Improvement",
                "priority": "High",
                "recommendation": "Implement 10-round deep thinking analysis for all training document reviews",
                "rationale": "Deep thinking analysis provides comprehensive insights and improves understanding of reconciliation processes"
            },
            {
                "category": "Pattern Recognition",
                "priority": "High",
                "recommendation": "Use pattern recognition insights to improve matching accuracy and reduce discrepancies",
                "rationale": "Pattern recognition helps identify successful reconciliation strategies and common failure modes"
            },
            {
                "category": "Rule Optimization",
                "priority": "Medium",
                "recommendation": "Continuously optimize reconciliation rules based on effectiveness analysis",
                "rationale": "Rule effectiveness varies across scenarios and needs regular review and optimization"
            },
            {
                "category": "Learning Integration",
                "priority": "Medium",
                "recommendation": "Integrate historical pattern insights into reconciliation processes",
                "rationale": "Historical patterns provide valuable learning opportunities for process improvement"
            },
            {
                "category": "Automation",
                "priority": "High",
                "recommendation": "Create automated systems that incorporate deep thinking insights",
                "rationale": "Automation ensures consistent application of insights and improves efficiency"
            }
        ]
        
        return recommendations
    
    def get_training_insights_summary(self) -> Dict[str, Any]:
        """Get summary of training insights generated."""
        return {
            "total_analysis_rounds": self.analysis_rounds,
            "insights_generated": len(self.deep_insights),
            "pattern_library_size": len(self.pattern_library),
            "rule_effectiveness_analyzed": len(self.rule_effectiveness),
            "last_analysis": datetime.now().isoformat()
        }


# Example usage
if __name__ == "__main__":
    # Initialize training document analyzer
    config = {
        "log_level": "INFO",
        "max_execution_time": 1800,  # 30 minutes for deep analysis
        "retry_attempts": 3
    }
    
    analyzer = TrainingDocumentAnalyzer(
        config=config,
        training_data_path="training_data"
    )
    
    # Execute deep training document analysis
    input_data = {
        "analysis_type": "comprehensive",
        "include_op_manual": True,
        "include_historical_patterns": True,
        "include_reconciliation_rules": True
    }
    
    result = analyzer.execute_with_monitoring(input_data)
    print(f"Training document analysis completed: {json.dumps(result, indent=2)}")
    
    # Get insights summary
    summary = analyzer.get_training_insights_summary()
    print(f"Insights summary: {json.dumps(summary, indent=2)}")
