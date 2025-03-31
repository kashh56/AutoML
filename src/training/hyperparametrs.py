import streamlit as st



#  Define Hyperparameter Options
def get_hyperparams_ui(model_name):
            """Generate UI components for model-specific hyperparameters."""
            hyperparams = {}

            if model_name in ["Random Forest Regressor", "Random Forest"]:
                hyperparams["n_estimators"] = st.number_input("Number of Trees (n_estimators)", min_value=10, max_value=500, value=100)
                hyperparams["max_depth"] = st.number_input("Max Depth", min_value=1, max_value=50, value=10)
                hyperparams["min_samples_split"] = st.number_input("Min Samples Split", min_value=2, max_value=10, value=2)

            elif model_name in ["XGBoost Regressor", "XGBoost"]:
                hyperparams["n_estimators"] = st.number_input("Number of Boosting Rounds (n_estimators)", min_value=10, max_value=500, value=100)
                hyperparams["learning_rate"] = st.slider("Learning Rate", 0.01, 1.0, 0.1)
                hyperparams["max_depth"] = st.number_input("Max Depth", min_value=1, max_value=50, value=6)

            elif model_name == "Linear Regression":
                st.info("No hyperparameters required for Linear Regression.")

            # New Regression Models:
            elif model_name == "Polynomial Regression":
                hyperparams["degree"] = st.number_input("Degree of Polynomial Features", min_value=2, max_value=10, value=2)
                # You may add additional hyperparameters for the underlying LinearRegression if needed

            elif model_name == "Ridge Regression":
                hyperparams["alpha"] = st.slider("Regularization Strength (alpha)", 0.01, 10.0, 1.0)
                hyperparams["solver"] = st.selectbox("Solver", ["auto", "svd", "cholesky", "lsqr", "sparse_cg", "sag", "saga", "lbfgs"])

            elif model_name == "Lasso Regression":
                hyperparams["alpha"] = st.slider("Regularization Strength (alpha)", 0.01, 10.0, 1.0)
                hyperparams["max_iter"] = st.number_input("Max Iterations", min_value=100, max_value=1000, value=1000)



            elif model_name == "Logistic Regression":
                hyperparams["C"] = st.slider("Regularization Strength (C)", 0.01, 10.0, 1.0)
                hyperparams["max_iter"] = st.number_input("Max Iterations", min_value=100, max_value=1000, value=200)

            elif model_name == "Support Vector Regressor":
                hyperparams["C"] = st.slider("Regularization parameter (C)", 0.1, 100.0, 1.0)
                hyperparams["epsilon"] = st.slider("Epsilon", 0.0, 1.0, 0.1)
                hyperparams["kernel"] = st.selectbox("Kernel", ["linear", "rbf", "poly", "sigmoid"])

            elif model_name == "Decision Tree Regressor":
                hyperparams["max_depth"] = st.number_input("Max Depth", min_value=1, max_value=50, value=10)
                hyperparams["min_samples_split"] = st.number_input("Min Samples Split", min_value=2, max_value=10, value=2)

            elif model_name == "K-Nearest Neighbors Regressor":
                hyperparams["n_neighbors"] = st.number_input("Number of Neighbors", min_value=1, max_value=100, value=5)
                hyperparams["weights"] = st.selectbox("Weight Function", ["uniform", "distance"])

            elif model_name == "ElasticNet":
                hyperparams["alpha"] = st.slider("Alpha", 0.01, 10.0, 1.0)
                hyperparams["l1_ratio"] = st.slider("L1 Ratio", 0.0, 1.0, 0.5)

            elif model_name == "Gradient Boosting Regressor":
                hyperparams["n_estimators"] = st.number_input("Number of Estimators", min_value=10, max_value=500, value=100)
                hyperparams["learning_rate"] = st.slider("Learning Rate", 0.01, 1.0, 0.1)
                hyperparams["max_depth"] = st.number_input("Max Depth", min_value=1, max_value=20, value=3)

            elif model_name == "AdaBoost Regressor":
                hyperparams["n_estimators"] = st.number_input("Number of Estimators", min_value=10, max_value=500, value=50)
                hyperparams["learning_rate"] = st.slider("Learning Rate", 0.01, 1.0, 0.1)

            elif model_name == "Bayesian Ridge":
                hyperparams["alpha_1"] = st.slider("Alpha 1", 1e-6, 1e-1, 1e-4, format="%.6f")
                hyperparams["alpha_2"] = st.slider("Alpha 2", 1e-6, 1e-1, 1e-4, format="%.6f")
                hyperparams["lambda_1"] = st.slider("Lambda 1", 1e-6, 1e-1, 1e-4, format="%.6f")
                hyperparams["lambda_2"] = st.slider("Lambda 2", 1e-6, 1e-1, 1e-4, format="%.6f")

            # --- Additional Classification Models ---
            elif model_name == "Support Vector Classifier":
                hyperparams["C"] = st.slider("Regularization parameter (C)", 0.1, 100.0, 1.0)
                hyperparams["kernel"] = st.selectbox("Kernel", ["linear", "rbf", "poly", "sigmoid"])

            elif model_name == "Decision Tree Classifier":
                hyperparams["max_depth"] = st.number_input("Max Depth", min_value=1, max_value=50, value=10)
                hyperparams["min_samples_split"] = st.number_input("Min Samples Split", min_value=2, max_value=10, value=2)

            elif model_name == "K-Nearest Neighbors Classifier":
                hyperparams["n_neighbors"] = st.number_input("Number of Neighbors", min_value=1, max_value=100, value=5)
                hyperparams["weights"] = st.selectbox("Weight Function", ["uniform", "distance"])

            elif model_name == "Gradient Boosting Classifier":
                hyperparams["n_estimators"] = st.number_input("Number of Estimators", min_value=10, max_value=500, value=100)
                hyperparams["learning_rate"] = st.slider("Learning Rate", 0.01, 1.0, 0.1)
                hyperparams["max_depth"] = st.number_input("Max Depth", min_value=1, max_value=20, value=3)

            elif model_name == "AdaBoost Classifier":
                hyperparams["n_estimators"] = st.number_input("Number of Estimators", min_value=10, max_value=500, value=50)
                hyperparams["learning_rate"] = st.slider("Learning Rate", 0.01, 1.0, 0.1)

            elif model_name == "Gaussian Naive Bayes":
                hyperparams["var_smoothing"] = st.slider("Var Smoothing", 1e-12, 1e-8, 1e-9, format="%.12f")

            elif model_name == "Quadratic Discriminant Analysis":
                hyperparams["reg_param"] = st.slider("Regularization Parameter", 0.0, 1.0, 0.0)

            elif model_name == "Linear Discriminant Analysis":
                hyperparams["solver"] = st.selectbox("Solver", ["svd", "lsqr", "eigen"])



            return hyperparams
