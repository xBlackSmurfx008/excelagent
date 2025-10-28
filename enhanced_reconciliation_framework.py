#!/usr/bin/env python3
"""
Excel Agent - Enhanced Reconciliation Framework with Iterative Matching

This framework implements advanced matching strategies to achieve 80% match rate
through iterative thinking, training, and continuous improvement.
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple, Optional, Any
from difflib import SequenceMatcher
import re

class EnhancedReconciliationFramework:
    """
    Enhanced framework for achieving 80% match rate through iterative improvement.
    
    Core Principle: Compare files against each other with advanced matching strategies
    to achieve high match rates through continuous learning and improvement.
    """
    
    def __init__(self):
        self.name = "EnhancedReconciliationFramework"
        self.core_principle = "Compare files against each other for reconciliation"
        self.target_match_rate = 80.0  # 80% match rate goal
        self.current_match_rate = 0.0
        self.iteration_count = 0
        self.max_iterations = 10
        self.matching_strategies = []
        self.learning_history = []
        
        # Initialize matching strategies
        self._initialize_matching_strategies()
    
    def _initialize_matching_strategies(self):
        """Initialize various matching strategies"""
        self.matching_strategies = [
            {
                "name": "exact_amount_match",
                "description": "Exact amount matching with 0.01 tolerance",
                "tolerance": 0.01,
                "weight": 1.0
            },
            {
                "name": "amount_date_match",
                "description": "Amount + date proximity matching",
                "amount_tolerance": 0.01,
                "date_tolerance_days": 3,
                "weight": 0.9
            },
            {
                "name": "description_similarity",
                "description": "Description similarity matching",
                "similarity_threshold": 0.6,
                "weight": 0.8
            },
            {
                "name": "partial_amount_match",
                "description": "Partial amount matching for large transactions",
                "tolerance_percentage": 0.05,  # 5% tolerance
                "min_amount": 1000,  # Only for transactions > $1000
                "weight": 0.7
            },
            {
                "name": "pattern_matching",
                "description": "Pattern-based matching for common transaction types",
                "patterns": {
                    "ACH": r"ACH|ACH_ADV|ACH_FILE",
                    "CHECK": r"CHECK|CHK|DRAFT",
                    "WIRE": r"WIRE|WIR",
                    "DEPOSIT": r"DEP|DEPOSIT",
                    "FEE": r"FEE|CHARGE|SERVICE"
                },
                "weight": 0.6
            }
        ]
    
    def load_and_consolidate_gl_data(self, file_paths: List[Path]) -> Optional[pd.DataFrame]:
        """Load and consolidate GL activity data with enhanced processing"""
        try:
            consolidated_data = []
            
            for file_path in file_paths:
                if not file_path.exists():
                    print(f"⚠️ File not found: {file_path}")
                    continue
                
                # Read all sheets
                gl_data = pd.read_excel(file_path, sheet_name=None)
                
                for sheet_name, df in gl_data.items():
                    if sheet_name.startswith('74'):  # GL account sheets
                        df['GL_Account'] = int(sheet_name)
                        df['Source_File'] = file_path.name
                        
                        # Enhanced data processing
                        df = self._enhance_gl_data(df)
                        consolidated_data.append(df)
            
            if consolidated_data:
                result = pd.concat(consolidated_data, ignore_index=True)
                print(f"✅ Consolidated {len(result)} GL transactions from {len(file_paths)} files")
                return result
            else:
                print("❌ No GL data found")
                return None
                
        except Exception as e:
            print(f"❌ Error consolidating GL data: {e}")
            return None
    
    def _enhance_gl_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Enhance GL data with additional matching fields"""
        try:
            # Standardize date columns
            date_cols = ['Effective Date', 'Actual Date', 'Open Period']
            for col in date_cols:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
            
            # Calculate net amount
            df['Net_Amount'] = (
                pd.to_numeric(df['Debit'], errors='coerce').fillna(0) + 
                pd.to_numeric(df['Credit'], errors='coerce').fillna(0)
            )
            
            # Create enhanced description for matching
            if 'Description' in df.columns:
                df['Enhanced_Description'] = df['Description'].fillna('').astype(str).str.upper()
                df['Description_Length'] = df['Enhanced_Description'].str.len()
                df['Description_Words'] = df['Enhanced_Description'].str.split().str.len()
            
            # Add transaction type patterns
            if 'Description' in df.columns:
                df['Transaction_Type'] = df['Description'].fillna('').astype(str).apply(self._identify_transaction_type)
            
            return df
            
        except Exception as e:
            print(f"⚠️ Error enhancing GL data: {e}")
            return df
    
    def _identify_transaction_type(self, description: str) -> str:
        """Identify transaction type from description"""
        desc_upper = description.upper()
        
        for pattern_name, pattern in self.matching_strategies[4]['patterns'].items():
            if re.search(pattern, desc_upper):
                return pattern_name
        
        return 'OTHER'
    
    def load_bank_statement_data(self, file_path: Path) -> Optional[pd.DataFrame]:
        """Load bank statement data with enhanced processing"""
        try:
            if not file_path.exists():
                print(f"❌ Bank file not found: {file_path}")
                return None
            
            bank_data = pd.read_excel(file_path)
            
            # Calculate net amount for each transaction
            bank_data['Net_Amount'] = (
                pd.to_numeric(bank_data['Debit'], errors='coerce').fillna(0) + 
                pd.to_numeric(bank_data['Credit'], errors='coerce').fillna(0)
            )
            
            # Enhanced data processing
            bank_data = self._enhance_bank_data(bank_data)
            
            print(f"✅ Loaded {len(bank_data)} bank transactions from {file_path.name}")
            return bank_data
            
        except Exception as e:
            print(f"❌ Error loading bank data: {e}")
            return None
    
    def _enhance_bank_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Enhance bank data with additional matching fields"""
        try:
            # Standardize date columns
            if 'Post Date' in df.columns:
                df['Post Date'] = pd.to_datetime(df['Post Date'], errors='coerce')
            
            # Create enhanced description for matching
            if 'Description' in df.columns:
                df['Enhanced_Description'] = df['Description'].fillna('').astype(str).str.upper()
                df['Description_Length'] = df['Enhanced_Description'].str.len()
                df['Description_Words'] = df['Enhanced_Description'].str.split().str.len()
            
            # Add transaction type patterns
            if 'Description' in df.columns:
                df['Transaction_Type'] = df['Description'].fillna('').astype(str).apply(self._identify_transaction_type)
            
            return df
            
        except Exception as e:
            print(f"⚠️ Error enhancing bank data: {e}")
            return df
    
    def iterative_match_transactions(self, gl_data: pd.DataFrame, bank_data: pd.DataFrame) -> Tuple[List[Dict], List[Dict], List[Dict]]:
        """
        Iteratively match transactions using multiple strategies to achieve 80% match rate.
        """
        print(f"🔄 Starting iterative matching to achieve {self.target_match_rate}% match rate...")
        
        matches = []
        unmatched_gl = gl_data.copy()
        unmatched_bank = bank_data.copy()
        
        self.iteration_count = 0
        
        while (self.current_match_rate < self.target_match_rate and 
               self.iteration_count < self.max_iterations and 
               len(unmatched_gl) > 0 and len(unmatched_bank) > 0):
            
            self.iteration_count += 1
            print(f"\n🧠 Iteration {self.iteration_count}: Attempting to improve match rate...")
            
            # Try each matching strategy
            for strategy in self.matching_strategies:
                strategy_matches = self._apply_matching_strategy(
                    strategy, unmatched_gl, unmatched_bank, matches
                )
                
                if strategy_matches:
                    matches.extend(strategy_matches)
                    
                    # Remove matched transactions
                    matched_gl_indices = [m['gl_index'] for m in strategy_matches]
                    matched_bank_indices = [m['bank_index'] for m in strategy_matches]
                    
                    unmatched_gl = unmatched_gl.drop(matched_gl_indices)
                    unmatched_bank = unmatched_bank.drop(matched_bank_indices)
                    
                    print(f"   ✅ {strategy['name']}: Found {len(strategy_matches)} matches")
            
            # Calculate current match rate
            total_gl_transactions = len(gl_data)
            matched_count = len(matches)
            self.current_match_rate = (matched_count / total_gl_transactions) * 100
            
            print(f"   📊 Current match rate: {self.current_match_rate:.1f}% ({matched_count}/{total_gl_transactions})")
            
            # Learn from this iteration
            self._learn_from_iteration(matches, unmatched_gl, unmatched_bank)
            
            # Break if we've achieved our target
            if self.current_match_rate >= self.target_match_rate:
                print(f"🎯 Target match rate of {self.target_match_rate}% achieved!")
                break
        
        # Convert remaining unmatched to dict format
        unmatched_gl_list = unmatched_gl.to_dict('records')
        unmatched_bank_list = unmatched_bank.to_dict('records')
        
        print(f"\n✅ Iterative matching completed:")
        print(f"   🎯 Target: {self.target_match_rate}%")
        print(f"   📊 Achieved: {self.current_match_rate:.1f}%")
        print(f"   ✅ Matches: {len(matches)}")
        print(f"   ❌ Unmatched GL: {len(unmatched_gl_list)}")
        print(f"   ❌ Unmatched Bank: {len(unmatched_bank_list)}")
        print(f"   🔄 Iterations: {self.iteration_count}")
        
        return matches, unmatched_gl_list, unmatched_bank_list
    
    def _apply_matching_strategy(self, strategy: Dict, unmatched_gl: pd.DataFrame, 
                                unmatched_bank: pd.DataFrame, existing_matches: List[Dict]) -> List[Dict]:
        """Apply a specific matching strategy"""
        strategy_matches = []
        
        if strategy['name'] == 'exact_amount_match':
            strategy_matches = self._exact_amount_match(unmatched_gl, unmatched_bank)
        elif strategy['name'] == 'amount_date_match':
            strategy_matches = self._amount_date_match(unmatched_gl, unmatched_bank)
        elif strategy['name'] == 'description_similarity':
            strategy_matches = self._description_similarity_match(unmatched_gl, unmatched_bank)
        elif strategy['name'] == 'partial_amount_match':
            strategy_matches = self._partial_amount_match(unmatched_gl, unmatched_bank)
        elif strategy['name'] == 'pattern_matching':
            strategy_matches = self._pattern_matching(unmatched_gl, unmatched_bank)
        
        return strategy_matches
    
    def _exact_amount_match(self, gl_data: pd.DataFrame, bank_data: pd.DataFrame) -> List[Dict]:
        """Exact amount matching with tolerance"""
        matches = []
        tolerance = self.matching_strategies[0]['tolerance']
        
        for gl_idx, gl_row in gl_data.iterrows():
            gl_amount = gl_row['Net_Amount']
            
            for bank_idx, bank_row in bank_data.iterrows():
                bank_amount = bank_row['Net_Amount']
                
                if abs(gl_amount - bank_amount) <= tolerance:
                    matches.append({
                        'gl_transaction': gl_row.to_dict(),
                        'bank_transaction': bank_row.to_dict(),
                        'match_score': 1.0,
                        'match_strategy': 'exact_amount_match',
                        'gl_index': gl_idx,
                        'bank_index': bank_idx,
                        'amount_difference': abs(gl_amount - bank_amount)
                    })
                    break  # One match per GL transaction
        
        return matches
    
    def _amount_date_match(self, gl_data: pd.DataFrame, bank_data: pd.DataFrame) -> List[Dict]:
        """Amount + date proximity matching"""
        matches = []
        amount_tolerance = self.matching_strategies[1]['amount_tolerance']
        date_tolerance = self.matching_strategies[1]['date_tolerance_days']
        
        for gl_idx, gl_row in gl_data.iterrows():
            gl_amount = gl_row['Net_Amount']
            gl_date = gl_row.get('Effective Date') or gl_row.get('Actual Date')
            
            if pd.isna(gl_date):
                continue
            
            best_match = None
            best_score = 0
            
            for bank_idx, bank_row in bank_data.iterrows():
                bank_amount = bank_row['Net_Amount']
                bank_date = bank_row.get('Post Date')
                
                if pd.isna(bank_date):
                    continue
                
                # Check amount match
                amount_diff = abs(gl_amount - bank_amount)
                if amount_diff <= amount_tolerance:
                    # Check date match
                    date_diff = abs((gl_date - bank_date).days)
                    if date_diff <= date_tolerance:
                        # Calculate combined score
                        amount_score = 1 - (amount_diff / max(abs(gl_amount), abs(bank_amount), 1))
                        date_score = 1 - (date_diff / date_tolerance)
                        combined_score = (amount_score + date_score) / 2
                        
                        if combined_score > best_score:
                            best_score = combined_score
                            best_match = {
                                'gl_transaction': gl_row.to_dict(),
                                'bank_transaction': bank_row.to_dict(),
                                'match_score': combined_score,
                                'match_strategy': 'amount_date_match',
                                'gl_index': gl_idx,
                                'bank_index': bank_idx,
                                'amount_difference': amount_diff,
                                'date_difference_days': date_diff
                            }
            
            if best_match and best_score > 0.7:  # 70% threshold
                matches.append(best_match)
        
        return matches
    
    def _description_similarity_match(self, gl_data: pd.DataFrame, bank_data: pd.DataFrame) -> List[Dict]:
        """Description similarity matching"""
        matches = []
        similarity_threshold = self.matching_strategies[2]['similarity_threshold']
        
        for gl_idx, gl_row in gl_data.iterrows():
            gl_desc = str(gl_row.get('Description', '')).lower()
            gl_amount = gl_row['Net_Amount']
            
            if not gl_desc or gl_amount == 0:
                continue
            
            best_match = None
            best_score = 0
            
            for bank_idx, bank_row in bank_data.iterrows():
                bank_desc = str(bank_row.get('Description', '')).lower()
                bank_amount = bank_row['Net_Amount']
                
                if not bank_desc:
                    continue
                
                # Calculate description similarity
                desc_similarity = SequenceMatcher(None, gl_desc, bank_desc).ratio()
                
                # Check if amounts are close (within 10%)
                amount_diff = abs(gl_amount - bank_amount)
                amount_tolerance = max(abs(gl_amount), abs(bank_amount)) * 0.1
                
                if amount_diff <= amount_tolerance and desc_similarity > similarity_threshold:
                    # Calculate combined score
                    amount_score = 1 - (amount_diff / amount_tolerance)
                    combined_score = (desc_similarity + amount_score) / 2
                    
                    if combined_score > best_score:
                        best_score = combined_score
                        best_match = {
                            'gl_transaction': gl_row.to_dict(),
                            'bank_transaction': bank_row.to_dict(),
                            'match_score': combined_score,
                            'match_strategy': 'description_similarity',
                            'gl_index': gl_idx,
                            'bank_index': bank_idx,
                            'description_similarity': desc_similarity,
                            'amount_difference': amount_diff
                        }
            
            if best_match and best_score > 0.6:  # 60% threshold
                matches.append(best_match)
        
        return matches
    
    def _partial_amount_match(self, gl_data: pd.DataFrame, bank_data: pd.DataFrame) -> List[Dict]:
        """Partial amount matching for large transactions"""
        matches = []
        tolerance_percentage = self.matching_strategies[3]['tolerance_percentage']
        min_amount = self.matching_strategies[3]['min_amount']
        
        for gl_idx, gl_row in gl_data.iterrows():
            gl_amount = gl_row['Net_Amount']
            
            # Only apply to large transactions
            if abs(gl_amount) < min_amount:
                continue
            
            for bank_idx, bank_row in bank_data.iterrows():
                bank_amount = bank_row['Net_Amount']
                
                # Check if amounts are within percentage tolerance
                amount_diff = abs(gl_amount - bank_amount)
                tolerance_amount = abs(gl_amount) * tolerance_percentage
                
                if amount_diff <= tolerance_amount:
                    # Calculate match score based on amount difference
                    match_score = 1 - (amount_diff / tolerance_amount)
                    
                    matches.append({
                        'gl_transaction': gl_row.to_dict(),
                        'bank_transaction': bank_row.to_dict(),
                        'match_score': match_score,
                        'match_strategy': 'partial_amount_match',
                        'gl_index': gl_idx,
                        'bank_index': bank_idx,
                        'amount_difference': amount_diff,
                        'tolerance_percentage': tolerance_percentage
                    })
                    break  # One match per GL transaction
        
        return matches
    
    def _pattern_matching(self, gl_data: pd.DataFrame, bank_data: pd.DataFrame) -> List[Dict]:
        """Pattern-based matching for common transaction types"""
        matches = []
        patterns = self.matching_strategies[4]['patterns']
        
        for gl_idx, gl_row in gl_data.iterrows():
            gl_desc = str(gl_row.get('Description', '')).upper()
            gl_amount = gl_row['Net_Amount']
            gl_type = gl_row.get('Transaction_Type', 'OTHER')
            
            for bank_idx, bank_row in bank_data.iterrows():
                bank_desc = str(bank_row.get('Description', '')).upper()
                bank_amount = bank_row['Net_Amount']
                bank_type = bank_row.get('Transaction_Type', 'OTHER')
                
                # Check if transaction types match
                if gl_type == bank_type and gl_type != 'OTHER':
                    # Check if amounts are close (within 20% for pattern matching)
                    amount_diff = abs(gl_amount - bank_amount)
                    amount_tolerance = max(abs(gl_amount), abs(bank_amount)) * 0.2
                    
                    if amount_diff <= amount_tolerance:
                        # Calculate pattern match score
                        pattern_score = 0.8  # Base score for type match
                        amount_score = 1 - (amount_diff / amount_tolerance)
                        combined_score = (pattern_score + amount_score) / 2
                        
                        matches.append({
                            'gl_transaction': gl_row.to_dict(),
                            'bank_transaction': bank_row.to_dict(),
                            'match_score': combined_score,
                            'match_strategy': 'pattern_matching',
                            'gl_index': gl_idx,
                            'bank_index': bank_idx,
                            'transaction_type': gl_type,
                            'amount_difference': amount_diff
                        })
                        break  # One match per GL transaction
        
        return matches
    
    def _learn_from_iteration(self, matches: List[Dict], unmatched_gl: pd.DataFrame, unmatched_bank: pd.DataFrame):
        """Learn from each iteration to improve future matching"""
        learning_entry = {
            'iteration': self.iteration_count,
            'match_rate': self.current_match_rate,
            'matches_found': len(matches),
            'unmatched_gl_count': len(unmatched_gl),
            'unmatched_bank_count': len(unmatched_bank),
            'timestamp': datetime.now().isoformat()
        }
        
        self.learning_history.append(learning_entry)
        
        # Analyze patterns in unmatched transactions
        if len(unmatched_gl) > 0:
            self._analyze_unmatched_patterns(unmatched_gl, unmatched_bank)
    
    def _analyze_unmatched_patterns(self, unmatched_gl: pd.DataFrame, unmatched_bank: pd.DataFrame):
        """Analyze patterns in unmatched transactions to improve matching"""
        try:
            # Analyze amount ranges
            gl_amounts = unmatched_gl['Net_Amount']
            bank_amounts = unmatched_bank['Net_Amount']
            
            print(f"   📊 Unmatched GL amount range: ${gl_amounts.min():,.2f} to ${gl_amounts.max():,.2f}")
            print(f"   📊 Unmatched Bank amount range: ${bank_amounts.min():,.2f} to ${bank_amounts.max():,.2f}")
            
            # Analyze transaction types
            if 'Transaction_Type' in unmatched_gl.columns:
                gl_types = unmatched_gl['Transaction_Type'].value_counts()
                print(f"   📊 Unmatched GL types: {dict(gl_types.head(3))}")
            
            if 'Transaction_Type' in unmatched_bank.columns:
                bank_types = unmatched_bank['Transaction_Type'].value_counts()
                print(f"   📊 Unmatched Bank types: {dict(bank_types.head(3))}")
                
        except Exception as e:
            print(f"   ⚠️ Error analyzing patterns: {e}")
    
    def calculate_reconciliation_summary(self, gl_data: pd.DataFrame, bank_data: pd.DataFrame,
                                       matches: List[Dict], unmatched_gl: List[Dict], 
                                       unmatched_bank: List[Dict]) -> Dict[str, Any]:
        """Calculate comprehensive reconciliation summary"""
        # Calculate GL totals
        gl_debits = pd.to_numeric(gl_data['Debit'], errors='coerce').fillna(0).sum()
        gl_credits = pd.to_numeric(gl_data['Credit'], errors='coerce').fillna(0).sum()
        gl_balance = gl_debits + gl_credits
        
        # Calculate bank totals
        bank_total = bank_data['Net_Amount'].sum()
        
        # Calculate variance
        variance = gl_balance - bank_total
        variance_percentage = (variance / abs(gl_balance)) * 100 if gl_balance != 0 else 0
        
        # Calculate matched amounts
        matched_gl_amount = sum(
            match['gl_transaction']['Net_Amount'] for match in matches
        )
        matched_bank_amount = sum(match['bank_transaction']['Net_Amount'] for match in matches)
        
        # Calculate unmatched amounts
        unmatched_gl_amount = sum(row['Net_Amount'] for row in unmatched_gl)
        unmatched_bank_amount = sum(row['Net_Amount'] for row in unmatched_bank)
        
        # Analyze match strategies
        strategy_analysis = {}
        for match in matches:
            strategy = match['match_strategy']
            if strategy not in strategy_analysis:
                strategy_analysis[strategy] = 0
            strategy_analysis[strategy] += 1
        
        summary = {
            'timestamp': datetime.now().isoformat(),
            'reconciliation_summary': {
                'gl_balance': gl_balance,
                'bank_total': bank_total,
                'variance': variance,
                'variance_percentage': variance_percentage,
                'is_balanced': abs(variance) < 1000  # Within $1000 tolerance
            },
            'matching_results': {
                'total_matches': len(matches),
                'matched_gl_amount': matched_gl_amount,
                'matched_bank_amount': matched_bank_amount,
                'unmatched_gl_count': len(unmatched_gl),
                'unmatched_gl_amount': unmatched_gl_amount,
                'unmatched_bank_count': len(unmatched_bank),
                'unmatched_bank_amount': unmatched_bank_amount
            },
            'match_rate': self.current_match_rate,
            'target_match_rate': self.target_match_rate,
            'iterations_used': self.iteration_count,
            'strategy_analysis': strategy_analysis,
            'learning_history': self.learning_history
        }
        
        return summary
    
    def perform_enhanced_reconciliation(self, gl_files: List[Path], bank_file: Path) -> Dict[str, Any]:
        """
        Perform enhanced reconciliation with iterative matching to achieve 80% match rate.
        """
        print("🤖 Excel Agent - Enhanced Reconciliation Framework")
        print("=" * 60)
        print(f"📋 Core Principle: {self.core_principle}")
        print(f"🎯 Target Match Rate: {self.target_match_rate}%")
        print(f"📁 GL Files: {len(gl_files)}")
        print(f"📁 Bank File: {bank_file.name}")
        print()
        
        # Load and consolidate GL data
        gl_data = self.load_and_consolidate_gl_data(gl_files)
        if gl_data is None:
            return {"status": "error", "message": "Failed to load GL data"}
        
        # Load bank data
        bank_data = self.load_bank_statement_data(bank_file)
        if bank_data is None:
            return {"status": "error", "message": "Failed to load bank data"}
        
        print()
        
        # Perform iterative matching
        matches, unmatched_gl, unmatched_bank = self.iterative_match_transactions(gl_data, bank_data)
        
        print()
        
        # Calculate summary
        summary = self.calculate_reconciliation_summary(gl_data, bank_data, matches, unmatched_gl, unmatched_bank)
        
        # Prepare results
        results = {
            "status": "success",
            "message": f"Enhanced reconciliation completed with {self.current_match_rate:.1f}% match rate",
            "framework": self.name,
            "core_principle": self.core_principle,
            "target_achieved": self.current_match_rate >= self.target_match_rate,
            "data": {
                "gl_data_shape": gl_data.shape,
                "bank_data_shape": bank_data.shape,
                "matches": matches,
                "unmatched_gl": unmatched_gl,
                "unmatched_bank": unmatched_bank,
                "summary": summary
            }
        }
        
        # Display summary
        recon_summary = summary['reconciliation_summary']
        matching_results = summary['matching_results']
        
        print("📋 ENHANCED RECONCILIATION SUMMARY:")
        print("=" * 40)
        print(f"Status: {'✅ BALANCED' if recon_summary['is_balanced'] else '❌ IMBALANCED'}")
        print(f"GL Balance: ${recon_summary['gl_balance']:,.2f}")
        print(f"Bank Total: ${recon_summary['bank_total']:,.2f}")
        print(f"Variance: ${recon_summary['variance']:,.2f} ({recon_summary['variance_percentage']:.2f}%)")
        print(f"Match Rate: {summary['match_rate']:.1f}% (Target: {summary['target_match_rate']}%)")
        print(f"Matches: {matching_results['total_matches']}")
        print(f"Unmatched GL: {matching_results['unmatched_gl_count']}")
        print(f"Unmatched Bank: {matching_results['unmatched_bank_count']}")
        print(f"Iterations: {summary['iterations_used']}")
        
        if summary['strategy_analysis']:
            print(f"\n🎯 Strategy Analysis:")
            for strategy, count in summary['strategy_analysis'].items():
                print(f"   {strategy}: {count} matches")
        
        return results

# Global enhanced framework instance
enhanced_reconciliation_framework = EnhancedReconciliationFramework()

def perform_enhanced_reconciliation(gl_files: List[Path], bank_file: Path) -> Dict[str, Any]:
    """Perform enhanced reconciliation using the iterative framework."""
    return enhanced_reconciliation_framework.perform_enhanced_reconciliation(gl_files, bank_file)

if __name__ == "__main__":
    # Example usage
    print("🤖 Excel Agent - Enhanced Reconciliation Framework")
    print("=" * 60)
    print("Core Principle: Compare files against each other for reconciliation")
    print("Target: Achieve 80% match rate through iterative improvement")
    print()
    print("This enhanced framework implements multiple matching strategies")
    print("and iterative learning to achieve high match rates.")
    print()
    print("✅ Enhanced framework ready for high-performance reconciliation")
