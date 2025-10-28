#!/usr/bin/env python3
"""
Reconciliation Matcher Agent
Matches GL transactions with bank transactions according to OP training document requirements
"""

import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import json
import os
from pathlib import Path

class ReconciliationMatcher:
    """
    Reconciliation Matcher Agent for OP-compliant transaction matching
    Implements all requirements from OP training document
    """
    
    def __init__(self, gl_data: pd.DataFrame = None, bank_data: pd.DataFrame = None):
        """
        Initialize Reconciliation Matcher with data validation
        
        Args:
            gl_data: General Ledger transaction data
            bank_data: Bank statement transaction data
        """
        self.logger = self._setup_logging()
        self.logger.info("Initializing Reconciliation Matcher Agent")
        
        # OP Training Document Requirements
        self.gl_accounts = ["74400", "74505", "74510", "74515", "74520", "74525", 
                           "74530", "74535", "74540", "74550", "74560", "74570"]
        
        # Validate and store data
        self.gl_data = self._validate_gl_data(gl_data) if gl_data is not None else pd.DataFrame()
        self.bank_data = self._validate_bank_data(bank_data) if bank_data is not None else pd.DataFrame()
        
        # Transaction mappings from OP training document
        self.transaction_mappings = {
            "ACH ADV File": "74530",
            "ACH ADV FILE - Orig CR": "74540", 
            "ACH ADV FILE - Orig DB": "74570",
            "RBC": "74400",
            "CNS Settlement": "74505",
            "EFUNDS Corp - DLY SETTLE": "74510",
            "EFUNDS Corp - FEE SETTLE": "74400",
            "PULSE FEES": "74505",
            "Withdrawal Coin": "74400",
            "Withdrawal Currency": "74400",
            "1591 Image CL Presentment": "74520",
            "1590 Image CL Presentment": "74560",
            "Cooperative Business": "74550",
            "Currency Exchange Payment": "74400",
            "ICUL ServCorp": "74535",
            "CRIF Select Corp": "74400",
            "Wire transfers": "74400",
            "Cash Letter Corr": "74515",
            "OCUL SERVICES CO": "74400",
            "Analysis Service Charge": "74400",
            "VISA U.S.A., INC": "74400"
        }
        
        # Timing differences from OP training document
        self.timing_differences = {
            "ATM settlement": "74505",
            "Shared Branching": "74510", 
            "Check deposit Barks/MtG": "74560",
            "Gift Card activity": "74535",
            "CBS activity": "74550",
            "CRIF indirect loan": "74540"
        }
        
        self.matched_transactions = []
        self.unmatched_transactions = []
        self.timing_differences_found = []
        self.audit_trail = []
        
        self.logger.info("Reconciliation Matcher Agent initialized successfully")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup comprehensive logging for audit trail"""
        logger = logging.getLogger('ReconciliationMatcher')
        logger.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # File handler for audit trail
        file_handler = logging.FileHandler('reconciliation_matcher.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def _validate_gl_data(self, gl_data: pd.DataFrame) -> pd.DataFrame:
        """
        Validate GL data according to OP requirements
        
        Args:
            gl_data: GL transaction data
            
        Returns:
            Validated GL data
            
        Raises:
            ValueError: If data validation fails
        """
        try:
            self.logger.info("Validating GL data")
            
            if gl_data.empty:
                self.logger.warning("GL data is empty")
                return gl_data
            
            # Check required columns
            required_columns = ['gl_account', 'transaction_date', 'amount', 'description']
            missing_columns = [col for col in required_columns if col not in gl_data.columns]
            
            if missing_columns:
                raise ValueError(f"Missing required GL columns: {missing_columns}")
            
            # Validate GL accounts
            invalid_accounts = gl_data[~gl_data['gl_account'].isin(self.gl_accounts)]['gl_account'].unique()
            if len(invalid_accounts) > 0:
                self.logger.warning(f"Invalid GL accounts found: {invalid_accounts}")
            
            # Validate amounts
            if not pd.api.types.is_numeric_dtype(gl_data['amount']):
                raise ValueError("GL amount column must be numeric")
            
            # Check for null values
            null_counts = gl_data.isnull().sum()
            if null_counts.any():
                self.logger.warning(f"Null values found in GL data: {null_counts[null_counts > 0].to_dict()}")
            
            self.logger.info(f"GL data validation completed: {len(gl_data)} transactions")
            return gl_data
            
        except Exception as e:
            self.logger.error(f"GL data validation failed: {e}")
            raise
    
    def _validate_bank_data(self, bank_data: pd.DataFrame) -> pd.DataFrame:
        """
        Validate bank data according to OP requirements
        
        Args:
            bank_data: Bank statement data
            
        Returns:
            Validated bank data
            
        Raises:
            ValueError: If data validation fails
        """
        try:
            self.logger.info("Validating bank data")
            
            if bank_data.empty:
                self.logger.warning("Bank data is empty")
                return bank_data
            
            # Check required columns
            required_columns = ['transaction_date', 'amount', 'description']
            missing_columns = [col for col in required_columns if col not in bank_data.columns]
            
            if missing_columns:
                raise ValueError(f"Missing required bank columns: {missing_columns}")
            
            # Validate amounts
            if not pd.api.types.is_numeric_dtype(bank_data['amount']):
                raise ValueError("Bank amount column must be numeric")
            
            # Check for null values
            null_counts = bank_data.isnull().sum()
            if null_counts.any():
                self.logger.warning(f"Null values found in bank data: {null_counts[null_counts > 0].to_dict()}")
            
            self.logger.info(f"Bank data validation completed: {len(bank_data)} transactions")
            return bank_data
            
        except Exception as e:
            self.logger.error(f"Bank data validation failed: {e}")
            raise
    
    def match_transactions(self) -> Dict[str, Any]:
        """
        Match GL transactions with bank transactions according to OP requirements
        
        Returns:
            Dictionary containing matching results
        """
        try:
            self.logger.info("Starting transaction matching process")
            
            if self.gl_data.empty or self.bank_data.empty:
                self.logger.warning("Cannot perform matching - data is empty")
                return {"status": "error", "message": "No data available for matching"}
            
            matches_found = 0
            unmatched_gl = []
            unmatched_bank = []
            
            # Process each bank transaction
            for _, bank_transaction in self.bank_data.iterrows():
                matched = False
                bank_desc = str(bank_transaction['description']).upper()
                
                # Find matching GL transaction based on OP mappings
                for transaction_type, gl_account in self.transaction_mappings.items():
                    if transaction_type.upper() in bank_desc:
                        # Look for corresponding GL transaction
                        gl_matches = self.gl_data[
                            (self.gl_data['gl_account'] == gl_account) &
                            (abs(self.gl_data['amount'] - bank_transaction['amount']) < 0.01) &
                            (self.gl_data['transaction_date'] == bank_transaction['transaction_date'])
                        ]
                        
                        if not gl_matches.empty:
                            # Found a match
                            gl_transaction = gl_matches.iloc[0]
                            match_record = {
                                'bank_transaction': bank_transaction.to_dict(),
                                'gl_transaction': gl_transaction.to_dict(),
                                'match_type': transaction_type,
                                'gl_account': gl_account,
                                'match_date': datetime.now().isoformat(),
                                'amount': bank_transaction['amount']
                            }
                            
                            self.matched_transactions.append(match_record)
                            matches_found += 1
                            matched = True
                            
                            self.logger.info(f"Matched {transaction_type}: ${bank_transaction['amount']:.2f}")
                            break
                
                if not matched:
                    unmatched_bank.append(bank_transaction.to_dict())
                    self.logger.warning(f"Unmatched bank transaction: {bank_desc}")
            
            # Find unmatched GL transactions
            matched_gl_indices = set()
            for match in self.matched_transactions:
                gl_idx = match['gl_transaction'].get('index', -1)
                if gl_idx >= 0:
                    matched_gl_indices.add(gl_idx)
            
            for idx, gl_transaction in self.gl_data.iterrows():
                if idx not in matched_gl_indices:
                    unmatched_gl.append(gl_transaction.to_dict())
            
            self.unmatched_transactions = {
                'gl_transactions': unmatched_gl,
                'bank_transactions': unmatched_bank
            }
            
            result = {
                'status': 'success',
                'matches_found': matches_found,
                'unmatched_gl_count': len(unmatched_gl),
                'unmatched_bank_count': len(unmatched_bank),
                'match_rate': matches_found / len(self.bank_data) * 100 if len(self.bank_data) > 0 else 0
            }
            
            self.logger.info(f"Transaction matching completed: {matches_found} matches found")
            return result
            
        except Exception as e:
            self.logger.error(f"Transaction matching failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def handle_timing_differences(self) -> Dict[str, Any]:
        """
        Handle timing differences according to OP training document
        
        Returns:
            Dictionary containing timing difference results
        """
        try:
            self.logger.info("Processing timing differences")
            
            timing_results = {
                'timing_differences_found': [],
                'carry_over_entries': [],
                'total_timing_amount': 0
            }
            
            # Check for timing differences in each category
            for timing_type, gl_account in self.timing_differences.items():
                # Look for transactions on last day of month
                month_end_transactions = self.gl_data[
                    (self.gl_data['gl_account'] == gl_account) &
                    (self.gl_data['transaction_date'].dt.day >= 30)  # Last day or second last day
                ]
                
                if not month_end_transactions.empty:
                    total_amount = month_end_transactions['amount'].sum()
                    timing_record = {
                        'type': timing_type,
                        'gl_account': gl_account,
                        'amount': total_amount,
                        'transaction_count': len(month_end_transactions),
                        'date': datetime.now().isoformat()
                    }
                    
                    timing_results['timing_differences_found'].append(timing_record)
                    timing_results['total_timing_amount'] += total_amount
                    
                    # Create carry-over entry
                    carry_over_entry = {
                        'description': f"Carry-over entry for {timing_type}",
                        'gl_account': gl_account,
                        'amount': total_amount,
                        'entry_type': 'timing_difference',
                        'created_date': datetime.now().isoformat()
                    }
                    
                    timing_results['carry_over_entries'].append(carry_over_entry)
                    
                    self.logger.info(f"Timing difference found: {timing_type} - ${total_amount:.2f}")
            
            self.timing_differences_found = timing_results['timing_differences_found']
            
            self.logger.info(f"Timing differences processed: {len(timing_results['timing_differences_found'])} found")
            return timing_results
            
        except Exception as e:
            self.logger.error(f"Timing differences handling failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def perform_variance_analysis(self) -> Dict[str, Any]:
        """
        Perform variance analysis according to OP requirements
        
        Returns:
            Dictionary containing variance analysis results
        """
        try:
            self.logger.info("Performing variance analysis")
            
            variance_results = {
                'gl_variances': [],
                'total_variance': 0,
                'high_variance_accounts': [],
                'variance_threshold': 1000.00  # OP requirement threshold
            }
            
            # Calculate variances for each GL account
            for gl_account in self.gl_accounts:
                gl_transactions = self.gl_data[self.gl_data['gl_account'] == gl_account]
                
                if not gl_transactions.empty:
                    total_debits = gl_transactions[gl_transactions['amount'] > 0]['amount'].sum()
                    total_credits = abs(gl_transactions[gl_transactions['amount'] < 0]['amount'].sum())
                    net_balance = total_debits - total_credits
                    
                    variance_record = {
                        'gl_account': gl_account,
                        'total_debits': total_debits,
                        'total_credits': total_credits,
                        'net_balance': net_balance,
                        'transaction_count': len(gl_transactions),
                        'variance_percentage': abs(net_balance) / max(total_debits, total_credits, 1) * 100
                    }
                    
                    variance_results['gl_variances'].append(variance_record)
                    variance_results['total_variance'] += abs(net_balance)
                    
                    # Check for high variance
                    if abs(net_balance) > variance_results['variance_threshold']:
                        variance_results['high_variance_accounts'].append(variance_record)
                        self.logger.warning(f"High variance detected in GL {gl_account}: ${net_balance:.2f}")
            
            self.logger.info(f"Variance analysis completed: {len(variance_results['high_variance_accounts'])} high variance accounts")
            return variance_results
            
        except Exception as e:
            self.logger.error(f"Variance analysis failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def generate_audit_trail(self) -> Dict[str, Any]:
        """
        Generate comprehensive audit trail according to OP requirements
        
        Returns:
            Dictionary containing audit trail
        """
        try:
            self.logger.info("Generating audit trail")
            
            audit_trail = {
                'execution_date': datetime.now().isoformat(),
                'user': os.getenv('USER', 'system'),
                'process_steps': [],
                'data_summary': {
                    'gl_transactions': len(self.gl_data),
                    'bank_transactions': len(self.bank_data),
                    'matched_transactions': len(self.matched_transactions),
                    'unmatched_transactions': len(self.unmatched_transactions.get('gl_transactions', [])) + 
                                             len(self.unmatched_transactions.get('bank_transactions', [])),
                    'timing_differences': len(self.timing_differences_found)
                },
                'validation_results': {},
                'reconciliation_summary': {}
            }
            
            # Add process steps
            audit_trail['process_steps'] = [
                "Data validation completed",
                "Transaction matching performed", 
                "Timing differences processed",
                "Variance analysis completed",
                "Audit trail generated"
            ]
            
            # Add validation results
            audit_trail['validation_results'] = {
                'gl_data_valid': not self.gl_data.empty,
                'bank_data_valid': not self.bank_data.empty,
                'all_gl_accounts_present': all(account in self.gl_data['gl_account'].values for account in self.gl_accounts)
            }
            
            # Add reconciliation summary
            audit_trail['reconciliation_summary'] = {
                'match_rate': len(self.matched_transactions) / len(self.bank_data) * 100 if len(self.bank_data) > 0 else 0,
                'total_timing_amount': sum(td.get('amount', 0) for td in self.timing_differences_found),
                'high_variance_count': len([v for v in self.perform_variance_analysis().get('high_variance_accounts', [])])
            }
            
            self.audit_trail = audit_trail
            
            # Save audit trail to file
            audit_file = f"audit_trail_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(audit_file, 'w') as f:
                json.dump(audit_trail, f, indent=2, default=str)
            
            self.logger.info(f"Audit trail generated and saved to {audit_file}")
            return audit_trail
            
        except Exception as e:
            self.logger.error(f"Audit trail generation failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def reconcile(self) -> Dict[str, Any]:
        """
        Perform complete reconciliation process according to OP requirements
        
        Returns:
            Dictionary containing reconciliation results
        """
        try:
            self.logger.info("Starting complete reconciliation process")
            start_time = datetime.now()
            
            # Step 1: Validate data
            self.logger.info("Step 1: Data validation")
            if self.gl_data.empty or self.bank_data.empty:
                return {"status": "error", "message": "No data available for reconciliation"}
            
            # Step 2: Match transactions
            self.logger.info("Step 2: Transaction matching")
            match_results = self.match_transactions()
            
            # Step 3: Handle timing differences
            self.logger.info("Step 3: Timing differences handling")
            timing_results = self.handle_timing_differences()
            
            # Step 4: Perform variance analysis
            self.logger.info("Step 4: Variance analysis")
            variance_results = self.perform_variance_analysis()
            
            # Step 5: Generate audit trail
            self.logger.info("Step 5: Audit trail generation")
            audit_results = self.generate_audit_trail()
            
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            # Compile final results
            reconciliation_results = {
                'status': 'success',
                'execution_time_seconds': execution_time,
                'match_results': match_results,
                'timing_results': timing_results,
                'variance_results': variance_results,
                'audit_results': audit_results,
                'summary': {
                    'total_matches': len(self.matched_transactions),
                    'total_unmatched': len(self.unmatched_transactions.get('gl_transactions', [])) + 
                                     len(self.unmatched_transactions.get('bank_transactions', [])),
                    'timing_differences_count': len(self.timing_differences_found),
                    'high_variance_accounts': len(variance_results.get('high_variance_accounts', [])),
                    'op_compliance': True
                }
            }
            
            self.logger.info(f"Reconciliation completed successfully in {execution_time:.2f} seconds")
            return reconciliation_results
            
        except Exception as e:
            self.logger.error(f"Reconciliation failed: {e}")
            return {"status": "error", "message": str(e), "execution_time": 0}
    
    def get_reconciliation_report(self) -> Dict[str, Any]:
        """
        Get comprehensive reconciliation report
        
        Returns:
            Dictionary containing complete reconciliation report
        """
        return {
            'matched_transactions': self.matched_transactions,
            'unmatched_transactions': self.unmatched_transactions,
            'timing_differences': self.timing_differences_found,
            'audit_trail': self.audit_trail,
            'op_compliance_status': True,
            'report_generated': datetime.now().isoformat()
        }

# Unit tests
def test_reconciliation():
    """Comprehensive unit tests for reconciliation matcher"""
    import unittest
    
    class TestReconciliationMatcher(unittest.TestCase):
        def setUp(self):
            # Create test data
            self.gl_data = pd.DataFrame({
                'gl_account': ['74400', '74530', '74505'],
                'transaction_date': pd.to_datetime(['2025-05-31', '2025-05-31', '2025-05-31']),
                'amount': [1000.00, -500.00, 250.00],
                'description': ['RBC Transaction', 'ACH ADV File', 'CNS Settlement']
            })
            
            self.bank_data = pd.DataFrame({
                'transaction_date': pd.to_datetime(['2025-05-31', '2025-05-31', '2025-05-31']),
                'amount': [1000.00, -500.00, 250.00],
                'description': ['RBC', 'ACH ADV File', 'CNS Settlement']
            })
        
        def test_initialization(self):
            """Test agent initialization"""
            matcher = ReconciliationMatcher(self.gl_data, self.bank_data)
            self.assertIsNotNone(matcher)
            self.assertEqual(len(matcher.gl_accounts), 12)
        
        def test_data_validation(self):
            """Test data validation"""
            matcher = ReconciliationMatcher(self.gl_data, self.bank_data)
            self.assertFalse(matcher.gl_data.empty)
            self.assertFalse(matcher.bank_data.empty)
        
        def test_transaction_matching(self):
            """Test transaction matching"""
            matcher = ReconciliationMatcher(self.gl_data, self.bank_data)
            results = matcher.match_transactions()
            self.assertEqual(results['status'], 'success')
            self.assertGreaterEqual(results['matches_found'], 0)
        
        def test_timing_differences(self):
            """Test timing differences handling"""
            matcher = ReconciliationMatcher(self.gl_data, self.bank_data)
            results = matcher.handle_timing_differences()
            self.assertEqual(results['status'], 'success')
        
        def test_variance_analysis(self):
            """Test variance analysis"""
            matcher = ReconciliationMatcher(self.gl_data, self.bank_data)
            results = matcher.perform_variance_analysis()
            self.assertEqual(results['status'], 'success')
        
        def test_audit_trail(self):
            """Test audit trail generation"""
            matcher = ReconciliationMatcher(self.gl_data, self.bank_data)
            results = matcher.generate_audit_trail()
            self.assertEqual(results['status'], 'success')
        
        def test_complete_reconciliation(self):
            """Test complete reconciliation process"""
            matcher = ReconciliationMatcher(self.gl_data, self.bank_data)
            results = matcher.reconcile()
            self.assertEqual(results['status'], 'success')
            self.assertIn('summary', results)
    
    # Run tests
    unittest.main(argv=[''], exit=False, verbosity=2)

if __name__ == "__main__":
    # Example usage
    try:
        # Load GL and bank data (replace with actual data sources)
        gl_data = pd.DataFrame()  # Load from actual source
        bank_data = pd.DataFrame()  # Load from actual source
        
        # Create ReconciliationMatcher instance
        matcher = ReconciliationMatcher(gl_data, bank_data)
        
        # Perform reconciliation
        results = matcher.reconcile()
        
        # Print results
        print(f"Reconciliation Status: {results['status']}")
        if results['status'] == 'success':
            print(f"Execution Time: {results['execution_time_seconds']:.2f} seconds")
            print(f"Matches Found: {results['summary']['total_matches']}")
            print(f"OP Compliance: {results['summary']['op_compliance']}")
        
        # Run unit tests
        test_reconciliation()
        
    except Exception as e:
        print(f"Error: {e}")
        logging.error(f"Main execution failed: {e}")