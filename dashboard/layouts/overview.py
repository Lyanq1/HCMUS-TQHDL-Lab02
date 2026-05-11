from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

def create_overview_layout(df):
    # Key metrics
    total_products = len(df)
    total_revenue = df['revenue_estimate'].sum()
    total_sold = df['quantity_sold'].sum()
    avg_price = df['price'].mean()
    avg_rating = df[df['rating_average'] > 0]['rating_average'].mean()
    total_brands = df['brand'].nunique()

    # Category analysis
    cat_stats = df.groupby('category').agg({
        'revenue_estimate': 'sum',
        'quantity_sold': 'sum',
        'id': 'count'
    }).reset_index()
    cat_stats.columns = ['category', 'revenue', 'sold', 'products']

    # Price segment revenue
    seg_revenue = df.groupby('price_segment')['revenue_estimate'].sum().reset_index()

    return dbc.Container([
        # KPI Cards
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{total_products:,}", className="text-primary"),
                        html.P("Products", className="mb-0"),
                        html.Small(f"{total_brands} brands", className="text-muted")
                    ])
                ], className="h-100")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{total_revenue/1e9:.1f}B", className="text-success"),
                        html.P("Revenue (VND)", className="mb-0"),
                        html.Small(f"Avg: {total_revenue/total_products/1000:.0f}k/product", className="text-muted")
                    ])
                ], className="h-100")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{total_sold:,}", className="text-info"),
                        html.P("Units Sold", className="mb-0"),
                        html.Small(f"Avg: {total_sold/total_products:.1f}/product", className="text-muted")
                    ])
                ], className="h-100")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{avg_price/1000:.0f}k", className="text-warning"),
                        html.P("Avg Price (VND)", className="mb-0"),
                        html.Small(f"Rating: {avg_rating:.2f}/5", className="text-muted")
                    ])
                ], className="h-100")
            ], width=3),
        ], className="mb-4"),

        # Charts
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=px.bar(
                        cat_stats,
                        x='category',
                        y='revenue',
                        title="Revenue by Category",
                        labels={'category': '', 'revenue': 'Revenue (VND)'},
                        color='revenue',
                        color_continuous_scale='Viridis'
                    ).update_xaxes(tickangle=-45).update_layout(showlegend=False)
                )
            ], width=6),
            dbc.Col([
                dcc.Graph(
                    figure=px.pie(
                        seg_revenue,
                        names='price_segment',
                        values='revenue_estimate',
                        title="Revenue Distribution by Price Segment",
                        hole=0.4
                    )
                )
            ], width=6),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=px.scatter(
                        cat_stats,
                        x='products',
                        y='revenue',
                        size='sold',
                        color='category',
                        text='category',
                        title="Category Performance: Products vs Revenue (bubble size = units sold)",
                        labels={'products': 'Product Count', 'revenue': 'Revenue (VND)'},
                        size_max=60
                    ).update_traces(
                        textposition='top center',
                        textfont_size=10,
                        marker=dict(line=dict(width=2, color='white'))
                    ).update_layout(height=450)
                )
            ], width=6),
            dbc.Col([
                dcc.Graph(
                    figure=go.Figure(data=[
                        go.Bar(name='Revenue (B VND)', x=cat_stats['category'],
                               y=cat_stats['revenue']/1e9, marker_color='lightseagreen'),
                        go.Bar(name='Products (x100)', x=cat_stats['category'],
                               y=cat_stats['products']/100, marker_color='lightcoral'),
                        go.Bar(name='Sales (x1000)', x=cat_stats['category'],
                               y=cat_stats['sold']/1000, marker_color='lightskyblue')
                    ]).update_layout(
                        title='Category Metrics Comparison (normalized)',
                        barmode='group',
                        xaxis_tickangle=-45,
                        height=450,
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                    )
                )
            ], width=6),
        ])
    ], fluid=True)
