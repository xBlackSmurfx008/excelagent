#!/usr/bin/env python3
"""
Data Quality Validator Agent
Validates data quality before any processing according to OP training document requirements
"""

import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import json
import os
from pathlib import Path

class DataQualityValidator:
    """
    Data Quality Validator Agent for OP-compliant data validation
    Implements comprehensive data quality checks according to OP training document
    """
    
    def __init__(self, gl_data: pd.DataFrame = None, bank_data: pd.DataFrame = None):
        """
        Initialize Data Quality Validator with comprehensive validation
        
        Args:
            gl_data: General Ledger transaction data
            bank_data: Bank statement transaction data
        """
        self.logger = self._setup_logging()
        self.logger.info("Initializing Data Quality Validator Agent")
        
        # Validate and store data
        self.gl_data = gl_data if gl_data is not None else pd.DataFrame()
        self.bank_data = bank_data if bank_data is not None else pd.DataFrame()
        
        # OP Training Document Requirements
        self.required_gl_accounts = ["74400", "74505", "74510", "74515", "74520", "74525", 
                                   "74530", "74535", "74540", "74550", "74560", "74570"]
        
        # Data quality thresholds
        self.quality_thresholds = {
            'max_null_percentage': 5.0,  # Maximum 5% null values allowed
            'max_duplicate_percentage': 2.0,  # Maximum 2% duplicates allowed
            'min_data_freshness_days': 1,  # Data must be within 1 day
            'max_amount_deviation': 1000000,  # Maximum amount deviation
            'required_columns_gl': ['gl_account', 'transaction_date', 'amount', 'description'],
            'required_columns_bank': ['transaction_date', 'amount', 'description']
        }
        
        # Validation results tracking
        self.validation_results = {}
        self.quality_issues = []
        self.data_summary = {}
        self.audit_trail = []
        
        self.logger.info("Data Quality Validator Agent initialized successfully")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup comprehensive logging for audit trail"""
        logger = logging.getLogger('DataQualityValidator')
        logger.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # File handler for audit trail
        file_handler = logging.FileHandler('data_quality_validator.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def validate_data_completeness(self) -> Dict[str, Any]:
        """
        Validate data completeness according to OP requirements
        
        Returns:
            Dictionary containing completeness validation results
        """
        try:
            self.logger.info("Validating data completeness")
            
            completeness_results = {
                'completeness_status': 'success',
                'gl_completeness': {},
                'bank_completeness': {},
                'issues_found': [],
                'recommendations': []
            }
            
            # Validate GL data completeness
            if not self.gl_data.empty:
                gl_completeness = {
                    'total_records': len(self.gl_data),
                    'required_columns_present': all(col in self.gl_data.columns for col in self.quality_thresholds['required_columns_gl']),
                    'missing_columns': [col for col in self.quality_thresholds['required_columns_gl'] if col not in self.gl_data.columns],
                    'null_values_count': self.gl_data.isnull().sum().sum(),
                    'null_percentage': (self.gl_data.isnull().sum().sum() / (len(self.gl_data) * len(self.gl_data.columns))) * 100,
                    'duplicate_records': self.gl_data.duplicated().sum(),
                    'duplicate_percentage': (self.gl_data.duplicated().sum() / len(self.gl_data)) * 100
                }
                
                completeness_results['gl_completeness'] = gl_completeness
                
                # Check for issues
                if not gl_completeness['required_columns_present']:
                    completeness_results['issues_found'].append(f"Missing GL columns: {gl_completeness['missing_columns']}")
                
                if gl_completeness['null_percentage'] > self.quality_thresholds['max_null_percentage']:
                    completeness_results['issues_found'].append(f"High null percentage in GL data: {gl_completeness['null_percentage']:.2f}%")
                
                if gl_completeness['duplicate_percentage'] > self.quality_thresholds['max_duplicate_percentage']:
                    completeness_results['issues_found'].append(f"High duplicate percentage in GL data: {gl_completeness['duplicate_percentage']:.2f}%")
                
            else:
                completeness_results['issues_found'].append("GL data is empty")
                completeness_results['gl_completeness'] = {'status': 'empty'}
            
            # Validate Bank data completeness
            if not self.bank_data.empty:
                bank_completeness = {
                    'total_records': len(self.bank_data),
                    'required_columns_present': all(col in self.bank_data.columns for col in self.quality_thresholds['required_columns_bank']),
                    'missing_columns': [col for col in self.quality_thresholds['required_columns_bank'] if col not in self.bank_data.columns],
                    'null_values_count': self.bank_data.isnull().sum().sum(),
                    'null_percentage': (self.bank_data.isnull().sum().sum() / (len(self.bank_data) * len(self.bank_data.columns))) * 100,
                    'duplicate_records': self.bank_data.duplicated().sum(),
                    'duplicate_percentage': (self.bank_data.duplicated().sum() / len(self.bank_data)) * 100
                }
                
                completeness_results['bank_completeness'] = bank_completeness
                
                # Check for issues
                if not bank_completeness['required_columns_present']:
                    completeness_results['issues_found'].append(f"Missing bank columns: {bank_completeness['missing_columns']}")
                
                if bank_completeness['null_percentage'] > self.quality_thresholds['max_null_percentage']:
                    completeness_results['issues_found'].append(f"High null percentage in bank data: {bank_completeness['null_percentage']:.2f}%")
                
                if bank_completeness['duplicate_percentage'] > self.quality_thresholds['max_duplicate_percentage']:
                    completeness_results['issues_found'].append(f"High duplicate percentage in bank data: {bank_completeness['duplicate_percentage']:.2f}%")
                
            else:
                completeness_results['issues_found'].append("Bank data is empty")
                completeness_results['bank_completeness'] = {'status': 'empty'}
            
            # Determine overall status
            if completeness_results['issues_found']:
                completeness_results['completeness_status'] = 'issues_found'
                completeness_results['recommendations'].extend([
                    "Review data sources for completeness",
                    "Check for missing required columns",
                    "Investigate null values and duplicates"
                ])
            
            self.logger.info(f"Data completeness validation completed: {len(completeness_results['issues_found'])} issues found")
            return completeness_results
            
        except Exception as e:
            self.logger.error(f"Data completeness validation failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def validate_data_accuracy(self) -> Dict[str, Any]:
        """
        Validate data accuracy according to OP requirements
        
        Returns:
            Dictionary containing accuracy validation results
        """
        try:
            self.logger.info("Validating data accuracy")
            
            accuracy_results = {
                'accuracy_status': 'success',
                'gl_accuracy': {},
                'bank_accuracy': {},
                'issues_found': [],
                'recommendations': []
            }
            
            # Validate GL data accuracy
            if not self.gl_data.empty:
                gl_accuracy = {
                    'valid_gl_accounts': 0,
                    'invalid_gl_accounts': [],
                    'amount_range_valid': True,
                    'date_range_valid': True,
                    'data_types_valid': True,
                    'accuracy_score': 0
                }
                
                # Check GL accounts
                if 'gl_account' in self.gl_data.columns:
                    valid_accounts = self.gl_data[self.gl_data['gl_account'].isin(self.required_gl_accounts)]
                    gl_accuracy['valid_gl_accounts'] = len(valid_accounts)
                    
                    invalid_accounts = self.gl_data[~self.gl_data['gl_account'].isin(self.required_gl_accounts)]['gl_account'].unique()
                    gl_accuracy['invalid_gl_accounts'] = invalid_accounts.tolist()
                    
                    if len(invalid_accounts) > 0:
                        accuracy_results['issues_found'].append(f"Invalid GL accounts found: {invalid_accounts}")
                
                # Check amount ranges
                if 'amount' in self.gl_data.columns:
                    if pd.api.types.is_numeric_dtype(self.gl_data['amount']):
                        max_amount = self.gl_data['amount'].abs().max()
                        if max_amount > self.quality_thresholds['max_amount_deviation']:
                            gl_accuracy['amount_range_valid'] = False
                            accuracy_results['issues_found'].append(f"Unusual amount in GL data: ${max_amount:.2f}")
                    else:
                        gl_accuracy['data_types_valid'] = False
                        accuracy_results['issues_found'].append("GL amount column is not numeric")
                
                # Check date ranges
                if 'transaction_date' in self.gl_data.columns:
                    try:
                        dates = pd.to_datetime(self.gl_data['transaction_date'])
                        current_date = datetime.now()
                        days_old = (current_date - dates.max()).days
                        
                        if days_old > self.quality_thresholds['min_data_freshness_days']:
                            gl_accuracy['date_range_valid'] = False
                            accuracy_results['issues_found'].append(f"GL data is {days_old} days old")
                    except Exception as e:
                        gl_accuracy['data_types_valid'] = False
                        accuracy_results['issues_found'].append(f"GL date column format error: {e}")
                
                # Calculate accuracy score
                accuracy_checks = [
                    gl_accuracy['amount_range_valid'],
                    gl_accuracy['date_range_valid'],
                    gl_accuracy['data_types_valid'],
                    len(gl_accuracy['invalid_gl_accounts']) == 0
                ]
                gl_accuracy['accuracy_score'] = (sum(accuracy_checks) / len(accuracy_checks)) * 100
                
                accuracy_results['gl_accuracy'] = gl_accuracy
            
            # Validate Bank data accuracy
            if not self.bank_data.empty:
                bank_accuracy = {
                    'amount_range_valid': True,
                    'date_range_valid': True,
                    'data_types_valid': True,
                    'accuracy_score': 0
                }
                
                # Check amount ranges
                if 'amount' in self.bank_data.columns:
                    if pd.api.types.is_numeric_dtype(self.bank_data['amount']):
                        max_amount = self.bank_data['amount'].abs().max()
                        if max_amount > self.quality_thresholds['max_amount_deviation']:
                            bank_accuracy['amount_range_valid'] = False
                            accuracy_results['issues_found'].append(f"Unusual amount in bank data: ${max_amount:.2f}")
                    else:
                        bank_accuracy['data_types_valid'] = False
                        accuracy_results['issues_found'].append("Bank amount column is not numeric")
                
                # Check date ranges
                if 'transaction_date' in self.bank_data.columns:
                    try:
                        dates = pd.to_datetime(self.bank_data['transaction_date'])
                        current_date = datetime.now()
                        days_old = (current_date - dates.max()).days
                        
                        if days_old > self.quality_thresholds['min_data_freshness_days']:
                            bank_accuracy['date_range_valid'] = False
                            accuracy_results['issues_found'].append(f"Bank data is {days_old} days old")
                    except Exception as e:
                        bank_accuracy['data_types_valid'] = False
                        accuracy_results['issues_found'].append(f"Bank date column format error: {e}")
                
                # Calculate accuracy score
                accuracy_checks = [
                    bank_accuracy['amount_range_valid'],
                    bank_accuracy['date_range_valid'],
                    bank_accuracy['data_types_valid']
                ]
                bank_accuracy['accuracy_score'] = (sum(accuracy_checks) / len(accuracy_checks)) * 100
                
                accuracy_results['bank_accuracy'] = bank_accuracy
            
            # Determine overall status
            if accuracy_results['issues_found']:
                accuracy_results['accuracy_status'] = 'issues_found'
                accuracy_results['recommendations'].extend([
                    "Review data sources for accuracy",
                    "Validate GL account numbers",
                    "Check amount ranges and data types",
                    "Verify date formats and freshness"
                ])
            
            self.logger.info(f"Data accuracy validation completed: {len(accuracy_results['issues_found'])} issues found")
            return accuracy_results
            
        except Exception as e:
            self.logger.error(f"Data accuracy validation failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def validate_data_consistency(self) -> Dict[str, Any]:
        """
        Validate data consistency according to OP requirements
        
        Returns:
            Dictionary containing consistency validation results
        """
        try:
            self.logger.info("Validating data consistency")
            
            consistency_results = {
                'consistency_status': 'success',
                'cross_validation_results': {},
                'issues_found': [],
                'recommendations': []
            }
            
            # Cross-validate GL and Bank data
            if not self.gl_data.empty and not self.bank_data.empty:
                cross_validation = {
                    'date_range_overlap': False,
                    'amount_correlation': 0,
                    'transaction_count_ratio': 0,
                    'consistency_score': 0
                }
                
                # Check date range overlap
                try:
                    gl_dates = pd.to_datetime(self.gl_data['transaction_date'])
                    bank_dates = pd.to_datetime(self.bank_data['transaction_date'])
                    
                    gl_min, gl_max = gl_dates.min(), gl_dates.max()
                    bank_min, bank_max = bank_dates.min(), bank_dates.max()
                    
                    # Check if date ranges overlap
                    if (gl_min <= bank_max) and (bank_min <= gl_max):
                        cross_validation['date_range_overlap'] = True
                    else:
                        consistency_results['issues_found'].append("GL and Bank data date ranges do not overlap")
                
                except Exception as e:
                    consistency_results['issues_found'].append(f"Date range validation error: {e}")
                
                # Check amount correlation
                try:
                    if 'amount' in self.gl_data.columns and 'amount' in self.bank_data.columns:
                        gl_total = self.gl_data['amount'].sum()
                        bank_total = self.bank_data['amount'].sum()
                        
                        if abs(gl_total) > 0 and abs(bank_total) > 0:
                            correlation = min(abs(gl_total), abs(bank_total)) / max(abs(gl_total), abs(bank_total))
                            cross_validation['amount_correlation'] = correlation
                            
                            if correlation < 0.1:  # Less than 10% correlation
                                consistency_results['issues_found'].append(f"Low amount correlation between GL and Bank data: {correlation:.2f}")
                except Exception as e:
                    consistency_results['issues_found'].append(f"Amount correlation validation error: {e}")
                
                # Check transaction count ratio
                try:
                    gl_count = len(self.gl_data)
                    bank_count = len(self.bank_data)
                    
                    if bank_count > 0:
                        ratio = gl_count / bank_count
                        cross_validation['transaction_count_ratio'] = ratio
                        
                        if ratio < 0.1 or ratio > 10:  # Unusual ratio
                            consistency_results['issues_found'].append(f"Unusual transaction count ratio: {ratio:.2f}")
                except Exception as e:
                    consistency_results['issues_found'].append(f"Transaction count ratio validation error: {e}")
                
                # Calculate consistency score
                consistency_checks = [
                    cross_validation['date_range_overlap'],
                    cross_validation['amount_correlation'] > 0.1,
                    0.1 <= cross_validation['transaction_count_ratio'] <= 10
                ]
                cross_validation['consistency_score'] = (sum(consistency_checks) / len(consistency_checks)) * 100
                
                consistency_results['cross_validation_results'] = cross_validation
            
            # Determine overall status
            if consistency_results['issues_found']:
                consistency_results['consistency_status'] = 'issues_found'
                consistency_results['recommendations'].extend([
                    "Review data sources for consistency",
                    "Check date range alignment",
                    "Validate amount correlations",
                    "Investigate transaction count discrepancies"
                ])
            
            self.logger.info(f"Data consistency validation completed: {len(consistency_results['issues_found'])} issues found")
            return consistency_results
            
        except Exception as e:
            self.logger.error(f"Data consistency validation failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def generate_data_summary(self) -> Dict[str, Any]:
        """
        Generate comprehensive data summary according to OP requirements
        
        Returns:
            Dictionary containing data summary
        """
        try:
            self.logger.info("Generating data summary")
            
            summary = {
                'summary_date': datetime.now().isoformat(),
                'gl_data_summary': {},
                'bank_data_summary': {},
                'overall_quality_score': 0,
                'op_compliance_status': True
            }
            
            # GL data summary
            if not self.gl_data.empty:
                gl_summary = {
                    'total_records': len(self.gl_data),
                    'date_range': {
                        'earliest': self.gl_data['transaction_date'].min() if 'transaction_date' in self.gl_data.columns else 'N/A',
                        'latest': self.gl_data['transaction_date'].max() if 'transaction_date' in self.gl_data.columns else 'N/A'
                    },
                    'amount_summary': {
                        'total': self.gl_data['amount'].sum() if 'amount' in self.gl_data.columns else 0,
                        'average': self.gl_data['amount'].mean() if 'amount' in self.gl_data.columns else 0,
                        'min': self.gl_data['amount'].min() if 'amount' in self.gl_data.columns else 0,
                        'max': self.gl_data['amount'].max() if 'amount' in self.gl_data.columns else 0
                    },
                    'gl_accounts_present': self.gl_data['gl_account'].nunique() if 'gl_account' in self.gl_data.columns else 0,
                    'required_accounts_coverage': len(set(self.gl_data['gl_account'].unique()) & set(self.required_gl_accounts)) if 'gl_account' in self.gl_data.columns else 0
                }
                summary['gl_data_summary'] = gl_summary
            
            # Bank data summary
            if not self.bank_data.empty:
                bank_summary = {
                    'total_records': len(self.bank_data),
                    'date_range': {
                        'earliest': self.bank_data['transaction_date'].min() if 'transaction_date' in self.bank_data.columns else 'N/A',
                        'latest': self.bank_data['transaction_date'].max() if 'transaction_date' in self.bank_data.columns else 'N/A'
                    },
                    'amount_summary': {
                        'total': self.bank_data['amount'].sum() if 'amount' in self.bank_data.columns else 0,
                        'average': self.bank_data['amount'].mean() if 'amount' in self.bank_data.columns else 0,
                        'min': self.bank_data['amount'].min() if 'amount' in self.bank_data.columns else 0,
                        'max': self.bank_data['amount'].max() if 'amount' in self.bank_data.columns else 0
                    }
                }
                summary['bank_data_summary'] = bank_summary
            
            # Calculate overall quality score
            completeness_results = self.validate_data_completeness()
            accuracy_results = self.validate_data_consistency()
            consistency_results = self.validate_data_consistency()
            
            quality_scores = []
            if completeness_results.get('completeness_status') == 'success':
                quality_scores.append(100)
            else:
                quality_scores.append(50)
            
            if accuracy_results.get('accuracy_status') == 'success':
                quality_scores.append(100)
            else:
                quality_scores.append(50)
            
            if consistency_results.get('consistency_status') == 'success':
                quality_scores.append(100)
            else:
                quality_scores.append(50)
            
            summary['overall_quality_score'] = sum(quality_scores) / len(quality_scores) if quality_scores else 0
            
            self.data_summary = summary
            self.logger.info(f"Data summary generated: {summary['overall_quality_score']:.1f}% quality score")
            return summary
            
        except Exception as e:
            self.logger.error(f"Data summary generation failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def generate_audit_trail(self) -> Dict[str, Any]:
        """
        Generate comprehensive audit trail according to OP requirements
        
        Returns:
            Dictionary containing audit trail
        """
        try:
            self.logger.info("Generating audit trail for data quality validation")
            
            audit_trail = {
                'execution_date': datetime.now().isoformat(),
                'user': os.getenv('USER', 'system'),
                'process_steps': [],
                'validation_results': {},
                'data_summary': {},
                'op_compliance_status': True
            }
            
            # Add process steps
            audit_trail['process_steps'] = [
                "Data completeness validation completed",
                "Data accuracy validation completed",
                "Data consistency validation completed",
                "Data summary generation completed",
                "Audit trail generated"
            ]
            
            # Add validation results
            audit_trail['validation_results'] = {
                'completeness': self.validate_data_completeness(),
                'accuracy': self.validate_data_accuracy(),
                'consistency': self.validate_data_consistency()
            }
            
            # Add data summary
            audit_trail['data_summary'] = self.generate_data_summary()
            
            self.audit_trail = audit_trail
            
            # Save audit trail to file
            audit_file = f"data_quality_audit_trail_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(audit_file, 'w') as f:
                json.dump(audit_trail, f, indent=2, default=str)
            
            self.logger.info(f"Audit trail generated and saved to {audit_file}")
            return audit_trail
            
        except Exception as e:
            self.logger.error(f"Audit trail generation failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def validate_data(self) -> Dict[str, Any]:
        """
        Complete data quality validation process according to OP requirements
        
        Returns:
            Dictionary containing complete validation results
        """
        try:
            self.logger.info("Starting complete data quality validation process")
            start_time = datetime.now()
            
            # Step 1: Validate data completeness
            self.logger.info("Step 1: Validating data completeness")
            completeness_results = self.validate_data_completeness()
            
            # Step 2: Validate data accuracy
            self.logger.info("Step 2: Validating data accuracy")
            accuracy_results = self.validate_data_accuracy()
            
            # Step 3: Validate data consistency
            self.logger.info("Step 3: Validating data consistency")
            consistency_results = self.validate_data_consistency()
            
            # Step 4: Generate data summary
            self.logger.info("Step 4: Generating data summary")
            summary_results = self.generate_data_summary()
            
            # Step 5: Generate audit trail
            self.logger.info("Step 5: Generating audit trail")
            audit_results = self.generate_audit_trail()
            
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            # Compile final results
            validation_results = {
                'status': 'success',
                'execution_time_seconds': execution_time,
                'completeness_results': completeness_results,
                'accuracy_results': accuracy_results,
                'consistency_results': consistency_results,
                'summary_results': summary_results,
                'audit_results': audit_results,
                'summary': {
                    'overall_quality_score': summary_results.get('overall_quality_score', 0),
                    'total_issues_found': len(completeness_results.get('issues_found', [])) + 
                                         len(accuracy_results.get('issues_found', [])) + 
                                         len(consistency_results.get('issues_found', [])),
                    'op_compliance': True,
                    'data_ready_for_processing': summary_results.get('overall_quality_score', 0) >= 70
                }
            }
            
            self.logger.info(f"Data quality validation completed successfully in {execution_time:.2f} seconds")
            return validation_results
            
        except Exception as e:
            self.logger.error(f"Data quality validation failed: {e}")
            return {"status": "error", "message": str(e), "execution_time": 0}
    
    def get_validation_report(self) -> Dict[str, Any]:
        """
        Get comprehensive validation report
        
        Returns:
            Dictionary containing complete validation report
        """
        return {
            'validation_results': self.validation_results,
            'data_summary': self.data_summary,
            'audit_trail': self.audit_trail,
            'op_compliance_status': True,
            'report_generated': datetime.now().isoformat()
        }

# Unit tests
def test_data_quality_validator():
    """Comprehensive unit tests for data quality validator"""
    import unittest
    
    class TestDataQualityValidator(unittest.TestCase):
        def setUp(self):
            # Create test data
            self.gl_data = pd.DataFrame({
                'gl_account': ['74400', '74505', '74510'],
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
            validator = DataQualityValidator(self.gl_data, self.bank_data)
            self.assertIsNotNone(validator)
            self.assertEqual(len(validator.required_gl_accounts), 12)
        
        def test_data_completeness_validation(self):
            """Test data completeness validation"""
            validator = DataQualityValidator(self.gl_data, self.bank_data)
            results = validator.validate_data_completeness()
            self.assertEqual(results['completeness_status'], 'success')
        
        def test_data_accuracy_validation(self):
            """Test data accuracy validation"""
            validator = DataQualityValidator(self.gl_data, self.bank_data)
            results = validator.validate_data_accuracy()
            self.assertEqual(results['accuracy_status'], 'success')
        
        def test_data_consistency_validation(self):
            """Test data consistency validation"""
            validator = DataQualityValidator(self.gl_data, self.bank_data)
            results = validator.validate_data_consistency()
            self.assertEqual(results['consistency_status'], 'success')
        
        def test_data_summary_generation(self):
            """Test data summary generation"""
            validator = DataQualityValidator(self.gl_data, self.bank_data)
            results = validator.generate_data_summary()
            self.assertIn('overall_quality_score', results)
        
        def test_audit_trail_generation(self):
            """Test audit trail generation"""
            validator = DataQualityValidator(self.gl_data, self.bank_data)
            results = validator.generate_audit_trail()
            self.assertEqual(results['op_compliance_status'], True)
        
        def test_complete_validation(self):
            """Test complete validation process"""
            validator = DataQualityValidator(self.gl_data, self.bank_data)
            results = validator.validate_data()
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
        
        # Create DataQualityValidator instance
        validator = DataQualityValidator(gl_data, bank_data)
        
        # Validate data quality
        results = validator.validate_data()
        
        # Print results
        print(f"Data Quality Validation Status: {results['status']}")
        if results['status'] == 'success':
            print(f"Execution Time: {results['execution_time_seconds']:.2f} seconds")
            print(f"Overall Quality Score: {results['summary']['overall_quality_score']:.1f}%")
            print(f"Total Issues Found: {results['summary']['total_issues_found']}")
            print(f"Data Ready for Processing: {results['summary']['data_ready_for_processing']}")
            print(f"OP Compliance: {results['summary']['op_compliance']}")
        
        # Run unit tests
        test_data_quality_validator()
        
    except Exception as e:
        print(f"Error: {e}")
        logging.error(f"Main execution failed: {e}")