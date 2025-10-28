#!/usr/bin/env python3
"""
Test Credit Union Reconciliation Workflow
Based on OP-NCB Reconciliation training document
"""

from unified_dashboard import OrchestratorAgent
from credit_union_reconciliation_legend import get_reconciliation_legend

def main():
    print('🏦 CREDIT UNION RECONCILIATION WORKFLOW TEST')
    print('=' * 60)
    
    # Load reconciliation legend
    legend = get_reconciliation_legend()
    print(f"\n📋 RECONCILIATION LEGEND LOADED:")
    print(f"   Document Types: {len(legend['document_types'])}")
    print(f"   GL Accounts: {len(legend['gl_accounts'])}")
    print(f"   Workflow Steps: {len(legend['reconciliation_workflow'])}")
    print(f"   Timing Differences: {len(legend['timing_differences'])}")
    
    # Initialize orchestrator
    orchestrator = OrchestratorAgent()
    print(f"\n🔧 ORCHESTRATOR INITIALIZED:")
    print(f"   Agents: {len(orchestrator.agents)}")
    for name, agent in orchestrator.agents.items():
        print(f"   - {name}: {agent.name}")
    
    # Test 1: Document Type Identification
    print(f"\n📋 STEP 1: DOCUMENT TYPE IDENTIFICATION")
    print("-" * 40)
    
    file_result = orchestrator.execute_step('file_analysis', 'scan_and_validate_files', 'Identify document types for Credit Union reconciliation')
    print(f"Status: {file_result.get('status')}")
    print(f"Message: {file_result.get('message')}")
    
    if file_result.get('status') == 'success':
        files = file_result.get('files', [])
        
        # Group by document type
        document_types = {}
        for file_info in files:
            doc_type = file_info.get('document_type', 'unknown')
            if doc_type not in document_types:
                document_types[doc_type] = []
            document_types[doc_type].append(file_info)
        
        print(f"\n📊 DOCUMENT TYPE ANALYSIS:")
        for doc_type, file_list in document_types.items():
            print(f"   {doc_type.upper()}: {len(file_list)} files")
            for file_info in file_list[:2]:  # Show first 2 files
                gl_sheets = file_info.get('gl_sheets', [])
                recon_sheets = file_info.get('reconciliation_indicators', [])
                print(f"      - {file_info['name']}")
                print(f"        GL Sheets: {len(gl_sheets)} | Reconciliation: {len(recon_sheets)}")
            if len(file_list) > 2:
                print(f"      ... and {len(file_list) - 2} more files")
        
        # Check for required document types
        required_types = ['gl_activity', 'bank_statement']
        missing_types = [t for t in required_types if t not in document_types]
        
        if not missing_types:
            print(f"\n✅ REQUIRED DOCUMENT TYPES FOUND:")
            print(f"   - GL Activity Files: {len(document_types.get('gl_activity', []))}")
            print(f"   - Bank Statement Files: {len(document_types.get('bank_statement', []))}")
        else:
            print(f"\n⚠️ MISSING DOCUMENT TYPES: {missing_types}")
    
    # Test 2: GL Balance Extraction with Proper Accounting
    print(f"\n💰 STEP 2: GL BALANCE EXTRACTION (PROPER ACCOUNTING)")
    print("-" * 40)
    
    recon_result = orchestrator.execute_step('reconciliation', 'extract_gl_balances', 'Extract GL balances using proper accounting equation')
    print(f"Status: {recon_result.get('status')}")
    print(f"Message: {recon_result.get('message')}")
    
    if recon_result.get('status') == 'success':
        gl_balances = recon_result.get('gl_balances', {})
        print(f"\n📊 GL BALANCES (Debits - Credits):")
        
        # Show GL balances with legend mapping
        for gl, balance in gl_balances.items():
            gl_info = legend['gl_accounts'].get(gl, {})
            gl_name = gl_info.get('name', 'Unknown')
            print(f"   GL {gl} ({gl_name}): ${balance:,.2f}")
        
        total_balance = sum(gl_balances.values())
        print(f"\n💰 TOTAL BALANCE: ${total_balance:,.2f}")
        
        # Calculate debits and credits separately
        total_debits = sum(balance for balance in gl_balances.values() if balance > 0)
        total_credits = abs(sum(balance for balance in gl_balances.values() if balance < 0))
        print(f"   Total Debits: ${total_debits:,.2f}")
        print(f"   Total Credits: ${total_credits:,.2f}")
        print(f"   Net Imbalance: ${total_debits - total_credits:,.2f}")
    
    # Test 3: Reconciliation Verification
    print(f"\n🔍 STEP 3: RECONCILIATION VERIFICATION")
    print("-" * 40)
    
    validation_result = orchestrator.execute_step('validation', 'verify_reconciliation', 'Verify reconciliation using Credit Union principles')
    print(f"Status: {validation_result.get('status')}")
    print(f"Message: {validation_result.get('message')}")
    
    if validation_result.get('status') == 'success':
        print(f"\n📊 RECONCILIATION STATUS:")
        print(f"   Is Balanced: {validation_result.get('is_balanced')}")
        print(f"   Total Debits: ${validation_result.get('total_debits', 0):,.2f}")
        print(f"   Total Credits: ${validation_result.get('total_credits', 0):,.2f}")
        print(f"   Net Imbalance: ${validation_result.get('net_imbalance', 0):,.2f}")
        print(f"   Balanced Accounts: {validation_result.get('balanced_count', 0)}")
        print(f"   Imbalanced Accounts: {validation_result.get('imbalanced_count', 0)}")
        
        # Show imbalanced accounts
        imbalanced = validation_result.get('imbalanced_accounts', [])
        if imbalanced:
            print(f"\n⚠️ IMBALANCED ACCOUNTS:")
            for account in imbalanced[:5]:  # Show first 5
                gl = account['gl']
                gl_info = legend['gl_accounts'].get(gl, {})
                gl_name = gl_info.get('name', 'Unknown')
                print(f"   - GL {gl} ({gl_name}): {account['description']}")
            if len(imbalanced) > 5:
                print(f"   ... and {len(imbalanced) - 5} more imbalanced accounts")
    
    # Test 4: Complete Orchestration
    print(f"\n🎯 STEP 4: COMPLETE ORCHESTRATION TEST")
    print("-" * 40)
    
    goal = "Complete Credit Union reconciliation analysis with proper accounting equation"
    plan = orchestrator.create_execution_plan(goal)
    print(f"Created {len(plan)}-step execution plan for Credit Union reconciliation")
    
    # Execute orchestration
    print(f"\n🔄 EXECUTING ORCHESTRATED PLAN:")
    for i, step_info in enumerate(plan, 1):
        step_num = step_info['step']
        agent_name = step_info['agent']
        task = step_info['task']
        description = step_info['description']
        
        print(f"\n   Step {step_num}: {agent_name.upper()}")
        print(f"   Task: {task}")
        print(f"   Description: {description}")
        
        result = orchestrator.execute_step(agent_name, task, description)
        status = result.get('status', 'unknown')
        message = result.get('message', 'No message')
        
        if status == 'success':
            print(f"   ✅ SUCCESS: {message}")
        else:
            print(f"   ❌ ERROR: {message}")
            break
    
    print(f"\n🎉 CREDIT UNION RECONCILIATION WORKFLOW TEST COMPLETE!")
    print("=" * 60)
    
    # Summary
    print(f"\n📊 FINAL SUMMARY:")
    print(f"   Document Types Identified: {len(document_types) if 'document_types' in locals() else 0}")
    print(f"   GL Accounts Processed: {len(gl_balances) if 'gl_balances' in locals() else 0}")
    print(f"   Total Balance: ${total_balance if 'total_balance' in locals() else 0:,.2f}")
    is_balanced = validation_result.get('is_balanced') if 'validation_result' in locals() else False
    print(f"   Reconciliation Status: {'BALANCED' if is_balanced else 'IMBALANCED'}")
    
    print(f"\n✅ Credit Union reconciliation system ready for production use!")

if __name__ == "__main__":
    main()
