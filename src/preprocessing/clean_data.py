from sklearn.impute import SimpleImputer
from dotenv import load_dotenv
from scipy import stats
from langchain_groq import ChatGroq  
from langchain.chains import LLMChain
import pandas as pd
import numpy as np
import re
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
import streamlit as st
from .clean_df_fallback  import clean_dataframe_fallback


# # Load environment variables

load_dotenv()



groq_api_key = os.getenv("GROQ_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")


if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")


# Initialize the LLM model
try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-lite-preview-02-05", 
        google_api_key=gemini_api_key
    )
    print("Primary Gemini LLM loaded successfully.")

except Exception as e:
    print(f"Error initializing primary Gemini LLM: {e}")
    
    # Fallback to a different LLM from Groq
    try:
        llm = ChatGroq(
            model="gemma2-9b-it",  # replace with your desired Groq model identifier
            groq_api_key=groq_api_key
        )
        print("Fallback Groq LLM loaded successfully.")
    
    except Exception as e2:
        print(f"Error initializing fallback Groq LLM: {e2}")
        llm=None



# Cache the clean_csv function to prevent redundant cleaning
@st.cache_data(ttl=3600, show_spinner=False)
def cached_clean_csv(df_json, skip_cleaning=False):
    """Cached version of the clean_csv function to prevent redundant cleaning.
    
    Args:
        df_json: JSON string representation of the dataframe (for hashing)
        skip_cleaning: Whether to skip cleaning
        
    Returns:
        Tuple of (cleaned_df, insights)
    """
    # Convert JSON back to dataframe
    df = pd.read_json(df_json, orient='records')
    
    # If skip_cleaning is True, return the dataframe as is
    if skip_cleaning:
        return df, "No cleaning performed (user skipped)."
    
    # Reset any test results if we're cleaning a new dataset
    if "test_results_calculated" in st.session_state:
        st.session_state.test_results_calculated = False
        # Clear any previous test metrics to avoid using stale data
        for key in ['test_metrics', 'test_y_pred', 'test_y_test', 'test_cm', 'sampling_message']:
            if key in st.session_state:
                del st.session_state[key]
    
    # Call the actual cleaning function
    return clean_csv(df)


def clean_csv(df):
    """Original clean_csv function that performs the actual cleaning."""
    # ---------------------------
    # Early fallback if LLM initialization failed
    # ---------------------------
    if llm is None:
        print("LLM initialization failed; using hardcoded cleaning function.")
        fallback_df = clean_dataframe_fallback(df)

        return fallback_df , "LLM initialization failed; using hardcoded cleaning function, so no insights were generated."



    # ---------------------------
    # LLM-based cleaning function generation
    # ---------------------------


    # Escape curly braces in the JSON sample and column names
    sample_data = df.head(3).to_json(orient='records')
    escaped_sample_data = sample_data.replace("{", "{{").replace("}", "}}")

    escaped_columns = [
        col.replace("{", "{{").replace("}", "}}") for col in df.columns
    ]
    column_names_str = ", ".join(escaped_columns)



    # Define the prompt for generating the cleaning function
    initial_prompt = PromptTemplate.from_template(f'''
            You are given the following sample data from a pandas DataFrame: 
                {escaped_sample_data}    
              
               column names are : [{column_names_str}].
             
                 Generate a Python function named clean_dataframe(df) considering the following:

                
                1. Performs thorough data cleaning without performing feature engineering. Ensure all necessary cleaning steps are included.
                2. Uses assignment operations (e.g., df = df.drop(...)) and avoids inplace=True for clarity.
                3. First deeply analyze each column’s content this is the most important step , to infer its predominant data type for example if we have RS.2100 in rows remove rs and if we have (89%) remove %  , if the column contains only text and no numbers then it is a text column and if it contains numbers and text then it is a mixed column and if it contains only numbers then it is a numeric column.
                4. For columns that are intended to be numeric but contain extra characters (such as '%' in percentage values, currency symbols like 'Rs.', '$', and commas), remove all non-digit characters (except for the decimal point) and convert them to a numeric type.
                5. For columns that are clearly text or categorical, preserve the content without removing digits or altering the textual information.
                6. Handles missing values appropriately: fill numeric columns with the median (or 0 if the median is not available) and non-numeric columns with 'Unknown'.
                7. For columns where more than 50% of values are strings and less than 10% are numeric, perform conservative string cleaning by removing unwanted special symbols while preserving meaningful digits.
                8. For columns whose names contain 'name', 'Name', or 'Names' (case-insensitive), convert to string type and remove extraneous numeric characters only if they are not part of the essential text.
                9. Preserves other categorical or text columns (such as Gender, City, State, Country, etc.) unless explicitly specified for removal.
                10. Handles edge cases such as completely empty columns appropriately.
                
                Return only the Python code for the function, with no explanations or extra formatting.
                        
               '''
        )



        # Define the refinement prompt
    refine_prompt = PromptTemplate.from_template(
            "The following Python code for cleaning a DataFrame caused an error: {error}\n"
            "Original code:\n{code}\n"
            "Please correct the code to fix the error and ensure it returns a cleaned DataFrame. "
            "Return only the corrected Python code for the function, no explanations or formatting."
        )




        # Create the chains using modern LangChain approach
    initial_chain = initial_prompt | llm
    refine_chain = refine_prompt | llm







    def extract_code(response):
            
            if isinstance(response, str):
                # Handle Markdown or plain text
                if "```python" in response:
                    match = re.search(r'```python\n(.*?)\n```', response, re.DOTALL)
                    return match.group(1).strip() if match else response
                
                elif "```" in response:
                    match = re.search(r'```\n(.*?)\n```', response, re.DOTALL)
                    return match.group(1).strip() if match else response
                
                return response.strip()
            
            # Handle LLM response objects
            content = getattr(response, 'content', str(response))
            
            if "```python" in content:
                match = re.search(r'```python\n(.*?)\n```', content, re.DOTALL)
                return match.group(1).strip() if match else content
            
            elif "```" in content:
                match = re.search(r'```\n(.*?)\n```', content, re.DOTALL)
                return match.group(1).strip() if match else content
            
            return content.strip()
    




    
    
    try:
        # Generate initial chain and extract the cleaned code 
        cleaning_function_code = extract_code(initial_chain.invoke({}))
        print("Initial generated cleaning function code not executed yet is:\n", cleaning_function_code)

    # Iterative refinement loop with max 5 attempts
        max_attempts = 5

        for attempt in range(max_attempts):
            print(f"Attempt {attempt} code:\n{cleaning_function_code}")  # <-- HERE
            try:
                # Execute the code in global namespace
                exec(cleaning_function_code, globals())               
                # Call the function and assign the result back to df


                if 'clean_dataframe' not in globals():
                    raise NameError("Cleaning function not defined in generated code")

                df = clean_dataframe(df)

                print(f"Cleaning successful on attempt {attempt + 1}")
                break
            
            # if the cleaning fails
            except Exception as e:
                error_message = str(e)
                print(f"Error on attempt {attempt + 1}: {error_message}")
            
            if attempt < max_attempts - 1:
                
                # Refine the code using the error message if there are still epochs left                
                refined_response = refine_chain.invoke({"error": error_message, "code": cleaning_function_code})
                cleaning_function_code = extract_code(refined_response)
                
                print(f"Refined cleaning function code:\n", cleaning_function_code)
            
            else:
                print("Failed to clean DataFrame after 5 maximum attempts")
                # AFter all the failed attempt using the hardcoded logic

                df = clean_dataframe_fallback(df)
            
    except Exception as e:
        print("⚡No successful cleaning done enforcing fallback")
        df = clean_dataframe_fallback(df)

    
    cleaned_df = df     


    insights_prompt = f"""
    Analyze this cleaned dataset:
    - Columns: {cleaned_df.columns.tolist()}
    - Sample data: {cleaned_df.head(3).to_dict()}
    - Numeric stats: {cleaned_df.describe().to_dict()}
    Provide key data quality insights and recommendations.
    """
    
    try:
        insights_response = llm.invoke(insights_prompt)
        analysis_insights = insights_response.content    
    except Exception as e:
        analysis_insights = f"Insight generation failed: {str(e)}"



    # Return the cleaned DataFrame and dummy insights
    return cleaned_df, analysis_insights
