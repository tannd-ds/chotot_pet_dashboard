import pandas as pd


def create_pet_image(data: pd.DataFrame):
    sampled_url = data.sample(1).img[0]
    return sampled_url
