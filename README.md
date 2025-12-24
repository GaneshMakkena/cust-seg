# Customer Segmentation Analysis & Dashboard

## 📊 Project Overview
This project performs unsupervised machine learning (K-Means Clustering) on customer data to identify distinct segments and tailored marketing strategies. It consists of two main components:
1.  **Jupyter Notebook**: A deep-dive analysis (EDA, Outlier Handling, Pipeline, Modeling, Evaluation).
2.  **Streamlit Dashboard**: An interactive web app for business stakeholders to explore segments and view recommendations.

## 📁 Key Files
*   `Customer-Segment.ipynb`: The main analysis notebook. Contains the complete data science workflow (Data Cleaning -> Feature Engineering -> K-Means -> Profiling).
*   `marketing_campaign.xlsx`: The dataset used for analysis.
*   `streamlit_app/`: Folder containing the source code for the interactive dashboard.
    *   `app.py`: Main application entry point.
    *   `data_processor.py`: Backend logic for data cleaning and pipeline transformation.

## 🚀 How to Run

### Prerequisities
*   Python 3.8+
*   Install dependencies:
    ```bash
    pip install -r streamlit_app/requirements.txt
    ```

### 1. Running the Analysis (Notebook)
Open `Customer-Segment.ipynb` in Jupyter Lab or VS Code.
```bash
jupyter notebook Customer-Segment.ipynb
```
Run all cells to regenerate the analysis, visualizations, and cluster profiles.

### 2. Running the Dashboard (App)
Navigate to the project directory and run:
```bash
streamlit run streamlit_app/app.py
```
The app will open in your browser at `http://localhost:8501`.

## 💡 Key Insights
The analysis identified **4 Customer Segments**:
1.  **Stars (VIPs)**: High Income, High Spend. Target with loyalty programs.
2.  **High Potential**: Above average income, parents. Target with family bundles.
3.  **Needs Attention**: Low spend, frequent visits. Target with coupons.
4.  **Low Value**: Minimal engagement. Maintain brand awareness.

See the **Profiling** page in the app for a detailed "Relative Importance Heatmap".
