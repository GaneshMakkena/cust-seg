# Deployment Guide: Streamlit Cloud

This guide explains how to deploy your **Customer Segmentation Dashboard** to the web using Streamlit Cloud for free.

## 1. Prepare Your Repository
Streamlit Cloud deploys directly from a GitHub repository.

1.  **Create a GitHub Repo**: Go to GitHub and create a new repository (e.g., `customer-segmentation-app`).
2.  **Upload Files**: Upload the entire project folder *or* just the following essential files:
    *   `streamlit_app/` (The entire folder)
    *   `marketing_campaign.xlsx` (The dataset - **Critical**: Must be in the root or accessible path).
    *   `README.md`
    *   `Customer-Segment.ipynb` (Optional, showcasing your work)
3.  **Requirements**: Ensure `streamlit_app/requirements.txt` is present.

## 2. Deploy to Streamlit Cloud
1.  Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
2.  Click **"New app"**.
3.  Select your Repository, Branch (usually `main`), and Main File path.
    *   **Main file path**: `streamlit_app/app.py`
4.  Click **"Deploy!"**.

## 3. Configuration (Crucial)
### File Paths
The app expects `marketing_campaign.xlsx` to be at `../marketing_campaign.xlsx` (relative to `app.py`).
*   **If you upload the dataset to the root of the repo**: The current code `DATA_PATH = "../marketing_campaign.xlsx"` should work fine.
*   **If you get a File Not Found Error**:
    *   Move the excel file inside the `streamlit_app` folder in your repo.
    *   Update `app.py` line 15 to: `DATA_PATH = "marketing_campaign.xlsx"`
    *   Push the changes.

## 4. Verify
Once deployed, click the URL provided by Streamlit. Navigate to the **Profiling** page to verify the Heatmap and Clusters are loading correctly.
