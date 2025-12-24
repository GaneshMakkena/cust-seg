import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

def show_eda_page(df_eda):
    """
    Renders the Exploratory Data Analysis page.
    """
    st.header("Exploratory Data Analysis")
    
    # Key Observations Section
    st.info("""
    **Key Observations:**
    *   **Income**: Right-skewed distribution. **Note**: Extreme outliers (>600k) have been removed to improve clustering.
    *   **Age**: Roughly normal distribution. Outliers (>100 years) have been removed.
    *   **Spending**: Highly positively skewed—most customers spend little, but a "whale" segment exists.
    """)

    st.subheader("Distributions Impacting Segmentation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_inc = px.histogram(df_eda, x="Income", nbins=30, title="Income Distribution")
        st.plotly_chart(fig_inc, use_container_width=True)
        st.caption("*Impact*: High variance in income suggests it will be a strong separator in clustering.")
        
    with col2:
        fig_spend = px.histogram(df_eda, x="TotalSpend", nbins=30, title="Total Spend Distribution")
        st.plotly_chart(fig_spend, use_container_width=True)
        st.caption("*Impact*: Spending patterns often define 'VIP' vs 'Low Value' clusters.")
        
    st.subheader("Correlation Analysis")
    # Compute correlation
    numeric_df = df_eda.select_dtypes(include=['float64', 'int64'])
    corr = numeric_df.corr()
    
    # Heatmap using Plotly
    fig_corr = px.imshow(corr, text_auto=False, aspect="auto", title="Feature Correlations (Heatmap)")
    st.plotly_chart(fig_corr, use_container_width=True)
    st.caption("**Insight**: Strong correlation between Income and TotalSpend confirms that wealthier customers tend to spend more, validitating our segmentation features.")
