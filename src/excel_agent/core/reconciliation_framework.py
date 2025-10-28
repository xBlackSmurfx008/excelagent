#!/usr/bin/env python3
"""
Excel Agent - Unified Reconciliation Framework

This framework ensures all agents understand that reconciliation means
comparing files against each other, not analyzing them separately.
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json
from typing import Dict, List, Tuple, Optional, Any

class ReconciliationFramework:
    """
    Unified framework for all reconciliation agents.
    
    Core Principle: Reconciliation means comparing files against each other
    to find matches, identify discrepancies, and calculate variances.
    """
    
    def __init__(self):
        self.name = "ReconciliationFramework"
        self.core_principle = "Compare files against each other for reconciliation"
        self.supported_file_types = ["gl_activity", "bank_statement"]
        
    def validate_reconciliation_approach(self, agent_name: str, method: str) -> bool:
        """
        Validate that an agent is using the correct reconciliation approach.
        
        Args:
            agent_name: Name of the agent
            method: Method being used
            
        Returns:
            True if using correct approach (file comparison), False otherwise
        """
        correct_keywords = [
            "compare", "match", "reconcile", "against", "versus", "vs",
            "transaction_matching", "file_comparison", "cross_reference"
        ]
        
        incorrect_keywords = [
            "analyze_separately", "individual_analysis", "separate_processing",
            "isolated_analysis", "independent_review"
        ]
        
        method_lower = method.lower()
        
        # Check for correct approach
        has_correct = any(keyword in method_lower for keyword in correct_keywords)
        
        # Check for incorrect approach
        has_incorrect = any(keyword in method_lower for keyword in incorrect_keywords)
        
        if has_incorrect:
            print(f"❌ {agent_name}: Using incorrect approach - {method}")
            print(f"   Correct approach: Compare files against each other")
            return False
        
        if has_correct:
            print(f"✅ {agent_name}: Using correct approach - {method}")
            return True
        
        print(f"⚠️ {agent_name}: Approach unclear - {method}")
        return False
    
    def load_and_consolidate_gl_data(self, file_paths: List[Path]) -> Optional[pd.DataFrame]:
        """
        Load and consolidate GL activity data from multiple files.
        
        Args:
            file_paths: List of file paths to GL activity files
            
        Returns:
            Consolidated DataFrame or None if error
        """
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
    
    def load_bank_statement_data(self, file_path: Path) -> Optional[pd.DataFrame]:
        """
        Load bank statement data from a single file.
        
        Args:
            file_path: Path to bank statement file
            
        Returns:
            Bank statement DataFrame or None if error
        """
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
            
            print(f"✅ Loaded {len(bank_data)} bank transactions from {file_path.name}")
            return bank_data
            
        except Exception as e:
            print(f"❌ Error loading bank data: {e}")
            return None
    
    def match_transactions(self, gl_data: pd.DataFrame, bank_data: pd.DataFrame, 
                          tolerance: float = 0.01) -> Tuple[List[Dict], List[Dict], List[Dict]]:
        """
        Match GL transactions with bank transactions.
        
        Args:
            gl_data: GL activity DataFrame
            bank_data: Bank statement DataFrame
            tolerance: Amount tolerance for matching
            
        Returns:
            Tuple of (matches, unmatched_gl, unmatched_bank)
        """
        matches = []
        unmatched_gl = []
        unmatched_bank = []
        
        # Create copies for matching
        gl_remaining = gl_data.copy()
        bank_remaining = bank_data.copy()
        
        print(f"🔄 Matching {len(gl_data)} GL transactions against {len(bank_data)} bank transactions...")
        
        for idx, gl_row in gl_data.iterrows():
            gl_debit = pd.to_numeric(gl_row['Debit'], errors='coerce')
            gl_credit = pd.to_numeric(gl_row['Credit'], errors='coerce')
            gl_amount = (gl_debit if not pd.isna(gl_debit) else 0) + (gl_credit if not pd.isna(gl_credit) else 0)
            
            if gl_amount == 0:
                unmatched_gl.append(gl_row.to_dict())
                continue
            
            # Find matching bank transaction
            best_match = None
            best_match_idx = None
            best_score = 0
            
            for bank_idx, bank_row in bank_remaining.iterrows():
                bank_amount = bank_row['Net_Amount']
                
                # Check amount match (within tolerance)
                amount_diff = abs(gl_amount - bank_amount)
                if amount_diff <= tolerance:
                    # Calculate match score
                    amount_score = 1 - (amount_diff / max(abs(gl_amount), abs(bank_amount), 1))
                    
                    if amount_score > best_score:
                        best_score = amount_score
                        best_match = bank_row
                        best_match_idx = bank_idx
            
            if best_match is not None and best_score > 0.9:  # 90% match threshold
                matches.append({
                    'gl_transaction': gl_row.to_dict(),
                    'bank_transaction': best_match.to_dict(),
                    'match_score': best_score,
                    'amount_difference': abs(gl_amount - best_match['Net_Amount'])
                })
                
                # Remove matched bank transaction
                bank_remaining = bank_remaining.drop(best_match_idx)
            else:
                unmatched_gl.append(gl_row.to_dict())
        
        # Remaining bank transactions are unmatched
        unmatched_bank = bank_remaining.to_dict('records')
        
        print(f"✅ Found {len(matches)} matches")
        print(f"❌ {len(unmatched_gl)} unmatched GL transactions")
        print(f"❌ {len(unmatched_bank)} unmatched bank transactions")
        
        return matches, unmatched_gl, unmatched_bank
    
    def calculate_reconciliation_summary(self, gl_data: pd.DataFrame, bank_data: pd.DataFrame,
                                       matches: List[Dict], unmatched_gl: List[Dict], 
                                       unmatched_bank: List[Dict]) -> Dict[str, Any]:
        """
        Calculate comprehensive reconciliation summary.
        
        Args:
            gl_data: GL activity DataFrame
            bank_data: Bank statement DataFrame
            matches: List of matched transactions
            unmatched_gl: List of unmatched GL transactions
            unmatched_bank: List of unmatched bank transactions
            
        Returns:
            Reconciliation summary dictionary
        """
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
            match['gl_transaction']['Debit'] + match['gl_transaction']['Credit'] 
            for match in matches
        )
        matched_bank_amount = sum(match['bank_transaction']['Net_Amount'] for match in matches)
        
        # Calculate unmatched amounts
        unmatched_gl_amount = 0
        for row in unmatched_gl:
            gl_debit = pd.to_numeric(row['Debit'], errors='coerce')
            gl_credit = pd.to_numeric(row['Credit'], errors='coerce')
            gl_amount = (gl_debit if not pd.isna(gl_debit) else 0) + (gl_credit if not pd.isna(gl_credit) else 0)
            unmatched_gl_amount += gl_amount
        unmatched_bank_amount = sum(row['Net_Amount'] for row in unmatched_bank)
        
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
            'match_rate': (len(matches) / len(gl_data)) * 100 if len(gl_data) > 0 else 0
        }
        
        return summary
    
    def perform_reconciliation(self, gl_files: List[Path], bank_file: Path) -> Dict[str, Any]:
        """
        Perform complete reconciliation by comparing GL files against bank statement.
        
        Args:
            gl_files: List of GL activity file paths
            bank_file: Bank statement file path
            
        Returns:
            Complete reconciliation results
        """
        print("🤖 Excel Agent - Unified Reconciliation Framework")
        print("=" * 50)
        print(f"📋 Core Principle: {self.core_principle}")
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
        
        # Match transactions
        matches, unmatched_gl, unmatched_bank = self.match_transactions(gl_data, bank_data)
        
        print()
        
        # Calculate summary
        summary = self.calculate_reconciliation_summary(gl_data, bank_data, matches, unmatched_gl, unmatched_bank)
        
        # Prepare results
        results = {
            "status": "success",
            "message": "Reconciliation completed successfully",
            "framework": self.name,
            "core_principle": self.core_principle,
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
        
        print("📋 RECONCILIATION SUMMARY:")
        print("=" * 30)
        print(f"Status: {'✅ BALANCED' if recon_summary['is_balanced'] else '❌ IMBALANCED'}")
        print(f"GL Balance: ${recon_summary['gl_balance']:,.2f}")
        print(f"Bank Total: ${recon_summary['bank_total']:,.2f}")
        print(f"Variance: ${recon_summary['variance']:,.2f} ({recon_summary['variance_percentage']:.2f}%)")
        print(f"Matches: {matching_results['total_matches']} ({summary['match_rate']:.1f}%)")
        print(f"Unmatched GL: {matching_results['unmatched_gl_count']}")
        print(f"Unmatched Bank: {matching_results['unmatched_bank_count']}")
        
        return results

# Global framework instance
reconciliation_framework = ReconciliationFramework()

def validate_agent_reconciliation_approach(agent_name: str, method: str) -> bool:
    """Validate that an agent is using the correct reconciliation approach."""
    return reconciliation_framework.validate_reconciliation_approach(agent_name, method)

def perform_unified_reconciliation(gl_files: List[Path], bank_file: Path) -> Dict[str, Any]:
    """Perform reconciliation using the unified framework."""
    return reconciliation_framework.perform_reconciliation(gl_files, bank_file)

if __name__ == "__main__":
    # Example usage
    print("🤖 Excel Agent - Unified Reconciliation Framework")
    print("=" * 50)
    print("Core Principle: Compare files against each other for reconciliation")
    print()
    print("This framework ensures all agents understand that reconciliation")
    print("means comparing files against each other, not analyzing them separately.")
    print()
    print("✅ Framework ready for use by all reconciliation agents")
