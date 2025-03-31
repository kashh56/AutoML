import streamlit as st
from src.preprocessing.clean_data import cached_clean_csv
import pandas as pd
from functools import lru_cache

# Cache static content to avoid recomputation
@lru_cache(maxsize=1)
def get_static_content():
    """Cache static HTML content to avoid regeneration."""
    welcome_header = """
        <div class="welcome-header" style="text-align: left; margin-bottom: 2rem;">
            <h1>Experience Ai like never before</h1>
            <p class="subtitle">
                Performance, Analysis, Insights Made Simple. 
            </p>
        </div>
    """
    features_header = "## ✨ Key Features"
    feature_cards = [
        """
        <div class="feature-card">
            <h3>📊 Data Analysis</h3>
            <ul>
                <li>Automated data cleaning</li>
                <li>Interactive visualizations</li>
                <li>Statistical insights</li>
                <li>Correlation analysis</li>
            </ul>
        </div>
        """,
        """
        <div class="feature-card">
            <h3>🤖 Machine Learning</h3>
            <ul>
                <li>Multiple ML algorithms</li>
                <li>Automated model selection</li>
                <li>Hyperparameter tuning</li>
                <li>Performance metrics</li>
            </ul>
        </div>
        """,
        """
        <div class="feature-card">
            <h3>🔍 AI Insights</h3>
            <ul>
                <li>Data quality checks</li>
                <li>Feature importance</li>
                <li>Model explanations</li>
                <li>Smart recommendations</li>
            </ul>
        </div>
        """
    ]
    getting_started = """
    ## 🚀 Getting Started
    1. **Upload Your Dataset**: Use the sidebar to upload your CSV file
    2. **Explore Data**: View statistics and visualizations in the Overview tab
    3. **Train Models**: Select algorithms and tune parameters
    4. **Get Insights**: Receive AI-powered recommendations
    """
    dataset_requirements = """
    * File format: CSV
    * Maximum size: 200MB
    * Supported column types:
        * Numeric (int, float)
        * Categorical (string, boolean)
        * Temporal (date, datetime)
    * Clean data preferred, but not required
    """
    example_datasets = """
    Try these example datasets to explore the app:
    * [Iris Dataset](https://archive.ics.uci.edu/ml/datasets/iris)
    * [Boston Housing](https://www.kaggle.com/c/boston-housing)
    * [Wine Quality](https://archive.ics.uci.edu/ml/datasets/wine+quality)
    """
    return welcome_header, features_header, feature_cards, getting_started, dataset_requirements, example_datasets

def show_welcome_page():
    """Display welcome page with features and instructions efficiently."""
    # Load cached static content
    welcome_header, features_header, feature_cards, getting_started, dataset_requirements, example_datasets = get_static_content()

    # Render static content
    st.markdown(welcome_header, unsafe_allow_html=True)
    st.markdown(features_header, unsafe_allow_html=True)



    # Feature columns with minimal overhead
    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        st.markdown(feature_cards[0], unsafe_allow_html=True)
    with col2:
        st.markdown(feature_cards[1], unsafe_allow_html=True)
    with col3:
        st.markdown(feature_cards[2], unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)  # Spacing

    # Getting Started and Expanders
    st.markdown(getting_started, unsafe_allow_html=True)
    with st.expander("📋 Dataset Requirements"):
        st.markdown(dataset_requirements)
    
    with st.expander("🎯 Example Datasets"):
        st.markdown(example_datasets)


 
     #  New File Uploader Section
    st.markdown("### 📤 Upload Your Dataset (Currently Using Default Dataset)")

    # Add a checkbox to indicate if the dataset is already cleaned
    skip_cleaning = st.checkbox("My dataset is already cleaned (skip cleaning)")
    
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    
    if uploaded_file is not None:
        try:
            # Validate file size
            file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
            if uploaded_file.size > 200 * 1024 * 1024:  # 200MB limit
                st.error("❌ File size exceeds 200MB limit. Please upload a smaller file.")
                return
                
            # Attempt to read the CSV
            try:
                df = pd.read_csv(uploaded_file)
                if df.empty:
                    st.error("❌ The uploaded file is empty. Please upload a file with data.")
                    return
                    
                st.success("✅ Dataset uploaded successfully!")
            except pd.errors.EmptyDataError:
                st.error("❌ The uploaded file is empty. Please upload a file with data.")
                return
            except pd.errors.ParserError:
                st.error("❌ Unable to parse the CSV file. Please ensure it's properly formatted.")
                return

            # Convert dataframe to JSON for caching
            df_json = df.to_json(orient='records')
            
            # Use the cached cleaning function with proper error handling
            with st.spinner("🧠 AI is analyzing and cleaning the data..." if not skip_cleaning else "Processing dataset..."):
                try:
                    cleaned_df, insights = cached_clean_csv(df_json, skip_cleaning)
                except Exception as cleaning_error:
                    st.error(f"❌ Error during data cleaning: {str(cleaning_error)}")
                    # Fallback to using the original dataframe
                    st.warning("⚠️ Using original dataset without cleaning due to errors.")
                    cleaned_df = df
                    insights = "Cleaning failed, using original data."
            
            # Save results to session state
            st.session_state.df = cleaned_df
            st.session_state.insights = insights
            st.session_state.data_cleaned = True
            st.session_state.dataset_loaded = True
            
            # Store a flag to indicate this is a user-uploaded dataset
            st.session_state.is_user_uploaded = True
            
            # Store the original dataframe JSON and skip_cleaning preference
            # This helps prevent redundant cleaning
            st.session_state.original_df_json = df_json
            st.session_state.skip_cleaning = skip_cleaning
            
            # Reset visualization and model training related session state
            if "column_types" in st.session_state:
                del st.session_state.column_types
            if "corr_matrix" in st.session_state:
                del st.session_state.corr_matrix
            if "df_hash" in st.session_state:
                del st.session_state.df_hash
            if "test_results_calculated" in st.session_state:
                st.session_state.test_results_calculated = False
            
            if skip_cleaning:
                st.success("✅ Using uploaded dataset as-is (skipped cleaning).")
            else:
                st.success("✅ Data cleaned successfully!")
                
        except Exception as e:
            st.error(f"❌ Error processing dataset: {str(e)}")
            st.info("ℹ️ Please check that your file is a valid CSV and try again.")
