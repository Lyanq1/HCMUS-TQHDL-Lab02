import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Initialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "TIKI Fashion Analytics Dashboard"

# Load data
data_path = Path(__file__).parent.parent / 'data' / 'processed'
df = pd.read_csv(data_path / 'combined_tiki_data.csv')

# Feature engineering
df['discount_pct'] = ((df['original_price'] - df['price']) / df['original_price'] * 100).round(2)
df['revenue_estimate'] = df['price'] * df['quantity_sold']
df['price_segment'] = pd.cut(df['price'],
                              bins=[0, 100000, 300000, 500000, 1000000, float('inf')],
                              labels=['0-100k', '100-300k', '300-500k', '500k-1M', '>1M'])

# Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("TIKI Fashion Analytics Dashboard", className="text-center mb-4 mt-4"),
            html.P("Interactive data visualization for TIKI e-commerce fashion products",
                   className="text-center text-muted mb-4")
        ])
    ]),

    dbc.Tabs([
        dbc.Tab(label="Overview", tab_id="overview"),
        dbc.Tab(label="Price Analysis", tab_id="price"),
        dbc.Tab(label="Sales Performance", tab_id="sales"),
        dbc.Tab(label="Brand & Market", tab_id="brand"),
        dbc.Tab(label="Customer Engagement", tab_id="engagement"),
        dbc.Tab(label="Deep Dive", tab_id="deepdive"),
        dbc.Tab(label="AI Assistant", tab_id="ai")
    ], id="tabs", active_tab="overview"),

    html.Div(id="tab-content", className="mt-4")
], fluid=True)

# Callback for tab content
@app.callback(Output("tab-content", "children"), Input("tabs", "active_tab"))
def render_tab_content(active_tab):
    if active_tab == "overview":
        from layouts.overview import create_overview_layout
        return create_overview_layout(df)
    elif active_tab == "price":
        from layouts.price_analysis import create_price_layout
        return create_price_layout(df)
    elif active_tab == "sales":
        from layouts.sales_performance import create_sales_layout
        return create_sales_layout(df)
    elif active_tab == "brand":
        from layouts.brand_market import create_brand_layout
        return create_brand_layout(df)
    elif active_tab == "engagement":
        from layouts.customer_engagement import create_engagement_layout
        return create_engagement_layout(df)
    elif active_tab == "deepdive":
        from layouts.deep_dive import create_deepdive_layout
        return create_deepdive_layout(df)
    elif active_tab == "ai":
        from layouts.ai_assistant import create_ai_layout
        return create_ai_layout(df)

# Callback for deep dive chart
@app.callback(Output("deepdive-chart", "figure"), Input("category-filter", "value"))
def update_deepdive_chart(category):
    filtered_df = df[df['category'] == category]
    fig = px.scatter(
        filtered_df.sample(min(1000, len(filtered_df))),
        x='price',
        y='quantity_sold',
        color='brand',
        title=f"Price vs Sales for {category}",
        labels={'price': 'Price (VND)', 'quantity_sold': 'Quantity Sold'}
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True, port=8050)
