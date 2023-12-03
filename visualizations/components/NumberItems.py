from dash import html
from data.load_data import PetData


def create_number_items(data: PetData):
    number_items_contents = [
        {
            "title": len(data.df),
            "description": "Tổng Số Bài Đăng",
            "id": "n-post",
        },
        {
            "title": f"{len(data.df['pet_type_name'].unique())}",
            "description": "Số Loại Thú Cưng",
            "id": "n-pet-type"
        },
        {
            "title": data.get_mean_price_simplified(),
            "description": "Giá Trung Bình",
            "id": "mean-price"
        },
        {
            "title": data.get_most_region(),
            "description": "Khu Vực Sôi Nổi Nhất",
            "id": "most-region",
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
                            className=f"{'text-6xl' if 'is_long_text' in content else 'text-7xl'} font-bold text-[#0C356A]",
                            id=content['id'],
                        ),
                    ],
                    className="h-full px-6 py-6 flex flex-col justify-between"
                )
            ],
            className="col-span-1 w-full h-[10rem] rounded-xl border-2 border-slate-400/10 bg-white",
        ) for content in number_items_contents
    ]
