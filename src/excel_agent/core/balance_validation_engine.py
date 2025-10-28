#!/usr/bin/env python3
"""
Balance Validation Engine
Implements real-time balance checking and automated discrepancy detection
Based on AI thinking insights for quality control and validation
"""

import json
import numpy as np
from datetime import datetime
from collections import defaultdict
import re

class BalanceValidationEngine:
    def __init__(self):
        self.name = "BalanceValidationEngine"
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Validation thresholds
        self.balance_tolerance = 0.01  # $0.01 tolerance
        self.large_transaction_threshold = 10000.0  # $10,000
        self.suspicious_amount_threshold = 50000.0  # $50,000
        
        # Balance validation rules
        self.validation_rules = {
            "balance_per_books": {
                "description": "Balance per Books validation",
                "tolerance": 0.01,
                "critical": True
            },
            "balance_per_statement": {
                "description": "Balance per Statement validation", 
                "tolerance": 0.01,
                "critical": True
            },
            "adjusted_totals": {
                "description": "Adjusted totals must match",
                "tolerance": 0.01,
                "critical": True
            },
            "transaction_completeness": {
                "description": "All transactions must be accounted for",
                "tolerance": 0.0,
                "critical": True
            }
        }
        
        # Validation results
        self.validation_results = []
        self.discrepancies_found = []
        self.exceptions_flagged = []
        self.quality_metrics = {
            "total_validations": 0,
            "passed_validations": 0,
            "failed_validations": 0,
            "critical_issues": 0,
            "warnings": 0
        }
        
    def validate_balances(self, gl_data, bank_data, reconciliation_data=None):
        """Comprehensive balance validation"""
        print("🔍 BALANCE VALIDATION ENGINE")
        print("=" * 40)
        print("🎯 Real-time balance checking and discrepancy detection")
        print("=" * 40)
        
        validation_results = []
        
        # 1. GL Balance Validation
        gl_validation = self._validate_gl_balances(gl_data)
        validation_results.extend(gl_validation)
        
        # 2. Bank Balance Validation
        bank_validation = self._validate_bank_balances(bank_data)
        validation_results.extend(bank_validation)
        
        # 3. Reconciliation Balance Validation
        if reconciliation_data:
            recon_validation = self._validate_reconciliation_balances(reconciliation_data)
            validation_results.extend(recon_validation)
        
        # 4. Cross-System Balance Validation
        cross_validation = self._validate_cross_system_balances(gl_data, bank_data)
        validation_results.extend(cross_validation)
        
        # 5. Transaction Completeness Validation
        completeness_validation = self._validate_transaction_completeness(gl_data, bank_data)
        validation_results.extend(completeness_validation)
        
        # Store results
        self.validation_results.extend(validation_results)
        
        # Update quality metrics
        self._update_quality_metrics(validation_results)
        
        print(f"✅ Validation complete: {len(validation_results)} checks performed")
        return validation_results
    
    def _validate_gl_balances(self, gl_data):
        """Validate GL account balances"""
        print("📊 Validating GL account balances...")
        
        validations = []
        total_gl_balance = 0.0
        
        for gl_account, account_data in gl_data.items():
            balance = account_data.get('balance', 0.0)
            total_gl_balance += balance
            
            # Check for unusual balances
            if abs(balance) > self.suspicious_amount_threshold:
                validation = {
                    'type': 'suspicious_balance',
                    'gl_account': gl_account,
                    'balance': balance,
                    'severity': 'high',
                    'message': f'Unusually large balance: ${balance:,.2f}',
                    'recommendation': 'Review transaction details for accuracy'
                }
                validations.append(validation)
                self.exceptions_flagged.append(validation)
            
            # Check for zero balance accounts with activity
            if abs(balance) < 0.01 and account_data.get('transaction_count', 0) > 0:
                validation = {
                    'type': 'zero_balance_with_activity',
                    'gl_account': gl_account,
                    'balance': balance,
                    'severity': 'medium',
                    'message': f'Zero balance with {account_data.get("transaction_count", 0)} transactions',
                    'recommendation': 'Verify all transactions are properly recorded'
                }
                validations.append(validation)
        
        # Check overall GL balance
        if abs(total_gl_balance) > self.balance_tolerance:
            validation = {
                'type': 'gl_balance_imbalance',
                'total_balance': total_gl_balance,
                'severity': 'critical',
                'message': f'GL accounts not balanced: ${total_gl_balance:,.2f}',
                'recommendation': 'Investigate and correct imbalances'
            }
            validations.append(validation)
            self.discrepancies_found.append(validation)
        else:
            validation = {
                'type': 'gl_balance_valid',
                'total_balance': total_gl_balance,
                'severity': 'info',
                'message': f'GL accounts balanced: ${total_gl_balance:,.2f}',
                'recommendation': 'No action required'
            }
            validations.append(validation)
        
        print(f"   ✅ GL validation complete: {len(validations)} checks")
        return validations
    
    def _validate_bank_balances(self, bank_data):
        """Validate bank statement balances"""
        print("🏦 Validating bank statement balances...")
        
        validations = []
        
        # Check bank statement balance
        bank_balance = bank_data.get('ending_balance', 0.0)
        total_debits = bank_data.get('total_debits', 0.0)
        total_credits = bank_data.get('total_credits', 0.0)
        
        # Validate bank balance calculation
        calculated_balance = total_credits - total_debits
        balance_difference = abs(bank_balance - calculated_balance)
        
        if balance_difference > self.balance_tolerance:
            validation = {
                'type': 'bank_balance_mismatch',
                'reported_balance': bank_balance,
                'calculated_balance': calculated_balance,
                'difference': balance_difference,
                'severity': 'high',
                'message': f'Bank balance mismatch: ${balance_difference:,.2f}',
                'recommendation': 'Verify bank statement calculations'
            }
            validations.append(validation)
            self.discrepancies_found.append(validation)
        else:
            validation = {
                'type': 'bank_balance_valid',
                'reported_balance': bank_balance,
                'calculated_balance': calculated_balance,
                'severity': 'info',
                'message': f'Bank balance validated: ${bank_balance:,.2f}',
                'recommendation': 'No action required'
            }
            validations.append(validation)
        
        # Check for unusual transaction amounts
        transactions = bank_data.get('transactions', [])
        for tx in transactions:
            amount = tx.get('amount', 0.0)
            if amount > self.large_transaction_threshold:
                validation = {
                    'type': 'large_transaction',
                    'transaction': tx,
                    'amount': amount,
                    'severity': 'medium',
                    'message': f'Large transaction detected: ${amount:,.2f}',
                    'recommendation': 'Verify transaction details'
                }
                validations.append(validation)
        
        print(f"   ✅ Bank validation complete: {len(validations)} checks")
        return validations
    
    def _validate_reconciliation_balances(self, reconciliation_data):
        """Validate reconciliation balances"""
        print("⚖️ Validating reconciliation balances...")
        
        validations = []
        
        # Check Balance per Books vs Balance per Statement
        balance_per_books = reconciliation_data.get('balance_per_books', 0.0)
        balance_per_statement = reconciliation_data.get('balance_per_statement', 0.0)
        
        difference = abs(balance_per_books - balance_per_statement)
        
        if difference > self.balance_tolerance:
            validation = {
                'type': 'reconciliation_imbalance',
                'balance_per_books': balance_per_books,
                'balance_per_statement': balance_per_statement,
                'difference': difference,
                'severity': 'critical',
                'message': f'Reconciliation imbalance: ${difference:,.2f}',
                'recommendation': 'Investigate and resolve discrepancies'
            }
            validations.append(validation)
            self.discrepancies_found.append(validation)
        else:
            validation = {
                'type': 'reconciliation_balanced',
                'balance_per_books': balance_per_books,
                'balance_per_statement': balance_per_statement,
                'severity': 'info',
                'message': f'Reconciliation balanced: ${difference:,.2f}',
                'recommendation': 'No action required'
            }
            validations.append(validation)
        
        print(f"   ✅ Reconciliation validation complete: {len(validations)} checks")
        return validations
    
    def _validate_cross_system_balances(self, gl_data, bank_data):
        """Validate balances across systems"""
        print("🔄 Validating cross-system balances...")
        
        validations = []
        
        # Calculate total GL balance
        total_gl_balance = sum(account.get('balance', 0.0) for account in gl_data.values())
        
        # Calculate total bank balance
        total_bank_balance = bank_data.get('ending_balance', 0.0)
        
        # Check for significant differences
        balance_difference = abs(total_gl_balance - total_bank_balance)
        
        if balance_difference > self.balance_tolerance:
            validation = {
                'type': 'cross_system_imbalance',
                'gl_balance': total_gl_balance,
                'bank_balance': total_bank_balance,
                'difference': balance_difference,
                'severity': 'high',
                'message': f'Cross-system imbalance: ${balance_difference:,.2f}',
                'recommendation': 'Investigate timing differences and missing transactions'
            }
            validations.append(validation)
            self.discrepancies_found.append(validation)
        else:
            validation = {
                'type': 'cross_system_balanced',
                'gl_balance': total_gl_balance,
                'bank_balance': total_bank_balance,
                'severity': 'info',
                'message': f'Cross-system balanced: ${balance_difference:,.2f}',
                'recommendation': 'No action required'
            }
            validations.append(validation)
        
        print(f"   ✅ Cross-system validation complete: {len(validations)} checks")
        return validations
    
    def _validate_transaction_completeness(self, gl_data, bank_data):
        """Validate transaction completeness"""
        print("📋 Validating transaction completeness...")
        
        validations = []
        
        # Check for missing transactions
        gl_transactions = []
        for account_data in gl_data.values():
            gl_transactions.extend(account_data.get('transactions', []))
        
        bank_transactions = bank_data.get('transactions', [])
        
        # Check for unmatched transactions
        unmatched_gl = self._find_unmatched_transactions(gl_transactions, bank_transactions)
        unmatched_bank = self._find_unmatched_transactions(bank_transactions, gl_transactions)
        
        if unmatched_gl:
            validation = {
                'type': 'unmatched_gl_transactions',
                'count': len(unmatched_gl),
                'transactions': unmatched_gl[:5],  # Show first 5
                'severity': 'high',
                'message': f'{len(unmatched_gl)} unmatched GL transactions',
                'recommendation': 'Find corresponding bank transactions or create adjustments'
            }
            validations.append(validation)
            self.exceptions_flagged.append(validation)
        
        if unmatched_bank:
            validation = {
                'type': 'unmatched_bank_transactions',
                'count': len(unmatched_bank),
                'transactions': unmatched_bank[:5],  # Show first 5
                'severity': 'high',
                'message': f'{len(unmatched_bank)} unmatched bank transactions',
                'recommendation': 'Find corresponding GL transactions or create adjustments'
            }
            validations.append(validation)
            self.exceptions_flagged.append(validation)
        
        print(f"   ✅ Completeness validation complete: {len(validations)} checks")
        return validations
    
    def _find_unmatched_transactions(self, transactions1, transactions2):
        """Find transactions that don't have matches"""
        unmatched = []
        
        for tx1 in transactions1:
            amount1 = tx1.get('amount', 0.0)
            desc1 = tx1.get('description', '').upper()
            
            found_match = False
            for tx2 in transactions2:
                amount2 = tx2.get('amount', 0.0)
                desc2 = tx2.get('description', '').upper()
                
                # Check amount match
                if abs(amount1 - amount2) < 0.01:
                    # Check description similarity
                    similarity = self._calculate_description_similarity(desc1, desc2)
                    if similarity > 0.7:
                        found_match = True
                        break
            
            if not found_match:
                unmatched.append(tx1)
        
        return unmatched
    
    def _calculate_description_similarity(self, desc1, desc2):
        """Calculate similarity between descriptions"""
        if not desc1 or not desc2:
            return 0.0
        
        words1 = set(desc1.split())
        words2 = set(desc2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def _update_quality_metrics(self, validation_results):
        """Update quality metrics based on validation results"""
        self.quality_metrics['total_validations'] += len(validation_results)
        
        for result in validation_results:
            severity = result.get('severity', 'info')
            
            if severity == 'info':
                self.quality_metrics['passed_validations'] += 1
            elif severity in ['medium', 'high', 'critical']:
                self.quality_metrics['failed_validations'] += 1
                
                if severity == 'critical':
                    self.quality_metrics['critical_issues'] += 1
                elif severity == 'medium':
                    self.quality_metrics['warnings'] += 1
    
    def get_validation_summary(self):
        """Get validation summary and recommendations"""
        summary = {
            'timestamp': self.timestamp,
            'total_validations': self.quality_metrics['total_validations'],
            'passed_validations': self.quality_metrics['passed_validations'],
            'failed_validations': self.quality_metrics['failed_validations'],
            'critical_issues': self.quality_metrics['critical_issues'],
            'warnings': self.quality_metrics['warnings'],
            'discrepancies_found': len(self.discrepancies_found),
            'exceptions_flagged': len(self.exceptions_flagged),
            'quality_score': self._calculate_quality_score()
        }
        
        return summary
    
    def _calculate_quality_score(self):
        """Calculate overall quality score"""
        total = self.quality_metrics['total_validations']
        if total == 0:
            return 100.0
        
        passed = self.quality_metrics['passed_validations']
        critical_penalty = self.quality_metrics['critical_issues'] * 10
        warning_penalty = self.quality_metrics['warnings'] * 5
        
        score = ((passed / total) * 100) - critical_penalty - warning_penalty
        return max(0.0, min(100.0, score))
    
    def save_validation_results(self):
        """Save validation results"""
        results_data = {
            'timestamp': self.timestamp,
            'validation_results': self.validation_results,
            'discrepancies_found': self.discrepancies_found,
            'exceptions_flagged': self.exceptions_flagged,
            'quality_metrics': self.quality_metrics,
            'summary': self.get_validation_summary()
        }
        
        filename = f"balance_validation_results_{self.timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(results_data, f, indent=2, default=str)
        
        print(f"✅ Validation results saved: {filename}")
        return filename

def main():
    """Test the balance validation engine"""
    print("🔍 BALANCE VALIDATION ENGINE")
    print("=" * 35)
    print("🎯 Testing balance validation and quality control")
    print("=" * 35)
    
    # Initialize engine
    engine = BalanceValidationEngine()
    
    # Sample GL data
    gl_data = {
        "74400": {"name": "RBC Activity", "balance": -845530.82, "transaction_count": 129},
        "74505": {"name": "CNS Settlement", "balance": -4688629.71, "transaction_count": 310},
        "74510": {"name": "EFUNDS Corp", "balance": 0.0, "transaction_count": 0}
    }
    
    # Sample bank data
    bank_data = {
        "ending_balance": 1329160.04,
        "total_debits": 21887988.14,
        "total_credits": 23217148.18,
        "transactions": [
            {"description": "ACH ADV FILE", "amount": 1000.00},
            {"description": "Large Transaction", "amount": 15000.00}
        ]
    }
    
    # Test balance validation
    validation_results = engine.validate_balances(gl_data, bank_data)
    
    print(f"\n📊 VALIDATION RESULTS:")
    for i, result in enumerate(validation_results, 1):
        print(f"\n{i}. {result['type'].upper()} - {result['severity'].upper()}")
        print(f"   Message: {result['message']}")
        print(f"   Recommendation: {result['recommendation']}")
    
    # Get summary
    summary = engine.get_validation_summary()
    print(f"\n📈 VALIDATION SUMMARY:")
    print(f"Total validations: {summary['total_validations']}")
    print(f"Passed: {summary['passed_validations']}")
    print(f"Failed: {summary['failed_validations']}")
    print(f"Critical issues: {summary['critical_issues']}")
    print(f"Quality score: {summary['quality_score']:.1f}%")
    
    # Save results
    engine.save_validation_results()

if __name__ == "__main__":
    main()
