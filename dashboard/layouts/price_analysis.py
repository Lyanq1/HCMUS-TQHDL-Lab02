from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

def create_price_layout(df):
    # Segment analysis
    segment_stats = df.groupby('price_segment').agg({
        'id': 'count',
        'revenue_estimate': 'sum',
        'quantity_sold': ['sum', 'mean'],
        'rating_average': 'mean',
        'discount_pct': 'mean'
    }).reset_index()
    segment_stats.columns = ['segment', 'count', 'revenue', 'total_sold', 'avg_sold', 'avg_rating', 'avg_discount']
    segment_stats['revenue_pct'] = (segment_stats['revenue'] / segment_stats['revenue'].sum() * 100).round(1)
    segment_stats['product_pct'] = (segment_stats['count'] / segment_stats['count'].sum() * 100).round(1)

    # Price vs performance
    price_perf = df.groupby('price_segment').agg({
        'quantity_sold': 'mean',
        'review_count': 'mean'
    }).reset_index()

    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H3("Price Segment Analysis"),
                html.P("Key Insight: 0-100k segment has 55.7% of products but only 28.1% of revenue",
                       className="text-muted")
            ])
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=go.Figure(data=[
                        go.Bar(name='Products %', x=segment_stats['segment'], y=segment_stats['product_pct'], marker_color='lightblue'),
                        go.Bar(name='Revenue %', x=segment_stats['segment'], y=segment_stats['revenue_pct'], marker_color='lightgreen')
                    ]).update_layout(
                        title='Product vs Revenue Distribution by Price Segment',
                        barmode='group',
                        xaxis_title='Price Segment',
                        yaxis_title='Percentage (%)'
                    )
                )
            ], width=6),
            dbc.Col([
                dcc.Graph(
                    figure=px.bar(
                        segment_stats,
                        x='segment',
                        y='avg_sold',
                        title="Average Sales per Product by Segment",
                        labels={'segment': 'Price Segment', 'avg_sold': 'Avg Units Sold'},
                        color='avg_sold',
                        color_continuous_scale='Reds'
                    ).update_layout(showlegend=False)
                )
            ], width=6),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=px.scatter(
                        df.sample(min(5000, len(df))),
                        x='price',
                        y='quantity_sold',
                        color='price_segment',
                        title="Price vs Sales Volume (sample)",
                        labels={'price': 'Price (VND)', 'quantity_sold': 'Quantity Sold'},
                        log_x=True,
                        log_y=True
                    )
                )
            ], width=6),
            dbc.Col([
                dcc.Graph(
                    figure=px.bar(
                        price_perf,
                        x='price_segment',
                        y='review_count',
                        title="Average Reviews by Price Segment",
                        labels={'price_segment': 'Price Segment', 'review_count': 'Avg Reviews'},
                        color='review_count',
                        color_continuous_scale='Purples'
                    ).update_layout(showlegend=False)
                )
            ], width=6),
        ])
    ], fluid=True)
