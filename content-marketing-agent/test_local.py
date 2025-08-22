#!/usr/bin/env python3
"""
Local Testing Script for Content Marketing Agent
Interactive testing of all major features
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def test_agent():
    """Interactive testing session"""
    
    print("🚀 Content Marketing Agent - Local Testing")
    print("=" * 50)
    
    # Initialize agent
    try:
        from agents.production_agent import ProductionContentAgent
        agent = ProductionContentAgent()
        print("✅ Production agent initialized")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        return
    
    # Test profile
    test_profile = {
        "name": "Test User",
        "brand_name": "Test Brand", 
        "expertise_areas": ["Business Coaching", "Personal Development"],
        "active_platforms": ["instagram", "linkedin"],
        "primary_language": "en",
        "cultural_background": "cameroon",
        "age": 35
    }
    
    print(f"🤖 Agent Status:")
    print(f"   DSPy AI: {'✅ Ready' if agent.dspy_initialized else '⚠️ Limited'}")
    print(f"   Scrapers: {'✅ Ready' if agent.scraper.api_token else '⚠️ Offline'}")
    
    while True:
        print("\n" + "="*50)
        print("🎯 Available Tests:")
        print("1. 🔍 Test Direct Scraper")
        print("2. 🤖 Test Content Generation") 
        print("3. 💬 Test Smart Chat")
        print("4. 📈 Test Trend Analysis")
        print("5. 🤖 Test React Agent Status")
        print("6. 🧪 Run All Tests")
        print("7. 🚀 Launch Streamlit App")
        print("8. ❌ Exit")
        
        choice = input("\nEnter choice (1-8): ").strip()
        
        if choice == "1":
            await test_scraper(agent)
        elif choice == "2":
            await test_content_generation(agent, test_profile)
        elif choice == "3":
            await test_chat(agent, test_profile)
        elif choice == "4":
            await test_trends(agent, test_profile)
        elif choice == "5":
            test_react_agent(agent)
        elif choice == "6":
            await run_all_tests(agent, test_profile)
        elif choice == "7":
            launch_streamlit_app()
        elif choice == "8":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")

async def test_scraper(agent):
    """Test direct scraper functionality"""
    print("\n🔍 Testing Direct Scraper...")
    
    if not agent.scraper.api_token:
        print("⚠️ No Apify token - scraper will return empty results")
    
    query = input("Enter search query (or press Enter for 'business coaching'): ").strip()
    if not query:
        query = "business coaching"
    
    platforms = input("Enter platforms (twitter,tiktok,instagram) or press Enter for all: ").strip()
    if platforms:
        platforms = [p.strip() for p in platforms.split(",")]
    else:
        platforms = ["twitter", "tiktok", "instagram"]
    
    print(f"🔍 Scraping '{query}' from {', '.join(platforms)}...")
    
    try:
        results = await agent.scrape_content(query, platforms, max_results=3)
        
        print(f"✅ Scraping completed!")
        print(f"   Total items found: {results.get('total_items', 0)}")
        print(f"   Platforms scraped: {', '.join(results.get('platforms', []))}")
        print(f"   Timestamp: {results.get('timestamp', 'Unknown')}")
        
        if results.get('summary'):
            print(f"\n📝 Summary:")
            print(results['summary'][:500] + "..." if len(results.get('summary', '')) > 500 else results.get('summary', ''))
        
        # Show detailed results
        show_details = input("\nShow detailed results? (y/n): ").strip().lower()
        if show_details == 'y':
            for platform, data in results.get('data', {}).items():
                print(f"\n📱 {platform.title()} Results:")
                for i, item in enumerate(data[:2], 1):
                    print(f"   {i}. @{item.get('author', 'unknown')}")
                    print(f"      Text: {item.get('text', '')[:100]}...")
                    print(f"      Engagement: {item.get('engagement_score', 0):.1f}%")
        
    except Exception as e:
        print(f"❌ Scraping failed: {e}")

async def test_content_generation(agent, profile):
    """Test content generation"""
    print("\n🤖 Testing Content Generation...")
    
    platform = input("Enter platform (instagram/linkedin/tiktok) or press Enter for 'instagram': ").strip()
    if not platform:
        platform = "instagram"
    
    content_type = input("Enter content type (educational/motivational/promotional) or press Enter for 'educational': ").strip()
    if not content_type:
        content_type = "educational"
    
    topic = input("Enter topic (optional): ").strip()
    
    print(f"🤖 Generating {content_type} content for {platform}...")
    
    try:
        content = await agent.generate_content_with_trends(
            profile, platform, content_type, "en", topic
        )
        
        print("✅ Content generated successfully!")
        print("\n📝 Generated Content:")
        print("-" * 40)
        print(content.get('content_text', 'No content generated'))
        print("-" * 40)
        
        if content.get('hashtags'):
            print(f"\n🏷️ Hashtags: {' '.join(content['hashtags'])}")
        
        if content.get('call_to_action'):
            print(f"\n📢 Call to Action: {content['call_to_action']}")
        
        if content.get('strategy'):
            print(f"\n🎯 Strategy: {content['strategy'][:200]}...")
        
    except Exception as e:
        print(f"❌ Content generation failed: {e}")

async def test_chat(agent, profile):
    """Test smart chat functionality"""
    print("\n💬 Testing Smart Chat...")
    
    print("Try commands like:")
    print("- 'scrape business content'")
    print("- 'find trending posts about marketing'")
    print("- 'what should I post today?'")
    
    message = input("\nEnter your message: ").strip()
    if not message:
        message = "Hello, what should I post today?"
    
    print(f"💬 Processing: '{message}'...")
    
    try:
        response = await agent.chat_response(message, profile, [])
        
        print("✅ Chat response generated!")
        print("\n🤖 AI Response:")
        print("-" * 40)
        print(response)
        print("-" * 40)
        
    except Exception as e:
        print(f"❌ Chat failed: {e}")

async def test_trends(agent, profile):
    """Test trend analysis"""
    print("\n📈 Testing Trend Analysis...")
    
    print("🔍 Analyzing trends based on your expertise areas...")
    
    try:
        trends = await agent.analyze_trends_direct(profile)
        
        print("✅ Trend analysis completed!")
        
        trending_topics = trends.get('trending_topics', [])
        if trending_topics:
            print(f"\n🔥 Found {len(trending_topics)} trending topics:")
            for i, topic in enumerate(trending_topics[:5], 1):
                print(f"   {i}. {topic.get('topic', 'Unknown')}")
                print(f"      Platform: {topic.get('platform', 'unknown')}")
                print(f"      Engagement: {topic.get('engagement_score', 0):.1f}%")
                print(f"      Relevance: {topic.get('relevance_score', 0):.1f}/10")
        
        opportunities = trends.get('content_opportunities', [])
        if opportunities:
            print(f"\n💡 Content Opportunities:")
            for i, opp in enumerate(opportunities[:3], 1):
                print(f"   {i}. {opp.get('topic', 'Unknown')}")
                print(f"      Potential: {opp.get('engagement_potential', 0):.1f}%")
                print(f"      Approach: {opp.get('suggested_approach', 'Create content')}")
        
        data_sources = trends.get('data_sources', {})
        if data_sources:
            print(f"\n📊 Data Sources:")
            print(f"   Twitter: {data_sources.get('twitter_posts_count', 0)} posts")
            print(f"   TikTok: {data_sources.get('tiktok_videos_count', 0)} videos")
            print(f"   Instagram: {data_sources.get('instagram_posts_count', 0)} posts")
        
    except Exception as e:
        print(f"❌ Trend analysis failed: {e}")

def test_react_agent(agent):
    """Test React agent status"""
    print("\n🤖 Testing React Agent...")
    
    try:
        status = agent.get_bot_state_summary()
        
        print("✅ React Agent Status:")
        print(f"   Current State: {status['agent_state']['current_state']}")
        print(f"   Iteration Count: {status['agent_state']['iteration_count']}")
        print(f"   Task Complexity: {status['agent_state']['task_complexity']}")
        print(f"   Error Occurred: {status['agent_state']['error_occurred']}")
        
        print(f"\n🛠️ Available Tools: {len(status['available_tools'])}")
        for tool in status['available_tools']:
            print(f"   - {tool}")
        
        print(f"\n📝 Available Signatures: {len(status['available_signatures'])}")
        for sig in status['available_signatures']:
            print(f"   - {sig}")
        
        print(f"\n💾 Cache Status:")
        print(f"   Has Trends Cache: {status['cache_status']['has_trends_cache']}")
        print(f"   Cache Timestamp: {status['cache_status']['cache_timestamp']}")
        
    except Exception as e:
        print(f"❌ React agent test failed: {e}")

async def run_all_tests(agent, profile):
    """Run all tests sequentially"""
    print("\n🧪 Running All Tests...")
    
    print("\n1/5 Testing Scraper...")
    try:
        results = await agent.scrape_content("business", ["twitter"], 2)
        print(f"   ✅ Scraper: {results.get('total_items', 0)} items found")
    except Exception as e:
        print(f"   ❌ Scraper: {e}")
    
    print("\n2/5 Testing Content Generation...")
    try:
        content = await agent.generate_content_with_trends(profile, "instagram", "educational", "en")
        print(f"   ✅ Content: {len(content.get('content_text', ''))} characters generated")
    except Exception as e:
        print(f"   ❌ Content: {e}")
    
    print("\n3/5 Testing Chat...")
    try:
        response = await agent.chat_response("Hello", profile, [])
        print(f"   ✅ Chat: {len(response)} character response")
    except Exception as e:
        print(f"   ❌ Chat: {e}")
    
    print("\n4/5 Testing Trends...")
    try:
        trends = await agent.analyze_trends_direct(profile)
        print(f"   ✅ Trends: {len(trends.get('trending_topics', []))} topics found")
    except Exception as e:
        print(f"   ❌ Trends: {e}")
    
    print("\n5/5 Testing React Agent...")
    try:
        status = agent.get_bot_state_summary()
        print(f"   ✅ React Agent: {status['agent_state']['current_state']} state")
    except Exception as e:
        print(f"   ❌ React Agent: {e}")
    
    print("\n🎉 All tests completed!")

def launch_streamlit_app():
    """Launch Streamlit app"""
    print("\n🚀 Launching Streamlit App...")
    print("Choose which app to launch:")
    print("1. app_production.py (Recommended)")
    print("2. app.py (Original)")
    print("3. app_modern.py (Modern UI)")
    print("4. app_native.py (Native Components)")
    
    choice = input("Enter choice (1-4): ").strip()
    
    app_files = {
        "1": "app_production.py",
        "2": "app.py", 
        "3": "app_modern.py",
        "4": "app_native.py"
    }
    
    app_file = app_files.get(choice, "app_production.py")
    
    print(f"🚀 Launching {app_file}...")
    print("📱 App will open at: http://localhost:8501")
    print("⚠️ Press Ctrl+C to stop the app")
    
    os.system(f"streamlit run {app_file}")

if __name__ == "__main__":
    asyncio.run(test_agent())