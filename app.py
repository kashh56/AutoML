import streamlit as st
import sys
import os
import pandas as pd
import time

# Streamlit page setup
st.set_page_config(
    page_title="AutoML",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"Get Help": None, "Report a bug": None, "About": None},
)

# Add project root and src to Python path
sys.path.extend([
    os.path.dirname(os.path.abspath(__file__)),  # Project root
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "src") 
])

# Import loading FIRST before any components
from src.ui.loading import show_loading_state
# Import CSS loader FIRST
from src.ui.css import load_css

# Load CSS immediately after imports
load_css()

# Cached resource loading with TTL to refresh components periodically
@st.cache_resource(ttl=3600)  # Cache for 1 hour
def load_components():
    """Cache component imports to avoid reloading on every rerun"""
    from src import (
        show_footer,
        visualize_data,
        show_welcome_page,
        show_overview_page,
        clean_csv,
        model_training_tab,
        display_ai_insights,
        display_model_evaluation
    )
    return (show_footer, visualize_data,
            show_welcome_page, show_overview_page, clean_csv,
            model_training_tab, display_ai_insights, display_model_evaluation)

# Cached header rendering
@st.cache_data(ttl=86400)  # Cache for 24 hours
def render_header():
    """Cache static header HTML"""
    return """
    <div class='app-header' style='padding: 1rem 0; margin-bottom: 2rem; text-align: center;'>
        <h1 class='app-title' style='margin: 0;'>AutoML</h1>
        <p class='app-tagline' style='margin-top: 0;'>Automated Machine Learning Made Simple.</p>
    </div>
    """

# Cached data loading
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_default_data():
    """Load and cache the default dataset"""
    try:
        return pd.read_csv("laptop_data.csv")
    except Exception as e:
        st.error(f"❌ Error loading default dataset: {str(e)}")
        return None

# Performance monitoring decorator
def measure_time(func):
    """Decorator to measure execution time of functions"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        if execution_time > 1.0:  # Only log slow operations
            print(f"⏱️ {func.__name__} took {execution_time:.2f} seconds to execute")
        return result
    return wrapper

@measure_time
def main():
    """Optimized main function for Streamlit AutoML app"""
    # First show loading screen before anything else
    if "initialized" not in st.session_state:
        # Show loading animation in full screen mode
        with st.container():
            show_loading_state()
            
            # Force render loading screen first
            st.empty().markdown("<style>#root > div:nth-child(1) > div > div > div > div > section > div {padding: 0rem;}</style>", unsafe_allow_html=True)
            
            # Now load components in background
            components = load_components()
            (show_footer, visualize_data,
             show_welcome_page, show_overview_page, clean_csv,
             model_training_tab, display_ai_insights, display_model_evaluation) = components
            
            try:
                # Load and clean data with caching
                default_df = load_default_data()
                if default_df is not None:
                    cleaned_df, insights = clean_csv(default_df)
                    
                    # Store everything in session state
                    st.session_state.update({
                        "df": cleaned_df,
                        "insights": insights,
                        "components": components,
                        "initialized": True,
                        "current_tab_index": 0  # Use consistent naming for tab tracking
                    })
                    
                    # Rerun to hide loading screen
                    st.rerun()
                else:
                    st.error("❌ Failed to load default dataset")
                    return
                
            except Exception as e:
                st.error(f"❌ Error during initialization: {str(e)}")
                return

    # After initialization, show main interface
    if "initialized" in st.session_state:
        components = st.session_state.components
        (show_footer, visualize_data,
         show_welcome_page, show_overview_page, clean_csv,
         model_training_tab, display_ai_insights, display_model_evaluation) = components
        
        # Render main interface
        st.markdown(render_header(), unsafe_allow_html=True)
        
        # Create tabs with tab names as constants to avoid recreation
        TAB_NAMES = ["👋 Welcome", "📊 Overview", "📈 Visualization", 
                    "🤖 Model Training", "💡 Insights", "📊 Test Results"]
        
        # Initialize current tab index if not present
        if "current_tab_index" not in st.session_state:
            st.session_state.current_tab_index = 0
        
        # Create tabs and get the current tab index
        tab_index = st.tabs(TAB_NAMES)
        
        # Display content in all tabs
        with tab_index[0]: 
            show_welcome_page()
                
        with tab_index[1]: 
            show_overview_page()
                
        with tab_index[2]: 
            visualize_data(st.session_state.df)
                
        with tab_index[3]: 
            model_training_tab(st.session_state.df)
                
        with tab_index[4]: 
            display_ai_insights()
                
        with tab_index[5]: 
            display_model_evaluation()

        show_footer()

if __name__ == "__main__":
    main()
