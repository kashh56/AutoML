import streamlit as st
import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

# ==== LLM Setup with Caching ====
@st.cache_resource(show_spinner=False)  # Disable default spinner
def get_llm():
    """Cached LLM initialization to prevent reloading on every rerun"""
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_groq import ChatGroq
    import os
    
    try:
        return ChatGroq(
            model="gemma2-9b-it",
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        
    except Exception as e:
        try:
            return ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-lite-preview-02-05",
                google_api_key=os.getenv("GEMINI_API_KEY")
            )
        except:
            return None

llm_insights = get_llm()

# ==== Cached Metric Calculations ====
@st.cache_data(show_spinner=False)  # Add to heavy computations
def _compute_classification_metrics(y_test, y_pred):
    """Cached metric computation for classification"""
    return {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, average="weighted", zero_division=0),
        'recall': recall_score(y_test, y_pred, average="weighted", zero_division=0),
        'f1': f1_score(y_test, y_pred, average="weighted", zero_division=0),
        'cm': confusion_matrix(y_test, y_pred)
    }

@st.cache_data
def _compute_regression_metrics(y_test, y_pred):
    """Cached metric computation for regression"""
    return {
        'mae': mean_absolute_error(y_test, y_pred),
        'mse': mean_squared_error(y_test, y_pred),
        'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
        'r2': r2_score(y_test, y_pred)
    }

# ==== Cached Visualization Generation ====
@st.cache_data(show_spinner=False)  # Add to heavy computations
def _plot_confusion_matrix(cm, classes):
    """Cached confusion matrix plotting"""
    fig, ax = plt.subplots(figsize=(2, 2), dpi=200)
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=classes,
        yticklabels=classes,
        annot_kws={"size": 8},
    )
    plt.xticks(fontsize=5)
    plt.yticks(fontsize=5)
    
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=200)
    buf.seek(0)
    return buf


# ==== Optimized Insights Generation ====
@st.cache_data(show_spinner=False)  # Add to heavy computations
def _get_insights_classification(accuracy, precision, recall, f1, cm_shape):
    """Cached insights generation based on metrics"""
    if llm_insights is None:
        return (
            f"### Classification Metrics Explained\n\n"
            f"**Accuracy** ({accuracy:.3f}): Correct predictions ratio\n"
            f"**Precision** ({precision:.3f}): Positive prediction accuracy\n"
            f"**Recall** ({recall:.3f}): Actual positives found\n"
            f"**F1 Score** ({f1:.3f}): Precision-Recall balance\n"
            f"Confusion Matrix ({cm_shape[0]}x{cm_shape[1]}): Prediction vs Actual distribution"
        )

    try:
        response = llm_insights.invoke(f"""
            Briefly explain these classification metrics (accuracy={accuracy:.3f}, 
            precision={precision:.3f}, recall={recall:.3f}, f1={f1:.3f}) 
            and {cm_shape[0]}x{cm_shape[1]} confusion matrix.
            Use markdown bullet points.
        """)
        return response.content.strip()
    except:
        return "Could not generate AI insights - showing basic metrics explanation."



def display_test_results(trained_model, X_test, y_test, task_type, label_encoder=None):
    """
    Displays test results, including metrics, confusion matrix (if classification),
    and LLM-based or fallback insights about the metrics.
    """
    
    # Create a placeholder for the loading message at the top of the page
    st.markdown("## Test Results")
    loading_placeholder = st.empty()
    
    # Show initial loading message
    with loading_placeholder.container():
        st.info("⏳ Evaluating model performance on test data. This may take a moment for large datasets.")
        progress_bar = st.progress(0)
    
    # Set a flag to track if results have been calculated
    if "test_results_calculated" not in st.session_state:
        st.session_state.test_results_calculated = False
    
    # Only perform calculations if they haven't been done yet
    if not st.session_state.test_results_calculated:
      
        sampling_message = None  
        MAX_SAMPLES = 5000  # Increased from 50 to 5000
        
        # Update progress - Starting evaluation
        with loading_placeholder.container():
            progress_bar.progress(10)
            
            if len(X_test) <= MAX_SAMPLES:
                # Use all test data
                X_test_sample = X_test
                y_test_sample = y_test
                st.info("🔍 Using all test data for evaluation...")
            else:
                # Use sampling for large datasets
                sampling_message = f"📊 Using {MAX_SAMPLES} samples from the test set for visualization (out of {len(X_test)} total)"
                st.info("🔍 Sampling test data for evaluation...")
                
                # Simple random sampling
                idx = np.random.choice(len(X_test.index if hasattr(X_test, 'index') else X_test), size=MAX_SAMPLES, replace=False)
                X_test_sample = X_test.iloc[idx] if hasattr(X_test, 'iloc') else X_test[idx]
                y_test_sample = y_test.iloc[idx] if hasattr(y_test, 'iloc') else y_test[idx]
        
        # Generate predictions
        with loading_placeholder.container():
            progress_bar.progress(30)
            st.info("🔄 Generating predictions... Please wait")
            # Add a spinner for visual feedback during prediction
            with st.spinner("Model working..."):
                if task_type == "regression":
                    y_pred = trained_model.predict(X_test_sample)
                elif task_type == "classification":
                    pipeline, enc = trained_model if label_encoder is None else (trained_model, label_encoder)
                    y_pred = pipeline.predict(X_test_sample)
                    
                    # Decode if label_encoder is used
                    if enc:
                        y_pred = enc.inverse_transform(y_pred)
                        y_test_decoded = enc.inverse_transform(y_test_sample)
                    else:
                        y_test_decoded = y_test_sample
        
        # Update progress - Computing metrics
        with loading_placeholder.container():
            progress_bar.progress(60)
            st.info("📊 Computing metrics...")
            
        # Compute metrics
        if task_type == "regression":
            metrics = _compute_regression_metrics(y_test_sample, y_pred)
        else:
            metrics = _compute_classification_metrics(y_test_decoded, y_pred)
        
        # Update progress - Preparing visualizations
        with loading_placeholder.container():
            progress_bar.progress(90)
            st.info("📈 Preparing visualizations...")
            
            # For classification, pre-calculate confusion matrix before showing "ready" message
            if task_type == "classification":
                # Pre-calculate confusion matrix (this is the slow part)
                _ = _plot_confusion_matrix(metrics['cm'], np.unique(y_test_decoded))
                # Pre-calculate insights (also potentially slow with LLM)
                _ = _get_insights_classification(
                    metrics['accuracy'], 
                    metrics['precision'], 
                    metrics['recall'], 
                    metrics['f1'], 
                    metrics['cm'].shape
                )
            
        # Update progress - Complete (only after all calculations are done)
        with loading_placeholder.container():
            progress_bar.progress(100)
            st.success("✅ Test results ready!")
            
        # Mark results as calculated
        st.session_state.test_results_calculated = True
        
        # Store results in session state for reuse
        st.session_state.test_metrics = metrics
        if task_type == "classification":
            st.session_state.test_y_pred = y_pred
            st.session_state.test_y_test = y_test_decoded
        else:
            st.session_state.test_y_pred = y_pred
            st.session_state.test_y_test = y_test_sample
        
        # Store sampling message
        st.session_state.sampling_message = sampling_message
        
        # Import time only when needed (moved from global to local scope)
        import time
        time.sleep(0.5)  # Short delay to show the "Test results ready!" message
        
    # Display sampling message if it exists
    if "sampling_message" in st.session_state and st.session_state.sampling_message:
        st.info(st.session_state.sampling_message)
    
    # Display the results using stored values
    if task_type == "regression":
        st.subheader("🔍 Regression Metrics")
        
        # Get metrics from session state or use the ones we just calculated
        if "test_metrics" in st.session_state and st.session_state.test_results_calculated:
            metrics = st.session_state.test_metrics
            y_pred = st.session_state.test_y_pred
            y_test = st.session_state.test_y_test
        
        mae, mse, rmse, r2 = metrics['mae'], metrics['mse'], np.sqrt(metrics['mse']), metrics['r2']

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📉 MAE", f"{mae:.4f}")
        col2.metric("📊 MSE", f"{mse:.4f}")
        col3.metric("📈 RMSE", f"{rmse:.4f}")
        col4.metric("📌 R² Score", f"{r2:.4f}")

        # Add regression visualization
        st.subheader("📈 Prediction vs Actual")
        df_results = pd.DataFrame({
            'Actual': y_test,
            'Predicted': y_pred
        })
        fig = px.scatter(df_results, x='Actual', y='Predicted', 
                        title='Predicted vs Actual Values',
                        labels={'Actual': 'Actual Values', 'Predicted': 'Predicted Values'})
        fig.add_shape(type='line', x0=min(y_test), y0=min(y_test), 
                    x1=max(y_test), y1=max(y_test),
                    line=dict(color='red', dash='dash'))
        st.plotly_chart(fig, use_container_width=True)

    elif task_type == "classification":
        st.subheader("🔍 Classification Metrics")
        
        # Get metrics from session state or use the ones we just calculated
        if "test_metrics" in st.session_state and st.session_state.test_results_calculated:
            metrics = st.session_state.test_metrics
            y_pred = st.session_state.test_y_pred
            y_test_decoded = st.session_state.test_y_test
        
        accuracy, precision, recall, f1 = metrics['accuracy'], metrics['precision'], metrics['recall'], metrics['f1']

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("✅ Accuracy", f"{accuracy:.4f}")
        col2.metric("🎯 Precision", f"{precision:.4f}")
        col3.metric("📢 Recall", f"{recall:.4f}")
        col4.metric("🔥 F1 Score", f"{f1:.4f}")

        st.subheader("📊 Confusion Matrix")
        # Use cached function for confusion matrix visualization
        buf = _plot_confusion_matrix(metrics['cm'], np.unique(y_test_decoded))
        st.image(buf, width=450)

        # === Additional Insights Section ===
        st.markdown("---")
        st.markdown("#### Test Insights")
        accuracy, precision, recall, f1 = metrics['accuracy'], metrics['precision'], metrics['recall'], metrics['f1']
        classification_insights = _get_insights_classification(accuracy, precision, recall, f1, metrics['cm'].shape)
        st.markdown(classification_insights)
