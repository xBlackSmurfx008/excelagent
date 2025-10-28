#!/usr/bin/env python3
"""
Test AI Reconciliation Agent in Orchestration System
"""

from unified_dashboard import OrchestratorAgent

def main():
    print('🤖 TESTING AI RECONCILIATION AGENT IN ORCHESTRATION SYSTEM')
    print('=' * 70)

    orchestrator = OrchestratorAgent()

    print(f'\n🔧 ORCHESTRATOR INITIALIZED:')
    print(f'   Total Agents: {len(orchestrator.agents)}')
    for name, agent in orchestrator.agents.items():
        print(f'   - {name}: {agent.name} ({len(agent.capabilities)} capabilities)')

    # Test AI Reconciliation Agent
    print(f'\n🤖 TESTING AI RECONCILIATION AGENT:')
    ai_result = orchestrator.execute_step('ai_reconciliation', 'ai_thinking_process', 'AI thinking process for GL vs Bank Statement comparison')
    print(f'Status: {ai_result.get("status")}')
    print(f'Message: {ai_result.get("message")}')

    if ai_result.get('status') == 'success':
        ai_analysis = ai_result.get('ai_analysis', {})
        print(f'\n📊 AI ANALYSIS RESULTS:')
        print(f'   Total GL Balance: ${ai_analysis.get("total_gl_balance", 0):,.2f}')
        print(f'   GL Count: {ai_analysis.get("gl_count", 0)}')
        print(f'   Is Balanced: {ai_analysis.get("is_balanced", False)}')
        print(f'   Imbalance Amount: ${ai_analysis.get("imbalance_amount", 0):,.2f}')
        
        thinking_process = ai_analysis.get('thinking_process', [])
        if thinking_process:
            print(f'\n🧠 AI THINKING PROCESS:')
            for i, thinking in enumerate(thinking_process[:5], 1):  # Show first 5
                print(f'   {i}. {thinking}')
            if len(thinking_process) > 5:
                print(f'   ... and {len(thinking_process) - 5} more AI insights')

    # Test other AI tasks
    print(f'\n🔍 TESTING AI DISCREPANCY IDENTIFICATION:')
    discrepancy_result = orchestrator.execute_step('ai_reconciliation', 'identify_discrepancies', 'Identify discrepancies using AI analysis')
    print(f'Status: {discrepancy_result.get("status")}')
    print(f'Message: {discrepancy_result.get("message")}')

    if discrepancy_result.get('status') == 'success':
        discrepancies = discrepancy_result.get('discrepancies', [])
        print(f'\n⚠️ AI IDENTIFIED DISCREPANCIES:')
        for i, disc in enumerate(discrepancies, 1):
            print(f'   {i}. {disc}')

    # Test AI recommendations
    print(f'\n💡 TESTING AI RECOMMENDATIONS:')
    rec_result = orchestrator.execute_step('ai_reconciliation', 'generate_recommendations', 'Generate AI recommendations for reconciliation')
    print(f'Status: {rec_result.get("status")}')
    print(f'Message: {rec_result.get("message")}')

    if rec_result.get('status') == 'success':
        recommendations = rec_result.get('recommendations', [])
        print(f'\n🎯 AI RECOMMENDATIONS:')
        for i, rec in enumerate(recommendations, 1):
            print(f'   {i}. {rec}')

    print(f'\n✅ AI Reconciliation Agent test complete!')

if __name__ == "__main__":
    main()
