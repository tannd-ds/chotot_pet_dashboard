from dash import html
from data.load_data import PetData


def create_number_items(data: PetData):
    number_items_contents = [
        {
            "title": len(data.df),
            "description": "Tổng Số Thú Cưng",
            "id": "n-post",
            "bg-color": "bg-gradient-to-tr from-[#37b7ee] to-[#86d1f3] to-80%"
        },
        {
            "title": f"{len(data.df['pet_type_name'].unique())}",
            "description": "Số Loại Thú Cưng",
            "id": "n-pet-type",
            "bg-color": "bg-gradient-to-tr from-[#40d1a6] to-[#8ADAB2] to-80%"
        },
        {
            "title": data.get_mean_price_simplified(),
            "description": "Giá Trung Bình",
            "id": "mean-price",
            "bg-color": "bg-gradient-to-tr from-[#653df4] to-[#B15EFF] to-80%",
        },
        {
            "title": data.get_most_region(),
            "description": "Khu Vực Sôi Nổi Nhất",
            "id": "most-region",
            "bg-color": "bg-gradient-to-tr from-[#3b82f5] to-[#8E8FFA] to-80%",
            "is_long_text": True,
        },
    ]

    return [
        html.Div(
            children=[
                html.Div(
                    [
                        html.Div(
                            children=[content['description']],
                            className="text-md font-bold truncate"
                        ),
                        html.Div(
                            children=[content['title']],
                            className=f"{'text-6xl' if 'is_long_text' in content else 'text-7xl'} font-bold",
                            id=content['id'],
                        ),
                    ],
                    className="h-full px-6 py-6 flex flex-col justify-between text-white"
                )
            ],
            className=f"col-span-1 w-full h-[10rem] rounded-xl {content['bg-color']}",
        ) for content in number_items_contents
    ]
