#!/usr/bin/env python3
"""
Content Marketing Agent - Health Check
Quick test to verify all components are working
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    print("🚀 Content Marketing Agent Health Check")
    print("=" * 50)
    
    # Check environment
    print("📁 Environment Check:")
    print(f"   Working Directory: {os.getcwd()}")
    print(f"   Python Version: {sys.version.split()[0]}")
    
    # Check API keys
    print("\n🔑 API Keys Check:")
    openai_key = os.getenv('OPENAI_API_KEY', '')
    apify_token = os.getenv('APIFY_API_TOKEN', '')
    
    print(f"   OpenAI API Key: {'✅ Set' if openai_key else '⚠️ Missing'}")
    print(f"   Apify API Token: {'✅ Set' if apify_token else '⚠️ Missing'}")
    
    # Check dependencies
    print("\n📦 Dependencies Check:")
    try:
        import streamlit
        print(f"   Streamlit: ✅ {streamlit.__version__}")
    except ImportError:
        print("   Streamlit: ❌ Not installed")
    
    try:
        import dspy
        print(f"   DSPy: ✅ Available")
    except ImportError:
        print("   DSPy: ❌ Not installed")
    
    try:
        import httpx
        print(f"   HTTPX: ✅ Available")
    except ImportError:
        print("   HTTPX: ❌ Not installed")
    
    # Test production agent
    print("\n🤖 Production Agent Check:")
    try:
        from agents.production_agent import ProductionContentAgent
        agent = ProductionContentAgent()
        
        print(f"   Agent Initialization: ✅ Success")
        print(f"   DSPy AI Engine: {'✅ Ready' if agent.dspy_initialized else '⚠️ Limited (no OpenAI key)'}")
        print(f"   Direct Scrapers: {'✅ Ready' if agent.scraper.api_token else '⚠️ Offline (no Apify token)'}")
        print(f"   Available Tools: {len(agent.tools)}")
        print(f"   DSPy Signatures: {len(agent.signatures)}")
        
        # Test basic functionality
        state = agent.get_bot_state_summary()
        print(f"   React Agent State: {state['agent_state']['current_state']}")
        
    except Exception as e:
        print(f"   Agent Initialization: ❌ Failed - {e}")
    
    # Test scraper
    print("\n🔍 Direct Scraper Check:")
    try:
        from scrapers.direct_scraper import DirectScraper
        scraper = DirectScraper()
        
        print(f"   Scraper Initialization: ✅ Success")
        print(f"   API Token Available: {'✅ Yes' if scraper.api_token else '⚠️ No'}")
        print(f"   Base URL: {scraper.base_url}")
        
    except Exception as e:
        print(f"   Scraper Initialization: ❌ Failed - {e}")
    
    # Check app files
    print("\n📱 App Files Check:")
    app_files = [
        "app_production.py",
        "app.py", 
        "app_modern.py",
        "app_native.py"
    ]
    
    for app_file in app_files:
        if os.path.exists(app_file):
            print(f"   {app_file}: ✅ Available")
        else:
            print(f"   {app_file}: ❌ Missing")
    
    # Final recommendations
    print("\n🎯 Recommendations:")
    
    if not openai_key:
        print("   • Add OPENAI_API_KEY for advanced AI features")
    
    if not apify_token:
        print("   • Add APIFY_API_TOKEN for real-time scraping")
    
    print("   • Run: streamlit run app_production.py")
    print("   • Access: http://localhost:8501")
    
    print("\n✅ Health check complete!")

if __name__ == "__main__":
    main()