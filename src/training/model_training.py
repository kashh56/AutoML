import streamlit as st 
from .hyperparametrs import get_hyperparams_ui 
import pickle
from .train import train_model

#  Model Training Tab
def model_training_tab(df):
    # Ensure we have session state for model training
    if "target_column" not in st.session_state:
        st.session_state.target_column = df.columns[0] if not df.empty else None
    
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = None
    
    st.subheader("📌 Model Training")

    # Use session state to maintain selection across reruns
    target_column = st.selectbox(
        "🎯 Select Target Column (Y)", 
        df.columns, 
        index=list(df.columns).index(st.session_state.target_column) if st.session_state.target_column in df.columns else 0,
        key="target_column_select"
    )
    
    # Update session state after selection
    st.session_state.target_column = target_column

    # Infer task type automatically
    task_type = "classification" if df[target_column].dtype == "object" or df[target_column].nunique() <= 10 else "regression"
    st.write(f"🔍 Detected Task Type: **{task_type.capitalize()}**")

    model_options = {
        "classification": ["Random Forest", "Logistic Regression", "XGBoost" , "Support Vector Classifier", "Decision Tree Classifier", "K-Nearest Neighbors Classifier", "Gradient Boosting Classifier", "AdaBoost Classifier", "Gaussian Naive Bayes", "Quadratic Discriminant Analysis", "Linear Discriminant Analysis"],
        "regression": ["Linear Regression", "Random Forest Regressor", "XGBoost Regressor" , "Support Vector Regressor", "Decision Tree Regressor", "K-Nearest Neighbors Regressor", "ElasticNet", "Gradient Boosting Regressor", "AdaBoost Regressor", "Bayesian Ridge" , "Ridge Regression", "Lasso Regression"],
    }

    # Initialize selected model if not already set or if task type changed
    if st.session_state.selected_model not in model_options[task_type]:
        st.session_state.selected_model = model_options[task_type][0]
    
    # Use session state to maintain selection across reruns
    selected_model_name = st.selectbox(
        "🤖 Choose Model", 
        model_options[task_type], 
        index=model_options[task_type].index(st.session_state.selected_model),
        key="selected_model_select"
    )
    
    # Update session state after selection
    st.session_state.selected_model = selected_model_name

    st.markdown("### 🔧 Hyperparameters")
    hyperparams = get_hyperparams_ui(selected_model_name)

    # Use a unique key for the button to avoid conflicts
    if st.button("🚀 Train Model", key="train_model_button_unique"):
        with st.spinner("Training in progress... ⏳"):
            trained_model = train_model(df, target_column, task_type, selected_model_name, hyperparams)
            st.success("✅ Model trained successfully!")
            st.session_state.trained_model = trained_model
            st.session_state.model_trained = True
            
            # Note: test_results_calculated is already reset in train_model function

    if "trained_model" in st.session_state:
        st.markdown("### 📥 Download Trained Model")
        
        # Use a safer approach for file operations with proper cleanup
        try:
            # Use a temporary file that will be automatically cleaned up
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as temp_file:
                pickle.dump(st.session_state.trained_model, temp_file)
                temp_file_path = temp_file.name
            
            # Read the file for download
            with open(temp_file_path, "rb") as f:
                st.download_button(
                    label="📥 Download Model",
                    data=f,
                    file_name="trained_model.pkl",
                    mime="application/octet-stream",
                )
                
            # Clean up the temporary file
            import os
            try:
                os.unlink(temp_file_path)
            except:
                pass  # Silently handle deletion errors
                
        except Exception as e:
            st.error(f"Error preparing model for download: {str(e)}")
