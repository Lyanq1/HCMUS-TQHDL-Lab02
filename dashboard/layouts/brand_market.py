from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def create_brand_layout(df):
    # Top brands by revenue
    top_brands = df.groupby('brand').agg({
        'revenue_estimate': 'sum',
        'quantity_sold': 'sum',
        'id': 'count',
        'price': 'mean'
    }).nlargest(10, 'revenue_estimate').reset_index()
    top_brands.columns = ['brand', 'revenue', 'sold', 'products', 'avg_price']

    # OEM vs Branded comparison
    oem_df = df[df['brand'] == 'OEM']
    branded_df = df[df['brand'] != 'OEM']

    comparison = pd.DataFrame({
        'Type': ['OEM', 'Branded'],
        'Products': [len(oem_df), len(branded_df)],
        'Avg Price': [oem_df['price'].mean(), branded_df['price'].mean()],
        'Total Revenue': [oem_df['revenue_estimate'].sum(), branded_df['revenue_estimate'].sum()],
        'Avg Sales': [oem_df['quantity_sold'].mean(), branded_df['quantity_sold'].mean()]
    })

    # Brand concentration
    brand_revenue = df.groupby('brand')['revenue_estimate'].sum().sort_values(ascending=False)
    top_10_share = (brand_revenue.head(10).sum() / brand_revenue.sum() * 100)

    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H3("Brand & Market Structure"),
                html.P(f"Key Insight: OEM products are 73.8% of catalog, but branded products have 4.1x higher price. Top 10 brands control {top_10_share:.1f}% of revenue",
                       className="text-muted")
            ])
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{len(oem_df):,}", className="text-secondary"),
                        html.P("OEM Products", className="mb-0"),
                        html.Small(f"{len(oem_df)/len(df)*100:.1f}% of catalog", className="text-muted")
                    ])
                ], className="h-100")
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{len(branded_df):,}", className="text-primary"),
                        html.P("Branded Products", className="mb-0"),
                        html.Small(f"{len(branded_df)/len(df)*100:.1f}% of catalog", className="text-muted")
                    ])
                ], className="h-100")
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{branded_df['price'].mean()/oem_df['price'].mean():.1f}x", className="text-success"),
                        html.P("Price Premium", className="mb-0"),
                        html.Small("Branded vs OEM", className="text-muted")
                    ])
                ], className="h-100")
            ], width=4),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=px.bar(
                        top_brands,
                        y='brand',
                        x='revenue',
                        orientation='h',
                        title="Top 10 Brands by Revenue",
                        labels={'brand': '', 'revenue': 'Revenue (VND)'},
                        color='revenue',
                        color_continuous_scale='Teal'
                    ).update_layout(showlegend=False, height=400)
                )
            ], width=6),
            dbc.Col([
                dcc.Graph(
                    figure=go.Figure(data=[
                        go.Bar(name='OEM', x=['Products', 'Avg Price', 'Avg Sales'],
                               y=[comparison.loc[0, 'Products'], comparison.loc[0, 'Avg Price']/1000, comparison.loc[0, 'Avg Sales']],
                               marker_color='lightcoral'),
                        go.Bar(name='Branded', x=['Products', 'Avg Price', 'Avg Sales'],
                               y=[comparison.loc[1, 'Products'], comparison.loc[1, 'Avg Price']/1000, comparison.loc[1, 'Avg Sales']],
                               marker_color='lightblue')
                    ]).update_layout(
                        title='OEM vs Branded Comparison (Price in 1000 VND)',
                        barmode='group',
                        yaxis_title='Value'
                    )
                )
            ], width=6),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=px.scatter(
                        top_brands,
                        x='products',
                        y='revenue',
                        size='sold',
                        color='brand',
                        title="Top Brands: Product Count vs Revenue (size = units sold)",
                        labels={'products': 'Product Count', 'revenue': 'Revenue (VND)'}
                    )
                )
            ], width=12),
        ])
    ], fluid=True)
