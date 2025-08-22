#!/usr/bin/env python3
"""
Test script for modern UI components
Run this to verify the enhanced frontend works correctly
"""

import streamlit as st
import sys
from pathlib import Path

# Add components to path
components_path = Path(__file__).parent / "components"
sys.path.insert(0, str(components_path))

from modern_ui import (
    render_modern_hero, render_modern_card, render_modern_stats,
    render_modern_chat_interface, render_modern_feature_grid,
    render_modern_form, render_modern_alert, add_modern_css
)

def main():
    st.set_page_config(
        page_title="Modern UI Test",
        page_icon="🎨",
        layout="wide"
    )
    
    # Add modern CSS
    add_modern_css()
    
    st.title("🎨 Modern UI Components Test")
    
    # Test Hero Component
    st.markdown("## Hero Component")
    render_modern_hero(
        title="Welcome to Modern UI",
        subtitle="Testing beautiful components inspired by 21st.dev",
        gradient_colors=["#667eea", "#764ba2"]
    )
    
    # Test Alert Components
    st.markdown("## Alert Components")
    render_modern_alert("This is an info alert", "info")
    render_modern_alert("This is a success alert", "success")
    render_modern_alert("This is a warning alert", "warning")
    render_modern_alert("This is an error alert", "error")
    
    # Test Stats Component
    st.markdown("## Stats Component")
    stats = [
        {"value": "150+", "label": "Components", "description": "Available UI elements", "color": "#667eea"},
        {"value": "98%", "label": "Satisfaction", "description": "User happiness rate", "color": "#764ba2"},
        {"value": "24/7", "label": "Support", "description": "Always available", "color": "#f093fb"}
    ]
    render_modern_stats(stats, "Test Statistics")
    
    # Test Card Components
    st.markdown("## Card Components")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_modern_card(
            title="Modern Design",
            content="Beautiful, responsive components with smooth animations and modern styling",
            icon="🎨",
            accent_color="#667eea",
            action_text="Learn More"
        )
    
    with col2:
        render_modern_card(
            title="Easy Integration",
            content="Simple to use components that integrate seamlessly with Streamlit applications",
            icon="🔧",
            accent_color="#764ba2",
            action_text="Get Started"
        )
    
    with col3:
        render_modern_card(
            title="Responsive",
            content="Mobile-first design that looks great on all devices and screen sizes",
            icon="📱",
            accent_color="#f093fb",
            action_text="View Demo"
        )
    
    # Test Feature Grid
    st.markdown("## Feature Grid Component")
    features = [
        {
            "title": "Modern Styling",
            "description": "Clean, modern design with beautiful gradients and animations",
            "icon": "✨",
            "color": "#667eea"
        },
        {
            "title": "Responsive Layout",
            "description": "Adapts perfectly to different screen sizes and devices",
            "icon": "📱",
            "color": "#764ba2"
        },
        {
            "title": "Easy to Use",
            "description": "Simple API that makes creating beautiful UIs effortless",
            "icon": "🚀",
            "color": "#f093fb"
        }
    ]
    render_modern_feature_grid(features, "Key Features")
    
    # Test Form Component
    st.markdown("## Form Component")
    form_config = {
        "title": "Test Form",
        "description": "This is a test form to demonstrate the modern form component",
        "fields": [
            {
                "name": "name",
                "label": "Your Name",
                "type": "text",
                "placeholder": "Enter your name",
                "help": "This is a text input field"
            },
            {
                "name": "email",
                "label": "Email Address",
                "type": "text",
                "placeholder": "your@email.com",
                "help": "We'll never share your email"
            },
            {
                "name": "category",
                "label": "Category",
                "type": "select",
                "options": ["Option 1", "Option 2", "Option 3"],
                "help": "Choose a category"
            },
            {
                "name": "message",
                "label": "Message",
                "type": "textarea",
                "placeholder": "Enter your message here...",
                "help": "Tell us what you think"
            }
        ],
        "submit_text": "Submit Test Form"
    }
    
    form_data, submitted = render_modern_form(form_config, "test_form")
    
    if submitted:
        st.success("Form submitted successfully!")
        st.json(form_data)
    
    # Test Chat Interface
    st.markdown("## Chat Interface Component")
    
    # Initialize chat history for demo
    if 'demo_chat' not in st.session_state:
        st.session_state.demo_chat = [
            {"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today?"},
            {"role": "user", "content": "Can you help me create some content?"},
            {"role": "assistant", "content": "Absolutely! I'd be happy to help you create engaging content. What type of content are you looking to create and for which platform?"}
        ]
    
    user_input, send_button = render_modern_chat_interface(
        st.session_state.demo_chat,
        "demo_chat_input"
    )
    
    if send_button and user_input:
        st.session_state.demo_chat.append({"role": "user", "content": user_input})
        st.session_state.demo_chat.append({"role": "assistant", "content": f"Thanks for your message: '{user_input}'. This is a demo response!"})
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 🎉 All components are working correctly!")

if __name__ == "__main__":
    main()