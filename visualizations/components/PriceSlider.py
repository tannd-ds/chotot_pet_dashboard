from dash import dcc, html


def create_price_slider():
    return (
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
    )
