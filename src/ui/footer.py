import streamlit as st

def show_footer():
    """Display footer with copyright information."""
    footer_html = """
        <div class="footer">
            © 2025 AutoML All Rights Reserved.
        </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)
