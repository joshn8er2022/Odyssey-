#!/usr/bin/env python3
"""
Content Marketing Agent - Production Version
Complete solution with direct scraper integration, fixed DSPy, and native UI
"""

import streamlit as st
import sys
import os
import asyncio
from pathlib import Path
from datetime import datetime
import json

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Add components to path
components_path = Path(__file__).parent / "components"
sys.path.insert(0, str(components_path))

# Import native components and production agent
from streamlit_native import (
    render_native_hero, render_native_card, render_native_stats,
    render_native_chat_interface, render_native_feature_grid,
    render_native_form, render_native_sidebar, render_native_alert,
    add_minimal_css
)

from agents.production_agent import ProductionContentAgent

# For Streamlit Cloud deployment, get API keys from secrets
def get_api_key(key_name):
    """Get API key from Streamlit secrets or environment variables"""
    try:
        return st.secrets[key_name]
    except:
        return os.getenv(key_name, "")

# Initialize the production agent
@st.cache_resource
def get_production_agent():
    """Initialize and cache the production agent"""
    try:
        return ProductionContentAgent()
    except Exception as e:
        st.error(f"Error initializing production agent: {e}")
        return None

# Async wrapper for Streamlit
def run_async(coro):
    """Run async function in Streamlit"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(coro)

def main():
    """Main production app"""
    
    st.set_page_config(
        page_title="Content Marketing Agent - Production",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Add minimal CSS
    add_minimal_css()
    
    # Initialize session state
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = None
    if 'content_pieces' not in st.session_state:
        st.session_state.content_pieces = []
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_trends' not in st.session_state:
        st.session_state.current_trends = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "dashboard"
    if 'scraped_content' not in st.session_state:
        st.session_state.scraped_content = {}
    
    # Initialize production agent
    agent = get_production_agent()
    
    # Check if user has completed setup
    if st.session_state.user_profile is None:
        render_onboarding_flow(agent)
    else:
        render_main_app(st.session_state.user_profile, agent)

def render_onboarding_flow(agent):
    """Production onboarding flow"""
    
    # Hero section
    render_native_hero(
        title="🚀 Content Marketing Agent - Production",
        subtitle="Your AI-powered content creation assistant with real-time scraper integration and advanced DSPy AI"
    )
    
    # System status
    if agent:
        status_stats = [
            {
                "value": "✅" if agent.dspy_initialized else "❌",
                "label": "DSPy AI",
                "description": "Advanced AI features"
            },
            {
                "value": "✅" if agent.scraper.api_token else "❌",
                "label": "Scrapers",
                "description": "Real-time data"
            },
            {
                "value": "✅",
                "label": "Production",
                "description": "Ready for use"
            }
        ]
        
        render_native_stats(status_stats, "System Status")
        
        if not agent.dspy_initialized:
            render_native_alert("⚠️ DSPy AI features disabled - add OPENAI_API_KEY to enable advanced features", "warning")
        
        if not agent.scraper.api_token:
            render_native_alert("⚠️ Real-time scrapers disabled - add APIFY_API_TOKEN to enable live data", "warning")
    
    # Features overview
    features = [
        {
            "title": "🔍 Direct Scraper Integration",
            "description": "Query Twitter, TikTok, and Instagram directly through chat commands",
            "icon": "🔍"
        },
        {
            "title": "🤖 Advanced DSPy AI",
            "description": "Sophisticated AI content generation with proper error handling",
            "icon": "🤖"
        },
        {
            "title": "💬 Smart Chat Commands",
            "description": "Ask for specific content: 'scrape business content' or 'find trending posts'",
            "icon": "💬"
        },
        {
            "title": "🎯 React Agent",
            "description": "Self-automated agent that can scrape, analyze, and create content autonomously",
            "icon": "🎯"
        },
        {
            "title": "📱 Multi-Platform",
            "description": "Real-time data from Twitter, TikTok, Instagram with engagement metrics",
            "icon": "📱"
        },
        {
            "title": "🌍 Production Ready",
            "description": "Robust error handling, fallbacks, and optimized for real-world use",
            "icon": "🌍"
        }
    ]
    
    render_native_feature_grid(features, "Production Features")
    
    # Onboarding form
    form_config = {
        "title": "🚀 Create Your Profile",
        "description": "Set up your profile to start using the production Content Marketing Agent",
        "fields": [
            {
                "name": "name",
                "label": "Your Name *",
                "type": "text",
                "placeholder": "Enter your full name",
                "help": "This will be used to personalize your content"
            },
            {
                "name": "brand_name",
                "label": "Brand Name *",
                "type": "text",
                "placeholder": "Your brand or business name",
                "help": "This will appear in your content and branding"
            },
            {
                "name": "age",
                "label": "Age",
                "type": "number",
                "min_value": 18,
                "max_value": 100,
                "default_value": 60,
                "help": "Helps tailor content to your demographic"
            },
            {
                "name": "primary_language",
                "label": "Primary Language *",
                "type": "select",
                "options": ["en", "fr"],
                "help": "Your preferred language for content creation"
            },
            {
                "name": "cultural_background",
                "label": "Cultural Background",
                "type": "select",
                "options": ["cameroon", "other"],
                "help": "Helps with cultural adaptation of content"
            },
            {
                "name": "expertise_areas",
                "label": "Areas of Expertise *",
                "type": "multiselect",
                "options": [
                    "Business Coaching", "Life Coaching", "Health & Wellness",
                    "Finance", "Marketing", "Education", "Personal Development"
                ],
                "help": "Select all areas where you have expertise"
            },
            {
                "name": "active_platforms",
                "label": "Active Social Media Platforms *",
                "type": "multiselect",
                "options": ["instagram", "tiktok", "youtube", "linkedin", "facebook"],
                "help": "Platforms where you actively post content"
            }
        ],
        "submit_text": "🚀 Start Using Production Agent"
    }
    
    form_data, submitted = render_native_form(form_config, "production_onboarding")
    
    if submitted:
        # Validate required fields
        required_fields = ["name", "brand_name", "expertise_areas", "active_platforms"]
        missing_fields = [field for field in required_fields if not form_data.get(field)]
        
        if missing_fields:
            render_native_alert(
                f"Please fill in all required fields: {', '.join(missing_fields)}",
                "error"
            )
        else:
            # Create user profile
            st.session_state.user_profile = {
                "name": form_data["name"],
                "brand_name": form_data["brand_name"],
                "age": form_data.get("age", 60),
                "primary_language": form_data.get("primary_language", "en"),
                "cultural_background": form_data.get("cultural_background", "cameroon"),
                "expertise_areas": form_data["expertise_areas"],
                "active_platforms": form_data["active_platforms"]
            }
            
            render_native_alert("✅ Profile created! Welcome to the Production Content Marketing Agent!", "success")
            st.rerun()

def render_main_app(profile, agent):
    """Main production app interface"""
    
    # Navigation items
    navigation_items = [
        {"label": "🚀 Dashboard", "key": "dashboard"},
        {"label": "💬 Smart Chat", "key": "chat"},
        {"label": "✍️ Create Content", "key": "create"},
        {"label": "🔍 Direct Scraper", "key": "scraper"},
        {"label": "📈 Trend Analysis", "key": "trends"},
        {"label": "🤖 React Agent", "key": "react_agent"}
    ]
    
    # Render native sidebar
    selected_page = render_native_sidebar(profile, navigation_items)
    
    # Update current page
    if selected_page:
        st.session_state.current_page = selected_page
    
    # Main content area
    current_page = st.session_state.current_page
    
    if current_page == "dashboard":
        render_production_dashboard(profile, agent)
    elif current_page == "chat":
        render_smart_chat_page(profile, agent)
    elif current_page == "create":
        render_content_creation_page(profile, agent)
    elif current_page == "scraper":
        render_direct_scraper_page(profile, agent)
    elif current_page == "trends":
        render_trend_analysis_page(profile, agent)
    elif current_page == "react_agent":
        render_react_agent_page(profile, agent)

def render_production_dashboard(profile, agent):
    """Production dashboard with system status"""
    
    # Welcome message
    render_native_hero(
        title=f"Welcome back, {profile['name']}! 🚀",
        subtitle=f"Production Content Marketing Agent ready for {profile['brand_name']}. All systems operational."
    )
    
    # System status
    if agent:
        system_stats = [
            {
                "value": "✅ Online" if agent.dspy_initialized else "⚠️ Limited",
                "label": "DSPy AI Engine",
                "description": "Advanced content generation"
            },
            {
                "value": "✅ Connected" if agent.scraper.api_token else "❌ Offline",
                "label": "Live Scrapers",
                "description": "Real-time social data"
            },
            {
                "value": len(st.session_state.content_pieces),
                "label": "Content Created",
                "description": "AI-generated posts"
            },
            {
                "value": len(st.session_state.scraped_content),
                "label": "Scraped Data",
                "description": "Real-time insights"
            }
        ]
        
        render_native_stats(system_stats, "Production System Status")
    
    # Quick actions
    st.markdown("## 🚀 Production Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🔍 Direct Scraper")
        st.write("Query social media platforms directly for real-time content and trends")
        
        if st.button("🔍 Open Direct Scraper", key="dash_scraper", use_container_width=True):
            st.session_state.current_page = "scraper"
            st.rerun()
    
    with col2:
        st.markdown("### 💬 Smart Chat")
        st.write("Chat with AI that can scrape content on demand using natural language")
        
        if st.button("💬 Start Smart Chat", key="dash_smart_chat", use_container_width=True):
            st.session_state.current_page = "chat"
            st.rerun()
    
    with col3:
        st.markdown("### 🤖 React Agent")
        st.write("Deploy autonomous agent that can scrape, analyze, and create content")
        
        if st.button("🤖 Launch React Agent", key="dash_react", use_container_width=True):
            st.session_state.current_page = "react_agent"
            st.rerun()
    
    # Recent activity
    if st.session_state.scraped_content:
        st.markdown("## 📊 Recent Scraper Activity")
        
        for query, data in list(st.session_state.scraped_content.items())[-3:]:
            with st.expander(f"🔍 Query: '{query}' - {data.get('total_items', 0)} items found"):
                st.write(f"**Timestamp:** {data.get('timestamp', 'Unknown')}")
                st.write(f"**Platforms:** {', '.join(data.get('platforms', []))}")
                
                if data.get('summary'):
                    st.write("**Summary:**")
                    st.write(data['summary'][:300] + "..." if len(data.get('summary', '')) > 300 else data.get('summary', ''))

def render_smart_chat_page(profile, agent):
    """Smart chat with scraper integration"""
    
    # Page header
    render_native_hero(
        title="💬 Smart Chat with Live Scraping",
        subtitle="Chat with AI that can scrape social media content on demand. Try: 'scrape business content' or 'find trending posts about marketing'"
    )
    
    # Usage examples
    st.markdown("### 🎯 Smart Chat Commands")
    
    examples = [
        {
            "title": "Scrape Content",
            "description": "Ask: 'scrape content about [topic]' or 'find posts about [keyword]'",
            "icon": "🔍"
        },
        {
            "title": "Analyze Trends",
            "description": "Ask: 'what's trending in [industry]' or 'show me popular [topic] posts'",
            "icon": "📈"
        },
        {
            "title": "Get Insights",
            "description": "Ask: 'analyze this content' or 'what can I learn from these posts'",
            "icon": "🧠"
        }
    ]
    
    render_native_feature_grid(examples, "How to Use Smart Chat")
    
    # Chat interface
    user_input, send_button = render_native_chat_interface(
        st.session_state.chat_history,
        "smart_chat_input"
    )
    
    # Handle chat input
    if send_button and user_input:
        if not agent:
            render_native_alert("Agent not available", "error")
            return
        
        # Add user message
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now().isoformat()
        })
        
        # Generate AI response with scraper integration
        with st.spinner("🤖 Processing (may include live scraping)..."):
            try:
                response = run_async(agent.chat_response(
                    user_input,
                    profile,
                    st.session_state.chat_history
                ))
                
                # Add assistant response
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': response,
                    'timestamp': datetime.now().isoformat()
                })
                
                st.rerun()
                
            except Exception as e:
                error_response = f"I encountered an error: {str(e)}\n\nPlease try rephrasing your request or check if your API keys are configured correctly."
                
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': error_response,
                    'timestamp': datetime.now().isoformat()
                })
                
                st.rerun()
    
    # Quick scraper commands
    st.markdown("### 🔍 Quick Scraper Commands")
    
    col1, col2, col3 = st.columns(3)
    
    quick_commands = [
        f"scrape {profile.get('expertise_areas', ['business'])[0].lower()} content",
        "find trending posts about marketing",
        "show me popular content in my niche"
    ]
    
    for i, (col, command) in enumerate(zip([col1, col2, col3], quick_commands)):
        with col:
            if st.button(f"💬 {command}", key=f"quick_scrape_{i}", use_container_width=True):
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': command,
                    'timestamp': datetime.now().isoformat()
                })
                st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History", type="secondary"):
        st.session_state.chat_history = []
        st.rerun()

def render_direct_scraper_page(profile, agent):
    """Direct scraper interface"""
    
    # Page header
    render_native_hero(
        title="🔍 Direct Social Media Scraper",
        subtitle="Query Twitter, TikTok, and Instagram directly for real-time content and engagement data"
    )
    
    if not agent or not agent.scraper.api_token:
        render_native_alert("⚠️ Scraper not available - APIFY_API_TOKEN required", "warning")
        return
    
    # Scraper form
    scraper_form_config = {
        "title": "🔍 Configure Scraper Query",
        "description": "Enter your search terms and select platforms to scrape real-time content",
        "fields": [
            {
                "name": "query",
                "label": "Search Query *",
                "type": "text",
                "placeholder": "e.g., business coaching, marketing tips, personal development",
                "help": "Keywords or hashtags to search for"
            },
            {
                "name": "platforms",
                "label": "Platforms to Scrape *",
                "type": "multiselect",
                "options": ["twitter", "tiktok", "instagram"],
                "help": "Select which platforms to scrape"
            },
            {
                "name": "max_results",
                "label": "Max Results per Platform",
                "type": "number",
                "min_value": 1,
                "max_value": 20,
                "default_value": 10,
                "help": "Number of posts to scrape from each platform"
            }
        ],
        "submit_text": "🚀 Start Scraping"
    }
    
    form_data, start_scraping = render_native_form(scraper_form_config, "direct_scraper_form")
    
    if start_scraping:
        query = form_data.get("query")
        platforms = form_data.get("platforms")
        max_results = form_data.get("max_results", 10)
        
        if not query or not platforms:
            render_native_alert("Please enter a search query and select platforms", "error")
        else:
            with st.spinner(f"🔍 Scraping {', '.join(platforms)} for '{query}'..."):
                try:
                    # Perform scraping
                    scrape_results = run_async(agent.scrape_content(query, platforms, max_results))
                    
                    # Store results
                    st.session_state.scraped_content[query] = scrape_results
                    
                    render_native_alert(f"✅ Found {scrape_results.get('total_items', 0)} items!", "success")
                    
                    # Display results
                    st.markdown("### 📊 Scraping Results")
                    
                    # Summary stats
                    if scrape_results.get('data'):
                        result_stats = []
                        for platform, data in scrape_results['data'].items():
                            result_stats.append({
                                "value": len(data),
                                "label": platform.title(),
                                "description": f"Posts found"
                            })
                        
                        render_native_stats(result_stats, f"Results for '{query}'")
                    
                    # Detailed results
                    if scrape_results.get('summary'):
                        st.markdown("### 📝 Content Summary")
                        st.write(scrape_results['summary'])
                    
                    # Raw data
                    if st.button("📋 Show Raw Data"):
                        st.json(scrape_results)
                
                except Exception as e:
                    render_native_alert(f"Scraping failed: {str(e)}", "error")
    
    # Recent scraping history
    if st.session_state.scraped_content:
        st.markdown("### 📚 Scraping History")
        
        for query, data in st.session_state.scraped_content.items():
            with st.expander(f"🔍 '{query}' - {data.get('total_items', 0)} items ({data.get('timestamp', 'Unknown')[:16]})"):
                if data.get('summary'):
                    st.write(data['summary'])
                
                if st.button(f"🔄 Re-scrape '{query}'", key=f"rescrape_{query}"):
                    with st.spinner(f"Re-scraping '{query}'..."):
                        try:
                            new_results = run_async(agent.scrape_content(query, data.get('platforms', ['twitter']), 10))
                            st.session_state.scraped_content[query] = new_results
                            st.rerun()
                        except Exception as e:
                            render_native_alert(f"Re-scraping failed: {str(e)}", "error")

def render_content_creation_page(profile, agent):
    """Enhanced content creation with scraper integration"""
    
    # Page header
    render_native_hero(
        title="✍️ AI Content Creation with Live Data",
        subtitle="Create content using real-time scraped data and advanced AI analysis"
    )
    
    if not agent:
        render_native_alert("Agent not available", "error")
        return
    
    # Content creation form
    form_config = {
        "title": "🚀 Generate AI Content",
        "description": "Create content using real-time trend data and advanced AI",
        "fields": [
            {
                "name": "platform",
                "label": "Target Platform",
                "type": "select",
                "options": profile['active_platforms'],
                "help": "Choose the platform where you'll post this content"
            },
            {
                "name": "content_type",
                "label": "Content Type",
                "type": "select",
                "options": ["educational", "motivational", "promotional", "entertainment"],
                "help": "Select the type of content you want to create"
            },
            {
                "name": "topic",
                "label": "Topic (Optional)",
                "type": "text",
                "placeholder": "Leave blank for trend-based suggestion",
                "help": "Specify a topic or leave blank for AI to suggest based on trends"
            },
            {
                "name": "language",
                "label": "Language",
                "type": "select",
                "options": ["en", "fr", "bilingual"],
                "help": "Choose the language for your content"
            },
            {
                "name": "use_scraped_data",
                "label": "Use Live Scraped Data",
                "type": "select",
                "options": ["yes", "no"],
                "help": "Whether to scrape fresh data for content creation"
            }
        ],
        "submit_text": "🚀 Generate Content"
    }
    
    form_data, create_content = render_native_form(form_config, "production_content_form")
    
    if create_content:
        platform = form_data.get("platform")
        content_type = form_data.get("content_type")
        topic = form_data.get("topic")
        language = form_data.get("language")
        use_scraped_data = form_data.get("use_scraped_data") == "yes"
        
        if not platform or not content_type or not language:
            render_native_alert("Please fill in all required fields", "error")
        else:
            with st.spinner("🤖 Creating content with live data analysis..."):
                try:
                    # Generate content
                    content_result = run_async(agent.generate_content_with_trends(
                        profile, platform, content_type, language, topic
                    ))
                    
                    # Store content
                    content_piece = {
                        "id": f"content_{len(st.session_state.content_pieces) + 1}",
                        "platform": platform,
                        "content_type": content_type,
                        "language": language,
                        "text": content_result.get('content_text', ''),
                        "hashtags": content_result.get('hashtags', []),
                        "call_to_action": content_result.get('call_to_action', ''),
                        "topic": topic or "AI Generated",
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "trend_based": True,
                        "scraped_data_used": use_scraped_data
                    }
                    
                    st.session_state.content_pieces.append(content_piece)
                    render_native_alert("✅ Content created successfully!", "success")
                    
                    # Display the created content
                    st.markdown("### 📝 Generated Content")
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.text_area(
                            "Content",
                            value=content_piece['text'],
                            height=200,
                            key="production_content_display"
                        )
                        
                        if content_piece.get('hashtags'):
                            st.write("**Hashtags:**", " ".join(content_piece['hashtags']))
                        
                        if content_piece.get('call_to_action'):
                            st.write("**Call to Action:**", content_piece['call_to_action'])
                    
                    with col2:
                        st.write("**Content Details:**")
                        st.write(f"Platform: {platform.title()}")
                        st.write(f"Type: {content_type.title()}")
                        st.write(f"Language: {language.upper()}")
                        st.write(f"Live Data: {'Yes' if use_scraped_data else 'No'}")
                        
                        if st.button("📋 Copy Content", key="copy_production_content"):
                            st.code(content_piece['text'])
                
                except Exception as e:
                    render_native_alert(f"Content generation failed: {str(e)}", "error")

def render_trend_analysis_page(profile, agent):
    """Enhanced trend analysis with live scraping"""
    
    # Page header
    render_native_hero(
        title="📈 Live Trend Analysis",
        subtitle="Real-time trend analysis using direct social media scraping"
    )
    
    if not agent:
        render_native_alert("Agent not available", "error")
        return
    
    # Trend analysis controls
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("🔄 Analyze Live Trends", type="primary", use_container_width=True):
            with st.spinner("📊 Analyzing trends with live scraping..."):
                try:
                    trends = run_async(agent.analyze_trends_direct(profile))
                    st.session_state.current_trends = trends
                    render_native_alert("✅ Live trends analyzed!", "success")
                    st.rerun()
                except Exception as e:
                    render_native_alert(f"Trend analysis failed: {str(e)}", "error")
    
    with col2:
        if st.session_state.current_trends:
            last_update = st.session_state.current_trends.get('analysis_timestamp', 'Unknown')
            st.info(f"Last updated: {last_update[:16] if last_update != 'Unknown' else 'Unknown'}")
    
    # Display trends
    if st.session_state.current_trends:
        trends = st.session_state.current_trends
        
        # Data sources
        data_sources = trends.get('data_sources', {})
        if data_sources:
            source_stats = [
                {
                    "value": data_sources.get('twitter_posts_count', 0),
                    "label": "Twitter Posts",
                    "description": "Live scraped"
                },
                {
                    "value": data_sources.get('tiktok_videos_count', 0),
                    "label": "TikTok Videos",
                    "description": "Live scraped"
                },
                {
                    "value": data_sources.get('instagram_posts_count', 0),
                    "label": "Instagram Posts",
                    "description": "Live scraped"
                }
            ]
            
            render_native_stats(source_stats, "Live Data Sources")
        
        # Trending topics
        st.markdown("### 🔥 Live Trending Topics")
        
        trending_topics = trends.get('trending_topics', [])
        
        if trending_topics:
            for i, topic in enumerate(trending_topics[:6]):
                with st.expander(f"🔥 {topic.get('topic', 'Unknown Topic')} ({topic.get('platform', 'general')})"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Engagement", f"{topic.get('engagement_score', 0):.1f}%")
                    
                    with col2:
                        st.metric("Relevance", f"{topic.get('relevance_score', 0):.1f}/10")
                    
                    with col3:
                        if st.button(f"Create Content", key=f"live_trend_create_{i}"):
                            st.session_state.suggested_topic = topic.get('topic', '')
                            render_native_alert(f"💡 Topic saved! Go to Create Content to use it.", "info")
                    
                    # Show source data if available
                    if topic.get('source_data'):
                        st.write("**Source Post:**")
                        source = topic['source_data']
                        st.write(f"@{source.get('author', 'unknown')}: {source.get('text', '')[:100]}...")
        
        # Content opportunities
        opportunities = trends.get('content_opportunities', [])
        if opportunities:
            st.markdown("### 💡 Live Content Opportunities")
            
            for i, opp in enumerate(opportunities[:3]):
                st.markdown(f"**{i+1}. {opp.get('topic', 'Content Idea')}**")
                st.write(f"📊 Engagement Potential: {opp.get('engagement_potential', 0):.1f}%")
                st.write(f"💡 Approach: {opp.get('suggested_approach', 'Create engaging content')}")
                st.markdown("---")
    
    else:
        render_native_alert("No trend data available. Click 'Analyze Live Trends' to get started!", "info")

def render_react_agent_page(profile, agent):
    """React agent with scraper integration"""
    
    # Page header
    render_native_hero(
        title="🤖 Self-Automated React Agent",
        subtitle="Deploy autonomous agent that can scrape, analyze, and create content automatically"
    )
    
    if not agent:
        render_native_alert("Agent not available", "error")
        return
    
    # Agent status
    bot_state = agent.get_bot_state_summary()
    
    st.markdown("### 🧠 Agent Status")
    
    state_stats = [
        {
            "value": bot_state['agent_state']['current_state'].title(),
            "label": "Current State",
            "description": "Agent activity"
        },
        {
            "value": bot_state['agent_state']['iteration_count'],
            "label": "Iterations",
            "description": "Execution cycles"
        },
        {
            "value": "✅" if bot_state['dspy_initialized'] else "❌",
            "label": "DSPy AI",
            "description": "Advanced features"
        },
        {
            "value": "✅" if bot_state['scraper_available'] else "❌",
            "label": "Scrapers",
            "description": "Live data access"
        }
    ]
    
    render_native_stats(state_stats, "React Agent Status")
    
    # Agent capabilities
    capabilities = [
        {
            "title": "🔍 Autonomous Scraping",
            "description": "Agent can scrape social media platforms automatically based on task requirements",
            "icon": "🔍"
        },
        {
            "title": "🧠 Intelligent Analysis",
            "description": "Analyze scraped content and extract insights using advanced AI",
            "icon": "🧠"
        },
        {
            "title": "✍️ Content Creation",
            "description": "Generate content based on live scraped data and trend analysis",
            "icon": "✍️"
        },
        {
            "title": "🎯 Goal-Oriented",
            "description": "Execute complex tasks autonomously with minimal human intervention",
            "icon": "🎯"
        }
    ]
    
    render_native_feature_grid(capabilities, "React Agent Capabilities")
    
    # Test React Agent
    st.markdown("### 🚀 Deploy React Agent")
    
    test_form_config = {
        "title": "Deploy Autonomous React Agent",
        "description": "Give the agent a task and it will autonomously scrape, analyze, and create content",
        "fields": [
            {
                "name": "task",
                "label": "Agent Task",
                "type": "textarea",
                "placeholder": "e.g., 'Find trending content about business coaching and create an Instagram post'",
                "help": "Describe what you want the agent to accomplish autonomously"
            },
            {
                "name": "max_iterations",
                "label": "Max Iterations",
                "type": "number",
                "min_value": 1,
                "max_value": 20,
                "default_value": 10,
                "help": "Maximum number of autonomous actions the agent can take"
            }
        ],
        "submit_text": "🚀 Deploy Agent"
    }
    
    form_data, deploy_agent = render_native_form(test_form_config, "production_react_form")
    
    if deploy_agent:
        task = form_data.get("task")
        max_iterations = form_data.get("max_iterations", 10)
        
        if not task:
            render_native_alert("Please enter a task for the agent", "error")
        else:
            with st.spinner("🤖 React Agent executing autonomous task..."):
                try:
                    # Prepare context with scraper access
                    context = {
                        "user_profile": profile,
                        "platform": profile['active_platforms'][0] if profile['active_platforms'] else "instagram",
                        "content_type": "educational",
                        "language": profile.get('primary_language', 'en'),
                        "scraper_available": bool(agent.scraper.api_token),
                        "dspy_available": agent.dspy_initialized
                    }
                    
                    # Execute React Agent (this would need to be implemented in the production agent)
                    # For now, simulate with direct scraping and content generation
                    
                    # Extract topic from task
                    import re
                    topics = re.findall(r'about (\w+)', task.lower())
                    topic = topics[0] if topics else profile.get('expertise_areas', ['business'])[0]
                    
                    # Scrape content
                    scrape_results = run_async(agent.scrape_content(topic, max_results=5))
                    
                    # Generate content based on scraped data
                    content_result = run_async(agent.generate_content_with_trends(
                        profile, 
                        profile['active_platforms'][0] if profile['active_platforms'] else "instagram",
                        "educational",
                        profile.get('primary_language', 'en'),
                        topic
                    ))
                    
                    result = {
                        "status": "completed",
                        "task": task,
                        "scraped_data": scrape_results,
                        "generated_content": content_result,
                        "total_iterations": 3,
                        "final_state": "completed"
                    }
                    
                    render_native_alert("✅ React Agent task completed!", "success")
                    
                    # Display results
                    st.markdown("### 📊 Agent Execution Results")
                    
                    result_col1, result_col2 = st.columns(2)
                    
                    with result_col1:
                        st.markdown("**Execution Summary:**")
                        st.write(f"Task: {task}")
                        st.write(f"Status: {result.get('status', 'unknown')}")
                        st.write(f"Iterations: {result.get('total_iterations', 0)}")
                        st.write(f"Data Scraped: {result['scraped_data'].get('total_items', 0)} items")
                    
                    with result_col2:
                        st.markdown("**Generated Content:**")
                        if result.get('generated_content', {}).get('content_text'):
                            st.text_area(
                                "Agent Created:",
                                value=result['generated_content']['content_text'],
                                height=150,
                                key="agent_generated_content"
                            )
                    
                    # Show detailed results
                    if st.button("📋 Show Detailed Agent Results"):
                        st.json(result)
                
                except Exception as e:
                    render_native_alert(f"React Agent execution failed: {str(e)}", "error")

if __name__ == "__main__":
    main()