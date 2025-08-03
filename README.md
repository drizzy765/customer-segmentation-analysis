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
   ### Streamlit App – Predict Customer Segments  
[Launch App](https://customer-segmentation-analysis-5fyjxuwsk8umayf5q3slzz.streamlit.app)  
Enter customer data and get real-time segment predictions powered by a trained KMeans model.

### Dash Dashboard – Visualize Segments  
[View Dashboard](https://customer-segmentation-dashboard-vkmx.onrender.com)  
Explore data distributions, cluster characteristics, and behavioral insights.

---

## Notes

- The dashboard uses a dark, neon-themed layout for modern and clear visualization.
- If you encounter errors about missing columns, make sure your CSV matches the columns used in the code or preprocess your data as in the notebook.
- For large datasets, consider sampling your data for faster loading.

---


