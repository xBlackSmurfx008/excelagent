#!/usr/bin/env python3
"""
Exception Handling Engine
Implements anomaly detection, escalation procedures, and intelligent exception management
Based on AI thinking insights for comprehensive exception handling
"""

import json
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict
import re

class ExceptionHandlingEngine:
    def __init__(self):
        self.name = "ExceptionHandlingEngine"
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Exception thresholds
        self.anomaly_threshold = 0.8  # 80% confidence for anomaly detection
        self.escalation_threshold = 0.9  # 90% confidence for escalation
        self.fraud_risk_threshold = 0.95  # 95% confidence for fraud risk
        
        # Exception categories
        self.exception_categories = {
            "anomaly": {
                "description": "Unusual transaction patterns",
                "severity": "medium",
                "escalation_level": 1
            },
            "discrepancy": {
                "description": "Balance or amount discrepancies",
                "severity": "high",
                "escalation_level": 2
            },
            "fraud_risk": {
                "description": "Potential fraudulent activity",
                "severity": "critical",
                "escalation_level": 3
            },
            "data_quality": {
                "description": "Data quality issues",
                "severity": "medium",
                "escalation_level": 1
            },
            "system_error": {
                "description": "System or processing errors",
                "severity": "high",
                "escalation_level": 2
            }
        }
        
        # Exception handling results
        self.exceptions_detected = []
        self.anomalies_found = []
        self.escalations_triggered = []
        self.fraud_risks_flagged = []
        self.resolution_actions = []
        
        # Performance metrics
        self.metrics = {
            "total_exceptions": 0,
            "anomalies_detected": 0,
            "discrepancies_found": 0,
            "fraud_risks_flagged": 0,
            "escalations_triggered": 0,
            "resolutions_completed": 0
        }
        
    def detect_exceptions(self, gl_data, bank_data, validation_results=None):
        """Comprehensive exception detection and handling"""
        print("🚨 EXCEPTION HANDLING ENGINE")
        print("=" * 40)
        print("🎯 Anomaly detection and intelligent exception management")
        print("=" * 40)
        
        exceptions = []
        
        # 1. Anomaly Detection
        anomalies = self._detect_anomalies(gl_data, bank_data)
        exceptions.extend(anomalies)
        
        # 2. Fraud Risk Detection
        fraud_risks = self._detect_fraud_risks(gl_data, bank_data)
        exceptions.extend(fraud_risks)
        
        # 3. Data Quality Exceptions
        quality_exceptions = self._detect_data_quality_exceptions(gl_data, bank_data)
        exceptions.extend(quality_exceptions)
        
        # 4. System Error Detection
        system_errors = self._detect_system_errors(gl_data, bank_data)
        exceptions.extend(system_errors)
        
        # 5. Process validation results if provided
        if validation_results:
            validation_exceptions = self._process_validation_exceptions(validation_results)
            exceptions.extend(validation_exceptions)
        
        # Store results
        self.exceptions_detected.extend(exceptions)
        
        # Update metrics
        self._update_metrics(exceptions)
        
        # Trigger escalations if needed
        self._trigger_escalations(exceptions)
        
        print(f"✅ Exception detection complete: {len(exceptions)} exceptions found")
        return exceptions
    
    def _detect_anomalies(self, gl_data, bank_data):
        """Detect unusual transaction patterns and anomalies"""
        print("🔍 Detecting anomalies...")
        
        anomalies = []
        
        # Check for unusual transaction amounts
        amount_anomalies = self._detect_amount_anomalies(gl_data, bank_data)
        anomalies.extend(amount_anomalies)
        
        # Check for unusual transaction frequencies
        frequency_anomalies = self._detect_frequency_anomalies(gl_data, bank_data)
        anomalies.extend(frequency_anomalies)
        
        # Check for unusual timing patterns
        timing_anomalies = self._detect_timing_anomalies(gl_data, bank_data)
        anomalies.extend(timing_anomalies)
        
        # Check for unusual description patterns
        description_anomalies = self._detect_description_anomalies(gl_data, bank_data)
        anomalies.extend(description_anomalies)
        
        print(f"   ✅ Anomaly detection complete: {len(anomalies)} anomalies found")
        return anomalies
    
    def _detect_amount_anomalies(self, gl_data, bank_data):
        """Detect unusual transaction amounts"""
        anomalies = []
        
        # Analyze GL amounts
        for gl_account, account_data in gl_data.items():
            transactions = account_data.get('transactions', [])
            amounts = [abs(tx.get('amount', 0.0)) for tx in transactions if tx.get('amount', 0.0) != 0]
            
            if amounts:
                mean_amount = np.mean(amounts)
                std_amount = np.std(amounts)
                
                for tx in transactions:
                    amount = abs(tx.get('amount', 0.0))
                    if amount > 0:
                        # Check for outliers (3 standard deviations)
                        if amount > mean_amount + 3 * std_amount:
                            anomaly = {
                                'type': 'amount_anomaly',
                                'category': 'anomaly',
                                'gl_account': gl_account,
                                'transaction': tx,
                                'amount': amount,
                                'mean_amount': mean_amount,
                                'std_amount': std_amount,
                                'severity': 'medium',
                                'confidence': min(0.95, (amount - mean_amount) / std_amount / 3),
                                'message': f'Unusually large amount: ${amount:,.2f} (mean: ${mean_amount:,.2f})',
                                'recommendation': 'Verify transaction amount and source'
                            }
                            anomalies.append(anomaly)
                            self.anomalies_found.append(anomaly)
        
        return anomalies
    
    def _detect_frequency_anomalies(self, gl_data, bank_data):
        """Detect unusual transaction frequencies"""
        anomalies = []
        
        # Analyze transaction frequencies by GL account
        for gl_account, account_data in gl_data.items():
            transactions = account_data.get('transactions', [])
            
            if len(transactions) > 0:
                # Group by date to find frequency patterns
                date_counts = defaultdict(int)
                for tx in transactions:
                    date = tx.get('date', '')
                    if date:
                        date_counts[date] += 1
                
                # Check for unusual frequency (more than 10 transactions in one day)
                for date, count in date_counts.items():
                    if count > 10:  # Threshold for unusual frequency
                        anomaly = {
                            'type': 'frequency_anomaly',
                            'category': 'anomaly',
                            'gl_account': gl_account,
                            'date': date,
                            'transaction_count': count,
                            'severity': 'medium',
                            'confidence': min(0.9, count / 20),  # Normalize to 0-1
                            'message': f'Unusual transaction frequency: {count} transactions on {date}',
                            'recommendation': 'Review transaction batch for accuracy'
                        }
                        anomalies.append(anomaly)
                        self.anomalies_found.append(anomaly)
        
        return anomalies
    
    def _detect_timing_anomalies(self, gl_data, bank_data):
        """Detect unusual timing patterns"""
        anomalies = []
        
        # Check for transactions outside business hours (simplified)
        for gl_account, account_data in gl_data.items():
            transactions = account_data.get('transactions', [])
            
            for tx in transactions:
                date = tx.get('date', '')
                # Check for weekend transactions (simplified check)
                if date and self._is_weekend_date(date):
                    anomaly = {
                        'type': 'timing_anomaly',
                        'category': 'anomaly',
                        'gl_account': gl_account,
                        'transaction': tx,
                        'date': date,
                        'severity': 'low',
                        'confidence': 0.6,
                        'message': f'Weekend transaction detected: {date}',
                        'recommendation': 'Verify transaction timing is correct'
                    }
                    anomalies.append(anomaly)
                    self.anomalies_found.append(anomaly)
        
        return anomalies
    
    def _detect_description_anomalies(self, gl_data, bank_data):
        """Detect unusual description patterns"""
        anomalies = []
        
        # Analyze description patterns
        all_descriptions = []
        for account_data in gl_data.values():
            transactions = account_data.get('transactions', [])
            for tx in transactions:
                desc = tx.get('description', '').strip()
                if desc:
                    all_descriptions.append(desc)
        
        # Find unusual descriptions (very short, very long, or with unusual characters)
        for gl_account, account_data in gl_data.items():
            transactions = account_data.get('transactions', [])
            
            for tx in transactions:
                desc = tx.get('description', '').strip()
                
                # Check for unusual description patterns
                if len(desc) < 3:  # Very short description
                    anomaly = {
                        'type': 'description_anomaly',
                        'category': 'anomaly',
                        'gl_account': gl_account,
                        'transaction': tx,
                        'description': desc,
                        'severity': 'medium',
                        'confidence': 0.8,
                        'message': f'Unusually short description: "{desc}"',
                        'recommendation': 'Verify description is complete and accurate'
                    }
                    anomalies.append(anomaly)
                    self.anomalies_found.append(anomaly)
                elif len(desc) > 100:  # Very long description
                    anomaly = {
                        'type': 'description_anomaly',
                        'category': 'anomaly',
                        'gl_account': gl_account,
                        'transaction': tx,
                        'description': desc,
                        'severity': 'low',
                        'confidence': 0.6,
                        'message': f'Unusually long description: {len(desc)} characters',
                        'recommendation': 'Verify description is accurate and necessary'
                    }
                    anomalies.append(anomaly)
                    self.anomalies_found.append(anomaly)
        
        return anomalies
    
    def _detect_fraud_risks(self, gl_data, bank_data):
        """Detect potential fraudulent activity"""
        print("🚨 Detecting fraud risks...")
        
        fraud_risks = []
        
        # Check for suspicious patterns
        suspicious_patterns = self._identify_suspicious_patterns(gl_data, bank_data)
        fraud_risks.extend(suspicious_patterns)
        
        # Check for unusual amounts
        unusual_amounts = self._identify_unusual_amounts(gl_data, bank_data)
        fraud_risks.extend(unusual_amounts)
        
        # Check for rapid transactions
        rapid_transactions = self._identify_rapid_transactions(gl_data, bank_data)
        fraud_risks.extend(rapid_transactions)
        
        print(f"   ✅ Fraud risk detection complete: {len(fraud_risks)} risks found")
        return fraud_risks
    
    def _identify_suspicious_patterns(self, gl_data, bank_data):
        """Identify suspicious transaction patterns"""
        suspicious = []
        
        # Check for round number transactions (potential test transactions)
        for gl_account, account_data in gl_data.items():
            transactions = account_data.get('transactions', [])
            
            for tx in transactions:
                amount = tx.get('amount', 0.0)
                
                # Check for suspicious round numbers
                if amount in [100.00, 1000.00, 10000.00, 100000.00]:
                    risk = {
                        'type': 'suspicious_pattern',
                        'category': 'fraud_risk',
                        'gl_account': gl_account,
                        'transaction': tx,
                        'amount': amount,
                        'severity': 'high',
                        'confidence': 0.7,
                        'message': f'Suspicious round number transaction: ${amount:,.2f}',
                        'recommendation': 'Investigate for potential fraud or test transactions'
                    }
                    suspicious.append(risk)
                    self.fraud_risks_flagged.append(risk)
        
        return suspicious
    
    def _identify_unusual_amounts(self, gl_data, bank_data):
        """Identify unusually large or small amounts"""
        unusual = []
        
        # Check for extremely large amounts
        for gl_account, account_data in gl_data.items():
            transactions = account_data.get('transactions', [])
            
            for tx in transactions:
                amount = abs(tx.get('amount', 0.0))
                
                if amount > 100000.00:  # $100K threshold
                    risk = {
                        'type': 'unusual_amount',
                        'category': 'fraud_risk',
                        'gl_account': gl_account,
                        'transaction': tx,
                        'amount': amount,
                        'severity': 'high',
                        'confidence': min(0.95, amount / 1000000),  # Scale confidence
                        'message': f'Unusually large amount: ${amount:,.2f}',
                        'recommendation': 'Verify transaction legitimacy and authorization'
                    }
                    unusual.append(risk)
                    self.fraud_risks_flagged.append(risk)
        
        return unusual
    
    def _identify_rapid_transactions(self, gl_data, bank_data):
        """Identify rapid successive transactions"""
        rapid = []
        
        # Check for multiple transactions within short time periods
        for gl_account, account_data in gl_data.items():
            transactions = account_data.get('transactions', [])
            
            # Sort by date and check for rapid succession
            sorted_transactions = sorted(transactions, key=lambda x: x.get('date', ''))
            
            for i in range(len(sorted_transactions) - 1):
                tx1 = sorted_transactions[i]
                tx2 = sorted_transactions[i + 1]
                
                # Check if transactions are on the same date (rapid succession)
                if tx1.get('date') == tx2.get('date'):
                    risk = {
                        'type': 'rapid_transactions',
                        'category': 'fraud_risk',
                        'gl_account': gl_account,
                        'transactions': [tx1, tx2],
                        'date': tx1.get('date'),
                        'severity': 'medium',
                        'confidence': 0.6,
                        'message': f'Rapid successive transactions on {tx1.get("date")}',
                        'recommendation': 'Review for potential duplicate or fraudulent activity'
                    }
                    rapid.append(risk)
                    self.fraud_risks_flagged.append(risk)
        
        return rapid
    
    def _detect_data_quality_exceptions(self, gl_data, bank_data):
        """Detect data quality issues"""
        print("📊 Detecting data quality exceptions...")
        
        quality_exceptions = []
        
        # Check for missing required fields
        missing_fields = self._check_missing_fields(gl_data, bank_data)
        quality_exceptions.extend(missing_fields)
        
        # Check for invalid data formats
        invalid_formats = self._check_invalid_formats(gl_data, bank_data)
        quality_exceptions.extend(invalid_formats)
        
        print(f"   ✅ Data quality detection complete: {len(quality_exceptions)} issues found")
        return quality_exceptions
    
    def _check_missing_fields(self, gl_data, bank_data):
        """Check for missing required fields"""
        missing = []
        
        # Check GL data
        for gl_account, account_data in gl_data.items():
            required_fields = ['name', 'balance', 'transaction_count']
            
            for field in required_fields:
                if field not in account_data or not account_data[field]:
                    missing.append({
                        'type': 'missing_field',
                        'category': 'data_quality',
                        'gl_account': gl_account,
                        'field': field,
                        'severity': 'medium',
                        'confidence': 1.0,
                        'message': f'Missing required field: {field}',
                        'recommendation': 'Complete missing data field'
                    })
        
        return missing
    
    def _check_invalid_formats(self, gl_data, bank_data):
        """Check for invalid data formats"""
        invalid = []
        
        # Check GL data formats
        for gl_account, account_data in gl_data.items():
            balance = account_data.get('balance', 0.0)
            
            # Check if balance is numeric
            if not isinstance(balance, (int, float)):
                invalid.append({
                    'type': 'invalid_format',
                    'category': 'data_quality',
                    'gl_account': gl_account,
                    'field': 'balance',
                    'value': balance,
                    'severity': 'high',
                    'confidence': 1.0,
                    'message': f'Invalid balance format: {balance}',
                    'recommendation': 'Fix data format to numeric value'
                })
        
        return invalid
    
    def _detect_system_errors(self, gl_data, bank_data):
        """Detect system or processing errors"""
        print("⚠️ Detecting system errors...")
        
        system_errors = []
        
        # Check for system-level issues
        system_issues = self._check_system_issues(gl_data, bank_data)
        system_errors.extend(system_issues)
        
        print(f"   ✅ System error detection complete: {len(system_errors)} errors found")
        return system_errors
    
    def _check_system_issues(self, gl_data, bank_data):
        """Check for system-level issues"""
        issues = []
        
        # Check for empty data sets
        if not gl_data:
            issues.append({
                'type': 'empty_dataset',
                'category': 'system_error',
                'dataset': 'gl_data',
                'severity': 'critical',
                'confidence': 1.0,
                'message': 'GL data is empty',
                'recommendation': 'Check data source and processing'
            })
        
        if not bank_data.get('transactions'):
            issues.append({
                'type': 'empty_dataset',
                'category': 'system_error',
                'dataset': 'bank_data',
                'severity': 'critical',
                'confidence': 1.0,
                'message': 'Bank data is empty',
                'recommendation': 'Check data source and processing'
            })
        
        return issues
    
    def _process_validation_exceptions(self, validation_results):
        """Process validation results into exceptions"""
        exceptions = []
        
        for result in validation_results:
            severity = result.get('severity', 'info')
            
            if severity in ['high', 'critical']:
                exception = {
                    'type': 'validation_exception',
                    'category': 'discrepancy',
                    'validation_result': result,
                    'severity': severity,
                    'confidence': 0.9,
                    'message': f'Validation failed: {result.get("message", "")}',
                    'recommendation': result.get('recommendation', 'Review and correct data')
                }
                exceptions.append(exception)
        
        return exceptions
    
    def _trigger_escalations(self, exceptions):
        """Trigger escalations based on exception severity"""
        print("📞 Checking for escalations...")
        
        escalations = []
        
        for exception in exceptions:
            severity = exception.get('severity', 'info')
            confidence = exception.get('confidence', 0.0)
            
            if severity == 'critical' or confidence >= self.escalation_threshold:
                escalation = {
                    'type': 'escalation',
                    'exception': exception,
                    'escalation_level': self._get_escalation_level(severity),
                    'timestamp': self.timestamp,
                    'message': f'Escalation triggered for {exception.get("type", "unknown")}',
                    'action_required': 'Immediate review and resolution'
                }
                escalations.append(escalation)
                self.escalations_triggered.append(escalation)
        
        print(f"   ✅ Escalation check complete: {len(escalations)} escalations triggered")
        return escalations
    
    def _get_escalation_level(self, severity):
        """Get escalation level based on severity"""
        escalation_levels = {
            'low': 1,
            'medium': 2,
            'high': 3,
            'critical': 4
        }
        return escalation_levels.get(severity, 1)
    
    def _is_weekend_date(self, date_str):
        """Check if date is a weekend (simplified)"""
        try:
            if isinstance(date_str, str):
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            else:
                date_obj = date_str
            
            # Saturday = 5, Sunday = 6
            return date_obj.weekday() >= 5
        except:
            return False
    
    def _update_metrics(self, exceptions):
        """Update performance metrics"""
        self.metrics['total_exceptions'] += len(exceptions)
        
        for exception in exceptions:
            category = exception.get('category', '')
            severity = exception.get('severity', 'info')
            
            if category == 'anomaly':
                self.metrics['anomalies_detected'] += 1
            elif category == 'discrepancy':
                self.metrics['discrepancies_found'] += 1
            elif category == 'fraud_risk':
                self.metrics['fraud_risks_flagged'] += 1
    
    def get_exception_summary(self):
        """Get exception handling summary"""
        summary = {
            'timestamp': self.timestamp,
            'total_exceptions': self.metrics['total_exceptions'],
            'anomalies_detected': self.metrics['anomalies_detected'],
            'discrepancies_found': self.metrics['discrepancies_found'],
            'fraud_risks_flagged': self.metrics['fraud_risks_flagged'],
            'escalations_triggered': len(self.escalations_triggered),
            'critical_exceptions': len([e for e in self.exceptions_detected if e.get('severity') == 'critical']),
            'high_priority_exceptions': len([e for e in self.exceptions_detected if e.get('severity') == 'high'])
        }
        
        return summary
    
    def save_exception_results(self):
        """Save exception handling results"""
        results_data = {
            'timestamp': self.timestamp,
            'exceptions_detected': self.exceptions_detected,
            'anomalies_found': self.anomalies_found,
            'escalations_triggered': self.escalations_triggered,
            'fraud_risks_flagged': self.fraud_risks_flagged,
            'metrics': self.metrics,
            'summary': self.get_exception_summary()
        }
        
        filename = f"exception_handling_results_{self.timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(results_data, f, indent=2, default=str)
        
        print(f"✅ Exception handling results saved: {filename}")
        return filename

def main():
    """Test the exception handling engine"""
    print("🚨 EXCEPTION HANDLING ENGINE")
    print("=" * 35)
    print("🎯 Testing exception detection and handling")
    print("=" * 35)
    
    # Initialize engine
    engine = ExceptionHandlingEngine()
    
    # Sample GL data with various issues
    gl_data = {
        "74400": {
            "name": "RBC Activity",
            "balance": -845530.82,
            "transaction_count": 129,
            "transactions": [
                {"description": "ACH ADV FILE", "amount": 1000.00, "date": "2025-05-31", "type": "debit"},
                {"description": "Suspicious Round Amount", "amount": 100000.00, "date": "2025-05-30", "type": "debit"},
                {"description": "Weekend Transaction", "amount": 500.00, "date": "2025-05-25", "type": "credit"},  # Saturday
                {"description": "", "amount": 200.00, "date": "2025-05-29", "type": "debit"},  # Empty description
                {"description": "Rapid Transaction 1", "amount": 100.00, "date": "2025-05-28", "type": "debit"},
                {"description": "Rapid Transaction 2", "amount": 100.00, "date": "2025-05-28", "type": "debit"}
            ]
        }
    }
    
    # Sample bank data
    bank_data = {
        "transactions": [
            {"description": "ACH ADV FILE", "amount": 1000.00, "date": "2025-05-31", "type": "debit"}
        ]
    }
    
    # Test exception detection
    exceptions = engine.detect_exceptions(gl_data, bank_data)
    
    print(f"\n📊 EXCEPTION RESULTS:")
    for i, exception in enumerate(exceptions, 1):
        print(f"\n{i}. {exception['type'].upper()} - {exception['severity'].upper()}")
        print(f"   Category: {exception.get('category', 'unknown')}")
        print(f"   Message: {exception['message']}")
        print(f"   Recommendation: {exception['recommendation']}")
    
    # Get summary
    summary = engine.get_exception_summary()
    print(f"\n📈 EXCEPTION SUMMARY:")
    print(f"Total exceptions: {summary['total_exceptions']}")
    print(f"Anomalies: {summary['anomalies_detected']}")
    print(f"Discrepancies: {summary['discrepancies_found']}")
    print(f"Fraud risks: {summary['fraud_risks_flagged']}")
    print(f"Escalations: {summary['escalations_triggered']}")
    print(f"Critical: {summary['critical_exceptions']}")
    print(f"High priority: {summary['high_priority_exceptions']}")
    
    # Save results
    engine.save_exception_results()

if __name__ == "__main__":
    main()
