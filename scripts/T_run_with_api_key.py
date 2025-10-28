#!/usr/bin/env python3
"""
Run AI Thinking Agent with API key input
Prompts user to paste API key from clipboard and runs the AI thinking agent
"""

import os
import sys
import getpass
from pathlib import Path

def get_api_key_from_user():
    """Get API key from user input"""
    print("🔑 OPENAI API KEY SETUP")
    print("=" * 30)
    print("Please paste your OpenAI API key:")
    print("(The key will be hidden for security)")
    print()
    
    api_key = getpass.getpass("API Key: ")
    
    if not api_key or len(api_key) < 20:
        print("❌ Invalid API key. Please try again.")
        return None
    
    return api_key

def run_ai_thinking_with_key():
    """Run AI thinking agent with provided API key"""
    print("\n🚀 RUNNING AI THINKING AGENT")
    print("=" * 35)
    
    # Get API key from user
    api_key = get_api_key_from_user()
    if not api_key:
        print("❌ No API key provided. Cannot proceed.")
        return False
    
    # Set the API key
    os.environ['OPENAI_API_KEY'] = api_key
    print("✅ API key set successfully")
    
    # Import and run the AI thinking agent
    try:
        from ai_thinking_agent import AIThinkingAgent
        
        # Initialize the agent
        agent = AIThinkingAgent(api_key=api_key)
        
        # OP document path
        op_file = "Knowledge Base/op-ncb-reconciliation-8-28-25.md"
        
        if not os.path.exists(op_file):
            print(f"❌ OP document not found: {op_file}")
            return False
        
        print(f"\n🔄 Starting AI thinking retraining on: {op_file}")
        print("🧠 This will use OpenAI's thinking model for deep analysis...")
        print("⏱️ This may take several minutes for 10 thinking sequences...")
        print()
        
        # Run the actual retraining
        final_insights = agent.retrain_on_op_document(op_file)
        
        if final_insights:
            print(f"\n🎉 AI THINKING RETRAINING COMPLETE!")
            print(f"📊 Total insights: {final_insights['total_insights']}")
            print(f"🔍 Key discoveries: {len(final_insights['key_discoveries'])}")
            print(f"✅ Thinking sequences: {final_insights['thinking_sequences_completed']}")
            print(f"📁 Results saved with timestamp: {agent.timestamp}")
            
            # Show key discoveries
            print(f"\n🎯 TOP KEY DISCOVERIES:")
            print("-" * 30)
            for i, discovery in enumerate(final_insights['key_discoveries'][:5], 1):
                print(f"{i}. {discovery}")
            
            print(f"\n📁 FILES CREATED:")
            print(f"• ai_thinking_sequences_{agent.timestamp}.json")
            print(f"• ai_thinking_insights_{agent.timestamp}.json")
            print(f"• ai_thinking_summary_{agent.timestamp}.txt")
            
            return True
        else:
            print("❌ AI thinking retraining failed")
            return False
            
    except ImportError as e:
        print(f"❌ Error importing AI thinking agent: {e}")
        return False
    except Exception as e:
        print(f"❌ Error running AI thinking task: {e}")
        return False

def main():
    """Main function"""
    print("🧠 AI THINKING AGENT - RUN WITH API KEY")
    print("=" * 45)
    print("🎯 This will run the real AI thinking agent")
    print("🔄 Using OpenAI API for deep analysis")
    print("=" * 45)
    
    # Check if we're in the right directory
    if not os.path.exists("ai_thinking_agent.py"):
        print("❌ Error: ai_thinking_agent.py not found")
        print("   Please run this from the Excel Agent directory")
        sys.exit(1)
    
    # Check for OP document
    op_file = "Knowledge Base/op-ncb-reconciliation-8-28-25.md"
    if not os.path.exists(op_file):
        print(f"❌ OP document not found: {op_file}")
        sys.exit(1)
    
    # Run the AI thinking agent
    success = run_ai_thinking_with_key()
    
    if success:
        print("\n🎉 AI THINKING AGENT COMPLETED SUCCESSFULLY!")
        print("✅ 10 thinking sequences completed")
        print("✅ New insights discovered from OP document")
        print("✅ AI agent retrained with deep analysis")
        print("✅ Ready for enhanced reconciliation")
    else:
        print("\n❌ AI THINKING AGENT FAILED")
        print("   Check API key and internet connection")
        sys.exit(1)

if __name__ == "__main__":
    main()
