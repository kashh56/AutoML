import re
import pandas as pd
import numpy as np
import streamlit as st

# Define fallback cleaning function

@st.cache_data
def clean_dataframe_fallback(df):
        """Hardcoded data cleaning pipeline"""
    
        """Generic data cleaning pipeline with categorical preservation"""
        df_cleaned = df.copy()


        df_cleaned = df_cleaned.applymap(
        lambda x: re.sub(r"\(.*?\)", "", str(x)) if isinstance(x, str) else x)

        # Remove 'ref.' references
        df_cleaned = df_cleaned.applymap(
            lambda x: re.sub(r"ref\.", "", str(x), flags=re.IGNORECASE) if isinstance(x, str) else x)
        
        # Remove any other special characters except letters, digits, spaces, and dots
        df_cleaned = df_cleaned.applymap(
            lambda x: re.sub(r"[^\w\s\d\.]", "", str(x)).strip() if isinstance(x, str) else x
        )


        # Step 0 - Clean column names first
        df_cleaned.columns = [col.strip().lower().replace(' ', '_') for col in df_cleaned.columns]
        
            # Define measurement units to remove
        measurement_units = {
            'weight': r'\s*(kg|kilograms|lbs|pounds)$',
            'height': r'\s*(cm|centimeters|inches|feet|ft)$'
        }


        # Step 1 - Remove redundant columns
        # Preservation patterns for categorical columns
        preserve_pattern = re.compile(r'(name|brand|model|type|category|region|text|desc|color|size)', re.IGNORECASE)
        preserved_cols = [col for col in df_cleaned.columns if preserve_pattern.search(col)]
        
        # ID pattern detection
        id_pattern = re.compile(r'(_id|id_|num|no|number|identifier|code|idx|row)', re.IGNORECASE)
        id_cols = [col for col in df_cleaned.columns if id_pattern.search(col) and col not in preserved_cols]
        
        # Unique value columns
        unique_cols = [col for col in df_cleaned.columns 
                    if df_cleaned[col].nunique() == len(df_cleaned) 
                    and col not in preserved_cols]
        
        redundant_cols = list(set(id_cols + unique_cols))
        df_cleaned = df_cleaned.drop(columns=redundant_cols)
        print(f"Removed {len(redundant_cols)} redundant columns: {redundant_cols}")

        # Step 2 - Enhanced numeric detection with categorical protection
        for col in df_cleaned.columns:
            if col in preserved_cols:
                print(f"Preserving categorical column: {col}")
                continue  # Skip preserved columns

            if any(unit in col for unit in measurement_units.keys()):  
                pattern = measurement_units.get(col.split('_')[0], r'')
                df_cleaned[col] = df_cleaned[col].astype(str).str.replace(pattern, '', regex=True).str.strip()
                            


            if pd.api.types.is_numeric_dtype(df_cleaned[col]):
                continue
                
            # Strict numeric pattern detection
            non_null_count = df_cleaned[col].dropna().shape[0]
            sample_size = min(100, non_null_count)
            sample = df_cleaned[col].dropna().sample(sample_size, random_state=42)
            numeric_pattern = r'^[-+]?\d*\.?\d+$'  # Full string match
            num_matches = sample.astype(str).str.fullmatch(numeric_pattern).mean()
                
            if num_matches > 0.8:  # High threshold
                # Conservative cleaning
                cleaned = df_cleaned[col].replace(r'[^\d\.\-]', '', regex=True)
                converted = pd.to_numeric(cleaned, errors='coerce')
                success_rate = converted.notna().mean()
                
                if success_rate > 0.9:  # Strict success requirement
                    df_cleaned[col] = converted
                    print(f"Converted {col} to numeric (success: {success_rate:.1%})")

        # Step 3 - Date detection
        date_cols = []
        for col in df_cleaned.select_dtypes(exclude=np.number).columns:
            if col in preserved_cols:
                continue
            try:
                df_cleaned[col] = pd.to_datetime(df_cleaned[col], errors='raise')
                date_cols.append(col)
                print(f"Detected datetime: {col}")
            except:
                pass

# Example manual approach:
        currency_cols = [col for col in df_cleaned.columns if any(keyword in col.lower() for keyword in ["price", "gross", "budget"])]
        for col in currency_cols:
            df_cleaned[col] = df_cleaned[col].astype(str).str.replace(r'[^\d\.]', '', regex=True)  # remove everything except digits & dots
            df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')



        # Step 4 - Missing value handling
        numeric_cols = df_cleaned.select_dtypes(include=np.number).columns
        categorical_cols = df_cleaned.select_dtypes(exclude=np.number).columns
        
        # Numeric imputation
        for col in numeric_cols:
            if df_cleaned[col].isna().any():
                df_cleaned[f'{col}_missing'] = df_cleaned[col].isna().astype(int)
                df_cleaned[col].fillna(df_cleaned[col].median(), inplace=True)
        
        # Categorical imputation
        for col in categorical_cols:
            if df_cleaned[col].isna().any():
                mode_val = df_cleaned[col].mode()[0] if not df_cleaned[col].mode().empty else 'Unknown'
                df_cleaned[col] = df_cleaned[col].fillna(mode_val)

        # Step 5 - Text normalization for non-preserved columns
        text_cols = [col for col in categorical_cols if col not in preserved_cols]
        for col in text_cols:
            df_cleaned[col] = df_cleaned[col].astype(str).apply(lambda x: re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', x)).strip().lower())
            
        
        # Step 6 - Outlier handling (preserve categoricals)
        numeric_cols = df_cleaned.select_dtypes(include=np.number).columns
        for col in numeric_cols:
            if df_cleaned[col].nunique() > 10:
                q1 = df_cleaned[col].quantile(0.05)
                q3 = df_cleaned[col].quantile(0.95)
                df_cleaned[col] = np.clip(df_cleaned[col], q1, q3)

        # Step 7 - Final validation
        df_cleaned = df_cleaned.drop_duplicates().reset_index(drop=True)
        
        return df_cleaned
    