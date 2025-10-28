#!/usr/bin/env python3
"""
Training Data Manager
Manages training data for all agents following Strands Agent best practices
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import pandas as pd
import openpyxl

class TrainingDataManager:
    """
    Manages training data for all agents in the Excel Agent system.
    
    This class provides:
    - Centralized training data management
    - Data validation and quality assurance
    - Version control for training data
    - Integration with all agents
    - Continuous learning support
    """
    
    def __init__(self, training_data_path: str = "training_data"):
        """
        Initialize the training data manager.
        
        Args:
            training_data_path: Path to training data directory
        """
        self.training_data_path = Path(training_data_path)
        self.training_data_path.mkdir(exist_ok=True)
        
        # Setup logging
        self.logger = logging.getLogger("training_data_manager")
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        # Initialize training data structure
        self.training_data = {}
        self.data_versions = {}
        self.quality_metrics = {}
        
        # Load existing training data
        self._load_all_training_data()
    
    def _load_all_training_data(self):
        """Load all existing training data from files."""
        self.logger.info("Loading all training data...")
        
        # Load OP manual
        self._load_op_manual()
        
        # Load historical patterns
        self._load_historical_patterns()
        
        # Load reconciliation rules
        self._load_reconciliation_rules()
        
        # Load visual training data
        self._load_visual_training_data()
        
        # Load learning history
        self._load_learning_history()
        
        self.logger.info(f"Loaded {len(self.training_data)} training data types")
    
    def _load_op_manual(self):
        """Load OP manual training data."""
        op_manual_path = self.training_data_path / "op_manual.json"
        
        if op_manual_path.exists():
            try:
                with open(op_manual_path, 'r') as f:
                    self.training_data["op_manual"] = json.load(f)
                self.logger.info("Loaded OP manual training data")
            except Exception as e:
                self.logger.error(f"Error loading OP manual: {str(e)}")
                self.training_data["op_manual"] = self._get_default_op_manual()
        else:
            self.training_data["op_manual"] = self._get_default_op_manual()
            self._save_op_manual()
    
    def _load_historical_patterns(self):
        """Load historical patterns training data."""
        patterns_path = self.training_data_path / "historical_patterns.json"
        
        if patterns_path.exists():
            try:
                with open(patterns_path, 'r') as f:
                    self.training_data["historical_patterns"] = json.load(f)
                self.logger.info("Loaded historical patterns training data")
            except Exception as e:
                self.logger.error(f"Error loading historical patterns: {str(e)}")
                self.training_data["historical_patterns"] = self._get_default_historical_patterns()
        else:
            self.training_data["historical_patterns"] = self._get_default_historical_patterns()
            self._save_historical_patterns()
    
    def _load_reconciliation_rules(self):
        """Load reconciliation rules training data."""
        rules_path = self.training_data_path / "reconciliation_rules.json"
        
        if rules_path.exists():
            try:
                with open(rules_path, 'r') as f:
                    self.training_data["reconciliation_rules"] = json.load(f)
                self.logger.info("Loaded reconciliation rules training data")
            except Exception as e:
                self.logger.error(f"Error loading reconciliation rules: {str(e)}")
                self.training_data["reconciliation_rules"] = self._get_default_reconciliation_rules()
        else:
            self.training_data["reconciliation_rules"] = self._get_default_reconciliation_rules()
            self._save_reconciliation_rules()
    
    def _load_visual_training_data(self):
        """Load visual training data."""
        visual_path = self.training_data_path / "visual_training_data.json"
        
        if visual_path.exists():
            try:
                with open(visual_path, 'r') as f:
                    self.training_data["visual_training_data"] = json.load(f)
                self.logger.info("Loaded visual training data")
            except Exception as e:
                self.logger.error(f"Error loading visual training data: {str(e)}")
                self.training_data["visual_training_data"] = self._get_default_visual_training_data()
        else:
            self.training_data["visual_training_data"] = self._get_default_visual_training_data()
            self._save_visual_training_data()
    
    def _load_learning_history(self):
        """Load learning history."""
        history_path = self.training_data_path / "learning_history.json"
        
        if history_path.exists():
            try:
                with open(history_path, 'r') as f:
                    self.training_data["learning_history"] = json.load(f)
                self.logger.info("Loaded learning history")
            except Exception as e:
                self.logger.error(f"Error loading learning history: {str(e)}")
                self.training_data["learning_history"] = []
        else:
            self.training_data["learning_history"] = []
            self._save_learning_history()
    
    def _get_default_op_manual(self) -> Dict[str, Any]:
        """Get default OP manual data."""
        return {
            "gl_accounts": {
                "74400": {
                    "name": "RBC Activity",
                    "bank_activities": ["RBC activity", "EFUNDS Corp – FEE SETTLE", "Withdrawal Coin or Withdrawal Currency"],
                    "expected_timing": "daily",
                    "variance_threshold": 1000.0,
                    "description": "RBC banking activity and fee settlements",
                    "matching_keywords": ["RBC", "EFUNDS", "FEE SETTLE", "Withdrawal"]
                },
                "74505": {
                    "name": "CNS Settlement",
                    "bank_activities": ["CNS Settlement activity", "PULSE FEES activity"],
                    "expected_timing": "daily",
                    "variance_threshold": 500.0,
                    "description": "CNS settlement and pulse fee activities",
                    "matching_keywords": ["CNS", "Settlement", "PULSE", "FEES"]
                },
                "74510": {
                    "name": "EFUNDS Corp Daily Settlement",
                    "bank_activities": ["EFUNDS Corp – DLY SETTLE activity"],
                    "expected_timing": "daily",
                    "variance_threshold": 2000.0,
                    "description": "EFUNDS daily settlement activities",
                    "matching_keywords": ["EFUNDS", "DLY SETTLE", "Daily Settlement"]
                },
                "74515": {
                    "name": "Cash Letter Corrections",
                    "bank_activities": ["Cash Letter Corr activity"],
                    "expected_timing": "as_needed",
                    "variance_threshold": 100.0,
                    "description": "Cash letter correction activities",
                    "matching_keywords": ["Cash Letter", "Corr", "Correction"]
                },
                "74520": {
                    "name": "Image Check Presentment",
                    "bank_activities": ["1591 Image CL Presentment activity"],
                    "expected_timing": "daily",
                    "variance_threshold": 5000.0,
                    "description": "Image check presentment activities",
                    "matching_keywords": ["1591", "Image", "CL Presentment", "Check"]
                },
                "74525": {
                    "name": "Returned Drafts",
                    "bank_activities": ["1590 Image CL Presentment activity (returns)"],
                    "expected_timing": "daily",
                    "variance_threshold": 1000.0,
                    "description": "Returned draft activities",
                    "matching_keywords": ["1590", "Image", "CL Presentment", "returns", "Returned"]
                },
                "74530": {
                    "name": "ACH Activity",
                    "bank_activities": ["ACH ADV File activity"],
                    "expected_timing": "daily",
                    "variance_threshold": 10000.0,
                    "description": "ACH advance file activities",
                    "matching_keywords": ["ACH", "ADV File", "Advance"]
                },
                "74535": {
                    "name": "ICUL Services",
                    "bank_activities": ["ICUL ServCorp activity"],
                    "expected_timing": "monthly",
                    "variance_threshold": 500.0,
                    "description": "ICUL service corporation activities",
                    "matching_keywords": ["ICUL", "ServCorp", "Service"]
                },
                "74540": {
                    "name": "CRIF Loans",
                    "bank_activities": ["ACH ADV FILE - Orig CR activity (CRIF loans)"],
                    "expected_timing": "daily",
                    "variance_threshold": 2000.0,
                    "description": "CRIF loan origination activities",
                    "matching_keywords": ["ACH", "ADV FILE", "Orig CR", "CRIF", "loans"]
                },
                "74550": {
                    "name": "Cooperative Business",
                    "bank_activities": ["Cooperative Business activity"],
                    "expected_timing": "monthly",
                    "variance_threshold": 1000.0,
                    "description": "Cooperative business activities",
                    "matching_keywords": ["Cooperative", "Business"]
                },
                "74560": {
                    "name": "Check Deposits",
                    "bank_activities": ["1590 Image CL Presentment activity (deposits)"],
                    "expected_timing": "daily",
                    "variance_threshold": 5000.0,
                    "description": "Check deposit activities",
                    "matching_keywords": ["1590", "Image", "CL Presentment", "deposits", "Check"]
                },
                "74570": {
                    "name": "ACH Returns",
                    "bank_activities": ["ACH ADV FILE - Orig DB activity (ACH returns)"],
                    "expected_timing": "daily",
                    "variance_threshold": 2000.0,
                    "description": "ACH return activities",
                    "matching_keywords": ["ACH", "ADV FILE", "Orig DB", "returns", "ACH returns"]
                }
            },
            "timing_differences": {
                "74505": {
                    "description": "ATM settlement activity posted to GL on last day of month",
                    "expected": True,
                    "variance_threshold": 1000.0,
                    "timing_window_days": 3
                },
                "74510": {
                    "description": "Shared Branching activity recorded in GL on last day of month",
                    "expected": True,
                    "variance_threshold": 2000.0,
                    "timing_window_days": 3
                },
                "74560": {
                    "description": "Check deposit activity at branches posted to GL on last day of month",
                    "expected": True,
                    "variance_threshold": 5000.0,
                    "timing_window_days": 3
                },
                "74535": {
                    "description": "Gift Card activity posted to GL on last day of month",
                    "expected": True,
                    "variance_threshold": 500.0,
                    "timing_window_days": 3
                },
                "74550": {
                    "description": "CBS activity posted to GL on last day of month",
                    "expected": True,
                    "variance_threshold": 1000.0,
                    "timing_window_days": 3
                },
                "74540": {
                    "description": "CRIF indirect loan activity posted to GL on last day of month",
                    "expected": True,
                    "variance_threshold": 2000.0,
                    "timing_window_days": 3
                }
            },
            "validation_rules": {
                "amount_tolerance": 0.01,
                "date_tolerance_days": 3,
                "description_similarity_threshold": 0.8,
                "min_transaction_amount": 0.01,
                "max_transaction_amount": 1000000.0
            }
        }
    
    def _get_default_historical_patterns(self) -> Dict[str, Any]:
        """Get default historical patterns."""
        return {
            "common_discrepancies": [
                {
                    "pattern": "timing_difference",
                    "description": "Activity posted on different days",
                    "frequency": 0.15,
                    "resolution": "Accept if within 3 days",
                    "severity": "low"
                },
                {
                    "pattern": "rounding_difference",
                    "description": "Small rounding differences in amounts",
                    "frequency": 0.08,
                    "resolution": "Accept if less than $0.01",
                    "severity": "low"
                },
                {
                    "pattern": "duplicate_entry",
                    "description": "Same transaction posted twice",
                    "frequency": 0.05,
                    "resolution": "Remove duplicate entry",
                    "severity": "medium"
                },
                {
                    "pattern": "missing_entry",
                    "description": "Transaction missing from one side",
                    "frequency": 0.03,
                    "resolution": "Investigate and add missing entry",
                    "severity": "high"
                }
            ],
            "success_patterns": [
                {
                    "pattern": "exact_match",
                    "description": "Perfect match between GL and bank data",
                    "frequency": 0.70,
                    "confidence": 1.0
                },
                {
                    "pattern": "timing_match",
                    "description": "Match with timing difference",
                    "frequency": 0.20,
                    "confidence": 0.95
                },
                {
                    "pattern": "partial_match",
                    "description": "Partial match with some variance",
                    "frequency": 0.08,
                    "confidence": 0.80
                }
            ],
            "learning_insights": {
                "avg_success_rate": 0.75,
                "avg_variance_percentage": 5.2,
                "most_common_issues": ["timing_difference", "rounding_difference"],
                "improvement_areas": ["pattern_matching", "variance_threshold_tuning"]
            }
        }
    
    def _get_default_reconciliation_rules(self) -> Dict[str, Any]:
        """Get default reconciliation rules."""
        return {
            "matching_criteria": {
                "amount_tolerance": 0.01,
                "date_tolerance_days": 3,
                "description_similarity_threshold": 0.8,
                "account_number_matching": True,
                "reference_number_matching": True
            },
            "validation_rules": {
                "min_transaction_amount": 0.01,
                "max_transaction_amount": 1000000.0,
                "required_fields": ["date", "amount", "description"],
                "date_format_validation": True,
                "amount_format_validation": True
            },
            "reporting_rules": {
                "include_timing_differences": True,
                "include_variance_analysis": True,
                "include_pattern_analysis": True,
                "include_learning_insights": True,
                "include_recommendations": True
            },
            "quality_thresholds": {
                "min_success_rate": 0.80,
                "max_variance_percentage": 10.0,
                "max_unmatched_percentage": 5.0
            }
        }
    
    def _get_default_visual_training_data(self) -> Dict[str, Any]:
        """Get default visual training data."""
        return {
            "image_patterns": {
                "reconciliation_sheets": {
                    "description": "Patterns for identifying reconciliation sheets",
                    "keywords": ["Reconciliation", "Final", "Summary", "Balance"],
                    "layout_indicators": ["GL Account", "Debits", "Credits", "Net Balance"]
                },
                "bank_statements": {
                    "description": "Patterns for identifying bank statements",
                    "keywords": ["Bank", "Statement", "Activity", "Transaction"],
                    "layout_indicators": ["Date", "Description", "Amount", "Balance"]
                }
            },
            "visual_rules": {
                "sheet_identification": {
                    "reconciliation_sheet_keywords": ["Reconciliation", "Final", "Summary"],
                    "bank_sheet_keywords": ["Bank", "Statement", "Activity"],
                    "gl_sheet_keywords": ["74400", "74505", "74510", "74520", "74530", "74540", "74550", "74560", "74570"]
                },
                "data_extraction": {
                    "amount_column_indicators": ["Amount", "Debit", "Credit", "Balance"],
                    "date_column_indicators": ["Date", "Transaction Date", "Posted Date"],
                    "description_column_indicators": ["Description", "Memo", "Reference", "Details"]
                }
            }
        }
    
    def _save_op_manual(self):
        """Save OP manual to file."""
        op_manual_path = self.training_data_path / "op_manual.json"
        with open(op_manual_path, 'w') as f:
            json.dump(self.training_data["op_manual"], f, indent=2)
    
    def _save_historical_patterns(self):
        """Save historical patterns to file."""
        patterns_path = self.training_data_path / "historical_patterns.json"
        with open(patterns_path, 'w') as f:
            json.dump(self.training_data["historical_patterns"], f, indent=2)
    
    def _save_reconciliation_rules(self):
        """Save reconciliation rules to file."""
        rules_path = self.training_data_path / "reconciliation_rules.json"
        with open(rules_path, 'w') as f:
            json.dump(self.training_data["reconciliation_rules"], f, indent=2)
    
    def _save_visual_training_data(self):
        """Save visual training data to file."""
        visual_path = self.training_data_path / "visual_training_data.json"
        with open(visual_path, 'w') as f:
            json.dump(self.training_data["visual_training_data"], f, indent=2)
    
    def _save_learning_history(self):
        """Save learning history to file."""
        history_path = self.training_data_path / "learning_history.json"
        with open(history_path, 'w') as f:
            json.dump(self.training_data["learning_history"], f, indent=2)
    
    def get_training_data(self, data_type: str) -> Optional[Dict[str, Any]]:
        """Get specific training data by type."""
        return self.training_data.get(data_type)
    
    def update_training_data(self, data_type: str, data: Dict[str, Any], version: str = None):
        """Update training data with version control."""
        if version is None:
            version = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self.training_data[data_type] = data
        self.data_versions[data_type] = version
        
        # Save to file
        if data_type == "op_manual":
            self._save_op_manual()
        elif data_type == "historical_patterns":
            self._save_historical_patterns()
        elif data_type == "reconciliation_rules":
            self._save_reconciliation_rules()
        elif data_type == "visual_training_data":
            self._save_visual_training_data()
        elif data_type == "learning_history":
            self._save_learning_history()
        
        self.logger.info(f"Updated training data for type: {data_type}, version: {version}")
    
    def add_learning_entry(self, entry: Dict[str, Any]):
        """Add a new learning entry to the history."""
        entry["timestamp"] = datetime.now().isoformat()
        entry["version"] = len(self.training_data["learning_history"]) + 1
        
        self.training_data["learning_history"].append(entry)
        
        # Keep only last 1000 entries
        if len(self.training_data["learning_history"]) > 1000:
            self.training_data["learning_history"] = self.training_data["learning_history"][-1000:]
        
        self._save_learning_history()
        self.logger.info("Added new learning entry")
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """Get learning insights from historical data."""
        if not self.training_data["learning_history"]:
            return {"message": "No learning history available"}
        
        recent_entries = self.training_data["learning_history"][-100:]  # Last 100 entries
        
        # Calculate metrics
        success_rates = [entry.get("success_rate", 0) for entry in recent_entries if "success_rate" in entry]
        variance_levels = [entry.get("variance_level", 0) for entry in recent_entries if "variance_level" in entry]
        
        avg_success_rate = sum(success_rates) / len(success_rates) if success_rates else 0
        avg_variance = sum(variance_levels) / len(variance_levels) if variance_levels else 0
        
        # Identify trends
        if len(success_rates) >= 10:
            recent_trend = sum(success_rates[-10:]) / 10
            older_trend = sum(success_rates[-20:-10]) / 10 if len(success_rates) >= 20 else recent_trend
            trend_direction = "improving" if recent_trend > older_trend else "declining" if recent_trend < older_trend else "stable"
        else:
            trend_direction = "insufficient_data"
        
        return {
            "total_learning_entries": len(self.training_data["learning_history"]),
            "recent_avg_success_rate": avg_success_rate,
            "recent_avg_variance": avg_variance,
            "learning_trend": trend_direction,
            "data_quality": "good" if avg_success_rate > 0.8 and avg_variance < 5 else "needs_improvement",
            "recommendations": self._generate_learning_recommendations(avg_success_rate, avg_variance)
        }
    
    def _generate_learning_recommendations(self, success_rate: float, avg_variance: float) -> List[str]:
        """Generate recommendations based on learning insights."""
        recommendations = []
        
        if success_rate < 0.6:
            recommendations.append("Consider retraining with more diverse data")
            recommendations.append("Review pattern matching algorithms")
        
        if avg_variance > 10:
            recommendations.append("Review variance thresholds and matching criteria")
            recommendations.append("Investigate data quality issues")
        
        if success_rate > 0.9 and avg_variance < 2:
            recommendations.append("Excellent performance - consider expanding to more complex scenarios")
        
        if success_rate < 0.8:
            recommendations.append("Implement additional validation rules")
        
        return recommendations
    
    def validate_training_data(self, data_type: str) -> Dict[str, Any]:
        """Validate training data quality."""
        validation_result = {
            "data_type": data_type,
            "is_valid": True,
            "issues": [],
            "quality_score": 0,
            "recommendations": []
        }
        
        data = self.training_data.get(data_type)
        if not data:
            validation_result["is_valid"] = False
            validation_result["issues"].append("Data not found")
            return validation_result
        
        # Type-specific validation
        if data_type == "op_manual":
            validation_result = self._validate_op_manual(data)
        elif data_type == "historical_patterns":
            validation_result = self._validate_historical_patterns(data)
        elif data_type == "reconciliation_rules":
            validation_result = self._validate_reconciliation_rules(data)
        
        return validation_result
    
    def _validate_op_manual(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate OP manual data."""
        validation_result = {
            "data_type": "op_manual",
            "is_valid": True,
            "issues": [],
            "quality_score": 0,
            "recommendations": []
        }
        
        required_sections = ["gl_accounts", "timing_differences", "validation_rules"]
        for section in required_sections:
            if section not in data:
                validation_result["issues"].append(f"Missing required section: {section}")
                validation_result["is_valid"] = False
        
        if "gl_accounts" in data:
            gl_accounts = data["gl_accounts"]
            if len(gl_accounts) < 10:
                validation_result["issues"].append("Insufficient GL accounts defined")
                validation_result["quality_score"] -= 20
        
        validation_result["quality_score"] = max(0, 100 - len(validation_result["issues"]) * 10)
        
        return validation_result
    
    def _validate_historical_patterns(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate historical patterns data."""
        validation_result = {
            "data_type": "historical_patterns",
            "is_valid": True,
            "issues": [],
            "quality_score": 0,
            "recommendations": []
        }
        
        required_sections = ["common_discrepancies", "success_patterns"]
        for section in required_sections:
            if section not in data:
                validation_result["issues"].append(f"Missing required section: {section}")
                validation_result["is_valid"] = False
        
        validation_result["quality_score"] = max(0, 100 - len(validation_result["issues"]) * 10)
        
        return validation_result
    
    def _validate_reconciliation_rules(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate reconciliation rules data."""
        validation_result = {
            "data_type": "reconciliation_rules",
            "is_valid": True,
            "issues": [],
            "quality_score": 0,
            "recommendations": []
        }
        
        required_sections = ["matching_criteria", "validation_rules", "reporting_rules"]
        for section in required_sections:
            if section not in data:
                validation_result["issues"].append(f"Missing required section: {section}")
                validation_result["is_valid"] = False
        
        validation_result["quality_score"] = max(0, 100 - len(validation_result["issues"]) * 10)
        
        return validation_result
    
    def export_training_data(self, output_path: str = None):
        """Export all training data to a single file."""
        if not output_path:
            output_path = f"training_data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "training_data": self.training_data,
            "data_versions": self.data_versions,
            "quality_metrics": self.quality_metrics
        }
        
        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        self.logger.info(f"Exported training data to {output_path}")
        return output_path
    
    def get_status(self) -> Dict[str, Any]:
        """Get training data manager status."""
        return {
            "training_data_path": str(self.training_data_path),
            "data_types_loaded": list(self.training_data.keys()),
            "total_learning_entries": len(self.training_data.get("learning_history", [])),
            "data_versions": self.data_versions,
            "last_updated": datetime.now().isoformat()
        }


# Example usage
if __name__ == "__main__":
    # Initialize training data manager
    manager = TrainingDataManager("training_data")
    
    # Get status
    status = manager.get_status()
    print(f"Training data manager status: {json.dumps(status, indent=2)}")
    
    # Get learning insights
    insights = manager.get_learning_insights()
    print(f"Learning insights: {json.dumps(insights, indent=2)}")
    
    # Export training data
    export_file = manager.export_training_data()
    print(f"Exported training data to: {export_file}")
