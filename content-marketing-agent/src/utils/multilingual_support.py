from typing import Dict, List, Optional, Tuple
from deep_translator import GoogleTranslator
from langdetect import detect
import re
import json


class MultilingualContentManager:
    """Manages multilingual content creation and cultural adaptation"""
    
    def __init__(self):
        self.cultural_adaptations = self._load_cultural_adaptations()
        self.language_codes = {
            "english": "en",
            "french": "fr",
            "en": "en",
            "fr": "fr"
        }
    
    def _load_cultural_adaptations(self) -> Dict:
        """Load cultural adaptation rules and preferences"""
        return {
            "cameroon": {
                "greetings": {
                    "en": ["Hello", "Good morning", "Good evening", "How are you?"],
                    "fr": ["Bonjour", "Bonsoir", "Comment allez-vous?", "Salut"]
                },
                "cultural_values": [
                    "community", "respect for elders", "family", "education",
                    "hard work", "spirituality", "unity", "tradition"
                ],
                "communication_style": {
                    "en": "warm, respectful, community-focused",
                    "fr": "chaleureux, respectueux, axé sur la communauté"
                },
                "avoid_topics": [
                    "political controversies", "religious conflicts", 
                    "ethnic tensions", "colonial references"
                ],
                "preferred_examples": {
                    "en": [
                        "Like a village coming together to build a school",
                        "As our elders say",
                        "In our community",
                        "Building bridges, not walls"
                    ],
                    "fr": [
                        "Comme un village qui se rassemble pour construire une école",
                        "Comme disent nos anciens",
                        "Dans notre communauté",
                        "Construire des ponts, pas des murs"
                    ]
                },
                "hashtags": {
                    "en": ["#CameroonPride", "#AfricanWisdom", "#CommunityFirst", "#BilingualLife"],
                    "fr": ["#FiertéCamerounaise", "#SagesseAfricaine", "#CommunautéDAbord", "#VieBilingue"]
                }
            }
        }
    
    def detect_language(self, text: str) -> str:
        """Detect the language of given text"""
        try:
            detected = detect(text)
            return detected if detected in ["en", "fr"] else "en"
        except:
            return "en"  # Default to English
    
    def translate_content(
        self, 
        content: str, 
        target_language: str,
        source_language: Optional[str] = None
    ) -> str:
        """Translate content to target language"""
        
        if not source_language:
            source_language = self.detect_language(content)
        
        target_code = self.language_codes.get(target_language.lower(), target_language)
        source_code = self.language_codes.get(source_language.lower(), source_language)
        
        if source_code == target_code:
            return content
        
        try:
            translator = GoogleTranslator(source=source_code, target=target_code)
            translated = translator.translate(content)
            return translated
        except Exception as e:
            print(f"Translation error: {e}")
            return content
    
    def create_bilingual_content(
        self, 
        content: str, 
        primary_language: str = "en"
    ) -> Dict[str, str]:
        """Create bilingual version of content"""
        
        primary_code = self.language_codes.get(primary_language.lower(), primary_language)
        secondary_code = "fr" if primary_code == "en" else "en"
        
        # Translate to secondary language
        translated_content = self.translate_content(content, secondary_code, primary_code)
        
        return {
            primary_code: content,
            secondary_code: translated_content,
            "bilingual": f"{content}\n\n---\n\n{translated_content}"
        }
    
    def adapt_for_culture(
        self, 
        content: str, 
        cultural_context: str = "cameroon",
        language: str = "en"
    ) -> str:
        """Adapt content for specific cultural context"""
        
        if cultural_context not in self.cultural_adaptations:
            return content
        
        adaptations = self.cultural_adaptations[cultural_context]
        language_code = self.language_codes.get(language.lower(), language)
        
        adapted_content = content
        
        # Add cultural greetings if appropriate
        if self._should_add_greeting(content):
            greetings = adaptations["greetings"].get(language_code, [])
            if greetings:
                adapted_content = f"{greetings[0]}! {adapted_content}"
        
        # Replace generic examples with culturally relevant ones
        if "preferred_examples" in adaptations:
            examples = adaptations["preferred_examples"].get(language_code, [])
            adapted_content = self._replace_generic_examples(adapted_content, examples)
        
        # Add cultural hashtags
        if "hashtags" in adaptations:
            cultural_hashtags = adaptations["hashtags"].get(language_code, [])
            adapted_content = self._add_cultural_hashtags(adapted_content, cultural_hashtags)
        
        return adapted_content
    
    def _should_add_greeting(self, content: str) -> bool:
        """Determine if content should include a cultural greeting"""
        greeting_indicators = [
            "welcome", "hello", "hi there", "good morning", "good evening",
            "bienvenue", "bonjour", "bonsoir", "salut"
        ]
        content_lower = content.lower()
        return not any(indicator in content_lower for indicator in greeting_indicators)
    
    def _replace_generic_examples(self, content: str, cultural_examples: List[str]) -> str:
        """Replace generic examples with culturally relevant ones"""
        
        generic_patterns = [
            r"for example,?\s*[^.!?]*[.!?]",
            r"like\s+[^.!?]*[.!?]",
            r"imagine\s+[^.!?]*[.!?]",
            r"think about\s+[^.!?]*[.!?]"
        ]
        
        for pattern in generic_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                if cultural_examples:
                    replacement = f"For example, {cultural_examples[0]}."
                    content = content.replace(match.group(), replacement)
                    cultural_examples = cultural_examples[1:]  # Use next example for next replacement
                    if not cultural_examples:
                        break
        
        return content
    
    def _add_cultural_hashtags(self, content: str, cultural_hashtags: List[str]) -> str:
        """Add cultural hashtags to content"""
        
        # Extract existing hashtags
        existing_hashtags = re.findall(r'#\w+', content)
        
        # Add cultural hashtags that aren't already present
        new_hashtags = []
        for hashtag in cultural_hashtags[:2]:  # Add max 2 cultural hashtags
            if hashtag not in existing_hashtags:
                new_hashtags.append(hashtag)
        
        if new_hashtags:
            content += f" {' '.join(new_hashtags)}"
        
        return content
    
    def optimize_for_platform_language(
        self, 
        content: str, 
        platform: str, 
        target_language: str,
        cultural_context: str = "cameroon"
    ) -> str:
        """Optimize content for specific platform and language combination"""
        
        # Platform-specific adaptations
        platform_adaptations = {
            "tiktok": {
                "en": {
                    "style": "casual, energetic, trending",
                    "length": "short and punchy",
                    "call_to_action": ["Drop a comment!", "Share if you agree!", "Follow for more!"]
                },
                "fr": {
                    "style": "décontracté, énergique, tendance",
                    "length": "court et percutant",
                    "call_to_action": ["Laisse un commentaire!", "Partage si tu es d'accord!", "Abonne-toi pour plus!"]
                }
            },
            "linkedin": {
                "en": {
                    "style": "professional, insightful, thought-provoking",
                    "length": "detailed but scannable",
                    "call_to_action": ["What's your experience?", "Share your thoughts", "Connect with me"]
                },
                "fr": {
                    "style": "professionnel, perspicace, stimulant",
                    "length": "détaillé mais lisible",
                    "call_to_action": ["Quelle est votre expérience?", "Partagez vos pensées", "Connectez-vous avec moi"]
                }
            },
            "instagram": {
                "en": {
                    "style": "visual, inspiring, authentic",
                    "length": "engaging with line breaks",
                    "call_to_action": ["Double tap if you agree!", "Save this post!", "Tag a friend!"]
                },
                "fr": {
                    "style": "visuel, inspirant, authentique",
                    "length": "engageant avec des sauts de ligne",
                    "call_to_action": ["Double-clic si tu es d'accord!", "Sauvegarde ce post!", "Tague un ami!"]
                }
            }
        }
        
        # Get platform-specific settings
        platform_settings = platform_adaptations.get(platform.lower(), {})
        language_settings = platform_settings.get(target_language, {})
        
        # Adapt content style
        adapted_content = content
        
        # Add platform-appropriate call-to-action
        if "call_to_action" in language_settings:
            cta_options = language_settings["call_to_action"]
            adapted_content += f"\n\n{cta_options[0]}"
        
        # Apply cultural adaptations
        adapted_content = self.adapt_for_culture(
            adapted_content, 
            cultural_context, 
            target_language
        )
        
        return adapted_content
    
    def generate_multilingual_hashtags(
        self, 
        topic: str, 
        cultural_context: str = "cameroon",
        max_hashtags: int = 10
    ) -> Dict[str, List[str]]:
        """Generate relevant hashtags in multiple languages"""
        
        # Base hashtags related to topic
        base_hashtags_en = self._generate_topic_hashtags(topic, "en")
        base_hashtags_fr = self._generate_topic_hashtags(topic, "fr")
        
        # Cultural hashtags
        cultural_hashtags = self.cultural_adaptations.get(cultural_context, {}).get("hashtags", {})
        
        # Combine and limit
        en_hashtags = (base_hashtags_en + cultural_hashtags.get("en", []))[:max_hashtags]
        fr_hashtags = (base_hashtags_fr + cultural_hashtags.get("fr", []))[:max_hashtags]
        
        return {
            "en": en_hashtags,
            "fr": fr_hashtags,
            "bilingual": en_hashtags[:5] + fr_hashtags[:5]
        }
    
    def _generate_topic_hashtags(self, topic: str, language: str) -> List[str]:
        """Generate hashtags based on topic and language"""
        
        # Simple hashtag generation based on topic keywords
        words = topic.lower().split()
        hashtags = []
        
        # Single word hashtags
        for word in words:
            if len(word) > 3:  # Skip short words
                hashtags.append(f"#{word.capitalize()}")
        
        # Combined hashtags
        if len(words) >= 2:
            combined = "".join([w.capitalize() for w in words[:3]])
            hashtags.append(f"#{combined}")
        
        # Language-specific common hashtags
        common_hashtags = {
            "en": ["#Motivation", "#Success", "#Growth", "#Inspiration", "#Tips"],
            "fr": ["#Motivation", "#Succès", "#Croissance", "#Inspiration", "#Conseils"]
        }
        
        hashtags.extend(common_hashtags.get(language, [])[:3])
        
        return hashtags[:8]  # Limit to 8 hashtags
    
    def validate_cultural_sensitivity(
        self, 
        content: str, 
        cultural_context: str = "cameroon"
    ) -> Dict[str, any]:
        """Validate content for cultural sensitivity"""
        
        if cultural_context not in self.cultural_adaptations:
            return {"is_sensitive": True, "warnings": [], "suggestions": []}
        
        adaptations = self.cultural_adaptations[cultural_context]
        avoid_topics = adaptations.get("avoid_topics", [])
        
        warnings = []
        suggestions = []
        
        content_lower = content.lower()
        
        # Check for topics to avoid
        for topic in avoid_topics:
            if topic in content_lower:
                warnings.append(f"Content mentions '{topic}' which may be culturally sensitive")
                suggestions.append(f"Consider reframing discussion of '{topic}' in a more neutral way")
        
        # Check for cultural values alignment
        cultural_values = adaptations.get("cultural_values", [])
        values_mentioned = sum(1 for value in cultural_values if value in content_lower)
        
        if values_mentioned == 0:
            suggestions.append("Consider incorporating cultural values like community, respect, or family")
        
        is_sensitive = len(warnings) == 0
        
        return {
            "is_sensitive": is_sensitive,
            "warnings": warnings,
            "suggestions": suggestions,
            "cultural_values_score": values_mentioned / len(cultural_values) * 10 if cultural_values else 5
        }


# Example usage
def main():
    """Example usage of multilingual content manager"""
    
    manager = MultilingualContentManager()
    
    # Example content
    content = "Here are 5 tips for building a successful business. First, focus on your customers."
    
    # Create bilingual version
    bilingual = manager.create_bilingual_content(content, "en")
    print("Bilingual Content:")
    print(bilingual["bilingual"])
    print("\n" + "="*50 + "\n")
    
    # Adapt for culture
    adapted = manager.adapt_for_culture(content, "cameroon", "en")
    print("Culturally Adapted Content:")
    print(adapted)
    print("\n" + "="*50 + "\n")
    
    # Generate hashtags
    hashtags = manager.generate_multilingual_hashtags("business success", "cameroon")
    print("Multilingual Hashtags:")
    print(json.dumps(hashtags, indent=2))
    print("\n" + "="*50 + "\n")
    
    # Validate cultural sensitivity
    validation = manager.validate_cultural_sensitivity(content, "cameroon")
    print("Cultural Sensitivity Check:")
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()