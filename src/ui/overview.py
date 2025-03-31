
import streamlit as st
import pandas as pd

@st.cache_data
def compute_column_info(df):
    """Compute summary statistics for each column."""
    return pd.DataFrame({
        "Column": df.dtypes.index,
        "Type": df.dtypes.astype(str),
        "Non-Null Count": df.count(),
        "Null Count": df.isnull().sum(),
        "Unique Values": df.nunique(),
    })

def show_overview_page():
    """Displays dataset statistics, preview, and column information."""
    
    if "df" not in st.session_state or st.session_state.df is None:
        st.warning("⚠️ No dataset loaded. Please upload a dataset first.")
        return

    df = st.session_state.df

    # Dataset Statistics
    st.markdown("## 📊 Dataset Statistics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Rows", len(df))
    with col2:
        st.metric("Total Columns", len(df.columns))
    with col3:
        numeric_count = len(df.select_dtypes(include=["int64", "float64"]).columns)
        st.metric("Numeric Columns", numeric_count)
    with col4:
        categorical_count = len(df.select_dtypes(include=["object", "category"]).columns)
        st.metric("Categorical Columns", categorical_count)

    # Data Preview: Only display the top few rows
    st.markdown("## 🔍 Data Preview")
    st.dataframe(df.head(), use_container_width=True)

    # Column Information: Use cached computation for faster loading
    st.markdown("## 📌 Column Information")
    dtypes_df = compute_column_info(df)
    st.dataframe(dtypes_df, use_container_width=True)
