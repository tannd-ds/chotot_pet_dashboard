from data.load_data import PetData
from dash import dcc, html, Input, Output, callback
import dash

ml_items = {
    'input-dropdown': [
        {
            'label': "Loài",
            'option_col_name': 'pet_type_name',
            'id': 'ml-type-dropdown'
        },
        {
            'label': "Giống",
            'option_col_name': 'pet_breed_name',
            'id': 'ml-breed-dropdown',
        },
        {
            'label': "Độ Tuổi",
            'option_col_name': 'pet_age_name',
            'id': 'ml-age-dropdown',
        },
        {
            'label': "Kích Cỡ",
            'option_col_name': 'pet_size_name',
            'id': 'ml-size-dropdown',
        },
        {
            'label': "Tỉnh/Thành Phố",
            'option_col_name': 'region_name',
            'id': 'ml-region-dropdown',
        },
        {
            'label': "Quận/Huyện",
            'option_col_name': 'area_name',
            'id': 'ml-area-dropdown',
        },
        {
            'label': "Xã/Thị Trấn",
            'option_col_name': 'ward_name',
            'id': 'ml-ward-dropdown',
        },
    ],
    'output': [
        {
            'id': 'decision_tree',
            'label': 'Decision Tree',
            "bg-color": "bg-gradient-to-tr from-[#37b7ee] to-[#86d1f3] to-80%"
        },
        {
            'id': 'ridge',
            'label': 'Ridge (L2)',
            "bg-color": "bg-gradient-to-tr from-[#40d1a6] to-[#8ADAB2] to-80%"
        },
        {
            'id': 'random_forest',
            'label': 'Random Forest',
            "bg-color": "bg-gradient-to-tr from-[#3b82f5] to-[#8E8FFA] to-80%",
        },
    ]
}


def create_tab_model(pet_data: PetData):

    input_dropdowns = html.Div(
        children=[
            html.Div(
                children=[
                    html.Div(
                        item['label'],
                        className="mb-2 font-bold text-center"
                    ),
                    dcc.Dropdown(
                        options=pet_data.get_options(
                            item['option_col_name']),
                        id=item['id'],
                        className="w-[10rem] lg:w-[15rem]",
                    )
                ]
            ) for item in ml_items['input-dropdown']
        ],
        className="grid grid-cols-4 gap-2 justify-center items-center"
    )

    submit_btn = html.Div(
        children=[
            html.Button(
                'Dự Đoán',
                id='ml-submit-btn',
                className="px-4 py-2 bg-gradient-to-tr from-[#37b7ee] to-[#86d1f3] to-80% rounded-md font-bold text-white",
                n_clicks=0
            ),
        ],
    )

    model_results = html.Div(
        children=[
            html.Div(
                children=[
                    html.Div(
                        output_item['label'],
                        className="font-bold text-lg"
                    ),
                    html.Div(
                        children=[],
                        id=output_item['id'],
                    )],
                className="h-full p-4 rounded-lg border-2 border-slate-400/10 bg-white",
            ) for output_item in ml_items['output']
        ],
        id="ml-output",
        className=f"grid grid-cols-{len(ml_items['output'])} auto-rows-[15rem] gap-2 justify-center items-center"
    )

    model_results = html.Div(
        children=[
            html.Div(
                children=[
                    html.Div(
                        [
                            html.Div(
                                children=[content['label']],
                                className="text-lg font-bold truncate"
                            ),
                            html.Div(
                                children=[""],
                                className=f"text-6xl font-bold",
                                id=content['id'],
                            ),
                        ],
                        className="h-full px-6 py-6 flex flex-col justify-between text-white"
                    )
                ],
                className=f"col-span-1 w-full h-full rounded-xl {content['bg-color']}",
            ) for content in ml_items['output']
        ],
        id="ml-output",
        className=f"grid grid-cols-{len(ml_items['output'])} auto-rows-[10rem] gap-2 justify-center items-center"
    )

    return (
        html.Div(
            children=[
                html.Div(
                    "Dự Đoán Giá Thú Cưng",
                    className="text-4xl font-bold text-center"
                ),
                html.Div(
                    children=[
                        input_dropdowns,
                        submit_btn,
                    ],
                    className="px-8 py-4 flex flex-col items-center gap-4 rounded-xl border-2 border-slate-400/10 bg-white"
                ),
                model_results,
            ],
            className="flex flex-col gap-4 "
        )
    )
