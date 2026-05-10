from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

def create_engagement_layout(df):
    # Review impact analysis
    review_bins = [0, 10, 50, 100, 500, float('inf')]
    review_labels = ['0-10', '10-50', '50-100', '100-500', '>500']
    df_copy = df.copy()
    df_copy['review_range'] = pd.cut(df_copy['review_count'], bins=review_bins, labels=review_labels)

    review_impact = df_copy.groupby('review_range').agg({
        'quantity_sold': 'mean',
        'revenue_estimate': 'mean',
        'rating_average': 'mean',
        'id': 'count'
    }).reset_index()
    review_impact.columns = ['review_range', 'avg_sold', 'avg_revenue', 'avg_rating', 'product_count']

    # Engagement metrics
    high_engagement = df[df['review_count'] >= 50]
    low_engagement = df[df['review_count'] < 10]

    # Rating distribution
    rating_dist = df[df['rating_average'] > 0].groupby(pd.cut(df[df['rating_average'] > 0]['rating_average'],
                                                                bins=[0, 2, 3, 4, 4.5, 5],
                                                                labels=['0-2', '2-3', '3-4', '4-4.5', '4.5-5'])).size().reset_index()
    rating_dist.columns = ['rating_range', 'count']

    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H3("Customer Engagement Analysis"),
                html.P("Key Insight: Products with 50+ reviews sell 26.8x more than products with <10 reviews (correlation: 0.621)",
                       className="text-muted")
            ])
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{len(high_engagement):,}", className="text-success"),
                        html.P("High Engagement", className="mb-0"),
                        html.Small("50+ reviews", className="text-muted")
                    ])
                ], className="h-100")
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{len(low_engagement):,}", className="text-warning"),
                        html.P("Low Engagement", className="mb-0"),
                        html.Small("<10 reviews", className="text-muted")
                    ])
                ], className="h-100")
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{high_engagement['quantity_sold'].mean()/low_engagement['quantity_sold'].mean():.1f}x", className="text-info"),
                        html.P("Sales Multiplier", className="mb-0"),
                        html.Small("High vs Low engagement", className="text-muted")
                    ])
                ], className="h-100")
            ], width=4),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=px.bar(
                        review_impact,
                        x='review_range',
                        y='avg_sold',
                        title="Review Count Impact on Average Sales",
                        labels={'review_range': 'Review Count', 'avg_sold': 'Avg Units Sold'},
                        color='avg_sold',
                        color_continuous_scale='YlOrRd',
                        text='avg_sold'
                    ).update_traces(texttemplate='%{text:.1f}', textposition='outside').update_layout(showlegend=False)
                )
            ], width=6),
            dbc.Col([
                dcc.Graph(
                    figure=px.bar(
                        rating_dist,
                        x='rating_range',
                        y='count',
                        title="Rating Distribution (products with ratings)",
                        labels={'rating_range': 'Rating Range', 'count': 'Product Count'},
                        color='count',
                        color_continuous_scale='Greens'
                    ).update_layout(showlegend=False)
                )
            ], width=6),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=px.scatter(
                        df[df['review_count'] > 0].sample(min(3000, len(df[df['review_count'] > 0]))),
                        x='review_count',
                        y='quantity_sold',
                        color='rating_average',
                        title="Reviews vs Sales (colored by rating)",
                        labels={'review_count': 'Review Count', 'quantity_sold': 'Quantity Sold', 'rating_average': 'Rating'},
                        log_x=True,
                        log_y=True
                    )
                )
            ], width=6),
            dbc.Col([
                dcc.Graph(
                    figure=px.bar(
                        review_impact,
                        x='review_range',
                        y='product_count',
                        title="Product Distribution by Review Count",
                        labels={'review_range': 'Review Count', 'product_count': 'Products'},
                        color='product_count',
                        color_continuous_scale='Blues'
                    ).update_layout(showlegend=False)
                )
            ], width=6),
        ])
    ], fluid=True)
