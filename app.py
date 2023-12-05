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
from visualizations.components.PetImage import create_pet_image
from visualizations.components.TabModel import ml_items, create_tab_model
# Models
from models.load_model import Models


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
models = Models('./models/pickles/')

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

contents[3] = html.Div(
    children=[
        html.Img(
            id='pet-img',
            className='h-full hover:h-screen hover:top-0 hover:fixed'
        )
    ],
    className='h-full',
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
            className=f'{"row-span-3" if i==1 else ""} {"col-span-2 row-span-2 min-w-[70%]" if i in [0] else ""} relative p-0 {"rounded-xl border-2 border-slate-400/10 bg-white" if i != 0 else ""} flex justify-center items-center overflow-hidden'
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
        'content': [create_tab_model(pet_data=pet_data),
                    ],
        'override_className': 'h-screen w-full p-4 flex flex-col justify-center items-center'
    }
]
app.layout = html.Div(
    children=[
        create_tabs(tab_contents=tab_contents)
    ],
    className="flex justify-start gap-2 bg-zinc-100",
)


@callback(
    [Output(output_item['id'], "children")
        for output_item in ml_items['output']
     ],
    [Input(item['id'], 'value') for item in ml_items['input-dropdown']
     ] + [Input('ml-submit-btn', 'n_clicks')],
    prevent_initial_call=True
)
def update_ml_dashboard(chosen_type, chosen_breed, chosen_age, chosen_size, chosen_region, chosen_area, chosen_ward, n_clicks):
    ctx = dash.callback_context

    if ctx.triggered_id == 'ml-submit-btn' and n_clicks > 0:
        chosen_breed_id = pet_data.get_breed_from_breed_name(chosen_breed)
        chosen_coordinate = pet_data.get_approximate_coordinate(chosen_ward)
        chosen_longitude, chosen_latitude = chosen_coordinate
        print(chosen_breed_id, chosen_coordinate)
        sample = {
            'pet_type_name': chosen_type,
            'pet_breed': chosen_breed_id,
            'pet_breed_name': chosen_breed,
            'pet_age_name': chosen_age,
            'pet_size_name': chosen_size,
            'region_name': chosen_region,
            'area_name': chosen_area,
            'ward_name': chosen_ward,
            'longtitude': chosen_longitude,
            'latitude': chosen_latitude,
        }
        result = models.predict(sample, beautiful_display=True)

        return tuple(str(v) for k, v in result.items() if k in [model['id'] for model in ml_items['output']])

    return [dash.no_update for i in range(len(ml_items['output']))]


@callback(
    [
        Output('map-graph', 'figure'),
        Output('box-graph', 'figure'),
        Output('pet-breed-bar-graph', 'figure'),
        Output('mean-price', 'children'),
        Output('n-pet-type', 'children'),
        Output('most-region', 'children'),
        Output('n-post', 'children'),
        Output('pet-img', 'src')
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
    pet_image = create_pet_image(pet_data.df)
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
        pet_image = create_pet_image(pet_data.df_types[chosen_pet_type])

    output_ = (
        map_fig,
        box_fig,
        breed_bar_fig,
        # Apply filters on number_items
        pet_data.get_mean_price_simplified(chosen_pet_type),
        n_type_number_items,
        pet_data.get_most_region(pet_type=chosen_pet_type),
        n_post,
        pet_image
    )
    return output_


if __name__ == "__main__":
    app.run_server(debug=True)
