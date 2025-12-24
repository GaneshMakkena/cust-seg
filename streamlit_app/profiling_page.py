import streamlit as st
import plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def show_profiling_page(df_with_clusters):
    """
    Shows detailed profile of the segments with business interpretations.
    Includes Relative Importance Heatmap.
    """
    st.header("Segment Profiling & Recommendations")
    
    if df_with_clusters is None or 'Cluster' not in df_with_clusters.columns:
        st.warning("Please verify data processing.")
        return

    # --- 1. Relative Importance Heatmap (New feature from Notebook) ---
    st.subheader("Strategic Overview: Relative Importance Heatmap")
    st.markdown("""
    This heatmap shows how each cluster differs from the **average customer**.  
    *   **Red**: Higher than average (e.g., +0.5 means 50% higher).
    *   **Blue**: Lower than average.
    """)
    
    # Calculate Relative Importance
    # Group by Cluster (ID) first
    cluster_avg = df_with_clusters.groupby('Cluster')[['Income', 'TotalSpend', 'Recency', 'Age', 'TotalChildren']].mean()
    population_avg = df_with_clusters[['Income', 'TotalSpend', 'Recency', 'Age', 'TotalChildren']].mean()
    relative_imp = cluster_avg / population_avg - 1
    
    # Plot using Seaborn
    fig_heatmap, ax = plt.subplots(figsize=(10, 5))
    sns.heatmap(relative_imp, annot=True, fmt='.2f', cmap='RdBu_r', center=0, ax=ax)
    plt.title("Relative Importance of Features by Cluster")
    st.pyplot(fig_heatmap)
    
    st.divider()

    # --- 2. Existing Profiling Logic ---
    
    # Calculate metrics for logic-based naming
    summary = df_with_clusters.groupby('Cluster').agg({
        'Income': 'mean',
        'TotalSpend': 'mean',
        'Age': 'mean',
        'TotalChildren': 'mean',
        'Recency': 'mean'
    }).reset_index()
    
    # Identifying clusters by logic to be deterministic regardless of label swap
    # Sort by TotalSpend to consistently identify tiers
    summary_sorted = summary.sort_values(by='TotalSpend', ascending=False)
    
    # Logic to map cluster ID to profile
    # Rank 0 = Top Spenders, Rank 3 = Lowest Spenders
    profile_map = {}
    ranks = range(len(summary_sorted))
    
    for rank, (index, row) in zip(ranks, summary_sorted.iterrows()):
        cluster_id = int(row['Cluster'])
        
        if rank == 0:
            name = "Stars (VIPs)"
            desc = [
                "High Income, High Spending.",
                "Low number of children.",
                "Responsive to campaigns."
            ]
            rec = "Offer exclusive premium loyalty programs and priority support."
        elif rank == 1:
            name = "High Potential"
            desc = [
                "Above average income.",
                "Moderate spending, potential to grow.",
                "Often middle-aged professionals."
            ]
            rec = "Upsell higher-margin products and use personalized email marketing."
        elif rank == 2:
            name = "Needs Attention"
            desc = [
                "Moderate to Low Income.",
                "Low Spending.",
                "Recent engagement varies."
            ]
            rec = "Use discounts and coupons to stimulate purchase frequency."
        else: # Rank 3
            name = "Low Value / At Risk"
            desc = [
                "Low Income.",
                "Very Low Spending.",
                "Often younger or much older with budget constraints."
            ]
            rec = "Focus on minimal cost retention or basic brand awareness."
            
        profile_map[cluster_id] = {
            "name": name,
            "desc": desc,
            "rec": rec,
            "stats": row
        }

    # Display Profiles
    st.subheader("Cluster Profiles")
    
    col_layout = st.columns(len(profile_map))
    
    # Iterate through sorted ranking for display consistency
    for i, (_, row) in enumerate(summary_sorted.iterrows()):
        c_id = int(row['Cluster'])
        p = profile_map[c_id]
        
        with col_layout[i]:
            st.markdown(f"### Cluster {c_id}")
            st.markdown(f"**{p['name']}**")
            st.write("---")
            for d in p['desc']:
                st.write(f"- {d}")
            st.write("---")
            st.info(f"💡 **Recommendation**: {p['rec']}")
            st.write(f"**Avg Income**: ${p['stats']['Income']:,.0f}")
            st.write(f"**Avg Spend**: ${p['stats']['TotalSpend']:,.0f}")

    st.divider()

    st.subheader("Comparative Statistics")
    st.dataframe(summary.style.format("{:.1f}").background_gradient(cmap="Blues"))
    
    st.subheader("Feature Deep Dive")
    feature_to_plot = st.selectbox("Select Feature", ['Income', 'TotalSpend', 'Age', 'Recency', 'TotalChildren'])
    
    fig_box = px.box(df_with_clusters, x="Cluster", y=feature_to_plot, color="Cluster", title=f"Distribution of {feature_to_plot} by Cluster")
    st.plotly_chart(fig_box, use_container_width=True)
