import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler, FunctionTransformer
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
import os

# --- Feature Engineer Class (From Notebook) ---
class FeatureEngineer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()
        # Ensure year_birth is numeric
        # Age
        X["Age"] = 2025 - X["Year_Birth"]
        # TotalChildren
        X["TotalChildren"] = X["Kidhome"] + X["Teenhome"]
        # TotalSpend
        mnt_cols = ["MntWines", "MntFruits", "MntMeatProducts", 
                    "MntFishProducts", "MntSweetProducts", "MntGoldProds"]
        X["TotalSpend"] = X[mnt_cols].sum(axis=1)
        return X

def load_and_preprocess_data(file_path):
    """
    Loads raw data, cleans it (Outliers!), engineers features (Class),
    and prepares it for clustering.
    Replicates logic from Customer-Segment.ipynb.
    """
    if not os.path.exists(file_path):
        return None, None, "File not found"

    # 1. Load Data
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        return None, None, f"Error loading excel file: {e}"

    # 2. Outlier Handling (Professional Standard)
    # Remove extreme outliers as identified in Notebook
    if "Income" in df.columns:
         # Initial Impute for Income just to safely filter (Pipeline does proper impute later)
         # Actually, notebook filtered BEFORE imputing? 
         # Notebook: cleaning -> fillna -> outliers. 
         # But the "Professional" block was inserted AFTER fillna.
         # So we should fillna first essentially, or just drop row if we want to be strict.
         # For app robustness, let's fillna median first so logic doesn't break.
         df['Income'] = df['Income'].fillna(df['Income'].median())
         df = df[df['Income'] < 600000]
         
    if "Year_Birth" in df.columns:
        df = df[df['Year_Birth'] > 1920]

    # 3. Feature Engineering (Pipeline Logic)
    # We apply this immediately to get the human-readable DB for EDA
    fe = FeatureEngineer()
    df_eda = fe.transform(df)

    # --- Add App-Specific "Glossy" Features for Profiling ---
    # These were in the old app and are good for the UI, even if not in the strict model
    if 'Marital_Status' in df_eda.columns:
        df_eda['Living_With'] = df_eda['Marital_Status'].replace({
            'Married': 'Partner', 'Together': 'Partner',
            'Single': 'Alone', 'Divorced': 'Alone', 'Widow': 'Alone', 'Absurd': 'Alone', 'YOLO': 'Alone'
        })
    
    if 'Education' in df_eda.columns:
        # Keep original education for display, maybe map if needed
        pass
    
    if 'Living_With' in df_eda.columns and 'TotalChildren' in df_eda.columns:
        df_eda['Family_Size'] = df_eda['Living_With'].replace({'Alone': 1, 'Partner': 2}).astype(int) + df_eda['TotalChildren']
        df_eda['Is_Parent'] = np.where(df_eda.TotalChildren > 0, 1, 0)

    # 4. Prepare Data for Model
    # Select exactly the features used in the Notebook Pipeline
    final_features = [
        "Age", "Income", "TotalChildren", "TotalSpend",
        "Recency", "NumWebPurchases", "NumCatalogPurchases",
        "NumStorePurchases", "NumWebVisitsMonth"
    ]
    
    # Check if all exist
    missing_cols = [c for c in final_features if c not in df_eda.columns]
    if missing_cols:
        return None, None, f"Missing columns for model: {missing_cols}"

    df_model = df_eda[final_features].copy()
        
    return df, df_eda, df_model

def perform_clustering(df_model, n_clusters=4):
    """
    Applies the Scikit-Learn Pipeline (Imputer -> Scaler) and then KMeans.
    """
    # Pipeline for Preprocessing
    preprocessor = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    # Fit and Transform
    scaled_data = preprocessor.fit_transform(df_model)
    
    # Clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(scaled_data)
    
    # We return the scaler/preprocessor too if we wanted to inverse transform, 
    # but for this app we just need clusters and scaled data for visualization.
    
    return clusters, scaled_data, kmeans
