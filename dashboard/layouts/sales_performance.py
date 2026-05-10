from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_sales_layout(df):
    # Top performers
    top_products = df.nlargest(20, 'quantity_sold').copy()
    top_products['short_name'] = top_products['name'].str[:40] + '...'

    # Top by revenue
    top_revenue = df.nlargest(10, 'revenue_estimate').copy()
    top_revenue['short_name'] = top_revenue['name'].str[:30] + '...'

    # Sales distribution
    sales_bins = [0, 10, 50, 100, 500, float('inf')]
    sales_labels = ['0-10', '10-50', '50-100', '100-500', '>500']
    df_copy = df.copy()
    df_copy['sales_range'] = pd.cut(df_copy['quantity_sold'], bins=sales_bins, labels=sales_labels)
    sales_dist = df_copy['sales_range'].value_counts().sort_index()

    # Category performance
    cat_perf = df.groupby('category').agg({
        'quantity_sold': 'sum',
        'revenue_estimate': 'sum'
    }).reset_index()

    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H3("Sales Performance Analysis"),
                html.P("Top 100 products (0.24%) generate 31.8% of total revenue", className="text-muted")
            ])
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=px.bar(
                        top_products.head(10),
                        y='short_name',
                        x='quantity_sold',
                        orientation='h',
                        title="Top 10 Best Sellers by Volume",
                        labels={'short_name': '', 'quantity_sold': 'Units Sold'},
                        color='quantity_sold',
                        color_continuous_scale='Blues'
                    ).update_layout(showlegend=False, height=400)
                )
            ], width=6),
            dbc.Col([
                dcc.Graph(
                    figure=px.bar(
                        top_revenue,
                        y='short_name',
                        x='revenue_estimate',
                        orientation='h',
                        title="Top 10 Products by Revenue",
                        labels={'short_name': '', 'revenue_estimate': 'Revenue (VND)'},
                        color='revenue_estimate',
                        color_continuous_scale='Greens'
                    ).update_layout(showlegend=False, height=400)
                )
            ], width=6),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=px.bar(
                        x=sales_dist.index,
                        y=sales_dist.values,
                        title="Sales Distribution (Product Count)",
                        labels={'x': 'Sales Range', 'y': 'Products'},
                        color=sales_dist.values,
                        color_continuous_scale='Oranges'
                    ).update_layout(showlegend=False)
                )
            ], width=6),
            dbc.Col([
                dcc.Graph(
                    figure=px.bar(
                        cat_perf,
                        x='category',
                        y='quantity_sold',
                        title="Total Sales by Category",
                        labels={'category': 'Category', 'quantity_sold': 'Total Units Sold'},
                        color='quantity_sold',
                        color_continuous_scale='Purples'
                    ).update_xaxes(tickangle=-45).update_layout(showlegend=False)
                )
            ], width=6),
        ])
    ], fluid=True)
