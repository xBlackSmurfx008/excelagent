#!/usr/bin/env python3
"""
Excel Agent - NCB Statement vs GL Activity Reconciliation

This agent compares NCB Bank Statement transactions against GL Activity transactions
to perform actual reconciliation matching and identify discrepancies.
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json
from difflib import SequenceMatcher

# NCB Transaction Mapping from process documentation
NCB_TRANSACTION_MAPPING = {
    "ACH_ADV_FILE": 74530,
    "ACH_ADV_FILE_Orig_CR": 74540,
    "ACH_ADV_FILE_Orig_DB": 74570,
    "RBC_activity": 74400,
    "CNS_Settlement": 74505,
    "EFUNDS_DLY_SETTLE": 74510,
    "EFUNDS_FEE_SETTLE": 74400,
    "PULSE_FEES": 74505,
    "Withdrawal_Coin_Currency": 74400,
    "Image_CL_Presentment_1591": 74520,
    "Image_CL_Presentment_1590": [74560, 74525],
    "ReImage_3091_Returned_Draft": [74560, 74525],
    "Cooperative_Business": 74550,
    "Currency_Exchange_Payment": 74400,
    "ICUL_ServCorp": 74535,
    "CRIF_Select_Corp": 74400,
    "Wires_Deposits": 74400,
    "Cash_Letter_Corr": 74515,
    "OCUL_ACH_NW_Fees": 74400,
    "OCUL_ACH_SB_Fees": 74400,
    "CRIF_Select_Corp_EOM": 74400,
    "Analysis_Service_Charge": 74400,
    "Cooperative_Business_ACH": 74400,
    "VISA_USA_VGBP_COL": 74400
}

def load_gl_activity(file_path):
    """Load and consolidate GL activity from all sheets"""
    print("📊 Loading GL Activity from all sheets...")
    
    try:
        gl_data = pd.read_excel(file_path, sheet_name=None)
        
        consolidated_gl = []
        gl_summary = {}
        
        for sheet_name, df in gl_data.items():
            if sheet_name.startswith('74'):  # GL account sheets
                gl_num = int(sheet_name)
                
                # Add GL number column
                df['GL_Account'] = gl_num
                
                # Standardize date columns
                date_cols = ['Effective Date', 'Actual Date', 'Open Period']
                for col in date_cols:
                    if col in df.columns:
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                
                # Add to consolidated data
                consolidated_gl.append(df)
                
                # Calculate summary for this GL
                debits = pd.to_numeric(df['Debit'], errors='coerce').fillna(0).sum()
                credits = pd.to_numeric(df['Credit'], errors='coerce').fillna(0).sum()
                
                gl_summary[gl_num] = {
                    'debits': debits,
                    'credits': credits,
                    'net_balance': debits + credits,
                    'transaction_count': len(df)
                }
                
                print(f"   ✅ GL {gl_num}: {len(df)} transactions, Net: ${debits + credits:,.2f}")
        
        # Combine all GL data
        if consolidated_gl:
            all_gl_data = pd.concat(consolidated_gl, ignore_index=True)
            print(f"   📊 Total GL transactions: {len(all_gl_data)}")
            return all_gl_data, gl_summary
        else:
            print("   ❌ No GL data found")
            return None, None
            
    except Exception as e:
        print(f"   ❌ Error loading GL activity: {e}")
        return None, None

def load_ncb_statement(file_path):
    """Load NCB bank statement"""
    print("📊 Loading NCB Bank Statement...")
    
    try:
        bank_data = pd.read_excel(file_path)
        
        # Standardize date column
        if 'Post Date' in bank_data.columns:
            bank_data['Post Date'] = pd.to_datetime(bank_data['Post Date'], errors='coerce')
        
        # Calculate net amount for each transaction
        bank_data['Net_Amount'] = pd.to_numeric(bank_data['Debit'], errors='coerce').fillna(0) + pd.to_numeric(bank_data['Credit'], errors='coerce').fillna(0)
        
        print(f"   ✅ NCB Statement: {len(bank_data)} transactions")
        print(f"   📅 Date range: {bank_data['Post Date'].min()} to {bank_data['Post Date'].max()}")
        print(f"   💰 Total net amount: ${bank_data['Net_Amount'].sum():,.2f}")
        
        return bank_data
        
    except Exception as e:
        print(f"   ❌ Error loading NCB statement: {e}")
        return None

def match_transactions_by_amount_and_date(gl_data, bank_data, tolerance=0.01):
    """Match transactions by amount and date with tolerance"""
    print("🔄 Matching transactions by amount and date...")
    
    matches = []
    unmatched_gl = []
    unmatched_bank = []
    
    # Create copies for matching
    gl_remaining = gl_data.copy()
    bank_remaining = bank_data.copy()
    
    for idx, gl_row in gl_data.iterrows():
        gl_debit = pd.to_numeric(gl_row['Debit'], errors='coerce')
        gl_credit = pd.to_numeric(gl_row['Credit'], errors='coerce')
        gl_amount = (gl_debit if not pd.isna(gl_debit) else 0) + (gl_credit if not pd.isna(gl_credit) else 0)
        gl_date = gl_row.get('Effective Date') or gl_row.get('Actual Date')
        
        if pd.isna(gl_date) or gl_amount == 0:
            unmatched_gl.append(gl_row)
            continue
        
        # Find matching bank transaction
        best_match = None
        best_match_idx = None
        best_score = 0
        
        for bank_idx, bank_row in bank_remaining.iterrows():
            bank_amount = bank_row['Net_Amount']
            bank_date = bank_row['Post Date']
            
            if pd.isna(bank_date):
                continue
            
            # Check amount match (within tolerance)
            amount_diff = abs(gl_amount - bank_amount)
            if amount_diff <= tolerance:
                # Check date match (within 3 days)
                date_diff = abs((gl_date - bank_date).days)
                if date_diff <= 3:
                    # Calculate match score
                    amount_score = 1 - (amount_diff / max(abs(gl_amount), abs(bank_amount), 1))
                    date_score = 1 - (date_diff / 3)
                    total_score = (amount_score + date_score) / 2
                    
                    if total_score > best_score:
                        best_score = total_score
                        best_match = bank_row
                        best_match_idx = bank_idx
        
        if best_match is not None and best_score > 0.7:  # 70% match threshold
            matches.append({
                'gl_transaction': gl_row,
                'bank_transaction': best_match,
                'match_score': best_score,
                'amount_difference': abs(gl_amount - best_match['Net_Amount']),
                'date_difference_days': abs((gl_date - best_match['Post Date']).days)
            })
            
            # Remove matched bank transaction
            bank_remaining = bank_remaining.drop(best_match_idx)
        else:
            unmatched_gl.append(gl_row)
    
    # Remaining bank transactions are unmatched
    unmatched_bank = bank_remaining.to_dict('records')
    
    print(f"   ✅ Matches found: {len(matches)}")
    print(f"   ❌ Unmatched GL: {len(unmatched_gl)}")
    print(f"   ❌ Unmatched Bank: {len(unmatched_bank)}")
    
    return matches, unmatched_gl, unmatched_bank

def match_transactions_by_description(gl_data, bank_data):
    """Match transactions by description similarity"""
    print("🔄 Matching transactions by description similarity...")
    
    matches = []
    unmatched_gl = []
    unmatched_bank = []
    
    # Create copies for matching
    gl_remaining = gl_data.copy()
    bank_remaining = bank_data.copy()
    
    for idx, gl_row in gl_data.iterrows():
        gl_desc = str(gl_row.get('Description', '')).lower()
        gl_debit = pd.to_numeric(gl_row['Debit'], errors='coerce')
        gl_credit = pd.to_numeric(gl_row['Credit'], errors='coerce')
        gl_amount = (gl_debit if not pd.isna(gl_debit) else 0) + (gl_credit if not pd.isna(gl_credit) else 0)
        
        if not gl_desc or gl_amount == 0:
            unmatched_gl.append(gl_row)
            continue
        
        # Find matching bank transaction by description
        best_match = None
        best_match_idx = None
        best_score = 0
        
        for bank_idx, bank_row in bank_remaining.iterrows():
            bank_desc = str(bank_row.get('Description', '')).lower()
            bank_amount = bank_row['Net_Amount']
            
            if not bank_desc:
                continue
            
            # Calculate description similarity
            desc_similarity = SequenceMatcher(None, gl_desc, bank_desc).ratio()
            
            # Check if amounts are close (within 10%)
            amount_diff = abs(gl_amount - bank_amount)
            amount_tolerance = max(abs(gl_amount), abs(bank_amount)) * 0.1
            
            if amount_diff <= amount_tolerance and desc_similarity > 0.6:  # 60% description match
                if desc_similarity > best_score:
                    best_score = desc_similarity
                    best_match = bank_row
                    best_match_idx = bank_idx
        
        if best_match is not None:
            matches.append({
                'gl_transaction': gl_row,
                'bank_transaction': best_match,
                'description_similarity': best_score,
                'amount_difference': abs(gl_amount - best_match['Net_Amount'])
            })
            
            # Remove matched bank transaction
            bank_remaining = bank_remaining.drop(best_match_idx)
        else:
            unmatched_gl.append(gl_row)
    
    # Remaining bank transactions are unmatched
    unmatched_bank = bank_remaining.to_dict('records')
    
    print(f"   ✅ Description matches found: {len(matches)}")
    print(f"   ❌ Unmatched GL: {len(unmatched_gl)}")
    print(f"   ❌ Unmatched Bank: {len(unmatched_bank)}")
    
    return matches, unmatched_gl, unmatched_bank

def analyze_reconciliation_results(gl_summary, bank_data, matches, unmatched_gl, unmatched_bank):
    """Analyze reconciliation results and generate summary"""
    print("📊 Analyzing reconciliation results...")
    
    # Calculate totals
    total_gl_debits = sum(gl_summary[gl]['debits'] for gl in gl_summary)
    total_gl_credits = sum(gl_summary[gl]['credits'] for gl in gl_summary)
    total_gl_balance = total_gl_debits + total_gl_credits
    
    total_bank_amount = bank_data['Net_Amount'].sum()
    
    # Calculate matched amounts
    matched_gl_amount = sum(match['gl_transaction']['Debit'] + match['gl_transaction']['Credit'] for match in matches if 'gl_transaction' in match)
    matched_bank_amount = sum(match['bank_transaction']['Net_Amount'] for match in matches if 'bank_transaction' in match)
    
    # Calculate unmatched amounts
    unmatched_gl_amount = 0
    for row in unmatched_gl:
        gl_debit = pd.to_numeric(row['Debit'], errors='coerce')
        gl_credit = pd.to_numeric(row['Credit'], errors='coerce')
        gl_amount = (gl_debit if not pd.isna(gl_debit) else 0) + (gl_credit if not pd.isna(gl_credit) else 0)
        unmatched_gl_amount += gl_amount
    unmatched_bank_amount = sum(row['Net_Amount'] for row in unmatched_bank)
    
    analysis = {
        'timestamp': datetime.now().isoformat(),
        'reconciliation_summary': {
            'total_gl_debits': total_gl_debits,
            'total_gl_credits': total_gl_credits,
            'total_gl_balance': total_gl_balance,
            'total_bank_amount': total_bank_amount,
            'variance': total_gl_balance - total_bank_amount,
            'variance_percentage': ((total_gl_balance - total_bank_amount) / abs(total_gl_balance)) * 100 if total_gl_balance != 0 else 0
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
        'gl_account_summary': gl_summary,
        'matches': matches,
        'unmatched_gl': unmatched_gl,
        'unmatched_bank': unmatched_bank
    }
    
    print(f"   📊 Reconciliation Summary:")
    print(f"      GL Balance: ${total_gl_balance:,.2f}")
    print(f"      Bank Amount: ${total_bank_amount:,.2f}")
    print(f"      Variance: ${total_gl_balance - total_bank_amount:,.2f}")
    print(f"      Matches: {len(matches)}")
    print(f"      Unmatched GL: {len(unmatched_gl)}")
    print(f"      Unmatched Bank: {len(unmatched_bank)}")
    
    return analysis

def main():
    """Main reconciliation function"""
    
    print("🤖 Excel Agent - NCB Statement vs GL Activity Reconciliation")
    print("=" * 60)
    
    # Define file paths
    gl_file = "uploads/17b27999-628f-456c-9039-796bc61cb19d_05 May 2025 Reconciliation and Flex GL Activity.xlsx"
    bank_file = "uploads/0e60826b-b004-4f37-8d57-163661c0d5fc_NCB Bank Activity 5-1 to 5-31 Support for May 2025 Rec.xls"
    
    print(f"📁 GL Activity File: {gl_file}")
    print(f"📁 Bank Statement File: {bank_file}")
    print()
    
    # Check if files exist
    if not os.path.exists(gl_file):
        print(f"❌ GL Activity file not found: {gl_file}")
        return
    
    if not os.path.exists(bank_file):
        print(f"❌ Bank Statement file not found: {bank_file}")
        return
    
    print("✅ Both files found!")
    print()
    
    # Load GL activity
    gl_data, gl_summary = load_gl_activity(gl_file)
    if gl_data is None:
        print("❌ Failed to load GL activity")
        return
    
    print()
    
    # Load NCB statement
    bank_data = load_ncb_statement(bank_file)
    if bank_data is None:
        print("❌ Failed to load NCB statement")
        return
    
    print()
    
    # Match transactions by amount and date
    amount_matches, unmatched_gl_amount, unmatched_bank_amount = match_transactions_by_amount_and_date(gl_data, bank_data)
    print()
    
    # Match remaining transactions by description
    desc_matches, unmatched_gl_desc, unmatched_bank_desc = match_transactions_by_description(
        pd.DataFrame(unmatched_gl_amount), 
        pd.DataFrame(unmatched_bank_amount)
    )
    print()
    
    # Combine all matches
    all_matches = amount_matches + desc_matches
    all_unmatched_gl = unmatched_gl_desc
    all_unmatched_bank = unmatched_bank_desc
    
    # Analyze reconciliation results
    analysis = analyze_reconciliation_results(gl_summary, bank_data, all_matches, all_unmatched_gl, all_unmatched_bank)
    print()
    
    # Save reconciliation report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"data/reports/ncb_gl_reconciliation_{timestamp}.json"
    
    os.makedirs("data/reports", exist_ok=True)
    with open(report_file, 'w') as f:
        json.dump(analysis, f, indent=2, default=str)
    
    print("📄 Reconciliation report saved!")
    print(f"📁 Report location: {report_file}")
    print()
    
    # Display final summary
    summary = analysis['reconciliation_summary']
    matching = analysis['matching_results']
    
    print("📋 RECONCILIATION SUMMARY:")
    print("=" * 30)
    print(f"GL Balance: ${summary['total_gl_balance']:,.2f}")
    print(f"Bank Amount: ${summary['total_bank_amount']:,.2f}")
    print(f"Variance: ${summary['variance']:,.2f} ({summary['variance_percentage']:.2f}%)")
    print(f"Matches Found: {matching['total_matches']}")
    print(f"Unmatched GL: {matching['unmatched_gl_count']} (${matching['unmatched_gl_amount']:,.2f})")
    print(f"Unmatched Bank: {matching['unmatched_bank_count']} (${matching['unmatched_bank_amount']:,.2f})")
    
    print("\n🎉 NCB vs GL reconciliation completed successfully!")

if __name__ == "__main__":
    main()
