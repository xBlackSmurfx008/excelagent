#!/usr/bin/env python3
"""
Excel Agent - Detailed NCB Statement & Flex Activity Analysis

This script performs detailed analysis with proper column detection for the NCB Bank Statement and Flex GL Activity files.
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json

def analyze_gl_activity_detailed(file_path):
    """Analyze GL Activity file with detailed column detection"""
    print("📊 Analyzing GL Activity file (detailed)...")
    
    try:
        # Read all sheets
        gl_data = pd.read_excel(file_path, sheet_name=None)
        
        analysis = {
            "file_path": file_path,
            "total_sheets": len(gl_data),
            "sheets": {},
            "summary": {}
        }
        
        total_debits = 0
        total_credits = 0
        total_transactions = 0
        
        for sheet_name, df in gl_data.items():
            if sheet_name.startswith('74'):  # GL account sheets
                print(f"   📋 Analyzing sheet {sheet_name}...")
                
                sheet_analysis = {
                    "rows": len(df),
                    "columns": list(df.columns),
                    "debits": 0,
                    "credits": 0,
                    "net_balance": 0,
                    "sample_data": df.head(3).to_dict('records') if len(df) > 0 else []
                }
                
                # Look for amount columns (case insensitive)
                amount_columns = []
                for col in df.columns:
                    if any(keyword in col.lower() for keyword in ['amount', 'debit', 'credit', 'balance']):
                        amount_columns.append(col)
                
                print(f"      Columns: {list(df.columns)}")
                print(f"      Amount columns found: {amount_columns}")
                
                if amount_columns:
                    # Try each amount column
                    for col in amount_columns:
                        try:
                            amounts = pd.to_numeric(df[col], errors='coerce').fillna(0)
                            if amounts.sum() != 0:  # If this column has non-zero values
                                debits = amounts[amounts > 0].sum()
                                credits = amounts[amounts < 0].sum()
                                
                                sheet_analysis["debits"] = debits
                                sheet_analysis["credits"] = credits
                                sheet_analysis["net_balance"] = debits + credits
                                sheet_analysis["amount_column_used"] = col
                                
                                total_debits += debits
                                total_credits += credits
                                total_transactions += len(df[amounts != 0])
                                
                                print(f"      ✅ Using column '{col}': Debits=${debits:,.2f}, Credits=${credits:,.2f}")
                                break
                        except Exception as e:
                            print(f"      ⚠️ Error with column '{col}': {e}")
                            continue
                
                # If no amount columns found, try to find numeric columns
                if sheet_analysis["debits"] == 0 and sheet_analysis["credits"] == 0:
                    numeric_cols = df.select_dtypes(include=[np.number]).columns
                    if len(numeric_cols) > 0:
                        print(f"      🔍 Trying numeric columns: {list(numeric_cols)}")
                        for col in numeric_cols:
                            try:
                                amounts = df[col].fillna(0)
                                if amounts.sum() != 0:
                                    debits = amounts[amounts > 0].sum()
                                    credits = amounts[amounts < 0].sum()
                                    
                                    sheet_analysis["debits"] = debits
                                    sheet_analysis["credits"] = credits
                                    sheet_analysis["net_balance"] = debits + credits
                                    sheet_analysis["amount_column_used"] = col
                                    
                                    total_debits += debits
                                    total_credits += credits
                                    total_transactions += len(df[amounts != 0])
                                    
                                    print(f"      ✅ Using numeric column '{col}': Debits=${debits:,.2f}, Credits=${credits:,.2f}")
                                    break
                            except Exception as e:
                                print(f"      ⚠️ Error with numeric column '{col}': {e}")
                                continue
                
                analysis["sheets"][sheet_name] = sheet_analysis
        
        analysis["summary"] = {
            "total_debits": total_debits,
            "total_credits": total_credits,
            "net_balance": total_debits + total_credits,
            "total_transactions": total_transactions
        }
        
        print(f"   ✅ Sheets analyzed: {len(gl_data)}")
        print(f"   💰 Total Debits: ${total_debits:,.2f}")
        print(f"   💰 Total Credits: ${total_credits:,.2f}")
        print(f"   ⚖️ Net Balance: ${total_debits + total_credits:,.2f}")
        print(f"   📊 Total Transactions: {total_transactions:,}")
        
        return analysis
        
    except Exception as e:
        print(f"   ❌ Error analyzing GL Activity: {e}")
        return None

def analyze_bank_statement_detailed(file_path):
    """Analyze Bank Statement file with detailed column detection"""
    print("📊 Analyzing Bank Statement file (detailed)...")
    
    try:
        # Read bank statement
        bank_data = pd.read_excel(file_path)
        
        print(f"   📋 Bank statement columns: {list(bank_data.columns)}")
        print(f"   📊 Bank statement shape: {bank_data.shape}")
        
        analysis = {
            "file_path": file_path,
            "total_transactions": len(bank_data),
            "columns": list(bank_data.columns),
            "date_range": {},
            "amount_analysis": {},
            "sample_data": bank_data.head(3).to_dict('records')
        }
        
        # Date analysis
        date_columns = [col for col in bank_data.columns if 'date' in col.lower()]
        if date_columns:
            date_col = date_columns[0]
            dates = pd.to_datetime(bank_data[date_col], errors='coerce')
            analysis["date_range"] = {
                "start_date": dates.min().strftime('%Y-%m-%d') if not dates.isna().all() else "Unknown",
                "end_date": dates.max().strftime('%Y-%m-%d') if not dates.isna().all() else "Unknown",
                "total_days": (dates.max() - dates.min()).days if not dates.isna().all() else 0,
                "date_column_used": date_col
            }
            print(f"   📅 Date range: {analysis['date_range']['start_date']} to {analysis['date_range']['end_date']}")
        
        # Amount analysis
        amount_columns = [col for col in bank_data.columns if any(keyword in col.lower() for keyword in ['amount', 'debit', 'credit', 'balance'])]
        if amount_columns:
            amount_col = amount_columns[0]
            amounts = pd.to_numeric(bank_data[amount_col], errors='coerce').fillna(0)
            analysis["amount_analysis"] = {
                "total_amount": amounts.sum(),
                "average_amount": amounts.mean(),
                "max_amount": amounts.max(),
                "min_amount": amounts.min(),
                "positive_transactions": len(amounts[amounts > 0]),
                "negative_transactions": len(amounts[amounts < 0]),
                "amount_column_used": amount_col
            }
            print(f"   💰 Total amount: ${amounts.sum():,.2f}")
            print(f"   📊 Avg transaction: ${amounts.mean():,.2f}")
        else:
            # Try numeric columns
            numeric_cols = bank_data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                amount_col = numeric_cols[0]
                amounts = bank_data[amount_col].fillna(0)
                analysis["amount_analysis"] = {
                    "total_amount": amounts.sum(),
                    "average_amount": amounts.mean(),
                    "max_amount": amounts.max(),
                    "min_amount": amounts.min(),
                    "positive_transactions": len(amounts[amounts > 0]),
                    "negative_transactions": len(amounts[amounts < 0]),
                    "amount_column_used": amount_col
                }
                print(f"   💰 Total amount (numeric): ${amounts.sum():,.2f}")
                print(f"   📊 Avg transaction: ${amounts.mean():,.2f}")
        
        print(f"   ✅ Transactions analyzed: {len(bank_data):,}")
        
        return analysis
        
    except Exception as e:
        print(f"   ❌ Error analyzing Bank Statement: {e}")
        return None

def main():
    """Main analysis function"""
    
    print("🤖 Excel Agent - Detailed NCB Statement & Flex Activity Analysis")
    print("=" * 70)
    
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
    
    # Analyze GL Activity with detailed detection
    gl_analysis = analyze_gl_activity_detailed(gl_file)
    print()
    
    # Analyze Bank Statement with detailed detection
    bank_analysis = analyze_bank_statement_detailed(bank_file)
    print()
    
    # Save detailed report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"data/reports/detailed_ncb_flex_analysis_{timestamp}.json"
    
    os.makedirs("data/reports", exist_ok=True)
    
    detailed_report = {
        "timestamp": timestamp,
        "gl_analysis": gl_analysis,
        "bank_analysis": bank_analysis,
        "analysis_type": "detailed_column_detection"
    }
    
    with open(report_file, 'w') as f:
        json.dump(detailed_report, f, indent=2, default=str)
    
    print("📄 Detailed report saved!")
    print(f"📁 Report location: {report_file}")
    print()
    
    # Display summary
    if gl_analysis and bank_analysis:
        print("📋 ANALYSIS SUMMARY:")
        print("=" * 20)
        print(f"GL Sheets: {gl_analysis['total_sheets']}")
        print(f"GL Transactions: {gl_analysis['summary']['total_transactions']:,}")
        print(f"GL Net Balance: ${gl_analysis['summary']['net_balance']:,.2f}")
        print(f"Bank Transactions: {bank_analysis['total_transactions']:,}")
        if bank_analysis['amount_analysis']:
            print(f"Bank Total: ${bank_analysis['amount_analysis']['total_amount']:,.2f}")
    
    print("\n🎉 Detailed analysis completed successfully!")

if __name__ == "__main__":
    main()
