import dspy
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import asyncio
import json

from .signatures import (
    TrendAnalyzer,
    ContentStrategist,
    ContentCreator,
    LeadMagnetManager,
    CulturalContextAnalyzer,
    PerformanceOptimizer
)
from ..models.user_profile import (
    UserProfile,
    ContentRequest,
    ContentPiece,
    Platform,
    Language,
    ContentType
)


class ContentMarketingAgent(dspy.Module):
    """Main orchestrator for the content marketing assistant"""
    
    def __init__(self, llm_model: str = "gpt-3.5-turbo"):
        super().__init__()
        
        # Initialize DSPy with the specified model
        dspy.settings.configure(lm=dspy.OpenAI(model=llm_model))
        
        # Initialize signature modules
        self.trend_analyzer = dspy.ChainOfThought(TrendAnalyzer)
        self.strategist = dspy.ChainOfThought(ContentStrategist)
        self.creator = dspy.ChainOfThought(ContentCreator)
        self.lead_manager = dspy.ChainOfThought(LeadMagnetManager)
        self.cultural_analyzer = dspy.ChainOfThought(CulturalContextAnalyzer)
        self.performance_optimizer = dspy.ChainOfThought(PerformanceOptimizer)
    
    def analyze_trends(self, user_profile: UserProfile) -> Dict:
        """Analyze current trends relevant to the user's audience and niche"""
        
        # Prepare demographics string
        demographics = f"""
        Age Range: {user_profile.audience_demographics.age_range}
        Gender: {user_profile.audience_demographics.gender_split}
        Locations: {', '.join(user_profile.audience_demographics.location)}
        Interests: {', '.join(user_profile.audience_demographics.interests)}
        Pain Points: {', '.join(user_profile.audience_demographics.pain_points)}
        """
        
        # Prepare cultural context
        cultural_context = f"""
        Cultural Background: {user_profile.cultural_background}
        Primary Language: {user_profile.primary_language}
        Secondary Language: {user_profile.secondary_language or 'None'}
        Brand Positioning: {user_profile.brand_positioning}
        """
        
        # Prepare content niche
        content_niche = f"""
        Expertise Areas: {', '.join(user_profile.expertise_areas)}
        Content Pillars: {', '.join(user_profile.content_preferences.content_pillars)}
        Current Offerings: {', '.join(user_profile.current_offerings)}
        """
        
        # Analyze trends
        trend_result = self.trend_analyzer(
            target_demographics=demographics,
            cultural_context=cultural_context,
            content_niche=content_niche
        )
        
        return {
            "trending_topics": trend_result.trending_topics,
            "content_opportunities": trend_result.content_opportunities,
            "optimal_timing": trend_result.optimal_timing,
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    def generate_content_strategy(
        self, 
        user_profile: UserProfile, 
        trend_data: Dict,
        content_type: ContentType = ContentType.EDUCATIONAL
    ) -> Dict:
        """Generate a personalized content strategy based on trends and user profile"""
        
        # Prepare user profile summary
        profile_summary = f"""
        Brand: {user_profile.brand_name}
        Positioning: {user_profile.brand_positioning}
        UVP: {user_profile.unique_value_proposition}
        Expertise: {', '.join(user_profile.expertise_areas)}
        Target Audience: {user_profile.audience_demographics.age_range} in {', '.join(user_profile.audience_demographics.location)}
        Business Goals: {user_profile.business_goals.primary_objective}
        Available Time: {user_profile.available_time} hours/week
        Active Platforms: {', '.join([p.value for p in user_profile.active_platforms])}
        """
        
        # Prepare trend data summary
        trends_summary = f"""
        Trending Topics: {trend_data.get('trending_topics', '')}
        Content Opportunities: {trend_data.get('content_opportunities', '')}
        Optimal Timing: {trend_data.get('optimal_timing', '')}
        """
        
        # Generate strategy
        strategy_result = self.strategist(
            user_profile=profile_summary,
            trend_data=trends_summary,
            content_type=content_type.value
        )
        
        return {
            "content_strategy": strategy_result.content_strategy,
            "target_outcome": strategy_result.target_outcome,
            "strategy_timestamp": datetime.now().isoformat()
        }
    
    def create_content(
        self,
        user_profile: UserProfile,
        strategy: Dict,
        platform: Platform,
        language: Language = Language.ENGLISH,
        topic: Optional[str] = None
    ) -> ContentPiece:
        """Create specific content based on strategy and requirements"""
        
        # Prepare strategy input
        strategy_input = f"""
        Content Strategy: {strategy.get('content_strategy', '')}
        Target Outcome: {strategy.get('target_outcome', '')}
        Specific Topic: {topic or 'Use trending topics from strategy'}
        Brand Voice: {user_profile.brand_positioning}
        """
        
        # Prepare platform specifications
        platform_specs = self._get_platform_specifications(platform)
        
        # Create content
        content_result = self.creator(
            strategy_input=strategy_input,
            language_preference=language.value,
            platform_specs=platform_specs
        )
        
        # Analyze cultural relevance
        cultural_result = self.cultural_analyzer(
            content=content_result.video_script + " " + content_result.text_content,
            target_culture=f"{user_profile.cultural_background}, {language.value}",
            content_type="video and text"
        )
        
        # Create ContentPiece object
        content_piece = ContentPiece(
            id=f"content_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            user_id=user_profile.user_id,
            title=topic or "Generated Content",
            content_type=ContentType.EDUCATIONAL,  # Default, can be customized
            platform=platform,
            language=language,
            video_script=content_result.video_script,
            text_content=content_result.text_content,
            hashtags=self._extract_hashtags(content_result.text_content),
            call_to_action=content_result.call_to_action,
            cultural_score=self._parse_cultural_score(cultural_result.cultural_score)
        )
        
        return content_piece
    
    def manage_lead_magnet_response(
        self,
        user_profile: UserProfile,
        comment_content: str,
        commenter_context: str = ""
    ) -> Dict:
        """Automatically match and respond with appropriate lead magnets"""
        
        # Prepare available lead magnets
        lead_magnets_summary = "\n".join([
            f"- {lm.title}: {lm.description} (Keywords: {', '.join(lm.keywords)})"
            for lm in user_profile.lead_magnets
        ])
        
        # Generate lead magnet response
        lead_result = self.lead_manager(
            comment_content=comment_content,
            user_context=commenter_context,
            available_lead_magnets=lead_magnets_summary
        )
        
        return {
            "lead_magnet_match": lead_result.lead_magnet_match,
            "personalized_message": lead_result.personalized_message,
            "qualification_questions": lead_result.qualification_questions,
            "response_timestamp": datetime.now().isoformat()
        }
    
    def daily_content_workflow(self, user_profile: UserProfile) -> List[ContentPiece]:
        """Execute the complete daily content creation workflow"""
        
        content_pieces = []
        
        # Step 1: Analyze current trends
        trends = self.analyze_trends(user_profile)
        
        # Step 2: Generate content strategy
        strategy = self.generate_content_strategy(user_profile, trends)
        
        # Step 3: Create content for each active platform
        for platform in user_profile.active_platforms:
            # Determine language preference for this platform
            language = user_profile.platform_language_preferences.get(
                platform, 
                user_profile.primary_language
            )
            
            # Create content piece
            content_piece = self.create_content(
                user_profile=user_profile,
                strategy=strategy,
                platform=platform,
                language=language
            )
            
            content_pieces.append(content_piece)
        
        return content_pieces
    
    def optimize_performance(
        self,
        user_profile: UserProfile,
        content_metrics: Dict,
        audience_feedback: str
    ) -> Dict:
        """Analyze performance and provide optimization suggestions"""
        
        # Prepare metrics summary
        metrics_summary = json.dumps(content_metrics, indent=2)
        
        # Prepare content details
        content_details = f"""
        Active Platforms: {', '.join([p.value for p in user_profile.active_platforms])}
        Content Types: {', '.join([ct.value for ct in user_profile.content_preferences.preferred_content_types])}
        Posting Frequency: {user_profile.content_preferences.posting_frequency}
        Target Audience: {user_profile.audience_demographics.age_range}
        """
        
        # Generate optimization suggestions
        optimization_result = self.performance_optimizer(
            content_metrics=metrics_summary,
            audience_feedback=audience_feedback,
            content_details=content_details
        )
        
        return {
            "performance_analysis": optimization_result.performance_analysis,
            "optimization_suggestions": optimization_result.optimization_suggestions,
            "trend_insights": optimization_result.trend_insights,
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    def _get_platform_specifications(self, platform: Platform) -> str:
        """Get platform-specific requirements and best practices"""
        
        specs = {
            Platform.TIKTOK: """
            - Video length: 15-60 seconds optimal
            - Vertical format (9:16 aspect ratio)
            - Hook within first 3 seconds
            - Trending sounds and effects
            - Clear, bold text overlays
            - Fast-paced, engaging content
            """,
            Platform.INSTAGRAM: """
            - Reels: 15-30 seconds, vertical format
            - Posts: Square or vertical images
            - Stories: Vertical format, 15 seconds
            - Captions: Engaging first line, use line breaks
            - Hashtags: 5-10 relevant hashtags
            - Call-to-action in captions
            """,
            Platform.YOUTUBE: """
            - Shorts: 60 seconds max, vertical
            - Long-form: 8-12 minutes optimal
            - Compelling thumbnails and titles
            - Strong hook in first 15 seconds
            - Clear value proposition
            - End screens and cards for engagement
            """,
            Platform.LINKEDIN: """
            - Professional tone and content
            - Text posts: 1300 characters max
            - Video: 3 minutes max
            - Industry insights and thought leadership
            - Professional storytelling
            - Clear business value
            """
        }
        
        return specs.get(platform, "General social media best practices")
    
    def _extract_hashtags(self, text_content: str) -> List[str]:
        """Extract hashtags from text content"""
        import re
        hashtags = re.findall(r'#\w+', text_content)
        return [tag.lower() for tag in hashtags]
    
    def _parse_cultural_score(self, cultural_score_text: str) -> Optional[float]:
        """Parse cultural score from text response"""
        import re
        score_match = re.search(r'(\d+(?:\.\d+)?)', cultural_score_text)
        if score_match:
            return float(score_match.group(1))
        return None