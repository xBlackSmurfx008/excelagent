#!/usr/bin/env python3
"""
Show detailed analysis report from orchestrated analysis
"""

import json

def main():
    print('📊 DETAILED ANALYSIS REPORT:')
    print('=========================')
    
    try:
        with open('orchestrated_analysis_report.json', 'r') as f:
            report = json.load(f)

        print('📋 EXECUTIVE SUMMARY:')
        summary = report.get('summary', {})
        for key, value in summary.items():
            if isinstance(value, float):
                print(f'   {key}: ${value:,.2f}')
            else:
                print(f'   {key}: {value}')

        print()
        print('🔍 DETAILED FINDINGS:')
        validation = report.get('validation', {})
        verification = validation.get('verification', {})
        if 'imbalanced_accounts' in verification:
            imbalanced = verification['imbalanced_accounts']
            print(f'   Imbalanced Accounts: {len(imbalanced)}')
            for account in imbalanced[:5]:  # Show first 5
                print(f'      - GL {account["gl"]}: ${account["balance"]:,.2f} ({account["type"]})')
            if len(imbalanced) > 5:
                print(f'      ... and {len(imbalanced) - 5} more imbalanced accounts')

        discrepancies = report.get('discrepancies', [])
        print(f'   File Discrepancies: {len(discrepancies)}')
        for disc in discrepancies[:3]:  # Show first 3
            print(f'      - {disc.get("description", "Unknown discrepancy")}')
        if len(discrepancies) > 3:
            print(f'      ... and {len(discrepancies) - 3} more discrepancies')

        print()
        print('📁 FILE ANALYSIS:')
        file_analysis = report.get('file_analysis', {})
        files = file_analysis.get('files', [])
        print(f'   Total Files: {len(files)}')
        reconciliation_files = [f for f in files if f.get('reconciliation_indicators')]
        print(f'   Reconciliation Files: {len(reconciliation_files)}')
        gl_files = [f for f in files if f.get('gl_sheets')]
        print(f'   GL Files: {len(gl_files)}')

        print()
        print('💰 GL BALANCE SUMMARY:')
        reconciliation = report.get('reconciliation', {})
        gl_balances = reconciliation.get('gl_balances', {})
        print(f'   Total GL Accounts: {len(gl_balances)}')
        total_balance = sum(gl_balances.values())
        print(f'   Total Balance: ${total_balance:,.2f}')
        print('   Top 5 GL Balances:')
        for gl, balance in sorted(gl_balances.items(), key=lambda x: abs(x[1]), reverse=True)[:5]:
            print(f'      - GL {gl}: ${balance:,.2f}')
            
        print()
        print('✅ Detailed report analysis complete!')
        
    except FileNotFoundError:
        print('❌ Report file not found. Run the orchestration test first.')
    except Exception as e:
        print(f'❌ Error reading report: {str(e)}')

if __name__ == "__main__":
    main()
