import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State, callback


def display_graph(fig, graph_id: str, show_display_mode_bar: bool = False, style: str = "w-full relative"):
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
                            center=dict(lat=16.0, lon=105),
                            title='<b>Bản Đồ Phân Bố Thú Cưng Được Bán Trên Chotot.com</b>',
                            mapbox_style="carto-positron",
                            height=1000,
                            )
    fig.update_layout(
        showlegend=False,
        margin=dict(l=0, b=0, t=30, r=0),
        xaxis_title="Giống Thú Cưng",
        yaxis_title="Số Lượng",
    )
    return fig


def update_type_box_figure(df: pd.DataFrame):
    fig = px.box(df,
                 y="price",
                 x="pet_type_name",
                 log_y=True,
                 color="pet_type_name",
                 title="<b>Phân Bố Giá theo Loại Thú Cưng</b>",
                 )
    fig.update_layout(
        showlegend=False,
        margin=dict(l=70, b=50, t=30, r=50),
        xaxis_title="Loại Thú Cưng",
        yaxis_title="log(Giá)",

    )
    return fig


def update_breed_box_figure(df: pd.DataFrame, pet_type: str):
    fig = px.box(df,
                 y="price",
                 x="pet_breed_name",
                 log_y=True,
                 color="pet_age_name",
                 title=f"<b>Phân Bố Giá theo Giống {pet_type}</b>",
                 )
    fig.update_layout(
        showlegend=False,
        margin=dict(l=70, b=50, t=30, r=50),
        xaxis_title=f"Giống {pet_type}",
        yaxis_title="log(Giá)",

    )
    return fig


def update_pet_type_count_figure(df: pd.DataFrame):
    # Group by pet type and count occurrences
    pet_type_counts = df.groupby('pet_type_name') \
        .size() \
        .reset_index(name='count')

    # Sort by count in descending order to find the most popular types
    pet_type_counts = pet_type_counts.sort_values(by='count', ascending=False)
    pet_type_counts.loc[4, 'pet_type_name'] = 'Khác'

    fig = px.bar(data_frame=pet_type_counts,
                 x="pet_type_name",
                 y="count",
                 text="count",
                 text_auto='.2s',
                 title="<b>Phân Bố Các Loại Thú Cưng</b>",
                 height=300,
                 )
    fig.update_traces(
        marker_color='#5272F2',
        texttemplate='<b>%{text:.2s}</b>',
        textposition='inside',
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(l=70, b=50, t=30, r=50),
        xaxis_title="Loại Thú Cưng",
        yaxis_title="Số Lượng",
    )

    return fig


def update_pet_breed_bar_figure(df: pd.DataFrame, pet_type: None | str = None):
    fig_title = "Phân Bố Các Loại Thú Cưng"
    if pet_type is not None:
        fig_title = f"Phân Bố Các Loại {pet_type}"
    fig = px.bar(data_frame=df,
                 x=df.index,
                 y="price",
                 text="price",
                 text_auto='.2s',
                 title="<b>" + fig_title + "</b>",
                 height=300,
                 )
    fig.update_traces(
        marker_color='#5272F2',
        texttemplate='<b>%{text:.2s}</b>',
        textposition='inside',
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(l=70, b=50, t=30, r=50),
        xaxis_title=f"Giống {'Thú Cưng' if pet_type is None else pet_type}",
        yaxis_title="Số Lượng",
    )

    return fig
