<!-- Custom header with green glow effect -->
<p align="center">
  <img src="header.svg" alt="AutoML - Automated Machine Learning Platform" width="800" />
</p>

<p>
<p align="center">
  <a href="https://github.com/username/Auto-ML/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg" alt="Made with Python"></a>
  <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Made%20with-Streamlit-FF4B4B.svg" alt="Made with Streamlit"></a>
  <a href="https://scikit-learn.org/"><img src="https://img.shields.io/badge/Made%20with-Scikit--Learn-F7931E.svg" alt="Made with Scikit-Learn"></a>
</p>

<p align="center">
  <a href="https://pandas.pydata.org/"><img src="https://img.shields.io/badge/Made%20with-Pandas-150458.svg" alt="Made with Pandas"></a>
  <a href="https://numpy.org/"><img src="https://img.shields.io/badge/Made%20with-NumPy-013243.svg" alt="Made with NumPy"></a>
  <a href="https://matplotlib.org/"><img src="https://img.shields.io/badge/Made%20with-Matplotlib-11557c.svg" alt="Made with Matplotlib"></a>
  <a href="https://seaborn.pydata.org/"><img src="https://img.shields.io/badge/Made%20with-Seaborn-3776AB.svg" alt="Made with Seaborn"></a>
  <a href="https://plotly.com/"><img src="https://img.shields.io/badge/Made%20with-Plotly-3F4F75.svg" alt="Made with Plotly"></a>
  <a href="https://xgboost.readthedocs.io/"><img src="https://img.shields.io/badge/Made%20with-XGBoost-0073B7.svg" alt="Made with XGBoost"></a>
</p>

<p align="center">
  <a href="https://python.langchain.com/"><img src="https://img.shields.io/badge/Made%20with-LangChain-00A86B.svg" alt="Made with LangChain"></a>
  <a href="https://smith.langchain.com/"><img src="https://img.shields.io/badge/Monitored%20with-LangSmith-7742DD.svg" alt="Monitored with LangSmith"></a>
  <a href="https://ai.google.dev/"><img src="https://img.shields.io/badge/Powered%20by-Google%20Gemini-4285F4.svg" alt="Powered by Google Gemini"></a>
  <a href="https://groq.com/"><img src="https://img.shields.io/badge/Powered%20by-Groq-6236FF.svg" alt="Powered by Groq"></a>
  <a href="https://www.python-dotenv.org/"><img src="https://img.shields.io/badge/Made%20with-python--dotenv-2E7D32.svg" alt="Made with python-dotenv"></a>
  <a href="https://pickle.readthedocs.io/"><img src="https://img.shields.io/badge/Uses-pickle-8BC34A.svg" alt="Uses pickle"></a>
</p>

<p align="center">
  <b>AutoML</b> is a powerful tool for automating the end-to-end process of applying machine learning to real-world problems. It simplifies the process of model selection, hyperparameter tuning, and downloading, making machine learning accessible to everyone.
</p>

## 🔗 Live Demo

<p align="center">
  <a href="https://automl-demo.streamlit.app" target="_blank">
    <img src="https://img.shields.io/badge/Try%20the%20Demo-00B8D9?style=for-the-badge&logo=streamlit&logoColor=white" alt="Try the Demo" />
  </a>
</p>

<p align="center">
  Check out the live demo of AutoML and experience the power of automated machine learning firsthand!
</p>

## 🎬 Video Showcase

<p align="center">
  <video width="800" controls>
    <source src="demo-video.mp4" type="video/mp4">
    Your browser does not support the video tag.
  </video>
</p>

<p align="center">
  <em>See AutoML in action: This demonstration shows how to analyze data, train models, and get AI-powered insights in minutes!</em>
</p>

## ✨ Features

- 📊 **Data Visualization and Analysis**: Interactive visualizations to understand your data
  - Correlation heatmaps
  - Distribution plots
  - Feature importance charts
  - Pair plots for relationship analysis
  
- 🧹 **Automated Data Cleaning and Preprocessing**: Handle missing values, outliers, and feature engineering
  - Automatic detection and handling of missing values
  - Outlier detection and treatment
  - Feature scaling and normalization
  - Categorical encoding (One-Hot, Label, Target encoding)
  
- 🤖 **Multiple ML Model Selection**: Choose from a variety of models or let AutoML select the best one
  - Classification models: Logistic Regression, Random Forest, XGBoost, SVC, Decision Tree, KNN, Gradient Boosting, AdaBoost, Gaussian Naive Bayes, QDA, LDA
  - Regression models: Linear Regression, Random Forest, XGBoost, SVR, Decision Tree, KNN, ElasticNet, Gradient Boosting, AdaBoost, Bayesian Ridge, Ridge, Lasso
  
- ⚙️ **Hyperparameter Tuning**: Optimize model performance with advanced tuning techniques
  - Added Support for 20+ Models to easily fine tune hyperparameters
  - Added Support for 10+ Hyperparameter Tuning Techniques
  
  
- 📈 **Model Performance Evaluation**: Comprehensive metrics and visualizations
  - Classification: Accuracy, Precision, Recall, F1-Score, ROC-AUC, Confusion Matrix
  - Regression: MAE, MSE, RMSE, R², Residual Plots
  
- 🔍 **AI-powered Data Insights**: Leverage Google's Gemini for intelligent data analysis
  - Natural language explanations of model decisions
  - Automated feature importance interpretation
  - Data quality assessment
  - Trend identification and anomaly detection

- 🧠 **LLM Fine-Tuning and Download**: Access and utilize pre-trained language models
  - Download fine-tuned LLMs for specific domains
  - Customize existing models for your specific use case
  - Access to various model sizes (small, medium, large)
  - Seamless integration with your data processing pipeline

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Google API key for Gemini for data insights and dataframe cleaning
- Groq API key for LLM based test results analysis
- langsmith API for monitoring llm calls

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Auto-ML
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your environment variables:
```bash
# Create a .env file with your Google API key as well as other keys
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

## 🎮 Usage

Start the application:

```bash
streamlit run app.py
```

### Quick Start Guide

1. **Upload Data**: Upload your CSV file
   - Supported format: CSV
   - Automatic data type detection
   - Preview of first few rows

2. **Explore Data**: Visualize and understand your dataset
   - Summary statistics
   - Correlation analysis
   - Distribution visualization
   - Missing value analysis

3. **Preprocess**: Clean and transform your data
   - Handle missing values (imputation strategies)
   - Remove or transform outliers
   - Feature scaling options
   - Encoding categorical variables

4. **Train Models**: Select models and tune hyperparameters
   - Choose target variable and features
   - Select machine learning algorithms
   - Configure hyperparameter search space
   - Set evaluation metrics

5. **Evaluate**: Compare model performance
   - Performance metrics visualization
   - Feature importance analysis
   - Model comparison dashboard
   - Cross-validation results

6. **Deploy**: Export your model 
   - Download trained model as pickle file



   
## 🧩 Project Structure

```
Auto-ML/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Project dependencies
├── .env                    # Environment variables (API keys)
├── README.md               # Project documentation
├── models/                 # Saved model files
├── logs/                   # Application logs
└── src/                    # Source code
    ├── __init__.py         # Package initialization
    ├── preprocessing/      # Data preprocessing modules
    │   ├── __init__.py
    │   └── ...             # Data cleaning, transformation
    ├── training/           # Model training modules
    │   ├── __init__.py
    │   └── ...             # Model training, evaluation
    ├── ui/                 # User interface components
    │   ├── __init__.py
    │   └── ...             # Streamlit UI elements
    └── utils/              # Utility functions
        ├── __init__.py
        └── ...             # Helper functions
```



# Preprocessing Pipelines

1\. Data Ingestion Pipeline
---------------------------

**Purpose:** Collects raw data from multiple sources (CSV, databases, APIs).

*   Reads structured/unstructured data
*   Handles missing values and duplicates
*   Converts raw data into a clean DataFrame

2\. Data Cleaning & Preprocessing Pipeline
------------------------------------------

**Purpose:** Transforms raw data into a machine-learning-ready format.

*   **Cleans Data:** Handles NaNs, outliers, and standardizes columns
*   **Encodes Categorical Features:** One-hot encoding, label encoding
*   **Scales Numerical Data:** MinMaxScaler, StandardScaler




3\. Model Selection & Training Pipeline
---------------------------------------

**Purpose:** Automates the process of selecting and training.

*   **Multiple Algorithms:** Trains XGBoost, RandomForest, Deep Learning models
*   **Hyperparameter Optimization:** Finds the best config for each model



6\. Model Deployment Pipeline
-----------------------------

**Purpose:** Makes the model available for real-world usage.

*   Exports the Model (Pickle, ONNX, TensorFlow SavedModel)
*   Easily Download after training



# Feedback and Fallback Mechanism

AutoML implements a robust feedback and fallback system to ensure reliability:

1. **Data Cleaning Validation**: The system validates all cleaning operations and provides feedback on the changes made
   - Automatic detection of cleaning effectiveness
   - Detailed logs of transformations applied to the data

2. **LLM Fallback Mechanism**: For AI-powered insights and data analysis
   - Primary attempt uses advanced LLMs (Google Gemini/Groq)
   - Automatic fallback to rule-based algorithms if LLM fails
   - Graceful degradation to ensure core functionality remains available
   - Error logging and reporting for continuous improvement
   - LangSmith integration for monitoring and tracking all LLM calls

3. **Error Feedback Loop**: Intelligent error handling during data cleaning
   - Automatically captures errors that occur during data cleaning operations
   - Sends error context to LLM to generate refined cleaning code
   - Re-executes the improved cleaning process
   - Iterative refinement ensures robust data preparation even with challenging datasets

## 🤝 Contributing

We welcome contributions! 

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
4. Make your changes
5. Run tests:
   ```bash
   pytest
   ```
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/) for the interactive web framework
- [Scikit-learn](https://scikit-learn.org/) for machine learning algorithms
- [Pandas](https://pandas.pydata.org/) for data manipulation
- [Plotly](https://plotly.com/) for interactive visualizations
- [Google Gemini](https://ai.google.dev/) for AI-powered insights
- [XGBoost](https://xgboost.readthedocs.io/) for gradient boosting
- [Seaborn](https://seaborn.pydata.org/) for statistical visualizations
- [LangChain](https://python.langchain.com/) for large language model integration
- [LangSmith](https://smith.langchain.com/) for LLM call tracking and monitoring
- [Groq](https://groq.com/) for high-performance computing

---

<p align="center">
  Made with ❤️ by Akash Anandani
</p>