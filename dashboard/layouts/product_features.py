from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_features_layout(df):
    # Video impact analysis
    video_stats = df.groupby('has_video').agg({
        'quantity_sold': 'mean',
        'revenue_estimate': 'mean',
        'id': 'count'
    }).reset_index()
    video_stats.columns = ['has_video', 'avg_sold', 'avg_revenue', 'count']
    video_stats['has_video'] = video_stats['has_video'].map({True: 'With Video', False: 'No Video'})

    # Pay later impact
    paylater_stats = df.groupby('pay_later').agg({
        'quantity_sold': 'mean',
        'revenue_estimate': 'mean',
        'id': 'count'
    }).reset_index()
    paylater_stats.columns = ['pay_later', 'avg_sold', 'avg_revenue', 'count']
    paylater_stats['pay_later'] = paylater_stats['pay_later'].map({True: 'Pay Later', False: 'No Pay Later'})

    # Images vs rating (filter valid ratings)
    df_rated = df[df['rating_average'] > 0].copy()

    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H3("Product Features Analysis"),
                html.P("Impact of product features on sales performance", className="text-muted")
            ])
        ], className="mb-4"),

        # KPI Cards
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{df['has_video'].sum():,}", className="text-info"),
                        html.P("Products with Video", className="mb-0"),
                        html.Small(f"{df['has_video'].sum()/len(df)*100:.1f}% of catalog", className="text-muted")
                    ])
                ], className="h-100")
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{df['number_of_images'].mean():.1f}", className="text-warning"),
                        html.P("Avg Images per Product", className="mb-0"),
                        html.Small(f"Range: {df['number_of_images'].min()}-{df['number_of_images'].max()}", className="text-muted")
                    ])
                ], className="h-100")
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{df['pay_later'].sum():,}", className="text-success"),
                        html.P("Products with Pay Later", className="mb-0"),
                        html.Small(f"{df['pay_later'].sum()/len(df)*100:.1f}% of catalog", className="text-muted")
                    ])
                ], className="h-100")
            ], width=4),
        ], className="mb-4"),

        # Charts Row 1
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=go.Figure(data=[
                        go.Bar(name='Avg Sales', x=video_stats['has_video'],
                               y=video_stats['avg_sold'], marker_color='lightblue'),
                        go.Bar(name='Product Count', x=video_stats['has_video'],
                               y=video_stats['count']/10, marker_color='lightcoral')
                    ]).update_layout(
                        title='Video Impact on Sales (count/10 for scale)',
                        barmode='group'
                    )
                )
            ], width=6),
            dbc.Col([
                dcc.Graph(
                    figure=go.Figure(data=[
                        go.Bar(name='Avg Sales', x=paylater_stats['pay_later'],
                               y=paylater_stats['avg_sold'], marker_color='lightgreen'),
                        go.Bar(name='Product Count', x=paylater_stats['pay_later'],
                               y=paylater_stats['count']/10, marker_color='lightsalmon')
                    ]).update_layout(
                        title='Pay Later Impact on Sales (count/10 for scale)',
                        barmode='group'
                    )
                )
            ], width=6),
        ], className="mb-4"),

        # Charts Row 2
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=px.scatter(
                        df_rated.sample(min(2000, len(df_rated))),
                        x='number_of_images',
                        y='rating_average',
                        color='price_segment',
                        title='Images Count vs Rating (sample)',
                        labels={'number_of_images': 'Number of Images', 'rating_average': 'Rating'}
                    )
                )
            ], width=12),
        ])
    ], fluid=True)
