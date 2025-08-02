import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Load your processed data
df_clusters = pd.read_csv('customer_segmentation - Copy (2).csv')

# --- Add missing columns as in your notebook ---
df_clusters['Age'] = 2025 - df_clusters['Year_Birth']
df_clusters['Total_children'] = df_clusters['Kidhome'] + df_clusters['Teenhome']
df_clusters['Dt_Customer'] = pd.to_datetime(df_clusters['Dt_Customer'], dayfirst=True)
df_clusters['Customer_Since'] = (pd.Timestamp('today') - df_clusters['Dt_Customer']).dt.days

df_clusters['Total_spending'] = df_clusters[['MntWines', 'MntFruits','MntMeatProducts', 'MntFishProducts', 'MntSweetProducts','MntGoldProds']].sum(axis=1)


df_clusters = df_clusters.dropna(subset=[
    'Age', 'Education', 'Total_spending', 'Marital_Status', 'Income', 'Total_children',
    'MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts',
    'MntSweetProducts', 'MntGoldProds', 'NumDealsPurchases',
    'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases',
    'NumWebVisitsMonth', 'Recency', 'Customer_Since'
])


if 'Cluster' not in df_clusters.columns:
    import joblib
    scaler = joblib.load('scaler_model.pkl')
    kmeans = joblib.load('kmeans_model.pkl')
    features = [ 'Age', 'Education','Total_spending','Marital_Status', 'Income', 'Total_children',
        'MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts',
        'MntSweetProducts', 'MntGoldProds', 'NumDealsPurchases',
        'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases',
        'NumWebVisitsMonth', 'Recency', 'Customer_Since']
    x = df_clusters[features].copy()
    x_encoded = pd.get_dummies(x, columns=['Education', 'Marital_Status'], drop_first=True)
    for col in scaler.feature_names_in_:
        if col not in x_encoded.columns:
            x_encoded[col] = 0
    x_encoded = x_encoded[scaler.feature_names_in_]
    X_scaled = scaler.transform(x_encoded)
    df_clusters['Cluster'] = kmeans.predict(X_scaled)

# --- Color palette ---
neon_colors = ['#00FFC6', '#FF00EA', '#00B3FF', '#FFB300', '#FF005C', '#39FF14']

# --- Top Customer Cluster (by spending) ---
top_cluster = df_clusters.groupby('Cluster')['Total_spending'].mean().idxmax()
top_cluster_df = df_clusters[df_clusters['Cluster'] == top_cluster]
top_cluster_card = dbc.Card(
    dbc.CardBody([
        html.H4("Top Customer Cluster", className="card-title", style={'color': neon_colors[1]}),
        html.H2(f"Cluster {top_cluster}", style={'color': neon_colors[0]}),
        html.P(f"Avg. Spending: ${top_cluster_df['Total_spending'].mean():,.0f}", style={'fontSize': 22}),
        html.P(f"Avg. Income: ${top_cluster_df['Income'].mean():,.0f}", style={'fontSize': 18}),
        html.P(f"Avg. Age: {top_cluster_df['Age'].mean():.0f}", style={'fontSize': 18}),
    ]),
    style={"background": "#181A20", "boxShadow": "0 0 16px #00FFC6", "border": "none"}
)

# --- Age vs Spending Scatter ---
scatter_fig = px.scatter(
    df_clusters, x='Age', y='Total_spending', color='Cluster',
    color_discrete_sequence=neon_colors,
    template='plotly_dark',
    hover_data=['Income'],
    title='Age vs Total Spending'
)
scatter_fig.update_traces(marker=dict(size=12, line=dict(width=1, color='#222')), selector=dict(mode='markers'))

# --- Income Distribution by Cluster ---
income_fig = px.box(
    df_clusters, x='Cluster', y='Income', color='Cluster',
    color_discrete_sequence=neon_colors,
    template='plotly_dark',
    title='Income Distribution by Cluster'
)
income_fig.update_traces(marker=dict(line=dict(width=1, color='#fff')))

# --- Cluster Comparison Radar Chart ---
radar_features = ['MntWines', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
radar_df = df_clusters.groupby('Cluster')[radar_features].mean().reset_index()
radar_fig = go.Figure()
for i, row in radar_df.iterrows():
    radar_fig.add_trace(go.Scatterpolar(
        r=row[radar_features].values,
        theta=radar_features,
        fill='toself',
        name=f'Cluster {int(row["Cluster"])}',
        line=dict(color=neon_colors[i % len(neon_colors)], width=3)
    ))
radar_fig.update_layout(
    template='plotly_dark',
    polar=dict(bgcolor='#181A20', radialaxis=dict(showticklabels=True, ticks='')),
    showlegend=True,
    title='Cluster Comparison: Product Spending'
)

# --- Purchasing Behavior Bar Chart ---
purchase_types = ['NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases']
purchase_df = df_clusters.groupby('Cluster')[purchase_types].mean().reset_index()
purchase_fig = go.Figure()
for i, col in enumerate(purchase_types):
    purchase_fig.add_trace(go.Bar(
        x=purchase_df['Cluster'],
        y=purchase_df[col],
        name=col.replace('Num', '').replace('Purchases', ''),
        marker_color=neon_colors[i]
    ))
purchase_fig.update_layout(
    barmode='group',
    template='plotly_dark',
    title='Purchasing Behavior by Channel',
    xaxis_title='Cluster',
    yaxis_title='Avg. Purchases',
    legend_title='Channel'
)

# --- App Layout ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "Customer Insights Dashboard"

app.layout = dbc.Container([
    html.H1("Customer Insights Dashboard", style={
        "color": neon_colors[0], "fontFamily": "Montserrat, Open Sans, sans-serif", "marginTop": 30, "marginBottom": 10, "fontWeight": "bold"
    }),
    dbc.Row([
        dbc.Col(top_cluster_card, width=4),
        dbc.Col(dcc.Graph(figure=scatter_fig, config={'displayModeBar': False}), width=8)
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=income_fig, config={'displayModeBar': False}), width=6),
        dbc.Col(dcc.Graph(figure=radar_fig, config={'displayModeBar': False}), width=6)
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=purchase_fig, config={'displayModeBar': False}), width=12)
    ]),
], fluid=True, style={"background": "#181A20", "paddingBottom": "40px"})

if __name__ == "__main__":
    app.run(debug=True)