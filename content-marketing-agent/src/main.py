import streamlit as st
import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Import our modules
from .agents.content_marketing_agent import ContentMarketingAgent
from .models.user_profile import UserProfile, ContentPiece, Platform, Language, ContentType
from .ui.intake_form import IntakeForm
from .api.trend_analyzer import TrendAnalysisOrchestrator
from .utils.multilingual_support import MultilingualContentManager


class ContentMarketingApp:
    """Main Streamlit application for the Content Marketing Agent"""
    
    def __init__(self):
        self.agent = ContentMarketingAgent()
        self.trend_orchestrator = TrendAnalysisOrchestrator()
        self.multilingual_manager = MultilingualContentManager()
        
        # Initialize session state
        if 'user_profile' not in st.session_state:
            st.session_state.user_profile = None
        if 'content_pieces' not in st.session_state:
            st.session_state.content_pieces = []
        if 'trend_data' not in st.session_state:
            st.session_state.trend_data = None
    
    def run(self):
        """Main application runner"""
        
        st.set_page_config(
            page_title="Content Marketing Agent",
            page_icon="🎯",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS
        st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
        }
        .success-message {
            background-color: #d4edda;
            color: #155724;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Main header
        st.markdown('<h1 class="main-header">🎯 Content Marketing Agent</h1>', unsafe_allow_html=True)
        st.markdown("*Your AI-powered content creation assistant for culturally-aware, trend-driven social media marketing*")
        
        # Sidebar navigation
        self.render_sidebar()
        
        # Main content area
        if st.session_state.user_profile is None:
            self.render_onboarding()
        else:
            self.render_main_dashboard()
    
    def render_sidebar(self):
        """Render the sidebar navigation"""
        
        st.sidebar.title("🎯 Navigation")
        
        if st.session_state.user_profile is None:
            st.sidebar.info("👋 Welcome! Please complete the setup to get started.")
            return
        
        # User profile summary
        profile = st.session_state.user_profile
        st.sidebar.markdown("### 👤 Profile")
        st.sidebar.write(f"**{profile.name}**")
        st.sidebar.write(f"Brand: {profile.brand_name}")
        st.sidebar.write(f"Languages: {profile.primary_language.value.upper()}" + 
                        (f", {profile.secondary_language.value.upper()}" if profile.secondary_language else ""))
        
        # Navigation options
        st.sidebar.markdown("### 📱 Quick Actions")
        
        if st.sidebar.button("🔄 Analyze Trends", use_container_width=True):
            st.session_state.page = "trends"
            st.rerun()
        
        if st.sidebar.button("✍️ Create Content", use_container_width=True):
            st.session_state.page = "create"
            st.rerun()
        
        if st.sidebar.button("📊 View Analytics", use_container_width=True):
            st.session_state.page = "analytics"
            st.rerun()
        
        if st.sidebar.button("🧲 Manage Leads", use_container_width=True):
            st.session_state.page = "leads"
            st.rerun()
        
        # Settings
        st.sidebar.markdown("### ⚙️ Settings")
        if st.sidebar.button("Edit Profile", use_container_width=True):
            st.session_state.user_profile = None
            st.rerun()
    
    def render_onboarding(self):
        """Render the onboarding/setup process"""
        
        st.markdown("## 🚀 Let's Set Up Your Content Marketing Assistant")
        st.markdown("Complete the form below to personalize your AI assistant for your unique needs and cultural context.")
        
        # Render intake form
        intake_form = IntakeForm()
        user_profile = intake_form.render_intake_form()
        
        if user_profile:
            st.session_state.user_profile = user_profile
            st.success("🎉 Profile created successfully! Your content marketing assistant is ready to help.")
            st.rerun()
    
    def render_main_dashboard(self):
        """Render the main dashboard"""
        
        # Get current page from session state
        current_page = getattr(st.session_state, 'page', 'dashboard')
        
        if current_page == 'trends':
            self.render_trends_page()
        elif current_page == 'create':
            self.render_content_creation_page()
        elif current_page == 'analytics':
            self.render_analytics_page()
        elif current_page == 'leads':
            self.render_lead_management_page()
        else:
            self.render_dashboard_overview()
    
    def render_dashboard_overview(self):
        """Render the main dashboard overview"""
        
        profile = st.session_state.user_profile
        
        st.markdown("## 📊 Dashboard Overview")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Active Platforms", len(profile.active_platforms))
        
        with col2:
            st.metric("Content Pieces", len(st.session_state.content_pieces))
        
        with col3:
            st.metric("Lead Magnets", len(profile.lead_magnets))
        
        with col4:
            st.metric("Weekly Time", f"{profile.available_time}h")
        
        # Quick actions
        st.markdown("## 🚀 Quick Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📈 Daily Content Workflow", use_container_width=True, type="primary"):
                self.run_daily_workflow()
        
        with col2:
            if st.button("🔍 Analyze Current Trends", use_container_width=True):
                st.session_state.page = "trends"
                st.rerun()
        
        with col3:
            if st.button("✍️ Create Single Content", use_container_width=True):
                st.session_state.page = "create"
                st.rerun()
        
        # Recent content
        if st.session_state.content_pieces:
            st.markdown("## 📝 Recent Content")
            
            for content in st.session_state.content_pieces[-3:]:  # Show last 3
                with st.expander(f"{content.title} - {content.platform.value.title()}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write("**Content:**")
                        st.write(content.text_content[:200] + "..." if len(content.text_content) > 200 else content.text_content)
                        
                        if content.hashtags:
                            st.write("**Hashtags:**", " ".join(content.hashtags))
                    
                    with col2:
                        st.write("**Platform:**", content.platform.value.title())
                        st.write("**Language:**", content.language.value.upper())
                        st.write("**Status:**", content.status.title())
                        if content.cultural_score:
                            st.write("**Cultural Score:**", f"{content.cultural_score:.1f}/10")
    
    def render_trends_page(self):
        """Render the trends analysis page"""
        
        st.markdown("## 📈 Trend Analysis")
        
        profile = st.session_state.user_profile
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Current Trends Analysis")
            
            if st.button("🔄 Refresh Trends", type="primary"):
                with st.spinner("Analyzing current trends..."):
                    trend_data = asyncio.run(self.analyze_trends())
                    st.session_state.trend_data = trend_data
                    st.success("Trends updated!")
                    st.rerun()
        
        with col2:
            st.markdown("### Settings")
            
            # Trend analysis settings
            include_twitter = st.checkbox("Include Twitter Trends", value=True)
            include_youtube = st.checkbox("Include YouTube Trends", value=True)
            include_google = st.checkbox("Include Google Trends", value=True)
        
        # Display trend data
        if st.session_state.trend_data:
            self.display_trend_data(st.session_state.trend_data)
        else:
            st.info("Click 'Refresh Trends' to analyze current trending topics relevant to your audience.")
    
    def render_content_creation_page(self):
        """Render the content creation page"""
        
        st.markdown("## ✍️ Content Creation Studio")
        
        profile = st.session_state.user_profile
        
        # Content creation form
        with st.form("content_creation_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                content_type = st.selectbox(
                    "Content Type",
                    options=[ct.value for ct in ContentType],
                    format_func=lambda x: x.replace("_", " ").title()
                )
                
                platform = st.selectbox(
                    "Target Platform",
                    options=[p.value for p in profile.active_platforms],
                    format_func=lambda x: x.title()
                )
                
                language = st.selectbox(
                    "Language",
                    options=[profile.primary_language.value] + 
                           ([profile.secondary_language.value] if profile.secondary_language else []) +
                           ["bilingual"],
                    format_func=lambda x: {"en": "English", "fr": "French", "bilingual": "Bilingual"}[x]
                )
            
            with col2:
                topic = st.text_input("Specific Topic (Optional)", placeholder="Leave blank to use trending topics")
                
                use_trends = st.checkbox("Incorporate Current Trends", value=True)
                
                cultural_adaptation = st.checkbox("Apply Cultural Adaptation", value=True)
            
            submitted = st.form_submit_button("🚀 Create Content", type="primary")
            
            if submitted:
                self.create_single_content(
                    content_type, platform, language, topic, use_trends, cultural_adaptation
                )
        
        # Display created content
        if st.session_state.content_pieces:
            st.markdown("### 📝 Created Content")
            
            for i, content in enumerate(reversed(st.session_state.content_pieces)):
                with st.expander(f"{content.title} - {content.created_at.strftime('%Y-%m-%d %H:%M')}"):
                    self.display_content_piece(content, i)
    
    def render_analytics_page(self):
        """Render the analytics and performance page"""
        
        st.markdown("## 📊 Analytics & Performance")
        
        # Placeholder for analytics
        st.info("📈 Analytics dashboard coming soon! This will show:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Content Performance:**
            - Engagement rates by platform
            - Best performing content types
            - Optimal posting times
            - Hashtag performance
            """)
        
        with col2:
            st.markdown("""
            **Audience Insights:**
            - Audience growth trends
            - Demographic breakdowns
            - Cultural engagement patterns
            - Language preference analysis
            """)
        
        # Mock analytics data
        if st.session_state.content_pieces:
            st.markdown("### 📈 Content Performance Summary")
            
            # Create mock performance data
            import random
            
            performance_data = []
            for content in st.session_state.content_pieces:
                performance_data.append({
                    "Title": content.title[:30] + "...",
                    "Platform": content.platform.value.title(),
                    "Language": content.language.value.upper(),
                    "Cultural Score": content.cultural_score or random.uniform(6, 9),
                    "Est. Engagement": f"{random.uniform(2, 8):.1f}%"
                })
            
            st.dataframe(performance_data, use_container_width=True)
    
    def render_lead_management_page(self):
        """Render the lead management page"""
        
        st.markdown("## 🧲 Lead Management")
        
        profile = st.session_state.user_profile
        
        # Lead magnets overview
        st.markdown("### 📋 Your Lead Magnets")
        
        if profile.lead_magnets:
            for lm in profile.lead_magnets:
                with st.expander(f"🧲 {lm.title}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write("**Description:**", lm.description)
                        st.write("**Target Audience:**", lm.target_audience)
                        st.write("**Keywords:**", ", ".join(lm.keywords))
                    
                    with col2:
                        if lm.file_url:
                            st.write("**Download URL:**", lm.file_url)
                        if lm.landing_page_url:
                            st.write("**Landing Page:**", lm.landing_page_url)
        else:
            st.info("No lead magnets configured. Edit your profile to add lead magnets.")
        
        # Comment monitoring simulation
        st.markdown("### 💬 Comment Monitoring")
        
        st.info("🤖 AI Comment Monitoring coming soon! This will:")
        st.markdown("""
        - Monitor comments across all platforms
        - Automatically identify potential leads
        - Match comments to relevant lead magnets
        - Generate personalized responses
        - Track lead qualification progress
        """)
        
        # Manual lead magnet testing
        st.markdown("### 🧪 Test Lead Magnet Matching")
        
        with st.form("test_lead_matching"):
            test_comment = st.text_area(
                "Test Comment",
                placeholder="Enter a sample comment to see which lead magnet would be recommended..."
            )
            
            if st.form_submit_button("🔍 Test Matching"):
                if test_comment and profile.lead_magnets:
                    result = self.agent.manage_lead_magnet_response(
                        profile, test_comment, "Interested user"
                    )
                    
                    st.success("🎯 Lead Magnet Match Found!")
                    st.write("**Recommended Response:**")
                    st.write(result["personalized_message"])
                    st.write("**Qualification Questions:**")
                    st.write(result["qualification_questions"])
    
    async def analyze_trends(self) -> Dict:
        """Analyze current trends for the user"""
        
        profile = st.session_state.user_profile
        
        return await self.trend_orchestrator.comprehensive_trend_analysis(
            user_interests=profile.audience_demographics.interests,
            expertise_areas=profile.expertise_areas,
            cultural_context=profile.cultural_background,
            audience_locations=profile.audience_demographics.location
        )
    
    def display_trend_data(self, trend_data: Dict):
        """Display trend analysis results"""
        
        st.markdown("### 🔥 Trending Topics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Top Relevant Trends:**")
            for i, trend in enumerate(trend_data["trending_topics"][:5], 1):
                st.write(f"{i}. **{trend['topic']}** ({trend['platform'].title()})")
                st.write(f"   Relevance: {trend['relevance_score']:.1f}/10")
                if trend['hashtags']:
                    st.write(f"   Hashtags: {', '.join(trend['hashtags'][:3])}")
                st.write("")
        
        with col2:
            st.markdown("**Content Opportunities:**")
            for i, opp in enumerate(trend_data["content_opportunities"][:5], 1):
                st.write(f"{i}. **{opp['topic']}**")
                st.write(f"   Type: {opp['type'].replace('_', ' ').title()}")
                st.write(f"   Engagement Potential: {opp['engagement_potential']:.1f}%")
                st.write(f"   Platforms: {', '.join(opp['platforms'][:2])}")
                st.write("")
        
        # Optimal timing
        if "optimal_timing" in trend_data:
            st.markdown("### ⏰ Optimal Posting Times")
            
            timing_data = trend_data["optimal_timing"]
            for platform, times in timing_data.items():
                st.write(f"**{platform.title()}:**")
                for time in times[:2]:  # Show top 2 times
                    st.write(f"  • {time}")
    
    def run_daily_workflow(self):
        """Run the complete daily content workflow"""
        
        profile = st.session_state.user_profile
        
        with st.spinner("🚀 Running daily content workflow..."):
            try:
                # Generate content for all active platforms
                content_pieces = self.agent.daily_content_workflow(profile)
                
                # Apply multilingual and cultural adaptations
                for content in content_pieces:
                    if content.language == Language.BILINGUAL:
                        bilingual_content = self.multilingual_manager.create_bilingual_content(
                            content.text_content, profile.primary_language.value
                        )
                        content.text_content = bilingual_content["bilingual"]
                    
                    # Apply cultural adaptation
                    content.text_content = self.multilingual_manager.adapt_for_culture(
                        content.text_content, profile.cultural_background, content.language.value
                    )
                
                # Add to session state
                st.session_state.content_pieces.extend(content_pieces)
                
                st.success(f"✅ Created {len(content_pieces)} content pieces for your active platforms!")
                
                # Show summary
                st.markdown("### 📝 Generated Content Summary")
                for content in content_pieces:
                    st.write(f"• **{content.platform.value.title()}** ({content.language.value.upper()}): {content.title}")
                
            except Exception as e:
                st.error(f"❌ Error running workflow: {str(e)}")
    
    def create_single_content(
        self, 
        content_type: str, 
        platform: str, 
        language: str, 
        topic: str,
        use_trends: bool,
        cultural_adaptation: bool
    ):
        """Create a single piece of content"""
        
        profile = st.session_state.user_profile
        
        with st.spinner("✍️ Creating content..."):
            try:
                # Get trend data if needed
                if use_trends and not st.session_state.trend_data:
                    trend_data = asyncio.run(self.analyze_trends())
                    st.session_state.trend_data = trend_data
                else:
                    trend_data = st.session_state.trend_data or {}
                
                # Generate strategy
                strategy = self.agent.generate_content_strategy(
                    profile, trend_data, ContentType(content_type)
                )
                
                # Create content
                content_piece = self.agent.create_content(
                    profile, strategy, Platform(platform), Language(language), topic
                )
                
                # Apply cultural adaptation if requested
                if cultural_adaptation:
                    content_piece.text_content = self.multilingual_manager.adapt_for_culture(
                        content_piece.text_content, profile.cultural_background, language
                    )
                
                # Handle bilingual content
                if language == "bilingual":
                    bilingual_content = self.multilingual_manager.create_bilingual_content(
                        content_piece.text_content, profile.primary_language.value
                    )
                    content_piece.text_content = bilingual_content["bilingual"]
                    content_piece.language = Language.BILINGUAL
                
                # Add to session state
                st.session_state.content_pieces.append(content_piece)
                
                st.success("✅ Content created successfully!")
                
            except Exception as e:
                st.error(f"❌ Error creating content: {str(e)}")
    
    def display_content_piece(self, content: ContentPiece, index: int):
        """Display a content piece with editing options"""
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Editable content
            edited_text = st.text_area(
                "Content Text",
                value=content.text_content,
                height=150,
                key=f"content_text_{index}"
            )
            
            edited_cta = st.text_input(
                "Call to Action",
                value=content.call_to_action,
                key=f"content_cta_{index}"
            )
            
            if edited_text != content.text_content or edited_cta != content.call_to_action:
                if st.button(f"💾 Save Changes", key=f"save_{index}"):
                    content.text_content = edited_text
                    content.call_to_action = edited_cta
                    st.success("Changes saved!")
        
        with col2:
            st.write("**Platform:**", content.platform.value.title())
            st.write("**Language:**", content.language.value.upper())
            st.write("**Type:**", content.content_type.value.replace("_", " ").title())
            
            if content.cultural_score:
                st.write("**Cultural Score:**", f"{content.cultural_score:.1f}/10")
            
            if content.hashtags:
                st.write("**Hashtags:**")
                st.write(" ".join(content.hashtags))
            
            # Action buttons
            if st.button(f"📋 Copy Text", key=f"copy_{index}"):
                st.code(content.text_content)
            
            if st.button(f"🗑️ Delete", key=f"delete_{index}"):
                st.session_state.content_pieces.remove(content)
                st.rerun()


def main():
    """Main application entry point"""
    app = ContentMarketingApp()
    app.run()


if __name__ == "__main__":
    main()