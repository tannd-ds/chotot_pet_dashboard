"""
Dashboard for Chotot.com Pet Data 
"""
import dash
import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State, callback
from data.load_data import PetData
from visualizations.displayGraph import *


external_script = ["https://tailwindcss.com/",
                   {"src": "https://cdn.tailwindcss.com"}
                   ]

app = dash.Dash(
    __name__,
    external_scripts=external_script,
)
app.scripts.config.serve_locally = True

pet_data = PetData('./data/new_pet_30_columns.json')
df_ = pet_data.df

# Create a scatter mapbox plot
contents = list(range(7))

fig = update_map_figure(df=df_)
contents[0] = html.Div(
    children=[
        html.Div(
            "OK", className="relative p-0 rounded-xl border-2 border-slate-400/10 bg-white flex justify-between items-start overflow-hidden")
        for i in range(3)],
    className='relative grid grid-cols-3 auto-rows-[calc(100vh_/_3.5)] gap-4'
)

contents[1] = display_graph(fig=fig,
                            graph_id='map-graph',
                            show_display_mode_bar=False,
                            style="w-full h-full relative")

fig1 = update_box_figure(df=pet_data.df_types['Mèo'])
contents[2] = display_graph(fig=fig1, graph_id='box-graph')

fig3 = update_pet_breed_bar_figure(df=pet_data.get_breed_groups('Mèo'))
contents[4] = display_graph(
    fig=fig3,
    graph_id='pet-breed-bar-graph',
    show_display_mode_bar=False,
    style="w-full h-full relative"
)

filter_bar = html.Div(
    children=[
        html.Div(
            children=["Loại Thú Cưng"]
        ),
        dcc.Dropdown(
            options=pet_data.pet_types,
            id='pet-type-dropdown',
            className="min-w-[10rem]"
        ),
        dcc.RangeSlider(
            id='price-slider',
            marks={0: '0', 1: '10K', 2: '100K',
                   3: '1M', 4: '10M', 5: '100M', 6: '1B'},
            value=[0, 6],
            dots=False,
            step=0.1,
            tooltip={"placement": "bottom", "always_visible": False},
            updatemode='drag',
            allowCross=False,
            className="price-slider min-w-[30rem]",
            verticalHeight=1,
        ),
    ],
    className="flex items-center gap-4"
)

main_content = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(
                    children=[contents[i]],
                    className="w-full"
                )
            ],
            className=f'{"row-span-3" if i==1 else "row-span-1"} {"col-span-2" if i in [0, 2] else ""} {"relative p-0 rounded-xl border-2 border-slate-400/10 bg-white flex justify-center items-start overflow-hidden origin-top-left hover:overflow-visible hover:z-[99] transition-all duration-200" if i != 0 else ""}'
        ) for i in range(6)
    ],
    className='relative px-4 pt-2 grid grid-cols-3 auto-rows-[calc(100vh_/_3.5)] gap-4'
)


app.layout = html.Div(
    children=[
        dcc.Tabs(
            children=[
                dcc.Tab(
                    label="A",
                    children=[
                        html.Div(
                            children=[
                                filter_bar,
                                main_content
                            ],
                            className='h-screen flex flex-col ml-[5rem] p-4'
                        )
                    ],
                    style={
                        'margin': '0',
                        'padding': '0.5rem',
                        'width': '80%',
                        'aspect-ratio': 'square',
                        'border-radius': '0.25rem',
                        'background-color': '#57cc99',
                        'border': '0',
                        'font-weight': '900',
                    },
                    selected_style={
                        'margin': '0',
                        'padding': '0.5rem',
                        'width': '80%',
                        'aspect-ratio': 'square',
                        'border': '0',
                        'border-radius': '0.25rem',
                        'background-color': '#80ed99',
                        'font-weight': '900',

                    }
                ),
                dcc.Tab(
                    label="M",
                    children=[
                        "OK"
                    ],
                    style={
                        'margin': '0',
                        'padding': '0.5rem',
                        'width': '80%',
                        'aspect-ratio': 'square',
                        'border-radius': '0.25rem',
                        'background-color': '#57cc99',
                        'border': '0',
                        'font-weight': '900',
                    },
                    selected_style={
                        'margin': '0',
                        'padding': '0.5rem',
                        'width': '80%',
                        'aspect-ratio': 'square',
                        'border': '0',
                        'border-radius': '0.25rem',
                        'background-color': '#80ed99',
                        'font-weight': '900',

                    }
                )
            ],
            style={
                'min-width': '4rem',
                'height': '100vh',
                'padding': '1rem 0 0 0',
                'margin': '0',
                'position': 'fixed',
                'top': '0',
                'left': '0',
                'display': 'flex',
                'flex-direction': 'column',
                'background-color': '#57cc99',
                'align-items': 'center',
                'gap': '1rem'
            },
            parent_style={'display': 'flex', 'flex-direction': 'row'},
        )
    ],
    className="flex gap-2 bg-zinc-100",
)


@callback(
    [
        Output('map-graph', 'figure'),
        Output('box-graph', 'figure'),
        Output('pet-breed-bar-graph', 'figure'),
    ],
    [
        Input('pet-type-dropdown', 'value'),
        Input('price-slider', 'value'),

    ]
)
def update_map_fig(chosen_pet_type, price_range):
    # filter pet_type
    if chosen_pet_type is None:
        filtered_df = df_
    else:
        filtered_df = pet_data.df_types[chosen_pet_type]

    price_range = [p ** 10 for p in price_range]
    # filter price range
    if price_range is not None and len(price_range) == 2:
        filtered_df = filtered_df[
            (filtered_df['price'] >= price_range[0]) &
            (filtered_df['price'] <= price_range[1])
        ]

    return (
        update_map_figure(df=filtered_df),
        update_box_figure(df=filtered_df),
        update_pet_type_count_figure(df=filtered_df)
    )


if __name__ == "__main__":
    app.run_server(debug=True)
