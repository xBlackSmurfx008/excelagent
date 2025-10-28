#!/usr/bin/env python3
"""
Test corrected accounting logic for credit union reconciliation
"""

from unified_dashboard import OrchestratorAgent

def main():
    print('🧮 TESTING CORRECTED ACCOUNTING LOGIC')
    print('=' * 50)

    orchestrator = OrchestratorAgent()

    # Test reconciliation agent with corrected logic
    print('\n1. Testing ReconciliationAgent with proper accounting equation...')
    recon_result = orchestrator.execute_step('reconciliation', 'extract_gl_balances', 'Test GL extraction with proper accounting')
    print(f'Status: {recon_result.get("status")}')
    print(f'Message: {recon_result.get("message")}')

    if recon_result.get('status') == 'success':
        gl_balances = recon_result.get('gl_balances', {})
        print(f'\nGL Balances (Debits - Credits):')
        for gl, balance in gl_balances.items():
            print(f'   GL {gl}: ${balance:,.2f}')
        
        total_balance = sum(gl_balances.values())
        print(f'\nTotal Balance: ${total_balance:,.2f}')
        
        # Test validation with corrected logic
        print('\n2. Testing ValidationAgent with proper reconciliation logic...')
        validation_result = orchestrator.execute_step('validation', 'verify_reconciliation', 'Test reconciliation verification')
        print(f'Status: {validation_result.get("status")}')
        print(f'Message: {validation_result.get("message")}')
        
        if validation_result.get('status') == 'success':
            print(f'\nReconciliation Details:')
            print(f'   Is Balanced: {validation_result.get("is_balanced")}')
            print(f'   Total Debits: ${validation_result.get("total_debits", 0):,.2f}')
            print(f'   Total Credits: ${validation_result.get("total_credits", 0):,.2f}')
            print(f'   Net Imbalance: ${validation_result.get("net_imbalance", 0):,.2f}')
            print(f'   Balanced Accounts: {validation_result.get("balanced_count", 0)}')
            print(f'   Imbalanced Accounts: {validation_result.get("imbalanced_count", 0)}')
            
            # Show imbalanced accounts
            imbalanced = validation_result.get('imbalanced_accounts', [])
            if imbalanced:
                print(f'\nImbalanced Accounts:')
                for account in imbalanced[:5]:  # Show first 5
                    print(f'   - {account["description"]}')
                if len(imbalanced) > 5:
                    print(f'   ... and {len(imbalanced) - 5} more')

    print('\n✅ Accounting logic test complete!')

if __name__ == "__main__":
    main()
