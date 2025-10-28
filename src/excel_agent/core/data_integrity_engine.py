#!/usr/bin/env python3
"""
Data Integrity Engine
Implements transaction completeness validation, duplicate detection, and data consistency verification
Based on AI thinking insights for comprehensive data quality control
"""

import json
import hashlib
from datetime import datetime
from collections import defaultdict, Counter
import re

class DataIntegrityEngine:
    def __init__(self):
        self.name = "DataIntegrityEngine"
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Integrity check thresholds
        self.duplicate_threshold = 0.95  # 95% similarity for duplicates
        self.completeness_threshold = 0.98  # 98% completeness required
        self.consistency_threshold = 0.90  # 90% consistency required
        
        # Data integrity rules
        self.integrity_rules = {
            "transaction_completeness": {
                "description": "All transactions must have required fields",
                "required_fields": ["description", "amount", "date", "type"],
                "critical": True
            },
            "duplicate_detection": {
                "description": "No duplicate transactions allowed",
                "similarity_threshold": 0.95,
                "critical": True
            },
            "data_consistency": {
                "description": "Data must be consistent across systems",
                "consistency_threshold": 0.90,
                "critical": True
            },
            "amount_validation": {
                "description": "Amounts must be valid and reasonable",
                "max_amount": 1000000.0,  # $1M
                "critical": True
            }
        }
        
        # Integrity results
        self.integrity_results = []
        self.duplicates_found = []
        self.missing_data = []
        self.inconsistencies = []
        self.quality_metrics = {
            "total_checks": 0,
            "passed_checks": 0,
            "failed_checks": 0,
            "duplicates_detected": 0,
            "missing_data_items": 0,
            "inconsistencies_found": 0
        }
        
    def validate_data_integrity(self, gl_data, bank_data):
        """Comprehensive data integrity validation"""
        print("🔍 DATA INTEGRITY ENGINE")
        print("=" * 35)
        print("🎯 Transaction completeness and data consistency validation")
        print("=" * 35)
        
        integrity_results = []
        
        # 1. Transaction Completeness Validation
        completeness_results = self._validate_transaction_completeness(gl_data, bank_data)
        integrity_results.extend(completeness_results)
        
        # 2. Duplicate Detection
        duplicate_results = self._detect_duplicates(gl_data, bank_data)
        integrity_results.extend(duplicate_results)
        
        # 3. Data Consistency Validation
        consistency_results = self._validate_data_consistency(gl_data, bank_data)
        integrity_results.extend(consistency_results)
        
        # 4. Amount Validation
        amount_results = self._validate_amounts(gl_data, bank_data)
        integrity_results.extend(amount_results)
        
        # 5. Date Validation
        date_results = self._validate_dates(gl_data, bank_data)
        integrity_results.extend(date_results)
        
        # Store results
        self.integrity_results.extend(integrity_results)
        
        # Update quality metrics
        self._update_quality_metrics(integrity_results)
        
        print(f"✅ Data integrity validation complete: {len(integrity_results)} checks performed")
        return integrity_results
    
    def _validate_transaction_completeness(self, gl_data, bank_data):
        """Validate transaction completeness"""
        print("📋 Validating transaction completeness...")
        
        results = []
        
        # Check GL transactions
        for gl_account, account_data in gl_data.items():
            transactions = account_data.get('transactions', [])
            
            for i, tx in enumerate(transactions):
                missing_fields = self._check_required_fields(tx, self.integrity_rules['transaction_completeness']['required_fields'])
                
                if missing_fields:
                    result = {
                        'type': 'missing_fields',
                        'gl_account': gl_account,
                        'transaction_index': i,
                        'missing_fields': missing_fields,
                        'severity': 'high',
                        'message': f'Missing required fields: {", ".join(missing_fields)}',
                        'recommendation': 'Complete missing transaction data'
                    }
                    results.append(result)
                    self.missing_data.append(result)
        
        # Check bank transactions
        bank_transactions = bank_data.get('transactions', [])
        for i, tx in enumerate(bank_transactions):
            missing_fields = self._check_required_fields(tx, self.integrity_rules['transaction_completeness']['required_fields'])
            
            if missing_fields:
                result = {
                    'type': 'missing_fields',
                    'source': 'bank',
                    'transaction_index': i,
                    'missing_fields': missing_fields,
                    'severity': 'high',
                    'message': f'Missing required fields: {", ".join(missing_fields)}',
                    'recommendation': 'Complete missing transaction data'
                }
                results.append(result)
                self.missing_data.append(result)
        
        print(f"   ✅ Completeness validation complete: {len(results)} issues found")
        return results
    
    def _check_required_fields(self, transaction, required_fields):
        """Check if transaction has all required fields"""
        missing_fields = []
        
        for field in required_fields:
            if field not in transaction or not transaction[field]:
                missing_fields.append(field)
        
        return missing_fields
    
    def _detect_duplicates(self, gl_data, bank_data):
        """Detect duplicate transactions"""
        print("🔍 Detecting duplicate transactions...")
        
        results = []
        
        # Check GL duplicates
        gl_duplicates = self._find_duplicates_in_transactions(gl_data, 'gl')
        results.extend(gl_duplicates)
        
        # Check bank duplicates
        bank_duplicates = self._find_duplicates_in_transactions(bank_data, 'bank')
        results.extend(bank_duplicates)
        
        # Check cross-system duplicates
        cross_duplicates = self._find_cross_system_duplicates(gl_data, bank_data)
        results.extend(cross_duplicates)
        
        print(f"   ✅ Duplicate detection complete: {len(results)} duplicates found")
        return results
    
    def _find_duplicates_in_transactions(self, data, source):
        """Find duplicates within a single system"""
        duplicates = []
        
        if source == 'gl':
            all_transactions = []
            for gl_account, account_data in data.items():
                transactions = account_data.get('transactions', [])
                for tx in transactions:
                    tx['gl_account'] = gl_account
                    all_transactions.append(tx)
        else:
            all_transactions = data.get('transactions', [])
        
        # Group transactions by similarity
        transaction_groups = defaultdict(list)
        
        for i, tx1 in enumerate(all_transactions):
            for j, tx2 in enumerate(all_transactions[i+1:], i+1):
                similarity = self._calculate_transaction_similarity(tx1, tx2)
                
                if similarity >= self.duplicate_threshold:
                    group_key = f"{tx1.get('description', '')}_{tx1.get('amount', 0)}"
                    transaction_groups[group_key].extend([tx1, tx2])
        
        # Report duplicate groups
        for group_key, duplicate_txs in transaction_groups.items():
            if len(duplicate_txs) > 1:
                duplicate = {
                    'type': 'duplicate_transactions',
                    'source': source,
                    'count': len(duplicate_txs),
                    'transactions': duplicate_txs[:3],  # Show first 3
                    'similarity': self._calculate_transaction_similarity(duplicate_txs[0], duplicate_txs[1]),
                    'severity': 'high',
                    'message': f'{len(duplicate_txs)} duplicate transactions found',
                    'recommendation': 'Review and remove duplicate transactions'
                }
                duplicates.append(duplicate)
                self.duplicates_found.append(duplicate)
        
        return duplicates
    
    def _find_cross_system_duplicates(self, gl_data, bank_data):
        """Find duplicates between GL and bank systems"""
        cross_duplicates = []
        
        # Get all GL transactions
        gl_transactions = []
        for account_data in gl_data.values():
            gl_transactions.extend(account_data.get('transactions', []))
        
        # Get all bank transactions
        bank_transactions = bank_data.get('transactions', [])
        
        # Check for cross-system duplicates
        for gl_tx in gl_transactions:
            for bank_tx in bank_transactions:
                similarity = self._calculate_transaction_similarity(gl_tx, bank_tx)
                
                if similarity >= self.duplicate_threshold:
                    duplicate = {
                        'type': 'cross_system_duplicate',
                        'gl_transaction': gl_tx,
                        'bank_transaction': bank_tx,
                        'similarity': similarity,
                        'severity': 'medium',
                        'message': f'Potential cross-system duplicate (similarity: {similarity:.2f})',
                        'recommendation': 'Verify if these are the same transaction'
                    }
                    cross_duplicates.append(duplicate)
        
        return cross_duplicates
    
    def _calculate_transaction_similarity(self, tx1, tx2):
        """Calculate similarity between two transactions"""
        # Amount similarity
        amount1 = tx1.get('amount', 0.0)
        amount2 = tx2.get('amount', 0.0)
        amount_similarity = 1.0 if abs(amount1 - amount2) < 0.01 else 0.0
        
        # Description similarity
        desc1 = tx1.get('description', '').upper()
        desc2 = tx2.get('description', '').upper()
        desc_similarity = self._calculate_text_similarity(desc1, desc2)
        
        # Date similarity
        date1 = tx1.get('date', '')
        date2 = tx2.get('date', '')
        date_similarity = 1.0 if date1 == date2 else 0.5
        
        # Weighted similarity
        similarity = (amount_similarity * 0.4 + desc_similarity * 0.4 + date_similarity * 0.2)
        
        return similarity
    
    def _calculate_text_similarity(self, text1, text2):
        """Calculate text similarity using simple word matching"""
        if not text1 or not text2:
            return 0.0
        
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def _validate_data_consistency(self, gl_data, bank_data):
        """Validate data consistency across systems"""
        print("🔄 Validating data consistency...")
        
        results = []
        
        # Check GL account consistency
        for gl_account, account_data in gl_data.items():
            balance = account_data.get('balance', 0.0)
            debits = account_data.get('debits', 0.0)
            credits = account_data.get('credits', 0.0)
            
            # Check if balance = credits - debits
            calculated_balance = credits - debits
            balance_difference = abs(balance - calculated_balance)
            
            if balance_difference > 0.01:
                result = {
                    'type': 'balance_calculation_inconsistency',
                    'gl_account': gl_account,
                    'reported_balance': balance,
                    'calculated_balance': calculated_balance,
                    'difference': balance_difference,
                    'severity': 'high',
                    'message': f'Balance calculation inconsistency: ${balance_difference:.2f}',
                    'recommendation': 'Recalculate account balance'
                }
                results.append(result)
                self.inconsistencies.append(result)
        
        # Check transaction count consistency
        total_gl_transactions = sum(account.get('transaction_count', 0) for account in gl_data.values())
        total_bank_transactions = bank_data.get('transaction_count', 0)
        
        if abs(total_gl_transactions - total_bank_transactions) > total_gl_transactions * 0.1:  # 10% difference
            result = {
                'type': 'transaction_count_inconsistency',
                'gl_transactions': total_gl_transactions,
                'bank_transactions': total_bank_transactions,
                'difference': abs(total_gl_transactions - total_bank_transactions),
                'severity': 'medium',
                'message': f'Transaction count inconsistency: GL {total_gl_transactions}, Bank {total_bank_transactions}',
                'recommendation': 'Verify transaction counts are accurate'
            }
            results.append(result)
            self.inconsistencies.append(result)
        
        print(f"   ✅ Consistency validation complete: {len(results)} issues found")
        return results
    
    def _validate_amounts(self, gl_data, bank_data):
        """Validate transaction amounts"""
        print("💰 Validating transaction amounts...")
        
        results = []
        max_amount = self.integrity_rules['amount_validation']['max_amount']
        
        # Check GL amounts
        for gl_account, account_data in gl_data.items():
            transactions = account_data.get('transactions', [])
            
            for tx in transactions:
                amount = abs(tx.get('amount', 0.0))
                
                if amount > max_amount:
                    result = {
                        'type': 'excessive_amount',
                        'gl_account': gl_account,
                        'amount': amount,
                        'max_allowed': max_amount,
                        'severity': 'high',
                        'message': f'Excessive amount: ${amount:,.2f} (max: ${max_amount:,.2f})',
                        'recommendation': 'Verify transaction amount is correct'
                    }
                    results.append(result)
        
        # Check bank amounts
        bank_transactions = bank_data.get('transactions', [])
        for tx in bank_transactions:
            amount = abs(tx.get('amount', 0.0))
            
            if amount > max_amount:
                result = {
                    'type': 'excessive_amount',
                    'source': 'bank',
                    'amount': amount,
                    'max_allowed': max_amount,
                    'severity': 'high',
                    'message': f'Excessive amount: ${amount:,.2f} (max: ${max_amount:,.2f})',
                    'recommendation': 'Verify transaction amount is correct'
                }
                results.append(result)
        
        print(f"   ✅ Amount validation complete: {len(results)} issues found")
        return results
    
    def _validate_dates(self, gl_data, bank_data):
        """Validate transaction dates"""
        print("📅 Validating transaction dates...")
        
        results = []
        
        # Check for future dates
        current_date = datetime.now()
        
        # Check GL dates
        for gl_account, account_data in gl_data.items():
            transactions = account_data.get('transactions', [])
            
            for tx in transactions:
                tx_date = tx.get('date', '')
                if tx_date and self._is_future_date(tx_date, current_date):
                    result = {
                        'type': 'future_date',
                        'gl_account': gl_account,
                        'date': tx_date,
                        'severity': 'medium',
                        'message': f'Future date detected: {tx_date}',
                        'recommendation': 'Verify transaction date is correct'
                    }
                    results.append(result)
        
        # Check bank dates
        bank_transactions = bank_data.get('transactions', [])
        for tx in bank_transactions:
            tx_date = tx.get('date', '')
            if tx_date and self._is_future_date(tx_date, current_date):
                result = {
                    'type': 'future_date',
                    'source': 'bank',
                    'date': tx_date,
                    'severity': 'medium',
                    'message': f'Future date detected: {tx_date}',
                    'recommendation': 'Verify transaction date is correct'
                }
                results.append(result)
        
        print(f"   ✅ Date validation complete: {len(results)} issues found")
        return results
    
    def _is_future_date(self, date_str, current_date):
        """Check if date is in the future"""
        try:
            if isinstance(date_str, str):
                tx_date = datetime.strptime(date_str, '%Y-%m-%d')
            else:
                tx_date = date_str
            
            return tx_date > current_date
        except:
            return False
    
    def _update_quality_metrics(self, integrity_results):
        """Update quality metrics based on integrity results"""
        self.quality_metrics['total_checks'] += len(integrity_results)
        
        for result in integrity_results:
            result_type = result.get('type', '')
            severity = result.get('severity', 'info')
            
            if severity in ['medium', 'high', 'critical']:
                self.quality_metrics['failed_checks'] += 1
                
                if 'duplicate' in result_type:
                    self.quality_metrics['duplicates_detected'] += 1
                elif 'missing' in result_type:
                    self.quality_metrics['missing_data_items'] += 1
                elif 'inconsistency' in result_type:
                    self.quality_metrics['inconsistencies_found'] += 1
            else:
                self.quality_metrics['passed_checks'] += 1
    
    def get_integrity_summary(self):
        """Get data integrity summary"""
        summary = {
            'timestamp': self.timestamp,
            'total_checks': self.quality_metrics['total_checks'],
            'passed_checks': self.quality_metrics['passed_checks'],
            'failed_checks': self.quality_metrics['failed_checks'],
            'duplicates_detected': self.quality_metrics['duplicates_detected'],
            'missing_data_items': self.quality_metrics['missing_data_items'],
            'inconsistencies_found': self.quality_metrics['inconsistencies_found'],
            'integrity_score': self._calculate_integrity_score()
        }
        
        return summary
    
    def _calculate_integrity_score(self):
        """Calculate data integrity score"""
        total = self.quality_metrics['total_checks']
        if total == 0:
            return 100.0
        
        passed = self.quality_metrics['passed_checks']
        duplicate_penalty = self.quality_metrics['duplicates_detected'] * 5
        missing_penalty = self.quality_metrics['missing_data_items'] * 10
        inconsistency_penalty = self.quality_metrics['inconsistencies_found'] * 15
        
        score = ((passed / total) * 100) - duplicate_penalty - missing_penalty - inconsistency_penalty
        return max(0.0, min(100.0, score))
    
    def save_integrity_results(self):
        """Save data integrity results"""
        results_data = {
            'timestamp': self.timestamp,
            'integrity_results': self.integrity_results,
            'duplicates_found': self.duplicates_found,
            'missing_data': self.missing_data,
            'inconsistencies': self.inconsistencies,
            'quality_metrics': self.quality_metrics,
            'summary': self.get_integrity_summary()
        }
        
        filename = f"data_integrity_results_{self.timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(results_data, f, indent=2, default=str)
        
        print(f"✅ Data integrity results saved: {filename}")
        return filename

def main():
    """Test the data integrity engine"""
    print("🔍 DATA INTEGRITY ENGINE")
    print("=" * 30)
    print("🎯 Testing data integrity validation")
    print("=" * 30)
    
    # Initialize engine
    engine = DataIntegrityEngine()
    
    # Sample GL data with some issues
    gl_data = {
        "74400": {
            "name": "RBC Activity", 
            "balance": -845530.82, 
            "debits": 2393612.32,
            "credits": 3239143.14,
            "transaction_count": 129,
            "transactions": [
                {"description": "ACH ADV FILE", "amount": 1000.00, "date": "2025-05-31", "type": "debit"},
                {"description": "ACH ADV FILE", "amount": 1000.00, "date": "2025-05-31", "type": "debit"},  # Duplicate
                {"description": "", "amount": 500.00, "date": "2025-05-30", "type": "credit"},  # Missing description
                {"description": "Large Transaction", "amount": 2000000.00, "date": "2025-05-29", "type": "debit"}  # Excessive amount
            ]
        }
    }
    
    # Sample bank data
    bank_data = {
        "transaction_count": 2,
        "transactions": [
            {"description": "ACH ADV FILE", "amount": 1000.00, "date": "2025-05-31", "type": "debit"},
            {"description": "Future Transaction", "amount": 100.00, "date": "2025-12-31", "type": "credit"}  # Future date
        ]
    }
    
    # Test data integrity validation
    integrity_results = engine.validate_data_integrity(gl_data, bank_data)
    
    print(f"\n📊 INTEGRITY RESULTS:")
    for i, result in enumerate(integrity_results, 1):
        print(f"\n{i}. {result['type'].upper()} - {result['severity'].upper()}")
        print(f"   Message: {result['message']}")
        print(f"   Recommendation: {result['recommendation']}")
    
    # Get summary
    summary = engine.get_integrity_summary()
    print(f"\n📈 INTEGRITY SUMMARY:")
    print(f"Total checks: {summary['total_checks']}")
    print(f"Passed: {summary['passed_checks']}")
    print(f"Failed: {summary['failed_checks']}")
    print(f"Duplicates: {summary['duplicates_detected']}")
    print(f"Missing data: {summary['missing_data_items']}")
    print(f"Inconsistencies: {summary['inconsistencies_found']}")
    print(f"Integrity score: {summary['integrity_score']:.1f}%")
    
    # Save results
    engine.save_integrity_results()

if __name__ == "__main__":
    main()
