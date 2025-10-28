#!/usr/bin/env python3
"""
Excel Agent - Comprehensive NCB Statement & Flex Activity Analysis

This script performs comprehensive analysis of the NCB Bank Statement and Flex GL Activity files.
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json

def analyze_gl_activity(file_path):
    """Analyze GL Activity file"""
    print("📊 Analyzing GL Activity file...")
    
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
                sheet_analysis = {
                    "rows": len(df),
                    "columns": list(df.columns),
                    "debits": 0,
                    "credits": 0,
                    "net_balance": 0
                }
                
                # Calculate debits and credits
                if 'Amount' in df.columns:
                    amounts = pd.to_numeric(df['Amount'], errors='coerce').fillna(0)
                    debits = amounts[amounts > 0].sum()
                    credits = amounts[amounts < 0].sum()
                    
                    sheet_analysis["debits"] = debits
                    sheet_analysis["credits"] = credits
                    sheet_analysis["net_balance"] = debits + credits
                    
                    total_debits += debits
                    total_credits += credits
                    total_transactions += len(df)
                
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

def analyze_bank_statement(file_path):
    """Analyze Bank Statement file"""
    print("📊 Analyzing Bank Statement file...")
    
    try:
        # Read bank statement
        bank_data = pd.read_excel(file_path)
        
        analysis = {
            "file_path": file_path,
            "total_transactions": len(bank_data),
            "columns": list(bank_data.columns),
            "date_range": {},
            "amount_analysis": {}
        }
        
        # Date analysis
        if 'Date' in bank_data.columns:
            dates = pd.to_datetime(bank_data['Date'], errors='coerce')
            analysis["date_range"] = {
                "start_date": dates.min().strftime('%Y-%m-%d') if not dates.isna().all() else "Unknown",
                "end_date": dates.max().strftime('%Y-%m-%d') if not dates.isna().all() else "Unknown",
                "total_days": (dates.max() - dates.min()).days if not dates.isna().all() else 0
            }
        
        # Amount analysis
        if 'Amount' in bank_data.columns:
            amounts = pd.to_numeric(bank_data['Amount'], errors='coerce').fillna(0)
            analysis["amount_analysis"] = {
                "total_amount": amounts.sum(),
                "average_amount": amounts.mean(),
                "max_amount": amounts.max(),
                "min_amount": amounts.min(),
                "positive_transactions": len(amounts[amounts > 0]),
                "negative_transactions": len(amounts[amounts < 0])
            }
        
        print(f"   ✅ Transactions analyzed: {len(bank_data):,}")
        print(f"   📅 Date range: {analysis['date_range'].get('start_date', 'Unknown')} to {analysis['date_range'].get('end_date', 'Unknown')}")
        if analysis["amount_analysis"]:
            print(f"   💰 Total amount: ${analysis['amount_analysis']['total_amount']:,.2f}")
            print(f"   📊 Avg transaction: ${analysis['amount_analysis']['average_amount']:,.2f}")
        
        return analysis
        
    except Exception as e:
        print(f"   ❌ Error analyzing Bank Statement: {e}")
        return None

def perform_reconciliation_analysis(gl_analysis, bank_analysis):
    """Perform reconciliation analysis"""
    print("🔄 Performing reconciliation analysis...")
    
    reconciliation = {
        "timestamp": datetime.now().isoformat(),
        "status": "completed",
        "analysis": {
            "gl_activity": gl_analysis,
            "bank_statement": bank_analysis
        },
        "reconciliation_summary": {},
        "recommendations": []
    }
    
    if gl_analysis and bank_analysis:
        gl_summary = gl_analysis["summary"]
        bank_summary = bank_analysis["amount_analysis"]
        
        # Calculate reconciliation metrics
        gl_net_balance = gl_summary["net_balance"]
        bank_total = bank_summary.get("total_amount", 0)
        
        variance = abs(gl_net_balance - bank_total)
        variance_percentage = (variance / abs(gl_net_balance)) * 100 if gl_net_balance != 0 else 0
        
        reconciliation["reconciliation_summary"] = {
            "gl_net_balance": gl_net_balance,
            "bank_total_amount": bank_total,
            "variance": variance,
            "variance_percentage": variance_percentage,
            "is_balanced": variance < 1000,  # Within $1000 tolerance
            "gl_transactions": gl_summary["total_transactions"],
            "bank_transactions": bank_analysis["total_transactions"]
        }
        
        # Generate recommendations
        if variance > 10000:
            reconciliation["recommendations"].append("High variance detected - requires detailed investigation")
        if variance_percentage > 5:
            reconciliation["recommendations"].append("Significant percentage variance - review transaction matching")
        if gl_summary["total_transactions"] != bank_analysis["total_transactions"]:
            reconciliation["recommendations"].append("Transaction count mismatch - verify completeness")
        
        print(f"   ⚖️ GL Net Balance: ${gl_net_balance:,.2f}")
        print(f"   💰 Bank Total: ${bank_total:,.2f}")
        print(f"   📊 Variance: ${variance:,.2f} ({variance_percentage:.2f}%)")
        print(f"   ✅ Balanced: {'Yes' if variance < 1000 else 'No'}")
    
    return reconciliation

def main():
    """Main analysis function"""
    
    print("🤖 Excel Agent - Comprehensive NCB Statement & Flex Activity Analysis")
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
    
    # Analyze GL Activity
    gl_analysis = analyze_gl_activity(gl_file)
    print()
    
    # Analyze Bank Statement
    bank_analysis = analyze_bank_statement(bank_file)
    print()
    
    # Perform reconciliation
    reconciliation = perform_reconciliation_analysis(gl_analysis, bank_analysis)
    print()
    
    # Save comprehensive report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"data/reports/comprehensive_ncb_flex_analysis_{timestamp}.json"
    
    os.makedirs("data/reports", exist_ok=True)
    with open(report_file, 'w') as f:
        json.dump(reconciliation, f, indent=2, default=str)
    
    print("📄 Comprehensive report saved!")
    print(f"📁 Report location: {report_file}")
    print()
    
    # Display summary
    if reconciliation["reconciliation_summary"]:
        summary = reconciliation["reconciliation_summary"]
        print("📋 RECONCILIATION SUMMARY:")
        print("=" * 30)
        print(f"Status: {'✅ BALANCED' if summary['is_balanced'] else '❌ IMBALANCED'}")
        print(f"GL Net Balance: ${summary['gl_net_balance']:,.2f}")
        print(f"Bank Total: ${summary['bank_total_amount']:,.2f}")
        print(f"Variance: ${summary['variance']:,.2f} ({summary['variance_percentage']:.2f}%)")
        print(f"GL Transactions: {summary['gl_transactions']:,}")
        print(f"Bank Transactions: {summary['bank_transactions']:,}")
        
        if reconciliation["recommendations"]:
            print("\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(reconciliation["recommendations"], 1):
                print(f"   {i}. {rec}")
    
    print("\n🎉 Analysis completed successfully!")

if __name__ == "__main__":
    main()
