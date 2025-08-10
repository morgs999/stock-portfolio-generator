import os
import pandas as pd
import json


current_dir = os.path.dirname(os.path.abspath(__file__))
json_file = os.path.join(current_dir, 'stock.json')

with open(json_file, 'r') as file:
    data = json.load(file)

metadata = data.get('Meta Data', {})
time_series = data.get('Time Series (Daily)', {})

metadata_dataframe = pd.DataFrame.from_dict(metadata, orient='index')
time_series_dataframe = pd.DataFrame.from_dict(time_series, orient='index')
# print('\n ___METADATA___')
# print(metadata_dataframe)
# print('\n __TIMESERIES__')
# print(time_series_dataframe.describe())
# print(time_series_dataframe.info())
# print(time_series_dataframe)


# df = pd.read_json(json_file)
# print(df)