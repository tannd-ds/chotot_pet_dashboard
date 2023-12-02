import pandas as pd
import numpy as np
import json


class PetData():
    def __init__(self, input_path: str = './new_pet_30_columns.json'):
        # Create a DataFrame of all Data.
        self.df = self.from_json(input_path)
        self.pet_types = self.df['pet_type_name'].unique().tolist()

        # Create dfs for each pet_type
        self.df_types = {}
        for pet_type in self.pet_types:
            self.df_types[pet_type] = self.df[self.df['pet_type_name'] == pet_type]

    def from_json(self, input_path: str = './new_pet_30_columns.json') -> pd.DataFrame:
        """
        Return a pandas.DataFrame with data read from input_path json file.
        """
        with open(input_path, 'r', encoding='utf-8') as f:
            df = json.load(f)
        df = pd.DataFrame.from_dict(df).T

        df.dropna(subset=['price'], axis=0, how='any', inplace=True)
        df['price'] = df['price'].astype('int')

        return df

    def get_breed_groups(self, pet_type: str, ascending: bool = False):
        data = self.df_types[pet_type].groupby(['pet_breed_name'])[
            'price'].count().sort_values(ascending=ascending)
        data.index = pd.Series(data.index).apply(
            lambda x: x[len(pet_type) + 1:] if x != 'Khác' else x)
        return data

    def get_mean_price_simplified(self, pet_type: None | str = None):
        mean_price = self.df.price.mean()
        if pet_type is not None:
            mean_price = self.df_types[pet_type].price.mean()

        price_tags = ['', 'K', 'M', 'B']
        n_divided = 0

        while mean_price > 1000:
            mean_price /= 1_000
            n_divided += 1

        mean_price = f"{mean_price:.2f}{price_tags[n_divided]}"
        return mean_price

    def get_most_region(self, pet_type: None | str = None):
        df_filtered = self.df
        if pet_type is not None:
            df_filtered = self.df_types[pet_type]

        result_region = df_filtered.groupby(by='region_name') \
            .published_date.count() \
            .sort_values(ascending=False) \
            .index[0]

        if result_region == 'Tp Hồ Chí Minh':
            return 'TP.HCM'
        return result_region
