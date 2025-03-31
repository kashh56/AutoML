import streamlit as st

def display_ai_insights():
    """Displays AI-Powered Insights and Data Cleaning Process."""
    
    st.header("💡 AI-Powered Insights")
    
    with st.expander("🧹 Data Cleaning Process", expanded=True):
        if "insights" in st.session_state and "df" in st.session_state:
            # Split insights into cleaning process and analysis
            parts = st.session_state.insights.split("ANALYSIS INSIGHTS:")
            
            # Show cleaning instructions
            st.markdown(parts[0])
            
            # Show interactive dataframe preview using st.session_state.df
            st.subheader("Cleaned Data Sample")
            st.dataframe(
                st.session_state.df.head(),  # Use the existing df state
                use_container_width=True,
                hide_index=True,
            )
            
            # Show analysis insights if present
            if len(parts) > 1:
                st.markdown("---")
                st.markdown("#### Analysis Insights")
                st.markdown(parts[1])
        else:
            st.warning("No insights generated yet. Upload and process a file first.")
