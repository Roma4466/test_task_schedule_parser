from typing import List

from pandas import DataFrame


def get_coordinates_of_column(data_frame: DataFrame, names: List[str]):
    mask = data_frame.isin(names)
    coordinates = mask.stack()[lambda x: x].index.tolist()
    if coordinates:
        return coordinates[0]
    return None
