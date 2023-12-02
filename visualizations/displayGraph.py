import dash
import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State, callback


def display_graph(fig, graph_id: str, show_display_mode_bar: bool = False, style: str = "w-full h-full relative"):
    graph = html.Div(
        children=[
            dcc.Graph(id=graph_id, figure=fig,
                      config={'displayModeBar': show_display_mode_bar}),
        ],
        className=style,
    )
    return graph


def update_map_figure(df: pd.DataFrame):
    fig = px.scatter_mapbox(df,
                            lat='latitude',
                            lon='longitude',
                            size=(df['price'] / 1000),
                            color='region_name',
                            hover_name='title',
                            zoom=5.5,
                            center=dict(lat=df['latitude'].mean() + 3,
                                        lon=df['longitude'].mean() - 1),
                            # title='Bản Đồ Phân Bố Thú Cưng Được Bán Trên Chotot.com',
                            mapbox_style="carto-positron",
                            width=540,
                            height=920,
                            )
    fig.update_layout(
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        xaxis_title="Giống Thú Cưng",
        yaxis_title="Số Lượng",
    )
    return fig


def update_box_figure(df: pd.DataFrame):
    df_filtered = df[df['price'] < 40_000_000]
    fig = px.box(df_filtered,
                 y="price",
                 x="pet_breed_name",
                 log_y=True,
                 color="pet_age_name",
                 title="<b>Phân Bố Giá theo Giống Thú Cưng</b>",
                 height=280,
                 )
    fig.update_layout(
        showlegend=False,
        margin=dict(l=70, b=50, t=30, r=50),
        xaxis_title="Giống Thú Cưng",
        yaxis_title="log(Giá)",

    )
    return fig


def update_pet_type_count_figure(df: pd.DataFrame):
    # Group by pet type and count occurrences
    pet_type_counts = df.groupby(
        'pet_type_name').size().reset_index(name='count')

    # Sort by count in descending order to find the most popular types
    pet_type_counts = pet_type_counts.sort_values(by='count', ascending=False)
    pet_type_counts.loc[4, 'pet_type_name'] = 'Khác'

    fig = px.bar(data_frame=pet_type_counts,
                 x="pet_type_name",
                 y="count",
                 color="pet_type_name",
                 title="<b>Phân Bố Các Loại Thú Cưng</b>",
                 height=280,
                 )
    fig.update_layout(
        showlegend=False,
        # margin=dict(l=32, r=16),
        margin=dict(l=70, b=50, t=30, r=50),
        xaxis_title="Giống Thú Cưng",
        yaxis_title="Số Lượng",
    )

    return fig


def update_pet_breed_bar_figure(df: pd.DataFrame, chosen_breed: None | str = None):
    fig_title = "Phân Bố Các Loại Thú Cưng"
    if chosen_breed is not None:
        fig_title = f"Phân Bố Các Loại {chosen_breed}"
    fig = px.bar(data_frame=df,
                 x=df.index,
                 y="price",
                 color=df.index,
                 title="<b>" + fig_title + "</b>",
                 height=290,
                 )
    fig.update_layout(
        showlegend=False,
        margin=dict(l=70, b=50, t=30, r=50),
        xaxis_title="Giống Thú Cưng",
        yaxis_title="Số Lượng",
    )

    return fig
