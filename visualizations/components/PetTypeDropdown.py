from dash import dcc, html
import pandas as pd
from data.load_data import PetData


def create_pet_type_dropdown(pet_data: pd.DataFrame) -> html.Div:
    return (
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
        )
    )
