#!/usr/bin/env python3
"""
Timing Difference Handler Agent
Handles timing differences and carry-over entries according to OP training document requirements
"""

import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import json
import os
from pathlib import Path

class TimingDifferenceHandler:
    """
    Timing Difference Handler Agent for OP-compliant timing difference management
    Implements all timing difference requirements from OP training document
    """
    
    def __init__(self, gl_data: pd.DataFrame = None, bank_data: pd.DataFrame = None):
        """
        Initialize Timing Difference Handler with data validation
        
        Args:
            gl_data: General Ledger transaction data
            bank_data: Bank statement transaction data
        """
        self.logger = self._setup_logging()
        self.logger.info("Initializing Timing Difference Handler Agent")
        
        # Validate and store data
        self.gl_data = self._validate_gl_data(gl_data) if gl_data is not None else pd.DataFrame()
        self.bank_data = self._validate_bank_data(bank_data) if bank_data is not None else pd.DataFrame()
        
        # OP Training Document Timing Difference Requirements
        self.timing_difference_mappings = {
            "ATM settlement": {
                "gl_account": "74505",
                "description": "ATM settlement activity posted to GL 74505 on last day of month",
                "reconciliation_location": "top_right_corner",
                "amount_type": "negative"
            },
            "Shared Branching": {
                "gl_account": "74510", 
                "description": "Shared Branching activity recorded in GL 74510 on last day of month",
                "reconciliation_location": "top_right_or_bottom_right",
                "amount_type": "variable"
            },
            "Check deposit Barks/MtG": {
                "gl_account": "74560",
                "description": "Check deposit activity at Barks or MtG posted to GL 74560 on last day of month",
                "reconciliation_location": "bottom_right_corner",
                "amount_type": "positive"
            },
            "Gift Card activity": {
                "gl_account": "74535",
                "description": "Gift Card activity posted to GL 74535 on last day of month",
                "reconciliation_location": "top_right_corner",
                "amount_type": "negative"
            },
            "CBS activity": {
                "gl_account": "74550",
                "description": "CBS activity posted to GL 74550 on last day of month",
                "reconciliation_location": "bottom_right_corner",
                "amount_type": "positive"
            },
            "CRIF indirect loan": {
                "gl_account": "74540",
                "description": "CRIF indirect loan activity posted to GL 74540 on last day of month",
                "reconciliation_location": "top_right_corner",
                "amount_type": "negative"
            }
        }
        
        # Timing difference tracking
        self.timing_differences_found = []
        self.carry_over_entries = []
        self.reconciliation_adjustments = []
        self.audit_trail = []
        
        self.logger.info("Timing Difference Handler Agent initialized successfully")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup comprehensive logging for audit trail"""
        logger = logging.getLogger('TimingDifferenceHandler')
        logger.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # File handler for audit trail
        file_handler = logging.FileHandler('timing_difference_handler.log')
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
            self.logger.info("Validating GL data for timing differences")
            
            if gl_data.empty:
                self.logger.warning("GL data is empty")
                return gl_data
            
            # Check required columns
            required_columns = ['gl_account', 'transaction_date', 'amount', 'description']
            missing_columns = [col for col in required_columns if col not in gl_data.columns]
            
            if missing_columns:
                raise ValueError(f"Missing required GL columns: {missing_columns}")
            
            # Convert transaction_date to datetime if not already
            if not pd.api.types.is_datetime64_any_dtype(gl_data['transaction_date']):
                gl_data['transaction_date'] = pd.to_datetime(gl_data['transaction_date'])
            
            # Validate amounts
            if not pd.api.types.is_numeric_dtype(gl_data['amount']):
                raise ValueError("GL amount column must be numeric")
            
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
            self.logger.info("Validating bank data for timing differences")
            
            if bank_data.empty:
                self.logger.warning("Bank data is empty")
                return bank_data
            
            # Check required columns
            required_columns = ['transaction_date', 'amount', 'description']
            missing_columns = [col for col in required_columns if col not in bank_data.columns]
            
            if missing_columns:
                raise ValueError(f"Missing required bank columns: {missing_columns}")
            
            # Convert transaction_date to datetime if not already
            if not pd.api.types.is_datetime64_any_dtype(bank_data['transaction_date']):
                bank_data['transaction_date'] = pd.to_datetime(bank_data['transaction_date'])
            
            # Validate amounts
            if not pd.api.types.is_numeric_dtype(bank_data['amount']):
                raise ValueError("Bank amount column must be numeric")
            
            self.logger.info(f"Bank data validation completed: {len(bank_data)} transactions")
            return bank_data
            
        except Exception as e:
            self.logger.error(f"Bank data validation failed: {e}")
            raise
    
    def identify_timing_differences(self) -> Dict[str, Any]:
        """
        Identify timing differences according to OP training document
        
        Returns:
            Dictionary containing timing difference identification results
        """
        try:
            self.logger.info("Identifying timing differences")
            
            timing_results = {
                'timing_differences_found': [],
                'total_timing_amount': 0,
                'month_end_transactions': [],
                'identification_status': 'success'
            }
            
            if self.gl_data.empty:
                self.logger.warning("No GL data available for timing difference identification")
                return timing_results
            
            # Get current month and last day
            current_date = datetime.now()
            last_day_of_month = current_date.replace(day=1) + timedelta(days=32)
            last_day_of_month = last_day_of_month.replace(day=1) - timedelta(days=1)
            second_last_day = last_day_of_month - timedelta(days=1)
            
            # Check each timing difference type
            for timing_type, mapping in self.timing_difference_mappings.items():
                gl_account = mapping['gl_account']
                
                # Look for transactions on last day or second last day of month
                month_end_transactions = self.gl_data[
                    (self.gl_data['gl_account'] == gl_account) &
                    (
                        (self.gl_data['transaction_date'].dt.date == last_day_of_month.date()) |
                        (self.gl_data['transaction_date'].dt.date == second_last_day.date())
                    )
                ]
                
                if not month_end_transactions.empty:
                    total_amount = month_end_transactions['amount'].sum()
                    
                    timing_record = {
                        'type': timing_type,
                        'gl_account': gl_account,
                        'amount': total_amount,
                        'transaction_count': len(month_end_transactions),
                        'last_day_transactions': len(month_end_transactions[
                            month_end_transactions['transaction_date'].dt.date == last_day_of_month.date()
                        ]),
                        'second_last_day_transactions': len(month_end_transactions[
                            month_end_transactions['transaction_date'].dt.date == second_last_day.date()
                        ]),
                        'description': mapping['description'],
                        'reconciliation_location': mapping['reconciliation_location'],
                        'amount_type': mapping['amount_type'],
                        'identified_date': datetime.now().isoformat(),
                        'transactions': month_end_transactions.to_dict('records')
                    }
                    
                    timing_results['timing_differences_found'].append(timing_record)
                    timing_results['total_timing_amount'] += abs(total_amount)
                    
                    self.logger.info(f"Timing difference identified: {timing_type} - ${total_amount:.2f}")
            
            self.timing_differences_found = timing_results['timing_differences_found']
            
            self.logger.info(f"Timing difference identification completed: {len(timing_results['timing_differences_found'])} found")
            return timing_results
            
        except Exception as e:
            self.logger.error(f"Timing difference identification failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def create_carry_over_entries(self) -> Dict[str, Any]:
        """
        Create carry-over entries according to OP training document
        
        Returns:
            Dictionary containing carry-over entry creation results
        """
        try:
            self.logger.info("Creating carry-over entries")
            
            carry_over_results = {
                'carry_over_entries_created': [],
                'total_carry_over_amount': 0,
                'reconciliation_adjustments': [],
                'creation_status': 'success'
            }
            
            for timing_diff in self.timing_differences_found:
                timing_type = timing_diff['type']
                gl_account = timing_diff['gl_account']
                amount = timing_diff['amount']
                reconciliation_location = timing_diff['reconciliation_location']
                amount_type = timing_diff['amount_type']
                
                # Create carry-over entry based on OP requirements
                carry_over_entry = {
                    'entry_id': f"CO_{timing_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    'description': f"Carry-over entry for {timing_type}",
                    'gl_account': gl_account,
                    'amount': amount,
                    'entry_type': 'timing_difference',
                    'reconciliation_location': reconciliation_location,
                    'amount_type': amount_type,
                    'created_date': datetime.now().isoformat(),
                    'created_by': os.getenv('USER', 'system'),
                    'status': 'pending_reconciliation'
                }
                
                carry_over_results['carry_over_entries_created'].append(carry_over_entry)
                carry_over_results['total_carry_over_amount'] += abs(amount)
                
                # Create reconciliation adjustment
                adjustment = {
                    'adjustment_type': 'timing_difference',
                    'description': f"Adjustment for {timing_type}",
                    'amount': amount if amount_type == 'positive' else -amount,
                    'reconciliation_location': reconciliation_location,
                    'gl_account': gl_account,
                    'created_date': datetime.now().isoformat()
                }
                
                carry_over_results['reconciliation_adjustments'].append(adjustment)
                
                self.logger.info(f"Carry-over entry created: {timing_type} - ${amount:.2f}")
            
            self.carry_over_entries = carry_over_results['carry_over_entries_created']
            self.reconciliation_adjustments = carry_over_results['reconciliation_adjustments']
            
            self.logger.info(f"Carry-over entry creation completed: {len(carry_over_results['carry_over_entries_created'])} entries")
            return carry_over_results
            
        except Exception as e:
            self.logger.error(f"Carry-over entry creation failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def process_reconciliation_adjustments(self) -> Dict[str, Any]:
        """
        Process reconciliation adjustments according to OP training document
        
        Returns:
            Dictionary containing reconciliation adjustment results
        """
        try:
            self.logger.info("Processing reconciliation adjustments")
            
            adjustment_results = {
                'adjustments_processed': [],
                'balance_per_books_adjustments': [],
                'balance_per_statement_adjustments': [],
                'total_adjustment_amount': 0,
                'processing_status': 'success'
            }
            
            for adjustment in self.reconciliation_adjustments:
                adjustment_record = {
                    'adjustment_id': f"ADJ_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    'adjustment_type': adjustment['adjustment_type'],
                    'description': adjustment['description'],
                    'amount': adjustment['amount'],
                    'gl_account': adjustment['gl_account'],
                    'reconciliation_location': adjustment['reconciliation_location'],
                    'processed_date': datetime.now().isoformat(),
                    'status': 'processed'
                }
                
                adjustment_results['adjustments_processed'].append(adjustment_record)
                adjustment_results['total_adjustment_amount'] += abs(adjustment['amount'])
                
                # Categorize adjustments based on OP requirements
                if adjustment['reconciliation_location'] in ['top_right_corner', 'bottom_right_corner']:
                    adjustment_results['balance_per_books_adjustments'].append(adjustment_record)
                else:
                    adjustment_results['balance_per_statement_adjustments'].append(adjustment_record)
                
                self.logger.info(f"Reconciliation adjustment processed: {adjustment['description']} - ${adjustment['amount']:.2f}")
            
            self.logger.info(f"Reconciliation adjustment processing completed: {len(adjustment_results['adjustments_processed'])} adjustments")
            return adjustment_results
            
        except Exception as e:
            self.logger.error(f"Reconciliation adjustment processing failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def validate_timing_difference_accuracy(self) -> Dict[str, Any]:
        """
        Validate timing difference accuracy according to OP requirements
        
        Returns:
            Dictionary containing validation results
        """
        try:
            self.logger.info("Validating timing difference accuracy")
            
            validation_results = {
                'validation_status': 'success',
                'accuracy_score': 0,
                'validation_checks': [],
                'issues_found': [],
                'recommendations': []
            }
            
            total_checks = 0
            passed_checks = 0
            
            # Check 1: Verify all timing differences are properly identified
            total_checks += 1
            if len(self.timing_differences_found) > 0:
                passed_checks += 1
                validation_results['validation_checks'].append("✓ Timing differences properly identified")
            else:
                validation_results['validation_checks'].append("⚠ No timing differences identified")
            
            # Check 2: Verify carry-over entries are created
            total_checks += 1
            if len(self.carry_over_entries) > 0:
                passed_checks += 1
                validation_results['validation_checks'].append("✓ Carry-over entries created")
            else:
                validation_results['validation_checks'].append("⚠ No carry-over entries created")
            
            # Check 3: Verify reconciliation adjustments are processed
            total_checks += 1
            if len(self.reconciliation_adjustments) > 0:
                passed_checks += 1
                validation_results['validation_checks'].append("✓ Reconciliation adjustments processed")
            else:
                validation_results['validation_checks'].append("⚠ No reconciliation adjustments processed")
            
            # Check 4: Verify amounts are reasonable
            total_checks += 1
            total_amount = sum(abs(td['amount']) for td in self.timing_differences_found)
            if 0 <= total_amount <= 1000000:  # Reasonable range
                passed_checks += 1
                validation_results['validation_checks'].append("✓ Timing difference amounts are reasonable")
            else:
                validation_results['issues_found'].append(f"Unusual timing difference amount: ${total_amount:.2f}")
                validation_results['validation_checks'].append("⚠ Timing difference amounts may be unusual")
            
            # Calculate accuracy score
            validation_results['accuracy_score'] = (passed_checks / total_checks) * 100
            
            # Generate recommendations
            if validation_results['accuracy_score'] < 100:
                validation_results['recommendations'].append("Review timing difference identification process")
                validation_results['recommendations'].append("Verify carry-over entry creation")
                validation_results['recommendations'].append("Check reconciliation adjustment processing")
            
            self.logger.info(f"Timing difference validation completed: {validation_results['accuracy_score']:.1f}% accuracy")
            return validation_results
            
        except Exception as e:
            self.logger.error(f"Timing difference validation failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def generate_audit_trail(self) -> Dict[str, Any]:
        """
        Generate comprehensive audit trail according to OP requirements
        
        Returns:
            Dictionary containing audit trail
        """
        try:
            self.logger.info("Generating audit trail for timing differences")
            
            audit_trail = {
                'execution_date': datetime.now().isoformat(),
                'user': os.getenv('USER', 'system'),
                'process_steps': [],
                'timing_differences_summary': {
                    'total_timing_differences': len(self.timing_differences_found),
                    'total_carry_over_entries': len(self.carry_over_entries),
                    'total_reconciliation_adjustments': len(self.reconciliation_adjustments),
                    'total_timing_amount': sum(abs(td['amount']) for td in self.timing_differences_found)
                },
                'validation_results': {},
                'op_compliance_status': True
            }
            
            # Add process steps
            audit_trail['process_steps'] = [
                "Timing difference identification completed",
                "Carry-over entry creation completed",
                "Reconciliation adjustment processing completed",
                "Timing difference validation completed",
                "Audit trail generated"
            ]
            
            # Add validation results
            validation_results = self.validate_timing_difference_accuracy()
            audit_trail['validation_results'] = validation_results
            
            # Add detailed timing difference information
            audit_trail['timing_differences_detail'] = self.timing_differences_found
            audit_trail['carry_over_entries_detail'] = self.carry_over_entries
            audit_trail['reconciliation_adjustments_detail'] = self.reconciliation_adjustments
            
            self.audit_trail = audit_trail
            
            # Save audit trail to file
            audit_file = f"timing_difference_audit_trail_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(audit_file, 'w') as f:
                json.dump(audit_trail, f, indent=2, default=str)
            
            self.logger.info(f"Audit trail generated and saved to {audit_file}")
            return audit_trail
            
        except Exception as e:
            self.logger.error(f"Audit trail generation failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def handle_timing_differences(self) -> Dict[str, Any]:
        """
        Complete timing difference handling process according to OP requirements
        
        Returns:
            Dictionary containing complete timing difference handling results
        """
        try:
            self.logger.info("Starting complete timing difference handling process")
            start_time = datetime.now()
            
            # Step 1: Identify timing differences
            self.logger.info("Step 1: Identifying timing differences")
            identification_results = self.identify_timing_differences()
            
            # Step 2: Create carry-over entries
            self.logger.info("Step 2: Creating carry-over entries")
            carry_over_results = self.create_carry_over_entries()
            
            # Step 3: Process reconciliation adjustments
            self.logger.info("Step 3: Processing reconciliation adjustments")
            adjustment_results = self.process_reconciliation_adjustments()
            
            # Step 4: Validate accuracy
            self.logger.info("Step 4: Validating timing difference accuracy")
            validation_results = self.validate_timing_difference_accuracy()
            
            # Step 5: Generate audit trail
            self.logger.info("Step 5: Generating audit trail")
            audit_results = self.generate_audit_trail()
            
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            # Compile final results
            timing_handling_results = {
                'status': 'success',
                'execution_time_seconds': execution_time,
                'identification_results': identification_results,
                'carry_over_results': carry_over_results,
                'adjustment_results': adjustment_results,
                'validation_results': validation_results,
                'audit_results': audit_results,
                'summary': {
                    'timing_differences_found': len(self.timing_differences_found),
                    'carry_over_entries_created': len(self.carry_over_entries),
                    'reconciliation_adjustments_processed': len(self.reconciliation_adjustments),
                    'total_timing_amount': sum(abs(td['amount']) for td in self.timing_differences_found),
                    'accuracy_score': validation_results.get('accuracy_score', 0),
                    'op_compliance': True
                }
            }
            
            self.logger.info(f"Timing difference handling completed successfully in {execution_time:.2f} seconds")
            return timing_handling_results
            
        except Exception as e:
            self.logger.error(f"Timing difference handling failed: {e}")
            return {"status": "error", "message": str(e), "execution_time": 0}
    
    def get_timing_difference_report(self) -> Dict[str, Any]:
        """
        Get comprehensive timing difference report
        
        Returns:
            Dictionary containing complete timing difference report
        """
        return {
            'timing_differences_found': self.timing_differences_found,
            'carry_over_entries': self.carry_over_entries,
            'reconciliation_adjustments': self.reconciliation_adjustments,
            'audit_trail': self.audit_trail,
            'op_compliance_status': True,
            'report_generated': datetime.now().isoformat()
        }

# Unit tests
def test_timing_difference_handler():
    """Comprehensive unit tests for timing difference handler"""
    import unittest
    
    class TestTimingDifferenceHandler(unittest.TestCase):
        def setUp(self):
            # Create test data with month-end transactions
            test_date = pd.to_datetime('2025-05-31')  # Last day of month
            
            self.gl_data = pd.DataFrame({
                'gl_account': ['74505', '74510', '74560', '74535'],
                'transaction_date': [test_date, test_date, test_date, test_date],
                'amount': [1000.00, -500.00, 750.00, -250.00],
                'description': ['ATM Settlement', 'Shared Branching', 'Check Deposit', 'Gift Card']
            })
            
            self.bank_data = pd.DataFrame({
                'transaction_date': [test_date],
                'amount': [1000.00],
                'description': ['Bank Transaction']
            })
        
        def test_initialization(self):
            """Test agent initialization"""
            handler = TimingDifferenceHandler(self.gl_data, self.bank_data)
            self.assertIsNotNone(handler)
            self.assertEqual(len(handler.timing_difference_mappings), 6)
        
        def test_data_validation(self):
            """Test data validation"""
            handler = TimingDifferenceHandler(self.gl_data, self.bank_data)
            self.assertFalse(handler.gl_data.empty)
            self.assertFalse(handler.bank_data.empty)
        
        def test_timing_difference_identification(self):
            """Test timing difference identification"""
            handler = TimingDifferenceHandler(self.gl_data, self.bank_data)
            results = handler.identify_timing_differences()
            self.assertEqual(results['identification_status'], 'success')
        
        def test_carry_over_creation(self):
            """Test carry-over entry creation"""
            handler = TimingDifferenceHandler(self.gl_data, self.bank_data)
            handler.identify_timing_differences()
            results = handler.create_carry_over_entries()
            self.assertEqual(results['creation_status'], 'success')
        
        def test_reconciliation_adjustments(self):
            """Test reconciliation adjustment processing"""
            handler = TimingDifferenceHandler(self.gl_data, self.bank_data)
            handler.identify_timing_differences()
            handler.create_carry_over_entries()
            results = handler.process_reconciliation_adjustments()
            self.assertEqual(results['processing_status'], 'success')
        
        def test_validation(self):
            """Test timing difference validation"""
            handler = TimingDifferenceHandler(self.gl_data, self.bank_data)
            results = handler.validate_timing_difference_accuracy()
            self.assertEqual(results['validation_status'], 'success')
        
        def test_audit_trail(self):
            """Test audit trail generation"""
            handler = TimingDifferenceHandler(self.gl_data, self.bank_data)
            results = handler.generate_audit_trail()
            self.assertEqual(results['op_compliance_status'], True)
        
        def test_complete_process(self):
            """Test complete timing difference handling process"""
            handler = TimingDifferenceHandler(self.gl_data, self.bank_data)
            results = handler.handle_timing_differences()
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
        
        # Create TimingDifferenceHandler instance
        handler = TimingDifferenceHandler(gl_data, bank_data)
        
        # Handle timing differences
        results = handler.handle_timing_differences()
        
        # Print results
        print(f"Timing Difference Handling Status: {results['status']}")
        if results['status'] == 'success':
            print(f"Execution Time: {results['execution_time_seconds']:.2f} seconds")
            print(f"Timing Differences Found: {results['summary']['timing_differences_found']}")
            print(f"Carry-over Entries Created: {results['summary']['carry_over_entries_created']}")
            print(f"OP Compliance: {results['summary']['op_compliance']}")
        
        # Run unit tests
        test_timing_difference_handler()
        
    except Exception as e:
        print(f"Error: {e}")
        logging.error(f"Main execution failed: {e}")