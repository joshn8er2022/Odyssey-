import streamlit as st
from typing import Dict, List
import json
from datetime import datetime

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user_profile import (
    UserProfile,
    AudienceDemographics,
    BusinessGoals,
    ContentPreferences,
    LeadMagnet,
    SalesProcess,
    Platform,
    Language,
    ContentType
)


class IntakeForm:
    """Streamlit-based user intake form for content marketing agent"""
    
    def __init__(self):
        self.user_profile = None
    
    def render_intake_form(self) -> UserProfile:
        """Render the complete intake form and return UserProfile"""
        
        st.title("🎯 Content Marketing Agent Setup")
        st.markdown("Let's set up your personalized content marketing assistant!")
        
        # Create tabs for different sections
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "👤 Personal & Brand",
            "🎯 Audience",
            "💼 Business Goals",
            "📱 Content Preferences",
            "🧲 Lead Generation"
        ])
        
        with tab1:
            personal_data = self._render_personal_brand_section()
        
        with tab2:
            audience_data = self._render_audience_section()
        
        with tab3:
            business_data = self._render_business_section()
        
        with tab4:
            content_data = self._render_content_section()
        
        with tab5:
            lead_data = self._render_lead_generation_section()
        
        # Submit button
        if st.button("🚀 Create My Content Marketing Profile", type="primary"):
            try:
                user_profile = self._create_user_profile(
                    personal_data, audience_data, business_data, 
                    content_data, lead_data
                )
                st.success("✅ Profile created successfully!")
                st.balloons()
                return user_profile
            except Exception as e:
                st.error(f"❌ Error creating profile: {str(e)}")
                return None
        
        return None
    
    def _render_personal_brand_section(self) -> Dict:
        """Render personal and brand information section"""
        
        st.header("Personal & Brand Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *", placeholder="Enter your full name")
            age = st.number_input("Age *", min_value=18, max_value=100, value=60)
            brand_name = st.text_input("Brand Name *", placeholder="Your personal or business brand")
        
        with col2:
            primary_language = st.selectbox(
                "Primary Language *",
                options=[lang.value for lang in Language],
                format_func=lambda x: {"en": "English", "fr": "French", "bilingual": "Bilingual"}[x]
            )
            secondary_language = st.selectbox(
                "Secondary Language",
                options=["None"] + [lang.value for lang in Language],
                format_func=lambda x: {"en": "English", "fr": "French", "bilingual": "Bilingual", "None": "None"}[x]
            )
            cultural_background = st.selectbox(
                "Cultural Background *",
                options=["cameroon", "other"],
                format_func=lambda x: {"cameroon": "Cameroon", "other": "Other"}[x]
            )
        
        brand_positioning = st.text_area(
            "Brand Positioning *",
            placeholder="How do you position yourself in the market? What makes you unique?",
            height=100
        )
        
        unique_value_proposition = st.text_area(
            "Unique Value Proposition *",
            placeholder="What unique value do you provide to your audience?",
            height=100
        )
        
        expertise_areas = st.multiselect(
            "Areas of Expertise *",
            options=[
                "Business Coaching", "Life Coaching", "Health & Wellness", "Finance",
                "Technology", "Marketing", "Education", "Spirituality", "Relationships",
                "Career Development", "Entrepreneurship", "Personal Development",
                "Cooking", "Travel", "Fashion", "Beauty", "Parenting", "Other"
            ]
        )
        
        if "Other" in expertise_areas:
            other_expertise = st.text_input("Please specify other expertise areas:")
            if other_expertise:
                expertise_areas = [area for area in expertise_areas if area != "Other"]
                expertise_areas.extend([area.strip() for area in other_expertise.split(",")])
        
        return {
            "name": name,
            "age": age,
            "brand_name": brand_name,
            "primary_language": Language(primary_language),
            "secondary_language": Language(secondary_language) if secondary_language != "None" else None,
            "cultural_background": cultural_background,
            "brand_positioning": brand_positioning,
            "unique_value_proposition": unique_value_proposition,
            "expertise_areas": expertise_areas
        }
    
    def _render_audience_section(self) -> Dict:
        """Render audience demographics section"""
        
        st.header("Target Audience")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age_range = st.selectbox(
                "Primary Age Range *",
                options=["18-24", "25-34", "35-44", "45-54", "55-64", "65+", "Mixed"]
            )
            gender_split = st.selectbox(
                "Gender Distribution *",
                options=["Mostly Female", "Mostly Male", "Balanced", "Non-binary inclusive"]
            )
        
        with col2:
            location = st.multiselect(
                "Primary Locations *",
                options=[
                    "Cameroon", "Nigeria", "Ghana", "Senegal", "Ivory Coast",
                    "France", "Canada", "United States", "United Kingdom",
                    "Germany", "Other African Countries", "Other European Countries",
                    "Other North American Countries", "Global"
                ]
            )
        
        interests = st.multiselect(
            "Audience Interests *",
            options=[
                "Personal Development", "Business Growth", "Health & Fitness",
                "Relationships", "Spirituality", "Finance & Money", "Career",
                "Parenting", "Education", "Technology", "Travel", "Food",
                "Fashion", "Beauty", "Entertainment", "Sports", "Politics",
                "Culture", "Art", "Music"
            ]
        )
        
        pain_points = st.multiselect(
            "Common Pain Points *",
            options=[
                "Lack of confidence", "Financial struggles", "Career stagnation",
                "Relationship issues", "Health problems", "Time management",
                "Work-life balance", "Lack of direction", "Fear of failure",
                "Communication problems", "Stress and anxiety", "Loneliness",
                "Cultural identity", "Language barriers", "Technology challenges"
            ]
        )
        
        preferred_content_types = st.multiselect(
            "Content Types They Engage With *",
            options=[ct.value for ct in ContentType],
            format_func=lambda x: {
                "educational": "Educational Content",
                "lead_magnet": "Lead Magnets",
                "cta_focused": "Call-to-Action Content",
                "entertainment": "Entertainment",
                "testimonial": "Testimonials"
            }[x]
        )
        
        return {
            "age_range": age_range,
            "gender_split": gender_split,
            "location": location,
            "interests": interests,
            "pain_points": pain_points,
            "preferred_content_types": [ContentType(ct) for ct in preferred_content_types]
        }
    
    def _render_business_section(self) -> Dict:
        """Render business goals section"""
        
        st.header("Business Goals & Offerings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            primary_objective = st.selectbox(
                "Primary Business Objective *",
                options=[
                    "Generate leads", "Increase brand awareness", "Drive sales",
                    "Build community", "Establish thought leadership",
                    "Launch new product/service", "Grow email list"
                ]
            )
            
            target_revenue = st.number_input(
                "Monthly Revenue Target (Optional)",
                min_value=0.0,
                value=0.0,
                step=100.0,
                format="%.2f"
            )
        
        with col2:
            lead_generation_target = st.number_input(
                "Monthly Lead Target (Optional)",
                min_value=0,
                value=0,
                step=10
            )
            
            brand_awareness_goals = st.text_area(
                "Brand Awareness Goals (Optional)",
                placeholder="What specific brand awareness goals do you have?",
                height=80
            )
        
        current_offerings = st.multiselect(
            "Current Products/Services *",
            options=[
                "1-on-1 Coaching", "Group Coaching", "Online Courses",
                "Digital Products", "Physical Products", "Consulting",
                "Speaking Services", "Workshops", "Membership Site",
                "Affiliate Marketing", "Sponsorships", "Other"
            ]
        )
        
        if "Other" in current_offerings:
            other_offerings = st.text_input("Please specify other offerings:")
            if other_offerings:
                current_offerings = [offer for offer in current_offerings if offer != "Other"]
                current_offerings.extend([offer.strip() for offer in other_offerings.split(",")])
        
        pricing_strategy = st.text_area(
            "Pricing Strategy (Optional)",
            placeholder="Describe your pricing approach and strategy",
            height=80
        )
        
        return {
            "primary_objective": primary_objective,
            "target_revenue": target_revenue if target_revenue > 0 else None,
            "lead_generation_target": lead_generation_target if lead_generation_target > 0 else None,
            "brand_awareness_goals": brand_awareness_goals if brand_awareness_goals else None,
            "current_offerings": current_offerings,
            "pricing_strategy": pricing_strategy if pricing_strategy else None
        }
    
    def _render_content_section(self) -> Dict:
        """Render content preferences section"""
        
        st.header("Content Preferences")
        
        # Content types and pillars
        preferred_content_types = st.multiselect(
            "Preferred Content Types to Create *",
            options=[ct.value for ct in ContentType],
            format_func=lambda x: {
                "educational": "Educational Content",
                "lead_magnet": "Lead Magnets",
                "cta_focused": "Call-to-Action Content",
                "entertainment": "Entertainment",
                "testimonial": "Testimonials"
            }[x]
        )
        
        content_pillars = st.multiselect(
            "Content Pillars/Themes *",
            options=[
                "Personal Stories", "Tips & Advice", "Behind the Scenes",
                "Client Success Stories", "Industry Insights", "Motivational Content",
                "Educational Tutorials", "Q&A Sessions", "Live Streams",
                "Product Demonstrations", "Cultural Content", "Trending Topics"
            ]
        )
        
        # Platform preferences
        st.subheader("Platform Preferences")
        
        active_platforms = st.multiselect(
            "Active Platforms *",
            options=[platform.value for platform in Platform],
            format_func=lambda x: {
                "tiktok": "TikTok",
                "instagram": "Instagram",
                "youtube": "YouTube",
                "linkedin": "LinkedIn",
                "facebook": "Facebook",
                "twitter": "Twitter"
            }[x]
        )
        
        # Posting frequency for each platform
        posting_frequency = {}
        platform_priorities = {}
        platform_language_preferences = {}
        
        if active_platforms:
            st.subheader("Platform-Specific Settings")
            
            for platform in active_platforms:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    freq = st.number_input(
                        f"Posts per week - {platform.title()}",
                        min_value=1,
                        max_value=21,
                        value=3,
                        key=f"freq_{platform}"
                    )
                    posting_frequency[Platform(platform)] = freq
                
                with col2:
                    priority = st.selectbox(
                        f"Priority - {platform.title()}",
                        options=[1, 2, 3, 4, 5],
                        index=2,
                        key=f"priority_{platform}"
                    )
                    platform_priorities[Platform(platform)] = priority
                
                with col3:
                    lang_pref = st.selectbox(
                        f"Language - {platform.title()}",
                        options=[lang.value for lang in Language],
                        format_func=lambda x: {"en": "English", "fr": "French", "bilingual": "Bilingual"}[x],
                        key=f"lang_{platform}"
                    )
                    platform_language_preferences[Platform(platform)] = Language(lang_pref)
        
        # Time and skills
        col1, col2 = st.columns(2)
        
        with col1:
            available_time = st.number_input(
                "Hours per week for content creation *",
                min_value=1,
                max_value=40,
                value=10
            )
        
        with col2:
            visual_style = st.selectbox(
                "Preferred Visual Style",
                options=[
                    "Professional", "Casual", "Colorful", "Minimalist",
                    "Bold & Vibrant", "Elegant", "Playful", "Cultural"
                ]
            )
        
        content_creation_skills = st.multiselect(
            "Current Content Creation Skills",
            options=[
                "Video editing", "Graphic design", "Photography", "Writing",
                "Social media management", "Live streaming", "Animation",
                "Audio editing", "SEO", "Analytics", "None"
            ]
        )
        
        return {
            "preferred_content_types": [ContentType(ct) for ct in preferred_content_types],
            "content_pillars": content_pillars,
            "active_platforms": [Platform(p) for p in active_platforms],
            "posting_frequency": posting_frequency,
            "platform_priorities": platform_priorities,
            "platform_language_preferences": platform_language_preferences,
            "available_time": available_time,
            "visual_style": visual_style,
            "content_creation_skills": content_creation_skills
        }
    
    def _render_lead_generation_section(self) -> Dict:
        """Render lead generation and sales process section"""
        
        st.header("Lead Generation & Sales Process")
        
        # Lead magnets
        st.subheader("Lead Magnets")
        
        lead_magnets = []
        num_lead_magnets = st.number_input(
            "How many lead magnets do you have?",
            min_value=0,
            max_value=10,
            value=1
        )
        
        for i in range(num_lead_magnets):
            with st.expander(f"Lead Magnet #{i+1}"):
                title = st.text_input(f"Title", key=f"lm_title_{i}")
                description = st.text_area(f"Description", key=f"lm_desc_{i}")
                target_audience = st.text_input(f"Target Audience", key=f"lm_audience_{i}")
                keywords = st.text_input(
                    f"Keywords (comma-separated)",
                    placeholder="free, guide, tips, checklist",
                    key=f"lm_keywords_{i}"
                )
                file_url = st.text_input(f"Download URL (optional)", key=f"lm_url_{i}")
                landing_page_url = st.text_input(f"Landing Page URL (optional)", key=f"lm_landing_{i}")
                
                if title and description:
                    lead_magnets.append(LeadMagnet(
                        id=f"lm_{i+1}",
                        title=title,
                        description=description,
                        target_audience=target_audience,
                        keywords=[k.strip() for k in keywords.split(",") if k.strip()],
                        file_url=file_url if file_url else None,
                        landing_page_url=landing_page_url if landing_page_url else None
                    ))
        
        # Sales process
        st.subheader("Sales Process")
        
        lead_qualification_questions = st.text_area(
            "Lead Qualification Questions *",
            placeholder="What questions do you ask to qualify leads? (one per line)",
            height=100
        ).split("\n")
        lead_qualification_questions = [q.strip() for q in lead_qualification_questions if q.strip()]
        
        follow_up_sequence = st.text_area(
            "Follow-up Message Sequence *",
            placeholder="What messages do you send in your follow-up sequence? (one per line)",
            height=100
        ).split("\n")
        follow_up_sequence = [msg.strip() for msg in follow_up_sequence if msg.strip()]
        
        sales_funnel_stages = st.multiselect(
            "Sales Funnel Stages *",
            options=[
                "Awareness", "Interest", "Consideration", "Intent",
                "Evaluation", "Purchase", "Retention", "Advocacy"
            ]
        )
        
        conversion_triggers = st.multiselect(
            "Conversion Triggers *",
            options=[
                "Downloaded lead magnet", "Engaged with multiple posts",
                "Asked specific question", "Mentioned pain point",
                "Requested consultation", "Shared personal story",
                "Showed buying intent", "Referred by someone"
            ]
        )
        
        return {
            "lead_magnets": lead_magnets,
            "lead_qualification_questions": lead_qualification_questions,
            "follow_up_sequence": follow_up_sequence,
            "sales_funnel_stages": sales_funnel_stages,
            "conversion_triggers": conversion_triggers
        }
    
    def _create_user_profile(
        self,
        personal_data: Dict,
        audience_data: Dict,
        business_data: Dict,
        content_data: Dict,
        lead_data: Dict
    ) -> UserProfile:
        """Create UserProfile object from form data"""
        
        # Validate required fields
        required_fields = [
            personal_data.get("name"),
            personal_data.get("brand_name"),
            personal_data.get("brand_positioning"),
            personal_data.get("unique_value_proposition"),
            personal_data.get("expertise_areas"),
            audience_data.get("age_range"),
            audience_data.get("location"),
            business_data.get("current_offerings"),
            content_data.get("active_platforms")
        ]
        
        if not all(required_fields):
            raise ValueError("Please fill in all required fields marked with *")
        
        # Create audience demographics
        audience_demographics = AudienceDemographics(
            age_range=audience_data["age_range"],
            gender_split=audience_data["gender_split"],
            location=audience_data["location"],
            interests=audience_data["interests"],
            pain_points=audience_data["pain_points"],
            preferred_content_types=audience_data["preferred_content_types"]
        )
        
        # Create business goals
        business_goals = BusinessGoals(
            primary_objective=business_data["primary_objective"],
            target_revenue=business_data.get("target_revenue"),
            lead_generation_target=business_data.get("lead_generation_target"),
            brand_awareness_goals=business_data.get("brand_awareness_goals")
        )
        
        # Create content preferences
        content_preferences = ContentPreferences(
            preferred_content_types=content_data["preferred_content_types"],
            content_pillars=content_data["content_pillars"],
            posting_frequency=content_data["posting_frequency"],
            content_length_preferences={},  # Can be added later
            visual_style=content_data["visual_style"]
        )
        
        # Create sales process
        sales_process = SalesProcess(
            lead_qualification_questions=lead_data["lead_qualification_questions"],
            follow_up_sequence=lead_data["follow_up_sequence"],
            sales_funnel_stages=lead_data["sales_funnel_stages"],
            conversion_triggers=lead_data["conversion_triggers"]
        )
        
        # Create user profile
        user_profile = UserProfile(
            user_id=f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            name=personal_data["name"],
            age=personal_data["age"],
            cultural_background=personal_data["cultural_background"],
            primary_language=personal_data["primary_language"],
            secondary_language=personal_data.get("secondary_language"),
            brand_name=personal_data["brand_name"],
            brand_positioning=personal_data["brand_positioning"],
            unique_value_proposition=personal_data["unique_value_proposition"],
            expertise_areas=personal_data["expertise_areas"],
            audience_demographics=audience_demographics,
            business_goals=business_goals,
            current_offerings=business_data["current_offerings"],
            pricing_strategy=business_data.get("pricing_strategy"),
            content_preferences=content_preferences,
            available_time=content_data["available_time"],
            content_creation_skills=content_data["content_creation_skills"],
            active_platforms=content_data["active_platforms"],
            platform_priorities=content_data["platform_priorities"],
            platform_language_preferences=content_data["platform_language_preferences"],
            lead_magnets=lead_data["lead_magnets"],
            sales_process=sales_process
        )
        
        return user_profile


def main():
    """Main function to run the intake form"""
    st.set_page_config(
        page_title="Content Marketing Agent Setup",
        page_icon="🎯",
        layout="wide"
    )
    
    intake_form = IntakeForm()
    user_profile = intake_form.render_intake_form()
    
    if user_profile:
        st.success("Profile created successfully!")
        
        # Save profile to session state
        st.session_state.user_profile = user_profile
        
        # Display profile summary
        with st.expander("📋 Profile Summary"):
            st.json(user_profile.dict())


if __name__ == "__main__":
    main()