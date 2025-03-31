import streamlit as st
from ui.test_results import display_test_results

def display_model_evaluation():
    """Displays the evaluation results of the trained model on the test set."""
    
    st.header("📊 Model Evaluation on Test Set")

    # Ensure model and test data exist in session state
    if "trained_model" in st.session_state and "X_test" in st.session_state:
        trained_model = st.session_state.trained_model
        X_test = st.session_state.X_test
        y_test = st.session_state.y_test
        task_type = st.session_state.task_type
        
        # Handle classification case where model may include a label encoder
        if task_type == "classification":
            if isinstance(trained_model, tuple):  
                pipeline, label_encoder = trained_model
                display_test_results((pipeline, label_encoder), X_test, y_test, task_type)
            else:
                display_test_results(trained_model, X_test, y_test, task_type)
        else:
            display_test_results(trained_model, X_test, y_test, task_type)
    
    else:
        st.warning("🚨 Train a model first to see test results!")
