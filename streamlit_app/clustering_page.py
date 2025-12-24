import streamlit as st
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from data_processor import perform_clustering

def show_clustering_page(df, df_model):
    """
    Renders clustering analysis visualization with fixed k=4.
    """
    st.header("Customer Segmentation Clustering")
    
    st.markdown("""
    **Model Selection:**
    KMeans clustering was chosen for its efficiency and interpretability. 
    
    **Hyperparameter Tuning:**
    Based on **Elbow Method** and **Silhouette Analysis** (performed during analysis phase), the optimal number of clusters was determined to be **k = 4**. This balances segmentation granularity with practical business usability.
    """)
    
    # Perform Clustering with fixed k=4
    # Note: In a production app, we might load a saved model, but here we re-run for simplicity as per instructions.
    clusters, scaled_data, kmeans = perform_clustering(df_model, n_clusters=4)
    
    # Add cluster labels to the original dataframe for visualization
    df_vis = df.copy()
    df_vis['Cluster'] = clusters
    
    st.subheader("Cluster Visualization (k=4)")
    
    # Cluster Distribution
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("**Cluster Sizes**")
        cluster_counts = df_vis['Cluster'].value_counts().reset_index()
        cluster_counts.columns = ['Cluster', 'Count']
        fig_bar = px.bar(cluster_counts, x='Cluster', y='Count', color='Cluster', title="Count")
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.write("**Cluster Separation**")
        fig_scatter = px.scatter(
            df_vis, 
            x='Income', 
            y='TotalSpend', 
            color='Cluster', 
            hover_data=['Age', 'Family_Size'],
            title="Income vs Total Spend (Key Differentiators)"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # 3D Scatter
    st.write("### Multi-Dimensional View")
    if all(col in df_vis.columns for col in ['Income', 'TotalSpend', 'Recency']):
        fig_3d = px.scatter_3d(
            df_vis, 
            x='Income', 
            y='TotalSpend', 
            z='Recency',
            color='Cluster',
            title="3D View: Income, Spend, and Recency"
        )
        st.plotly_chart(fig_3d, use_container_width=True)
        
    return df_vis # Return dataframe with clusters for profiling page
