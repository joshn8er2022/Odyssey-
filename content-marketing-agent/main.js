/**
 * Content Marketing Agent - Apify Actor
 * This actor provides AI-powered content marketing assistance with real trend analysis
 */

import { Actor } from 'apify';
import { spawn } from 'child_process';
import { promisify } from 'util';
import fs from 'fs';
import path from 'path';

const execAsync = promisify(spawn);

await Actor.init();

try {
    console.log('🚀 Starting Content Marketing Agent...');
    
    // Get input from Apify
    const input = await Actor.getInput() || {};
    console.log('📝 Input received:', JSON.stringify(input, null, 2));
    
    // Default input if none provided
    const {
        user_interests = ['business', 'personal development'],
        expertise_areas = ['life coaching', 'business coaching'],
        cultural_context = 'cameroon',
        content_type = 'educational',
        platform = 'instagram',
        language = 'en'
    } = input;
    
    console.log('🔧 Processing with parameters:');
    console.log(`   - User interests: ${user_interests.join(', ')}`);
    console.log(`   - Expertise areas: ${expertise_areas.join(', ')}`);
    console.log(`   - Cultural context: ${cultural_context}`);
    console.log(`   - Content type: ${content_type}`);
    console.log(`   - Platform: ${platform}`);
    console.log(`   - Language: ${language}`);
    
    // Install Python dependencies if needed
    console.log('📦 Installing Python dependencies...');
    try {
        const installProcess = spawn('pip', ['install', '-r', 'requirements.txt'], {
            stdio: 'inherit'
        });
        
        await new Promise((resolve, reject) => {
            installProcess.on('close', (code) => {
                if (code === 0) {
                    console.log('✅ Dependencies installed successfully');
                    resolve();
                } else {
                    console.log('⚠️ Some dependencies may have failed to install, continuing...');
                    resolve(); // Continue anyway
                }
            });
            installProcess.on('error', (error) => {
                console.log('⚠️ Dependency installation error:', error.message);
                resolve(); // Continue anyway
            });
        });
    } catch (error) {
        console.log('⚠️ Dependency installation failed, continuing with available packages...');
    }
    
    // Run the Python content marketing agent
    console.log('🤖 Running Content Marketing Agent...');
    
    const pythonScript = `
import sys
import os
import json
import asyncio
from datetime import datetime

# Add src to path
sys.path.insert(0, 'src')

async def run_content_agent():
    try:
        # Import our modules
        from agents.dspy_agent import DSPyContentAgent
        from api.apify_integration import ApifyTrendAnalyzer
        
        print("✅ Modules imported successfully")
        
        # Create user profile
        profile = {
            'name': 'Content Creator',
            'brand_name': 'AI Content Brand',
            'expertise_areas': ${JSON.stringify(expertise_areas)},
            'cultural_background': '${cultural_context}',
            'primary_language': '${language}',
            'active_platforms': ['${platform}']
        }
        
        print("👤 Profile created:", json.dumps(profile, indent=2))
        
        # Initialize agent
        agent = DSPyContentAgent()
        print("🤖 DSPy agent initialized")
        
        # Analyze trends
        print("📈 Analyzing trends...")
        analyzer = ApifyTrendAnalyzer()
        trends = await analyzer.comprehensive_trend_analysis(
            user_interests=${JSON.stringify(user_interests)},
            expertise_areas=${JSON.stringify(expertise_areas)},
            cultural_context='${cultural_context}'
        )
        
        print(f"✅ Found {len(trends.get('trending_topics', []))} trending topics")
        
        # Generate content
        print("✍️ Generating content...")
        content = await agent.generate_content_with_trends(
            profile, '${platform}', '${content_type}', '${language}'
        )
        
        print("✅ Content generated successfully")
        
        # Prepare results
        results = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'profile': profile,
            'trends': trends,
            'generated_content': content,
            'summary': {
                'trending_topics_count': len(trends.get('trending_topics', [])),
                'content_length': len(content.get('content_text', '')),
                'hashtags_count': len(content.get('hashtags', [])),
                'data_source': trends.get('data_source', 'unknown')
            }
        }
        
        return results
        
    except Exception as e:
        print(f"❌ Error in content agent: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat(),
            'fallback_content': {
                'content_text': f"🎯 {expertise_areas[0] if expertise_areas else 'Success'} Tips\\n\\nAs an expert, here's what I've learned:\\n\\n✨ Focus on progress, not perfection\\n✨ Consistency beats intensity\\n✨ Your mindset shapes your reality\\n\\nWhat's your biggest challenge right now? 👇",
                'hashtags': ['#Success', '#Motivation', '#PersonalDevelopment'],
                'call_to_action': 'Share your thoughts in the comments!'
            }
        }

# Run the async function
if __name__ == "__main__":
    result = asyncio.run(run_content_agent())
    print("📊 FINAL RESULT:")
    print(json.dumps(result, indent=2, default=str))
`;
    
    // Write and execute Python script
    fs.writeFileSync('run_agent.py', pythonScript);
    
    const pythonProcess = spawn('python3', ['run_agent.py'], {
        stdio: ['pipe', 'pipe', 'pipe']
    });
    
    let output = '';
    let error = '';
    
    pythonProcess.stdout.on('data', (data) => {
        const text = data.toString();
        console.log(text);
        output += text;
    });
    
    pythonProcess.stderr.on('data', (data) => {
        const text = data.toString();
        console.error(text);
        error += text;
    });
    
    const exitCode = await new Promise((resolve) => {
        pythonProcess.on('close', resolve);
    });
    
    console.log(`🏁 Python process finished with exit code: ${exitCode}`);
    
    // Parse results from Python output
    let results;
    try {
        // Extract JSON from output
        const jsonMatch = output.match(/📊 FINAL RESULT:\s*(\{[\s\S]*\})/);
        if (jsonMatch) {
            results = JSON.parse(jsonMatch[1]);
        } else {
            throw new Error('No JSON result found in output');
        }
    } catch (parseError) {
        console.log('⚠️ Could not parse Python results, creating fallback...');
        results = {
            success: false,
            error: 'Failed to parse results',
            timestamp: new Date().toISOString(),
            raw_output: output,
            raw_error: error,
            fallback_content: {
                content_text: `🎯 ${expertise_areas[0] || 'Success'} Tips\\n\\nAs an expert, here's what I've learned:\\n\\n✨ Focus on progress, not perfection\\n✨ Consistency beats intensity\\n✨ Your mindset shapes your reality\\n\\nWhat's your biggest challenge right now? 👇`,
                hashtags: ['#Success', '#Motivation', '#PersonalDevelopment'],
                call_to_action: 'Share your thoughts in the comments!'
            }
        };
    }
    
    // Save results to Apify dataset
    console.log('💾 Saving results to dataset...');
    await Actor.pushData(results);
    
    console.log('✅ Content Marketing Agent completed successfully!');
    console.log('📊 Results summary:');
    console.log(`   - Success: ${results.success}`);
    console.log(`   - Trending topics: ${results.summary?.trending_topics_count || 0}`);
    console.log(`   - Content generated: ${results.generated_content ? 'Yes' : 'No'}`);
    
} catch (error) {
    console.error('❌ Actor failed:', error);
    
    // Save error info to dataset
    await Actor.pushData({
        success: false,
        error: error.message,
        timestamp: new Date().toISOString(),
        stack: error.stack
    });
    
    throw error;
}

await Actor.exit();