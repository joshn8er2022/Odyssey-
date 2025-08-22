# 🎯 Content Marketing Agent

An intelligent content marketing assistant designed specifically for a 60-year-old Cameroonian content creator who speaks English and French. This AI-powered tool specializes in trend-aware, culturally-relevant content creation and automated social media management.

## ✨ Features

### 🧠 Core AI Capabilities
- **Trend Analysis**: Real-time analysis of social media trends across platforms
- **Content Strategy**: AI-generated personalized content strategies
- **Multilingual Content**: Seamless English/French content creation
- **Cultural Adaptation**: Cameroon-specific cultural context and sensitivity
- **Lead Management**: Automated lead magnet distribution and qualification

### 📱 Platform Support
- TikTok
- Instagram
- YouTube
- LinkedIn
- Facebook
- Twitter

### 🌍 Multilingual & Cultural Features
- **Bilingual Content Creation**: English and French content generation
- **Cultural Sensitivity**: Cameroon-specific cultural adaptations
- **Localized Hashtags**: Platform and culture-specific hashtag recommendations
- **Regional Optimization**: Content optimized for African diaspora audiences

### 🚀 Automation Features
- **Daily Workflow**: Automated daily content creation pipeline
- **Trend Integration**: Automatic incorporation of relevant trending topics
- **Lead Qualification**: AI-powered comment monitoring and lead scoring
- **Performance Optimization**: Content performance analysis and suggestions

## 🛠️ Installation

### Prerequisites
- Python 3.9 or higher
- OpenAI API key (for GPT models)
- Social media API keys (optional, for enhanced trend analysis)

### Setup

1. **Clone the repository:**
```bash
git clone <repository-url>
cd content-marketing-agent
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. **Run the application:**
```bash
streamlit run src/main.py
```

## 🎯 Quick Start

### 1. Initial Setup
1. Launch the application
2. Complete the comprehensive intake form:
   - Personal and brand information
   - Target audience demographics
   - Business goals and offerings
   - Content preferences
   - Lead generation setup

### 2. Daily Workflow
1. **Trend Analysis**: Click "Analyze Trends" to get current relevant trends
2. **Content Creation**: Use "Daily Content Workflow" for automated content generation
3. **Review & Edit**: Review generated content and make adjustments
4. **Schedule & Post**: Copy content to your preferred scheduling tools

### 3. Lead Management
1. Set up lead magnets in your profile
2. Use the comment monitoring simulation
3. Test lead magnet matching with sample comments

## 📊 User Interface

### Dashboard Overview
- **Metrics**: Active platforms, content pieces, lead magnets
- **Quick Actions**: Daily workflow, trend analysis, content creation
- **Recent Content**: Preview of recently created content

### Trend Analysis
- **Current Trends**: Relevant trending topics across platforms
- **Content Opportunities**: Specific content ideas with engagement potential
- **Optimal Timing**: Best posting times for your audience

### Content Creation Studio
- **Single Content**: Create individual content pieces
- **Batch Creation**: Generate content for all active platforms
- **Multilingual Options**: English, French, or bilingual content
- **Cultural Adaptation**: Automatic cultural sensitivity adjustments

### Lead Management
- **Lead Magnets**: Manage your lead magnet library
- **Comment Monitoring**: AI-powered comment analysis (coming soon)
- **Response Generation**: Automated personalized responses

## 🔧 Configuration

### API Keys Required
```env
# Core AI
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key (optional)

# Social Media APIs (optional, for enhanced trend analysis)
TWITTER_API_KEY=your_twitter_key
TWITTER_API_SECRET=your_twitter_secret
YOUTUBE_API_KEY=your_youtube_key

# Database
DATABASE_URL=sqlite:///./content_marketing.db
```

### Customization Options
- **Cultural Context**: Modify cultural adaptations in `src/utils/multilingual_support.py`
- **Platform Specifications**: Adjust platform requirements in `src/agents/content_marketing_agent.py`
- **Trend Sources**: Add new trend analysis sources in `src/api/trend_analyzer.py`

## 🏗️ Architecture

### Core Components

1. **DSPy Signatures** (`src/agents/signatures.py`)
   - TrendAnalyzer: Analyzes social media trends
   - ContentStrategist: Generates content strategies
   - ContentCreator: Creates video scripts and text content
   - LeadMagnetManager: Manages lead distribution
   - CulturalContextAnalyzer: Ensures cultural sensitivity

2. **Content Marketing Agent** (`src/agents/content_marketing_agent.py`)
   - Main orchestrator for all AI operations
   - Coordinates trend analysis, strategy, and content creation

3. **User Profile Management** (`src/models/user_profile.py`)
   - Comprehensive user profile data models
   - Content piece tracking and management

4. **Trend Analysis** (`src/api/trend_analyzer.py`)
   - Multi-platform trend analysis
   - Relevance scoring and opportunity identification

5. **Multilingual Support** (`src/utils/multilingual_support.py`)
   - Translation and cultural adaptation
   - Platform-specific language optimization

6. **Web Interface** (`src/ui/intake_form.py`, `src/main.py`)
   - Streamlit-based user interface
   - Interactive forms and dashboards

### Data Flow
1. **User Setup**: Complete intake form → Create user profile
2. **Trend Analysis**: Analyze social media trends → Score relevance → Identify opportunities
3. **Content Strategy**: Generate strategy based on trends and user profile
4. **Content Creation**: Create platform-specific content → Apply cultural adaptations
5. **Lead Management**: Monitor engagement → Match lead magnets → Generate responses

## 🎨 Customization for Different Users

### For Other Cultural Contexts
1. **Update Cultural Adaptations**: Modify `src/utils/multilingual_support.py`
2. **Add New Languages**: Extend language support in models and translation
3. **Regional Hashtags**: Add region-specific hashtag libraries

### For Different Industries
1. **Expertise Areas**: Update options in intake form
2. **Content Pillars**: Add industry-specific content themes
3. **Platform Priorities**: Adjust platform recommendations

### For Different Age Groups
1. **Platform Focus**: Modify platform recommendations
2. **Content Style**: Adjust tone and approach in DSPy signatures
3. **Trend Sources**: Update trend analysis sources

## 🚀 Advanced Features

### Batch Operations
- Generate content for multiple platforms simultaneously
- Bulk cultural adaptation and translation
- Automated scheduling recommendations

### Performance Analytics
- Content performance tracking (coming soon)
- Engagement rate analysis
- Cultural relevance scoring

### Integration Capabilities
- Social media scheduling tools
- CRM systems for lead management
- Analytics platforms for performance tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup
```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/
flake8 src/
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, please:
1. Check the documentation
2. Search existing issues
3. Create a new issue with detailed information

## 🔮 Roadmap

### Phase 1 (Current)
- ✅ Core AI agent implementation
- ✅ Multilingual content creation
- ✅ Cultural adaptation
- ✅ Web interface

### Phase 2 (Coming Soon)
- 🔄 Real-time social media posting
- 🔄 Advanced analytics dashboard
- 🔄 Comment monitoring automation
- 🔄 Performance optimization AI

### Phase 3 (Future)
- 📅 Video editing automation
- 📅 Voice-over generation
- 📅 Advanced lead scoring
- 📅 Multi-user collaboration

## 🙏 Acknowledgments

- Built with [DSPy](https://github.com/stanfordnlp/dspy) for AI orchestration
- [Streamlit](https://streamlit.io/) for the web interface
- [OpenAI](https://openai.com/) for language model capabilities
- Designed specifically for Cameroonian content creators and the African diaspora

---

*Made with ❤️ for content creators who want to bridge cultures and languages through authentic, AI-enhanced storytelling.*