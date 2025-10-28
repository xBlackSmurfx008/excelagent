#!/usr/bin/env python3
"""
Test Enhanced Reconciliation Framework for 80% Match Rate
"""

import sys
from pathlib import Path
sys.path.insert(0, '/Users/mr.adams/Desktop/Excel Agent')

from enhanced_reconciliation_framework import perform_enhanced_reconciliation

def main():
    print("🤖 Testing Enhanced Reconciliation Framework")
    print("🎯 Target: 80% match rate through iterative improvement")
    print("=" * 60)
    
    # Define file paths
    gl_files = [Path('uploads/17b27999-628f-456c-9039-796bc61cb19d_05 May 2025 Reconciliation and Flex GL Activity.xlsx')]
    bank_file = Path('uploads/0e60826b-b004-4f37-8d57-163661c0d5fc_NCB Bank Activity 5-1 to 5-31 Support for May 2025 Rec.xls')
    
    print(f"📁 GL Files: {len(gl_files)}")
    print(f"📁 Bank File: {bank_file.name}")
    print()
    
    # Run enhanced reconciliation
    result = perform_enhanced_reconciliation(gl_files, bank_file)
    
    print()
    print("📊 Enhanced Framework Test Results:")
    print("=" * 40)
    print(f"Status: {result['status']}")
    print(f"Target Achieved: {result['target_achieved']}")
    
    if result['status'] == 'success':
        data = result['data']
        summary = data['summary']
        
        print(f"✅ Match Rate: {summary['match_rate']:.1f}% (Target: {summary['target_match_rate']}%)")
        print(f"✅ Matches: {summary['matching_results']['total_matches']}")
        print(f"📊 GL Balance: ${summary['reconciliation_summary']['gl_balance']:,.2f}")
        print(f"📊 Bank Total: ${summary['reconciliation_summary']['bank_total']:,.2f}")
        print(f"📊 Variance: ${summary['reconciliation_summary']['variance']:,.2f}")
        print(f"🔄 Iterations Used: {summary['iterations_used']}")
        
        if summary['strategy_analysis']:
            print(f"\n🎯 Strategy Analysis:")
            for strategy, count in summary['strategy_analysis'].items():
                print(f"   {strategy}: {count} matches")
        
        # Save detailed results
        import json
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"data/reports/enhanced_reconciliation_{timestamp}.json"
        
        Path("data/reports").mkdir(parents=True, exist_ok=True)
        with open(report_file, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        
        print(f"\n📄 Detailed report saved: {report_file}")
        
    else:
        print(f"❌ Error: {result['message']}")
    
    print("\n🎉 Enhanced reconciliation test completed!")

if __name__ == "__main__":
    from datetime import datetime
    main()
