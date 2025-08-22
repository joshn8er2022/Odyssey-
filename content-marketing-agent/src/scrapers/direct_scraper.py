"""
Direct Scraper Integration
Direct access to Apify scrapers for real-time content analysis
"""

import httpx
import asyncio
import json
import os
import streamlit as st
from typing import Dict, List, Optional, Any
from datetime import datetime

class DirectScraper:
    """Direct scraper for real-time social media data"""
    
    def __init__(self):
        self.api_token = self._get_api_key("APIFY_API_TOKEN")
        self.base_url = "https://api.apify.com/v2/acts"
        
    def _get_api_key(self, key_name: str) -> str:
        """Get API key from Streamlit secrets or environment"""
        try:
            return st.secrets[key_name]
        except:
            return os.getenv(key_name, "")
    
    async def scrape_twitter_content(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Scrape Twitter content directly"""
        
        if not self.api_token:
            return []
        
        scraper_id = "apidojo~twitter-scraper-lite"
        
        input_data = {
            "searchTerms": [query],
            "maxTweets": max_results,
            "addUserInfo": True,
            "includeSearchTerms": False
        }
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/{scraper_id}/run-sync-get-dataset-items?token={self.api_token}",
                    headers={'Content-Type': 'application/json'},
                    json=input_data
                )
                
                if response.status_code in [200, 201]:
                    tweets = response.json()
                    return self._process_twitter_data(tweets)
                else:
                    return []
                    
        except Exception as e:
            print(f"Twitter scraping error: {e}")
            return []
    
    async def scrape_tiktok_content(self, hashtag: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Scrape TikTok content directly"""
        
        if not self.api_token:
            return []
        
        scraper_id = "clockworks~tiktok-scraper"
        
        input_data = {
            "hashtags": [hashtag.replace('#', '')],
            "resultsPerPage": max_results
        }
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/{scraper_id}/run-sync-get-dataset-items?token={self.api_token}",
                    headers={'Content-Type': 'application/json'},
                    json=input_data
                )
                
                if response.status_code in [200, 201]:
                    videos = response.json()
                    return self._process_tiktok_data(videos)
                else:
                    return []
                    
        except Exception as e:
            print(f"TikTok scraping error: {e}")
            return []
    
    async def scrape_instagram_content(self, hashtag: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Scrape Instagram content directly"""
        
        if not self.api_token:
            return []
        
        scraper_id = "shu8hvrXbJbY3Eb9W"
        
        input_data = {
            "hashtags": [hashtag.replace('#', '')],
            "resultsLimit": max_results
        }
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/{scraper_id}/run-sync-get-dataset-items?token={self.api_token}",
                    headers={'Content-Type': 'application/json'},
                    json=input_data
                )
                
                if response.status_code in [200, 201]:
                    posts = response.json()
                    return self._process_instagram_data(posts)
                else:
                    return []
                    
        except Exception as e:
            print(f"Instagram scraping error: {e}")
            return []
    
    async def scrape_multi_platform(self, query: str, platforms: List[str] = None, max_results: int = 5) -> Dict[str, List[Dict[str, Any]]]:
        """Scrape multiple platforms simultaneously"""
        
        if platforms is None:
            platforms = ["twitter", "tiktok", "instagram"]
        
        results = {}
        tasks = []
        
        if "twitter" in platforms:
            tasks.append(("twitter", self.scrape_twitter_content(query, max_results)))
        
        if "tiktok" in platforms:
            tasks.append(("tiktok", self.scrape_tiktok_content(f"#{query}", max_results)))
        
        if "instagram" in platforms:
            tasks.append(("instagram", self.scrape_instagram_content(f"#{query}", max_results)))
        
        # Execute all scraping tasks in parallel
        if tasks:
            task_results = await asyncio.gather(*[task[1] for task in tasks], return_exceptions=True)
            
            for i, (platform, _) in enumerate(tasks):
                result = task_results[i]
                if isinstance(result, Exception):
                    results[platform] = []
                else:
                    results[platform] = result
        
        return results
    
    def _process_twitter_data(self, tweets: List[Dict]) -> List[Dict[str, Any]]:
        """Process raw Twitter data"""
        
        processed = []
        for tweet in tweets:
            processed.append({
                "platform": "twitter",
                "id": tweet.get("id", ""),
                "text": tweet.get("text", ""),
                "author": tweet.get("author", {}).get("userName", "unknown"),
                "likes": tweet.get("likeCount", 0),
                "retweets": tweet.get("retweetCount", 0),
                "replies": tweet.get("replyCount", 0),
                "created_at": tweet.get("createdAt", ""),
                "url": tweet.get("url", ""),
                "engagement_score": self._calculate_twitter_engagement(tweet)
            })
        
        return processed
    
    def _process_tiktok_data(self, videos: List[Dict]) -> List[Dict[str, Any]]:
        """Process raw TikTok data"""
        
        processed = []
        for video in videos:
            processed.append({
                "platform": "tiktok",
                "id": video.get("id", ""),
                "text": video.get("text", ""),
                "author": video.get("authorMeta", {}).get("name", "unknown"),
                "likes": video.get("diggCount", 0),
                "shares": video.get("shareCount", 0),
                "comments": video.get("commentCount", 0),
                "views": video.get("playCount", 0),
                "created_at": video.get("createTime", ""),
                "url": video.get("webVideoUrl", ""),
                "engagement_score": self._calculate_tiktok_engagement(video)
            })
        
        return processed
    
    def _process_instagram_data(self, posts: List[Dict]) -> List[Dict[str, Any]]:
        """Process raw Instagram data"""
        
        processed = []
        for post in posts:
            processed.append({
                "platform": "instagram",
                "id": post.get("id", ""),
                "text": post.get("caption", ""),
                "author": post.get("ownerUsername", "unknown"),
                "likes": post.get("likesCount", 0),
                "comments": post.get("commentsCount", 0),
                "created_at": post.get("timestamp", ""),
                "url": post.get("url", ""),
                "engagement_score": self._calculate_instagram_engagement(post)
            })
        
        return processed
    
    def _calculate_twitter_engagement(self, tweet: Dict) -> float:
        """Calculate Twitter engagement score"""
        likes = tweet.get("likeCount", 0)
        retweets = tweet.get("retweetCount", 0)
        replies = tweet.get("replyCount", 0)
        
        # Simple engagement calculation
        total_engagement = likes + (retweets * 2) + (replies * 3)
        return min(total_engagement / 100.0, 100.0)  # Normalize to 0-100
    
    def _calculate_tiktok_engagement(self, video: Dict) -> float:
        """Calculate TikTok engagement score"""
        likes = video.get("diggCount", 0)
        shares = video.get("shareCount", 0)
        comments = video.get("commentCount", 0)
        views = video.get("playCount", 1)  # Avoid division by zero
        
        # Engagement rate calculation
        total_engagement = likes + (shares * 2) + (comments * 3)
        engagement_rate = (total_engagement / views) * 100
        return min(engagement_rate, 100.0)
    
    def _calculate_instagram_engagement(self, post: Dict) -> float:
        """Calculate Instagram engagement score"""
        likes = post.get("likesCount", 0)
        comments = post.get("commentsCount", 0)
        
        # Simple engagement calculation
        total_engagement = likes + (comments * 5)
        return min(total_engagement / 50.0, 100.0)  # Normalize to 0-100
    
    def format_scraper_results(self, results: Dict[str, List[Dict[str, Any]]]) -> str:
        """Format scraper results for display"""
        
        if not results:
            return "No data found from scrapers."
        
        formatted = "📊 **Real-Time Social Media Data:**\n\n"
        
        for platform, data in results.items():
            if data:
                formatted += f"### 🔥 {platform.title()} Results ({len(data)} items)\n\n"
                
                for i, item in enumerate(data[:3], 1):  # Show top 3
                    formatted += f"**{i}. @{item['author']}**\n"
                    formatted += f"📝 {item['text'][:100]}{'...' if len(item['text']) > 100 else ''}\n"
                    formatted += f"📊 Engagement: {item['engagement_score']:.1f}%"
                    
                    if platform == "twitter":
                        formatted += f" | ❤️ {item['likes']} | 🔄 {item['retweets']}\n"
                    elif platform == "tiktok":
                        formatted += f" | ❤️ {item['likes']} | 👁️ {item['views']}\n"
                    elif platform == "instagram":
                        formatted += f" | ❤️ {item['likes']} | 💬 {item['comments']}\n"
                    
                    formatted += "\n"
                
                formatted += "---\n\n"
        
        return formatted
    
    async def get_trending_content(self, topic: str, platforms: List[str] = None) -> str:
        """Get trending content for a specific topic"""
        
        results = await self.scrape_multi_platform(topic, platforms)
        return self.format_scraper_results(results)