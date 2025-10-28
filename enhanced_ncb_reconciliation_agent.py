#!/usr/bin/env python3
"""
Enhanced NCB GL Reconciliation Agent - Targeting 80% Match Rate

This agent implements advanced matching strategies to achieve high match rates
through iterative improvement and multiple matching algorithms.
"""

import pandas as pd
from pathlib import Path
import os
from datetime import datetime
import json
from difflib import SequenceMatcher
import re

class EnhancedNCBReconciliationAgent:
    """
    Enhanced reconciliation agent targeting 80% match rate through iterative improvement.
    """
    
    def __init__(self):
        self.name = "EnhancedNCBReconciliationAgent"
        self.target_match_rate = 80.0
        self.current_match_rate = 0.0
        self.matching_strategies = [
            {"name": "exact_amount", "tolerance": 0.01, "weight": 1.0},
            {"name": "amount_date", "amount_tol": 0.01, "date_tol": 3, "weight": 0.9},
            {"name": "description_similarity", "threshold": 0.6, "weight": 0.8},
            {"name": "partial_amount", "tolerance_pct": 0.05, "min_amount": 1000, "weight": 0.7},
            {"name": "pattern_matching", "patterns": ["ACH", "CHECK", "WIRE", "DEPOSIT", "FEE"], "weight": 0.6}
        ]
    
    def load_gl_activity(self, gl_file):
        """Load and consolidate GL activity from all sheets"""
        print(f"📊 Loading GL Activity from all sheets...")
        
        gl_data = pd.read_excel(gl_file, sheet_name=None)
        consolidated_data = []
        
        for sheet_name, df in gl_data.items():
            if sheet_name.startswith('74'):  # GL account sheets
                # Calculate net amount
                df['Net_Amount'] = (
                    pd.to_numeric(df['Debit'], errors='coerce').fillna(0) + 
                    pd.to_numeric(df['Credit'], errors='coerce').fillna(0)
                )
                
                # Add GL account
                df['GL_Account'] = int(sheet_name)
                
                # Enhance description for matching
                if 'Description' in df.columns:
                    df['Enhanced_Description'] = df['Description'].fillna('').astype(str).str.upper()
                
                # Add transaction type
                df['Transaction_Type'] = df['Description'].fillna('').astype(str).apply(self._identify_transaction_type)
                
                consolidated_data.append(df)
                
                net_total = df['Net_Amount'].sum()
                print(f"   ✅ GL {sheet_name}: {len(df)} transactions, Net: ${net_total:,.2f}")
        
        if consolidated_data:
            result = pd.concat(consolidated_data, ignore_index=True)
            print(f"   📊 Total GL transactions: {len(result)}")
            return result
        return pd.DataFrame()
    
    def _identify_transaction_type(self, description):
        """Identify transaction type from description"""
        desc_upper = description.upper()
        
        if re.search(r'ACH|ACH_ADV|ACH_FILE', desc_upper):
            return 'ACH'
        elif re.search(r'CHECK|CHK|DRAFT', desc_upper):
            return 'CHECK'
        elif re.search(r'WIRE|WIR', desc_upper):
            return 'WIRE'
        elif re.search(r'DEP|DEPOSIT', desc_upper):
            return 'DEPOSIT'
        elif re.search(r'FEE|CHARGE|SERVICE', desc_upper):
            return 'FEE'
        else:
            return 'OTHER'
    
    def load_bank_statement(self, bank_file):
        """Load bank statement data"""
        print(f"📊 Loading NCB Bank Statement...")
        
        bank_df = pd.read_excel(bank_file)
        
        # Calculate net amount
        bank_df['Net_Amount'] = (
            pd.to_numeric(bank_df['Credit'], errors='coerce').fillna(0) + 
            pd.to_numeric(bank_df['Debit'], errors='coerce').fillna(0)
        )
        
        # Enhance description for matching
        if 'Description' in bank_df.columns:
            bank_df['Enhanced_Description'] = bank_df['Description'].fillna('').astype(str).str.upper()
        
        # Add transaction type
        bank_df['Transaction_Type'] = bank_df['Description'].fillna('').astype(str).apply(self._identify_transaction_type)
        
        # Get date range
        if 'Post Date' in bank_df.columns:
            bank_df['Post Date'] = pd.to_datetime(bank_df['Post Date'], errors='coerce')
            start_date = bank_df['Post Date'].min().strftime('%Y-%m-%d')
            end_date = bank_df['Post Date'].max().strftime('%Y-%m-%d')
            print(f"   📅 Date range: {start_date} to {end_date}")
        
        total_amount = bank_df['Net_Amount'].sum()
        print(f"   💰 Total net amount: ${total_amount:,.2f}")
        print(f"   📊 NCB Statement: {len(bank_df)} transactions")
        
        return bank_df
    
    def iterative_match_transactions(self, gl_data, bank_data):
        """Iteratively match transactions using multiple strategies"""
        print(f"\n🔄 Starting iterative matching to achieve {self.target_match_rate}% match rate...")
        
        matches = []
        unmatched_gl = gl_data.copy()
        unmatched_bank = bank_data.copy()
        
        iteration = 0
        max_iterations = 5
        
        while (self.current_match_rate < self.target_match_rate and 
               iteration < max_iterations and 
               len(unmatched_gl) > 0 and len(unmatched_bank) > 0):
            
            iteration += 1
            print(f"\n🧠 Iteration {iteration}: Attempting to improve match rate...")
            
            # Strategy 1: Exact amount matching
            exact_matches = self._exact_amount_match(unmatched_gl, unmatched_bank)
            if exact_matches:
                matches.extend(exact_matches)
                unmatched_gl, unmatched_bank = self._remove_matched_transactions(
                    unmatched_gl, unmatched_bank, exact_matches
                )
                print(f"   ✅ Exact amount: Found {len(exact_matches)} matches")
            
            # Strategy 2: Amount + Date matching
            amount_date_matches = self._amount_date_match(unmatched_gl, unmatched_bank)
            if amount_date_matches:
                matches.extend(amount_date_matches)
                unmatched_gl, unmatched_bank = self._remove_matched_transactions(
                    unmatched_gl, unmatched_bank, amount_date_matches
                )
                print(f"   ✅ Amount+Date: Found {len(amount_date_matches)} matches")
            
            # Strategy 3: Description similarity
            desc_matches = self._description_similarity_match(unmatched_gl, unmatched_bank)
            if desc_matches:
                matches.extend(desc_matches)
                unmatched_gl, unmatched_bank = self._remove_matched_transactions(
                    unmatched_gl, unmatched_bank, desc_matches
                )
                print(f"   ✅ Description similarity: Found {len(desc_matches)} matches")
            
            # Strategy 4: Partial amount matching
            partial_matches = self._partial_amount_match(unmatched_gl, unmatched_bank)
            if partial_matches:
                matches.extend(partial_matches)
                unmatched_gl, unmatched_bank = self._remove_matched_transactions(
                    unmatched_gl, unmatched_bank, partial_matches
                )
                print(f"   ✅ Partial amount: Found {len(partial_matches)} matches")
            
            # Strategy 5: Pattern matching
            pattern_matches = self._pattern_matching(unmatched_gl, unmatched_bank)
            if pattern_matches:
                matches.extend(pattern_matches)
                unmatched_gl, unmatched_bank = self._remove_matched_transactions(
                    unmatched_gl, unmatched_bank, pattern_matches
                )
                print(f"   ✅ Pattern matching: Found {len(pattern_matches)} matches")
            
            # Calculate current match rate
            total_gl_transactions = len(gl_data)
            matched_count = len(matches)
            self.current_match_rate = (matched_count / total_gl_transactions) * 100
            
            print(f"   📊 Current match rate: {self.current_match_rate:.1f}% ({matched_count}/{total_gl_transactions})")
            
            # Break if no new matches found
            if len(matches) == 0:
                print(f"   ⚠️ No new matches found in iteration {iteration}")
                break
        
        print(f"\n✅ Iterative matching completed:")
        print(f"   🎯 Target: {self.target_match_rate}%")
        print(f"   📊 Achieved: {self.current_match_rate:.1f}%")
        print(f"   ✅ Matches: {len(matches)}")
        print(f"   ❌ Unmatched GL: {len(unmatched_gl)}")
        print(f"   ❌ Unmatched Bank: {len(unmatched_bank)}")
        print(f"   🔄 Iterations: {iteration}")
        
        return matches, unmatched_gl.to_dict('records'), unmatched_bank.to_dict('records')
    
    def _exact_amount_match(self, gl_data, bank_data):
        """Exact amount matching with tolerance"""
        matches = []
        tolerance = 0.01
        
        for gl_idx, gl_row in gl_data.iterrows():
            gl_amount = gl_row['Net_Amount']
            
            for bank_idx, bank_row in bank_data.iterrows():
                bank_amount = bank_row['Net_Amount']
                
                if abs(gl_amount - bank_amount) <= tolerance:
                    matches.append({
                        'gl_transaction': gl_row.to_dict(),
                        'bank_transaction': bank_row.to_dict(),
                        'match_type': 'exact_amount',
                        'gl_index': gl_idx,
                        'bank_index': bank_idx,
                        'amount_difference': abs(gl_amount - bank_amount)
                    })
                    break
        
        return matches
    
    def _amount_date_match(self, gl_data, bank_data):
        """Amount + date proximity matching"""
        matches = []
        amount_tolerance = 0.01
        date_tolerance_days = 3
        
        for gl_idx, gl_row in gl_data.iterrows():
            gl_amount = gl_row['Net_Amount']
            gl_date = gl_row.get('Effective Date')
            
            if pd.isna(gl_date):
                continue
            
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
                    if date_diff <= date_tolerance_days:
                        matches.append({
                            'gl_transaction': gl_row.to_dict(),
                            'bank_transaction': bank_row.to_dict(),
                            'match_type': 'amount_date',
                            'gl_index': gl_idx,
                            'bank_index': bank_idx,
                            'amount_difference': amount_diff,
                            'date_difference_days': date_diff
                        })
                        break
        
        return matches
    
    def _description_similarity_match(self, gl_data, bank_data):
        """Description similarity matching"""
        matches = []
        similarity_threshold = 0.6
        
        for gl_idx, gl_row in gl_data.iterrows():
            gl_desc = str(gl_row.get('Description', '')).lower()
            gl_amount = gl_row['Net_Amount']
            
            if not gl_desc or gl_amount == 0:
                continue
            
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
                    matches.append({
                        'gl_transaction': gl_row.to_dict(),
                        'bank_transaction': bank_row.to_dict(),
                        'match_type': 'description_similarity',
                        'gl_index': gl_idx,
                        'bank_index': bank_idx,
                        'description_similarity': desc_similarity,
                        'amount_difference': amount_diff
                    })
                    break
        
        return matches
    
    def _partial_amount_match(self, gl_data, bank_data):
        """Partial amount matching for large transactions"""
        matches = []
        tolerance_percentage = 0.05  # 5% tolerance
        min_amount = 1000  # Only for transactions > $1000
        
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
                    matches.append({
                        'gl_transaction': gl_row.to_dict(),
                        'bank_transaction': bank_row.to_dict(),
                        'match_type': 'partial_amount',
                        'gl_index': gl_idx,
                        'bank_index': bank_idx,
                        'amount_difference': amount_diff,
                        'tolerance_percentage': tolerance_percentage
                    })
                    break
        
        return matches
    
    def _pattern_matching(self, gl_data, bank_data):
        """Pattern-based matching for common transaction types"""
        matches = []
        
        for gl_idx, gl_row in gl_data.iterrows():
            gl_amount = gl_row['Net_Amount']
            gl_type = gl_row.get('Transaction_Type', 'OTHER')
            
            for bank_idx, bank_row in bank_data.iterrows():
                bank_amount = bank_row['Net_Amount']
                bank_type = bank_row.get('Transaction_Type', 'OTHER')
                
                # Check if transaction types match
                if gl_type == bank_type and gl_type != 'OTHER':
                    # Check if amounts are close (within 20% for pattern matching)
                    amount_diff = abs(gl_amount - bank_amount)
                    amount_tolerance = max(abs(gl_amount), abs(bank_amount)) * 0.2
                    
                    if amount_diff <= amount_tolerance:
                        matches.append({
                            'gl_transaction': gl_row.to_dict(),
                            'bank_transaction': bank_row.to_dict(),
                            'match_type': 'pattern_matching',
                            'gl_index': gl_idx,
                            'bank_index': bank_idx,
                            'transaction_type': gl_type,
                            'amount_difference': amount_diff
                        })
                        break
        
        return matches
    
    def _remove_matched_transactions(self, gl_data, bank_data, matches):
        """Remove matched transactions from unmatched lists"""
        matched_gl_indices = [m['gl_index'] for m in matches]
        matched_bank_indices = [m['bank_index'] for m in matches]
        
        unmatched_gl = gl_data.drop(matched_gl_indices)
        unmatched_bank = bank_data.drop(matched_bank_indices)
        
        return unmatched_gl, unmatched_bank
    
    def run_enhanced_reconciliation(self, gl_file, bank_file):
        """Run enhanced reconciliation with iterative matching"""
        print("🤖 Excel Agent - Enhanced NCB Statement vs GL Activity Reconciliation")
        print("=" * 70)
        print(f"🎯 Target Match Rate: {self.target_match_rate}%")
        print()
        
        # Load data
        gl_data = self.load_gl_activity(gl_file)
        if gl_data.empty:
            return {"status": "error", "message": "No GL data found"}
        
        bank_data = self.load_bank_statement(bank_file)
        if bank_data.empty:
            return {"status": "error", "message": "No bank data found"}
        
        print()
        
        # Perform iterative matching
        matches, unmatched_gl, unmatched_bank = self.iterative_match_transactions(gl_data, bank_data)
        
        print()
        
        # Calculate reconciliation summary
        gl_balance = gl_data['Net_Amount'].sum()
        bank_total = bank_data['Net_Amount'].sum()
        variance = gl_balance - bank_total
        variance_percentage = (variance / abs(gl_balance)) * 100 if gl_balance != 0 else 0
        
        # Analyze match strategies
        strategy_analysis = {}
        for match in matches:
            match_type = match['match_type']
            if match_type not in strategy_analysis:
                strategy_analysis[match_type] = 0
            strategy_analysis[match_type] += 1
        
        print("📊 Analyzing reconciliation results...")
        print(f"   📊 Reconciliation Summary:")
        print(f"      GL Balance: ${gl_balance:,.2f}")
        print(f"      Bank Amount: ${bank_total:,.2f}")
        print(f"      Variance: ${variance:,.2f}")
        print(f"      Matches: {len(matches)}")
        print(f"      Unmatched GL: {len(unmatched_gl)}")
        print(f"      Unmatched Bank: {len(unmatched_bank)}")
        
        # Save detailed report
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "agent": self.name,
            "target_match_rate": self.target_match_rate,
            "achieved_match_rate": self.current_match_rate,
            "target_achieved": self.current_match_rate >= self.target_match_rate,
            "gl_file": str(gl_file),
            "bank_file": str(bank_file),
            "reconciliation_summary": {
                "gl_balance": gl_balance,
                "bank_total": bank_total,
                "variance": variance,
                "variance_percentage": variance_percentage,
                "is_balanced": abs(variance) < 1000
            },
            "matching_results": {
                "total_matches": len(matches),
                "unmatched_gl_count": len(unmatched_gl),
                "unmatched_bank_count": len(unmatched_bank),
                "match_rate": self.current_match_rate
            },
            "strategy_analysis": strategy_analysis,
            "matches": matches,
            "unmatched_gl": unmatched_gl,
            "unmatched_bank": unmatched_bank
        }
        
        # Save report
        reports_dir = Path("data/reports")
        reports_dir.mkdir(parents=True, exist_ok=True)
        report_filename = f"enhanced_ncb_reconciliation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path = reports_dir / report_filename
        
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=4, default=str)
        
        print(f"\n📄 Enhanced reconciliation report saved!")
        print(f"📁 Report location: {report_path}")
        
        print("\n📋 ENHANCED RECONCILIATION SUMMARY:")
        print("=" * 40)
        print(f"Status: {'✅ BALANCED' if abs(variance) < 1000 else '❌ IMBALANCED'}")
        print(f"GL Balance: ${gl_balance:,.2f}")
        print(f"Bank Amount: ${bank_total:,.2f}")
        print(f"Variance: ${variance:,.2f} ({variance_percentage:.2f}%)")
        print(f"Match Rate: {self.current_match_rate:.1f}% (Target: {self.target_match_rate}%)")
        print(f"Matches Found: {len(matches)}")
        print(f"Unmatched GL: {len(unmatched_gl)}")
        print(f"Unmatched Bank: {len(unmatched_bank)}")
        
        if strategy_analysis:
            print(f"\n🎯 Strategy Analysis:")
            for strategy, count in strategy_analysis.items():
                print(f"   {strategy}: {count} matches")
        
        print(f"\n🎉 Enhanced NCB vs GL reconciliation completed!")
        
        return report_data

def main():
    """Main function to run enhanced reconciliation"""
    print("🚀 Running Enhanced NCB GL Reconciliation Agent...")
    
    # Find files
    upload_dir = Path("uploads")
    gl_file = None
    bank_file = None
    
    for f in upload_dir.iterdir():
        if "Flex GL Activity" in f.name and f.suffix in ['.xlsx', '.xls']:
            gl_file = f
        if "NCB Bank Activity" in f.name and f.suffix in ['.xlsx', '.xls']:
            bank_file = f
    
    if not gl_file:
        print("❌ GL Activity file not found")
        return
    
    if not bank_file:
        print("❌ Bank Statement file not found")
        return
    
    print(f"📁 GL Activity File: {gl_file}")
    print(f"📁 Bank Statement File: {bank_file}")
    print("\n✅ Both files found!\n")
    
    # Run enhanced reconciliation
    agent = EnhancedNCBReconciliationAgent()
    result = agent.run_enhanced_reconciliation(gl_file, bank_file)
    
    if result.get('target_achieved'):
        print(f"\n🎯 SUCCESS: Target match rate of {agent.target_match_rate}% achieved!")
    else:
        print(f"\n⚠️ PARTIAL SUCCESS: Achieved {agent.current_match_rate:.1f}% match rate (Target: {agent.target_match_rate}%)")

if __name__ == "__main__":
    main()
