from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal
from datetime import datetime
from enum import Enum


class ContentType(str, Enum):
    EDUCATIONAL = "educational"
    LEAD_MAGNET = "lead_magnet"
    CTA_FOCUSED = "cta_focused"
    ENTERTAINMENT = "entertainment"
    TESTIMONIAL = "testimonial"


class Platform(str, Enum):
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    LINKEDIN = "linkedin"
    FACEBOOK = "facebook"
    TWITTER = "twitter"


class Language(str, Enum):
    ENGLISH = "en"
    FRENCH = "fr"
    BILINGUAL = "bilingual"


class AudienceDemographics(BaseModel):
    age_range: str = Field(..., description="Primary age range of audience")
    gender_split: str = Field(..., description="Gender distribution")
    location: List[str] = Field(..., description="Primary geographic locations")
    interests: List[str] = Field(..., description="Main interests and hobbies")
    pain_points: List[str] = Field(..., description="Common problems they face")
    preferred_content_types: List[ContentType] = Field(..., description="Content types they engage with most")


class BusinessGoals(BaseModel):
    primary_objective: str = Field(..., description="Main business goal")
    target_revenue: Optional[float] = Field(None, description="Monthly revenue target")
    lead_generation_target: Optional[int] = Field(None, description="Monthly lead target")
    brand_awareness_goals: Optional[str] = Field(None, description="Brand awareness objectives")
    conversion_metrics: Dict[str, float] = Field(default_factory=dict, description="Key conversion rates")


class ContentPreferences(BaseModel):
    preferred_content_types: List[ContentType] = Field(..., description="Preferred content types to create")
    content_pillars: List[str] = Field(..., description="Main content themes/pillars")
    posting_frequency: Dict[Platform, int] = Field(..., description="Posts per week per platform")
    content_length_preferences: Dict[Platform, str] = Field(..., description="Preferred content length per platform")
    visual_style: str = Field(..., description="Preferred visual style and branding")


class LeadMagnet(BaseModel):
    id: str = Field(..., description="Unique identifier")
    title: str = Field(..., description="Lead magnet title")
    description: str = Field(..., description="What the lead magnet offers")
    target_audience: str = Field(..., description="Who this is for")
    keywords: List[str] = Field(..., description="Keywords that trigger this lead magnet")
    file_url: Optional[str] = Field(None, description="Download link")
    landing_page_url: Optional[str] = Field(None, description="Landing page URL")
    conversion_rate: Optional[float] = Field(None, description="Historical conversion rate")


class SalesProcess(BaseModel):
    lead_qualification_questions: List[str] = Field(..., description="Questions to qualify leads")
    follow_up_sequence: List[str] = Field(..., description="Automated follow-up messages")
    sales_funnel_stages: List[str] = Field(..., description="Stages in the sales process")
    conversion_triggers: List[str] = Field(..., description="What triggers a sales conversation")


class UserProfile(BaseModel):
    # Personal Information
    user_id: str = Field(..., description="Unique user identifier")
    name: str = Field(..., description="User's name")
    age: int = Field(..., description="User's age")
    cultural_background: str = Field(default="cameroon", description="Cultural context")
    primary_language: Language = Field(..., description="Primary language preference")
    secondary_language: Optional[Language] = Field(None, description="Secondary language")
    
    # Brand Positioning
    brand_name: str = Field(..., description="Personal or business brand name")
    brand_positioning: str = Field(..., description="How they position themselves in the market")
    unique_value_proposition: str = Field(..., description="What makes them unique")
    expertise_areas: List[str] = Field(..., description="Areas of expertise")
    
    # Audience Information
    audience_demographics: AudienceDemographics = Field(..., description="Target audience details")
    audience_size: Dict[Platform, int] = Field(default_factory=dict, description="Follower count per platform")
    
    # Business Information
    business_goals: BusinessGoals = Field(..., description="Business objectives")
    current_offerings: List[str] = Field(..., description="Products/services offered")
    pricing_strategy: Optional[str] = Field(None, description="Pricing approach")
    
    # Content Preferences
    content_preferences: ContentPreferences = Field(..., description="Content creation preferences")
    available_time: int = Field(..., description="Hours per week available for content creation")
    content_creation_skills: List[str] = Field(..., description="Current content creation skills")
    
    # Platform Preferences
    active_platforms: List[Platform] = Field(..., description="Platforms they're active on")
    platform_priorities: Dict[Platform, int] = Field(..., description="Priority ranking per platform (1-5)")
    platform_language_preferences: Dict[Platform, Language] = Field(..., description="Language preference per platform")
    
    # Lead Generation
    lead_magnets: List[LeadMagnet] = Field(default_factory=list, description="Available lead magnets")
    sales_process: SalesProcess = Field(..., description="Sales and follow-up process")
    
    # Analytics and Optimization
    performance_goals: Dict[str, float] = Field(default_factory=dict, description="Performance targets")
    current_metrics: Dict[str, float] = Field(default_factory=dict, description="Current performance metrics")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ContentRequest(BaseModel):
    user_id: str = Field(..., description="User requesting content")
    content_type: ContentType = Field(..., description="Type of content to create")
    target_platform: Platform = Field(..., description="Primary platform for content")
    language_preference: Language = Field(..., description="Language for this content")
    topic: Optional[str] = Field(None, description="Specific topic or theme")
    call_to_action_type: Optional[str] = Field(None, description="Type of CTA needed")
    urgency: Literal["low", "medium", "high"] = Field(default="medium", description="Content urgency")
    created_at: datetime = Field(default_factory=datetime.now)


class ContentPiece(BaseModel):
    id: str = Field(..., description="Unique content identifier")
    user_id: str = Field(..., description="Content creator")
    title: str = Field(..., description="Content title")
    content_type: ContentType = Field(..., description="Type of content")
    platform: Platform = Field(..., description="Target platform")
    language: Language = Field(..., description="Content language")
    
    # Content Details
    video_script: Optional[str] = Field(None, description="Video script with timing")
    text_content: str = Field(..., description="Captions, descriptions")
    hashtags: List[str] = Field(default_factory=list, description="Relevant hashtags")
    call_to_action: str = Field(..., description="Specific CTA")
    
    # Metadata
    trending_topics_used: List[str] = Field(default_factory=list, description="Trending topics incorporated")
    cultural_score: Optional[float] = Field(None, description="Cultural relevance score")
    estimated_engagement: Optional[float] = Field(None, description="Predicted engagement rate")
    
    # Status
    status: Literal["draft", "approved", "scheduled", "published"] = Field(default="draft")
    scheduled_time: Optional[datetime] = Field(None, description="When to publish")
    published_time: Optional[datetime] = Field(None, description="When it was published")
    
    # Performance
    actual_engagement: Optional[Dict[str, float]] = Field(None, description="Actual performance metrics")
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)