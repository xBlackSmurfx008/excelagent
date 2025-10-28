#!/usr/bin/env python3
"""
Test Enhanced GL Sheet Analysis
"""

from unified_dashboard import OrchestratorAgent

def main():
    print('🔍 TESTING ENHANCED GL SHEET ANALYSIS')
    print('=' * 60)

    orchestrator = OrchestratorAgent()

    # Test file analysis with enhanced data
    print('\n1. Testing FileAnalysisAgent with enhanced Excel file...')
    file_result = orchestrator.execute_step('file_analysis', 'scan_and_validate_files', 'Test enhanced Excel file analysis')
    print(f'Status: {file_result.get("status")}')
    print(f'Message: {file_result.get("message")}')

    if file_result.get('status') == 'success':
        files = file_result.get('files', [])
        print(f'\n📊 ENHANCED FILE ANALYSIS:')
        
        # Find the main GL activity file
        main_file = None
        for file_info in files:
            if '05 May 2025 Reconciliation and Flex GL Activity.xlsx' in file_info['name'] and file_info.get('document_type') == 'gl_activity':
                main_file = file_info
                break
        
        if main_file:
            print(f'\n📄 MAIN GL ACTIVITY FILE: {main_file["name"]}')
            print(f'   Document Type: {main_file.get("document_type")}')
            print(f'   GL Sheets: {len(main_file.get("gl_sheets", []))}')
            print(f'   Reconciliation Sheets: {len(main_file.get("reconciliation_indicators", []))}')
            print(f'   File Size: {main_file.get("size", 0):,} bytes')
            
            gl_sheets = main_file.get('gl_sheets', [])
            print(f'\n💰 GL SHEETS FOUND: {gl_sheets}')
            
            # Test GL balance extraction with enhanced data
            print(f'\n2. Testing enhanced GL balance extraction...')
            recon_result = orchestrator.execute_step('reconciliation', 'extract_gl_balances', 'Extract GL balances from enhanced sheets')
            print(f'Status: {recon_result.get("status")}')
            print(f'Message: {recon_result.get("message")}')
            
            if recon_result.get('status') == 'success':
                gl_balances = recon_result.get('gl_balances', {})
                print(f'\n📊 ENHANCED GL BALANCES:')
                for gl, balance in gl_balances.items():
                    print(f'   GL {gl}: ${balance:,.2f}')
                
                total_balance = sum(gl_balances.values())
                print(f'\n💰 TOTAL BALANCE: ${total_balance:,.2f}')
                
                # Test validation
                print(f'\n3. Testing reconciliation verification...')
                validation_result = orchestrator.execute_step('validation', 'verify_reconciliation', 'Verify enhanced reconciliation')
                print(f'Status: {validation_result.get("status")}')
                print(f'Message: {validation_result.get("message")}')
                
                if validation_result.get('status') == 'success':
                    print(f'\n📊 RECONCILIATION STATUS:')
                    print(f'   Is Balanced: {validation_result.get("is_balanced")}')
                    print(f'   Total Debits: ${validation_result.get("total_debits", 0):,.2f}')
                    print(f'   Total Credits: ${validation_result.get("total_credits", 0):,.2f}')
                    print(f'   Net Imbalance: ${validation_result.get("net_imbalance", 0):,.2f}')
                    print(f'   Balanced Accounts: {validation_result.get("balanced_count", 0)}')
                    print(f'   Imbalanced Accounts: {validation_result.get("imbalanced_count", 0)}')
                    
                    # Show imbalanced accounts
                    imbalanced = validation_result.get('imbalanced_accounts', [])
                    if imbalanced:
                        print(f'\n⚠️ IMBALANCED ACCOUNTS:')
                        for account in imbalanced[:5]:  # Show first 5
                            print(f'   - {account["description"]}')
                        if len(imbalanced) > 5:
                            print(f'   ... and {len(imbalanced) - 5} more imbalanced accounts')

    print('\n✅ Enhanced GL sheet analysis test complete!')

if __name__ == "__main__":
    main()
