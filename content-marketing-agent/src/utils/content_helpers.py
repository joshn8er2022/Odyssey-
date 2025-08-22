"""
Simple Python utilities for content processing
Non-AI operations that don't need DSPy
"""

from typing import Dict, List, Optional, Any
import re
from datetime import datetime
import json


class ContentFormatter:
    """Simple utilities for content formatting"""
    
    @staticmethod
    def extract_hashtags(text: str) -> List[str]:
        """Extract hashtags from text"""
        hashtags = re.findall(r'#\w+', text)
        return [tag.lower() for tag in hashtags]
    
    @staticmethod
    def format_bilingual_content(en_content: str, fr_content: str) -> str:
        """Format bilingual content with separator"""
        return f"{en_content}\n\n---\n\n{fr_content}"
    
    @staticmethod
    def truncate_for_platform(content: str, platform: str) -> str:
        """Truncate content based on platform limits"""
        limits = {
            "twitter": 280,
            "instagram": 2200,
            "linkedin": 3000,
            "tiktok": 150,  # For video descriptions
            "facebook": 63206
        }
        
        limit = limits.get(platform, 2200)
        if len(content) <= limit:
            return content
        
        return content[:limit-3] + "..."
    
    @staticmethod
    def add_cultural_hashtags(hashtags: List[str], cultural_context: str, language: str) -> List[str]:
        """Add cultural hashtags based on context"""
        cultural_tags = {
            "cameroon": {
                "en": ["#CameroonPride", "#AfricanWisdom", "#CommunityFirst"],
                "fr": ["#FiertéCamerounaise", "#SagesseAfricaine", "#CommunautéDAbord"]
            }
        }
        
        if cultural_context in cultural_tags:
            cultural_hashtags = cultural_tags[cultural_context].get(language, [])
            # Add 1-2 cultural hashtags if not already present
            for tag in cultural_hashtags[:2]:
                if tag.lower() not in [h.lower() for h in hashtags]:
                    hashtags.append(tag)
        
        return hashtags
    
    @staticmethod
    def format_content_piece(content_data: Dict) -> Dict[str, Any]:
        """Format content piece with metadata"""
        return {
            "id": f"content_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "platform": content_data.get("platform", "general"),
            "language": content_data.get("language", "en"),
            "content_type": content_data.get("content_type", "educational"),
            "text": content_data.get("text", ""),
            "hashtags": content_data.get("hashtags", []),
            "call_to_action": content_data.get("call_to_action", ""),
            "topic": content_data.get("topic", "Generated Content"),
            "trend_based": content_data.get("trend_based", False),
            "cultural_score": content_data.get("cultural_score", None)
        }


class PlatformOptimizer:
    """Simple utilities for platform-specific optimization"""
    
    @staticmethod
    def get_platform_best_practices(platform: str) -> Dict[str, Any]:
        """Get platform-specific best practices"""
        practices = {
            "instagram": {
                "optimal_length": "1-3 sentences for posts, longer for carousels",
                "hashtag_count": "5-10 hashtags",
                "posting_times": ["11 AM - 1 PM", "7 PM - 9 PM"],
                "content_types": ["carousel", "reel", "story", "post"],
                "engagement_tactics": ["ask questions", "use polls", "share behind-scenes"]
            },
            "tiktok": {
                "optimal_length": "15-60 seconds video, short captions",
                "hashtag_count": "3-5 hashtags",
                "posting_times": ["6 AM - 10 AM", "7 PM - 9 PM"],
                "content_types": ["short video", "trending audio", "challenge"],
                "engagement_tactics": ["trending sounds", "quick hooks", "call-to-action"]
            },
            "linkedin": {
                "optimal_length": "1300-1900 characters",
                "hashtag_count": "3-5 hashtags",
                "posting_times": ["8 AM - 10 AM", "12 PM - 2 PM"],
                "content_types": ["article", "post", "video", "document"],
                "engagement_tactics": ["industry insights", "thought leadership", "professional stories"]
            },
            "youtube": {
                "optimal_length": "8-12 minutes for long-form",
                "hashtag_count": "10-15 hashtags in description",
                "posting_times": ["2 PM - 4 PM", "8 PM - 11 PM"],
                "content_types": ["tutorial", "vlog", "educational", "entertainment"],
                "engagement_tactics": ["strong thumbnails", "compelling titles", "clear value proposition"]
            },
            "facebook": {
                "optimal_length": "40-80 characters for high engagement",
                "hashtag_count": "1-2 hashtags",
                "posting_times": ["1 PM - 3 PM", "9 AM - 10 AM"],
                "content_types": ["post", "video", "live", "event"],
                "engagement_tactics": ["community building", "shareable content", "conversation starters"]
            }
        }
        
        return practices.get(platform, {
            "optimal_length": "Keep it concise and engaging",
            "hashtag_count": "3-5 hashtags",
            "posting_times": ["Peak audience hours"],
            "content_types": ["post", "video"],
            "engagement_tactics": ["ask questions", "provide value", "be authentic"]
        })
    
    @staticmethod
    def optimize_hashtags_for_platform(hashtags: List[str], platform: str) -> List[str]:
        """Optimize hashtags for specific platform"""
        platform_limits = {
            "instagram": 30,
            "tiktok": 10,
            "linkedin": 5,
            "twitter": 2,
            "facebook": 2,
            "youtube": 15
        }
        
        limit = platform_limits.get(platform, 10)
        return hashtags[:limit]
    
    @staticmethod
    def get_optimal_posting_schedule(platform: str, timezone: str = "WAT") -> List[str]:
        """Get optimal posting schedule for platform"""
        schedules = {
            "instagram": [
                "Monday-Friday: 11 AM - 1 PM WAT",
                "Tuesday-Thursday: 7 PM - 9 PM WAT",
                "Weekend: 10 AM - 12 PM WAT"
            ],
            "tiktok": [
                "Tuesday-Thursday: 6 AM - 10 AM WAT",
                "Tuesday-Thursday: 7 PM - 9 PM WAT",
                "Weekend: 9 AM - 12 PM WAT"
            ],
            "linkedin": [
                "Tuesday-Thursday: 8 AM - 10 AM WAT",
                "Tuesday-Thursday: 12 PM - 2 PM WAT",
                "Wednesday: 5 PM - 6 PM WAT"
            ],
            "youtube": [
                "Monday-Wednesday: 2 PM - 4 PM WAT",
                "Thursday-Friday: 12 PM - 3 PM WAT",
                "Weekend: 9 AM - 11 AM WAT"
            ],
            "facebook": [
                "Tuesday-Thursday: 1 PM - 3 PM WAT",
                "Wednesday-Friday: 9 AM - 10 AM WAT",
                "Weekend: 12 PM - 1 PM WAT"
            ]
        }
        
        return schedules.get(platform, ["Peak audience hours based on your analytics"])


class TrendDataProcessor:
    """Simple utilities for processing trend data"""
    
    @staticmethod
    def calculate_relevance_score(
        trend_topic: str, 
        user_interests: List[str], 
        expertise_areas: List[str]
    ) -> float:
        """Calculate relevance score for a trend topic"""
        score = 0.0
        topic_lower = trend_topic.lower()
        
        # Check interest alignment
        for interest in user_interests:
            if interest.lower() in topic_lower:
                score += 2.0
        
        # Check expertise alignment (higher weight)
        for expertise in expertise_areas:
            if expertise.lower() in topic_lower:
                score += 3.0
        
        # Normalize to 0-10 scale
        return min(score, 10.0)
    
    @staticmethod
    def filter_relevant_trends(
        trends: List[Dict], 
        user_profile: Dict, 
        min_relevance: float = 2.0
    ) -> List[Dict]:
        """Filter trends by relevance to user"""
        relevant_trends = []
        
        user_interests = user_profile.get('expertise_areas', [])
        
        for trend in trends:
            relevance = TrendDataProcessor.calculate_relevance_score(
                trend.get('topic', ''),
                user_interests,
                user_interests  # Using same list for both
            )
            
            if relevance >= min_relevance:
                trend['relevance_score'] = relevance
                relevant_trends.append(trend)
        
        # Sort by relevance score
        return sorted(relevant_trends, key=lambda x: x.get('relevance_score', 0), reverse=True)
    
    @staticmethod
    def summarize_trends(trends: List[Dict], max_trends: int = 5) -> str:
        """Create a summary of trending topics"""
        if not trends:
            return "No trending topics available"
        
        summary = "📈 **Current Trending Topics:**\n\n"
        
        for i, trend in enumerate(trends[:max_trends], 1):
            topic = trend.get('topic', 'Unknown')
            platform = trend.get('platform', 'general')
            engagement = trend.get('engagement_score', 0)
            relevance = trend.get('relevance_score', 0)
            
            summary += f"{i}. **{topic}** ({platform})\n"
            summary += f"   📊 Engagement: {engagement:.1f}% | Relevance: {relevance:.1f}/10\n\n"
        
        return summary


class ConversationHelper:
    """Simple utilities for conversation management"""
    
    @staticmethod
    def extract_intent(user_message: str) -> str:
        """Extract user intent from message"""
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ['create', 'generate', 'make', 'write']):
            return 'content_creation'
        elif any(word in message_lower for word in ['trend', 'trending', 'popular', 'viral']):
            return 'trend_analysis'
        elif any(word in message_lower for word in ['improve', 'optimize', 'better', 'enhance']):
            return 'content_optimization'
        elif any(word in message_lower for word in ['when', 'time', 'schedule', 'post']):
            return 'posting_strategy'
        elif any(word in message_lower for word in ['hashtag', 'tag', '#']):
            return 'hashtag_advice'
        else:
            return 'general_advice'
    
    @staticmethod
    def format_conversation_history(history: List[Dict], max_messages: int = 5) -> str:
        """Format conversation history for context"""
        if not history:
            return "No previous conversation"
        
        formatted = "Recent conversation:\n"
        recent_messages = history[-max_messages:]
        
        for msg in recent_messages:
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')[:100]  # Truncate long messages
            formatted += f"- {role}: {content}...\n"
        
        return formatted
    
    @staticmethod
    def generate_follow_up_questions(intent: str, user_profile: Dict) -> List[str]:
        """Generate relevant follow-up questions"""
        expertise = user_profile.get('expertise_areas', ['personal development'])[0]
        
        questions = {
            'content_creation': [
                f"What specific aspect of {expertise.lower()} would you like to focus on?",
                "Which platform is your priority right now?",
                "Are you looking for educational or motivational content?"
            ],
            'trend_analysis': [
                "Would you like me to analyze trends for a specific platform?",
                "Are you interested in local or global trends?",
                "What type of content performs best for your audience?"
            ],
            'content_optimization': [
                "What specific metrics are you trying to improve?",
                "Which piece of content would you like to optimize?",
                "Are you looking to increase engagement or reach?"
            ],
            'posting_strategy': [
                "What's your current posting frequency?",
                "Which time zones is your audience in?",
                "Are you posting consistently across all platforms?"
            ],
            'general_advice': [
                "What's your biggest content marketing challenge?",
                "Which platform drives the most engagement for you?",
                "How can I help you grow your audience?"
            ]
        }
        
        return questions.get(intent, questions['general_advice'])[:3]
    
    @staticmethod
    def generate_fallback_response(user_message: str, user_profile: Dict) -> str:
        """Generate a fallback response when DSPy fails"""
        expertise = ', '.join(user_profile.get('expertise_areas', ['personal development']))
        
        return f"""I understand you're asking about: "{user_message}"

Based on your expertise in {expertise}, here are some thoughts:

💡 **Quick Suggestion:** Focus on creating authentic content that showcases your knowledge while connecting with your audience's needs.

🎯 **Next Steps:**
- Consider creating educational content around this topic
- Share your personal experience or client success stories
- Engage with your audience by asking questions

Would you like me to help you create some content around this topic?"""