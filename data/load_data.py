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
        """
        Return a pandas.Series that count number of pet in each pet_breed.
        """
        data = self.df_types[pet_type].groupby(['pet_breed_name'])[
            'price'].count().sort_values(ascending=ascending)
        data.index = pd.Series(data.index).apply(
            lambda x: x[len(pet_type) + 1:] if x != 'Khác' else x)
        return data

    def get_mean_price_simplified(self, pet_type: None | str = None):
        """
        Return a number (as a string) that is simplified to 'K' 'M' or 'B'
        """
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
        """
        Return the name of the region that has the most number of pet being sold.
        """
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

    def get_options(self, col_name: str):
        if col_name not in self.df.columns:
            return [f"Can't find {col_name}"]
        return self.df[col_name].unique().tolist()

    def get_breed_from_breed_name(self, breed_name: 'str'):
        if breed_name in self.get_options('pet_breed_name'):
            result = self.df[self.df['pet_breed_name'] == breed_name]['pet_breed'] \
                .iloc[0]
            return result
        return 0

    def get_approximate_coordinate(self, ward_name: 'str'):
        if ward_name in self.get_options('ward_name'):
            longitude, latitude = self.df[self.df['ward_name'] == ward_name][['longitude', 'latitude']] \
                .iloc[0]
            return (longitude, latitude)
        return (106, 11)
