#!/usr/bin/env python3
"""
Quick test to verify modern UI components render correctly
"""

import streamlit as st
import sys
from pathlib import Path

# Add components to path
components_path = Path(__file__).parent / "components"
sys.path.insert(0, str(components_path))

from modern_ui import (
    render_modern_hero, render_modern_card, render_modern_stats,
    render_modern_feature_grid, render_modern_alert, add_modern_css
)

def main():
    st.set_page_config(
        page_title="Component Fix Test",
        page_icon="🔧",
        layout="wide"
    )
    
    # Add modern CSS
    add_modern_css()
    
    st.title("🔧 Component Rendering Test")
    
    # Test Hero Component
    render_modern_hero(
        title="Component Test",
        subtitle="Testing if all components render properly without showing raw HTML",
        gradient_colors=["#667eea", "#764ba2"]
    )
    
    # Test individual cards
    st.markdown("## Individual Cards Test")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_modern_card(
            title="Test Card 1",
            content="This should show as a beautiful card, not raw HTML code",
            icon="🎯",
            accent_color="#667eea"
        )
    
    with col2:
        render_modern_card(
            title="Test Card 2", 
            content="Another test card to verify proper rendering",
            icon="🚀",
            accent_color="#764ba2"
        )
    
    with col3:
        render_modern_card(
            title="Test Card 3",
            content="Final test card with different styling",
            icon="✨",
            accent_color="#f093fb"
        )
    
    # Test Feature Grid
    st.markdown("## Feature Grid Test")
    
    features = [
        {
            "title": "Feature 1",
            "description": "This should render as a proper card in the grid",
            "icon": "🎨",
            "color": "#667eea"
        },
        {
            "title": "Feature 2", 
            "description": "Another feature card that should display correctly",
            "icon": "🔧",
            "color": "#764ba2"
        },
        {
            "title": "Feature 3",
            "description": "Third feature to test grid layout",
            "icon": "📱",
            "color": "#f093fb"
        }
    ]
    
    render_modern_feature_grid(features, "Test Features")
    
    # Test Stats
    st.markdown("## Stats Test")
    
    stats = [
        {"value": "100%", "label": "Working", "description": "Components functional", "color": "#667eea"},
        {"value": "0", "label": "HTML Errors", "description": "No raw HTML showing", "color": "#43e97b"}
    ]
    
    render_modern_stats(stats, "Component Status")
    
    # Test Alerts
    st.markdown("## Alerts Test")
    
    render_modern_alert("✅ If you see this as a styled alert (not raw HTML), the fix worked!", "success")
    render_modern_alert("⚠️ This should be a warning alert with proper styling", "warning")
    
    st.markdown("---")
    st.markdown("### 🎉 If all components above show as styled elements (not raw HTML), the fix is successful!")

if __name__ == "__main__":
    main()