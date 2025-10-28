#!/usr/bin/env python3
"""
Test AI Reconciliation Agent directly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the AIReconciliationAgent class directly
from unified_dashboard import AIReconciliationAgent

def main():
    print('🤖 TESTING AI RECONCILIATION AGENT DIRECTLY')
    print('=' * 60)

    # Create AI agent directly
    ai_agent = AIReconciliationAgent()
    
    print(f'\n🔧 AI AGENT INITIALIZED:')
    print(f'   Name: {ai_agent.name}')
    print(f'   Capabilities: {ai_agent.capabilities}')
    print(f'   OP Manual GL Accounts: {len(ai_agent.op_manual["gl_accounts"])}')
    print(f'   Timing Differences: {len(ai_agent.op_manual["timing_differences"])}')

    # Test AI thinking process (without orchestrator)
    print(f'\n🤖 TESTING AI THINKING PROCESS:')
    print('   Note: This test requires GL data from reconciliation agent')
    print('   For full test, use the orchestration system')
    
    # Test other AI capabilities
    print(f'\n🔍 TESTING AI DISCREPANCY IDENTIFICATION:')
    discrepancy_result = ai_agent.identify_discrepancies()
    print(f'Status: {discrepancy_result.get("status")}')
    print(f'Message: {discrepancy_result.get("message")}')

    if discrepancy_result.get('status') == 'success':
        discrepancies = discrepancy_result.get('discrepancies', [])
        print(f'\n⚠️ AI IDENTIFIED DISCREPANCIES:')
        for i, disc in enumerate(discrepancies, 1):
            print(f'   {i}. {disc}')

    # Test AI recommendations
    print(f'\n💡 TESTING AI RECOMMENDATIONS:')
    rec_result = ai_agent.generate_recommendations()
    print(f'Status: {rec_result.get("status")}')
    print(f'Message: {rec_result.get("message")}')

    if rec_result.get('status') == 'success':
        recommendations = rec_result.get('recommendations', [])
        print(f'\n🎯 AI RECOMMENDATIONS:')
        for i, rec in enumerate(recommendations, 1):
            print(f'   {i}. {rec}')

    print(f'\n✅ AI Reconciliation Agent test complete!')
    print(f'\n📋 NEXT STEPS:')
    print(f'   1. Integrate AI agent into orchestration system')
    print(f'   2. Test with actual GL and bank statement data')
    print(f'   3. Implement bank statement parsing')
    print(f'   4. Add AI thinking to reconciliation workflow')

if __name__ == "__main__":
    main()
