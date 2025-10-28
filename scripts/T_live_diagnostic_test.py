#!/usr/bin/env python3
"""
Excel Agent Orchestration System - Live Diagnostic Test
Tests the full orchestration system with real-time monitoring
"""

import json
import time
from datetime import datetime
from unified_dashboard import OrchestratorAgent

def main():
    print('🚀 EXCEL AGENT ORCHESTRATION SYSTEM - LIVE DIAGNOSTIC TEST')
    print('=' * 60)
    print(f'Test Started: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print()

    # Initialize orchestrator
    print('🔧 Initializing OrchestratorAgent...')
    orchestrator = OrchestratorAgent()
    print(f'✅ Orchestrator initialized with {len(orchestrator.agents)} specialized agents')
    for name, agent in orchestrator.agents.items():
        print(f'   - {name}: {agent.name} ({len(agent.capabilities)} capabilities)')
    print()

    # Create execution plan
    print('📋 Creating execution plan...')
    goal = 'Complete Excel reconciliation analysis with discrepancy detection'
    plan = orchestrator.create_execution_plan(goal)
    print(f'✅ Created {len(plan)}-step execution plan')
    print()

    # Execute with live monitoring
    print('🎯 EXECUTING ORCHESTRATED PLAN WITH LIVE MONITORING')
    print('=' * 60)

    for i, step_info in enumerate(plan, 1):
        step_num = step_info['step']
        agent_name = step_info['agent']
        task = step_info['task']
        description = step_info['description']
        
        print(f'\n🔄 STEP {step_num}: {agent_name.upper()} - {description}')
        print(f'   Task: {task}')
        print(f'   Agent: {orchestrator.agents[agent_name].name}')
        
        # Execute step with timing
        start_time = time.time()
        result = orchestrator.execute_step(agent_name, task, description)
        end_time = time.time()
        duration = end_time - start_time
        
        # Display results
        status = result.get('status', 'unknown')
        message = result.get('message', 'No message')
        
        if status == 'success':
            print(f'   ✅ SUCCESS ({duration:.2f}s): {message}')
            
            # Show detailed results for key steps
            if agent_name == 'file_analysis' and 'files' in result:
                files = result['files']
                print(f'   📊 Found {len(files)} files:')
                for file_info in files[:3]:  # Show first 3 files
                    gl_sheets = file_info.get('gl_sheets', [])
                    recon_sheets = file_info.get('reconciliation_indicators', [])
                    print(f'      - {file_info["name"]}: {len(gl_sheets)} GL sheets, {len(recon_sheets)} reconciliation sheets')
                if len(files) > 3:
                    print(f'      ... and {len(files) - 3} more files')
            
            elif agent_name == 'reconciliation' and 'gl_balances' in result:
                gl_balances = result['gl_balances']
                print(f'   📊 Extracted {len(gl_balances)} GL balances:')
                for gl, balance in list(gl_balances.items())[:5]:  # Show first 5
                    print(f'      - GL {gl}: ${balance:,.2f}')
                if len(gl_balances) > 5:
                    print(f'      ... and {len(gl_balances) - 5} more GL accounts')
            
            elif agent_name == 'validation':
                if 'is_balanced' in result:
                    is_balanced = result['is_balanced']
                    total_balance = result.get('total_balance', 0)
                    print(f'   📊 Reconciliation Status: {"BALANCED" if is_balanced else "IMBALANCED"}')
                    print(f'   📊 Total Balance: ${total_balance:,.2f}')
                
                if 'discrepancies' in result:
                    discrepancies = result['discrepancies']
                    print(f'   📊 Found {len(discrepancies)} discrepancies')
                    for disc in discrepancies[:3]:  # Show first 3
                        print(f'      - {disc.get("description", "Unknown discrepancy")}')
                    if len(discrepancies) > 3:
                        print(f'      ... and {len(discrepancies) - 3} more discrepancies')
            
            elif agent_name == 'communication' and 'presentation' in result:
                presentation = result['presentation']
                findings = presentation.get('detailed_findings', [])
                recommendations = presentation.get('recommendations', [])
                human_input = presentation.get('human_input_required', [])
                
                print(f'   📊 Analysis Results:')
                for finding in findings:
                    print(f'      - {finding}')
                
                if recommendations:
                    print(f'   💡 Recommendations:')
                    for rec in recommendations:
                        print(f'      - {rec}')
                
                if human_input:
                    print(f'   👤 Human Input Required:')
                    for req in human_input:
                        print(f'      - {req}')
        
        else:
            print(f'   ❌ ERROR ({duration:.2f}s): {message}')
            print(f'   🔍 Error details: {result}')
            break
        
        # Store result
        orchestrator.step_results[step_num] = result

    print()
    print('🎉 ORCHESTRATION TEST COMPLETE!')
    print('=' * 60)

    # Final summary
    print('📊 FINAL SUMMARY:')
    total_steps = len(plan)
    successful_steps = sum(1 for result in orchestrator.step_results.values() if result.get('status') == 'success')
    print(f'   Steps Executed: {successful_steps}/{total_steps}')
    print(f'   Success Rate: {(successful_steps/total_steps)*100:.1f}%')

    # Check if report was generated
    try:
        with open('orchestrated_analysis_report.json', 'r') as f:
            report = json.load(f)
            summary = report.get('summary', {})
            print(f'   Files Analyzed: {summary.get("files_analyzed", 0)}')
            print(f'   GL Accounts Found: {summary.get("gl_accounts_found", 0)}')
            print(f'   Total Balance: ${summary.get("total_balance", 0):,.2f}')
            print(f'   Is Balanced: {summary.get("is_balanced", False)}')
            print(f'   Discrepancies Found: {summary.get("discrepancies_found", 0)}')
    except:
        print('   Report file not found')

    print()
    print('✅ Live diagnostic test completed successfully!')

if __name__ == "__main__":
    main()
