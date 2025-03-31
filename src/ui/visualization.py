import re
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from src.utils.logging import log_frontend_error, log_frontend_warning

SAMPLE_SIZE = 10000  # Define a sample size for subsampling large datasets

# Efficiently hash a dataframe to detect changes
@st.cache_data(show_spinner=False)
def compute_df_hash(df):
    """Optimized dataframe hashing"""
    return hash((df.shape, pd.util.hash_pandas_object(df.iloc[:min(100, len(df))]).sum()))  # Sample-based hashing


@st.cache_data(show_spinner=False, ttl=3600)  # Cache for 1 hour
def is_potential_date_column(series, sample_size=5):
    """Check if column might contain dates"""
    # Check column name first
    if any(keyword in series.name.lower() for keyword in ['date', 'time', 'year', 'month', 'day']):
        return True
    
    # Check sample values
    sample = series.dropna().head(sample_size).astype(str)
    date_patterns = [
        r'\d{4}-\d{2}-\d{2}',      # YYYY-MM-DD
        r'\d{2}/\d{2}/\d{4}',      # MM/DD/YYYY
        r'\d{2}-\w{3}-\d{2,4}',    # DD-MON-YY(Y)
        r'\d{1,2} \w{3,} \d{4}'    # 1 January 2023
    ]
    
    date_count = sum(1 for val in sample if any(re.match(p, val) for p in date_patterns))
    return date_count / len(sample) > 0.5 if len(sample) > 0 else False  # >50% match




# Cache column type detection with improved performance
@st.cache_data(show_spinner=False, ttl=3600)  # Cache for 1 hour
def get_column_types(df):
    """Detect column types efficiently and cache the results."""
    column_types = {}
    
    # Process columns in batches for better performance
    for chunk_start in range(0, len(df.columns), 10):
        chunk_end = min(chunk_start + 10, len(df.columns))
        chunk_columns = df.columns[chunk_start:chunk_end]
        
        for column in chunk_columns:
            # Check for numeric columns
            if pd.api.types.is_numeric_dtype(df[column]):
                # Detect if it's a binary column (0/1, True/False)
                if df[column].nunique() <= 2:
                    column_types[column] = "BINARY"
                # Detect if it's a discrete numeric column (few unique values)
                elif df[column].nunique() < 20:
                    column_types[column] = "NUMERIC_DISCRETE"
                # Otherwise it's a continuous numeric column
                else:
                    column_types[column] = "NUMERIC_CONTINUOUS"
            else:
                # Check for temporal/date columns
                if is_potential_date_column(df[column]):
                    try:
                        # Attempt conversion with coerce
                        converted = pd.to_datetime(df[column], errors='coerce')
                        if not converted.isnull().all():  # At least some valid dates
                            column_types[column] = "TEMPORAL"
                            continue
                    except Exception:
                        pass
                
                # Check for ID-like columns (high cardinality with unique patterns)
                if (df[column].nunique() > len(df) * 0.9 and 
                    any(x in column.lower() for x in ['id', 'code', 'key', 'uuid', 'identifier'])):
                    column_types[column] = "ID"
                # Check for categorical columns (low to medium cardinality)
                elif df[column].nunique() <= 20:
                    column_types[column] = "CATEGORICAL"
                # Otherwise it's a text column
                else:
                    column_types[column] = "TEXT"
   
    return column_types




# Cache correlation matrix computation with improved performance
@st.cache_data(show_spinner=False, ttl=3600)  # Cache for 1 hour
def get_corr_matrix(df):
    """Compute and cache the correlation matrix for numeric columns."""
    # Only select numeric columns to avoid errors
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    # If we have too many numeric columns, sample them for better performance
    if len(numeric_cols) > 30:
        numeric_cols = numeric_cols[:30]
    
    # Return correlation matrix if we have at least 2 numeric columns
    return df[numeric_cols].corr() if len(numeric_cols) > 1 else None





# Cache subsampled data with improved performance
@st.cache_data(show_spinner=False, ttl=3600)  # Cache for 1 hour
def get_subsampled_data(df, column):
    """Return subsampled data for faster visualization."""
    # Check if column exists
    if column not in df.columns:
        return pd.DataFrame()
    
    # Use stratified sampling for categorical columns if possible
    if df[column].nunique() < 20 and len(df) > SAMPLE_SIZE:
        try:
            # Try to get a representative sample
            fractions = min(0.5, SAMPLE_SIZE / len(df))
            return df[[column]].groupby(column, group_keys=False).apply(
                lambda x: x.sample(max(1, int(fractions * len(x))), random_state=42)
            )
        except Exception:
            # Fall back to random sampling
            pass
    
    # Use random sampling
    return df[[column]].sample(min(len(df), SAMPLE_SIZE), random_state=42)




# Cache chart creation with improved performance
@st.cache_data(show_spinner=False, ttl=1800, hash_funcs={  # Cache for 30 minutes
    pd.DataFrame: compute_df_hash,
    pd.Series: lambda s: hash((s.name, compute_df_hash(s.to_frame())))
})
def create_chart(df, column, column_type):
    """Generate optimized charts based on column type."""
    # Check if column exists in the dataframe
    if column not in df.columns:
        return None
        
    # Get subsampled data for better performance
    df_sample = get_subsampled_data(df, column)
    if df_sample.empty:
        return None
    
    try:
        # Year-based columns (special case)
        if "year" in column.lower():
            fig = make_subplots(rows=1, cols=2, subplot_titles=("Year Distribution", "Box Plot"),
                               specs=[[{"type": "bar"}, {"type": "box"}]], column_widths=[0.7, 0.3], horizontal_spacing=0.1)
            year_counts = df_sample[column].value_counts().sort_index()
            fig.add_trace(go.Bar(x=year_counts.index, y=year_counts.values, marker_color='#7B68EE'), row=1, col=1)
            fig.add_trace(go.Box(x=df_sample[column], marker_color='#7B68EE'), row=1, col=2)
        
        # Binary columns (0/1, True/False)
        elif column_type == "BINARY":
            value_counts = df_sample[column].value_counts()
            fig = make_subplots(rows=1, cols=2, 
                               subplot_titles=("Distribution", "Percentage"),
                               specs=[[{"type": "bar"}, {"type": "pie"}]], 
                               column_widths=[0.5, 0.5], 
                               horizontal_spacing=0.1)
            
            fig.add_trace(go.Bar(
                x=value_counts.index, 
                y=value_counts.values, 
                marker_color=['#FF4B4B', '#4CAF50'],
                text=value_counts.values,
                textposition='auto'
            ), row=1, col=1)
            
            fig.add_trace(go.Pie(
                labels=value_counts.index, 
                values=value_counts.values,
                marker=dict(colors=['#FF4B4B', '#4CAF50']),
                textinfo='percent+label'
            ), row=1, col=2)
            
            fig.update_layout(title_text=f"Binary Distribution: {column}")
        
        # Numeric continuous columns
        elif column_type == "NUMERIC_CONTINUOUS":
            fig = make_subplots(rows=2, cols=2, 
                               subplot_titles=("Distribution", "Box Plot", "Violin Plot", "Cumulative Distribution"),
                               specs=[[{"type": "histogram"}, {"type": "box"}], 
                                      [{"type": "violin"}, {"type": "scatter"}]], 
                               vertical_spacing=0.15,
                               horizontal_spacing=0.1)
            
            # Histogram
            fig.add_trace(go.Histogram(
                x=df_sample[column], 
                nbinsx=30, 
                marker_color='#FF4B4B',
                opacity=0.7
            ), row=1, col=1)
            
            # Box plot
            fig.add_trace(go.Box(
                x=df_sample[column], 
                marker_color='#FF4B4B',
                boxpoints='outliers'
            ), row=1, col=2)
            
            # Violin plot
            fig.add_trace(go.Violin(
                x=df_sample[column], 
                marker_color='#FF4B4B',
                box_visible=True,
                points='outliers'
            ), row=2, col=1)
            
            # CDF
            sorted_data = np.sort(df_sample[column].dropna())
            cumulative = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
            
            fig.add_trace(go.Scatter(
                x=sorted_data,
                y=cumulative,
                mode='lines',
                line=dict(color='#FF4B4B', width=2)
            ), row=2, col=2)
            
            fig.update_layout(height=600, title_text=f"Continuous Variable Analysis: {column}")
        
        # Numeric discrete columns
        elif column_type == "NUMERIC_DISCRETE":
            value_counts = df_sample[column].value_counts().sort_index()
            fig = make_subplots(rows=1, cols=2, 
                               subplot_titles=("Distribution", "Percentage"),
                               specs=[[{"type": "bar"}, {"type": "pie"}]], 
                               column_widths=[0.7, 0.3], 
                               horizontal_spacing=0.1)
            
            fig.add_trace(go.Bar(
                x=value_counts.index, 
                y=value_counts.values, 
                marker_color='#FF4B4B',
                text=value_counts.values,
                textposition='auto'
            ), row=1, col=1)
            
            fig.add_trace(go.Pie(
                labels=value_counts.index, 
                values=value_counts.values,
                marker=dict(colors=px.colors.sequential.Reds),
                textinfo='percent+label'
            ), row=1, col=2)
            
            fig.update_layout(title_text=f"Discrete Numeric Distribution: {column}")
        
        # Categorical columns
        elif column_type == "CATEGORICAL":
            value_counts = df_sample[column].value_counts().head(20)  # Limit to top 20 categories
            fig = make_subplots(rows=1, cols=2, 
                               subplot_titles=("Category Distribution", "Percentage Breakdown"),
                               specs=[[{"type": "bar"}, {"type": "pie"}]], 
                               column_widths=[0.6, 0.4], 
                               horizontal_spacing=0.1)
            
            # Bar chart
            fig.add_trace(go.Bar(
                x=value_counts.index, 
                y=value_counts.values, 
                marker_color='#00FFA3',
                text=value_counts.values,
                textposition='auto'
            ), row=1, col=1)
            
            # Pie chart
            fig.add_trace(go.Pie(
                labels=value_counts.index, 
                values=value_counts.values,
                marker=dict(colors=px.colors.sequential.Greens),
                textinfo='percent+label'
            ), row=1, col=2)
            
            fig.update_layout(title_text=f"Categorical Analysis: {column}")
        
        # Temporal/date columns
        elif column_type == "TEMPORAL":
            # Convert with safe datetime parsing
            dates = pd.to_datetime(df_sample[column], errors='coerce', format='mixed')
            valid_dates = dates[dates.notna()]
            
            fig = make_subplots(
                rows=2, 
                cols=2,
                subplot_titles=("Monthly Pattern", "Yearly Pattern", "Cumulative Trend", "Day of Week Distribution"),
                vertical_spacing=0.15,
                horizontal_spacing=0.1,
                specs=[[{"type": "bar"}, {"type": "bar"}], 
                       [{"type": "scatter"}, {"type": "bar"}]]
            )
            
            # Monthly pattern
            if not valid_dates.empty:
                monthly_counts = valid_dates.dt.month.value_counts().sort_index()
                month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                month_labels = [month_names[i-1] for i in monthly_counts.index]
                
                fig.add_trace(go.Bar(
                    x=month_labels,
                    y=monthly_counts.values,
                    marker_color='#7B68EE',
                    text=monthly_counts.values,
                    textposition='auto'
                ), row=1, col=1)
                
                # Yearly pattern
                yearly_counts = valid_dates.dt.year.value_counts().sort_index()
                
                fig.add_trace(go.Bar(
                    x=yearly_counts.index,
                    y=yearly_counts.values,
                    marker_color='#7B68EE',
                    text=yearly_counts.values,
                    textposition='auto'
                ), row=1, col=2)
                
                # Cumulative trend
                sorted_dates = valid_dates.sort_values()
                cumulative = np.arange(1, len(sorted_dates) + 1)
                
                fig.add_trace(go.Scatter(
                    x=sorted_dates,
                    y=cumulative,
                    mode='lines',
                    line=dict(color='#7B68EE', width=2)
                ), row=2, col=1)
                
                # Day of week distribution
                dow_counts = valid_dates.dt.dayofweek.value_counts().sort_index()
                dow_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                dow_labels = [dow_names[i] for i in dow_counts.index]
                
                fig.add_trace(go.Bar(
                    x=dow_labels,
                    y=dow_counts.values,
                    marker_color='#7B68EE',
                    text=dow_counts.values,
                    textposition='auto'
                ), row=2, col=2)
            
            fig.update_layout(height=600, title_text=f"Temporal Analysis: {column}")
        
        # ID columns (show distribution of first few characters, length distribution)
        elif column_type == "ID":
            # Calculate ID length statistics
            id_lengths = df_sample[column].astype(str).str.len()
            
            # Extract first 2 characters for prefix analysis
            id_prefixes = df_sample[column].astype(str).str[:2].value_counts().head(15)
            
            fig = make_subplots(
                rows=1, 
                cols=2,
                subplot_titles=("ID Length Distribution", "Common ID Prefixes"),
                horizontal_spacing=0.1,
                specs=[[{"type": "histogram"}, {"type": "bar"}]]
            )
            
            # ID length histogram
            fig.add_trace(go.Histogram(
                x=id_lengths,
                nbinsx=20,
                marker_color='#9C27B0'
            ), row=1, col=1)
            
            # ID prefix bar chart
            fig.add_trace(go.Bar(
                x=id_prefixes.index,
                y=id_prefixes.values,
                marker_color='#9C27B0',
                text=id_prefixes.values,
                textposition='auto'
            ), row=1, col=2)
            
            fig.update_layout(title_text=f"ID Analysis: {column}")
        
        # Text columns
        elif column_type == "TEXT":
            # For text columns, show top values and length distribution
            value_counts = df_sample[column].value_counts().head(15)
            
            # Calculate text length statistics
            text_lengths = df_sample[column].astype(str).str.len()
            
            fig = make_subplots(
                rows=2, 
                cols=1,
                subplot_titles=("Top Values", "Text Length Distribution"),
                vertical_spacing=0.2,
                specs=[[{"type": "bar"}], [{"type": "histogram"}]]
            )
            
            # Top values bar chart
            fig.add_trace(
                go.Bar(
                    x=value_counts.index,
                    y=value_counts.values,
                    marker_color='#00B4D8',
                    text=value_counts.values,
                    textposition='auto'
                ),
                row=1, col=1
            )
            
            # Text length histogram
            fig.add_trace(
                go.Histogram(
                    x=text_lengths,
                    nbinsx=20,
                    marker_color='#00B4D8'
                ),
                row=2, col=1
            )
            
            fig.update_layout(
                height=600,
                title_text=f"Text Analysis: {column}"
            )
        
        # Fallback for any other column type
        else:
            fig = go.Figure(go.Histogram(x=df_sample[column], marker_color='#888'))
            fig.update_layout(title_text=f"Generic Analysis: {column}")

        # Common layout settings
        fig.update_layout(
            height=400, 
            showlegend=False, 
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)', 
            font=dict(color='#FFFFFF'),
            margin=dict(l=40, r=40, t=50, b=40)
        )
        
        return fig
    
    except Exception as e:
        log_frontend_error("Chart Generation", f"Error creating chart for {column}: {str(e)}")
        return None




def visualize_data(df):
    """Automated dashboard with optimized visualizations."""
    if df is None or df.empty:
        st.error("❌ No data available. Please upload and clean your data first.")
        return

    # Calculate dataframe hash only once
    df_hash = compute_df_hash(df)  

    # Initialize selected columns in session state if not already present
    if "selected_viz_columns" not in st.session_state:
        # Initialize with first 4 columns or fewer if df has fewer columns
        initial_columns = list(df.columns[:min(4, len(df.columns))])
        st.session_state.selected_viz_columns = initial_columns
    
    # Filter out any columns that no longer exist in the dataframe
    valid_columns = [col for col in st.session_state.selected_viz_columns if col in df.columns]
    
    # Define a callback function to update selected columns
    def on_column_selection_change():
        # Store the selected columns in session state
        st.session_state.selected_viz_columns = st.session_state.viz_column_selector
        # Ensure we stay on the visualization tab (index 2)
        st.session_state.current_tab_index = 2
    
    # Use session state for the multiselect with a consistent key and callback
    selected_columns = st.multiselect(
        "Select columns to visualize", 
        options=df.columns, 
        default=valid_columns,
        key="viz_column_selector",
        on_change=on_column_selection_change
    )
    
    # Check if we need to recompute column types and correlation matrix
    # This will only happen when:
    # 1. We don't have column_types in session_state
    # 2. The dataframe hash has changed (new data)
    # 3. We're using a user-uploaded dataset for the first time
    recompute_needed = (
        "column_types" not in st.session_state or 
        "df_hash" not in st.session_state or 
        st.session_state.get("df_hash") != df_hash
    )
    
    if recompute_needed:
        with st.spinner("🔄 Analyzing data structure..."):
            # Compute and cache column types
            st.session_state.column_types = get_column_types(df)
            # Compute and cache correlation matrix
            st.session_state.corr_matrix = get_corr_matrix(df)
            # Update the dataframe hash
            st.session_state.df_hash = df_hash
            # Ensure we stay on the visualization tab
            st.session_state.current_tab_index = 2
            
            # Reset any test results if the data has changed
            if "test_results_calculated" in st.session_state:
                st.session_state.test_results_calculated = False
                # Clear any previous test metrics to avoid using stale data
                for key in ['test_metrics', 'test_y_pred', 'test_y_test', 'test_cm', 'sampling_message']:
                    if key in st.session_state:
                        del st.session_state[key]
    
    # Use cached values from session state
    column_types = st.session_state.column_types
    corr_matrix = st.session_state.corr_matrix

    if selected_columns:
        # Use a container to wrap all visualizations
        viz_container = st.container()
        
        with viz_container:
            for idx in range(0, len(selected_columns), 2):
                col1, col2 = st.columns(2)

                for i, col in enumerate([col1, col2]):
                    if idx + i < len(selected_columns):
                        column = selected_columns[idx + i]
                        with col:
                            # Use consistent keys for charts based on column name
                            chart_key = f"plot_{column.replace(' ', '_')}"
                            
                            # Only create chart if column exists in column_types
                            if column in column_types:
                                fig = create_chart(df, column, column_types[column])
                                if fig:
                                    st.plotly_chart(fig, use_container_width=True, key=chart_key)
                                    with st.expander(f"📊 Summary Statistics - {column}", expanded=False):
                                        if "NUMERIC" in column_types[column]:
                                            st.dataframe(df[column].describe(), key=f"stats_{column.replace(' ', '_')}")
                                        else:
                                            st.dataframe(df[column].value_counts(), key=f"counts_{column.replace(' ', '_')}")
                            else:
                                st.warning(f"⚠️ Column '{column}' not found in the dataset or its type couldn't be determined.")

            if corr_matrix is not None:
                st.subheader("🔗 Correlation Analysis")
                fig = px.imshow(corr_matrix, title="Correlation Matrix", color_continuous_scale="RdBu")
                st.plotly_chart(fig, use_container_width=True, key="corr_matrix_plot")
    
    else:
        st.info("👆 Please select columns to visualize")
