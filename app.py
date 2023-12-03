"""
Dashboard for Chotot.com Pet Data 
"""
import dash
from dash import html, Input, Output, callback
from data.load_data import PetData
from visualizations.displayGraph import *
# Custom Components
from visualizations.components.PriceSlider import create_price_slider
from visualizations.components.PetTypeDropdown import create_pet_type_dropdown
from visualizations.components.Tabs import create_tabs
from visualizations.components.NumberItems import create_number_items


external_script = [
    "https://tailwindcss.com/",
    {"src": "https://cdn.tailwindcss.com"}
]

app = dash.Dash(
    __name__,
    external_scripts=external_script,
)
app.scripts.config.serve_locally = True

FILTER_BAR_HEIGHT = '4rem'

pet_data = PetData('./data/new_pet_30_columns.json')

contents = list(range(4))


fig1 = update_type_box_figure(df=pet_data.df)
number_items = create_number_items(data=pet_data)
box_fig = [
    html.Div(
        children=[display_graph(fig=fig1, graph_id='box-graph')],
        className="col-span-full rounded-xl border-2 border-slate-400/10 bg-white overflow-hidden flex justify-center items-center"
    )
]

contents[0] = html.Div(
    children=number_items + box_fig,
    className='w-full h-full relative grid grid-cols-4 gap-4 grid-rows-[10rem_auto]'
)

fig = update_map_figure(df=pet_data.df)
contents[1] = display_graph(fig=fig,
                            graph_id='map-graph',
                            show_display_mode_bar=False)

fig3 = update_pet_breed_bar_figure(df=pet_data.get_breed_groups('Mèo'))
contents[2] = display_graph(
    fig=fig3,
    graph_id='pet-breed-bar-graph',
    show_display_mode_bar=False,
)

pet_type_dropdown = create_pet_type_dropdown(pet_data=pet_data)
slider = create_price_slider()
filter_bar = html.Div(
    children=[pet_type_dropdown, slider],
    className=f"h-[{FILTER_BAR_HEIGHT}] flex items-center gap-4"
)

main_content = html.Div(
    children=[
        html.Div(
            children=[contents[i]],
            className=f'{"row-span-3" if i==1 else ""} {"col-span-2 row-span-2" if i in [0] else ""} relative p-0 {"rounded-xl border-2 border-slate-400/10 bg-white" if i != 0 else ""} flex justify-center items-center overflow-hidden'
        ) for i in range(len(contents))
    ],
    className='relative grow grid grid-cols-3 auto-rows-auto gap-[1rem]'
)


tab_contents = [
    {
        'label': 'A',
        'content': [filter_bar, main_content],
        'override_className': 'h-screen w-full p-4 flex flex-col gap-2'
    },
    {
        'label': 'M',
        'content': ["Machine Learning"]
    }
]
app.layout = html.Div(
    children=[
        create_tabs(tab_contents=tab_contents)
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
        filtered_df = pet_data.df
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
