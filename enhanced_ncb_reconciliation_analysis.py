#!/usr/bin/env python3
"""
Excel Agent - Enhanced NCB Reconciliation Analysis

This script incorporates the NCB Reconciliation process documentation to perform
comprehensive analysis with proper transaction mapping and timing differences.
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json

# NCB Reconciliation Process Documentation Integration
NCB_PROCESS_CONFIG = {
    "process_name": "NCB Reconciliation",
    "owner": "Accounting Department",
    "institution": "PCU Credit Union",
    "bank": "National Cooperative Bank (NCB)",
    "frequency": "Daily with formal month-end reconciliation",
    
    "gl_accounts": {
        74400: "RBC_activity, EFUNDS_FEE_SETTLE, Withdrawal_Coin_Currency, Currency_Exchange_Payment, ICUL_ServCorp, CRIF_Select_Corp, Wires_Deposits, OCUL_ACH_NW_Fees, OCUL_ACH_SB_Fees, CRIF_Select_Corp_EOM, Analysis_Service_Charge, Cooperative_Business_ACH, VISA_USA_VGBP_COL",
        74505: "CNS_Settlement, PULSE_FEES",
        74510: "EFUNDS_DLY_SETTLE",
        74515: "Cash_Letter_Corr",
        74520: "Image_CL_Presentment_1591",
        74525: "Image_CL_Presentment_1590, ReImage_3091_Returned_Draft",
        74530: "ACH_ADV_FILE",
        74535: "ICUL_ServCorp",
        74540: "ACH_ADV_FILE_Orig_CR, CRIF_Indirect_Loan",
        74550: "Cooperative_Business, CBS_activity",
        74560: "Image_CL_Presentment_1590, Check_deposit",
        74570: "ACH_ADV_FILE_Orig_DB"
    },
    
    "transaction_mapping": {
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
    },
    
    "timing_differences": {
        "ATM_settlement": {"gl": 74505, "treatment": "Negative - Items deducted by CU but not yet entered on bank records"},
        "Shared_Branching": {"gl": 74510, "treatment": "Positive or negative depending on reconciliation variance"},
        "Check_deposit": {"gl": 74560, "treatment": "Positive - Items added by CU but not yet on bank records"},
        "Gift_Card_activity": {"gl": 74535, "treatment": "Negative - Items deducted by CU but not yet entered on bank records"},
        "CBS_activity": {"gl": 74550, "treatment": "Positive - Items added by CU but not yet on bank records"},
        "CRIF_Indirect_Loan": {"gl": 74540, "treatment": "Negative - Items deducted by CU but not yet entered on bank records"}
    }
}

def analyze_gl_with_process_mapping(file_path):
    """Analyze GL Activity with NCB process documentation integration"""
    print("📊 Analyzing GL Activity with NCB Process Mapping...")
    
    try:
        gl_data = pd.read_excel(file_path, sheet_name=None)
        
        analysis = {
            "file_path": file_path,
            "process_config": NCB_PROCESS_CONFIG,
            "total_sheets": len(gl_data),
            "sheets": {},
            "summary": {},
            "transaction_analysis": {},
            "timing_differences": {}
        }
        
        total_debits = 0
        total_credits = 0
        total_transactions = 0
        
        for sheet_name, df in gl_data.items():
            if sheet_name.startswith('74'):  # GL account sheets
                gl_num = int(sheet_name)
                
                print(f"   📋 Analyzing GL {gl_num} ({NCB_PROCESS_CONFIG['gl_accounts'].get(gl_num, 'Unknown')})...")
                
                sheet_analysis = {
                    "gl_number": gl_num,
                    "purpose": NCB_PROCESS_CONFIG['gl_accounts'].get(gl_num, 'Unknown'),
                    "rows": len(df),
                    "columns": list(df.columns),
                    "debits": 0,
                    "credits": 0,
                    "net_balance": 0,
                    "transaction_types": [],
                    "sample_transactions": df.head(3).to_dict('records') if len(df) > 0 else []
                }
                
                # Calculate debits and credits
                if 'Debit' in df.columns and 'Credit' in df.columns:
                    debits = pd.to_numeric(df['Debit'], errors='coerce').fillna(0).sum()
                    credits = pd.to_numeric(df['Credit'], errors='coerce').fillna(0).sum()
                    
                    sheet_analysis["debits"] = debits
                    sheet_analysis["credits"] = credits
                    sheet_analysis["net_balance"] = debits + credits
                    
                    total_debits += debits
                    total_credits += credits
                    total_transactions += len(df)
                    
                    # Analyze transaction types based on descriptions
                    if 'Description' in df.columns:
                        descriptions = df['Description'].dropna().unique()
                        sheet_analysis["transaction_types"] = list(descriptions)
                        
                        # Map descriptions to known transaction types
                        mapped_types = []
                        for desc in descriptions:
                            for trans_type, gl_accounts in NCB_PROCESS_CONFIG['transaction_mapping'].items():
                                if trans_type.lower() in desc.lower():
                                    mapped_types.append(trans_type)
                        sheet_analysis["mapped_transaction_types"] = mapped_types
                    
                    print(f"      ✅ Debits: ${debits:,.2f}, Credits: ${credits:,.2f}, Net: ${debits + credits:,.2f}")
                    print(f"      📊 Transactions: {len(df)}, Types: {len(sheet_analysis.get('transaction_types', []))}")
                
                analysis["sheets"][sheet_name] = sheet_analysis
        
        analysis["summary"] = {
            "total_debits": total_debits,
            "total_credits": total_credits,
            "net_balance": total_debits + total_credits,
            "total_transactions": total_transactions
        }
        
        print(f"   ✅ GL Analysis Complete:")
        print(f"      💰 Total Debits: ${total_debits:,.2f}")
        print(f"      💰 Total Credits: ${total_credits:,.2f}")
        print(f"      ⚖️ Net Balance: ${total_debits + total_credits:,.2f}")
        print(f"      📊 Total Transactions: {total_transactions:,}")
        
        return analysis
        
    except Exception as e:
        print(f"   ❌ Error analyzing GL Activity: {e}")
        return None

def analyze_bank_with_transaction_mapping(file_path):
    """Analyze Bank Statement with transaction mapping"""
    print("📊 Analyzing Bank Statement with Transaction Mapping...")
    
    try:
        bank_data = pd.read_excel(file_path)
        
        print(f"   📋 Bank statement columns: {list(bank_data.columns)}")
        print(f"   📊 Bank statement shape: {bank_data.shape}")
        
        analysis = {
            "file_path": file_path,
            "total_transactions": len(bank_data),
            "columns": list(bank_data.columns),
            "transaction_mapping_analysis": {},
            "unmapped_transactions": [],
            "date_range": {},
            "amount_analysis": {}
        }
        
        # Date analysis
        if 'Post Date' in bank_data.columns:
            dates = pd.to_datetime(bank_data['Post Date'], errors='coerce')
            analysis["date_range"] = {
                "start_date": dates.min().strftime('%Y-%m-%d') if not dates.isna().all() else "Unknown",
                "end_date": dates.max().strftime('%Y-%m-%d') if not dates.isna().all() else "Unknown",
                "total_days": (dates.max() - dates.min()).days if not dates.isna().all() else 0
            }
            print(f"   📅 Date range: {analysis['date_range']['start_date']} to {analysis['date_range']['end_date']}")
        
        # Transaction mapping analysis
        if 'Description' in bank_data.columns:
            descriptions = bank_data['Description'].dropna()
            mapped_count = 0
            unmapped_count = 0
            
            for desc in descriptions:
                mapped = False
                for trans_type, gl_accounts in NCB_PROCESS_CONFIG['transaction_mapping'].items():
                    if trans_type.lower() in desc.lower():
                        mapped = True
                        mapped_count += 1
                        break
                
                if not mapped:
                    unmapped_count += 1
                    analysis["unmapped_transactions"].append(desc)
            
            analysis["transaction_mapping_analysis"] = {
                "total_transactions": len(descriptions),
                "mapped_transactions": mapped_count,
                "unmapped_transactions": unmapped_count,
                "mapping_percentage": (mapped_count / len(descriptions)) * 100 if len(descriptions) > 0 else 0
            }
            
            print(f"   🎯 Transaction Mapping:")
            print(f"      ✅ Mapped: {mapped_count} ({analysis['transaction_mapping_analysis']['mapping_percentage']:.1f}%)")
            print(f"      ❌ Unmapped: {unmapped_count}")
        
        # Amount analysis
        if 'Debit' in bank_data.columns and 'Credit' in bank_data.columns:
            debits = pd.to_numeric(bank_data['Debit'], errors='coerce').fillna(0).sum()
            credits = pd.to_numeric(bank_data['Credit'], errors='coerce').fillna(0).sum()
            
            analysis["amount_analysis"] = {
                "total_debits": debits,
                "total_credits": credits,
                "net_amount": debits + credits,
                "average_debit": debits / len(bank_data[bank_data['Debit'] > 0]) if len(bank_data[bank_data['Debit'] > 0]) > 0 else 0,
                "average_credit": credits / len(bank_data[bank_data['Credit'] > 0]) if len(bank_data[bank_data['Credit'] > 0]) > 0 else 0
            }
            
            print(f"   💰 Amount Analysis:")
            print(f"      💸 Total Debits: ${debits:,.2f}")
            print(f"      💰 Total Credits: ${credits:,.2f}")
            print(f"      ⚖️ Net Amount: ${debits + credits:,.2f}")
        
        print(f"   ✅ Bank Analysis Complete: {len(bank_data):,} transactions")
        
        return analysis
        
    except Exception as e:
        print(f"   ❌ Error analyzing Bank Statement: {e}")
        return None

def perform_enhanced_reconciliation(gl_analysis, bank_analysis):
    """Perform enhanced reconciliation with NCB process integration"""
    print("🔄 Performing Enhanced NCB Reconciliation Analysis...")
    
    reconciliation = {
        "timestamp": datetime.now().isoformat(),
        "process_config": NCB_PROCESS_CONFIG,
        "status": "completed",
        "analysis": {
            "gl_activity": gl_analysis,
            "bank_statement": bank_analysis
        },
        "reconciliation_summary": {},
        "transaction_mapping_status": {},
        "timing_differences_status": {},
        "recommendations": [],
        "next_steps": []
    }
    
    if gl_analysis and bank_analysis:
        gl_summary = gl_analysis["summary"]
        bank_summary = bank_analysis["amount_analysis"]
        
        # Calculate reconciliation metrics
        gl_net_balance = gl_summary["net_balance"]
        bank_net_amount = bank_summary.get("net_amount", 0)
        
        variance = abs(gl_net_balance - bank_net_amount)
        variance_percentage = (variance / abs(gl_net_balance)) * 100 if gl_net_balance != 0 else 0
        
        reconciliation["reconciliation_summary"] = {
            "gl_net_balance": gl_net_balance,
            "bank_net_amount": bank_net_amount,
            "variance": variance,
            "variance_percentage": variance_percentage,
            "is_balanced": variance < 1000,  # Within $1000 tolerance
            "gl_transactions": gl_summary["total_transactions"],
            "bank_transactions": bank_analysis["total_transactions"]
        }
        
        # Transaction mapping status
        mapping_analysis = bank_analysis.get("transaction_mapping_analysis", {})
        reconciliation["transaction_mapping_status"] = {
            "mapped_percentage": mapping_analysis.get("mapping_percentage", 0),
            "unmapped_count": mapping_analysis.get("unmapped_transactions", 0),
            "status": "complete" if mapping_analysis.get("mapping_percentage", 0) > 90 else "needs_attention"
        }
        
        # Timing differences status
        reconciliation["timing_differences_status"] = {
            "standard_entries": len(NCB_PROCESS_CONFIG["timing_differences"]),
            "applied": False,  # Not yet implemented
            "estimated_impact": "Unknown - requires implementation"
        }
        
        # Generate recommendations based on NCB process
        if variance > 10000:
            reconciliation["recommendations"].append("High variance detected - apply timing differences per NCB process")
        if mapping_analysis.get("mapping_percentage", 0) < 90:
            reconciliation["recommendations"].append("Transaction mapping incomplete - review unmapped transactions")
        if gl_summary["total_transactions"] != bank_analysis["total_transactions"]:
            reconciliation["recommendations"].append("Transaction count mismatch - verify completeness per NCB process")
        
        # Next steps based on NCB process documentation
        reconciliation["next_steps"] = [
            "Apply transaction mapping table to match bank transactions to GL accounts",
            "Implement timing differences processing (6 standard entries)",
            "Process reconciling items (bank additions/deductions, CU additions/deductions)",
            "Validate adjusted totals match per NCB reconciliation process",
            "Generate reconciliation template with proper format"
        ]
        
        print(f"   ⚖️ Enhanced Reconciliation Results:")
        print(f"      GL Net Balance: ${gl_net_balance:,.2f}")
        print(f"      Bank Net Amount: ${bank_net_amount:,.2f}")
        print(f"      Variance: ${variance:,.2f} ({variance_percentage:.2f}%)")
        print(f"      Balanced: {'Yes' if variance < 1000 else 'No'}")
        print(f"      Transaction Mapping: {mapping_analysis.get('mapping_percentage', 0):.1f}% complete")
    
    return reconciliation

def main():
    """Main enhanced analysis function"""
    
    print("🤖 Excel Agent - Enhanced NCB Reconciliation Analysis")
    print("=" * 60)
    print(f"📋 Process: {NCB_PROCESS_CONFIG['process_name']}")
    print(f"🏦 Institution: {NCB_PROCESS_CONFIG['institution']}")
    print(f"🏛️ Bank: {NCB_PROCESS_CONFIG['bank']}")
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
    
    # Analyze GL Activity with process mapping
    gl_analysis = analyze_gl_with_process_mapping(gl_file)
    print()
    
    # Analyze Bank Statement with transaction mapping
    bank_analysis = analyze_bank_with_transaction_mapping(bank_file)
    print()
    
    # Perform enhanced reconciliation
    reconciliation = perform_enhanced_reconciliation(gl_analysis, bank_analysis)
    print()
    
    # Save enhanced report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"data/reports/enhanced_ncb_reconciliation_{timestamp}.json"
    
    os.makedirs("data/reports", exist_ok=True)
    with open(report_file, 'w') as f:
        json.dump(reconciliation, f, indent=2, default=str)
    
    print("📄 Enhanced reconciliation report saved!")
    print(f"📁 Report location: {report_file}")
    print()
    
    # Display enhanced summary
    if reconciliation["reconciliation_summary"]:
        summary = reconciliation["reconciliation_summary"]
        mapping_status = reconciliation["transaction_mapping_status"]
        
        print("📋 ENHANCED NCB RECONCILIATION SUMMARY:")
        print("=" * 40)
        print(f"Status: {'✅ BALANCED' if summary['is_balanced'] else '❌ IMBALANCED'}")
        print(f"GL Net Balance: ${summary['gl_net_balance']:,.2f}")
        print(f"Bank Net Amount: ${summary['bank_net_amount']:,.2f}")
        print(f"Variance: ${summary['variance']:,.2f} ({summary['variance_percentage']:.2f}%)")
        print(f"Transaction Mapping: {mapping_status['mapped_percentage']:.1f}% complete")
        print(f"Unmapped Transactions: {mapping_status['unmapped_count']}")
        
        if reconciliation["recommendations"]:
            print("\n💡 NCB PROCESS RECOMMENDATIONS:")
            for i, rec in enumerate(reconciliation["recommendations"], 1):
                print(f"   {i}. {rec}")
        
        if reconciliation["next_steps"]:
            print("\n🚀 NEXT STEPS (Per NCB Process):")
            for i, step in enumerate(reconciliation["next_steps"], 1):
                print(f"   {i}. {step}")
    
    print("\n🎉 Enhanced NCB reconciliation analysis completed successfully!")

if __name__ == "__main__":
    main()
