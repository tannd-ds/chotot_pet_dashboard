"""
Dashboard for Chotot.com Pet Data 
"""
import dash
from dash import dcc, html, Input, Output, callback
from data.load_data import PetData
from visualizations.displayGraph import *


external_script = [
    "https://tailwindcss.com/",
    {"src": "https://cdn.tailwindcss.com"}
]

app = dash.Dash(
    __name__,
    external_scripts=external_script,
)
app.scripts.config.serve_locally = True

FILTER_BAR_HEIGHT = '5rem'
BENTO_BOX_HEIGHT = f'calc((100vh_-_{FILTER_BAR_HEIGHT}_-_2rem)/3)'

pet_data = PetData('./data/new_pet_30_columns.json')
df_ = pet_data.df

contents = list(range(4))

fig = update_map_figure(df=df_)
contents[1] = display_graph(fig=fig,
                            graph_id='map-graph',
                            show_display_mode_bar=False)

fig1 = update_type_box_figure(df=df_)
number_items_contents = [
    {
        "title": len(pet_data.df),
        "description": "Tổng Số Bài Đăng",
        "id": "n-post",
    },
    {
        "title": f"{len(df_['pet_type_name'].unique())}",
        "description": "Số Loại Thú Cưng",
        "id": "n-pet-type"
    },
    {
        "title": pet_data.get_mean_price_simplified(),
        "description": "Giá Trung Bình",
        "id": "mean-price"
    },
    {
        "title": pet_data.get_most_region(),
        "description": "Khu Vực Sôi Nổi Nhất",
        "id": "most-region",
        "is_long_text": True,
    },
]

number_items = contents[0] = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(
                    [
                        html.Div(
                            children=[content['description']],
                            className="text-md font-bold truncate  "
                        ),
                        html.Div(
                            children=[content['title']],
                            className=f"{'text-6xl' if 'is_long_text' in content else 'text-7xl'} font-bold text-[#0C356A]",
                            id=content['id'],
                        ),

                    ],
                    className="h-full px-6 py-6 flex flex-col justify-between"
                )
            ],
            className="col-span-1 w-full h-[10rem] rounded-xl border-2 border-slate-400/10 bg-white",
        ) for content in number_items_contents]
    + [
        html.Div(
            children=[
                display_graph(
                    fig=fig1, graph_id='box-graph')
            ],
            className="col-span-full rounded-xl border-2 border-slate-400/10 bg-white overflow-hidden flex justify-center items-center"
        )
    ],
    className='w-full h-full relative grid grid-cols-4 gap-4 grid-rows-[10rem_auto]'
)

fig3 = update_pet_breed_bar_figure(
    df=pet_data.get_breed_groups('Mèo'),
    pet_type=''
)
contents[2] = display_graph(
    fig=fig3,
    graph_id='pet-breed-bar-graph',
    show_display_mode_bar=False,
)


filter_bar = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(
                    children=["Loại Thú Cưng"]
                ),
                dcc.Dropdown(
                    options=pet_data.pet_types,
                    id='pet-type-dropdown',
                    className="min-w-[10rem]"
                ),
            ],
            className='flex items-center gap-2',
        ),
        html.Div(
            children=[
                html.Div(
                    children=["Khoảng Giá"]
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
            className='flex items-center',
        )
    ],
    className=f"h-[{FILTER_BAR_HEIGHT}] flex items-center gap-4"
)

main_content = html.Div(
    children=[
        html.Div(
            children=[contents[i]],
            className=f'{"row-span-3" if i==1 else ""} {"col-span-2 row-span-2" if i in [0] else ""} relative p-0 {"rounded-xl border-2 border-slate-400/10 bg-white" if i != 0 else ""} flex justify-center items-center overflow-hidden'
        ) for i in range(4)
    ],
    className=f'relative pt-2 grid grid-cols-3 auto-rows-[{BENTO_BOX_HEIGHT}] gap-[1rem]'
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
                            className='h-screen w-full flex flex-col p-4'
                        )
                    ],
                    style={
                        'margin': '0',
                        'padding': '0.5rem',
                        'width': '80%',
                        'aspect-ratio': 'square',
                        'border-radius': '0.25rem',
                        'background-color': '#fca311',
                        'border': 0,
                        'font-weight': '900',
                    },
                    selected_style={
                        'margin': '0',
                        'padding': '0.5rem',
                        'width': '80%',
                        'aspect-ratio': 'square',
                        'border': '0',
                        'border-radius': '0.25rem',
                        'background-color': '#fcbf49',
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
                        'background-color': '#fca311',
                        'border': 0,
                        'font-weight': '900',
                    },
                    selected_style={
                        'margin': '0',
                        'padding': '0.5rem',
                        'width': '80%',
                        'aspect-ratio': 'square',
                        'border': '0',
                        'border-radius': '0.25rem',
                        'background-color': '#fcbf49',
                        'font-weight': '900',

                    }
                )
            ],
            style={
                'width': '4rem',
                'height': '100vh',
                'padding': '1rem 0 0 0',
                'margin': '0',
                # 'position': 'fixed',
                'top': '0',
                'left': '0',
                'display': 'flex',
                'flex-direction': 'column',
                'background-color': '#fca311',
                'align-items': 'center',
                'gap': '1rem'
            },
            parent_style={'width': '100%',
                          'display': 'flex',
                          'flexDirection': 'row'},
        )
    ],
    className="flex justify-start gap-2 bg-zinc-100",
)


@callback(
    [
        Output('map-graph', 'figure'),
        Output('box-graph', 'figure'),
        Output('pet-breed-bar-graph', 'figure'),
        Output('mean-price', 'children'),
        Output('n-pet-type', 'children'),
        Output('most-region', 'children'),
        Output('n-post', 'children')
    ],
    [
        Input('pet-type-dropdown', 'value'),
        Input('price-slider', 'value'),

    ]
)
def update_dashboard(chosen_pet_type, price_range):
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

    map_fig = update_map_figure(df=filtered_df)
    box_fig = update_type_box_figure(df=filtered_df)
    breed_bar_fig = update_pet_type_count_figure(df=filtered_df)
    n_type_number_items = len(pet_data.df.pet_type_name.unique())
    n_post = len(pet_data.df)
    if chosen_pet_type is not None:
        box_fig = update_breed_box_figure(
            df=filtered_df, pet_type=chosen_pet_type)
        breed_bar_fig = update_pet_breed_bar_figure(
            df=pet_data.get_breed_groups(chosen_pet_type).head(10),
            pet_type=chosen_pet_type,
        )
        n_type_number_items = len(
            pet_data.df_types[chosen_pet_type].pet_breed_name.unique()
        )
        n_post = len(pet_data.df_types[chosen_pet_type])

    output_ = (
        map_fig,
        box_fig,
        breed_bar_fig,
        # Apply filters on number_items
        pet_data.get_mean_price_simplified(chosen_pet_type),
        n_type_number_items,
        pet_data.get_most_region(pet_type=chosen_pet_type),
        n_post
    )
    return output_


if __name__ == "__main__":
    app.run_server(debug=True)
