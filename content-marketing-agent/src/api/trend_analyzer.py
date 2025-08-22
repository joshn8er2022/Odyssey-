import asyncio
import httpx
import tweepy
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import json
import re
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class TrendData:
    """Data structure for trend information"""
    topic: str
    platform: str
    engagement_score: float
    relevance_score: float
    hashtags: List[str]
    sample_content: str
    timestamp: datetime


@dataclass
class ContentOpportunity:
    """Data structure for content opportunities"""
    topic: str
    opportunity_type: str
    engagement_potential: float
    cultural_relevance: float
    suggested_approach: str
    optimal_platforms: List[str]
    recommended_hashtags: List[str]


class SocialMediaTrendAnalyzer:
    """Analyzes trends across multiple social media platforms"""
    
    def __init__(self):
        self.twitter_api = self._setup_twitter_api()
        self.youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        self.session = httpx.AsyncClient()
    
    def _setup_twitter_api(self) -> Optional[tweepy.API]:
        """Setup Twitter API connection"""
        try:
            auth = tweepy.OAuthHandler(
                os.getenv("TWITTER_API_KEY"),
                os.getenv("TWITTER_API_SECRET")
            )
            auth.set_access_token(
                os.getenv("TWITTER_ACCESS_TOKEN"),
                os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
            )
            return tweepy.API(auth, wait_on_rate_limit=True)
        except Exception as e:
            print(f"Twitter API setup failed: {e}")
            return None
    
    async def analyze_twitter_trends(self, location_woeid: int = 1) -> List[TrendData]:
        """Analyze trending topics on Twitter"""
        trends = []
        
        if not self.twitter_api:
            return trends
        
        try:
            # Get trending topics
            trending_topics = self.twitter_api.get_place_trends(location_woeid)[0]['trends']
            
            for trend in trending_topics[:10]:  # Top 10 trends
                topic = trend['name']
                
                # Search for tweets about this topic
                try:
                    tweets = tweepy.Cursor(
                        self.twitter_api.search_tweets,
                        q=topic,
                        lang='en',
                        result_type='popular',
                        count=20
                    ).items(20)
                    
                    tweet_texts = [tweet.text for tweet in tweets]
                    engagement_scores = [
                        tweet.retweet_count + tweet.favorite_count 
                        for tweet in tweets
                    ]
                    
                    avg_engagement = sum(engagement_scores) / len(engagement_scores) if engagement_scores else 0
                    
                    # Extract hashtags
                    hashtags = []
                    for text in tweet_texts:
                        hashtags.extend(re.findall(r'#\w+', text))
                    
                    unique_hashtags = list(set(hashtags))[:5]
                    
                    trends.append(TrendData(
                        topic=topic,
                        platform="twitter",
                        engagement_score=avg_engagement,
                        relevance_score=0.0,  # Will be calculated later
                        hashtags=unique_hashtags,
                        sample_content=tweet_texts[0] if tweet_texts else "",
                        timestamp=datetime.now()
                    ))
                    
                except Exception as e:
                    print(f"Error analyzing trend {topic}: {e}")
                    continue
        
        except Exception as e:
            print(f"Error fetching Twitter trends: {e}")
        
        return trends
    
    async def analyze_youtube_trends(self, region_code: str = "US") -> List[TrendData]:
        """Analyze trending videos on YouTube"""
        trends = []
        
        if not self.youtube_api_key:
            return trends
        
        try:
            url = "https://www.googleapis.com/youtube/v3/videos"
            params = {
                "part": "snippet,statistics",
                "chart": "mostPopular",
                "regionCode": region_code,
                "maxResults": 20,
                "key": self.youtube_api_key
            }
            
            response = await self.session.get(url, params=params)
            data = response.json()
            
            if "items" in data:
                for video in data["items"]:
                    snippet = video["snippet"]
                    stats = video["statistics"]
                    
                    # Extract hashtags from description
                    hashtags = re.findall(r'#\w+', snippet.get("description", ""))
                    
                    # Calculate engagement score
                    views = int(stats.get("viewCount", 0))
                    likes = int(stats.get("likeCount", 0))
                    comments = int(stats.get("commentCount", 0))
                    
                    engagement_score = (likes + comments) / max(views, 1) * 1000
                    
                    trends.append(TrendData(
                        topic=snippet["title"],
                        platform="youtube",
                        engagement_score=engagement_score,
                        relevance_score=0.0,
                        hashtags=hashtags[:5],
                        sample_content=snippet.get("description", "")[:200],
                        timestamp=datetime.now()
                    ))
        
        except Exception as e:
            print(f"Error fetching YouTube trends: {e}")
        
        return trends
    
    async def analyze_google_trends(self, keywords: List[str], geo: str = "CM") -> List[TrendData]:
        """Analyze Google Trends data (using unofficial API)"""
        trends = []
        
        try:
            # This would typically use pytrends or similar library
            # For now, we'll simulate trend data
            for keyword in keywords:
                trends.append(TrendData(
                    topic=keyword,
                    platform="google",
                    engagement_score=75.0,  # Simulated
                    relevance_score=0.0,
                    hashtags=[f"#{keyword.replace(' ', '').lower()}"],
                    sample_content=f"Trending searches related to {keyword}",
                    timestamp=datetime.now()
                ))
        
        except Exception as e:
            print(f"Error fetching Google trends: {e}")
        
        return trends
    
    def calculate_relevance_scores(
        self, 
        trends: List[TrendData], 
        user_interests: List[str],
        expertise_areas: List[str],
        cultural_context: str = "cameroon"
    ) -> List[TrendData]:
        """Calculate relevance scores for trends based on user profile"""
        
        # Keywords that indicate cultural relevance for Cameroon
        cultural_keywords = [
            "africa", "cameroon", "francophone", "bilingual", "french",
            "african", "diaspora", "culture", "tradition", "community"
        ]
        
        for trend in trends:
            relevance_score = 0.0
            
            # Check interest alignment
            for interest in user_interests:
                if interest.lower() in trend.topic.lower() or interest.lower() in trend.sample_content.lower():
                    relevance_score += 2.0
            
            # Check expertise alignment
            for expertise in expertise_areas:
                if expertise.lower() in trend.topic.lower() or expertise.lower() in trend.sample_content.lower():
                    relevance_score += 3.0
            
            # Check cultural relevance
            if cultural_context == "cameroon":
                for keyword in cultural_keywords:
                    if keyword in trend.topic.lower() or keyword in trend.sample_content.lower():
                        relevance_score += 1.5
            
            # Normalize score (0-10)
            trend.relevance_score = min(relevance_score, 10.0)
        
        return trends
    
    def identify_content_opportunities(
        self, 
        trends: List[TrendData],
        user_profile_data: Dict
    ) -> List[ContentOpportunity]:
        """Identify specific content opportunities from trends"""
        
        opportunities = []
        
        # Sort trends by combined engagement and relevance score
        sorted_trends = sorted(
            trends, 
            key=lambda t: (t.engagement_score * 0.3 + t.relevance_score * 0.7),
            reverse=True
        )
        
        for trend in sorted_trends[:15]:  # Top 15 opportunities
            if trend.relevance_score < 2.0:  # Skip low relevance trends
                continue
            
            # Determine opportunity type
            opportunity_type = self._classify_opportunity_type(trend, user_profile_data)
            
            # Calculate engagement potential
            engagement_potential = min(
                (trend.engagement_score * 0.4 + trend.relevance_score * 0.6) / 10 * 100,
                100.0
            )
            
            # Suggest approach
            suggested_approach = self._suggest_content_approach(trend, user_profile_data)
            
            # Recommend platforms
            optimal_platforms = self._recommend_platforms(trend, user_profile_data)
            
            opportunities.append(ContentOpportunity(
                topic=trend.topic,
                opportunity_type=opportunity_type,
                engagement_potential=engagement_potential,
                cultural_relevance=trend.relevance_score,
                suggested_approach=suggested_approach,
                optimal_platforms=optimal_platforms,
                recommended_hashtags=trend.hashtags
            ))
        
        return opportunities
    
    def _classify_opportunity_type(self, trend: TrendData, user_profile: Dict) -> str:
        """Classify the type of content opportunity"""
        
        topic_lower = trend.topic.lower()
        content_lower = trend.sample_content.lower()
        
        # Educational content indicators
        educational_keywords = ["how to", "tips", "guide", "learn", "tutorial", "advice"]
        if any(keyword in topic_lower or keyword in content_lower for keyword in educational_keywords):
            return "educational"
        
        # Trending/viral content indicators
        viral_keywords = ["viral", "trending", "challenge", "meme", "popular"]
        if any(keyword in topic_lower or keyword in content_lower for keyword in viral_keywords):
            return "viral_trend"
        
        # News/current events
        news_keywords = ["breaking", "news", "update", "announcement", "latest"]
        if any(keyword in topic_lower or keyword in content_lower for keyword in news_keywords):
            return "news_commentary"
        
        # Personal development
        personal_keywords = ["motivation", "inspiration", "success", "growth", "mindset"]
        if any(keyword in topic_lower or keyword in content_lower for keyword in personal_keywords):
            return "personal_development"
        
        return "general_content"
    
    def _suggest_content_approach(self, trend: TrendData, user_profile: Dict) -> str:
        """Suggest how to approach creating content for this trend"""
        
        approaches = {
            "educational": "Create a tutorial or how-to guide that incorporates this trending topic while showcasing your expertise.",
            "viral_trend": "Put your unique spin on this trend by relating it to your niche and personal experience.",
            "news_commentary": "Share your expert perspective on this news/event and how it relates to your audience's interests.",
            "personal_development": "Create motivational content that connects this trend to your audience's growth journey.",
            "general_content": "Find a way to connect this trend to your expertise and provide value to your audience."
        }
        
        opportunity_type = self._classify_opportunity_type(trend, user_profile)
        return approaches.get(opportunity_type, approaches["general_content"])
    
    def _recommend_platforms(self, trend: TrendData, user_profile: Dict) -> List[str]:
        """Recommend optimal platforms for this trend"""
        
        platform_recommendations = {
            "educational": ["youtube", "linkedin", "instagram"],
            "viral_trend": ["tiktok", "instagram", "twitter"],
            "news_commentary": ["twitter", "linkedin", "facebook"],
            "personal_development": ["instagram", "linkedin", "youtube"],
            "general_content": ["instagram", "tiktok", "facebook"]
        }
        
        opportunity_type = self._classify_opportunity_type(trend, user_profile)
        return platform_recommendations.get(opportunity_type, ["instagram", "tiktok"])
    
    async def get_optimal_posting_times(
        self, 
        platforms: List[str], 
        audience_locations: List[str]
    ) -> Dict[str, List[str]]:
        """Get optimal posting times for each platform based on audience location"""
        
        # This would typically analyze audience activity data
        # For now, we'll provide general best practices
        
        optimal_times = {
            "instagram": [
                "Monday-Friday: 11 AM - 1 PM",
                "Tuesday-Thursday: 5 PM - 7 PM",
                "Weekend: 10 AM - 12 PM"
            ],
            "tiktok": [
                "Tuesday-Thursday: 6 AM - 10 AM",
                "Tuesday-Thursday: 7 PM - 9 PM",
                "Weekend: 9 AM - 12 PM"
            ],
            "youtube": [
                "Monday-Wednesday: 2 PM - 4 PM",
                "Thursday-Friday: 12 PM - 3 PM",
                "Weekend: 9 AM - 11 AM"
            ],
            "linkedin": [
                "Tuesday-Thursday: 8 AM - 10 AM",
                "Tuesday-Thursday: 12 PM - 2 PM",
                "Wednesday: 5 PM - 6 PM"
            ],
            "twitter": [
                "Monday-Friday: 9 AM - 10 AM",
                "Monday-Friday: 12 PM - 3 PM",
                "Tuesday-Thursday: 5 PM - 6 PM"
            ],
            "facebook": [
                "Tuesday-Thursday: 1 PM - 3 PM",
                "Wednesday-Friday: 9 AM - 10 AM",
                "Weekend: 12 PM - 1 PM"
            ]
        }
        
        # Adjust for audience locations (basic timezone consideration)
        if "cameroon" in [loc.lower() for loc in audience_locations]:
            # Adjust times for West Africa Time (WAT)
            adjusted_times = {}
            for platform, times in optimal_times.items():
                adjusted_times[platform] = [
                    f"{time} WAT" for time in times
                ]
            return adjusted_times
        
        return optimal_times
    
    async def close(self):
        """Close HTTP session"""
        await self.session.aclose()


class TrendAnalysisOrchestrator:
    """Orchestrates trend analysis across multiple platforms"""
    
    def __init__(self):
        self.analyzer = SocialMediaTrendAnalyzer()
    
    async def comprehensive_trend_analysis(
        self,
        user_interests: List[str],
        expertise_areas: List[str],
        cultural_context: str = "cameroon",
        audience_locations: List[str] = ["Cameroon"]
    ) -> Dict:
        """Perform comprehensive trend analysis"""
        
        try:
            # Gather trends from multiple sources
            twitter_trends = await self.analyzer.analyze_twitter_trends()
            youtube_trends = await self.analyzer.analyze_youtube_trends()
            google_trends = await self.analyzer.analyze_google_trends(expertise_areas)
            
            # Combine all trends
            all_trends = twitter_trends + youtube_trends + google_trends
            
            # Calculate relevance scores
            relevant_trends = self.analyzer.calculate_relevance_scores(
                all_trends, user_interests, expertise_areas, cultural_context
            )
            
            # Identify content opportunities
            opportunities = self.analyzer.identify_content_opportunities(
                relevant_trends, {
                    "interests": user_interests,
                    "expertise": expertise_areas,
                    "cultural_context": cultural_context
                }
            )
            
            # Get optimal posting times
            platforms = list(set([opp.optimal_platforms[0] for opp in opportunities if opp.optimal_platforms]))
            optimal_times = await self.analyzer.get_optimal_posting_times(platforms, audience_locations)
            
            return {
                "trending_topics": [
                    {
                        "topic": trend.topic,
                        "platform": trend.platform,
                        "engagement_score": trend.engagement_score,
                        "relevance_score": trend.relevance_score,
                        "hashtags": trend.hashtags
                    }
                    for trend in sorted(relevant_trends, key=lambda t: t.relevance_score, reverse=True)[:10]
                ],
                "content_opportunities": [
                    {
                        "topic": opp.topic,
                        "type": opp.opportunity_type,
                        "engagement_potential": opp.engagement_potential,
                        "cultural_relevance": opp.cultural_relevance,
                        "approach": opp.suggested_approach,
                        "platforms": opp.optimal_platforms,
                        "hashtags": opp.recommended_hashtags
                    }
                    for opp in opportunities[:10]
                ],
                "optimal_timing": optimal_times,
                "analysis_timestamp": datetime.now().isoformat(),
                "total_trends_analyzed": len(all_trends),
                "relevant_trends_found": len([t for t in relevant_trends if t.relevance_score > 2.0])
            }
        
        finally:
            await self.analyzer.close()


# Example usage
async def main():
    """Example usage of the trend analyzer"""
    
    orchestrator = TrendAnalysisOrchestrator()
    
    result = await orchestrator.comprehensive_trend_analysis(
        user_interests=["personal development", "business", "health"],
        expertise_areas=["life coaching", "entrepreneurship"],
        cultural_context="cameroon",
        audience_locations=["Cameroon", "Nigeria", "France"]
    )
    
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())