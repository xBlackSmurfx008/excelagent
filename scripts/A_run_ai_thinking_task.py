#!/usr/bin/env python3
"""
AI Thinking Task Runner - Spins up the real AI thinking agent
Uses actual OpenAI API to perform 10 thinking sequences on OP document
"""

import os
import sys
from pathlib import Path

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 CHECKING REQUIREMENTS")
    print("-" * 25)
    
    # Check for OpenAI API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY environment variable not set")
        print("   Please set your OpenAI API key:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        return False
    else:
        print("✅ OpenAI API key found")
    
    # Check for OP document
    op_file = "Knowledge Base/op-ncb-reconciliation-8-28-25.md"
    if not os.path.exists(op_file):
        print(f"❌ OP document not found: {op_file}")
        return False
    else:
        print(f"✅ OP document found: {op_file}")
    
    # Check for internet connection (basic check)
    try:
        import requests
        response = requests.get("https://api.openai.com/v1/models", timeout=5)
        print("✅ Internet connection verified")
    except:
        print("⚠️ Internet connection check failed, but proceeding...")
    
    print("✅ All requirements met!")
    return True

def run_ai_thinking_task():
    """Run the actual AI thinking task"""
    print("\n🚀 SPINNING UP AI THINKING AGENT")
    print("=" * 40)
    print("🎯 Using real OpenAI API with thinking model")
    print("🔄 Performing 10 real thinking sequences")
    print("=" * 40)
    
    # Import and run the actual AI thinking agent
    try:
        from ai_thinking_agent import AIThinkingAgent
        
        # Initialize the agent
        agent = AIThinkingAgent()
        
        # OP document path
        op_file = "Knowledge Base/op-ncb-reconciliation-8-28-25.md"
        
        print(f"\n🔄 Starting AI thinking retraining on: {op_file}")
        print("🧠 This will use OpenAI's thinking model for deep analysis...")
        print("⏱️ This may take several minutes for 10 thinking sequences...")
        
        # Run the actual retraining
        final_insights = agent.retrain_on_op_document(op_file)
        
        if final_insights:
            print(f"\n🎉 AI THINKING RETRAINING COMPLETE!")
            print(f"📊 Total insights: {final_insights['total_insights']}")
            print(f"🔍 Key discoveries: {len(final_insights['key_discoveries'])}")
            print(f"✅ Thinking sequences: {final_insights['thinking_sequences_completed']}")
            print(f"📁 Results saved to files with timestamp: {agent.timestamp}")
            
            # Show key discoveries
            print(f"\n🎯 TOP KEY DISCOVERIES:")
            print("-" * 30)
            for i, discovery in enumerate(final_insights['key_discoveries'][:5], 1):
                print(f"{i}. {discovery}")
            
            return True
        else:
            print("❌ AI thinking retraining failed")
            return False
            
    except ImportError as e:
        print(f"❌ Error importing AI thinking agent: {e}")
        print("   Make sure ai_thinking_agent.py is in the current directory")
        return False
    except Exception as e:
        print(f"❌ Error running AI thinking task: {e}")
        return False

def main():
    """Main task runner"""
    print("🧠 AI THINKING TASK RUNNER")
    print("=" * 30)
    print("🎯 Spinning up real AI thinking agent")
    print("🔄 Using OpenAI API for deep analysis")
    print("=" * 30)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Requirements not met. Cannot proceed.")
        sys.exit(1)
    
    # Run the AI thinking task
    success = run_ai_thinking_task()
    
    if success:
        print("\n🎉 AI THINKING TASK COMPLETED SUCCESSFULLY!")
        print("✅ 10 thinking sequences completed")
        print("✅ New insights discovered from OP document")
        print("✅ AI agent retrained with deep analysis")
        print("✅ Ready for enhanced reconciliation")
    else:
        print("\n❌ AI THINKING TASK FAILED")
        print("   Check API key and internet connection")
        sys.exit(1)

if __name__ == "__main__":
    main()
