#!/usr/bin/env python3
"""
Display AI Reconciliation Report
"""

import json

def main():
    print('📊 AI RECONCILIATION REPORT ANALYSIS')
    print('=' * 50)

    try:
        with open('ai_reconciliation_report.json', 'r') as f:
            report = json.load(f)
        
        print(f'\n📋 AI ANALYSIS SUMMARY:')
        ai_analysis = report['ai_analysis']
        print(f'   GL Accounts Analyzed: {ai_analysis["gl_activity_analyzed"]}')
        print(f'   Total GL Balance: ${ai_analysis["total_gl_balance"]:,.2f}')
        print(f'   Total Debits: ${ai_analysis["total_debits"]:,.2f}')
        print(f'   Total Credits: ${ai_analysis["total_credits"]:,.2f}')
        print(f'   Is Balanced: {ai_analysis["is_balanced"]}')
        print(f'   Reconciliation Status: {report["reconciliation_status"]}')
        
        print(f'\n💰 GL ACCOUNT ANALYSIS:')
        for gl_num, gl_data in report['gl_analysis'].items():
            print(f'   GL {gl_num} ({gl_data["name"]}):')
            print(f'      Balance: ${gl_data["balance"]:,.2f}')
            print(f'      Debits: ${gl_data["debits"]:,.2f}')
            print(f'      Credits: ${gl_data["credits"]:,.2f}')
            print(f'      Transactions: {gl_data["transaction_count"]}')
        
        print(f'\n💡 AI RECOMMENDATIONS:')
        for i, rec in enumerate(report['recommendations'], 1):
            print(f'   {i}. {rec}')
        
        print(f'\n🎯 AI CONCLUSION:')
        if report['reconciliation_status'] == 'COMPLETE':
            print('   ✅ Perfect reconciliation achieved!')
        else:
            print(f'   ⚠️ Reconciliation imbalanced by ${ai_analysis["total_gl_balance"]:,.2f}')
            print('   🔍 AI recommends cross-referencing with bank statement')

    except FileNotFoundError:
        print('❌ AI reconciliation report not found')
    except Exception as e:
        print(f'❌ Error reading report: {e}')

if __name__ == "__main__":
    main()
