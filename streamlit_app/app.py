import streamlit as st
import pandas as pd
from data_processor import load_and_preprocess_data, perform_clustering
from eda_page import show_eda_page
from clustering_page import show_clustering_page
from profiling_page import show_profiling_page
from conclusion_page import show_conclusion_page
import os

# Set Process Layout
st.set_page_config(page_title="Customer Segmentation Dashboard", layout="wide")

# --- Data Loading (Global) ---
# Data is loaded once. Model training/clustering happens only when needed but here strictly separate from Nav.
DATA_PATH = "../marketing_campaign.xlsx"

@st.cache_data
def get_data():
    if os.path.exists(DATA_PATH):
        return load_and_preprocess_data(DATA_PATH)
    else:
        # Fallback for checking if run from app folder
        alt_path = "marketing_campaign.xlsx"
        if os.path.exists(alt_path):
             return load_and_preprocess_data(alt_path)
        return None, None, None

df, df_eda, df_model = get_data()

# --- Pre-calculate Clusters (One-time) ---
if df is not None and 'clustered_df' not in st.session_state:
    # Perform clustering ONCE on startup/load with FIXED k=4
    clusters, _, _ = perform_clustering(df_model, n_clusters=4)
    # Store result in session state
    df_result = df_eda.copy()
    df_result['Cluster'] = clusters
    st.session_state['clustered_df'] = df_result

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "EDA", "Clustering", "Profiling", "Conclusion"])

# --- Page Logic ---

if df is None:
    st.error(f"Could not load data. Please ensure 'marketing_campaign.xlsx' is in the project root or app folder.")
else:
    if page == "Home":
        st.title("Customer Segmentation Dashboard")
        st.markdown("### Objective")
        st.write("To identify distinct customer segments for targeted marketing strategies using unsupervised machine learning.")
        
        st.markdown("### Dataset")
        st.write("Source: `marketing_campaign.xlsx` (2240 records, 29 features).")
        
        st.markdown("### Application Overview")
        st.info("""
        *   **EDA**: Understand data distributions and correlations.
        *   **Clustering**: Visualize customer segments (KMeans, k=4).
        *   **Profiling**: actionable business profiles and recommendations.
        *   **Conclusion**: Summary of insights and strategic next steps.
        """)
        
    elif page == "EDA":
        show_eda_page(df_eda)
        
    elif page == "Clustering":
        # Pass the pre-clustered dataframe or just the raw data if the page handles visualization? 
        # The page function expects df and df_model to visualize. 
        # However, to be CONSISTENT with 'clustering_page.py' refactor (which runs clustering for 'live' feel but fixed k),
        # we can pass it there. But ideally we use the session state one to ensure Profiling sees the SAME clusters.
        # Let's Modify clustering_page to accept the result OR run it deterministically.
        # Given it's deterministic (random_state=42), running it again is safe.
        show_clustering_page(df_eda, df_model)
            
    elif page == "Profiling":
        show_profiling_page(st.session_state['clustered_df'])
        
    elif page == "Conclusion":
        show_conclusion_page()
