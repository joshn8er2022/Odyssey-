import dspy
from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class TrendAnalyzer(dspy.Signature):
    """Analyze current social media trends across platforms and identify opportunities for content creation"""
    
    target_demographics: str = dspy.InputField(
        desc="User's specific audience demographics and interests"
    )
    cultural_context: str = dspy.InputField(
        desc="Cultural background (Cameroonian, bilingual EN/FR)"
    )
    content_niche: str = dspy.InputField(
        desc="User's specified content focus area"
    )
    
    trending_topics: str = dspy.OutputField(
        desc="Top 5 trending topics relevant to audience"
    )
    content_opportunities: str = dspy.OutputField(
        desc="Specific content ideas with engagement potential"
    )
    optimal_timing: str = dspy.OutputField(
        desc="Best posting times for target audience"
    )


class ContentStrategist(dspy.Signature):
    """Generate personalized content strategy based on trends and user profile"""
    
    user_profile: str = dspy.InputField(
        desc="Complete user intake information"
    )
    trend_data: str = dspy.InputField(
        desc="Current trending topics and opportunities"
    )
    content_type: str = dspy.InputField(
        desc="Educational, lead magnet, or CTA-focused content"
    )
    
    content_strategy: str = dspy.OutputField(
        desc="Detailed content plan with hooks and value propositions"
    )
    target_outcome: str = dspy.OutputField(
        desc="Expected engagement and conversion goals"
    )


class ContentCreator(dspy.Signature):
    """Create engaging video scripts and text content in English and French"""
    
    strategy_input: str = dspy.InputField(
        desc="Content strategy and key messaging"
    )
    language_preference: str = dspy.InputField(
        desc="Primary language (EN/FR) or bilingual approach"
    )
    platform_specs: str = dspy.InputField(
        desc="Target platform requirements (TikTok, Instagram, etc.)"
    )
    
    video_script: str = dspy.OutputField(
        desc="Complete video script with timing and visual cues"
    )
    text_content: str = dspy.OutputField(
        desc="Captions, descriptions, and hashtags"
    )
    call_to_action: str = dspy.OutputField(
        desc="Specific CTA based on content purpose"
    )


class LeadMagnetManager(dspy.Signature):
    """Monitor comments and automatically distribute relevant lead magnets"""
    
    comment_content: str = dspy.InputField(
        desc="User comment or engagement"
    )
    user_context: str = dspy.InputField(
        desc="Commenter's apparent interests and needs"
    )
    available_lead_magnets: str = dspy.InputField(
        desc="Library of lead magnets to choose from"
    )
    
    lead_magnet_match: str = dspy.OutputField(
        desc="Most relevant lead magnet for this user"
    )
    personalized_message: str = dspy.OutputField(
        desc="Custom message to accompany lead magnet"
    )
    qualification_questions: str = dspy.OutputField(
        desc="Follow-up questions to qualify the lead"
    )


class CulturalContextAnalyzer(dspy.Signature):
    """Analyze content for cultural sensitivity and relevance to Cameroonian audience"""
    
    content: str = dspy.InputField(
        desc="Content to analyze for cultural appropriateness"
    )
    target_culture: str = dspy.InputField(
        desc="Target cultural context (Cameroonian, bilingual)"
    )
    content_type: str = dspy.InputField(
        desc="Type of content (video, text, image)"
    )
    
    cultural_score: str = dspy.OutputField(
        desc="Cultural relevance score (1-10) with explanation"
    )
    suggestions: str = dspy.OutputField(
        desc="Specific suggestions to improve cultural relevance"
    )
    warnings: str = dspy.OutputField(
        desc="Any potential cultural sensitivity issues"
    )


class PerformanceOptimizer(dspy.Signature):
    """Analyze content performance and suggest optimizations"""
    
    content_metrics: str = dspy.InputField(
        desc="Engagement metrics, reach, and performance data"
    )
    audience_feedback: str = dspy.InputField(
        desc="Comments, shares, and audience reactions"
    )
    content_details: str = dspy.InputField(
        desc="Content type, timing, and platform specifics"
    )
    
    performance_analysis: str = dspy.OutputField(
        desc="Detailed analysis of what worked and what didn't"
    )
    optimization_suggestions: str = dspy.OutputField(
        desc="Specific recommendations for future content"
    )
    trend_insights: str = dspy.OutputField(
        desc="Emerging trends based on performance data"
    )