# 🚀 Local Testing Guide - Content Marketing Agent

## Quick Start Commands

### 1. **Production App (Recommended)**
```bash
# Navigate to project
cd content-marketing-agent

# Install dependencies
pip install -r requirements.txt

# Run production app
streamlit run app_production.py
```

### 2. **Alternative Apps**
```bash
# Original app with all features
streamlit run app.py

# Modern UI version
streamlit run app_modern.py

# Native components version
streamlit run app_native.py
```

## 🔧 Environment Setup

### **Option 1: Using .env file (Recommended)**
```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your API keys
nano .env
# or
code .env
```

Add your API keys to `.env`:
```env
OPENAI_API_KEY=your_openai_key_here
APIFY_API_TOKEN=your_apify_token_here
```

### **Option 2: Export environment variables**
```bash
# Set API keys for current session
export OPENAI_API_KEY="your_openai_key_here"
export APIFY_API_TOKEN="your_apify_token_here"

# Run the app
streamlit run app_production.py
```

### **Option 3: Inline environment variables**
```bash
# Run with environment variables inline
OPENAI_API_KEY="your_key" APIFY_API_TOKEN="your_token" streamlit run app_production.py
```

## 🧪 Testing Different Features

### **Test 1: Basic App Launch (No API Keys)**
```bash
# Test app launches without API keys
streamlit run app_production.py

# Expected: App loads with warnings about missing API keys
# Features available: Basic UI, fallback content generation
```

### **Test 2: DSPy AI Features (OpenAI API Key Only)**
```bash
# Set only OpenAI key
export OPENAI_API_KEY="your_openai_key"
streamlit run app_production.py

# Expected: Advanced AI content generation works
# Missing: Real-time scraping features
```

### **Test 3: Full Production Mode (Both API Keys)**
```bash
# Set both API keys
export OPENAI_API_KEY="your_openai_key"
export APIFY_API_TOKEN="your_apify_token"
streamlit run app_production.py

# Expected: All features work including live scraping
```

### **Test 4: Direct Scraper Testing**
```bash
# Test scraper independently
cd src/scrapers
python -c "
import asyncio
from direct_scraper import DirectScraper
scraper = DirectScraper()
print('Scraper initialized:', bool(scraper.api_token))
"
```

### **Test 5: Production Agent Testing**
```bash
# Test production agent
cd src/agents
python -c "
from production_agent import ProductionContentAgent
agent = ProductionContentAgent()
print('DSPy initialized:', agent.dspy_initialized)
print('Scraper available:', bool(agent.scraper.api_token))
"
```

## 🔍 Command Line Testing Scripts

### **Quick Health Check**
```bash
# Create and run health check
cat > health_check.py << 'EOF'
#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from agents.production_agent import ProductionContentAgent
    agent = ProductionContentAgent()
    
    print("🚀 Content Marketing Agent Health Check")
    print("=" * 50)
    print(f"✅ Production Agent: Initialized")
    print(f"🤖 DSPy AI: {'✅ Ready' if agent.dspy_initialized else '⚠️ Limited (no OpenAI key)'}")
    print(f"🔍 Scrapers: {'✅ Ready' if agent.scraper.api_token else '⚠️ Offline (no Apify token)'}")
    print(f"🛠️ Available Tools: {len(agent.tools)}")
    print(f"📝 DSPy Signatures: {len(agent.signatures)}")
    
    # Test basic functionality
    state = agent.get_bot_state_summary()
    print(f"🤖 React Agent: {state['agent_state']['current_state']}")
    
    print("\n🎯 Ready for testing!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("Check your dependencies and API keys")

EOF

python health_check.py
```

### **Interactive Testing Session**
```bash
# Create interactive test script
cat > interactive_test.py << 'EOF'
#!/usr/bin/env python3
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from agents.production_agent import ProductionContentAgent

async def test_agent():
    agent = ProductionContentAgent()
    
    print("🚀 Interactive Content Marketing Agent Test")
    print("=" * 50)
    
    # Test profile
    test_profile = {
        "name": "Test User",
        "brand_name": "Test Brand",
        "expertise_areas": ["Business Coaching"],
        "active_platforms": ["instagram"],
        "primary_language": "en",
        "cultural_background": "cameroon"
    }
    
    while True:
        print("\n🎯 Available Tests:")
        print("1. Test scraper (requires APIFY_API_TOKEN)")
        print("2. Test content generation")
        print("3. Test chat response")
        print("4. Test trend analysis")
        print("5. Show agent status")
        print("6. Exit")
        
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == "1":
            query = input("Enter search query: ").strip() or "business coaching"
            print(f"🔍 Scraping for '{query}'...")
            try:
                results = await agent.scrape_content(query, max_results=3)
                print(f"✅ Found {results.get('total_items', 0)} items")
                print(results.get('summary', 'No summary available')[:300])
            except Exception as e:
                print(f"❌ Scraping failed: {e}")
        
        elif choice == "2":
            print("🤖 Generating content...")
            try:
                content = await agent.generate_content_with_trends(
                    test_profile, "instagram", "educational", "en"
                )
                print("✅ Content generated:")
                print(content.get('content_text', 'No content generated')[:200])
            except Exception as e:
                print(f"❌ Content generation failed: {e}")
        
        elif choice == "3":
            message = input("Enter chat message: ").strip() or "Hello"
            print(f"💬 Processing '{message}'...")
            try:
                response = await agent.chat_response(message, test_profile, [])
                print("✅ Chat response:")
                print(response[:300])
            except Exception as e:
                print(f"❌ Chat failed: {e}")
        
        elif choice == "4":
            print("📈 Analyzing trends...")
            try:
                trends = await agent.analyze_trends_direct(test_profile)
                print(f"✅ Found {len(trends.get('trending_topics', []))} trending topics")
                for topic in trends.get('trending_topics', [])[:2]:
                    print(f"- {topic.get('topic', 'Unknown')}: {topic.get('engagement_score', 0):.1f}%")
            except Exception as e:
                print(f"❌ Trend analysis failed: {e}")
        
        elif choice == "5":
            status = agent.get_bot_state_summary()
            print("🤖 Agent Status:")
            print(f"- DSPy: {'✅' if status['dspy_initialized'] else '❌'}")
            print(f"- Scrapers: {'✅' if status['scraper_available'] else '❌'}")
            print(f"- State: {status['agent_state']['current_state']}")
            print(f"- Tools: {len(status['available_tools'])}")
        
        elif choice == "6":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    asyncio.run(test_agent())

EOF

python interactive_test.py
```

## 🌐 Browser Testing

### **Local URLs**
After running `streamlit run app_production.py`, access:
- **Main App**: http://localhost:8501
- **Network URL**: Usually shown in terminal (e.g., http://192.168.1.x:8501)

### **Test Different Browsers**
```bash
# Chrome
open -a "Google Chrome" http://localhost:8501

# Firefox  
open -a Firefox http://localhost:8501

# Safari
open -a Safari http://localhost:8501
```

## 🐛 Troubleshooting

### **Common Issues & Solutions**

#### **1. Import Errors**
```bash
# If you get import errors, install dependencies
pip install -r requirements.txt

# Or install specific packages
pip install streamlit dspy-ai httpx asyncio
```

#### **2. Port Already in Use**
```bash
# Use different port
streamlit run app_production.py --server.port 8502

# Or kill existing Streamlit processes
pkill -f streamlit
```

#### **3. API Key Issues**
```bash
# Check if environment variables are set
echo $OPENAI_API_KEY
echo $APIFY_API_TOKEN

# Check .env file
cat .env
```

#### **4. Module Not Found**
```bash
# Make sure you're in the right directory
pwd
# Should show: /path/to/content-marketing-agent

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

## 📊 Performance Testing

### **Load Testing**
```bash
# Test multiple concurrent users (requires siege)
# brew install siege  # macOS
# sudo apt-get install siege  # Ubuntu

siege -c 5 -t 30s http://localhost:8501
```

### **Memory Usage**
```bash
# Monitor memory usage while running
top -pid $(pgrep -f "streamlit run")

# Or use htop
htop -p $(pgrep -f "streamlit run")
```

## 🚀 Quick Demo Commands

### **Full Feature Demo**
```bash
# Set API keys and run full demo
export OPENAI_API_KEY="your_key"
export APIFY_API_TOKEN="your_token"
streamlit run app_production.py

# Then in browser:
# 1. Complete onboarding
# 2. Try Smart Chat: "scrape business content"
# 3. Use Direct Scraper page
# 4. Generate content with live data
```

### **Minimal Demo (No API Keys)**
```bash
# Run without API keys to see fallback behavior
streamlit run app_production.py

# Features available:
# - Basic UI navigation
# - Fallback content generation
# - System status indicators
```

---

## 🎯 Next Steps

1. **Start with health check**: `python health_check.py`
2. **Run production app**: `streamlit run app_production.py`
3. **Test interactive features**: `python interactive_test.py`
4. **Add API keys for full functionality**

Your Content Marketing Agent is ready for local testing! 🚀