#!/usr/bin/env python3
"""
Predictive Timing Difference Engine
Implements historical pattern analysis and month-end timing prediction
Based on AI thinking insights for intelligent timing difference detection
"""

import json
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict
import re

class PredictiveTimingEngine:
    def __init__(self):
        self.name = "PredictiveTimingEngine"
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Timing difference patterns from AI insights
        self.expected_timing_differences = {
            "74505": {
                "description": "ATM settlement activity posted to GL on last day of month",
                "pattern": "month_end",
                "confidence": 0.9,
                "expected_amount_range": (100, 1000)
            },
            "74510": {
                "description": "Shared Branching activity recorded in GL on last day of month",
                "pattern": "month_end",
                "confidence": 0.85,
                "expected_amount_range": (500, 2000)
            },
            "74560": {
                "description": "Check deposit activity at branches posted to GL on last day of month",
                "pattern": "month_end",
                "confidence": 0.8,
                "expected_amount_range": (1000, 5000)
            },
            "74535": {
                "description": "Gift Card activity posted to GL on last day of month",
                "pattern": "month_end",
                "confidence": 0.75,
                "expected_amount_range": (50, 500)
            },
            "74550": {
                "description": "CBS activity posted to GL on last day of month",
                "pattern": "month_end",
                "confidence": 0.8,
                "expected_amount_range": (200, 1000)
            },
            "74540": {
                "description": "CRIF indirect loan activity posted to GL on last day of month",
                "pattern": "month_end",
                "confidence": 0.7,
                "expected_amount_range": (100, 800)
            }
        }
        
        # Historical data for pattern analysis
        self.historical_patterns = defaultdict(list)
        self.timing_predictions = []
        self.accuracy_metrics = {
            "total_predictions": 0,
            "accurate_predictions": 0,
            "false_positives": 0,
            "false_negatives": 0
        }
        
    def predict_timing_differences(self, gl_transactions, bank_transactions, current_date=None):
        """Predict timing differences based on historical patterns"""
        print("🔮 PREDICTIVE TIMING DIFFERENCE ANALYSIS")
        print("-" * 45)
        
        if not current_date:
            current_date = datetime.now()
        
        predictions = []
        
        # Analyze each GL account for timing differences
        for gl_account, timing_rule in self.expected_timing_differences.items():
            print(f"🔍 Analyzing GL {gl_account}: {timing_rule['description']}")
            
            # Find GL transactions for this account
            gl_txs = [tx for tx in gl_transactions if tx.get('gl_account') == gl_account]
            
            # Find potential timing differences
            timing_diffs = self._analyze_account_timing_differences(
                gl_account, gl_txs, bank_transactions, timing_rule, current_date
            )
            
            predictions.extend(timing_diffs)
        
        # Store predictions for learning
        self.timing_predictions.extend(predictions)
        
        print(f"✅ Generated {len(predictions)} timing difference predictions")
        return predictions
    
    def _analyze_account_timing_differences(self, gl_account, gl_transactions, bank_transactions, timing_rule, current_date):
        """Analyze timing differences for a specific GL account"""
        timing_diffs = []
        
        for gl_tx in gl_transactions:
            # Check if this is a month-end transaction
            if self._is_month_end_transaction(gl_tx, current_date):
                # Look for corresponding bank transaction
                bank_match = self._find_bank_match(gl_tx, bank_transactions)
                
                if not bank_match:
                    # This is likely a timing difference
                    timing_diff = {
                        'gl_account': gl_account,
                        'gl_transaction': gl_tx,
                        'bank_transaction': None,
                        'type': 'predicted_timing_difference',
                        'confidence': timing_rule['confidence'],
                        'reason': timing_rule['description'],
                        'predicted_bank_appearance': self._predict_bank_appearance_date(gl_tx, current_date),
                        'amount': gl_tx.get('amount', 0),
                        'status': 'expected',
                        'ai_insight': f"AI predicts timing difference for {timing_rule['description']}"
                    }
                    timing_diffs.append(timing_diff)
                else:
                    # Check if amounts match (might be partial timing difference)
                    amount_diff = abs(gl_tx.get('amount', 0) - bank_match.get('amount', 0))
                    if amount_diff > 0.01:
                        timing_diff = {
                            'gl_account': gl_account,
                            'gl_transaction': gl_tx,
                            'bank_transaction': bank_match,
                            'type': 'partial_timing_difference',
                            'confidence': timing_rule['confidence'] * 0.8,
                            'reason': f"Partial timing difference - amount mismatch: ${amount_diff:.2f}",
                            'amount_difference': amount_diff,
                            'status': 'partial',
                            'ai_insight': "AI detected partial timing difference"
                        }
                        timing_diffs.append(timing_diff)
        
        return timing_diffs
    
    def _is_month_end_transaction(self, transaction, current_date):
        """Check if transaction is a month-end timing difference"""
        tx_date = transaction.get('date', '')
        if not tx_date:
            return False
        
        try:
            # Parse date (simplified)
            if isinstance(tx_date, str):
                tx_date = datetime.strptime(tx_date, '%Y-%m-%d')
            
            # Check if it's within last 2 days of month
            month_end = current_date.replace(day=1) + timedelta(days=32)
            month_end = month_end.replace(day=1) - timedelta(days=1)
            
            return tx_date >= month_end - timedelta(days=1)
        except:
            return False
    
    def _find_bank_match(self, gl_transaction, bank_transactions):
        """Find matching bank transaction"""
        gl_amount = gl_transaction.get('amount', 0)
        gl_desc = gl_transaction.get('description', '').upper()
        
        for bank_tx in bank_transactions:
            bank_amount = bank_tx.get('amount', 0)
            bank_desc = bank_tx.get('description', '').upper()
            
            # Check amount match
            if abs(gl_amount - bank_amount) < 0.01:
                # Check description similarity
                similarity = self._calculate_description_similarity(gl_desc, bank_desc)
                if similarity > 0.7:
                    return bank_tx
        
        return None
    
    def _predict_bank_appearance_date(self, gl_transaction, current_date):
        """Predict when the bank transaction will appear"""
        # Based on AI insights, most timing differences appear within 1-3 business days
        predicted_days = np.random.randint(1, 4)  # 1-3 days
        return current_date + timedelta(days=predicted_days)
    
    def _calculate_description_similarity(self, desc1, desc2):
        """Calculate similarity between descriptions"""
        if not desc1 or not desc2:
            return 0.0
        
        # Simple word-based similarity
        words1 = set(desc1.split())
        words2 = set(desc2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def analyze_historical_patterns(self, historical_data):
        """Analyze historical timing patterns for learning"""
        print("📊 ANALYZING HISTORICAL TIMING PATTERNS")
        print("-" * 40)
        
        patterns = defaultdict(list)
        
        for data_point in historical_data:
            gl_account = data_point.get('gl_account')
            timing_diff = data_point.get('timing_difference', False)
            amount = data_point.get('amount', 0)
            date = data_point.get('date')
            
            if gl_account and timing_diff:
                patterns[gl_account].append({
                    'amount': amount,
                    'date': date,
                    'timing_difference': True
                })
        
        # Update expected patterns based on historical data
        for gl_account, historical_txs in patterns.items():
            if historical_txs:
                amounts = [tx['amount'] for tx in historical_txs]
                avg_amount = np.mean(amounts)
                std_amount = np.std(amounts)
                
                # Update expected amount range
                if gl_account in self.expected_timing_differences:
                    self.expected_timing_differences[gl_account]['expected_amount_range'] = (
                        max(0, avg_amount - 2 * std_amount),
                        avg_amount + 2 * std_amount
                    )
                
                print(f"   📈 GL {gl_account}: Avg amount ${avg_amount:.2f}, Std ${std_amount:.2f}")
        
        print(f"✅ Analyzed {len(historical_data)} historical data points")
        return patterns
    
    def validate_predictions(self, actual_timing_differences):
        """Validate predictions against actual timing differences"""
        print("✅ VALIDATING TIMING DIFFERENCE PREDICTIONS")
        print("-" * 45)
        
        correct_predictions = 0
        false_positives = 0
        false_negatives = 0
        
        # Check each prediction
        for prediction in self.timing_predictions:
            gl_account = prediction['gl_account']
            predicted_amount = prediction['amount']
            
            # Find matching actual timing difference
            actual_match = None
            for actual in actual_timing_differences:
                if (actual.get('gl_account') == gl_account and 
                    abs(actual.get('amount', 0) - predicted_amount) < 0.01):
                    actual_match = actual
                    break
            
            if actual_match:
                correct_predictions += 1
                print(f"   ✅ Correct prediction: GL {gl_account} - ${predicted_amount:.2f}")
            else:
                false_positives += 1
                print(f"   ❌ False positive: GL {gl_account} - ${predicted_amount:.2f}")
        
        # Check for missed timing differences (false negatives)
        for actual in actual_timing_differences:
            gl_account = actual.get('gl_account')
            actual_amount = actual.get('amount', 0)
            
            predicted_match = None
            for prediction in self.timing_predictions:
                if (prediction['gl_account'] == gl_account and 
                    abs(prediction['amount'] - actual_amount) < 0.01):
                    predicted_match = prediction
                    break
            
            if not predicted_match:
                false_negatives += 1
                print(f"   ⚠️ Missed prediction: GL {gl_account} - ${actual_amount:.2f}")
        
        # Update accuracy metrics
        total_predictions = len(self.timing_predictions)
        self.accuracy_metrics = {
            "total_predictions": total_predictions,
            "accurate_predictions": correct_predictions,
            "false_positives": false_positives,
            "false_negatives": false_negatives
        }
        
        accuracy = correct_predictions / max(total_predictions, 1)
        print(f"\n📊 PREDICTION ACCURACY: {accuracy:.2%}")
        print(f"   ✅ Correct: {correct_predictions}")
        print(f"   ❌ False Positives: {false_positives}")
        print(f"   ⚠️ False Negatives: {false_negatives}")
        
        return self.accuracy_metrics
    
    def get_timing_insights(self):
        """Get insights about timing differences"""
        insights = {
            "total_predictions": len(self.timing_predictions),
            "accuracy_metrics": self.accuracy_metrics,
            "expected_timing_differences": self.expected_timing_differences,
            "historical_patterns": dict(self.historical_patterns)
        }
        
        return insights
    
    def save_timing_analysis(self):
        """Save timing analysis results"""
        analysis_data = {
            'timestamp': self.timestamp,
            'predictions': self.timing_predictions,
            'accuracy_metrics': self.accuracy_metrics,
            'expected_timing_differences': self.expected_timing_differences,
            'insights': self.get_timing_insights()
        }
        
        filename = f"predictive_timing_analysis_{self.timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(analysis_data, f, indent=2, default=str)
        
        print(f"✅ Timing analysis saved: {filename}")
        return filename

def main():
    """Test the predictive timing engine"""
    print("🔮 PREDICTIVE TIMING DIFFERENCE ENGINE")
    print("=" * 45)
    print("🎯 Testing timing difference prediction")
    print("=" * 45)
    
    # Initialize engine
    engine = PredictiveTimingEngine()
    
    # Sample GL transactions
    gl_transactions = [
        {
            'gl_account': '74505',
            'description': 'ATM Settlement',
            'amount': 162.00,
            'date': '2025-05-31',
            'type': 'debit'
        },
        {
            'gl_account': '74510',
            'description': 'EFUNDS Corp Daily Settlement',
            'amount': 600.00,
            'date': '2025-05-31',
            'type': 'credit'
        },
        {
            'gl_account': '74560',
            'description': 'Check Deposits',
            'amount': 13709.62,
            'date': '2025-05-31',
            'type': 'credit'
        }
    ]
    
    # Sample bank transactions
    bank_transactions = [
        {
            'description': 'ACH ADV FILE - Rcvd DB',
            'amount': 1000.00,
            'date': '2025-05-30',
            'type': 'debit'
        },
        {
            'description': 'CNS Settlement',
            'amount': 500.00,
            'date': '2025-05-30',
            'type': 'credit'
        }
    ]
    
    # Test timing difference prediction
    predictions = engine.predict_timing_differences(gl_transactions, bank_transactions)
    
    print(f"\n📊 TIMING DIFFERENCE PREDICTIONS:")
    for i, prediction in enumerate(predictions, 1):
        print(f"\n{i}. GL {prediction['gl_account']} - ${prediction['amount']:.2f}")
        print(f"   Type: {prediction['type']}")
        print(f"   Confidence: {prediction['confidence']:.2f}")
        print(f"   Reason: {prediction['reason']}")
        print(f"   AI Insight: {prediction['ai_insight']}")
    
    # Test historical pattern analysis
    historical_data = [
        {'gl_account': '74505', 'amount': 150.00, 'timing_difference': True, 'date': '2025-04-30'},
        {'gl_account': '74505', 'amount': 175.00, 'timing_difference': True, 'date': '2025-03-31'},
        {'gl_account': '74510', 'amount': 550.00, 'timing_difference': True, 'date': '2025-04-30'}
    ]
    
    engine.analyze_historical_patterns(historical_data)
    
    # Get insights
    insights = engine.get_timing_insights()
    print(f"\n📈 TIMING INSIGHTS:")
    print(f"Total predictions: {insights['total_predictions']}")
    print(f"Expected timing differences: {len(insights['expected_timing_differences'])}")
    
    # Save analysis
    engine.save_timing_analysis()

if __name__ == "__main__":
    main()
