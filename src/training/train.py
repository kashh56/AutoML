from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from xgboost import XGBRegressor, XGBClassifier
from sklearn.svm import SVR, SVC
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.linear_model import ElasticNet, BayesianRidge
from sklearn.ensemble import GradientBoostingRegressor, AdaBoostRegressor, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis, LinearDiscriminantAnalysis
from sklearn.linear_model import Ridge, Lasso
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline as SkPipeline

import streamlit as st




def get_model(task_type, model_name, hyperparams):
    """Returns the model instance based on user selection with hyperparameters."""
    models = {
        "regression": {
            # Already existing:
            "Linear Regression": LinearRegression,
            "Random Forest Regressor": RandomForestRegressor,
            "XGBoost Regressor": XGBRegressor,
            # Additional regression models:
            "Support Vector Regressor": SVR,
            "Decision Tree Regressor": DecisionTreeRegressor,
            "K-Nearest Neighbors Regressor": KNeighborsRegressor,
            "ElasticNet": ElasticNet,
            "Gradient Boosting Regressor": GradientBoostingRegressor,
            "AdaBoost Regressor": AdaBoostRegressor,
            "Bayesian Ridge": BayesianRidge,
            "Ridge Regression": Ridge,
            "Lasso Regression": Lasso ,

        },
        "classification": {
            # Already existing:
            "Logistic Regression": LogisticRegression,
            "Random Forest": RandomForestClassifier,
            "XGBoost": XGBClassifier,
            # Additional classification models:
            "Support Vector Classifier": SVC,
            "Decision Tree Classifier": DecisionTreeClassifier,
            "K-Nearest Neighbors Classifier": KNeighborsClassifier,
            "Gradient Boosting Classifier": GradientBoostingClassifier,
            "AdaBoost Classifier": AdaBoostClassifier,
            "Gaussian Naive Bayes": GaussianNB,
            "Quadratic Discriminant Analysis": QuadraticDiscriminantAnalysis,
            "Linear Discriminant Analysis": LinearDiscriminantAnalysis
        }
    }        
    

    if task_type in models and model_name in models[task_type]:
        return models[task_type][model_name](**hyperparams)  # Apply hyperparameters
    else:
        raise ValueError(f"Invalid model selection: {model_name} for {task_type}")
    
    
def train_model(df, target_column, task_type, selected_model_name, hyperparams):
    """Preprocess data, train the selected model with hyperparameters, and return the trained model."""

    with st.spinner(" Training model... Please wait!"):  
   
        # Get the model with hyperparameters
        model = get_model(task_type, selected_model_name, hyperparams)

        # Split features and target
        X = df.drop(columns=[target_column])
        y = df[target_column]

        # Label encode target if classification (for categorical labels)
        label_encoder = None
        if task_type == "classification" and y.dtype == "object":
            from sklearn.preprocessing import LabelEncoder
            label_encoder = LabelEncoder()
            y = label_encoder.fit_transform(y)

        # Train-Test Split (80-20)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Identify numerical and categorical columns
        num_cols = X.select_dtypes(include=["int64", "float64"]).columns
        cat_cols = X.select_dtypes(include=["object", "category"]).columns

        # Preprocessing Pipeline
        # Numeric pipeline: impute missing values then scale them
        num_pipeline = SkPipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ])

        # Categorical pipeline: impute missing values then one-hot encode them
        cat_pipeline = SkPipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
        ])

        preprocessor = ColumnTransformer([
            ("num", num_pipeline, num_cols),
            ("cat", cat_pipeline, cat_cols)
        ])

        pipeline = SkPipeline([
            ("preprocessor", preprocessor),
            ("model", model)
        ])

        # Train Model
        pipeline.fit(X_train, y_train)

        # Store test data and metadata in session state
        st.session_state.X_test = X_test
        st.session_state.y_test = y_test
        st.session_state.task_type = task_type
        st.session_state.label_encoder = label_encoder  # Store label encoder for decoding predictions
        
        # Reset test results calculation flag when a new model is trained
        if "test_results_calculated" in st.session_state:
            st.session_state.test_results_calculated = False
        
        # Clear any previous test metrics to avoid using stale data
        for key in ['test_metrics', 'test_y_pred', 'test_y_test', 'test_cm', 'sampling_message']:
            if key in st.session_state:
                del st.session_state[key]

        # Return trained model + label encoder (needed for decoding predictions if classification)
        if task_type == "classification":
            return pipeline, label_encoder
        else:
            return pipeline