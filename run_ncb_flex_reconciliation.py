#!/usr/bin/env python3
"""
Excel Agent - NCB Statement & Flex Activity Reconciliation Runner

This script runs the Excel Agent on the NCB Bank Statement and Flex GL Activity files.
"""

import os
import sys
import pandas as pd
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    """Run Excel Agent on NCB Statement and Flex Activity files"""
    
    print("🤖 Excel Agent - NCB Statement & Flex Activity Reconciliation")
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
    
    try:
        # Try to import and run the AI reconciliation agent
        from excel_agent.core.A_ai_reconciliation_agent import AIReconciliationAgent
        
        print("🧠 Initializing AI Reconciliation Agent...")
        agent = AIReconciliationAgent()
        
        print("🔄 Running reconciliation analysis...")
        result = agent.think_and_analyze(gl_file, bank_file)
        
        print("✅ Reconciliation completed!")
        print(f"📊 Status: {result.get('reconciliation_status', 'Unknown')}")
        print(f"💰 Total GL Balance: ${result.get('ai_analysis', {}).get('total_gl_balance', 0):,.2f}")
        
        # Save results
        import json
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"data/reports/ncb_flex_reconciliation_{timestamp}.json"
        
        os.makedirs("data/reports", exist_ok=True)
        with open(report_file, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        
        print(f"📄 Report saved: {report_file}")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("🔄 Trying alternative approach...")
        
        # Alternative: Use pandas to analyze the files
        try:
            print("📊 Analyzing GL Activity file...")
            gl_data = pd.read_excel(gl_file, sheet_name=None)
            print(f"   Sheets found: {list(gl_data.keys())}")
            
            print("📊 Analyzing Bank Statement file...")
            bank_data = pd.read_excel(bank_file)
            print(f"   Bank transactions: {len(bank_data)}")
            
            print("✅ File analysis completed!")
            print("📋 Summary:")
            print(f"   - GL Sheets: {len(gl_data)}")
            print(f"   - Bank Transactions: {len(bank_data)}")
            
        except Exception as e2:
            print(f"❌ Analysis error: {e2}")
    
    except Exception as e:
        print(f"❌ Error running reconciliation: {e}")

if __name__ == "__main__":
    main()
