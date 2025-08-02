# Customer Insights Dashboard

This project provides an interactive dashboard for customer segmentation and analysis using Dash and Plotly. The dashboard visualizes customer clusters, spending patterns, income distribution, and purchasing behaviors.

---

## Features

- **Top Customer Cluster**: Highlights the cluster with the highest average spending.
- **Age vs Spending Scatter Plot**: Visualizes the relationship between customer age and total spending.
- **Income Distribution by Cluster**: Compares income across clusters.
- **Cluster Comparison Radar Chart**: Shows average product spending per cluster.
- **Purchasing Behavior**: Compares store, web, and catalog purchases by cluster.

---

## How to Run

1. **Install requirements**  
   Make sure you have Python 3.8+ and run:
   ```
   pip install dash dash-bootstrap-components plotly pandas scikit-learn joblib
   ```

2. **Prepare your data**  
   Ensure your data file (`customer_segmentation - Copy (2).csv`) is in the project folder.

3. **Start the dashboard**  
   In your terminal, run:
   ```
   python dashboard.py
   ```

4. **Open the dashboard in your browser**  
   - For the Dash dashboard:  
     [http://127.0.0.1:8050/](http://127.0.0.1:8050/)
   - For the Streamlit app (if you use it):  
     [http://localhost:8501/](http://localhost:8501/)

---

## Notes

- The dashboard uses a dark, neon-themed layout for modern and clear visualization.
- If you encounter errors about missing columns, make sure your CSV matches the columns used in the code or preprocess your data as in the notebook.
- For large datasets, consider sampling your data for faster loading.

---

## Screenshots

_Add screenshots of your dashboard# customer-segmentation-analysis
