#!/usr/bin/env python3
"""
Content Marketing Agent - Modern UI Version
Enhanced with 21st.dev-inspired components and modern design
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

# Import modern UI components (with fixed versions as fallback)
try:
    from modern_ui_fixed import (
        render_modern_hero_fixed as render_modern_hero,
        render_modern_card_fixed as render_modern_card,
        render_modern_stats_fixed as render_modern_stats,
        render_modern_chat_interface_fixed as render_modern_chat_interface,
        render_modern_feature_grid_fixed as render_modern_feature_grid,
        render_modern_alert_fixed as render_modern_alert,
        add_modern_css_fixed as add_modern_css
    )
    # Keep the original functions that don't have fixed versions
    from modern_ui import render_modern_form, render_modern_sidebar
except ImportError:
    from modern_ui import (
        render_modern_hero, render_modern_card, render_modern_stats,
        render_modern_chat_interface, render_modern_feature_grid,
        render_modern_form, render_modern_sidebar, render_modern_alert,
        add_modern_css
    )

# For Streamlit Cloud deployment, get API keys from secrets
def get_api_key(key_name):
    """Get API key from Streamlit secrets or environment variables"""
    try:
        return st.secrets[key_name]
    except:
        return os.getenv(key_name, "")

# Initialize the DSPy agent (AI-heavy operations only)
@st.cache_resource
def get_dspy_agent():
    """Initialize and cache the DSPy agent for AI operations"""
    try:
        from agents.dspy_agent import DSPyContentAgent
        return DSPyContentAgent()
    except Exception as e:
        st.error(f"Error initializing DSPy agent: {e}")
        return None

# Initialize content helpers (simple Python utilities)
@st.cache_resource
def get_content_helpers():
    """Initialize content helper utilities"""
    try:
        from utils.content_helpers import ContentFormatter, PlatformOptimizer, TrendDataProcessor, ConversationHelper
        return {
            'formatter': ContentFormatter(),
            'optimizer': PlatformOptimizer(),
            'trend_processor': TrendDataProcessor(),
            'conversation_helper': ConversationHelper()
        }
    except Exception as e:
        st.error(f"Error initializing content helpers: {e}")
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
    """Main Streamlit app with modern UI"""
    
    st.set_page_config(
        page_title="Content Marketing Agent",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Add modern CSS
    add_modern_css()
    
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
    
    # Initialize DSPy agent and content helpers
    agent = get_dspy_agent()
    helpers = get_content_helpers()
    
    # Check if user has completed setup
    if st.session_state.user_profile is None:
        render_onboarding_flow()
    else:
        render_main_app(st.session_state.user_profile, agent, helpers)

def render_onboarding_flow():
    """Modern onboarding flow"""
    
    # Hero section
    render_modern_hero(
        title="🎯 Content Marketing Agent",
        subtitle="Your AI-powered content creation assistant with real-time trend analysis and cultural adaptation",
        gradient_colors=["#667eea", "#764ba2"]
    )
    
    # Features overview
    features = [
        {
            "title": "AI-Powered Content",
            "description": "Generate engaging, culturally-relevant content using advanced DSPy AI technology",
            "icon": "🤖",
            "color": "#667eea"
        },
        {
            "title": "Real-Time Trends",
            "description": "Analyze current trends from Twitter, TikTok, and YouTube using Apify integration",
            "icon": "📈",
            "color": "#764ba2"
        },
        {
            "title": "Multi-Platform",
            "description": "Optimize content for Instagram, TikTok, LinkedIn, Facebook, and YouTube",
            "icon": "📱",
            "color": "#f093fb"
        },
        {
            "title": "Bilingual Support",
            "description": "Create content in English, French, or both with cultural adaptation",
            "icon": "🌍",
            "color": "#4facfe"
        },
        {
            "title": "Smart Chat",
            "description": "Get personalized advice and strategy recommendations from your AI assistant",
            "icon": "💬",
            "color": "#43e97b"
        },
        {
            "title": "Analytics Ready",
            "description": "Track performance and optimize your content strategy with built-in insights",
            "icon": "📊",
            "color": "#fa709a"
        }
    ]
    
    render_modern_feature_grid(features, "Powerful Features")
    
    # Onboarding form
    form_config = {
        "title": "🚀 Create Your Profile",
        "description": "Complete the form below to personalize your AI assistant for your unique needs and cultural context.",
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
        "submit_text": "🚀 Create My Profile"
    }
    
    form_data, submitted = render_modern_form(form_config, "onboarding_form")
    
    if submitted:
        # Validate required fields
        required_fields = ["name", "brand_name", "expertise_areas", "active_platforms"]
        missing_fields = [field for field in required_fields if not form_data.get(field)]
        
        if missing_fields:
            render_modern_alert(
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
            
            render_modern_alert("✅ Profile created successfully! Welcome to your Content Marketing Agent!", "success")
            st.rerun()

def render_main_app(profile, agent, helpers):
    """Main app interface with modern UI"""
    
    # Navigation items
    navigation_items = [
        {"label": "📊 Dashboard", "key": "dashboard"},
        {"label": "💬 AI Chat", "key": "chat"},
        {"label": "✍️ Create Content", "key": "create"},
        {"label": "📈 Trend Analysis", "key": "trends"},
        {"label": "🔗 Social Media", "key": "social"},
        {"label": "🤖 React Agent", "key": "react_agent"}
    ]
    
    # Render modern sidebar
    selected_page = render_modern_sidebar(profile, navigation_items)
    
    # Update current page
    if selected_page:
        st.session_state.current_page = selected_page
    
    # Main content area
    current_page = st.session_state.current_page
    
    if current_page == "dashboard":
        render_modern_dashboard(profile, agent, helpers)
    elif current_page == "chat":
        render_modern_chat_page(profile, agent, helpers)
    elif current_page == "create":
        render_modern_content_creation(profile, agent, helpers)
    elif current_page == "trends":
        render_modern_trend_analysis(profile, agent, helpers)
    elif current_page == "social":
        render_modern_social_connections(profile, agent, helpers)
    elif current_page == "react_agent":
        render_modern_react_agent(profile, agent, helpers)

def render_modern_dashboard(profile, agent, helpers):
    """Modern dashboard with enhanced UI"""
    
    # Welcome hero
    render_modern_hero(
        title=f"Welcome back, {profile['name']}! 👋",
        subtitle=f"Ready to create amazing content for {profile['brand_name']}? Let's analyze trends and generate engaging posts.",
        gradient_colors=["#4facfe", "#00f2fe"]
    )
    
    # Key metrics
    stats = [
        {
            "value": len(profile['active_platforms']),
            "label": "Active Platforms",
            "description": "Connected social media",
            "color": "#667eea"
        },
        {
            "value": len(st.session_state.content_pieces),
            "label": "Content Created",
            "description": "AI-generated posts",
            "color": "#764ba2"
        },
        {
            "value": len(profile['expertise_areas']),
            "label": "Expertise Areas",
            "description": "Your specializations",
            "color": "#f093fb"
        },
        {
            "value": len(st.session_state.chat_history),
            "label": "Chat Messages",
            "description": "AI conversations",
            "color": "#4facfe"
        }
    ]
    
    render_modern_stats(stats, "Your Content Marketing Overview")
    
    # Quick actions
    st.markdown("## 🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_modern_card(
            title="Analyze Trends",
            content="Get real-time insights from social media platforms to inform your content strategy",
            icon="📈",
            accent_color="#667eea",
            action_text="Analyze Now"
        )
        
        if st.button("📈 Analyze Current Trends", key="dash_trends", use_container_width=True):
            with st.spinner("Analyzing trends with Apify..."):
                if agent:
                    trends = run_async(agent.analyze_trends_with_apify(profile))
                    st.session_state.current_trends = trends
                    render_modern_alert("✅ Trends analyzed successfully!", "success")
                    st.rerun()
    
    with col2:
        render_modern_card(
            title="AI Chat Assistant",
            content="Get personalized advice and strategy recommendations from your intelligent assistant",
            icon="💬",
            accent_color="#764ba2",
            action_text="Start Chat"
        )
        
        if st.button("💬 Start Chat Session", key="dash_chat", use_container_width=True):
            st.session_state.current_page = "chat"
            st.rerun()
    
    with col3:
        render_modern_card(
            title="Create Content",
            content="Generate engaging, trend-aware content optimized for your target platforms",
            icon="✍️",
            accent_color="#f093fb",
            action_text="Create Now"
        )
        
        if st.button("✍️ Create Content Now", key="dash_create", use_container_width=True):
            st.session_state.current_page = "create"
            st.rerun()
    
    # Current trends summary
    if st.session_state.current_trends and helpers:
        st.markdown("## 📈 Current Trends Summary")
        
        trends = st.session_state.current_trends
        trending_topics = trends.get('trending_topics', [])[:3]
        
        if trending_topics:
            cols = st.columns(len(trending_topics))
            
            for i, topic in enumerate(trending_topics):
                with cols[i]:
                    render_modern_card(
                        title=topic.get('topic', 'Unknown Topic'),
                        content=f"Platform: {topic.get('platform', 'general').title()}\nEngagement: {topic.get('engagement_score', 0):.1f}%\nRelevance: {topic.get('relevance_score', 0):.1f}/10",
                        icon="🔥",
                        accent_color="#43e97b"
                    )
    
    # Recent content
    if st.session_state.content_pieces:
        st.markdown("## 📝 Recent Content")
        
        recent_content = st.session_state.content_pieces[-3:]  # Show last 3
        
        for i, content in enumerate(recent_content):
            with st.expander(f"📱 {content['platform'].title()} - {content['topic']} ({content['created_at']})"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write("**Content:**")
                    st.write(content['text'])
                    
                    if content.get('hashtags'):
                        st.write("**Hashtags:**", " ".join(content['hashtags']))
                
                with col2:
                    st.write("**Details:**")
                    st.write(f"Platform: {content['platform'].title()}")
                    st.write(f"Type: {content['content_type'].title()}")
                    st.write(f"Language: {content['language'].upper()}")
                    
                    if st.button("📋 Copy Content", key=f"copy_dash_{content['id']}"):
                        st.code(content['text'])

def render_modern_chat_page(profile, agent, helpers):
    """Modern chat interface page"""
    
    # Page header
    render_modern_hero(
        title="💬 AI Content Marketing Assistant",
        subtitle="Get personalized advice, strategy recommendations, and content ideas from your intelligent assistant",
        gradient_colors=["#43e97b", "#38f9d7"]
    )
    
    # Chat interface
    user_input, send_button = render_modern_chat_interface(
        st.session_state.chat_history,
        "main_chat_input"
    )
    
    # Handle chat input
    if send_button and user_input:
        # Add user message
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now().isoformat()
        })
        
        # Generate AI response
        with st.spinner("🤖 Thinking..."):
            if agent and helpers:
                try:
                    response = run_async(agent.chat_response(
                        user_input,
                        profile,
                        st.session_state.chat_history
                    ))
                    
                    # Add follow-up suggestions
                    intent = helpers['conversation_helper'].extract_intent(user_input)
                    follow_ups = helpers['conversation_helper'].generate_follow_up_questions(intent, profile)
                    
                    if follow_ups:
                        response += f"\n\n**💡 You might also want to ask:**\n"
                        for i, question in enumerate(follow_ups[:2], 1):
                            response += f"{i}. {question}\n"
                
                except Exception as e:
                    response = helpers['conversation_helper'].generate_fallback_response(user_input, profile) if helpers else f"I understand you're asking about: {user_input}\n\nBased on your expertise, I'd recommend creating authentic content that showcases your knowledge."
            else:
                response = "I'm here to help with your content marketing! Let me know what you'd like to create or discuss."
        
        # Add assistant response
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now().isoformat()
        })
        
        st.rerun()
    
    # Quick action buttons
    st.markdown("### 🎯 Quick Questions")
    
    col1, col2, col3 = st.columns(3)
    
    quick_questions = [
        "What should I post today?",
        "How can I improve my social media engagement?",
        "What are the best times to post on social media?"
    ]
    
    for i, (col, question) in enumerate(zip([col1, col2, col3], quick_questions)):
        with col:
            if st.button(question, key=f"quick_q_{i}", use_container_width=True):
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': question,
                    'timestamp': datetime.now().isoformat()
                })
                st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History", type="secondary"):
        st.session_state.chat_history = []
        st.rerun()

def render_modern_content_creation(profile, agent, helpers):
    """Modern content creation interface"""
    
    # Page header
    render_modern_hero(
        title="✍️ AI-Powered Content Creation",
        subtitle="Create trend-aware, culturally-relevant content using real-time data analysis and advanced AI",
        gradient_colors=["#fa709a", "#fee140"]
    )
    
    # Trend status
    if not st.session_state.current_trends:
        render_modern_alert(
            "💡 Tip: Analyze current trends first for better content recommendations!",
            "info"
        )
        
        if st.button("📈 Analyze Trends Now", type="primary", use_container_width=True):
            with st.spinner("Analyzing trends with Apify..."):
                if agent:
                    trends = run_async(agent.analyze_trends_with_apify(profile))
                    st.session_state.current_trends = trends
                    render_modern_alert("✅ Trends analyzed successfully!", "success")
                    st.rerun()
    else:
        render_modern_alert("✅ Using current trend data for content creation", "success")
    
    # Content creation form
    form_config = {
        "title": "🚀 Generate AI Content",
        "description": "Configure your content preferences and let AI create engaging posts for you",
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
            }
        ],
        "submit_text": "🚀 Generate AI Content"
    }
    
    form_data, create_content = render_modern_form(form_config, "content_creation_form")
    
    if create_content:
        platform = form_data.get("platform")
        content_type = form_data.get("content_type")
        topic = form_data.get("topic")
        language = form_data.get("language")
        
        if not platform or not content_type or not language:
            render_modern_alert("Please fill in all required fields", "error")
        else:
            with st.spinner("🤖 Creating trend-aware content with DSPy..."):
                try:
                    if agent:
                        # Use DSPy agent for advanced content generation
                        content_result = run_async(agent.generate_content_with_trends(
                            profile, platform, content_type, language, topic
                        ))
                        
                        # Process and format content
                        if helpers:
                            hashtags = content_result.get('hashtags', [])
                            hashtags = helpers['formatter'].add_cultural_hashtags(
                                hashtags, profile.get('cultural_background', 'cameroon'), language
                            )
                            hashtags = helpers['optimizer'].optimize_hashtags_for_platform(hashtags, platform)
                            
                            content_piece = helpers['formatter'].format_content_piece({
                                "platform": platform,
                                "content_type": content_type,
                                "language": language,
                                "text": content_result['content_text'],
                                "hashtags": hashtags,
                                "call_to_action": content_result.get('call_to_action', ''),
                                "topic": topic or "AI Generated",
                                "trend_based": True
                            })
                            
                            content_piece.update({
                                "strategy": content_result.get('strategy', ''),
                                "engagement_tactics": content_result.get('engagement_tactics', ''),
                                "trending_topics": content_result.get('trending_topics', ''),
                                "cultural_insights": content_result.get('cultural_insights', '')
                            })
                        else:
                            content_piece = {
                                "id": f"content_{len(st.session_state.content_pieces) + 1}",
                                "platform": platform,
                                "content_type": content_type,
                                "language": language,
                                "text": content_result['content_text'],
                                "hashtags": content_result.get('hashtags', []),
                                "call_to_action": content_result.get('call_to_action', ''),
                                "topic": topic or "AI Generated",
                                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "trend_based": True
                            }
                        
                        st.session_state.content_pieces.append(content_piece)
                        render_modern_alert("✅ AI-powered content created successfully!", "success")
                        
                        # Display the created content
                        st.markdown("### 📝 Generated Content")
                        
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.text_area(
                                "Content",
                                value=content_piece['text'],
                                height=200,
                                key="generated_content_display"
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
                            st.write(f"Trend-based: {'Yes' if content_piece.get('trend_based') else 'No'}")
                            
                            if st.button("📋 Copy to Clipboard", key="copy_generated"):
                                st.code(content_piece['text'])
                        
                        # Show insights
                        if content_result.get('strategy') or content_result.get('engagement_tactics'):
                            st.markdown("### 📊 Content Insights")
                            
                            insight_col1, insight_col2 = st.columns(2)
                            
                            with insight_col1:
                                if content_result.get('strategy'):
                                    st.markdown("**Strategy Used:**")
                                    st.write(content_result['strategy'])
                            
                            with insight_col2:
                                if content_result.get('engagement_tactics'):
                                    st.markdown("**Engagement Tactics:**")
                                    st.write(content_result['engagement_tactics'])
                
                except Exception as e:
                    render_modern_alert(f"Content generation failed: {str(e)}", "error")

def render_modern_trend_analysis(profile, agent, helpers):
    """Modern trend analysis interface"""
    
    # Page header
    render_modern_hero(
        title="📈 Real-Time Trend Analysis",
        subtitle="Powered by Apify for accurate, up-to-date social media insights across multiple platforms",
        gradient_colors=["#667eea", "#764ba2"]
    )
    
    # Refresh trends button
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("🔄 Refresh Trend Analysis", type="primary", use_container_width=True):
            with st.spinner("Analyzing trends across platforms..."):
                if agent:
                    trends = run_async(agent.analyze_trends_with_apify(profile))
                    st.session_state.current_trends = trends
                    render_modern_alert("✅ Trends updated successfully!", "success")
                    st.rerun()
    
    with col2:
        if st.session_state.current_trends:
            last_update = st.session_state.current_trends.get('analysis_timestamp', 'Unknown')
            st.info(f"Last updated: {last_update[:16] if last_update != 'Unknown' else 'Unknown'}")
    
    # Display trends
    if st.session_state.current_trends:
        trends = st.session_state.current_trends
        
        # Trending topics
        st.markdown("### 🔥 Trending Topics")
        
        trending_topics = trends.get('trending_topics', [])
        
        if trending_topics:
            # Filter relevant trends
            if helpers:
                relevant_trends = helpers['trend_processor'].filter_relevant_trends(
                    trending_topics, profile, min_relevance=1.0
                )[:6]  # Show top 6
            else:
                relevant_trends = trending_topics[:6]
            
            # Display in grid
            cols_per_row = 3
            rows = [relevant_trends[i:i + cols_per_row] for i in range(0, len(relevant_trends), cols_per_row)]
            
            for row in rows:
                cols = st.columns(len(row))
                
                for i, topic in enumerate(row):
                    with cols[i]:
                        render_modern_card(
                            title=topic.get('topic', 'Unknown Topic'),
                            content=f"Platform: {topic.get('platform', 'general').title()}\nEngagement: {topic.get('engagement_score', 0):.1f}%\nRelevance: {topic.get('relevance_score', 0):.1f}/10",
                            icon="🔥",
                            accent_color="#43e97b",
                            action_text="Create Content"
                        )
                        
                        if st.button(f"Create Content", key=f"trend_create_{i}_{topic.get('topic', 'unknown')}"):
                            st.session_state.suggested_topic = topic.get('topic', '')
                            render_modern_alert(f"💡 Topic '{topic.get('topic', '')}' saved! Go to Create Content to use it.", "info")
        
        # Content opportunities
        opportunities = trends.get('content_opportunities', [])
        if opportunities:
            st.markdown("### 💡 Content Opportunities")
            
            for i, opp in enumerate(opportunities[:3]):
                render_modern_card(
                    title=opp.get('topic', 'Content Idea'),
                    content=f"Engagement Potential: {opp.get('engagement_potential', 0):.1f}%\nApproach: {opp.get('suggested_approach', 'Create engaging content')}",
                    icon="💡",
                    accent_color="#f093fb"
                )
        
        # Data sources stats
        data_sources = trends.get('data_sources', {})
        if data_sources:
            st.markdown("### 📊 Data Sources")
            
            source_stats = [
                {
                    "value": data_sources.get('instagram_posts_count', 0),
                    "label": "Instagram Posts",
                    "color": "#E4405F"
                },
                {
                    "value": data_sources.get('tiktok_videos_count', 0),
                    "label": "TikTok Videos",
                    "color": "#000000"
                },
                {
                    "value": data_sources.get('youtube_videos_count', 0),
                    "label": "YouTube Videos",
                    "color": "#FF0000"
                },
                {
                    "value": data_sources.get('google_trends_count', 0),
                    "label": "Google Trends",
                    "color": "#4285F4"
                }
            ]
            
            render_modern_stats(source_stats, "Real-Time Data Collection")
    
    else:
        render_modern_alert("No trend data available. Click 'Refresh Trend Analysis' to get started!", "info")
        
        # What you'll get section
        benefits = [
            {
                "title": "Real-time Trending Topics",
                "description": "Get the latest trending topics from Instagram, TikTok, and YouTube",
                "icon": "🔥",
                "color": "#667eea"
            },
            {
                "title": "Engagement Predictions",
                "description": "AI-powered predictions for your content's engagement potential",
                "icon": "📊",
                "color": "#764ba2"
            },
            {
                "title": "Cultural Relevance",
                "description": "Content scoring adapted for your cultural background and audience",
                "icon": "🌍",
                "color": "#f093fb"
            }
        ]
        
        render_modern_feature_grid(benefits, "What You'll Get from Trend Analysis")

def render_modern_social_connections(profile, agent, helpers):
    """Modern social media connections interface"""
    
    # Page header
    render_modern_hero(
        title="🔗 Connect to Real Social Media Data",
        subtitle="Connect your Content Marketing Agent to real social media platforms for authentic trend analysis",
        gradient_colors=["#4facfe", "#00f2fe"]
    )
    
    # Connection status
    if 'social_connections' not in st.session_state:
        st.session_state.social_connections = {
            'twitter_enabled': False,
            'tiktok_enabled': False,
            'youtube_enabled': False,
            'last_data_source': 'enhanced_fallback'
        }
    
    # Status cards
    st.markdown("### 📊 Connection Status")
    
    connections = [
        {
            "platform": "Twitter",
            "status": st.session_state.social_connections['twitter_enabled'],
            "icon": "🐦",
            "color": "#1DA1F2"
        },
        {
            "platform": "TikTok", 
            "status": st.session_state.social_connections['tiktok_enabled'],
            "icon": "🎵",
            "color": "#000000"
        },
        {
            "platform": "YouTube",
            "status": st.session_state.social_connections['youtube_enabled'],
            "icon": "🎥",
            "color": "#FF0000"
        }
    ]
    
    cols = st.columns(3)
    
    for i, conn in enumerate(connections):
        with cols[i]:
            status_text = "🟢 Connected" if conn['status'] else "🔴 Disconnected"
            render_modern_card(
                title=f"{conn['icon']} {conn['platform']}",
                content=f"Status: {status_text}\nReal-time data collection for trend analysis",
                icon=conn['icon'],
                accent_color=conn['color']
            )
    
    # Current data source
    current_source = st.session_state.social_connections.get('last_data_source', 'enhanced_fallback')
    
    if current_source.startswith('real_'):
        render_modern_alert("✅ Currently using REAL social media data for trend analysis", "success")
    else:
        render_modern_alert("⚠️ Currently using enhanced sample data - connect to social media for real trends", "warning")
    
    # Connection features
    platform_features = [
        {
            "title": "Twitter Integration",
            "description": "Real tweets, hashtags, engagement metrics, and sentiment analysis",
            "icon": "🐦",
            "color": "#1DA1F2",
            "features": [
                "Real tweets with engagement metrics",
                "Trending hashtags with usage counts", 
                "Authentic user interactions",
                "Live sentiment analysis"
            ]
        },
        {
            "title": "TikTok Integration",
            "description": "Viral videos, trending sounds, hashtag performance, and creator insights",
            "icon": "🎵",
            "color": "#000000",
            "features": [
                "Viral videos with view counts",
                "Trending hashtags and challenges",
                "Popular sounds and music trends",
                "Creator engagement patterns"
            ]
        },
        {
            "title": "YouTube Integration", 
            "description": "Trending videos, channel strategies, engagement data, and topic analysis",
            "icon": "🎥",
            "color": "#FF0000",
            "features": [
                "Trending videos with metrics",
                "Popular channel strategies",
                "Video engagement analysis",
                "Content topic performance"
            ]
        }
    ]
    
    render_modern_feature_grid(platform_features, "Platform Integration Features")

def render_modern_react_agent(profile, agent, helpers):
    """Modern React Agent interface"""
    
    # Page header
    render_modern_hero(
        title="🤖 Self-Automated React Agent",
        subtitle="Advanced AI agent with autonomous decision-making, state management, and dynamic tool creation",
        gradient_colors=["#667eea", "#764ba2"]
    )
    
    if not agent:
        render_modern_alert("React Agent not available. Please check your configuration.", "error")
        return
    
    # Agent status
    bot_state = agent.get_bot_state_summary()
    
    st.markdown("### 🧠 Agent State")
    
    state_stats = [
        {
            "value": bot_state['agent_state']['current_state'].title(),
            "label": "Current State",
            "color": "#667eea"
        },
        {
            "value": bot_state['agent_state']['iteration_count'],
            "label": "Iterations",
            "color": "#764ba2"
        },
        {
            "value": len(bot_state['created_agents']),
            "label": "Created Agents",
            "color": "#f093fb"
        },
        {
            "value": f"{bot_state['agent_state']['task_complexity']:.1f}",
            "label": "Task Complexity",
            "color": "#4facfe"
        }
    ]
    
    render_modern_stats(state_stats, "React Agent Status")
    
    # Agent capabilities
    capabilities = [
        {
            "title": "Dynamic Agent Creation",
            "description": "Create React, Chain-of-Thought, or Predict agents on demand with custom signatures",
            "icon": "🔧",
            "color": "#667eea"
        },
        {
            "title": "Autonomous State Management",
            "description": "Think → Act → Rethink → Plan → Execute → Create → Sleep cycle with intelligent transitions",
            "icon": "🧠",
            "color": "#764ba2"
        },
        {
            "title": "Signature Management",
            "description": "Manage and utilize multiple DSPy signatures for different AI operations",
            "icon": "📝",
            "color": "#f093fb"
        },
        {
            "title": "Self-Learning Engine",
            "description": "Learn from execution history and adapt decision-making based on context",
            "icon": "🎯",
            "color": "#4facfe"
        }
    ]
    
    render_modern_feature_grid(capabilities, "React Agent Capabilities")
    
    # Test React Agent
    st.markdown("### 🚀 Test React Agent")
    
    test_form_config = {
        "title": "Test Self-Automated React Agent",
        "description": "Enter a task for the React Agent to execute autonomously",
        "fields": [
            {
                "name": "task",
                "label": "Task Description",
                "type": "textarea",
                "placeholder": "e.g., Generate educational content about personal development for Instagram",
                "help": "Describe what you want the React Agent to accomplish"
            },
            {
                "name": "max_iterations",
                "label": "Max Iterations",
                "type": "number",
                "min_value": 1,
                "max_value": 20,
                "default_value": 5,
                "help": "Maximum number of state transitions allowed"
            }
        ],
        "submit_text": "🚀 Execute React Agent"
    }
    
    form_data, execute_agent = render_modern_form(test_form_config, "react_agent_form")
    
    if execute_agent:
        task = form_data.get("task")
        max_iterations = form_data.get("max_iterations", 5)
        
        if not task:
            render_modern_alert("Please enter a task description", "error")
        else:
            with st.spinner("🤖 React Agent executing task..."):
                try:
                    # Prepare context
                    context = {
                        "user_profile": profile,
                        "platform": profile['active_platforms'][0] if profile['active_platforms'] else "instagram",
                        "content_type": "educational",
                        "language": profile.get('primary_language', 'en')
                    }
                    
                    # Execute React Agent
                    result = run_async(agent.react_engine(task, context, max_iterations))
                    
                    render_modern_alert("✅ React Agent execution completed!", "success")
                    
                    # Display results
                    st.markdown("### 📊 Execution Results")
                    
                    result_col1, result_col2 = st.columns(2)
                    
                    with result_col1:
                        st.markdown("**Execution Summary:**")
                        st.write(f"Final State: {result.get('final_state', 'unknown')}")
                        st.write(f"Total Iterations: {result.get('total_iterations', 0)}")
                        st.write(f"Status: {result.get('status', 'incomplete')}")
                        
                        if result.get('error'):
                            st.error(f"Error: {result['error']}")
                    
                    with result_col2:
                        st.markdown("**State Transitions:**")
                        transitions = result.get('state_transitions', [])
                        
                        if transitions:
                            for i, transition in enumerate(transitions, 1):
                                st.write(f"{i}. {transition['from']} → {transition['to']}")
                        else:
                            st.write("No state transitions recorded")
                    
                    # Show detailed results
                    if st.button("📋 Show Detailed Results"):
                        st.json(result)
                
                except Exception as e:
                    render_modern_alert(f"React Agent execution failed: {str(e)}", "error")
    
    # Available signatures and tools
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 Available Signatures")
        for signature in bot_state['available_signatures']:
            st.write(f"• {signature}")
    
    with col2:
        st.markdown("### 🛠️ Available Tools")
        for tool in bot_state['available_tools']:
            st.write(f"• {tool}")

if __name__ == "__main__":
    main()