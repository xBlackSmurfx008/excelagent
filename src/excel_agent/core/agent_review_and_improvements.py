#!/usr/bin/env python3
"""
Agent Review and Improvements Script
Ensures all agents follow Strands Agent best practices and properly integrate training data
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import inspect

class AgentReviewer:
    """Reviews agents for Strands Agent best practices compliance"""
    
    def __init__(self):
        self.agent_files = [
            "ai_reconciliation_agent.py",
            "enhanced_thinking_agent.py", 
            "vision_enhanced_ai_agent.py",
            "data_consolidation_agent.py",
            "high_variance_investigator.py",
            "bank_cross_match_agent.py",
            "discrepancy_discovery_agent.py",
            "enhanced_ai_reconciliation_agent.py",
            "ai_thinking_agent.py"
        ]
        self.review_results = {}
        self.improvements_needed = []
        
    def review_all_agents(self):
        """Review all agents for best practices compliance"""
        print("🔍 REVIEWING ALL AGENTS FOR STRANDS AGENT BEST PRACTICES")
        print("=" * 70)
        
        for agent_file in self.agent_files:
            if os.path.exists(agent_file):
                print(f"\n📊 Reviewing {agent_file}...")
                review_result = self._review_agent_file(agent_file)
                self.review_results[agent_file] = review_result
            else:
                print(f"⚠️  {agent_file} not found, skipping...")
        
        self._generate_review_report()
        return self.review_results
    
    def _review_agent_file(self, agent_file: str) -> Dict[str, Any]:
        """Review a single agent file for best practices compliance"""
        review_result = {
            "file": agent_file,
            "timestamp": datetime.now().isoformat(),
            "compliance_score": 0,
            "issues": [],
            "recommendations": [],
            "training_data_integration": {},
            "best_practices": {}
        }
        
        try:
            with open(agent_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for Strands Agent best practices
            review_result["best_practices"] = self._check_best_practices(content, agent_file)
            
            # Check training data integration
            review_result["training_data_integration"] = self._check_training_data_integration(content, agent_file)
            
            # Calculate compliance score
            review_result["compliance_score"] = self._calculate_compliance_score(review_result)
            
            # Generate recommendations
            review_result["recommendations"] = self._generate_recommendations(review_result)
            
        except Exception as e:
            review_result["issues"].append(f"Error reading file: {str(e)}")
            review_result["compliance_score"] = 0
        
        return review_result
    
    def _check_best_practices(self, content: str, agent_file: str) -> Dict[str, Any]:
        """Check if agent follows Strands Agent best practices"""
        best_practices = {
            "model_driven": False,
            "error_handling": False,
            "logging": False,
            "type_hints": False,
            "docstrings": False,
            "configuration_management": False,
            "data_validation": False,
            "separation_of_concerns": False
        }
        
        # Check for model-driven development
        if "class" in content and "def __init__" in content:
            best_practices["model_driven"] = True
        
        # Check for error handling
        if "try:" in content and "except" in content:
            best_practices["error_handling"] = True
        
        # Check for logging
        if "import logging" in content or "print(" in content:
            best_practices["logging"] = True
        
        # Check for type hints
        if "->" in content and ":" in content:
            best_practices["type_hints"] = True
        
        # Check for docstrings
        if '"""' in content or "'''" in content:
            best_practices["docstrings"] = True
        
        # Check for configuration management
        if "config" in content.lower() or "environment" in content.lower():
            best_practices["configuration_management"] = True
        
        # Check for data validation
        if "validate" in content.lower() or "check" in content.lower():
            best_practices["data_validation"] = True
        
        # Check for separation of concerns
        if len(content.split("def ")) > 3:  # Multiple methods indicate separation
            best_practices["separation_of_concerns"] = True
        
        return best_practices
    
    def _check_training_data_integration(self, content: str, agent_file: str) -> Dict[str, Any]:
        """Check how well the agent integrates training data"""
        training_integration = {
            "op_manual_usage": False,
            "historical_data_usage": False,
            "pattern_recognition": False,
            "learning_capabilities": False,
            "data_validation": False,
            "fallback_mechanisms": False
        }
        
        # Check for OP manual usage
        if "op_manual" in content.lower() or "manual" in content.lower():
            training_integration["op_manual_usage"] = True
        
        # Check for historical data usage
        if "historical" in content.lower() or "previous" in content.lower():
            training_integration["historical_data_usage"] = True
        
        # Check for pattern recognition
        if "pattern" in content.lower() or "match" in content.lower():
            training_integration["pattern_recognition"] = True
        
        # Check for learning capabilities
        if "learn" in content.lower() or "training" in content.lower():
            training_integration["learning_capabilities"] = True
        
        # Check for data validation
        if "validate" in content.lower() or "check" in content.lower():
            training_integration["data_validation"] = True
        
        # Check for fallback mechanisms
        if "fallback" in content.lower() or "default" in content.lower():
            training_integration["fallback_mechanisms"] = True
        
        return training_integration
    
    def _calculate_compliance_score(self, review_result: Dict[str, Any]) -> int:
        """Calculate compliance score based on best practices"""
        best_practices = review_result["best_practices"]
        training_integration = review_result["training_data_integration"]
        
        # Weight different aspects
        best_practices_score = sum(best_practices.values()) / len(best_practices) * 50
        training_score = sum(training_integration.values()) / len(training_integration) * 50
        
        return int(best_practices_score + training_score)
    
    def _generate_recommendations(self, review_result: Dict[str, Any]) -> List[str]:
        """Generate recommendations for improving the agent"""
        recommendations = []
        best_practices = review_result["best_practices"]
        training_integration = review_result["training_data_integration"]
        
        # Best practices recommendations
        if not best_practices["model_driven"]:
            recommendations.append("Implement model-driven development with clear input-processing-output pattern")
        
        if not best_practices["error_handling"]:
            recommendations.append("Add comprehensive error handling with try-catch blocks")
        
        if not best_practices["logging"]:
            recommendations.append("Implement structured logging for better monitoring and debugging")
        
        if not best_practices["type_hints"]:
            recommendations.append("Add type hints to all methods for better code clarity")
        
        if not best_practices["docstrings"]:
            recommendations.append("Add comprehensive docstrings to all classes and methods")
        
        if not best_practices["configuration_management"]:
            recommendations.append("Implement configuration management for better flexibility")
        
        if not best_practices["data_validation"]:
            recommendations.append("Add input data validation at agent boundaries")
        
        # Training data integration recommendations
        if not training_integration["op_manual_usage"]:
            recommendations.append("Integrate OP manual data for reconciliation rules and patterns")
        
        if not training_integration["historical_data_usage"]:
            recommendations.append("Implement historical data usage for pattern learning")
        
        if not training_integration["pattern_recognition"]:
            recommendations.append("Add pattern recognition capabilities for better matching")
        
        if not training_integration["learning_capabilities"]:
            recommendations.append("Implement learning capabilities to improve over time")
        
        if not training_integration["data_validation"]:
            recommendations.append("Add training data validation and quality checks")
        
        if not training_integration["fallback_mechanisms"]:
            recommendations.append("Implement fallback mechanisms when training data is unavailable")
        
        return recommendations
    
    def _generate_review_report(self):
        """Generate comprehensive review report"""
        print("\n" + "=" * 70)
        print("📊 AGENT REVIEW SUMMARY")
        print("=" * 70)
        
        total_agents = len(self.review_results)
        avg_score = sum(result["compliance_score"] for result in self.review_results.values()) / total_agents if total_agents > 0 else 0
        
        print(f"Total Agents Reviewed: {total_agents}")
        print(f"Average Compliance Score: {avg_score:.1f}%")
        
        print("\n📋 AGENT COMPLIANCE SCORES:")
        for agent_file, result in self.review_results.items():
            score = result["compliance_score"]
            status = "✅ EXCELLENT" if score >= 80 else "⚠️  NEEDS IMPROVEMENT" if score >= 60 else "❌ POOR"
            print(f"  {agent_file}: {score}% {status}")
        
        print("\n🔧 TOP IMPROVEMENTS NEEDED:")
        all_recommendations = []
        for result in self.review_results.values():
            all_recommendations.extend(result["recommendations"])
        
        # Count most common recommendations
        recommendation_counts = {}
        for rec in all_recommendations:
            recommendation_counts[rec] = recommendation_counts.get(rec, 0) + 1
        
        # Sort by frequency
        sorted_recommendations = sorted(recommendation_counts.items(), key=lambda x: x[1], reverse=True)
        
        for i, (rec, count) in enumerate(sorted_recommendations[:5], 1):
            print(f"  {i}. {rec} (mentioned in {count} agents)")
        
        # Save detailed report
        self._save_detailed_report()
    
    def _save_detailed_report(self):
        """Save detailed review report to file"""
        report_data = {
            "review_timestamp": datetime.now().isoformat(),
            "total_agents": len(self.review_results),
            "average_compliance_score": sum(result["compliance_score"] for result in self.review_results.values()) / len(self.review_results) if self.review_results else 0,
            "agent_reviews": self.review_results,
            "strands_agent_best_practices": {
                "model_driven_development": "Each agent should follow a clear input-processing-output model",
                "error_handling": "Comprehensive error handling with try-catch blocks and graceful degradation",
                "logging": "Structured logging with appropriate levels for monitoring and debugging",
                "type_hints": "Type hints for all methods to improve code clarity and IDE support",
                "docstrings": "Comprehensive docstrings for all classes and methods",
                "configuration_management": "Environment-based configuration with parameter validation",
                "data_validation": "Input validation at agent boundaries with proper error handling",
                "separation_of_concerns": "Clear separation of responsibilities across different methods"
            },
            "training_data_integration_requirements": {
                "op_manual_usage": "Integration of OP manual data for reconciliation rules and patterns",
                "historical_data_usage": "Usage of historical data for pattern learning and improvement",
                "pattern_recognition": "Pattern recognition capabilities for better data matching",
                "learning_capabilities": "Learning capabilities to improve performance over time",
                "data_validation": "Training data validation and quality assurance",
                "fallback_mechanisms": "Fallback mechanisms when training data is unavailable"
            }
        }
        
        with open("agent_review_report.json", "w") as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: agent_review_report.json")

def main():
    """Main function to run agent review"""
    print("🚀 STARTING AGENT REVIEW FOR STRANDS AGENT BEST PRACTICES")
    print("=" * 70)
    
    reviewer = AgentReviewer()
    review_results = reviewer.review_all_agents()
    
    print("\n✅ Agent review completed!")
    print("📄 Review report saved to: agent_review_report.json")
    
    return review_results

if __name__ == "__main__":
    main()
