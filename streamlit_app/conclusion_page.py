import streamlit as st

def show_conclusion_page():
    """
    Renders the Insights & Conclusion page.
    """
    st.header("Insights & Conclusion")
    
    st.markdown("""
    ### Summary of Analysis
    We identified **4 distinct customer segments** based on their demographics, spending behavior, and campaign engagement.
    
    ### Key Segments
    1.  **Stars (VIPs)**: High income, high spenders. The most crucial segment for revenue.
    2.  **High Potential**: Good income but moderate spending. Prone to upselling.
    3.  **Needs Attention**: Moderate income, low engagement. Requires incentives.
    4.  **Low Value**: Budget-conscious customers with minimal spending.
    
    ### Business Implications
    *   **Targeted Marketing**: Instead of generic blasts, tailor campaigns (Luxury vs Discount) to specific clusters.
    *   **Resource Allocation**: Focus retention budget on 'Stars' and acquisition/growth budget on 'High Potential'.
    *   **Product Development**: Develop specific product bundles for 'Needs Attention' customers (e.g., family packs).
    
    ### Limitations
    *   **Static Data**: This analysis is based on a static snapshot. Customer behavior changes over time.
    *   **Feature Scope**: We focused on demographics and spend. Adding web interaction data could refine segments further.
    """)
